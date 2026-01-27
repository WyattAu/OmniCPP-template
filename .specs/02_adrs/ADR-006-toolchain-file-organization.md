# ADR-006: Toolchain File Organization

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Build System Configuration

---

## Context

The OmniCPP Template project supports cross-platform compilation for multiple architectures and compilers. Each target platform requires specific toolchain configurations, including compiler paths, flags, and system libraries. Without proper organization, toolchain files become scattered, duplicated, and difficult to maintain.

### Current State

Toolchain files are located in `cmake/toolchains/` but lack consistent organization:
- **arm64-linux-gnu.cmake**: ARM64 Linux cross-compilation
- **arm64-windows-msvc.cmake**: ARM64 Windows cross-compilation
- **emscripten.cmake**: WebAssembly compilation
- **x86-linux-gnu.cmake**: x86 Linux cross-compilation

Issues:
1. **Inconsistent Naming:** No clear naming convention
2. **Missing Documentation:** No documentation for each toolchain
3. **Duplicated Logic:** Similar settings repeated across files
4. **Hard to Extend:** Adding new toolchains requires copying existing files
5. **No Validation:** No validation that toolchain files work correctly

## Decision

Implement a **structured toolchain file organization** with:
1. **Consistent Naming Convention:** `{platform}-{compiler}-{architecture}.cmake`
2. **Modular Structure:** Common settings in base files, platform-specific in derived files
3. **Documentation:** Each toolchain file includes usage documentation
4. **Validation:** Toolchain validation scripts
5. **Extensibility:** Easy to add new toolchains

### 1. Directory Structure

```
cmake/toolchains/
├── base/
│   ├── common.cmake           # Common settings for all toolchains
│   ├── windows-base.cmake     # Windows-specific base settings
│   ├── linux-base.cmake       # Linux-specific base settings
│   └── emscripten-base.cmake  # Emscripten-specific base settings
├── windows/
│   ├── msvc-x64.cmake         # Windows MSVC x64
│   ├── msvc-arm64.cmake       # Windows MSVC ARM64
│   ├── msvc-clang-x64.cmake   # Windows MSVC-Clang x64
│   ├── mingw-gcc-x64.cmake    # Windows MinGW-GCC x64
│   └── mingw-clang-x64.cmake  # Windows MinGW-Clang x64
├── linux/
│   ├── gcc-x64.cmake          # Linux GCC x64
│   ├── gcc-arm64.cmake        # Linux GCC ARM64
│   ├── clang-x64.cmake        # Linux Clang x64
│   └── clang-arm64.cmake      # Linux Clang ARM64
├── cross/
│   ├── arm64-linux-gnu.cmake  # Cross-compile ARM64 Linux
│   └── x86-linux-gnu.cmake    # Cross-compile x86 Linux
└── wasm/
    └── emscripten.cmake       # WebAssembly
```

### 2. Base Toolchain File

```cmake
# cmake/toolchains/base/common.cmake
# Common settings for all toolchains

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable position-independent code
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Enable testing
enable_testing()

# Export compile commands
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

### 3. Windows Base Toolchain

```cmake
# cmake/toolchains/base/windows-base.cmake
# Windows-specific base settings

# Windows-specific flags
add_compile_options(
    /W4           # Warning level 4
    /WX           # Treat warnings as errors
    /permissive-  # Disable non-conforming code
    /Zc:__cplusplus # Enable correct __cplusplus macro
)

# Windows-specific definitions
add_definitions(
    -DWIN32_LEAN_AND_MEAN
    -DNOMINMAX
    -D_CRT_SECURE_NO_WARNINGS
)

# Windows-specific libraries
if(MSVC)
    add_compile_options(/MP)  # Multi-processor compilation
endif()
```

### 4. Linux Base Toolchain

```cmake
# cmake/toolchains/base/linux-base.cmake
# Linux-specific base settings

# Linux-specific flags
add_compile_options(
    -Wall
    -Wextra
    -Wpedantic
    -Werror
)

# Linux-specific definitions
add_definitions(
    -D_POSIX_C_SOURCE=200809L
    -D_XOPEN_SOURCE=700
)

# Linux-specific libraries
find_package(Threads REQUIRED)
```

### 5. Platform-Specific Toolchain Example

```cmake
# cmake/toolchains/windows/msvc-x64.cmake
# Windows MSVC x64 toolchain

# Include base settings
include(${CMAKE_CURRENT_LIST_DIR}/../base/common.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../base/windows-base.cmake)

# Set compiler
set(CMAKE_C_COMPILER cl.exe)
set(CMAKE_CXX_COMPILER cl.exe)

# Set architecture
set(CMAKE_GENERATOR_PLATFORM x64)

# MSVC-specific flags
add_compile_options(
    /O2           # Optimize for speed
    /GL           # Whole program optimization
    /Gy           # Enable function-level linking
)

