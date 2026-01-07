# ADR-014: File Rotation and Log Retention Policy

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Logging

---

## Context

The OmniCPP Template project generates log files for both C++ and Python code. Without proper log rotation and retention policies, log files can grow indefinitely, consuming disk space and making it difficult to find relevant information.

### Current State

Log files are written without rotation:
- **C++ Logs:** Written to single file without rotation
- **Python Logs:** Written to single file without rotation
- **No Retention Policy:** No policy for old log files
- **No Cleanup:** No automatic cleanup of old logs

### Issues

1. **Unbounded Growth:** Log files grow indefinitely
2. **Disk Space:** Consumes excessive disk space
3. **Performance:** Large log files slow down logging
4. **No Retention:** No policy for old log files
5. **No Cleanup:** No automatic cleanup of old logs
6. **Difficult Analysis:** Large log files are hard to analyze

## Decision

Implement **file rotation and log retention policy** with:
1. **Automatic Rotation:** Rotate log files based on size
2. **Retention Policy:** Keep only recent log files
3. **Compression:** Compress old log files
4. **Cleanup:** Automatic cleanup of old logs
5. **Configurable:** Configurable rotation and retention settings
6. **Cross-Language:** Consistent policy for both C++ and Python

### 1. Rotation Policy

```cpp
// include/engine/logging/rotation_policy.hpp
#pragma once

#include <string>
#include <filesystem>
#include <chrono>

namespace engine {
namespace logging {

/**
 * @brief Log rotation policy
 */
class RotationPolicy {
public:
    /**
     * @brief Rotation trigger
     */
    enum class Trigger {
        SIZE,      // Rotate based on file size
        TIME,      // Rotate based on time
        BOTH       // Rotate based on both size and time
    };

    /**
     * @brief Constructor
     * @param max_file_size Maximum file size in bytes
     * @param max_files Maximum number of files to keep
     * @param rotation_interval Rotation interval in hours
     * @param trigger Rotation trigger
     */
    RotationPolicy(
        size_t max_file_size = 1024 * 1024 * 5,  // 5 MB
        size_t max_files = 3,
        std::chrono::hours rotation_interval = std::chrono::hours(24),
        Trigger trigger = Trigger::SIZE
    );

    /**
     * @brief Check if rotation is needed
     * @param log_file Path to log file
     * @return True if rotation is needed
     */
    bool shouldRotate(const std::filesystem::path& log_file) const;

    /**
     * @brief Rotate log file
     * @param log_file Path to log file
     */
    void rotate(const std::filesystem::path& log_file) const;

    /**
     * @brief Clean old log files
     * @param log_dir Directory containing log files
     * @param log_prefix Prefix of log files
     */
    void cleanOldLogs(
        const std::filesystem::path& log_dir,
        const std::string& log_prefix
    ) const;

    /**
     * @brief Get maximum file size
     * @return Maximum file size in bytes
     */
    size_t getMaxFileSize() const { return max_file_size_; }

    /**
     * @brief Get maximum number of files
     * @return Maximum number of files
     */
    size_t getMaxFiles() const { return max_files_; }

    /**
     * @brief Get rotation interval
     * @return Rotation interval
     */
    std::chrono::hours getRotationInterval() const { return rotation_interval_; }

    /**
     * @brief Get rotation trigger
     * @return Rotation trigger
     */
    Trigger getTrigger() const { return trigger_; }

private:
    size_t max_file_size_;
    size_t max_files_;
    std::chrono::hours rotation_interval_;
    Trigger trigger_;

    /**
     * @brief Check if file size exceeds maximum
     * @param log_file Path to log file
     * @return True if file size exceeds maximum
     */
    bool checkSize(const std::filesystem::path& log_file) const;

    /**
     * @brief Check if rotation interval has passed
     * @param log_file Path to log file
     * @return True if rotation interval has passed
     */
    bool checkTime(const std::filesystem::path& log_file) const;

    /**
     * @brief Compress log file
     * @param log_file Path to log file
     */
    void compress(const std::filesystem::path& log_file) const;
};

} // namespace logging
} // namespace engine
```

### 2. Python Rotation Handler

