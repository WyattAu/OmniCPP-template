# ADR-021: Secure Terminal Invocation

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Security

---

## Context

The OmniCPP Template project invokes terminal commands for building, testing, and other operations. Secure terminal invocation is critical for security and reliability. The threat model (`.specs/03_threat_model/analysis.md`) identifies command injection as a significant threat (TM-017, TM-018).

### Current State

Terminal invocation is inconsistent:
- **No Validation:** No validation of terminal commands
- **No Sanitization:** No sanitization of command arguments
- **No Logging:** No logging of terminal commands
- **No Error Handling:** No proper error handling
- **No Timeout:** No timeout for terminal commands
- **No Resource Limits:** No resource limits for terminal commands

### Issues

1. **No Validation:** No validation of terminal commands
2. **No Sanitization:** No sanitization of command arguments
3. **No Logging:** No logging of terminal commands
4. **No Error Handling:** No proper error handling
5. **No Timeout:** No timeout for terminal commands
6. **No Resource Limits:** No resource limits for terminal commands
7. **Injection Risk:** Risk of command injection

## Decision

Implement **secure terminal invocation** with:
1. **Command Validation:** Validate all terminal commands
2. **Argument Sanitization:** Sanitize all command arguments
3. **Command Logging:** Log all terminal commands
4. **Error Handling:** Proper error handling for terminal commands
5. **Timeout:** Timeout for terminal commands
6. **Resource Limits:** Resource limits for terminal commands
7. **Whitelist:** Whitelist of allowed commands

### 1. Secure Terminal Invoker

