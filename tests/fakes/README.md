# Testing Patterns: Fakes Over Mocks

## Overview

This document establishes the **Fakes Over Mocks** pattern as the preferred testing approach in this codebase.

## The Problem with Mocks

Traditional mocking frameworks (like GMock's `EXPECT_CALL().Times(1)`) create several issues:

1. **Coupling to Implementation Details**: Tests become brittle and break when internal implementation changes
2. **Overspecification**: Tests specify *how* code works, not *what* it does
3. **False Confidence**: Green tests don't mean correct behavior
4. **Maintenance Burden**: Refactoring requires updating many tests

```cpp
// ❌ BAD: Mock-based test (brittle)
TEST(UserServiceTest, CreateUser) {
    MockDatabase mock_db;
    EXPECT_CALL(mock_db, insert(_, _))
        .Times(1)
        .WillOnce(Return(true));
    EXPECT_CALL(mock_db, commit())
        .Times(1);
    
    UserService service(mock_db);
    service.createUser("Alice");
    // Test passes, but what if we batch inserts? Test breaks!
}
```

## The Solution: Fakes

**Fakes** are lightweight, in-memory implementations that provide the same behavior as real components.

```cpp
// ✅ GOOD: Fake-based test (behavior-focused)
TEST(UserServiceTest, CreateUser) {
    FakeDatabase fake_db;  // In-memory implementation
    UserService service(fake_db);
    
    auto result = service.createUser("Alice");
    
    ASSERT_TRUE(result.has_value());
    ASSERT_TRUE(fake_db.contains("Alice"));
    // Test focuses on outcome, not implementation
}
```

## Implementation Pattern

### 1. Define the Interface

```cpp
// include/engine/database/IDatabase.hpp
#pragma once

#include <string>
#include <optional>
#include <vector>
#include "engine/core/Expected.hpp"

namespace omnicpp {
namespace database {

struct User {
    std::string id;
    std::string name;
    std::string email;
};

enum class DatabaseError {
    ConnectionFailed,
    NotFound,
    DuplicateKey,
    QueryError,
};

class IDatabase {
public:
    virtual ~IDatabase() = default;
    
    // Core operations
    [[nodiscard]] virtual core::Expected<void, DatabaseError> 
    insert(std::string_view key, const User& user) = 0;
    
    [[nodiscard]] virtual core::Expected<User, DatabaseError>
    find(std::string_view key) const = 0;
    
    [[nodiscard]] virtual core::Expected<void, DatabaseError>
    remove(std::string_view key) = 0;
    
    [[nodiscard]] virtual bool contains(std::string_view key) const = 0;
    
    [[nodiscard]] virtual std::vector<User> find_all() const = 0;
    
    // Transaction support
    [[nodiscard]] virtual core::Expected<void, DatabaseError> begin_transaction() = 0;
    [[nodiscard]] virtual core::Expected<void, DatabaseError> commit() = 0;
    [[nodiscard]] virtual core::Expected<void, DatabaseError> rollback() = 0;
};

} // namespace database
} // namespace omnicpp
```

### 2. Implement the Fake

```cpp
// tests/fakes/FakeDatabase.hpp
#pragma once

#include "engine/database/IDatabase.hpp"
#include <unordered_map>
#include <vector>

namespace omnicpp {
namespace test {

/**
 * @brief In-memory fake database for testing
 * 
 * COMPLIANCE: Phase 7 - Fakes Over Mocks
 * - Provides real behavior, not stub responses
 * - Tests interaction with component, not implementation details
 * - Can be used in integration tests
 */
class FakeDatabase : public database::IDatabase {
public:
    core::Expected<void, database::DatabaseError> 
    insert(std::string_view key, const database::User& user) override {
        if (data_.contains(std::string(key))) {
            return core::make_unexpected(database::DatabaseError::DuplicateKey);
        }
        data_[std::string(key)] = user;
        return {};
    }
    
    core::Expected<database::User, database::DatabaseError>
    find(std::string_view key) const override {
        auto it = data_.find(std::string(key));
        if (it == data_.end()) {
            return core::make_unexpected(database::DatabaseError::NotFound);
        }
        return it->second;
    }
    
    core::Expected<void, database::DatabaseError>
    remove(std::string_view key) override {
        auto it = data_.find(std::string(key));
        if (it == data_.end()) {
            return core::make_unexpected(database::DatabaseError::NotFound);
        }
        data_.erase(it);
        return {};
    }
    
    bool contains(std::string_view key) const override {
        return data_.contains(std::string(key));
    }
    
    std::vector<database::User> find_all() const override {
        std::vector<database::User> result;
        result.reserve(data_.size());
        for (const auto& [_, user] : data_) {
            result.push_back(user);
        }
        return result;
    }
    
    // Transaction support (simple in-memory implementation)
    core::Expected<void, database::DatabaseError> begin_transaction() override {
        snapshot_ = data_;
        return {};
    }
    
    core::Expected<void, database::DatabaseError> commit() override {
        snapshot_.clear();
        return {};
    }
    
    core::Expected<void, database::DatabaseError> rollback() override {
        if (!snapshot_.empty()) {
            data_ = snapshot_;
            snapshot_.clear();
        }
        return {};
    }
    
    // Test helpers (not in interface)
    void clear() { data_.clear(); snapshot_.clear(); }
    std::size_t size() const { return data_.size(); }
    
private:
    std::unordered_map<std::string, database::User> data_;
    std::unordered_map<std::string, database::User> snapshot_;
};

} // namespace test
} // namespace omnicpp
```

### 3. Write Tests Using Fakes

```cpp
// tests/unit/test_user_service.cpp
#include <gtest/gtest.h>
#include "services/UserService.hpp"
#include "fakes/FakeDatabase.hpp"
#include "engine/core/DeterministicProviders.hpp"

namespace omnicpp {
namespace test {

class UserServiceTest : public ::testing::Test {
protected:
    void SetUp() override {
        fake_db_ = std::make_unique<FakeDatabase>();
        mock_time_ = std::make_unique<MockTimeProvider>();
        service_ = std::make_unique<UserService>(*fake_db_, *mock_time_);
    }
    
    std::unique_ptr<FakeDatabase> fake_db_;
    std::unique_ptr<MockTimeProvider> mock_time_;
    std::unique_ptr<UserService> service_;
};

TEST_F(UserServiceTest, CreateUser_ReturnsUserWithGeneratedId) {
    // Arrange
    std::string name = "Alice";
    std::string email = "alice@example.com";
    
    // Act
    auto result = service_->createUser(name, email);
    
    // Assert
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(result->name, name);
    EXPECT_EQ(result->email, email);
    EXPECT_FALSE(result->id.empty());
}

TEST_F(UserServiceTest, CreateUser_PersistsToDatabase) {
    // Arrange
    std::string name = "Bob";
    
    // Act
    auto result = service_->createUser(name, "bob@example.com");
    
    // Assert - Check side effects via fake
    ASSERT_TRUE(result.has_value());
    EXPECT_TRUE(fake_db_->contains(result->id));
    
    auto stored = fake_db_->find(result->id);
    ASSERT_TRUE(stored.has_value());
    EXPECT_EQ(stored->name, name);
}

TEST_F(UserServiceTest, CreateUser_DetectsDuplicateEmail) {
    // Arrange
    std::string email = "duplicate@example.com";
    auto first = service_->createUser("Alice", email);
    ASSERT_TRUE(first.has_value());
    
    // Act
    auto second = service_->createUser("Bob", email);
    
    // Assert
    EXPECT_FALSE(second.has_value());
    EXPECT_EQ(second.error(), UserServiceError::DuplicateEmail);
}

TEST_F(UserServiceTest, GetUser_WithDeterministicTime) {
    // Using mock time for deterministic testing
    mock_time_->set_unix_millis(1000000);
    
    auto result = service_->createUser("Test", "test@example.com");
    ASSERT_TRUE(result.has_value());
    
    // Verify timestamp is set correctly
    auto stored = fake_db_->find(result->id);
    ASSERT_TRUE(stored.has_value());
    EXPECT_EQ(stored->created_at, 1000000);
}

TEST_F(UserServiceTest, DeleteUser_RemovesFromDatabase) {
    // Arrange
    auto user = service_->createUser("ToDelete", "delete@example.com");
    ASSERT_TRUE(user.has_value());
    auto user_id = user->id;
    
    // Act
    auto result = service_->deleteUser(user_id);
    
    // Assert
    EXPECT_TRUE(result.has_value());
    EXPECT_FALSE(fake_db_->contains(user_id));
}

} // namespace test
} // namespace omnicpp
```

## When to Use Fakes vs Mocks

| Use Fakes | Use Mocks (Rare) |
|-----------|------------------|
| Database abstractions | External services you don't control |
| File system abstractions | Network calls with specific error codes |
| Time providers | Complex state machines with many transitions |
| Random number providers | Event handlers with specific call orders |
| Message queues | Legacy code that's difficult to fake |
| Caching layers | Performance testing (measure call counts) |

## Fake Implementation Guidelines

1. **Keep it Simple**: Fakes should be straightforward implementations
2. **Match Behavior**: Fakes should behave like real implementations
3. **Add Test Helpers**: Include methods for inspection (`contains()`, `size()`, etc.)
4. **Thread Safety**: Consider thread safety if tests run in parallel
5. **Performance**: Fakes should be fast - that's the point!

## Example Fake Collection

```
tests/
├── fakes/
│   ├── FakeDatabase.hpp
│   ├── FakeFileSystem.hpp
│   ├── FakeNetworkClient.hpp
│   ├── FakeMessageQueue.hpp
│   ├── FakeCache.hpp
│   └── README.md  (this file)
├── mocks/
│   └── MockExternalApi.hpp  (only for external services)
└── unit/
    └── test_*.cpp
```

## Integration with Deterministic Providers

Combine Fakes with `MockTimeProvider` and `MockRandomProvider` for fully deterministic tests:

```cpp
TEST_F(GameLogicTest, CriticalHit_IsDeterministic) {
    MockRandomProvider rng;
    FakeCombatLog combat_log;
    
    rng.set_next_double(0.05);  // Force a crit (< 0.1 = crit)
    
    GameLogic logic(rng, combat_log);
    auto result = logic.attack(enemy, 100);
    
    EXPECT_TRUE(result.is_critical);
    EXPECT_DOUBLE_EQ(result.damage, 200.0);  // 2x damage on crit
}
```

## References

- [Martin Fowler: TestDouble](https://martinfowler.com/bliki/TestDouble.html)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Google Test Primer on Fakes](https://google.github.io/googletest/gmock_for_dummies.html)
