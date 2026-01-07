"""
MinGW-GCC Compiler Detector

This module provides comprehensive detection of MinGW GCC compiler installations,
including MSYS2 environments, standalone installations, TDM-GCC, and package
manager installations.
"""

import logging
import os
import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class CompilerType(Enum):
    """Compiler type enumeration"""
    MSVC = "msvc"
    MSVC_CLANG = "msvc_clang"
    MINGW_GCC = "mingw_gcc"
    MINGW_CLANG = "mingw_clang"
    GCC = "gcc"
    CLANG = "clang"


class Architecture(Enum):
    """Architecture enumeration"""
    X64 = "x64"
    X86 = "x86"
    ARM = "arm"
    ARM64 = "arm64"


@dataclass
class VersionInfo:
    """Compiler version information"""
    major: int
    minor: int
    patch: int
    build: Optional[str] = None
    full_version: str = ""

    def __str__(self) -> str:
        if self.build:
            return f"{self.major}.{self.minor}.{self.patch}.{self.build}"
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: 'VersionInfo') -> bool:
        """Compare versions"""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        return False


@dataclass
class CapabilityInfo:
    """Compiler capability information"""
    cpp23: bool = False
    cpp20: bool = False
    cpp17: bool = False
    cpp14: bool = False
    modules: bool = False
    coroutines: bool = False
    concepts: bool = False
    ranges: bool = False
    std_format: bool = False
    msvc_compatibility: bool = False
    mingw_compatibility: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {
            "cpp23": self.cpp23,
            "cpp20": self.cpp20,
            "cpp17": self.cpp17,
            "cpp14": self.cpp14,
            "modules": self.modules,
            "coroutines": self.coroutines,
            "concepts": self.concepts,
            "ranges": self.ranges,
            "std_format": self.std_format,
            "msvc_compatibility": self.msvc_compatibility,
            "mingw_compatibility": self.mingw_compatibility
        }

    def supports_cpp_standard(self, standard: str) -> bool:
        """Check if compiler supports C++ standard"""
        return getattr(self, standard.lower(), False)


@dataclass
class EnvironmentInfo:
    """Compiler environment information"""
    path: str
    include_paths: List[str] = field(default_factory=list)
    library_paths: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, any]:
        return {
            "path": self.path,
            "include_paths": self.include_paths,
            "library_paths": self.library_paths,
            "environment_variables": self.environment_variables
        }


@dataclass
class CompilerInfo:
    """Compiler information"""
    compiler_type: CompilerType
    version: VersionInfo
    path: str
    architecture: Architecture
    capabilities: CapabilityInfo
    environment: EnvironmentInfo
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, any]:
        return {
            "compiler_type": self.compiler_type.value,
            "version": str(self.version),
            "path": self.path,
            "architecture": self.architecture.value,
            "capabilities": self.capabilities.to_dict(),
            "environment": self.environment.to_dict(),
            "metadata": self.metadata
        }

    def is_valid(self) -> bool:
        """Check if compiler is valid"""
        return os.path.exists(self.path)


