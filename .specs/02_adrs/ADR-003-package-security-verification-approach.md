# ADR-003: Package Security Verification Approach

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Package Management Security

---

## Context

Package managers (Conan, vcpkg, CPM.cmake) download and install dependencies from external sources, which introduces security risks:

1. **Malicious Packages:** Attackers can upload malicious packages to public repositories
2. **Dependency Confusion:** Attackers can publish packages with same names but higher versions
3. **Typosquatting:** Attackers can publish packages with similar names to trick users
4. **Supply Chain Compromise:** Attackers can compromise legitimate package maintainers
5. **Repository Compromise:** Attackers can gain access to package repositories

The threat model analysis (TM-001, TM-002, TM-003, TM-004) identifies these as **Critical** severity risks requiring immediate mitigation.

## Decision

Implement a **multi-layered package security verification approach** with the following components:

### 1. Package Signature Verification

Verify package signatures before installation:

```python
# omni_scripts/package_managers/base.py
from typing import Optional
import hashlib

class PackageManagerBase:
    """Base class for package managers with security verification."""

    def verify_package_signature(
        self,
        package_name: str,
        package_version: str,
        signature_path: Optional[str] = None
    ) -> bool:
        """
        Verify package signature before installation.

        Args:
            package_name: Package name
            package_version: Package version
            signature_path: Path to signature file (optional)

        Returns:
            True if signature is valid, False otherwise
        """
        if not signature_path:
            # No signature available, skip verification
            return True

        # Calculate package checksum
        package_checksum = self._calculate_package_checksum(package_name, package_version)

        # Verify signature
        if not self._verify_signature(package_checksum, signature_path):
            raise SecurityError(
                f"Package signature verification failed: {package_name}@{package_version}"
            )

        return True
```

### 2. Exact Version Pinning

Pin all dependencies to exact versions to prevent dependency confusion:

```python
# conan/conanfile.py
class OmniCppConan(ConanFile):
    name = "omnicpp-template"
    version = "0.0.3"

    def requirements(self):
        # Use exact versions, not version ranges
        self.requires("fmt/10.2.1")  # Exact version
        # NOT: self.requires("fmt/[~10.2]")  # Version range
        self.requires("spdlog/1.14.1")
        self.requires("nlohmann_json/3.12.0")
        self.requires("zlib/1.3.1")
```

```json
// vcpkg.json
{
  "name": "omnicpp",
  "version": "0.0.3",
  "dependencies": [
    {
      "name": "fmt",
      "version>=": "10.2.1",
      "version<": "10.3.0"
    },
    {
      "name": "spdlog",
      "version>=": "1.14.1",
      "version<": "1.15.0"
    }
  ]
}
```

```cmake
# dependencies.cmake
CPMAddPackage(
    NAME fmt
    VERSION 10.2.1  # Exact version
    GITHUB_REPOSITORY fmtlib/fmt
    GIT_TAG 10.2.1  # Exact tag
    GIT_SHALLOW TRUE
)
```

### 3. Dependency Allowlisting

Maintain an allowlist of approved dependencies:

```python
# omni_scripts/package_managers/manager.py
ALLOWED_DEPENDENCIES = {
    "fmt": "10.2.1",
    "spdlog": "1.14.1",
    "nlohmann_json": "3.12.0",
    "zlib": "1.3.1",
    "glm": "0.9.9.8",
    "stb": "2.28.0",
    "catch2": "3.5.2",
    "gtest": "1.14.0",
    "vulkan-headers": "1.3.280.0",
    "vulkan-loader": "1.3.280.0",
    "qt6": "6.7.0"
}

def validate_dependency(self, name: str, version: str) -> bool:
    """Validate dependency against allowlist."""
    if name not in ALLOWED_DEPENDENCIES:
        raise SecurityError(
            f"Dependency {name} not in allowlist"
        )

    allowed_version = ALLOWED_DEPENDENCIES[name]
    if version != allowed_version:
        raise SecurityError(
            f"Dependency {name} version {version} not allowed. "
            f"Expected: {allowed_version}"
        )

    return True
```

### 4. Lock Files

Generate and use lock files for reproducible builds:

```bash
# Generate Conan lock file
conan lock create conanfile.py --lockfile-out=conan.lock

# Use lock file in builds
conan install . --lockfile=conan.lock
```

