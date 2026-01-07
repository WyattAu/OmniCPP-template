"""
CMake command wrapper and execution

This module provides a comprehensive CMake wrapper for executing CMake commands
including configure, build, install, test, and package operations with proper
error handling and output parsing.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

from core.exception_handler import BuildError, CommandError
from core.logger import Logger
from core.terminal_invoker import ExecutionResult, TerminalInvoker
from core.terminal_detector import TerminalDetector


class CMakeWrapper:
    """CMake command wrapper with comprehensive execution support.
    
    This class provides methods for executing CMake commands including
    configure, build, install, test, and package operations with proper
    error handling, logging, and cross-platform support.
    """
    
    def __init__(
        self,
        cmake_path: Optional[str] = None,
        logger: Optional[Logger] = None
    ) -> None:
        """Initialize CMake wrapper.
        
        Args:
            cmake_path: Path to CMake executable (auto-detect if None)
            logger: Logger instance for logging operations
            
        Raises:
            BuildError: If CMake cannot be found
        """
        self.cmake_path = cmake_path or self._find_cmake()
        self.logger = logger or Logger("CMakeWrapper", {
            "level": "INFO",
            "console_handler_enabled": True,
            "file_handler_enabled": False
        })
        
        # Detect terminal for command execution
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise BuildError("No suitable terminal found for command execution")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Verify CMake version
        self._verify_cmake_version()
        
        self.logger.info(f"CMake wrapper initialized with: {self.cmake_path}")
    
    def _find_cmake(self) -> str:
        """Find CMake executable in system PATH.
        
        Returns:
            Path to CMake executable
            
        Raises:
            BuildError: If CMake cannot be found
        """
        # Try common CMake executable names
        cmake_names = ["cmake", "cmake.exe"]
        
        for name in cmake_names:
            cmake_path = shutil.which(name)
            if cmake_path:
                return cmake_path
        
        raise BuildError(
            "CMake executable not found in system PATH",
            {"searched_names": cmake_names}
        )
    
    def _verify_cmake_version(self) -> None:
        """Verify CMake version meets minimum requirements (4.0+).
        
        Raises:
            BuildError: If CMake version is too old
        """
        try:
            result = self.terminal_invoker.execute(
                f'"{self.cmake_path}" --version',
                timeout=10
            )
            
            if result.success and result.stdout:
                # Parse version from output (e.g., "cmake version 4.0.0")
                for line in result.stdout.split('\n'):
                    if 'cmake version' in line.lower():
                        version_str = line.split()[-1]
                        major_version = int(version_str.split('.')[0])
                        
                        if major_version < 4:
                            raise BuildError(
                                f"CMake version {version_str} is too old. "
                                f"Minimum required version is 4.0",
                                {"found_version": version_str, "required": "4.0"}
                            )
                        
                        self.logger.info(f"CMake version verified: {version_str}")
                        return
        except Exception as e:
            self.logger.warning(f"Could not verify CMake version: {e}")
    
    def configure(
        self,
        source_dir: str,
        build_dir: str,
        generator: str,
        cache_vars: dict[str, str],
        toolchain_file: Optional[str] = None,
        preset: Optional[str] = None
    ) -> bool:
        """Run CMake configuration.
        
        Args:
            source_dir: Source directory path
            build_dir: Build directory path
            generator: CMake generator (e.g., "Ninja", "Visual Studio 17 2022")
            cache_vars: Dictionary of CMake cache variables
            toolchain_file: Optional path to CMake toolchain file
            preset: Optional CMake preset name
            
        Returns:
            True if configuration succeeded, False otherwise
            
        Raises:
            BuildError: If configuration fails
        """
        self.logger.info(f"Configuring CMake project in {build_dir}")
        
        # Ensure build directory exists
        Path(build_dir).mkdir(parents=True, exist_ok=True)
        
        # Build CMake configure command
        cmd_parts = [f'"{self.cmake_path}"']
        
        # Add preset if specified
        if preset:
            cmd_parts.append(f'--preset "{preset}"')
        else:
            # Add source directory
            cmd_parts.append(f'-S "{source_dir}"')
            cmd_parts.append(f'-B "{build_dir}"')
            
            # Add generator
            cmd_parts.append(f'-G "{generator}"')
            
            # Add toolchain file if specified
            if toolchain_file:
                cmd_parts.append(f'-DCMAKE_TOOLCHAIN_FILE="{toolchain_file}"')
            
            # Add cache variables
            for key, value in cache_vars.items():
                cmd_parts.append(f'-D{key}="{value}"')
        
        cmd = " ".join(cmd_parts)
        
        try:
            result = self.terminal_invoker.execute(
                cmd,
                timeout=300,
                cwd=build_dir
            )
            
            if result.success:
                self.logger.info("CMake configuration completed successfully")
                return True
            else:
                self.logger.error(f"CMake configuration failed:\n{result.stderr}")
                raise BuildError(
                    "CMake configuration failed",
                    {
                        "source_dir": source_dir,
                        "build_dir": build_dir,
                        "generator": generator,
                        "stderr": result.stderr
                    }
                )
        except Exception as e:
            self.logger.error(f"CMake configuration error: {e}")
            raise BuildError(
                f"CMake configuration failed: {e}",
                {"source_dir": source_dir, "build_dir": build_dir}
            )
    
    def build(
        self,
        build_dir: str,
        target: Optional[str] = None,
        jobs: int = 1,
        config: Optional[str] = None,
        clean_first: bool = False
    ) -> bool:
        """Run CMake build.
        
        Args:
            build_dir: Build directory path
            target: Target to build (None for all targets)
            jobs: Number of parallel jobs
            config: Build configuration (Debug, Release, etc.)
            clean_first: Clean before building
            
        Returns:
            True if build succeeded, False otherwise
            
        Raises:
            BuildError: If build fails
        """
        self.logger.info(f"Building CMake project in {build_dir}")
        
        # Build CMake build command
        cmd_parts = [f'"{self.cmake_path}"', '--build', f'"{build_dir}"']
        
        # Add parallel jobs
        cmd_parts.append(f'--parallel {jobs}')
        
        # Add target if specified
        if target:
            cmd_parts.append(f'--target "{target}"')
        
        # Add configuration if specified
        if config:
            cmd_parts.append(f'--config "{config}"')
        
        # Add clean first if requested
        if clean_first:
            cmd_parts.append('--clean-first')
        
        cmd = " ".join(cmd_parts)
        
        try:
            result = self.terminal_invoker.execute(
                cmd,
                timeout=3600,  # 1 hour timeout for builds
                cwd=build_dir
            )
            
            if result.success:
                self.logger.info("CMake build completed successfully")
                return True
            else:
                self.logger.error(f"CMake build failed:\n{result.stderr}")
                raise BuildError(
                    "CMake build failed",
                    {
                        "build_dir": build_dir,
                        "target": target,
                        "stderr": result.stderr
                    }
                )
        except Exception as e:
            self.logger.error(f"CMake build error: {e}")
            raise BuildError(
                f"CMake build failed: {e}",
                {"build_dir": build_dir, "target": target}
            )
    
    def install(
        self,
        build_dir: str,
        config: Optional[str] = None,
        component: Optional[str] = None
    ) -> bool:
        """Run CMake install.
        
        Args:
            build_dir: Build directory path
            config: Build configuration (Debug, Release, etc.)
            component: Component to install
            
        Returns:
            True if installation succeeded, False otherwise
            
        Raises:
            BuildError: If installation fails
        """
        self.logger.info(f"Installing CMake project from {build_dir}")
        
        # Build CMake install command
        cmd_parts = [f'"{self.cmake_path}"', '--install', f'"{build_dir}"']
        
        # Add configuration if specified
        if config:
            cmd_parts.append(f'--config "{config}"')
        
        # Add component if specified
        if component:
            cmd_parts.append(f'--component "{component}"')
        
        cmd = " ".join(cmd_parts)
        
        try:
            result = self.terminal_invoker.execute(
                cmd,
                timeout=600,  # 10 minute timeout for installation
                cwd=build_dir
            )
            
            if result.success:
                self.logger.info("CMake installation completed successfully")
                return True
            else:
                self.logger.error(f"CMake installation failed:\n{result.stderr}")
                raise BuildError(
                    "CMake installation failed",
                    {
                        "build_dir": build_dir,
                        "stderr": result.stderr
                    }
                )
        except Exception as e:
            self.logger.error(f"CMake installation error: {e}")
            raise BuildError(
                f"CMake installation failed: {e}",
                {"build_dir": build_dir}
            )
    
    def test(
        self,
        build_dir: str,
        config: Optional[str] = None,
        tests: Optional[list[str]] = None,
        timeout: int = 300,
        verbose: bool = False
    ) -> bool:
        """Run CMake tests using CTest.
        
        Args:
            build_dir: Build directory path
            config: Build configuration (Debug, Release, etc.)
            tests: List of specific tests to run (None for all)
            timeout: Test timeout in seconds
            verbose: Enable verbose output
            
        Returns:
            True if all tests passed, False otherwise
            
        Raises:
            BuildError: If test execution fails
        """
        self.logger.info(f"Running CMake tests in {build_dir}")
        
        # Build CTest command
        cmd_parts = [f'"{self.cmake_path}"', '--build', f'"{build_dir}"', '--target', 'test']
        
        # Alternatively, use ctest directly
        ctest_path = self.cmake_path.replace("cmake", "ctest")
        if not os.path.exists(ctest_path):
            ctest_path = "ctest"
        
        cmd = f'"{ctest_path}" --output-on-failure'
        
        # Add configuration if specified
        if config:
            cmd += f' -C "{config}"'
        
        # Add timeout
        cmd += f' --timeout {timeout}'
        
        # Add verbose if requested
        if verbose:
            cmd += ' --verbose'
        
        # Add specific tests if specified
        if tests:
            for test in tests:
                cmd += f' -R "{test}"'
        
        try:
            result = self.terminal_invoker.execute(
                cmd,
                timeout=timeout + 60,  # Extra time for overhead
                cwd=build_dir
            )
            
            if result.success:
                self.logger.info("All CMake tests passed")
                return True
            else:
                self.logger.error(f"CMake tests failed:\n{result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"CMake test execution error: {e}")
            raise BuildError(
                f"CMake test execution failed: {e}",
                {"build_dir": build_dir}
            )
    
    def package(
        self,
        build_dir: str,
        config: Optional[str] = None,
        generator: Optional[str] = None
    ) -> bool:
        """Run CMake package.
        
        Args:
            build_dir: Build directory path
            config: Build configuration (Debug, Release, etc.)
            generator: CPack generator (e.g., "ZIP", "TGZ", "NSIS")
            
        Returns:
            True if packaging succeeded, False otherwise
            
        Raises:
            BuildError: If packaging fails
        """
        self.logger.info(f"Packaging CMake project from {build_dir}")
        
        # Build CMake package command
        cmd_parts = [f'"{self.cmake_path}"', '--build', f'"{build_dir}"', '--target', 'package']
        
        # Alternatively, use cpack directly
        cpack_path = self.cmake_path.replace("cmake", "cpack")
        if not os.path.exists(cpack_path):
            cpack_path = "cpack"
        
        cmd = f'"{cpack_path}"'
        
        # Add configuration if specified
        if config:
            cmd += f' -C "{config}"'
        
        # Add generator if specified
        if generator:
            cmd += f' -G "{generator}"'
        
        try:
            result = self.terminal_invoker.execute(
                cmd,
                timeout=600,  # 10 minute timeout for packaging
                cwd=build_dir
            )
            
            if result.success:
                self.logger.info("CMake packaging completed successfully")
                return True
            else:
                self.logger.error(f"CMake packaging failed:\n{result.stderr}")
                raise BuildError(
                    "CMake packaging failed",
                    {
                        "build_dir": build_dir,
                        "stderr": result.stderr
                    }
                )
        except Exception as e:
            self.logger.error(f"CMake packaging error: {e}")
            raise BuildError(
                f"CMake packaging failed: {e}",
                {"build_dir": build_dir}
            )
    
    def clean(self, build_dir: str) -> bool:
        """Clean CMake build directory.
        
        Args:
            build_dir: Build directory path
            
        Returns:
            True if cleaning succeeded, False otherwise
        """
        self.logger.info(f"Cleaning CMake build directory: {build_dir}")
        
        try:
            build_path = Path(build_dir)
            if build_path.exists():
                # Remove entire build directory
                shutil.rmtree(build_path)
                self.logger.info("Build directory cleaned successfully")
            else:
                self.logger.warning("Build directory does not exist, nothing to clean")
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to clean build directory: {e}")
            return False
    
    def get_version(self) -> str:
        """Get CMake version string.
        
        Returns:
            CMake version string
        """
        try:
            result = self.terminal_invoker.execute(
                f'"{self.cmake_path}" --version',
                timeout=10
            )
            
            if result.success and result.stdout:
                # Extract version from first line
                for line in result.stdout.split('\n'):
                    if 'cmake version' in line.lower():
                        return line.split()[-1]
            
            return "unknown"
        except Exception:
            return "unknown"
