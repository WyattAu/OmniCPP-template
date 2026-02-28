# Conan Linux Profiles

**Version:** 1.0.0  
**Last Updated:** 2026-01-28  
**Project:** OmniCPP-Template  
**References:** [ADR-031](../.specs/02_adrs/ADR-031-conan-linux-profiles.md) | [REQ-008-004](../.specs/04_future_state/reqs/REQ-008-documentation.md)

---

## Table of Contents

1. [Introduction to Conan Linux Profiles](#introduction-to-conan-linux-profiles)
2. [Profile Overview](#profile-overview)
3. [GCC Linux Profiles](#gcc-linux-profiles)
4. [Clang Linux Profiles](#clang-linux-profiles)
5. [CachyOS Profiles](#cachyos-profiles)
6. [Profile Usage Examples](#profile-usage-examples)
7. [Profile Best Practices](#profile-best-practices)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## Introduction to Conan Linux Profiles

Conan profiles are configuration files that define build settings for different compilers, platforms, and build types. The OmniCPP-Template project includes a comprehensive set of Linux profiles for GCC and Clang compilers, including specialized profiles for CachyOS.

### What is a Conan Profile?

A Conan profile is an INI-formatted configuration file that specifies:

- **Settings:** Compiler, OS, architecture, build type, C++ standard
- **Configuration (conf):** Toolchain settings, generator options, compiler flags
- **Options:** Package-specific options (e.g., shared vs static libraries)
- **Build Environment:** Environment variables for the build process

### Why Use Profiles?

Profiles provide several benefits:

1. **Reproducibility:** Consistent build configurations across environments
2. **Portability:** Share build settings between team members
3. **Flexibility:** Easy switching between compilers and build types
4. **Optimization:** Platform-specific optimizations (e.g., CachyOS)
5. **Integration:** Seamless integration with CMake toolchain generation

### Profile Location

All Conan Linux profiles are located in the [`conan/profiles/`](../conan/profiles/) directory:

```
conan/profiles/
├── gcc-linux              # GCC release profile
├── gcc-linux-debug        # GCC debug profile
├── clang-linux            # Clang release profile
├── clang-linux-debug      # Clang debug profile
├── cachyos                # CachyOS GCC release profile
├── cachyos-debug          # CachyOS GCC debug profile
├── cachyos-clang          # CachyOS Clang release profile
└── cachyos-clang-debug    # CachyOS Clang debug profile
```

---

## Profile Overview

### Available Profiles

| Profile | Compiler | Build Type | C++ Standard | C++ Library | Description |
|---------|-----------|-------------|--------------|--------------|-------------|
| [`gcc-linux`](#gcc-linux-profile) | GCC 13 | Release | C++23 | libstdc++11 | Standard GCC release build |
| [`gcc-linux-debug`](#gcc-linux-debug-profile) | GCC 13 | Debug | C++23 | libstdc++11 | GCC debug build with symbols |
| [`clang-linux`](#clang-linux-profile) | Clang 21 | Release | C++23 | libc++ | Standard Clang release build |
| [`clang-linux-debug`](#clang-linux-debug-profile) | Clang 19 | Debug | C++23 | libc++ | Clang debug build with symbols |
| [`cachyos`](#cachyos-profile) | GCC 13 | Release | C++23 | libstdc++11 | CachyOS optimized GCC release |
| [`cachyos-debug`](#cachyos-debug-profile) | GCC 13 | Debug | C++23 | libstdc++11 | CachyOS GCC debug with hardening |
| [`cachyos-clang`](#cachyos-clang-profile) | Clang 19 | Release | C++23 | libc++ | CachyOS optimized Clang release |
| [`cachyos-clang-debug`](#cachyos-clang-debug-profile) | Clang 19 | Debug | C++23 | libc++ | CachyOS Clang debug with hardening |

### Profile Selection Guide

| Use Case | Recommended Profile |
|----------|-------------------|
| Standard Linux development (Ubuntu/Debian) | `gcc-linux` or `gcc-linux-debug` |
| Modern C++ development with Clang | `clang-linux` or `clang-linux-debug` |
| High-performance builds on CachyOS | `cachyos` or `cachyos-clang` |
| Debugging with security hardening | `cachyos-debug` or `cachyos-clang-debug` |
| Maximum performance optimization | `cachyos` or `cachyos-clang` |

---

## GCC Linux Profiles

### gcc-linux Profile

The [`gcc-linux`](../conan/profiles/gcc-linux) profile provides a standard GCC-based build configuration for Linux.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
compiler.cppstd=23
build_type=Release

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}

[options]
vulkan/*:shared=True

[buildenv]
CC=gcc
CXX=g++
```

#### Features

- **Compiler:** GCC 13 with C++23 support
- **C++ Library:** libstdc++11 (GNU C++ standard library)
- **Build Type:** Release (optimized)
- **Generator:** Ninja (fast parallel builds)
- **Vulkan:** Shared libraries enabled

#### Usage

```bash
# Install dependencies with gcc-linux profile
conan install . --profile gcc-linux

# Build with gcc-linux profile
conan build . --profile gcc-linux
```

#### When to Use

- Standard Linux development on Ubuntu/Debian/Fedora
- Projects requiring GNU C++ standard library compatibility
- General-purpose C++ development
- CI/CD pipelines with GCC toolchain

---

### gcc-linux-debug Profile

The [`gcc-linux-debug`](../conan/profiles/gcc-linux-debug) profile provides a GCC-based debug build configuration.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
compiler.cppstd=23
build_type=Debug

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}

[options]
vulkan/*:shared=True

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-g -O0 -DDEBUG
CXXFLAGS=-g -O0 -DDEBUG
```

#### Features

- **Compiler:** GCC 13 with C++23 support
- **Build Type:** Debug with full symbols
- **Debug Flags:**
  - `-g`: Generate debug information (DWARF format)
  - `-O0`: No optimization for better debugging
  - `-DDEBUG`: Enable debug-specific code paths
- **C++ Library:** libstdc++11
- **Generator:** Ninja

#### Usage

```bash
# Install dependencies with gcc-linux-debug profile
conan install . --profile gcc-linux-debug

# Build with gcc-linux-debug profile
conan build . --profile gcc-linux-debug
```

#### When to Use

- Active development and debugging
- Unit testing with debug builds
- Profiling and performance analysis
- Catching runtime errors with debug symbols

---

## Clang Linux Profiles

### clang-linux Profile

The [`clang-linux`](../conan/profiles/clang-linux) profile provides a standard Clang-based build configuration for Linux.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=21.1.6
compiler.libcxx=libc++
build_type=Release

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:user_toolchain=["${PROJECT_ROOT}/cmake/toolchains/clang-linux.cmake"]

[buildenv]
CC=clang
CXX=clang++
```

#### Features

- **Compiler:** Clang 21.1.6 with C++23 support
- **C++ Library:** libc++ (LLVM's C++ standard library)
- **Build Type:** Release (optimized)
- **Toolchain:** Custom Clang toolchain file
- **Generator:** Ninja (via toolchain file)

#### Usage

```bash
# Install dependencies with clang-linux profile
conan install . --profile clang-linux

# Build with clang-linux profile
conan build . --profile clang-linux
```

#### When to Use

- Modern C++ development with Clang
- Projects requiring libc++ compatibility
- Better diagnostics and error messages
- Static analysis integration

---

### clang-linux-debug Profile

The [`clang-linux-debug`](../conan/profiles/clang-linux-debug) profile provides a Clang-based debug build configuration.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
compiler.cppstd=23
build_type=Debug

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}

[options]
vulkan/*:shared=True

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-g -O0 -DDEBUG
CXXFLAGS=-g -O0 -DDEBUG
```

#### Features

- **Compiler:** Clang 19 with C++23 support
- **Build Type:** Debug with full symbols
- **Debug Flags:**
  - `-g`: Generate debug information (DWARF format)
  - `-O0`: No optimization for better debugging
  - `-DDEBUG`: Enable debug-specific code paths
- **C++ Library:** libc++
- **Generator:** Ninja

#### Usage

```bash
# Install dependencies with clang-linux-debug profile
conan install . --profile clang-linux-debug

# Build with clang-linux-debug profile
conan build . --profile clang-linux-debug
```

#### When to Use

- Active development and debugging with Clang
- Unit testing with debug builds
- Advanced diagnostics with AddressSanitizer/ThreadSanitizer
- Memory leak detection with LeakSanitizer

---

## CachyOS Profiles

### cachyos Profile

The [`cachyos`](../conan/profiles/cachyos) profile provides an optimized GCC build configuration for CachyOS.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
compiler.cppstd=23
build_type=Release

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.build:cxxflags=-march=native -O3 -flto -DNDEBUG
tools.build:cflags=-march=native -O3 -flto -DNDEBUG
tools.build:sharedlinkflags=-Wl,--as-needed -Wl,--no-undefined -flto
tools.build:exelinkflags=-Wl,--as-needed -Wl,--no-undefined -flto

[options]
vulkan/*:shared=True

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -flto
```

#### Features

- **Compiler:** GCC 13 with C++23 support
- **Build Type:** Release with maximum optimization
- **Optimization Flags:**
  - `-march=native`: Optimize for host CPU architecture
  - `-O3`: Maximum optimization level (includes auto-vectorization)
  - `-flto`: Link-Time Optimization for cross-module optimization
  - `-DNDEBUG`: Disable assertions for release builds
- **Linker Flags:**
  - `--as-needed`: Only link libraries that are actually used
  - `--no-undefined`: Fail if any undefined symbols remain
  - `-flto`: Apply LTO during linking
- **C++ Library:** libstdc++11
- **Generator:** Ninja

#### Flag Explanations

| Flag | Purpose | Effect |
|-------|---------|--------|
| `-march=native` | Host-specific optimization | Generates code optimized for your specific CPU architecture |
| `-O3` | Maximum optimization | Enables all optimization flags including auto-vectorization and loop unrolling |
| `-flto` | Link-Time Optimization | Optimizes across translation units during linking for better performance |
| `-DNDEBUG` | Disable assertions | Removes `assert()` calls for release builds |
| `--as-needed` | Link only used libraries | Reduces binary size by removing unused dependencies |
| `--no-undefined` | Fail on undefined symbols | Ensures all symbols are resolved at link time |

#### Usage

```bash
# Install dependencies with cachyos profile
conan install . --profile cachyos

# Build with cachyos profile
conan build . --profile cachyos
```

#### When to Use

- High-performance builds on CachyOS
- Gaming and real-time applications
- CPU-intensive workloads
- Production releases requiring maximum performance

---

### cachyos-debug Profile

The [`cachyos-debug`](../conan/profiles/cachyos-debug) profile provides a GCC debug build configuration with security hardening for CachyOS.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
compiler.cppstd=23
build_type=Debug

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.build:cxxflags=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
tools.build:cflags=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
tools.build:sharedlinkflags=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now
tools.build:exelinkflags=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now

[options]
vulkan/*:shared=True

[buildenv]
CC=gcc
CXX=g++
CFLAGS=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
CXXFLAGS=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now
```

#### Features

- **Compiler:** GCC 13 with C++23 support
- **Build Type:** Debug with full symbols and security hardening
- **Debug Flags:**
  - `-march=native`: Optimize for host CPU architecture
  - `-g`: Generate debug information
  - `-O0`: No optimization for better debugging
  - `-DDEBUG`: Enable debug-specific code paths
- **Security Hardening Flags:**
  - `-fstack-protector-strong`: Stack protection against buffer overflows
  - `-D_FORTIFY_SOURCE=2`: Runtime buffer overflow detection
- **Linker Flags:**
  - `--as-needed`: Only link libraries that are actually used
  - `--no-undefined`: Fail if any undefined symbols remain
  - `-z,relro`: Relocation read-only after load
  - `-z,now`: Bind all symbols at load time (no lazy binding)
- **C++ Library:** libstdc++11
- **Generator:** Ninja

#### Security Flag Explanations

| Flag | Purpose | Effect |
|-------|---------|--------|
| `-fstack-protector-strong` | Stack protection | Adds stack canaries to detect and prevent buffer overflows |
| `-D_FORTIFY_SOURCE=2` | Runtime buffer checks | Adds runtime checks for buffer operations to prevent overflows |
| `-z,relro` | Relocation read-only | Makes some sections read-only after relocation to prevent certain attacks |
| `-z,now` | Immediate symbol binding | Binds all symbols at load time instead of lazy binding |

#### Usage

```bash
# Install dependencies with cachyos-debug profile
conan install . --profile cachyos-debug

# Build with cachyos-debug profile
conan build . --profile cachyos-debug
```

#### When to Use

- Debugging with security hardening on CachyOS
- Security-focused development
- Testing for buffer overflow vulnerabilities
- Production debugging with enhanced security

---

### cachyos-clang Profile

The [`cachyos-clang`](../conan/profiles/cachyos-clang) profile provides an optimized Clang build configuration for CachyOS.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
compiler.cppstd=23
build_type=Release

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.build:cxxflags=-march=native -O3 -flto -DNDEBUG
tools.build:cflags=-march=native -O3 -flto -DNDEBUG
tools.build:sharedlinkflags=-Wl,--as-needed -Wl,--no-undefined -flto
tools.build:exelinkflags=-Wl,--as-needed -Wl,--no-undefined -flto

[options]
vulkan/*:shared=True

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-march=native -O3 -flto -DNDEBUG
CXXFLAGS=-march=native -O3 -flto -DNDEBUG
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -flto
```

#### Features

- **Compiler:** Clang 19 with C++23 support
- **Build Type:** Release with maximum optimization
- **Optimization Flags:**
  - `-march=native`: Optimize for host CPU architecture
  - `-O3`: Maximum optimization level
  - `-flto`: Link-Time Optimization
  - `-DNDEBUG`: Disable assertions
- **Linker Flags:**
  - `--as-needed`: Only link used libraries
  - `--no-undefined`: Fail on undefined symbols
  - `-flto`: Apply LTO during linking
- **C++ Library:** libc++ (LLVM's C++ standard library)
- **Generator:** Ninja

#### Usage

```bash
# Install dependencies with cachyos-clang profile
conan install . --profile cachyos-clang

# Build with cachyos-clang profile
conan build . --profile cachyos-clang
```

#### When to Use

- High-performance builds on CachyOS with Clang
- Projects requiring libc++ compatibility
- Modern C++ development with advanced diagnostics
- Performance-critical applications

---

### cachyos-clang-debug Profile

The [`cachyos-clang-debug`](../conan/profiles/cachyos-clang-debug) profile provides a Clang debug build configuration with security hardening for CachyOS.

#### Configuration

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
compiler.cppstd=23
build_type=Debug

[conf]
tools.cmake.cmaketoolchain:system_name=Linux
tools.cmake.cmaketoolchain:generator=Ninja
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.build:cxxflags=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
tools.build:cflags=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
tools.build:sharedlinkflags=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now
tools.build:exelinkflags=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now

[options]
vulkan/*:shared=True

[buildenv]
CC=clang
CXX=clang++
CFLAGS=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
CXXFLAGS=-march=native -g -O0 -DDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
LDFLAGS=-Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now
```

#### Features

- **Compiler:** Clang 19 with C++23 support
- **Build Type:** Debug with full symbols and security hardening
- **Debug Flags:**
  - `-march=native`: Optimize for host CPU architecture
  - `-g`: Generate debug information
  - `-O0`: No optimization for better debugging
  - `-DDEBUG`: Enable debug-specific code paths
- **Security Hardening Flags:**
  - `-fstack-protector-strong`: Stack protection
  - `-D_FORTIFY_SOURCE=2`: Runtime buffer checks
- **Linker Flags:**
  - `--as-needed`: Only link used libraries
  - `--no-undefined`: Fail on undefined symbols
  - `-z,relro`: Relocation read-only
  - `-z,now`: Immediate symbol binding
- **C++ Library:** libc++
- **Generator:** Ninja

#### Usage

```bash
# Install dependencies with cachyos-clang-debug profile
conan install . --profile cachyos-clang-debug

# Build with cachyos-clang-debug profile
conan build . --profile cachyos-clang-debug
```

#### When to Use

- Debugging with Clang and security hardening on CachyOS
- Advanced diagnostics with sanitizers (AddressSanitizer, ThreadSanitizer)
- Memory leak detection with LeakSanitizer
- Security-focused development with libc++

---

## Profile Usage Examples

### Basic Usage

#### Installing Dependencies

```bash
# Install dependencies with specific profile
conan install . --profile gcc-linux

# Install with debug profile
conan install . --profile gcc-linux-debug

# Install with CachyOS profile
conan install . --profile cachyos
```

#### Building with Profiles

```bash
# Build with profile
conan build . --profile gcc-linux

# Build with debug profile
conan build . --profile gcc-linux-debug
```

### Combining Profiles

You can combine multiple profiles using the `-pr` or `--profile` flag multiple times:

```bash
# Combine base profile with custom settings
conan install . --profile gcc-linux --profile:settings=build_type=RelWithDebInfo

# Combine profiles using profile host/build pattern
conan install . --profile:build=gcc-linux --profile:host=gcc-linux-debug
```

### Using with CMake Presets

Conan profiles integrate seamlessly with CMake presets defined in [`CMakePresets.json`](../CMakePresets.json):

```bash
# Configure with CMake preset (uses associated Conan profile)
cmake --preset generic-linux-x86_64-gcc-15-debug

# Build with preset
cmake --build --preset generic-linux-x86_64-gcc-15-debug
```

### Using with Python Controller

The [`OmniCppController.py`](../OmniCppController.py) script supports Conan profiles:

```bash
# Build with specific profile
python OmniCppController.py build standalone "Conan install" default Debug --profile gcc-linux

# Build with CachyOS profile
python OmniCppController.py build standalone "Conan install" default Debug --profile cachyos
```

### Using with Makefile

The project's Makefile supports profile selection:

```bash
# Install dependencies with specific profile
make conan-install PROFILE=gcc-linux

# Install with debug profile
make conan-install PROFILE=gcc-linux-debug
```

---

## Profile Best Practices

### 1. Profile Selection

Choose the appropriate profile based on your use case:

| Scenario | Recommended Profile | Reason |
|----------|-------------------|---------|
| Development | `gcc-linux-debug` or `clang-linux-debug` | Full debug symbols, no optimization |
| Testing | `gcc-linux-debug` or `clang-linux-debug` | Debug builds enable better test coverage |
| Release | `gcc-linux` or `clang-linux` | Optimized builds for production |
| Performance | `cachyos` or `cachyos-clang` | Maximum optimization with LTO |
| Security | `cachyos-debug` or `cachyos-clang-debug` | Debug with security hardening |

### 2. Profile Customization

Create custom profiles by extending existing ones:

```ini
# conan/profiles/custom-profile
include(gcc-linux)

[settings]
build_type=RelWithDebInfo

[conf]
tools.build:cxxflags=-march=haswell -O2
```

### 3. Profile Validation

Validate profiles before use:

```bash
# Validate profile syntax
conan profile show gcc-linux

# Test profile with a simple package
conan install hello/1.0@ --profile gcc-linux
```

### 4. Profile Management

List and manage available profiles:

```bash
# List all profiles
conan profile list

# Show profile details
conan profile show gcc-linux

# Remove profile
conan profile remove custom-profile
```

### 5. Profile Versioning

Commit profiles to version control for reproducibility:

```bash
# Add profiles to git
git add conan/profiles/

# Commit with descriptive message
git commit -m "Add GCC 13 Linux profiles with C++23 support"
```

### 6. Profile Documentation

Document custom profiles with inline comments:

```ini
# conan/profiles/custom-profile
# Custom profile for specific use case
# Author: Your Name
# Date: 2026-01-28
#
# This profile configures:
# - Custom compiler flags for specific optimization
# - Security hardening for production builds
```

### 7. Profile Testing

Test profiles across different environments:

```bash
# Test on local machine
conan install . --profile gcc-linux

# Test in CI/CD
conan install . --profile gcc-linux --build=missing
```

### 8. Profile Updates

Keep profiles updated with compiler versions:

```ini
# Update compiler version when new release is available
[settings]
compiler.version=14  # Updated from 13 to 14
```

---

## Security Considerations

### Threat Model: TM-LX-004 (Linux Build System Security)

According to the [Threat Model Analysis](../.specs/03_threat_model/analysis.md), Linux build systems face several security risks. When using Conan profiles, consider the following security best practices:

### 1. Profile Integrity

Validate profile contents before use:

```bash
# Check for suspicious patterns in profiles
grep -r "eval\|exec\|curl\|wget" conan/profiles/

# Verify profile syntax
conan profile show gcc-linux
```

### 2. Dependency Security

Use lock files to ensure dependency integrity:

```bash
# Generate lock file
conan lock create conanfile.py --lockfile-out=conan.lock --profile gcc-linux

# Use lock file in builds
conan install . --lockfile=conan.lock --profile gcc-linux
```

### 3. Compiler Flag Validation

Validate compiler flags in profiles:

```python
# Validate compiler flags for security
def validate_compiler_flags(flags):
    dangerous_flags = [
        '-fno-stack-protector',  # Disables stack protection
        '-D_FORTIFY_SOURCE=0',   # Disables buffer checks
        '-U_FORTIFY_SOURCE',      # Undefines fortification
    ]
    for flag in dangerous_flags:
        if flag in flags:
            raise SecurityError(f"Dangerous compiler flag: {flag}")
```

### 4. Environment Variable Security

Validate environment variables in `[buildenv]` section:

```bash
# Check for suspicious environment variables
grep -r "LD_PRELOAD\|LD_LIBRARY_PATH" conan/profiles/
```

### 5. Profile Signing

Consider signing profiles for authenticity:

```bash
# Sign profile
gpg --detach-sign --armor conan/profiles/gcc-linux

# Verify signature
gpg --verify conan/profiles/gcc-linux.asc
```

### 6. Security Hardening in Debug Builds

Debug profiles include security hardening flags:

- `-fstack-protector-strong`: Stack protection against buffer overflows
- `-D_FORTIFY_SOURCE=2`: Runtime buffer overflow detection
- `-z,relro`: Relocation read-only after load
- `-z,now`: Immediate symbol binding

These flags are enabled in `cachyos-debug` and `cachyos-clang-debug` profiles.

### 7. Dependency Pinning

Pin exact dependency versions in profiles:

```ini
# Pin exact versions instead of ranges
[settings]
compiler.version=13  # Exact version, not 13.x

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
```

### 8. Regular Security Audits

Perform regular security audits of profiles:

```bash
# Audit profiles for security issues
./scripts/security/audit_profiles.sh

# Check for outdated compiler versions
grep -r "compiler.version" conan/profiles/
```

---

## Troubleshooting

### Common Issues

#### 1. "Profile not found" Error

**Symptoms:** Conan fails with "Profile not found" error

**Solutions:**
```bash
# Check profile location
ls conan/profiles/

# Verify profile name
conan profile list

# Use full path if needed
conan install . --profile ./conan/profiles/gcc-linux
```

#### 2. "Compiler not found" Error

**Symptoms:** Build fails with "compiler not found" error

**Solutions:**
```bash
# Check compiler availability
which gcc
which clang

# Verify compiler version
gcc --version
clang --version

# Update profile with correct version
[settings]
compiler.version=13  # Update to match installed version
```

#### 3. "Architecture mismatch" Error

**Symptoms:** Build fails with architecture mismatch error

**Solutions:**
```bash
# Check system architecture
uname -m

# Update profile with correct architecture
[settings]
arch=x86_64  # or arm64 for ARM systems
```

#### 4. "C++ standard not supported" Error

**Symptoms:** Build fails with C++ standard not supported error

**Solutions:**
```bash
# Check compiler C++ support
gcc --version | grep C++
clang --version | grep C++

# Update profile with supported standard
[settings]
compiler.cppstd=20  # Downgrade if C++23 not supported
```

#### 5. "Linker errors" with LTO

**Symptoms:** Build fails with linker errors when using `-flto`

**Solutions:**
```bash
# Disable LTO temporarily
[conf]
tools.build:cxxflags=-march=native -O3 -DNDEBUG  # Remove -flto

# Use gold linker for better LTO support
[buildenv]
LDFLAGS=-fuse-ld=gold -Wl,--as-needed
```

### Debug Information

Enable verbose output for troubleshooting:

```bash
# Verbose Conan install
conan install . --profile gcc-linux -v

# Verbose Conan build
conan build . --profile gcc-linux -v

# Show profile configuration
conan profile show gcc-linux
```

### Profile Verification

Verify profile configuration:

```bash
# Show all profile settings
conan profile show gcc-linux

# Test profile with simple package
conan install hello/1.0@ --profile gcc-linux

# Check generated toolchain
ls build/*/generators/
```

### Environment Verification

Verify build environment:

```bash
# Check environment variables
conan install . --profile gcc-linux -e

# Verify compiler in PATH
echo $CC
echo $CXX

# Check CMake toolchain
cat build/*/generators/conan_toolchain.cmake
```

---

## Related Documentation

- [Linux Builds](linux-builds.md) - General Linux build instructions
- [CachyOS Builds](cachyos-builds.md) - CachyOS-specific build instructions
- [Compiler Detection](compiler-detection.md) - Compiler detection and configuration
- [Linux Troubleshooting](linux-troubleshooting.md) - Linux-specific troubleshooting

---

## References

- [ADR-031: Conan Linux Profiles](../.specs/02_adrs/ADR-031-conan-linux-profiles.md) - Architecture Decision Record
- [REQ-008-004: Documentation](../.specs/04_future_state/reqs/REQ-008-documentation.md) - Documentation requirements
- [TM-LX-004: Linux Build System Security](../.specs/03_threat_model/analysis.md) - Security threat model
- [Conan Documentation](https://docs.conan.io/) - Official Conan documentation
- [Conan Profiles Guide](https://docs.conan.io/en/latest/reference/profiles.html) - Conan profiles reference
