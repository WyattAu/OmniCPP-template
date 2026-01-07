"""
CPM.cmake package manager integration

This module provides integration with CPM.cmake for C/C++ dependencies.
CPM.cmake is a CMake script that adds dependencies directly to CMake projects.
It downloads dependencies from Git repositories and integrates them with CMake.
"""

import os
import re
import shutil
import subprocess
import urllib.request
from typing import Any, Dict, Optional

from ..core.exception_handler import DependencyError
from ..core.logger import Logger
from .base import ExecutionResult, PackageInfo, PackageManagerBase


class CpmPackageManager(PackageManagerBase):
    """CPM.cmake package manager integration.
    
    This class provides methods to interact with CPM.cmake,
    including dependency management and CMake integration.
    """
    
    CPM_VERSION: str = "0.40.2"
    CPM_URL: str = f"https://github.com/cpm-cmake/CPM.cmake/releases/download/v{CPM_VERSION}/CPM.cmake"
    CPM_CACHE_DIR: str = ".cpm-cache"
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize CPM package manager.
        
        Args:
            config: Configuration dictionary containing CPM settings
        """
        super().__init__(config)
        self.logger: Optional[Logger] = None
        self._cpm_path: Optional[str] = None
        self._project_root: Optional[str] = None
        self._dependencies: Dict[str, Dict[str, str]] = {}
    
    def get_name(self) -> str:
        """Get package manager name.
        
        Returns:
            Package manager name
        """
        return "cpm"
    
    def is_available(self) -> bool:
        """Check if CPM.cmake is available.
        
        Returns:
            True if CPM.cmake is available, False otherwise
        """
        # CPM is always available as it can be downloaded
        return True
    
    def initialize(self) -> None:
        """Initialize CPM package manager.
        
        This method ensures CPM.cmake is available, either by finding
        an existing installation or downloading it.
        
        Raises:
            DependencyError: If CPM.cmake cannot be downloaded
        """
        if self._is_initialized:
            return
        
        # Initialize logger if available
        if "logger" in self.config:
            self.logger = self.config["logger"]
        
        # Get project root
        self._project_root = self.get_config("project_root", os.getcwd())
        
        # Find or download CPM.cmake
        self._cpm_path = self._find_or_download_cpm()
        if self._cpm_path is None:
            raise DependencyError(
                "Failed to download CPM.cmake. Please check your internet connection."
            )
        
        if self.logger:
            self.logger.info(f"CPM.cmake {self.CPM_VERSION} ready at {self._cpm_path}")
        
        # Set executable path (CPM is a CMake script, not executable)
        self._set_executable_path(self._cpm_path)
        self._mark_initialized()
    
    def install_package(self, package: str, version: Optional[str] = None) -> bool:
        """Install package with CPM.cmake.
        
        Note: CPM.cmake doesn't install packages directly. Instead,
        it adds dependencies to CMakeLists.txt. This method records
        the dependency for later CMake integration.
        
        Args:
            package: Package name or Git repository URL
            version: Package version (Git tag or commit)
            
        Returns:
            True if dependency was recorded, False otherwise
        """
        if not self._is_initialized:
            self.initialize()
        
        # Parse package reference
        git_repo, pkg_version = self._parse_package_reference(package, version)
        
        if self.logger:
            self.logger.info(f"Adding CPM dependency: {git_repo} @ {pkg_version}")
        
        # Record dependency
        self._dependencies[package] = {
            "git_repo": git_repo,
            "version": pkg_version
        }
        
        return True
    
    def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """Get package information.
        
        Note: CPM.cmake doesn't have a package registry. This method
        returns basic information based on the package name.
        
        Args:
            package: Package name or Git repository URL
            
        Returns:
            Package information or None if package is invalid
        """
        if not self._is_initialized:
            self.initialize()
        
        # Parse package reference
        git_repo, version = self._parse_package_reference(package)
        
        if not git_repo:
            return None
        
        # Extract package name from Git URL
        package_name = self._extract_package_name(git_repo)
        
        return PackageInfo(
            name=package_name,
            version=version or "latest",
            description=f"CPM.cmake dependency from {git_repo}",
            location=git_repo
        )
    
    def add_cpm_dependency(self, name: str, git_repo: str, version: Optional[str] = None) -> None:
        """Add CPM dependency.
        
        This method adds a dependency to the CPM dependency list.
        The dependency will be integrated into CMakeLists.txt.
        
        Args:
            name: Dependency name
            git_repo: Git repository URL
            version: Git tag or commit (latest if None)
        """
        if not self._is_initialized:
            self.initialize()
        
        if self.logger:
            self.logger.info(f"Adding CPM dependency: {name} from {git_repo}")
        
        # Record dependency
        self._dependencies[name] = {
            "git_repo": git_repo,
            "version": version or "latest"
        }
    
    def get_cmake_integration_code(self) -> str:
        """Generate CMake integration code for CPM.cmake.
        
        Returns:
            CMake code snippet to include CPM.cmake and add dependencies
        """
        if not self._is_initialized:
            self.initialize()
        
        # Generate CPM include statement
        code = f"# CPM.cmake integration\n"
        code += f"include(FETCHCONTENT_MAKEFILES_SERIAL)\n"
        code += f"include({self._cpm_path})\n\n"
        
        # Generate dependency statements
        for name, dep_info in self._dependencies.items():
            git_repo = dep_info["git_repo"]
            version = dep_info["version"]
            
            if version and version != "latest":
                code += f'CPMAddPackage("{name}"\n'
                code += f'    NAME {name}\n'
                code += f'    GITHUB_REPOSITORY {git_repo}\n'
                code += f'    VERSION {version}\n'
                code += f'    OPTIONS "FETCHCONTENT_UPDATES_DISCONNECTED {name}"\n'
                code += f')\n\n'
            else:
                code += f'CPMAddPackage("{name}"\n'
                code += f'    NAME {name}\n'
                code += f'    GITHUB_REPOSITORY {git_repo}\n'
                code += f'    OPTIONS "FETCHCONTENT_UPDATES_DISCONNECTED {name}"\n'
                code += f')\n\n'
        
        return code
    
    def get_dependencies(self) -> Dict[str, Dict[str, str]]:
        """Get all recorded CPM dependencies.
        
        Returns:
            Dictionary of dependencies with their Git repositories and versions
        """
        return self._dependencies.copy()
    
    def clear_cache(self) -> bool:
        """Clear CPM cache directory.
        
        Returns:
            True if cache was cleared, False otherwise
        """
        if not self._is_initialized:
            self.initialize()
        
        cache_dir = os.path.join(self._project_root, self.CPM_CACHE_DIR)
        
        if not os.path.exists(cache_dir):
            if self.logger:
                self.logger.warning(f"CPM cache directory not found: {cache_dir}")
            return False
        
        try:
            shutil.rmtree(cache_dir)
            if self.logger:
                self.logger.info(f"CPM cache cleared: {cache_dir}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to clear CPM cache: {e}")
            return False
    
    def _find_or_download_cpm(self) -> Optional[str]:
        """Find existing CPM.cmake or download it.
        
        Returns:
            Path to CPM.cmake or None if download fails
        """
        # Check for CPM in cmake directory
        cmake_dir = os.path.join(self._project_root, "cmake")
        cpm_path = os.path.join(cmake_dir, f"CPM_{self.CPM_VERSION}.cmake")
        
        if os.path.exists(cpm_path):
            return cpm_path
        
        # Check for CPM in project root
        cpm_path = os.path.join(self._project_root, "cmake", "CPM.cmake")
        if os.path.exists(cpm_path):
            return cpm_path
        
        # Download CPM.cmake
        return self._download_cpm()
    
    def _download_cpm(self) -> Optional[str]:
        """Download CPM.cmake from GitHub.
        
        Returns:
            Path to downloaded CPM.cmake or None if download fails
        """
        # Create cmake directory if it doesn't exist
        cmake_dir = os.path.join(self._project_root, "cmake")
        os.makedirs(cmake_dir, exist_ok=True)
        
        cpm_path = os.path.join(cmake_dir, f"CPM_{self.CPM_VERSION}.cmake")
        
        try:
            if self.logger:
                self.logger.info(f"Downloading CPM.cmake {self.CPM_VERSION}...")
            
            # Download CPM.cmake
            urllib.request.urlretrieve(self.CPM_URL, cpm_path)
            
            if self.logger:
                self.logger.info(f"CPM.cmake downloaded to {cpm_path}")
            
            return cpm_path
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to download CPM.cmake: {e}")
            return None
    
    def _parse_package_reference(self, package: str, version: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
        """Parse package reference into Git repository and version.
        
        Args:
            package: Package name or Git repository URL
            version: Package version
            
        Returns:
            Tuple of (git_repo, version)
        """
        # Check if package is a Git URL
        if package.startswith("http://") or package.startswith("https://") or package.startswith("git@"):
            return package, version
        
        # Check if package is in format "owner/repo"
        if "/" in package and not package.startswith("http"):
            return f"https://github.com/{package}", version
        
        # Assume it's a package name - try to find in common repositories
        common_repos = {
            "fmt": "https://github.com/fmtlib/fmt",
            "spdlog": "https://github.com/gabime/spdlog",
            "glm": "https://github.com/g-truc/glm",
            "stb": "https://github.com/nothings/stb",
            "nlohmann_json": "https://github.com/nlohmann/json",
            "catch2": "https://github.com/catchorg/Catch2",
            "doctest": "https://github.com/doctest/doctest",
            "eigen": "https://gitlab.com/libeigen/eigen",
        }
        
        git_repo = common_repos.get(package.lower())
        if git_repo:
            return git_repo, version
        
        return None, version
    
    def _extract_package_name(self, git_repo: str) -> str:
        """Extract package name from Git repository URL.
        
        Args:
            git_repo: Git repository URL
            
        Returns:
            Package name
        """
        # Remove trailing slash
        git_repo = git_repo.rstrip("/")
        
        # Extract name from URL
        if "/" in git_repo:
            return git_repo.split("/")[-1]
        
        return git_repo
    
    def __repr__(self) -> str:
        """String representation of CPM package manager.
        
        Returns:
            String representation
        """
        return f"CpmPackageManager(version='{self.CPM_VERSION}', dependencies={len(self._dependencies)})"
