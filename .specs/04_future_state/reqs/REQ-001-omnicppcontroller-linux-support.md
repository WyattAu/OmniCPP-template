# REQ-001: OmniCppController.py Linux Support

**Requirement ID:** REQ-001
**Title:** OmniCppController.py Linux Support
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

The OmniCppController.py build system shall be enhanced to provide comprehensive Linux support, including detection of Linux distributions (with special support for CachyOS), Nix environment integration, package manager detection, CachyOS-specific compiler flag application, and Linux build command generation.

### Overview

The system shall:
1. Detect the Linux distribution and version
2. Specifically detect CachyOS as a special case
3. Detect if running in a Nix shell environment
4. Detect the system package manager (pacman, apt, dnf, etc.)
5. Apply CachyOS-specific compiler optimizations
6. Integrate seamlessly with Nix shell environments
7. Validate the Linux build environment before builds
8. Generate appropriate Linux build commands

---

## REQ-001-001: Detect Linux Distribution

### Description

The system shall detect the Linux distribution and version information by reading system files and parsing distribution-specific metadata.

### Functional Requirements

The system shall:
1. Read `/etc/os-release` file to obtain distribution information
2. Parse distribution ID, name, version, and version ID
3. Support detection of major distributions: Arch Linux, Ubuntu, Fedora, Debian, CentOS, openSUSE
4. Return a structured [`LinuxDistribution`](../linux_expansion_manifest.md:199) object containing:
   - Distribution name (e.g., "Arch Linux", "Ubuntu 22.04")
   - Distribution version
   - Distribution family (arch, debian, fedora, suse)
   - Package manager type
   - CachyOS flag
5. Handle missing or malformed `/etc/os-release` gracefully
6. Log detected distribution information at INFO level
7. Cache detection results for performance

### Acceptance Criteria

- [ ] Function `detect_linux_distribution()` exists in `omni_scripts/platform/linux.py`
- [ ] Returns valid [`LinuxDistribution`](../linux_expansion_manifest.md:199) object for Arch Linux
- [ ] Returns valid [`LinuxDistribution`](../linux_expansion_manifest.md:199) object for Ubuntu
- [ ] Returns valid [`LinuxDistribution`](../linux_expansion_manifest.md:199) object for Fedora
- [ ] Returns valid [`LinuxDistribution`](../linux_expansion_manifest.md:199) object for Debian
- [ ] Returns generic distribution object for unknown distributions
- [ ] Handles missing `/etc/os-release` without crashing
- [ ] Logs distribution detection at INFO level
- [ ] Detection results are cached

### Priority

**Critical** - Distribution detection is foundational for all Linux-specific behavior.

### Dependencies

- None

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- None directly, but supports platform validation

### Test Cases

#### Unit Tests

1. **Test Arch Linux Detection**
   - **Description:** Verify Arch Linux is detected correctly
   - **Steps:**
     1. Mock `/etc/os-release` with Arch Linux content
     2. Call `detect_linux_distribution()`
     3. Verify distribution name is "Arch Linux"
     4. Verify family is "arch"
     5. Verify package manager is "pacman"
   - **Expected Result:** Arch Linux detected correctly

2. **Test Ubuntu Detection**
   - **Description:** Verify Ubuntu is detected correctly
   - **Steps:**
     1. Mock `/etc/os-release` with Ubuntu content
     2. Call `detect_linux_distribution()`
     3. Verify distribution name contains "Ubuntu"
     4. Verify family is "debian"
     5. Verify package manager is "apt"
   - **Expected Result:** Ubuntu detected correctly

3. **Test Missing os-release**
   - **Description:** Verify graceful handling of missing file
   - **Steps:**
     1. Mock `/etc/os-release` as non-existent
     2. Call `detect_linux_distribution()`
     3. Verify returns generic distribution object
     4. Verify no exception is raised
   - **Expected Result:** Generic distribution object returned

---

## REQ-001-002: Detect CachyOS Specifically

### Description

The system shall specifically detect CachyOS as a special case and mark it appropriately in the distribution information.

### Functional Requirements

The system shall:
1. Check for `ID=cachyos` in `/etc/os-release`
2. Check for `ID_LIKE=arch` with CachyOS-specific markers
3. Set `is_cachyos=True` flag in [`LinuxDistribution`](../linux_expansion_manifest.md:199) object
4. Detect CachyOS version if available
5. Log CachyOS detection at INFO level with version information
6. Handle CachyOS detection before generic Arch detection
7. Support detection of CachyOS variants (e.g., CachyOS KDE, CachyOS GNOME)

