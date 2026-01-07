"""
Linux Cross-Compiler Detection Module

This module provides detection and validation for Linux cross-compilation toolchains
on Windows systems, supporting various target architectures including x86_64, aarch64,
and ARM variants.
"""

import os
import logging
from typing import Optional, Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ToolchainInfo:
    """Toolchain information dataclass
    
    Attributes:
        name: Toolchain name (e.g., "x86_64-linux-gnu")
        gcc: Path to GCC compiler
        gxx: Path to G++ compiler
        ar: Path to ar utility
        strip: Path to strip utility
        sysroot: Path to sysroot directory
    """
    name: str
    gcc: str
    gxx: str
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
            "gcc": self.gcc,
            "gxx": self.gxx,
            "ar": self.ar,
            "strip": self.strip,
            "sysroot": self.sysroot
        }

    def is_valid(self) -> bool:
        """Check if toolchain is valid
        
        Returns:
            True if all executables exist, False otherwise
        """
        executables = [self.gcc, self.gxx, self.ar, self.strip]
        return all(os.path.exists(exe) for exe in executables)


@dataclass
class CrossCompilerInfo:
    """Cross-compiler information dataclass
    
    Attributes:
        target_platform: Target platform (e.g., "linux")
        target_architecture: Target architecture (e.g., "x86_64-linux-gnu")
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

    def to_dict(self) -> Dict[str, any]:
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


class LinuxCrossCompiler(ICrossCompiler):
    """Linux cross-compiler detector and configurator
    
    This class detects Linux cross-compilation toolchains on Windows systems,
    supporting various target architectures including x86_64, aarch64, and ARM.
    
    Supported target architectures:
    - x86_64-linux-gnu
    - aarch64-linux-gnu
    - arm-linux-gnueabihf
    - arm-linux-gnueabi
    """

    # Common toolchain search paths on Windows
    TOOLCHAIN_PATHS = [
        r"C:\msys64\mingw64\bin",
        r"C:\msys64\ucrt64\bin",
        r"C:\msys64\mingw32\bin",
        r"C:\mingw64\bin",
        r"C:\mingw\bin",
        r"C:\tools\mingw64\bin",
    ]

    # Supported Linux target architectures
    SUPPORTED_TARGETS = [
        "x86_64-linux-gnu",
        "aarch64-linux-gnu",
        "arm-linux-gnueabihf",
        "arm-linux-gnueabi",
    ]

    def __init__(self, target_architecture: str = "x86_64-linux-gnu") -> None:
        """Initialize Linux cross-compiler detector
        
        Args:
            target_architecture: Target architecture (default: x86_64-linux-gnu)
        """
        self._target_architecture = target_architecture
        self._toolchain: Optional[ToolchainInfo] = None
        self._info: Optional[CrossCompilerInfo] = None
        self._logger = logging.getLogger(__name__)

    def detect(self) -> Optional[CrossCompilerInfo]:
        """Detect Linux cross-compiler
        
        This method searches for Linux cross-compilation toolchains in standard
        locations and validates their availability.
        
        Returns:
            Cross-compiler information or None if not found
        """
        self._logger.info(f"Detecting Linux cross-compiler for {self._target_architecture}")

        try:
            toolchains = self._detect_toolchains()

            if self._target_architecture in toolchains:
                self._toolchain = toolchains[self._target_architecture]
                self._info = self._create_cross_compiler_info()
                self._logger.info(
                    f"Successfully detected Linux cross-compiler: {self._target_architecture}"
                )
                return self._info
            else:
                self._logger.warning(
                    f"No Linux cross-compiler found for {self._target_architecture}"
                )
                return None

        except Exception as e:
            self._logger.error(
                f"Error detecting Linux cross-compiler: {str(e)}"
            )
            return None

    def detect_toolchain(self) -> Optional[ToolchainInfo]:
        """Detect toolchain for target architecture
        
        This method searches for the toolchain executables and sysroot for the
        specified target architecture.
        
        Returns:
            Toolchain information or None if not found
        """
        self._logger.info(f"Detecting toolchain for {self._target_architecture}")

        try:
            toolchains = self._detect_toolchains()

            if self._target_architecture in toolchains:
                toolchain = toolchains[self._target_architecture]
                self._logger.info(
                    f"Successfully detected toolchain: {toolchain.name}"
                )
                return toolchain
            else:
                self._logger.warning(
                    f"No toolchain found for {self._target_architecture}"
                )
                return None

        except Exception as e:
            self._logger.error(
                f"Error detecting toolchain: {str(e)}"
            )
            return None

    def detect_sysroot(self) -> Optional[str]:
        """Detect sysroot for target architecture
        
        This method searches for the sysroot directory for the specified
        target architecture.
        
        Returns:
            Sysroot path or None if not found
        """
        self._logger.info(f"Detecting sysroot for {self._target_architecture}")

        try:
            toolchain = self.detect_toolchain()

            if toolchain and toolchain.sysroot:
                if os.path.exists(toolchain.sysroot):
                    self._logger.info(
                        f"Successfully detected sysroot: {toolchain.sysroot}"
                    )
                    return toolchain.sysroot
                else:
                    self._logger.warning(
                        f"Sysroot path does not exist: {toolchain.sysroot}"
                    )
                    return None
            else:
                self._logger.warning(
                    f"No sysroot found for {self._target_architecture}"
                )
                return None

        except Exception as e:
            self._logger.error(
                f"Error detecting sysroot: {str(e)}"
            )
            return None

    def detect_target_triple(self) -> Optional[str]:
        """Detect target triple for architecture
        
        This method returns the target triple for the specified architecture.
        
        Returns:
            Target triple string or None if not supported
        """
        self._logger.info(f"Detecting target triple for {self._target_architecture}")

        if self._target_architecture in self.SUPPORTED_TARGETS:
            self._logger.info(
                f"Target triple: {self._target_architecture}"
            )
            return self._target_architecture
        else:
            self._logger.warning(
                f"Unsupported target architecture: {self._target_architecture}"
            )
            return None

    def setup_environment(self) -> Dict[str, str]:
        """Setup Linux cross-compilation environment
        
        This method configures the environment variables required for Linux
        cross-compilation, including CMake variables and compiler paths.
        
        Returns:
            Dictionary of environment variables
            
        Raises:
            RuntimeError: If toolchain has not been detected
        """
        if not self._toolchain:
            raise RuntimeError(
                "Toolchain not detected. Call detect() first."
            )

        self._logger.info(
            f"Setting up Linux cross-compilation environment for {self._target_architecture}"
        )

        try:
            # Extract processor from target triple
            processor = self._target_architecture.split("-")[0]

            # Build environment variables
            env = {
                "CMAKE_SYSTEM_NAME": "Linux",
                "CMAKE_SYSTEM_PROCESSOR": processor,
                "CMAKE_C_COMPILER": self._toolchain.gcc,
                "CMAKE_CXX_COMPILER": self._toolchain.gxx,
                "CMAKE_AR": self._toolchain.ar,
                "CMAKE_STRIP": self._toolchain.strip,
                "CMAKE_GENERATOR": "Ninja",
            }

            # Add sysroot if available
            if self._toolchain.sysroot and os.path.exists(self._toolchain.sysroot):
                env["CMAKE_SYSROOT"] = self._toolchain.sysroot
                env["CMAKE_FIND_ROOT_PATH"] = self._toolchain.sysroot
                env["CMAKE_FIND_ROOT_PATH_MODE_PROGRAM"] = "NEVER"
                env["CMAKE_FIND_ROOT_PATH_MODE_LIBRARY"] = "ONLY"
                env["CMAKE_FIND_ROOT_PATH_MODE_INCLUDE"] = "ONLY"

            self._logger.info(
                f"Successfully configured Linux cross-compilation environment"
            )

            return env

        except Exception as e:
            self._logger.error(
                f"Error setting up environment: {str(e)}"
            )
            raise

    def get_cmake_generator(self) -> str:
        """Get CMake generator for Linux cross-compilation
        
        Returns:
            CMake generator string (always "Ninja" for cross-compilation)
        """
        return "Ninja"

    def validate(self) -> bool:
        """Validate Linux cross-compiler installation
        
        This method validates that all required toolchain executables exist
        and are accessible.
        
        Returns:
            True if valid, False otherwise
        """
        self._logger.info(
            f"Validating Linux cross-compiler for {self._target_architecture}"
        )

        try:
            if not self._toolchain:
                self._logger.error("No toolchain to validate")
                return False

            # Check if all executables exist
            executables = [
                (self._toolchain.gcc, "GCC compiler"),
                (self._toolchain.gxx, "G++ compiler"),
                (self._toolchain.ar, "AR utility"),
                (self._toolchain.strip, "Strip utility"),
            ]

            all_valid = True
            for exe_path, exe_name in executables:
                if os.path.exists(exe_path):
                    self._logger.debug(f"Found {exe_name}: {exe_path}")
                else:
                    self._logger.error(f"Missing {exe_name}: {exe_path}")
                    all_valid = False

            # Check sysroot if specified
            if self._toolchain.sysroot:
                if os.path.exists(self._toolchain.sysroot):
                    self._logger.debug(f"Found sysroot: {self._toolchain.sysroot}")
                else:
                    self._logger.warning(
                        f"Sysroot does not exist: {self._toolchain.sysroot}"
                    )

            if all_valid:
                self._logger.info(
                    f"Linux cross-compiler validation successful"
                )
            else:
                self._logger.error(
                    f"Linux cross-compiler validation failed"
                )

            return all_valid

        except Exception as e:
            self._logger.error(
                f"Error validating cross-compiler: {str(e)}"
            )
            return False

    def _detect_toolchains(self) -> Dict[str, ToolchainInfo]:
        """Detect Linux cross-compilation toolchains
        
        This method searches for all available Linux cross-compilation toolchains
        in standard locations.
        
        Returns:
            Dictionary mapping toolchain names to toolchain information
        """
        toolchains: Dict[str, ToolchainInfo] = {}

        for path in self.TOOLCHAIN_PATHS:
            if not os.path.exists(path):
                continue

            # Check for each supported target
            for target in self.SUPPORTED_TARGETS:
                toolchain = self._check_toolchain(path, target)
                if toolchain:
                    toolchains[target] = toolchain
                    self._logger.debug(f"Found toolchain {target} in {path}")

        return toolchains

    def _check_toolchain(self, path: str, target: str) -> Optional[ToolchainInfo]:
        """Check if toolchain exists for target in path
        
        Args:
            path: Directory to search for toolchain
            target: Target architecture
            
        Returns:
            ToolchainInfo if found, None otherwise
        """
        # Construct executable paths
        gcc_path = os.path.join(path, f"{target}-gcc.exe")
        gxx_path = os.path.join(path, f"{target}-g++.exe")
        ar_path = os.path.join(path, f"{target}-gcc-ar.exe")
        strip_path = os.path.join(path, f"{target}-strip.exe")

        # Check if all executables exist
        if not all(os.path.exists(p) for p in [gcc_path, gxx_path, ar_path, strip_path]):
            return None

        # Determine sysroot path
        # Try common sysroot locations
        sysroot_candidates = [
            os.path.join(os.path.dirname(path), target),
            os.path.join(path, "..", "..", target),
            os.path.join(path, "..", target),
        ]

        sysroot = None
        for candidate in sysroot_candidates:
            if os.path.exists(candidate):
                sysroot = os.path.normpath(candidate)
                break

        return ToolchainInfo(
            name=target,
            gcc=gcc_path,
            gxx=gxx_path,
            ar=ar_path,
            strip=strip_path,
            sysroot=sysroot or ""
        )

    def _create_cross_compiler_info(self) -> CrossCompilerInfo:
        """Create cross-compiler information from detected toolchain
        
        Returns:
            Cross-compiler information
        """
        if not self._toolchain:
            raise RuntimeError("Toolchain not detected")

        return CrossCompilerInfo(
            target_platform="linux",
            target_architecture=self._target_architecture,
            toolchain_path=os.path.dirname(self._toolchain.gcc),
            sysroot=self._toolchain.sysroot,
            compilers={
                "cc": self._toolchain.gcc,
                "cxx": self._toolchain.gxx,
                "ar": self._toolchain.ar,
                "strip": self._toolchain.strip
            },
            cmake_generator="Ninja",
            metadata={
                "target_triple": self._target_architecture,
                "toolchain_name": self._toolchain.name
            }
        )