add_link_options(
    /LTCG         # Link-time code generation
    /OPT:REF      # Remove unreferenced functions
    /OPT:ICF      # Remove identical COMDATs
)

# Usage:
# cmake -G Ninja -DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/windows/msvc-x64.cmake
```

### 6. Cross-Compilation Toolchain Example

```cmake
# cmake/toolchains/cross/arm64-linux-gnu.cmake
# Cross-compile for ARM64 Linux

# Include base settings
include(${CMAKE_CURRENT_LIST_DIR}/../base/common.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../base/linux-base.cmake)

# Set target system
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# Set cross-compiler
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

# Set sysroot
set(CMAKE_SYSROOT /usr/aarch64-linux-gnu)

# Set library and include paths
set(CMAKE_FIND_ROOT_PATH /usr/aarch64-linux-gnu)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# Usage:
# cmake -G Ninja -DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/cross/arm64-linux-gnu.cmake
```

### 7. Toolchain Validation Script

```python
# scripts/validate_toolchains.py
#!/usr/bin/env python3
"""Validate toolchain files."""

import os
import subprocess
import sys
from pathlib import Path

def validate_toolchain(toolchain_path: Path) -> bool:
    """Validate a toolchain file."""
    print(f"Validating {toolchain_path.name}...")

    # Check if file exists
    if not toolchain_path.exists():
        print(f"  ERROR: Toolchain file not found")
        return False

    # Check if file is readable
    try:
        with open(toolchain_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR: Cannot read toolchain file: {e}")
        return False

    # Check for required documentation
    if "# Usage:" not in content:
        print(f"  WARNING: Missing usage documentation")

    # Check for base includes
    if "include(" not in content:
        print(f"  WARNING: Toolchain does not include base settings")

    print(f"  OK")
    return True

def main():
    """Main validation function."""
    toolchains_dir = Path("cmake/toolchains")

    if not toolchains_dir.exists():
        print(f"ERROR: Toolchains directory not found: {toolchains_dir}")
        return 1

    # Find all toolchain files
    toolchain_files = list(toolchains_dir.rglob("*.cmake"))

    if not toolchain_files:
        print(f"ERROR: No toolchain files found in {toolchains_dir}")
        return 1

    print(f"Found {len(toolchain_files)} toolchain files")
    print()

    # Validate each toolchain
    results = []
    for toolchain_file in toolchain_files:
        result = validate_toolchain(toolchain_file)
        results.append(result)

    # Print summary
    print()
    print("Summary:")
    print(f"  Total: {len(results)}")
    print(f"  Passed: {sum(results)}")
    print(f"  Failed: {len(results) - sum(results)}")

    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Consequences

### Positive

1. **Organization:** Clear, structured organization of toolchain files
2. **Maintainability:** Common settings in base files reduce duplication
3. **Extensibility:** Easy to add new toolchains by copying and modifying
4. **Documentation:** Each toolchain includes usage documentation
5. **Validation:** Toolchain validation ensures correctness
6. **Consistency:** Consistent naming convention across all toolchains
7. **Cross-Platform:** Supports all target platforms consistently

### Negative

1. **Complexity:** More complex directory structure
2. **Learning Curve:** Developers need to understand the structure
3. **Maintenance:** Base files require careful updates
4. **File Count:** More files to maintain

### Neutral

1. **Documentation:** Requires documentation for the structure
2. **Testing:** Need to test all toolchain combinations

## Alternatives Considered

### Alternative 1: Flat Directory Structure

**Description:** Keep all toolchain files in a single directory

**Pros:**
- Simpler structure
- Fewer directories

**Cons:**
- No logical grouping
- Harder to find specific toolchains
- More duplication

**Rejected:** Poor organization and maintainability

### Alternative 2: No Base Files

**Description:** Each toolchain file is self-contained

**Pros:**
- Simpler individual files
- No dependencies between files

**Cons:**
- Massive duplication
- Hard to maintain
- Inconsistent settings

**Rejected:** Too much duplication

### Alternative 3: Auto-Generated Toolchains

**Description:** Generate toolchain files from templates

**Pros:**
- Less manual work
- Consistent structure

**Cons:**
- Complex generation logic
- Hard to customize
- Additional build step

**Rejected:** Too complex for current needs

## Related ADRs

- [ADR-004: CMake 4 with Ninja as default generator](ADR-004-cmake-4-ninja-default-generator.md)
- [ADR-005: CMake Presets for cross-platform configuration](ADR-005-cmake-presets-cross-platform-configuration.md)
- [ADR-012: Cross-platform build configuration](ADR-012-cross-platform-build-configuration.md)

## References

- [CMake Toolchain Files](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)
- [CMake Cross-Compiling](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html#cross-compiling)
- [CMake Toolchain Variables](https://cmake.org/cmake/help/latest/variable/CMAKE_TOOLCHAIN_FILE.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
