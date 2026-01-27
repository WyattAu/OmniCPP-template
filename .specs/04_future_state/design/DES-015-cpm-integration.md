# DES-015: CPM Integration Design

## Overview
Defines CPM (CMake Package Manager) integration for managing C++ dependencies directly in CMake.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import subprocess
import os
import re

@dataclass
class CPMPackage:
    """CPM package information"""
    name: str
    version: str
    git_tag: Optional[str] = None
    git_commit: Optional[str] = None
    git_shallow: bool = False
    git_submodules: bool = False
    git_subdirectory: Optional[str] = None
    url: Optional[str] = None
    options: Dict[str, str] = None
    excludes: List[str] = None

@dataclass
class CPMConfig:
    """CPM configuration"""
    cache_dir: str
    source_dir: str
    download_only: bool = False
    git_shallow: bool = False
    git_submodules: bool = False
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None

class ICPMManager(ABC):
    """Interface for CPM package manager"""

    @abstractmethod
    def add_package(self, package: CPMPackage) -> bool:
        """Add CPM package to CMakeLists.txt"""
        pass

    @abstractmethod
    def remove_package(self, package_name: str) -> bool:
        """Remove CPM package from CMakeLists.txt"""
        pass

    @abstractmethod
    def list_packages(self) -> List[CPMPackage]:
        """List CPM packages in CMakeLists.txt"""
        pass

    @abstractmethod
    def update_packages(self) -> bool:
        """Update all CPM packages"""
        pass

    @abstractmethod
    def get_package_info(self, package_name: str) -> Optional[CPMPackage]:
        """Get package information"""
        pass

    @abstractmethod
    def generate_cmake_script(self, packages: List[CPMPackage]) -> str:
        """Generate CPM CMake script"""
        pass

    @abstractmethod
    def parse_cmake_lists(self, cmake_lists_path: str) -> List[CPMPackage]:
        """Parse CMakeLists.txt for CPM packages"""
        pass

