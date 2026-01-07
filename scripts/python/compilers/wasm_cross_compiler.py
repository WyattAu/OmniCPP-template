"""
WASM Cross-Compiler Detection Module

This module provides detection and validation for WebAssembly (WASM) cross-compilation
using Emscripten on Windows systems, supporting various target architectures including
wasm32 and wasm64.
"""

import os
import logging
import subprocess
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class EmscriptenInfo:
    """Emscripten information dataclass
    
    Attributes:
        version: Emscripten version string
        root_path: Path to Emscripten root directory
        emcc_path: Path to emcc compiler
        emxx_path: Path to em++ compiler
        emar_path: Path to emar archiver
        emcmake_path: Path to emcmake tool
        emconfigure_path: Path to emconfigure tool
    """
    version: str
    root_path: str
    emcc_path: str
    emxx_path: str
    emar_path: str
    emcmake_path: str
    emconfigure_path: str

    def to_dict(self) -> Dict[str, str]:
        """Convert Emscripten info to dictionary
        
        Returns:
            Dictionary representation of Emscripten info
        """
        return {
            "version": self.version,
            "root_path": self.root_path,
            "emcc_path": self.emcc_path,
            "emxx_path": self.emxx_path,
            "emar_path": self.emar_path,
            "emcmake_path": self.emcmake_path,
            "emconfigure_path": self.emconfigure_path
        }

    def is_valid(self) -> bool:
        """Check if Emscripten installation is valid
        
        Returns:
            True if all executables exist, False otherwise
        """
        executables = [
            self.emcc_path,
            self.emxx_path,
            self.emar_path,
            self.emcmake_path,
            self.emconfigure_path
        ]
        return all(os.path.exists(exe) for exe in executables)


