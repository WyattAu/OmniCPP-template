"""
Compiler Detection Logging Integration

This module provides structured logging for compiler detection operations,
including file logging with rotation and support for multiple log levels.
"""

import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

from .msvc_detector import (
    Architecture,
    CompilerType,
    VersionInfo,
)


class CompilerDetectionLogger:
    """
    Logger for compiler detection operations.

    Provides structured logging with context information including
    compiler type, version, path, and architecture. Supports
    file logging with rotation and multiple log levels.
    """

    def __init__(
        self,
        name: str = "compiler_detection",
        level: str = "INFO",
        log_file: Optional[str] = None,
        log_dir: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        verbose: bool = False,
    ) -> None:
        """
        Initialize the compiler detection logger.

        Args:
            name: Logger name
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Specific log file path (overrides log_dir)
            log_dir: Directory for log files (defaults to 'logs')
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            verbose: Enable verbose output to console
        """
        self._name = name
        self._level = self._parse_log_level(level)
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._verbose = verbose

        # Create logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._level)

        # Clear existing handlers
        self._logger.handlers.clear()

        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler(log_file, log_dir)

    def _parse_log_level(self, level: str) -> int:
        """
        Parse log level string to logging constant.

        Args:
            level: Log level string

        Returns:
            Logging level constant

        Raises:
            ValueError: If log level is invalid
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        level_upper = level.upper()
        if level_upper not in level_map:
            raise ValueError(
                f"Invalid log level: {level}. "
                f"Must be one of: {', '.join(level_map.keys())}"
            )

        return level_map[level_upper]

    def _setup_console_handler(self) -> None:
        """Setup console handler for logging."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self._level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        self._logger.addHandler(console_handler)

    def _setup_file_handler(
        self,
        log_file: Optional[str],
        log_dir: Optional[str],
    ) -> None:
        """
        Setup file handler with rotation for logging.

        Args:
            log_file: Specific log file path
            log_dir: Directory for log files
        """
        # Determine log file path
        if log_file:
            log_path = Path(log_file)
        else:
            # Use default log directory
            if log_dir is None:
                log_dir = "logs"

            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)

            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file_name = f"{self._name}_{timestamp}.log"
            log_path = log_path / log_file_name

        # Create rotating file handler
        file_handler = RotatingFileHandler(
            filename=str(log_path),
            maxBytes=self._max_bytes,
            backupCount=self._backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(self._level)

        # Create formatter with more detail for file logs
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - "
            "[%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)

    def _format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context dictionary for logging.

        Args:
            context: Context dictionary

        Returns:
            Formatted context string
        """
        if not context:
            return ""

        parts: list[str] = []
        for key, value in context.items():
            if value is not None:
                parts.append(f"{key}={value}")

        return f" | Context: {', '.join(parts)}" if parts else ""

    def log_detection_start(
        self,
        component: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log the start of a detection operation.

        Args:
            component: Component being detected (e.g., "MSVC", "MinGW")
            context: Additional context information
        """
        context_str = self._format_context(context or {})
        self._logger.info(f"Starting detection for {component}{context_str}")

    def log_detection_success(
        self,
        component: str,
        count: int,
        duration: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log successful detection operation.

        Args:
            component: Component that was detected
            count: Number of items detected
            duration: Detection duration in seconds
            context: Additional context information
        """
        context_str = self._format_context(context or {})
        self._logger.info(
            f"Detection complete for {component}: "
            f"found {count} items in {duration:.2f}s{context_str}"
        )

    def log_detection_failure(
        self,
        component: str,
        error: str,
        exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log failed detection operation.

        Args:
            component: Component that failed detection
            error: Error message
            exception: Exception that caused the failure (optional)
            context: Additional context information
        """
        context_str = self._format_context(context or {})
        log_message = f"Detection failed for {component}: {error}{context_str}"

        if exception:
            self._logger.error(log_message, exc_info=exception)
        else:
            self._logger.error(log_message)

    def log_detection_warning(
        self,
        component: str,
        warning: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a warning during detection operation.

        Args:
            component: Component being detected
            warning: Warning message
            context: Additional context information
        """
        context_str = self._format_context(context or {})
        self._logger.warning(f"Detection warning for {component}: {warning}{context_str}")

    def log_compiler_selected(
        self,
        compiler_type: CompilerType,
        architecture: Architecture,
        version: VersionInfo,
        path: str,
    ) -> None:
        """
        Log compiler selection.

        Args:
            compiler_type: Type of compiler
            architecture: Target architecture
            version: Compiler version
            path: Compiler path
        """
        context = {
            "compiler_type": compiler_type.value,
            "architecture": architecture.value,
            "version": str(version),
            "path": path,
        }
        self._logger.info(
            f"Selected compiler: {compiler_type.value} {architecture.value} {version}"
        )
        if self._verbose:
            self._logger.debug(f"Compiler details: {context}")

    def log_terminal_selected(
        self,
        terminal_id: str,
        terminal_name: str,
        terminal_type: str,
    ) -> None:
        """
        Log terminal selection.

        Args:
            terminal_id: Terminal identifier
            terminal_name: Terminal name
            terminal_type: Terminal type
        """
        context = {
            "terminal_id": terminal_id,
            "terminal_name": terminal_name,
            "terminal_type": terminal_type,
        }
        self._logger.info(f"Selected terminal: {terminal_name} ({terminal_id})")
        if self._verbose:
            self._logger.debug(f"Terminal details: {context}")

    def log_environment_setup(
        self,
        compiler_type: CompilerType,
        architecture: Architecture,
        env_vars: Dict[str, str],
    ) -> None:
        """
        Log environment setup.

        Args:
            compiler_type: Type of compiler
            architecture: Target architecture
            env_vars: Environment variables set
        """
        context = {
            "compiler_type": compiler_type.value,
            "architecture": architecture.value,
            "env_vars_count": len(env_vars),
        }
        self._logger.info(
            f"Setting up environment for {compiler_type.value} {architecture.value}"
        )
        if self._verbose:
            self._logger.debug(f"Environment variables: {list(env_vars.keys())}")
        self._logger.debug(f"Environment setup: {context}")

    def log_command_execution(
        self,
        command: str,
        duration: float,
        success: bool,
        exit_code: Optional[int] = None,
    ) -> None:
        """
        Log command execution.

        Args:
            command: Command that was executed
            duration: Execution duration in seconds
            success: Whether command succeeded
            exit_code: Exit code (optional)
        """
        status = "succeeded" if success else "failed"
        context: Dict[str, Any] = {
            "command": command,
            "duration": f"{duration:.2f}s",
            "status": status,
        }
        if exit_code is not None:
            context["exit_code"] = str(exit_code)

        self._logger.info(f"Command {status}: {command} (took {duration:.2f}s)")
        if self._verbose:
            self._logger.debug(f"Command execution details: {context}")

    def log_cache_hit(self, key: str) -> None:
        """
        Log cache hit.

        Args:
            key: Cache key
        """
        self._logger.debug(f"Cache hit for key: {key}")

    def log_cache_miss(self, key: str) -> None:
        """
        Log cache miss.

        Args:
            key: Cache key
        """
        self._logger.debug(f"Cache miss for key: {key}")

    def log_cache_invalidation(self, key: Optional[str] = None) -> None:
        """
        Log cache invalidation.

        Args:
            key: Cache key to invalidate, or None for all
        """
        if key:
            self._logger.debug(f"Invalidating cache for key: {key}")
        else:
            self._logger.debug("Invalidating entire cache")

    def log_validation_result(
        self,
        component: str,
        is_valid: bool,
        errors: Optional[list[str]] = None,
        warnings: Optional[list[str]] = None,
    ) -> None:
        """
        Log validation result.

        Args:
            component: Component being validated
            is_valid: Whether validation passed
            errors: List of errors (optional)
            warnings: List of warnings (optional)
        """
        status = "passed" if is_valid else "failed"
        context: Dict[str, Any] = {"component": component, "status": status}

        if is_valid:
            self._logger.info(f"Validation {status} for {component}")
        else:
            self._logger.warning(f"Validation {status} for {component}")
            if errors:
                context["errors"] = ", ".join(errors)
                for error in errors:
                    self._logger.error(f"  - Error: {error}")
            if warnings:
                context["warnings"] = ", ".join(warnings)
                for warning in warnings:
                    self._logger.warning(f"  - Warning: {warning}")

        if self._verbose:
            self._logger.debug(f"Validation details: {context}")

    def set_level(self, level: str) -> None:
        """
        Set the logging level.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._level = self._parse_log_level(level)
        self._logger.setLevel(self._level)

        # Update all handlers
        for handler in self._logger.handlers:
            handler.setLevel(self._level)

    def get_level(self) -> str:
        """
        Get the current logging level.

        Returns:
            Current logging level as string
        """
        level_map = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL",
        }
        return level_map.get(self._level, "INFO")

    def enable_verbose(self) -> None:
        """Enable verbose logging."""
        self._verbose = True

    def disable_verbose(self) -> None:
        """Disable verbose logging."""
        self._verbose = False

    def is_verbose(self) -> bool:
        """
        Check if verbose logging is enabled.

        Returns:
            True if verbose logging is enabled
        """
        return self._verbose

    def close(self) -> None:
        """Close all handlers and cleanup resources."""
        for handler in self._logger.handlers[:]:
            handler.close()
            self._logger.removeHandler(handler)


# Global logger instance
_global_logger: Optional[CompilerDetectionLogger] = None


def get_logger(
    name: str = "compiler_detection",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: Optional[str] = None,
    verbose: bool = False,
) -> CompilerDetectionLogger:
    """
    Get or create the global logger instance.

    Args:
        name: Logger name
        level: Log level
        log_file: Specific log file path
        log_dir: Directory for log files
        verbose: Enable verbose output

    Returns:
        CompilerDetectionLogger instance
    """
    global _global_logger

    if _global_logger is None:
        _global_logger = CompilerDetectionLogger(
            name=name,
            level=level,
            log_file=log_file,
            log_dir=log_dir,
            verbose=verbose,
        )

    return _global_logger


def reset_logger() -> None:
    """Reset the global logger instance."""
    global _global_logger

    if _global_logger is not None:
        _global_logger.close()
        _global_logger = None
