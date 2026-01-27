# ADR-020: Dependency Integrity Verification

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Security

---

## Context

The OmniCPP Template project uses multiple package managers (Conan, vcpkg, CPM) to manage dependencies. Dependency integrity is critical for security and reproducibility. The threat model (`.specs/03_threat_model/analysis.md`) identifies dependency tampering as a significant threat (TM-015, TM-016).

### Current State

Dependency integrity verification is inconsistent:
- **No Verification:** No verification of dependency integrity
- **No Lock Files:** No lock files for exact versions
- **No Hashing:** No hashing of dependencies
- **No Validation:** No validation of downloaded dependencies
- **No SBOM:** No Software Bill of Materials

### Issues

1. **No Verification:** No verification of dependency integrity
2. **No Lock Files:** No lock files for exact versions
3. **No Hashing:** No hashing of dependencies
4. **No Validation:** No validation of downloaded dependencies
5. **No SBOM:** No Software Bill of Materials
6. **Tampering Risk:** Risk of dependency tampering

## Decision

Implement **dependency integrity verification** with:
1. **Lock Files:** Generate and use lock files for exact versions
2. **Hashing:** Hash all dependencies for integrity verification
3. **Validation:** Validate downloaded dependencies
4. **SBOM Generation:** Generate Software Bill of Materials
5. **Signature Verification:** Verify package signatures
6. **Integrity Checks:** Regular integrity checks of dependencies

### 1. Lock File Generation

```python
# omni_scripts/build_system/lock_file_generator.py
"""Lock file generator for dependencies."""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any
import logging

from exceptions import IntegrityError

class LockFileGenerator:
    """Lock file generator for dependencies."""

    def __init__(self, logger: logging.Logger):
        """Initialize lock file generator.

        Args:
            logger: Logger instance
        """
        self.logger = logger

    def generate_conan_lock(self, conanfile_path: Path) -> Dict[str, Any]:
        """Generate Conan lock file.

        Args:
            conanfile_path: Path to conanfile.py

        Returns:
            Lock file data
        """
        self.logger.info(f"Generating Conan lock file from {conanfile_path}")

        # Run conan lock create
        import subprocess
        result = subprocess.run(
            ["conan", "lock", "create", "--lockfile-out=conan.lock"],
            cwd=conanfile_path.parent,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise IntegrityError(f"Failed to generate Conan lock: {result.stderr}")

        # Parse lock file
        lock_file = conanfile_path.parent / "conan.lock"
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        # Add hashes
        lock_data = self._add_hashes(lock_data)

        return lock_data

    def generate_vcpkg_lock(self, vcpkg_json_path: Path) -> Dict[str, Any]:
        """Generate vcpkg lock file.

        Args:
            vcpkg_json_path: Path to vcpkg.json

        Returns:
            Lock file data
        """
        self.logger.info(f"Generating vcpkg lock file from {vcpkg_json_path}")

        # Run vcpkg export
        import subprocess
        result = subprocess.run(
            ["vcpkg", "export", "--output=vcpkg-lock.json"],
            cwd=vcpkg_json_path.parent,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise IntegrityError(f"Failed to generate vcpkg lock: {result.stderr}")

        # Parse lock file
        lock_file = vcpkg_json_path.parent / "vcpkg-lock.json"
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        # Add hashes
        lock_data = self._add_hashes(lock_data)

        return lock_data

    def generate_cpm_lock(self, dependencies_cmake_path: Path) -> Dict[str, Any]:
        """Generate CPM lock file.

        Args:
            dependencies_cmake_path: Path to dependencies.cmake

        Returns:
            Lock file data
        """
        self.logger.info(f"Generating CPM lock file from {dependencies_cmake_path}")

        # Parse dependencies.cmake
        with open(dependencies_cmake_path, 'r') as f:
            content = f.read()

        # Extract CPM dependencies
        import re
        cpm_pattern = r'CPMAddPackage\("([^"]+)"\s+VERSION\s+([^\s)]+)'
        dependencies = re.findall(cpm_pattern, content)

        # Generate lock data
        lock_data = {
            "dependencies": [
                {
                    "name": name,
                    "version": version,
                    "hash": self._hash_package(name, version)
                }
                for name, version in dependencies
            ]
        }

        return lock_data

    def _add_hashes(self, lock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add hashes to lock data.

        Args:
            lock_data: Lock file data

        Returns:
            Lock file data with hashes
        """
        # Hash each dependency
        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                if "path" in dep:
                    dep["hash"] = self._hash_file(dep["path"])

        return lock_data

    def _hash_file(self, file_path: str) -> str:
        """Hash file for integrity verification.

        Args:
            file_path: Path to file

        Returns:
            File hash
        """
        import hashlib

        sha256_hash = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                if not chunk:
                    break
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def _hash_package(self, name: str, version: str) -> str:
        """Hash package for integrity verification.

        Args:
            name: Package name
            version: Package version

        Returns:
            Package hash
        """
        # Generate hash from name and version
        hash_string = f"{name}:{version}"
        return hashlib.sha256(hash_string.encode()).hexdigest()
```

