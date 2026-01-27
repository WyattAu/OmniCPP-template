# DES-005: Exception Hierarchy Design

## Overview
Defines the exception hierarchy for the OmniCppController system, providing structured error handling and meaningful error messages.

## Exception Hierarchy

### Python Exception Classes

```python
from typing import Optional, Dict, Any
from dataclasses import dataclass
import traceback

class OmniCppException(Exception):
    """Base exception for all OmniCppController exceptions"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize exception with message and optional details"""
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.traceback = traceback.format_exc()

    def __str__(self) -> str:
        """String representation of exception"""
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary"""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "traceback": self.traceback
        }

# Configuration Exceptions
class ConfigurationError(OmniCppException):
    """Base exception for configuration errors"""
    pass

class ConfigurationFileNotFoundError(ConfigurationError):
    """Raised when configuration file is not found"""

    def __init__(self, file_path: str) -> None:
        """Initialize with file path"""
        super().__init__(
            f"Configuration file not found: {file_path}",
            {"file_path": file_path}
        )

class ConfigurationParseError(ConfigurationError):
    """Raised when configuration file cannot be parsed"""

    def __init__(self, file_path: str, parse_error: str) -> None:
        """Initialize with file path and parse error"""
        super().__init__(
            f"Failed to parse configuration file: {file_path}",
            {"file_path": file_path, "parse_error": parse_error}
        )

class ConfigurationValidationError(ConfigurationError):
    """Raised when configuration validation fails"""

    def __init__(self, field: str, value: Any, reason: str) -> None:
        """Initialize with field, value, and reason"""
        super().__init__(
            f"Configuration validation failed for field '{field}'",
            {"field": field, "value": str(value), "reason": reason}
        )

class ConfigurationMissingError(ConfigurationError):
    """Raised when required configuration is missing"""

    def __init__(self, field: str) -> None:
        """Initialize with missing field"""
        super().__init__(
            f"Required configuration field is missing: {field}",
            {"field": field}
        )

# Platform Exceptions
class PlatformError(OmniCppException):
    """Base exception for platform errors"""
    pass

class UnsupportedPlatformError(PlatformError):
    """Raised when platform is not supported"""

    def __init__(self, platform: str) -> None:
        """Initialize with platform name"""
        super().__init__(
            f"Unsupported platform: {platform}",
            {"platform": platform}
        )

class PlatformDetectionError(PlatformError):
    """Raised when platform cannot be detected"""

    def __init__(self, reason: str) -> None:
        """Initialize with reason"""
        super().__init__(
            f"Failed to detect platform: {reason}",
            {"reason": reason}
        )

# Compiler Exceptions
class CompilerError(OmniCppException):
    """Base exception for compiler errors"""
    pass

class CompilerNotFoundError(CompilerError):
    """Raised when compiler is not found"""

    def __init__(self, compiler_type: str) -> None:
        """Initialize with compiler type"""
        super().__init__(
            f"Compiler not found: {compiler_type}",
            {"compiler_type": compiler_type}
        )

class CompilerVersionError(CompilerError):
    """Raised when compiler version is incompatible"""

    def __init__(self, compiler_type: str, required_version: str, actual_version: str) -> None:
        """Initialize with compiler type and versions"""
        super().__init__(
            f"Compiler version mismatch for {compiler_type}",
            {
                "compiler_type": compiler_type,
                "required_version": required_version,
                "actual_version": actual_version
            }
        )

class CompilerExecutionError(CompilerError):
    """Raised when compiler execution fails"""

    def __init__(self, compiler_type: str, command: str, exit_code: int, output: str) -> None:
        """Initialize with compiler details"""
        super().__init__(
            f"Compiler execution failed: {compiler_type}",
            {
                "compiler_type": compiler_type,
                "command": command,
                "exit_code": exit_code,
                "output": output
            }
        )

class CompilerDetectionError(CompilerError):
    """Raised when compiler cannot be detected"""

    def __init__(self, reason: str) -> None:
        """Initialize with reason"""
        super().__init__(
            f"Failed to detect compiler: {reason}",
            {"reason": reason}
        )

# Build System Exceptions
class BuildSystemError(OmniCppException):
    """Base exception for build system errors"""
    pass

class BuildConfigurationError(BuildSystemError):
    """Raised when build configuration fails"""

    def __init__(self, reason: str) -> None:
        """Initialize with reason"""
        super().__init__(
            f"Build configuration failed: {reason}",
            {"reason": reason}
        )

class BuildExecutionError(BuildSystemError):
    """Raised when build execution fails"""

    def __init__(self, target: str, exit_code: int, output: str) -> None:
        """Initialize with target and error details"""
        super().__init__(
            f"Build execution failed for target: {target}",
            {
                "target": target,
                "exit_code": exit_code,
                "output": output
            }
        )

class BuildDependencyError(BuildSystemError):
    """Raised when build dependency is missing"""

    def __init__(self, dependency: str) -> None:
        """Initialize with dependency name"""
        super().__init__(
            f"Build dependency not found: {dependency}",
            {"dependency": dependency}
        )

class CMakeNotFoundError(BuildSystemError):
    """Raised when CMake is not found"""

    def __init__(self) -> None:
        """Initialize"""
        super().__init__(
            "CMake not found",
            {}
        )

class CMakeVersionError(BuildSystemError):
    """Raised when CMake version is incompatible"""

    def __init__(self, required_version: str, actual_version: str) -> None:
        """Initialize with versions"""
        super().__init__(
            "CMake version mismatch",
            {
                "required_version": required_version,
                "actual_version": actual_version
            }
        )

# Package Manager Exceptions
class PackageManagerError(OmniCppException):
    """Base exception for package manager errors"""
    pass

class PackageManagerNotFoundError(PackageManagerError):
    """Raised when package manager is not found"""

    def __init__(self, package_manager: str) -> None:
        """Initialize with package manager name"""
        super().__init__(
            f"Package manager not found: {package_manager}",
            {"package_manager": package_manager}
        )

class PackageNotFoundError(PackageManagerError):
    """Raised when package is not found"""

    def __init__(self, package_name: str, package_manager: str) -> None:
        """Initialize with package name and manager"""
        super().__init__(
            f"Package not found: {package_name}",
            {
                "package_name": package_name,
                "package_manager": package_manager
            }
        )

class PackageInstallationError(PackageManagerError):
    """Raised when package installation fails"""

    def __init__(self, package_name: str, package_manager: str, reason: str) -> None:
        """Initialize with package details"""
        super().__init__(
            f"Package installation failed: {package_name}",
            {
                "package_name": package_name,
                "package_manager": package_manager,
                "reason": reason
            }
        )

class PackageDependencyError(PackageManagerError):
    """Raised when package dependency cannot be resolved"""

    def __init__(self, package_name: str, dependency: str) -> None:
        """Initialize with package and dependency"""
        super().__init__(
            f"Package dependency error: {package_name}",
            {
                "package_name": package_name,
                "dependency": dependency
            }
        )

# Terminal Exceptions
class TerminalError(OmniCppException):
    """Base exception for terminal errors"""
    pass

class TerminalNotFoundError(TerminalError):
    """Raised when terminal is not found"""

    def __init__(self, terminal_type: str) -> None:
        """Initialize with terminal type"""
        super().__init__(
            f"Terminal not found: {terminal_type}",
            {"terminal_type": terminal_type}
        )

class TerminalExecutionError(TerminalError):
    """Raised when terminal command execution fails"""

    def __init__(self, command: str, exit_code: int, output: str) -> None:
        """Initialize with command details"""
        super().__init__(
            f"Terminal command execution failed",
            {
                "command": command,
                "exit_code": exit_code,
                "output": output
            }
        )

class TerminalTimeoutError(TerminalError):
    """Raised when terminal command times out"""

    def __init__(self, command: str, timeout: int) -> None:
        """Initialize with command and timeout"""
        super().__init__(
            f"Terminal command timed out",
            {
                "command": command,
                "timeout": timeout
            }
        )

# Controller Exceptions
class ControllerError(OmniCppException):
    """Base exception for controller errors"""
    pass

class ControllerNotFoundError(ControllerError):
    """Raised when controller is not found"""

    def __init__(self, controller_name: str) -> None:
        """Initialize with controller name"""
        super().__init__(
            f"Controller not found: {controller_name}",
            {"controller_name": controller_name}
        )

class ControllerExecutionError(ControllerError):
    """Raised when controller execution fails"""

    def __init__(self, controller_name: str, reason: str) -> None:
        """Initialize with controller name and reason"""
        super().__init__(
            f"Controller execution failed: {controller_name}",
            {
                "controller_name": controller_name,
                "reason": reason
            }
        )

class InvalidArgumentError(ControllerError):
    """Raised when controller receives invalid arguments"""

    def __init__(self, controller_name: str, argument: str, reason: str) -> None:
        """Initialize with argument details"""
        super().__init__(
            f"Invalid argument for controller: {controller_name}",
            {
                "controller_name": controller_name,
                "argument": argument,
                "reason": reason
            }
        )

# Testing Exceptions
class TestingError(OmniCppException):
    """Base exception for testing errors"""
    pass

class TestExecutionError(TestingError):
    """Raised when test execution fails"""

    def __init__(self, test_name: str, exit_code: int, output: str) -> None:
        """Initialize with test details"""
        super().__init__(
            f"Test execution failed: {test_name}",
            {
                "test_name": test_name,
                "exit_code": exit_code,
                "output": output
            }
        )

class TestNotFoundError(TestingError):
    """Raised when test is not found"""

    def __init__(self, test_name: str) -> None:
        """Initialize with test name"""
        super().__init__(
            f"Test not found: {test_name}",
            {"test_name": test_name}
        )

class TestTimeoutError(TestingError):
    """Raised when test times out"""

    def __init__(self, test_name: str, timeout: int) -> None:
        """Initialize with test name and timeout"""
        super().__init__(
            f"Test timed out: {test_name}",
            {
                "test_name": test_name,
                "timeout": timeout
            }
        )

# Formatting Exceptions
class FormattingError(OmniCppException):
    """Base exception for formatting errors"""
    pass

class FormatterNotFoundError(FormattingError):
    """Raised when formatter is not found"""

    def __init__(self, formatter_type: str) -> None:
        """Initialize with formatter type"""
        super().__init__(
            f"Formatter not found: {formatter_type}",
            {"formatter_type": formatter_type}
        )

class FormattingExecutionError(FormattingError):
    """Raised when formatting execution fails"""

    def __init__(self, formatter_type: str, file_path: str, reason: str) -> None:
        """Initialize with formatting details"""
        super().__init__(
            f"Formatting execution failed: {formatter_type}",
            {
                "formatter_type": formatter_type,
                "file_path": file_path,
                "reason": reason
            }
        )

# Linting Exceptions
class LintingError(OmniCppException):
    """Base exception for linting errors"""
    pass

class LinterNotFoundError(LintingError):
    """Raised when linter is not found"""

    def __init__(self, linter_type: str) -> None:
        """Initialize with linter type"""
        super().__init__(
            f"Linter not found: {linter_type}",
            {"linter_type": linter_type}
        )

class LintingExecutionError(LintingError):
    """Raised when linting execution fails"""

    def __init__(self, linter_type: str, file_path: str, reason: str) -> None:
        """Initialize with linting details"""
        super().__init__(
            f"Linting execution failed: {linter_type}",
            {
                "linter_type": linter_type,
                "file_path": file_path,
                "reason": reason
            }
        )

# Security Exceptions
class SecurityError(OmniCppException):
    """Base exception for security errors"""
    pass

class SecurityValidationError(SecurityError):
    """Raised when security validation fails"""

    def __init__(self, resource: str, reason: str) -> None:
        """Initialize with resource and reason"""
        super().__init__(
            f"Security validation failed: {resource}",
            {
                "resource": resource,
                "reason": reason
            }
        )

class IntegrityCheckError(SecurityError):
    """Raised when integrity check fails"""

    def __init__(self, resource: str, expected_hash: str, actual_hash: str) -> None:
        """Initialize with hash details"""
        super().__init__(
            f"Integrity check failed: {resource}",
            {
                "resource": resource,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash
            }
        )

# IO Exceptions
class IOError(OmniCppException):
    """Base exception for IO errors"""
    pass

class FileNotFoundError(IOError):
    """Raised when file is not found"""

    def __init__(self, file_path: str) -> None:
        """Initialize with file path"""
        super().__init__(
            f"File not found: {file_path}",
            {"file_path": file_path}
        )

class DirectoryNotFoundError(IOError):
    """Raised when directory is not found"""

    def __init__(self, dir_path: str) -> None:
        """Initialize with directory path"""
        super().__init__(
            f"Directory not found: {dir_path}",
            {"dir_path": dir_path}
        )

class PermissionError(IOError):
    """Raised when permission is denied"""

    def __init__(self, resource: str, operation: str) -> None:
        """Initialize with resource and operation"""
        super().__init__(
            f"Permission denied: {operation} on {resource}",
            {
                "resource": resource,
                "operation": operation
            }
        )

# Network Exceptions
class NetworkError(OmniCppException):
    """Base exception for network errors"""
    pass

class NetworkConnectionError(NetworkError):
    """Raised when network connection fails"""

    def __init__(self, url: str, reason: str) -> None:
        """Initialize with URL and reason"""
        super().__init__(
            f"Network connection failed: {url}",
            {
                "url": url,
                "reason": reason
            }
        )

class DownloadError(NetworkError):
    """Raised when download fails"""

    def __init__(self, url: str, reason: str) -> None:
        """Initialize with URL and reason"""
        super().__init__(
            f"Download failed: {url}",
            {
                "url": url,
                "reason": reason
            }
        )

# Exception Handler
class ExceptionHandler:
    """Central exception handler for OmniCppController"""

    @staticmethod
    def handle(exception: Exception, logger: Any) -> None:
        """Handle exception with logging"""
        if isinstance(exception, OmniCppException):
            # Handle OmniCpp exceptions
            logger.error(f"{exception.__class__.__name__}: {exception.message}")
            if exception.details:
                logger.debug(f"Exception details: {exception.details}")
        else:
            # Handle generic exceptions
            logger.error(f"Unexpected error: {str(exception)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    @staticmethod
    def to_dict(exception: Exception) -> Dict[str, Any]:
        """Convert exception to dictionary"""
        if isinstance(exception, OmniCppException):
            return exception.to_dict()
        else:
            return {
                "type": exception.__class__.__name__,
                "message": str(exception),
                "traceback": traceback.format_exc()
            }
```

