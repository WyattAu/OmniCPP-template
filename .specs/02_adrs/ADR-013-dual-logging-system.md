# ADR-013: Dual Logging System (spdlog for C++, Custom for Python)

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Logging

---

## Context

The OmniCPP Template project uses both C++ and Python code. Each language requires different logging approaches due to their different ecosystems and requirements. A unified logging strategy is needed to ensure consistent logging across both languages while leveraging language-specific best practices.

### Current State

Logging is implemented inconsistently:

- **C++:** Uses various logging approaches (std::cout, printf, custom logging)
- **Python:** Uses standard logging module with inconsistent configuration
- **No Unified Format:** Different log formats across languages
- **No Log Levels:** Inconsistent log level usage
- **No Structured Logging:** No structured logging for analysis

### Issues

1. **Inconsistent Logging:** Different logging approaches across languages
2. **No Unified Format:** Different log formats make analysis difficult
3. **No Log Rotation:** No automatic log rotation
4. **No Structured Logging:** No structured logging for analysis
5. **Performance:** Poor logging performance in C++
6. **No Thread Safety:** No thread-safe logging in C++

## Decision

Implement a **dual logging system** with:

1. **C++ Logging:** Use spdlog for high-performance, thread-safe logging
2. **Python Logging:** Use custom logging module with structured logging
3. **Unified Format:** Consistent log format across both languages
4. **Log Levels:** Consistent log levels across both languages
5. **Log Rotation:** Automatic log rotation for both languages
6. **Structured Logging:** JSON-based structured logging for analysis

### 1. C++ Logging with spdlog

```cpp
// include/engine/logging/logger.hpp
#pragma once

#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/sinks/rotating_file_sink.h>
#include <memory>
#include <string>

namespace engine {
namespace logging {

/**
 * @brief Log levels
 */
enum class LogLevel {
    TRACE = 0,
    DEBUG = 1,
    INFO = 2,
    WARN = 3,
    ERROR = 4,
    CRITICAL = 5,
    OFF = 6
};

/**
 * @brief Logger class for C++ logging
 */
class Logger {
public:
    /**
     * @brief Get singleton instance
     * @return Logger instance
     */
    static Logger& getInstance();

    /**
     * @brief Initialize logger
     * @param log_file Path to log file
     * @param log_level Log level
     * @param max_file_size Maximum file size in bytes
     * @param max_files Maximum number of files
     */
    void initialize(
        const std::string& log_file,
        LogLevel log_level = LogLevel::INFO,
        size_t max_file_size = 1024 * 1024 * 5,  // 5 MB
        size_t max_files = 3
    );

    /**
     * @brief Set log level
     * @param level Log level
     */
    void setLogLevel(LogLevel level);

    /**
     * @brief Get log level
     * @return Current log level
     */
    LogLevel getLogLevel() const;

    /**
     * @brief Log trace message
     * @param message Message to log
     */
    void trace(const std::string& message);

    /**
     * @brief Log debug message
     * @param message Message to log
     */
    void debug(const std::string& message);

    /**
     * @brief Log info message
     * @param message Message to log
     */
    void info(const std::string& message);

    /**
     * @brief Log warning message
     * @param message Message to log
     */
    void warn(const std::string& message);

    /**
     * @brief Log error message
     * @param message Message to log
     */
    void error(const std::string& message);

    /**
     * @brief Log critical message
     * @param message Message to log
     */
    void critical(const std::string& message);

    /**
     * @brief Flush logger
     */
    void flush();

private:
    Logger() = default;
    ~Logger() = default;
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    std::shared_ptr<spdlog::logger> logger_;
    LogLevel current_level_ = LogLevel::INFO;
};

} // namespace logging
} // namespace engine
```

