# Python Logging Infrastructure Requirements

**Document ID:** req_logging_01
**Component:** Python Logging System
**Status:** Draft
**Created:** 2026-01-06

---

## 1. Overview

This document defines requirements for a robust, production-ready Python logging infrastructure for the OmniCPP project. The logging system must replace the current simple print-based logging with a comprehensive solution supporting multiple handlers, log levels, formatters, and configuration-driven behavior.

### 1.1 Current State

The current implementation in [`omni_scripts/utils/logging_utils.py`](omni_scripts/utils/logging_utils.py) provides basic logging functions:

- `log_info()`, `log_warning()`, `log_error()`, `log_success()`
- Simple timestamp formatting using ISO format
- Output to stdout/stderr only
- No configuration support
- No log rotation or file management

### 1.2 Target State

A full-featured logging system based on Python's standard `logging` module with:

- Configurable log levels per module
- Multiple handlers (console, file, rotating file)
- Custom formatters with rich context
- Color-coded console output
- Automatic log rotation and retention
- Thread-safe operations
- Performance-optimized for high-throughput scenarios

---

## 2. Functional Requirements

### 2.1 Log Level Configuration

**REQ-LOG-001:** The system SHALL support all standard Python logging levels:

- DEBUG (10): Detailed diagnostic information
- INFO (20): General informational messages
- WARNING (30): Warning messages for potentially harmful situations
- ERROR (40): Error messages for serious problems
- CRITICAL (50): Critical messages for severe errors

**REQ-LOG-002:** The system SHALL allow configuration of the global log level via [`config/logging_python.json`](config/logging_python.json).

**REQ-LOG-003:** The system SHALL support per-module log level overrides to enable fine-grained control over logging verbosity.

**REQ-LOG-004:** The system SHALL provide a mechanism to dynamically change log levels at runtime without restarting the application.

**REQ-LOG-005:** The system SHALL default to INFO level if no configuration is provided.

### 2.2 Custom Formatters

**REQ-LOG-006:** The system SHALL support custom log formatters configurable via JSON configuration.

**REQ-LOG-007:** The default formatter SHALL include the following fields:

- Timestamp (configurable format, default: `%Y-%m-%d %H:%M:%S`)
- Logger name (module/script identifier)
- Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Log message
- Optional: Thread ID for multi-threaded scenarios
- Optional: Process ID for multi-process scenarios

**REQ-LOG-008:** The system SHALL support structured logging with additional context fields (e.g., function name, line number, file path).

**REQ-LOG-009:** The system SHALL support JSON-formatted logs for machine-readable output and log aggregation systems.

**REQ-LOG-010:** The system SHALL allow custom format strings to be defined in configuration for flexibility.

### 2.3 Console Output

**REQ-LOG-011:** The system SHALL provide a console handler for real-time log output during development and debugging.

**REQ-LOG-012:** The console handler SHALL support color-coded output based on log level:

- DEBUG: Gray/Blue
- INFO: Green
- WARNING: Yellow
- ERROR: Red
- CRITICAL: Magenta/Bold Red

**REQ-LOG-013:** The system SHALL detect terminal capabilities and disable colors if the terminal does not support ANSI color codes.

**REQ-LOG-014:** The console handler SHALL be configurable (enabled/disabled) via [`config/logging_python.json`](config/logging_python.json).

**REQ-LOG-015:** The system SHALL provide an option to suppress console output in production environments.

### 2.4 File Output

**REQ-LOG-016:** The system SHALL provide a file handler for persistent log storage.

**REQ-LOG-017:** The file handler SHALL support log rotation based on file size (configurable via `max_bytes` parameter).

**REQ-LOG-018:** The file handler SHALL support retention policies with configurable backup count (number of rotated files to keep).

**REQ-LOG-019:** The system SHALL create log directories automatically if they do not exist.

**REQ-LOG-020:** The default log file path SHALL be `logs/omnicpp_python.log` but SHALL be configurable.

**REQ-LOG-021:** The system SHALL use a default maximum file size of 10MB (10,485,760 bytes) if not configured.

**REQ-LOG-022:** The system SHALL keep a default of 5 backup files if not configured.

