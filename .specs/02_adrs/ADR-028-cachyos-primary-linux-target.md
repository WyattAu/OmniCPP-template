# ADR-028: CachyOS as Primary Linux Target

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Linux Platform Targeting Strategy

---

## Context

The OmniCPP Template project needs to support Linux development. The Linux ecosystem is highly fragmented with multiple distributions, package managers, and system configurations. Key considerations:

1. **Distribution Fragmentation:** Ubuntu, Fedora, Arch Linux, Debian, CentOS, and many others
2. **Package Manager Diversity:** apt, dnf, pacman, zypper, and others
3. **Library Version Variability:** Different distributions ship different library versions
4. **Compiler Availability:** GCC and Clang versions vary across distributions
5. **System Configuration:** Different init systems, desktop environments, and graphics stacks

The project's primary development machine is a CachyOS PC, which is:
- An Arch Linux derivative
- Optimized for performance with custom kernel patches
- Uses rolling release model
- Ships with latest GCC and Clang versions
- Has Wayland as default display server
- Includes performance-oriented system tuning

The project needs to balance:
- Optimizing for the primary development platform (CachyOS)
- Maintaining compatibility with other Linux distributions
- Ensuring reproducible builds across platforms
- Minimizing platform-specific code complexity

## Decision

Adopt **CachyOS as the primary Linux target** while maintaining compatibility with other Linux distributions.

### 1. CachyOS-First Development

All Linux development and testing will prioritize CachyOS:

```python
# omni_scripts/platform/linux.py
def detect_linux_distribution() -> LinuxDistribution:
    """Detect Linux distribution and version."""
    if is_cachyos():
        return LinuxDistribution(
            name="CachyOS",
            version=get_cachyos_version(),
            family="arch",
            package_manager="pacman",
            is_cachyos=True
        )
    # Fallback to other distributions
    return detect_other_distribution()
```

### 2. CachyOS-Specific Optimizations

Implement CachyOS-specific compiler flags and configurations:

```python
def get_cachyos_compiler_flags(compiler: str, build_type: str) -> list[str]:
    """Get CachyOS-specific compiler flags."""
    flags = []

    if build_type == "release":
        # CachyOS performance optimizations
        flags.extend([
            "-march=native",  # Use native CPU features
            "-O3",            # Maximum optimization
            "-flto",          # Link-time optimization
            "-DNDEBUG"        # Disable debug assertions
        ])
    else:
        # Debug build flags
        flags.extend([
            "-g",
            "-O0",
            "-DDEBUG"
        ])

    # CachyOS-specific flags
    if compiler == "gcc":
        flags.extend([
            "-fstack-protector-strong",
            "-D_FORTIFY_SOURCE=2"
        ])

    return flags
```

### 3. General Linux Compatibility

Maintain compatibility with other Linux distributions through:

```python
def get_linux_compiler_flags(compiler: str, build_type: str, distro: LinuxDistribution) -> list[str]:
    """Get compiler flags for Linux distribution."""
    if distro.is_cachyos:
        return get_cachyos_compiler_flags(compiler, build_type)
    else:
        return get_generic_linux_flags(compiler, build_type)
```

### 4. Distribution Detection

Implement comprehensive distribution detection:

```python
def detect_linux_distribution() -> LinuxDistribution:
    """Detect Linux distribution."""
    # Check /etc/os-release
    if Path("/etc/os-release").exists():
        with open("/etc/os-release") as f:
            content = f.read()

        if "ID=cachyos" in content:
            return create_cachyos_info()
        elif "ID=arch" in content:
            return create_arch_info()
        elif "ID=ubuntu" in content:
            return create_ubuntu_info()
        elif "ID=fedora" in content:
            return create_fedora_info()
        # ... other distributions

    return LinuxDistribution(
        name="Unknown",
        version="",
        family="unknown",
        package_manager="unknown",
        is_cachyos=False
    )
```

### 5. Package Manager Detection

Detect and support multiple package managers:

```python
def detect_package_manager() -> PackageManager:
    """Detect system package manager."""
    if shutil.which("pacman"):
        return PackageManager("pacman", "pacman")
    elif shutil.which("apt"):
        return PackageManager("apt", "apt-get")
    elif shutil.which("dnf"):
        return PackageManager("dnf", "dnf")
    elif shutil.which("zypper"):
        return PackageManager("zypper", "zypper")

    return PackageManager("unknown", "")
```

### 6. Conan Profile Strategy

Create CachyOS-specific Conan profiles:

```ini
# conan/profiles/cachyos-gcc
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
```

### 7. CMake Preset Strategy

Create CachyOS-optimized CMake presets:

```json
{
  "name": "cachyos-gcc-debug",
  "displayName": "CachyOS GCC Debug",
  "binaryDir": "${sourceDir}/build/cachyos-gcc-debug",
  "generator": "Ninja",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_COMPILER": "gcc",
    "CMAKE_CXX_COMPILER": "g++",
    "CMAKE_CXX_FLAGS": "-march=native -g -O0"
  }
}
```

