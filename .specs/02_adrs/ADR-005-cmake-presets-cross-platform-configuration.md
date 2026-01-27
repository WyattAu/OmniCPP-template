# ADR-005: CMake Presets for Cross-Platform Configuration

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Build System Configuration

---

## Context

The OmniCPP Template project supports multiple platforms (Windows, Linux, WASM) and multiple compilers (MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang). Each platform and compiler combination requires different CMake configurations, making manual configuration error-prone and time-consuming.

### Current State

Developers must manually configure CMake for each combination:
- **Windows + MSVC:** `cmake -G "Visual Studio 17 2022" -A x64`
- **Windows + MSVC-clang:** `cmake -G Ninja -DCMAKE_C_COMPILER=clang-cl.exe`
- **Windows + MinGW-GCC:** `cmake -G Ninja -DCMAKE_C_COMPILER=gcc.exe`
- **Linux + GCC:** `cmake -G Ninja -DCMAKE_C_COMPILER=gcc`
- **Linux + Clang:** `cmake -G Ninja -DCMAKE_C_COMPILER=clang`
- **WASM:** `emcmake .`

This leads to:
1. **Configuration Errors:** Wrong flags or generators for platform/compiler combination
2. **Inconsistent Builds:** Different developers use different configurations
3. **Slow Development:** Manual configuration for each build
4. **Documentation Burden:** Complex setup instructions required

## Decision

Implement **CMake Presets** for all platform and compiler combinations to provide:
1. **Pre-configured Build Settings:** All flags, generators, and paths predefined
2. **Cross-Platform Support:** Presets for Windows, Linux, and WASM
3. **Compiler-Specific Presets:** Separate presets for each compiler
4. **Easy Switching:** Simple command to switch between configurations

### 1. Preset Structure

```json
// CMakePresets.json
{
  "version": 3,
  "configurePresets": [
    // Windows Presets
    {
      "name": "windows-msvc-debug",
      "displayName": "Windows MSVC Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "cl.exe",
        "CMAKE_CXX_COMPILER": "cl.exe"
      },
      "environment": {
        "CC": "cl.exe",
        "CXX": "cl.exe"
      }
    },
    {
      "name": "windows-msvc-release",
      "displayName": "Windows MSVC Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "cl.exe",
        "CMAKE_CXX_COMPILER": "cl.exe"
      },
      "environment": {
        "CC": "cl.exe",
        "CXX": "cl.exe"
      }
    },
    {
      "name": "windows-msvc-clang-debug",
      "displayName": "Windows MSVC-Clang Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "clang-cl.exe",
        "CMAKE_CXX_COMPILER": "clang-cl.exe"
      },
      "environment": {
        "CC": "clang-cl.exe",
        "CXX": "clang-cl.exe"
      }
    },
    {
      "name": "windows-mingw-gcc-debug",
      "displayName": "Windows MinGW-GCC Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "gcc.exe",
        "CMAKE_CXX_COMPILER": "g++.exe"
      },
      "environment": {
        "CC": "gcc.exe",
        "CXX": "g++.exe"
      }
    },
    {
      "name": "windows-mingw-clang-debug",
      "displayName": "Windows MinGW-Clang Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "clang.exe",
        "CMAKE_CXX_COMPILER": "clang++.exe"
      },
      "environment": {
        "CC": "clang.exe",
        "CXX": "clang++.exe"
      }
    },

    // Linux Presets
    {
      "name": "linux-gcc-debug",
      "displayName": "Linux GCC Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++"
      }
    },
    {
      "name": "linux-gcc-release",
      "displayName": "Linux GCC Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++"
      }
    },
    {
      "name": "linux-clang-debug",
      "displayName": "Linux Clang Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "clang",
        "CMAKE_CXX_COMPILER": "clang++"
      }
    },
    {
      "name": "linux-clang-release",
      "displayName": "Linux Clang Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "clang",
        "CMAKE_CXX_COMPILER": "clang++"
      }
    },

    // WASM Presets
    {
      "name": "wasm-debug",
      "displayName": "WASM Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "${sourceDir}/cmake/toolchains/emscripten.cmake"
      }
    },
    {
      "name": "wasm-release",
      "displayName": "WASM Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_TOOLCHAIN_FILE": "${sourceDir}/cmake/toolchains/emscripten.cmake"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "windows-msvc-debug",
      "configurePreset": "windows-msvc-debug"
    },
    {
      "name": "windows-msvc-release",
      "configurePreset": "windows-msvc-release"
    },
    {
      "name": "windows-msvc-clang-debug",
      "configurePreset": "windows-msvc-clang-debug"
    },
    {
      "name": "windows-mingw-gcc-debug",
      "configurePreset": "windows-mingw-gcc-debug"
    },
    {
      "name": "windows-mingw-clang-debug",
      "configurePreset": "windows-mingw-clang-debug"
    },
    {
      "name": "linux-gcc-debug",
      "configurePreset": "linux-gcc-debug"
    },
    {
      "name": "linux-gcc-release",
      "configurePreset": "linux-gcc-release"
    },
    {
      "name": "linux-clang-debug",
      "configurePreset": "linux-clang-debug"
    },
    {
      "name": "linux-clang-release",
      "configurePreset": "linux-clang-release"
    },
    {
      "name": "wasm-debug",
      "configurePreset": "wasm-debug"
    },
    {
      "name": "wasm-release",
      "configurePreset": "wasm-release"
    }
  ]
}
```

