"""
Core utilities for OmniCPP build system.

This package provides core utilities including configuration management,
logging, terminal detection and invocation, platform detection,
exception handling, and file operations.
"""

from core.config_manager import ConfigManager
from core.logger import Logger
from core.terminal_detector import TerminalDetector, TerminalInfo
from core.terminal_invoker import TerminalInvoker, ExecutionResult
from core.platform_detector import PlatformDetector, CompilerInfo
from core.exception_handler import (
    OmniCppException,
    ConfigurationError,
    BuildError,
    DependencyError,
    CompilerError,
    PlatformError,
    TerminalError,
    CommandError,
    ValidationError,
    FileNotFoundError,
    PermissionError,
    format_exception,
    get_error_code,
)
from core.file_utils import (
    ensure_directory,
    copy_file,
    copy_directory,
    delete_file,
    delete_directory,
    hash_file,
    create_temp_directory,
    create_temp_file,
    file_exists,
    directory_exists,
    get_file_size,
    list_files,
    list_directories,
    normalize_path,
    join_paths,
    get_relative_path,
    get_absolute_path,
    read_text_file,
    write_text_file,
    get_file_extension,
    change_extension,
    is_executable,
    make_executable,
)

__all__ = [
    # Config
    "ConfigManager",
    # Logger
    "Logger",
    # Terminal
    "TerminalDetector",
    "TerminalInfo",
    "TerminalInvoker",
    "ExecutionResult",
    # Platform
    "PlatformDetector",
    "CompilerInfo",
    # Exceptions
    "OmniCppException",
    "ConfigurationError",
    "BuildError",
    "DependencyError",
    "CompilerError",
    "PlatformError",
    "TerminalError",
    "CommandError",
    "ValidationError",
    "FileNotFoundError",
    "PermissionError",
    "format_exception",
    "get_error_code",
    # File utils
    "ensure_directory",
    "copy_file",
    "copy_directory",
    "delete_file",
    "delete_directory",
    "hash_file",
    "create_temp_directory",
    "create_temp_file",
    "file_exists",
    "directory_exists",
    "get_file_size",
    "list_files",
    "list_directories",
    "normalize_path",
    "join_paths",
    "get_relative_path",
    "get_absolute_path",
    "read_text_file",
    "write_text_file",
    "get_file_extension",
    "change_extension",
    "is_executable",
    "make_executable",
]
