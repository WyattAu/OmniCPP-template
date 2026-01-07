# ADR-015: Structured Logging Format

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Logging

---

## Context

The OmniCPP Template project generates logs for both C++ and Python code. Unstructured logs make it difficult to analyze, search, and extract meaningful information. Structured logging provides a consistent format that enables better log analysis and debugging.

### Current State

Logs are unstructured:
- **C++ Logs:** Plain text logs with inconsistent format
- **Python Logs:** Plain text logs with inconsistent format
- **No Metadata:** No structured metadata in logs
- **No Context:** No contextual information in logs
- **Hard to Parse:** Difficult to parse and analyze logs

### Issues

1. **Unstructured:** Logs are unstructured and inconsistent
2. **No Metadata:** No structured metadata in logs
3. **No Context:** No contextual information in logs
4. **Hard to Parse:** Difficult to parse and analyze logs
5. **No Search:** Difficult to search logs
6. **No Analysis:** Difficult to perform log analysis

## Decision

Implement **structured logging format** with:
1. **JSON Format:** JSON-based structured logging
2. **Consistent Schema:** Consistent log schema across both languages
3. **Metadata:** Include metadata in all logs
4. **Context:** Include contextual information in logs
5. **Timestamps:** ISO 8601 timestamps in all logs
6. **Log Levels:** Consistent log levels across both languages

### 1. Log Schema

```json
{
  "timestamp": "2026-01-07T05:30:00.000Z",
  "level": "INFO",
  "logger": "omnicpp",
  "message": "User logged in",
  "module": "auth",
  "function": "login",
  "line": 42,
  "thread": "main",
  "process": 12345,
  "context": {
    "user_id": 123,
    "username": "john_doe",
    "ip_address": "192.168.1.1"
  },
  "exception": null
}
```

### 2. C++ Structured Logging

```cpp
// include/engine/logging/structured_logger.hpp
#pragma once

#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/fmt/ostr.h>
#include <memory>
#include <string>
#include <unordered_map>
#include <chrono>

namespace engine {
namespace logging {

/**
 * @brief Structured log entry
 */
struct LogEntry {
    std::string timestamp;
    std::string level;
    std::string logger;
    std::string message;
    std::string module;
    std::string function;
    int line;
    std::string thread;
    int process;
    std::unordered_map<std::string, std::string> context;
    std::string exception;
};

/**
 * @brief Structured logger class
 */
class StructuredLogger {
public:
    /**
     * @brief Get singleton instance
     * @return Logger instance
     */
    static StructuredLogger& getInstance();

    /**
     * @brief Initialize logger
     * @param log_file Path to log file
     * @param log_level Log level
     */
    void initialize(
        const std::string& log_file,
        LogLevel log_level = LogLevel::INFO
    );

    /**
     * @brief Log structured message
     * @param level Log level
     * @param message Message to log
     * @param module Module name
     * @param function Function name
     * @param line Line number
     * @param context Contextual information
     */
    void log(
        LogLevel level,
        const std::string& message,
        const std::string& module,
        const std::string& function,
        int line,
        const std::unordered_map<std::string, std::string>& context = {}
    );

    /**
     * @brief Log structured message with exception
     * @param level Log level
     * @param message Message to log
     * @param module Module name
     * @param function Function name
     * @param line Line number
     * @param exception Exception message
     * @param context Contextual information
     */
    void logException(
        LogLevel level,
        const std::string& message,
        const std::string& module,
        const std::string& function,
        int line,
        const std::string& exception,
        const std::unordered_map<std::string, std::string>& context = {}
    );

private:
    StructuredLogger() = default;
    ~StructuredLogger() = default;
    StructuredLogger(const StructuredLogger&) = delete;
    StructuredLogger& operator=(const StructuredLogger&) = delete;

    std::shared_ptr<spdlog::logger> logger_;
    LogLevel current_level_ = LogLevel::INFO;

    /**
     * @brief Get current timestamp
     * @return ISO 8601 timestamp
     */
    std::string getTimestamp() const;

    /**
     * @brief Get log level string
     * @param level Log level
     * @return Log level string
     */
    std::string getLevelString(LogLevel level) const;

    /**
     * @brief Get thread ID
     * @return Thread ID string
     */
    std::string getThreadId() const;

    /**
     * @brief Get process ID
     * @return Process ID
     */
    int getProcessId() const;

    /**
     * @brief Format log entry as JSON
     * @param entry Log entry
     * @return JSON-formatted log entry
     */
    std::string formatAsJson(const LogEntry& entry) const;
};

} // namespace logging
} // namespace engine
```

### 3. Python Structured Logging

