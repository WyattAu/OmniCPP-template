"""
Compiler Detection Cache

This module provides caching functionality for compiler detection results
to improve performance by avoiding redundant detection operations.
"""

import hashlib
import json
import logging
import os
import time
from dataclasses import asdict, is_dataclass
from typing import Any, Optional


class CacheError(Exception):
    """Exception raised for cache-related errors."""
    pass


class CompilerDetectionCache:
    """Cache for compiler detection results.
    
    This class provides a persistent cache for compiler detection results,
    storing them in a JSON file with time-to-live (TTL) support.
    Cache entries are automatically invalidated when they expire.
    
    Attributes:
        cache_file: Path to cache file
        ttl: Time-to-live for cache entries in seconds
        _cache: In-memory cache dictionary
        _logger: Logger instance for cache operations
    """
    
    def __init__(self, cache_file: str = ".compiler_cache.json", ttl: int = 3600) -> None:
        """Initialize compiler detection cache.
        
        Args:
            cache_file: Path to cache file (default: .compiler_cache.json)
            ttl: Time-to-live for cache entries in seconds (default: 3600 = 1 hour)
            
        Raises:
            CacheError: If cache file cannot be loaded
        """
        self.cache_file: str = cache_file
        self.ttl: int = ttl
        self._cache: dict[str, dict[str, Any]] = {}
        self._logger: logging.Logger = logging.getLogger(__name__)
        
        # Load existing cache if it exists
        self._load_cache()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache.
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Cached value if found and not expired, None otherwise
            
        Raises:
            CacheError: If cache read operation fails
        """
        try:
            if key not in self._cache:
                self._logger.debug(f"Cache miss for key: {key}")
                return None
            
            entry = self._cache[key]
            
            # Check if entry is expired
            if time.time() - entry["timestamp"] > self.ttl:
                self._logger.debug(f"Cache entry expired for key: {key}")
                self.invalidate(key)
                return None
            
            self._logger.debug(f"Cache hit for key: {key}")
            return entry["value"]
        except Exception as e:
            error_msg = f"Failed to get cache entry for key '{key}': {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in cache.
        
        Args:
            key: Cache key to set
            value: Value to cache
            
        Raises:
            CacheError: If cache write operation fails
        """
        try:
            # Convert dataclass to dict if necessary
            if is_dataclass(value):
                cache_value = asdict(value)  # type: ignore[arg-type]
            else:
                cache_value = value
            
            self._cache[key] = {
                "value": cache_value,
                "timestamp": time.time()
            }
            
            self._save_cache()
            self._logger.debug(f"Cache set for key: {key}")
        except Exception as e:
            error_msg = f"Failed to set cache entry for key '{key}': {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def invalidate(self, key: str) -> None:
        """Invalidate a specific cache entry.
        
        Args:
            key: Cache key to invalidate
            
        Raises:
            CacheError: If cache invalidation fails
        """
        try:
            if key in self._cache:
                del self._cache[key]
                self._save_cache()
                self._logger.debug(f"Cache invalidated for key: {key}")
            else:
                self._logger.debug(f"Cache key not found for invalidation: {key}")
        except Exception as e:
            error_msg = f"Failed to invalidate cache entry for key '{key}': {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def clear(self) -> None:
        """Clear all cache entries.
        
        Raises:
            CacheError: If cache clear operation fails
        """
        try:
            cache_size = len(self._cache)
            self._cache.clear()
            self._save_cache()
            self._logger.info(f"Cache cleared: {cache_size} entries removed")
        except Exception as e:
            error_msg = f"Failed to clear cache: {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def get_cache_key(self, *args: Any) -> str:
        """Generate a cache key from arguments.
        
        This method creates a deterministic hash key from provided
        arguments, which can be used to cache and retrieve values.
        
        Args:
            *args: Arguments to generate cache key from
            
        Returns:
            MD5 hash of serialized arguments
            
        Raises:
            CacheError: If key generation fails
        """
        try:
            # Convert arguments to JSON string with sorted keys for consistency
            key_data = json.dumps(args, sort_keys=True, default=str)
            # Generate MD5 hash
            hash_key = hashlib.md5(key_data.encode()).hexdigest()
            self._logger.debug(f"Generated cache key: {hash_key} from args: {args}")
            return hash_key
        except Exception as e:
            error_msg = f"Failed to generate cache key from args {args}: {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def is_cached(self, key: str) -> bool:
        """Check if a key exists in cache and is not expired.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists and is not expired, False otherwise
            
        Raises:
            CacheError: If cache check operation fails
        """
        try:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            
            # Check if entry is expired
            if time.time() - entry["timestamp"] > self.ttl:
                return False
            
            return True
        except Exception as e:
            error_msg = f"Failed to check cache for key '{key}': {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def get_cache_info(self) -> dict[str, Any]:
        """Get information about cache.
        
        Returns:
            Dictionary containing cache statistics including:
            - total_entries: Total number of cache entries
            - valid_entries: Number of non-expired entries
            - expired_entries: Number of expired entries
            - cache_file: Path to cache file
            - ttl: Time-to-live in seconds
            - cache_size_bytes: Size of cache file in bytes
            
        Raises:
            CacheError: If cache info retrieval fails
        """
        try:
            total_entries = len(self._cache)
            current_time = time.time()
            
            valid_entries = sum(
                1 for entry in self._cache.values()
                if current_time - entry["timestamp"] <= self.ttl
            )
            
            expired_entries = total_entries - valid_entries
            
            cache_size_bytes = 0
            if os.path.exists(self.cache_file):
                cache_size_bytes = os.path.getsize(self.cache_file)
            
            return {
                "total_entries": total_entries,
                "valid_entries": valid_entries,
                "expired_entries": expired_entries,
                "cache_file": self.cache_file,
                "ttl": self.ttl,
                "cache_size_bytes": cache_size_bytes
            }
        except Exception as e:
            error_msg = f"Failed to get cache info: {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def cleanup_expired(self) -> int:
        """Remove all expired cache entries.
        
        Returns:
            Number of expired entries removed
            
        Raises:
            CacheError: If cleanup operation fails
        """
        try:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time - entry["timestamp"] > self.ttl
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            if expired_keys:
                self._save_cache()
                self._logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
            
            return len(expired_keys)
        except Exception as e:
            error_msg = f"Failed to cleanup expired cache entries: {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
    
    def _load_cache(self) -> None:
        """Load cache from file.
        
        Raises:
            CacheError: If cache file cannot be loaded
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
                self._logger.info(f"Loaded cache from {self.cache_file}: {len(self._cache)} entries")
            else:
                self._cache = {}
                self._logger.debug(f"Cache file not found, starting with empty cache: {self.cache_file}")
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse cache file {self.cache_file}: {str(e)}"
            self._logger.error(error_msg)
            self._cache = {}
            raise CacheError(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to load cache from {self.cache_file}: {str(e)}"
            self._logger.error(error_msg)
            self._cache = {}
            raise CacheError(error_msg) from e
    
    def _save_cache(self) -> None:
        """Save cache to file.
        
        Raises:
            CacheError: If cache file cannot be saved
        """
        try:
            # Ensure directory exists
            cache_dir = os.path.dirname(self.cache_file)
            if cache_dir and not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            
            # Write cache to file
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, indent=2)
            
            self._logger.debug(f"Saved cache to {self.cache_file}: {len(self._cache)} entries")
        except Exception as e:
            error_msg = f"Failed to save cache to {self.cache_file}: {str(e)}"
            self._logger.error(error_msg)
            raise CacheError(error_msg) from e
