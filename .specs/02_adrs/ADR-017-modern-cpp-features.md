# ADR-017: Modern C++ Features Adoption Strategy

**Status:** Accepted
**Date:** 2026-01-07
**Context:** C++ Standards

---

## Context

The OmniCPP Template project uses C++23 as the standard language version. C++23 introduces many modern features that improve code quality, safety, and performance. The project needs a strategy for adopting these modern features while maintaining compatibility and code quality.

### Current State

The project uses a mix of C++ features:
- **Modern Features:** Some C++23 features used
- **Legacy Code:** Some legacy C++ code patterns
- **Inconsistent Usage:** Inconsistent use of modern features
- **No Guidelines:** No clear guidelines for feature adoption

### Issues

1. **Inconsistent Usage:** Inconsistent use of modern features
2. **Legacy Code:** Legacy C++ code patterns still present
3. **No Guidelines:** No clear guidelines for feature adoption
4. **Safety Issues:** Not using modern safety features
5. **Performance Issues:** Not using modern performance features
6. **Readability:** Code readability suffers from inconsistent usage

## Decision

Implement **modern C++ features adoption strategy** with:
1. **Feature Guidelines:** Clear guidelines for feature adoption
2. **Code Standards:** Coding standards for modern C++
3. **Linting Rules:** Linting rules for modern features
4. **Training:** Training for modern C++ features
5. **Gradual Adoption:** Gradual adoption of modern features
6. **Code Reviews:** Code reviews for modern feature usage

### 1. Modern C++ Features to Adopt

```cpp
// 1. Smart Pointers (RAII)
#include <memory>

// Use std::unique_ptr for exclusive ownership
std::unique_ptr<Engine> engine = std::make_unique<Engine>();

// Use std::shared_ptr for shared ownership
std::shared_ptr<Renderer> renderer = std::make_shared<Renderer>();

// Use std::weak_ptr for non-owning references
std::weak_ptr<Renderer> weak_renderer = renderer;

// 2. std::optional for optional values
#include <optional>

std::optional<int> find_value(const std::vector<int>& vec, int target) {
    auto it = std::find(vec.begin(), vec.end(), target);
    if (it != vec.end()) {
        return *it;
    }
    return std::nullopt;
}

// 3. std::expected for error handling
#include <expected>

std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}

// 4. std::variant for type-safe unions
#include <variant>

std::variant<int, float, std::string> value = 42;

// 5. std::string_view for string views
#include <string_view>

void process_string(std::string_view str) {
    // Process string without copying
    std::print("{}\n", str);
}

// 6. std::span for array views
#include <span>

void process_array(std::span<int> arr) {
    // Process array without copying
    for (auto& elem : arr) {
        std::print("{}\n", elem);
    }
}

// 7. std::ranges for range-based algorithms
#include <ranges>

void example_ranges() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};

    // Filter even numbers
    auto evens = numbers | std::views::filter([](int n) { return n % 2 == 0; });

    // Transform to squares
    auto squares = evens | std::views::transform([](int n) { return n * n; });

    // Print results
    for (auto n : squares) {
        std::print("{}\n", n);
    }
}

// 8. std::format for string formatting
#include <format>

void example_format() {
    std::string name = "John";
    int age = 30;
    std::string message = std::format("Name: {}, Age: {}", name, age);
    std::print("{}\n", message);
}

// 9. std::print for output
#include <print>

void example_print() {
    std::print("Hello, World!\n");
}

// 10. Concepts for template constraints
#include <concepts>

template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T add(T a, T b) {
    return a + b;
}

// 11. constexpr for compile-time computation
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

// 12. auto for type deduction
auto add_numbers(int a, int b) {
    return a + b;  // Type deduced as int
}

// 13. Range-based for loops
std::vector<int> numbers = {1, 2, 3, 4, 5};
for (auto& n : numbers) {
    std::print("{}\n", n);
}

// 14. Structured bindings
std::map<std::string, int> ages = {{"John", 30}, {"Jane", 25}};
for (const auto& [name, age] : ages) {
    std::print("{}: {}\n", name, age);
}

// 15. if constexpr for compile-time branching
template<typename T>
void process(T value) {
    if constexpr (std::is_integral_v<T>) {
        std::print("Integral: {}\n", value);
    } else if constexpr (std::is_floating_point_v<T>) {
        std::print("Floating: {}\n", value);
    }
}

// 16. std::function for function objects
#include <functional>

std::function<int(int, int)> add = [](int a, int b) { return a + b; };

// 17. Lambda expressions
auto lambda = [](int a, int b) { return a + b; };

// 18. std::move and std::forward for move semantics
std::string str1 = "Hello";
std::string str2 = std::move(str1);  // Move str1 to str2

template<typename T>
void forward_value(T&& value) {
    process(std::forward<T>(value));
}

// 19. std::chrono for time handling
#include <chrono>

auto now = std::chrono::system_clock::now();
auto duration = std::chrono::milliseconds(1000);

// 20. std::filesystem for file operations
#include <filesystem>

std::filesystem::path file_path = "data/file.txt";
if (std::filesystem::exists(file_path)) {
    std::print("File exists\n");
}
```