```python
# omni_scripts/utils/secure_terminal_invoker.py
"""Secure terminal invoker for safe command execution."""

import subprocess
import shlex
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import signal
import resource
import os

from exceptions import SecurityError, CommandError

@dataclass
class CommandResult:
    """Result of command execution."""

    returncode: int
    stdout: str
    stderr: str
    success: bool
    timed_out: bool

    @property
    def output(self) -> str:
        """Get combined output."""
        return self.stdout + self.stderr

class SecureTerminalInvoker:
    """Secure terminal invoker for safe command execution."""

    # Whitelist of allowed commands
    ALLOWED_COMMANDS = {
        # Build commands
        "cmake",
        "ninja",
        "make",
        "gcc",
        "g++",
        "clang",
        "clang++",
        "cl",
        # Package managers
        "conan",
        "vcpkg",
        "pip",
        # Testing
        "ctest",
        "pytest",
        # Utilities
        "git",
        "python",
        "python3",
        # Platform-specific
        "cmd",
        "powershell",
        "bash",
        "sh",
    }

    # Maximum command execution time (seconds)
    DEFAULT_TIMEOUT = 300  # 5 minutes

    # Maximum memory usage (MB)
    DEFAULT_MEMORY_LIMIT = 1024  # 1 GB

    def __init__(
        self,
        logger: logging.Logger,
        timeout: int = DEFAULT_TIMEOUT,
        memory_limit: int = DEFAULT_MEMORY_LIMIT
    ):
        """Initialize secure terminal invoker.

        Args:
            logger: Logger instance
            timeout: Maximum command execution time (seconds)
            memory_limit: Maximum memory usage (MB)
        """
        self.logger = logger
        self.timeout = timeout
        self.memory_limit = memory_limit

    def invoke(
        self,
        command: str,
        args: Optional[List[str]] = None,
        cwd: Optional[Path] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        check: bool = True
    ) -> CommandResult:
        """Invoke terminal command securely.

        Args:
            command: Command to execute
            args: Command arguments
            cwd: Working directory
            env: Environment variables
            timeout: Command timeout (seconds)
            capture_output: Capture command output
            check: Raise exception on non-zero exit code

        Returns:
            Command result

        Raises:
            SecurityError: If command is not allowed
            CommandError: If command fails
        """
        # Validate command
        self._validate_command(command)

        # Sanitize arguments
        sanitized_args = self._sanitize_args(args or [])

        # Build command list
        cmd_list = [command] + sanitized_args

        # Log command
        self._log_command(cmd_list, cwd, env)

        # Set timeout
        cmd_timeout = timeout or self.timeout

        # Set resource limits
        self._set_resource_limits()

        try:
            # Execute command
            result = subprocess.run(
                cmd_list,
                cwd=cwd,
                env=env,
                timeout=cmd_timeout,
                capture_output=capture_output,
                text=True,
                check=False
            )

            # Create command result
            command_result = CommandResult(
                returncode=result.returncode,
                stdout=result.stdout if capture_output else "",
                stderr=result.stderr if capture_output else "",
                success=result.returncode == 0,
                timed_out=False
            )

            # Check return code
            if check and result.returncode != 0:
                raise CommandError(
                    f"Command failed with exit code {result.returncode}: {command}",
                    command_result
                )

            # Log result
            self._log_result(command_result)

            return command_result

        except subprocess.TimeoutExpired as e:
            # Log timeout
            self.logger.error(f"Command timed out after {cmd_timeout} seconds: {command}")

            # Create timeout result
            command_result = CommandResult(
                returncode=-1,
                stdout=e.stdout if e.stdout else "",
                stderr=e.stderr if e.stderr else "",
                success=False,
                timed_out=True
            )

            raise CommandError(
                f"Command timed out after {cmd_timeout} seconds: {command}",
                command_result
            )

        except Exception as e:
            # Log error
            self.logger.error(f"Command execution failed: {command}: {e}")

            # Create error result
            command_result = CommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
                success=False,
                timed_out=False
            )

            raise CommandError(
                f"Command execution failed: {command}: {e}",
                command_result
            )

    def _validate_command(self, command: str) -> None:
        """Validate command.

        Args:
            command: Command to validate

        Raises:
            SecurityError: If command is not allowed
        """
        # Extract command name
        command_name = command.split()[0]

        # Check if command is allowed
        if command_name not in self.ALLOWED_COMMANDS:
            raise SecurityError(
                f"Command not allowed: {command_name}. "
                f"Allowed commands: {', '.join(sorted(self.ALLOWED_COMMANDS))}"
            )

        # Check for command injection
        if ";" in command or "|" in command or "&" in command:
            raise SecurityError(
                f"Command injection detected: {command}"
            )

    def _sanitize_args(self, args: List[str]) -> List[str]:
        """Sanitize command arguments.

        Args:
            args: Command arguments

        Returns:
            Sanitized arguments
        """
        sanitized = []

        for arg in args:
            # Check for shell metacharacters
            if any(char in arg for char in [";", "|", "&", "$", "`", "\\", "\n"]):
                raise SecurityError(
                    f"Shell metacharacter detected in argument: {arg}"
                )

            # Quote argument if necessary
            if " " in arg or '"' in arg or "'" in arg:
                arg = shlex.quote(arg)

            sanitized.append(arg)

        return sanitized

    def _log_command(
        self,
        cmd_list: List[str],
        cwd: Optional[Path],
        env: Optional[Dict[str, str]]
    ) -> None:
        """Log command.

        Args:
            cmd_list: Command list
            cwd: Working directory
            env: Environment variables
        """
        # Build command string
        cmd_str = " ".join(shlex.quote(arg) for arg in cmd_list)

        # Log command
        self.logger.info(f"Executing command: {cmd_str}")

        # Log working directory
        if cwd:
            self.logger.debug(f"Working directory: {cwd}")

        # Log environment variables (sanitized)
        if env:
            # Sanitize environment variables
            sanitized_env = {
                k: v for k, v in env.items()
                if not any(sensitive in k.lower() for sensitive in ["password", "token", "secret", "key"])
            }
            self.logger.debug(f"Environment variables: {sanitized_env}")

    def _log_result(self, result: CommandResult) -> None:
        """Log command result.

        Args:
            result: Command result
        """
        # Log return code
        self.logger.info(f"Command return code: {result.returncode}")

        # Log stdout
        if result.stdout:
            self.logger.debug(f"Command stdout:\n{result.stdout}")

        # Log stderr
        if result.stderr:
            self.logger.debug(f"Command stderr:\n{result.stderr}")

    def _set_resource_limits(self) -> None:
        """Set resource limits for command execution."""
        try:
            # Set memory limit
            resource.setrlimit(
                resource.RLIMIT_AS,
                (self.memory_limit * 1024 * 1024, self.memory_limit * 1024 * 1024)
            )
        except (ValueError, resource.error) as e:
            self.logger.warning(f"Failed to set resource limits: {e}")
```

### 2. Command Whitelist Manager

```python
# omni_scripts/utils/command_whitelist.py
"""Command whitelist manager for secure terminal invocation."""

import json
from pathlib import Path
from typing import Set, Dict, List
import logging

from exceptions import SecurityError

