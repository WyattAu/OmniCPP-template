# ADR-036: CMake Preset Expansion

**Status:** Accepted
**Date:** 2026-01-27
**Context:** CMake Configuration for Linux

---

## Context

The OmniCPP Template project uses CMake presets ([`CMakePresets.json`](../../CMakePresets.json:1)) for cross-platform build configuration. The current presets are primarily Windows-centric, with presets for MSVC, MSVC-clang, MinGW-GCC, and MinGW-Clang.

### Current State

**Existing Presets:**
- `msvc-debug` - MSVC debug configuration
- `msvc-release` - MSVC release configuration
- `clang-msvc-debug` - Clang with MSVC runtime debug
- `clang-msvc-release` - Clang with MSVC runtime release
- `mingw-gcc-debug` - MinGW GCC debug
- `mingw-gcc-release` - MinGW GCC release
- `mingw-clang-debug` - MinGW Clang debug
- `mingw-clang-release` - MinGW Clang release
- `emscripten-debug` - Emscripten WASM debug
- `emscripten-release` - Emscripten WASM release

### Linux Expansion Requirements

The Linux expansion requires CMake presets for:

1. **GCC Presets:** GCC compiler on Linux
2. **Clang Presets:** Clang compiler on Linux
3. **CachyOS Presets:** CachyOS-specific configurations
4. **Nix Presets:** Nix environment configurations
5. **Debug/Release Variants:** Debug and release configurations
6. **Build Type Variants:** Debug, Release, RelWithDebInfo, MinSizeRel
7. **C++ Standard:** C++23 support
8. **Toolchain Integration:** Integration with CMake toolchains

### Challenges

1. **Preset Proliferation:** Many presets increase complexity
2. **Maintenance Burden:** More presets to maintain
3. **Preset Inheritance:** Need to manage preset inheritance
4. **Compiler Versions:** Different GCC and Clang versions
5. **Distribution Differences:** Different Linux distributions
6. **Nix Integration:** Nix-provided toolchains
7. **CachyOS Optimizations:** CachyOS-specific flags
8. **Preset Naming:** Consistent naming convention

## Decision

Create comprehensive Linux CMake presets with clear organization and inheritance.

### 1. Preset Organization

Organize presets by platform and compiler:

```json
{
  "version": 3,
  "include": [],
  "configurePresets": [
    // Windows Presets (existing)
    {
      "name": "msvc-debug",
      "displayName": "MSVC Debug",
      "binaryDir": "${sourceDir}/build/msvc-debug",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_C_COMPILER": "cl",
        "CMAKE_CXX_COMPILER": "cl"
      }
    },

    // Linux Presets (new)
    {
      "name": "linux-gcc-debug",
      "displayName": "Linux GCC Debug",
      "binaryDir": "${sourceDir}/build/linux-gcc-debug",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_C_COMPILER": "gcc",
        "CMAKE_CXX_COMPILER": "g++",
        "CMAKE_C_FLAGS": "-g -O0 -DDEBUG",
        "CMAKE_CXX_FLAGS": "-g -O0 -DDEBUG"
      }
    }
  ]
}
```

### 2. Base GCC Preset

Create base GCC preset:

```json
{
  "name": "linux-gcc-base",
  "hidden": true,
  "generator": "Ninja",
  "cacheVariables": {
    "CMAKE_C_COMPILER": "gcc",
    "CMAKE_CXX_COMPILER": "g++",
    "CMAKE_CXX_STANDARD": "23",
    "CMAKE_CXX_STANDARD_REQUIRED": "ON",
    "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
  },
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Linux"
  }
}
```

### 3. GCC Debug Preset

Create GCC debug preset:

```json
{
  "name": "linux-gcc-debug",
  "displayName": "Linux GCC Debug",
  "inherits": "linux-gcc-base",
  "binaryDir": "${sourceDir}/build/linux-gcc-debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_FLAGS": "-g -O0 -DDEBUG",
    "CMAKE_CXX_FLAGS": "-g -O0 -DDEBUG",
    "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
  }
}
```

### 4. GCC Release Preset

Create GCC release preset:

```json
{
  "name": "linux-gcc-release",
  "displayName": "Linux GCC Release",
  "inherits": "linux-gcc-base",
  "binaryDir": "${sourceDir}/build/linux-gcc-release",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_C_FLAGS": "-O3 -DNDEBUG",
    "CMAKE_CXX_FLAGS": "-O3 -DNDEBUG"
  }
}
```

### 5. Base Clang Preset

Create base Clang preset:

```json
{
  "name": "linux-clang-base",
  "hidden": true,
  "generator": "Ninja",
  "cacheVariables": {
    "CMAKE_C_COMPILER": "clang",
    "CMAKE_CXX_COMPILER": "clang++",
    "CMAKE_CXX_STANDARD": "23",
    "CMAKE_CXX_STANDARD_REQUIRED": "ON",
    "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
  },
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Linux"
  }
}
```

