"""
Base build target interface
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class TargetBase(ABC):
    """Abstract base class for build targets.
    
    Provides a unified interface for platform-specific build targets
    including Windows, Linux, and WebAssembly (WASM).
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Get target name.
        
        Returns:
            Target name (e.g., 'windows', 'linux', 'wasm')
        """
        pass
    
    @abstractmethod
    def get_platform(self) -> str:
        """Get target platform.
        
        Returns:
            Platform name (windows, linux, wasm)
        """
        pass
    
    @abstractmethod
    def get_architecture(self) -> str:
        """Get target architecture.
        
        Returns:
            Architecture name (x64, arm64)
        """
        pass
    
    @abstractmethod
    def configure(self, config: dict[str, Any]) -> None:
        """Configure target with build settings.
        
        Args:
            config: Configuration dictionary containing build settings
            
        Raises:
            ValueError: If configuration is invalid
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate target configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_cmake_args(self) -> list[str]:
        """Get CMake arguments for this target.
        
        Returns:
            List of CMake arguments
        """
        pass
    
    @abstractmethod
    def get_toolchain_file(self) -> Optional[str]:
        """Get toolchain file path for this target.
        
        Returns:
            Path to toolchain file or None if not applicable
        """
        pass
