# DES-012: Package Manager Interface

## Overview
Defines the package manager interface for managing dependencies across different package managers (Conan, vcpkg, CPM).

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import subprocess
import json

class PackageManagerType(Enum):
    """Package manager types"""
    CONAN = "conan"
    VCPKG = "vcpkg"
    CPM = "cpm"
    UNKNOWN = "unknown"

class PackageStatus(Enum):
    """Package status"""
    INSTALLED = "installed"
    NOT_INSTALLED = "not_installed"
    OUTDATED = "outdated"
    ERROR = "error"

@dataclass
class PackageInfo:
    """Package information"""
    name: str
    version: str
    status: PackageStatus
    description: Optional[str] = None
    homepage: Optional[str] = None
    license: Optional[str] = None
    dependencies: List[str] = None
    location: Optional[str] = None

@dataclass
class PackageDependency:
    """Package dependency"""
    name: str
    version: Optional[str] = None
    required: bool = True
    scope: Optional[str] = None  # build, test, runtime, etc.

@dataclass
class PackageManagerConfig:
    """Package manager configuration"""
    type: PackageManagerType
    executable: Optional[str] = None
    config_file: Optional[str] = None
    cache_dir: Optional[str] = None
    install_dir: Optional[str] = None
    environment: Dict[str, str] = None

class IPackageManager(ABC):
    """Interface for package manager"""

    @abstractmethod
    def get_type(self) -> PackageManagerType:
        """Get package manager type"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if package manager is available"""
        pass

    @abstractmethod
    def install(self, package: str, version: Optional[str] = None) -> bool:
        """Install package"""
        pass

    @abstractmethod
    def uninstall(self, package: str) -> bool:
        """Uninstall package"""
        pass

    @abstractmethod
    def update(self, package: Optional[str] = None) -> bool:
        """Update package(s)"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[PackageInfo]:
        """Search for packages"""
        pass

    @abstractmethod
    def info(self, package: str) -> Optional[PackageInfo]:
        """Get package information"""
        pass

    @abstractmethod
    def list_installed(self) -> List[PackageInfo]:
        """List installed packages"""
        pass

    @abstractmethod
    def get_dependencies(self, package: str) -> List[PackageDependency]:
        """Get package dependencies"""
        pass

    @abstractmethod
    def resolve_dependencies(self, packages: List[str]) -> List[PackageDependency]:
        """Resolve dependencies for multiple packages"""
        pass

    @abstractmethod
    def export(self, packages: List[str], output_file: str) -> bool:
        """Export package list to file"""
        pass

    @abstractmethod
    def import_packages(self, input_file: str) -> bool:
        """Import package list from file"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate package manager configuration"""
        pass

