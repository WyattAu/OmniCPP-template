# DES-004: Logging Configuration Schema

## Overview
Defines the logging configuration schema for both Python and C++ components, including log levels, formatters, handlers, and rotation policies.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Logging Configuration",
  "description": "Logging configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "version": {
      "type": "integer",
      "default": 1,
      "description": "Configuration version"
    },
    "disable_existing_loggers": {
      "type": "boolean",
      "default": false,
      "description": "Disable existing loggers"
    },
    "formatters": {
      "type": "object",
      "description": "Log formatters",
      "properties": {
        "standard": {
          "type": "object",
          "description": "Standard formatter",
          "properties": {
            "format": {
              "type": "string",
              "default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
              "description": "Log message format"
            },
            "datefmt": {
              "type": "string",
              "default": "%Y-%m-%d %H:%M:%S",
              "description": "Date format"
            },
            "class": {
              "type": "string",
              "default": "logging.Formatter",
              "description": "Formatter class"
            }
          }
        },
        "detailed": {
          "type": "object",
          "description": "Detailed formatter",
          "properties": {
            "format": {
              "type": "string",
              "default": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
              "description": "Detailed log message format"
            },
            "datefmt": {
              "type": "string",
              "default": "%Y-%m-%d %H:%M:%S",
              "description": "Date format"
            },
            "class": {
              "type": "string",
              "default": "logging.Formatter",
              "description": "Formatter class"
            }
          }
        },
        "json": {
          "type": "object",
          "description": "JSON formatter",
          "properties": {
            "format": {
              "type": "string",
              "default": "json",
              "description": "JSON format indicator"
            },
            "class": {
              "type": "string",
              "default": "pythonjsonlogger.jsonlogger.JsonFormatter",
              "description": "JSON formatter class"
            }
          }
        }
      }
    },
    "filters": {
      "type": "object",
      "description": "Log filters",
      "properties": {
        "level_filter": {
          "type": "object",
          "description": "Level filter",
          "properties": {
            "class": {
              "type": "string",
              "default": "logging.Filter",
              "description": "Filter class"
            },
            "name": {
              "type": "string",
              "default": "level_filter",
              "description": "Filter name"
            }
          }
        }
      }
    },
    "handlers": {
      "type": "object",
      "description": "Log handlers",
      "properties": {
        "console": {
          "type": "object",
          "description": "Console handler",
          "properties": {
            "class": {
              "type": "string",
              "default": "logging.StreamHandler",
              "description": "Handler class"
            },
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "INFO",
              "description": "Log level"
            },
            "formatter": {
              "type": "string",
              "default": "standard",
              "description": "Formatter name"
            },
            "stream": {
              "type": "string",
              "default": "ext://sys.stdout",
              "description": "Output stream"
            },
            "color": {
              "type": "boolean",
              "default": true,
              "description": "Enable colored output"
            }
          }
        },
        "file": {
          "type": "object",
          "description": "File handler",
          "properties": {
            "class": {
              "type": "string",
              "default": "logging.handlers.RotatingFileHandler",
              "description": "Handler class"
            },
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "formatter": {
              "type": "string",
              "default": "detailed",
              "description": "Formatter name"
            },
            "filename": {
              "type": "string",
              "default": "logs/omnicpp.log",
              "description": "Log file path"
            },
            "maxBytes": {
              "type": "integer",
              "default": 10485760,
              "description": "Maximum file size in bytes"
            },
            "backupCount": {
              "type": "integer",
              "default": 5,
              "description": "Number of backup files"
            },
            "encoding": {
              "type": "string",
              "default": "utf-8",
              "description": "File encoding"
            }
          }
        },
        "error_file": {
          "type": "object",
          "description": "Error file handler",
          "properties": {
            "class": {
              "type": "string",
              "default": "logging.handlers.RotatingFileHandler",
              "description": "Handler class"
            },
            "level": {
              "type": "string",
              "enum": ["ERROR", "CRITICAL"],
              "default": "ERROR",
              "description": "Log level"
            },
            "formatter": {
              "type": "string",
              "default": "detailed",
              "description": "Formatter name"
            },
            "filename": {
              "type": "string",
              "default": "logs/omnicpp_error.log",
              "description": "Error log file path"
            },
            "maxBytes": {
              "type": "integer",
              "default": 10485760,
              "description": "Maximum file size in bytes"
            },
            "backupCount": {
              "type": "integer",
              "default": 5,
              "description": "Number of backup files"
            },
            "encoding": {
              "type": "string",
              "default": "utf-8",
              "description": "File encoding"
            }
          }
        },
        "timed_file": {
          "type": "object",
          "description": "Timed rotating file handler",
          "properties": {
            "class": {
              "type": "string",
              "default": "logging.handlers.TimedRotatingFileHandler",
              "description": "Handler class"
            },
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "formatter": {
              "type": "string",
              "default": "detailed",
              "description": "Formatter name"
            },
            "filename": {
              "type": "string",
              "default": "logs/omnicpp_timed.log",
              "description": "Log file path"
            },
            "when": {
              "type": "string",
              "enum": ["S", "M", "H", "D", "midnight", "W0", "W1", "W2", "W3", "W4", "W5", "W6"],
              "default": "D",
              "description": "Rotation interval type"
            },
            "interval": {
              "type": "integer",
              "default": 1,
              "description": "Rotation interval"
            },
            "backupCount": {
              "type": "integer",
              "default": 30,
              "description": "Number of backup files"
            },
            "encoding": {
              "type": "string",
              "default": "utf-8",
              "description": "File encoding"
            }
          }
        }
      }
    },
    "loggers": {
      "type": "object",
      "description": "Loggers",
      "properties": {
        "": {
          "type": "object",
          "description": "Root logger",
          "properties": {
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "INFO",
              "description": "Log level"
            },
            "handlers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["console", "file"],
              "description": "Handler names"
            },
            "propagate": {
              "type": "boolean",
              "default": false,
              "description": "Propagate to parent logger"
            }
          }
        },
        "omni_scripts": {
          "type": "object",
          "description": "OmniScripts logger",
          "properties": {
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "handlers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["console", "file"],
              "description": "Handler names"
            },
            "propagate": {
              "type": "boolean",
              "default": false,
              "description": "Propagate to parent logger"
            }
          }
        },
        "omni_scripts.build_system": {
          "type": "object",
          "description": "Build system logger",
          "properties": {
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "handlers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["console", "file"],
              "description": "Handler names"
            },
            "propagate": {
              "type": "boolean",
              "default": false,
              "description": "Propagate to parent logger"
            }
          }
        },
        "omni_scripts.compilers": {
          "type": "object",
          "description": "Compilers logger",
          "properties": {
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "handlers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["console", "file"],
              "description": "Handler names"
            },
            "propagate": {
              "type": "boolean",
              "default": false,
              "description": "Propagate to parent logger"
            }
          }
        },
        "omni_scripts.platform": {
          "type": "object",
          "description": "Platform logger",
          "properties": {
            "level": {
              "type": "string",
              "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
              "default": "DEBUG",
              "description": "Log level"
            },
            "handlers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["console", "file"],
              "description": "Handler names"
            },
            "propagate": {
              "type": "boolean",
              "default": false,
              "description": "Propagate to parent logger"
            }
          }
        }
      }
    },
    "cpp_logging": {
      "type": "object",
      "description": "C++ logging configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable C++ logging"
        },
        "level": {
          "type": "string",
          "enum": ["trace", "debug", "info", "warn", "err", "critical", "off"],
          "default": "info",
          "description": "C++ log level"
        },
        "pattern": {
          "type": "string",
          "default": "[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] [%s:%#] %v",
          "description": "Log pattern format"
        },
        "file": {
          "type": "object",
          "description": "C++ file logging",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable file logging"
            },
            "path": {
              "type": "string",
              "default": "logs/omnicpp_cpp.log",
              "description": "Log file path"
            },
            "max_size": {
              "type": "integer",
              "default": 10485760,
              "description": "Maximum file size in bytes"
            },
            "max_files": {
              "type": "integer",
              "default": 5,
              "description": "Maximum number of files"
            }
          }
        },
        "console": {
          "type": "object",
          "description": "C++ console logging",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable console logging"
            },
            "color": {
              "type": "boolean",
              "default": true,
              "description": "Enable colored output"
            }
          }
        },
        "async": {
          "type": "object",
          "description": "Async logging configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable async logging"
            },
            "queue_size": {
              "type": "integer",
              "default": 8192,
              "description": "Async queue size"
            },
            "thread_count": {
              "type": "integer",
              "default": 1,
              "description": "Number of worker threads"
            }
          }
        }
      }
    }
  }
}
```

### Python Data Classes

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class CppLogLevel(Enum):
    """C++ logging levels"""
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERR = "err"
    CRITICAL = "critical"
    OFF = "off"

class RotationType(Enum):
    """Log rotation types"""
    SIZE = "size"
    TIME = "time"

class RotationInterval(Enum):
    """Time-based rotation intervals"""
    SECOND = "S"
    MINUTE = "M"
    HOUR = "H"
    DAY = "D"
    MIDNIGHT = "midnight"
    MONDAY = "W0"
    TUESDAY = "W1"
    WEDNESDAY = "W2"
    THURSDAY = "W3"
    FRIDAY = "W4"
    SATURDAY = "W5"
    SUNDAY = "W6"

@dataclass
class FormatterConfig:
    """Formatter configuration"""
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    class_name: str = "logging.Formatter"

@dataclass
class ConsoleHandlerConfig:
    """Console handler configuration"""
    class_name: str = "logging.StreamHandler"
    level: LogLevel = LogLevel.INFO
    formatter: str = "standard"
    stream: str = "ext://sys.stdout"
    color: bool = True

@dataclass
class FileHandlerConfig:
    """File handler configuration"""
    class_name: str = "logging.handlers.RotatingFileHandler"
    level: LogLevel = LogLevel.DEBUG
    formatter: str = "detailed"
    filename: str = "logs/omnicpp.log"
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5
    encoding: str = "utf-8"

@dataclass
class TimedFileHandlerConfig:
    """Timed rotating file handler configuration"""
    class_name: str = "logging.handlers.TimedRotatingFileHandler"
    level: LogLevel = LogLevel.DEBUG
    formatter: str = "detailed"
    filename: str = "logs/omnicpp_timed.log"
    when: RotationInterval = RotationInterval.DAY
    interval: int = 1
    backup_count: int = 30
    encoding: str = "utf-8"

@dataclass
class HandlersConfig:
    """Handlers configuration"""
    console: ConsoleHandlerConfig = field(default_factory=ConsoleHandlerConfig)
    file: FileHandlerConfig = field(default_factory=FileHandlerConfig)
    error_file: FileHandlerConfig = field(default_factory=lambda: FileHandlerConfig(
        filename="logs/omnicpp_error.log",
        level=LogLevel.ERROR
    ))
    timed_file: TimedFileHandlerConfig = field(default_factory=TimedFileHandlerConfig)

@dataclass
class LoggerConfig:
    """Logger configuration"""
    level: LogLevel = LogLevel.INFO
    handlers: List[str] = field(default_factory=lambda: ["console", "file"])
    propagate: bool = False

@dataclass
class LoggersConfig:
    """Loggers configuration"""
    root: LoggerConfig = field(default_factory=LoggerConfig)
    omni_scripts: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        level=LogLevel.DEBUG
    ))
    build_system: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        level=LogLevel.DEBUG
    ))
    compilers: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        level=LogLevel.DEBUG
    ))
    platform: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        level=LogLevel.DEBUG
    ))

@dataclass
class CppFileLoggingConfig:
    """C++ file logging configuration"""
    enabled: bool = True
    path: str = "logs/omnicpp_cpp.log"
    max_size: int = 10485760  # 10MB
    max_files: int = 5

@dataclass
class CppConsoleLoggingConfig:
    """C++ console logging configuration"""
    enabled: bool = True
    color: bool = True

@dataclass
class CppAsyncLoggingConfig:
    """C++ async logging configuration"""
    enabled: bool = True
    queue_size: int = 8192
    thread_count: int = 1

@dataclass
class CppLoggingConfig:
    """C++ logging configuration"""
    enabled: bool = True
    level: CppLogLevel = CppLogLevel.INFO
    pattern: str = "[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] [%s:%#] %v"
    file: CppFileLoggingConfig = field(default_factory=CppFileLoggingConfig)
    console: CppConsoleLoggingConfig = field(default_factory=CppConsoleLoggingConfig)
    async_config: CppAsyncLoggingConfig = field(default_factory=CppAsyncLoggingConfig)

@dataclass
class LoggingConfig:
    """Main logging configuration"""
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict[str, FormatterConfig] = field(default_factory=lambda: {
        "standard": FormatterConfig(),
        "detailed": FormatterConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        ),
        "json": FormatterConfig(
            format="json",
            class_name="pythonjsonlogger.jsonlogger.JsonFormatter"
        )
    })
    handlers: HandlersConfig = field(default_factory=HandlersConfig)
    loggers: LoggersConfig = field(default_factory=LoggersConfig)
    cpp_logging: CppLoggingConfig = field(default_factory=CppLoggingConfig)
```

