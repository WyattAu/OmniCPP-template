"""
Windows build target implementation
"""

import platform as sys_platform
from typing import Any, Optional

from .base import TargetBase


class WindowsTarget(TargetBase):
    """Windows-specific build target.
    
    Handles Windows platform-specific build configuration including:
    - MSVC and MinGW compiler support
    - Windows-specific CMake generators
    - Windows path handling
    - Windows registry operations
    """
    
    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize Windows target.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self._architecture: str = self._detect_architecture()
    
    def get_name(self) -> str:
        """Get target name.
        
        Returns:
            Target name 'windows'
        """
        return "windows"
    
    def get_platform(self) -> str:
        """Get target platform.
        
        Returns:
            Platform name 'windows'
        """
        return "windows"
    
    def get_architecture(self) -> str:
        """Get target architecture.
        
        Returns:
            Architecture name (x64, arm64)
        """
        return self._architecture
    
    def configure(self, config: dict[str, Any]) -> None:
        """Configure Windows target with build settings.
        
        Args:
            config: Configuration dictionary containing build settings
            
        Raises:
            ValueError: If configuration is invalid
        """
        self.config = config
        
        # Validate required configuration
        if "build_type" not in config:
            raise ValueError("build_type is required in configuration")
        
        build_type = config["build_type"]
        valid_build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]
        
        if build_type not in valid_build_types:
            raise ValueError(
                f"Invalid build_type '{build_type}'. "
                f"Must be one of: {', '.join(valid_build_types)}"
            )
        
        # Validate compiler if specified
        if "compiler" in config:
            compiler = config["compiler"]
            valid_compilers = ["msvc", "msvc-clang", "mingw-gcc", "mingw-clang"]
            
            if compiler not in valid_compilers:
                raise ValueError(
                    f"Invalid compiler '{compiler}'. "
                    f"Must be one of: {', '.join(valid_compilers)}"
                )
    
    def validate(self) -> bool:
        """Validate Windows target configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.config:
            return False
        
        # Check required fields
        required_fields = ["build_type"]
        for field in required_fields:
            if field not in self.config:
                return False
        
        # Validate build type
        build_type = self.config.get("build_type", "")
        valid_build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]
        
        if build_type not in valid_build_types:
            return False
        
        # Validate compiler if specified
        if "compiler" in self.config:
            compiler = self.config["compiler"]
            valid_compilers = ["auto", "msvc", "msvc-clang", "mingw-gcc", "mingw-clang"]
            
            if compiler not in valid_compilers:
                return False
        
        return True
    
    def get_cmake_args(self) -> list[str]:
        """Get CMake arguments for Windows target.
        
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add build type
        build_type = self.config.get("build_type", "Release")
        args.append(f"-DCMAKE_BUILD_TYPE={build_type}")
        
        # Add platform-specific flags
        args.append("-DCMAKE_SYSTEM_NAME=Windows")
        
        # Add architecture-specific flags
        if self._architecture == "arm64":
            args.append("-AARM64")
        else:
            args.append("-Ax64")
        
        # Add compiler-specific flags
        compiler = self.config.get("compiler", "auto")
        
        if compiler == "msvc":
            args.extend([
                "-DCMAKE_C_COMPILER=cl",
                "-DCMAKE_CXX_COMPILER=cl",
            ])
        elif compiler == "msvc-clang":
            args.extend([
                "-DCMAKE_C_COMPILER=clang-cl",
                "-DCMAKE_CXX_COMPILER=clang-cl",
            ])
        elif compiler == "mingw-gcc":
            args.extend([
                "-DCMAKE_C_COMPILER=gcc",
                "-DCMAKE_CXX_COMPILER=g++",
            ])
        elif compiler == "mingw-clang":
            args.extend([
                "-DCMAKE_C_COMPILER=clang",
                "-DCMAKE_CXX_COMPILER=clang++",
            ])
        
        return args
    
    def get_toolchain_file(self) -> Optional[str]:
        """Get toolchain file path for Windows target.
        
        Returns:
            Path to toolchain file or None if not applicable
        """
        compiler = self.config.get("compiler", "auto")
        
        # Return toolchain file for MinGW compilers
        if compiler in ["mingw-gcc", "mingw-clang"]:
            if self._architecture == "arm64":
                return "cmake/toolchains/arm64-windows-msvc.cmake"
            else:
                return "cmake/toolchains/x86-windows-msvc.cmake"
        
        # MSVC compilers don't need explicit toolchain file
        return None
    
    def _detect_architecture(self) -> str:
        """Detect system architecture.
        
        Returns:
            Architecture name (x64, arm64)
        """
        machine = sys_platform.machine().lower()
        
        if "arm64" in machine or "aarch64" in machine:
            return "arm64"
        elif "amd64" in machine or "x86_64" in machine:
            return "x64"
        else:
            # Default to x64 for Windows
            return "x64"
