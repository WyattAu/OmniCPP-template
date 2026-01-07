"""
Unit tests for Compiler Detection Logging Integration

Tests the CompilerDetectionLogger class including:
- Structured logging with context
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File logging with rotation
- All logging methods
"""

import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add scripts/python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from compilers.logging_integration import (
    CompilerDetectionLogger,
    get_logger,
    reset_logger,
)
from compilers.msvc_detector import (
    Architecture,
    CompilerType,
    VersionInfo,
)


class TestCompilerDetectionLogger(unittest.TestCase):
    """Test cases for CompilerDetectionLogger class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create temporary directory for log files
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")

        # Reset global logger before each test
        reset_logger()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        # Clean up temporary files
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

        # Reset global logger
        reset_logger()

    def test_logger_initialization(self) -> None:
        """Test logger initialization with default parameters."""
        logger = CompilerDetectionLogger()

        self.assertIsNotNone(logger._logger)
        self.assertEqual(logger._level, logging.INFO)
        self.assertFalse(logger._verbose)
        self.assertEqual(logger.get_level(), "INFO")

    def test_logger_initialization_with_custom_level(self) -> None:
        """Test logger initialization with custom log level."""
        logger = CompilerDetectionLogger(level="DEBUG")

        self.assertEqual(logger._level, logging.DEBUG)
        self.assertEqual(logger.get_level(), "DEBUG")

    def test_logger_initialization_with_log_file(self) -> None:
        """Test logger initialization with custom log file."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        self.assertTrue(os.path.exists(self.log_file))
        logger.close()

    def test_logger_initialization_with_log_dir(self) -> None:
        """Test logger initialization with custom log directory."""
        logger = CompilerDetectionLogger(log_dir=self.temp_dir)

        # Check that log file was created in the directory
        log_files = [f for f in os.listdir(self.temp_dir) if f.endswith(".log")]
        self.assertTrue(len(log_files) > 0)
        logger.close()

    def test_logger_initialization_with_verbose(self) -> None:
        """Test logger initialization with verbose mode."""
        logger = CompilerDetectionLogger(verbose=True)

        self.assertTrue(logger._verbose)
        self.assertTrue(logger.is_verbose())

    def test_invalid_log_level(self) -> None:
        """Test that invalid log level raises ValueError."""
        with self.assertRaises(ValueError) as context:
            CompilerDetectionLogger(level="INVALID")

        self.assertIn("Invalid log level", str(context.exception))

    def test_log_detection_start(self) -> None:
        """Test logging detection start."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_detection_start("MSVC")

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Starting detection for MSVC", call_args)

        logger.close()

    def test_log_detection_start_with_context(self) -> None:
        """Test logging detection start with context."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        context = {"architecture": "x64", "search_paths": 3}
        with patch.object(logger._logger, "info") as mock_info:
            logger.log_detection_start("MSVC", context)

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Starting detection for MSVC", call_args)
            self.assertIn("architecture=x64", call_args)
            self.assertIn("search_paths=3", call_args)

        logger.close()

    def test_log_detection_success(self) -> None:
        """Test logging detection success."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_detection_success("MSVC", count=5, duration=1.23)

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Detection complete for MSVC", call_args)
            self.assertIn("found 5 items", call_args)
            self.assertIn("1.23s", call_args)

        logger.close()

    def test_log_detection_success_with_context(self) -> None:
        """Test logging detection success with context."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        context = {"architecture": "x64", "method": "vswhere"}
        with patch.object(logger._logger, "info") as mock_info:
            logger.log_detection_success(
                "MSVC", count=3, duration=0.5, context=context
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Detection complete for MSVC", call_args)
            self.assertIn("architecture=x64", call_args)
            self.assertIn("method=vswhere", call_args)

        logger.close()

    def test_log_detection_failure(self) -> None:
        """Test logging detection failure."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "error") as mock_error:
            logger.log_detection_failure("MinGW", error="Not found")

            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            self.assertIn("Detection failed for MinGW", call_args)
            self.assertIn("Not found", call_args)

        logger.close()

    def test_log_detection_failure_with_exception(self) -> None:
        """Test logging detection failure with exception."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        exception = Exception("Test exception")
        with patch.object(logger._logger, "error") as mock_error:
            logger.log_detection_failure(
                "MinGW", error="Not found", exception=exception
            )

            mock_error.assert_called_once()
            # Check that exc_info was passed
            self.assertIn("exc_info", mock_error.call_args[1])

        logger.close()

    def test_log_detection_failure_with_context(self) -> None:
        """Test logging detection failure with context."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        context = {"path": "/invalid/path", "attempt": 1}
        with patch.object(logger._logger, "error") as mock_error:
            logger.log_detection_failure(
                "MinGW", error="Not found", context=context
            )

            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            self.assertIn("Detection failed for MinGW", call_args)
            self.assertIn("path=/invalid/path", call_args)
            self.assertIn("attempt=1", call_args)

        logger.close()

    def test_log_detection_warning(self) -> None:
        """Test logging detection warning."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "warning") as mock_warning:
            logger.log_detection_warning("MSVC", warning="Partial detection")

            mock_warning.assert_called_once()
            call_args = mock_warning.call_args[0][0]
            self.assertIn("Detection warning for MSVC", call_args)
            self.assertIn("Partial detection", call_args)

        logger.close()

    def test_log_detection_warning_with_context(self) -> None:
        """Test logging detection warning with context."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        context = {"component": "vswhere", "warning_code": "WARN_001"}
        with patch.object(logger._logger, "warning") as mock_warning:
            logger.log_detection_warning(
                "MSVC", warning="Partial detection", context=context
            )

            mock_warning.assert_called_once()
            call_args = mock_warning.call_args[0][0]
            self.assertIn("Detection warning for MSVC", call_args)
            self.assertIn("component=vswhere", call_args)
            self.assertIn("warning_code=WARN_001", call_args)

        logger.close()

    def test_log_compiler_selected(self) -> None:
        """Test logging compiler selection."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        compiler_type = CompilerType.MSVC
        architecture = Architecture.X64
        version = VersionInfo(major=19, minor=40, patch=0)
        path = r"C:\Program Files\Microsoft Visual Studio\2022\cl.exe"

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_compiler_selected(compiler_type, architecture, version, path)

            mock_info.assert_called()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Selected compiler", call_args)
            self.assertIn("msvc", call_args)
            self.assertIn("x64", call_args)
            self.assertIn("19.40.0", call_args)

        logger.close()

    def test_log_compiler_selected_verbose(self) -> None:
        """Test logging compiler selection in verbose mode."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, verbose=True
        )

        compiler_type = CompilerType.MSVC
        architecture = Architecture.X64
        version = VersionInfo(major=19, minor=40, patch=0)
        path = r"C:\Program Files\Microsoft Visual Studio\2022\cl.exe"

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_compiler_selected(compiler_type, architecture, version, path)

            # Debug should be called with compiler details
            mock_debug.assert_called()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Compiler details", call_args)

        logger.close()

    def test_log_terminal_selected(self) -> None:
        """Test logging terminal selection."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_terminal_selected(
                "x64_native", "x64 Native Tools Command Prompt", "msvc"
            )

            mock_info.assert_called()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Selected terminal", call_args)
            self.assertIn("x64 Native Tools Command Prompt", call_args)
            self.assertIn("x64_native", call_args)

        logger.close()

    def test_log_terminal_selected_verbose(self) -> None:
        """Test logging terminal selection in verbose mode."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, verbose=True
        )

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_terminal_selected(
                "x64_native", "x64 Native Tools Command Prompt", "msvc"
            )

            # Debug should be called with terminal details
            mock_debug.assert_called()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Terminal details", call_args)

        logger.close()

    def test_log_environment_setup(self) -> None:
        """Test logging environment setup."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        compiler_type = CompilerType.MSVC
        architecture = Architecture.X64
        env_vars = {"PATH": "/new/path", "INCLUDE": "/new/include"}

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_environment_setup(compiler_type, architecture, env_vars)

            mock_info.assert_called()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Setting up environment", call_args)
            self.assertIn("msvc", call_args)
            self.assertIn("x64", call_args)

        logger.close()

    def test_log_environment_setup_verbose(self) -> None:
        """Test logging environment setup in verbose mode."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, verbose=True
        )

        compiler_type = CompilerType.MSVC
        architecture = Architecture.X64
        env_vars = {"PATH": "/new/path", "INCLUDE": "/new/include"}

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_environment_setup(compiler_type, architecture, env_vars)

            # Debug should be called with environment variable keys
            mock_debug.assert_called()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Environment setup", call_args)

        logger.close()

    def test_log_command_execution_success(self) -> None:
        """Test logging successful command execution."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_command_execution(
                "cmake --version", duration=0.5, success=True
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Command succeeded", call_args)
            self.assertIn("cmake --version", call_args)
            self.assertIn("0.50s", call_args)

        logger.close()

    def test_log_command_execution_failure(self) -> None:
        """Test logging failed command execution."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_command_execution(
                "invalid_command", duration=0.1, success=False, exit_code=1
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Command failed", call_args)
            self.assertIn("invalid_command", call_args)

        logger.close()

    def test_log_command_execution_verbose(self) -> None:
        """Test logging command execution in verbose mode."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, verbose=True
        )

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_command_execution(
                "cmake --version", duration=0.5, success=True
            )

            # Debug should be called with command details
            mock_debug.assert_called()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Command execution details", call_args)

        logger.close()

    def test_log_cache_hit(self) -> None:
        """Test logging cache hit."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_cache_hit("msvc_x64")

            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Cache hit", call_args)
            self.assertIn("msvc_x64", call_args)

        logger.close()

    def test_log_cache_miss(self) -> None:
        """Test logging cache miss."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_cache_miss("mingw_x64")

            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Cache miss", call_args)
            self.assertIn("mingw_x64", call_args)

        logger.close()

    def test_log_cache_invalidation_key(self) -> None:
        """Test logging cache invalidation for specific key."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_cache_invalidation("msvc_x64")

            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Invalidating cache", call_args)
            self.assertIn("msvc_x64", call_args)

        logger.close()

    def test_log_cache_invalidation_all(self) -> None:
        """Test logging cache invalidation for all keys."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_cache_invalidation()

            mock_debug.assert_called_once()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Invalidating entire cache", call_args)

        logger.close()

    def test_log_validation_result_success(self) -> None:
        """Test logging successful validation result."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with patch.object(logger._logger, "info") as mock_info:
            logger.log_validation_result("MSVC", is_valid=True)

            mock_info.assert_called_once()
            call_args = mock_info.call_args[0][0]
            self.assertIn("Validation passed", call_args)
            self.assertIn("MSVC", call_args)

        logger.close()

    def test_log_validation_result_failure(self) -> None:
        """Test logging failed validation result."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        errors = ["Executable not found", "Invalid version"]
        warnings = ["Missing SDK"]

        with patch.object(logger._logger, "warning") as mock_warning:
            with patch.object(logger._logger, "error") as mock_error:
                logger.log_validation_result(
                    "MSVC",
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                )

                # Warning should be called for validation failure
                mock_warning.assert_called()
                # Error should be called for each error
                self.assertEqual(mock_error.call_count, 2)

        logger.close()

    def test_log_validation_result_verbose(self) -> None:
        """Test logging validation result in verbose mode."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, verbose=True
        )

        with patch.object(logger._logger, "debug") as mock_debug:
            logger.log_validation_result("MSVC", is_valid=True)

            # Debug should be called with validation details
            mock_debug.assert_called()
            call_args = mock_debug.call_args[0][0]
            self.assertIn("Validation details", call_args)

        logger.close()

    def test_set_level(self) -> None:
        """Test setting log level."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        logger.set_level("DEBUG")
        self.assertEqual(logger.get_level(), "DEBUG")
        self.assertEqual(logger._level, logging.DEBUG)

        logger.set_level("ERROR")
        self.assertEqual(logger.get_level(), "ERROR")
        self.assertEqual(logger._level, logging.ERROR)

        logger.close()

    def test_set_level_invalid(self) -> None:
        """Test setting invalid log level."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        with self.assertRaises(ValueError):
            logger.set_level("INVALID")

        logger.close()

    def test_enable_disable_verbose(self) -> None:
        """Test enabling and disabling verbose mode."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        self.assertFalse(logger.is_verbose())

        logger.enable_verbose()
        self.assertTrue(logger.is_verbose())

        logger.disable_verbose()
        self.assertFalse(logger.is_verbose())

        logger.close()

    def test_file_rotation(self) -> None:
        """Test that log file rotation is configured."""
        logger = CompilerDetectionLogger(
            log_file=self.log_file, max_bytes=1024, backup_count=3
        )

        # Check that rotating file handler is configured
        rotating_handler = None
        for handler in logger._logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                rotating_handler = handler
                break

        self.assertIsNotNone(rotating_handler)
        self.assertEqual(rotating_handler.maxBytes, 1024)
        self.assertEqual(rotating_handler.backupCount, 3)

        logger.close()

    def test_close(self) -> None:
        """Test closing logger and cleanup."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        initial_handler_count = len(logger._logger.handlers)
        self.assertGreater(initial_handler_count, 0)

        logger.close()

        # All handlers should be removed
        self.assertEqual(len(logger._logger.handlers), 0)

    def test_format_context_empty(self) -> None:
        """Test formatting empty context."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        result = logger._format_context({})
        self.assertEqual(result, "")

        logger.close()

    def test_format_context_with_none_values(self) -> None:
        """Test formatting context with None values."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        context = {"key1": "value1", "key2": None, "key3": "value3"}
        result = logger._format_context(context)

        self.assertIn("key1=value1", result)
        self.assertNotIn("key2", result)
        self.assertIn("key3=value3", result)

        logger.close()

    def test_all_log_levels(self) -> None:
        """Test all log levels work correctly."""
        logger = CompilerDetectionLogger(log_file=self.log_file)

        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in levels:
            logger.set_level(level)
            self.assertEqual(logger.get_level(), level)

        logger.close()


class TestGlobalLogger(unittest.TestCase):
    """Test cases for global logger functions."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        reset_logger()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        reset_logger()

    def test_get_logger_creates_instance(self) -> None:
        """Test that get_logger creates a new instance."""
        logger = get_logger()

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, CompilerDetectionLogger)

        logger.close()

    def test_get_logger_returns_same_instance(self) -> None:
        """Test that get_logger returns the same instance."""
        logger1 = get_logger()
        logger2 = get_logger()

        self.assertIs(logger1, logger2)

        logger1.close()

    def test_get_logger_with_custom_parameters(self) -> None:
        """Test get_logger with custom parameters."""
        logger = get_logger(
            name="custom_logger",
            level="DEBUG",
            verbose=True,
        )

        self.assertEqual(logger._name, "custom_logger")
        self.assertEqual(logger.get_level(), "DEBUG")
        self.assertTrue(logger.is_verbose())

        logger.close()

    def test_reset_logger(self) -> None:
        """Test resetting global logger."""
        logger1 = get_logger()
        reset_logger()

        logger2 = get_logger()

        self.assertIsNot(logger1, logger2)

        logger1.close()
        logger2.close()


if __name__ == "__main__":
    unittest.main()