### 2. Coding Standards

```cpp
// include/engine/core/coding_standards.hpp
#pragma once

/**
 * @file coding_standards.hpp
 * @brief Coding standards for modern C++
 */

namespace engine {
namespace standards {

/**
 * @brief Memory management standards
 */
namespace memory {
    /**
     * @brief Use smart pointers for automatic memory management
     *
     * - Use std::unique_ptr for exclusive ownership
     * - Use std::shared_ptr for shared ownership
     * - Use std::weak_ptr for non-owning references
     * - Never use raw pointers for ownership
     */
    constexpr bool USE_SMART_POINTERS = true;

    /**
     * @brief Use RAII for resource management
     *
     * - Use RAII for all resources
     * - Use destructors for cleanup
     * - Never use manual resource management
     */
    constexpr bool USE_RAII = true;
}

/**
 * @brief Error handling standards
 */
namespace error {
    /**
     * @brief Use std::expected for error handling
     *
     * - Use std::expected for functions that can fail
     * - Use std::unexpected for errors
     * - Never use exceptions for control flow
     */
    constexpr bool USE_EXPECTED = true;

    /**
     * @brief Use std::optional for optional values
     *
     * - Use std::optional for optional return values
     * - Use std::nullopt for no value
     * - Never use sentinel values
     */
    constexpr bool USE_OPTIONAL = true;
}

/**
 * @brief String handling standards
 */
namespace string {
    /**
     * @brief Use std::string_view for string views
     *
     * - Use std::string_view for read-only strings
     * - Use std::string for owned strings
     * - Never use const char* for strings
     */
    constexpr bool USE_STRING_VIEW = true;

    /**
     * @brief Use std::format for string formatting
     *
     * - Use std::format for string formatting
     * - Never use printf-style formatting
     */
    constexpr bool USE_FORMAT = true;
}

/**
 * @brief Container standards
 */
namespace container {
    /**
     * @brief Use std::span for array views
     *
     * - Use std::span for array views
     * - Use std::vector for dynamic arrays
     * - Never use raw pointers for arrays
     */
    constexpr bool USE_SPAN = true;

    /**
     * @brief Use std::ranges for range-based algorithms
     *
     * - Use std::ranges for range-based algorithms
     * - Use std::views for range adaptors
     * - Never use iterator-based algorithms
     */
    constexpr bool USE_RANGES = true;
}

/**
 * @brief Template standards
 */
namespace template {
    /**
     * @brief Use concepts for template constraints
     *
     * - Use concepts for template constraints
     * - Use requires clauses for constraints
     * - Never use SFINAE
     */
    constexpr bool USE_CONCEPTS = true;

    /**
     * @brief Use auto for type deduction
     *
     * - Use auto for type deduction
     * - Use explicit types when needed
     * - Never use auto for clarity
     */
    constexpr bool USE_AUTO = true;
}

} // namespace standards
} // namespace engine
```

### 3. Linting Rules

```cmake
# cmake/LintTargets.cmake
# Linting rules for modern C++

# Enable clang-tidy
find_program(CLANG_TIDY clang-tidy)
if(CLANG_TIDY)
    set(CLANG_TIDY_CHECKS
        modernize-use-nullptr
        modernize-use-auto
        modernize-use-override
        modernize-use-noexcept
        modernize-use-bool-literals
        modernize-use-default-member-init
        modernize-use-using
        modernize-use-equals-default
        modernize-use-emplace
        modernize-use-transparent-functors
        modernize-use-std-print
        modernize-use-std-format
        modernize-use-std-numbers
        modernize-use-std-optional
        modernize-use-std-expected
        modernize-use-std-variant
        modernize-use-std-string-view
        modernize-use-std-span
        modernize-use-std-ranges
        modernize-use-std-concepts
        modernize-use-std-chrono
        modernize-use-std-filesystem
        modernize-use-std-smart-ptr
        modernize-use-std-unique-ptr
        modernize-use-std-shared-ptr
        modernize-use-std-weak-ptr
        modernize-use-std-make-unique
        modernize-use-std-make-shared
        modernize-use-std-allocate
        modernize-use-std-allocator-traits
        modernize-use-std-allocator-arg
        modernize-use-std-allocator-traits
        modernize-use-std-allocator-arg-traits
        modernize-use-std-allocator-arg-traits-arg
        modernize-use-std-allocator-arg-traits-arg-arg
    )

    set_target_properties(${TARGET} PROPERTIES
        CXX_CLANG_TIDY "${CLANG_TIDY}"
        CXX_CLANG_TIDY_CHECKS "${CLANG_TIDY_CHECKS}"
    )
endif()
```

### 4. Training Guide