### C++ Struct Definitions

```cpp
#include <string>
#include <cstdint>
#include <vector>
#include <memory>

namespace omnicpp {
namespace logging {

// Log level enumeration
enum class LogLevel : uint8_t {
    Trace = 0,
    Debug = 1,
    Info = 2,
    Warning = 3,
    Error = 4,
    Critical = 5,
    Off = 6
};

// Log message structure
struct LogMessage {
    LogLevel level;
    std::string message;
    std::string logger_name;
    std::string file;
    uint32_t line;
    std::string function;
    uint64_t timestamp;

    LogMessage() = default;
    LogMessage(LogLevel lvl, const std::string& msg, const std::string& logger,
               const std::string& f, uint32_t l, const std::string& func)
        : level(lvl), message(msg), logger_name(logger), file(f), line(l),
          function(func), timestamp(0) {}
};

// File logging configuration
struct FileLoggingConfig {
    bool enabled = true;
    std::string path = "logs/omnicpp_cpp.log";
    uint64_t max_size = 10485760;  // 10MB
    uint32_t max_files = 5;
    bool truncate = false;
};

// Console logging configuration
struct ConsoleLoggingConfig {
    bool enabled = true;
    bool color = true;
    bool force_ansi = false;
};

// Async logging configuration
struct AsyncLoggingConfig {
    bool enabled = true;
    uint32_t queue_size = 8192;
    uint32_t thread_count = 1;
    bool overflow_policy = "block";  // "block" or "discard"
};

// C++ logging configuration
struct LoggingConfig {
    bool enabled = true;
    LogLevel level = LogLevel::Info;
    std::string pattern = "[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] [%s:%#] %v";
    FileLoggingConfig file;
    ConsoleLoggingConfig console;
    AsyncLoggingConfig async_config;

    // Validate configuration
    bool validate() const {
        if (enabled && !file.enabled && !console.enabled) {
            return false;
        }
        if (async_config.enabled && async_config.thread_count == 0) {
            return false;
        }
        return true;
    }
};

// Logger interface
class ILogger {
public:
    virtual ~ILogger() = default;

    virtual void log(LogLevel level, const std::string& message) = 0;
    virtual void log(const LogMessage& message) = 0;

    virtual void trace(const std::string& message) = 0;
    virtual void debug(const std::string& message) = 0;
    virtual void info(const std::string& message) = 0;
    virtual void warning(const std::string& message) = 0;
    virtual void error(const std::string& message) = 0;
    virtual void critical(const std::string& message) = 0;

    virtual void set_level(LogLevel level) = 0;
    virtual LogLevel get_level() const = 0;

    virtual void flush() = 0;
};

// Logger factory
class LoggerFactory {
public:
    static std::shared_ptr<ILogger> create(const std::string& name,
                                          const LoggingConfig& config);
    static std::shared_ptr<ILogger> get(const std::string& name);
    static void shutdown();
};

} // namespace logging
} // namespace omnicpp
```

