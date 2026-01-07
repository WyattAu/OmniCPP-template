"""
Configure command - CMake configuration with generator selection

This module provides the configure command for setting up the build system
with CMake, including generator selection, cache variables, and build type
configuration.
"""

import argparse
import os
import shutil
from typing import Any, Dict, Optional

from core.logger import Logger
from core.exception_handler import BuildError, ConfigurationError
from core.terminal_invoker import TerminalInvoker
from core.terminal_detector import TerminalDetector
from cmake.cmake_wrapper import CMakeWrapper
from cmake.generator_selector import GeneratorSelector


class ConfigureCommand:
    """Configure build system with CMake.
    
    This command handles CMake configuration including:
    - Generator selection based on platform and compiler
    - Build type selection (Debug, Release, RelWithDebInfo, MinSizeRel)
    - Cache variable configuration
    - Toolchain selection
    - Preset selection
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize configure command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("configure", config.get("logging", {}))
        
        # Initialize terminal invoker
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise ConfigurationError("No terminal detected")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Initialize CMake wrapper
        self.cmake_wrapper = CMakeWrapper(config)
        
        # Initialize generator selector
        self.generator_selector = GeneratorSelector(config)
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute configure command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting CMake configuration...")
            
            # Get configuration parameters
            build_type = getattr(args, "build_type", "Release")
            generator = getattr(args, "generator", None)
            toolchain = getattr(args, "toolchain", None)
            preset = getattr(args, "preset", None)
            source_dir = getattr(args, "source_dir", ".")
            build_dir = getattr(args, "build_dir", "build")
            
            # Validate build type
            valid_build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]
            if build_type not in valid_build_types:
                raise ConfigurationError(
                    f"Invalid build type: {build_type}. "
                    f"Valid types: {', '.join(valid_build_types)}"
                )
            
            # Ensure build directory exists
            self._ensure_build_directory(build_dir)
            
            # Select generator if not specified
            if not generator:
                platform = self._detect_platform()
                compiler = self._detect_compiler()
                generator = self.generator_selector.select(platform, compiler)
                self.logger.info(f"Auto-selected generator: {generator}")
            
            # Build CMake configure command
            cmake_args = self._build_cmake_args(
                source_dir=source_dir,
                build_dir=build_dir,
                build_type=build_type,
                generator=generator,
                toolchain=toolchain,
                preset=preset
            )
            
            # Execute CMake configure
            self.logger.info(f"Configuring with build type: {build_type}")
            self.logger.info(f"Build directory: {os.path.abspath(build_dir)}")
            
            result = self.cmake_wrapper.configure(cmake_args)
            
            if result.return_code != 0:
                self.logger.error("CMake configuration failed")
                if result.stderr:
                    self.logger.error(f"Error output:\n{result.stderr}")
                raise BuildError(
                    "CMake configuration failed",
                    {
                        "return_code": result.return_code,
                        "stderr": result.stderr
                    }
                )
            
            self.logger.info("CMake configuration completed successfully")
            return 0
            
        except (BuildError, ConfigurationError) as e:
            self.logger.error(f"Configuration failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during configuration: {e}")
            return 1
    
    def _ensure_build_directory(self, build_dir: str) -> None:
        """Ensure build directory exists.
        
        Args:
            build_dir: Build directory path
            
        Raises:
            ConfigurationError: If directory cannot be created
        """
        try:
            os.makedirs(build_dir, exist_ok=True)
            self.logger.debug(f"Build directory ensured: {build_dir}")
        except OSError as e:
            raise ConfigurationError(
                f"Failed to create build directory: {build_dir}",
                {"error": str(e)}
            )
    
    def _detect_platform(self) -> str:
        """Detect current platform.
        
        Returns:
            Platform name (windows, linux, wasm)
        """
        if os.name == "nt":
            return "windows"
        elif os.name == "posix":
            return "linux"
        else:
            return "wasm"
    
    def _detect_compiler(self) -> str:
        """Detect available compiler.
        
        Returns:
            Compiler name (msvc, gcc, clang, etc.)
        """
        # Check for MSVC
        if shutil.which("cl.exe") or os.environ.get("VSINSTALLDIR"):
            return "msvc"
        
        # Check for GCC
        if shutil.which("gcc"):
            return "gcc"
        
        # Check for Clang
        if shutil.which("clang"):
            return "clang"
        
        # Default to auto
        return "auto"
    
    def _build_cmake_args(
        self,
        source_dir: str,
        build_dir: str,
        build_type: str,
        generator: str,
        toolchain: Optional[str],
        preset: Optional[str]
    ) -> list[str]:
        """Build CMake configure arguments.
        
        Args:
            source_dir: Source directory
            build_dir: Build directory
            build_type: Build type
            generator: CMake generator
            toolchain: Toolchain file path
            preset: CMake preset name
            
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add preset if specified
        if preset:
            args.extend(["--preset", preset])
        else:
            # Add generator
            args.extend(["-G", generator])
            
            # Add build type
            args.extend(["-DCMAKE_BUILD_TYPE=" + build_type])
            
            # Add toolchain if specified
            if toolchain:
                args.extend(["-DCMAKE_TOOLCHAIN_FILE=" + toolchain])
            
            # Add cache variables from config
            cache_vars = self.config.get("cmake_cache_vars", {})
            for key, value in cache_vars.items():
                args.extend([f"-D{key}={value}"])
        
        # Add source directory
        args.append(source_dir)
        
        return args
