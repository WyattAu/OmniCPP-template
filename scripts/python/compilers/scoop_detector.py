"""
Scoop Package Manager Detector

This module provides comprehensive detection of Scoop package manager
and compiler packages installed via Scoop (LLVM, MinGW, etc.).
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


class ScoopDetector:
    """Detector for Scoop package manager and compiler packages"""

    # Known compiler packages that can be installed via Scoop
    COMPILER_PACKAGES = [
        "llvm",
        "mingw",
        "gcc",
        "clang",
        "msys2",
        "cmake",
        "ninja",
        "make",
        "gcc-arm-none-eabi",
        "llvm-mingw"
    ]

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize Scoop detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._scoop_path: Optional[str] = None
        self._detected_packages: List[PackageInfo] = []

    def detect(self) -> List[PackageInfo]:
        """
        Detect Scoop installation and all compiler packages

        Returns:
            List of detected package information
        """
        self._logger.info("Starting Scoop package detection")
        self._detected_packages.clear()

        # Detect Scoop installation
        scoop_path = self.detect_scoop()
        if not scoop_path:
            self._logger.warning("Scoop not found, skipping package detection")
            return []

        self._scoop_path = scoop_path
        self._logger.info(f"Found Scoop at: {scoop_path}")

        # Detect packages installed via Scoop
        packages = self.detect_packages()
        self._detected_packages = packages

        self._logger.info(f"Detected {len(packages)} compiler packages via Scoop")
        return packages

    def detect_scoop(self) -> Optional[str]:
        """
        Detect Scoop installation (scoop.exe)

        Returns:
            Path to scoop.exe or None if not found
        """
        self._logger.debug("Detecting Scoop installation")

        # Check common Scoop installation paths
        scoop_paths = self._get_scoop_paths()

        for path in scoop_paths:
            self._logger.debug(f"Checking Scoop path: {path}")
            if os.path.exists(path):
                self._logger.info(f"Found Scoop at: {path}")
                return path

        # Try to find scoop.exe in PATH
        try:
            result = subprocess.run(
                ["where", "scoop"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                scoop_path = result.stdout.strip().split('\n')[0]
                if os.path.exists(scoop_path):
                    self._logger.info(f"Found Scoop in PATH at: {scoop_path}")
                    return scoop_path
        except subprocess.TimeoutExpired:
            self._logger.error("Scoop detection via 'where' timed out")
        except Exception as e:
            self._logger.error(f"Error detecting Scoop via 'where': {e}")

        self._logger.warning("Scoop not found")
        return None

    def detect_packages(self) -> List[PackageInfo]:
        """
        Detect packages installed via Scoop

        Returns:
            List of detected package information
        """
        self._logger.debug("Detecting packages installed via Scoop")

        if not self._scoop_path:
            self._logger.error("Scoop not detected, cannot detect packages")
            return []

        packages: List[PackageInfo] = []

        # Get list of all installed packages
        try:
            result = subprocess.run(
                [self._scoop_path, "list"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self._logger.error(f"Failed to list Scoop packages: {result.stderr}")
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
            self._logger.error("Scoop package list timed out")
        except Exception as e:
            self._logger.error(f"Error detecting Scoop packages: {e}")

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

        if not self._scoop_path:
            self._logger.error("Scoop not detected")
            return None

        try:
            # Get package information
            result = subprocess.run(
                [self._scoop_path, "info", package_name],
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

        # Check if Scoop is still installed
        if not self._scoop_path or not os.path.exists(self._scoop_path):
            warnings.append("Scoop package manager is not accessible")

        is_valid = len(errors) == 0

        self._logger.debug(f"Validation result: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}")
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _get_scoop_paths(self) -> List[str]:
        """
        Get list of possible Scoop installation paths

        Returns:
            List of scoop.exe paths
        """
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expandvars(r"%LOCALAPPDATA%"))

        return [
            os.path.join(user_profile, r"scoop\shims\scoop.exe"),
            os.path.join(local_app_data, r"scoop\shims\scoop.exe"),
            os.path.join(os.environ.get("SCOOP", ""), "shims", "scoop.exe"),
            os.path.join(os.environ.get("SCOOP_GLOBAL", r"C:\ProgramData\scoop"), "shims", "scoop.exe"),
        ]

    def _parse_package_list(self, output: str) -> List[str]:
        """
        Parse Scoop package list output

        Args:
            output: Output from 'scoop list' command

        Returns:
            List of package names
        """
        packages: List[str] = []

        # Scoop list output format:
        # package1 version1
        # package2 version2
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Skip header lines
            if line.startswith('Name') or line.startswith('-') or line.startswith('scoop'):
                continue

            # Extract package name (first word before space)
            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[0].lower()
                packages.append(package_name)

        return packages

    def _parse_package_info(self, package_name: str, output: str) -> Optional[PackageInfo]:
        """
        Parse Scoop package info output

        Args:
            package_name: Name of package
            output: Output from 'scoop info' command

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
            elif line.lower().startswith('description:'):
                # Description might contain package name
                pass
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
            package_manager=PackageManagerType.SCOOP,
            metadata={
                "detection_method": "scoop",
                "scoop_path": self._scoop_path or ""
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
        # Common Scoop package installation locations
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        scoop_root = os.path.join(user_profile, "scoop")
        scoop_global = os.environ.get("SCOOP_GLOBAL", r"C:\ProgramData\scoop")

        # Check user scoop apps directory
        for scoop_base in [scoop_root, scoop_global]:
            # Check package directory
            package_dir = os.path.join(scoop_base, "apps", package_name)
            if os.path.exists(package_dir):
                # Look for current version directory
                current_dir = os.path.join(package_dir, "current")
                if os.path.exists(current_dir):
                    # Look for main executable
                    for item in os.listdir(current_dir):
                        item_path = os.path.join(current_dir, item)
                        if os.path.isfile(item_path) and (item.endswith('.exe') or item.endswith('.sh')):
                            return item_path
                    # If no executable found, return current directory
                    return current_dir
                else:
                    # Return package directory
                    return package_dir

        # Try to find executable in shims
        shims_dir = os.path.join(scoop_root, "shims")
        if os.path.exists(shims_dir):
            shim_path = os.path.join(shims_dir, f"{package_name}.exe")
            if os.path.exists(shim_path):
                return shim_path

        # Try to find executable in PATH
        try:
            result = subprocess.run(
                ["where", package_name],
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
