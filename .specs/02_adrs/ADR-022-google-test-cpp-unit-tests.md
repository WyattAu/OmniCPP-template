# ADR-022: Google Test for C++ Unit Tests

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Testing

---

## Context

The OmniCPP Template project requires a robust testing framework for C++ code. Unit testing is critical for code quality and maintainability. The coding standards (`.specs/01_standards/coding_standards.md`) specify the need for comprehensive testing.

### Current State

C++ testing is inconsistent:
- **No Framework:** No consistent testing framework
- **No Coverage:** No code coverage tracking
- **No Integration:** No integration with build system
- **No CI/CD:** No CI/CD integration
- **No Reporting:** No test reporting

### Issues

1. **No Framework:** No consistent testing framework
2. **No Coverage:** No code coverage tracking
3. **No Integration:** No integration with build system
4. **No CI/CD:** No CI/CD integration
5. **No Reporting:** No test reporting
6. **No Standards:** No testing standards

## Decision

Implement **Google Test** for C++ unit tests with:
1. **Google Test Framework:** Use Google Test for unit testing
2. **Google Mock:** Use Google Mock for mocking
3. **CMake Integration:** Integrate with CMake build system
4. **Code Coverage:** Track code coverage with gcov/lcov
5. **Test Organization:** Organize tests by module
6. **Test Naming:** Follow consistent test naming conventions
7. **Test Documentation:** Document all tests

### 1. Google Test Integration

```cmake
# cmake/Testing.cmake
# Google Test integration for C++ testing

include(FetchContent)

# Find Google Test
find_package(GTest QUIET)

if(NOT GTest_FOUND)
    # Fetch Google Test if not found
    message(STATUS "Fetching Google Test...")

    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.14.0
        GIT_SHALLOW TRUE
    )

    # For Windows: Prevent overriding parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

    FetchContent_MakeAvailable(googletest)

    # Create GTest::gtest and GTest::gtest_main targets
    add_library(GTest::gtest ALIAS gtest)
    add_library(GTest::gtest_main ALIAS gtest_main)
    add_library(GTest::gmock ALIAS gmock)
    add_library(GTest::gmock_main ALIAS gmock_main)
endif()

# Enable testing
enable_testing()

# Function to add test
function(omni_add_test test_name)
    cmake_parse_arguments(
        PARSED_ARGS
        ""
        "SOURCE;WORKING_DIRECTORY"
        "LINK_LIBRARIES;COMPILE_DEFINITIONS;COMPILE_OPTIONS"
        ${ARGN}
    )

    # Create test executable
    add_executable(${test_name} ${PARSED_ARGS_SOURCE})

    # Link Google Test
    target_link_libraries(${test_name}
        PRIVATE
        GTest::gtest
        GTest::gtest_main
        ${PARSED_ARGS_LINK_LIBRARIES}
    )

    # Add compile definitions
    if(PARSED_ARGS_COMPILE_DEFINITIONS)
        target_compile_definitions(${test_name}
            PRIVATE
            ${PARSED_ARGS_COMPILE_DEFINITIONS}
        )
    endif()

    # Add compile options
    if(PARSED_ARGS_COMPILE_OPTIONS)
        target_compile_options(${test_name}
            PRIVATE
            ${PARSED_ARGS_COMPILE_OPTIONS}
        )
    endif()

    # Add test
    add_test(
        NAME ${test_name}
        COMMAND ${test_name}
        WORKING_DIRECTORY ${PARSED_ARGS_WORKING_DIRECTORY}
    )

    # Set test properties
    set_tests_properties(${test_name} PROPERTIES
        LABELS "unit"
        TIMEOUT 300
    )
endfunction()

# Function to add test suite
function(omni_add_test_suite suite_name)
    cmake_parse_arguments(
        PARSED_ARGS
        ""
        "WORKING_DIRECTORY"
        "TESTS;LINK_LIBRARIES"
        ${ARGN}
    )

    # Create test suite executable
    add_executable(${suite_name})

    # Add test sources
    target_sources(${suite_name}
        PRIVATE
        ${PARSED_ARGS_TESTS}
    )

    # Link Google Test
    target_link_libraries(${suite_name}
        PRIVATE
        GTest::gtest
        GTest::gtest_main
        ${PARSED_ARGS_LINK_LIBRARIES}
    )

    # Add test suite
    add_test(
        NAME ${suite_name}
        COMMAND ${suite_name}
        WORKING_DIRECTORY ${PARSED_ARGS_WORKING_DIRECTORY}
    )

    # Set test properties
    set_tests_properties(${suite_name} PROPERTIES
        LABELS "suite"
        TIMEOUT 600
    )
endfunction()

# Function to add test with coverage
function(omni_add_test_with_coverage test_name)
    cmake_parse_arguments(
        PARSED_ARGS
        ""
        "SOURCE;WORKING_DIRECTORY"
        "LINK_LIBRARIES;COMPILE_DEFINITIONS;COMPILE_OPTIONS"
        ${ARGN}
    )

    # Create test executable
    add_executable(${test_name} ${PARSED_ARGS_SOURCE})

    # Link Google Test
    target_link_libraries(${test_name}
        PRIVATE
        GTest::gtest
        GTest::gtest_main
        ${PARSED_ARGS_LINK_LIBRARIES}
    )

    # Add compile definitions
    if(PARSED_ARGS_COMPILE_DEFINITIONS)
        target_compile_definitions(${test_name}
            PRIVATE
            ${PARSED_ARGS_COMPILE_DEFINITIONS}
        )
    endif()

    # Add compile options
    if(PARSED_ARGS_COMPILE_OPTIONS)
        target_compile_options(${test_name}
            PRIVATE
            ${PARSED_ARGS_COMPILE_OPTIONS}
        )
    endif()

    # Enable coverage
    if(CMAKE_BUILD_TYPE STREQUAL "Debug" OR CMAKE_BUILD_TYPE STREQUAL "Coverage")
        target_compile_options(${test_name}
            PRIVATE
            $<$<CXX_COMPILER_ID:GNU,Clang>:-fprofile-arcs>
            $<$<CXX_COMPILER_ID:GNU,Clang>:-ftest-coverage>
        )
        target_link_options(${test_name}
            PRIVATE
            $<$<CXX_COMPILER_ID:GNU,Clang>:-fprofile-arcs>
        )
    endif()

    # Add test
    add_test(
        NAME ${test_name}
        COMMAND ${test_name}
        WORKING_DIRECTORY ${PARSED_ARGS_WORKING_DIRECTORY}
    )

    # Set test properties
    set_tests_properties(${test_name} PROPERTIES
        LABELS "unit;coverage"
        TIMEOUT 300
    )
endfunction()
```