class CPMManager(ICPMManager):
    """Implementation of CPM package manager"""

    def __init__(self, config: CPMConfig) -> None:
        """Initialize CPM manager"""
        self._config = config
        self._cache: Dict[str, Any] = {}

    def add_package(self, package: CPMPackage) -> bool:
        """Add CPM package to CMakeLists.txt"""
        cmake_lists_path = self._find_cmake_lists()

        if not cmake_lists_path:
            return False

        try:
            with open(cmake_lists_path, 'r') as f:
                content = f.read()

            # Check if CPM is already included
            if "CPM.cmake" not in content:
                # Add CPM include
                content = self._add_cpm_include(content)

            # Add package
            package_cmake = self._generate_package_cmake(package)
            content = content.replace("CPMAddPackage(", f"{package_cmake}\nCPMAddPackage(")

            with open(cmake_lists_path, 'w') as f:
                f.write(content)

            return True
        except IOError:
            return False

    def remove_package(self, package_name: str) -> bool:
        """Remove CPM package from CMakeLists.txt"""
        cmake_lists_path = self._find_cmake_lists()

        if not cmake_lists_path:
            return False

        try:
            with open(cmake_lists_path, 'r') as f:
                content = f.read()

            # Remove package CPM call
            pattern = rf'CPMAddPackage\([^)]*NAME\s+"{package_name}"[^)]*\)'
            content = re.sub(pattern, '', content)

            with open(cmake_lists_path, 'w') as f:
                f.write(content)

            return True
        except IOError:
            return False

    def list_packages(self) -> List[CPMPackage]:
        """List CPM packages in CMakeLists.txt"""
        cmake_lists_path = self._find_cmake_lists()

        if not cmake_lists_path:
            return []

        return self.parse_cmake_lists(cmake_lists_path)

    def update_packages(self) -> bool:
        """Update all CPM packages"""
        # CPM updates packages automatically on CMake configure
        # Just need to reconfigure
        cmake_lists_path = self._find_cmake_lists()

        if not cmake_lists_path:
            return False

        # Run CMake to update packages
        build_dir = os.path.dirname(cmake_lists_path)
        build_dir = os.path.join(build_dir, 'build')

        result = subprocess.run(
            ["cmake", "-S", os.path.dirname(cmake_lists_path), "-B", build_dir],
            capture_output=True,
            text=True,
            timeout=300
        )

        return result.returncode == 0

    def get_package_info(self, package_name: str) -> Optional[CPMPackage]:
        """Get package information"""
        packages = self.list_packages()

        for pkg in packages:
            if pkg.name == package_name:
                return pkg

        return None

    def generate_cmake_script(self, packages: List[CPMPackage]) -> str:
        """Generate CPM CMake script"""
        script_lines = []

        for pkg in packages:
            script_lines.append(self._generate_package_cmake(pkg))

        return '\n'.join(script_lines)

    def parse_cmake_lists(self, cmake_lists_path: str) -> List[CPMPackage]:
        """Parse CMakeLists.txt for CPM packages"""
        try:
            with open(cmake_lists_path, 'r') as f:
                content = f.read()
        except IOError:
            return []

        packages = []

        # Find all CPMAddPackage calls
        pattern = r'CPMAddPackage\(([^)]+)\)'
        matches = re.findall(pattern, content)

        for match in matches:
            pkg = self._parse_package_cmake(match)
            if pkg:
                packages.append(pkg)

        return packages

    def _find_cmake_lists(self) -> Optional[str]:
        """Find CMakeLists.txt file"""
        # Search in current directory and parent directories
        current_dir = os.getcwd()

        for _ in range(5):  # Search up to 5 levels
            cmake_lists = os.path.join(current_dir, 'CMakeLists.txt')
            if os.path.exists(cmake_lists):
                return cmake_lists

            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                break
            current_dir = parent

        return None

    def _add_cpm_include(self, content: str) -> str:
        """Add CPM include to CMakeLists.txt"""
        cpm_include = '''
# CPM integration
include(FetchContent)
FetchContent_Declare(
  cpm
  GIT_REPOSITORY https://github.com/cpm-cmake/CPM.cmake
  GIT_TAG        0.40.2
)

FetchContent_MakeAvailable(cpm)

include(CPM)
'''

        # Add after project() declaration
        project_pattern = r'(project\([^)]+\))'
        match = re.search(project_pattern, content)

        if match:
            insert_pos = match.end()
            return content[:insert_pos] + cpm_include + content[insert_pos:]
        else:
            return cpm_include + '\n' + content

    def _generate_package_cmake(self, package: CPMPackage) -> str:
        """Generate CPM package CMake code"""
        args = []

        if package.name:
            args.append(f'NAME "{package.name}"')

        if package.version:
            args.append(f'VERSION "{package.version}"')

        if package.git_tag:
            args.append(f'GIT_TAG "{package.git_tag}"')

        if package.git_commit:
            args.append(f'GIT_COMMIT "{package.git_commit}"')

        if package.git_shallow:
            args.append('GIT_SHALLOWS TRUE')

        if package.git_submodules:
            args.append('GIT_SUBMODULES TRUE')

        if package.git_subdirectory:
            args.append(f'GIT_SUBDIRECTORY "{package.git_subdirectory}"')

        if package.url:
            args.append(f'URL "{package.url}"')

        if package.options:
            for key, value in package.options.items():
                args.append(f'OPTIONS "{key}={value}"')

        if package.excludes:
            for exclude in package.excludes:
                args.append(f'EXCLUDE "{exclude}"')

        args_str = ' '.join(args)
        return f'CPMAddPackage({args_str})'

    def _parse_package_cmake(self, cmake_code: str) -> Optional[CPMPackage]:
        """Parse CPM package CMake code"""
        package = CPMPackage(name="", version="")

        # Parse NAME
        name_match = re.search(r'NAME\s+"([^"]+)"', cmake_code)
        if name_match:
            package.name = name_match.group(1)

        # Parse VERSION
        version_match = re.search(r'VERSION\s+"([^"]+)"', cmake_code)
        if version_match:
            package.version = version_match.group(1)

        # Parse GIT_TAG
        git_tag_match = re.search(r'GIT_TAG\s+"([^"]+)"', cmake_code)
        if git_tag_match:
            package.git_tag = git_tag_match.group(1)

        # Parse GIT_COMMIT
        git_commit_match = re.search(r'GIT_COMMIT\s+"([^"]+)"', cmake_code)
        if git_commit_match:
            package.git_commit = git_commit_match.group(1)

        # Parse GIT_SHALLOWS
        shallow_match = re.search(r'GIT_SHALLOWS\s+(TRUE|FALSE)', cmake_code)
        if shallow_match:
            package.git_shallow = shallow_match.group(1) == 'TRUE'

        # Parse GIT_SUBMODULES
        submodules_match = re.search(r'GIT_SUBMODULES\s+(TRUE|FALSE)', cmake_code)
        if submodules_match:
            package.git_submodules = submodules_match.group(1) == 'TRUE'

        # Parse GIT_SUBDIRECTORY
        subdir_match = re.search(r'GIT_SUBDIRECTORY\s+"([^"]+)"', cmake_code)
        if subdir_match:
            package.git_subdirectory = subdir_match.group(1)

        # Parse URL
        url_match = re.search(r'URL\s+"([^"]+)"', cmake_code)
        if url_match:
            package.url = url_match.group(1)

        # Parse OPTIONS
        options = {}
        options_matches = re.findall(r'OPTIONS\s+"([^"]+)"', cmake_code)
        for match in options_matches:
            if '=' in match:
                key, value = match.split('=', 1)
                options[key] = value
        if options:
            package.options = options

        # Parse EXCLUDE
        excludes = []
        exclude_matches = re.findall(r'EXCLUDE\s+"([^"]+)"', cmake_code)
        for match in exclude_matches:
            excludes.append(match)
        if excludes:
            package.excludes = excludes

        return package if package.name else None

