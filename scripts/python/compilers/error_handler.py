"""
Error handler for compiler detection system

This module provides centralized error handling for compiler detection,
including error categorization, recovery suggestions, and logging.
"""

import logging
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ErrorSeverity(Enum):
    """Error severity enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """Error category enumeration"""
    DETECTION_ERROR = "detection_error"
    VALIDATION_ERROR = "validation_error"
    CONFIGURATION_ERROR = "configuration_error"
    EXECUTION_ERROR = "execution_error"
    ENVIRONMENT_ERROR = "environment_error"
    PERMISSION_ERROR = "permission_error"
    TIMEOUT_ERROR = "timeout_error"
    FILE_NOT_FOUND_ERROR = "file_not_found_error"


@dataclass
class ErrorInfo:
    """Error information dataclass
    
    Attributes:
        category: Error category
        severity: Error severity
        component: Component that raised the error
        error_code: Error code for identification
        message: Human-readable error message
        details: Additional error details
        suggestion: Recovery suggestion
        exception: Original exception if available
        timestamp: When the error occurred
    """
    category: ErrorCategory
    severity: ErrorSeverity
    component: str
    error_code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict[str, Any])
    suggestion: Optional[str] = None
    exception: Optional[Exception] = None
    timestamp: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert error info to dictionary
        
        Returns:
            Dictionary representation of error info
        """
        return {
            "category": self.category.value,
            "severity": self.severity.value,
            "component": self.component,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "suggestion": self.suggestion,
            "exception": str(self.exception) if self.exception else None,
            "timestamp": self.timestamp
        }

    def __str__(self) -> str:
        """String representation of error info
        
        Returns:
            Formatted error string
        """
        return f"[{self.severity.value.upper()}] {self.component}: {self.message}"


