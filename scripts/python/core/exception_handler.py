"""
Exception Handler - Custom exception classes and error handling

This module provides custom exception classes for OmniCPP build system
with detailed error context and user-friendly messages.
"""

from typing import Any, Dict, Optional


class OmniCppException(Exception):
    """Base exception for all OmniCPP errors.
    
    Attributes:
        message: Error message
        context: Additional error context dictionary
    """
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Initialize exception.
        
        Args:
            message: Error message
            context: Additional error context
        """
        super().__init__(message)
        self.message: str = message
        self.context: Optional[Dict[str, Any]] = context or {}
    
    def __str__(self) -> str:
        """String representation of exception."""
        return self.message
    
    def get_context(self) -> Dict[str, Any]:
        """Get error context.
        
        Returns:
            Error context dictionary
        """
        return self.context.copy()


class ConfigurationError(OmniCppException):
    """Configuration-related errors.
    
    Raised when configuration files are missing, invalid, or
    contain unsupported values.
    """
    pass


class BuildError(OmniCppException):
    """Build-related errors.
    
    Raised when build operations fail, including compilation,
    linking, or CMake errors.
    """
    pass


class DependencyError(OmniCppException):
    """Dependency-related errors.
    
    Raised when required dependencies are missing or incompatible.
    """
    pass


class CompilerError(OmniCppException):
    """Compiler-related errors.
    
    Raised when compiler detection, configuration, or invocation fails.
    """
    pass


class PlatformError(OmniCppException):
    """Platform-related errors.
    
    Raised when platform detection or platform-specific operations fail.
    """
    pass


class TerminalError(OmniCppException):
    """Terminal-related errors.
    
    Raised when terminal detection or invocation fails.
    """
    pass


class CommandError(OmniCppException):
    """Command execution errors.
    
    Raised when command execution fails or returns non-zero exit code.
    """
    pass


class ValidationError(OmniCppException):
    """Validation errors.
    
    Raised when input validation fails.
    """
    pass


class FileNotFoundError(OmniCppException):
    """File not found errors.
    
    Raised when required files or directories are missing.
    """
    pass


class PermissionError(OmniCppException):
    """Permission errors.
    
    Raised when file or directory operations fail due to permissions.
    """
    pass


def format_exception(exception: Exception, verbose: bool = False) -> str:
    """Format exception for display.
    
    Args:
        exception: Exception to format
        verbose: Whether to include verbose details
        
    Returns:
        Formatted exception string
    """
    if isinstance(exception, OmniCppException):
        result = f"{exception.__class__.__name__}: {exception.message}"
        
        if exception.context and verbose:
            context_str = ", ".join(
                f"{k}={v}" for k, v in exception.context.items()
            )
            result += f" (Context: {context_str})"
        
        return result
    else:
        if verbose:
            import traceback
            return f"{exception.__class__.__name__}: {exception}\n{traceback.format_exc()}"
        else:
            return f"{exception.__class__.__name__}: {exception}"


def get_error_code(exception: Exception) -> int:
    """Get appropriate error exit code for exception.
    
    Args:
        exception: Exception that occurred
        
    Returns:
        Exit code (1 for general errors, specific codes for known types)
    """
    error_codes = {
        ConfigurationError: 3,
        BuildError: 4,
        DependencyError: 5,
        CompilerError: 6,
        PlatformError: 7,
        TerminalError: 8,
        CommandError: 9,
        ValidationError: 10,
        FileNotFoundError: 11,
        PermissionError: 12,
    }
    
    return error_codes.get(type(exception), 1)
