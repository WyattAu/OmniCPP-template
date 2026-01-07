"""
CMake cache management

This module provides comprehensive CMake cache variable management including
reading, writing, and manipulating CMake cache entries with proper error
handling and validation.
"""

import os
import re
from pathlib import Path
from typing import Any, Optional

from core.exception_handler import BuildError, ConfigurationError
from core.logger import Logger


class CacheManager:
    """Manage CMake cache variables.
    
    This class provides methods for reading, writing, and manipulating
    CMake cache entries stored in CMakeCache.txt files with proper
    validation and error handling.
    """
    
    # CMake cache entry types
    CACHE_TYPES = {
        "BOOL": "BOOL",
        "STRING": "STRING",
        "PATH": "PATH",
        "FILEPATH": "FILEPATH",
        "INTERNAL": "INTERNAL",
        "STATIC": "STATIC",
        "UNINITIALIZED": "UNINITIALIZED"
    }
    
    def __init__(self, build_dir: str, logger: Optional[Logger] = None) -> None:
        """Initialize cache manager.
        
        Args:
            build_dir: Build directory containing CMakeCache.txt
            logger: Logger instance for logging operations
            
        Raises:
            ConfigurationError: If build directory is invalid
        """
        self.build_dir = Path(build_dir).resolve()
        self.cache_file = self.build_dir / "CMakeCache.txt"
        self.logger = logger or Logger("CacheManager", {
            "level": "INFO",
            "console_handler_enabled": True,
            "file_handler_enabled": False
        })
        
        # Validate build directory
        if not self.build_dir.exists():
            self.logger.warning(f"Build directory does not exist: {self.build_dir}")
        
        self.logger.info(f"Cache manager initialized for: {self.cache_file}")
    
    def get(self, key: str) -> Optional[str]:
        """Get cache variable value.
        
        Args:
            key: Cache variable key
            
        Returns:
            Cache variable value or None if not found
        """
        if not self.cache_file.exists():
            self.logger.debug("CMakeCache.txt does not exist")
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # Parse cache entry
                    match = re.match(r'^([^:=]+)[:=](.*)$', line)
                    if match:
                        entry_key = match.group(1).strip()
                        if entry_key == key:
                            # Extract value (remove type and description)
                            value_part = match.group(2).strip()
                            # Value is after the type
                            value_match = re.match(r'^([^=]+)=(.*)$', value_part)
                            if value_match:
                                return value_match.group(2).strip()
            
            return None
        except Exception as e:
            self.logger.error(f"Failed to read cache entry '{key}': {e}")
            return None
    
    def get_with_type(self, key: str) -> Optional[tuple[str, str]]:
        """Get cache variable value with type.
        
        Args:
            key: Cache variable key
            
        Returns:
            Tuple of (type, value) or None if not found
        """
        if not self.cache_file.exists():
            self.logger.debug("CMakeCache.txt does not exist")
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # Parse cache entry
                    match = re.match(r'^([^:=]+)[:=](.*)$', line)
                    if match:
                        entry_key = match.group(1).strip()
                        if entry_key == key:
                            # Extract type and value
                            value_part = match.group(2).strip()
                            value_match = re.match(r'^([^=]+)=(.*)$', value_part)
                            if value_match:
                                cache_type = value_match.group(1).strip()
                                value = value_match.group(2).strip()
                                return (cache_type, value)
            
            return None
        except Exception as e:
            self.logger.error(f"Failed to read cache entry '{key}': {e}")
            return None
    
    def set(self, key: str, value: str, cache_type: str = "STRING") -> None:
        """Set cache variable value.
        
        Args:
            key: Cache variable key
            value: Cache variable value
            cache_type: Cache variable type (BOOL, STRING, PATH, etc.)
            
        Raises:
            ConfigurationError: If cache type is invalid
            BuildError: If cache file cannot be written
        """
        # Validate cache type
        if cache_type not in self.CACHE_TYPES:
            raise ConfigurationError(
                f"Invalid cache type: {cache_type}",
                {"valid_types": list(self.CACHE_TYPES.keys()), "provided": cache_type}
            )
        
        # Ensure build directory exists
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Read existing cache entries
            entries = []
            key_found = False
            
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        stripped_line = line.strip()
                        # Check if this is the key we're updating
                        if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith('//'):
                            match = re.match(r'^([^:=]+)[:=](.*)$', stripped_line)
                            if match:
                                entry_key = match.group(1).strip()
                                if entry_key == key:
                                    # Replace this entry
                                    entries.append(f"{key}:{cache_type}={value}\n")
                                    key_found = True
                                    continue
                        
                        entries.append(line)
            
            # Add new entry if not found
            if not key_found:
                entries.append(f"{key}:{cache_type}={value}\n")
            
            # Write back to cache file
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                f.writelines(entries)
            
            self.logger.debug(f"Set cache entry: {key}={value} ({cache_type})")
        except Exception as e:
            self.logger.error(f"Failed to set cache entry '{key}': {e}")
            raise BuildError(
                f"Failed to set cache entry: {e}",
                {"key": key, "value": value, "cache_type": cache_type}
            )
    
    def remove(self, key: str) -> bool:
        """Remove cache variable.
        
        Args:
            key: Cache variable key to remove
            
        Returns:
            True if entry was removed, False if not found
        """
        if not self.cache_file.exists():
            return False
        
        try:
            # Read existing cache entries
            entries = []
            key_found = False
            
            with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    stripped_line = line.strip()
                    # Check if this is the key we're removing
                    if stripped_line and not stripped_line.startswith('#') and not stripped_line.startswith('//'):
                        match = re.match(r'^([^:=]+)[:=](.*)$', stripped_line)
                        if match:
                            entry_key = match.group(1).strip()
                            if entry_key == key:
                                key_found = True
                                continue
                    
                    entries.append(line)
            
            # Write back to cache file if key was found
            if key_found:
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    f.writelines(entries)
                
                self.logger.debug(f"Removed cache entry: {key}")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove cache entry '{key}': {e}")
            return False
    
    def list_all(self) -> dict[str, tuple[str, str]]:
        """List all cache variables.
        
        Returns:
            Dictionary mapping keys to (type, value) tuples
        """
        cache_vars: dict[str, tuple[str, str]] = {}
        
        if not self.cache_file.exists():
            self.logger.debug("CMakeCache.txt does not exist")
            return cache_vars
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # Parse cache entry
                    match = re.match(r'^([^:=]+)[:=](.*)$', line)
                    if match:
                        entry_key = match.group(1).strip()
                        value_part = match.group(2).strip()
                        value_match = re.match(r'^([^=]+)=(.*)$', value_part)
                        if value_match:
                            cache_type = value_match.group(1).strip()
                            value = value_match.group(2).strip()
                            cache_vars[entry_key] = (cache_type, value)
            
            self.logger.debug(f"Found {len(cache_vars)} cache entries")
            return cache_vars
        except Exception as e:
            self.logger.error(f"Failed to list cache entries: {e}")
            return cache_vars
    
    def clear(self) -> bool:
        """Clear all cache variables.
        
        Returns:
            True if cache was cleared, False otherwise
        """
        if not self.cache_file.exists():
            self.logger.debug("CMakeCache.txt does not exist, nothing to clear")
            return True
        
        try:
            # Remove cache file
            self.cache_file.unlink()
            self.logger.info("CMake cache cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if cache variable exists.
        
        Args:
            key: Cache variable key
            
        Returns:
            True if key exists in cache, False otherwise
        """
        return self.get(key) is not None
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean cache variable.
        
        Args:
            key: Cache variable key
            default: Default value if key not found
            
        Returns:
            Boolean value
        """
        value = self.get(key)
        if value is None:
            return default
        
        # Parse boolean value
        value_upper = value.upper()
        if value_upper in ("ON", "TRUE", "1", "YES"):
            return True
        elif value_upper in ("OFF", "FALSE", "0", "NO", ""):
            return False
        else:
            self.logger.warning(f"Invalid boolean value for '{key}': {value}")
            return default
    
    def set_bool(self, key: str, value: bool) -> None:
        """Set boolean cache variable.
        
        Args:
            key: Cache variable key
            value: Boolean value
        """
        cmake_value = "ON" if value else "OFF"
        self.set(key, cmake_value, "BOOL")
    
    def get_path(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get path cache variable.
        
        Args:
            key: Cache variable key
            default: Default value if key not found
            
        Returns:
            Path value or default
        """
        return self.get(key) or default
    
    def set_path(self, key: str, value: str) -> None:
        """Set path cache variable.
        
        Args:
            key: Cache variable key
            value: Path value
        """
        self.set(key, value, "PATH")
    
    def validate_cache(self) -> list[str]:
        """Validate cache entries and return list of issues.
        
        Returns:
            List of validation issue messages
        """
        issues: list[str] = []
        
        if not self.cache_file.exists():
            issues.append("CMakeCache.txt does not exist")
            return issues
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # Validate cache entry format
                    match = re.match(r'^([^:=]+)[:=](.*)$', line)
                    if not match:
                        issues.append(f"Line {line_num}: Invalid cache entry format")
                        continue
                    
                    entry_key = match.group(1).strip()
                    value_part = match.group(2).strip()
                    
                    # Validate value format
                    value_match = re.match(r'^([^=]+)=(.*)$', value_part)
                    if not value_match:
                        issues.append(f"Line {line_num}: Invalid value format for '{entry_key}'")
                        continue
                    
                    cache_type = value_match.group(1).strip()
                    
                    # Validate cache type
                    if cache_type not in self.CACHE_TYPES:
                        issues.append(f"Line {line_num}: Unknown cache type '{cache_type}' for '{entry_key}'")
            
            if not issues:
                self.logger.info("Cache validation passed")
            else:
                self.logger.warning(f"Cache validation found {len(issues)} issues")
            
            return issues
        except Exception as e:
            issues.append(f"Failed to validate cache: {e}")
            return issues
    
    def export_to_dict(self) -> dict[str, Any]:
        """Export cache variables to a dictionary.
        
        Returns:
            Dictionary with cache variables and their types
        """
        cache_dict: dict[str, Any] = {}
        
        for key, (cache_type, value) in self.list_all().items():
            # Convert boolean values
            if cache_type == "BOOL":
                cache_dict[key] = value.upper() in ("ON", "TRUE", "1")
            # Convert path values
            elif cache_type in ("PATH", "FILEPATH"):
                cache_dict[key] = str(Path(value).resolve())
            else:
                cache_dict[key] = value
        
        return cache_dict
    
    def import_from_dict(self, cache_dict: dict[str, Any]) -> None:
        """Import cache variables from a dictionary.
        
        Args:
            cache_dict: Dictionary with cache variables
        """
        for key, value in cache_dict.items():
            # Determine cache type based on value type
            if isinstance(value, bool):
                self.set_bool(key, value)
            elif isinstance(value, (str, Path)):
                self.set_path(key, str(value))
            else:
                self.set(key, str(value))
        
        self.logger.info(f"Imported {len(cache_dict)} cache entries")