### 6. Clang Debug Preset

Create Clang debug preset:

```json
{
  "name": "linux-clang-debug",
  "displayName": "Linux Clang Debug",
  "inherits": "linux-clang-base",
  "binaryDir": "${sourceDir}/build/linux-clang-debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_FLAGS": "-g -O0 -DDEBUG",
    "CMAKE_CXX_FLAGS": "-g -O0 -DDEBUG",
    "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
  }
}
```

### 7. Clang Release Preset

Create Clang release preset:

```json
{
  "name": "linux-clang-release",
  "displayName": "Linux Clang Release",
  "inherits": "linux-clang-base",
  "binaryDir": "${sourceDir}/build/linux-clang-release",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_C_FLAGS": "-O3 -DNDEBUG",
    "CMAKE_CXX_FLAGS": "-O3 -DNDEBUG"
  }
}
```

### 8. CachyOS GCC Preset

Create CachyOS-specific GCC preset with optimizations:

```json
{
  "name": "cachyos-gcc-base",
  "hidden": true,
  "inherits": "linux-gcc-base",
  "cacheVariables": {
    "CMAKE_C_FLAGS": "-march=native",
    "CMAKE_CXX_FLAGS": "-march=native"
  },
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Linux"
  },
  "environment": {
    "CACHYOS": "1"
  }
}
```

### 9. CachyOS GCC Debug Preset

Create CachyOS GCC debug preset:

```json
{
  "name": "cachyos-gcc-debug",
  "displayName": "CachyOS GCC Debug",
  "inherits": "cachyos-gcc-base",
  "binaryDir": "${sourceDir}/build/cachyos-gcc-debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_FLAGS": "-march=native -g -O0 -DDEBUG",
    "CMAKE_CXX_FLAGS": "-march=native -g -O0 -DDEBUG"
  }
}
```

### 10. CachyOS GCC Release Preset

Create CachyOS GCC release preset with optimizations:

```json
{
  "name": "cachyos-gcc-release",
  "displayName": "CachyOS GCC Release",
  "inherits": "cachyos-gcc-base",
  "binaryDir": "${sourceDir}/build/cachyos-gcc-release",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_C_FLAGS": "-march=native -O3 -flto -DNDEBUG",
    "CMAKE_CXX_FLAGS": "-march=native -O3 -flto -DNDEBUG",
    "CMAKE_EXE_LINKER_FLAGS": "-Wl,--as-needed -Wl,--no-undefined -flto",
    "CMAKE_SHARED_LINKER_FLAGS": "-Wl,--as-needed -Wl,--no-undefined -flto"
  }
}
```

### 11. CachyOS Clang Preset

Create CachyOS-specific Clang preset:

```json
{
  "name": "cachyos-clang-base",
  "hidden": true,
  "inherits": "linux-clang-base",
  "cacheVariables": {
    "CMAKE_C_FLAGS": "-march=native",
    "CMAKE_CXX_FLAGS": "-march=native"
  },
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Linux"
  },
  "environment": {
    "CACHYOS": "1"
  }
}
```

### 12. CachyOS Clang Debug Preset

Create CachyOS Clang debug preset:

```json
{
  "name": "cachyos-clang-debug",
  "displayName": "CachyOS Clang Debug",
  "inherits": "cachyos-clang-base",
  "binaryDir": "${sourceDir}/build/cachyos-clang-debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_FLAGS": "-march=native -g -O0 -DDEBUG",
    "CMAKE_CXX_FLAGS": "-march=native -g -O0 -DDEBUG"
  }
}
```

### 13. CachyOS Clang Release Preset

Create CachyOS Clang release preset:

```json
{
  "name": "cachyos-clang-release",
  "displayName": "CachyOS Clang Release",
  "inherits": "cachyos-clang-base",
  "binaryDir": "${sourceDir}/build/cachyos-clang-release",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_C_FLAGS": "-march=native -O3 -flto -DNDEBUG",
    "CMAKE_CXX_FLAGS": "-march=native -O3 -flto -DNDEBUG",
    "CMAKE_EXE_LINKER_FLAGS": "-Wl,--as-needed -Wl,--no-undefined -flto",
    "CMAKE_SHARED_LINKER_FLAGS": "-Wl,--as-needed -Wl,--no-undefined -flto"
  }
}
```

### 14. Nix GCC Preset

Create Nix-specific GCC preset:

```json
{
  "name": "nix-gcc-base",
  "hidden": true,
  "inherits": "linux-gcc-base",
  "environment": {
    "IN_NIX_SHELL": "1"
  },
  "condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Linux"
  }
}
```

### 15. Nix GCC Debug Preset

Create Nix GCC debug preset:

