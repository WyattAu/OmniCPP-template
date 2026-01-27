# ADR-018: Memory Management Approach (RAII, Smart Pointers)

**Status:** Accepted
**Date:** 2026-01-07
**Context:** C++ Standards

---

## Context

The OmniCPP Template project uses C++23 for game engine development. Memory management is critical for performance, stability, and preventing memory leaks. The project needs a consistent approach to memory management across all code.

### Current State

Memory management is inconsistent:

- **Mixed Approaches:** Mix of raw pointers and smart pointers
- **Manual Management:** Some code uses manual memory management
- **Memory Leaks:** Potential memory leaks from inconsistent approaches
- **No Guidelines:** No clear guidelines for memory management
- **Performance Issues:** Inefficient memory usage patterns

### Issues

1. **Memory Leaks:** Potential memory leaks from inconsistent approaches
2. **Performance Issues:** Inefficient memory usage patterns
3. **No Guidelines:** No clear guidelines for memory management
4. **Safety Issues:** Unsafe memory access patterns
5. **Maintenance:** Difficult to maintain inconsistent code
6. **Debugging:** Difficult to debug memory issues

## Decision

Implement **RAII and smart pointer-based memory management** with:

1. **RAII Principle:** Use RAII for all resource management
2. **Smart Pointers:** Use smart pointers for all dynamic memory
3. **No Raw Pointers:** Eliminate raw pointers for ownership
4. **Move Semantics:** Use move semantics for efficiency
5. **Custom Allocators:** Use custom allocators for performance
6. **Memory Pooling:** Use memory pooling for performance

### 1. RAII Principles

```cpp
// include/engine/memory/raii.hpp
#pragma once

#include <memory>
#include <functional>
#include <utility>

namespace engine {
namespace memory {

/**
 * @brief RAII wrapper for resources
 */
template<typename T, typename Deleter = std::default_delete<T>>
class RAIIWrapper {
public:
    /**
     * @brief Constructor
     * @param resource Resource to manage
     * @param deleter Deleter function
     */
    explicit RAIIWrapper(
        T* resource,
        Deleter deleter = Deleter()
    ) : resource_(resource), deleter_(std::move(deleter)) {}

    /**
     * @brief Destructor
     */
    ~RAIIWrapper() {
        if (resource_) {
            deleter_(resource_);
        }
    }

    /**
     * @brief Move constructor
     */
    RAIIWrapper(RAIIWrapper&& other) noexcept
        : resource_(other.resource_), deleter_(std::move(other.deleter_)) {
        other.resource_ = nullptr;
    }

    /**
     * @brief Move assignment
     */
    RAIIWrapper& operator=(RAIIWrapper&& other) noexcept {
        if (this != &other) {
            if (resource_) {
                deleter_(resource_);
            }
            resource_ = other.resource_;
            deleter_ = std::move(other.deleter_);
            other.resource_ = nullptr;
        }
        return *this;
    }

    /**
     * @brief Delete copy constructor
     */
    RAIIWrapper(const RAIIWrapper&) = delete;

    /**
     * @brief Delete copy assignment
     */
    RAIIWrapper& operator=(const RAIIWrapper&) = delete;

    /**
     * @brief Get resource
     * @return Resource pointer
     */
    T* get() const { return resource_; }

    /**
     * @brief Get resource
     * @return Resource pointer
     */
    T* operator->() const { return resource_; }

    /**
     * @brief Dereference resource
     * @return Resource reference
     */
    T& operator*() const { return *resource_; }

    /**
     * @brief Release resource
     * @return Resource pointer
     */
    T* release() {
        T* resource = resource_;
        resource_ = nullptr;
        return resource;
    }

    /**
     * @brief Reset resource
     * @param resource New resource
     */
    void reset(T* resource = nullptr) {
        if (resource_) {
            deleter_(resource_);
        }
        resource_ = resource;
    }

private:
    T* resource_;
    Deleter deleter_;
};

/**
 * @brief RAII wrapper for file handles
 */
class FileHandle {
public:
    /**
     * @brief Constructor
     * @param file File handle
     */
    explicit FileHandle(FILE* file) : file_(file) {}

    /**
     * @brief Destructor
     */
    ~FileHandle() {
        if (file_) {
            std::fclose(file_);
        }
    }

    /**
     * @brief Get file handle
     * @return File handle
     */
    FILE* get() const { return file_; }

private:
    FILE* file_;
};

} // namespace memory
} // namespace engine
```

