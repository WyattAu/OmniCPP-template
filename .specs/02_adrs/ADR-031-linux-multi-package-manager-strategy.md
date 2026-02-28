# ADR-031: Linux-Specific Multi-Package Manager Strategy

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Linux Package Management Architecture

---

## Context

The OmniCPP Template project currently uses three package managers (Conan, vcpkg, CPM.cmake) as documented in [ADR-001](ADR-001-multi-package-manager-strategy.md). This multi-package manager strategy was designed with Windows as the primary platform.

### Current State

1. **Conan:** Primary package manager for binary dependencies
2. **vcpkg:** Secondary package manager, Windows-optimized
3. **CPM.cmake:** Tertiary package manager for header-only libraries
4. **Priority:** Conan > vcpkg > CPM.cmake

### Linux Expansion Requirements

The Linux expansion introduces new considerations:

1. **Nix as Environment Manager:** Nix provides the development environment (see [ADR-027](ADR-027-nix-package-manager-integration.md))
2. **System Package Managers:** Linux distributions have system package managers (pacman, apt, dnf)
3. **Nix Packages:** Nix can provide packages directly (GCC, Clang, CMake, Ninja, Qt6, Vulkan)
4. **Conan for C++ Dependencies:** Conan still needed for C++ libraries (fmt, spdlog, glm, etc.)
5. **vcpkg on Linux:** vcpkg has limited Linux support
6. **CPM.cmake Still Relevant:** CPM.cmake useful for header-only libraries

### Challenges

1. **Package Manager Overlap:** Nix and Conan both can provide packages
2. **Dependency Conflicts:** Nix packages may conflict with Conan packages
3. **Reproducibility:** Need reproducible builds across different package managers
4. **Complexity:** Four package managers increase complexity
5. **Maintenance:** More configurations to maintain
6. **Documentation:** Need to document when to use which package manager
7. **User Confusion:** Developers may not know which package manager to use

### Questions to Answer

1. Should Nix be considered a package manager or just an environment manager?
2. How should Conan integrate with Nix environment?
3. Should vcpkg be used on Linux?
4. How should package managers be prioritized on Linux?
5. What happens when Nix and Conan provide the same package?

## Decision

Adopt a **four-tier package management strategy** for Linux, with clear roles for each package manager.

### 1. Package Manager Roles

Define clear roles for each package manager:

```python
# Package Manager Hierarchy (Linux)

# Tier 1: System Environment (Nix)
# Role: Provide development environment and system libraries
# Examples: GCC, Clang, CMake, Ninja, Qt6, Vulkan, OpenSSL
# Priority: Always use Nix if available

# Tier 2: C++ Dependencies (Conan)
# Role: Provide C++ library dependencies
# Examples: fmt, spdlog, glm, nlohmann_json, catch2, gtest
# Priority: Use Conan for C++ libraries not in Nix

# Tier 3: Header-Only Libraries (CPM.cmake)
# Role: Provide header-only libraries
# Examples: stb, single-header libraries
# Priority: Use CPM for header-only libraries

# Tier 4: Windows-Optimized (vcpkg)
# Role: Windows-specific packages
# Examples: Windows-specific libraries
# Priority: Use vcpkg only on Windows
```

### 2. Nix as Environment Manager

Nix provides the development environment:

```nix
# flake.nix
{
  devShells.${system}.default = pkgs.mkShell {
    buildInputs = with pkgs; [
      # Compilers
      gcc
      clang

      # Build System
      cmake
      ninja

      # Graphics (provided by Nix)
      qt6.qtbase
      vulkan-headers
      vulkan-loader

      # System libraries (provided by Nix)
      openssl
      zlib
    ];
  };
}
```

### 3. Conan for C++ Dependencies

Conan provides C++ library dependencies:

```python
# conan/conanfile.py
class OmniCppConan(ConanFile):
    name = "omnicpp-template"
    version = "0.0.3"

    # C++ dependencies (not provided by Nix)
    requirements = [
        "fmt/10.2.1",
        "spdlog/1.14.1",
        "glm/0.9.9.8",
        "nlohmann_json/3.11.3",
        "catch2/3.5.2",
        "gtest/1.14.0",
    ]

    # Don't use Conan for packages provided by Nix
    # Qt6, Vulkan, OpenSSL, zlib are provided by Nix
```

### 4. CPM.cmake for Header-Only Libraries

CPM.cmake provides header-only libraries:

```cmake
# dependencies.cmake
# Header-only libraries (not in Conan)
CPMAddPackage(
    NAME stb
    GITHUB_REPOSITORY nothings/stb
    GIT_TAG master
    DOWNLOAD_ONLY TRUE
)
```

### 5. vcpkg Windows-Only

vcpkg is used only on Windows:

```cmake
# CMakeLists.txt
if(WIN32)
    option(OMNICPP_USE_VCPKG "Use vcpkg package manager" ON)
else()
    option(OMNICPP_USE_VCPKG "Use vcpkg package manager" OFF)
endif()
```

### 6. Priority-Based Selection

Implement priority-based selection:

```python
def select_package_manager(
    package_type: str,
    platform: PlatformInfo
) -> PackageManager:
    """Select appropriate package manager based on package type and platform."""

    if package_type == "system":
        # System packages: Use Nix
        if platform.is_nix:
            return PackageManager("nix", "nix")
        else:
            return PackageManager("system", detect_system_package_manager())

    elif package_type == "cpp_library":
        # C++ libraries: Use Conan
        return PackageManager("conan", "conan")

    elif package_type == "header_only":
        # Header-only libraries: Use CPM.cmake
        return PackageManager("cpm", "cpm")

    elif package_type == "windows_specific":
        # Windows-specific: Use vcpkg
        if platform.os == "Windows":
            return PackageManager("vcpkg", "vcpkg")
        else:
            raise ValueError("vcpkg not supported on Linux")

    else:
        raise ValueError(f"Unknown package type: {package_type}")
```

