"""
Linux build target implementation
"""

import platform as sys_platform
from typing import Any, Optional

from .base import TargetBase


class LinuxTarget(TargetBase):
    """Linux-specific build target.
    
    Handles Linux platform-specific build configuration including:
    - GCC and Clang compiler support
    - Linux-specific CMake generators
    - Linux path handling
    - Linux permissions handling
    """
    
    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize Linux target.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self._architecture: str = self._detect_architecture()
    
    def get_name(self) -> str:
        """Get target name.
        
        Returns:
            Target name 'linux'
        """
        return "linux"
    
    def get_platform(self) -> str:
        """Get target platform.
        
        Returns:
            Platform name 'linux'
        """
        return "linux"
    
    def get_architecture(self) -> str:
        """Get target architecture.
        
        Returns:
            Architecture name (x64, arm64)
        """
        return self._architecture
    
    def configure(self, config: dict[str, Any]) -> None:
        """Configure Linux target with build settings.
        
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
            valid_compilers = ["gcc", "clang"]
            
            if compiler not in valid_compilers:
                raise ValueError(
                    f"Invalid compiler '{compiler}'. "
                    f"Must be one of: {', '.join(valid_compilers)}"
                )
    
    def validate(self) -> bool:
        """Validate Linux target configuration.
        
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
            valid_compilers = ["auto", "gcc", "clang"]
            
            if compiler not in valid_compilers:
                return False
        
        return True
    
    def get_cmake_args(self) -> list[str]:
        """Get CMake arguments for Linux target.
        
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add build type
        build_type = self.config.get("build_type", "Release")
        args.append(f"-DCMAKE_BUILD_TYPE={build_type}")
        
        # Add platform-specific flags
        args.append("-DCMAKE_SYSTEM_NAME=Linux")
        
        # Add architecture-specific flags
        if self._architecture == "arm64":
            args.append("-AARCH64")
        else:
            args.append("-Ax64")
        
        # Add compiler-specific flags
        compiler: str = self.config.get("compiler", "auto")
        
        if compiler == "gcc":
            args.extend([
                "-DCMAKE_C_COMPILER=gcc",
                "-DCMAKE_CXX_COMPILER=g++",
            ])
        elif compiler == "clang":
            args.extend([
                "-DCMAKE_C_COMPILER=clang",
                "-DCMAKE_CXX_COMPILER=clang++",
            ])
        else:
            # Auto-detect compiler (default to gcc for Linux)
            args.extend([
                "-DCMAKE_C_COMPILER=gcc",
                "-DCMAKE_CXX_COMPILER=g++",
            ])
        
        return args
    
    def get_toolchain_file(self) -> Optional[str]:
        """Get toolchain file path for Linux target.
        
        Returns:
            Path to toolchain file or None if not applicable
        """
        compiler = self.config.get("compiler", "auto")
        
        # Return toolchain file for specific architectures
        if self._architecture == "arm64":
            return "cmake/toolchains/arm64-linux-gnu.cmake"
        else:
            return "cmake/toolchains/x86-linux-gnu.cmake"
    
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
            # Default to x64 for Linux
            return "x64"
