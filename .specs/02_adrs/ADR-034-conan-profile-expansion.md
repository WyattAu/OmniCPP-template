# ADR-034: Conan Profile Expansion

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Conan Configuration for Linux

---

## Context

The OmniCPP Template project uses Conan as the primary package manager for C++ dependencies (see [ADR-001](ADR-001-multi-package-manager-strategy.md)). The current Conan profiles ([`conan/profiles/`](../../conan/profiles:1)) are primarily Windows-centric, with profiles for MSVC, MSVC-clang, MinGW-GCC, and MinGW-Clang.

### Current State

**Existing Profiles:**
- [`msvc`](../../conan/profiles/msvc:1) - MSVC compiler
- [`msvc-debug`](../../conan/profiles/msvc-debug:1) - MSVC debug configuration
- [`msvc-release`](../../conan/profiles/msvc-release:1) - MSVC release configuration
- [`clang-msvc`](../../conan/profiles/clang-msvc:1) - Clang with MSVC runtime
- [`clang-msvc-debug`](../../conan/profiles/clang-msvc-debug:1) - Clang debug configuration
- [`clang-msvc-release`](../../conan/profiles/clang-msvc-release:1) - Clang release configuration
- [`mingw-gcc-release`](../../conan/profiles/mingw-gcc-release:1) - MinGW GCC release
- [`mingw-clang-debug`](../../conan/profiles/mingw-clang-debug:1) - MinGW Clang debug
- [`mingw-clang-release`](../../conan/profiles/mingw-clang-release:1) - MinGW Clang release
- [`gcc-mingw-ucrt`](../../conan/profiles/gcc-mingw-ucrt:1) - GCC MinGW UCRT
- [`emscripten`](../../conan/profiles/emscripten:1) - Emscripten WASM
- [`test_profile`](../../conan/profiles/test_profile:1) - Test profile
- [`test_validate`](../../conan/profiles/test_validate:1) - Validation profile

### Linux Expansion Requirements

The Linux expansion requires Conan profiles for:

1. **GCC Profiles:** GCC compiler on Linux
2. **Clang Profiles:** Clang compiler on Linux
3. **CachyOS Profiles:** CachyOS-specific configurations
4. **Nix Profiles:** Nix environment configurations
5. **Debug/Release Variants:** Debug and release configurations
6. **Build Type Variants:** Debug, Release, RelWithDebInfo, MinSizeRel
7. **C++ Standard:** C++23 support
8. **Toolchain Integration:** Integration with CMake toolchains

### Challenges

1. **Profile Proliferation:** Many profiles increase complexity
2. **Maintenance Burden:** More profiles to maintain
3. **Profile Inheritance:** Need to manage profile inheritance
4. **Compiler Versions:** Different GCC and Clang versions
5. **Distribution Differences:** Different Linux distributions
6. **Nix Integration:** Nix-provided toolchains
7. **CachyOS Optimizations:** CachyOS-specific flags
8. **Profile Naming:** Consistent naming convention

## Decision

Create comprehensive Linux Conan profiles with clear organization and inheritance.

### 1. Profile Organization

Organize profiles by platform and compiler:

```bash
conan/profiles/
├── windows/
│   ├── msvc
│   ├── msvc-debug
│   ├── msvc-release
│   ├── clang-msvc
│   ├── clang-msvc-debug
│   ├── clang-msvc-release
│   ├── mingw-gcc
│   ├── mingw-gcc-release
│   ├── mingw-clang
│   ├── mingw-clang-debug
│   └── mingw-clang-release
├── linux/
│   ├── gcc
│   ├── gcc-debug
│   ├── gcc-release
│   ├── clang
│   ├── clang-debug
│   ├── clang-release
│   ├── cachyos-gcc
│   ├── cachyos-gcc-debug
│   ├── cachyos-gcc-release
│   ├── cachyos-clang
│   ├── cachyos-clang-debug
│   └── cachyos-clang-release
└── emscripten/
    └── emscripten
```

### 2. Base Linux GCC Profile

Create base GCC profile:

```ini
# conan/profiles/linux/gcc
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=gcc
CXX=g++
```

### 3. GCC Debug Profile

Create GCC debug profile:

```ini
# conan/profiles/linux/gcc-debug
include(linux/gcc)

[settings]
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-g -O0 -DDEBUG
CXXFLAGS=-g -O0 -DDEBUG
```

### 4. GCC Release Profile

Create GCC release profile:

```ini
# conan/profiles/linux/gcc-release
include(linux/gcc)

[settings]
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-O3 -DNDEBUG
CXXFLAGS=-O3 -DNDEBUG
```

### 5. Base Linux Clang Profile

Create base Clang profile:

```ini
# conan/profiles/linux/clang
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Release

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=clang
CXX=clang++
```

### 6. Clang Debug Profile

Create Clang debug profile:

```ini
# conan/profiles/linux/clang-debug
include(linux/clang)

[settings]
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-g -O0 -DDEBUG
CXXFLAGS=-g -O0 -DDEBUG
```

### 7. Clang Release Profile

Create Clang release profile:

```ini
# conan/profiles/linux/clang-release
include(linux/clang)

[settings]
build_type=Release

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-O3 -DNDEBUG
CXXFLAGS=-O3 -DNDEBUG
```

### 8. CachyOS GCC Profile

Create CachyOS-specific GCC profile with optimizations:

```ini
# conan/profiles/linux/cachyos-gcc
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined
```

### 9. CachyOS GCC Debug Profile

Create CachyOS GCC debug profile:

