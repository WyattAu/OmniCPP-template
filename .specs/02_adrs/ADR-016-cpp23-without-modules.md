# ADR-016: C++23 Without Modules

**Status:** Accepted
**Date:** 2026-01-07
**Context:** C++ Standards

---

## Context

The OmniCPP Template project uses C++23 as the standard language version. C++23 introduces modules as a major feature, but module support across compilers is still inconsistent and experimental. The project needs to decide whether to use modules or stick with traditional header-based includes.

### Current State

The project uses C++23 with traditional header-based includes:
- **Header Files:** Traditional header files with `.hpp` extension
- **Include Directives:** `#include` directives for headers
- **No Modules:** No C++ modules used
- **Traditional Build:** Traditional build system

### Issues

1. **Inconsistent Support:** Module support varies across compilers
2. **Experimental:** Module support is experimental in many compilers
3. **Build Complexity:** Modules require complex build system changes
4. **Tooling:** Limited tooling support for modules
5. **Performance:** Unclear performance benefits
6. **Migration Effort:** Significant effort to migrate to modules

## Decision

**Use C++23 without modules** and continue with traditional header-based includes.

### 1. C++23 Features Without Modules

```cpp
// Use C++23 features without modules
#include <vector>
#include <string>
#include <optional>
#include <expected>
#include <print>
#include <ranges>
#include <algorithm>
#include <memory>
#include <functional>

// Use std::print for output
void example_print() {
    std::print("Hello, World!\n");
}

// Use std::expected for error handling
std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}

// Use std::optional for optional values
std::optional<int> find_value(const std::vector<int>& vec, int target) {
    auto it = std::find(vec.begin(), vec.end(), target);
    if (it != vec.end()) {
        return *it;
    }
    return std::nullopt;
}

// Use ranges for algorithms
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

// Use deducing this
template<typename T>
class Wrapper {
public:
    explicit Wrapper(T value) : value_(value) {}

    auto get_value() this {
        return value_;
    }

private:
    T value_;
};

// Use std::format for string formatting
void example_format() {
    std::string name = "John";
    int age = 30;
    std::string message = std::format("Name: {}, Age: {}", name, age);
    std::print("{}\n", message);
}
```

### 2. Header Organization

```cpp
// include/engine/core/engine.hpp
#pragma once

#include <memory>
#include <string>
#include <vector>
#include <functional>
#include <optional>
#include <expected>

namespace engine {
namespace core {

/**
 * @brief Engine class
 */
class Engine {
public:
    /**
     * @brief Constructor
     */
    Engine();

    /**
     * @brief Destructor
     */
    ~Engine();

    /**
     * @brief Initialize engine
     * @return True if successful
     */
    std::expected<bool, std::string> initialize();

    /**
     * @brief Run engine
     * @return Exit code
     */
    int run();

    /**
     * @brief Shutdown engine
     */
    void shutdown();

private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace core
} // namespace engine
```

### 3. CMake Configuration

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 4.0)
project(OmniCppTemplate
    VERSION 1.0.0
    DESCRIPTION "OmniCpp Template Project"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Disable modules
set(CMAKE_CXX_SCAN_FOR_MODULES OFF)

# Compiler flags
if(MSVC)
    add_compile_options(
        /std:c++23
        /permissive-
        /Zc:__cplusplus
    )
else()
    add_compile_options(
        -std=c++23
        -Wall
        -Wextra
        -Wpedantic
        -Werror
    )
endif()

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/include/engine
)

# Source files
set(SOURCES
    src/engine/core/engine.cpp
    src/engine/logging/logger.cpp
    src/engine/memory/memory_manager.cpp
)

# Header files
set(HEADERS
    include/engine/core/engine.hpp
    include/engine/logging/logger.hpp
    include/engine/memory/memory_manager.hpp
)

# Create library
add_library(omnicpp ${SOURCES} ${HEADERS})