## Exception Hierarchy Diagram

```
OmniCppException
├── ConfigurationError
│   ├── ConfigurationFileNotFoundError
│   ├── ConfigurationParseError
│   ├── ConfigurationValidationError
│   └── ConfigurationMissingError
├── PlatformError
│   ├── UnsupportedPlatformError
│   └── PlatformDetectionError
├── CompilerError
│   ├── CompilerNotFoundError
│   ├── CompilerVersionError
│   ├── CompilerExecutionError
│   └── CompilerDetectionError
├── BuildSystemError
│   ├── BuildConfigurationError
│   ├── BuildExecutionError
│   ├── BuildDependencyError
│   ├── CMakeNotFoundError
│   └── CMakeVersionError
├── PackageManagerError
│   ├── PackageManagerNotFoundError
│   ├── PackageNotFoundError
│   ├── PackageInstallationError
│   └── PackageDependencyError
├── TerminalError
│   ├── TerminalNotFoundError
│   ├── TerminalExecutionError
│   └── TerminalTimeoutError
├── ControllerError
│   ├── ControllerNotFoundError
│   ├── ControllerExecutionError
│   └── InvalidArgumentError
├── TestingError
│   ├── TestExecutionError
│   ├── TestNotFoundError
│   └── TestTimeoutError
├── FormattingError
│   ├── FormatterNotFoundError
│   └── FormattingExecutionError
├── LintingError
│   ├── LinterNotFoundError
│   └── LintingExecutionError
├── SecurityError
│   ├── SecurityValidationError
│   └── IntegrityCheckError
├── IOError
│   ├── FileNotFoundError
│   ├── DirectoryNotFoundError
│   └── PermissionError
└── NetworkError
    ├── NetworkConnectionError
    └── DownloadError
```

