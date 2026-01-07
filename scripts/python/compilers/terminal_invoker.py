"""
Terminal Invoker

This module provides comprehensive terminal invocation for executing commands
with proper environment setup for compiler-specific operations.
"""

import logging
import os
import subprocess
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


@dataclass
class CommandResult:
    """Command execution result
    
    Attributes:
        exit_code: Exit code from command execution
        stdout: Standard output from command
        stderr: Standard error from command
        environment: Environment variables after execution
        execution_time: Time taken to execute command in seconds
    """
    exit_code: int
    stdout: str
    stderr: str
    environment: Dict[str, str] = field(default_factory=dict)
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "environment": self.environment,
            "execution_time": self.execution_time
        }

    @property
    def success(self) -> bool:
        """Check if command succeeded"""
        return self.exit_code == 0


@dataclass
class CompilerInfo:
    """Compiler information for environment setup
    
    Attributes:
        compiler_type: Type of compiler (msvc, msvc_clang, mingw_gcc, mingw_clang)
        version: Compiler version
        path: Path to compiler executable
        architecture: Target architecture (x64, x86, arm, arm64)
        metadata: Additional compiler metadata
    """
    compiler_type: str
    version: str
    path: str
    architecture: str
    metadata: Dict[str, str] = field(default_factory=dict)


