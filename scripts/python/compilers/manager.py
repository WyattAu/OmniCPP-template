"""
Compiler manager for managing compiler detection and selection
"""

import platform
from typing import Any
from .base import CompilerBase, CompilerInfo
from .factory import CompilerFactory


class CompilerManager:
    """Manager for compiler detection and selection"""
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize compiler manager
        
        Args:
            config: Configuration dictionary
        """
        self.config: dict[str, Any] = config or {}
        self._available_compilers: list[CompilerInfo] = []
        self._selected_compiler: CompilerBase | None = None
    
    def detect_compilers(self) -> list[CompilerInfo]:
        """Detect all available compilers
        
        Returns:
            List of available compilers
        """
        self._available_compilers = CompilerFactory.detect_available()
        return self._available_compilers
    
    def get_available_compilers(self) -> list[CompilerInfo]:
        """Get list of available compilers
        
        Returns:
            List of available compilers
        """
        if not self._available_compilers:
            self.detect_compilers()
        return self._available_compilers
    
    def select_compiler(self, compiler_type: str, version: str | None = None) -> CompilerBase:
        """Select a compiler
        
        Args:
            compiler_type: Compiler type (msvc, msvc-clang, mingw-gcc, mingw-clang, gcc, clang)
            version: Compiler version (auto-detect if None)
            
        Returns:
            Selected compiler instance
            
        Raises:
            ValueError: If compiler type is invalid or not available
        """
        # Validate compiler type
        available_types = [info.name.lower() for info in self._available_compilers]
        
        # Map compiler type to name
        type_to_name = {
            "msvc": "msvc",
            "msvc-clang": "msvc-clang",
            "mingw-gcc": "mingw-gcc",
            "mingw-clang": "mingw-clang",
            "gcc": "gcc",
            "clang": "clang"
        }
        
        compiler_name = type_to_name.get(compiler_type.lower())
        if not compiler_name:
            raise ValueError(f"Unknown compiler type: {compiler_type}")
        
        # Check if compiler is available
        if compiler_name not in available_types:
            raise ValueError(f"Compiler {compiler_name} is not available")
        
        # Create compiler instance
        self._selected_compiler = CompilerFactory.create(compiler_type, version)
        return self._selected_compiler
    
    def get_selected_compiler(self) -> CompilerBase | None:
        """Get currently selected compiler
        
        Returns:
            Selected compiler instance or None if none selected
        """
        return self._selected_compiler
    
    def get_default_compiler(self) -> CompilerBase | None:
        """Get default compiler for current platform
        
        Returns:
            Default compiler instance or None if not found
        """
        self._selected_compiler = CompilerFactory.get_default_compiler()
        return self._selected_compiler
    
    def get_compiler_info(self, compiler_type: str) -> CompilerInfo | None:
        """Get information about a specific compiler
        
        Args:
            compiler_type: Compiler type
            
        Returns:
            Compiler information or None if not found
        """
        for info in self._available_compilers:
            if info.name.lower() == compiler_type.lower():
                return info
        return None
    
    def is_compiler_available(self, compiler_type: str) -> bool:
        """Check if a compiler is available
        
        Args:
            compiler_type: Compiler type
            
        Returns:
            True if compiler is available, False otherwise
        """
        return self.get_compiler_info(compiler_type) is not None
    
    def get_platform(self) -> str:
        """Get current platform
        
        Returns:
            Platform name (windows, linux, wasm)
        """
        return platform.system().lower()
    
    def get_architecture(self) -> str:
        """Get current architecture
        
        Returns:
            Architecture name (x64, arm64)
        """
        machine = platform.machine().lower()
        
        if machine in ["x86_64", "amd64"]:
            return "x64"
        elif machine in ["arm64", "aarch64"]:
            return "arm64"
        elif machine in ["i386", "i686"]:
            return "x86"
        else:
            return machine
    
    def get_recommended_compiler(self) -> str:
        """Get recommended compiler for current platform
        
        Returns:
            Recommended compiler type
        """
        current_platform = self.get_platform()
        
        if current_platform == "windows":
            # Prefer MSVC on Windows
            if self.is_compiler_available("msvc"):
                return "msvc"
            elif self.is_compiler_available("msvc-clang"):
                return "msvc-clang"
            elif self.is_compiler_available("mingw-gcc"):
                return "mingw-gcc"
            elif self.is_compiler_available("mingw-clang"):
                return "mingw-clang"
        
        elif current_platform == "linux":
            # Prefer GCC on Linux
            if self.is_compiler_available("gcc"):
                return "gcc"
            elif self.is_compiler_available("clang"):
                return "clang"
        
        return "unknown"
    
    def get_compiler_flags(self, build_type: str = "Release") -> list[str]:
        """Get flags for selected compiler
        
        Args:
            build_type: Build type (Debug, Release, RelWithDebInfo, MinSizeRel)
            
        Returns:
            List of compiler flags
            
        Raises:
            RuntimeError: If no compiler is selected
        """
        if not self._selected_compiler:
            raise RuntimeError("No compiler selected")
        
        return self._selected_compiler.get_flags(build_type)
    
    def setup_compiler_environment(self) -> dict[str, str]:
        """Set up environment for selected compiler
        
        Returns:
            Dictionary of environment variables
            
        Raises:
            RuntimeError: If no compiler is selected
        """
        if not self._selected_compiler:
            raise RuntimeError("No compiler selected")
        
        return self._selected_compiler.setup_environment()
    
    def get_compiler_summary(self) -> dict[str, Any]:
        """Get summary of compiler status
        
        Returns:
            Dictionary with compiler status information
        """
        return {
            "platform": self.get_platform(),
            "architecture": self.get_architecture(),
            "available_compilers": [
                {
                    "name": info.name,
                    "version": info.version,
                    "path": info.path,
                    "target": info.target
                }
                for info in self._available_compilers
            ],
            "selected_compiler": (
                {
                    "name": self._selected_compiler.get_name(),
                    "version": self._selected_compiler.get_version()
                }
                if self._selected_compiler
                else None
            ),
            "recommended_compiler": self.get_recommended_compiler()
        }