### 2. Test Organization

```cpp
// tests/unit/math/test_vec3.cpp
// Vec3 unit tests

#include <gtest/gtest.h>
#include <engine/math/Vec3.hpp>

namespace engine::math::test {

// Test fixture for Vec3
class Vec3Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
        vec1 = Vec3(1.0f, 2.0f, 3.0f);
        vec2 = Vec3(4.0f, 5.0f, 6.0f);
    }

    void TearDown() override {
        // Teardown code
    }

    Vec3 vec1;
    Vec3 vec2;
};

// Test default constructor
TEST_F(Vec3Test, DefaultConstructor) {
    Vec3 vec;
    EXPECT_FLOAT_EQ(vec.x, 0.0f);
    EXPECT_FLOAT_EQ(vec.y, 0.0f);
    EXPECT_FLOAT_EQ(vec.z, 0.0f);
}

// Test parameterized constructor
TEST_F(Vec3Test, ParameterizedConstructor) {
    Vec3 vec(1.0f, 2.0f, 3.0f);
    EXPECT_FLOAT_EQ(vec.x, 1.0f);
    EXPECT_FLOAT_EQ(vec.y, 2.0f);
    EXPECT_FLOAT_EQ(vec.z, 3.0f);
}

// Test addition
TEST_F(Vec3Test, Addition) {
    Vec3 result = vec1 + vec2;
    EXPECT_FLOAT_EQ(result.x, 5.0f);
    EXPECT_FLOAT_EQ(result.y, 7.0f);
    EXPECT_FLOAT_EQ(result.z, 9.0f);
}

// Test subtraction
TEST_F(Vec3Test, Subtraction) {
    Vec3 result = vec2 - vec1;
    EXPECT_FLOAT_EQ(result.x, 3.0f);
    EXPECT_FLOAT_EQ(result.y, 3.0f);
    EXPECT_FLOAT_EQ(result.z, 3.0f);
}

// Test scalar multiplication
TEST_F(Vec3Test, ScalarMultiplication) {
    Vec3 result = vec1 * 2.0f;
    EXPECT_FLOAT_EQ(result.x, 2.0f);
    EXPECT_FLOAT_EQ(result.y, 4.0f);
    EXPECT_FLOAT_EQ(result.z, 6.0f);
}

// Test dot product
TEST_F(Vec3Test, DotProduct) {
    float result = vec1.dot(vec2);
    EXPECT_FLOAT_EQ(result, 32.0f);
}

// Test cross product
TEST_F(Vec3Test, CrossProduct) {
    Vec3 result = vec1.cross(vec2);
    EXPECT_FLOAT_EQ(result.x, -3.0f);
    EXPECT_FLOAT_EQ(result.y, 6.0f);
    EXPECT_FLOAT_EQ(result.z, -3.0f);
}

// Test magnitude
TEST_F(Vec3Test, Magnitude) {
    float result = vec1.magnitude();
    EXPECT_FLOAT_EQ(result, std::sqrt(14.0f));
}

// Test normalization
TEST_F(Vec3Test, Normalization) {
    Vec3 result = vec1.normalized();
    float magnitude = result.magnitude();
    EXPECT_FLOAT_EQ(magnitude, 1.0f);
}

// Test equality
TEST_F(Vec3Test, Equality) {
    Vec3 vec3(1.0f, 2.0f, 3.0f);
    EXPECT_TRUE(vec1 == vec3);
    EXPECT_FALSE(vec1 == vec2);
}

// Test inequality
TEST_F(Vec3Test, Inequality) {
    EXPECT_TRUE(vec1 != vec2);
    EXPECT_FALSE(vec1 != vec1);
}

} // namespace engine::math::test
```

