# DES-034: Python Logging Interface

## Overview
Defines the Python logging interface for the OmniCpp build system.

## Interface Definition

### Python Code

```python
"""
Python Logging Interface for OmniCpp

This module provides a unified logging interface for the OmniCpp build system.
"""

import logging
import sys
from typing import Optional, Callable, Dict, List, Any
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
import json


class LogLevel(Enum):
    """Log levels for the logging system"""
    TRACE = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50
    OFF = 100


class LogFormat(Enum):
    """Log format types"""
    DEFAULT = "default"
    DETAILED = "detailed"
    COMPACT = "compact"
    JSON = "json"
    CUSTOM = "custom"


class LogHandlerType(Enum):
    """Log handler types"""
    CONSOLE = "console"
    FILE = "file"
    ROTATING_FILE = "rotating_file"
    TIMED_ROTATING_FILE = "timed_rotating_file"
    CUSTOM = "custom"


@dataclass
class LogMessage:
    """Log message structure"""
    level: LogLevel
    message: str
    logger_name: str
    file: str
    line: int
    function: str
    timestamp: float
    thread_id: int
    extra: Dict[str, Any]

    def __post_init__(self):
        if self.timestamp is None:
            import time
            self.timestamp = time.time()


@dataclass
class LogHandlerConfig:
    """Log handler configuration"""
    type: LogHandlerType
    path: Optional[str] = None
    format: str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    level: LogLevel = LogLevel.INFO
    async: bool = False
    queue_size: int = 8192
    flush_on_error: bool = True
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    encoding: str = "utf-8"
    errors: str = "replace"

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "type": self.type.value,
            "path": self.path,
            "format": self.format,
            "level": self.level.value,
            "async": self.async,
            "queue_size": self.queue_size,
            "flush_on_error": self.flush_on_error,
            "max_bytes": self.max_bytes,
            "backup_count": self.backup_count,
            "encoding": self.encoding,
            "errors": self.errors
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogHandlerConfig":
        """Create configuration from dictionary"""
        return cls(
            type=LogHandlerType(data.get("type", "console")),
            path=data.get("path"),
            format=data.get("format", "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"),
            level=LogLevel(data.get("level", 20)),
            async=data.get("async", False),
            queue_size=data.get("queue_size", 8192),
            flush_on_error=data.get("flush_on_error", True),
            max_bytes=data.get("max_bytes", 10 * 1024 * 1024),
            backup_count=data.get("backup_count", 5),
            encoding=data.get("encoding", "utf-8"),
            errors=data.get("errors", "replace")
        )


@dataclass
class LoggerConfig:
    """Logger configuration"""
    name: str
    level: LogLevel = LogLevel.INFO
    format: LogFormat = LogFormat.DEFAULT
    handlers: List[LogHandlerConfig] = None
    propagate: bool = True
    disabled: bool = False
    capture_warnings: bool = True
    capture_exceptions: bool = True

    def __post_init__(self):
        if self.handlers is None:
            self.handlers = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "name": self.name,
            "level": self.level.value,
            "format": self.format.value,
            "handlers": [h.to_dict() for h in self.handlers],
            "propagate": self.propagate,
            "disabled": self.disabled,
            "capture_warnings": self.capture_warnings,
            "capture_exceptions": self.capture_exceptions
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoggerConfig":
        """Create configuration from dictionary"""
        handlers_data = data.get("handlers", [])
        handlers = [LogHandlerConfig.from_dict(h) for h in handlers_data]

        return cls(
            name=data.get("name", "OmniCppLogger"),
            level=LogLevel(data.get("level", 20)),
            format=LogFormat(data.get("format", "default")),
            handlers=handlers,
            propagate=data.get("propagate", True),
            disabled=data.get("disabled", False),
            capture_warnings=data.get("capture_warnings", True),
            capture_exceptions=data.get("capture_exceptions", True)
        )


class ILogger:
    """Logger interface"""

    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message"""
        raise NotImplementedError

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message"""
        raise NotImplementedError

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message"""
        raise NotImplementedError

    def warn(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message"""
        raise NotImplementedError

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message"""
        raise NotImplementedError

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message"""
        raise NotImplementedError

    def exception(self, message: str, exc_info: bool = True) -> None:
        """Log an exception"""
        raise NotImplementedError

    def set_level(self, level: LogLevel) -> None:
        """Set the log level"""
        raise NotImplementedError

    def get_level(self) -> LogLevel:
        """Get the current log level"""
        raise NotImplementedError

    def get_name(self) -> str:
        """Get the logger name"""
        raise NotImplementedError

    def add_handler(self, handler: logging.Handler) -> None:
        """Add a log handler"""
        raise NotImplementedError

    def remove_handler(self, handler: logging.Handler) -> None:
        """Remove a log handler"""
        raise NotImplementedError

    def get_handlers(self) -> List[logging.Handler]:
        """Get all log handlers"""
        raise NotImplementedError

    def set_propagate(self, propagate: bool) -> None:
        """Set propagation to parent loggers"""
        raise NotImplementedError

    def get_propagate(self) -> bool:
        """Get propagation setting"""
        raise NotImplementedError

    def flush(self) -> None:
        """Flush all handlers"""
        raise NotImplementedError


class DefaultLogger(ILogger):
    """Default logger implementation"""

    def __init__(self, config: LoggerConfig):
        self._config = config
        self._logger = logging.getLogger(config.name)
        self._logger.setLevel(config.level.value)
        self._logger.propagate = config.propagate
        self._logger.disabled = config.disabled

        # Set up handlers
        for handler_config in config.handlers:
            handler = self._create_handler(handler_config)
            self._logger.addHandler(handler)

        # Capture warnings and exceptions
        if config.capture_warnings:
            logging.captureWarnings(True)

        if config.capture_exceptions:
            self._logger.exception = self._exception_handler

    def _create_handler(self, config: LogHandlerConfig) -> logging.Handler:
        """Create a log handler from configuration"""
        if config.type == LogHandlerType.CONSOLE:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter(config.format))
            handler.setLevel(config.level.value)
            return handler

        elif config.type == LogHandlerType.FILE:
            handler = logging.FileHandler(
                config.path,
                mode='a',
                encoding=config.encoding,
                errors=config.errors
            )
            handler.setFormatter(logging.Formatter(config.format))
            handler.setLevel(config.level.value)
            return handler

        elif config.type == LogHandlerType.ROTATING_FILE:
            from logging.handlers import RotatingFileHandler
            handler = RotatingFileHandler(
                config.path,
                maxBytes=config.max_bytes,
                backupCount=config.backup_count,
                encoding=config.encoding,
                errors=config.errors
            )
            handler.setFormatter(logging.Formatter(config.format))
            handler.setLevel(config.level.value)
            return handler

        elif config.type == LogHandlerType.TIMED_ROTATING_FILE:
            from logging.handlers import TimedRotatingFileHandler
            handler = TimedRotatingFileHandler(
                config.path,
                when='midnight',
                interval=1,
                backupCount=config.backup_count,
                encoding=config.encoding,
                errors=config.errors
            )
            handler.setFormatter(logging.Formatter(config.format))
            handler.setLevel(config.level.value)
            return handler

        else:
            raise ValueError(f"Unknown handler type: {config.type}")

    def _exception_handler(self, exc_type, exc_value, exc_traceback):
        """Exception handler"""
        self._logger.error(
            "Exception occurred",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.log(LogLevel.TRACE.value, message)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.debug(message)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.info(message)

    def warn(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.warning(message)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.error(message)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message"""
        if args or kwargs:
            message = message % args if args else message
            message = message % kwargs if kwargs else message
        self._logger.critical(message)

    def exception(self, message: str, exc_info: bool = True) -> None:
        """Log an exception"""
        self._logger.exception(message, exc_info=exc_info)

    def set_level(self, level: LogLevel) -> None:
        """Set the log level"""
        self._logger.setLevel(level.value)
        self._config.level = level

    def get_level(self) -> LogLevel:
        """Get the current log level"""
        return self._config.level

    def get_name(self) -> str:
        """Get the logger name"""
        return self._config.name

    def add_handler(self, handler: logging.Handler) -> None:
        """Add a log handler"""
        self._logger.addHandler(handler)

    def remove_handler(self, handler: logging.Handler) -> None:
        """Remove a log handler"""
        self._logger.removeHandler(handler)

    def get_handlers(self) -> List[logging.Handler]:
        """Get all log handlers"""
        return self._logger.handlers

    def set_propagate(self, propagate: bool) -> None:
        """Set propagation to parent loggers"""
        self._logger.propagate = propagate
        self._config.propagate = propagate

    def get_propagate(self) -> bool:
        """Get propagation setting"""
        return self._config.propagate

    def flush(self) -> None:
        """Flush all handlers"""
        for handler in self._logger.handlers:
            handler.flush()


class ILoggerManager:
    """Logger manager interface"""

    def register_logger(self, name: str, logger: ILogger) -> None:
        """Register a logger"""
        raise NotImplementedError

    def unregister_logger(self, name: str) -> None:
        """Unregister a logger"""
        raise NotImplementedError

    def get_logger(self, name: str) -> Optional[ILogger]:
        """Get a logger by name"""
        raise NotImplementedError

    def get_default_logger(self) -> Optional[ILogger]:
        """Get the default logger"""
        raise NotImplementedError

    def set_default_logger(self, name: str) -> None:
        """Set the default logger"""
        raise NotImplementedError

    def set_global_level(self, level: LogLevel) -> None:
        """Set the global log level"""
        raise NotImplementedError

    def get_global_level(self) -> LogLevel:
        """Get the global log level"""
        raise NotImplementedError

    def flush_all(self) -> None:
        """Flush all loggers"""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Shutdown the logger manager"""
        raise NotImplementedError


class DefaultLoggerManager(ILoggerManager):
    """Default logger manager implementation"""

    def __init__(self):
        self._loggers: Dict[str, ILogger] = {}
        self._default_logger_name: Optional[str] = None
        self._global_level: LogLevel = LogLevel.INFO

    def register_logger(self, name: str, logger: ILogger) -> None:
        """Register a logger"""
        self._loggers[name] = logger

    def unregister_logger(self, name: str) -> None:
        """Unregister a logger"""
        if name in self._loggers:
            del self._loggers[name]

    def get_logger(self, name: str) -> Optional[ILogger]:
        """Get a logger by name"""
        return self._loggers.get(name)

    def get_default_logger(self) -> Optional[ILogger]:
        """Get the default logger"""
        if self._default_logger_name:
            return self._loggers.get(self._default_logger_name)
        return None

    def set_default_logger(self, name: str) -> None:
        """Set the default logger"""
        self._default_logger_name = name

    def set_global_level(self, level: LogLevel) -> None:
        """Set the global log level"""
        self._global_level = level
        for logger in self._loggers.values():
            logger.set_level(level)

    def get_global_level(self) -> LogLevel:
        """Get the global log level"""
        return self._global_level

    def flush_all(self) -> None:
        """Flush all loggers"""
        for logger in self._loggers.values():
            logger.flush()

    def shutdown(self) -> None:
        """Shutdown the logger manager"""
        for logger in self._loggers.values():
            for handler in logger.get_handlers():
                handler.close()
        self._loggers.clear()


class ILoggerFactory:
    """Logger factory interface"""

    def create_logger(self, config: LoggerConfig) -> ILogger:
        """Create a logger from configuration"""
        raise NotImplementedError

    def create_logger_from_dict(self, data: Dict[str, Any]) -> ILogger:
        """Create a logger from dictionary"""
        raise NotImplementedError

    def create_logger_from_file(self, path: Path) -> ILogger:
        """Create a logger from file"""
        raise NotImplementedError


class DefaultLoggerFactory(ILoggerFactory):
    """Default logger factory implementation"""

    def create_logger(self, config: LoggerConfig) -> ILogger:
        """Create a logger from configuration"""
        return DefaultLogger(config)

    def create_logger_from_dict(self, data: Dict[str, Any]) -> ILogger:
        """Create a logger from dictionary"""
        config = LoggerConfig.from_dict(data)
        return self.create_logger(config)

    def create_logger_from_file(self, path: Path) -> ILogger:
        """Create a logger from file"""
        with open(path, 'r') as f:
            data = json.load(f)
        return self.create_logger_from_dict(data)


# Global logger accessor
class GlobalLogger:
    """Global logger accessor"""

    _manager: Optional[ILoggerManager] = None

    @classmethod
    def initialize(cls, config: LoggerConfig) -> None:
        """Initialize the global logger"""
        factory = DefaultLoggerFactory()
        logger = factory.create_logger(config)

        if cls._manager is None:
            cls._manager = DefaultLoggerManager()

        cls._manager.register_logger(config.name, logger)
        cls._manager.set_default_logger(config.name)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown the global logger"""
        if cls._manager:
            cls._manager.shutdown()
            cls._manager = None

    @classmethod
    def get_logger(cls, name: str = "") -> Optional[ILogger]:
        """Get a logger by name"""
        if cls._manager is None:
            return None

        if name:
            return cls._manager.get_logger(name)
        else:
            return cls._manager.get_default_logger()

    @classmethod
    def set_global_level(cls, level: LogLevel) -> None:
        """Set the global log level"""
        if cls._manager:
            cls._manager.set_global_level(level)

    @classmethod
    def get_global_level(cls) -> LogLevel:
        """Get the global log level"""
        if cls._manager:
            return cls._manager.get_global_level()
        return LogLevel.INFO

    @classmethod
    def flush_all(cls) -> None:
        """Flush all loggers"""
        if cls._manager:
            cls._manager.flush_all()

    @classmethod
    def trace(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message"""
        logger = cls.get_logger()
        if logger:
            logger.trace(message, *args, **kwargs)

    @classmethod
    def debug(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message"""
        logger = cls.get_logger()
        if logger:
            logger.debug(message, *args, **kwargs)

    @classmethod
    def info(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message"""
        logger = cls.get_logger()
        if logger:
            logger.info(message, *args, **kwargs)

    @classmethod
    def warn(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message"""
        logger = cls.get_logger()
        if logger:
            logger.warn(message, *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message"""
        logger = cls.get_logger()
        if logger:
            logger.error(message, *args, **kwargs)

    @classmethod
    def critical(cls, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message"""
        logger = cls.get_logger()
        if logger:
            logger.critical(message, *args, **kwargs)

    @classmethod
    def exception(cls, message: str, exc_info: bool = True) -> None:
        """Log an exception"""
        logger = cls.get_logger()
        if logger:
            logger.exception(message, exc_info=exc_info)
```

