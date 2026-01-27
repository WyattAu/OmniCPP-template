"""
Unit tests for ErrorHandler class
"""

import logging
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

# Add scripts/python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from compilers.error_handler import (
    ErrorHandler,
    ErrorSeverity,
    ErrorCategory,
    ErrorInfo
)


class TestErrorHandler(unittest.TestCase):
    """Test cases for ErrorHandler class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.logger = Mock(spec=logging.Logger)
        self.error_handler = ErrorHandler(logger=self.logger)

    def test_initialization(self) -> None:
        """Test ErrorHandler initialization"""
        handler = ErrorHandler()
        self.assertIsNotNone(handler._logger)
        self.assertEqual(handler.get_error_count(), 0)

    def test_initialization_with_logger(self) -> None:
        """Test ErrorHandler initialization with custom logger"""
        handler = ErrorHandler(logger=self.logger)
        self.assertEqual(handler._logger, self.logger)
        self.assertEqual(handler.get_error_count(), 0)

    def test_handle_error_basic(self) -> None:
        """Test basic error handling"""
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message"
        )

        self.assertIsInstance(error_info, ErrorInfo)
        self.assertEqual(error_info.component, "test_component")
        self.assertEqual(error_info.error_code, "TEST_ERROR")
        self.assertEqual(error_info.message, "Test error message")
        self.assertEqual(self.error_handler.get_error_count(), 1)

    def test_handle_error_with_category(self) -> None:
        """Test error handling with explicit category"""
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message",
            category=ErrorCategory.DETECTION_ERROR
        )

        self.assertEqual(error_info.category, ErrorCategory.DETECTION_ERROR)

    def test_handle_error_with_severity(self) -> None:
        """Test error handling with explicit severity"""
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message",
            severity=ErrorSeverity.HIGH
        )

        self.assertEqual(error_info.severity, ErrorSeverity.HIGH)

    def test_handle_error_with_details(self) -> None:
        """Test error handling with details"""
        details = {"key1": "value1", "key2": "value2"}
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message",
            details=details
        )

        self.assertEqual(error_info.details, details)

    def test_handle_error_with_suggestion(self) -> None:
        """Test error handling with custom suggestion"""
        suggestion = "Custom recovery suggestion"
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message",
            suggestion=suggestion
        )

        self.assertEqual(error_info.suggestion, suggestion)

    def test_handle_error_with_exception(self) -> None:
        """Test error handling with exception"""
        exception = ValueError("Test exception")
        error_info = self.error_handler.handle_error(
            component="test_component",
            error_code="TEST_ERROR",
            message="Test error message",
            exception=exception
        )

        self.assertEqual(error_info.exception, exception)

    def test_handle_exception_file_not_found(self) -> None:
        """Test handling FileNotFoundError exception"""
        exception = FileNotFoundError("File not found: test.txt")
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception
        )

        self.assertEqual(error_info.category, ErrorCategory.FILE_NOT_FOUND_ERROR)
        self.assertEqual(error_info.severity, ErrorSeverity.MEDIUM)
        self.assertIn("FILE_NOT_FOUND", error_info.error_code)
        self.assertIsNotNone(error_info.suggestion)

    def test_handle_exception_permission_error(self) -> None:
        """Test handling PermissionError exception"""
        exception = PermissionError("Permission denied")
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception
        )

        self.assertEqual(error_info.category, ErrorCategory.PERMISSION_ERROR)
        self.assertEqual(error_info.severity, ErrorSeverity.HIGH)
        self.assertIn("PERMISSION", error_info.error_code)
        self.assertIsNotNone(error_info.suggestion)

    def test_handle_exception_timeout_expired(self) -> None:
        """Test handling subprocess.TimeoutExpired exception"""
        exception = subprocess.TimeoutExpired("cmd", 10)
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception
        )

        self.assertEqual(error_info.category, ErrorCategory.TIMEOUT_ERROR)
        self.assertEqual(error_info.severity, ErrorSeverity.MEDIUM)
        self.assertIn("TIMEOUT", error_info.error_code)
        self.assertIsNotNone(error_info.suggestion)

    def test_handle_exception_called_process_error(self) -> None:
        """Test handling subprocess.CalledProcessError exception"""
        exception = subprocess.CalledProcessError(1, "cmd")
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception
        )

        self.assertEqual(error_info.category, ErrorCategory.EXECUTION_ERROR)
        self.assertEqual(error_info.severity, ErrorSeverity.MEDIUM)
        self.assertIn("EXECUTION", error_info.error_code)
        self.assertIsNotNone(error_info.suggestion)

    def test_handle_exception_generic_exception(self) -> None:
        """Test handling generic exception"""
        exception = RuntimeError("Runtime error occurred")
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception
        )

        self.assertEqual(error_info.category, ErrorCategory.DETECTION_ERROR)
        self.assertEqual(error_info.severity, ErrorSeverity.MEDIUM)
        self.assertIn("RUNTIMEERROR", error_info.error_code)
        self.assertIsNotNone(error_info.suggestion)

    def test_handle_exception_with_custom_error_code(self) -> None:
        """Test handling exception with custom error code"""
        exception = ValueError("Test exception")
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception,
            error_code="CUSTOM_ERROR_001"
        )

        self.assertEqual(error_info.error_code, "CUSTOM_ERROR_001")

    def test_handle_exception_with_details(self) -> None:
        """Test handling exception with details"""
        exception = ValueError("Test exception")
        details = {"context": "test context"}
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception,
            details=details
        )

        self.assertEqual(error_info.details, details)

    def test_handle_exception_with_custom_suggestion(self) -> None:
        """Test handling exception with custom suggestion"""
        exception = ValueError("Test exception")
        suggestion = "Custom suggestion"
        error_info = self.error_handler.handle_exception(
            component="test_component",
            exception=exception,
            suggestion=suggestion
        )

        self.assertEqual(error_info.suggestion, suggestion)

    def test_get_error_summary_empty(self) -> None:
        """Test error summary with no errors"""
        summary = self.error_handler.get_error_summary()

        self.assertEqual(summary["total_errors"], 0)
        self.assertEqual(summary["severity_counts"]["critical"], 0)
        self.assertEqual(summary["severity_counts"]["high"], 0)
        self.assertEqual(summary["severity_counts"]["medium"], 0)
        self.assertEqual(summary["severity_counts"]["low"], 0)
        self.assertEqual(summary["severity_counts"]["info"], 0)
        self.assertFalse(summary["has_critical_errors"])
        self.assertFalse(summary["has_high_errors"])
        self.assertEqual(len(summary["errors"]), 0)

    def test_get_error_summary_with_errors(self) -> None:
        """Test error summary with multiple errors"""
        # Add multiple errors
        self.error_handler.handle_error(
            component="component1",
            error_code="ERROR_001",
            message="Error 1",
            severity=ErrorSeverity.CRITICAL
        )
        self.error_handler.handle_error(
            component="component2",
            error_code="ERROR_002",
            message="Error 2",
            severity=ErrorSeverity.HIGH
        )
        self.error_handler.handle_error(
            component="component1",
            error_code="ERROR_003",
            message="Error 3",
            severity=ErrorSeverity.MEDIUM
        )

        summary = self.error_handler.get_error_summary()

        self.assertEqual(summary["total_errors"], 3)
        self.assertEqual(summary["severity_counts"]["critical"], 1)
        self.assertEqual(summary["severity_counts"]["high"], 1)
        self.assertEqual(summary["severity_counts"]["medium"], 1)
        self.assertTrue(summary["has_critical_errors"])
        self.assertTrue(summary["has_high_errors"])
        self.assertEqual(summary["component_counts"]["component1"], 2)
        self.assertEqual(summary["component_counts"]["component2"], 1)
        self.assertEqual(len(summary["errors"]), 3)

    def test_clear_errors(self) -> None:
        """Test clearing all errors"""
        # Add some errors
        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="Error 1"
        )
        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_002",
            message="Error 2"
        )

        self.assertEqual(self.error_handler.get_error_count(), 2)

        # Clear errors
        self.error_handler.clear_errors()

        self.assertEqual(self.error_handler.get_error_count(), 0)

    def test_get_errors_by_severity(self) -> None:
        """Test filtering errors by severity"""
        # Add errors with different severities
        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="Critical error",
            severity=ErrorSeverity.CRITICAL
        )
        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_002",
            message="High error",
            severity=ErrorSeverity.HIGH
        )
        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_003",
            message="Medium error",
            severity=ErrorSeverity.MEDIUM
        )

        critical_errors = self.error_handler.get_errors_by_severity(ErrorSeverity.CRITICAL)
        high_errors = self.error_handler.get_errors_by_severity(ErrorSeverity.HIGH)
        medium_errors = self.error_handler.get_errors_by_severity(ErrorSeverity.MEDIUM)

        self.assertEqual(len(critical_errors), 1)
        self.assertEqual(len(high_errors), 1)
        self.assertEqual(len(medium_errors), 1)
        self.assertEqual(critical_errors[0].message, "Critical error")
        self.assertEqual(high_errors[0].message, "High error")
        self.assertEqual(medium_errors[0].message, "Medium error")

    def test_get_errors_by_category(self) -> None:
        """Test filtering errors by category"""
        # Add errors with different categories
        self.error_handler.handle_error(
            component="test_component",
            error_code="DETECTION_ERROR_001",
            message="Detection error",
            category=ErrorCategory.DETECTION_ERROR
        )
        self.error_handler.handle_error(
            component="test_component",
            error_code="VALIDATION_ERROR_001",
            message="Validation error",
            category=ErrorCategory.VALIDATION_ERROR
        )
        self.error_handler.handle_error(
            component="test_component",
            error_code="DETECTION_ERROR_002",
            message="Another detection error",
            category=ErrorCategory.DETECTION_ERROR
        )

        detection_errors = self.error_handler.get_errors_by_category(ErrorCategory.DETECTION_ERROR)
        validation_errors = self.error_handler.get_errors_by_category(ErrorCategory.VALIDATION_ERROR)

        self.assertEqual(len(detection_errors), 2)
        self.assertEqual(len(validation_errors), 1)

    def test_get_errors_by_component(self) -> None:
        """Test filtering errors by component"""
        # Add errors from different components
        self.error_handler.handle_error(
            component="component1",
            error_code="ERROR_001",
            message="Error from component 1"
        )
        self.error_handler.handle_error(
            component="component2",
            error_code="ERROR_002",
            message="Error from component 2"
        )
        self.error_handler.handle_error(
            component="component1",
            error_code="ERROR_003",
            message="Another error from component 1"
        )

        component1_errors = self.error_handler.get_errors_by_component("component1")
        component2_errors = self.error_handler.get_errors_by_component("component2")

        self.assertEqual(len(component1_errors), 2)
        self.assertEqual(len(component2_errors), 1)

    def test_has_critical_errors(self) -> None:
        """Test checking for critical errors"""
        self.assertFalse(self.error_handler.has_critical_errors())

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="High error",
            severity=ErrorSeverity.HIGH
        )
        self.assertFalse(self.error_handler.has_critical_errors())

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_002",
            message="Critical error",
            severity=ErrorSeverity.CRITICAL
        )
        self.assertTrue(self.error_handler.has_critical_errors())

    def test_has_high_errors(self) -> None:
        """Test checking for high severity errors"""
        self.assertFalse(self.error_handler.has_high_errors())

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="Medium error",
            severity=ErrorSeverity.MEDIUM
        )
        self.assertFalse(self.error_handler.has_high_errors())

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_002",
            message="High error",
            severity=ErrorSeverity.HIGH
        )
        self.assertTrue(self.error_handler.has_high_errors())

    def test_get_error_count(self) -> None:
        """Test getting error count"""
        self.assertEqual(self.error_handler.get_error_count(), 0)

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="Error 1"
        )
        self.assertEqual(self.error_handler.get_error_count(), 1)

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_002",
            message="Error 2"
        )
        self.assertEqual(self.error_handler.get_error_count(), 2)

    def test_error_info_to_dict(self) -> None:
        """Test ErrorInfo to_dict method"""
        error_info = ErrorInfo(
            category=ErrorCategory.DETECTION_ERROR,
            severity=ErrorSeverity.HIGH,
            component="test_component",
            error_code="TEST_ERROR",
            message="Test message",
            details={"key": "value"},
            suggestion="Test suggestion",
            exception=ValueError("Test exception"),
            timestamp=1234567890.0
        )

        error_dict = error_info.to_dict()

        self.assertEqual(error_dict["category"], "detection_error")
        self.assertEqual(error_dict["severity"], "high")
        self.assertEqual(error_dict["component"], "test_component")
        self.assertEqual(error_dict["error_code"], "TEST_ERROR")
        self.assertEqual(error_dict["message"], "Test message")
        self.assertEqual(error_dict["details"], {"key": "value"})
        self.assertEqual(error_dict["suggestion"], "Test suggestion")
        self.assertIsNotNone(error_dict["exception"])
        self.assertEqual(error_dict["timestamp"], 1234567890.0)

    def test_error_info_str(self) -> None:
        """Test ErrorInfo __str__ method"""
        error_info = ErrorInfo(
            category=ErrorCategory.DETECTION_ERROR,
            severity=ErrorSeverity.HIGH,
            component="test_component",
            error_code="TEST_ERROR",
            message="Test message"
        )

        error_str = str(error_info)

        self.assertIn("HIGH", error_str)
        self.assertIn("test_component", error_str)
        self.assertIn("Test message", error_str)

    def test_auto_determine_category_from_error_code(self) -> None:
        """Test automatic category determination from error code"""
        # Detection error
        error1 = self.error_handler.handle_error(
            component="test",
            error_code="DETECTION_ERROR_001",
            message="Detection error"
        )
        self.assertEqual(error1.category, ErrorCategory.DETECTION_ERROR)

        # Validation error
        error2 = self.error_handler.handle_error(
            component="test",
            error_code="VALIDATION_ERROR_001",
            message="Validation error"
        )
        self.assertEqual(error2.category, ErrorCategory.VALIDATION_ERROR)

        # Configuration error
        error3 = self.error_handler.handle_error(
            component="test",
            error_code="CONFIGURATION_ERROR_001",
            message="Configuration error"
        )
        self.assertEqual(error3.category, ErrorCategory.CONFIGURATION_ERROR)

    def test_auto_determine_severity_from_error_code(self) -> None:
        """Test automatic severity determination from error code"""
        # Critical
        error1 = self.error_handler.handle_error(
            component="test",
            error_code="CRITICAL_ERROR_001",
            message="Critical error"
        )
        self.assertEqual(error1.severity, ErrorSeverity.CRITICAL)

        # High
        error2 = self.error_handler.handle_error(
            component="test",
            error_code="HIGH_ERROR_001",
            message="High error"
        )
        self.assertEqual(error2.severity, ErrorSeverity.HIGH)

        # Medium
        error3 = self.error_handler.handle_error(
            component="test",
            error_code="MEDIUM_ERROR_001",
            message="Medium error"
        )
        self.assertEqual(error3.severity, ErrorSeverity.MEDIUM)

        # Low
        error4 = self.error_handler.handle_error(
            component="test",
            error_code="LOW_ERROR_001",
            message="Low error"
        )
        self.assertEqual(error4.severity, ErrorSeverity.LOW)

    def test_auto_generate_suggestion(self) -> None:
        """Test automatic suggestion generation"""
        # Detection error suggestion
        error1 = self.error_handler.handle_error(
            component="test",
            error_code="DETECTION_ERROR_001",
            message="Detection error",
            category=ErrorCategory.DETECTION_ERROR
        )
        self.assertIsNotNone(error1.suggestion)
        self.assertIn("compiler", error1.suggestion.lower())

        # Validation error suggestion
        error2 = self.error_handler.handle_error(
            component="test",
            error_code="VALIDATION_ERROR_001",
            message="Validation error",
            category=ErrorCategory.VALIDATION_ERROR
        )
        self.assertIsNotNone(error2.suggestion)

        # Configuration error suggestion
        error3 = self.error_handler.handle_error(
            component="test",
            error_code="CONFIGURATION_ERROR_001",
            message="Configuration error",
            category=ErrorCategory.CONFIGURATION_ERROR
        )
        self.assertIsNotNone(error3.suggestion)
        self.assertIn("configuration", error3.suggestion.lower())

    def test_logging_critical_error(self) -> None:
        """Test logging of critical errors"""
        self.error_handler.handle_error(
            component="test_component",
            error_code="CRITICAL_ERROR_001",
            message="Critical error",
            severity=ErrorSeverity.CRITICAL
        )

        self.logger.critical.assert_called_once()
        call_args = str(self.logger.critical.call_args)
        self.assertIn("CRITICAL", call_args)
        self.assertIn("test_component", call_args)
        self.assertIn("Critical error", call_args)

    def test_logging_high_error(self) -> None:
        """Test logging of high severity errors"""
        self.error_handler.handle_error(
            component="test_component",
            error_code="HIGH_ERROR_001",
            message="High error",
            severity=ErrorSeverity.HIGH
        )

        self.logger.error.assert_called_once()
        call_args = str(self.logger.error.call_args)
        self.assertIn("HIGH", call_args)
        self.assertIn("test_component", call_args)

    def test_logging_medium_error(self) -> None:
        """Test logging of medium severity errors"""
        self.error_handler.handle_error(
            component="test_component",
            error_code="MEDIUM_ERROR_001",
            message="Medium error",
            severity=ErrorSeverity.MEDIUM
        )

        self.logger.warning.assert_called_once()
        call_args = str(self.logger.warning.call_args)
        self.assertIn("MEDIUM", call_args)
        self.assertIn("test_component", call_args)

    def test_logging_low_error(self) -> None:
        """Test logging of low severity errors"""
        self.error_handler.handle_error(
            component="test_component",
            error_code="LOW_ERROR_001",
            message="Low error",
            severity=ErrorSeverity.LOW
        )

        self.logger.info.assert_called_once()
        call_args = str(self.logger.info.call_args)
        self.assertIn("LOW", call_args)
        self.assertIn("test_component", call_args)

    def test_logging_with_details_and_suggestion(self) -> None:
        """Test logging with details and suggestion"""
        details = {"key": "value"}
        suggestion = "Test suggestion"

        self.error_handler.handle_error(
            component="test_component",
            error_code="ERROR_001",
            message="Test error",
            details=details,
            suggestion=suggestion
        )

        call_args = str(self.logger.warning.call_args)
        self.assertIn("Details:", call_args)
        self.assertIn("Suggestion:", call_args)
        self.assertIn("Test suggestion", call_args)

    def test_error_code_counter(self) -> None:
        """Test error code counter increments"""
        exception1 = ValueError("Error 1")
        exception2 = RuntimeError("Error 2")

        error1 = self.error_handler.handle_exception(
            component="test",
            exception=exception1
        )
        error2 = self.error_handler.handle_exception(
            component="test",
            exception=exception2
        )

        self.assertNotEqual(error1.error_code, error2.error_code)

    def test_clear_resets_error_code_counter(self) -> None:
        """Test that clear_errors resets error code counter"""
        exception1 = ValueError("Error 1")
        error1 = self.error_handler.handle_exception(
            component="test",
            exception=exception1
        )

        # Store first error code
        first_error_code = error1.error_code

        self.error_handler.clear_errors()

        exception2 = ValueError("Error 2")
        error2 = self.error_handler.handle_exception(
            component="test",
            exception=exception2
        )

        # Error codes should be the same after clear (counter reset to 0)
        # This is the expected behavior - counter resets to 0, so second error gets code 0001
        self.assertEqual(first_error_code, error2.error_code)

    def test_multiple_errors_same_component(self) -> None:
        """Test handling multiple errors from same component"""
        for i in range(5):
            self.error_handler.handle_error(
                component="test_component",
                error_code=f"ERROR_{i:03d}",
                message=f"Error {i}"
            )

        self.assertEqual(self.error_handler.get_error_count(), 5)
        component_errors = self.error_handler.get_errors_by_component("test_component")
        self.assertEqual(len(component_errors), 5)

    def test_all_error_categories(self) -> None:
        """Test all error categories are supported"""
        categories = [
            ErrorCategory.DETECTION_ERROR,
            ErrorCategory.VALIDATION_ERROR,
            ErrorCategory.CONFIGURATION_ERROR,
            ErrorCategory.EXECUTION_ERROR,
            ErrorCategory.ENVIRONMENT_ERROR,
            ErrorCategory.PERMISSION_ERROR,
            ErrorCategory.TIMEOUT_ERROR,
            ErrorCategory.FILE_NOT_FOUND_ERROR
        ]

        for category in categories:
            error = self.error_handler.handle_error(
                component="test",
                error_code=f"{category.value.upper()}_001",
                message="Test error",
                category=category
            )
            self.assertEqual(error.category, category)

    def test_all_error_severities(self) -> None:
        """Test all error severities are supported"""
        severities = [
            ErrorSeverity.CRITICAL,
            ErrorSeverity.HIGH,
            ErrorSeverity.MEDIUM,
            ErrorSeverity.LOW,
            ErrorSeverity.INFO
        ]

        for severity in severities:
            error = self.error_handler.handle_error(
                component="test",
                error_code=f"{severity.value.upper()}_ERROR_001",
                message="Test error",
                severity=severity
            )
            self.assertEqual(error.severity, severity)


if __name__ == "__main__":
    unittest.main()
