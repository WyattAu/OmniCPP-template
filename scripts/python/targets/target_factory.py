"""
Target factory for creating target instances
"""

from typing import Any, Dict
from .target_base import TargetBase, TargetInfo
from .windows_target import WindowsTarget
from .linux_target import LinuxTarget
from .wasm_target import WasmTarget


class TargetFactory:
    """Factory for creating target instances"""
    
    @staticmethod
    def create(target_type: str, config: Dict[str, Any]) -> TargetBase:
        """Create target instance"""
        if target_type == "windows":
            return WindowsTarget(config)
        elif target_type == "linux":
            return LinuxTarget(config)
        elif target_type == "wasm":
            return WasmTarget(config)
        else:
            raise ValueError(f"Unknown target type: {target_type}")
    
    @staticmethod
    def get_all_targets() -> list[str]:
        """Get all available target types"""
        return ["windows", "linux", "wasm"]
