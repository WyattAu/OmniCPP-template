# DES-035: Log Message Schema

## Overview

Defines the log message schema for both Python and C++ logging systems.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Log Message Schema",
  "description": "Schema for log messages in OmniCpp",
  "type": "object",
  "properties": {
    "level": {
      "type": "string",
      "enum": ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
      "description": "Log level"
    },
    "message": {
      "type": "string",
      "description": "Log message content"
    },
    "logger_name": {
      "type": "string",
      "description": "Name of the logger"
    },
    "timestamp": {
      "type": "number",
      "description": "Unix timestamp"
    },
    "file": {
      "type": "string",
      "description": "Source file name"
    },
    "line": {
      "type": "integer",
      "description": "Source line number"
    },
    "function": {
      "type": "string",
      "description": "Source function name"
    },
    "thread_id": {
      "type": "string",
      "description": "Thread identifier"
    },
    "process_id": {
      "type": "integer",
      "description": "Process identifier"
    },
    "extra": {
      "type": "object",
      "description": "Additional log data",
      "additionalProperties": {
        "type": "string"
      }
    }
  },
  "required": ["level", "message", "timestamp"],
  "additionalProperties": false
}
```

### Python Data Classes

```python
"""
Log Message Schema for OmniCpp

This module defines the log message schema for the logging system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
import time


class LogLevel(Enum):
    """Log levels"""
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogMessage:
    """Log message structure"""
    level: LogLevel
    message: str
    logger_name: str = "OmniCppLogger"
    timestamp: float = field(default_factory=time.time)
    file: str = ""
    line: int = 0
    function: str = ""
    thread_id: str = ""
    process_id: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert log message to dictionary"""
        return {
            "level": self.level.value,
            "message": self.message,
            "logger_name": self.logger_name,
            "timestamp": self.timestamp,
            "file": self.file,
            "line": self.line,
            "function": self.function,
            "thread_id": self.thread_id,
            "process_id": self.process_id,
            "extra": self.extra
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogMessage":
        """Create log message from dictionary"""
        return cls(
            level=LogLevel(data.get("level", "INFO")),
            message=data.get("message", ""),
            logger_name=data.get("logger_name", "OmniCppLogger"),
            timestamp=data.get("timestamp", time.time()),
            file=data.get("file", ""),
            line=data.get("line", 0),
            function=data.get("function", ""),
            thread_id=data.get("thread_id", ""),
            process_id=data.get("process_id", 0),
            extra=data.get("extra", {})
        )

    def to_json(self) -> str:
        """Convert log message to JSON string"""
        import json
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "LogMessage":
        """Create log message from JSON string"""
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self) -> str:
        """String representation of log message"""
        return f"[{self.level.value}] {self.message}"
```

### C++ Structs

```cpp
#ifndef OMNICPP_LOG_MESSAGE_SCHEMA_H
#define OMNICPP_LOG_MESSAGE_SCHEMA_H

#include <string>
#include <chrono>
#include <unordered_map>
#include <thread>

namespace omnicpp {
namespace logging {

// Log level enum
enum class LogLevel {
    TRACE,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    CRITICAL,
    OFF
};

// Log message structure
struct LogMessage {
    LogLevel level;
    std::string message;
    std::string logger_name;
    std::chrono::system_clock::time_point timestamp;
    std::string file;
    int line;
    std::string function;
    std::thread::id thread_id;
    std::unordered_map<std::string, std::string> extra;

    LogMessage()
        : level(LogLevel::INFO)
        , message("")
        , logger_name("OmniCppLogger")
        , timestamp(std::chrono::system_clock::now())
        , file("")
        , line(0)
        , function("")
        , thread_id(std::this_thread::get_id())
        , extra()
    {}

    // Convert to string
    std::string to_string() const {
        std::string level_str;
        switch (level) {
            case LogLevel::TRACE:
                level_str = "TRACE";
                break;
            case LogLevel::DEBUG:
                level_str = "DEBUG";
                break;
            case LogLevel::INFO:
                level_str = "INFO";
                break;
            case LogLevel::WARN:
                level_str = "WARN";
                break;
            case LogLevel::ERROR:
                level_str = "ERROR";
                break;
            case LogLevel::CRITICAL:
                level_str = "CRITICAL";
                break;
            case LogLevel::OFF:
                level_str = "OFF";
                break;
        }

        return "[" + level_str + "] " + message;
    }