### Acceptance Criteria

- [ ] CachyOS detection logic exists in `omni_scripts/platform/linux.py`
- [ ] Detects CachyOS when `ID=cachyos` is present
- [ ] Detects CachyOS when `ID_LIKE=arch` with CachyOS markers
- [ ] Sets `is_cachyos=True` in [`LinuxDistribution`](../linux_expansion_manifest.md:199) object
- [ ] Logs CachyOS detection with version information
- [ ] CachyOS is detected before generic Arch Linux
- [ ] Supports CachyOS variants

### Priority

**Critical** - CachyOS is the primary Linux target platform.

### Dependencies

- REQ-001-001: Detect Linux distribution

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- **TM-LX-002: Distribution-Specific Vulnerabilities** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:352)

### Test Cases

#### Unit Tests

1. **Test CachyOS Detection**
   - **Description:** Verify CachyOS is detected correctly
   - **Steps:**
     1. Mock `/etc/os-release` with CachyOS content
     2. Call `detect_linux_distribution()`
     3. Verify `is_cachyos=True`
     4. Verify distribution name contains "CachyOS"
     5. Verify family is "arch"
   - **Expected Result:** CachyOS detected with flag set

2. **Test CachyOS vs Arch Differentiation**
   - **Description:** Verify CachyOS is distinguished from Arch Linux
   - **Steps:**
     1. Mock `/etc/os-release` with Arch Linux content
     2. Call `detect_linux_distribution()`
     3. Verify `is_cachyos=False`
     4. Mock `/etc/os-release` with CachyOS content
     5. Call `detect_linux_distribution()`
     6. Verify `is_cachyos=True`
   - **Expected Result:** CachyOS and Arch Linux are distinguished

---

## REQ-001-003: Detect Nix Environment

### Description

The system shall detect if it is running within a Nix shell environment and adjust behavior accordingly.

### Functional Requirements

The system shall:
1. Check for `IN_NIX_SHELL` environment variable
2. Check for `NIX_PATH` environment variable
3. Check for `NIX_PROFILES` environment variable
4. Return boolean indicating Nix environment status
5. Log Nix environment detection at INFO level
6. Cache Nix environment detection result
7. Provide function to get Nix store paths

### Acceptance Criteria

- [ ] Function `is_nix_environment()` exists in `omni_scripts/platform/linux.py`
- [ ] Returns `True` when `IN_NIX_SHELL=1`
- [ ] Returns `False` when `IN_NIX_SHELL` is not set
- [ ] Logs Nix environment detection at INFO level
- [ ] Detection result is cached
- [ ] Function to get Nix store paths exists

### Priority

**Critical** - Nix integration is essential for reproducible builds.

### Dependencies

- None

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Unit Tests

1. **Test Nix Environment Detection**
   - **Description:** Verify Nix environment is detected
   - **Steps:**
     1. Set `IN_NIX_SHELL=1` environment variable
     2. Call `is_nix_environment()`
     3. Verify returns `True`
   - **Expected Result:** Nix environment detected

2. **Test Non-Nix Environment**
   - **Description:** Verify non-Nix environment is detected
   - **Steps:**
     1. Unset `IN_NIX_SHELL` environment variable
     2. Call `is_nix_environment()`
     3. Verify returns `False`
   - **Expected Result:** Non-Nix environment detected

---

## REQ-001-004: Detect Package Manager

### Description

The system shall detect the system package manager (pacman, apt, dnf, zypper, etc.) to enable appropriate package installation commands.

### Functional Requirements

The system shall:
1. Check for `pacman` executable (Arch Linux family)
2. Check for `apt` or `apt-get` executable (Debian family)
3. Check for `dnf` or `yum` executable (Fedora family)
4. Check for `zypper` executable (openSUSE family)
5. Return a structured [`PackageManager`](../linux_expansion_manifest.md:141) object containing:
   - Package manager name
   - Package manager command
   - Package manager family
6. Handle multiple package managers present (return first match)
7. Log detected package manager at INFO level
8. Cache package manager detection result

### Acceptance Criteria

- [ ] Function `detect_package_manager()` exists in `omni_scripts/platform/linux.py`
- [ ] Detects pacman on Arch Linux systems
- [ ] Detects apt on Ubuntu/Debian systems
- [ ] Detects dnf on Fedora systems
- [ ] Detects zypper on openSUSE systems
- [ ] Returns valid [`PackageManager`](../linux_expansion_manifest.md:141) object
- [ ] Logs package manager detection at INFO level
- [ ] Detection result is cached

