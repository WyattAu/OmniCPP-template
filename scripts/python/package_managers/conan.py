"""
Conan package manager integration

This module provides integration with Conan package manager for C/C++ dependencies.
It supports Conan 2.x and provides methods for package installation, information retrieval,
and command execution.
"""

import json
import re
import shutil
import subprocess
from typing import Any, Dict, Optional

from ..core.exception_handler import DependencyError
from ..core.logger import Logger
from .base import ExecutionResult, PackageInfo, PackageManagerBase


class ConanPackageManager(PackageManagerBase):
    """Conan package manager integration.
    
    This class provides methods to interact with Conan package manager,
    including package installation, information retrieval, and command execution.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize Conan package manager.
        
        Args:
            config: Configuration dictionary containing Conan settings
        """
        super().__init__(config)
        self.logger: Optional[Logger] = None
        self._conan_path: Optional[str] = None
        self._version: Optional[str] = None
    
    def get_name(self) -> str:
        """Get package manager name.
        
        Returns:
            Package manager name
        """
        return "conan"
    
    def is_available(self) -> bool:
        """Check if Conan is available.
        
        Returns:
            True if Conan is installed and available, False otherwise
        """
        if self._conan_path is None:
            self._conan_path = self._find_conan_executable()
        return self._conan_path is not None
    
    def initialize(self) -> None:
        """Initialize Conan package manager.
        
        This method detects Conan installation, validates version,
        and sets up paths.
        
        Raises:
            DependencyError: If Conan is not available
        """
        if self._is_initialized:
            return
        
        # Initialize logger if available
        if "logger" in self.config:
            self.logger = self.config["logger"]
        
        # Find Conan executable
        self._conan_path = self._find_conan_executable()
        if self._conan_path is None:
            raise DependencyError(
                "Conan package manager not found. Please install Conan 2.x from "
                "https://docs.conan.io/2/installation.html"
            )
        
        # Get Conan version
        self._version = self._get_conan_version()
        if self.logger:
            self.logger.info(f"Conan {self._version} found at {self._conan_path}")
        
        # Set executable path
        self._set_executable_path(self._conan_path)
        self._mark_initialized()
    
    def install_package(self, package: str, version: Optional[str] = None) -> bool:
        """Install package with Conan.
        
        Args:
            package: Package name (e.g., "fmt/10.1.1")
            version: Package version (ignored if version is in package name)
            
        Returns:
            True if installation succeeded, False otherwise
        """
        if not self._is_initialized:
            self.initialize()
        
        # Construct package reference
        package_ref = package if "/" in package else f"{package}/{version}" if version else package
        
        if self.logger:
            self.logger.info(f"Installing Conan package: {package_ref}")
        
        try:
            result = self.execute_conan_command(f"install {package_ref} --requires")
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
            package: Package name or reference
            
        Returns:
            Package information or None if package not found
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            # Try to get package info using conan search
            result = self.execute_conan_command(f"search {package} --remote=conancenter")
            
            if not result.success:
                return None
            
            # Parse output to extract package info
            return self._parse_package_info(result.stdout, package)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting package info for {package}: {e}")
            return None
    
    def execute_conan_command(self, command: str) -> ExecutionResult:
        """Execute Conan command.
        
        Args:
            command: Conan command to execute (without 'conan' prefix)
            
        Returns:
            Execution result with exit code, stdout, and stderr
        """
        if not self._is_initialized:
            self.initialize()
        
        full_command = f"{self._conan_path} {command}"
        
        try:
            process = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
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
    
    def get_conan_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """Get Conan profile configuration.
        
        Args:
            profile_name: Profile name (e.g., "default", "gcc", "msvc")
            
        Returns:
            Profile configuration dictionary or None if not found
        """
        if not self._is_initialized:
            self.initialize()
        
        try:
            result = self.execute_conan_command(f"profile show {profile_name}")
            
            if not result.success:
                return None
            
            # Parse profile output
            return self._parse_profile(result.stdout)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting profile {profile_name}: {e}")
            return None
    
    def _find_conan_executable(self) -> Optional[str]:
        """Find Conan executable in system PATH.
        
        Returns:
            Path to Conan executable or None if not found
        """
        # Try 'conan' command
        conan_path = shutil.which("conan")
        if conan_path:
            return conan_path
        
        # Try 'conan.exe' on Windows
        if shutil.which("conan.exe"):
            return "conan.exe"
        
        return None
    
    def _get_conan_version(self) -> str:
        """Get Conan version.
        
        Returns:
            Conan version string
        """
        try:
            result = self.execute_conan_command("--version")
            if result.success:
                # Parse version from output (e.g., "Conan version 2.0.17")
                match = re.search(r"Conan version (\d+\.\d+\.\d+)", result.stdout)
                if match:
                    return match.group(1)
            return "unknown"
        except Exception:
            return "unknown"
    
    def _parse_package_info(self, output: str, package: str) -> Optional[PackageInfo]:
        """Parse package information from Conan search output.
        
        Args:
            output: Conan search output
            package: Package name
            
        Returns:
            Package information or None if parsing fails
        """
        try:
            # Try to parse JSON output if available
            if output.strip().startswith("{"):
                json.loads(output)
                # Extract package info from JSON structure
                # This is a simplified parser - actual structure may vary
                return PackageInfo(
                    name=package,
                    version="unknown",
                    description="Conan package"
                )
            
            # Parse text output
            lines = output.strip().split("\n")
            for line in lines:
                if package in line:
                    # Extract version from line
                    match = re.search(rf"{package}/(\d+\.\d+\.\d+)", line)
                    if match:
                        return PackageInfo(
                            name=package,
                            version=match.group(1),
                            description="Conan package"
                        )
            
            return None
        except Exception:
            return None
    
    def _parse_profile(self, output: str) -> Dict[str, Any]:
        """Parse Conan profile output.
        
        Args:
            output: Profile show output
            
        Returns:
            Profile configuration dictionary
        """
        profile: Dict[str, Any] = {}
        current_section: Optional[str] = None
        
        for line in output.split("\n"):
            line = line.strip()
            
            # Detect section headers
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                profile[current_section] = {}
            elif "=" in line and current_section:
                key, value = line.split("=", 1)
                profile[current_section][key.strip()] = value.strip()
        
        return profile
    
    def __repr__(self) -> str:
        """String representation of Conan package manager.
        
        Returns:
            String representation
        """
        return f"ConanPackageManager(version='{self._version}', available={self.is_available()})"
