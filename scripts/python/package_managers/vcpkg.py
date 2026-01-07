"""
vcpkg package manager integration

This module provides integration with vcpkg package manager for C/C++ dependencies.
It supports vcpkg and provides methods for package installation, information retrieval,
and command execution.
"""

import re
import shutil
import subprocess
from typing import Any, Dict, Optional

from ..core.exception_handler import DependencyError
from ..core.logger import Logger
from .base import ExecutionResult, PackageInfo, PackageManagerBase


class VcpkgPackageManager(PackageManagerBase):
    """vcpkg package manager integration.
    
    This class provides methods to interact with vcpkg package manager,
    including package installation, information retrieval, and command execution.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize vcpkg package manager.
        
        Args:
            config: Configuration dictionary containing vcpkg settings
        """
        super().__init__(config)
        self.logger: Optional[Logger] = None
        self._vcpkg_path: Optional[str] = None
        self._version: Optional[str] = None
        self._triplet: Optional[str] = None
    
    def get_name(self) -> str:
        """Get package manager name.
        
        Returns:
            Package manager name
        """
        return "vcpkg"
    
    def is_available(self) -> bool:
        """Check if vcpkg is available.
        
        Returns:
            True if vcpkg is installed and available, False otherwise
        """
        if self._vcpkg_path is None:
            self._vcpkg_path = self._find_vcpkg_executable()
        return self._vcpkg_path is not None
    
    def initialize(self) -> None:
        """Initialize vcpkg package manager.
        
        This method detects vcpkg installation, validates version,
        and sets up paths.
        
        Raises:
            DependencyError: If vcpkg is not available
        """
        if self._is_initialized:
            return
        
        # Initialize logger if available
        if "logger" in self.config:
            self.logger = self.config["logger"]
        
        # Find vcpkg executable
        self._vcpkg_path = self._find_vcpkg_executable()
        if self._vcpkg_path is None:
            raise DependencyError(
                "vcpkg package manager not found. Please install vcpkg from "
                "https://vcpkg.io/en/getting-started.html"
            )
        
        # Get vcpkg version
        self._version = self._get_vcpkg_version()
        if self.logger:
            self.logger.info(f"vcpkg {self._version} found at {self._vcpkg_path}")
        
        # Get default triplet
        self._triplet = self._get_default_triplet()
        if self.logger and self._triplet:
            self.logger.info(f"Default triplet: {self._triplet}")
        
        # Set executable path
        self._set_executable_path(self._vcpkg_path)
        self._mark_initialized()
    
    def install_package(self, package: str, version: Optional[str] = None) -> bool:
        """Install package with vcpkg.
        
        Args:
            package: Package name (e.g., "fmt", "openssl")
            version: Package version (ignored by vcpkg, uses latest)
            
        Returns:
            True if installation succeeded, False otherwise
        """
        if not self._is_initialized:
            self.initialize()
        
        # Construct package reference with triplet
        triplet = self.get_config("triplet", self._triplet)
        package_ref = f"{package}:{triplet}" if triplet else package
        
        if self.logger:
            self.logger.info(f"Installing vcpkg package: {package_ref}")
        
        try:
            result = self.execute_vcpkg_command(f"install {package_ref}")
            if result.success:
                if self.logger:
                    self.logger.info(f"Successfully installed {package_ref}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"Failed to install {package_ref}: {result.stderr}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error installing {package_ref}: {e}")
            return False
    
    def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """Get package information.
        
        Args:
            package: Package name
            
        Returns:
            Package information or None if package not found
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            # Try to get package info using vcpkg search
            result = self.execute_vcpkg_command(f"search {package}")
            
            if not result.success:
                return None
            
            # Parse output to extract package info
            return self._parse_package_info(result.stdout, package)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting package info for {package}: {e}")
            return None
    
    def execute_vcpkg_command(self, command: str) -> ExecutionResult:
        """Execute vcpkg command.
        
        Args:
            command: vcpkg command to execute (without 'vcpkg' prefix)
            
        Returns:
            Execution result with exit code, stdout, and stderr
        """
        if not self._is_initialized:
            self.initialize()
        
        full_command = f"{self._vcpkg_path} {command}"
        
        try:
            process = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for builds
            )
            
            return ExecutionResult(
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                success=process.returncode == 0
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                exit_code=-1,
                stdout="",
                stderr="Command timed out",
                success=False
            )
        except Exception as e:
            return ExecutionResult(
                exit_code=-1,
                stdout="",
                stderr=str(e),
                success=False
            )
    
    def get_vcpkg_triplet(self) -> Optional[str]:
        """Get current vcpkg triplet.
        
        Returns:
            Triplet string or None if not set
        """
        return self._triplet
    
    def list_installed_packages(self) -> list[str]:
        """List all installed packages.
        
        Returns:
            List of installed package names
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            result = self.execute_vcpkg_command("list")
            
            if not result.success:
                return []
            
            # Parse output to extract package names
            return self._parse_installed_packages(result.stdout)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error listing installed packages: {e}")
            return []
    
    def _find_vcpkg_executable(self) -> Optional[str]:
        """Find vcpkg executable in system PATH.
        
        Returns:
            Path to vcpkg executable or None if not found
        """
        # Try 'vcpkg' command
        vcpkg_path = shutil.which("vcpkg")
        if vcpkg_path:
            return vcpkg_path
        
        # Try 'vcpkg.exe' on Windows
        if shutil.which("vcpkg.exe"):
            return "vcpkg.exe"
        
        # Try common installation paths
        common_paths = [
            "C:/vcpkg/vcpkg.exe",
            "C:/tools/vcpkg/vcpkg.exe",
            "/usr/local/bin/vcpkg",
            "/opt/vcpkg/vcpkg"
        ]
        
        for path in common_paths:
            if shutil.which(path):
                return path
        
        return None
    
    def _get_vcpkg_version(self) -> str:
        """Get vcpkg version.
        
        Returns:
            vcpkg version string
        """
        try:
            result = self.execute_vcpkg_command("version")
            if result.success:
                # Parse version from output (e.g., "vcpkg package management program version 2024-01-10-hash...")
                match = re.search(r"version (\d{4}-\d{2}-\d{2})", result.stdout)
                if match:
                    return match.group(1)
            return "unknown"
        except Exception:
            return "unknown"
    
    def _get_default_triplet(self) -> Optional[str]:
        """Get default vcpkg triplet for current platform.
        
        Returns:
            Default triplet string or None if not detected
        """
        import platform
        system = platform.system()
        machine = platform.machine()
        
        if system == "Windows":
            if machine == "AMD64":
                return "x64-windows"
            elif machine == "ARM64":
                return "arm64-windows"
        elif system == "Linux":
            if machine == "x86_64":
                return "x64-linux"
            elif machine == "aarch64":
                return "arm64-linux"
        elif system == "Darwin":
            if machine == "x86_64":
                return "x64-osx"
            elif machine == "arm64":
                return "arm64-osx"
        
        return None
    
    def _parse_package_info(self, output: str, package: str) -> Optional[PackageInfo]:
        """Parse package information from vcpkg search output.
        
        Args:
            output: vcpkg search output
            package: Package name
            
        Returns:
            Package information or None if parsing fails
        """
        try:
            # Parse text output
            lines = output.strip().split("\n")
            for line in lines:
                if package.lower() in line.lower():
                    # Extract package name and description
                    parts = line.split(maxsplit=1)
                    if parts:
                        name = parts[0].strip()
                        description = parts[1].strip() if len(parts) > 1 else "vcpkg package"
                        return PackageInfo(
                            name=name,
                            version="latest",
                            description=description
                        )
            
            return None
        except Exception:
            return None
    
    def _parse_installed_packages(self, output: str) -> list[str]:
        """Parse installed packages from vcpkg list output.
        
        Args:
            output: vcpkg list output
            
        Returns:
            List of installed package names
        """
        packages: list[str] = []
        
        for line in output.strip().split("\n"):
            line = line.strip()
            if line and not line.startswith(":"):
                # Extract package name (before colon)
                if ":" in line:
                    package_name = line.split(":")[0].strip()
                    if package_name and package_name not in packages:
                        packages.append(package_name)
        
        return packages
    
    def __repr__(self) -> str:
        """String representation of vcpkg package manager.
        
        Returns:
            String representation
        """
        return f"VcpkgPackageManager(version='{self._version}', triplet='{self._triplet}', available={self.is_available()})"