```python
# omni_scripts/logging/structured_logger.py
"""Structured logger for Python."""

import logging
import json
import threading
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

class StructuredLogger:
    """Structured logger for Python."""

    _instance: Optional['StructuredLogger'] = None
    _lock = threading.Lock()

    def __new__(cls, config: Optional[Dict[str, Any]] = None) -> 'StructuredLogger':
        """Get singleton instance.

        Args:
            config: Log configuration

        Returns:
            Logger instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize structured logger.

        Args:
            config: Log configuration
        """
        if self._initialized:
            return

        self.config = config or {}
        self.logger = logging.getLogger("omnicpp")
        self._setup_logger()
        self._initialized = True

    def _setup_logger(self) -> None:
        """Setup logger with structured formatter."""
        # Set log level
        self.logger.setLevel(self.config.get('level', logging.INFO))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create file handler
        log_file = self.config.get('log_file', 'logs/omnicpp.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.config.get('level', logging.INFO))

        # Use structured formatter
        formatter = StructuredFormatter()
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log(
        self,
        level: int,
        message: str,
        module: str,
        function: str,
        line: int,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[str] = None
    ) -> None:
        """Log structured message.

        Args:
            level: Log level
            message: Message to log
            module: Module name
            function: Function name
            line: Line number
            context: Contextual information
            exception: Exception message
        """
        # Create log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": logging.getLevelName(level),
            "logger": "omnicpp",
            "message": message,
            "module": module,
            "function": function,
            "line": line,
            "thread": threading.current_thread().name,
            "process": threading.get_ident(),
        }

        # Add context if present
        if context:
            log_entry["context"] = context

        # Add exception if present
        if exception:
            log_entry["exception"] = exception

        # Log as JSON
        self.logger.log(level, json.dumps(log_entry))

    def trace(self, message: str, **kwargs) -> None:
        """Log trace message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.DEBUG - 5, message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.log(logging.CRITICAL, message, **kwargs)

class StructuredFormatter(logging.Formatter):
    """Structured formatter for JSON logging."""

    def __init__(self):
        """Initialize structured formatter."""
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record

        Returns:
            JSON-formatted log message
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": threading.current_thread().name,
            "process": threading.get_ident(),
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra'):
            log_entry.update(record.extra)

        return json.dumps(log_entry)
```

### 4. Usage Examples

```cpp
// C++ usage
#include "engine/logging/structured_logger.hpp"

int main() {
    // Initialize logger
    auto& logger = engine::logging::StructuredLogger::getInstance();
    logger.initialize("logs/omnicpp.log", engine::logging::LogLevel::INFO);

    // Log structured message
    std::unordered_map<std::string, std::string> context = {
        {"user_id", "123"},
        {"username", "john_doe"},
        {"ip_address", "192.168.1.1"}
    };

    logger.log(
        engine::logging::LogLevel::INFO,
        "User logged in",
        "auth",
        "login",
        42,
        context
    );

    // Log structured message with exception
    logger.logException(
        engine::logging::LogLevel::ERROR,
        "Login failed",
        "auth",
        "login",
        42,
        "Invalid credentials",
        context
    );

    return 0;
}
```

```python
# Python usage
from logging.structured_logger import StructuredLogger

# Create logger
logger = StructuredLogger()

# Log structured message
logger.info(
    "User logged in",
    module="auth",
    function="login",
    line=42,
    context={
        "user_id": 123,
        "username": "john_doe",
        "ip_address": "192.168.1.1"
    }
)

# Log structured message with exception
logger.error(
    "Login failed",
    module="auth",
    function="login",
    line=42,
    exception="Invalid credentials",
    context={
        "user_id": 123,
        "username": "john_doe",
        "ip_address": "192.168.1.1"
    }
)
```

## Consequences

### Positive

1. **Structured:** Logs are structured and consistent
2. **Metadata:** Includes metadata in all logs
3. **Context:** Includes contextual information in logs
4. **Parseable:** Easy to parse and analyze logs
5. **Searchable:** Easy to search logs
6. **Analyzable:** Easy to perform log analysis
7. **JSON Format:** Standard JSON format for easy processing

### Negative

1. **File Size:** JSON format increases log file size
2. **Complexity:** More complex than plain text logging
3. **Learning Curve:** Developers need to understand structured logging
4. **Performance:** Slightly slower than plain text logging

### Neutral

1. **Documentation:** Requires documentation for log schema
2. **Testing:** Need to test structured logging

## Alternatives Considered

### Alternative 1: Plain Text Logging

**Description:** Use plain text logging

**Pros:**
- Simpler implementation
- Smaller log files
- Faster logging

**Cons:**
- Unstructured logs
- No metadata
- Hard to parse
- Hard to analyze

**Rejected:** Unstructured and hard to analyze

### Alternative 2: Custom Format

**Description:** Use custom log format

**Pros:**
- Tailored to needs
- Smaller than JSON

**Cons:**
- Non-standard
- Hard to parse
- No tool support

**Rejected:** Non-standard and hard to parse

### Alternative 3: No Logging

**Description:** No logging system

**Pros:**
- No dependencies
- No complexity

**Cons:**
- No debugging capability
- No audit trail
- Poor developer experience

**Rejected:** No debugging capability

## Related ADRs

- [ADR-013: Dual logging system (spdlog for C++, custom for Python)](ADR-013-dual-logging-system.md)
- [ADR-014: File rotation and log retention policy](ADR-014-file-rotation-retention.md)

## References

- [Structured Logging](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html)
- [JSON Logging](https://www.loggly.com/blog/json-logging-best-practices/)
- [ECS Schema](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
