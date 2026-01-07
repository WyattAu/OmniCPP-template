"""
Logger - Custom logging setup with colored output and file rotation

This module provides a custom logging implementation with colored console
output, file rotation, and custom formatting for the OmniCPP build system.
"""

import logging
import sys
from typing import Any, Dict
from logging.handlers import RotatingFileHandler

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for console."""
    
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }
    
    def __init__(self, fmt: str, datefmt: str, use_colors: bool = True) -> None:
        """Initialize colored formatter.
        
        Args:
            fmt: Log format string
            datefmt: Date format string
            use_colors: Whether to use colored output
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and COLORAMA_AVAILABLE
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors.
        
        Args:
            record: Log record to format
            
        Returns:
            Formatted log string
        """
        if self.use_colors:
            levelname = record.levelname
            color = self.COLORS.get(levelname, "")
            record.levelname = f"{color}{levelname}{Style.RESET_ALL}"
        
        return super().format(record)


class Logger:
    """Custom logger with colored output and file rotation."""
    
    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        """Initialize logger.
        
        Args:
            name: Logger name
            config: Logger configuration dictionary
        """
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.get("level", "INFO")))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Add console handler
        if config.get("console_handler_enabled", True):
            self._add_console_handler()
        
        # Add file handler
        if config.get("file_handler_enabled", False):
            self._add_file_handler()
    
    def _add_console_handler(self) -> None:
        """Add console handler with colored output."""
        console_handler = logging.StreamHandler(sys.stdout)
        
        log_format = self.config.get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        date_format = self.config.get("datefmt", "%Y-%m-%d %H:%M:%S")
        
        use_colors = self.config.get("colored_output", True)
        formatter = ColoredFormatter(log_format, date_format, use_colors)
        
        console_handler.setFormatter(formatter)
        console_handler.setLevel(getattr(logging, self.config.get("level", "INFO")))
        
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self) -> None:
        """Add file handler with rotation."""
        file_path = self.config.get("file_path", "logs/omnicpp_python.log")
        max_bytes = self.config.get("max_bytes", 10485760)  # 10MB default
        backup_count = self.config.get("backup_count", 5)
        
        try:
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            
            log_format = self.config.get(
                "format",
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            date_format = self.config.get("datefmt", "%Y-%m-%d %H:%M:%S")
            
            formatter = logging.Formatter(log_format, date_format)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(getattr(logging, self.config.get("level", "INFO")))
            
            self.logger.addHandler(file_handler)
        except Exception as e:
            # Log to stderr if file handler fails
            print(f"Failed to create file handler: {e}", file=sys.stderr)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message.
        
        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message.
        
        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message.
        
        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message.
        
        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message.
        
        Args:
            message: Message to log
            **kwargs: Additional context
        """
        self.logger.critical(message, extra=kwargs)
    
    def set_level(self, level: str) -> None:
        """Set log level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        for handler in self.logger.handlers:
            handler.setLevel(log_level)
    
    def get_level(self) -> str:
        """Get current log level.
        
        Returns:
            Current log level name
        """
        return logging.getLevelName(self.logger.level)