```bash
# Generate vcpkg lock file (vcpkg-lock.json is auto-generated)
vcpkg install --triplet x64-windows
```

```cmake
# Use CPM lock file
CPMUseLockFile(${CMAKE_SOURCE_DIR}/cpm.lock)
```

### 5. Private Package Repositories

Use private package repositories with authentication:

```bash
# Configure Conan to use private repository first
conan remote add company-registry https://conan.company.com --index 0
```

```bash
# Configure vcpkg to use private registry
vcpkg set-registry https://vcpkg.company.com
```

### 6. SBOM Generation

Generate Software Bill of Materials (SBOM) for all builds:

```python
# omni_scripts/package_managers/manager.py
import json
from typing import Dict, Any

def generate_sbom(self) -> Dict[str, Any]:
    """Generate Software Bill of Materials for all dependencies."""
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "metadata": {
            "component": {
                "name": "omnicpp-template",
                "version": "0.0.3",
                "type": "application"
            }
        },
        "components": []
    }

    # Add all dependencies
    for package_name, version in self.dependencies.items():
        sbom["components"].append({
            "name": package_name,
            "version": version,
            "type": "library",
            "purl": f"pkg:generic/{package_name}@{version}"
        })

    # Write SBOM to file
    with open("sbom.json", "w") as f:
        json.dump(sbom, f, indent=2)

    return sbom
```

## Consequences

### Positive

1. **Security:** Multiple layers of protection against malicious packages
2. **Reproducibility:** Lock files ensure consistent dependency versions
3. **Auditability:** SBOM provides complete dependency inventory
4. **Compliance:** Meets security best practices and regulatory requirements
5. **Supply Chain Security:** Reduces risk of supply chain attacks
6. **Traceability:** Can trace which dependencies are used in each build

### Negative

1. **Complexity:** Multiple security layers increase configuration complexity
2. **Maintenance:** Allowlists and lock files require ongoing maintenance
3. **Build Time:** Signature verification adds to build time
4. **Learning Curve:** Developers need to understand security verification process
5. **False Positives:** Strict validation may reject legitimate packages
6. **Dependency Updates:** Updating dependencies requires updating multiple files

### Neutral

1. **Documentation:** Requires documentation for security verification process
2. **Testing:** Need to test security verification mechanisms

## Alternatives Considered

### Alternative 1: No Security Verification

**Description:** Download and install packages without any verification

**Pros:**
- Simplest approach
- Fastest builds
- No maintenance burden

**Cons:**
- High security risk
- Vulnerable to malicious packages
- No reproducibility
- No audit trail

**Rejected:** Unacceptable security risk

### Alternative 2: Signature Verification Only

**Description:** Only verify package signatures, no version pinning or allowlisting

**Pros:**
- Protects against package tampering
- Simpler than full approach

**Cons:**
- Doesn't prevent dependency confusion
- Doesn't prevent typosquatting
- Doesn't ensure reproducibility

**Rejected:** Insufficient protection

### Alternative 3: Version Pinning Only

**Description:** Only pin versions, no signature verification or allowlisting

**Pros:**
- Ensures reproducibility
- Prevents dependency confusion
- Simple to implement

**Cons:**
- Doesn't protect against malicious packages
- Doesn't protect against typosquatting
- Vulnerable to supply chain compromise

**Rejected:** Insufficient protection

### Alternative 4: Allowlisting Only

**Description:** Only use allowlist, no signature verification or version pinning

**Pros:**
- Prevents unauthorized dependencies
- Simple to understand

**Cons:**
- Doesn't protect against malicious packages in allowlist
- Doesn't ensure reproducibility
- High maintenance burden
- Inflexible

**Rejected:** Too restrictive, doesn't protect against all threats

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-002: Priority-based package manager selection](ADR-002-priority-based-package-manager-selection.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)
- [ADR-020: Dependency integrity verification](ADR-020-dependency-integrity-verification.md)

## References

- [Conan Security Best Practices](https://docs.conan.io/en/latest/concepts/secure_practices/)
- [vcpkg Security](https://vcpkg.io/en/docs/users/security/)
- [CycloneDX SBOM Standard](https://cyclonedx.org/)
- [OWASP Dependency Confusion](https://owasp.org/www-community/attacks/04/Dependency_Confusion)
- [NIST Supply Chain Security](https://www.nist.gov/cyberframework)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