### Priority

**Critical** - Package manager detection is required for environment validation.

### Dependencies

- REQ-001-001: Detect Linux distribution

### Related ADRs

- [ADR-031: Linux-Specific Multi-Package Manager Strategy](../02_adrs/ADR-031-linux-multi-package-manager-strategy.md)

### Related Threats

- None directly

### Test Cases

#### Unit Tests

1. **Test Pacman Detection**
   - **Description:** Verify pacman is detected on Arch Linux
   - **Steps:**
     1. Mock `shutil.which("pacman")` to return path
     2. Call `detect_package_manager()`
     3. Verify returns pacman package manager
     4. Verify command is "pacman"
   - **Expected Result:** Pacman detected

2. **Test Apt Detection**
   - **Description:** Verify apt is detected on Debian systems
   - **Steps:**
     1. Mock `shutil.which("apt")` to return path
     2. Call `detect_package_manager()`
     3. Verify returns apt package manager
     4. Verify command is "apt"
   - **Expected Result:** Apt detected

---

## REQ-001-005: Apply CachyOS-Specific Compiler Flags

### Description

The system shall apply CachyOS-specific compiler flags to optimize builds for the CachyOS platform.

### Functional Requirements

The system shall:
1. Provide function `get_cachyos_compiler_flags(compiler: str, build_type: str)`
2. Apply `-march=native` for release builds on CachyOS
3. Apply `-O3` optimization for release builds
4. Apply `-flto` (link-time optimization) for release builds
5. Apply `-DNDEBUG` for release builds
6. Apply `-g` for debug builds
7. Apply `-O0` for debug builds
8. Apply `-DDEBUG` for debug builds
9. Apply `-fstack-protector-strong` for GCC
10. Apply `-D_FORTIFY_SOURCE=2` for GCC
11. Return list of compiler flags
12. Log applied flags at DEBUG level

### Acceptance Criteria

- [ ] Function `get_cachyos_compiler_flags()` exists in `omni_scripts/platform/linux.py`
- [ ] Returns `-march=native` for release builds
- [ ] Returns `-O3` for release builds
- [ ] Returns `-flto` for release builds
- [ ] Returns `-DNDEBUG` for release builds
- [ ] Returns `-g` for debug builds
- [ ] Returns `-O0` for debug builds
- [ ] Returns `-DDEBUG` for debug builds
- [ ] Returns `-fstack-protector-strong` for GCC
- [ ] Returns `-D_FORTIFY_SOURCE=2` for GCC
- [ ] Logs applied flags at DEBUG level

### Priority

**High** - CachyOS-specific optimizations improve build performance.

### Dependencies

- REQ-001-002: Detect CachyOS specifically

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- None directly

### Test Cases

#### Unit Tests

1. **Test CachyOS Release Flags**
   - **Description:** Verify release build flags are correct
   - **Steps:**
     1. Call `get_cachyos_compiler_flags("gcc", "release")`
     2. Verify `-march=native` is in flags
     3. Verify `-O3` is in flags
     4. Verify `-flto` is in flags
     5. Verify `-DNDEBUG` is in flags
   - **Expected Result:** Correct release flags returned

2. **Test CachyOS Debug Flags**
   - **Description:** Verify debug build flags are correct
   - **Steps:**
     1. Call `get_cachyos_compiler_flags("gcc", "debug")`
     2. Verify `-g` is in flags
     3. Verify `-O0` is in flags
     4. Verify `-DDEBUG` is in flags
   - **Expected Result:** Correct debug flags returned

---

## REQ-001-006: Integrate with Nix Shell

### Description

The system shall integrate with Nix shell environments to use Nix-provided toolchains and dependencies.

### Functional Requirements

The system shall:
1. Provide function `setup_nix_environment()` in [`OmniCppController.py`](../../OmniCppController.py:1)
2. Detect Nix environment before setup
3. Use Nix-provided compiler paths when in Nix shell
4. Use Nix-provided CMake when in Nix shell
5. Use Nix-provided Ninja when in Nix shell
6. Use Nix-provided Qt6 when in Nix shell
7. Use Nix-provided Vulkan when in Nix shell
8. Set environment variables for Nix paths
9. Configure CMake to use Nix toolchain
10. Log Nix environment setup at INFO level
11. Skip Nix setup when not in Nix environment

### Acceptance Criteria

