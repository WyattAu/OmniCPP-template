"""
MSVC Compiler Detector

This module provides comprehensive detection of Microsoft Visual C++ compiler
installations, including all versions, editions, and architecture variants.
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
    X86_AMD64 = "x86_amd64"
    AMD64_X86 = "amd64_x86"
    AMD64_ARM = "amd64_arm"
    AMD64_ARM64 = "amd64_arm64"
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


@dataclass
class WindowsSDKInfo:
    """Windows SDK information"""
    version: str
    path: str
    product_version: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, any]:
        return {
            "version": self.version,
            "path": self.path,
            "product_version": self.product_version,
            "metadata": self.metadata
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


class MSVCDetector(ICompilerDetector):
    """Detector for Microsoft Visual C++ compiler installations"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize MSVC detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._vswhere_paths: List[str] = self._get_vswhere_paths()
        self._standard_paths: List[str] = self._get_standard_paths()
        self._detected_compilers: List[CompilerInfo] = []

    def detect(self) -> List[CompilerInfo]:
        """
        Detect all MSVC compiler installations

        Returns:
            List of detected compiler information
        """
        self._logger.info("Starting MSVC compiler detection")
        self._detected_compilers.clear()

        # Try detection methods in order of preference
        compilers = self._detect_via_vswhere()
        if not compilers:
            self._logger.warning("vswhere detection failed, trying standard paths")
            compilers = self._detect_via_standard_paths()
        if not compilers:
            self._logger.warning("Standard paths detection failed, trying registry")
            compilers = self._detect_via_registry()

        self._detected_compilers = compilers
        self._logger.info(f"Detected {len(compilers)} MSVC compiler installations")

        return compilers

    def detect_version(self, compiler_path: str) -> Optional[VersionInfo]:
        """
        Detect MSVC compiler version

        Args:
            compiler_path: Path to cl.exe

        Returns:
            Version information or None if detection fails
        """
        self._logger.debug(f"Detecting version for {compiler_path}")

        if not os.path.exists(compiler_path):
            self._logger.error(f"Compiler executable not found: {compiler_path}")
            return None

        try:
            result = subprocess.run(
                [compiler_path, "/?"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                self._logger.error(f"Failed to execute cl.exe: {result.stderr}")
                return None

            # Parse version from output
            # Example: "Microsoft (R) C/C++ Optimizing Compiler Version 19.40.33811 for x64"
            for line in result.stdout.split('\n'):
                if "Version" in line:
                    parts = line.split("Version")
                    if len(parts) > 1:
                        version_str = parts[1].strip().split()[0]
                        version_parts = version_str.split('.')
                        
                        # MSVC version format: major.minor.build (e.g., 19.40.33811)
                        # The third part is the build number, patch is typically 0
                        if len(version_parts) >= 3:
                            major = int(version_parts[0])
                            minor = int(version_parts[1])
                            build = version_parts[2] if len(version_parts) >= 3 else None
                            patch = 0  # MSVC typically uses build number instead of patch

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
            self._logger.error("cl.exe version detection timed out")
        except Exception as e:
            self._logger.error(f"Error detecting cl.exe version: {e}")

        return None

    def detect_capabilities(self, compiler_path: str) -> CapabilityInfo:
        """
        Detect MSVC compiler capabilities

        Args:
            compiler_path: Path to cl.exe

        Returns:
            Capability information
        """
        self._logger.debug(f"Detecting capabilities for {compiler_path}")

        capabilities = CapabilityInfo()

        # MSVC 19.40+ supports C++23
        # MSVC 19.28+ supports C++20
        # MSVC 19.14+ supports C++17
        # MSVC 19.00+ supports C++14

        version = self.detect_version(compiler_path)
        if version:
            if version.major >= 19 and version.minor >= 40:
                capabilities.cpp23 = True
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 19 and version.minor >= 28:
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
                capabilities.concepts = True
                capabilities.ranges = True
                capabilities.std_format = True
            elif version.major >= 19 and version.minor >= 14:
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.modules = True
                capabilities.coroutines = True
            elif version.major >= 19 and version.minor >= 0:
                capabilities.cpp14 = True

        capabilities.msvc_compatibility = True

        self._logger.debug(f"Detected capabilities: {capabilities.to_dict()}")
        return capabilities

    def validate(self, compiler_info: CompilerInfo) -> ValidationResult:
        """
        Validate MSVC compiler installation

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
                    [compiler_info.path, "/?"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    errors.append(f"Compiler executable is not functional: {result.stderr}")
            except Exception as e:
                errors.append(f"Failed to execute compiler: {e}")

        # Check if vcvarsall.bat exists
        vcvarsall_path = os.path.join(
            os.path.dirname(compiler_info.path),
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

    def _detect_via_vswhere(self) -> List[CompilerInfo]:
        """
        Detect MSVC installations via vswhere.exe

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting MSVC installations via vswhere.exe")

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
            self._logger.debug(f"Found {len(installations)} installations via vswhere")

            compilers: List[CompilerInfo] = []
            for installation in installations:
                compiler = self._parse_vswhere_installation(installation)
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

    def _detect_via_standard_paths(self) -> List[CompilerInfo]:
        """
        Detect MSVC installations via standard paths

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting MSVC installations via standard paths")

        compilers: List[CompilerInfo] = []

        for path in self._standard_paths:
            self._logger.debug(f"Checking standard path: {path}")

            if not os.path.exists(path):
                continue

            # Look for VC directory
            vc_path = os.path.join(path, "VC")
            if not os.path.exists(vc_path):
                continue

            # Detect cl.exe in various architecture directories
            architectures = [
                ("x64", "Hostx64", "x64"),
                ("x86", "Hostx86", "x86"),
                ("x86_amd64", "Hostx86", "x64"),
                ("amd64_x86", "Hostx64", "x86"),
                ("amd64_arm", "Hostx64", "arm"),
                ("amd64_arm64", "Hostx64", "arm64")
            ]

            for arch_name, host_dir, target_dir in architectures:
                cl_path = os.path.join(
                    vc_path,
                    "Tools",
                    "MSVC",
                    host_dir,
                    target_dir,
                    "cl.exe"
                )

                if os.path.exists(cl_path):
                    version = self.detect_version(cl_path)
                    capabilities = self.detect_capabilities(cl_path)

                    # Map architecture name to Architecture enum
                    # For cross-compilation architectures, use the target architecture
                    if arch_name == "x86_amd64":
                        arch_enum = Architecture.X64
                    elif arch_name == "amd64_x86":
                        arch_enum = Architecture.X86
                    elif arch_name == "amd64_arm":
                        arch_enum = Architecture.ARM
                    elif arch_name == "amd64_arm64":
                        arch_enum = Architecture.ARM64
                    else:
                        # For native architectures, try to map to enum
                        try:
                            arch_enum = Architecture(arch_name)
                        except ValueError:
                            # Fallback to X64 if unknown
                            arch_enum = Architecture.X64

                    compiler = CompilerInfo(
                        compiler_type=CompilerType.MSVC,
                        version=version or VersionInfo(major=0, minor=0, patch=0),
                        path=cl_path,
                        architecture=arch_enum,
                        capabilities=capabilities,
                        environment=EnvironmentInfo(path=path),
                        metadata={
                            "installation_path": path,
                            "detection_method": "standard_paths",
                            "architecture_name": arch_name
                        }
                    )
                    compilers.append(compiler)
                    self._logger.debug(f"Found compiler: {cl_path}")

        return compilers

    def _detect_via_registry(self) -> List[CompilerInfo]:
        """
        Detect MSVC installations via Windows registry

        Returns:
            List of detected compiler information
        """
        self._logger.info("Detecting MSVC installations via registry")

        compilers: List[CompilerInfo] = []

        try:
            import winreg

            # Registry keys to check
            registry_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\17.0"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\16.0"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\17.0"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\16.0")
            ]

            for hkey, subkey in registry_keys:
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        installation_path, _ = winreg.QueryValueEx(key, "InstallDir")
                        self._logger.debug(f"Found registry entry: {subkey} -> {installation_path}")

                        # Look for cl.exe
                        vc_path = os.path.join(installation_path, "..", "VC")
                        if os.path.exists(vc_path):
                            cl_path = os.path.join(
                                vc_path,
                                "Tools",
                                "MSVC",
                                "Hostx64",
                                "x64",
                                "cl.exe"
                            )

                            if os.path.exists(cl_path):
                                version = self.detect_version(cl_path)
                                capabilities = self.detect_capabilities(cl_path)

                                compiler = CompilerInfo(
                                    compiler_type=CompilerType.MSVC,
                                    version=version or VersionInfo(major=0, minor=0, patch=0),
                                    path=cl_path,
                                    architecture=Architecture.X64,
                                    capabilities=capabilities,
                                    environment=EnvironmentInfo(path=vc_path),
                                    metadata={
                                        "installation_path": installation_path,
                                        "detection_method": "registry",
                                        "registry_key": subkey
                                    }
                                )
                                compilers.append(compiler)
                                self._logger.debug(f"Found compiler via registry: {cl_path}")

                except (FileNotFoundError, OSError):
                    continue

        except ImportError:
            self._logger.error("winreg module not available (not on Windows)")
        except Exception as e:
            self._logger.error(f"Error querying registry: {e}")

        return compilers

    def _detect_executables(self, installation: Dict[str, str]) -> Dict[str, str]:
        """
        Detect compiler executables for an installation

        Args:
            installation: Installation information dictionary

        Returns:
            Dictionary mapping executable names to paths
        """
        self._logger.debug("Detecting executables for installation")

        executables: Dict[str, str] = {}
        installation_path = installation.get("installationPath", "")

        if not installation_path:
            return executables

        # Look for cl.exe in various architecture directories
        vc_path = os.path.join(installation_path, "VC")
        if not os.path.exists(vc_path):
            return executables

        architectures = [
            ("x64", "Hostx64", "x64"),
            ("x86", "Hostx86", "x86"),
            ("x86_amd64", "Hostx86", "x64"),
            ("amd64_x86", "Hostx64", "x86"),
            ("amd64_arm", "Hostx64", "arm"),
            ("amd64_arm64", "Hostx64", "arm64")
        ]

        for arch_name, host_dir, target_dir in architectures:
            cl_path = os.path.join(
                vc_path,
                "Tools",
                "MSVC",
                host_dir,
                target_dir,
                "cl.exe"
            )

            if os.path.exists(cl_path):
                executables[f"cl_{arch_name}"] = cl_path

            # Also look for link.exe
            link_path = os.path.join(
                vc_path,
                "Tools",
                "MSVC",
                host_dir,
                target_dir,
                "link.exe"
            )

            if os.path.exists(link_path):
                executables[f"link_{arch_name}"] = link_path

        self._logger.debug(f"Found {len(executables)} executables")
        return executables

    def _detect_windows_sdk(self) -> Optional[WindowsSDKInfo]:
        """
        Detect Windows SDK installation

        Returns:
            Windows SDK information or None if not found
        """
        self._logger.info("Detecting Windows SDK")

        try:
            import winreg

            # Registry keys for Windows SDK
            sdk_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Kits\Installed Roots"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows Kits\Installed Roots")
            ]

            for hkey, subkey in sdk_keys:
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        kits_root, _ = winreg.QueryValueEx(key, "KitsRoot10")
                        self._logger.debug(f"Found Windows Kits root: {kits_root}")

                        # Look for SDK versions
                        if os.path.exists(kits_root):
                            versions = [
                                d for d in os.listdir(kits_root)
                                if d.startswith("10.") and os.path.isdir(os.path.join(kits_root, d))
                            ]

                            if versions:
                                # Sort versions and get latest
                                versions.sort(reverse=True)
                                latest_version = versions[0]

                                sdk_info = WindowsSDKInfo(
                                    version=latest_version,
                                    path=os.path.join(kits_root, latest_version),
                                    metadata={"kits_root": kits_root}
                                )

                                self._logger.info(f"Detected Windows SDK {latest_version}")
                                return sdk_info

                except (FileNotFoundError, OSError):
                    continue

        except ImportError:
            self._logger.error("winreg module not available (not on Windows)")
        except Exception as e:
            self._logger.error(f"Error detecting Windows SDK: {e}")

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
        Get list of standard MSVC installation paths

        Returns:
            List of installation paths
        """
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        return [
            os.path.join(program_files, r"Microsoft Visual Studio\2022"),
            os.path.join(program_files, r"Microsoft Visual Studio\2019"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2022"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2019"),
            os.path.join(program_files, r"Microsoft Visual Studio\2022\BuildTools"),
            os.path.join(program_files, r"Microsoft Visual Studio\2019\BuildTools"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2022\BuildTools"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2019\BuildTools"),
        ]

    def _parse_vswhere_installation(self, installation: Dict[str, str]) -> Optional[CompilerInfo]:
        """
        Parse vswhere installation data into CompilerInfo

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

        # Detect executables
        executables = self._detect_executables(installation)

        # Use x64 native compiler as default
        cl_path = executables.get("cl_x64")
        if not cl_path:
            # Try to find any cl.exe
            for key, path in executables.items():
                if key.startswith("cl_"):
                    cl_path = path
                    break

        if not cl_path:
            return None

        # Detect version and capabilities
        version = self.detect_version(cl_path)
        capabilities = self.detect_capabilities(cl_path)

        # Detect Windows SDK
        sdk_info = self._detect_windows_sdk()

        # Determine architecture from path
        architecture = Architecture.X64
        if "x86" in cl_path:
            architecture = Architecture.X86
        elif "arm64" in cl_path:
            architecture = Architecture.ARM64
        elif "arm" in cl_path:
            architecture = Architecture.ARM

        # Build environment info
        env_info = EnvironmentInfo(
            path=installation_path,
            include_paths=[],
            library_paths=[],
            environment_variables={}
        )

        if sdk_info:
            env_info.include_paths.append(os.path.join(sdk_info.path, "Include"))
            env_info.library_paths.append(os.path.join(sdk_info.path, "Lib"))
            env_info.environment_variables["WindowsSDKVersion"] = sdk_info.version

        # Build metadata
        metadata = {
            "installation_path": installation_path,
            "product_id": product_id,
            "display_name": display_name,
            "detection_method": "vswhere",
            "executables": json.dumps(executables)
        }

        if sdk_info:
            metadata["windows_sdk"] = json.dumps(sdk_info.to_dict())

        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version or VersionInfo(major=0, minor=0, patch=0),
            path=cl_path,
            architecture=architecture,
            capabilities=capabilities,
            environment=env_info,
            metadata=metadata
        )

        self._logger.debug(f"Parsed compiler: {display_name} at {cl_path}")
        return compiler