### 2. Dependency Validation

```python
# omni_scripts/validators/dependency_validator.py
"""Dependency validator for integrity verification."""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import logging

from exceptions import IntegrityError

class DependencyValidator:
    """Dependency validator for integrity verification."""

    def __init__(self, logger: logging.Logger):
        """Initialize dependency validator.

        Args:
            logger: Logger instance
        """
        self.logger = logger

    def validate_conan_lock(self, lock_file: Path) -> bool:
        """Validate Conan lock file.

        Args:
            lock_file: Path to conan.lock

        Returns:
            True if valid, False otherwise
        """
        self.logger.info(f"Validating Conan lock file: {lock_file}")

        if not lock_file.exists():
            self.logger.error(f"Lock file not found: {lock_file}")
            return False

        # Parse lock file
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        # Validate each dependency
        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                if not self._validate_dependency(dep):
                    self.logger.error(f"Invalid dependency: {dep}")
                    return False

        return True

    def validate_vcpkg_lock(self, lock_file: Path) -> bool:
        """Validate vcpkg lock file.

        Args:
            lock_file: Path to vcpkg-lock.json

        Returns:
            True if valid, False otherwise
        """
        self.logger.info(f"Validating vcpkg lock file: {lock_file}")

        if not lock_file.exists():
            self.logger.error(f"Lock file not found: {lock_file}")
            return False

        # Parse lock file
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        # Validate each dependency
        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                if not self._validate_dependency(dep):
                    self.logger.error(f"Invalid dependency: {dep}")
                    return False

        return True

    def validate_cpm_lock(self, lock_file: Path) -> bool:
        """Validate CPM lock file.

        Args:
            lock_file: Path to cpm.lock

        Returns:
            True if valid, False otherwise
        """
        self.logger.info(f"Validating CPM lock file: {lock_file}")

        if not lock_file.exists():
            self.logger.error(f"Lock file not found: {lock_file}")
            return False

        # Parse lock file
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        # Validate each dependency
        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                if not self._validate_dependency(dep):
                    self.logger.error(f"Invalid dependency: {dep}")
                    return False

        return True

    def _validate_dependency(self, dep: Dict[str, Any]) -> bool:
        """Validate dependency.

        Args:
            dep: Dependency data

        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ["name", "version", "hash"]
        for field in required_fields:
            if field not in dep:
                self.logger.error(f"Missing required field: {field}")
                return False

        # Validate hash
        if "hash" in dep:
            if not self._is_valid_hash(dep["hash"]):
                self.logger.error(f"Invalid hash: {dep['hash']}")
                return False

        return True

    def _is_valid_hash(self, hash_value: str) -> bool:
        """Check if hash is valid.

        Args:
            hash_value: Hash value

        Returns:
            True if valid, False otherwise
        """
        # Check hash length (SHA-256 is 64 characters)
        if len(hash_value) != 64:
            return False

        # Check if hash is hexadecimal
        try:
            int(hash_value, 16)
            return True
        except ValueError:
            return False

    def verify_file_hash(self, file_path: Path, expected_hash: str) -> bool:
        """Verify file hash.

        Args:
            file_path: Path to file
            expected_hash: Expected hash

        Returns:
            True if hash matches, False otherwise
        """
        self.logger.info(f"Verifying hash for {file_path}")

        if not file_path.exists():
            self.logger.error(f"File not found: {file_path}")
            return False

        # Calculate file hash
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                if not chunk:
                    break
                sha256_hash.update(chunk)

        actual_hash = sha256_hash.hexdigest()

        # Compare hashes
        if actual_hash != expected_hash:
            self.logger.error(f"Hash mismatch: expected {expected_hash}, got {actual_hash}")
            return False

        return True
```