```json
{
  "name": "nix-gcc-debug",
  "displayName": "Nix GCC Debug",
  "inherits": "nix-gcc-base",
  "binaryDir": "${sourceDir}/build/nix-gcc-debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_FLAGS": "-g -O0 -DDEBUG",
    "CMAKE_CXX_FLAGS": "-g -O0 -DDEBUG"
  }
}
```

### 16. Nix GCC Release Preset

Create Nix GCC release preset:

```json
{
  "name": "nix-gcc-release",
  "displayName": "Nix GCC Release",
  "inherits": "nix-gcc-base",
  "binaryDir": "${sourceDir}/build/nix-gcc-release",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Release",
    "CMAKE_C_FLAGS": "-O3 -DNDEBUG",
    "CMAKE_CXX_FLAGS": "-O3 -DNDEBUG"
  }
}
```

### 17. Preset Selection Logic

Implement preset selection in OmniCppController.py:

```python
def select_cmake_preset(
    platform: PlatformInfo,
    compiler: str,
    build_type: str
) -> str:
    """Select appropriate CMake preset based on platform and compiler."""

    if platform.os == "Linux":
        if platform.is_cachyos:
            return f"cachyos-{compiler}-{build_type.lower()}"
        elif platform.is_nix:
            return f"nix-{compiler}-{build_type.lower()}"
        else:
            return f"linux-{compiler}-{build_type.lower()}"
    elif platform.os == "Windows":
        # Existing Windows preset selection
        pass
    else:
        raise ValueError(f"Unsupported platform: {platform.os}")
```

## Consequences

### Positive

1. **Comprehensive Linux Support:** Full Linux CMake preset coverage
2. **CachyOS Optimizations:** CachyOS-specific performance optimizations
3. **Nix Integration:** Nix-aware CMake presets
4. **Clear Organization:** Organized by platform and compiler
5. **Preset Inheritance:** Reduces duplication
6. **Consistent Naming:** Clear naming convention
7. **Debug/Release:** Separate debug and release presets
8. **Multiple Compilers:** Support for GCC and Clang
9. **C++23 Support:** C++23 standard support
10. **Toolchain Integration:** Integration with CMake toolchains

### Negative

1. **Preset Proliferation:** Many presets increase complexity
2. **Maintenance Burden:** More presets to maintain
3. **Preset Selection:** Complex preset selection logic
4. **Documentation Burden:** Need to document all presets
5. **Testing Burden:** Need to test all presets
6. **Version Updates:** Need to update compiler versions
7. **Distribution Differences:** Different Linux distributions may need different presets
8. **Preset Conflicts:** Potential conflicts between presets

### Neutral

1. **Preset Inheritance:** Need to manage preset inheritance
2. **Preset Naming:** Need consistent naming convention
3. **Preset Documentation:** Need to document preset usage
4. **Preset Updates:** Need to update presets when compilers change

## Alternatives Considered

### Alternative 1: Single Linux Preset

**Description:** Use single Linux preset for all compilers

**Pros:**
- Fewer presets
- Simpler maintenance
- Less complexity

**Cons:**
- No compiler-specific optimizations
- No CachyOS optimizations
- No Nix integration
- Poor performance
- Not flexible

**Rejected:** No compiler-specific optimizations, poor performance

### Alternative 2: Dynamic Preset Generation

**Description:** Generate presets dynamically based on environment

**Pros:**
- Fewer static presets
- More flexible
- Adapts to environment

**Cons:**
- Complex to implement
- Harder to debug
- Less predictable
- More runtime overhead
- Not standard CMake practice

**Rejected:** Too complex, not standard practice

### Alternative 3: Environment Variables Only

**Description:** Use environment variables instead of presets

**Pros:**
- No presets needed
- Simple configuration
- Flexible

**Cons:**
- Not reproducible
- Hard to share
- No version pinning
- Not standard CMake practice
- Hard to maintain

**Rejected:** Not reproducible, not standard practice

### Alternative 4: Minimal Linux Presets

**Description:** Add only basic Linux presets, no CachyOS or Nix

**Pros:**
- Fewer presets
- Simpler maintenance
- Faster implementation

**Cons:**
- No CachyOS optimizations
- No Nix integration
- Poor performance on CachyOS
- Not aligned with Linux expansion goals

**Rejected:** No CachyOS optimizations, not aligned with goals

## Related ADRs

- [ADR-005: CMake Presets for cross-platform configuration](ADR-005-cmake-presets-cross-platform-configuration.md)
- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)

## Threat Model References

- **TM-LX-008: CMake Configuration Security** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - CMake injection attacks
  - Preset manipulation
  - Environment variable leakage
  - Mitigation: Validate presets, use secure defaults, avoid exposing sensitive data

## References

- [CMake Presets Documentation](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
- [CMake Toolchains](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)
- [CachyOS Compiler Flags](https://wiki.cachyos.org/)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