### 2. Preset Usage

```bash
# Configure with preset
cmake --preset windows-msvc-debug

# Build with preset
cmake --build --preset windows-msvc-debug

# List available presets
cmake --list-presets
```

### 3. VSCode Integration

```json
// .vscode/settings.json
{
  "cmake.configureOnOpen": false,
  "cmake.generator": "Ninja",
  "cmake.presetPreferred": "windows-msvc-debug"
  "cmake.buildDirectory": "${workspaceFolder}/build"
}
```

## Consequences

### Positive

1. **Consistency:** All developers use same pre-configured settings
2. **Error Reduction:** Pre-configured settings reduce configuration errors
3. **Faster Development:** Quick switching between configurations
4. **Documentation:** Presets serve as documentation for valid configurations
5. **CI/CD Friendly:** Presets work well with CI/CD pipelines
6. **Cross-Platform:** Presets for all platforms ensure consistent builds
7. **IDE Integration:** VSCode and other IDEs can use presets directly

### Negative

1. **File Size:** CMakePresets.json becomes large with many presets
2. **Maintenance:** Adding new compilers or platforms requires updating presets
3. **Complexity:** Preset file can become complex with many options
4. **Learning Curve:** Developers need to understand preset system
5. **Flexibility:** Presets may not cover all edge cases

### Neutral

1. **Documentation:** Requires documentation for preset usage
2. **Testing:** Need to test all preset combinations

## Alternatives Considered

### Alternative 1: Manual Configuration Only

**Description:** Continue with manual CMake configuration

**Pros:**
- No preset file maintenance
- Maximum flexibility

**Cons:**
- High error rate
- Inconsistent builds
- Slow development
- Poor documentation

**Rejected:** Too error-prone and slow

### Alternative 2: Build Scripts Only

**Description:** Use build scripts to configure CMake

**Pros:**
- Can handle complex logic
- Can detect environment

**Cons:**
- Script maintenance burden
- Less IDE integration
- Harder to document

**Rejected:** Less IDE-friendly than presets

### Alternative 3: Environment-Based Configuration

**Description:** Use environment variables to control configuration

**Pros:**
- Flexible
- Works with any tool

**Cons:**
- Non-deterministic
- Hard to reproduce builds
- Environment pollution

**Rejected:** Non-deterministic behavior

## Related ADRs

- [ADR-004: CMake 4 with Ninja as default generator](ADR-004-cmake-4-ninja-default-generator.md)
- [ADR-006: Toolchain file organization](ADR-006-toolchain-file-organization.md)
- [ADR-012: Cross-platform build configuration](ADR-012-cross-platform-build-configuration.md)
- [ADR-026: VSCode tasks.json and launch.json configuration](ADR-026-vscode-tasks-launch-configuration.md)

## References

- [CMake Presets Documentation](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
- [CMake User Presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html#user-presets)
- [VSCode CMake Tools](https://code.visualstudio.com/docs/cpp/cmake-linux)
- [CMake Presets Best Practices](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html#best-practices)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