```python
# omni_scripts/logging/handlers.py
"""Custom logging handlers with rotation."""

import logging
import gzip
import os
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
import threading

class RotatingFileHandler(logging.Handler):
    """Custom rotating file handler with compression."""

    def __init__(
        self,
        filename: Path,
        max_bytes: int = 1024 * 1024 * 5,  # 5 MB
        backup_count: int = 3,
        rotation_interval: int = 24,  # hours
        compress: bool = True
    ):
        """Initialize rotating file handler.

        Args:
            filename: Path to log file
            max_bytes: Maximum file size in bytes
            backup_count: Maximum number of backup files
            rotation_interval: Rotation interval in hours
            compress: Compress old log files
        """
        super().__init__()
        self.filename = Path(filename)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.rotation_interval = rotation_interval
        self.compress = compress
        self._lock = threading.Lock()

        # Create log directory if it doesn't exist
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        # Open log file
        self.stream = open(self.filename, 'a', encoding='utf-8')

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record.

        Args:
            record: Log record
        """
        try:
            # Check if rotation is needed
            if self._should_rotate():
                self._rotate()

            # Write log record
            msg = self.format(record)
            self.stream.write(msg + '\n')
            self.stream.flush()

        except Exception:
            self.handleError(record)

    def _should_rotate(self) -> bool:
        """Check if rotation is needed.

        Returns:
            True if rotation is needed
        """
        with self._lock:
            # Check file size
            if self.filename.stat().st_size >= self.max_bytes:
                return True

            # Check rotation interval
            if self.rotation_interval > 0:
                file_time = datetime.fromtimestamp(self.filename.stat().st_mtime)
                if datetime.now() - file_time >= timedelta(hours=self.rotation_interval):
                    return True

            return False

    def _rotate(self) -> None:
        """Rotate log file."""
        with self._lock:
            # Close current file
            self.stream.close()

            # Rotate backup files
            for i in range(self.backup_count - 1, 0, -1):
                old_file = self._get_backup_file(i)
                new_file = self._get_backup_file(i + 1)

                if old_file.exists():
                    if new_file.exists():
                        new_file.unlink()
                    old_file.rename(new_file)

            # Move current file to backup
            backup_file = self._get_backup_file(1)
            if backup_file.exists():
                backup_file.unlink()
            self.filename.rename(backup_file)

            # Compress old backup files
            if self.compress:
                self._compress_backups()

            # Clean old backups
            self._clean_old_backups()

            # Open new log file
            self.stream = open(self.filename, 'a', encoding='utf-8')

    def _get_backup_file(self, index: int) -> Path:
        """Get backup file path.

        Args:
            index: Backup index

        Returns:
            Backup file path
        """
        if index == 0:
            return self.filename
        else:
            return self.filename.with_suffix(f'.{index}.log')

    def _compress_backups(self) -> None:
        """Compress old backup files."""
        for i in range(2, self.backup_count + 1):
            backup_file = self._get_backup_file(i)
            if backup_file.exists() and not backup_file.suffix == '.gz':
                compressed_file = backup_file.with_suffix(f'.{i}.log.gz')

                # Compress file
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Remove original file
                backup_file.unlink()

    def _clean_old_backups(self) -> None:
        """Clean old backup files."""
        for i in range(self.backup_count + 1, 100):
            backup_file = self._get_backup_file(i)
            if backup_file.exists():
                backup_file.unlink()
            else:
                break

    def close(self) -> None:
        """Close handler."""
        with self._lock:
            if self.stream:
                self.stream.close()
                self.stream = None
```

### 3. Retention Policy

```python
# omni_scripts/logging/retention.py
"""Log retention policy."""

from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import logging

class RetentionPolicy:
    """Log retention policy."""

    def __init__(
        self,
        max_age_days: int = 30,
        max_size_mb: int = 100,
        max_files: int = 10
    ):
        """Initialize retention policy.

        Args:
            max_age_days: Maximum age of log files in days
            max_size_mb: Maximum total size of log files in MB
            max_files: Maximum number of log files
        """
        self.max_age_days = max_age_days
        self.max_size_mb = max_size_mb
        self.max_files = max_files
        self.logger = logging.getLogger(__name__)

    def cleanup(self, log_dir: Path, log_prefix: str = "omnicpp") -> List[Path]:
        """Clean up old log files.

        Args:
            log_dir: Directory containing log files
            log_prefix: Prefix of log files

        Returns:
            List of deleted files
        """
        deleted_files = []

        # Find all log files
        log_files = self._find_log_files(log_dir, log_prefix)

        # Sort by modification time (oldest first)
        log_files.sort(key=lambda f: f.stat().st_mtime)

        # Apply retention policy
        for log_file in log_files:
            if self._should_delete(log_file, log_files):
                try:
                    log_file.unlink()
                    deleted_files.append(log_file)
                    self.logger.info(f"Deleted old log file: {log_file}")
                except Exception as e:
                    self.logger.error(f"Failed to delete {log_file}: {e}")

        return deleted_files

    def _find_log_files(self, log_dir: Path, log_prefix: str) -> List[Path]:
        """Find all log files.

        Args:
            log_dir: Directory containing log files
            log_prefix: Prefix of log files

        Returns:
            List of log files
        """
        log_files = []

        if not log_dir.exists():
            return log_files

        for file in log_dir.iterdir():
            if file.is_file() and file.name.startswith(log_prefix):
                log_files.append(file)

        return log_files

    def _should_delete(self, log_file: Path, all_files: List[Path]) -> bool:
        """Check if file should be deleted.

        Args:
            log_file: Log file to check
            all_files: All log files

        Returns:
            True if file should be deleted
        """
        # Check file age
        if self._is_too_old(log_file):
            return True

        # Check total size
        if self._is_too_large(all_files):
            return True

        # Check file count
        if self._is_too_many(all_files):
            return True

        return False

    def _is_too_old(self, log_file: Path) -> bool:
        """Check if file is too old.

        Args:
            log_file: Log file to check

        Returns:
            True if file is too old
        """
        if self.max_age_days <= 0:
            return False

        file_age = datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)
        return file_age > timedelta(days=self.max_age_days)

    def _is_too_large(self, all_files: List[Path]) -> bool:
        """Check if total size is too large.

        Args:
            all_files: All log files

        Returns:
            True if total size is too large
        """
        if self.max_size_mb <= 0:
            return False

        total_size = sum(f.stat().st_size for f in all_files)
        total_size_mb = total_size / (1024 * 1024)

        return total_size_mb > self.max_size_mb

    def _is_too_many(self, all_files: List[Path]) -> bool:
        """Check if there are too many files.

        Args:
            all_files: All log files

        Returns:
            True if there are too many files
        """
        if self.max_files <= 0:
            return False

        return len(all_files) > self.max_files
```

