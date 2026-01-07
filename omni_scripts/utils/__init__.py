# omni_scripts/utils/__init__.py
"""
Shared utilities for OmniCPP project.

This package provides common utilities used across all scripts:
- Exception classes
- Logging functions
- Command execution
- File operations
- System detection
- Path manipulation
"""

# Import exception classes
from .exceptions import (
    CommandExecutionError,
    NotADirectoryError,
    PathValidationError,
)

# Import logging functions
from .logging_utils import (
    log_error,
    log_info,
    log_success,
    log_warning,
)

# Import command execution
from .command_utils import execute_command

# Import platform detection
from .platform_utils import (
    get_workspace_dir,
    get_system_platform,
    is_windows,
    is_linux,
    is_macos,
    get_executable_extension,
    get_library_extension,
)

# Import utility classes
from .file_utils import FileUtils
from .path_utils import PathUtils
from .system_utils import SystemUtils
from .terminal_utils import (
    TerminalEnvironment,
    TerminalSetupError,
    execute_with_terminal_setup,
    setup_terminal_environment,
)

__all__ = [
    # Exceptions
    'CommandExecutionError',
    'NotADirectoryError',
    'PathValidationError',
    # Logging
    'log_error',
    'log_info',
    'log_success',
    'log_warning',
    # Command execution
    'execute_command',
    # Platform detection
    'get_workspace_dir',
    'get_system_platform',
    'is_windows',
    'is_linux',
    'is_macos',
    'get_executable_extension',
    'get_library_extension',
    # Utility classes
    'FileUtils',
    'PathUtils',
    'SystemUtils',
    # Terminal utilities
    'TerminalEnvironment',
    'TerminalSetupError',
    'execute_with_terminal_setup',
    'setup_terminal_environment',
]