```markdown
# Modern C++ Features Training Guide

## 1. Smart Pointers

### Why Use Smart Pointers?
- Automatic memory management
- No memory leaks
- Exception-safe
- Clear ownership semantics

### When to Use Which Smart Pointer?
- **std::unique_ptr**: Exclusive ownership
- **std::shared_ptr**: Shared ownership
- **std::weak_ptr**: Non-owning references

### Example
```cpp
// Bad: Raw pointer
Engine* engine = new Engine();
delete engine;  // Easy to forget

// Good: Smart pointer
std::unique_ptr<Engine> engine = std::make_unique<Engine>();
// Automatic cleanup
```

## 2. std::optional

### Why Use std::optional?
- Type-safe optional values
- No sentinel values needed
- Clear API

### Example
```cpp
// Bad: Sentinel value
int find_value(const std::vector<int>& vec, int target) {
    auto it = std::find(vec.begin(), vec.end(), target);
    if (it != vec.end()) {
        return *it;
    }
    return -1;  // Sentinel value
}

// Good: std::optional
std::optional<int> find_value(const std::vector<int>& vec, int target) {
    auto it = std::find(vec.begin(), vec.end(), target);
    if (it != vec.end()) {
        return *it;
    }
    return std::nullopt;
}
```

## 3. std::expected

### Why Use std::expected?
- Type-safe error handling
- No exceptions needed
- Clear API

### Example
```cpp
// Bad: Exceptions
int divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero");
    }
    return a / b;
}

// Good: std::expected
std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}
```

## 4. std::string_view

### Why Use std::string_view?
- No string copying
- Efficient string handling
- Compatible with std::string

### Example
```cpp
// Bad: String copying
void process_string(const std::string& str) {
    std::string copy = str;  // Unnecessary copy
    // Process copy
}

// Good: std::string_view
void process_string(std::string_view str) {
    // Process string without copying
}
```

## 5. std::ranges

### Why Use std::ranges?
- Composable algorithms
- Readable code
- Efficient

### Example
```cpp
// Bad: Iterator-based
std::vector<int> evens;
for (auto it = numbers.begin(); it != numbers.end(); ++it) {
    if (*it % 2 == 0) {
        evens.push_back(*it);
    }
}

// Good: std::ranges
auto evens = numbers | std::views::filter([](int n) { return n % 2 == 0; });
```

## 6. std::format

### Why Use std::format?
- Type-safe formatting
- No format string vulnerabilities
- Flexible formatting

### Example
```cpp
// Bad: printf-style
printf("Name: %s, Age: %d\n", name, age);  // Type-unsafe

// Good: std::format
std::string message = std::format("Name: {}, Age: {}", name, age);  // Type-safe
```

## 7. Concepts

### Why Use Concepts?
- Clear template constraints
- Better error messages
- Type-safe templates

### Example
```cpp
// Bad: SFINAE
template<typename T, typename = void>
struct has_size {
    static constexpr bool value = false;
};

template<typename T>
struct has_size<T, decltype(std::declval<T>().size(), void())> {
    static constexpr bool value = true;
};

// Good: Concepts
template<typename T>
concept HasSize = requires(T t) {
    { t.size() } -> std::convertible_to<std::size_t>;
};
```
```

## Consequences

### Positive

1. **Code Quality:** Improved code quality and safety
2. **Safety:** Fewer bugs and memory leaks
3. **Performance:** Better performance with modern features
4. **Readability:** More readable and maintainable code
5. **Type Safety:** Type-safe code with modern features
6. **Consistency:** Consistent use of modern features
7. **Future-Proof:** Code is future-proof

### Negative

1. **Learning Curve:** Developers need to learn modern features
2. **Compiler Support:** Some features require newer compilers
3. **Code Reviews:** More code reviews needed
4. **Training:** Training required for developers

### Neutral

1. **Documentation:** Requires documentation for modern features
2. **Testing:** Need to test modern features

## Alternatives Considered

### Alternative 1: No Modern Features

**Description:** Continue with legacy C++ code

**Pros:**
- No learning curve
- Works with older compilers

**Cons:**
- Poor code quality
- More bugs
- Poor performance
- Hard to maintain

**Rejected:** Poor code quality and maintainability

### Alternative 2: Gradual Migration

**Description:** Gradually migrate to modern features

**Pros:**
- Less disruption
- Learn gradually

**Cons:**
- Inconsistent code
- Longer migration
- More complex

**Rejected:** Inconsistent code and longer migration

### Alternative 3: External Libraries

**Description:** Use external libraries for modern features

**Pros:**
- Immediate benefits
- No code changes

**Cons:**
- External dependencies
- Licensing issues
- Maintenance burden

**Rejected:** External dependencies and maintenance burden

## Related ADRs

- [ADR-016: C++23 without modules](ADR-016-cpp23-without-modules.md)
- [ADR-018: Memory management approach (RAII, smart pointers)](ADR-018-memory-management.md)

## References

- [C++23 Features](https://en.cppreference.com/w/cpp/23)
- [Modern C++ Features](https://github.com/AnthonyCalandra/modern-cpp-features)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Effective Modern C++](https://www.oreilly.com/library/view/149190399583/effective-modern-c)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