### 3. Test Naming Conventions

```cpp
// Test naming conventions

// 1. Test fixture name: <ClassName>Test
class Vec3Test : public ::testing::Test {};

// 2. Test name: <Feature><Behavior>
TEST_F(Vec3Test, DefaultConstructor) {}
TEST_F(Vec3Test, ParameterizedConstructor) {}
TEST_F(Vec3Test, Addition) {}
TEST_F(Vec3Test, Subtraction) {}

// 3. Parameterized test: <Feature><Behavior><Parameter>
class Vec3ParameterizedTest : public ::testing::TestWithParam<float> {};

TEST_P(Vec3ParameterizedTest, ScalarMultiplication) {
    Vec3 vec(1.0f, 2.0f, 3.0f);
    Vec3 result = vec * GetParam();
    EXPECT_FLOAT_EQ(result.x, 1.0f * GetParam());
    EXPECT_FLOAT_EQ(result.y, 2.0f * GetParam());
    EXPECT_FLOAT_EQ(result.z, 3.0f * GetParam());
}

INSTANTIATE_TEST_SUITE_P(
    ScalarValues,
    Vec3ParameterizedTest,
    ::testing::Values(0.0f, 1.0f, 2.0f, -1.0f)
);

// 4. Typed test: <Feature><Behavior><Type>
template<typename T>
class Vec3TypedTest : public ::testing::Test {};

using Vec3Types = ::testing::Types<float, double>;
TYPED_TEST_SUITE(Vec3TypedTest, Vec3Types);

TYPED_TEST(Vec3TypedTest, DefaultConstructor) {
    Vec3<TypeParam> vec;
    EXPECT_EQ(vec.x, TypeParam(0));
    EXPECT_EQ(vec.y, TypeParam(0));
    EXPECT_EQ(vec.z, TypeParam(0));
}
```

### 4. Test Documentation