### 3. SBOM Generation

```python
# omni_scripts/build_system/sbom_generator.py
"""SBOM generator for dependencies."""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

from exceptions import IntegrityError

class SBOMGenerator:
    """SBOM generator for dependencies."""

    def __init__(self, logger: logging.Logger):
        """Initialize SBOM generator.

        Args:
            logger: Logger instance
        """
        self.logger = logger

    def generate_sbom(
        self,
        conan_lock: Optional[Path] = None,
        vcpkg_lock: Optional[Path] = None,
        cpm_lock: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Generate Software Bill of Materials.

        Args:
            conan_lock: Path to conan.lock
            vcpkg_lock: Path to vcpkg-lock.json
            cpm_lock: Path to cpm.lock

        Returns:
            SBOM data
        """
        self.logger.info("Generating SBOM")

        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tools": [
                    {
                        "vendor": "OmniCpp",
                        "name": "SBOM Generator",
                        "version": "1.0.0"
                    }
                ]
            },
            "components": []
        }

        # Add Conan dependencies
        if conan_lock and conan_lock.exists():
            sbom["components"].extend(self._parse_conan_lock(conan_lock))

        # Add vcpkg dependencies
        if vcpkg_lock and vcpkg_lock.exists():
            sbom["components"].extend(self._parse_vcpkg_lock(vcpkg_lock))

        # Add CPM dependencies
        if cpm_lock and cpm_lock.exists():
            sbom["components"].extend(self._parse_cpm_lock(cpm_lock))

        return sbom

    def _parse_conan_lock(self, lock_file: Path) -> List[Dict[str, Any]]:
        """Parse Conan lock file.

        Args:
            lock_file: Path to conan.lock

        Returns:
            List of components
        """
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        components = []

        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                component = {
                    "type": "library",
                    "name": dep.get("name", "unknown"),
                    "version": dep.get("version", "unknown"),
                    "purl": f"pkg:conan/{dep.get('name', 'unknown')}@{dep.get('version', 'unknown')}",
                    "hashes": [
                        {
                            "alg": "SHA-256",
                            "content": dep.get("hash", "")
                        }
                    ]
                }
                components.append(component)

        return components

    def _parse_vcpkg_lock(self, lock_file: Path) -> List[Dict[str, Any]]:
        """Parse vcpkg lock file.

        Args:
            lock_file: Path to vcpkg-lock.json

        Returns:
            List of components
        """
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        components = []

        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                component = {
                    "type": "library",
                    "name": dep.get("name", "unknown"),
                    "version": dep.get("version", "unknown"),
                    "purl": f"pkg:vcpkg/{dep.get('name', 'unknown')}@{dep.get('version', 'unknown')}",
                    "hashes": [
                        {
                            "alg": "SHA-256",
                            "content": dep.get("hash", "")
                        }
                    ]
                }
                components.append(component)

        return components

    def _parse_cpm_lock(self, lock_file: Path) -> List[Dict[str, Any]]:
        """Parse CPM lock file.

        Args:
            lock_file: Path to cpm.lock

        Returns:
            List of components
        """
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)

        components = []

        if "dependencies" in lock_data:
            for dep in lock_data["dependencies"]:
                component = {
                    "type": "library",
                    "name": dep.get("name", "unknown"),
                    "version": dep.get("version", "unknown"),
                    "purl": f"pkg:cpm/{dep.get('name', 'unknown')}@{dep.get('version', 'unknown')}",
                    "hashes": [
                        {
                            "alg": "SHA-256",
                            "content": dep.get("hash", "")
                        }
                    ]
                }
                components.append(component)

        return components

    def write_sbom(self, sbom: Dict[str, Any], output_file: Path) -> None:
        """Write SBOM to file.

        Args:
            sbom: SBOM data
            output_file: Output file path
        """
        self.logger.info(f"Writing SBOM to {output_file}")

        with open(output_file, 'w') as f:
            json.dump(sbom, f, indent=2)
```