**REQ-LOG-023:** The file handler SHALL support time-based rotation as an alternative to size-based rotation (TBD).

**REQ-LOG-024:** The system SHALL ensure atomic writes to prevent log corruption in multi-process scenarios.

### 2.5 Configuration Management

**REQ-LOG-025:** The system SHALL load configuration from [`config/logging_python.json`](config/logging_python.json).

**REQ-LOG-026:** The configuration SHALL support the following parameters:

- `level`: Global log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `format`: Log format string
- `datefmt`: Date/time format string
- `console_handler_enabled`: Boolean to enable/disable console output
- `file_handler_enabled`: Boolean to enable/disable file output
- `file_path`: Path to log file
- `max_bytes`: Maximum file size before rotation
- `backup_count`: Number of backup files to retain
- `colored_output`: Boolean to enable/disable colored console output

**REQ-LOG-027:** The system SHALL validate configuration values and provide clear error messages for invalid settings.

**REQ-LOG-028:** The system SHALL provide sensible defaults if configuration file is missing or incomplete.

**REQ-LOG-029:** The system SHALL support environment variable overrides for critical configuration parameters (TBD).

**REQ-LOG-030:** The system SHALL reload configuration without application restart (TBD).

### 2.6 Integration with Python Scripts

**REQ-LOG-031:** The system SHALL provide a unified logging interface that can be imported by all Python scripts in the project.

**REQ-LOG-032:** The system SHALL maintain backward compatibility with existing logging functions (`log_info`, `log_warning`, `log_error`, `log_success`) during migration.

**REQ-LOG-033:** The system SHALL provide a factory function or context manager to initialize logging for each module.

**REQ-LOG-034:** The system SHALL support automatic logger name resolution based on the calling module's `__name__`.

**REQ-LOG-035:** The system SHALL integrate with the controller ([`OmniCppController.py`](OmniCppController.py)) to provide centralized logging configuration.

**REQ-LOG-036:** The system SHALL support logging from utility modules in [`omni_scripts/utils/`](omni_scripts/utils/) with appropriate logger names.

**REQ-LOG-037:** The system SHALL support logging from validator modules in [`omni_scripts/validators/`](omni_scripts/validators/) with appropriate logger names.

---

## 3. Non-Functional Requirements

### 3.1 Performance

**REQ-LOG-038:** The logging system SHALL have minimal performance impact on application execution (< 1% overhead for INFO level and above).

**REQ-LOG-039:** The system SHALL use lazy evaluation of log messages to avoid string formatting when the log level is disabled.

**REQ-LOG-040:** The system SHALL support asynchronous logging for high-throughput scenarios (TBD).

**REQ-LOG-041:** File I/O operations SHALL be buffered to reduce disk writes and improve performance.

**REQ-LOG-042:** The system SHALL avoid blocking the main thread during log file rotation.

### 3.2 Thread Safety

**REQ-LOG-043:** The logging system SHALL be thread-safe and support concurrent logging from multiple threads.

**REQ-LOG-044:** The system SHALL use Python's built-in thread-safe logging handlers or implement appropriate locking mechanisms.

**REQ-LOG-045:** Log messages from different threads SHALL not be interleaved or corrupted.

**REQ-LOG-046:** The system SHALL handle thread shutdown gracefully to prevent log loss during application termination.

### 3.3 Reliability

**REQ-LOG-047:** The system SHALL handle file system errors gracefully (e.g., disk full, permission denied) without crashing the application.

**REQ-LOG-048:** The system SHALL log errors that occur during logging operations to stderr as a fallback.

**REQ-LOG-049:** The system SHALL ensure log files are properly closed on application shutdown.

**REQ-LOG-050:** The system SHALL prevent log file corruption during abnormal termination.

### 3.4 Maintainability

**REQ-LOG-051:** The logging code SHALL be well-documented with clear docstrings and type hints.

**REQ-LOG-052:** The system SHALL follow Python logging best practices and PEP 282 guidelines.

**REQ-LOG-053:** The system SHALL provide clear error messages for configuration issues.

**REQ-LOG-054:** The system SHALL be easily extensible to support custom handlers and formatters.

---

## 4. Integration Requirements

### 4.1 Controller Integration

