# REQ-008: CMake Integration

**Requirement ID:** REQ-008
**Title:** CMake Integration
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

CMake integration shall be enhanced with Nix-aware presets, CachyOS build configurations, enhanced platform detection, and Linux compiler flags.

### Overview

The system shall:
1. Add Nix-aware CMake presets
2. Add CachyOS build configurations
3. Enhance platform detection
4. Add Linux compiler flags

---

## REQ-008-001: Add Nix-Aware CMake Presets

### Description

CMake presets shall be added to support Nix environment builds.

### Functional Requirements

The system shall:
1. Add `nix-debug` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
2. Add `nix-release` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
3. Add `nix-gcc-debug` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
4. Add `nix-gcc-release` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
5. Add `nix-clang-debug` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
6. Add `nix-clang-release` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
7. Set `CMAKE_PREFIX_PATH` to Nix paths
8. Set `CMAKE_LIBRARY_PATH` to Nix library paths
9. Set `CMAKE_INCLUDE_PATH` to Nix include paths
10. Set `CMAKE_C_COMPILER` based on Nix toolchain
11. Set `CMAKE_CXX_COMPILER` based on Nix toolchain

### Acceptance Criteria

- [ ] `nix-debug` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `nix-release` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `nix-gcc-debug` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `nix-gcc-release` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `nix-clang-debug` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `nix-clang-release` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] Presets set `CMAKE_PREFIX_PATH` to Nix paths
- [ ] Presets set `CMAKE_LIBRARY_PATH` to Nix library paths
- [ ] Presets set `CMAKE_INCLUDE_PATH` to Nix include paths
- [ ] Presets set `CMAKE_C_COMPILER` based on Nix toolchain
- [ ] Presets set `CMAKE_CXX_COMPILER` based on Nix toolchain

### Priority

**High** - Nix-aware CMake presets are required for Nix builds.

### Dependencies

- REQ-002-007: Configure CMake integration

### Related ADRs

- [ADR-036: CMake Preset Expansion](../02_adrs/ADR-036-cmake-preset-expansion.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Nix Debug Preset**
   - **Description:** Verify Nix debug preset works
   - **Steps:**
     1. Run `cmake --preset nix-debug`
     2. Verify configuration succeeds
     3. Verify Nix paths are used
   - **Expected Result:** Nix debug preset works correctly

2. **Test Nix Release Preset**
   - **Description:** Verify Nix release preset works
   - **Steps:**
     1. Run `cmake --preset nix-release`
     2. Verify configuration succeeds
     3. Verify Nix paths are used
   - **Expected Result:** Nix release preset works correctly

---

## REQ-008-002: Add CachyOS Build Configurations

### Description

CMake configurations shall be added for CachyOS-specific builds.

### Functional Requirements

The system shall:
1. Add `cachyos-gcc-debug` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
2. Add `cachyos-gcc-release` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
3. Add `cachyos-clang-debug` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
4. Add `cachyos-clang-release` preset to [`CMakePresets.json`](../../CMakePresets.json:1)
5. Apply CachyOS-specific compiler flags
6. Set `CMAKE_CXX_FLAGS` to CachyOS flags
7. Set `CMAKE_EXE_LINKER_FLAGS` to CachyOS flags
8. Set `CMAKE_SHARED_LINKER_FLAGS` to CachyOS flags
9. Enable link-time optimization for release builds
10. Set `QT_QPA_PLATFORM=wayland` for Qt6

### Acceptance Criteria

- [ ] `cachyos-gcc-debug` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `cachyos-gcc-release` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `cachyos-clang-debug` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] `cachyos-clang-release` preset exists in [`CMakePresets.json`](../../CMakePresets.json:1)
- [ ] Presets apply CachyOS-specific flags
- [ ] Presets set `CMAKE_CXX_FLAGS` to CachyOS flags
- [ ] Presets set linker flags to CachyOS flags
- [ ] Presets enable LTO for release builds
- [ ] Presets set `QT_QPA_PLATFORM=wayland`