@dataclass
class CrossCompilerInfo:
    """Cross-compiler information dataclass
    
    Attributes:
        target_platform: Target platform (e.g., "wasm")
        target_architecture: Target architecture (e.g., "wasm32", "wasm64")
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


class WASMCrossCompiler(ICrossCompiler):
    """WASM cross-compiler detector and configurator
    
    This class detects Emscripten installation on Windows systems for WebAssembly
    cross-compilation, supporting various target architectures including wasm32 and wasm64.
    
    Supported target architectures:
    - wasm32 (32-bit WebAssembly)
    - wasm64 (64-bit WebAssembly)
    """

    # Common Emscripten search paths on Windows
    EMSCRIPTEN_PATHS = [
        r"C:\emsdk",
        r"C:\emsdk\upstream\emscripten",
        r"C:\Program Files\Emscripten",
        r"C:\Program Files (x86)\Emscripten",
        r"C:\tools\emsdk",
        r"C:\tools\emsdk\upstream\emscripten",
        os.path.expanduser(r"~\emsdk"),
        os.path.expanduser(r"~\emsdk\upstream\emscripten"),
    ]

    # Supported WASM target architectures
    SUPPORTED_TARGETS = [
        "wasm32",
        "wasm64",
    ]

    def __init__(self, target_architecture: str = "wasm32") -> None:
        """Initialize WASM cross-compiler detector
        
        Args:
            target_architecture: Target architecture (default: wasm32)
        """
        self._target_architecture = target_architecture
        self._emscripten: Optional[EmscriptenInfo] = None
        self._info: Optional[CrossCompilerInfo] = None
        self._logger = logging.getLogger(__name__)

    def detect(self) -> Optional[CrossCompilerInfo]:
        """Detect WASM cross-compiler
        
        This method searches for Emscripten installation in standard locations
        and validates its availability.
        
        Returns:
            Cross-compiler information or None if not found
        """
        self._logger.info(f"Detecting WASM cross-compiler for {self._target_architecture}")

        try:
            # Validate target architecture
            if self._target_architecture not in self.SUPPORTED_TARGETS:
                self._logger.error(
                    f"Unsupported target architecture: {self._target_architecture}"
                )
                return None

            # Detect Emscripten
            emscripten = self.detect_emscripten()
            
            if not emscripten:
                self._logger.warning("No Emscripten installation found")
                return None

            self._emscripten = emscripten
            self._info = self._create_cross_compiler_info()
            
            self._logger.info(
                f"Successfully detected WASM cross-compiler: {self._target_architecture} "
                f"(Emscripten {emscripten.version})"
            )
            return self._info

        except Exception as e:
            self._logger.error(
                f"Error detecting WASM cross-compiler: {str(e)}"
            )
            return None

    def detect_emscripten(self) -> Optional[EmscriptenInfo]:
        """Detect Emscripten installation
        
        This method searches for Emscripten in standard locations and
        validates the installation by checking for required executables.
        
        Returns:
            Emscripten information or None if not found
        """
        self._logger.info("Detecting Emscripten installation")

        try:
            # Check environment variable first
            emscripten_root = os.environ.get("EMSCRIPTEN_ROOT_PATH")
            if emscripten_root and os.path.exists(emscripten_root):
                self._logger.debug(
                    f"Found EMSCRIPTEN_ROOT_PATH: {emscripten_root}"
                )
                emscripten = self._check_emscripten(emscripten_root)
                if emscripten:
                    return emscripten

            # Search in standard paths
            for path in self.EMSCRIPTEN_PATHS:
                if not os.path.exists(path):
                    continue

                self._logger.debug(f"Checking path: {path}")
                emscripten = self._check_emscripten(path)
                if emscripten:
                    return emscripten

            # Try to find emcc in PATH
            emscripten = self._detect_emscripten_from_path()
            if emscripten:
                return emscripten

            self._logger.warning("No Emscripten installation found")
            return None

        except Exception as e:
            self._logger.error(
                f"Error detecting Emscripten: {str(e)}"
            )
            return None

    def detect_emcc(self) -> Optional[str]:
        """Detect emcc compiler path
        
        This method searches for the emcc compiler executable.
        
        Returns:
            Path to emcc or None if not found
        """
        self._logger.info("Detecting emcc compiler")

        try:
            # Check if Emscripten is already detected
            if self._emscripten:
                return self._emscripten.emcc_path

            # Try to find emcc in PATH
            emcc_path = self._find_executable_in_path("emcc")
            if emcc_path:
                self._logger.info(f"Found emcc: {emcc_path}")
                return emcc_path

            self._logger.warning("emcc not found")
            return None

        except Exception as e:
            self._logger.error(
                f"Error detecting emcc: {str(e)}"
            )
            return None

    def detect_emar(self) -> Optional[str]:
        """Detect emar archiver path
        
        This method searches for the emar archiver executable.
        
        Returns:
            Path to emar or None if not found
        """
        self._logger.info("Detecting emar archiver")

        try:
            # Check if Emscripten is already detected
            if self._emscripten:
                return self._emscripten.emar_path

            # Try to find emar in PATH
            emar_path = self._find_executable_in_path("emar")
            if emar_path:
                self._logger.info(f"Found emar: {emar_path}")
                return emar_path

            self._logger.warning("emar not found")
            return None

        except Exception as e:
            self._logger.error(
                f"Error detecting emar: {str(e)}"
            )
            return None

    def setup_environment(self) -> Dict[str, str]:
        """Setup WASM cross-compilation environment
        
        This method configures environment variables required for WebAssembly
        cross-compilation using Emscripten, including CMake variables and
        Emscripten-specific settings.
        
        Returns:
            Dictionary of environment variables
            
        Raises:
            RuntimeError: If Emscripten has not been detected
        """
        if not self._emscripten:
            raise RuntimeError(
                "Emscripten not detected. Call detect() first."
            )

        self._logger.info(
            f"Setting up WASM cross-compilation environment for {self._target_architecture}"
        )

        try:
            # Build environment variables
            env = {
                "CMAKE_SYSTEM_NAME": "Emscripten",
                "CMAKE_SYSTEM_PROCESSOR": self._target_architecture,
                "CMAKE_C_COMPILER": self._emscripten.emcc_path,
                "CMAKE_CXX_COMPILER": self._emscripten.emxx_path,
                "CMAKE_AR": self._emscripten.emar_path,
                "EMSCRIPTEN_ROOT_PATH": self._emscripten.root_path,
                "EMSCRIPTEN": self._emscripten.root_path,
                "CMAKE_GENERATOR": "Ninja",
                "CMAKE_EXECUTABLE_SUFFIX": ".html",
                "CMAKE_POSITION_INDEPENDENT_CODE": "ON",
            }

            # Add Emscripten tools to PATH
            emscripten_bin = os.path.join(self._emscripten.root_path, "bin")
            if os.path.exists(emscripten_bin):
                current_path = os.environ.get("PATH", "")
                env["PATH"] = f"{emscripten_bin}{os.pathsep}{current_path}"

            self._logger.info(
                f"Successfully configured WASM cross-compilation environment"
            )

            return env

        except Exception as e:
            self._logger.error(
                f"Error setting up environment: {str(e)}"
            )
            raise

    def get_cmake_generator(self) -> str:
        """Get CMake generator for WASM cross-compilation
        
        Returns:
            CMake generator string (always "Ninja" for Emscripten)
        """
        return "Ninja"

    def validate(self) -> bool:
        """Validate WASM cross-compiler installation
        
        This method validates that all required Emscripten executables exist
        and are accessible, and that the installation can compile a simple program.
        
        Returns:
            True if valid, False otherwise
        """
        self._logger.info(
            f"Validating WASM cross-compiler for {self._target_architecture}"
        )

        try:
            if not self._emscripten:
                self._logger.error("No Emscripten installation to validate")
                return False

            # Check if all executables exist
            executables = [
                (self._emscripten.emcc_path, "emcc compiler"),
                (self._emscripten.emxx_path, "em++ compiler"),
                (self._emscripten.emar_path, "emar archiver"),
                (self._emscripten.emcmake_path, "emcmake tool"),
                (self._emscripten.emconfigure_path, "emconfigure tool"),
            ]

            all_valid = True
            for exe_path, exe_name in executables:
                if os.path.exists(exe_path):
                    self._logger.debug(f"Found {exe_name}: {exe_path}")
                else:
                    self._logger.error(f"Missing {exe_name}: {exe_path}")
                    all_valid = False

            # Check root path
            if os.path.exists(self._emscripten.root_path):
                self._logger.debug(f"Found Emscripten root: {self._emscripten.root_path}")
            else:
                self._logger.error(
                    f"Emscripten root path does not exist: {self._emscripten.root_path}"
                )
                all_valid = False

            # Try to get version
            if self._emscripten.version:
                self._logger.debug(f"Emscripten version: {self._emscripten.version}")
            else:
                self._logger.warning("Could not determine Emscripten version")

            if all_valid:
                self._logger.info(
                    f"WASM cross-compiler validation successful"
                )
            else:
                self._logger.error(
                    f"WASM cross-compiler validation failed"
                )

            return all_valid

        except Exception as e:
            self._logger.error(
                f"Error validating cross-compiler: {str(e)}"
            )
            return False

    def _check_emscripten(self, path: str) -> Optional[EmscriptenInfo]:
        """Check if Emscripten exists in path
        
        Args:
            path: Directory to check for Emscripten
            
        Returns:
            EmscriptenInfo if found, None otherwise
        """
        # Normalize path
        path = os.path.normpath(path)

        # Check for emcc executable
        emcc_path = os.path.join(path, "emcc")
        if not os.path.exists(emcc_path):
            emcc_path = os.path.join(path, "emcc.bat")
        if not os.path.exists(emcc_path):
            emcc_path = os.path.join(path, "emcc.exe")

        if not os.path.exists(emcc_path):
            return None

        # Check for other executables
        emxx_path = os.path.join(path, "em++")
        if not os.path.exists(emxx_path):
            emxx_path = os.path.join(path, "em++.bat")
        if not os.path.exists(emxx_path):
            emxx_path = os.path.join(path, "em++.exe")

        emar_path = os.path.join(path, "emar")
        if not os.path.exists(emar_path):
            emar_path = os.path.join(path, "emar.bat")
        if not os.path.exists(emar_path):
            emar_path = os.path.join(path, "emar.exe")

        emcmake_path = os.path.join(path, "emcmake")
        if not os.path.exists(emcmake_path):
            emcmake_path = os.path.join(path, "emcmake.bat")
        if not os.path.exists(emcmake_path):
            emcmake_path = os.path.join(path, "emcmake.exe")

        emconfigure_path = os.path.join(path, "emconfigure")
        if not os.path.exists(emconfigure_path):
            emconfigure_path = os.path.join(path, "emconfigure.bat")
        if not os.path.exists(emconfigure_path):
            emconfigure_path = os.path.join(path, "emconfigure.exe")

        # Verify all executables exist
        if not all(os.path.exists(p) for p in [
            emcc_path, emxx_path, emar_path, emcmake_path, emconfigure_path
        ]):
            return None

        # Get version
        version = self._get_emscripten_version(emcc_path)

        return EmscriptenInfo(
            version=version,
            root_path=path,
            emcc_path=emcc_path,
            emxx_path=emxx_path,
            emar_path=emar_path,
            emcmake_path=emcmake_path,
            emconfigure_path=emconfigure_path
        )

    def _detect_emscripten_from_path(self) -> Optional[EmscriptenInfo]:
        """Detect Emscripten from system PATH
        
        Returns:
            EmscriptenInfo if found, None otherwise
        """
        try:
            emcc_path = self._find_executable_in_path("emcc")
            if not emcc_path:
                return None

            # Get root path from emcc location
            root_path = os.path.dirname(emcc_path)

            # Check for other executables
            emxx_path = self._find_executable_in_path("em++")
            emar_path = self._find_executable_in_path("emar")
            emcmake_path = self._find_executable_in_path("emcmake")
            emconfigure_path = self._find_executable_in_path("emconfigure")

            if not all([emxx_path, emar_path, emcmake_path, emconfigure_path]):
                return None

            # Get version
            version = self._get_emscripten_version(emcc_path)

            # Ensure all paths are strings (not None)
            return EmscriptenInfo(
                version=version,
                root_path=root_path or "",
                emcc_path=emcc_path or "",
                emxx_path=emxx_path or "",
                emar_path=emar_path or "",
                emcmake_path=emcmake_path or "",
                emconfigure_path=emconfigure_path or ""
            )

        except Exception as e:
            self._logger.error(
                f"Error detecting Emscripten from PATH: {str(e)}"
            )
            return None

    def _get_emscripten_version(self, emcc_path: str) -> str:
        """Get Emscripten version
        
        Args:
            emcc_path: Path to emcc executable
            
        Returns:
            Version string or empty string if detection fails
        """
        try:
            result = subprocess.run(
                [emcc_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse version from output
                # Expected format: "emcc (Emscripten gcc-like replacement) 3.1.34"
                # Try multiple patterns
                patterns = [
                    r"Emscripten\s+(\d+\.\d+\.\d+)",  # "Emscripten 3.1.34"
                    r"Emscripten\s+([\d.]+)",  # "Emscripten 3.1.34"
                    r"emcc.*?(\d+\.\d+\.\d+)",  # "emcc ... 3.1.34"
                    r"(\d+\.\d+\.\d+)",  # Just version number
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, result.stdout)
                    if match:
                        return match.group(1)

            return ""

        except Exception as e:
            self._logger.warning(
                f"Could not get Emscripten version: {str(e)}"
            )
            return ""

    def _find_executable_in_path(self, name: str) -> Optional[str]:
        """Find executable in system PATH
        
        Args:
            name: Name of executable to find
            
        Returns:
            Path to executable or None if not found
        """
        try:
            # Check for .bat, .exe, or no extension
            extensions = [".bat", ".exe", ""] if os.name == "nt" else [""]

            for ext in extensions:
                executable = f"{name}{ext}"
                result = subprocess.run(
                    ["where", executable] if os.name == "nt" else ["which", executable],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:
                    path = result.stdout.strip().split("\n")[0]
                    if os.path.exists(path):
                        return path

            return None

        except Exception as e:
            self._logger.debug(
                f"Could not find {name} in PATH: {str(e)}"
            )
            return None

    def _create_cross_compiler_info(self) -> CrossCompilerInfo:
        """Create cross-compiler information from detected Emscripten
        
        Returns:
            Cross-compiler information
        """
        if not self._emscripten:
            raise RuntimeError("Emscripten not detected")

        return CrossCompilerInfo(
            target_platform="wasm",
            target_architecture=self._target_architecture,
            toolchain_path=self._emscripten.root_path,
            sysroot=self._emscripten.root_path,
            compilers={
                "cc": self._emscripten.emcc_path,
                "cxx": self._emscripten.emxx_path,
                "ar": self._emscripten.emar_path,
                "emcmake": self._emscripten.emcmake_path,
                "emconfigure": self._emscripten.emconfigure_path
            },
            cmake_generator="Ninja",
            metadata={
                "emscripten_version": self._emscripten.version,
                "emscripten_root": self._emscripten.root_path,
                "target_architecture": self._target_architecture
            }
        )
