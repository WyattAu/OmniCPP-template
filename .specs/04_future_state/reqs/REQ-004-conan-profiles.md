# REQ-004: Conan Profiles

**Requirement ID:** REQ-004
**Title:** Conan Profiles
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

Conan profiles shall be created for Linux, GCC, Clang, and CachyOS to support comprehensive Linux builds with Conan package manager.

### Overview

The system shall:
1. Create gcc-linux profile
2. Create gcc-linux-debug profile
3. Create clang-linux profile
4. Create clang-linux-debug profile
5. Create cachyos profile
6. Create cachyos-debug profile
7. Create cachyos-clang profile
8. Create cachyos-clang-debug profile

---

## REQ-004-001: Create gcc-linux Profile

### Description

A Conan profile shall be created for GCC on Linux with release configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/gcc-linux`](../../conan/profiles/gcc-linux:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=gcc`
5. Set `compiler.version=13`
6. Set `compiler.libcxx=libstdc++11`
7. Set `build_type=Release`
8. Set `tools.build:compiler_executables` to gcc and g++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Add comments explaining profile usage

### Acceptance Criteria

- [ ] [`conan/profiles/gcc-linux`](../../conan/profiles/gcc-linux:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=gcc`
- [ ] Profile has `compiler.version=13`
- [ ] Profile has `compiler.libcxx=libstdc++11`
- [ ] Profile has `build_type=Release`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has usage comments

### Priority

**High** - GCC Linux profile is required for Linux builds.

### Dependencies

- None

### Related ADRs

- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test GCC Linux Profile**
   - **Description:** Verify GCC Linux profile works
   - **Steps:**
     1. Run `conan install . --profile gcc-linux`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-002: Create gcc-linux-debug Profile

### Description

A Conan profile shall be created for GCC on Linux with debug configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/gcc-linux-debug`](../../conan/profiles/gcc-linux-debug:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=gcc`
5. Set `compiler.version=13`
6. Set `compiler.libcxx=libstdc++11`
7. Set `build_type=Debug`
8. Set `tools.build:compiler_executables` to gcc and g++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Add comments explaining profile usage

### Acceptance Criteria

- [ ] [`conan/profiles/gcc-linux-debug`](../../conan/profiles/gcc-linux-debug:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=gcc`
- [ ] Profile has `compiler.version=13`
- [ ] Profile has `compiler.libcxx=libstdc++11`
- [ ] Profile has `build_type=Debug`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has usage comments

### Priority

**High** - GCC Linux debug profile is required for debug builds.

### Dependencies

- REQ-004-001: Create gcc-linux profile

### Related ADRs

- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test GCC Linux Debug Profile**
   - **Description:** Verify GCC Linux debug profile works
   - **Steps:**
     1. Run `conan install . --profile gcc-linux-debug`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-003: Create clang-linux Profile

### Description

A Conan profile shall be created for Clang on Linux with release configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/clang-linux`](../../conan/profiles/clang-linux:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=clang`
5. Set `compiler.version=19`
6. Set `compiler.libcxx=libc++`
7. Set `build_type=Release`
8. Set `tools.build:compiler_executables` to clang and clang++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Add comments explaining profile usage

### Acceptance Criteria

- [ ] [`conan/profiles/clang-linux`](../../conan/profiles/clang-linux:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=clang`
- [ ] Profile has `compiler.version=19`
- [ ] Profile has `compiler.libcxx=libc++`
- [ ] Profile has `build_type=Release`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has usage comments

### Priority

**High** - Clang Linux profile is required for Linux builds.

### Dependencies

- None

### Related ADRs

- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test Clang Linux Profile**
   - **Description:** Verify Clang Linux profile works
   - **Steps:**
     1. Run `conan install . --profile clang-linux`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-004: Create clang-linux-debug Profile

### Description

A Conan profile shall be created for Clang on Linux with debug configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/clang-linux-debug`](../../conan/profiles/clang-linux-debug:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=clang`
5. Set `compiler.version=19`
6. Set `compiler.libcxx=libc++`
7. Set `build_type=Debug`
8. Set `tools.build:compiler_executables` to clang and clang++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Add comments explaining profile usage

### Acceptance Criteria

- [ ] [`conan/profiles/clang-linux-debug`](../../conan/profiles/clang-linux-debug:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=clang`
- [ ] Profile has `compiler.version=19`
- [ ] Profile has `compiler.libcxx=libc++`
- [ ] Profile has `build_type=Debug`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has usage comments

### Priority

**High** - Clang Linux debug profile is required for debug builds.

### Dependencies

- REQ-004-003: Create clang-linux profile

### Related ADRs

- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test Clang Linux Debug Profile**
   - **Description:** Verify Clang Linux debug profile works
   - **Steps:**
     1. Run `conan install . --profile clang-linux-debug`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-005: Create cachyos Profile

### Description

A Conan profile shall be created for CachyOS with GCC and release configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/cachyos`](../../conan/profiles/cachyos:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=gcc`
5. Set `compiler.version=13`
6. Set `compiler.libcxx=libstdc++11`
7. Set `build_type=Release`
8. Set `tools.build:compiler_executables` to gcc and g++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Set `tools.build:cxxflags` to CachyOS-specific flags
11. Add comments explaining CachyOS-specific configuration

### Acceptance Criteria

- [ ] [`conan/profiles/cachyos`](../../conan/profiles/cachyos:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=gcc`
- [ ] Profile has `compiler.version=13`
- [ ] Profile has `compiler.libcxx=libstdc++11`
- [ ] Profile has `build_type=Release`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has CachyOS-specific flags
- [ ] Profile has usage comments

### Priority

**High** - CachyOS profile is required for CachyOS builds.

### Dependencies

- REQ-004-001: Create gcc-linux profile

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test CachyOS Profile**
   - **Description:** Verify CachyOS profile works
   - **Steps:**
     1. Run `conan install . --profile cachyos`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-006: Create cachyos-debug Profile

### Description

A Conan profile shall be created for CachyOS with GCC and debug configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/cachyos-debug`](../../conan/profiles/cachyos-debug:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=gcc`
5. Set `compiler.version=13`
6. Set `compiler.libcxx=libstdc++11`
7. Set `build_type=Debug`
8. Set `tools.build:compiler_executables` to gcc and g++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Set `tools.build:cxxflags` to CachyOS-specific debug flags
11. Add comments explaining CachyOS-specific configuration

### Acceptance Criteria

- [ ] [`conan/profiles/cachyos-debug`](../../conan/profiles/cachyos-debug:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=gcc`
- [ ] Profile has `compiler.version=13`
- [ ] Profile has `compiler.libcxx=libstdc++11`
- [ ] Profile has `build_type=Debug`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has CachyOS-specific flags
- [ ] Profile has usage comments

### Priority

**High** - CachyOS debug profile is required for debug builds.

### Dependencies

- REQ-004-005: Create cachyos profile

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test CachyOS Debug Profile**
   - **Description:** Verify CachyOS debug profile works
   - **Steps:**
     1. Run `conan install . --profile cachyos-debug`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-007: Create cachyos-clang Profile

### Description

A Conan profile shall be created for CachyOS with Clang and release configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/cachyos-clang`](../../conan/profiles/cachyos-clang:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=clang`
5. Set `compiler.version=19`
6. Set `compiler.libcxx=libc++`
7. Set `build_type=Release`
8. Set `tools.build:compiler_executables` to clang and clang++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Set `tools.build:cxxflags` to CachyOS-specific flags
11. Add comments explaining CachyOS-specific configuration

### Acceptance Criteria

- [ ] [`conan/profiles/cachyos-clang`](../../conan/profiles/cachyos-clang:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=clang`
- [ ] Profile has `compiler.version=19`
- [ ] Profile has `compiler.libcxx=libc++`
- [ ] Profile has `build_type=Release`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has CachyOS-specific flags
- [ ] Profile has usage comments

### Priority

**High** - CachyOS Clang profile is required for CachyOS builds.

### Dependencies

- REQ-004-003: Create clang-linux profile

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test CachyOS Clang Profile**
   - **Description:** Verify CachyOS Clang profile works
   - **Steps:**
     1. Run `conan install . --profile cachyos-clang`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## REQ-004-008: Create cachyos-clang-debug Profile

### Description

A Conan profile shall be created for CachyOS with Clang and debug configuration.

### Functional Requirements

The system shall:
1. Create [`conan/profiles/cachyos-clang-debug`](../../conan/profiles/cachyos-clang-debug:1) file
2. Set `os=Linux`
3. Set `arch=x86_64`
4. Set `compiler=clang`
5. Set `compiler.version=19`
6. Set `compiler.libcxx=libc++`
7. Set `build_type=Debug`
8. Set `tools.build:compiler_executables` to clang and clang++
9. Set `tools.cmake.cmaketoolchain:system_name` to Linux
10. Set `tools.build:cxxflags` to CachyOS-specific debug flags
11. Add comments explaining CachyOS-specific configuration

### Acceptance Criteria

- [ ] [`conan/profiles/cachyos-clang-debug`](../../conan/profiles/cachyos-clang-debug:1) file exists
- [ ] Profile has `os=Linux`
- [ ] Profile has `arch=x86_64`
- [ ] Profile has `compiler=clang`
- [ ] Profile has `compiler.version=19`
- [ ] Profile has `compiler.libcxx=libc++`
- [ ] Profile has `build_type=Debug`
- [ ] Profile has compiler executables configured
- [ ] Profile has CMake toolchain configured
- [ ] Profile has CachyOS-specific flags
- [ ] Profile has usage comments

### Priority

**High** - CachyOS Clang debug profile is required for debug builds.

### Dependencies

- REQ-004-007: Create cachyos-clang profile

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test CachyOS Clang Debug Profile**
   - **Description:** Verify CachyOS Clang debug profile works
   - **Steps:**
     1. Run `conan install . --profile cachyos-clang-debug`
     2. Verify profile is loaded
     3. Verify packages are installed
   - **Expected Result:** Profile works correctly

---

## Implementation Notes

### Profile File Structure

#### gcc-linux Profile

```ini
# Conan profile for GCC on Linux (Release)
# Usage: conan install . --profile gcc-linux

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
```

#### gcc-linux-debug Profile

```ini
# Conan profile for GCC on Linux (Debug)
# Usage: conan install . --profile gcc-linux-debug

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux
```

#### clang-linux Profile

```ini
# Conan profile for Clang on Linux (Release)
# Usage: conan install . --profile clang-linux

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
```

#### clang-linux-debug Profile

```ini
# Conan profile for Clang on Linux (Debug)
# Usage: conan install . --profile clang-linux-debug

[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux
```

#### cachyos Profile

```ini
# Conan profile for CachyOS with GCC (Release)
# Usage: conan install . --profile cachyos

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
tools.build:cxxflags=["-march=native", "-O3", "-flto", "-DNDEBUG"]
```

#### cachyos-debug Profile

```ini
# Conan profile for CachyOS with GCC (Debug)
# Usage: conan install . --profile cachyos-debug

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:system_name=Linux
tools.build:cxxflags=["-g", "-O0", "-DDEBUG"]
```

#### cachyos-clang Profile

```ini
# Conan profile for CachyOS with Clang (Release)
# Usage: conan install . --profile cachyos-clang

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
tools.build:cxxflags=["-march=native", "-O3", "-flto", "-DNDEBUG"]
```

#### cachyos-clang-debug Profile

```ini
# Conan profile for CachyOS with Clang (Debug)
# Usage: conan install . --profile cachyos-clang-debug

[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Debug

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:system_name=Linux
tools.build:cxxflags=["-g", "-O0", "-DDEBUG"]
```

### Profile Selection

The system shall automatically select the appropriate profile based on:
- Detected compiler (GCC or Clang)
- Build type (Debug or Release)
- Detected distribution (CachyOS or generic Linux)

### Documentation

Add documentation to [`conan/README.md`](../../conan/README.md:1) explaining:
- Available profiles
- Profile usage
- Profile selection logic
- CachyOS-specific flags

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)
- [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md) - Threat Model Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