    // Convert to JSON
    std::string to_json() const {
        std::string level_str;
        switch (level) {
            case LogLevel::TRACE:
                level_str = "TRACE";
                break;
            case LogLevel::DEBUG:
                level_str = "DEBUG";
                break;
            case LogLevel::INFO:
                level_str = "INFO";
                break;
            case LogLevel::WARN:
                level_str = "WARN";
                break;
            case LogLevel::ERROR:
                level_str = "ERROR";
                break;
            case LogLevel::CRITICAL:
                level_str = "CRITICAL";
                break;
            case LogLevel::OFF:
                level_str = "OFF";
                break;
        }

        std::string json = "{";
        json += "\"level\": \"" + level_str + "\",";
        json += "\"message\": \"" + message + "\",";
        json += "\"logger_name\": \"" + logger_name + "\",";
        json += "\"timestamp\": " + std::to_string(std::chrono::duration_cast<std::chrono::milliseconds>(
            timestamp.time_since_epoch()).count()) + ",";
        json += "\"file\": \"" + file + "\",";
        json += "\"line\": " + std::to_string(line) + ",";
        json += "\"function\": \"" + function + "\"";
        json += "}";

        return json;
    }

    // Get level as string
    static std::string level_to_string(LogLevel level) {
        switch (level) {
            case LogLevel::TRACE:
                return "TRACE";
            case LogLevel::DEBUG:
                return "DEBUG";
            case LogLevel::INFO:
                return "INFO";
            case LogLevel::WARN:
                return "WARN";
            case LogLevel::ERROR:
                return "ERROR";
            case LogLevel::CRITICAL:
                return "CRITICAL";
            case LogLevel::OFF:
                return "OFF";
            default:
                return "UNKNOWN";
        }
    }

    // Parse level from string
    static LogLevel string_to_level(const std::string& level_str) {
        if (level_str == "TRACE") return LogLevel::TRACE;
        if (level_str == "DEBUG") return LogLevel::DEBUG;
        if (level_str == "INFO") return LogLevel::INFO;
        if (level_str == "WARN") return LogLevel::WARN;
        if (level_str == "ERROR") return LogLevel::ERROR;
        if (level_str == "CRITICAL") return LogLevel::CRITICAL;
        if (level_str == "OFF") return LogLevel::OFF;
        return LogLevel::INFO;
    }
};

} // namespace logging
} // namespace omnicpp

#endif // OMNICPP_LOG_MESSAGE_SCHEMA_H
```

## Dependencies

### Internal Dependencies

- `DES-033` - C++ Logging Interface
- `DES-034` - Python Logging Interface

### External Dependencies

- `dataclasses` - Data structures (Python)
- `typing` - Type hints (Python)
- `enum` - Enumerations (Python)
- `time` - Time handling (Python)
- `json` - JSON parsing (Python)
- `string` - String handling (C++)
- `chrono` - Time handling (C++)
- `unordered_map` - Hash map (C++)
- `thread` - Thread handling (C++)

## Related Requirements

- REQ-053: Log Message Format
- REQ-054: Log Serialization

## Related ADRs

- ADR-003: Logging Architecture

## Implementation Notes

### Log Message Structure

1. Level - Log severity level
2. Message - Log message content
3. Logger Name - Name of the logger
4. Timestamp - Unix timestamp
5. File - Source file name
6. Line - Source line number
7. Function - Source function name
8. Thread ID - Thread identifier
9. Process ID - Process identifier
10. Extra - Additional log data

### Log Levels

1. TRACE - Most verbose
2. DEBUG - Debug information
3. INFO - General information
4. WARN - Warning messages
5. ERROR - Error messages
6. CRITICAL - Critical errors
7. OFF - Logging disabled

### Serialization

1. JSON serialization
2. Dictionary conversion
3. String representation
4. Parse from JSON

## Usage Example

### Python Example

```python
from omni_scripts.logging import LogMessage, LogLevel

# Create log message
message = LogMessage(
    level=LogLevel.INFO,
    message="User logged in successfully",
    logger_name="AuthLogger",
    file="auth.py",
    line=42,
    function="login",
    thread_id="MainThread",
    process_id=12345,
    extra={
        "user_id": "john",
        "ip_address": "192.168.1.1"
    }
)

# Convert to dictionary
data = message.to_dict()
print(data)

# Convert to JSON
json_str = message.to_json()
print(json_str)

# String representation
print(message)

# Parse from JSON
parsed_message = LogMessage.from_json(json_str)
print(parsed_message)
```

### C++ Example

```cpp
#include "log_message_schema.hpp"

using namespace omnicpp::logging;

int main() {
    // Create log message
    LogMessage message;
    message.level = LogLevel::INFO;
    message.message = "User logged in successfully";
    message.logger_name = "AuthLogger";
    message.file = "auth.cpp";
    message.line = 42;
    message.function = "login";
    message.thread_id = std::this_thread::get_id();
    message.extra["user_id"] = "john";
    message.extra["ip_address"] = "192.168.1.1";

    // Convert to string
    std::string str = message.to_string();
    std::cout << str << std::endl;

    // Convert to JSON
    std::string json = message.to_json();
    std::cout << json << std::endl;

    // Get level as string
    std::string level_str = LogMessage::level_to_string(LogLevel::INFO);
    std::cout << level_str << std::endl;

    // Parse level from string
    LogLevel level = LogMessage::string_to_level("INFO");

    return 0;
}
```