### 4. Configuration

```json
// config/logging_cpp.json
{
  "log_file": "logs/omnicpp.log",
  "log_level": "INFO",
  "max_file_size": 5242880,
  "max_files": 3,
  "rotation_interval_hours": 24,
  "compress_old_logs": true,
  "retention_policy": {
    "max_age_days": 30,
    "max_size_mb": 100,
    "max_files": 10
  }
}
```

```json
// config/logging_python.json
{
  "log_file": "logs/omnicpp.log",
  "log_level": "INFO",
  "max_file_size": 5242880,
  "max_files": 3,
  "rotation_interval_hours": 24,
  "compress_old_logs": true,
  "retention_policy": {
    "max_age_days": 30,
    "max_size_mb": 100,
    "max_files": 10
  }
}
```

### 5. Usage Examples

```cpp
// C++ usage
#include "engine/logging/logger.hpp"
#include "engine/logging/rotation_policy.hpp"

int main() {
    // Initialize logger with rotation policy
    auto& logger = engine::logging::Logger::getInstance();

    engine::logging::RotationPolicy policy(
        1024 * 1024 * 5,  // 5 MB
        3,                      // 3 files
        std::chrono::hours(24),  // 24 hours
        engine::logging::RotationPolicy::Trigger::SIZE
    );

    logger.initialize("logs/omnicpp.log", engine::logging::LogLevel::INFO);

    // Log messages
    logger.info("This is an info message");

    return 0;
}
```

```python
# Python usage
from logging.logger import Logger
from logging.config import LogConfig
from logging.handlers import RotatingFileHandler
from logging.retention import RetentionPolicy

# Create logger with rotation
config = LogConfig(
    log_file=Path("logs/omnicpp.log"),
    max_file_size=1024 * 1024 * 5,  # 5 MB
    max_files=3,
    rotation_interval=24,  # hours
    compress=True
)

logger = Logger(config)

# Log messages
logger.info("This is an info message")

# Clean old logs
retention_policy = RetentionPolicy(
    max_age_days=30,
    max_size_mb=100,
    max_files=10
)
deleted_files = retention_policy.cleanup(Path("logs"))
print(f"Deleted {len(deleted_files)} old log files")
```

## Consequences

### Positive

1. **Bounded Growth:** Log files have bounded growth
2. **Disk Space:** Controlled disk space usage
3. **Performance:** Consistent logging performance
4. **Retention Policy:** Clear policy for old log files
5. **Automatic Cleanup:** Automatic cleanup of old logs
6. **Compression:** Compressed old logs save space
7. **Configurable:** Configurable rotation and retention settings

### Negative

1. **Complexity:** More complex than simple logging
2. **Overhead:** Rotation and cleanup overhead
3. **Learning Curve:** Developers need to understand policy
4. **File Management:** More files to manage

### Neutral

1. **Documentation:** Requires documentation for policy
2. **Testing:** Need to test rotation and cleanup

## Alternatives Considered

### Alternative 1: No Rotation

**Description:** No log rotation

**Pros:**
- Simpler implementation
- No overhead

**Cons:**
- Unbounded growth
- Excessive disk space
- Poor performance

**Rejected:** Unbounded growth and poor performance

### Alternative 2: Manual Rotation

**Description:** Manual log rotation

**Pros:**
- Simple implementation
- No automatic overhead

**Cons:**
- Manual intervention required
- Inconsistent rotation
- No retention policy

**Rejected:** Manual intervention required

### Alternative 3: External Tool

**Description:** Use external tool for log rotation

**Pros:**
- No custom code
- Proven solution

**Cons:**
- External dependency
- Less control
- Platform-specific

**Rejected:** External dependency and less control

## Related ADRs

- [ADR-013: Dual logging system (spdlog for C++, custom for Python)](ADR-013-dual-logging-system.md)
- [ADR-015: Structured logging format](ADR-015-structured-logging-format.md)

## References

- [logrotate Documentation](https://linux.die.net/man/8/logrotate)
- [Python Logging Handlers](https://docs.python.org/3/library/logging.handlers.html)
- [spdlog Rotating File Sink](https://github.com/gabime/spdlog/wiki/3.-Custom-formatting)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
