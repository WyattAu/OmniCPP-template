# DES-014: vcpkg Integration Design

## Overview
Defines vcpkg package manager integration for managing C++ dependencies.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import subprocess
import json
import os

class VcpkgTriplet(Enum):
    """vcpkg triplet types"""
    X64_WINDOWS = "x64-windows"
    X86_WINDOWS = "x86-windows"
    X64_LINUX = "x64-linux"
    X86_LINUX = "x86-linux"
    X64_OSX = "x64-osx"
    ARM64_WINDOWS = "arm64-windows"
    ARM64_OSX = "arm64-osx"

@dataclass
class VcpkgPackage:
    """vcpkg package information"""
    name: str
    version: str
    triplet: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    license: Optional[str] = None
    dependencies: List[str] = None
    location: Optional[str] = None

@dataclass
class VcpkgConfig:
    """vcpkg configuration"""
    executable: str
    root_dir: str
    downloads_dir: str
    packages_dir: str
    installed_dir: str
    buildtrees_dir: str
    triplets_dir: str
    overlay_triplets: List[str]
    default_triplet: VcpkgTriplet

class IVcpkgManager(ABC):
    """Interface for vcpkg package manager"""

    @abstractmethod
    def install(self, package: str, triplet: Optional[str] = None) -> bool:
        """Install vcpkg package"""
        pass

    @abstractmethod
    def remove(self, package: str, triplet: Optional[str] = None) -> bool:
        """Remove vcpkg package"""
        pass

    @abstractmethod
    def update(self) -> bool:
        """Update vcpkg package database"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[VcpkgPackage]:
        """Search for packages"""
        pass

    @abstractmethod
    def info(self, package: str) -> Optional[VcpkgPackage]:
        """Get package information"""
        pass

    @abstractmethod
    def list_installed(self, triplet: Optional[str] = None) -> List[VcpkgPackage]:
        """List installed packages"""
        pass

    @abstractmethod
    def get_dependencies(self, package: str, triplet: Optional[str] = None) -> List[str]:
        """Get package dependencies"""
        pass

    @abstractmethod
    def export(self, packages: List[str], output_file: str,
               triplet: Optional[str] = None) -> bool:
        """Export package list to file"""
        pass

    @abstractmethod
    def import_packages(self, input_file: str) -> bool:
        """Import package list from file"""
        pass

    @abstractmethod
    def integrate(self, project: str) -> bool:
        """Integrate vcpkg with project"""
        pass

    @abstractmethod
    def remove_integration(self, project: str) -> bool:
        """Remove vcpkg integration from project"""
        pass

    @abstractmethod
    def create_triplet(self, name: str, triplet: str) -> bool:
        """Create custom triplet"""
        pass

    @abstractmethod
    def list_triplets(self) -> List[str]:
        """List available triplets"""
        pass

class VcpkgManager(IVcpkgManager):
    """Implementation of vcpkg package manager"""

    def __init__(self, config: VcpkgConfig) -> None:
        """Initialize vcpkg manager"""
        self._config = config
        self._cache: Dict[str, Any] = {}

    def install(self, package: str, triplet: Optional[str] = None) -> bool:
        """Install vcpkg package"""
        args = ["install", package]

        if triplet:
            args.extend(["--triplet", triplet])
        elif self._config.default_triplet:
            args.extend(["--triplet", self._config.default_triplet.value])

        result = self._execute_command(args)
        return result.returncode == 0

    def remove(self, package: str, triplet: Optional[str] = None) -> bool:
        """Remove vcpkg package"""
        args = ["remove", package]

        if triplet:
            args.extend(["--triplet", triplet])
        elif self._config.default_triplet:
            args.extend(["--triplet", self._config.default_triplet.value])

        result = self._execute_command(args)
        return result.returncode == 0

    def update(self) -> bool:
        """Update vcpkg package database"""
        result = self._execute_command(["update"])
        return result.returncode == 0

    def search(self, query: str) -> List[VcpkgPackage]:
        """Search for packages"""
        result = self._execute_command(["search", query])

        if result.returncode != 0:
            return []

        packages = []
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 1:
                    packages.append(VcpkgPackage(
                        name=parts[0],
                        version="latest"
                    ))

        return packages

    def info(self, package: str) -> Optional[VcpkgPackage]:
        """Get package information"""
        result = self._execute_command(["info", package])

        if result.returncode != 0:
            return None

        # Parse output
        lines = result.stdout.strip().split('\n')
        version = "latest"
        description = None
        homepage = None
        license = None
        dependencies = []

        for line in lines:
            if line.startswith("Version:"):
                version = line.split(":", 1)[1].strip()
            elif line.startswith("Description:"):
                description = line.split(":", 1)[1].strip()
            elif line.startswith("Homepage:"):
                homepage = line.split(":", 1)[1].strip()
            elif line.startswith("License:"):
                license = line.split(":", 1)[1].strip()
            elif line.startswith("Dependencies:"):
                deps_str = line.split(":", 1)[1].strip()
                dependencies = [d.strip() for d in deps_str.split(',') if d.strip()]

        return VcpkgPackage(
            name=package,
            version=version,
            description=description,
            homepage=homepage,
            license=license,
            dependencies=dependencies
        )

    def list_installed(self, triplet: Optional[str] = None) -> List[VcpkgPackage]:
        """List installed packages"""
        args = ["list"]

        if triplet:
            args.extend(["--triplet", triplet])
        elif self._config.default_triplet:
            args.extend(["--triplet", self._config.default_triplet.value])

        result = self._execute_command(args)

        if result.returncode != 0:
            return []

        packages = []
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append(VcpkgPackage(
                        name=parts[0],
                        version=parts[1],
                        location=os.path.join(self._config.installed_dir, parts[0])
                    ))

        return packages

    def get_dependencies(self, package: str, triplet: Optional[str] = None) -> List[str]:
        """Get package dependencies"""
        args = ["depend-info", package]

        if triplet:
            args.extend(["--triplet", triplet])
        elif self._config.default_triplet:
            args.extend(["--triplet", self._config.default_triplet.value])

        result = self._execute_command(args)

        if result.returncode != 0:
            return []

        dependencies = []
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if line.strip():
                dependencies.append(line.strip())

        return dependencies

    def export(self, packages: List[str], output_file: str,
               triplet: Optional[str] = None) -> bool:
        """Export package list to file"""
        args = ["export", output_file]
        args.extend(packages)

        if triplet:
            args.extend(["--triplet", triplet])
        elif self._config.default_triplet:
            args.extend(["--triplet", self._config.default_triplet.value])

        result = self._execute_command(args)
        return result.returncode == 0

    def import_packages(self, input_file: str) -> bool:
        """Import package list from file"""
        result = self._execute_command(["import", input_file])
        return result.returncode == 0

    def integrate(self, project: str) -> bool:
        """Integrate vcpkg with project"""
        result = self._execute_command(["integrate", "install", "--project", project])
        return result.returncode == 0

    def remove_integration(self, project: str) -> bool:
        """Remove vcpkg integration from project"""
        result = self._execute_command(["integrate", "remove", "--project", project])
        return result.returncode == 0

    def create_triplet(self, name: str, triplet: str) -> bool:
        """Create custom triplet"""
        triplet_path = os.path.join(self._config.triplets_dir, f"{name}.cmake")

        try:
            with open(triplet_path, 'w') as f:
                f.write(f"set(VCPKG_TARGET_TRIPLET {triplet})\n")

            return True
        except IOError:
            return False

    def list_triplets(self) -> List[str]:
        """List available triplets"""
        if not os.path.exists(self._config.triplets_dir):
            return []

        triplets = []
        for file in os.listdir(self._config.triplets_dir):
            if file.endswith('.cmake'):
                triplets.append(file.rsplit('.', 1)[0])

        return triplets

    def _execute_command(self, args: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
        """Execute vcpkg command"""
        return subprocess.run(
            [self._config.executable] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )

class VcpkgTripletGenerator:
    """Generator for vcpkg triplets"""

    @staticmethod
    def generate_windows_x64() -> str:
        """Generate x64-windows triplet"""
        return "x64-windows"

    @staticmethod
    def generate_windows_x86() -> str:
        """Generate x86-windows triplet"""
        return "x86-windows"

    @staticmethod
    def generate_linux_x64() -> str:
        """Generate x64-linux triplet"""
        return "x64-linux"

    @staticmethod
    def generate_linux_x86() -> str:
        """Generate x86-linux triplet"""
        return "x86-linux"

    @staticmethod
    def generate_osx_x64() -> str:
        """Generate x64-osx triplet"""
        return "x64-osx"

    @staticmethod
    def generate_arm64_windows() -> str:
        """Generate arm64-windows triplet"""
        return "arm64-windows"

    @staticmethod
    def generate_arm64_osx() -> str:
        """Generate arm64-osx triplet"""
        return "arm64-osx"

    @staticmethod
    def generate_custom_triplet(architecture: str, os: str,
                             compiler: str = "msvc",
                             runtime: str = "dynamic") -> str:
        """Generate custom triplet"""
        return f"{architecture}-{os}-{compiler}-{runtime}"
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-012` - Package manager interface

### External Dependencies
- `subprocess` - Process execution
- `json` - JSON parsing
- `os` - Operating system interface
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-017: vcpkg Integration
- REQ-019: Priority-Based Package Manager Selection
- REQ-020: Package Security Verification
- REQ-021: Dependency Resolution & Caching

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### vcpkg Detection
1. Check for vcpkg executable in PATH
2. Execute vcpkg version
3. Parse version output
4. Validate minimum version

### Triplet Management
1. Use default triplets for common platforms
2. Create custom triplets for specific configurations
3. Store triplets in triplets directory
4. Support overlay triplets

### Package Installation Flow
1. Resolve package dependencies
2. Download package source
3. Build package from source
4. Install to installed directory
5. Generate integration files

### Integration with CMake
1. Generate vcpkg toolchain file
2. Set CMAKE_TOOLCHAIN_FILE
3. Set CMAKE_PREFIX_PATH
4. Generate vcpkg.cmake for project integration

## Usage Example

```python
from omni_scripts.vcpkg import (
    VcpkgManager,
    VcpkgConfig,
    VcpkgTriplet,
    VcpkgTripletGenerator
)

# Create vcpkg configuration
config = VcpkgConfig(
    executable="vcpkg",
    root_dir="C:/vcpkg",
    downloads_dir="C:/vcpkg/downloads",
    packages_dir="C:/vcpkg/packages",
    installed_dir="C:/vcpkg/installed",
    buildtrees_dir="C:/vcpkg/buildtrees",
    triplets_dir="C:/vcpkg/triplets",
    overlay_triplets=[],
    default_triplet=VcpkgTriplet.X64_WINDOWS
)

# Create vcpkg manager
manager = VcpkgManager(config)

# Install package
if manager.install("fmt"):
    print("Package installed successfully")

# List installed packages
packages = manager.list_installed()
for pkg in packages:
    print(f"{pkg.name} v{pkg.version}")

# Integrate with project
if manager.integrate("C:/path/to/project"):
    print("Integration successful")
```