- [ ] Function `setup_nix_environment()` exists in [`OmniCppController.py`](../../OmniCppController.py:1)
- [ ] Detects Nix environment before setup
- [ ] Uses Nix-provided compiler paths when in Nix shell
- [ ] Uses Nix-provided CMake when in Nix shell
- [ ] Uses Nix-provided Ninja when in Nix shell
- [ ] Sets environment variables for Nix paths
- [ ] Configures CMake to use Nix toolchain
- [ ] Logs Nix environment setup at INFO level
- [ ] Skips Nix setup when not in Nix environment

### Priority

**Critical** - Nix integration is essential for reproducible builds.

### Dependencies

- REQ-001-003: Detect Nix environment

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Integration Tests

1. **Test Nix Environment Setup**
   - **Description:** Verify Nix environment is set up correctly
   - **Steps:**
     1. Set `IN_NIX_SHELL=1` environment variable
     2. Call `setup_nix_environment()`
     3. Verify compiler paths point to Nix store
     4. Verify CMake path points to Nix store
     5. Verify Ninja path points to Nix store
   - **Expected Result:** Nix environment set up correctly

2. **Test Non-Nix Environment Skip**
   - **Description:** Verify Nix setup is skipped when not in Nix
   - **Steps:**
     1. Unset `IN_NIX_SHELL` environment variable
     2. Call `setup_nix_environment()`
     3. Verify no Nix paths are used
     4. Verify system paths are used
   - **Expected Result:** Nix setup skipped, system paths used

---

## REQ-001-007: Validate Linux Build Environment

### Description

The system shall validate that the Linux build environment is complete and functional before attempting builds.

### Functional Requirements

The system shall:
1. Provide function `validate_linux_environment()` in [`OmniCppController.py`](../../OmniCppController.py:1)
2. Check compiler availability (GCC or Clang)
3. Check CMake availability
4. Check Ninja availability
5. Check Qt6 availability (if required)
6. Check Vulkan availability (if required)
7. Check Conan availability
8. Validate compiler version meets minimum requirements
9. Validate CMake version meets minimum requirements
10. Return boolean indicating environment validity
11. Log validation results at INFO level
12. Provide detailed error messages for missing dependencies
13. Return list of missing dependencies

### Acceptance Criteria

- [ ] Function `validate_linux_environment()` exists in [`OmniCppController.py`](../../OmniCppController.py:1)
- [ ] Checks GCC availability
- [ ] Checks Clang availability
- [ ] Checks CMake availability
- [ ] Checks Ninja availability
- [ ] Checks Qt6 availability (if required)
- [ ] Checks Vulkan availability (if required)
- [ ] Checks Conan availability
- [ ] Validates compiler version
- [ ] Validates CMake version
- [ ] Returns boolean indicating validity
- [ ] Logs validation results at INFO level
- [ ] Provides detailed error messages
- [ ] Returns list of missing dependencies

### Priority

**Critical** - Environment validation prevents build failures.

### Dependencies

- REQ-001-004: Detect package manager
- REQ-001-006: Integrate with Nix shell

### Related ADRs

- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Valid Environment**
   - **Description:** Verify valid environment is detected
   - **Steps:**
     1. Mock all required tools as available
     2. Call `validate_linux_environment()`
     3. Verify returns `True`
     4. Verify logs success at INFO level
   - **Expected Result:** Valid environment detected

2. **Test Missing Compiler**
   - **Description:** Verify missing compiler is detected
   - **Steps:**
     1. Mock GCC and Clang as unavailable
     2. Call `validate_linux_environment()`
     3. Verify returns `False`
     4. Verify compiler is in missing dependencies list
     5. Verify error message mentions missing compiler
   - **Expected Result:** Missing compiler detected

---

## REQ-001-008: Generate Linux Build Commands

### Description

The system shall generate appropriate Linux build commands based on the detected environment and configuration.

### Functional Requirements

The system shall:
1. Provide function `get_linux_build_context()` in [`OmniCppController.py`](../../OmniCppController.py:1)
2. Accept target, pipeline, preset, config, and compiler parameters
3. Use Nix-provided toolchain when in Nix environment
4. Use CachyOS-specific flags when on CachyOS
5. Use generic Linux flags for other distributions
6. Generate CMake configuration command
7. Generate build command
8. Apply appropriate compiler flags
9. Set appropriate environment variables
10. Return [`BuildContext`](../linux_expansion_manifest.md:142) object
11. Log generated commands at DEBUG level

### Acceptance Criteria

