#!/usr/bin/env python3
"""
OmniCpp Controller - Build and Package Management System.

This module provides the main controller for the OmniCpp build system,
supporting multiple compilers, toolchains, and platforms. It supports
MSVC, MSVC-clang, mingw-clang, and mingw-gcc on Windows,
and GCC and Clang on Linux.

Usage:
    python OmniCppController.py <command> [target] [pipeline] [preset] [config] [options]

Commands:
    configure   Configure the build system with CMake
    build       Build the project
    clean       Clean build artifacts
    install     Install build artifacts
    test        Run tests
    package     Create distribution packages
    format      Format code with clang-format and black
    lint        Run static analysis with clang-tidy, pylint, and mypy
    help        Show help information

Examples:
    python OmniCppController.py configure
    python OmniCppController.py build engine "Clean Build Pipeline" default release --compiler msvc
    python OmniCppController.py build game "Clean Build Pipeline" default debug --compiler clang-msvc
    python OmniCppController.py build standalone "Clean Build Pipeline" default release
    python OmniCppController.py format
    python OmniCppController.py lint
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

# Import modular build components
from omni_scripts.build import (
    BuildContext,
    BuildError,
    BuildManager,
    ToolchainError,
)
from omni_scripts.cmake import CMakeManager
from omni_scripts.conan import ConanManager

# Import new logging system
from omni_scripts.logging import (
    get_logger,
    log_error,
    log_info,
    log_success,
    log_warning,
    setup_logging,
)

# Import platform detection
from omni_scripts.platform.detector import detect_platform, PlatformInfo

# Import compiler detection
from omni_scripts.compilers.detector import detect_compiler, validate_cpp23_support, CompilerInfo

# Import terminal setup
from omni_scripts.utils.terminal_utils import execute_with_terminal_setup

# Import utility functions
from omni_scripts.utils import (
    is_linux,
    is_windows,
    get_system_platform,
)


class ControllerError(Exception):
    """Base exception for controller-related errors."""

    def __init__(
        self,
        message: str,
        command: Optional[str] = None,
    ) -> None:
        """Initialize controller error.

        Args:
            message: Error message describing the issue.
            command: Optional command that caused the error.
        """
        self.command = command
        super().__init__(message)


class InvalidTargetError(ControllerError):
    """Exception raised when an invalid target is specified."""

    def __init__(
        self,
        message: str,
        target: Optional[str] = None,
    ) -> None:
        """Initialize invalid target error.

        Args:
            message: Error message describing the issue.
            target: Optional invalid target name.
        """
        self.target = target
        super().__init__(message)


class InvalidPipelineError(ControllerError):
    """Exception raised when an invalid pipeline is specified."""

    def __init__(
        self,
        message: str,
        pipeline: Optional[str] = None,
    ) -> None:
        """Initialize invalid pipeline error.

        Args:
            message: Error message describing the issue.
            pipeline: Optional invalid pipeline name.
        """
        self.pipeline = pipeline
        super().__init__(message)


class OmniCppController:
    """Main controller for OmniCpp build system.

    This class manages the overall build process, coordinating
    between CMake, Conan, and build managers.

    Attributes:
        project_root: The root directory of project.
        build_dir: The build directory path.
        install_dir: The installation directory path.
        cmake_manager: The CMake manager instance.
        conan_manager: The Conan manager instance.
        build_manager: The build manager instance.
    """

    def __init__(self) -> None:
        """Initialize the OmniCpp controller.

        Raises:
            NotADirectoryError: If project root is not a valid directory.
        """
        # Initialize logging system
        setup_logging()
        self.logger = get_logger(__name__)

        # Detect platform
        self.platform_info: PlatformInfo = detect_platform()
        self.logger.info(
            f"Initializing OmniCpp Controller on {self.platform_info.os} "
            f"{self.platform_info.architecture}"
        )

        # Initialize paths
        self.project_root: Path = Path(__file__).parent.resolve()
        self.build_dir: Path = self.project_root / "build"
        self.install_dir: Path = self.project_root / "install"

        # Initialize managers
        self.cmake_manager: CMakeManager = CMakeManager(self.build_dir)
        self.conan_manager: ConanManager = ConanManager(self.build_dir)
        self.build_manager: BuildManager = BuildManager(self.project_root)

        # Detect compiler
        self.compiler_info: Optional[CompilerInfo] = None
        self._detect_available_compiler()

    def _detect_available_compiler(self) -> None:
        """Detect available compiler for current platform.

        This method detects the best available compiler based on the current
        platform and validates C++23 support.
        """
        self.logger.info("Detecting available compiler...")

        # Detect compiler
        self.compiler_info = detect_compiler(platform_info=self.platform_info)

        if self.compiler_info:
            self.logger.info(
                f"Detected compiler: {self.compiler_info.name} "
                f"{self.compiler_info.version}"
            )

            # Validate C++23 support
            validation = validate_cpp23_support(self.compiler_info)
            if validation.valid:
                self.logger.info(
                    f"Compiler supports C++23: {self.compiler_info.supports_cpp23}"
                )
            else:
                self.logger.warning(
                    f"Compiler does not fully support C++23, "
                    f"falling back to {validation.fallback}"
                )
                for warning in validation.warnings:
                    self.logger.warning(warning)
        else:
            self.logger.warning("No compiler detected, will use default")

    def build(
        self,
        target: str,
        pipeline: str,
        preset: str,
        config: str,
        compiler: Optional[str] = None,
        clean: bool = False,
    ) -> int:
        """Build the project.

        This method builds the specified target using the given pipeline,
        preset, configuration, and compiler.

        Args:
            target: Build target (engine, game, standalone, all).
            pipeline: Build pipeline name.
            preset: CMake preset name.
            config: Build configuration (debug, release).
            compiler: Optional compiler to use (msvc, clang-msvc, mingw-clang, mingw-gcc).
            clean: Whether to clean before building.

        Returns:
            Exit code (0 for success, non-zero for failure).

        Raises:
            InvalidTargetError: If target is invalid.
            InvalidPipelineError: If pipeline is invalid.
            BuildError: If build process fails.
            ToolchainError: If toolchain is not available.
        """
        try:
            self.logger.info(f"Building target: {target}")
            self.logger.info(f"Pipeline: {pipeline}")
            self.logger.info(f"Preset: {preset}")
            self.logger.info(f"Config: {config}")

            # Determine compiler if not specified
            detected_compiler: Optional[str] = compiler
            if not detected_compiler:
                if self.compiler_info:
                    detected_compiler = self.compiler_info.name.lower().replace(" ", "-").lower()
                    self.logger.info(f"Using detected compiler: {detected_compiler}")
                else:
                    detected_compiler = self._detect_compiler()

            if detected_compiler:
                self.logger.info(f"Compiler: {detected_compiler}")

            # Map target to build flags
            lib_flag: bool = target in ["engine", "all"]
            st_flag: bool = target in ["game", "standalone", "all"]

            # Create build context
            context: BuildContext = BuildContext(
                product=target,
                task=pipeline,
                arch="x64",
                build_type=config,
                compiler=detected_compiler,
                is_cross_compilation=False,
                lib_flag=lib_flag,
                st_flag=st_flag,
            )

            # Execute build pipeline with terminal environment setup for MinGW compilers
            if detected_compiler and detected_compiler.lower() in ["mingw-clang", "mingw-gcc"]:
                # Use terminal environment setup for MinGW compilers
                from omni_scripts.utils.terminal_utils import execute_with_terminal_setup
                self.logger.info(f"Setting up terminal environment for {detected_compiler}")

                # Find Python executable path - use full path to avoid PATH corruption issues
                # Don't use shutil.which() as it may return corrupted paths
                # Instead, use the Python executable from user's local bin directory
                python_exe = None
                # Check if Python is in user's local bin directory
                user_local_bin = Path.home() / ".local" / "bin"
                if user_local_bin.exists():
                    # Look for python.exe or python3.exe in user's local bin
                    for python_file in ["python.exe", "python3.exe"]:
                        python_path = user_local_bin / python_file
                        if python_path.exists():
                            python_exe = str(python_path)
                            break

                # If not found in user's local bin, fall back to system Python
                if not python_exe:
                    python_exe = "python"

                # Execute appropriate build pipeline directly in MSYS2 environment
                # Don't recursively call the controller - execute the pipeline directly
                if pipeline == "Clean Build Pipeline":
                    result = execute_with_terminal_setup(
                        f'"{python_exe}" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\\"{target}\\", task=\\"Clean Build Pipeline\\", arch=\\"x64\\", build_type=\\"{config}\\", compiler=\\"{detected_compiler}\\", is_cross_compilation=False, lib_flag={lib_flag}, st_flag={st_flag}, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"',
                        compiler=detected_compiler,
                        cwd=str(self.project_root),
                    )
                elif pipeline == "Build Project":
                    result = execute_with_terminal_setup(
                        f'"{python_exe}" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\\"{target}\\", task=\\"Build Project\\", arch=\\"x64\\", build_type=\\"{config}\\", compiler=\\"{detected_compiler}\\", is_cross_compilation=False, lib_flag={lib_flag}, st_flag={st_flag}, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.build_project(ctx)"',
                        compiler=detected_compiler,
                        cwd=str(self.project_root),
                    )
                elif pipeline == "Configure Build System":
                    result = execute_with_terminal_setup(
                        f'"{python_exe}" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\\"{target}\\", task=\\"Configure Build System\\", arch=\\"x64\\", build_type=\\"{config}\\", compiler=\\"{detected_compiler}\\", is_cross_compilation=False, lib_flag={lib_flag}, st_flag={st_flag}, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.configure_build_system(ctx)"',
                        compiler=detected_compiler,
                        cwd=str(self.project_root),
                    )
                elif pipeline == "Install Build Artifacts":
                    result = execute_with_terminal_setup(
                        f'"{python_exe}" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\\"{target}\\", task=\\"Install Build Artifacts\\", arch=\\"x64\\", build_type=\\"{config}\\", compiler=\\"{detected_compiler}\\", is_cross_compilation=False, lib_flag={lib_flag}, st_flag={st_flag}, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.install_artifacts(ctx)"',
                        compiler=detected_compiler,
                        cwd=str(self.project_root),
                    )
                else:
                    error_msg: str = f"Unknown pipeline: {pipeline}"
                    self.logger.error(error_msg)
                    raise InvalidPipelineError(error_msg, pipeline=pipeline)
                return result
            else:
                # Execute build pipeline normally for MSVC and MSVC-Clang
                if pipeline == "Clean Build Pipeline":
                    self.build_manager.run_clean_build_pipeline(context)
                elif pipeline == "Build Project":
                    self.build_manager.build_project(context)
                elif pipeline == "Configure Build System":
                    self.build_manager.configure_build_system(context)
                elif pipeline == "Install Build Artifacts":
                    self.build_manager.install_artifacts(context)
                else:
                    error_msg: str = f"Unknown pipeline: {pipeline}"
                    self.logger.error(error_msg)
                    raise InvalidPipelineError(error_msg, pipeline=pipeline)

            return 0

        except (BuildError, ToolchainError, InvalidPipelineError) as e:
            self.logger.error(f"Build error: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return 1

    def clean(self, target: Optional[str] = None) -> int:
        """Clean build artifacts.

        This method removes build artifacts for the specified target.

        Args:
            target: Optional target to clean (engine, game, standalone, all, or None for all).

        Returns:
            Exit code (0 for success, non-zero for failure).

        Raises:
            BuildError: If cleaning fails.
        """
        try:
            self.logger.info("Cleaning build artifacts...")

            # Map target to build flags
            lib_flag: bool = target in ["engine", "all", None]
            st_flag: bool = target in ["game", "standalone", "all", None]

            context: BuildContext = BuildContext(
                product=target or "all",
                task="clean",
                arch="x64",
                build_type="all",
                compiler=None,
                is_cross_compilation=False,
                lib_flag=lib_flag,
                st_flag=st_flag,
            )

            self.build_manager.clean_build_directories(context)
            log_success("Build artifacts cleaned successfully")
            return 0
        except BuildError as e:
            self.logger.error(f"Clean error: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during clean: {e}")
            return 1

    def install(self, target: str, config: str) -> int:
        """Install build artifacts.

        This method installs build artifacts for the specified target
        and configuration.

        Args:
            target: Target to install (engine, game, standalone, all).
            config: Build configuration (debug, release).

        Returns:
            Exit code (0 for success, non-zero for failure).

        Raises:
            InvalidTargetError: If target is invalid.
            BuildError: If installation fails.
            ToolchainError: If toolchain is not available.
        """
        try:
            self.logger.info(f"Installing target: {target}")
            self.logger.info(f"Config: {config}")

            # Map target to build flags
            lib_flag: bool = target in ["engine", "all"]
            st_flag: bool = target in ["game", "standalone", "all"]

            context: BuildContext = BuildContext(
                product=target,
                task="install",
                arch="x64",
                build_type=config,
                compiler=self._detect_compiler(),
                is_cross_compilation=False,
                lib_flag=lib_flag,
                st_flag=st_flag,
            )

            self.build_manager.install_artifacts(context)
            return 0

        except (BuildError, ToolchainError) as e:
            self.logger.error(f"Install error: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during install: {e}")
            return 1

    def test(self, target: str, config: str) -> int:
        """Run tests.

        This method runs tests for the specified target and configuration.

        Args:
            target: Target to test (engine, game, standalone, all).
            config: Build configuration (debug, release).

        Returns:
            Exit code (0 for success, non-zero for failure).

        Note:
            Test execution is not yet implemented.
        """
        try:
            self.logger.info(f"Running tests for target: {target}")
            self.logger.info(f"Config: {config}")

            # TODO: Implement test execution
            self.logger.warning("Test execution not yet implemented")
            return 0

        except Exception as e:
            self.logger.error(f"Test error: {e}")
            return 1

    def package(self, target: str, config: str) -> int:
        """Create distribution packages.

        This method creates distribution packages for the specified
        target and configuration.

        Args:
            target: Target to package (engine, game, standalone, all).
            config: Build configuration (debug, release).

        Returns:
            Exit code (0 for success, non-zero for failure).

        Note:
            Packaging is not yet implemented.
        """
        try:
            self.logger.info(f"Creating packages for target: {target}")
            self.logger.info(f"Config: {config}")

            # TODO: Implement packaging
            self.logger.warning("Packaging not yet implemented")
            return 0

        except Exception as e:
            self.logger.error(f"Package error: {e}")
            return 1

    def configure(
        self,
        build_type: str = "Release",
        generator: Optional[str] = None,
        toolchain: Optional[str] = None,
        preset: Optional[str] = None,
    ) -> int:
        """Configure the build system with CMake.

        This method configures the build system using CMake with the specified
        build type, generator, toolchain, and preset.

        Args:
            build_type: Build configuration (Debug, Release, RelWithDebInfo, MinSizeRel).
            generator: Optional CMake generator.
            toolchain: Optional toolchain file path.
            preset: Optional CMake preset name.

        Returns:
            Exit code (0 for success, non-zero for failure).

        Raises:
            BuildError: If configuration fails.
            ToolchainError: If toolchain is not available.
        """
        try:
            self.logger.info("Configuring build system...")
            self.logger.info(f"Build type: {build_type}")
            if generator:
                self.logger.info(f"Generator: {generator}")
            if toolchain:
                self.logger.info(f"Toolchain: {toolchain}")
            if preset:
                self.logger.info(f"Preset: {preset}")

            # Execute CMake configure
            result = self.cmake_manager.configure(
                source_dir=self.project_root,
                build_dir=self.build_dir,
                build_type=build_type,
                compiler=None,
                is_cross_compilation=False,
                build_library=False,
                enable_coverage=False,
                unique_id=None,
            )

            if result is None:
                self.logger.error("CMake configuration failed")
                return 1

            log_success("CMake configuration completed successfully")
            return 0

        except Exception as e:
            self.logger.error(f"Configure error: {e}")
            return 1

    def format(
        self,
        files: Optional[list[str]] = None,
        directories: Optional[list[str]] = None,
        check: bool = False,
        dry_run: bool = False,
        cpp_only: bool = False,
        python_only: bool = False,
    ) -> int:
        """Format code with clang-format and black.

        This method formats C++ and Python code using clang-format and black.

        Args:
            files: Optional list of specific files to format.
            directories: Optional list of directories to scan.
            check: Whether to only check formatting without modifying files.
            dry_run: Whether to run in dry-run mode.
            cpp_only: Only format C++ files.
            python_only: Only format Python files.

        Returns:
            Exit code (0 for success, non-zero for failure).
        """
        try:
            self.logger.info("Starting code formatting...")

            # Collect files to format
            files_to_format: list[str] = self._collect_files(
                files=files,
                directories=directories,
            )

            if not files_to_format:
                self.logger.info("No files to format")
                return 0

            # Separate C++ and Python files
            cpp_files = [
                f
                for f in files_to_format
                if f.endswith((".cpp", ".hpp", ".h", ".cc", ".cxx"))
            ]
            python_files = [f for f in files_to_format if f.endswith((".py"))]

            # Format C++ files
            if not python_only and cpp_files:
                self.logger.info(f"Formatting {len(cpp_files)} C++ file(s)...")
                self._format_cpp_files(
                    files=cpp_files,
                    check=check,
                    dry_run=dry_run,
                )

            # Format Python files
            if not cpp_only and python_files:
                self.logger.info(f"Formatting {len(python_files)} Python file(s)...")
                self._format_python_files(
                    files=python_files,
                    check=check,
                    dry_run=dry_run,
                )

            log_success("Code formatting completed successfully")
            return 0

        except Exception as e:
            log_error(f"Format error: {e}")
            return 1

    def lint(
        self,
        files: Optional[list[str]] = None,
        directories: Optional[list[str]] = None,
        fix: bool = False,
        cpp_only: bool = False,
        python_only: bool = False,
    ) -> int:
        """Run static analysis on code.

        This method runs static analysis on C++ and Python code using
        clang-tidy, pylint, and mypy.

        Args:
            files: Optional list of specific files to lint.
            directories: Optional list of directories to scan.
            fix: Whether to apply automatic fixes.
            cpp_only: Only lint C++ files.
            python_only: Only lint Python files.

        Returns:
            Exit code (0 for success, non-zero for failure).
        """
        try:
            self.logger.info("Starting static analysis...")

            # Collect files to lint
            files_to_lint: list[str] = self._collect_files(
                files=files,
                directories=directories,
            )

            if not files_to_lint:
                self.logger.info("No files to lint")
                return 0

            # Separate C++ and Python files
            cpp_files = [
                f
                for f in files_to_lint
                if f.endswith((".cpp", ".hpp", ".h", ".cc", ".cxx"))
            ]
            python_files = [f for f in files_to_lint if f.endswith((".py"))]

            # Track overall success
            overall_success: bool = True

            # Lint C++ files
            if not python_only and cpp_files:
                self.logger.info(f"Linting {len(cpp_files)} C++ file(s)...")
                cpp_success = self._lint_cpp_files(
                    files=cpp_files,
                    fix=fix,
                )
                overall_success = overall_success and cpp_success

            # Lint Python files
            if not cpp_only and python_files:
                self.logger.info(f"Linting {len(python_files)} Python file(s)...")
                pylint_success = self._lint_python_files_pylint(
                    files=python_files,
                    fix=fix,
                )
                mypy_success = self._lint_python_files_mypy(files=python_files)
                overall_success = overall_success and pylint_success and mypy_success

            if overall_success:
                log_success("Static analysis completed successfully")
                return 0
            else:
                log_error("Static analysis found issues")
                return 1

        except Exception as e:
            log_error(f"Lint error: {e}")
            return 1

    def _collect_files(
        self,
        files: Optional[list[str]] = None,
        directories: Optional[list[str]] = None,
    ) -> list[str]:
        """Collect files to format or lint.

        Args:
            files: Optional list of specific files.
            directories: Optional list of directories to scan.

        Returns:
            List of files found.
        """
        collected_files: list[str] = []

        # Add specific files
        if files:
            for file_path in files:
                if Path(file_path).exists():
                    collected_files.append(file_path)

        # Scan directories
        if directories:
            for directory in directories:
                dir_path = Path(directory)
                if dir_path.is_dir():
                    collected_files.extend(self._scan_directory(directory))

        # If no files or directories specified, scan current directory
        if not files and not directories:
            collected_files.extend(self._scan_directory("."))

        return collected_files

    def _scan_directory(self, directory: str) -> list[str]:
        """Scan directory for C++ and Python files.

        Args:
            directory: Directory to scan.

        Returns:
            List of files found.
        """
        import os
        files: list[str] = []

        # File extensions to process
        cpp_extensions = [".cpp", ".hpp", ".h", ".cc", ".cxx"]
        python_extensions = [".py"]

        # Walk directory
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = Path(root) / filename

                # Skip hidden files and directories
                if filename.startswith("."):
                    continue

                # Check file extension
                ext = filepath.suffix.lower()
                if ext in cpp_extensions or ext in python_extensions:
                    files.append(str(filepath))

        return files

    def _format_cpp_files(
        self,
        files: list[str],
        check: bool,
        dry_run: bool,
    ) -> None:
        """Format C++ files with clang-format.

        Args:
            files: List of C++ files.
            check: Whether to only check formatting.
            dry_run: Whether to run in dry-run mode.

        Raises:
            Exception: If formatting fails.
        """
        import subprocess

        # Check if clang-format is available
        if not self._command_exists("clang-format"):
            self.logger.warning("clang-format not found, skipping C++ formatting")
            return

        # Build clang-format command
        cmd: list[str] = ["clang-format"]

        if check:
            cmd.append("--dry-run")
            cmd.append("--Werror")
        elif dry_run:
            cmd.append("--dry-run")

        cmd.append("-i")  # In-place editing
        cmd.extend(files)

        # Execute clang-format
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise Exception(
                    f"clang-format failed with exit code {result.returncode}"
                )

            if check and result.stdout:
                self.logger.warning("C++ files need formatting")

        except FileNotFoundError:
            raise Exception("clang-format executable not found")
        except Exception as e:
            raise Exception(f"Failed to run clang-format: {e}")

    def _format_python_files(
        self,
        files: list[str],
        check: bool,
        dry_run: bool,
    ) -> None:
        """Format Python files with black.

        Args:
            files: List of Python files.
            check: Whether to only check formatting.
            dry_run: Whether to run in dry-run mode.

        Raises:
            Exception: If formatting fails.
        """
        import subprocess

        # Check if black is available
        if not self._command_exists("black"):
            self.logger.warning("black not found, skipping Python formatting")
            return

        # Build black command
        cmd: list[str] = ["black"]

        if check:
            cmd.append("--check")
        elif dry_run:
            cmd.append("--diff")

        cmd.extend(files)

        # Execute black
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise Exception(f"black failed with exit code {result.returncode}")

            if check and result.stdout:
                self.logger.warning("Python files need formatting")

        except FileNotFoundError:
            raise Exception("black executable not found")
        except Exception as e:
            raise Exception(f"Failed to run black: {e}")

    def _lint_cpp_files(self, files: list[str], fix: bool) -> bool:
        """Lint C++ files with clang-tidy.

        Args:
            files: List of C++ files.
            fix: Whether to apply fixes.

        Returns:
            True if no issues found, False otherwise.

        Raises:
            Exception: If linting fails.
        """
        import subprocess

        # Check if clang-tidy is available
        if not self._command_exists("clang-tidy"):
            self.logger.warning("clang-tidy not found, skipping C++ linting")
            return True

        # Build clang-tidy command
        cmd: list[str] = ["clang-tidy"]

        if fix:
            cmd.append("--fix")

        cmd.extend(files)

        # Execute clang-tidy
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                self.logger.error(f"clang-tidy found issues in {len(files)} file(s)")
                if result.stdout:
                    self.logger.info(f"clang-tidy output:\n{result.stdout}")
                if result.stderr:
                    self.logger.error(f"clang-tidy errors:\n{result.stderr}")
                return False
            else:
                self.logger.info(f"clang-tidy: No issues found in {len(files)} file(s)")
                return True

        except FileNotFoundError:
            raise Exception("clang-tidy executable not found")
        except Exception as e:
            raise Exception(f"Failed to run clang-tidy: {e}")

    def _lint_python_files_pylint(self, files: list[str], fix: bool) -> bool:
        """Lint Python files with pylint.

        Args:
            files: List of Python files.
            fix: Whether to apply fixes.

        Returns:
            True if no issues found, False otherwise.

        Raises:
            Exception: If linting fails.
        """
        import subprocess

        # Check if pylint is available
        if not self._command_exists("pylint"):
            self.logger.warning("pylint not found, skipping Python linting")
            return True

        # Build pylint command
        cmd: list[str] = ["pylint"]

        if fix:
            cmd.append("--fix")

        cmd.extend(files)

        # Execute pylint
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                self.logger.error(f"pylint found issues in {len(files)} file(s)")
                if result.stdout:
                    self.logger.info(f"pylint output:\n{result.stdout}")
                if result.stderr:
                    self.logger.error(f"pylint errors:\n{result.stderr}")
                return False
            else:
                self.logger.info(f"pylint: No issues found in {len(files)} file(s)")
                return True

        except FileNotFoundError:
            raise Exception("pylint executable not found")
        except Exception as e:
            raise Exception(f"Failed to run pylint: {e}")

    def _lint_python_files_mypy(self, files: list[str]) -> bool:
        """Type check Python files with mypy.

        Args:
            files: List of Python files.

        Returns:
            True if no type errors found, False otherwise.

        Raises:
            Exception: If type checking fails.
        """
        import subprocess

        # Check if mypy is available
        if not self._command_exists("mypy"):
            self.logger.warning("mypy not found, skipping type checking")
            return True

        # Build mypy command
        cmd: list[str] = ["mypy"]
        cmd.extend(files)

        # Execute mypy
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                self.logger.error(f"mypy found type errors in {len(files)} file(s)")
                if result.stdout:
                    self.logger.info(f"mypy output:\n{result.stdout}")
                if result.stderr:
                    self.logger.error(f"mypy errors:\n{result.stderr}")
                return False
            else:
                self.logger.info(f"mypy: No type errors found in {len(files)} file(s)")
                return True

        except FileNotFoundError:
            raise Exception("mypy executable not found")
        except Exception as e:
            raise Exception(f"Failed to run mypy: {e}")

    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH.

        Args:
            command: Command to check.

        Returns:
            True if command exists, False otherwise.
        """
        import shutil

        return shutil.which(command) is not None


def main() -> int:
    """Main entry point for OmniCpp controller.

    This function delegates to the modular command dispatcher
    which provides a single source of truth for CLI parsing.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Import dispatcher here to avoid circular imports
    from omni_scripts.controller.dispatcher import main as dispatcher_main
    
    # Delegate to modular dispatcher
    return dispatcher_main()


if __name__ == "__main__":
    sys.exit(main())