## Dependencies

### Internal Dependencies
- `DES-003` - Configuration schema
- `DES-004` - Logging configuration schema

### External Dependencies
- `logging` - Python logging module
- `sys` - System module
- `typing` - Type hints
- `dataclasses` - Data classes
- `pathlib` - Path handling
- `json` - JSON parsing
- `enum` - Enumerations

## Related Requirements
- REQ-005: Logging Configuration
- REQ-006: Error Handling & Exception Management

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Logger Design
1. Abstract logger interface
2. Multiple log levels
3. Multiple handler types
4. Async logging support

### Log Levels
1. TRACE - Most verbose
2. DEBUG - Debug information
3. INFO - General information
4. WARN - Warning messages
5. ERROR - Error messages
6. CRITICAL - Critical errors
7. OFF - Logging disabled

### Log Handlers
1. Console handler
2. File handler
3. Rotating file handler
4. Timed rotating file handler
5. Custom handler

### Logger Manager
1. Register/unregister loggers
2. Default logger management
3. Global level management
4. Flush all loggers

## Usage Example

```python
from omni_scripts.logging import GlobalLogger, LoggerConfig, LogLevel, LogHandlerConfig, LogHandlerType, LogFormat

# Create logger configuration
config = LoggerConfig(
    name="MyLogger",
    level=LogLevel.DEBUG,
    format=LogFormat.DETAILED
)

# Add console handler
console_handler = LogHandlerConfig(
    type=LogHandlerType.CONSOLE,
    level=LogLevel.INFO
)
config.handlers.append(console_handler)

# Add file handler
file_handler = LogHandlerConfig(
    type=LogHandlerType.FILE,
    path="logs/myapp.log",
    level=LogLevel.DEBUG
)
config.handlers.append(file_handler)

# Add rotating file handler
rotating_handler = LogHandlerConfig(
    type=LogHandlerType.ROTATING_FILE,
    path="logs/myapp_rotating.log",
    level=LogLevel.DEBUG,
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5
)
config.handlers.append(rotating_handler)

# Initialize global logger
GlobalLogger.initialize(config)

# Log messages
GlobalLogger.trace("This is a trace message")
GlobalLogger.debug("This is a debug message")
GlobalLogger.info("This is an info message")
GlobalLogger.warn("This is a warning message")
GlobalLogger.error("This is an error message")
GlobalLogger.critical("This is a critical message")

# Log with formatting
GlobalLogger.info("User %s logged in at %s", "john", "10:00")

# Log exception
try:
    # Some code that might raise an exception
    pass
except Exception as e:
    GlobalLogger.exception(f"An error occurred: {e}")

# Set global level
GlobalLogger.set_global_level(LogLevel.WARN)

# Flush all loggers
GlobalLogger.flush_all()

# Shutdown
GlobalLogger.shutdown()
```