```cpp
// src/engine/logging/logger.cpp
#include "engine/logging/logger.hpp"
#include <spdlog/spdlog.h>
#include <spdlog/sinks/rotating_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/pattern_formatter.h>
#include <filesystem>

namespace engine {
namespace logging {

Logger& Logger::getInstance() {
    static Logger instance;
    return instance;
}

void Logger::initialize(
    const std::string& log_file,
    LogLevel log_level,
    size_t max_file_size,
    size_t max_files
) {
    // Create log directory if it doesn't exist
    std::filesystem::path log_path(log_file);
    std::filesystem::create_directories(log_path.parent_path());

    // Create rotating file sink
    auto file_sink = std::make_shared<spdlog::sinks::rotating_file_sink_mt>(
        log_file,
        max_file_size,
        max_files
    );

    // Create console sink
    auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();

    // Set log pattern (JSON format for structured logging)
    std::string pattern = R"({"timestamp":"%Y-%m-%dT%H:%M:%S.%e%z","level":"%l","message":"%v"})";
    file_sink->set_pattern(pattern);
    console_sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] %v");

    // Create logger with both sinks
    std::vector<spdlog::sink_ptr> sinks = {file_sink, console_sink};
    logger_ = std::make_shared<spdlog::logger>("omnicpp", sinks.begin(), sinks.end());

    // Set log level
    setLogLevel(log_level);

    // Register logger
    spdlog::register_logger(logger_);
    spdlog::set_default_logger(logger_);
}

void Logger::setLogLevel(LogLevel level) {
    current_level_ = level;
    spdlog::level::level_enum spdlog_level;

    switch (level) {
        case LogLevel::TRACE:
            spdlog_level = spdlog::level::trace;
            break;
        case LogLevel::DEBUG:
            spdlog_level = spdlog::level::debug;
            break;
        case LogLevel::INFO:
            spdlog_level = spdlog::level::info;
            break;
        case LogLevel::WARN:
            spdlog_level = spdlog::level::warn;
            break;
        case LogLevel::ERROR:
            spdlog_level = spdlog::level::err;
            break;
        case LogLevel::CRITICAL:
            spdlog_level = spdlog::level::critical;
            break;
        case LogLevel::OFF:
            spdlog_level = spdlog::level::off;
            break;
    }

    logger_->set_level(spdlog_level);
}

LogLevel Logger::getLogLevel() const {
    return current_level_;
}

void Logger::trace(const std::string& message) {
    logger_->trace(message);
}

void Logger::debug(const std::string& message) {
    logger_->debug(message);
}

void Logger::info(const std::string& message) {
    logger_->info(message);
}

void Logger::warn(const std::string& message) {
    logger_->warn(message);
}

void Logger::error(const std::string& message) {
    logger_->error(message);
}

void Logger::critical(const std::string& message) {
    logger_->critical(message);
}

void Logger::flush() {
    logger_->flush();
}

} // namespace logging
} // namespace engine
```

### 2. Python Logging Module

```python
# omni_scripts/logging/logger.py
"""Custom logging module for Python."""

import logging
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import threading

from logging.config import LogConfig
from logging.formatters import JSONFormatter
from logging.handlers import RotatingFileHandler

class Logger:
    """Custom logger for Python."""

    _instance: Optional['Logger'] = None
    _lock = threading.Lock()

    def __new__(cls, config: Optional[LogConfig] = None) -> 'Logger':
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

    def __init__(self, config: Optional[LogConfig] = None):
        """Initialize logger.

        Args:
            config: Log configuration
        """
        if self._initialized:
            return

        self.config = config or LogConfig()
        self.logger = logging.getLogger("omnicpp")
        self._setup_logger()
        self._initialized = True

    def _setup_logger(self) -> None:
        """Setup logger with handlers and formatters."""
        # Set log level
        self.logger.setLevel(self.config.level)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create file handler with rotation
        if self.config.log_file:
            file_handler = RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.max_files,
                encoding='utf-8'
            )
            file_handler.setLevel(self.config.level)

            # Use JSON formatter for structured logging
            file_formatter = JSONFormatter()
            file_handler.setFormatter(file_formatter)

            self.logger.addHandler(file_handler)

        # Create console handler
        if self.config.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.config.level)

            # Use simple formatter for console
            console_formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)

            self.logger.addHandler(console_handler)

    def set_level(self, level: int) -> None:
        """Set log level.

        Args:
            level: Log level
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def get_level(self) -> int:
        """Get log level.

        Returns:
            Current log level
        """
        return self.logger.level

    def trace(self, message: str, **kwargs) -> None:
        """Log trace message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.DEBUG - 5, message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message.

        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self._log(logging.CRITICAL, message, **kwargs)

    def _log(self, level: int, message: str, **kwargs) -> None:
        """Log message with context.

        Args:
            level: Log level
            message: Message to log
            **kwargs: Additional context
        """
        if kwargs:
            # Add context to message
            context = json.dumps(kwargs)
            message = f"{message} | context={context}"

        self.logger.log(level, message)

    def flush(self) -> None:
        """Flush all handlers."""
        for handler in self.logger.handlers:
            handler.flush()
```