## Dependencies

### Internal Dependencies
- `DES-001` - ControllerConfig
- `DES-004` - Logging configuration

### External Dependencies
- `typing` - Type hints
- `dataclasses` - Data structures
- `traceback` - Exception traceback

## Related Requirements
- REQ-006: Error Handling & Exception Management
- REQ-043: Secure Terminal Invocation
- REQ-044: Dependency Integrity Verification
- REQ-045: Secure Logging
- REQ-046: Build System Security
- REQ-047: Package Manager Security

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Exception Handling Strategy
1. Catch specific exceptions first
2. Log exceptions with appropriate level
3. Provide meaningful error messages
4. Include context in exception details
5. Propagate exceptions up the call stack

### Exception Recovery
- Some exceptions are recoverable (e.g., retry network operations)
- Some exceptions are fatal (e.g., configuration errors)
- Document which exceptions are recoverable

### Exception Logging
- Log all exceptions with appropriate level
- Include exception details in debug logs
- Sanitize sensitive information before logging

### Exception Testing
- Test all exception paths
- Verify exception messages are meaningful
- Test exception details are correct

## Usage Example

```python
from omni_scripts.exceptions import (
    ConfigurationError,
    CompilerNotFoundError,
    ExceptionHandler
)
import logging

# Setup logger
logger = logging.getLogger("omni_scripts")

try:
    # Some operation that might raise an exception
    compiler = detect_compiler()
except CompilerNotFoundError as e:
    # Handle specific exception
    ExceptionHandler.handle(e, logger)
    # Try fallback
    compiler = try_fallback_compiler()
except ConfigurationError as e:
    # Handle configuration error
    ExceptionHandler.handle(e, logger)
    raise  # Re-raise if unrecoverable
except Exception as e:
    # Handle unexpected exception
    ExceptionHandler.handle(e, logger)
    raise
```