```ini
# conan/profiles/linux/cachyos-gcc-debug
include(linux/cachyos-gcc)

[settings]
build_type=Debug

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-march=native -g -O0 -DDEBUG
CXXFLAGS=-march=native -g -O0 -DDEBUG
```

### 10. CachyOS GCC Release Profile

Create CachyOS GCC release profile with optimizations:

```ini
# conan/profiles/linux/cachyos-gcc-release
include(linux/cachyos-gcc)

[settings]
build_type=Release

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -flto
```

### 11. CachyOS Clang Profile

Create CachyOS-specific Clang profile:

```ini
# conan/profiles/linux/cachyos-clang
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Release

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined
```

### 12. CachyOS Clang Debug Profile

Create CachyOS Clang debug profile:

```ini
# conan/profiles/linux/cachyos-clang-debug
include(linux/cachyos-clang)

[settings]
build_type=Debug

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-march=native -g -O0 -DDEBUG
CXXFLAGS=-march=native -g -O0 -DDEBUG
```

### 13. CachyOS Clang Release Profile

Create CachyOS Clang release profile:

```ini
# conan/profiles/linux/cachyos-clang-release
include(linux/cachyos-clang)

[settings]
build_type=Release

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -flto
```

### 14. Nix GCC Profile

Create Nix-specific GCC profile:

```ini
# conan/profiles/linux/nix-gcc
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux

[buildenv]
CC=gcc
CXX=g++
NIX_STORE=/nix/store
```

### 15. Profile Selection Logic

Implement profile selection in OmniCppController.py:

```python
def select_conan_profile(
    platform: PlatformInfo,
    compiler: str,
    build_type: str
) -> str:
    """Select appropriate Conan profile based on platform and compiler."""

    if platform.os == "Linux":
        if platform.is_cachyos:
            return f"linux/cachyos-{compiler}-{build_type.lower()}"
        elif platform.is_nix:
            return f"linux/nix-{compiler}-{build_type.lower()}"
        else:
            return f"linux/{compiler}-{build_type.lower()}"
    elif platform.os == "Windows":
        # Existing Windows profile selection
        pass
    else:
        raise ValueError(f"Unsupported platform: {platform.os}")
```

## Consequences

### Positive

1. **Comprehensive Linux Support:** Full Linux Conan profile coverage
2. **CachyOS Optimizations:** CachyOS-specific performance optimizations
3. **Nix Integration:** Nix-aware Conan profiles
4. **Clear Organization:** Organized by platform and compiler
5. **Profile Inheritance:** Reduces duplication
6. **Consistent Naming:** Clear naming convention
7. **Debug/Release:** Separate debug and release profiles
8. **Multiple Compilers:** Support for GCC and Clang
9. **C++23 Support:** C++23 standard support
10. **Toolchain Integration:** Integration with CMake toolchains

### Negative

1. **Profile Proliferation:** Many profiles increase complexity
2. **Maintenance Burden:** More profiles to maintain
3. **Profile Selection:** Complex profile selection logic
4. **Documentation Burden:** Need to document all profiles
5. **Testing Burden:** Need to test all profiles
6. **Version Updates:** Need to update compiler versions
7. **Distribution Differences:** Different Linux distributions may need different profiles
8. **Profile Conflicts:** Potential conflicts between profiles

### Neutral

1. **Profile Inheritance:** Need to manage profile inheritance
2. **Profile Naming:** Need consistent naming convention
3. **Profile Documentation:** Need to document profile usage
4. **Profile Updates:** Need to update profiles when compilers change

## Alternatives Considered

### Alternative 1: Single Linux Profile

**Description:** Use single Linux profile for all compilers

**Pros:**
- Fewer profiles
- Simpler maintenance
- Less complexity

**Cons:**
- No compiler-specific optimizations
- No CachyOS optimizations
- No Nix integration
- Poor performance
- Not flexible

**Rejected:** No compiler-specific optimizations, poor performance

### Alternative 2: Dynamic Profile Generation

**Description:** Generate profiles dynamically based on environment

**Pros:**
- Fewer static profiles
- More flexible
- Adapts to environment

**Cons:**
- Complex to implement
- Harder to debug
- Less predictable
- More runtime overhead
- Not standard Conan practice

**Rejected:** Too complex, not standard practice

### Alternative 3: Environment Variables Only

**Description:** Use environment variables instead of profiles

**Pros:**
- No profiles needed
- Simple configuration
- Flexible

**Cons:**
- Not reproducible
- Hard to share
- No version pinning
- Not standard Conan practice
- Hard to maintain

**Rejected:** Not reproducible, not standard practice

### Alternative 4: Minimal Linux Profiles

**Description:** Add only basic Linux profiles, no CachyOS or Nix

**Pros:**
- Fewer profiles
- Simpler maintenance
- Faster implementation

**Cons:**
- No CachyOS optimizations
- No Nix integration
- Poor performance on CachyOS
- Not aligned with Linux expansion goals

**Rejected:** No CachyOS optimizations, not aligned with goals

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-031: Linux-Specific Multi-Package Manager Strategy](ADR-031-linux-multi-package-manager-strategy.md)

## Threat Model References

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)
- **TM-004: Dependency Confusion Attack** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:412)

Mitigation:
- Use lock files for all profiles
- Pin exact versions in profiles
- Verify package signatures
- Use private Conan repository
- Implement dependency allowlist

## References

- [Conan Profiles Documentation](https://docs.conan.io/en/latest/reference/profiles.html)
- [Conan Linux Guide](https://docs.conan.io/en/latest/howtos/cross_compilation/linux_to_windows.html)
- [CachyOS Compiler Flags](https://wiki.cachyos.org/)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