### 2. Smart Pointer Guidelines

```cpp
// include/engine/memory/smart_pointers.hpp
#pragma once

#include <memory>
#include <vector>
#include <string>

namespace engine {
namespace memory {

/**
 * @brief Smart pointer guidelines
 */
namespace guidelines {
    /**
     * @brief Use std::unique_ptr for exclusive ownership
     *
     * - Use when only one owner exists
     * - Use std::make_unique for creation
     * - Never use raw pointers for ownership
     */
    constexpr bool USE_UNIQUE_PTR = true;

    /**
     * @brief Use std::shared_ptr for shared ownership
     *
     * - Use when multiple owners exist
     * - Use std::make_shared for creation
     * - Use std::weak_ptr for non-owning references
     */
    constexpr bool USE_SHARED_PTR = true;

    /**
     * @brief Use std::weak_ptr for non-owning references
     *
     * - Use for observing shared_ptr
     * - Never use for ownership
     * - Always lock before use
     */
    constexpr bool USE_WEAK_PTR = true;

    /**
     * @brief Never use raw pointers for ownership
     *
     * - Raw pointers only for non-owning references
     * - Document ownership semantics
     * - Use const for non-owning references
     */
    constexpr bool NO_RAW_POINTERS = true;
}

/**
 * @brief Smart pointer factory
 */
class SmartPointerFactory {
public:
    /**
     * @brief Create unique_ptr
     * @tparam T Type to create
     * @tparam Args Constructor argument types
     * @param args Constructor arguments
     * @return unique_ptr
     */
    template<typename T, typename... Args>
    static std::unique_ptr<T> make_unique(Args&&... args) {
        return std::make_unique<T>(std::forward<Args>(args)...);
    }

    /**
     * @brief Create shared_ptr
     * @tparam T Type to create
     * @tparam Args Constructor argument types
     * @param args Constructor arguments
     * @return shared_ptr
     */
    template<typename T, typename... Args>
    static std::shared_ptr<T> make_shared(Args&&... args) {
        return std::make_shared<T>(std::forward<Args>(args)...);
    }

    /**
     * @brief Create vector of unique_ptrs
     * @tparam T Type to create
     * @param count Number of elements
     * @return vector of unique_ptrs
     */
    template<typename T>
    static std::vector<std::unique_ptr<T>> make_unique_vector(size_t count) {
        std::vector<std::unique_ptr<T>> vec;
        vec.reserve(count);
        for (size_t i = 0; i < count; ++i) {
            vec.push_back(std::make_unique<T>());
        }
        return vec;
    }
};

} // namespace memory
} // namespace engine
```

### 3. Memory Pool

