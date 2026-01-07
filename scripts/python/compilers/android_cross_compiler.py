"""
Android Cross-Compiler Detection Module

This module provides detection and validation for Android NDK cross-compilation
toolchains on Windows systems, supporting various target architectures including
arm64-v8a, armeabi-v7a, x86_64, and x86.
"""

import os
import logging
import subprocess
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class NDKInfo:
    """Android NDK information dataclass
    
    Attributes:
        version: NDK version string
        root_path: Path to NDK root directory
        toolchain_path: Path to toolchain directory
        platforms_path: Path to platforms directory
        sysroot_path: Path to sysroot directory
    """
    version: str
    root_path: str
    toolchain_path: str
    platforms_path: str
    sysroot_path: str

    def to_dict(self) -> Dict[str, str]:
        """Convert NDK info to dictionary
        
        Returns:
            Dictionary representation of NDK info
        """
        return {
            "version": self.version,
            "root_path": self.root_path,
            "toolchain_path": self.toolchain_path,
            "platforms_path": self.platforms_path,
            "sysroot_path": self.sysroot_path
        }

    def is_valid(self) -> bool:
        """Check if NDK installation is valid
        
        Returns:
            True if all paths exist, False otherwise
        """
        paths = [
            self.root_path,
            self.toolchain_path,
            self.platforms_path,
            self.sysroot_path
        ]
        return all(os.path.exists(p) for p in paths)


@dataclass
class ToolchainInfo:
    """Android toolchain information dataclass
    
    Attributes:
        name: Toolchain name (e.g., "arm64-v8a")
        clang: Path to clang compiler
        clangxx: Path to clang++ compiler
        ar: Path to ar utility
        strip: Path to strip utility
        sysroot: Path to sysroot directory
    """
    name: str
    clang: str
    clangxx: str
    ar: str
    strip: str
    sysroot: str

    def to_dict(self) -> Dict[str, str]:
        """Convert toolchain info to dictionary
        
        Returns:
            Dictionary representation of toolchain info
        """
        return {
            "name": self.name,
            "clang": self.clang,
            "clangxx": self.clangxx,
            "ar": self.ar,
            "strip": self.strip,
            "sysroot": self.sysroot
        }

    def is_valid(self) -> bool:
        """Check if toolchain is valid
        
        Returns:
            True if all executables exist, False otherwise
        """
        executables = [self.clang, self.clangxx, self.ar, self.strip]
        return all(os.path.exists(exe) for exe in executables)