@dataclass
class ValidationResult:
    """Compiler validation result"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class ICompilerDetector(ABC):
    """Interface for compiler detectors"""

    @abstractmethod
    def detect(self) -> List[CompilerInfo]:
        """
        Detect all compilers of this type

        Returns:
            List of detected compiler information
        """
        pass

    @abstractmethod
    def detect_version(self, compiler_path: str) -> Optional[VersionInfo]:
        """
        Detect compiler version

        Args:
            compiler_path: Path to compiler executable

        Returns:
            Version information or None if detection fails
        """
        pass

    @abstractmethod
    def detect_capabilities(self, compiler_path: str) -> CapabilityInfo:
        """
        Detect compiler capabilities

        Args:
            compiler_path: Path to compiler executable

        Returns:
            Capability information
        """
        pass

    @abstractmethod
    def validate(self, compiler_info: CompilerInfo) -> ValidationResult:
        """
        Validate compiler installation

        Args:
            compiler_info: Compiler information to validate

        Returns:
            Validation result
        """
        pass


class MinGWDetector(ICompilerDetector):
    """Detector for MinGW-GCC compiler installations"""

    # MSYS2 environment configurations
    MSYS2_ENVIRONMENTS = {
        "UCRT64": {
            "bin_path": "ucrt64/bin",
            "msystem": "UCRT64",
            "mingw_prefix": "/ucrt64",
            "mingw_chost": "x86_64-w64-mingw32",
            "architecture": Architecture.X64,
            "recommended": True
        },
        "MINGW64": {
            "bin_path": "mingw64/bin",
            "msystem": "MINGW64",
            "mingw_prefix": "/mingw64",
            "mingw_chost": "x86_64-w64-mingw32",
            "architecture": Architecture.X64,
            "recommended": False
        },
        "MINGW32": {
            "bin_path": "mingw32/bin",
            "msystem": "MINGW32",
            "mingw_prefix": "/mingw32",
            "mingw_chost": "i686-w64-mingw32",
            "architecture": Architecture.X86,
            "recommended": False
        },
        "MSYS": {
            "bin_path": "usr/bin",
            "msystem": "MSYS",
            "mingw_prefix": "/usr",
            "mingw_chost": "x86_64-pc-msys",
            "architecture": Architecture.X64,
            "recommended": False
        },
        "CLANG64": {
            "bin_path": "clang64/bin",
            "msystem": "CLANG64",
            "mingw_prefix": "/clang64",
            "mingw_chost": "x86_64-w64-mingw32",
            "architecture": Architecture.X64,
            "recommended": False
        }
    }

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize MinGW-GCC detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._msys2_paths: List[str] = self._get_msys2_paths()
        self._standalone_paths: List[str] = self._get_standalone_paths()
        self._tdm_gcc_paths: List[str] = self._get_tdm_gcc_paths()
        self._package_manager_paths: Dict[str, List[str]] = self._get_package_manager_paths()
        self._detected_compilers: List[CompilerInfo] = []

    def detect(self) -> List[CompilerInfo]:
        """
        Detect all MinGW-GCC compiler installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Starting MinGW-GCC compiler detection")
        self._detected_compilers.clear()

        # Try detection methods in order of preference
        compilers: List[CompilerInfo] = []

        # Detect MSYS2 environments
        msys2_compilers = self._detect_via_msys2()
        compilers.extend(msys2_compilers)
        self._logger.info(f"Found {len(msys2_compilers)} MSYS2 installations")

        # Detect standalone MinGW-w64 installations
        standalone_compilers = self._detect_standalone()
        compilers.extend(standalone_compilers)
        self._logger.info(f"Found {len(standalone_compilers)} standalone MinGW installations")

        # Detect TDM-GCC installations
        tdm_compilers = self._detect_tdm_gcc()
        compilers.extend(tdm_compilers)
        self._logger.info(f"Found {len(tdm_compilers)} TDM-GCC installations")

        # Detect MinGW via package managers
        package_compilers = self._detect_via_package_managers()
        compilers.extend(package_compilers)
        self._logger.info(f"Found {len(package_compilers)} package manager MinGW installations")

        # Sort by version (latest first)
        compilers.sort(key=lambda c: (c.version.major, c.version.minor, c.version.patch), reverse=True)

        # Mark recommended installation (first one)
        if compilers:
            compilers[0].metadata["recommended"] = "true"

        self._detected_compilers = compilers
        self._logger.info(f"Detected {len(compilers)} MinGW-GCC compiler installations")

        return compilers

    def detect_version(self, compiler_path: str) -> Optional[VersionInfo]:
        """
        Detect GCC compiler version

        Args:
            compiler_path: Path to g++.exe

        Returns:
            Version information or None if detection fails
        """
        self._logger.debug(f"Detecting version for {compiler_path}")

        if not os.path.exists(compiler_path):
            self._logger.error(f"Compiler executable not found: {compiler_path}")
            return None

        try:
            result = subprocess.run(
                [compiler_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                self._logger.error(f"Failed to execute g++.exe: {result.stderr}")
                return None

            # Parse version from output
            # Example: "g++.exe (Rev2, Built by MSYS2 project) 13.2.0"
            # Example: "g++.exe (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 12.2.0"
            for line in result.stdout.split('\n'):
                if "g++" in line or "gcc" in line or "g++.exe" in line:
                    # Look for version pattern: major.minor.patch
                    match = re.search(r"(\d+)\.(\d+)\.(\d+)", line)
                    if match:
                        major = int(match.group(1))
                        minor = int(match.group(2))
                        patch = int(match.group(3))
                        build = None

                        # Try to extract build number if present
                        build_match = re.search(r"(\d+)\.(\d+)\.(\d+)\.(\d+)", line)
                        if build_match:
                            build = build_match.group(4)

                        version_str = f"{major}.{minor}.{patch}"
                        if build:
                            version_str += f".{build}"

                        version_info = VersionInfo(
                            major=major,
                            minor=minor,
                            patch=patch,
                            build=build,
                            full_version=version_str
                        )
                        self._logger.debug(f"Detected version: {version_info}")
                        return version_info

        except subprocess.TimeoutExpired:
            self._logger.error("g++.exe version detection timed out")
        except Exception as e:
            self._logger.error(f"Error detecting g++.exe version: {e}")

        return None

    def detect_capabilities(self, compiler_path: str) -> CapabilityInfo:
        """
        Detect GCC compiler capabilities

        Args:
            compiler_path: Path to g++.exe

        Returns:
            Capability information
        """
        self._logger.debug(f"Detecting capabilities for {compiler_path}")

        capabilities = CapabilityInfo()

        # GCC 13+ supports C++23
        # GCC 11+ supports C++20
        # GCC 8+ supports C++17
        # GCC 6+ supports C++14

        version = self.detect_version(compiler_path)
        if version:
            if version.major >= 13:
                capabilities.cpp23 = True
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 11:
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 8:
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 6:
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True

        capabilities.mingw_compatibility = True

        self._logger.debug(f"Detected capabilities: {capabilities.to_dict()}")
        return capabilities

    def validate(self, compiler_info: CompilerInfo) -> ValidationResult:
        """
        Validate MinGW-GCC compiler installation

        Args:
            compiler_info: Compiler information to validate

        Returns:
            Validation result
        """
        self._logger.debug(f"Validating compiler: {compiler_info.path}")

        errors: List[str] = []
        warnings: List[str] = []

        # Check if compiler executable exists
        if not os.path.exists(compiler_info.path):
            errors.append(f"Compiler executable not found: {compiler_info.path}")

        # Check if compiler is executable
        if os.path.exists(compiler_info.path):
            try:
                result = subprocess.run(
                    [compiler_info.path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    errors.append(f"Compiler executable is not functional: {result.stderr}")
            except Exception as e:
                errors.append(f"Failed to execute compiler: {e}")

        # Check if required environment variables are set
        env = compiler_info.metadata.get("environment", "")
        if env and "MSYSTEM" not in compiler_info.environment.environment_variables:
            warnings.append("MSYSTEM environment variable not set")

        is_valid = len(errors) == 0

        self._logger.debug(f"Validation result: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}")
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _detect_via_msys2(self) -> List[CompilerInfo]:
        """
        Detect MSYS2 MinGW-GCC installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting MSYS2 installations")

        compilers: List[CompilerInfo] = []

        for msys2_path in self._msys2_paths:
            self._logger.debug(f"Checking MSYS2 path: {msys2_path}")

            if not os.path.exists(msys2_path):
                continue

            # Check each MSYS2 environment
            for env_name, env_config in self.MSYS2_ENVIRONMENTS.items():
                gpp_path = os.path.join(msys2_path, env_config["bin_path"], "g++.exe")

                if os.path.exists(gpp_path):
                    version = self.detect_version(gpp_path)
                    capabilities = self.detect_capabilities(gpp_path)

                    # Build environment variables
                    env_vars = {
                        "MSYSTEM": env_config["msystem"],
                        "MINGW_PREFIX": env_config["mingw_prefix"],
                        "MINGW_CHOST": env_config["mingw_chost"]
                    }

                    # Build include and library paths
                    include_paths = [
                        os.path.join(msys2_path, env_config["bin_path"].replace("/bin", "/include")),
                        os.path.join(msys2_path, "usr/include")
                    ]

                    library_paths = [
                        os.path.join(msys2_path, env_config["bin_path"].replace("/bin", "/lib")),
                        os.path.join(msys2_path, "usr/lib")
                    ]

                    compiler = CompilerInfo(
                        compiler_type=CompilerType.MINGW_GCC,
                        version=version or VersionInfo(major=0, minor=0, patch=0),
                        path=gpp_path,
                        architecture=env_config["architecture"],
                        capabilities=capabilities,
                        environment=EnvironmentInfo(
                            path=msys2_path,
                            include_paths=include_paths,
                            library_paths=library_paths,
                            environment_variables=env_vars
                        ),
                        metadata={
                            "installation_path": msys2_path,
                            "installation_type": "msys2",
                            "environment": env_name,
                            "msystem": env_config["msystem"],
                            "mingw_prefix": env_config["mingw_prefix"],
                            "mingw_chost": env_config["mingw_chost"],
                            "recommended": "true" if env_config["recommended"] else "false",
                            "detection_method": "msys2"
                        }
                    )
                    compilers.append(compiler)
                    self._logger.debug(f"Found MSYS2 {env_name}: {gpp_path}")

        return compilers

    def _detect_standalone(self) -> List[CompilerInfo]:
        """
        Detect standalone MinGW-w64 installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting standalone MinGW-w64 installations")

        compilers: List[CompilerInfo] = []

        for path in self._standalone_paths:
            self._logger.debug(f"Checking standalone path: {path}")

            if not os.path.exists(path):
                continue

            # Look for g++.exe in bin directory
            gpp_path = os.path.join(path, "bin", "g++.exe")

            if os.path.exists(gpp_path):
                version = self.detect_version(gpp_path)
                capabilities = self.detect_capabilities(gpp_path)

                # Determine architecture from path
                architecture = Architecture.X64
                if "mingw32" in path.lower() or "mingw-w32" in path.lower():
                    architecture = Architecture.X86
                elif "mingw64" in path.lower() or "mingw-w64" in path.lower():
                    architecture = Architecture.X64

                # Build include and library paths
                include_paths = [
                    os.path.join(path, "include"),
                    os.path.join(path, "x86_64-w64-mingw32", "include")
                ]

                library_paths = [
                    os.path.join(path, "lib"),
                    os.path.join(path, "x86_64-w64-mingw32", "lib")
                ]

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=gpp_path,
                    architecture=architecture,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(
                        path=path,
                        include_paths=include_paths,
                        library_paths=library_paths
                    ),
                    metadata={
                        "installation_path": path,
                        "installation_type": "standalone",
                        "detection_method": "standard_paths"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found standalone MinGW: {gpp_path}")

        return compilers

    def _detect_tdm_gcc(self) -> List[CompilerInfo]:
        """
        Detect TDM-GCC installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting TDM-GCC installations")

        compilers: List[CompilerInfo] = []

        for path in self._tdm_gcc_paths:
            self._logger.debug(f"Checking TDM-GCC path: {path}")

            if not os.path.exists(path):
                continue

            # Look for g++.exe in bin directory
            gpp_path = os.path.join(path, "bin", "g++.exe")

            if os.path.exists(gpp_path):
                version = self.detect_version(gpp_path)
                capabilities = self.detect_capabilities(gpp_path)

                # Determine architecture from path
                architecture = Architecture.X64
                if "TDM-GCC-32" in path:
                    architecture = Architecture.X86
                elif "TDM-GCC-64" in path:
                    architecture = Architecture.X64

                # Build include and library paths
                include_paths = [
                    os.path.join(path, "include"),
                    os.path.join(path, "lib", "gcc")
                ]

                library_paths = [
                    os.path.join(path, "lib"),
                    os.path.join(path, "lib64")
                ]

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=gpp_path,
                    architecture=architecture,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(
                        path=path,
                        include_paths=include_paths,
                        library_paths=library_paths
                    ),
                    metadata={
                        "installation_path": path,
                        "installation_type": "tdm_gcc",
                        "detection_method": "standard_paths"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found TDM-GCC: {gpp_path}")

        return compilers

    def _detect_via_package_managers(self) -> List[CompilerInfo]:
        """
        Detect MinGW installations via package managers

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting MinGW installations via package managers")

        compilers: List[CompilerInfo] = []

        # Detect Chocolatey installations
        chocolatey_compilers = self._detect_chocolatey_mingw()
        compilers.extend(chocolatey_compilers)
        self._logger.info(f"Found {len(chocolatey_compilers)} Chocolatey MinGW installations")

        # Detect Scoop installations
        scoop_compilers = self._detect_scoop_mingw()
        compilers.extend(scoop_compilers)
        self._logger.info(f"Found {len(scoop_compilers)} Scoop MinGW installations")

        # Detect winget installations
        winget_compilers = self._detect_winget_mingw()
        compilers.extend(winget_compilers)
        self._logger.info(f"Found {len(winget_compilers)} winget MinGW installations")

        return compilers

    def _detect_chocolatey_mingw(self) -> List[CompilerInfo]:
        """
        Detect MinGW installations via Chocolatey

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting Chocolatey MinGW installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("chocolatey", [])

        for path in paths:
            self._logger.debug(f"Checking Chocolatey path: {path}")

            if not os.path.exists(path):
                continue

            gpp_path = os.path.join(path, "bin", "g++.exe")

            if os.path.exists(gpp_path):
                version = self.detect_version(gpp_path)
                capabilities = self.detect_capabilities(gpp_path)

                # Build include and library paths
                include_paths = [
                    os.path.join(path, "include"),
                    os.path.join(path, "x86_64-w64-mingw32", "include")
                ]

                library_paths = [
                    os.path.join(path, "lib"),
                    os.path.join(path, "x86_64-w64-mingw32", "lib")
                ]

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=gpp_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(
                        path=path,
                        include_paths=include_paths,
                        library_paths=library_paths
                    ),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "chocolatey",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found Chocolatey MinGW: {gpp_path}")

        return compilers

    def _detect_scoop_mingw(self) -> List[CompilerInfo]:
        """
        Detect MinGW installations via Scoop

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting Scoop MinGW installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("scoop", [])

        for path in paths:
            self._logger.debug(f"Checking Scoop path: {path}")

            if not os.path.exists(path):
                continue

            gpp_path = os.path.join(path, "bin", "g++.exe")

            if os.path.exists(gpp_path):
                version = self.detect_version(gpp_path)
                capabilities = self.detect_capabilities(gpp_path)

                # Build include and library paths
                include_paths = [
                    os.path.join(path, "include"),
                    os.path.join(path, "x86_64-w64-mingw32", "include")
                ]

                library_paths = [
                    os.path.join(path, "lib"),
                    os.path.join(path, "x86_64-w64-mingw32", "lib")
                ]

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=gpp_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(
                        path=path,
                        include_paths=include_paths,
                        library_paths=library_paths
                    ),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "scoop",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found Scoop MinGW: {gpp_path}")

        return compilers

    def _detect_winget_mingw(self) -> List[CompilerInfo]:
        """
        Detect MinGW installations via winget

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting winget MinGW installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("winget", [])

        for path in paths:
            self._logger.debug(f"Checking winget path: {path}")

            if not os.path.exists(path):
                continue

            gpp_path = os.path.join(path, "bin", "g++.exe")

            if os.path.exists(gpp_path):
                version = self.detect_version(gpp_path)
                capabilities = self.detect_capabilities(gpp_path)

                # Build include and library paths
                include_paths = [
                    os.path.join(path, "include"),
                    os.path.join(path, "x86_64-w64-mingw32", "include")
                ]

                library_paths = [
                    os.path.join(path, "lib"),
                    os.path.join(path, "x86_64-w64-mingw32", "lib")
                ]

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=gpp_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(
                        path=path,
                        include_paths=include_paths,
                        library_paths=library_paths
                    ),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "winget",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found winget MinGW: {gpp_path}")

        return compilers

    def _get_msys2_paths(self) -> List[str]:
        """
        Get list of MSYS2 installation paths

        Returns:
            List of MSYS2 installation paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expandvars(r"%LOCALAPPDATA%"))

        return [
            r"C:\msys64",
            r"C:\msys32",
            os.path.join(local_app_data, "msys64"),
            os.path.join(local_app_data, "msys32"),
            os.path.join(program_files, "MSYS2"),
            os.path.join(program_files_x86, "MSYS2")
        ]

    def _get_standalone_paths(self) -> List[str]:
        """
        Get list of standalone MinGW-w64 installation paths

        Returns:
            List of standalone MinGW-w64 installation paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        return [
            r"C:\mingw64",
            r"C:\mingw32",
            r"C:\mingw",
            r"C:\mingw-w64",
            os.path.join(program_files, "mingw-w64"),
            os.path.join(program_files_x86, "mingw-w64"),
            os.path.join(program_files, "MinGW"),
            os.path.join(program_files_x86, "MinGW")
        ]

    def _get_tdm_gcc_paths(self) -> List[str]:
        """
        Get list of TDM-GCC installation paths

        Returns:
            List of TDM-GCC installation paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        return [
            r"C:\TDM-GCC-64",
            r"C:\TDM-GCC-32",
            r"C:\TDM-GCC",
            os.path.join(program_files, "TDM-GCC-64"),
            os.path.join(program_files_x86, "TDM-GCC-32"),
            os.path.join(program_files, "TDM-GCC")
        ]

    def _get_package_manager_paths(self) -> Dict[str, List[str]]:
        """
        Get list of package manager installation paths

        Returns:
            Dictionary mapping package manager names to paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        program_data = os.environ.get("ProgramData", r"C:\ProgramData")
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expandvars(r"%LOCALAPPDATA%"))

        return {
            "chocolatey": [
                os.path.join(program_data, r"chocolatey\lib\mingw\tools"),
                os.path.join(program_data, r"chocolatey\lib\mingw-w64\tools"),
                os.path.join(program_data, r"chocolatey\lib\mingw64\tools")
            ],
            "scoop": [
                os.path.join(local_app_data, r"scoop\apps\mingw\current"),
                os.path.join(local_app_data, r"scoop\apps\mingw-w64\current"),
                os.path.join(local_app_data, r"scoop\apps\mingw64\current")
            ],
            "winget": [
                os.path.join(program_files, "mingw-w64"),
                os.path.join(program_files_x86, "mingw-w64"),
                os.path.join(program_files, "MinGW"),
                os.path.join(program_files_x86, "MinGW")
            ]
        }