class CPMPackageGenerator:
    """Generator for CPM packages"""

    @staticmethod
    def generate_github_package(owner: str, repo: str, version: str = "latest") -> CPMPackage:
        """Generate GitHub package"""
        return CPMPackage(
            name=f"{owner}/{repo}",
            version=version,
            url=f"https://github.com/{owner}/{repo}.git"
        )

    @staticmethod
    def generate_gitlab_package(owner: str, repo: str, version: str = "latest") -> CPMPackage:
        """Generate GitLab package"""
        return CPMPackage(
            name=f"{owner}/{repo}",
            version=version,
            url=f"https://gitlab.com/{owner}/{repo}.git"
        )

    @staticmethod
    def generate_git_package(url: str, version: str = "latest") -> CPMPackage:
        """Generate Git package"""
        return CPMPackage(
            name=url.split('/')[-1].replace('.git', ''),
            version=version,
            url=url
        )

    @staticmethod
    def generate_local_package(path: str) -> CPMPackage:
        """Generate local package"""
        return CPMPackage(
            name=os.path.basename(path),
            version="local",
            url=f"file://{os.path.abspath(path)}"
        )
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-012` - Package manager interface

### External Dependencies
- `subprocess` - Process execution
- `re` - Regular expressions
- `os` - Operating system interface
- `typing` - Type hints
- `dataclasses` - Data structures

## Related Requirements
- REQ-018: CPM CMake Integration
- REQ-019: Priority-Based Package Manager Selection
- REQ-020: Package Security Verification
- REQ-021: Dependency Resolution & Caching

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### CPM Detection
1. Check for CPM.cmake in CMakeLists.txt
2. Check for CPM cache directory
3. Validate CPM version
4. Ensure CMake FetchContent is available

### Package Management
1. Parse CPMAddPackage calls from CMakeLists.txt
2. Extract package information
3. Generate CMake code for new packages
4. Update CMakeLists.txt

### CMake Integration
1. Add CPM include to CMakeLists.txt
2. Use CPMAddPackage for dependencies
3. Configure CMake to download packages
4. Use CPM packages in project

### Caching Strategy
1. Download packages to cache directory
2. Reuse cached packages
3. Update packages on demand
4. Clean old cache entries

## Usage Example

```python
from omni_scripts.cpm import (
    CPMManager,
    CPMConfig,
    CPMPackage,
    CPMPackageGenerator
)

# Create CPM configuration
config = CPMConfig(
    cache_dir=os.path.expanduser("~/.cache/CPM"),
    source_dir=os.path.expanduser("~/.cache/CPM/source"),
    download_only=False,
    git_shallow=False,
    git_submodules=False
)

# Create CPM manager
manager = CPMManager(config)

# Add GitHub package
fmt_package = CPMPackageGenerator.generate_github_package("fmtlib", "fmt", "10.0.0")
if manager.add_package(fmt_package):
    print("Package added successfully")

# List packages
packages = manager.list_packages()
for pkg in packages:
    print(f"{pkg.name} v{pkg.version}")

# Update packages
if manager.update_packages():
    print("Packages updated successfully")
```
