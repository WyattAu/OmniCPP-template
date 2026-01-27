# ADR-001: Multi-Package Manager Strategy

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Package Management Architecture

---

## Context

The OmniCPP Template project requires dependency management for C++ libraries across multiple platforms (Windows, Linux, WASM). Different package managers offer varying capabilities:

- **Conan:** Binary distribution, cross-platform support, complex configuration
- **vcpkg:** Microsoft's package manager, excellent Windows support, growing Linux support
- **CPM.cmake:** CMake-based dependency fetcher, header-only library support, simple integration

The project needs to support multiple package managers to:
1. Provide flexibility for different development environments
2. Support both binary and source-only dependencies
3. Enable fallback mechanisms when one package manager is unavailable
4. Maintain reproducible builds across different environments

## Decision

Adopt a **multi-package manager strategy** with the following characteristics:

### 1. Priority-Based Selection

Package managers are selected in priority order:
1. **Conan** (highest priority) - For binary dependencies and complex configurations
2. **vcpkg** (medium priority) - For Windows-first development and Microsoft ecosystem
3. **CPM.cmake** (lowest priority) - For header-only libraries and simple dependencies

### 2. Unified Interface

Create a unified package manager interface in [`omni_scripts/package_managers/`](../omni_scripts/package_managers/):

```python
class PackageManagerManager:
    """Coordinates multiple package managers with priority-based selection."""

    def __init__(self) -> None:
        self.available_managers: List[PackageManagerType] = []
        self._detect_available()

    def select_manager(self, preferred: Optional[PackageManagerType] = None) -> PackageManager:
        """Select package manager based on priority and preference."""
        if preferred and preferred in self.available_managers:
            return self._get_manager(preferred)

        # Return highest priority available
        return self._get_manager(self.available_managers[0])
```

### 3. Dependency Declaration

Dependencies are declared in multiple formats:
- **Conan:** [`conan/conanfile.py`](../../conan/conanfile.py)
- **vcpkg:** [`vcpkg.json`](../../vcpkg.json)
- **CPM:** [`dependencies.cmake`](../../dependencies.cmake)

### 4. CMake Integration

CMake configuration in [`CMakeLists.txt`](../../CMakeLists.txt) enables package managers via options:

```cmake
option(OMNICPP_USE_CONAN "Use Conan package manager" ON)
option(OMNICPP_USE_VCPKG "Use vcpkg package manager" OFF)
option(OMNICPP_USE_CPM "Use CPM.cmake package manager" ON)

# Priority: Conan > vcpkg > CPM
if(OMNICPP_USE_CONAN)
    include(cmake/ConanIntegration.cmake)
elseif(OMNICPP_USE_VCPKG)
    include(cmake/VcpkgIntegration.cmake)
else()
    include(cmake/CPM.cmake)
endif()
```

### 5. Lock Files

Generate and use lock files for reproducible builds:
- **Conan:** `conan.lock`
- **vcpkg:** `vcpkg-lock.json`
- **CPM:** `cpm.lock`

## Consequences

### Positive

1. **Flexibility:** Developers can choose package manager based on their environment and preferences
2. **Fallback Mechanism:** If one package manager is unavailable, others can be used
3. **Platform Optimization:** vcpkg optimized for Windows, Conan for cross-platform, CPM for simple cases
4. **Reproducible Builds:** Lock files ensure consistent dependency versions across builds
5. **Community Support:** Multiple package managers provide access to larger dependency ecosystem

### Negative

1. **Complexity:** Maintaining three package manager configurations increases complexity
2. **Learning Curve:** Developers need to understand multiple package managers
3. **Configuration Overhead:** Multiple configuration files (conanfile.py, vcpkg.json, dependencies.cmake)
4. **Potential Conflicts:** Different package managers may have conflicting dependency versions
5. **Build Time:** Package manager detection and selection adds to build time

### Neutral

1. **Documentation:** Requires documentation for each package manager's usage
2. **CI/CD:** CI/CD pipelines must handle multiple package managers

## Alternatives Considered

### Alternative 1: Single Package Manager (Conan Only)

**Description:** Use only Conan for all dependencies

**Pros:**
- Simpler configuration
- Single learning curve
- Consistent interface

**Cons:**
- Conan may not be available in all environments
- Limited to Conan's dependency ecosystem
- Binary distribution may not work for all platforms

**Rejected:** Too restrictive, limits flexibility

### Alternative 2: Single Package Manager (vcpkg Only)

**Description:** Use only vcpkg for all dependencies

**Pros:**
- Excellent Windows support
- Microsoft ecosystem integration
- Simple configuration

**Cons:**
- Limited Linux support
- Not suitable for cross-platform development
- Microsoft-centric dependency ecosystem

**Rejected:** Not suitable for cross-platform development

### Alternative 3: Single Package Manager (CPM Only)

**Description:** Use only CPM.cmake for all dependencies

**Pros:**
- Simplest configuration
- No external dependencies
- Header-only library support

**Cons:**
- No binary distribution
- Limited to header-only libraries
- Not suitable for complex dependencies

**Rejected:** Too limited for complex dependencies

### Alternative 4: Package Manager Abstraction Layer

**Description:** Create a custom abstraction layer that provides unified interface to all package managers

**Pros:**
- Completely unified interface
- Can switch package managers transparently
- Customizable behavior

**Cons:**
- Significant development effort
- Maintenance burden
- May not support all package manager features
- Another layer of abstraction to debug

**Rejected:** Too complex, maintenance burden outweighs benefits

## Related ADRs

- [ADR-002: Priority-based package manager selection](ADR-002-priority-based-package-manager-selection.md)
- [ADR-003: Package security verification approach](ADR-003-package-security-verification-approach.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)
- [ADR-020: Dependency integrity verification](ADR-020-dependency-integrity-verification.md)

## References

- [Conan Documentation](https://docs.conan.io/)
- [vcpkg Documentation](https://vcpkg.io/)
- [CPM.cmake Documentation](https://github.com/cpm-cmake/CPM.cmake)
- [CMake Package Management](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html)
- [Package Manager Best Practices](https://github.com/fperrin48/cpp-package-manager)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