class ErrorHandler:
    """Error handler for compiler detection system
    
    This class provides centralized error handling with categorization,
    severity assessment, and recovery suggestions for all compiler
    detection operations.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """Initialize error handler
        
        Args:
            logger: Logger instance for error logging
        """
        self._logger = logger or logging.getLogger(__name__)
        self._errors: list[ErrorInfo] = []
        self._error_code_counter: int = 0

    def handle_error(
        self,
        component: str,
        error_code: str,
        message: str,
        category: Optional[ErrorCategory] = None,
        severity: Optional[ErrorSeverity] = None,
        details: Optional[dict[str, Any]] = None,
        suggestion: Optional[str] = None,
        exception: Optional[Exception] = None
    ) -> ErrorInfo:
        """Handle an error
        
        Args:
            component: Component that raised the error
            error_code: Error code for identification
            message: Human-readable error message
            category: Error category (auto-determined if None)
            severity: Error severity (auto-determined if None)
            details: Additional error details
            suggestion: Recovery suggestion
            exception: Original exception
            
        Returns:
            ErrorInfo object representing the handled error
        """
        import time

        # Auto-determine category if not provided
        if category is None:
            category = self._determine_category(exception, error_code)

        # Auto-determine severity if not provided
        if severity is None:
            severity = self._determine_severity(category, error_code)

        # Auto-generate suggestion if not provided
        if suggestion is None:
            suggestion = self._generate_suggestion(category, error_code, exception)

        # Create error info
        error_info = ErrorInfo(
            category=category,
            severity=severity,
            component=component,
            error_code=error_code,
            message=message,
            details=details or {},
            suggestion=suggestion,
            exception=exception,
            timestamp=time.time()
        )

        # Store error
        self._errors.append(error_info)

        # Log error
        self._log_error(error_info)

        return error_info

    def handle_exception(
        self,
        component: str,
        exception: Exception,
        error_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
        suggestion: Optional[str] = None
    ) -> ErrorInfo:
        """Handle an exception
        
        Args:
            component: Component that raised the exception
            exception: Exception to handle
            error_code: Error code (auto-generated if None)
            details: Additional error details
            suggestion: Recovery suggestion
            
        Returns:
            ErrorInfo object representing the handled exception
        """
        # Auto-generate error code if not provided
        if error_code is None:
            error_code = self._generate_error_code(exception)

        # Extract message from exception
        message = str(exception) if str(exception) else type(exception).__name__

        # Handle exception
        return self.handle_error(
            component=component,
            error_code=error_code,
            message=message,
            exception=exception,
            details=details,
            suggestion=suggestion
        )

    def get_error_summary(self) -> dict[str, Any]:
        """Get summary of all errors
        
        Returns:
            Dictionary containing error summary statistics and details
        """
        # Count errors by severity
        severity_counts: dict[str, int] = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        # Count errors by category
        category_counts: dict[str, int] = {
            "detection_error": 0,
            "validation_error": 0,
            "configuration_error": 0,
            "execution_error": 0,
            "environment_error": 0,
            "permission_error": 0,
            "timeout_error": 0,
            "file_not_found_error": 0
        }

        # Count errors by component
        component_counts: dict[str, int] = {}

        # Process all errors
        for error in self._errors:
            # Update severity counts
            severity_counts[error.severity.value] += 1

            # Update category counts
            category_counts[error.category.value] += 1

            # Update component counts
            component_counts[error.component] = component_counts.get(error.component, 0) + 1

        return {
            "total_errors": len(self._errors),
            "severity_counts": severity_counts,
            "category_counts": category_counts,
            "component_counts": component_counts,
            "has_critical_errors": any(e.severity == ErrorSeverity.CRITICAL for e in self._errors),
            "has_high_errors": any(e.severity == ErrorSeverity.HIGH for e in self._errors),
            "errors": [e.to_dict() for e in self._errors]
        }

    def clear_errors(self) -> None:
        """Clear all stored errors"""
        self._errors.clear()
        self._error_code_counter = 0

    def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorInfo]:
        """Get errors filtered by severity
        
        Args:
            severity: Error severity to filter by
            
        Returns:
            List of errors with specified severity
        """
        return [e for e in self._errors if e.severity == severity]

    def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorInfo]:
        """Get errors filtered by category
        
        Args:
            category: Error category to filter by
            
        Returns:
            List of errors with specified category
        """
        return [e for e in self._errors if e.category == category]

    def get_errors_by_component(self, component: str) -> list[ErrorInfo]:
        """Get errors filtered by component
        
        Args:
            component: Component name to filter by
            
        Returns:
            List of errors from specified component
        """
        return [e for e in self._errors if e.component == component]

    def has_critical_errors(self) -> bool:
        """Check if there are critical errors
        
        Returns:
            True if critical errors exist, False otherwise
        """
        return any(e.severity == ErrorSeverity.CRITICAL for e in self._errors)

    def has_high_errors(self) -> bool:
        """Check if there are high severity errors
        
        Returns:
            True if high severity errors exist, False otherwise
        """
        return any(e.severity == ErrorSeverity.HIGH for e in self._errors)

    def get_error_count(self) -> int:
        """Get total number of errors
        
        Returns:
            Total error count
        """
        return len(self._errors)

    def _determine_category(
        self,
        exception: Optional[Exception],
        error_code: str
    ) -> ErrorCategory:
        """Determine error category from exception and error code
        
        Args:
            exception: Exception that occurred
            error_code: Error code
            
        Returns:
            Determined error category
        """
        # Check exception type first
        if exception is not None:
            if isinstance(exception, FileNotFoundError):
                return ErrorCategory.FILE_NOT_FOUND_ERROR
            elif isinstance(exception, PermissionError):
                return ErrorCategory.PERMISSION_ERROR
            elif isinstance(exception, subprocess.TimeoutExpired):
                return ErrorCategory.TIMEOUT_ERROR
            elif isinstance(exception, subprocess.CalledProcessError):
                return ErrorCategory.EXECUTION_ERROR

        # Check error code
        if "DETECTION" in error_code.upper():
            return ErrorCategory.DETECTION_ERROR
        elif "VALIDATION" in error_code.upper():
            return ErrorCategory.VALIDATION_ERROR
        elif "CONFIG" in error_code.upper():
            return ErrorCategory.CONFIGURATION_ERROR
        elif "EXECUTION" in error_code.upper():
            return ErrorCategory.EXECUTION_ERROR
        elif "TIMEOUT" in error_code.upper():
            return ErrorCategory.TIMEOUT_ERROR
        elif "PERMISSION" in error_code.upper():
            return ErrorCategory.PERMISSION_ERROR
        elif "FILE_NOT_FOUND" in error_code.upper():
            return ErrorCategory.FILE_NOT_FOUND_ERROR

        # Default to detection error
        return ErrorCategory.DETECTION_ERROR

    def _determine_severity(
        self,
        category: ErrorCategory,
        error_code: str
    ) -> ErrorSeverity:
        """Determine error severity from category and error code
        
        Args:
            category: Error category
            error_code: Error code
            
        Returns:
            Determined error severity
        """
        # Check error code for severity hints
        if error_code.startswith("CRITICAL_"):
            return ErrorSeverity.CRITICAL
        elif error_code.startswith("HIGH_"):
            return ErrorSeverity.HIGH
        elif error_code.startswith("MEDIUM_"):
            return ErrorSeverity.MEDIUM
        elif error_code.startswith("LOW_"):
            return ErrorSeverity.LOW

        # Determine severity based on category
        if category == ErrorCategory.PERMISSION_ERROR:
            return ErrorSeverity.HIGH
        elif category == ErrorCategory.FILE_NOT_FOUND_ERROR:
            return ErrorSeverity.MEDIUM
        elif category == ErrorCategory.TIMEOUT_ERROR:
            return ErrorSeverity.MEDIUM
        elif category == ErrorCategory.CONFIGURATION_ERROR:
            return ErrorSeverity.HIGH
        elif category == ErrorCategory.VALIDATION_ERROR:
            return ErrorSeverity.HIGH
        elif category == ErrorCategory.EXECUTION_ERROR:
            return ErrorSeverity.MEDIUM
        elif category == ErrorCategory.ENVIRONMENT_ERROR:
            return ErrorSeverity.HIGH

        # Default to medium
        return ErrorSeverity.MEDIUM

    def _generate_suggestion(
        self,
        category: ErrorCategory,
        error_code: str,
        exception: Optional[Exception]
    ) -> str:
        """Generate recovery suggestion for error
        
        Args:
            category: Error category
            error_code: Error code
            exception: Exception that occurred
            
        Returns:
            Recovery suggestion string
        """
        # Check exception type first
        if exception is not None:
            if isinstance(exception, FileNotFoundError):
                return "Check if the file or directory exists and the path is correct."
            elif isinstance(exception, PermissionError):
                return "Check file/directory permissions and ensure you have necessary access rights."
            elif isinstance(exception, subprocess.TimeoutExpired):
                return "Increase timeout duration or check for blocking operations."
            elif isinstance(exception, subprocess.CalledProcessError):
                return f"Command failed with exit code {exception.returncode}. Check command syntax and dependencies."

        # Generate suggestion based on category
        if category == ErrorCategory.DETECTION_ERROR:
            return "Ensure compiler is installed and accessible in system PATH or standard locations."
        elif category == ErrorCategory.VALIDATION_ERROR:
            return "Verify compiler installation and check for corrupted files."
        elif category == ErrorCategory.CONFIGURATION_ERROR:
            return "Review configuration file and ensure all settings are valid."
        elif category == ErrorCategory.EXECUTION_ERROR:
            return "Check command syntax and ensure all dependencies are available."
        elif category == ErrorCategory.ENVIRONMENT_ERROR:
            return "Verify environment variables and system configuration."
        elif category == ErrorCategory.PERMISSION_ERROR:
            return "Run with appropriate permissions or check file/directory access rights."
        elif category == ErrorCategory.TIMEOUT_ERROR:
            return "Increase timeout or check for blocking operations."
        elif category == ErrorCategory.FILE_NOT_FOUND_ERROR:
            return "Verify file/directory exists and path is correct."

        # Default suggestion
        return "Review error details and check system configuration."

    def _generate_error_code(self, exception: Exception) -> str:
        """Generate error code from exception
        
        Args:
            exception: Exception to generate code from
            
        Returns:
            Generated error code
        """
        self._error_code_counter += 1

        exception_type = type(exception).__name__

        if isinstance(exception, FileNotFoundError):
            return f"FILE_NOT_FOUND_{self._error_code_counter:04d}"
        elif isinstance(exception, PermissionError):
            return f"PERMISSION_{self._error_code_counter:04d}"
        elif isinstance(exception, subprocess.TimeoutExpired):
            return f"TIMEOUT_{self._error_code_counter:04d}"
        elif isinstance(exception, subprocess.CalledProcessError):
            return f"EXECUTION_{self._error_code_counter:04d}"
        else:
            return f"ERROR_{exception_type.upper()}_{self._error_code_counter:04d}"

    def _log_error(self, error_info: ErrorInfo) -> None:
        """Log error with appropriate level
        
        Args:
            error_info: Error information to log
        """
        log_message = str(error_info)

        if error_info.details:
            log_message += f" | Details: {error_info.details}"

        if error_info.suggestion:
            log_message += f" | Suggestion: {error_info.suggestion}"

        if error_info.severity == ErrorSeverity.CRITICAL:
            self._logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            self._logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            self._logger.warning(log_message)
        elif error_info.severity == ErrorSeverity.LOW:
            self._logger.info(log_message)
        else:
            self._logger.debug(log_message)
