"""
Configuration Manager - Load, validate, and manage configuration files

This module provides configuration file loading, validation, caching,
and management for the OmniCPP build system.
"""

import json
import os
from typing import Any, Dict
from pathlib import Path

from core.exception_handler import ConfigurationError


class ConfigManager:
    """Configuration file loading, validation, and management."""
    
    def __init__(self, config_path: str) -> None:
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path: str = config_path
        self._config: Dict[str, Any] | None = None
        self._cache: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        """Load and validate configuration.
        
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigurationError: If configuration file is invalid or missing
        """
        if not os.path.exists(self.config_path):
            raise ConfigurationError(
                f"Configuration file not found: {self.config_path}",
                {"path": self.config_path}
            )
        
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in configuration file: {e}",
                {"path": self.config_path, "error": str(e)}
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load configuration: {e}",
                {"path": self.config_path, "error": str(e)}
            )
        
        # Validate configuration
        if not self.validate(config):
            raise ConfigurationError(
                "Configuration validation failed",
                {"path": self.config_path}
            )
        
        self._config = config
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        if self._config is None:
            self.load()
        
        # Support dot notation for nested keys
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._config = None
        self._cache.clear()
        self.load()
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic validation - check required fields
        required_fields = ["project_name", "project_version"]
        
        for field in required_fields:
            if field not in config:
                return False
        
        # Validate types
        if not isinstance(config.get("project_name"), str):
            return False
        
        if not isinstance(config.get("project_version"), str):
            return False
        
        # Validate optional fields if present
        if "cpp_standard" in config:
            if config["cpp_standard"] not in ["20", "23"]:
                return False
        
        return True
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.
        
        Returns:
            Complete configuration dictionary
        """
        if self._config is None:
            self.load()
        
        return self._config.copy()
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value in memory (not persisted).
        
        Args:
            key: Configuration key
            value: Value to set
        """
        if self._config is None:
            self.load()
        
        # Support dot notation for nested keys
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save current configuration to file.
        
        Raises:
            ConfigurationError: If save fails
        """
        if self._config is None:
            raise ConfigurationError(
                "No configuration loaded to save",
                {"path": self.config_path}
            )
        
        try:
            # Ensure directory exists
            config_dir = os.path.dirname(self.config_path)
            if config_dir:
                os.makedirs(config_dir, exist_ok=True)
            
            with open(self.config_path, "w") as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            raise ConfigurationError(
                f"Failed to save configuration: {e}",
                {"path": self.config_path, "error": str(e)}
            )
    
    def get_path(self) -> str:
        """Get configuration file path.
        
        Returns:
            Configuration file path
        """
        return self.config_path
    
    def exists(self) -> bool:
        """Check if configuration file exists.
        
        Returns:
            True if configuration file exists, False otherwise
        """
        return os.path.exists(self.config_path)
