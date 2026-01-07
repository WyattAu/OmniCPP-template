"""
CMake generator selection logic

This module provides intelligent CMake generator selection based on
platform, compiler, and build configuration with proper validation.
"""

from typing import Optional, Union

from core.exception_handler import ConfigurationError
from core.logger import Logger


class GeneratorSelector:
    """Select appropriate CMake generator based on platform and compiler.
    
    This class provides methods for selecting the appropriate CMake generator
    for different platforms, compilers, and build configurations with
    proper validation and error handling.
    """
    
    # Generator mappings for different platforms and compilers
    GENERATOR_MAP = {
        # Windows generators
        "windows-msvc": ["Visual Studio 17 2022", "Visual Studio 16 2019", "Visual Studio 15 2017"],
        "windows-msvc-clang": ["Ninja", "Ninja Multi-Config"],
        "windows-mingw-gcc": ["Ninja", "MinGW Makefiles", "Unix Makefiles"],
        "windows-mingw-clang": ["Ninja", "MinGW Makefiles", "Unix Makefiles"],
        
        # Linux generators
        "linux-gcc": ["Ninja", "Unix Makefiles"],
        "linux-clang": ["Ninja", "Unix Makefiles"],
        
        # WASM generators
        "wasm-emscripten": ["Ninja", "Unix Makefiles"]
    }
    
    # Preferred generators (in order of preference)
    PREFERRED_GENERATORS = ["Ninja", "Ninja Multi-Config", "Unix Makefiles"]
    
    def __init__(self, logger: Optional[Logger] = None) -> None:
        """Initialize generator selector.
        
        Args:
            logger: Logger instance for logging operations
        """
        self.logger = logger or Logger("GeneratorSelector", {
            "level": "INFO",
            "console_handler_enabled": True,
            "file_handler_enabled": False
        })
        
        self.logger.info("Generator selector initialized")
    
    def select(
        self,
        platform: str,
        compiler: str,
        multi_config: bool = False
    ) -> str:
        """Select CMake generator for platform and compiler.
        
        Args:
            platform: Target platform (windows, linux, wasm)
            compiler: Compiler type (msvc, gcc, clang, etc.)
            multi_config: Whether to use multi-config generator
            
        Returns:
            Selected CMake generator name
            
        Raises:
            ConfigurationError: If platform/compiler combination is invalid
        """
        # Build platform-compiler key
        key = f"{platform}-{compiler}"
        
        # Get available generators for this combination
        available_generators = self.GENERATOR_MAP.get(key)
        
        if not available_generators:
            raise ConfigurationError(
                f"No generators available for platform '{platform}' with compiler '{compiler}'",
                {"platform": platform, "compiler": compiler}
            )
        
        # Select preferred generator
        selected_generator = self._select_preferred_generator(
            available_generators,
            multi_config
        )
        
        self.logger.info(
            f"Selected generator '{selected_generator}' for {key}"
        )
        
        return selected_generator
    
    def _select_preferred_generator(
        self,
        available_generators: list[str],
        multi_config: bool
    ) -> str:
        """Select preferred generator from available options.
        
        Args:
            available_generators: List of available generators
            multi_config: Whether to use multi-config generator
            
        Returns:
            Selected generator name
        """
        # If multi-config is requested, prefer Ninja Multi-Config
        if multi_config and "Ninja Multi-Config" in available_generators:
            return "Ninja Multi-Config"
        
        # Otherwise, select from preferred generators
        for preferred in self.PREFERRED_GENERATORS:
            if preferred in available_generators:
                return preferred
        
        # Return first available generator if no preferred found
        return available_generators[0]
    
    def get_available_generators(
        self,
        platform: Optional[str] = None,
        compiler: Optional[str] = None
    ) -> list[str]:
        """Get available CMake generators.
        
        Args:
            platform: Optional platform filter
            compiler: Optional compiler filter
            
        Returns:
            List of available generator names
        """
        if platform and compiler:
            # Get generators for specific platform/compiler combination
            key = f"{platform}-{compiler}"
            return self.GENERATOR_MAP.get(key, []).copy()
        elif platform:
            # Get all generators for platform
            generators: list[str] = []
            for key, gens in self.GENERATOR_MAP.items():
                if key.startswith(f"{platform}-"):
                    generators.extend(gens)
            return list(set(generators))
        elif compiler:
            # Get all generators for compiler
            generators: list[str] = []
            for key, gens in self.GENERATOR_MAP.items():
                if key.endswith(f"-{compiler}"):
                    generators.extend(gens)
            return list(set(generators))
        else:
            # Get all generators
            generators: list[str] = []
            for gens in self.GENERATOR_MAP.values():
                generators.extend(gens)
            return list(set(generators))
    
    def is_multi_config_generator(self, generator: str) -> bool:
        """Check if generator supports multiple configurations.
        
        Args:
            generator: Generator name to check
            
        Returns:
            True if generator is multi-config, False otherwise
        """
        multi_config_generators = [
            "Visual Studio",
            "Xcode",
            "Ninja Multi-Config"
        ]
        
        return any(mcg in generator for mcg in multi_config_generators)
    
    def is_single_config_generator(self, generator: str) -> bool:
        """Check if generator supports single configuration.
        
        Args:
            generator: Generator name to check
            
        Returns:
            True if generator is single-config, False otherwise
        """
        return not self.is_multi_config_generator(generator)
    
    def validate_generator(self, generator: str) -> bool:
        """Validate generator name.
        
        Args:
            generator: Generator name to validate
            
        Returns:
            True if generator is valid, False otherwise
        """
        # Check against known generators
        all_generators = self.get_available_generators()
        return generator in all_generators
    
    def get_generator_info(self, generator: str) -> dict[str, Union[bool, str]]:
        """Get information about a generator.
        
        Args:
            generator: Generator name
            
        Returns:
            Dictionary with generator information
        """
        return {
            "name": generator,
            "multi_config": self.is_multi_config_generator(generator),
            "single_config": self.is_single_config_generator(generator),
            "valid": self.validate_generator(generator)
        }
    
    def recommend_generator(
        self,
        platform: str,
        compiler: str,
        build_type: Optional[str] = None
    ) -> str:
        """Recommend generator based on platform, compiler, and build type.
        
        Args:
            platform: Target platform
            compiler: Compiler type
            build_type: Optional build type (Debug, Release, etc.)
            
        Returns:
            Recommended generator name
        """
        # Select base generator
        generator = self.select(platform, compiler)
        
        # Adjust for build type if needed
        if build_type and self.is_single_config_generator(generator):
            # Single-config generators are fine for any build type
            pass
        elif build_type and self.is_multi_config_generator(generator):
            # Multi-config generators support all build types
            pass
        
        return generator
    
    def get_default_generator(self, platform: str) -> str:
        """Get default generator for platform.
        
        Args:
            platform: Target platform
            
        Returns:
            Default generator name
        """
        defaults = {
            "windows": "Ninja",
            "linux": "Ninja",
            "wasm": "Ninja"
        }
        
        return defaults.get(platform, "Ninja")