### 8. Documentation Strategy

Document CachyOS-specific setup and provide general Linux guidance:

```markdown
# Linux Setup Guide

## CachyOS (Primary)

CachyOS is the primary development platform. See [CachyOS Setup Guide](cachyos-setup.md).

## Other Linux Distributions

The project should work on other distributions, but may require additional configuration:

- Arch Linux: Should work identically to CachyOS
- Ubuntu: May need to install additional packages
- Fedora: May need to adjust compiler flags
```

## Consequences

### Positive

1. **Optimized Performance:** CachyOS-specific optimizations for primary platform
2. **Simplified Development:** Single primary platform reduces complexity
3. **Better Testing:** Comprehensive testing on primary platform
4. **Performance Focus:** Leverages CachyOS performance optimizations
5. **Latest Toolchains:** Access to latest GCC and Clang versions
6. **Rolling Release:** Always up-to-date dependencies
7. **Clear Documentation:** Clear primary platform documentation
8. **Faster Development:** Less time spent on distribution compatibility
9. **Better Bug Reproduction:** Consistent environment for bug fixing
10. **Performance Benchmarking:** Reliable performance measurements

### Negative

1. **Limited Audience:** CachyOS has smaller user base than Ubuntu
2. **Compatibility Risk:** May not work on other distributions
3. **Testing Gap:** Other distributions may have issues
4. **Documentation Bias:** Documentation may be CachyOS-centric
5. **Community Perception:** May appear to exclude other distributions
6. **Dependency Issues:** CachyOS may have different library versions
7. **Kernel Differences:** CachyOS kernel patches may cause issues elsewhere
8. **Wayland-First:** Wayland default may not work on X11 systems
9. **Package Manager:** pacman is not available on all distributions
10. **Rolling Release Risk:** Updates may break builds

### Neutral

1. **Maintenance:** Must maintain CachyOS-specific code paths
2. **Testing:** Need to test on other distributions periodically
3. **Support:** May receive bug reports from other distributions
4. **CI/CD:** May need multiple Linux CI targets
5. **Documentation:** Need to document both CachyOS and general Linux

## Alternatives Considered

### Alternative 1: Ubuntu as Primary Target

**Description:** Use Ubuntu LTS as primary Linux target

**Pros:**
- Largest Linux user base
- Well-documented
- Stable LTS releases
- Corporate support (Canonical)
- Most common in enterprise

**Cons:**
- Older compiler versions
- Older library versions
- Less performance-oriented
- More conservative updates
- Not aligned with primary development machine

**Rejected:** Not aligned with primary development platform and performance goals

### Alternative 2: Arch Linux as Primary Target

**Description:** Use Arch Linux as primary target (not CachyOS)

**Pros:**
- Rolling release like CachyOS
- Large community
- Well-documented
- Latest packages
- Similar to CachyOS

**Cons:**
- Not the actual development platform
- Missing CachyOS performance optimizations
- Different kernel configuration
- Different default settings

**Rejected:** CachyOS is the actual development platform

### Alternative 3: Distribution-Agnostic Approach

**Description:** Support all distributions equally without primary target

**Pros:**
- Inclusive approach
- No distribution bias
- Works everywhere
- Larger user base

**Cons:**
- Higher complexity
- More testing required
- Harder to optimize
- Slower development
- No clear primary platform

**Rejected:** Too complex, no clear optimization target

### Alternative 4: Multiple Primary Targets

**Description:** Support multiple distributions as primary targets (e.g., Ubuntu + CachyOS)

**Pros:**
- Broader coverage
- More inclusive
- Better compatibility

**Cons:**
- Higher complexity
- More testing required
- Conflicting requirements
- Slower development
- Harder to optimize

**Rejected:** Too complex, conflicting requirements

### Alternative 5: Container-Based Approach

**Description:** Use containers to provide consistent environment across distributions

**Pros:**
- Consistent environment
- Works on any distribution
- Isolated from host system

**Cons:**
- Container overhead
- Not suitable for graphics development
- IDE integration complexity
- Performance overhead
- Not aligned with Nix approach

**Rejected:** Conflicts with Nix approach, not suitable for graphics

## Related ADRs

- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](ADR-029-direnv-environment-management.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-034: Conan Profile Expansion](ADR-034-conan-profile-expansion.md)
- [ADR-036: CMake Preset Expansion](ADR-036-cmake-preset-expansion.md)

## Threat Model References

- **TM-LX-002: Distribution-Specific Vulnerabilities** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - CachyOS-specific kernel vulnerabilities
  - Arch Linux package vulnerabilities
  - Mitigation: Keep system updated, use security advisories

## References

- [CachyOS Website](https://cachyos.org/)
- [CachyOS Wiki](https://wiki.cachyos.org/)
- [Arch Linux Wiki](https://wiki.archlinux.org/)
- [Linux Standard Base](https://refspecs.linuxfoundation.org/lsb.shtml)
- [Package Manager Comparison](https://wiki.archlinux.org/title/Pacman/Rosetta)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