### Priority

**High** - CachyOS build configurations are required for CachyOS builds.

### Dependencies

- REQ-001-005: Apply CachyOS-specific compiler flags

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-036: CMake Preset Expansion](../02_adrs/ADR-036-cmake-preset-expansion.md)

### Related Threats

- **TM-LX-002: Distribution-Specific Vulnerabilities** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:352)

### Test Cases

#### Integration Tests

1. **Test CachyOS GCC Debug Preset**
   - **Description:** Verify CachyOS GCC debug preset works
   - **Steps:**
     1. Run `cmake --preset cachyos-gcc-debug`
     2. Verify configuration succeeds
     3. Verify CachyOS flags are applied
   - **Expected Result:** CachyOS GCC debug preset works correctly

2. **Test CachyOS Clang Release Preset**
   - **Description:** Verify CachyOS Clang release preset works
   - **Steps:**
     1. Run `cmake --preset cachyos-clang-release`
     2. Verify configuration succeeds
     3. Verify CachyOS flags are applied
     4. Verify LTO is enabled
   - **Expected Result:** CachyOS Clang release preset works correctly

---

## REQ-008-003: Enhance Platform Detection

### Description

Platform detection in CMake shall be enhanced to support Linux distributions and CachyOS.

### Functional Requirements

The system shall:
1. Add Linux distribution detection to [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
2. Add CachyOS detection to [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
3. Add Nix environment detection to [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
4. Set `OMNI_LINUX_DISTRIBUTION` variable
5. Set `OMNI_IS_CACHYOS` variable
6. Set `OMNI_IN_NIX_SHELL` variable
7. Log detected platform at configuration time
8. Provide platform-specific configuration
9. Handle unknown distributions gracefully
10. Document platform detection logic

### Acceptance Criteria

- [ ] Linux distribution detection exists in [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
- [ ] CachyOS detection exists in [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
- [ ] Nix environment detection exists in [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1)
- [ ] `OMNI_LINUX_DISTRIBUTION` variable is set
- [ ] `OMNI_IS_CACHYOS` variable is set
- [ ] `OMNI_IN_NIX_SHELL` variable is set
- [ ] Platform is logged at configuration time
- [ ] Platform-specific configuration is provided
- [ ] Unknown distributions are handled gracefully
- [ ] Platform detection logic is documented

### Priority

**Critical** - Enhanced platform detection is required for Linux builds.

### Dependencies

- REQ-001-001: Detect Linux distribution
- REQ-001-002: Detect CachyOS specifically
- REQ-001-003: Detect Nix environment

### Related ADRs

- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Linux Distribution Detection**
   - **Description:** Verify Linux distribution is detected
   - **Steps:**
     1. Run `cmake --preset nix-debug`
     2. Check `OMNI_LINUX_DISTRIBUTION` variable
     3. Verify distribution is detected
   - **Expected Result:** Linux distribution is detected

2. **Test CachyOS Detection**
   - **Description:** Verify CachyOS is detected
   - **Steps:**
     1. Run `cmake --preset cachyos-gcc-debug`
     2. Check `OMNI_IS_CACHYOS` variable
     3. Verify CachyOS is detected
   - **Expected Result:** CachyOS is detected

---

## REQ-008-004: Add Linux Compiler Flags

### Description

Linux-specific compiler flags shall be added to CMake configuration.

### Functional Requirements

The system shall:
1. Add Linux compiler flags to [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
2. Add CachyOS-specific flags to [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
3. Add Nix-specific flags to [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
4. Set `CMAKE_CXX_FLAGS_DEBUG` for Linux debug builds
5. Set `CMAKE_CXX_FLAGS_RELEASE` for Linux release builds
6. Apply `-march=native` for CachyOS release builds
7. Apply `-O3` for release builds
8. Apply `-flto` for release builds
9. Apply `-g` for debug builds
10. Apply security flags for GCC builds
11. Document compiler flag logic

### Acceptance Criteria

- [ ] Linux compiler flags exist in [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
- [ ] CachyOS-specific flags exist in [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
- [ ] Nix-specific flags exist in [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1)
- [ ] `CMAKE_CXX_FLAGS_DEBUG` is set for Linux debug builds
- [ ] `CMAKE_CXX_FLAGS_RELEASE` is set for Linux release builds
- [ ] `-march=native` is applied for CachyOS release builds
- [ ] `-O3` is applied for release builds
- [ ] `-flto` is applied for release builds
- [ ] `-g` is applied for debug builds
- [ ] Security flags are applied for GCC builds
- [ ] Compiler flag logic is documented

### Priority

**High** - Linux compiler flags are required for Linux builds.

### Dependencies

- REQ-001-005: Apply CachyOS-specific compiler flags

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Linux Debug Flags**
   - **Description:** Verify Linux debug flags are applied
   - **Steps:**
     1. Run `cmake --preset nix-debug`
     2. Check `CMAKE_CXX_FLAGS_DEBUG` variable
     3. Verify debug flags are present
   - **Expected Result:** Linux debug flags are applied

2. **Test CachyOS Release Flags**
   - **Description:** Verify CachyOS release flags are applied
   - **Steps:**
     1. Run `cmake --preset cachyos-gcc-release`
     2. Check `CMAKE_CXX_FLAGS_RELEASE` variable
     3. Verify CachyOS flags are present
     4. Verify LTO is enabled
   - **Expected Result:** CachyOS release flags are applied

---

## Implementation Notes

### CMakePresets.json Structure

Add to [`CMakePresets.json`](../../CMakePresets.json:1):

```json
{
  "version": 3,
  "cmakeMinimumRequired": "3.20",
  "include": [
    "cmake-presets/linux.json"
  ],
  "configurePresets": [
    {
      "name": "nix-debug",
      "displayName": "Nix Debug",
      "binaryDir": "${sourceDir}/build/nix-debug",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++",
        "CMAKE_CXX_FLAGS_DEBUG": "-g -O0 -DDEBUG",
        "CMAKE_PREFIX_PATH": "/nix/store/.../qt6:/nix/store/.../vulkan-headers",
        "CMAKE_LIBRARY_PATH": "/nix/store/.../qt6/lib:/nix/store/.../vulkan-loader/lib",
        "CMAKE_INCLUDE_PATH": "/nix/store/.../qt6/include:/nix/store/.../vulkan-headers/include",
        "OMNI_IN_NIX_SHELL": "ON"
      }
    },
    {
      "name": "nix-release",
      "displayName": "Nix Release",
      "binaryDir": "${sourceDir}/build/nix-release",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++",
        "CMAKE_CXX_FLAGS_RELEASE": "-O3 -DNDEBUG",
        "CMAKE_EXE_LINKER_FLAGS": "-flto",
        "CMAKE_SHARED_LINKER_FLAGS": "-flto",
        "CMAKE_PREFIX_PATH": "/nix/store/.../qt6:/nix/store/.../vulkan-headers",
        "CMAKE_LIBRARY_PATH": "/nix/store/.../qt6/lib:/nix/store/.../vulkan-loader/lib",
        "CMAKE_INCLUDE_PATH": "/nix/store/.../qt6/include:/nix/store/.../vulkan-headers/include",
        "OMNI_IN_NIX_SHELL": "ON"
      }
    },
    {
      "name": "cachyos-gcc-debug",
      "displayName": "CachyOS GCC Debug",
      "binaryDir": "${sourceDir}/build/cachyos-gcc-debug",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++",
        "CMAKE_CXX_FLAGS_DEBUG": "-g -O0 -DDEBUG",
        "OMNI_LINUX_DISTRIBUTION": "CachyOS",
        "OMNI_IS_CACHYOS": "ON",
        "QT_QPA_PLATFORM": "wayland"
      }
    },
    {
      "name": "cachyos-gcc-release",
      "displayName": "CachyOS GCC Release",
      "binaryDir": "${sourceDir}/build/cachyos-gcc-release",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++",
        "CMAKE_CXX_FLAGS_RELEASE": "-march=native -O3 -flto -DNDEBUG",
        "CMAKE_EXE_LINKER_FLAGS": "-march=native -flto",
        "CMAKE_SHARED_LINKER_FLAGS": "-march=native -flto",
        "OMNI_LINUX_DISTRIBUTION": "CachyOS",
        "OMNI_IS_CACHYOS": "ON",
        "QT_QPA_PLATFORM": "wayland"
      }
    }
  ]
}
```

### PlatformConfig.cmake Enhancements

Add to [`cmake/PlatformConfig.cmake`](../../cmake/PlatformConfig.cmake:1):

```cmake
# Linux distribution detection
if(UNIX AND NOT APPLE)
    # Read /etc/os-release
    if(EXISTS "/etc/os-release")
        file(READ "/etc/os-release" OS_RELEASE)
        string(REPLACE "${OS_RELEASE}" "\n" ";" OS_RELEASE_LIST)
        foreach(LINE ${OS_RELEASE_LIST})
            string(STRIP ${LINE} LINE)
            if(LINE MATCHES "^ID=.*")
                string(REPLACE "${LINE}" "ID=" "" LINUX_ID)
                if(LINUX_ID STREQUAL "cachyos")
                    set(OMNI_IS_CACHYOS ON)
                    set(OMNI_LINUX_DISTRIBUTION "CachyOS")
                elseif(LINUX_ID STREQUAL "arch")
                    set(OMNI_LINUX_DISTRIBUTION "Arch Linux")
                elseif(LINUX_ID STREQUAL "ubuntu")
                    set(OMNI_LINUX_DISTRIBUTION "Ubuntu")
                endif()
            endif()
        endforeach()
    endif()

    # Detect Nix environment
    if(DEFINED ENV{IN_NIX_SHELL})
        set(OMNI_IN_NIX_SHELL ON)
    endif()

    message(STATUS "Linux Distribution: ${OMNI_LINUX_DISTRIBUTION}")
    if(OMNI_IS_CACHYOS)
        message(STATUS "CachyOS detected")
    endif()
    if(OMNI_IN_NIX_SHELL)
        message(STATUS "Nix environment detected")
    endif()
endif()
```

### CompilerFlags.cmake Enhancements

Add to [`cmake/CompilerFlags.cmake`](../../cmake/CompilerFlags.cmake:1):

```cmake
# Linux compiler flags
if(UNIX AND NOT APPLE)
    # Common Linux flags
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0 -DDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")

    # CachyOS-specific flags
    if(OMNI_IS_CACHYOS)
        set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native -flto")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -march=native -flto")
        set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -march=native -flto")
        
        # GCC security flags
        if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fstack-protector-strong")
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_FORTIFY_SOURCE=2")
        endif()
    endif()

    # Nix-specific flags
    if(OMNI_IN_NIX_SHELL)
        # Nix paths are handled via CMAKE_PREFIX_PATH
        message(STATUS "Using Nix environment")
    endif()
endif()
```

### Preset Organization

Organize CMake presets into logical groups:
- **Nix:** Nix environment presets
- **CachyOS:** CachyOS-specific presets
- **Linux:** Generic Linux presets
- **Cross-Platform:** Cross-compilation presets

### Documentation

Add comments to CMake files explaining:
- Platform detection logic
- Compiler flag selection
- CachyOS-specific optimizations
- Nix environment integration

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-036: CMake Preset Expansion](../02_adrs/ADR-036-cmake-preset-expansion.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
