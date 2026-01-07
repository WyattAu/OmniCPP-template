"""
Terminal Invoker - Execute commands in detected terminals

This module provides terminal invocation with proper environment setup,
command execution, and output capture for OmniCPP build system.
"""

import subprocess
import os
from typing import Optional, Dict, List
from dataclasses import dataclass

from core.terminal_detector import TerminalInfo
from core.exception_handler import TerminalError


@dataclass
class ExecutionResult:
    """Command execution result data class."""
    
    exit_code: int
    stdout: str
    stderr: str
    success: bool


class TerminalInvoker:
    """Execute commands in detected terminals."""
    
    def __init__(self, terminal: TerminalInfo) -> None:
        """Initialize terminal invoker.
        
        Args:
            terminal: Terminal to use
        """
        self.terminal = terminal
        self.system = os.name
    
    def execute(
        self,
        command: str,
        timeout: int = 300,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
        capture_output: bool = True
    ) -> ExecutionResult:
        """Execute command in terminal.
        
        Args:
            command: Command to execute
            timeout: Command timeout in seconds
            env: Environment variables (uses current env if None)
            cwd: Working directory (uses current dir if None)
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Execution result with output and exit code
            
        Raises:
            TerminalError: If terminal invocation fails
        """
        try:
            # Prepare environment
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
            
            # Build command based on terminal type
            if self.terminal.type == "powershell":
                cmd_list = self._build_powershell_command(command)
            elif self.terminal.type == "cmd":
                cmd_list = self._build_cmd_command(command)
            elif self.terminal.type in ["bash", "zsh", "wsl"]:
                cmd_list = self._build_unix_command(command)
            else:
                raise TerminalError(
                    f"Unsupported terminal type: {self.terminal.type}",
                    {"terminal_type": self.terminal.type}
                )
            
            # Execute command
            if capture_output:
                result = subprocess.run(
                    cmd_list,
                    env=process_env,
                    cwd=cwd,
                    timeout=timeout,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                return ExecutionResult(
                    exit_code=result.returncode,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    success=result.returncode == 0
                )
            else:
                subprocess.run(
                    cmd_list,
                    env=process_env,
                    cwd=cwd,
                    timeout=timeout,
                    check=False
                )
                
                return ExecutionResult(
                    exit_code=0,
                    stdout="",
                    stderr="",
                    success=True
                )
                
        except subprocess.TimeoutExpired:
            raise TerminalError(
                f"Command timed out after {timeout} seconds",
                {"command": command, "timeout": timeout}
            )
        except FileNotFoundError as e:
            raise TerminalError(
                f"Terminal executable not found: {e}",
                {"terminal_path": self.terminal.path, "error": str(e)}
            )
        except Exception as e:
            raise TerminalError(
                f"Failed to execute command: {e}",
                {"command": command, "error": str(e)}
            )
    
    def _build_powershell_command(self, command: str) -> List[str]:
        """Build PowerShell command.
        
        Args:
            command: Command to execute
            
        Returns:
            Command list for subprocess
        """
        return [self.terminal.path, "-Command", command]
    
    def _build_cmd_command(self, command: str) -> List[str]:
        """Build CMD command.
        
        Args:
            command: Command to execute
            
        Returns:
            Command list for subprocess
        """
        return [self.terminal.path, "/c", command]
    
    def _build_unix_command(self, command: str) -> List[str]:
        """Build Unix shell command.
        
        Args:
            command: Command to execute
            
        Returns:
            Command list for subprocess
        """
        return [self.terminal.path, "-c", command]
    
    def execute_interactive(
        self,
        command: str,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None
    ) -> int:
        """Execute command in interactive mode.
        
        Args:
            command: Command to execute
            env: Environment variables
            cwd: Working directory
            
        Returns:
            Exit code
        """
        try:
            # Prepare environment
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
            
            # Build command
            if self.terminal.type == "powershell":
                cmd_list = self._build_powershell_command(command)
            elif self.terminal.type == "cmd":
                cmd_list = self._build_cmd_command(command)
            elif self.terminal.type in ["bash", "zsh", "wsl"]:
                cmd_list = self._build_unix_command(command)
            else:
                raise TerminalError(
                    f"Unsupported terminal type: {self.terminal.type}",
                    {"terminal_type": self.terminal.type}
                )
            
            # Execute interactively
            return subprocess.call(
                cmd_list,
                env=process_env,
                cwd=cwd
            )
            
        except Exception as e:
            raise TerminalError(
                f"Failed to execute interactive command: {e}",
                {"command": command, "error": str(e)}
            )
    
    def get_terminal(self) -> TerminalInfo:
        """Get terminal information.
        
        Returns:
            Terminal info
        """
        return self.terminal