# Set target properties
target_include_directories(omnicpp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Install targets
install(TARGETS omnicpp
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include
)
```

### 4. Compiler Compatibility

```cmake
# cmake/CompilerFlags.cmake
# C++23 compiler flags

if(MSVC)
    # MSVC C++23 flags
    add_compile_options(
        /std:c++23
        /permissive-
        /Zc:__cplusplus
        /EHsc
        /GR
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    # GCC C++23 flags
    add_compile_options(
        -std=c++23
        -Wall
        -Wextra
        -Wpedantic
        -Werror
        -fPIC
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    # Clang C++23 flags
    add_compile_options(
        -std=c++23
        -Wall
        -Wextra
        -Wpedantic
        -Werror
        -fPIC
    )
endif()

# Disable modules
set(CMAKE_CXX_SCAN_FOR_MODULES OFF)
```

### 5. Migration Guide

```markdown
# C++23 Migration Guide

## Why No Modules?

C++23 modules are not yet mature enough for production use:
- Inconsistent compiler support
- Experimental implementations
- Complex build system requirements
- Limited tooling support
- Unclear performance benefits

## C++23 Features to Use

### 1. std::print
```cpp
#include <print>

std::print("Hello, World!\n");
```

### 2. std::expected
```cpp
#include <expected>

std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}
```

### 3. std::optional
```cpp
#include <optional>

std::optional<int> find_value(const std::vector<int>& vec, int target);
```

### 4. Ranges
```cpp
#include <ranges>

auto evens = numbers | std::views::filter([](int n) { return n % 2 == 0; });
```

### 5. std::format
```cpp
#include <format>

std::string message = std::format("Name: {}, Age: {}", name, age);
```

### 6. Deducing This
```cpp
template<typename T>
class Wrapper {
    auto get_value() this {
        return value_;
    }
};
```

## Future Migration to Modules

When C++23 modules become mature:
1. Update compiler to latest version with stable module support
2. Refactor headers to modules
3. Update CMake configuration for modules
4. Update build system for module dependencies
5. Update tooling for module support
```

## Consequences

### Positive

1. **Stability:** Stable and well-tested approach
2. **Compatibility:** Works across all compilers
3. **Tooling:** Full tooling support
4. **Simplicity:** Simple build system
5. **Performance:** Known performance characteristics
6. **Documentation:** Extensive documentation available

### Negative

1. **No Modules:** Missing module benefits
2. **Build Times:** Slower compilation than modules
3. **Header Dependencies:** Complex header dependencies
4. **No Isolation:** No module isolation

### Neutral

1. **Future Migration:** May need to migrate to modules in the future
2. **Documentation:** Requires documentation for C++23 features

## Alternatives Considered

### Alternative 1: Use C++23 Modules

**Description:** Use C++23 modules

**Pros:**
- Faster compilation
- Better isolation
- Cleaner dependencies

**Cons:**
- Inconsistent compiler support
- Experimental implementations
- Complex build system
- Limited tooling

**Rejected:** Inconsistent support and experimental

### Alternative 2: Use C++20

**Description:** Use C++20 instead of C++23

**Pros:**
- Better compiler support
- More stable
- Better tooling

**Cons:**
- Missing C++23 features
- Less modern
- Future migration needed

**Rejected:** Missing C++23 features

### Alternative 3: Use C++17

**Description:** Use C++17 instead of C++23

**Pros:**
- Excellent compiler support
- Very stable
- Excellent tooling

**Cons:**
- Missing many modern features
- Less modern
- Significant migration needed

**Rejected:** Missing many modern features

## Related ADRs

- [ADR-017: Modern C++ features adoption strategy](ADR-017-modern-cpp-features.md)
- [ADR-018: Memory management approach (RAII, smart pointers)](ADR-018-memory-management.md)

## References

- [C++23 Standard](https://en.cppreference.com/w/cpp/23)
- [C++ Modules Status](https://en.cppreference.com/w/cpp/language/modules)
- [C++23 Features](https://en.cppreference.com/w/cpp/23)
- [CMake C++ Modules](https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