### 3. JSON Formatter for Structured Logging

```python
# omni_scripts/logging/formatters.py
"""Formatters for structured logging."""

import logging
import json
from datetime import datetime
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def __init__(self):
        """Initialize JSON formatter."""
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record

        Returns:
            JSON-formatted log message
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        return json.dumps(log_data)
```

### 4. Log Configuration

```python
# omni_scripts/logging/config.py
"""Log configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class LogConfig:
    """Log configuration."""

    # Log file path
    log_file: Optional[Path] = Path("logs/omnicpp.log")

    # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level: int = 20  # INFO

    # Maximum file size in bytes (default: 5 MB)
    max_file_size: int = 1024 * 1024 * 5

    # Maximum number of files to keep
    max_files: int = 3

    # Console output
    console_output: bool = True

    # JSON format for file output
    json_format: bool = True

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'LogConfig':
        """Create configuration from dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Log configuration
        """
        return cls(
            log_file=Path(config_dict.get('log_file', 'logs/omnicpp.log')),
            level=config_dict.get('level', 20),
            max_file_size=config_dict.get('max_file_size', 1024 * 1024 * 5),
            max_files=config_dict.get('max_files', 3),
            console_output=config_dict.get('console_output', True),
            json_format=config_dict.get('json_format', True),
        )

    @classmethod
    def from_file(cls, config_file: Path) -> 'LogConfig':
        """Create configuration from file.

        Args:
            config_file: Path to configuration file

        Returns:
            Log configuration
        """
        import json

        with open(config_file, 'r') as f:
            config_dict = json.load(f)

        return cls.from_dict(config_dict)
```

### 5. Usage Examples

```cpp
// C++ usage
#include "engine/logging/logger.hpp"

int main() {
    // Initialize logger
    auto& logger = engine::logging::Logger::getInstance();
    logger.initialize("logs/omnicpp.log", engine::logging::LogLevel::INFO);

    // Log messages
    logger.trace("This is a trace message");
    logger.debug("This is a debug message");
    logger.info("This is an info message");
    logger.warn("This is a warning message");
    logger.error("This is an error message");
    logger.critical("This is a critical message");

    // Flush logger
    logger.flush();

    return 0;
}
```

```python
# Python usage
from logging.logger import Logger
from logging.config import LogConfig

# Create logger
config = LogConfig(log_file=Path("logs/omnicpp.log"))
logger = Logger(config)

# Log messages
logger.trace("This is a trace message")
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Log with context
logger.info("User logged in", user_id=123, username="john_doe")

# Flush logger
logger.flush()
```

## Consequences

### Positive

1. **High Performance:** spdlog provides high-performance logging for C++
2. **Thread Safety:** Both logging systems are thread-safe
3. **Structured Logging:** JSON-based structured logging for analysis
4. **Log Rotation:** Automatic log rotation for both languages
5. **Consistent Format:** Unified log format across both languages
6. **Log Levels:** Consistent log levels across both languages
7. **Flexible Configuration:** Easy to configure logging behavior

### Negative

1. **Dependency:** Adds spdlog dependency for C++
2. **Complexity:** More complex than simple logging
3. **Learning Curve:** Developers need to understand logging system
4. **File Size:** JSON format increases log file size

### Neutral

1. **Documentation:** Requires documentation for logging system
2. **Testing:** Need to test logging in both languages

## Alternatives Considered

### Alternative 1: Single Logging Library

**Description:** Use single logging library for both languages

**Pros:**

- Consistent implementation
- Less complexity

**Cons:**

- No native C++ logging library
- Poor performance in C++
- Limited features

**Rejected:** Poor performance in C++

### Alternative 2: Standard Library Logging

**Description:** Use standard library logging for both languages

**Pros:**

- No additional dependencies
- Simple implementation

**Cons:**

- Poor performance in C++
- No structured logging
- No log rotation

**Rejected:** Poor performance and no structured logging

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

- [ADR-014: File rotation and log retention policy](ADR-014-file-rotation-retention.md)
- [ADR-015: Structured logging format](ADR-015-structured-logging-format.md)

## References

- [spdlog Documentation](https://github.com/gabime/spdlog)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Structured Logging](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html)

---

**Document Control**

| Version | Date       | Author           | Changes         |
| ------- | ---------- | ---------------- | --------------- |
| 1.0     | 2026-01-07 | System Architect | Initial version |