```cpp
// tests/unit/math/test_vec3.cpp
// Vec3 unit tests
//
// This file contains unit tests for the Vec3 class.
//
// Test Coverage:
// - Constructors (default, parameterized, copy)
// - Arithmetic operations (addition, subtraction, multiplication, division)
// - Vector operations (dot product, cross product, magnitude, normalization)
// - Comparison operations (equality, inequality)
//
// Test Organization:
// - Test fixture: Vec3Test
// - Test naming: <Feature><Behavior>
// - Test documentation: Each test has a descriptive name and comments
//
// Dependencies:
// - Google Test framework
// - Vec3 class
//
// Author: OmniCpp Team
// Date: 2026-01-07
```

### 5. CMakeLists.txt for Tests

```cmake
# tests/CMakeLists.txt
# CMakeLists.txt for tests

# Include testing configuration
include(${CMAKE_SOURCE_DIR}/cmake/Testing.cmake)

# Add test subdirectories
add_subdirectory(unit)
add_subdirectory(integration)

# Add test suite
omni_add_test_suite(omni_tests
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    LINK_LIBRARIES
        OmniCppLib
    TESTS
        unit/math/test_vec3.cpp
        unit/math/test_mat4.cpp
        unit/core/test_engine.cpp
        unit/ecs/test_entity.cpp
        unit/ecs/test_component.cpp
        unit/ecs/test_system.cpp
)

# Add coverage target
if(CMAKE_BUILD_TYPE STREQUAL "Coverage")
    add_custom_target(coverage
        COMMAND lcov --capture --directory . --output-file coverage.info
        COMMAND lcov --remove coverage.info '/usr/*' --output-file coverage.info
        COMMAND lcov --list coverage.info
        COMMAND genhtml coverage.info --output-directory coverage_html
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Generating code coverage report"
    )
endif()
```

### 6. Usage Examples

```cmake
# Example: Add a test
omni_add_test(test_vec3
    SOURCE tests/unit/math/test_vec3.cpp
    LINK_LIBRARIES
        OmniCppLib
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Example: Add a test with coverage
omni_add_test_with_coverage(test_vec3_coverage
    SOURCE tests/unit/math/test_vec3.cpp
    LINK_LIBRARIES
        OmniCppLib
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Example: Add a test suite
omni_add_test_suite(math_tests
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    LINK_LIBRARIES
        OmniCppLib
    TESTS
        tests/unit/math/test_vec3.cpp
        tests/unit/math/test_mat4.cpp
)
```

## Consequences

### Positive

1. **Framework:** Consistent testing framework
2. **Coverage:** Code coverage tracking
3. **Integration:** Integration with build system
4. **CI/CD:** CI/CD integration
5. **Reporting:** Test reporting
6. **Standards:** Testing standards
7. **Documentation:** Test documentation
8. **Mocking:** Google Mock for mocking

### Negative

1. **Complexity:** More complex than no testing
2. **Build Time:** Tests add build time
3. **Maintenance:** Tests need to be maintained
4. **Learning Curve:** Learning curve for Google Test

### Neutral

1. **Documentation:** Requires documentation for testing
2. **Training:** Need to train developers on Google Test

## Alternatives Considered

### Alternative 1: No Testing Framework

**Description:** No testing framework

**Pros:**
- Simpler implementation
- No build time overhead

**Cons:**
- No consistent testing
- No code coverage
- No CI/CD integration

**Rejected:** No consistent testing and no code coverage

### Alternative 2: Catch2

**Description:** Use Catch2 for testing

**Pros:**
- Header-only
- Modern C++
- Easy to use

**Cons:**
- Less mature than Google Test
- Less community support
- No mocking framework

**Rejected:** Less mature and no mocking framework

### Alternative 3: Boost.Test

**Description:** Use Boost.Test for testing

**Pros:**
- Part of Boost
- Mature framework
- Rich features

**Cons:**
- Requires Boost
- More complex
- Slower compilation

**Rejected:** Requires Boost and more complex

## Related ADRs

- [ADR-023: pytest for Python tests](ADR-023-pytest-python-tests.md)
- [ADR-024: Code coverage requirements (80%)](ADR-024-code-coverage-requirements.md)

## References

- [Google Test Documentation](https://google.github.io/googletest/)
- [Google Mock Documentation](https://google.github.io/googletest/gmock_for_dummies.html)
- [CMake Testing](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [Code Coverage](https://cmake.org/cmake/help/latest/module/FindLcov.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
