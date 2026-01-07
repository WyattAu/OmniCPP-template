"""
MinGW-GCC compiler detection and configuration
"""

import os
import re
import platform
from typing import Any
from .base import CompilerBase, CompilerInfo


class MinWGGCCCompiler(CompilerBase):
    """MinGW-GCC compiler detection and configuration"""
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize MinGW-GCC compiler
        
        Args:
            version: GCC version (auto-detect if None)
        """
        super().__init__(version)
        self._gcc_path: str | None = None
        self._mingw_path: str | None = None
    
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        return "MinGW-GCC"
    
    def get_version(self) -> str:
        """Get compiler version
        
        Returns:
            Compiler version string
        """
        if self._detected_version:
            return self._detected_version
        
        if self._version:
            return self._version
        
        # Auto-detect version
        version_info = self._detect_gcc_version()
        if version_info:
            self._detected_version = version_info
            return version_info
        
        return "unknown"
    
    def get_flags(self, build_type: str) -> list[str]:
        """Get compiler flags
        
        Args:
            build_type: Build type (Debug, Release, RelWithDebInfo, MinSizeRel)
            
        Returns:
            List of compiler flags
        """
        flags: list[str] = []
        
        # Standard flags
        flags.extend([
            "-std=c++23",
            "-fno-exceptions",
            "-fcxx-exceptions"
        ])
        
        # Build type specific flags
        build_type_lower = build_type.lower()
        if build_type_lower == "debug":
            flags.extend([
                "-O0",
                "-g",
                "-D_DEBUG"
            ])
        elif build_type_lower == "release":
            flags.extend([
                "-O3",
                "-DNDEBUG",
                "-flto"
            ])
        elif build_type_lower == "relwithdebinfo":
            flags.extend([
                "-O2",
                "-g",
                "-DNDEBUG"
            ])
        elif build_type_lower == "minsizerel":
            flags.extend([
                "-Os",
                "-DNDEBUG",
                "-flto"
            ])
        
        # Warning flags
        flags.extend([
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unused-parameter",
            "-Wno-missing-field-initializers"
        ])
        
        return flags
    
    def setup_environment(self) -> dict[str, str]:
        """Set up MinGW-GCC environment
        
        Returns:
            Dictionary of environment variables
        """
        env: dict[str, str] = {}
        
        if platform.system() != "Windows":
            return env
        
        # Find MinGW installation
        mingw_path = self._find_mingw_installation()
        if not mingw_path:
            return env
        
        self._mingw_path = mingw_path
        
        # Set up environment variables
        bin_path = os.path.join(mingw_path, "bin")
        env.update({
            "MINGW_HOME": mingw_path,
            "PATH": f"{bin_path};{env.get('PATH', os.environ.get('PATH', ''))}"
        })
        
        return env
    
    def _detect_compiler(self) -> bool:
        """Internal method to detect MinGW-GCC compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        if platform.system() != "Windows":
            return False
        
        # Check for g++.exe
        gcc_path = self._find_gcc_exe()
        if not gcc_path:
            return False
        
        self._gcc_path = gcc_path
        
        # Verify it works
        exit_code, stdout, stderr = self._run_command([gcc_path, "--version"])
        return exit_code == 0 and ("gcc" in stdout or "gcc" in stderr)
    
    def _find_gcc_exe(self) -> str | None:
        """Find g++.exe compiler
        
        Returns:
            Path to g++.exe or None if not found
        """
        # Check PATH first
        exit_code, stdout, _ = self._run_command(["where", "g++.exe"])
        if exit_code == 0 and stdout.strip():
            return stdout.strip().split("\n")[0]
        
        # Search in common locations
        mingw_paths = self._get_common_mingw_paths()
        
        for mingw_path in mingw_paths:
            gcc_path = os.path.join(mingw_path, "bin", "g++.exe")
            if os.path.exists(gcc_path):
                return gcc_path
        
        return None
    
    def _find_mingw_installation(self) -> str | None:
        """Find MinGW installation path
        
        Returns:
            Installation path or None if not found
        """
        # Check environment variables
        mingw_home = os.environ.get("MINGW_HOME")
        if mingw_home and os.path.exists(mingw_home):
            return mingw_home
        
        # Search in common locations
        mingw_paths = self._get_common_mingw_paths()
        
        for path in mingw_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _get_common_mingw_paths(self) -> list[str]:
        """Get common MinGW installation paths
        
        Returns:
            List of common MinGW paths
        """
        paths: list[str] = []
        
        # Common installation locations
        common_locations = [
            "C:/mingw64",
            "C:/mingw",
            "C:/msys64/mingw64",
            "C:/msys64/usr",
            os.path.join(os.environ.get("ProgramFiles", ""), "mingw-w64"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "mingw-w64"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "mingw64")
        ]
        
        for location in common_locations:
            if os.path.exists(location):
                paths.append(location)
        
        return paths
    
    def _detect_gcc_version(self) -> str | None:
        """Detect GCC version
        
        Returns:
            Version string or None if not detected
        """
        gcc_path = self._find_gcc_exe()
        if not gcc_path:
            return None
        
        # Run g++.exe to get version
        exit_code, stdout, stderr = self._run_command([gcc_path, "--version"])
        output = stdout + stderr
        
        # Parse version from output
        # Example: "g++.exe (Rev2, Built by MSYS2 project) 13.2.0"
        match = re.search(r"g\+\+.*?(\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
        
        return None
