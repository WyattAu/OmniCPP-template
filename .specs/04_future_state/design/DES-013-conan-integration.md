# DES-013: Conan Integration Design

## Overview
Defines the Conan package manager integration for managing C++ dependencies.

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

class ConanProfileType(Enum):
    """Conan profile types"""
    DEFAULT = "default"
    DEBUG = "debug"
    RELEASE = "release"
    RELWITHDEBINFO = "relwithdebinfo"
    MINSIZEREL = "minsizerel"

class ConanBuildType(Enum):
    """Conan build types"""
    DEBUG = "Debug"
    RELEASE = "Release"
    RELWITHDEBINFO = "RelWithDebInfo"
    MINSIZEREL = "MinSizeRel"

@dataclass
class ConanProfile:
    """Conan profile configuration"""
    name: str
    settings: Dict[str, str]
    build_requires: List[str]
    requires: List[str]
    tools: Dict[str, str]
    conf: Dict[str, str]
    env: Dict[str, str]

@dataclass
class ConanPackage:
    """Conan package information"""
    name: str
    version: str
    user: Optional[str] = None
    channel: Optional[str] = None
    recipe_file: Optional[str] = None
    options: Dict[str, str] = None
    settings: Dict[str, str] = None

@dataclass
class ConanConfig:
    """Conan configuration"""
    executable: str
    config_dir: str
    cache_dir: str
    profiles_dir: str
    remotes: List[Dict[str, str]]
    default_profile: str
    default_build_type: ConanBuildType