class TerminalInvoker:
    """Invoker for executing commands in terminals with proper environment setup"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize terminal invoker
        
        Args:
            logger: Logger instance for logging operations
        """
        self._logger = logger or logging.getLogger(__name__)
        self._environment: Dict[str, str] = {}
        self._original_environment: Dict[str, str] = {}
        self._terminal_info: Optional[Any] = None

    def execute_command(
        self,
        command: str,
        timeout: int = 300,
        cwd: Optional[str] = None
    ) -> CommandResult:
        """
        Execute a command in the terminal
        
        Args:
            command: Command to execute
            timeout: Command timeout in seconds (default: 300)
            cwd: Working directory for command execution (optional)
            
        Returns:
            Command execution result
            
        Raises:
            ValueError: If command is empty
        """
        if not command or not command.strip():
            raise ValueError("Command cannot be empty")

        self._logger.info(f"Executing command: {command}")
        start_time = time.time()

        try:
            # Prepare environment
            env = self._environment if self._environment else dict(os.environ)

            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=cwd
            )

            execution_time = time.time() - start_time

            command_result = CommandResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                environment=dict(os.environ),
                execution_time=execution_time
            )

            if command_result.success:
                self._logger.info(
                    f"Command succeeded in {execution_time:.2f}s"
                )
            else:
                self._logger.error(
                    f"Command failed with exit code {result.returncode} "
                    f"in {execution_time:.2f}s"
                )
                self._logger.debug(f"Command stderr: {result.stderr}")

            return command_result

        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            self._logger.error(
                f"Command timed out after {timeout} seconds"
            )
            return CommandResult(
                exit_code=-1,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
                environment=dict(os.environ),
                execution_time=execution_time
            )

        except FileNotFoundError as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Command not found: {e}")
            return CommandResult(
                exit_code=-1,
                stdout="",
                stderr=f"Command not found: {str(e)}",
                environment=dict(os.environ),
                execution_time=execution_time
            )

        except PermissionError as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Permission denied: {e}")
            return CommandResult(
                exit_code=-1,
                stdout="",
                stderr=f"Permission denied: {str(e)}",
                environment=dict(os.environ),
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Command execution failed: {e}")
            return CommandResult(
                exit_code=-1,
                stdout="",
                stderr=f"Command execution failed: {str(e)}",
                environment=dict(os.environ),
                execution_time=execution_time
            )

    def setup_environment(self, compiler_info: CompilerInfo) -> Dict[str, str]:
        """
        Setup environment for compiler
        
        Args:
            compiler_info: Compiler information
            
        Returns:
            Environment variables after setup
            
        Raises:
            ValueError: If compiler type is not supported
        """
        self._logger.info(
            f"Setting up environment for {compiler_info.compiler_type} "
            f"{compiler_info.architecture}"
        )

        # Save original environment
        self._original_environment = dict(os.environ)

        # Setup environment based on compiler type
        if compiler_info.compiler_type == "msvc":
            self._setup_msvc_environment(compiler_info)
        elif compiler_info.compiler_type == "msvc_clang":
            self._setup_msvc_clang_environment(compiler_info)
        elif compiler_info.compiler_type == "mingw_gcc":
            self._setup_mingw_gcc_environment(compiler_info)
        elif compiler_info.compiler_type == "mingw_clang":
            self._setup_mingw_clang_environment(compiler_info)
        else:
            raise ValueError(
                f"Unsupported compiler type: {compiler_info.compiler_type}"
            )

        # Capture environment after setup
        self._environment = dict(os.environ)

        self._logger.info("Environment setup complete")
        return self._environment

    def capture_environment(self) -> Dict[str, str]:
        """
        Capture current environment
        
        Returns:
            Current environment variables
        """
        self._logger.debug("Capturing current environment")
        return dict(os.environ)

    def restore_environment(self, env: Dict[str, str]) -> None:
        """
        Restore environment to previous state
        
        Args:
            env: Environment variables to restore
        """
        self._logger.debug("Restoring environment")
        os.environ.clear()
        os.environ.update(env)
        self._environment = env
        self._logger.debug("Environment restored")

    def execute_batch_file(
        self,
        batch_file: str,
        args: List[str],
        timeout: int = 300
    ) -> CommandResult:
        """
        Execute a batch file
        
        Args:
            batch_file: Path to batch file
            args: Arguments to pass to batch file
            timeout: Command timeout in seconds (default: 300)
            
        Returns:
            Command execution result
            
        Raises:
            FileNotFoundError: If batch file does not exist
            ValueError: If batch file path is empty
        """
        if not batch_file or not batch_file.strip():
            raise ValueError("Batch file path cannot be empty")

        if not os.path.exists(batch_file):
            raise FileNotFoundError(f"Batch file not found: {batch_file}")

        self._logger.info(f"Executing batch file: {batch_file}")

        # Build command with arguments
        args_str = " ".join(f'"{arg}"' if " " in arg else arg for arg in args)
        command = f'"{batch_file}" {args_str}'

        return self.execute_command(command, timeout=timeout)

    def _setup_msvc_environment(self, compiler_info: CompilerInfo) -> None:
        """
        Setup MSVC environment
        
        Args:
            compiler_info: Compiler information
        """
        self._logger.debug("Setting up MSVC environment")

        # Find vcvarsall.bat
        vcvarsall_path = self._find_vcvarsall(compiler_info.path)

        if not vcvarsall_path:
            self._logger.warning("vcvarsall.bat not found, skipping MSVC environment setup")
            return

        # Execute vcvarsall.bat with architecture
        architecture = compiler_info.architecture
        self._logger.debug(f"Executing vcvarsall.bat with architecture: {architecture}")

        # Map architecture to vcvarsall argument
        arch_map = {
            "x64": "x64",
            "x86": "x86",
            "arm": "arm",
            "arm64": "arm64"
        }

        arch_arg = arch_map.get(architecture, "x64")

        # Execute vcvarsall.bat and capture environment
        result = self.execute_batch_file(vcvarsall_path, [arch_arg])

        if result.success:
            self._logger.info("MSVC environment setup successful")
        else:
            self._logger.warning(
                f"MSVC environment setup may have failed: {result.stderr}"
            )

    def _setup_msvc_clang_environment(self, compiler_info: CompilerInfo) -> None:
        """
        Setup MSVC-Clang environment
        
        Args:
            compiler_info: Compiler information
        """
        self._logger.debug("Setting up MSVC-Clang environment")

        # Setup MSVC environment first
        self._setup_msvc_environment(compiler_info)

        # Add LLVM to PATH
        llvm_path = os.path.dirname(compiler_info.path)
        if os.path.exists(llvm_path):
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{llvm_path};{current_path}"
            os.environ["LLVM_DIR"] = llvm_path
            self._logger.debug(f"Added LLVM to PATH: {llvm_path}")
        else:
            self._logger.warning(f"LLVM path not found: {llvm_path}")

    def _setup_mingw_gcc_environment(self, compiler_info: CompilerInfo) -> None:
        """
        Setup MinGW-GCC environment
        
        Args:
            compiler_info: Compiler information
        """
        self._logger.debug("Setting up MinGW-GCC environment")

        # Get MSYS2 path from metadata
        msys2_path = compiler_info.metadata.get("msys2_path", "")
        environment = compiler_info.metadata.get("environment", "UCRT64")

        if not msys2_path:
            self._logger.warning(
                "MSYS2 path not found in metadata, "
                "skipping MinGW-GCC environment setup"
            )
            return

        if not os.path.exists(msys2_path):
            self._logger.warning(
                f"MSYS2 path does not exist: {msys2_path}"
            )
            return

        # Set MSYSTEM
        os.environ["MSYSTEM"] = environment
        self._logger.debug(f"Set MSYSTEM={environment}")

        # Set MINGW_PREFIX based on environment
        prefix_map = {
            "UCRT64": "/ucrt64",
            "MINGW64": "/mingw64",
            "MINGW32": "/mingw32",
            "MSYS": "/usr",
            "CLANG64": "/clang64"
        }

        mingw_prefix = prefix_map.get(environment, "/usr")
        os.environ["MINGW_PREFIX"] = mingw_prefix
        self._logger.debug(f"Set MINGW_PREFIX={mingw_prefix}")

        # Add environment-specific bin directory to PATH
        env_bin_path = os.path.join(msys2_path, environment.lower(), "bin")
        usr_bin_path = os.path.join(msys2_path, "usr", "bin")

        if os.path.exists(env_bin_path):
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{env_bin_path};{usr_bin_path};{current_path}"
            self._logger.debug(f"Added {environment} bin to PATH: {env_bin_path}")
        else:
            self._logger.warning(f"Environment bin path not found: {env_bin_path}")

    def _setup_mingw_clang_environment(self, compiler_info: CompilerInfo) -> None:
        """
        Setup MinGW-Clang environment
        
        Args:
            compiler_info: Compiler information
        """
        self._logger.debug("Setting up MinGW-Clang environment")

        # Setup MinGW environment first
        self._setup_mingw_gcc_environment(compiler_info)

        # Add LLVM to PATH
        llvm_path = os.path.dirname(compiler_info.path)
        if os.path.exists(llvm_path):
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{llvm_path};{current_path}"
            os.environ["LLVM_DIR"] = llvm_path
            self._logger.debug(f"Added LLVM to PATH: {llvm_path}")
        else:
            self._logger.warning(f"LLVM path not found: {llvm_path}")

    def _find_vcvarsall(self, compiler_path: str) -> Optional[str]:
        """
        Find vcvarsall.bat path from compiler path
        
        Args:
            compiler_path: Path to compiler executable
            
        Returns:
            Path to vcvarsall.bat or None if not found
        """
        # Try to find vcvarsall.bat in common locations
        possible_paths = [
            # From compiler path (e.g., cl.exe)
            os.path.join(
                os.path.dirname(compiler_path),
                "..",
                "..",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            # From VS installation
            os.path.join(
                os.path.dirname(compiler_path),
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            # From VC directory
            os.path.join(
                os.path.dirname(compiler_path),
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            )
        ]

        for path in possible_paths:
            if os.path.exists(path):
                self._logger.debug(f"Found vcvarsall.bat: {path}")
                return path

        self._logger.debug("vcvarsall.bat not found")
        return None

    def reset_environment(self) -> None:
        """
        Reset environment to original state
        """
        self._logger.debug("Resetting environment to original state")
        if self._original_environment:
            self.restore_environment(self._original_environment)
        else:
            self._logger.warning("No original environment to restore")
