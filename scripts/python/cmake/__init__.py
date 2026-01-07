"""
CMake integration and management

This package provides comprehensive CMake integration including:
- CMake command execution and wrapping
- CMake cache variable management
- CMake presets file generation and management
- CMake toolchain file generation and management
- CMake generator selection
"""

from cmake.cmake_wrapper import CMakeWrapper
from cmake.cache_manager import CacheManager
from cmake.presets_manager import PresetsManager, PresetInfo
from cmake.toolchain_manager import ToolchainManager
from cmake.generator_selector import GeneratorSelector

__all__ = [
    "CMakeWrapper",
    "CacheManager",
    "PresetsManager",
    "PresetInfo",
    "ToolchainManager",
    "GeneratorSelector"
]