## Dependencies

### Internal Dependencies
- `DES-003` - Configuration schema

### External Dependencies
- `logging` - Python logging module
- `logging.handlers` - Python logging handlers
- `dataclasses` - Data structures
- `typing` - Type hints
- `enum` - Enumerations
- `spdlog` - C++ logging library

## Related Requirements
- REQ-005: Logging Configuration
- REQ-033: Structured Logging Format
- REQ-032: File Rotation & Log Retention
- REQ-045: Secure Logging

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Python Logging Setup
1. Load configuration from JSON file
2. Create formatters
3. Create handlers
4. Configure loggers
5. Apply to logging dictConfig

### C++ Logging Setup
1. Load configuration from JSON file
2. Create spdlog logger
3. Configure sinks (file, console)
4. Set log level
5. Configure async logging if enabled

### Log Rotation
- Python: Use RotatingFileHandler or TimedRotatingFileHandler
- C++: Use spdlog's rotating file sink

### Performance Considerations
- Use async logging for high-throughput scenarios
- Configure appropriate queue sizes
- Consider log level filtering at compile time for C++

### Security Considerations
- Sanitize log messages to prevent log injection
- Avoid logging sensitive information
- Use secure file permissions for log files

## Usage Example

### Python

```python
from omni_scripts.logging import LoggingConfig, setup_logging
import logging

# Load configuration
config = LoggingConfig.from_file("config/logging.json")

# Setup logging
setup_logging(config)

# Get logger
logger = logging.getLogger("omni_scripts.build_system")

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### C++

```cpp
#include "engine/logging/logger.hpp"

using namespace omnicpp::logging;

// Get logger
auto logger = LoggerFactory::get("omnicpp.engine");

// Log messages
logger->trace("Trace message");
logger->debug("Debug message");
logger->info("Info message");
logger->warning("Warning message");
logger->error("Error message");
logger->critical("Critical message");

// Flush logs
logger->flush();
```
