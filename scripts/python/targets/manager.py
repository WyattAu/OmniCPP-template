"""
Target manager for managing build targets
"""

from typing import Any, Dict, Optional

from .base import TargetBase
from .factory import TargetFactory


class TargetManager:
    """Manager for build targets.
    
    Provides centralized management of build targets including:
    - Target creation and lifecycle management
    - Target validation
    - Target configuration
    - Cross-compilation support
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize target manager.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self._current_target: Optional[TargetBase] = None
        self._targets: Dict[str, TargetBase] = {}
    
    def create_target(self, target_type: str) -> TargetBase:
        """Create and initialize a target.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Returns:
            Target instance
            
        Raises:
            ValueError: If target type is invalid
        """
        target = TargetFactory.create(target_type, self.config)
        self._targets[target_type] = target
        self._current_target = target
        return target
    
    def get_current_target(self) -> Optional[TargetBase]:
        """Get current active target.
        
        Returns:
            Current target or None if no target is active
        """
        return self._current_target
    
    def set_current_target(self, target_type: str) -> None:
        """Set current active target.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Raises:
            ValueError: If target type is invalid
        """
        if target_type not in self._targets:
            target = self.create_target(target_type)
        else:
            target = self._targets[target_type]
        
        self._current_target = target
    
    def validate_target(self, target_type: str) -> bool:
        """Validate target configuration.
        
        Args:
            target_type: Target type to validate
            
        Returns:
            True if target configuration is valid, False otherwise
        """
        if target_type not in self._targets:
            return False
        
        target = self._targets[target_type]
        return target.validate()
    
    def get_target_info(self, target_type: str) -> Dict[str, str]:
        """Get target information.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Returns:
            Dictionary with target information
            
        Raises:
            ValueError: If target type is invalid
        """
        return TargetFactory.get_target_info(target_type)
    
    def get_all_targets(self) -> list[str]:
        """Get all available target types.
        
        Returns:
            List of available target types
        """
        return TargetFactory.get_all_targets()
    
    def configure_current_target(self) -> None:
        """Configure current target with settings.
        
        Raises:
            ValueError: If no target is current
        """
        if not self._current_target:
            raise ValueError("No target is currently active")
        
        self._current_target.configure(self.config)
    
    def get_cmake_args(self, target_type: str) -> list[str]:
        """Get CMake arguments for target.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Returns:
            List of CMake arguments
            
        Raises:
            ValueError: If target type is invalid
        """
        if target_type not in self._targets:
            raise ValueError(f"Target '{target_type}' has not been created")
        
        target = self._targets[target_type]
        return target.get_cmake_args()
    
    def get_toolchain_file(self, target_type: str) -> Optional[str]:
        """Get toolchain file for target.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Returns:
            Path to toolchain file or None
            
        Raises:
            ValueError: If target type is invalid
        """
        if target_type not in self._targets:
            raise ValueError(f"Target '{target_type}' has not been created")
        
        target = self._targets[target_type]
        return target.get_toolchain_file()
    
    def supports_cross_compilation(self, target_type: str) -> bool:
        """Check if target supports cross-compilation.
        
        Args:
            target_type: Target type to check
            
        Returns:
            True if target supports cross-compilation, False otherwise
        """
        # All targets support cross-compilation
        return True
    
    def get_cross_compile_args(
            self,
            target_type: str,
            host_platform: str
        ) -> list[str]:
        """Get cross-compilation arguments.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            host_platform: Host platform (windows, linux)
            
        Returns:
            List of cross-compilation CMake arguments
        """
        args: list[str] = []
        
        # Add cross-compilation flags
        if target_type == "wasm":
            # WASM is always cross-compiled
            args.extend([
                "-DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/emscripten.cmake",
            ])
        elif host_platform == "windows" and target_type == "linux":
            # Cross-compiling from Windows to Linux
            args.extend([
                "-DCMAKE_SYSTEM_NAME=Linux",
                "-DCMAKE_CROSSCOMPILING=TRUE",
            ])
        elif host_platform == "linux" and target_type == "windows":
            # Cross-compiling from Linux to Windows
            args.extend([
                "-DCMAKE_SYSTEM_NAME=Windows",
                "-DCMAKE_CROSSCOMPILING=TRUE",
            ])
        
        return args