class CommandWhitelistManager:
    """Command whitelist manager for secure terminal invocation."""

    def __init__(self, logger: logging.Logger, whitelist_file: Optional[Path] = None):
        """Initialize command whitelist manager.

        Args:
            logger: Logger instance
            whitelist_file: Path to whitelist file
        """
        self.logger = logger
        self.whitelist_file = whitelist_file
        self.whitelist: Set[str] = set()

        # Load whitelist
        if whitelist_file and whitelist_file.exists():
            self.load_whitelist(whitelist_file)

    def load_whitelist(self, whitelist_file: Path) -> None:
        """Load whitelist from file.

        Args:
            whitelist_file: Path to whitelist file
        """
        self.logger.info(f"Loading whitelist from {whitelist_file}")

        with open(whitelist_file, 'r') as f:
            whitelist_data = json.load(f)

        # Load allowed commands
        self.whitelist = set(whitelist_data.get("allowed_commands", []))

        self.logger.info(f"Loaded {len(self.whitelist)} allowed commands")

    def save_whitelist(self, whitelist_file: Path) -> None:
        """Save whitelist to file.

        Args:
            whitelist_file: Path to whitelist file
        """
        self.logger.info(f"Saving whitelist to {whitelist_file}")

        whitelist_data = {
            "allowed_commands": sorted(self.whitelist)
        }

        with open(whitelist_file, 'w') as f:
            json.dump(whitelist_data, f, indent=2)

    def add_command(self, command: str) -> None:
        """Add command to whitelist.

        Args:
            command: Command to add
        """
        self.logger.info(f"Adding command to whitelist: {command}")
        self.whitelist.add(command)

    def remove_command(self, command: str) -> None:
        """Remove command from whitelist.

        Args:
            command: Command to remove
        """
        self.logger.info(f"Removing command from whitelist: {command}")
        self.whitelist.discard(command)

    def is_allowed(self, command: str) -> bool:
        """Check if command is allowed.

        Args:
            command: Command to check

        Returns:
            True if allowed, False otherwise
        """
        command_name = command.split()[0]
        return command_name in self.whitelist

    def get_allowed_commands(self) -> Set[str]:
        """Get allowed commands.

        Returns:
            Set of allowed commands
        """
        return self.whitelist.copy()
```

### 3. Usage Examples

```python
# Example usage
from utils.secure_terminal_invoker import SecureTerminalInvoker, CommandResult
from utils.command_whitelist import CommandWhitelistManager
from logging.logger import Logger

# Initialize logger
logger = Logger()

# Initialize secure terminal invoker
invoker = SecureTerminalInvoker(
    logger=logger,
    timeout=300,
    memory_limit=1024
)

# Execute command
result = invoker.invoke(
    command="cmake",
    args=["--version"],
    capture_output=True,
    check=True
)

print(f"Return code: {result.returncode}")
print(f"Output: {result.output}")

# Execute command with timeout
try:
    result = invoker.invoke(
        command="cmake",
        args=["--build", "build"],
        cwd=Path("build"),
        timeout=600,
        check=True
    )
except CommandError as e:
    logger.error(f"Command failed: {e}")
    print(f"Return code: {e.result.returncode}")
    print(f"Output: {e.result.output}")

# Initialize command whitelist manager
whitelist_manager = CommandWhitelistManager(
    logger=logger,
    whitelist_file=Path("config/command_whitelist.json")
)

# Add command to whitelist
whitelist_manager.add_command("cmake")

# Check if command is allowed
if whitelist_manager.is_allowed("cmake"):
    print("cmake is allowed")

# Save whitelist
whitelist_manager.save_whitelist(Path("config/command_whitelist.json"))
```

### 4. Configuration

```json
{
  "allowed_commands": [
    "cmake",
    "ninja",
    "make",
    "gcc",
    "g++",
    "clang",
    "clang++",
    "cl",
    "conan",
    "vcpkg",
    "pip",
    "ctest",
    "pytest",
    "git",
    "python",
    "python3",
    "cmd",
    "powershell",
    "bash",
    "sh"
  ],
  "timeout": 300,
  "memory_limit": 1024
}
```

## Consequences

### Positive

1. **Security:** Prevents command injection
2. **Validation:** Validates all terminal commands
3. **Sanitization:** Sanitizes all command arguments
4. **Logging:** Logs all terminal commands
5. **Error Handling:** Proper error handling for terminal commands
6. **Timeout:** Timeout for terminal commands
7. **Resource Limits:** Resource limits for terminal commands
8. **Whitelist:** Whitelist of allowed commands

### Negative

1. **Complexity:** More complex than direct invocation
2. **Overhead:** Validation and sanitization add overhead
3. **Maintenance:** Whitelist needs to be maintained
4. **Flexibility:** Less flexible than direct invocation

### Neutral

1. **Documentation:** Requires documentation for secure invocation
2. **Testing:** Need to test secure invocation

## Alternatives Considered

### Alternative 1: Direct Invocation

**Description:** Direct invocation of terminal commands

**Pros:**
- Simpler implementation
- No overhead
- More flexible

**Cons:**
- No validation
- No sanitization
- Risk of command injection

**Rejected:** No validation and risk of command injection

### Alternative 2: Shell Invocation

**Description:** Invoke commands through shell

**Pros:**
- Shell features available
- More flexible

**Cons:**
- Higher risk of injection
- More complex
- Platform-specific

**Rejected:** Higher risk of injection and platform-specific

### Alternative 3: External Libraries

**Description:** Use external libraries for secure invocation

**Pros:**
- No custom code
- Proven solutions

**Cons:**
- External dependencies
- Less control
- Platform-specific

**Rejected:** External dependencies and less control

## Related ADRs

- [ADR-010: Terminal invocation patterns for different compilers](ADR-010-terminal-invocation-patterns.md)
- [ADR-011: Compiler detection and selection strategy](ADR-011-compiler-detection-selection.md)
- [ADR-019: Security-first build configuration](ADR-019-security-first-build-configuration.md)

## References

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html)
- [Shell Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
