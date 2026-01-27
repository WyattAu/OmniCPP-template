# ADR-004: CMake 4 with Ninja as Default Generator

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Build System Configuration

---

## Context

The OmniCPP Template project requires a modern, fast build system that supports cross-platform compilation (Windows, Linux, WASM). CMake 4.0+ provides significant improvements over earlier versions, and Ninja is a fast, low-overhead build tool that significantly reduces build times.

### Current State

The project currently uses CMake with various generators:

- **Windows:** Visual Studio (MSVC), Ninja
- **Linux:** Makefiles, Ninja
- **WASM:** Emscripten

### Requirements

1. **Performance:** Build times should be minimized
2. **Cross-Platform:** Must work on Windows, Linux, and WASM
3. **Modern Features:** Leverage CMake 4.0+ improvements
4. **Parallelism:** Maximize parallel compilation
5. **Reproducibility:** Ensure consistent builds across platforms

## Decision

Adopt **CMake 4.0+ with Ninja as the default generator** for all platforms.

### 1. CMake Version Requirement

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 4.0)
project(OmniCppTemplate
    VERSION 1.0.0
    DESCRIPTION "OmniCpp Template Project"
    LANGUAGES CXX
)
```

### 2. Ninja as Default Generator

```cmake
# CMakePresets.json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "default",
      "displayName": "Default Config",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER_LAUNCHER": "ccache"
      },
      "cacheVariables": {
        "CMAKE_CXX_COMPILER_LAUNCHER": "ccache"
      }
    },
    {
      "name": "debug",
      "displayName": "Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "release",
      "displayName": "Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ]
}
```

### 3. Platform-Specific Configuration

```cmake
# cmake/PlatformConfig.cmake
if(WIN32)
    # Windows: Use Ninja with MSVC or MinGW
    if(NOT CMAKE_GENERATOR MATCHES "Ninja")
        message(WARNING "Ninja generator not detected. Build times may be slower.")
    endif()
elseif(UNIX AND NOT APPLE)
    # Linux: Use Ninja
    if(NOT CMAKE_GENERATOR MATCHES "Ninja")
        message(WARNING "Ninja generator not detected. Build times may be slower.")
    endif()
elseif(APPLE)
    # macOS: Use Ninja
    if(NOT CMAKE_GENERATOR MATCHES "Ninja")
        message(WARNING "Ninja generator not detected. Build times may be slower.")
    endif()
endif()
```

### 4. Build Optimization

```cmake
# cmake/CompilerFlags.cmake
# Enable parallel compilation
if(NOT DEFINED CMAKE_JOB_POOLS)
    include(ProcessorCount)
    ProcessorCount(CPU_COUNT)
    set(CMAKE_JOB_POOLS ${CPU_COUNT})
    message(STATUS "Using ${CMAKE_JOB_POOLS} parallel jobs")
endif()

# Enable ccache for faster rebuilds
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(ENV{CCACHE_DIR} "${CMAKE_BINARY_DIR}/.ccache")
    message(STATUS "ccache enabled: ${CCACHE_PROGRAM}")
endif()
```

### 5. Ninja Build Configuration

```cmake
# cmake/ProjectConfig.cmake
# Ninja-specific optimizations
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_COLOR_MAKEFILE ON)

# Reduce build noise
set(CMAKE_RULE_MESSAGES OFF)
set(CMAKE_PROGRESS_BAR OFF)
```

## Consequences

### Positive

1. **Performance:** Ninja provides significantly faster builds than Makefiles or Visual Studio
2. **Parallelism:** Ninja automatically parallelizes builds across all CPU cores
3. **Cross-Platform:** Works consistently across Windows, Linux, and WASM
4. **Modern Features:** CMake 4.0+ provides better dependency handling and faster configuration
5. **Reproducibility:** Consistent generator across platforms improves build reproducibility
6. **Incremental Builds:** Ninja efficiently handles incremental builds
7. **Better Error Messages:** Ninja provides clearer error messages than Makefiles

### Negative

1. **Ninja Dependency:** Requires Ninja to be installed on all build machines
2. **Learning Curve:** Developers unfamiliar with Ninja may need to learn its syntax
3. **Debugging:** Debugging Ninja build files can be more complex than Makefiles
4. **Windows Support:** Ninja on Windows requires proper environment setup (MSVC or MinGW)
5. **IDE Integration:** Some IDEs may have better integration with Visual Studio projects

### Neutral

1. **Documentation:** Requires documentation for Ninja-specific debugging
2. **CI/CD:** CI/CD pipelines must ensure Ninja is available

## Alternatives Considered

### Alternative 1: Visual Studio Generator (Windows Only)

**Description:** Use Visual Studio generator on Windows

**Pros:**

- Excellent IDE integration
- Native Windows development experience
- Built-in debugging support

**Cons:**

- Windows-only, not cross-platform
- Slower builds than Ninja
- Not suitable for CI/CD
- Larger build files

**Rejected:** Not cross-platform, slower builds

### Alternative 2: Unix Makefiles Generator

**Description:** Use Unix Makefiles generator on all platforms

**Pros:**

- Universal availability
- Simple to understand
- Good IDE support

**Cons:**

- Slower builds than Ninja
- Poor parallelism
- No incremental build optimization

**Rejected:** Slower builds, poor performance

### Alternative 3: Xcode Generator (macOS Only)

**Description:** Use Xcode generator on macOS

**Pros:**

- Native macOS development experience
- Excellent IDE integration
- Built-in debugging support

**Cons:**

- macOS-only, not cross-platform
- Slower builds than Ninja
- Not suitable for CI/CD

**Rejected:** Not cross-platform, slower builds

### Alternative 4: CMake 3.x with Ninja

**Description:** Use CMake 3.x with Ninja generator

**Pros:**

- Wider CMake version support
- Still uses Ninja for fast builds

**Cons:**

- Missing CMake 4.0+ features
- Slower configuration
- Less efficient dependency handling

**Rejected:** Missing modern CMake features

## Related ADRs

- [ADR-005: CMake Presets for cross-platform configuration](ADR-005-cmake-presets-cross-platform-configuration.md)
- [ADR-006: Toolchain file organization](ADR-006-toolchain-file-organization.md)
- [ADR-012: Cross-platform build configuration](ADR-012-cross-platform-build-configuration.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)

## References

- [CMake 4.0 Release Notes](https://cmake.org/cmake/help/latest/release/4.0.html)
- [Ninja Documentation](https://ninja-build.org/)
- [CMake Generators](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html)
- [CMake Performance Tips](https://cmake.org/cmake/help/latest/manual/cmake-performance.7.html)
- [CMake Presets Documentation](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)

---

**Document Control**

| Version | Date       | Author           | Changes         |
| ------- | ---------- | ---------------- | --------------- |
| 1.0     | 2026-01-07 | System Architect | Initial version |