```cpp
// include/engine/memory/memory_pool.hpp
#pragma once

#include <memory>
#include <vector>
#include <stack>
#include <mutex>

namespace engine {
namespace memory {

/**
 * @brief Memory pool for efficient allocation
 */
template<typename T, size_t PoolSize = 1024>
class MemoryPool {
public:
    /**
     * @brief Constructor
     */
    MemoryPool() {
        // Pre-allocate pool
        pool_.reserve(PoolSize);
        for (size_t i = 0; i < PoolSize; ++i) {
            pool_.push_back(std::make_unique<T>());
            available_.push(i);
        }
    }

    /**
     * @brief Allocate object from pool
     * @return Pointer to allocated object
     */
    std::unique_ptr<T, PoolDeleter> allocate() {
        std::lock_guard<std::mutex> lock(mutex_);

        if (available_.empty()) {
            // Pool exhausted, allocate new object
            return std::unique_ptr<T, PoolDeleter>(
                new T(),
                PoolDeleter(this)
            );
        }

        // Get index from available stack
        size_t index = available_.top();
        available_.pop();

        // Return pointer with custom deleter
        return std::unique_ptr<T, PoolDeleter>(
            pool_[index].get(),
            PoolDeleter(this, index)
        );
    }

    /**
     * @brief Get pool size
     * @return Pool size
     */
    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return pool_.size();
    }

    /**
     * @brief Get available count
     * @return Available count
     */
    size_t available() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return available_.size();
    }

private:
    /**
     * @brief Custom deleter for pool objects
     */
    struct PoolDeleter {
        MemoryPool* pool;
        size_t index;

        PoolDeleter() : pool(nullptr), index(0) {}
        PoolDeleter(MemoryPool* p, size_t i) : pool(p), index(i) {}

        void operator()(T* ptr) {
            if (pool) {
                std::lock_guard<std::mutex> lock(pool->mutex_);
                pool->available_.push(index);
            }
        }
    };

    std::vector<std::unique_ptr<T>> pool_;
    std::stack<size_t> available_;
    mutable std::mutex mutex_;
};

} // namespace memory
} // namespace engine
```

### 4. Usage Examples

```cpp
// Example 1: RAII for file handles
#include "engine/memory/raii.hpp"

void example_raii() {
    // RAII automatically closes file
    FileHandle file(std::fopen("data.txt", "r"));

    if (file.get()) {
        // Use file
        std::fscanf(file.get(), "%s", buffer);
    }
    // File automatically closed when file goes out of scope
}

// Example 2: Smart pointers
#include "engine/memory/smart_pointers.hpp"

void example_smart_pointers() {
    // Use unique_ptr for exclusive ownership
    std::unique_ptr<Engine> engine = SmartPointerFactory::make_unique<Engine>();

    // Use shared_ptr for shared ownership
    std::shared_ptr<Renderer> renderer = SmartPointerFactory::make_shared<Renderer>();

    // Use weak_ptr for non-owning references
    std::weak_ptr<Renderer> weak_renderer = renderer;

    // Lock weak_ptr before use
    if (auto locked = weak_renderer.lock()) {
        locked->render();
    }
}

// Example 3: Memory pool
#include "engine/memory/memory_pool.hpp"

void example_memory_pool() {
    // Create memory pool
    MemoryPool<Entity, 1024> pool;

    // Allocate from pool
    auto entity1 = pool.allocate();
    auto entity2 = pool.allocate();

    // Use entities
    entity1->update();
    entity2->update();

    // Entities automatically returned to pool when destroyed
}

// Example 4: Move semantics
void example_move_semantics() {
    // Use move semantics for efficiency
    std::vector<std::unique_ptr<Entity>> entities;

    // Move instead of copy
    entities.push_back(std::move(entity1));
    entities.push_back(std::move(entity2));

    // Use std::move for function arguments
    process_entity(std::move(entity3));
}

// Example 5: Custom allocator
template<typename T>
using PoolAllocator = std::allocator<T>;

void example_custom_allocator() {
    // Use custom allocator for performance
    std::vector<Entity, PoolAllocator<Entity>> entities;

    // Reserve capacity for efficiency
    entities.reserve(1000);

    // Add entities
    for (int i = 0; i < 1000; ++i) {
        entities.emplace_back();
    }
}
```

### 5. Memory Management Guidelines

````markdown
# Memory Management Guidelines

## 1. RAII Principles

### What is RAII?

- Resource Acquisition Is Initialization
- Resources acquired in constructor
- Resources released in destructor
- Exception-safe

### When to Use RAII?

- All resource management
- File handles
- Network sockets
- Database connections
- Mutex locks

### Example

```cpp
// Bad: Manual resource management
FILE* file = std::fopen("data.txt", "r");
if (file) {
    // Use file
    std::fscanf(file, "%s", buffer);
    std::fclose(file);  // Easy to forget
}

// Good: RAII
FileHandle file(std::fopen("data.txt", "r"));
if (file.get()) {
    // Use file
    std::fscanf(file.get(), "%s", buffer);
}
// File automatically closed
```
````