class BasePackageManager(IPackageManager):
    """Base implementation for package manager"""

    def __init__(self, config: PackageManagerConfig) -> None:
        """Initialize package manager"""
        self._config = config
        self._executable = config.executable
        self._cache: Dict[str, Any] = {}

    def get_type(self) -> PackageManagerType:
        """Get package manager type"""
        return self._config.type

    def is_available(self) -> bool:
        """Check if package manager is available"""
        if not self._executable:
            return False

        try:
            result = subprocess.run(
                [self._executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def install(self, package: str, version: Optional[str] = None) -> bool:
        """Install package"""
        raise NotImplementedError("Subclasses must implement install()")

    def uninstall(self, package: str) -> bool:
        """Uninstall package"""
        raise NotImplementedError("Subclasses must implement uninstall()")

    def update(self, package: Optional[str] = None) -> bool:
        """Update package(s)"""
        raise NotImplementedError("Subclasses must implement update()")

    def search(self, query: str) -> List[PackageInfo]:
        """Search for packages"""
        raise NotImplementedError("Subclasses must implement search()")

    def info(self, package: str) -> Optional[PackageInfo]:
        """Get package information"""
        raise NotImplementedError("Subclasses must implement info()")

    def list_installed(self) -> List[PackageInfo]:
        """List installed packages"""
        raise NotImplementedError("Subclasses must implement list_installed()")

    def get_dependencies(self, package: str) -> List[PackageDependency]:
        """Get package dependencies"""
        raise NotImplementedError("Subclasses must implement get_dependencies()")

    def resolve_dependencies(self, packages: List[str]) -> List[PackageDependency]:
        """Resolve dependencies for multiple packages"""
        all_dependencies = []
        seen = set()

        for package in packages:
            deps = self.get_dependencies(package)
            for dep in deps:
                if dep.name not in seen:
                    all_dependencies.append(dep)
                    seen.add(dep.name)

        return all_dependencies

    def export(self, packages: List[str], output_file: str) -> bool:
        """Export package list to file"""
        raise NotImplementedError("Subclasses must implement export()")

    def import_packages(self, input_file: str) -> bool:
        """Import package list from file"""
        raise NotImplementedError("Subclasses must implement import_packages()")

    def validate(self) -> bool:
        """Validate package manager configuration"""
        return self.is_available()

    def _execute_command(self, args: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
        """Execute command with timeout"""
        return subprocess.run(
            [self._executable] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )

    def _parse_version(self, output: str) -> Optional[str]:
        """Parse version from command output"""
        import re
        match = re.search(r'(\d+\.\d+\.\d+)', output)
        return match.group(1) if match else None

class PackageManagerFactory:
    """Factory for creating package managers"""

    @staticmethod
    def create(config: PackageManagerConfig) -> IPackageManager:
        """Create package manager from configuration"""
        if config.type == PackageManagerType.CONAN:
            from .DES-013 import ConanPackageManager
            return ConanPackageManager(config)
        elif config.type == PackageManagerType.VCPKG:
            from .DES-014 import VcpkgPackageManager
            return VcpkgPackageManager(config)
        elif config.type == PackageManagerType.CPM:
            from .DES-015 import CPMPackageManager
            return CPMPackageManager(config)
        else:
            raise ValueError(f"Unknown package manager type: {config.type}")

    @staticmethod
    def detect_available() -> List[PackageManagerType]:
        """Detect available package managers"""
        available = []

        # Check Conan
        try:
            result = subprocess.run(
                ["conan", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                available.append(PackageManagerType.CONAN)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Check vcpkg
        try:
            result = subprocess.run(
                ["vcpkg", "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                available.append(PackageManagerType.VCPKG)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # CPM is always available if CMake is available
        available.append(PackageManagerType.CPM)

        return available

    @staticmethod
    def get_default() -> Optional[PackageManagerType]:
        """Get default package manager based on priority"""
        available = PackageManagerFactory.detect_available()

        if not available:
            return None

        # Priority: Conan > vcpkg > CPM
        if PackageManagerType.CONAN in available:
            return PackageManagerType.CONAN
        elif PackageManagerType.VCPKG in available:
            return PackageManagerType.VCPKG
        else:
            return PackageManagerType.CPM

class PackageManagerSelector:
    """Selector for choosing package manager"""

    def __init__(self, priority: List[PackageManagerType] = None) -> None:
        """Initialize selector"""
        self._priority = priority or [
            PackageManagerType.CONAN,
            PackageManagerType.VCPKG,
            PackageManagerType.CPM
        ]
        self._available = PackageManagerFactory.detect_available()

    def select(self) -> Optional[PackageManagerType]:
        """Select package manager based on priority and availability"""
        for pm_type in self._priority:
            if pm_type in self._available:
                return pm_type
        return None

    def get_available(self) -> List[PackageManagerType]:
        """Get available package managers"""
        return self._available

    def set_priority(self, priority: List[PackageManagerType]) -> None:
        """Set priority order"""
        self._priority = priority
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-013` - Conan integration
- `DES-014` - vcpkg integration
- `DES-015` - CPM integration

### External Dependencies
- `subprocess` - Process execution
- `json` - JSON parsing
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-016: Conan Integration
- REQ-017: vcpkg Integration
- REQ-018: CPM CMake Integration
- REQ-019: Priority-Based Package Manager Selection
- REQ-020: Package Security Verification
- REQ-021: Dependency Resolution & Caching

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Package Manager Detection
1. Check for executable in PATH
2. Execute version command
3. Parse version output
4. Cache detection result

### Package Installation Flow
1. Resolve dependencies
2. Check for conflicts
3. Download packages
4. Install packages
5. Verify installation

### Dependency Resolution
1. Build dependency graph
2. Detect circular dependencies
3. Resolve version conflicts
4. Optimize installation order

### Error Handling
- Handle missing executables
- Handle network failures
- Handle version conflicts
- Provide clear error messages

## Usage Example

```python
from omni_scripts.package_manager import (
    PackageManagerFactory,
    PackageManagerSelector,
    PackageManagerType,
    PackageManagerConfig
)

# Detect available package managers
available = PackageManagerFactory.detect_available()
print(f"Available package managers: {[pm.value for pm in available]}")

# Select package manager
selector = PackageManagerSelector()
selected = selector.select()
print(f"Selected package manager: {selected.value if selected else 'None'}")

# Create package manager
config = PackageManagerConfig(
    type=selected,
    executable="conan"
)
pm = PackageManagerFactory.create(config)

# Install package
if pm.install("fmt/10.0.0"):
    print("Package installed successfully")
else:
    print("Package installation failed")

# List installed packages
packages = pm.list_installed()
for pkg in packages:
    print(f"{pkg.name} v{pkg.version}")
```
