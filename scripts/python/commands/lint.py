"""
Lint command - Static analysis with clang-tidy, pylint, and mypy

This module provides lint command for running static analysis
on C++ and Python code with clang-tidy, pylint, and mypy.
"""

import argparse
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

from core.logger import Logger
from core.exception_handler import BuildError, CommandError


class LintCommand:
    """Run static analysis on code.
    
    This command handles linting including:
    - C++ code analysis with clang-tidy
    - Python code analysis with pylint
    - Python type checking with mypy
    - File and directory selection
    - Lint result display
    - Fix mode support
    - Error handling
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize lint command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("lint", config.get("logging", {}))
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute lint command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting static analysis...")
            
            # Get configuration parameters
            files = getattr(args, "files", None)
            directories = getattr(args, "directories", None)
            fix = getattr(args, "fix", False)
            cpp_only = getattr(args, "cpp_only", False)
            python_only = getattr(args, "python_only", False)
            
            # Collect files to lint
            files_to_lint = self._collect_files(
                files=files,
                directories=directories
            )
            
            if not files_to_lint:
                self.logger.info("No files to lint")
                return 0
            
            # Separate C++ and Python files
            cpp_files = [f for f in files_to_lint if f.endswith((".cpp", ".hpp", ".h", ".cc", ".cxx"))]
            python_files = [f for f in files_to_lint if f.endswith((".py"))]
            
            # Track overall success
            overall_success = True
            
            # Lint C++ files
            if not python_only and cpp_files:
                self.logger.info(f"Linting {len(cpp_files)} C++ file(s)...")
                cpp_success = self._lint_cpp_files(
                    files=cpp_files,
                    fix=fix
                )
                overall_success = overall_success and cpp_success
            
            # Lint Python files
            if not cpp_only and python_files:
                self.logger.info(f"Linting {len(python_files)} Python file(s)...")
                pylint_success = self._lint_python_files_pylint(
                    files=python_files,
                    fix=fix
                )
                mypy_success = self._lint_python_files_mypy(
                    files=python_files
                )
                overall_success = overall_success and pylint_success and mypy_success
            
            if overall_success:
                self.logger.info("Static analysis completed successfully")
                return 0
            else:
                self.logger.error("Static analysis found issues")
                return 1
            
        except (BuildError, CommandError) as e:
            self.logger.error(f"Linting failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during linting: {e}")
            return 1
    
    def _collect_files(
        self,
        files: Optional[List[str]],
        directories: Optional[List[str]]
    ) -> List[str]:
        """Collect files to lint.
        
        Args:
            files: List of specific files
            directories: List of directories to scan
            
        Returns:
            List of files to lint
        """
        collected_files: List[str] = []
        
        # Add specific files
        if files:
            for file_path in files:
                if os.path.exists(file_path):
                    collected_files.append(file_path)
        
        # Scan directories
        if directories:
            for directory in directories:
                if os.path.isdir(directory):
                    collected_files.extend(self._scan_directory(directory))
        
        # If no files or directories specified, scan current directory
        if not files and not directories:
            collected_files.extend(self._scan_directory("."))
        
        return collected_files
    
    def _scan_directory(self, directory: str) -> List[str]:
        """Scan directory for C++ and Python files.
        
        Args:
            directory: Directory to scan
            
        Returns:
            List of files found
        """
        files: List[str] = []
        
        # File extensions to lint
        cpp_extensions = [".cpp", ".hpp", ".h", ".cc", ".cxx"]
        python_extensions = [".py"]
        
        # Walk directory
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                
                # Skip hidden files and directories
                if filename.startswith("."):
                    continue
                
                # Check file extension
                ext = os.path.splitext(filename)[1].lower()
                if ext in cpp_extensions or ext in python_extensions:
                    files.append(filepath)
        
        return files
    
    def _lint_cpp_files(
        self,
        files: List[str],
        fix: bool
    ) -> bool:
        """Lint C++ files with clang-tidy.
        
        Args:
            files: List of C++ files
            fix: Whether to apply fixes
            
        Returns:
            True if no issues found, False otherwise
            
        Raises:
            CommandError: If linting fails
        """
        # Check if clang-tidy is available
        if not shutil.which("clang-tidy"):
            self.logger.warning("clang-tidy not found, skipping C++ linting")
            return True
        
        # Build clang-tidy command
        cmd = ["clang-tidy"]
        
        if fix:
            cmd.append("--fix")
        
        cmd.extend(files)
        
        # Execute clang-tidy
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
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
            raise CommandError("clang-tidy executable not found")
        except Exception as e:
            raise CommandError(f"Failed to run clang-tidy: {e}")
    
    def _lint_python_files_pylint(
        self,
        files: List[str],
        fix: bool
    ) -> bool:
        """Lint Python files with pylint.
        
        Args:
            files: List of Python files
            fix: Whether to apply fixes
            
        Returns:
            True if no issues found, False otherwise
            
        Raises:
            CommandError: If linting fails
        """
        # Check if pylint is available
        if not shutil.which("pylint"):
            self.logger.warning("pylint not found, skipping Python linting")
            return True
        
        # Build pylint command
        cmd = ["pylint"]
        
        if fix:
            cmd.append("--fix")
        
        cmd.extend(files)
        
        # Execute pylint
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
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
            raise CommandError("pylint executable not found")
        except Exception as e:
            raise CommandError(f"Failed to run pylint: {e}")
    
    def _lint_python_files_mypy(self, files: List[str]) -> bool:
        """Type check Python files with mypy.
        
        Args:
            files: List of Python files
            
        Returns:
            True if no type errors found, False otherwise
            
        Raises:
            CommandError: If type checking fails
        """
        # Check if mypy is available
        if not shutil.which("mypy"):
            self.logger.warning("mypy not found, skipping type checking")
            return True
        
        # Build mypy command
        cmd = ["mypy"]
        cmd.extend(files)
        
        # Execute mypy
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
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
            raise CommandError("mypy executable not found")
        except Exception as e:
            raise CommandError(f"Failed to run mypy: {e}")
