"""
Compile command - Build project with parallel jobs

This module provides compile command for building the configured project
with CMake, including parallel job execution, target selection, and
error handling.
"""

import argparse
import os
from typing import Any, Dict, Optional

from core.logger import Logger
from core.exception_handler import BuildError
from core.terminal_invoker import TerminalInvoker
from core.terminal_detector import TerminalDetector
from cmake.cmake_wrapper import CMakeWrapper


class CompileCommand:
    """Compile configured project.
    
    This command handles CMake build including:
    - Parallel job execution
    - Target selection
    - Incremental builds
    - Build progress display
    - Error handling and reporting
    - Clean builds
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize compile command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("compile", config.get("logging", {}))
        
        # Initialize terminal invoker
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise BuildError("No terminal detected")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Initialize CMake wrapper
        self.cmake_wrapper = CMakeWrapper(config)
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute compile command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting build...")
            
            # Get configuration parameters
            build_dir = getattr(args, "build_dir", "build")
            target = getattr(args, "target", None)
            jobs = getattr(args, "jobs", None)
            clean = getattr(args, "clean", False)
            verbose = getattr(args, "verbose", False)
            
            # Validate build directory exists
            if not os.path.exists(build_dir):
                raise BuildError(
                    f"Build directory does not exist: {build_dir}. "
                    "Run configure command first."
                )
            
            # Determine number of parallel jobs
            if jobs is None:
                jobs = self._get_default_jobs()
                self.logger.info(f"Using {jobs} parallel jobs")
            else:
                self.logger.info(f"Using {jobs} parallel jobs (user-specified)")
            
            # Clean build if requested
            if clean:
                self.logger.info("Cleaning build directory...")
                self._clean_build(build_dir)
            
            # Build CMake arguments
            cmake_args = self._build_cmake_args(
                build_dir=build_dir,
                target=target,
                jobs=jobs,
                verbose=verbose
            )
            
            # Execute CMake build
            self.logger.info(f"Building in: {os.path.abspath(build_dir)}")
            if target:
                self.logger.info(f"Building target: {target}")
            else:
                self.logger.info("Building all targets")
            
            result = self.cmake_wrapper.build(cmake_args)
            
            if result.return_code != 0:
                self.logger.error("Build failed")
                if result.stderr:
                    self.logger.error(f"Error output:\n{result.stderr}")
                raise BuildError(
                    "Build failed",
                    {
                        "return_code": result.return_code,
                        "stderr": result.stderr
                    }
                )
            
            self.logger.info("Build completed successfully")
            return 0
            
        except BuildError as e:
            self.logger.error(f"Build failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during build: {e}")
            return 1
    
    def _get_default_jobs(self) -> int:
        """Get default number of parallel jobs.
        
        Returns:
            Number of parallel jobs (CPU count or 4)
        """
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except Exception:
            return 4
    
    def _clean_build(self, build_dir: str) -> None:
        """Clean build directory.
        
        Args:
            build_dir: Build directory path
        """
        try:
            import shutil
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                self.logger.debug(f"Removed build directory: {build_dir}")
        except Exception as e:
            self.logger.warning(f"Failed to clean build directory: {e}")
    
    def _build_cmake_args(
        self,
        build_dir: str,
        target: Optional[str],
        jobs: int,
        verbose: bool
    ) -> list[str]:
        """Build CMake build arguments.
        
        Args:
            build_dir: Build directory
            target: Target to build (None for all)
            jobs: Number of parallel jobs
            verbose: Whether to enable verbose output
            
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add build directory
        args.extend(["--build", build_dir])
        
        # Add parallel jobs
        args.extend(["--parallel", str(jobs)])
        
        # Add target if specified
        if target:
            args.extend(["--target", target])
        
        # Add verbose flag if requested
        if verbose:
            args.append("--verbose")
        
        return args
