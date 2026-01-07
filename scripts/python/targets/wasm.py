"""
WebAssembly (WASM) build target implementation
"""

import os
from typing import Any, Optional

from .base import TargetBase


class WasmTarget(TargetBase):
    """WebAssembly-specific build target.
    
    Handles WASM platform-specific build configuration including:
    - Emscripten compiler support
    - WASM-specific CMake generators
    - Browser environment handling
    - WASM limitations and fallbacks
    """
    
    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize WASM target.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self._architecture: str = "wasm32"
    
    def get_name(self) -> str:
        """Get target name.
        
        Returns:
            Target name 'wasm'
        """
        return "wasm"
    
    def get_platform(self) -> str:
        """Get target platform.
        
        Returns:
            Platform name 'wasm'
        """
        return "wasm"
    
    def get_architecture(self) -> str:
        """Get target architecture.
        
        Returns:
            Architecture name (wasm32)
        """
        return self._architecture
    
    def configure(self, config: dict[str, Any]) -> None:
        """Configure WASM target with build settings.
        
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
        
        # Validate Emscripten if specified
        if "emscripten_path" in config:
            emscripten_path = config["emscripten_path"]
            
            if not os.path.exists(emscripten_path):
                raise ValueError(
                    f"Emscripten path '{emscripten_path}' does not exist"
                )
    
    def validate(self) -> bool:
        """Validate WASM target configuration.
        
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
        
        # Validate Emscripten path if specified
        if "emscripten_path" in self.config:
            emscripten_path = self.config["emscripten_path"]
            
            if not os.path.exists(emscripten_path):
                return False
        
        return True
    
    def get_cmake_args(self) -> list[str]:
        """Get CMake arguments for WASM target.
        
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add build type
        build_type = self.config.get("build_type", "Release")
        args.append(f"-DCMAKE_BUILD_TYPE={build_type}")
        
        # Add platform-specific flags
        args.append("-DCMAKE_SYSTEM_NAME=Emscripten")
        args.append("-DCMAKE_SYSTEM_PROCESSOR=WASM")
        
        # Add WASM-specific flags
        args.extend([
            "-DCMAKE_C_COMPILER=emcc",
            "-DCMAKE_CXX_COMPILER=em++",
        ])
        
        # Add Emscripten-specific flags
        args.extend([
            "-DEMSCRIPTEN",
            "-DUSE_SDL=2",
        ])
        
        return args
    
    def get_toolchain_file(self) -> Optional[str]:
        """Get toolchain file path for WASM target.
        
        Returns:
            Path to toolchain file
        """
        return "cmake/toolchains/emscripten.cmake"