class IConanManager(ABC):
    """Interface for Conan package manager"""

    @abstractmethod
    def install(self, package: str, profile: Optional[str] = None,
                build_type: Optional[ConanBuildType] = None) -> bool:
        """Install Conan package"""
        pass

    @abstractmethod
    def remove(self, package: str) -> bool:
        """Remove Conan package"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[ConanPackage]:
        """Search for packages"""
        pass

    @abstractmethod
    def info(self, package: str) -> Optional[ConanPackage]:
        """Get package information"""
        pass

    @abstractmethod
    def create_profile(self, profile: ConanProfile) -> bool:
        """Create Conan profile"""
        pass

    @abstractmethod
    def get_profile(self, name: str) -> Optional[ConanProfile]:
        """Get Conan profile"""
        pass

    @abstractmethod
    def list_profiles(self) -> List[str]:
        """List available profiles"""
        pass

    @abstractmethod
    def install_toolchain(self, profile: Optional[str] = None) -> bool:
        """Install Conan toolchain"""
        pass

    @abstractmethod
    def export_toolchain(self, output_dir: str, profile: Optional[str] = None) -> bool:
        """Export Conan toolchain"""
        pass

    @abstractmethod
    def add_remote(self, name: str, url: str, verify_ssl: bool = True) -> bool:
        """Add Conan remote"""
        pass

    @abstractmethod
    def remove_remote(self, name: str) -> bool:
        """Remove Conan remote"""
        pass

    @abstractmethod
    def list_remotes(self) -> List[Dict[str, str]]:
        """List Conan remotes"""
        pass

    @abstractmethod
    def authenticate(self, remote: str, username: str, password: str) -> bool:
        """Authenticate with remote"""
        pass

    @abstractmethod
    def create(self, package: str, recipe_file: str) -> bool:
        """Create package from recipe"""
        pass

    @abstractmethod
    def export(self, package: str, recipe_file: str) -> bool:
        """Export package to cache"""
        pass

class ConanManager(IConanManager):
    """Implementation of Conan package manager"""

    def __init__(self, config: ConanConfig) -> None:
        """Initialize Conan manager"""
        self._config = config
        self._cache: Dict[str, Any] = {}

    def install(self, package: str, profile: Optional[str] = None,
                build_type: Optional[ConanBuildType] = None) -> bool:
        """Install Conan package"""
        args = ["install", package]

        if profile:
            args.extend(["--profile", profile])
        elif self._config.default_profile:
            args.extend(["--profile", self._config.default_profile])

        if build_type:
            args.extend(["--build", build_type.value])
        elif self._config.default_build_type:
            args.extend(["--build", self._config.default_build_type.value])

        result = self._execute_command(args)
        return result.returncode == 0

    def remove(self, package: str) -> bool:
        """Remove Conan package"""
        result = self._execute_command(["remove", package, "--force"])
        return result.returncode == 0

    def search(self, query: str) -> List[ConanPackage]:
        """Search for packages"""
        result = self._execute_command(["search", query])

        if result.returncode != 0:
            return []

        packages = []
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if line.strip():
                parts = line.split('/')
                if len(parts) >= 2:
                    packages.append(ConanPackage(
                        name=parts[0],
                        version=parts[1].split('@')[0]
                    ))

        return packages

    def info(self, package: str) -> Optional[ConanPackage]:
        """Get package information"""
        result = self._execute_command(["info", package, "--json"])

        if result.returncode != 0:
            return None

        try:
            info = json.loads(result.stdout)
            return ConanPackage(
                name=info.get("name", ""),
                version=info.get("version", ""),
                description=info.get("description"),
                homepage=info.get("homepage"),
                license=info.get("license")
            )
        except json.JSONDecodeError:
            return None

    def create_profile(self, profile: ConanProfile) -> bool:
        """Create Conan profile"""
        profile_path = os.path.join(self._config.profiles_dir, profile.name)

        try:
            with open(profile_path, 'w') as f:
                f.write("[settings]\n")
                for key, value in profile.settings.items():
                    f.write(f"{key}={value}\n")

                f.write("\n[build_requires]\n")
                for req in profile.build_requires:
                    f.write(f"{req}\n")

                f.write("\n[requires]\n")
                for req in profile.requires:
                    f.write(f"{req}\n")

                f.write("\n[tools]\n")
                for key, value in profile.tools.items():
                    f.write(f"{key}={value}\n")

                f.write("\n[conf]\n")
                for key, value in profile.conf.items():
                    f.write(f"{key}={value}\n")

                f.write("\n[env]\n")
                for key, value in profile.env.items():
                    f.write(f"{key}={value}\n")

            return True
        except IOError:
            return False

    def get_profile(self, name: str) -> Optional[ConanProfile]:
        """Get Conan profile"""
        profile_path = os.path.join(self._config.profiles_dir, name)

        if not os.path.exists(profile_path):
            return None

        try:
            with open(profile_path, 'r') as f:
                content = f.read()

            return self._parse_profile(content, name)
        except IOError:
            return None

    def list_profiles(self) -> List[str]:
        """List available profiles"""
        if not os.path.exists(self._config.profiles_dir):
            return []

        profiles = []
        for file in os.listdir(self._config.profiles_dir):
            if file.endswith('.txt') or file.endswith('.conf'):
                profiles.append(file.rsplit('.', 1)[0])

        return profiles

    def install_toolchain(self, profile: Optional[str] = None) -> bool:
        """Install Conan toolchain"""
        args = ["install", "--toolchain", "requires"]

        if profile:
            args.extend(["--profile", profile])
        elif self._config.default_profile:
            args.extend(["--profile", self._config.default_profile])

        result = self._execute_command(args)
        return result.returncode == 0

    def export_toolchain(self, output_dir: str, profile: Optional[str] = None) -> bool:
        """Export Conan toolchain"""
        args = ["install", "--toolchain", "requires", "--toolchains", output_dir]

        if profile:
            args.extend(["--profile", profile])
        elif self._config.default_profile:
            args.extend(["--profile", self._config.default_profile])

        result = self._execute_command(args)
        return result.returncode == 0

    def add_remote(self, name: str, url: str, verify_ssl: bool = True) -> bool:
        """Add Conan remote"""
        args = ["remote", "add", name, url]

        if not verify_ssl:
            args.append("--insecure")

        result = self._execute_command(args)
        return result.returncode == 0

    def remove_remote(self, name: str) -> bool:
        """Remove Conan remote"""
        result = self._execute_command(["remote", "remove", name])
        return result.returncode == 0

    def list_remotes(self) -> List[Dict[str, str]]:
        """List Conan remotes"""
        result = self._execute_command(["remote", "list"])

        if result.returncode != 0:
            return []

        remotes = []
        lines = result.stdout.strip().split('\n')

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    remotes.append({
                        "name": parts[0],
                        "url": parts[1]
                    })

        return remotes

    def authenticate(self, remote: str, username: str, password: str) -> bool:
        """Authenticate with remote"""
        result = self._execute_command(["user", username, "-p", password, "-r", remote])
        return result.returncode == 0

    def create(self, package: str, recipe_file: str) -> bool:
        """Create package from recipe"""
        result = self._execute_command(["create", recipe_file, package])
        return result.returncode == 0

    def export(self, package: str, recipe_file: str) -> bool:
        """Export package to cache"""
        result = self._execute_command(["export", recipe_file])
        return result.returncode == 0

    def _execute_command(self, args: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
        """Execute Conan command"""
        return subprocess.run(
            [self._config.executable] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )

    def _parse_profile(self, content: str, name: str) -> ConanProfile:
        """Parse Conan profile file"""
        import configparser

        config = configparser.ConfigParser()
        config.read_string(content)

        settings = {}
        if config.has_section('settings'):
            settings = dict(config.items('settings'))

        build_requires = []
        if config.has_section('build_requires'):
            build_requires = [line.strip() for line in config.get('build_requires', '').split('\n') if line.strip()]

        requires = []
        if config.has_section('requires'):
            requires = [line.strip() for line in config.get('requires', '').split('\n') if line.strip()]

        tools = {}
        if config.has_section('tools'):
            tools = dict(config.items('tools'))

        conf = {}
        if config.has_section('conf'):
            conf = dict(config.items('conf'))

        env = {}
        if config.has_section('env'):
            env = dict(config.items('env'))

        return ConanProfile(
            name=name,
            settings=settings,
            build_requires=build_requires,
            requires=requires,
            tools=tools,
            conf=conf,
            env=env
        )

class ConanProfileGenerator:
    """Generator for Conan profiles"""

    @staticmethod
    def generate_default_profile(compiler: str, build_type: str,
                             architecture: str = "x86_64") -> ConanProfile:
        """Generate default Conan profile"""
        settings = {
            "os": "Linux",
            "arch": architecture,
            "compiler": compiler,
            "build_type": build_type,
            "compiler.libcxx": "libstdc++11"
        }

        return ConanProfile(
            name="default",
            settings=settings,
            build_requires=[],
            requires=[],
            tools={},
            conf={},
            env={}
        )

    @staticmethod
    def generate_msvc_profile(architecture: str = "x64",
                          toolset: str = "v143") -> ConanProfile:
        """Generate MSVC Conan profile"""
        settings = {
            "os": "Windows",
            "arch": architecture,
            "compiler": "msvc",
            "build_type": "Release",
            "compiler.toolset": toolset,
            "compiler.runtime": "dynamic"
        }

        return ConanProfile(
            name="msvc",
            settings=settings,
            build_requires=[],
            requires=[],
            tools={},
            conf={},
            env={}
        )

    @staticmethod
    def generate_gcc_profile(version: str = "11",
                         architecture: str = "x86_64") -> ConanProfile:
        """Generate GCC Conan profile"""
        settings = {
            "os": "Linux",
            "arch": architecture,
            "compiler": "gcc",
            "compiler.version": version,
            "build_type": "Release",
            "compiler.libcxx": "libstdc++11"
        }

        return ConanProfile(
            name="gcc",
            settings=settings,
            build_requires=[],
            requires=[],
            tools={},
            conf={},
            env={}
        )

    @staticmethod
    def generate_clang_profile(version: str = "14",
                           architecture: str = "x86_64") -> ConanProfile:
        """Generate Clang Conan profile"""
        settings = {
            "os": "Linux",
            "arch": architecture,
            "compiler": "clang",
            "compiler.version": version,
            "build_type": "Release",
            "compiler.libcxx": "libc++"
        }

        return ConanProfile(
            name="clang",
            settings=settings,
            build_requires=[],
            requires=[],
            tools={},
            conf={},
            env={}
        )
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-012` - Package manager interface

### External Dependencies
- `subprocess` - Process execution
- `json` - JSON parsing
- `os` - Operating system interface
- `configparser` - Configuration file parsing
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-016: Conan Integration
- REQ-019: Priority-Based Package Manager Selection
- REQ-020: Package Security Verification
- REQ-021: Dependency Resolution & Caching

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Conan Detection
1. Check for conan executable in PATH
2. Execute conan --version
3. Parse version output
4. Validate minimum version

### Profile Management
1. Create profiles for different configurations
2. Store profiles in .conan2/profiles directory
3. Use profiles for consistent builds
4. Support profile inheritance

### Package Installation Flow
1. Resolve package dependencies
2. Download package recipes
3. Build packages if needed
4. Install to cache
5. Generate toolchain files

### Toolchain Integration
1. Generate CMake toolchain file
2. Generate compiler wrapper scripts
3. Set environment variables
4. Integrate with CMake

## Usage Example

```python
from omni_scripts.conan import (
    ConanManager,
    ConanConfig,
    ConanProfileGenerator,
    ConanBuildType
)

# Create Conan configuration
config = ConanConfig(
    executable="conan",
    config_dir=os.path.expanduser("~/.conan2"),
    cache_dir=os.path.expanduser("~/.conan2/data"),
    profiles_dir=os.path.expanduser("~/.conan2/profiles"),
    remotes=[],
    default_profile="default",
    default_build_type=ConanBuildType.RELEASE
)

# Create Conan manager
manager = ConanManager(config)

# Install package
if manager.install("fmt/10.0.0"):
    print("Package installed successfully")

# Create profile
profile = ConanProfileGenerator.generate_gcc_profile("11", "x86_64")
if manager.create_profile(profile):
    print("Profile created successfully")

# List profiles
profiles = manager.list_profiles()
print(f"Available profiles: {profiles}")
```
