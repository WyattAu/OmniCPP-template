"""
winget Package Manager Detector

This module provides comprehensive detection of winget package manager
and compiler packages installed via winget (LLVM, MinGW, etc.).
"""

import logging
import os
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class PackageManagerType(Enum):
    """Package manager type enumeration"""
    CHOCOLATEY = "chocolatey"
    SCOOP = "scoop"
    WINGET = "winget"


@dataclass
class PackageInfo:
    """Package information"""
    name: str
    version: str
    path: str
    package_manager: PackageManagerType
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "path": self.path,
            "package_manager": self.package_manager.value,
            "metadata": self.metadata
        }

    def is_valid(self) -> bool:
        """Check if package is valid"""
        return os.path.exists(self.path)


@dataclass
class ValidationResult:
    """Package validation result"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class WingetDetector:
    """Detector for winget package manager and compiler packages"""

    # Known compiler packages that can be installed via winget
    COMPILER_PACKAGES = [
        "LLVM.LLVM",
        "LLVM.Clang",
        "GNU.Mingw",
        "GCC.GCC",
        "MSYS2.MSYS2",
        "Kitware.CMake",
        "Ninja-build.Ninja",
        "GnuWin32.Make"
    ]

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize winget detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._winget_path: Optional[str] = None
        self._detected_packages: List[PackageInfo] = []

    def detect(self) -> List[PackageInfo]:
        """
        Detect winget installation and all compiler packages

        Returns:
            List of detected package information
        """
        self._logger.info("Starting winget package detection")
        self._detected_packages.clear()

        # Detect winget installation
        winget_path = self.detect_winget()
        if not winget_path:
            self._logger.warning("winget not found, skipping package detection")
            return []

        self._winget_path = winget_path
        self._logger.info(f"Found winget at: {winget_path}")

        # Detect packages installed via winget
        packages = self.detect_packages()
        self._detected_packages = packages

        self._logger.info(f"Detected {len(packages)} compiler packages via winget")
        return packages

    def detect_winget(self) -> Optional[str]:
        """
        Detect winget installation (winget.exe)

        Returns:
            Path to winget.exe or None if not found
        """
        self._logger.debug("Detecting winget installation")

        # Check common winget installation paths
        winget_paths = self._get_winget_paths()

        for path in winget_paths:
            self._logger.debug(f"Checking winget path: {path}")
            if os.path.exists(path):
                self._logger.info(f"Found winget at: {path}")
                return path

        # Try to find winget.exe in PATH
        try:
            result = subprocess.run(
                ["where", "winget"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                winget_path = result.stdout.strip().split('\n')[0]
                if os.path.exists(winget_path):
                    self._logger.info(f"Found winget in PATH at: {winget_path}")
                    return winget_path
        except subprocess.TimeoutExpired:
            self._logger.error("winget detection via 'where' timed out")
        except Exception as e:
            self._logger.error(f"Error detecting winget via 'where': {e}")

        self._logger.warning("winget not found")
        return None

    def detect_packages(self) -> List[PackageInfo]:
        """
        Detect packages installed via winget

        Returns:
            List of detected package information
        """
        self._logger.debug("Detecting packages installed via winget")

        if not self._winget_path:
            self._logger.error("winget not detected, cannot detect packages")
            return []

        packages: List[PackageInfo] = []

        # Get list of all installed packages
        try:
            result = subprocess.run(
                [self._winget_path, "list"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self._logger.error(f"Failed to list winget packages: {result.stderr}")
                return []

            # Parse package list
            installed_packages = self._parse_package_list(result.stdout)

            # Filter for compiler packages
            for package_name in self.COMPILER_PACKAGES:
                if package_name in installed_packages:
                    package_info = self.get_package_info(package_name)
                    if package_info:
                        packages.append(package_info)
                        self._logger.debug(f"Found package: {package_name}")

        except subprocess.TimeoutExpired:
            self._logger.error("winget package list timed out")
        except Exception as e:
            self._logger.error(f"Error detecting winget packages: {e}")

        return packages

    def get_package_info(self, package_name: str) -> Optional[PackageInfo]:
        """
        Get detailed information about a specific package

        Args:
            package_name: Name of package

        Returns:
            Package information or None if not found
        """
        self._logger.debug(f"Getting package info for: {package_name}")

        if not self._winget_path:
            self._logger.error("winget not detected")
            return None

        try:
            # Get package information
            result = subprocess.run(
                [self._winget_path, "show", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self._logger.warning(f"Package {package_name} not found: {result.stderr}")
                return None

            # Parse package information
            package_info = self._parse_package_info(package_name, result.stdout)
            return package_info

        except subprocess.TimeoutExpired:
            self._logger.error(f"Package info for {package_name} timed out")
        except Exception as e:
            self._logger.error(f"Error getting package info for {package_name}: {e}")

        return None

    def validate_package(self, package_info: PackageInfo) -> ValidationResult:
        """
        Validate a package installation

        Args:
            package_info: Package information to validate

        Returns:
            Validation result
        """
        self._logger.debug(f"Validating package: {package_info.name}")

        errors: List[str] = []
        warnings: List[str] = []

        # Check if package path exists
        if not os.path.exists(package_info.path):
            errors.append(f"Package path not found: {package_info.path}")

        # Check if package is accessible
        if os.path.exists(package_info.path):
            try:
                # Try to access path
                if os.path.isfile(package_info.path):
                    # Check if file is executable
                    if not package_info.path.endswith('.exe') and not package_info.path.endswith('.sh'):
                        warnings.append(f"Package file is not an executable: {package_info.path}")
                elif os.path.isdir(package_info.path):
                    # Check if directory contains executables
                    has_executables = False
                    for item in os.listdir(package_info.path):
                        item_path = os.path.join(package_info.path, item)
                        if os.path.isfile(item_path) and (item_path.endswith('.exe') or item_path.endswith('.sh')):
                            has_executables = True
                            break

                    if not has_executables:
                        warnings.append(f"Package directory contains no executables: {package_info.path}")
            except PermissionError:
                errors.append(f"Permission denied accessing package path: {package_info.path}")
            except Exception as e:
                errors.append(f"Error accessing package path: {e}")

        # Check if winget is still installed
        if not self._winget_path or not os.path.exists(self._winget_path):
            warnings.append("winget package manager is not accessible")

        is_valid = len(errors) == 0

        self._logger.debug(f"Validation result: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}")
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _get_winget_paths(self) -> List[str]:
        """
        Get list of possible winget installation paths

        Returns:
            List of winget.exe paths
        """
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expandvars(r"%LOCALAPPDATA%"))
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        return [
            os.path.join(local_app_data, r"Microsoft\WindowsApps\winget.exe"),
            os.path.join(local_app_data, r"Microsoft\WindowsApps\WindowsPackageManager\winget.exe"),
            os.path.join(program_files, r"WindowsApps\Microsoft.DesktopAppInstaller_*\winget.exe"),
            os.path.join(program_files_x86, r"WindowsApps\Microsoft.DesktopAppInstaller_*\winget.exe"),
        ]

    def _parse_package_list(self, output: str) -> List[str]:
        """
        Parse winget package list output

        Args:
            output: Output from 'winget list' command

        Returns:
            List of package names
        """
        packages: List[str] = []

        # winget list output format:
        # Name           Id              Version        Available Source
        # ----------------------------------------------------------------
        # LLVM           LLVM.LLVM        17.0.6         18.1.0    winget
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Skip header lines
            if line.startswith('Name') or line.startswith('-') or line.startswith('Id'):
                continue

            # Extract package ID (second column)
            parts = line.split()
            if len(parts) >= 2:
                package_id = parts[1]
                packages.append(package_id)

        return packages

    def _parse_package_info(self, package_name: str, output: str) -> Optional[PackageInfo]:
        """
        Parse winget package info output

        Args:
            package_name: Name of package
            output: Output from 'winget show' command

        Returns:
            Package information or None if parsing fails
        """
        # Parse package information from output
        version = "unknown"
        path = ""

        for line in output.split('\n'):
            line = line.strip()

            if line.lower().startswith('version:'):
                version = line.split(':', 1)[1].strip()
            elif line.lower().startswith('install location:'):
                path = line.split(':', 1)[1].strip()

        # If path not found, try to find it in common locations
        if not path:
            path = self._find_package_path(package_name)

        if not path:
            self._logger.warning(f"Could not determine path for package: {package_name}")
            return None

        package_info = PackageInfo(
            name=package_name,
            version=version,
            path=path,
            package_manager=PackageManagerType.WINGET,
            metadata={
                "detection_method": "winget",
                "winget_path": self._winget_path or ""
            }
        )

        return package_info

    def _find_package_path(self, package_name: str) -> Optional[str]:
        """
        Find installation path for a package

        Args:
            package_name: Name of package

        Returns:
            Package installation path or None if not found
        """
        # Common winget package installation locations
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expandvars(r"%LOCALAPPDATA%"))
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        # Map package names to common installation directories
        package_dirs: Dict[str, List[str]] = {
            "LLVM.LLVM": [
                os.path.join(program_files, "LLVM"),
                os.path.join(local_app_data, "Programs", "LLVM"),
            ],
            "LLVM.Clang": [
                os.path.join(program_files, "LLVM"),
                os.path.join(local_app_data, "Programs", "LLVM"),
            ],
            "GNU.Mingw": [
                os.path.join(program_files, "mingw64"),
                os.path.join(program_files_x86, "mingw32"),
                os.path.join(local_app_data, "Programs", "mingw64"),
            ],
            "GCC.GCC": [
                os.path.join(program_files, "gcc"),
                os.path.join(local_app_data, "Programs", "gcc"),
            ],
            "MSYS2.MSYS2": [
                os.path.join(program_files, "msys64"),
                os.path.join(local_app_data, "Programs", "msys64"),
            ],
            "Kitware.CMake": [
                os.path.join(program_files, "CMake"),
                os.path.join(program_files_x86, "CMake"),
                os.path.join(local_app_data, "Programs", "CMake"),
            ],
            "Ninja-build.Ninja": [
                os.path.join(program_files, "Ninja"),
                os.path.join(local_app_data, "Programs", "Ninja"),
            ],
            "GnuWin32.Make": [
                os.path.join(program_files, "GnuWin32"),
                os.path.join(local_app_data, "Programs", "GnuWin32"),
            ],
        }

        # Check package directories
        for dir_path in package_dirs.get(package_name, []):
            if os.path.exists(dir_path):
                # Look for main executable
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path) and (item.endswith('.exe') or item.endswith('.sh')):
                        return item_path
                # If no executable found, return directory
                return dir_path

        # Try to find executable in PATH
        try:
            # Map package ID to executable name
            executable_map: Dict[str, str] = {
                "LLVM.LLVM": "clang",
                "LLVM.Clang": "clang",
                "GNU.Mingw": "gcc",
                "GCC.GCC": "gcc",
                "MSYS2.MSYS2": "bash",
                "Kitware.CMake": "cmake",
                "Ninja-build.Ninja": "ninja",
                "GnuWin32.Make": "make",
            }

            executable_name = executable_map.get(package_name, package_name.split('.')[-1].lower())
            result = subprocess.run(
                ["where", executable_name],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                executable_path = result.stdout.strip().split('\n')[0]
                if os.path.exists(executable_path):
                    return executable_path
        except Exception:
            pass

        return None