**REQ-LOG-055:** The controller SHALL initialize the logging system on startup.

**REQ-LOG-056:** The controller SHALL pass configuration file path to the logging system.

**REQ-LOG-057:** The controller SHALL handle logging initialization errors gracefully and fall back to basic logging.

**REQ-LOG-058:** The controller SHALL provide a mechanism to change log levels via command-line arguments (TBD).

### 4.2 Cross-Platform Compatibility

**REQ-LOG-059:** The logging system SHALL work correctly on Windows, Linux, and macOS.

**REQ-LOG-060:** File paths SHALL be handled correctly across different operating systems (using `os.path` or `pathlib`).

**REQ-LOG-061:** Color codes SHALL work correctly across different terminal emulators.

**REQ-LOG-062:** The system SHALL handle platform-specific file system limitations (e.g., maximum path length on Windows).

---

## 5. Migration Requirements

### 5.1 Backward Compatibility

**REQ-LOG-063:** The system SHALL maintain the existing API (`log_info`, `log_warning`, `log_error`, `log_success`) during the transition period.

**REQ-LOG-064:** Existing scripts using the old logging functions SHALL continue to work without modification.

**REQ-LOG-065:** The system SHALL provide deprecation warnings for old logging functions to encourage migration.

### 5.2 Migration Path

**REQ-LOG-066:** The system SHALL provide a migration guide for updating scripts to use the new logging API.

**REQ-LOG-067:** The system SHALL support both old and new logging APIs simultaneously during the migration phase.

**REQ-LOG-068:** The migration SHALL be incremental, allowing scripts to be updated one at a time.

---

## 6. Testing Requirements

### 6.1 Unit Tests

**REQ-LOG-069:** Unit tests SHALL verify log level filtering works correctly.

**REQ-LOG-070:** Unit tests SHALL verify formatter output matches expected format.

**REQ-LOG-071:** Unit tests SHALL verify configuration loading and validation.

**REQ-LOG-072:** Unit tests SHALL verify log rotation triggers at the correct file size.

### 6.2 Integration Tests

**REQ-LOG-073:** Integration tests SHALL verify logging works correctly with the controller.

**REQ-LOG-074:** Integration tests SHALL verify logging works correctly across multiple modules.

**REQ-LOG-075:** Integration tests SHALL verify file handler creates and rotates log files correctly.

### 6.3 Performance Tests

**REQ-LOG-076:** Performance tests SHALL measure logging overhead under high load.

**REQ-LOG-077:** Performance tests SHALL verify thread safety under concurrent logging.

---

## 7. Documentation Requirements

**REQ-LOG-078:** The system SHALL include comprehensive documentation in the codebase.

**REQ-LOG-079:** Documentation SHALL include usage examples for common scenarios.

**REQ-LOG-080:** Documentation SHALL explain configuration options and their effects.

**REQ-LOG-081:** Documentation SHALL include troubleshooting guide for common logging issues.

**REQ-LOG-082:** Documentation SHALL be updated in the project's MkDocs site.

---

## 8. Success Criteria

The Python logging infrastructure is considered complete when:

1. All functional requirements (REQ-LOG-001 to REQ-LOG-037) are implemented and tested
2. All non-functional requirements (REQ-LOG-038 to REQ-LOG-054) are met
3. Integration with the controller is working correctly
4. All Python scripts in the project use the new logging system
5. Configuration via [`config/logging_python.json`](config/logging_python.json) is fully functional
6. Log rotation and retention policies are working as expected
7. Thread safety is verified through testing
8. Performance impact is within acceptable limits (< 1% overhead)
9. Documentation is complete and up-to-date
10. Migration from old logging functions is complete

---

## 9. Open Questions / TBD Items

- **REQ-LOG-023:** Should time-based rotation be implemented in addition to size-based rotation?
- **REQ-LOG-029:** Which environment variables should be supported for configuration overrides?
- **REQ-LOG-030:** Should configuration hot-reload be implemented?
- **REQ-LOG-040:** Should asynchronous logging be implemented for high-throughput scenarios?
- **REQ-LOG-058:** Should command-line arguments for log level control be implemented?

These items are marked as TBD and will be addressed during the design phase based on project priorities and requirements.

