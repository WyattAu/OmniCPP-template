"""
Platform Detector - Detect OS, compiler, and build environment

This module provides platform detection for operating system, CPU architecture,
available compilers, and build environment for OmniCPP build system.
"""

import platform
import shutil
import subprocess
import sys
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class CompilerInfo:
    """Compiler information data class."""
    
    name: str
    version: str
    path: str
    type: str  # msvc, msvc-clang, mingw-gcc, mingw-clang, gcc, clang


class PlatformDetector:
    """Detect OS, compiler, and build environment."""
    
    def __init__(self) -> None:
        """Initialize platform detector."""
        self.system = platform.system()
        self.machine = platform.machine()
    
    def detect_os(self) -> str:
        """Detect operating system.
        
        Returns:
            OS name (windows, linux, wasm)
        """
        if self.system == "Windows":
            return "windows"
        elif self.system == "Linux":
            return "linux"
        elif "emscripten" in sys.version.lower() or "wasm" in sys.version.lower():
            return "wasm"
        else:
            return "unknown"
    
    def detect_architecture(self) -> str:
        """Detect CPU architecture.
        
        Returns:
            Architecture name (x64, arm64)
        """
        machine = self.machine.lower()
        
        if machine in ["x86_64", "amd64"]:
            return "x64"
        elif machine in ["arm64", "aarch64"]:
            return "arm64"
        elif machine in ["i386", "i686"]:
            return "x86"
        elif machine in ["armv7l"]:
            return "arm"
        else:
            return "unknown"
    
    def detect_compilers(self) -> List[CompilerInfo]:
        """Detect available compilers.
        
        Returns:
            List of available compilers
        """
        compilers: List[CompilerInfo] = []
        
        if self.system == "Windows":
            compilers.extend(self._detect_windows_compilers())
        elif self.system == "Linux":
            compilers.extend(self._detect_linux_compilers())
        
        return compilers
    
    def _detect_windows_compilers(self) -> List[CompilerInfo]:
        """Detect Windows compilers.
        
        Returns:
            List of detected Windows compilers
        """
        compilers: List[CompilerInfo] = []
        
        # Detect MSVC (cl.exe)
        cl_path = shutil.which("cl.exe")
        if cl_path:
            version = self._get_msvc_version()
            compilers.append(CompilerInfo(
                name="MSVC",
                version=version,
                path=cl_path,
                type="msvc"
            ))
        
        # Detect MSVC-Clang (clang-cl)
        clang_cl_path = shutil.which("clang-cl")
        if clang_cl_path:
            version = self._get_clang_version(clang_cl_path)
            compilers.append(CompilerInfo(
                name="MSVC-Clang",
                version=version,
                path=clang_cl_path,
                type="msvc-clang"
            ))
        
        # Detect MinGW-GCC
        gcc_path = shutil.which("gcc.exe")
        if gcc_path and "mingw" in gcc_path.lower():
            version = self._get_gcc_version(gcc_path)
            compilers.append(CompilerInfo(
                name="MinGW-GCC",
                version=version,
                path=gcc_path,
                type="mingw-gcc"
            ))
        
        # Detect MinGW-Clang
        clang_path = shutil.which("clang.exe")
        if clang_path and "mingw" in clang_path.lower():
            version = self._get_clang_version(clang_path)
            compilers.append(CompilerInfo(
                name="MinGW-Clang",
                version=version,
                path=clang_path,
                type="mingw-clang"
            ))
        
        return compilers
    
    def _detect_linux_compilers(self) -> List[CompilerInfo]:
        """Detect Linux compilers.
        
        Returns:
            List of detected Linux compilers
        """
        compilers: List[CompilerInfo] = []
        
        # Detect GCC
        gcc_path = shutil.which("gcc")
        if gcc_path:
            version = self._get_gcc_version(gcc_path)
            compilers.append(CompilerInfo(
                name="GCC",
                version=version,
                path=gcc_path,
                type="gcc"
            ))
        
        # Detect Clang
        clang_path = shutil.which("clang")
        if clang_path:
            version = self._get_clang_version(clang_path)
            compilers.append(CompilerInfo(
                name="Clang",
                version=version,
                path=clang_path,
                type="clang"
            ))
        
        return compilers
    
    def _get_msvc_version(self) -> str:
        """Get MSVC version.
        
        Returns:
            MSVC version string
        """
        try:
            result = subprocess.run(
                ["cl.exe"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse version from output
            for line in result.stderr.split("\n"):
                if "Microsoft" in line and "C/C++" in line:
                    return line.strip()
            
            return "unknown"
        except Exception:
            return "unknown"
    
    def _get_gcc_version(self, gcc_path: str) -> str:
        """Get GCC version.
        
        Args:
            gcc_path: Path to GCC executable
            
        Returns:
            GCC version string
        """
        try:
            result = subprocess.run(
                [gcc_path, "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse version from output
            for line in result.stdout.split("\n"):
                if "gcc" in line.lower():
                    return line.strip()
            
            return "unknown"
        except Exception:
            return "unknown"
    
    def _get_clang_version(self, clang_path: str) -> str:
        """Get Clang version.
        
        Args:
            clang_path: Path to Clang executable
            
        Returns:
            Clang version string
        """
        try:
            result = subprocess.run(
                [clang_path, "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse version from output
            for line in result.stdout.split("\n"):
                if "clang" in line.lower():
                    return line.strip()
            
            return "unknown"
        except Exception:
            return "unknown"
    
    def detect_python_version(self) -> str:
        """Detect Python version.
        
        Returns:
            Python version string
        """
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def detect_cmake_version(self) -> str:
        """Detect CMake version.
        
        Returns:
            CMake version string
        """
        cmake_path = shutil.which("cmake")
        if not cmake_path:
            return "not found"
        
        try:
            result = subprocess.run(
                ["cmake", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse version from output
            for line in result.stdout.split("\n"):
                if "cmake" in line.lower():
                    return line.strip()
            
            return "unknown"
        except Exception:
            return "unknown"
    
    def get_platform_info(self) -> Dict[str, str]:
        """Get complete platform information.
        
        Returns:
            Dictionary with platform information
        """
        return {
            "os": self.detect_os(),
            "architecture": self.detect_architecture(),
            "python_version": self.detect_python_version(),
            "cmake_version": self.detect_cmake_version(),
            "system": self.system,
            "machine": self.machine,
        }
    
    def get_default_compiler(self) -> Optional[CompilerInfo]:
        """Get default compiler for current platform.
        
        Returns:
            Default compiler or None
        """
        compilers = self.detect_compilers()
        
        if not compilers:
            return None
        
        # Prefer MSVC on Windows, GCC on Linux
        if self.system == "Windows":
            for compiler in compilers:
                if compiler.type == "msvc":
                    return compiler
            # Fallback to MSVC-Clang
            for compiler in compilers:
                if compiler.type == "msvc-clang":
                    return compiler
        elif self.system == "Linux":
            for compiler in compilers:
                if compiler.type == "gcc":
                    return compiler
            # Fallback to Clang
            for compiler in compilers:
                if compiler.type == "clang":
                    return compiler
        
        return compilers[0]
