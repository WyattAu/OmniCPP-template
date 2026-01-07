"""
Format command - Code formatting with clang-format and black

This module provides format command for formatting C++ and Python
code with clang-format and black respectively.
"""

import argparse
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

from core.logger import Logger
from core.exception_handler import BuildError, CommandError


class FormatCommand:
    """Format code with clang-format and black.
    
    This command handles code formatting including:
    - C++ code formatting with clang-format
    - Python code formatting with black
    - File and directory selection
    - Formatting verification
    - Dry-run mode
    - Error handling
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize format command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("format", config.get("logging", {}))
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute format command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting code formatting...")
            
            # Get configuration parameters
            files = getattr(args, "files", None)
            directories = getattr(args, "directories", None)
            check = getattr(args, "check", False)
            dry_run = getattr(args, "dry_run", False)
            cpp_only = getattr(args, "cpp_only", False)
            python_only = getattr(args, "python_only", False)
            
            # Collect files to format
            files_to_format = self._collect_files(
                files=files,
                directories=directories
            )
            
            if not files_to_format:
                self.logger.info("No files to format")
                return 0
            
            # Separate C++ and Python files
            cpp_files = [f for f in files_to_format if f.endswith((".cpp", ".hpp", ".h", ".cc", ".cxx"))]
            python_files = [f for f in files_to_format if f.endswith((".py"))]
            
            # Format C++ files
            if not python_only and cpp_files:
                self.logger.info(f"Formatting {len(cpp_files)} C++ file(s)...")
                self._format_cpp_files(
                    files=cpp_files,
                    check=check,
                    dry_run=dry_run
                )
            
            # Format Python files
            if not cpp_only and python_files:
                self.logger.info(f"Formatting {len(python_files)} Python file(s)...")
                self._format_python_files(
                    files=python_files,
                    check=check,
                    dry_run=dry_run
                )
            
            self.logger.info("Code formatting completed successfully")
            return 0
            
        except (BuildError, CommandError) as e:
            self.logger.error(f"Formatting failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during formatting: {e}")
            return 1
    
    def _collect_files(
        self,
        files: Optional[List[str]],
        directories: Optional[List[str]]
    ) -> List[str]:
        """Collect files to format.
        
        Args:
            files: List of specific files
            directories: List of directories to scan
            
        Returns:
            List of files to format
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
        
        # File extensions to format
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
    
    def _format_cpp_files(
        self,
        files: List[str],
        check: bool,
        dry_run: bool
    ) -> None:
        """Format C++ files with clang-format.
        
        Args:
            files: List of C++ files
            check: Whether to only check formatting
            dry_run: Whether to run in dry-run mode
            
        Raises:
            CommandError: If formatting fails
        """
        # Check if clang-format is available
        if not shutil.which("clang-format"):
            self.logger.warning("clang-format not found, skipping C++ formatting")
            return
        
        # Build clang-format command
        cmd = ["clang-format"]
        
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
                check=False
            )
            
            if result.returncode != 0:
                raise CommandError(
                    f"clang-format failed with exit code {result.returncode}",
                    {
                        "return_code": result.returncode,
                        "stderr": result.stderr
                    }
                )
            
            if check and result.stdout:
                self.logger.warning("C++ files need formatting")
            
        except FileNotFoundError:
            raise CommandError("clang-format executable not found")
        except Exception as e:
            raise CommandError(f"Failed to run clang-format: {e}")
    
    def _format_python_files(
        self,
        files: List[str],
        check: bool,
        dry_run: bool
    ) -> None:
        """Format Python files with black.
        
        Args:
            files: List of Python files
            check: Whether to only check formatting
            dry_run: Whether to run in dry-run mode
            
        Raises:
            CommandError: If formatting fails
        """
        # Check if black is available
        if not shutil.which("black"):
            self.logger.warning("black not found, skipping Python formatting")
            return
        
        # Build black command
        cmd = ["black"]
        
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
                check=False
            )
            
            if result.returncode != 0:
                raise CommandError(
                    f"black failed with exit code {result.returncode}",
                    {
                        "return_code": result.returncode,
                        "stderr": result.stderr
                    }
                )
            
            if check and result.stdout:
                self.logger.warning("Python files need formatting")
            
        except FileNotFoundError:
            raise CommandError("black executable not found")
        except Exception as e:
            raise CommandError(f"Failed to run black: {e}")
