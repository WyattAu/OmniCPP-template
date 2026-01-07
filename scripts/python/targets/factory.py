"""
Target factory for creating target instances
"""

from typing import Any, Dict

from .base import TargetBase
from .windows import WindowsTarget
from .linux import LinuxTarget
from .wasm import WasmTarget


class TargetFactory:
    """Factory for creating target instances.
    
    Provides a centralized way to create target instances
    based on target type (windows, linux, wasm).
    """
    
    @staticmethod
    def create(target_type: str, config: Dict[str, Any]) -> TargetBase:
        """Create target instance.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            config: Configuration dictionary containing build settings
            
        Returns:
            Target instance
            
        Raises:
            ValueError: If target type is invalid
        """
        target_type_lower = target_type.lower()
        
        if target_type_lower == "windows":
            return WindowsTarget(config)
        elif target_type_lower == "linux":
            return LinuxTarget(config)
        elif target_type_lower == "wasm":
            return WasmTarget(config)
        else:
            raise ValueError(
                f"Unknown target type: {target_type}. "
                f"Must be one of: windows, linux, wasm"
            )
    
    @staticmethod
    def get_all_targets() -> list[str]:
        """Get all available target types.
        
        Returns:
            List of available target types
        """
        return ["windows", "linux", "wasm"]
    
    @staticmethod
    def get_target_info(target_type: str) -> Dict[str, str]:
        """Get target information without creating instance.
        
        Args:
            target_type: Target type (windows, linux, wasm)
            
        Returns:
            Dictionary with target information
            
        Raises:
            ValueError: If target type is invalid
        """
        target_info: Dict[str, Dict[str, str]] = {
            "windows": {
                "name": "windows",
                "platform": "windows",
                "architecture": "x64",
                "description": "Windows platform with MSVC/MinGW support",
            },
            "linux": {
                "name": "linux",
                "platform": "linux",
                "architecture": "x64",
                "description": "Linux platform with GCC/Clang support",
            },
            "wasm": {
                "name": "wasm",
                "platform": "wasm",
                "architecture": "wasm32",
                "description": "WebAssembly platform with Emscripten",
            },
        }
        
        target_type_lower = target_type.lower()
        
        if target_type_lower in target_info:
            return target_info[target_type_lower]
        
        raise ValueError(
            f"Unknown target type: {target_type}. "
            f"Must be one of: {', '.join(target_info.keys())}"
        )
