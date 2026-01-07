"""
GCC compiler detection and configuration
"""

import os
import re
import platform
import shutil
from typing import Any
from .base import CompilerBase, CompilerInfo


class GCCCompiler(CompilerBase):
    """GCC compiler detection and configuration"""
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize GCC compiler
        
        Args:
            version: GCC version (auto-detect if None)
        """
        super().__init__(version)
        self._gcc_path: str | None = None
    
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        return "GCC"
    
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
            "-fcxx-exceptions",
            "-fPIC"
        ])
        
        # Build type specific flags
        build_type_lower = build_type.lower()
        if build_type_lower == "debug":
            flags.extend([
                "-O0",
                "-g",
                "-D_DEBUG",
                "-fno-omit-frame-pointer"
            ])
        elif build_type_lower == "release":
            flags.extend([
                "-O3",
                "-DNDEBUG",
                "-flto",
                "-fomit-frame-pointer"
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
                "-flto",
                "-fomit-frame-pointer"
            ])
        
        # Warning flags
        flags.extend([
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unused-parameter",
            "-Wno-missing-field-initializers",
            "-Wpedantic"
        ])
        
        return flags
    
    def setup_environment(self) -> dict[str, str]:
        """Set up GCC environment
        
        Returns:
            Dictionary of environment variables
        """
        env: dict[str, str] = {}
        
        if platform.system() != "Linux":
            return env
        
        # Find GCC installation
        gcc_path = self._find_gcc_exe()
        if not gcc_path:
            return env
        
        self._gcc_path = gcc_path
        
        # Set up environment variables
        gcc_dir = os.path.dirname(gcc_path)
        env.update({
            "CC": gcc_path,
            "CXX": gcc_path.replace("gcc", "g++"),
            "PATH": f"{gcc_dir}:{env.get('PATH', os.environ.get('PATH', ''))}"
        })
        
        return env
    
    def _detect_compiler(self) -> bool:
        """Internal method to detect GCC compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        if platform.system() != "Linux":
            return False
        
        # Check for g++
        gcc_path = self._find_gcc_exe()
        if not gcc_path:
            return False
        
        self._gcc_path = gcc_path
        
        # Verify it works
        exit_code, stdout, stderr = self._run_command([gcc_path, "--version"])
        return exit_code == 0 and ("gcc" in stdout or "gcc" in stderr)
    
    def _find_gcc_exe(self) -> str | None:
        """Find g++ compiler
        
        Returns:
            Path to g++ or None if not found
        """
        # Use shutil.which to find g++
        gcc_path = shutil.which("g++")
        if gcc_path:
            return gcc_path
        
        # Check common locations
        common_paths = [
            "/usr/bin/g++",
            "/usr/local/bin/g++",
            "/opt/gcc/bin/g++"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _detect_gcc_version(self) -> str | None:
        """Detect GCC version
        
        Returns:
            Version string or None if not detected
        """
        gcc_path = self._find_gcc_exe()
        if not gcc_path:
            return None
        
        # Run g++ to get version
        exit_code, stdout, stderr = self._run_command([gcc_path, "--version"])
        output = stdout + stderr
        
        # Parse version from output
        # Example: "g++ (Ubuntu 13.2.0-23ubuntu4) 13.2.0"
        match = re.search(r"g\+\+.*?(\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
        
        return None
