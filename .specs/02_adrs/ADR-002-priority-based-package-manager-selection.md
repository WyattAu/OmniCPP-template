# ADR-002: Priority-Based Package Manager Selection

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Package Management Architecture

---

## Context

With multiple package managers available (Conan, vcpkg, CPM.cmake), the project needs a deterministic way to select which package manager to use for dependency resolution. Different scenarios require different package managers:

- **Windows Development:** vcpkg provides excellent Windows support and Microsoft ecosystem integration
- **Cross-Platform Development:** Conan offers the best cross-platform support and binary distribution
- **Simple Dependencies:** CPM.cmake is ideal for header-only libraries and simple source dependencies
- **CI/CD Environments:** Different CI/CD environments may have different package managers available

Without a clear selection strategy, builds may be non-deterministic, and developers may be confused about which package manager is being used.

## Decision

Implement a **priority-based package manager selection** with the following rules:

### 1. Priority Order

Package managers are selected in this priority order:

1. **Conan** (Priority 1 - Highest)

   - Best for cross-platform development
   - Binary distribution support
   - Complex dependency management
   - Profile-based configuration

2. **vcpkg** (Priority 2 - Medium)

   - Excellent Windows support
   - Microsoft ecosystem integration
   - Growing Linux support
   - Simple configuration

3. **CPM.cmake** (Priority 3 - Lowest)
   - Header-only library support
   - Simple source dependencies
   - No external dependencies
   - Fast for simple cases

### 2. Selection Algorithm

```python
# omni_scripts/package_managers/manager.py
from enum import Enum
from typing import Optional

class PackageManagerType(Enum):
    """Package manager types with priority."""
    CONAN = 1      # Highest priority
    VCPKG = 2      # Medium priority
    CPM = 3        # Lowest priority

class PackageManagerManager:
    """Package manager coordinator with priority-based selection."""

    def __init__(self) -> None:
        self.available_managers: list[PackageManagerType] = []
        self._detect_available()

    def select_manager(
        self,
        preferred: Optional[PackageManagerType] = None
    ) -> Optional[PackageManagerType]:
        """
        Select package manager based on priority and preference.

        Args:
            preferred: Preferred package manager (optional)

        Returns:
            Selected package manager type
        """
        if not self.available_managers:
            return None

        # If preferred manager is available, use it
        if preferred and preferred in self.available_managers:
            return preferred

        # Otherwise, return highest priority available
        # Sort by priority (lower number = higher priority)
        sorted_managers = sorted(
            self.available_managers,
            key=lambda x: x.value
        )
        return sorted_managers[0]
```

### 3. CMake Integration

```cmake
# CMakeLists.txt
option(OMNICPP_USE_CONAN "Use Conan package manager" ON)
option(OMNICPP_USE_VCPKG "Use vcpkg package manager" OFF)
option(OMNICPP_USE_CPM "Use CPM.cmake package manager" ON)

# Auto-detect and select package manager
if(OMNICPP_USE_CONAN)
    message(STATUS "Using Conan package manager")
    include(cmake/ConanIntegration.cmake)
elseif(OMNICPP_USE_VCPKG)
    message(STATUS "Using vcpkg package manager")
    include(cmake/VcpkgIntegration.cmake)
else()
    message(STATUS "Using CPM.cmake package manager")
    include(cmake/CPM.cmake)
endif()
```

### 4. Configuration File Support

```json
// config/build.json
{
  "package_manager": {
    "preferred": "conan",
    "auto_detect": true,
    "fallback_enabled": true
  }
}
```

## Consequences

### Positive

1. **Deterministic Builds:** Package manager selection is predictable and consistent
2. **Flexibility:** Developers can override default selection via configuration
3. **Optimization:** Each package manager is used for its strengths
4. **Fallback Support:** If preferred manager is unavailable, others can be used
5. **Clear Documentation:** Priority order is documented and easy to understand
6. **CI/CD Friendly:** CI/CD pipelines can rely on deterministic selection

### Negative

1. **Configuration Complexity:** Multiple package managers require more configuration files
2. **Learning Curve:** Developers need to understand multiple package managers
3. **Potential Conflicts:** Different package managers may have conflicting dependency versions
4. **Build Time:** Package manager detection adds to build time
5. **Maintenance Burden:** Multiple package managers require ongoing maintenance

### Neutral

1. **Documentation:** Requires documentation for each package manager's usage
2. **Testing:** Need to test builds with each package manager

## Alternatives Considered

### Alternative 1: Single Package Manager (Conan Only)

**Description:** Use only Conan for all dependencies

**Pros:**

- Simplest configuration
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
- Fast for simple cases

**Cons:**

- No binary distribution
- Limited to header-only libraries
- Not suitable for complex dependencies

**Rejected:** Too limited for complex dependencies

### Alternative 4: Environment-Based Selection

**Description:** Select package manager based on environment variables or CI/CD environment

**Pros:**

- Flexible for different environments
- Can optimize for specific CI/CD pipelines

**Cons:**

- Non-deterministic across environments
- Harder to reproduce builds locally
- Environment-specific behavior

**Rejected:** Non-deterministic behavior is undesirable

### Alternative 5: Dependency-Based Selection

**Description:** Select package manager based on dependency type (binary vs header-only)

**Pros:**

- Optimizes for each dependency type
- Uses best tool for each case

**Cons:**

- Complex to implement
- Multiple package managers in single build
- Dependency conflicts between managers

**Rejected:** Too complex, potential for conflicts

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-003: Package security verification approach](ADR-003-package-security-verification-approach.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)
- [ADR-020: Dependency integrity verification](ADR-020-dependency-integrity-verification.md)

## References

- [Conan Documentation](https://docs.conan.io/)
- [vcpkg Documentation](https://vcpkg.io/)
- [CPM.cmake Documentation](https://github.com/cpm-cmake/CPM.cmake)
- [CMake Package Management](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html)
- [Package Manager Comparison](https://github.com/fperrin48/cpp-package-manager)

---

**Document Control**

| Version | Date       | Author           | Changes         |
| ------- | ---------- | ---------------- | --------------- |
| 1.0     | 2026-01-07 | System Architect | Initial version |