@dataclass
class CrossCompilerInfo:
    """Cross-compiler information dataclass
    
    Attributes:
        target_platform: Target platform (e.g., "android")
        target_architecture: Target architecture (e.g., "arm64-v8a")
        toolchain_path: Path to toolchain directory
        sysroot: Path to sysroot directory
        compilers: Dictionary of compiler tools
        cmake_generator: CMake generator name
        metadata: Additional metadata
    """
    target_platform: str
    target_architecture: str
    toolchain_path: str
    sysroot: str
    compilers: Dict[str, str]
    cmake_generator: str
    metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert cross-compiler info to dictionary
        
        Returns:
            Dictionary representation of cross-compiler info
        """
        return {
            "target_platform": self.target_platform,
            "target_architecture": self.target_architecture,
            "toolchain_path": self.toolchain_path,
            "sysroot": self.sysroot,
            "compilers": self.compilers,
            "cmake_generator": self.cmake_generator,
            "metadata": self.metadata
        }

    def is_valid(self) -> bool:
        """Check if cross-compiler is valid
        
        Returns:
            True if toolchain path exists, False otherwise
        """
        return os.path.exists(self.toolchain_path)


class ICrossCompiler(ABC):
    """Interface for cross-compilers
    
    All cross-compiler implementations must inherit from this class and implement
    abstract methods defined below.
    """

    @abstractmethod
    def detect(self) -> Optional[CrossCompilerInfo]:
        """Detect cross-compiler
        
        Returns:
            Cross-compiler information or None if not found
        """
        pass

    @abstractmethod
    def setup_environment(self) -> Dict[str, str]:
        """Setup cross-compilation environment
        
        Returns:
            Dictionary of environment variables
        """
        pass

    @abstractmethod
    def get_cmake_generator(self) -> str:
        """Get CMake generator for this cross-compiler
        
        Returns:
            CMake generator string
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate cross-compiler installation
        
        Returns:
            True if valid, False otherwise
        """
        pass


class AndroidCrossCompiler(ICrossCompiler):
    """Android cross-compiler detector and configurator
    
    This class detects Android NDK installation on Windows systems for Android
    cross-compilation, supporting various target architectures including arm64-v8a,
    armeabi-v7a, x86_64, and x86.
    
    Supported target architectures:
    - arm64-v8a (64-bit ARM)
    - armeabi-v7a (32-bit ARM)
    - x86_64 (64-bit x86)
    - x86 (32-bit x86)
    """

    # Common Android NDK search paths on Windows
    NDK_PATHS = [
        r"C:\Android\Sdk\ndk",
        r"C:\Android\ndk",
        r"C:\Android\android-ndk",
        r"C:\Program Files\Android\ndk",
        r"C:\Program Files (x86)\Android\ndk",
        r"C:\tools\android-ndk",
        os.path.expanduser(r"~\AppData\Local\Android\Sdk\ndk"),
        os.path.expanduser(r"~\AppData\Local\Android\ndk"),
    ]

    # Supported Android target architectures
    SUPPORTED_TARGETS = [
        "arm64-v8a",
        "armeabi-v7a",
        "x86_64",
        "x86",
    ]

    # Architecture to LLVM triple mapping
    ARCH_TRIPLE_MAP = {
        "arm64-v8a": "aarch64-linux-android",
        "armeabi-v7a": "armv7a-linux-androideabi",
        "x86_64": "x86_64-linux-android",
        "x86": "i686-linux-android",
    }

    # Architecture to CMake processor mapping
    ARCH_PROCESSOR_MAP = {
        "arm64-v8a": "aarch64",
        "armeabi-v7a": "armv7-a",
        "x86_64": "x86_64",
        "x86": "i686",
    }

    def __init__(self, target_architecture: str = "arm64-v8a") -> None:
        """Initialize Android cross-compiler detector
        
        Args:
            target_architecture: Target architecture (default: arm64-v8a)
        """
        self._target_architecture = target_architecture
        self._ndk: Optional[NDKInfo] = None
        self._toolchain: Optional[ToolchainInfo] = None
        self._info: Optional[CrossCompilerInfo] = None
        self._logger = logging.getLogger(__name__)

    def detect(self) -> Optional[CrossCompilerInfo]:
        """Detect Android cross-compiler
        
        This method searches for Android NDK installation in standard locations
        and validates its availability for the specified target architecture.
        
        Returns:
            Cross-compiler information or None if not found
        """
        self._logger.info(f"Detecting Android cross-compiler for {self._target_architecture}")

        try:
            # Validate target architecture
            if self._target_architecture not in self.SUPPORTED_TARGETS:
                self._logger.error(
                    f"Unsupported target architecture: {self._target_architecture}"
                )
                return None

            # Detect NDK
            ndk = self.detect_ndk()
            
            if not ndk:
                self._logger.warning("No Android NDK installation found")
                return None

            self._ndk = ndk

            # Detect toolchain
            toolchain = self.detect_toolchain()
            
            if not toolchain:
                self._logger.warning(
                    f"No toolchain found for {self._target_architecture}"
                )
                return None

            self._toolchain = toolchain
            self._info = self._create_cross_compiler_info()
            
            self._logger.info(
                f"Successfully detected Android cross-compiler: {self._target_architecture} "
                f"(NDK {ndk.version})"
            )
            return self._info

        except Exception as e:
            self._logger.error(
                f"Error detecting Android cross-compiler: {str(e)}"
            )
            return None

    def detect_ndk(self) -> Optional[NDKInfo]:
        """Detect Android NDK installation
        
        This method searches for Android NDK in standard locations and
        validates installation by checking for required directories and files.
        
        Returns:
            NDK information or None if not found
        """
        self._logger.info("Detecting Android NDK installation")

        try:
            # Check environment variable first
            ndk_path = os.environ.get("ANDROID_NDK_ROOT") or os.environ.get("NDK_HOME")
            if ndk_path and os.path.exists(ndk_path):
                self._logger.debug(f"Found ANDROID_NDK_ROOT: {ndk_path}")
                ndk = self._check_ndk(ndk_path)
                if ndk:
                    return ndk

            # Search in standard paths
            for path in self.NDK_PATHS:
                if not os.path.exists(path):
                    continue

                # Check for NDK subdirectories (versioned)
                try:
                    for entry in os.listdir(path):
                        entry_path = os.path.join(path, entry)
                        if os.path.isdir(entry_path):
                            self._logger.debug(f"Checking NDK path: {entry_path}")
                            ndk = self._check_ndk(entry_path)
                            if ndk:
                                return ndk
                except Exception as e:
                    self._logger.debug(f"Error listing directory {path}: {str(e)}")
                    continue

            self._logger.warning("No Android NDK installation found")
            return None

        except Exception as e:
            self._logger.error(
                f"Error detecting Android NDK: {str(e)}"
            )
            return None

    def detect_toolchain(self) -> Optional[ToolchainInfo]:
        """Detect toolchain for target architecture
        
        This method searches for Android toolchain executables and sysroot for
        the specified target architecture.
        
        Returns:
            Toolchain information or None if not found
        """
        self._logger.info(f"Detecting toolchain for {self._target_architecture}")

        try:
            if not self._ndk:
                self._logger.error("NDK not detected. Call detect_ndk() first.")
                return None

            # Get LLVM triple for architecture
            llvm_triple = self.ARCH_TRIPLE_MAP.get(self._target_architecture)
            if not llvm_triple:
                self._logger.error(
                    f"Unknown LLVM triple for architecture: {self._target_architecture}"
                )
                return None

            # Construct toolchain paths
            toolchain_dir = os.path.join(
                self._ndk.toolchain_path,
                "llvm",
                "prebuilt",
                self._get_host_tag(),
                "bin"
            )

            if not os.path.exists(toolchain_dir):
                self._logger.warning(
                    f"Toolchain directory does not exist: {toolchain_dir}"
                )
                return None

            # Construct executable paths
            clang_path = os.path.join(toolchain_dir, f"clang")
            clangxx_path = os.path.join(toolchain_dir, f"clang++")
            ar_path = os.path.join(toolchain_dir, f"llvm-ar")
            strip_path = os.path.join(toolchain_dir, f"llvm-strip")

            # Check if executables exist
            if not all(os.path.exists(p) for p in [clang_path, clangxx_path, ar_path, strip_path]):
                self._logger.warning(
                    f"Toolchain executables not found in {toolchain_dir}"
                )
                return None

            toolchain = ToolchainInfo(
                name=self._target_architecture,
                clang=clang_path,
                clangxx=clangxx_path,
                ar=ar_path,
                strip=strip_path,
                sysroot=self._ndk.sysroot_path
            )

            self._logger.info(
                f"Successfully detected toolchain: {toolchain.name}"
            )
            return toolchain

        except Exception as e:
            self._logger.error(
                f"Error detecting toolchain: {str(e)}"
            )
            return None

    def detect_target_triple(self) -> Optional[str]:
        """Detect target triple for architecture
        
        This method returns the LLVM target triple for the specified architecture.
        
        Returns:
            Target triple string or None if not supported
        """
        self._logger.info(f"Detecting target triple for {self._target_architecture}")

        if self._target_architecture in self.ARCH_TRIPLE_MAP:
            target_triple = self.ARCH_TRIPLE_MAP[self._target_architecture]
            self._logger.info(f"Target triple: {target_triple}")
            return target_triple
        else:
            self._logger.warning(
                f"Unsupported target architecture: {self._target_architecture}"
            )
            return None

    def setup_environment(self) -> Dict[str, str]:
        """Setup Android cross-compilation environment
        
        This method configures environment variables required for Android
        cross-compilation, including CMake variables and NDK-specific settings.
        
        Returns:
            Dictionary of environment variables
            
        Raises:
            RuntimeError: If NDK or toolchain has not been detected
        """
        if not self._ndk or not self._toolchain:
            raise RuntimeError(
                "NDK or toolchain not detected. Call detect() first."
            )

        self._logger.info(
            f"Setting up Android cross-compilation environment for {self._target_architecture}"
        )

        try:
            # Get processor for architecture
            processor = self.ARCH_PROCESSOR_MAP.get(self._target_architecture, self._target_architecture)

            # Build environment variables
            env = {
                "CMAKE_SYSTEM_NAME": "Android",
                "CMAKE_SYSTEM_PROCESSOR": processor,
                "CMAKE_C_COMPILER": self._toolchain.clang,
                "CMAKE_CXX_COMPILER": self._toolchain.clangxx,
                "CMAKE_AR": self._toolchain.ar,
                "CMAKE_STRIP": self._toolchain.strip,
                "CMAKE_ANDROID_NDK": self._ndk.root_path,
                "CMAKE_ANDROID_STL": "c++_shared",
                "CMAKE_ANDROID_ARCH_ABI": self._target_architecture,
                "CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION": "clang",
                "CMAKE_GENERATOR": "Ninja",
            }

            # Add architecture-specific settings
            if self._target_architecture == "arm64-v8a":
                env["CMAKE_ANDROID_ARM_MODE"] = "arm"
                env["CMAKE_ANDROID_ARM_NEON"] = "ON"

            # Add NDK toolchain to PATH
            toolchain_bin = os.path.dirname(self._toolchain.clang)
            if os.path.exists(toolchain_bin):
                current_path = os.environ.get("PATH", "")
                env["PATH"] = f"{toolchain_bin}{os.pathsep}{current_path}"

            self._logger.info(
                f"Successfully configured Android cross-compilation environment"
            )

            return env

        except Exception as e:
            self._logger.error(
                f"Error setting up environment: {str(e)}"
            )
            raise

    def get_cmake_generator(self) -> str:
        """Get CMake generator for Android cross-compilation
        
        Returns:
            CMake generator string (always "Ninja" for Android)
        """
        return "Ninja"

    def validate(self) -> bool:
        """Validate Android cross-compiler installation
        
        This method validates that all required NDK and toolchain executables
        exist and are accessible.
        
        Returns:
            True if valid, False otherwise
        """
        self._logger.info(
            f"Validating Android cross-compiler for {self._target_architecture}"
        )

        try:
            if not self._ndk:
                self._logger.error("No NDK installation to validate")
                return False

            if not self._toolchain:
                self._logger.error("No toolchain to validate")
                return False

            # Check NDK paths
            ndk_paths = [
                (self._ndk.root_path, "NDK root"),
                (self._ndk.toolchain_path, "Toolchain directory"),
                (self._ndk.platforms_path, "Platforms directory"),
                (self._ndk.sysroot_path, "Sysroot directory"),
            ]

            all_valid = True
            for path, name in ndk_paths:
                if os.path.exists(path):
                    self._logger.debug(f"Found {name}: {path}")
                else:
                    self._logger.error(f"Missing {name}: {path}")
                    all_valid = False

            # Check toolchain executables
            executables = [
                (self._toolchain.clang, "Clang compiler"),
                (self._toolchain.clangxx, "Clang++ compiler"),
                (self._toolchain.ar, "LLVM ar utility"),
                (self._toolchain.strip, "LLVM strip utility"),
            ]

            for exe_path, exe_name in executables:
                if os.path.exists(exe_path):
                    self._logger.debug(f"Found {exe_name}: {exe_path}")
                else:
                    self._logger.error(f"Missing {exe_name}: {exe_path}")
                    all_valid = False

            # Check NDK version
            if self._ndk.version:
                self._logger.debug(f"NDK version: {self._ndk.version}")
            else:
                self._logger.warning("Could not determine NDK version")

            if all_valid:
                self._logger.info(
                    f"Android cross-compiler validation successful"
                )
            else:
                self._logger.error(
                    f"Android cross-compiler validation failed"
                )

            return all_valid

        except Exception as e:
            self._logger.error(
                f"Error validating cross-compiler: {str(e)}"
            )
            return False

    def _check_ndk(self, path: str) -> Optional[NDKInfo]:
        """Check if Android NDK exists in path
        
        Args:
            path: Directory to check for NDK
            
        Returns:
            NDKInfo if found, None otherwise
        """
        # Normalize path
        path = os.path.normpath(path)

        # Check for required directories
        toolchain_path = os.path.join(path, "toolchains")
        platforms_path = os.path.join(path, "platforms")
        sysroot_path = os.path.join(path, "sysroot")

        if not all(os.path.exists(p) for p in [toolchain_path, platforms_path, sysroot_path]):
            return None

        # Get version
        version = self._get_ndk_version(path)

        return NDKInfo(
            version=version,
            root_path=path,
            toolchain_path=toolchain_path,
            platforms_path=platforms_path,
            sysroot_path=sysroot_path
        )

    def _get_ndk_version(self, ndk_path: str) -> str:
        """Get Android NDK version
        
        Args:
            ndk_path: Path to NDK root directory
            
        Returns:
            Version string or empty string if detection fails
        """
        try:
            # Try to read source.properties file
            source_props = os.path.join(ndk_path, "source.properties")
            if os.path.exists(source_props):
                with open(source_props, 'r') as f:
                    content = f.read()
                    # Parse version from source.properties
                    # Format: Pkg.Revision = 25.2.9519653
                    match = re.search(r"Pkg\.Revision\s*=\s*([\d.]+)", content)
                    if match:
                        return match.group(1)

            # Try to read release.txt file
            release_txt = os.path.join(ndk_path, "release.txt")
            if os.path.exists(release_txt):
                with open(release_txt, 'r') as f:
                    content = f.read()
                    # Parse version from release.txt
                    # Format: r25b (64-bit) or 25.2.9519653
                    match = re.search(r"r(\d+)[b\.]?\s*\((\d+-bit)\)", content)
                    if match:
                        return f"{match.group(1)} ({match.group(2)})"
                    match = re.search(r"([\d.]+)", content)
                    if match:
                        return match.group(1)

            # Try to get version from directory name
            dir_name = os.path.basename(ndk_path)
            match = re.search(r"android-ndk-r?(\d+)", dir_name)
            if match:
                return match.group(1)

            return ""

        except Exception as e:
            self._logger.warning(
                f"Could not get NDK version: {str(e)}"
            )
            return ""

    def _get_host_tag(self) -> str:
        """Get host tag for current platform
        
        Returns:
            Host tag string (e.g., "windows-x86_64")
        """
        import platform
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "windows":
            if machine in ["amd64", "x86_64"]:
                return "windows-x86_64"
            elif machine in ["i386", "i686", "x86"]:
                return "windows"
        elif system == "linux":
            if machine in ["amd64", "x86_64"]:
                return "linux-x86_64"
            elif machine in ["i386", "i686", "x86"]:
                return "linux"
        elif system == "darwin":
            if machine in ["amd64", "x86_64"]:
                return "darwin-x86_64"
            elif machine in ["arm64", "aarch64"]:
                return "darwin-arm64"

        # Default to windows-x86_64
        return "windows-x86_64"

    def _create_cross_compiler_info(self) -> CrossCompilerInfo:
        """Create cross-compiler information from detected NDK and toolchain
        
        Returns:
            Cross-compiler information
        """
        if not self._ndk or not self._toolchain:
            raise RuntimeError("NDK or toolchain not detected")

        return CrossCompilerInfo(
            target_platform="android",
            target_architecture=self._target_architecture,
            toolchain_path=os.path.dirname(self._toolchain.clang),
            sysroot=self._ndk.sysroot_path,
            compilers={
                "cc": self._toolchain.clang,
                "cxx": self._toolchain.clangxx,
                "ar": self._toolchain.ar,
                "strip": self._toolchain.strip
            },
            cmake_generator="Ninja",
            metadata={
                "ndk_version": self._ndk.version,
                "ndk_root": self._ndk.root_path,
                "target_architecture": self._target_architecture,
                "llvm_triple": self.ARCH_TRIPLE_MAP.get(self._target_architecture, ""),
                "toolchain_name": self._toolchain.name
            }
        )