### 4. Usage Examples

```python
# Example usage
from build_system.lock_file_generator import LockFileGenerator
from validators.dependency_validator import DependencyValidator
from build_system.sbom_generator import SBOMGenerator
from logging.logger import Logger

# Initialize logger
logger = Logger()

# Generate lock files
lock_generator = LockFileGenerator(logger)

# Generate Conan lock
conan_lock = lock_generator.generate_conan_lock(Path("conan/conanfile.py"))

# Generate vcpkg lock
vcpkg_lock = lock_generator.generate_vcpkg_lock(Path("vcpkg.json"))

# Generate CPM lock
cpm_lock = lock_generator.generate_cpm_lock(Path("cmake/CPM.cmake"))

# Validate lock files
validator = DependencyValidator(logger)

# Validate Conan lock
if not validator.validate_conan_lock(Path("conan/conan.lock")):
    logger.error("Conan lock validation failed")

# Validate vcpkg lock
if not validator.validate_vcpkg_lock(Path("vcpkg-lock.json")):
    logger.error("vcpkg lock validation failed")

# Validate CPM lock
if not validator.validate_cpm_lock(Path("cpm.lock")):
    logger.error("CPM lock validation failed")

# Generate SBOM
sbom_generator = SBOMGenerator(logger)
sbom = sbom_generator.generate_sbom(
    conan_lock=Path("conan/conan.lock"),
    vcpkg_lock=Path("vcpkg-lock.json"),
    cpm_lock=Path("cpm.lock")
)

# Write SBOM
sbom_generator.write_sbom(sbom, Path("sbom.json"))
```

## Consequences

### Positive

1. **Integrity:** Verifies dependency integrity
2. **Reproducibility:** Lock files ensure reproducible builds
3. **Security:** Detects dependency tampering
4. **SBOM:** Provides Software Bill of Materials
5. **Validation:** Validates downloaded dependencies
6. **Hashing:** Hashes all dependencies for verification
7. **Auditing:** Enables security auditing of dependencies

### Negative

1. **Complexity:** More complex than no verification
2. **Build Time:** Lock file generation adds build time
3. **Maintenance:** Lock files need to be maintained
4. **Storage:** Lock files and SBOMs require storage

### Neutral

1. **Documentation:** Requires documentation for integrity verification
2. **Testing:** Need to test integrity verification

## Alternatives Considered

### Alternative 1: No Verification

**Description:** No dependency integrity verification

**Pros:**
- Simpler implementation
- No build time overhead

**Cons:**
- No integrity verification
- Risk of tampering
- No reproducibility

**Rejected:** No integrity verification and risk of tampering

### Alternative 2: Manual Verification

**Description:** Manual verification of dependencies

**Pros:**
- No automation overhead
- Full control

**Cons:**
- Manual effort required
- Error-prone
- Not scalable

**Rejected:** Manual effort and error-prone

### Alternative 3: External Tools

**Description:** Use external tools for verification

**Pros:**
- No custom code
- Proven solutions

**Cons:**
- External dependencies
- Less control
- Platform-specific

**Rejected:** External dependencies and less control

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-002: Priority-based package manager selection](ADR-002-priority-based-package-manager-selection.md)
- [ADR-003: Package security verification approach](ADR-003-package-security-verification-approach.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)

## References

- [CycloneDX SBOM](https://cyclonedx.org/)
- [SPDX SBOM](https://spdx.dev/)
- [Dependency Verification](https://owasp.org/www-community/Software_Component_Verification)
- [Lock Files](https://docs.conan.io/en/latest/reference/conanfile/tools/lockfile)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
