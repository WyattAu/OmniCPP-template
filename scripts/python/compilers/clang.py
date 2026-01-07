"""
Clang compiler detection and configuration
"""

import os
import re
import platform
import shutil
from typing import Any
from .base import CompilerBase, CompilerInfo


class ClangCompiler(CompilerBase):
    """Clang compiler detection and configuration"""
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize Clang compiler
        
        Args:
            version: Clang version (auto-detect if None)
        """
        super().__init__(version)
        self._clang_path: str | None = None
    
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        return "Clang"
    
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
        version_info = self._detect_clang_version()
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
        """Set up Clang environment
        
        Returns:
            Dictionary of environment variables
        """
        env: dict[str, str] = {}
        
        if platform.system() != "Linux":
            return env
        
        # Find Clang installation
        clang_path = self._find_clang_exe()
        if not clang_path:
            return env
        
        self._clang_path = clang_path
        
        # Set up environment variables
        clang_dir = os.path.dirname(clang_path)
        env.update({
            "CC": clang_path,
            "CXX": clang_path.replace("clang", "clang++"),
            "PATH": f"{clang_dir}:{env.get('PATH', os.environ.get('PATH', ''))}"
        })
        
        return env
    
    def _detect_compiler(self) -> bool:
        """Internal method to detect Clang compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        if platform.system() != "Linux":
            return False
        
        # Check for clang++
        clang_path = self._find_clang_exe()
        if not clang_path:
            return False
        
        self._clang_path = clang_path
        
        # Verify it works
        exit_code, stdout, stderr = self._run_command([clang_path, "--version"])
        return exit_code == 0 and ("clang" in stdout or "clang" in stderr)
    
    def _find_clang_exe(self) -> str | None:
        """Find clang++ compiler
        
        Returns:
            Path to clang++ or None if not found
        """
        # Use shutil.which to find clang++
        clang_path = shutil.which("clang++")
        if clang_path:
            return clang_path
        
        # Check common locations
        common_paths = [
            "/usr/bin/clang++",
            "/usr/local/bin/clang++",
            "/opt/llvm/bin/clang++"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _detect_clang_version(self) -> str | None:
        """Detect Clang version
        
        Returns:
            Version string or None if not detected
        """
        clang_path = self._find_clang_exe()
        if not clang_path:
            return None
        
        # Run clang++ to get version
        exit_code, stdout, stderr = self._run_command([clang_path, "--version"])
        output = stdout + stderr
        
        # Parse version from output
        # Example: "clang version 18.1.0"
        match = re.search(r"clang version (\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
        
        return None
