# DES-009: Terminal Invocation Interface

## Overview
Defines the terminal invocation interface for executing commands securely and reliably across different platforms and terminals.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import subprocess
import os
import shlex

class TerminalType(Enum):
    """Terminal types"""
    CMD = "cmd"
    POWERSHELL = "powershell"
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    MSYS2 = "msys2"
    GIT_BASH = "git_bash"
    WSL = "wsl"
    UNKNOWN = "unknown"

class ExecutionResult:
    """Result of command execution"""

    def __init__(self, returncode: int, stdout: str, stderr: str,
                 execution_time: float, command: str) -> None:
        """Initialize execution result"""
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.execution_time = execution_time
        self.command = command

    @property
    def success(self) -> bool:
        """Check if command succeeded"""
        return self.returncode == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "execution_time": self.execution_time,
            "command": self.command,
            "success": self.success
        }

@dataclass
class TerminalConfig:
    """Terminal configuration"""
    terminal_type: TerminalType
    executable: str
    args: List[str]
    env: Dict[str, str]
    working_dir: Optional[str] = None
    timeout: Optional[int] = None
    shell: bool = False
    capture_output: bool = True
    text: bool = True
    encoding: str = "utf-8"
    errors: str = "replace"

class ITerminalInvoker(ABC):
    """Interface for terminal invocation"""

    @abstractmethod
    def execute(self, command: str, config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command in terminal"""
        pass

    @abstractmethod
    def execute_list(self, args: List[str], config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command from argument list"""
        pass

    @abstractmethod
    def execute_interactive(self, command: str, config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command interactively"""
        pass

    @abstractmethod
    def detect_terminal(self) -> TerminalType:
        """Detect current terminal type"""
        pass

    @abstractmethod
    def get_terminal_config(self, terminal_type: TerminalType) -> TerminalConfig:
        """Get terminal configuration for type"""
        pass

    @abstractmethod
    def validate_command(self, command: str) -> bool:
        """Validate command for security"""
        pass

class TerminalInvoker(ITerminalInvoker):
    """Implementation of terminal invoker"""

    def __init__(self, default_timeout: int = 300,
                 default_working_dir: Optional[str] = None) -> None:
        """Initialize terminal invoker"""
        self._default_timeout = default_timeout
        self._default_working_dir = default_working_dir
        self._terminal_cache: Optional[TerminalType] = None
        self._command_whitelist: List[str] = []
        self._command_blacklist: List[str] = []

    def execute(self, command: str, config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command in terminal"""
        import time

        # Validate command
        if not self.validate_command(command):
            raise ValueError(f"Command validation failed: {command}")

        # Get or create config
        if config is None:
            config = self._get_default_config()

        # Sanitize command
        sanitized_command = self._sanitize_command(command)

        # Prepare environment
        env = os.environ.copy()
        env.update(config.env)

        # Execute command
        start_time = time.time()
        try:
            result = subprocess.run(
                sanitized_command,
                shell=config.shell,
                cwd=config.working_dir or self._default_working_dir,
                env=env,
                timeout=config.timeout or self._default_timeout,
                capture_output=config.capture_output,
                text=config.text,
                encoding=config.encoding,
                errors=config.errors
            )
            execution_time = time.time() - start_time

            return ExecutionResult(
                returncode=result.returncode,
                stdout=result.stdout if result.stdout else "",
                stderr=result.stderr if result.stderr else "",
                execution_time=execution_time,
                command=sanitized_command
            )
        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                returncode=-1,
                stdout=e.stdout if e.stdout else "",
                stderr=f"Command timed out after {config.timeout or self._default_timeout} seconds",
                execution_time=execution_time,
                command=sanitized_command
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=sanitized_command
            )

    def execute_list(self, args: List[str], config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command from argument list"""
        # Convert list to command string
        command = " ".join(shlex.quote(arg) for arg in args)
        return self.execute(command, config)

    def execute_interactive(self, command: str, config: Optional[TerminalConfig] = None) -> ExecutionResult:
        """Execute command interactively"""
        import time

        # Validate command
        if not self.validate_command(command):
            raise ValueError(f"Command validation failed: {command}")

        # Get or create config
        if config is None:
            config = self._get_default_config()

        # Sanitize command
        sanitized_command = self._sanitize_command(command)

        # Prepare environment
        env = os.environ.copy()
        env.update(config.env)

        # Execute command interactively
        start_time = time.time()
        try:
            result = subprocess.run(
                sanitized_command,
                shell=config.shell,
                cwd=config.working_dir or self._default_working_dir,
                env=env,
                timeout=config.timeout or self._default_timeout,
                capture_output=False,
                text=False
            )
            execution_time = time.time() - start_time

            return ExecutionResult(
                returncode=result.returncode,
                stdout="",
                stderr="",
                execution_time=execution_time,
                command=sanitized_command
            )
        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                returncode=-1,
                stdout="",
                stderr=f"Command timed out after {config.timeout or self._default_timeout} seconds",
                execution_time=execution_time,
                command=sanitized_command
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=sanitized_command
            )

    def detect_terminal(self) -> TerminalType:
        """Detect current terminal type"""
        if self._terminal_cache:
            return self._terminal_cache

        # Check environment variables
        if os.name == 'nt':
            # Windows
            if 'MSYSTEM' in os.environ:
                self._terminal_cache = TerminalType.MSYS2
            elif 'WT_SESSION' in os.environ:
                self._terminal_cache = TerminalType.POWERSHELL
            elif 'PSModulePath' in os.environ:
                self._terminal_cache = TerminalType.POWERSHELL
            else:
                self._terminal_cache = TerminalType.CMD
        else:
            # Unix-like
            shell = os.environ.get('SHELL', '')
            if 'zsh' in shell:
                self._terminal_cache = TerminalType.ZSH
            elif 'bash' in shell:
                self._terminal_cache = TerminalType.BASH
            elif 'fish' in shell:
                self._terminal_cache = TerminalType.FISH
            elif 'wsl' in shell.lower():
                self._terminal_cache = TerminalType.WSL
            else:
                self._terminal_cache = TerminalType.BASH

        return self._terminal_cache

    def get_terminal_config(self, terminal_type: TerminalType) -> TerminalConfig:
        """Get terminal configuration for type"""
        configs = {
            TerminalType.CMD: TerminalConfig(
                terminal_type=TerminalType.CMD,
                executable="cmd.exe",
                args=["/c"],
                env={},
                shell=True
            ),
            TerminalType.POWERSHELL: TerminalConfig(
                terminal_type=TerminalType.POWERSHELL,
                executable="powershell.exe",
                args=["-Command"],
                env={},
                shell=True
            ),
            TerminalType.BASH: TerminalConfig(
                terminal_type=TerminalType.BASH,
                executable="bash",
                args=["-c"],
                env={},
                shell=True
            ),
            TerminalType.ZSH: TerminalConfig(
                terminal_type=TerminalType.ZSH,
                executable="zsh",
                args=["-c"],
                env={},
                shell=True
            ),
            TerminalType.FISH: TerminalConfig(
                terminal_type=TerminalType.FISH,
                executable="fish",
                args=["-c"],
                env={},
                shell=True
            ),
            TerminalType.MSYS2: TerminalConfig(
                terminal_type=TerminalType.MSYS2,
                executable="bash.exe",
                args=["-c"],
                env={},
                shell=True
            ),
            TerminalType.GIT_BASH: TerminalConfig(
                terminal_type=TerminalType.GIT_BASH,
                executable="bash.exe",
                args=["-c"],
                env={},
                shell=True
            ),
            TerminalType.WSL: TerminalConfig(
                terminal_type=TerminalType.WSL,
                executable="wsl.exe",
                args=["bash", "-c"],
                env={},
                shell=True
            )
        }

        return configs.get(terminal_type, configs[TerminalType.BASH])

    def validate_command(self, command: str) -> bool:
        """Validate command for security"""
        # Check blacklist
        for blacklisted in self._command_blacklist:
            if blacklisted in command.lower():
                return False

        # Check whitelist if configured
        if self._command_whitelist:
            command_parts = command.split()
            if not command_parts:
                return False
            base_command = command_parts[0].lower()
            if base_command not in self._command_whitelist:
                return False

        # Check for dangerous patterns
        dangerous_patterns = [
            "rm -rf /",
            "mkfs",
            "dd if=",
            ":(){ :|:& };:",
            "chmod 777 /",
            "chown -R root"
        ]

        for pattern in dangerous_patterns:
            if pattern in command.lower():
                return False

        return True

    def set_command_whitelist(self, commands: List[str]) -> None:
        """Set command whitelist"""
        self._command_whitelist = [cmd.lower() for cmd in commands]

    def set_command_blacklist(self, commands: List[str]) -> None:
        """Set command blacklist"""
        self._command_blacklist = [cmd.lower() for cmd in commands]

    def clear_cache(self) -> None:
        """Clear terminal cache"""
        self._terminal_cache = None

    def _get_default_config(self) -> TerminalConfig:
        """Get default terminal configuration"""
        terminal_type = self.detect_terminal()
        return self.get_terminal_config(terminal_type)

    def _sanitize_command(self, command: str) -> str:
        """Sanitize command for security"""
        # Remove potentially dangerous characters
        # Note: This is a basic sanitization, more sophisticated checks may be needed

        # Remove null bytes
        command = command.replace('\x00', '')

        # Remove excessive whitespace
        command = ' '.join(command.split())

        return command

class MSVCEnvironmentSetup:
    """Helper for setting up MSVC environment"""

    @staticmethod
    def get_vswhere_path() -> Optional[str]:
        """Get path to vswhere.exe"""
        from shutil import which
        return which("vswhere")

    @staticmethod
    def find_visual_studio_installations() -> List[Dict[str, str]]:
        """Find Visual Studio installations"""
        vswhere_path = MSVCEnvironmentSetup.get_vswhere_path()
        if not vswhere_path:
            return []

        try:
            result = subprocess.run(
                [vswhere_path, "-all", "-format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

        return []

    @staticmethod
    def get_msvc_env_vars(architecture: str = "x64") -> Dict[str, str]:
        """Get MSVC environment variables"""
        installations = MSVCEnvironmentSetup.find_visual_studio_installations()

        if not installations:
            return {}

        # Get latest installation
        latest = max(installations, key=lambda x: x.get('installationVersion', ''))

        # Get vcvarsall.bat path
        vcvars_path = os.path.join(
            latest.get('installationPath', ''),
            'VC',
            'Auxiliary',
            'Build',
            'vcvarsall.bat'
        )

        if not os.path.exists(vcvars_path):
            return {}

        # Execute vcvarsall.bat and capture environment
        try:
            result = subprocess.run(
                f'cmd /c "{vcvars_path}" {architecture} && set',
                capture_output=True,
                text=True,
                timeout=30,
                shell=True
            )

            if result.returncode == 0:
                env_vars = {}
                for line in result.stdout.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key] = value
                return env_vars
        except subprocess.TimeoutExpired:
            pass

        return {}

class MSYS2EnvironmentSetup:
    """Helper for setting up MSYS2 environment"""

    @staticmethod
    def find_msys2_installation() -> Optional[str]:
        """Find MSYS2 installation"""
        # Check common paths
        common_paths = [
            r"C:\msys64",
            r"C:\msys32",
            os.path.expanduser("~/msys64"),
            os.path.expanduser("~/msys32")
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    @staticmethod
    def get_msys2_env_vars() -> Dict[str, str]:
        """Get MSYS2 environment variables"""
        msys2_path = MSYS2EnvironmentSetup.find_msys2_installation()
        if not msys2_path:
            return {}

        return {
            'MSYSTEM': 'UCRT64',
            'MSYS2_PATH_TYPE': 'inherit',
            'MINGW_PREFIX': os.path.join(msys2_path, 'mingw64'),
            'MINGW_CHOST': 'x86_64-w64-mingw32'
        }
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-007` - Platform detection

### External Dependencies
- `subprocess` - Process execution
- `os` - Operating system interface
- `shlex` - Shell lexing
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-011: Terminal Invocation Patterns
- REQ-012: MSVC Developer Command Prompt Integration
- REQ-013: MSYS2 Terminal Integration
- REQ-043: Secure Terminal Invocation

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Terminal Detection Strategy
1. Check environment variables
2. Detect shell type
3. Determine terminal capabilities
4. Cache detection results

### Command Execution Flow
1. Validate command for security
2. Sanitize command
3. Prepare environment
4. Execute with timeout
5. Capture output
6. Return result

### Security Considerations
- Validate all commands before execution
- Use command whitelist/blacklist
- Sanitize command input
- Set appropriate timeouts
- Capture output securely

### Error Handling
- Handle timeouts gracefully
- Provide clear error messages
- Log execution failures
- Return structured results

## Usage Example

```python
from omni_scripts.terminal import TerminalInvoker, TerminalType

# Create invoker
invoker = TerminalInvoker(default_timeout=60)

# Execute command
result = invoker.execute("cmake --version")
if result.success:
    print(f"CMake version: {result.stdout.strip()}")
else:
    print(f"Error: {result.stderr}")

# Execute with custom config
config = TerminalConfig(
    terminal_type=TerminalType.BASH,
    executable="bash",
    args=["-c"],
    env={"MY_VAR": "value"},
    working_dir="/path/to/project"
)
result = invoker.execute("echo $MY_VAR", config)

# Detect terminal
terminal_type = invoker.detect_terminal()
print(f"Terminal type: {terminal_type}")

# Set up MSVC environment
from omni_scripts.terminal import MSVCEnvironmentSetup
env_vars = MSVCEnvironmentSetup.get_msvc_env_vars("x64")
print(f"MSVC env vars: {env_vars}")
```