- [ ] Function `get_linux_build_context()` exists in [`OmniCppController.py`](../../OmniCppController.py:1)
- [ ] Accepts target, pipeline, preset, config, and compiler parameters
- [ ] Uses Nix toolchain when in Nix environment
- [ ] Uses CachyOS flags when on CachyOS
- [ ] Uses generic Linux flags for other distributions
- [ ] Generates CMake configuration command
- [ ] Generates build command
- [ ] Applies appropriate compiler flags
- [ ] Sets appropriate environment variables
- [ ] Returns [`BuildContext`](../linux_expansion_manifest.md:142) object
- [ ] Logs generated commands at DEBUG level

### Priority

**High** - Build command generation is essential for Linux builds.

### Dependencies

- REQ-001-005: Apply CachyOS-specific compiler flags
- REQ-001-007: Validate Linux build environment

### Related ADRs

- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test CachyOS Build Context**
   - **Description:** Verify CachyOS build context is generated correctly
   - **Steps:**
     1. Mock CachyOS detection
     2. Call `get_linux_build_context()` with release config
     3. Verify CachyOS flags are applied
     4. Verify CMake command is correct
     5. Verify build command is correct
   - **Expected Result:** CachyOS build context generated correctly

2. **Test Nix Build Context**
   - **Description:** Verify Nix build context is generated correctly
   - **Steps:**
     1. Mock Nix environment detection
     2. Call `get_linux_build_context()`
     3. Verify Nix toolchain is used
     4. Verify Nix paths are in context
   - **Expected Result:** Nix build context generated correctly

---

## Implementation Notes

### Module Structure

Create new module `omni_scripts/platform/linux.py` with the following structure:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class LinuxDistribution:
    """Linux distribution information."""
    name: str
    version: str
    family: str
    package_manager: str
    is_cachyos: bool

@dataclass
class PackageManager:
    """Package manager information."""
    name: str
    command: str
    family: str

def detect_linux_distribution() -> LinuxDistribution:
    """Detect Linux distribution and version."""
    pass

def detect_package_manager() -> PackageManager:
    """Detect system package manager."""
    pass

def is_nix_environment() -> bool:
    """Check if running in Nix shell."""
    pass

def is_cachyos() -> bool:
    """Check if running on CachyOS."""
    pass

def get_cachyos_compiler_flags(compiler: str, build_type: str) -> list[str]:
    """Get CachyOS-specific compiler flags."""
    pass

def get_cachyos_linker_flags() -> list[str]:
    """Get CachyOS-specific linker flags."""
    pass

def get_cachyos_library_paths() -> list[Path]:
    """Get CachyOS library search paths."""
    pass
```

### Integration with OmniCppController.py

Add the following methods to [`OmniCppController.py`](../../OmniCppController.py:1):

```python
def _setup_nix_environment(self) -> None:
    """Configure build environment for Nix shell."""
    pass

def _validate_linux_environment(self) -> bool:
    """Validate Linux build environment is complete."""
    pass

def _get_linux_build_context(
    self,
    target: str,
    pipeline: str,
    preset: str,
    config: str,
    compiler: Optional[str] = None
) -> BuildContext:
    """Create BuildContext optimized for Linux builds."""
    pass
```

### Environment Variables

The following environment variables shall be used:

- `IN_NIX_SHELL`: Set to "1" when in Nix shell
- `NIX_PATH`: Nix search path
- `NIX_PROFILES`: Nix profiles
- `QT_QPA_PLATFORM`: Qt platform (wayland for CachyOS)
- `VK_LAYER_PATH`: Vulkan validation layers path
- `VK_ICD_FILENAMES`: Vulkan ICD filenames

### Logging

All detection and setup operations shall be logged:
- Distribution detection: INFO level
- Package manager detection: INFO level
- Nix environment detection: INFO level
- CachyOS detection: INFO level
- Compiler flag application: DEBUG level
- Environment validation: INFO level
- Build command generation: DEBUG level

### Error Handling

The system shall handle the following error conditions:
- Missing `/etc/os-release` file
- Malformed `/etc/os-release` content
- Unknown Linux distribution
- Missing package manager
- Missing compiler
- Missing CMake
- Missing Ninja
- Missing Qt6 (if required)
- Missing Vulkan (if required)
- Missing Conan

All errors shall be logged with appropriate severity and provide actionable error messages.

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-031: Linux-Specific Multi-Package Manager Strategy](../02_adrs/ADR-031-linux-multi-package-manager-strategy.md)
- [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md) - Threat Model Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
