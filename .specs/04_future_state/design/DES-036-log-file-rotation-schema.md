# DES-036: Log File Rotation Schema

## Overview
Defines the log file rotation schema for both Python and C++ logging systems.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Log File Rotation Schema",
  "description": "Schema for log file rotation in OmniCpp",
  "type": "object",
  "properties": {
    "enabled": {
      "type": "boolean",
      "description": "Enable log file rotation",
      "default": true
    },
    "type": {
      "type": "string",
      "enum": ["size", "time", "both"],
      "description": "Rotation type",
      "default": "size"
    },
    "max_size": {
      "type": "integer",
      "description": "Maximum file size in bytes",
      "default": 10485760
    },
    "max_count": {
      "type": "integer",
      "description": "Maximum number of backup files",
      "default": 5
    },
    "when": {
      "type": "string",
      "enum": ["midnight", "H", "M", "S", "W", "D"],
      "description": "When to rotate (time-based)",
      "default": "midnight"
    },
    "interval": {
      "type": "integer",
      "description": "Rotation interval in hours",
      "default": 24
    },
    "backup_count": {
      "type": "integer",
      "description": "Number of backup files to keep",
      "default": 5
    },
    "compression": {
      "type": "boolean",
      "description": "Compress rotated files",
      "default": false
    },
    "compression_level": {
      "type": "integer",
      "description": "Compression level (0-9)",
      "default": 6
    },
    "naming": {
      "type": "string",
      "description": "File naming pattern",
      "default": "{name}.{timestamp}.{ext}"
    },
    "extension": {
      "type": "string",
      "description": "File extension",
      "default": "log"
    },
    "directory": {
      "type": "string",
      "description": "Log directory",
      "default": "logs"
    },
    "delay": {
      "type": "boolean",
      "description": "Delay rotation until first write",
      "default": false
    },
    "utc": {
      "type": "boolean",
      "description": "Use UTC time for rotation",
      "default": false
    }
  },
  "required": ["enabled", "type"],
  "additionalProperties": false
}
```

### Python Data Classes

```python
"""
Log File Rotation Schema for OmniCpp

This module defines the log file rotation schema for the logging system.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from pathlib import Path


class RotationType(Enum):
    """Rotation types"""
    SIZE = "size"
    TIME = "time"
    BOTH = "both"


class RotationWhen(Enum):
    """When to rotate (time-based)"""
    MIDNIGHT = "midnight"
    H = "H"
    M = "M"
    S = "S"
    D = "D"
    W = "W"


class CompressionLevel(Enum):
    """Compression levels"""
    NONE = 0
    FASTEST = 1
    FAST = 3
    NORMAL = 6
    MAXIMUM = 9


@dataclass
class LogRotationConfig:
    """Log rotation configuration"""
    enabled: bool = True
    type: RotationType = RotationType.SIZE
    max_size: int = 10 * 1024 * 1024  # 10MB
    max_count: int = 5
    when: RotationWhen = RotationWhen.MIDNIGHT
    interval: int = 24  # hours
    backup_count: int = 5
    compression: bool = False
    compression_level: CompressionLevel = CompressionLevel.NORMAL
    naming: str = "{name}.{timestamp}.{ext}"
    extension: str = "log"
    directory: str = "logs"
    delay: bool = False
    utc: bool = False

    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            "enabled": self.enabled,
            "type": self.type.value,
            "max_size": self.max_size,
            "max_count": self.max_count,
            "when": self.when.value,
            "interval": self.interval,
            "backup_count": self.backup_count,
            "compression": self.compression,
            "compression_level": self.compression_level.value,
            "naming": self.naming,
            "extension": self.extension,
            "directory": self.directory,
            "delay": self.delay,
            "utc": self.utc
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LogRotationConfig":
        """Create configuration from dictionary"""
        return cls(
            enabled=data.get("enabled", True),
            type=RotationType(data.get("type", "size")),
            max_size=data.get("max_size", 10 * 1024 * 1024),
            max_count=data.get("max_count", 5),
            when=RotationWhen(data.get("when", "midnight")),
            interval=data.get("interval", 24),
            backup_count=data.get("backup_count", 5),
            compression=data.get("compression", False),
            compression_level=CompressionLevel(data.get("compression_level", 6)),
            naming=data.get("naming", "{name}.{timestamp}.{ext}"),
            extension=data.get("extension", "log"),
            directory=data.get("directory", "logs"),
            delay=data.get("delay", False),
            utc=data.get("utc", False)
        )

    def get_log_path(self, name: str) -> Path:
        """Get the log file path"""
        return Path(self.directory) / f"{name}.{self.extension}"

    def get_backup_path(self, name: str, timestamp: float) -> Path:
        """Get the backup log file path"""
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        timestamp_str = dt.strftime("%Y%m%d_%H%M%S")
        return Path(self.directory) / f"{name}.{timestamp_str}.{self.extension}"

    def should_rotate_by_size(self, current_size: int) -> bool:
        """Check if rotation is needed by size"""
        return self.enabled and self.type in [RotationType.SIZE, RotationType.BOTH] and current_size >= self.max_size

    def should_rotate_by_time(self, current_time: float) -> bool:
        """Check if rotation is needed by time"""
        if not self.enabled or self.type not in [RotationType.TIME, RotationType.BOTH]:
            return False

        from datetime import datetime
        dt = datetime.fromtimestamp(current_time)

        if self.when == RotationWhen.MIDNIGHT:
            return dt.hour == 0 and dt.minute == 0 and dt.second == 0
        elif self.when == RotationWhen.H:
            return dt.minute == 0 and dt.second == 0
        elif self.when == RotationWhen.M:
            return dt.second == 0
        elif self.when == RotationWhen.S:
            return dt.weekday() == 6  # Sunday
        elif self.when == RotationWhen.D:
            return dt.day == 1  # First day of month

        return False

    def should_rotate(self, current_size: int, current_time: float) -> bool:
        """Check if rotation is needed"""
        return self.should_rotate_by_size(current_size) or self.should_rotate_by_time(current_time)


class LogRotationHandler:
    """Log rotation handler"""

    def __init__(self, config: LogRotationConfig):
        self._config = config
        self._current_size = 0
        self._current_time = 0.0
        self._backup_files = []

    def write(self, data: str, name: str) -> None:
        """Write data to log file"""
        import os
        import time

        log_path = self._config.get_log_path(name)

        # Check if rotation is needed
        if self._config.should_rotate(self._current_size, self._current_time):
            self._rotate(name)

        # Write data
        with open(log_path, 'a') as f:
            f.write(data)

        # Update size and time
        self._current_size += len(data.encode('utf-8'))
        self._current_time = time.time()

    def _rotate(self, name: str) -> None:
        """Rotate log file"""
        import shutil
        import time

        log_path = self._config.get_log_path(name)

        # Create backup
        backup_path = self._config.get_backup_path(name, time.time())
        shutil.move(str(log_path), str(backup_path))
        self._backup_files.append(backup_path)

        # Compress if enabled
        if self._config.compression:
            self._compress(backup_path)

        # Clean up old backups
        self._cleanup_backups(name)

        # Reset size
        self._current_size = 0

    def _compress(self, path: Path) -> None:
        """Compress log file"""
        import gzip

        compressed_path = path.with_suffix('.gz')
        with open(path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb', compresslevel=self._config.compression_level.value) as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove original file
        path.unlink()

    def _cleanup_backups(self, name: str) -> None:
        """Clean up old backup files"""
        import os

        # Get all backup files for this log
        backup_files = []
        for file in Path(self._config.directory).glob(f"{name}.*.{self._config.extension}*"):
            if file.is_file() and file.name != f"{name}.{self._config.extension}":
                backup_files.append(file)

        # Sort by modification time (newest first)
        backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        # Keep only the specified number of backups
        if len(backup_files) > self._config.backup_count:
            for file in backup_files[self._config.backup_count:]:
                file.unlink()

    def get_backup_files(self, name: str) -> list:
        """Get all backup files for a log"""
        import os

        backup_files = []
        for file in Path(self._config.directory).glob(f"{name}.*.{self._config.extension}*"):
            if file.is_file() and file.name != f"{name}.{self._config.extension}":
                backup_files.append(file)

        return backup_files

    def cleanup_all(self, name: str) -> None:
        """Clean up all log files"""
        import shutil

        log_path = self._config.get_log_path(name)
        backup_files = self.get_backup_files(name)

        # Remove all files
        if log_path.exists():
            log_path.unlink()

        for file in backup_files:
            file.unlink()
```

### C++ Structs

```cpp
#ifndef OMNICPP_LOG_FILE_ROTATION_SCHEMA_H
#define OMNICPP_LOG_FILE_ROTATION_SCHEMA_H

#include <string>
#include <vector>
#include <chrono>
#include <filesystem>

namespace omnicpp {
namespace logging {

// Rotation type
enum class RotationType {
    SIZE,
    TIME,
    BOTH
};

// Rotation when (time-based)
enum class RotationWhen {
    MIDNIGHT,
    H,
    M,
    S,
    D,
    W
};

// Compression level
enum class CompressionLevel {
    NONE = 0,
    FASTEST = 1,
    FAST = 3,
    NORMAL = 6,
    MAXIMUM = 9
};

// Log rotation configuration
struct LogRotationConfig {
    bool enabled;
    RotationType type;
    size_t max_size;
    int max_count;
    RotationWhen when;
    int interval;
    int backup_count;
    bool compression;
    CompressionLevel compression_level;
    std::string naming;
    std::string extension;
    std::string directory;
    bool delay;
    bool utc;

    LogRotationConfig()
        : enabled(true)
        , type(RotationType::SIZE)
        , max_size(10 * 1024 * 1024) // 10MB
        , max_count(5)
        , when(RotationWhen::MIDNIGHT)
        , interval(24)
        , backup_count(5)
        , compression(false)
        , compression_level(CompressionLevel::NORMAL)
        , naming("{name}.{timestamp}.{ext}")
        , extension("log")
        , directory("logs")
        , delay(false)
        , utc(false)
    {}

    // Get log file path
    std::filesystem::path get_log_path(const std::string& name) const {
        return std::filesystem::path(directory) / (name + "." + extension);
    }

    // Get backup file path
    std::filesystem::path get_backup_path(const std::string& name, std::chrono::system_clock::time_point timestamp) const {
        auto time_t = std::chrono::system_clock::to_time_t(timestamp);
        std::tm tm = *std::localtime(&time_t);
        char buffer[32];
        std::strftime(buffer, sizeof(buffer), "%Y%m%d_%H%M%S", &tm);
        return std::filesystem::path(directory) / (name + "." + std::string(buffer) + "." + extension);
    }

    // Check if rotation is needed by size
    bool should_rotate_by_size(size_t current_size) const {
        return enabled && (type == RotationType::SIZE || type == RotationType::BOTH) && current_size >= max_size;
    }

    // Check if rotation is needed by time
    bool should_rotate_by_time(std::chrono::system_clock::time_point current_time) const {
        if (!enabled || (type != RotationType::TIME && type != RotationType::BOTH)) {
            return false;
        }

        auto time_t = std::chrono::system_clock::to_time_t(current_time);
        std::tm tm = utc ? *std::gmtime(&time_t) : *std::localtime(&time_t);

        switch (when) {
            case RotationWhen::MIDNIGHT:
                return tm.tm_hour == 0 && tm.tm_min == 0 && tm.tm_sec == 0;
            case RotationWhen::H:
                return tm.tm_min == 0 && tm.tm_sec == 0;
            case RotationWhen::M:
                return tm.tm_sec == 0;
            case RotationWhen::S:
                return tm.tm_wday == 0; // Sunday
            case RotationWhen::D:
                return tm.tm_mday == 1; // First day of month
            case RotationWhen::W:
                return tm.tm_wday == 1; // Monday
            default:
                return false;
        }
    }

    // Check if rotation is needed
    bool should_rotate(size_t current_size, std::chrono::system_clock::time_point current_time) const {
        return should_rotate_by_size(current_size) || should_rotate_by_time(current_time);
    }
};

// Log rotation handler
class LogRotationHandler {
private:
    LogRotationConfig m_config;
    size_t m_current_size;
    std::chrono::system_clock::time_point m_current_time;
    std::vector<std::filesystem::path> m_backup_files;

public:
    LogRotationHandler(const LogRotationConfig& config)
        : m_config(config)
        , m_current_size(0)
        , m_current_time(std::chrono::system_clock::now())
        , m_backup_files()
    {}

    // Write data to log file
    void write(const std::string& data, const std::string& name) {
        std::filesystem::path log_path = m_config.get_log_path(name);

        // Check if rotation is needed
        if (m_config.should_rotate(m_current_size, m_current_time)) {
            rotate(name);
        }

        // Write data
        std::ofstream file(log_path, std::ios::app);
        file << data;
        file.close();

        // Update size and time
        m_current_size += data.size();
        m_current_time = std::chrono::system_clock::now();
    }

    // Rotate log file
    void rotate(const std::string& name) {
        std::filesystem::path log_path = m_config.get_log_path(name);
        std::filesystem::path backup_path = m_config.get_backup_path(name, m_current_time);

        // Create backup
        std::filesystem::rename(log_path, backup_path);
        m_backup_files.push_back(backup_path);

        // Compress if enabled
        if (m_config.compression) {
            compress(backup_path);
        }

        // Clean up old backups
        cleanup_backups(name);

        // Reset size
        m_current_size = 0;
    }

    // Compress log file
    void compress(const std::filesystem::path& path) {
        std::filesystem::path compressed_path = path;
        compressed_path += ".gz";

        // Use gzip compression
        // Implementation would use zlib or similar library
        // This is a placeholder for the actual implementation
    }

    // Clean up old backups
    void cleanup_backups(const std::string& name) {
        std::vector<std::filesystem::path> backup_files;

        // Get all backup files for this log
        for (const auto& entry : std::filesystem::directory_iterator(m_config.directory)) {
            std::string filename = entry.path().filename().string();
            if (entry.is_regular_file() &&
                filename.find(name) == 0 &&
                filename != (name + "." + m_config.extension)) {
                backup_files.push_back(entry.path());
            }
        }

        // Sort by modification time (newest first)
        std::sort(backup_files.begin(), backup_files.end(),
            [](const std::filesystem::path& a, const std::filesystem::path& b) {
                return std::filesystem::last_write_time(a) > std::filesystem::last_write_time(b);
            });

        // Keep only the specified number of backups
        if (backup_files.size() > static_cast<size_t>(m_config.backup_count)) {
            for (size_t i = m_config.backup_count; i < backup_files.size(); ++i) {
                std::filesystem::remove(backup_files[i]);
            }
        }
    }

    // Get all backup files
    std::vector<std::filesystem::path> get_backup_files(const std::string& name) const {
        std::vector<std::filesystem::path> backup_files;

        for (const auto& entry : std::filesystem::directory_iterator(m_config.directory)) {
            std::string filename = entry.path().filename().string();
            if (entry.is_regular_file() &&
                filename.find(name) == 0 &&
                filename != (name + "." + m_config.extension)) {
                backup_files.push_back(entry.path());
            }
        }

        return backup_files;
    }

    // Clean up all log files
    void cleanup_all(const std::string& name) {
        std::filesystem::path log_path = m_config.get_log_path(name);
        std::vector<std::filesystem::path> backup_files = get_backup_files(name);

        // Remove all files
        if (std::filesystem::exists(log_path)) {
            std::filesystem::remove(log_path);
        }

        for (const auto& file : backup_files) {
            std::filesystem::remove(file);
        }
    }
};

} // namespace logging
} // namespace omnicpp

#endif // OMNICPP_LOG_FILE_ROTATION_SCHEMA_H
```

## Dependencies

### Internal Dependencies
- `DES-033` - C++ Logging Interface
- `DES-034` - Python Logging Interface

### External Dependencies
- `dataclasses` - Data structures (Python)
- `typing` - Type hints (Python)
- `enum` - Enumerations (Python)
- `pathlib` - Path handling (Python)
- `string` - String handling (C++)
- `vector` - Dynamic arrays (C++)
- `chrono` - Time handling (C++)
- `filesystem` - File system (C++)

## Related Requirements
- REQ-055: Log File Rotation
- REQ-056: Log Compression

## Related ADRs
- ADR-003: Logging Architecture

## Implementation Notes

### Rotation Types
1. Size-based rotation
2. Time-based rotation
3. Both size and time rotation

### Rotation Triggers
1. Maximum file size
2. Time intervals (hourly, daily, weekly, monthly)
3. Specific times (midnight, hour, minute, second)

### Backup Management
1. Keep specified number of backups
2. Compress old backups
3. Clean up old backups
4. Naming pattern for backups

### Compression
1. Gzip compression
2. Compression levels (0-9)
3. Optional compression
4. Compress rotated files only

## Usage Example

### Python Example

```python
from omni_scripts.logging import LogRotationConfig, RotationType, RotationWhen, LogRotationHandler

# Create rotation configuration
config = LogRotationConfig(
    enabled=True,
    type=RotationType.BOTH,
    max_size=10 * 1024 * 1024,  # 10MB
    max_count=5,
    when=RotationWhen.MIDNIGHT,
    interval=24,
    backup_count=5,
    compression=True,
    compression_level=6,
    naming="{name}.{timestamp}.{ext}",
    extension="log",
    directory="logs"
)

# Create rotation handler
handler = LogRotationHandler(config)

# Write log data
handler.write("This is a log message\n", "myapp")

# Write more data
handler.write("Another log message\n", "myapp")

# Get backup files
backups = handler.get_backup_files("myapp")
print(f"Backup files: {backups}")

# Clean up all logs
handler.cleanup_all("myapp")
```

### C++ Example

```cpp
#include "log_file_rotation_schema.hpp"

using namespace omnicpp::logging;

int main() {
    // Create rotation configuration
    LogRotationConfig config;
    config.enabled = true;
    config.type = RotationType::BOTH;
    config.max_size = 10 * 1024 * 1024; // 10MB
    config.max_count = 5;
    config.when = RotationWhen::MIDNIGHT;
    config.interval = 24;
    config.backup_count = 5;
    config.compression = true;
    config.compression_level = CompressionLevel::NORMAL;
    config.naming = "{name}.{timestamp}.{ext}";
    config.extension = "log";
    config.directory = "logs";

    // Create rotation handler
    LogRotationHandler handler(config);

    // Write log data
    handler.write("This is a log message\n", "myapp");

    // Write more data
    handler.write("Another log message\n", "myapp");

    // Get backup files
    std::vector<std::filesystem::path> backups = handler.get_backup_files("myapp");
    std::cout << "Backup files: " << backups.size() << std::endl;

    // Clean up all logs
    handler.cleanup_all("myapp");

    return 0;
}
```
