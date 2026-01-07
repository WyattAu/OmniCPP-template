"""
MSVC-Clang Compiler Detector

This module provides comprehensive detection of LLVM/Clang compiler installations
that work with MSVC environment, including bundled LLVM, standalone installations,
and package manager installations.
"""

import json
import logging
import os
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


class MSVCClangDetector(ICompilerDetector):
    """Detector for MSVC-Clang (LLVM/Clang with MSVC compatibility) installations"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize MSVC-Clang detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._vswhere_paths: List[str] = self._get_vswhere_paths()
        self._standard_paths: List[str] = self._get_standard_paths()
        self._package_manager_paths: Dict[str, List[str]] = self._get_package_manager_paths()
        self._detected_compilers: List[CompilerInfo] = []

    def detect(self) -> List[CompilerInfo]:
        """
        Detect all MSVC-Clang compiler installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Starting MSVC-Clang compiler detection")
        self._detected_compilers.clear()

        # Try detection methods in order of preference
        compilers: List[CompilerInfo] = []

        # Detect bundled LLVM with VS installations
        bundled_compilers = self._detect_bundled_llvm()
        compilers.extend(bundled_compilers)
        self._logger.info(f"Found {len(bundled_compilers)} bundled LLVM installations")

        # Detect standalone LLVM installations
        standalone_compilers = self._detect_standalone_llvm()
        compilers.extend(standalone_compilers)
        self._logger.info(f"Found {len(standalone_compilers)} standalone LLVM installations")

        # Detect LLVM via package managers
        package_compilers = self._detect_via_package_managers()
        compilers.extend(package_compilers)
        self._logger.info(f"Found {len(package_compilers)} package manager LLVM installations")

        # Sort by version (latest first)
        compilers.sort(key=lambda c: (c.version.major, c.version.minor, c.version.patch), reverse=True)

        # Mark recommended installation (first one)
        if compilers:
            compilers[0].metadata["recommended"] = "true"

        self._detected_compilers = compilers
        self._logger.info(f"Detected {len(compilers)} MSVC-Clang compiler installations")

        return compilers

    def detect_version(self, compiler_path: str) -> Optional[VersionInfo]:
        """
        Detect Clang compiler version

        Args:
            compiler_path: Path to clang-cl.exe

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
                self._logger.error(f"Failed to execute clang-cl.exe: {result.stderr}")
                return None

            # Parse version from output
            # Example: "clang version 18.1.3 (https://github.com/llvm/llvm-project.git ...)"
            for line in result.stdout.split('\n'):
                if "clang version" in line:
                    parts = line.split("clang version")
                    if len(parts) > 1:
                        version_str = parts[1].strip().split()[0]
                        version_parts = version_str.split('.')

                        # Clang version format: major.minor.patch (e.g., 18.1.3)
                        if len(version_parts) >= 3:
                            major = int(version_parts[0])
                            minor = int(version_parts[1])
                            patch = int(version_parts[2])
                            build = None

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
            self._logger.error("clang-cl.exe version detection timed out")
        except Exception as e:
            self._logger.error(f"Error detecting clang-cl.exe version: {e}")

        return None

    def detect_capabilities(self, compiler_path: str) -> CapabilityInfo:
        """
        Detect Clang compiler capabilities

        Args:
            compiler_path: Path to clang-cl.exe

        Returns:
            Capability information
        """
        self._logger.debug(f"Detecting capabilities for {compiler_path}")

        capabilities = CapabilityInfo()

        # Clang 18+ supports C++23
        # Clang 17+ supports C++20
        # Clang 16+ supports C++17
        # Clang 14+ supports C++14

        version = self.detect_version(compiler_path)
        if version:
            if version.major >= 18:
                capabilities.cpp23 = True
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 17:
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 16:
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 14:
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True

        capabilities.msvc_compatibility = True

        self._logger.debug(f"Detected capabilities: {capabilities.to_dict()}")
        return capabilities

    def validate(self, compiler_info: CompilerInfo) -> ValidationResult:
        """
        Validate MSVC-Clang compiler installation

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

        # Check if MSVC environment is available
        vcvarsall_path = os.path.join(
            os.path.dirname(compiler_info.path),
            "..",
            "..",
            "..",
            "Auxiliary",
            "Build",
            "vcvarsall.bat"
        )
        if not os.path.exists(vcvarsall_path):
            warnings.append(f"vcvarsall.bat not found at: {vcvarsall_path}")

        is_valid = len(errors) == 0

        self._logger.debug(f"Validation result: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}")
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _detect_bundled_llvm(self) -> List[CompilerInfo]:
        """
        Detect LLVM bundled with Visual Studio installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting bundled LLVM installations")

        vswhere_path = self._find_vswhere()
        if not vswhere_path:
            self._logger.error("vswhere.exe not found")
            return []

        self._logger.debug(f"Using vswhere at: {vswhere_path}")

        try:
            # Query vswhere for all installations
            result = subprocess.run(
                [
                    vswhere_path,
                    "-all",
                    "-products", "*",
                    "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86_x64",
                    "-property", "installationPath",
                    "-property", "productId",
                    "-property", "displayName",
                    "-format", "json"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self._logger.error(f"vswhere failed: {result.stderr}")
                return []

            installations = json.loads(result.stdout)
            self._logger.debug(f"Found {len(installations)} VS installations via vswhere")

            compilers: List[CompilerInfo] = []
            for installation in installations:
                compiler = self._parse_bundled_llvm_installation(installation)
                if compiler:
                    compilers.append(compiler)

            return compilers

        except json.JSONDecodeError as e:
            self._logger.error(f"Failed to parse vswhere JSON output: {e}")
        except subprocess.TimeoutExpired:
            self._logger.error("vswhere execution timed out")
        except Exception as e:
            self._logger.error(f"Error executing vswhere: {e}")

        return []

    def _detect_standalone_llvm(self) -> List[CompilerInfo]:
        """
        Detect standalone LLVM installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting standalone LLVM installations")

        compilers: List[CompilerInfo] = []

        for path in self._standard_paths:
            self._logger.debug(f"Checking standard path: {path}")

            if not os.path.exists(path):
                continue

            # Look for clang-cl.exe in bin directory
            clang_cl_path = os.path.join(path, "bin", "clang-cl.exe")

            if os.path.exists(clang_cl_path):
                version = self.detect_version(clang_cl_path)
                capabilities = self.detect_capabilities(clang_cl_path)

                # Determine architecture from path
                architecture = Architecture.X64
                if "x86" in path.lower():
                    architecture = Architecture.X86
                elif "arm64" in path.lower():
                    architecture = Architecture.ARM64
                elif "arm" in path.lower():
                    architecture = Architecture.ARM

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=clang_cl_path,
                    architecture=architecture,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(path=path),
                    metadata={
                        "installation_path": path,
                        "installation_type": "standalone",
                        "detection_method": "standard_paths"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found standalone LLVM: {clang_cl_path}")

        return compilers

    def _detect_via_package_managers(self) -> List[CompilerInfo]:
        """
        Detect LLVM installations via package managers

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting LLVM installations via package managers")

        compilers: List[CompilerInfo] = []

        # Detect Chocolatey installations
        chocolatey_compilers = self._detect_chocolatey_llvm()
        compilers.extend(chocolatey_compilers)
        self._logger.info(f"Found {len(chocolatey_compilers)} Chocolatey LLVM installations")

        # Detect Scoop installations
        scoop_compilers = self._detect_scoop_llvm()
        compilers.extend(scoop_compilers)
        self._logger.info(f"Found {len(scoop_compilers)} Scoop LLVM installations")

        # Detect winget installations
        winget_compilers = self._detect_winget_llvm()
        compilers.extend(winget_compilers)
        self._logger.info(f"Found {len(winget_compilers)} winget LLVM installations")

        return compilers

    def _detect_chocolatey_llvm(self) -> List[CompilerInfo]:
        """
        Detect LLVM installations via Chocolatey

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting Chocolatey LLVM installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("chocolatey", [])

        for path in paths:
            self._logger.debug(f"Checking Chocolatey path: {path}")

            if not os.path.exists(path):
                continue

            clang_cl_path = os.path.join(path, "bin", "clang-cl.exe")

            if os.path.exists(clang_cl_path):
                version = self.detect_version(clang_cl_path)
                capabilities = self.detect_capabilities(clang_cl_path)

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=clang_cl_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(path=path),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "chocolatey",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found Chocolatey LLVM: {clang_cl_path}")

        return compilers

    def _detect_scoop_llvm(self) -> List[CompilerInfo]:
        """
        Detect LLVM installations via Scoop

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting Scoop LLVM installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("scoop", [])

        for path in paths:
            self._logger.debug(f"Checking Scoop path: {path}")

            if not os.path.exists(path):
                continue

            clang_cl_path = os.path.join(path, "bin", "clang-cl.exe")

            if os.path.exists(clang_cl_path):
                version = self.detect_version(clang_cl_path)
                capabilities = self.detect_capabilities(clang_cl_path)

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=clang_cl_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(path=path),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "scoop",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found Scoop LLVM: {clang_cl_path}")

        return compilers

    def _detect_winget_llvm(self) -> List[CompilerInfo]:
        """
        Detect LLVM installations via winget

        Returns:
            List of detected compiler information
        """
        self._logger.debug("Detecting winget LLVM installations")

        compilers: List[CompilerInfo] = []
        paths = self._package_manager_paths.get("winget", [])

        for path in paths:
            self._logger.debug(f"Checking winget path: {path}")

            if not os.path.exists(path):
                continue

            clang_cl_path = os.path.join(path, "bin", "clang-cl.exe")

            if os.path.exists(clang_cl_path):
                version = self.detect_version(clang_cl_path)
                capabilities = self.detect_capabilities(clang_cl_path)

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=clang_cl_path,
                    architecture=Architecture.X64,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(path=path),
                    metadata={
                        "installation_path": path,
                        "installation_type": "package_manager",
                        "package_manager": "winget",
                        "detection_method": "package_manager"
                    }
                )
                compilers.append(compiler)
                self._logger.debug(f"Found winget LLVM: {clang_cl_path}")

        return compilers

    def _parse_bundled_llvm_installation(self, installation: Dict[str, str]) -> Optional[CompilerInfo]:
        """
        Parse bundled LLVM installation data into CompilerInfo

        Args:
            installation: Installation data from vswhere

        Returns:
            CompilerInfo or None if parsing fails
        """
        installation_path = installation.get("installationPath", "")
        product_id = installation.get("productId", "")
        display_name = installation.get("displayName", "")

        if not installation_path:
            return None

        # Look for LLVM in VC\Tools\Llvm
        llvm_path = os.path.join(installation_path, "VC", "Tools", "Llvm")
        if not os.path.exists(llvm_path):
            self._logger.debug(f"No bundled LLVM found at: {llvm_path}")
            return None

        # Detect clang-cl.exe in various architecture directories
        architectures = [
            ("x64", "x64"),
            ("x86", "x86")
        ]

        for arch_name, arch_dir in architectures:
            clang_cl_path = os.path.join(llvm_path, arch_dir, "bin", "clang-cl.exe")

            if os.path.exists(clang_cl_path):
                version = self.detect_version(clang_cl_path)
                capabilities = self.detect_capabilities(clang_cl_path)

                # Map architecture name to Architecture enum
                try:
                    arch_enum = Architecture(arch_name)
                except ValueError:
                    arch_enum = Architecture.X64

                # Build metadata
                metadata = {
                    "installation_path": installation_path,
                    "llvm_path": llvm_path,
                    "product_id": product_id,
                    "display_name": display_name,
                    "installation_type": "bundled",
                    "detection_method": "vswhere"
                }

                # Extract VS version from display name
                if "2022" in display_name:
                    metadata["vs_version"] = "2022"
                elif "2019" in display_name:
                    metadata["vs_version"] = "2019"

                compiler = CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=version or VersionInfo(major=0, minor=0, patch=0),
                    path=clang_cl_path,
                    architecture=arch_enum,
                    capabilities=capabilities,
                    environment=EnvironmentInfo(path=llvm_path),
                    metadata=metadata
                )

                self._logger.debug(f"Parsed bundled LLVM: {display_name} at {clang_cl_path}")
                return compiler

        return None

    def _find_vswhere(self) -> Optional[str]:
        """
        Find vswhere.exe executable

        Returns:
            Path to vswhere.exe or None if not found
        """
        self._logger.debug("Searching for vswhere.exe")

        for path in self._vswhere_paths:
            if os.path.exists(path):
                self._logger.debug(f"Found vswhere at: {path}")
                return path

        return None

    def _get_vswhere_paths(self) -> List[str]:
        """
        Get list of possible vswhere.exe paths

        Returns:
            List of vswhere.exe paths
        """
        program_files = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        program_data = os.environ.get("ProgramData", r"C:\ProgramData")

        return [
            os.path.join(program_files, r"Microsoft Visual Studio\Installer\vswhere.exe"),
            os.path.join(program_data, r"Microsoft Visual Studio\Installer\vswhere.exe"),
            os.path.join(program_files, r"Microsoft Visual Studio\Installer\vswhere.exe"),
        ]

    def _get_standard_paths(self) -> List[str]:
        """
        Get list of standard LLVM installation paths

        Returns:
            List of installation paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        return [
            os.path.join(program_files, "LLVM"),
            os.path.join(program_files_x86, "LLVM"),
            r"C:\LLVM"
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
                os.path.join(program_data, r"chocolatey\lib\LLVM\tools"),
                os.path.join(program_data, r"chocolatey\lib\llvm\tools")
            ],
            "scoop": [
                os.path.join(local_app_data, r"scoop\apps\llvm\current"),
                os.path.join(local_app_data, r"scoop\apps\LLVM\current")
            ],
            "winget": [
                os.path.join(program_files, "LLVM"),
                os.path.join(program_files_x86, "LLVM")
            ]
        }