## 2. Smart Pointers

### When to Use unique_ptr?

- Exclusive ownership
- Single owner
- No sharing needed

### When to Use shared_ptr?

- Shared ownership
- Multiple owners
- Reference counting needed

### When to Use weak_ptr?

- Non-owning references
- Observing shared_ptr
- Breaking cycles

### Example

```cpp
// Bad: Raw pointer ownership
Engine* engine = new Engine();
delete engine;  // Easy to forget

// Good: unique_ptr
std::unique_ptr<Engine> engine = std::make_unique<Engine>();
// Automatic cleanup
```

## 3. Move Semantics

### When to Use Move Semantics?

- Large objects
- Temporary objects
- Function returns
- Container operations

### Example

```cpp
// Bad: Copy semantics
std::vector<Entity> entities;
entities.push_back(entity1);  // Copy

// Good: Move semantics
std::vector<std::unique_ptr<Entity>> entities;
entities.push_back(std::move(entity1));  // Move
```

## 4. Memory Pooling

### When to Use Memory Pooling?

- Many small allocations
- Frequent allocations/deallocations
- Performance-critical code

### Example

```cpp
// Bad: Individual allocations
for (int i = 0; i < 1000; ++i) {
    entities.push_back(std::make_unique<Entity>());
}

// Good: Memory pool
MemoryPool<Entity, 1024> pool;
for (int i = 0; i < 1000; ++i) {
    entities.push_back(pool.allocate());
}
```

## 5. Custom Allocators

### When to Use Custom Allocators?

- Performance-critical code
- Specific allocation patterns
- Memory fragmentation issues

### Example

```cpp
// Bad: Default allocator
std::vector<Entity> entities;

// Good: Custom allocator
std::vector<Entity, PoolAllocator<Entity>> entities;
```

```

## Consequences

### Positive

1. **No Memory Leaks:** Automatic memory management prevents leaks
2. **Exception Safety:** RAII provides exception safety
3. **Performance:** Efficient memory usage patterns
4. **Safety:** Safe memory access patterns
5. **Maintainability:** Easier to maintain consistent code
6. **Debugging:** Easier to debug memory issues
7. **Clear Ownership:** Clear ownership semantics

### Negative

1. **Learning Curve:** Developers need to learn RAII and smart pointers
2. **Overhead:** Slight overhead from smart pointers
3. **Complexity:** More complex than raw pointers
4. **Performance:** Some performance overhead from reference counting

### Neutral

1. **Documentation:** Requires documentation for memory management
2. **Testing:** Need to test memory management

## Alternatives Considered

### Alternative 1: Manual Memory Management

**Description:** Use manual memory management with raw pointers

**Pros:**
- No overhead
- Simple to understand
- Full control

**Cons:**
- Memory leaks
- Exception unsafe
- Difficult to maintain
- Safety issues

**Rejected:** Memory leaks and safety issues

### Alternative 2: Garbage Collection

**Description:** Use garbage collection

**Pros:**
- Automatic memory management
- No manual cleanup

**Cons:**
- Performance overhead
- Non-deterministic
- Not suitable for game engines
- Limited control

**Rejected:** Performance overhead and not suitable for game engines

### Alternative 3: Reference Counting

**Description:** Use manual reference counting

**Pros:**
- Shared ownership
- Automatic cleanup

**Cons:**
- Manual management
- Error-prone
- Cyclic references
- Performance overhead

**Rejected:** Manual management and error-prone

## Related ADRs

- [ADR-016: C++23 without modules](ADR-016-cpp23-without-modules.md)
- [ADR-017: Modern C++ features adoption strategy](ADR-017-modern-cpp-features.md)

## References

- [RAII Wikipedia](https://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization)
- [Smart Pointers](https://en.cppreference.com/w/cpp/memory)
- [C++ Memory Management](https://www.learncpp.com/cpp-programming/memory-management/)
- [Effective C++](https://www.aristeia.com/BOOKS/EFFECTIVE_CPP.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
```