### 7. Dependency Declaration

Declare dependencies in multiple formats:

```python
# Python: Package manager selection
dependencies = {
    "fmt": {"type": "cpp_library", "manager": "conan"},
    "spdlog": {"type": "cpp_library", "manager": "conan"},
    "qt6": {"type": "system", "manager": "nix"},
    "vulkan": {"type": "system", "manager": "nix"},
    "stb": {"type": "header_only", "manager": "cpm"},
}
```

### 8. Conflict Resolution

Implement conflict resolution:

```python
def resolve_dependency_conflicts(dependencies: dict) -> dict:
    """Resolve conflicts between package managers."""

    # Check for Nix/Conan conflicts
    nix_packages = get_nix_packages()
    conan_packages = get_conan_packages()

    # Prefer Nix for system packages
    for pkg in conan_packages:
        if pkg in nix_packages:
            log_warning(f"Package {pkg} provided by both Nix and Conan")
            log_info(f"Using Nix version: {pkg}")

    # Remove duplicates
    resolved = {}
    for name, info in dependencies.items():
        if name not in resolved:
            resolved[name] = info

    return resolved
```

### 9. Lock Files

Generate and use lock files for reproducibility:

```bash
# Nix lock file
nix flake update  # Updates flake.lock

# Conan lock file
conan lock create conanfile.py --lockfile-out=conan.lock

# CPM lock file (manual)
# Commit cpm.lock to repository
```

## Consequences

### Positive

1. **Clear Separation:** Each package manager has clear role
2. **Nix for Environment:** Nix provides reproducible environment
3. **Conan for C++:** Conan provides C++ library dependencies
4. **CPM for Headers:** CPM provides header-only libraries
5. **vcpkg Windows-Only:** vcpkg only used on Windows
6. **Reduced Conflicts:** Clear rules prevent conflicts
7. **Reproducible Builds:** Lock files ensure reproducibility
8. **Flexibility:** Can use different package managers for different needs
9. **Optimized:** Each package manager used for what it's best at
10. **Maintainable:** Clear rules make maintenance easier

### Negative

1. **Increased Complexity:** Four package managers instead of three
2. **Learning Curve:** Developers must understand all four package managers
3. **Configuration Overhead:** Multiple configuration files
4. **Potential Conflicts:** Still possible to have conflicts
5. **Documentation Burden:** Need to document all four package managers
6. **Testing Burden:** Need to test all package managers
7. **CI/CD Complexity:** CI/CD must handle all package managers
8. **Dependency Updates:** Updating dependencies requires updating multiple lock files

### Neutral

1. **Nix Learning Curve:** Developers must learn Nix
2. **Conan Still Needed:** Conan still needed for C++ libraries
3. **CPM Still Relevant:** CPM still useful for header-only libraries
4. **vcpkg Limited:** vcpkg limited to Windows

## Alternatives Considered

### Alternative 1: Nix-Only Approach

**Description:** Use Nix for all dependencies, drop Conan, vcpkg, CPM

**Pros:**
- Single package manager
- Fully reproducible
- Declarative
- No conflicts

**Cons:**
- Limited C++ ecosystem in Nix
- Not all libraries available
- May need to package libraries manually
- Not aligned with existing Conan usage
- Windows support limited

**Rejected:** Limited C++ ecosystem in Nix

### Alternative 2: Conan-Only on Linux

**Description:** Use Conan for all dependencies on Linux, ignore Nix packages

**Pros:**
- Single package manager on Linux
- Familiar to developers
- Good C++ ecosystem

**Cons:**
- Ignores Nix environment
- Potential conflicts with Nix
- Less reproducible
- Wastes Nix capabilities
- Not aligned with Nix approach

**Rejected:** Ignores Nix environment, wastes Nix capabilities

### Alternative 3: System Package Manager + Conan

**Description:** Use system package manager (pacman, apt) + Conan, ignore Nix

**Pros:**
- Familiar to Linux developers
- No Nix learning curve
- Good C++ ecosystem with Conan

**Cons:**
- Not reproducible across distributions
- System package drift
- No environment isolation
- Not aligned with Nix approach
- Conflicts with system packages

**Rejected:** Not reproducible, not aligned with Nix approach

### Alternative 4: Drop vcpkg Entirely

**Description:** Remove vcpkg from project entirely

**Pros:**
- One less package manager
- Less complexity
- Simpler architecture

**Cons:**
- Loses Windows-optimized packages
- May need to find alternatives
- Windows users may be affected
- Breaks existing Windows workflows

**Rejected:** Would break existing Windows workflows

### Alternative 5: Conan + CPM Only

**Description:** Use Conan and CPM only, drop Nix and vcpkg

**Pros:**
- Two package managers instead of four
- Familiar to developers
- Good C++ ecosystem

**Cons:**
- Loses Nix reproducibility
- Loses vcpkg Windows optimization
- Not aligned with Nix approach
- Less reproducible on Linux

**Rejected:** Loses Nix reproducibility, not aligned with Nix approach

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-034: Conan Profile Expansion](ADR-034-conan-profile-expansion.md)

## Threat Model References

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)
- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)
- **TM-004: Dependency Confusion Attack** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:412)

Mitigation:
- Use lock files for all package managers
- Verify package signatures
- Pin exact versions
- Use private repositories where possible
- Implement dependency allowlist

## References

- [Conan Documentation](https://docs.conan.io/)
- [Nix Manual](https://nixos.org/manual/nix/stable/)
- [CPM.cmake Documentation](https://github.com/cpm-cmake/CPM.cmake)
- [vcpkg Documentation](https://vcpkg.io/)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
