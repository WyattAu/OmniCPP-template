"""
Unit tests for Compiler Detection Cache

Tests caching functionality for compiler detection results,
including get/set operations, invalidation, clearing, and cache key generation.
"""

import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from dataclasses import dataclass

# Add scripts/python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from compilers.base import CompilerInfo
from compilers.compiler_detection_cache import (
    CacheError,
    CompilerDetectionCache
)


@dataclass
class MockDataclass:
    """Mock dataclass for testing."""
    name: str
    value: int


class TestCompilerDetectionCache(unittest.TestCase):
    """Test cases for CompilerDetectionCache class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create temporary cache file
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")
        self.cache = CompilerDetectionCache(cache_file=self.cache_file, ttl=60)
    
    def tearDown(self) -> None:
        """Clean up test fixtures."""
        # Remove temporary directory and all contents
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_cache_initialization(self) -> None:
        """Test cache initialization creates empty cache."""
        self.assertEqual(len(self.cache._cache), 0)
        self.assertEqual(self.cache.cache_file, self.cache_file)
        self.assertEqual(self.cache.ttl, 60)
    
    def test_cache_set_and_get(self) -> None:
        """Test setting and getting cache values."""
        # Set a value
        self.cache.set("test_key", "test_value")
        
        # Get value
        result = self.cache.get("test_key")
        
        # Verify
        self.assertEqual(result, "test_value")
    
    def test_cache_get_nonexistent_key(self) -> None:
        """Test getting a non-existent key returns None."""
        result = self.cache.get("nonexistent_key")
        self.assertIsNone(result)
    
    def test_cache_set_and_get_dict(self) -> None:
        """Test setting and getting dictionary values."""
        test_dict = {"key1": "value1", "key2": "value2"}
        
        # Set dictionary
        self.cache.set("dict_key", test_dict)
        
        # Get dictionary
        result = self.cache.get("dict_key")
        
        # Verify
        self.assertEqual(result, test_dict)
    
    def test_cache_set_and_get_list(self) -> None:
        """Test setting and getting list values."""
        test_list = ["item1", "item2", "item3"]
        
        # Set list
        self.cache.set("list_key", test_list)
        
        # Get list
        result = self.cache.get("list_key")
        
        # Verify
        self.assertEqual(result, test_list)
    
    def test_cache_set_and_get_dataclass(self) -> None:
        """Test setting and getting dataclass values."""
        test_dataclass = MockDataclass(name="test", value=42)
        
        # Set dataclass
        self.cache.set("dataclass_key", test_dataclass)
        
        # Get dataclass (should be converted to dict)
        result = self.cache.get("dataclass_key")
        
        # Verify (dataclass is converted to dict)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "test")
        self.assertEqual(result["value"], 42)
    
    def test_cache_set_and_get_compiler_info(self) -> None:
        """Test setting and getting CompilerInfo values."""
        test_compiler_info = CompilerInfo(
            name="MSVC",
            version="19.40.33807",
            path="C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.40.33807\\bin\\Hostx64\\x64\\cl.exe",
            target="windows",
            flags=["/O2", "/W3"]
        )
        
        # Set CompilerInfo
        self.cache.set("compiler_key", test_compiler_info)
        
        # Get CompilerInfo (should be converted to dict)
        result = self.cache.get("compiler_key")
        
        # Verify (CompilerInfo is converted to dict)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "MSVC")
        self.assertEqual(result["version"], "19.40.33807")
        self.assertEqual(result["target"], "windows")
    
    def test_cache_invalidate_existing_key(self) -> None:
        """Test invalidating an existing cache key."""
        # Set a value
        self.cache.set("test_key", "test_value")
        
        # Verify it exists
        self.assertIsNotNone(self.cache.get("test_key"))
        
        # Invalidate
        self.cache.invalidate("test_key")
        
        # Verify it's gone
        self.assertIsNone(self.cache.get("test_key"))
    
    def test_cache_invalidate_nonexistent_key(self) -> None:
        """Test invalidating a non-existent key does not raise error."""
        # Should not raise an exception
        self.cache.invalidate("nonexistent_key")
    
    def test_cache_clear(self) -> None:
        """Test clearing all cache entries."""
        # Set multiple values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Verify they exist
        self.assertEqual(len(self.cache._cache), 3)
        
        # Clear cache
        self.cache.clear()
        
        # Verify all are gone
        self.assertEqual(len(self.cache._cache), 0)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
        self.assertIsNone(self.cache.get("key3"))
    
    def test_cache_key_generation_single_arg(self) -> None:
        """Test cache key generation with single argument."""
        key = self.cache.get_cache_key("test_arg")
        
        # Verify key is a string (MD5 hash)
        self.assertIsInstance(key, str)
        self.assertEqual(len(key), 32)  # MD5 hash length
    
    def test_cache_key_generation_multiple_args(self) -> None:
        """Test cache key generation with multiple arguments."""
        key1 = self.cache.get_cache_key("arg1", "arg2", "arg3")
        key2 = self.cache.get_cache_key("arg1", "arg2", "arg3")
        
        # Verify keys are consistent
        self.assertEqual(key1, key2)
    
    def test_cache_key_generation_different_args(self) -> None:
        """Test cache key generation with different arguments produces different keys."""
        key1 = self.cache.get_cache_key("arg1", "arg2")
        key2 = self.cache.get_cache_key("arg1", "arg3")
        
        # Verify keys are different
        self.assertNotEqual(key1, key2)
    
    def test_cache_key_generation_dict_args(self) -> None:
        """Test cache key generation with dictionary arguments."""
        key1 = self.cache.get_cache_key({"key": "value"})
        key2 = self.cache.get_cache_key({"key": "value"})
        
        # Verify keys are consistent (sorted keys)
        self.assertEqual(key1, key2)
    
    def test_cache_key_generation_order_independence(self) -> None:
        """Test cache key generation is order-independent for dicts."""
        key1 = self.cache.get_cache_key({"a": 1, "b": 2})
        key2 = self.cache.get_cache_key({"b": 2, "a": 1})
        
        # Verify keys are same (sorted keys)
        self.assertEqual(key1, key2)
    
    def test_is_cached_existing_key(self) -> None:
        """Test is_cached returns True for existing, non-expired key."""
        # Set a value
        self.cache.set("test_key", "test_value")
        
        # Check if cached
        self.assertTrue(self.cache.is_cached("test_key"))
    
    def test_is_cached_nonexistent_key(self) -> None:
        """Test is_cached returns False for non-existent key."""
        self.assertFalse(self.cache.is_cached("nonexistent_key"))
    
    def test_is_cached_expired_key(self) -> None:
        """Test is_cached returns False for expired key."""
        # Create cache with very short TTL
        short_ttl_cache = CompilerDetectionCache(
            cache_file=self.cache_file,
            ttl=0  # Immediate expiration
        )
        
        # Set a value
        short_ttl_cache.set("test_key", "test_value")
        
        # Wait a moment to ensure expiration
        time.sleep(0.1)
        
        # Check if cached (should be False due to expiration)
        self.assertFalse(short_ttl_cache.is_cached("test_key"))
    
    def test_cache_expiration(self) -> None:
        """Test cache entries expire after TTL."""
        # Create cache with very short TTL and different file
        short_ttl_cache_file = os.path.join(self.temp_dir, "short_ttl_cache.json")
        short_ttl_cache = CompilerDetectionCache(
            cache_file=short_ttl_cache_file,
            ttl=0.1  # Very short TTL (100ms)
        )
        
        # Set a value
        short_ttl_cache.set("test_key", "test_value")
        
        # Verify it exists initially
        self.assertIsNotNone(short_ttl_cache.get("test_key"))
        
        # Wait longer than TTL to ensure expiration
        time.sleep(0.2)
        
        # Verify it's expired
        self.assertIsNone(short_ttl_cache.get("test_key"))
    
    def test_cache_persistence(self) -> None:
        """Test cache persists to file and can be loaded."""
        # Set a value
        self.cache.set("test_key", "test_value")
        
        # Create new cache instance with same file
        new_cache = CompilerDetectionCache(cache_file=self.cache_file, ttl=60)
        
        # Verify value is loaded
        result = new_cache.get("test_key")
        self.assertEqual(result, "test_value")
    
    def test_get_cache_info(self) -> None:
        """Test getting cache information."""
        # Set some values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        # Get cache info
        info = self.cache.get_cache_info()
        
        # Verify
        self.assertEqual(info["total_entries"], 2)
        self.assertEqual(info["valid_entries"], 2)
        self.assertEqual(info["expired_entries"], 0)
        self.assertEqual(info["cache_file"], self.cache_file)
        self.assertEqual(info["ttl"], 60)
        self.assertGreater(info["cache_size_bytes"], 0)
    
    def test_get_cache_info_with_expired_entries(self) -> None:
        """Test getting cache info with expired entries."""
        # Create cache with very short TTL
        short_ttl_cache = CompilerDetectionCache(
            cache_file=self.cache_file,
            ttl=0  # Immediate expiration
        )
        
        # Set some values
        short_ttl_cache.set("key1", "value1")
        short_ttl_cache.set("key2", "value2")
        
        # Wait a moment to ensure expiration
        time.sleep(0.1)
        
        # Get cache info
        info = short_ttl_cache.get_cache_info()
        
        # Verify
        self.assertEqual(info["total_entries"], 2)
        self.assertEqual(info["valid_entries"], 0)
        self.assertEqual(info["expired_entries"], 2)
    
    def test_cleanup_expired(self) -> None:
        """Test cleanup of expired entries."""
        # Create cache with very short TTL
        short_ttl_cache = CompilerDetectionCache(
            cache_file=self.cache_file,
            ttl=0  # Immediate expiration
        )
        
        # Set some values
        short_ttl_cache.set("key1", "value1")
        short_ttl_cache.set("key2", "value2")
        
        # Wait a moment to ensure expiration
        time.sleep(0.1)
        
        # Cleanup expired entries
        removed_count = short_ttl_cache.cleanup_expired()
        
        # Verify
        self.assertEqual(removed_count, 2)
        self.assertEqual(len(short_ttl_cache._cache), 0)
    
    def test_cleanup_expired_with_valid_entries(self) -> None:
        """Test cleanup only removes expired entries."""
        # Set some values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        # Cleanup expired entries (none should be expired)
        removed_count = self.cache.cleanup_expired()
        
        # Verify
        self.assertEqual(removed_count, 0)
        self.assertEqual(len(self.cache._cache), 2)
    
    def test_cache_overwrite_existing_key(self) -> None:
        """Test overwriting an existing cache key."""
        # Set initial value
        self.cache.set("test_key", "value1")
        
        # Overwrite with new value
        self.cache.set("test_key", "value2")
        
        # Verify new value
        result = self.cache.get("test_key")
        self.assertEqual(result, "value2")
    
    def test_cache_with_special_characters_in_key(self) -> None:
        """Test cache with special characters in key."""
        special_key = "key_with-special.chars_123"
        
        # Set and get
        self.cache.set(special_key, "value")
        result = self.cache.get(special_key)
        
        # Verify
        self.assertEqual(result, "value")
    
    def test_cache_with_unicode_values(self) -> None:
        """Test cache with unicode values."""
        unicode_value = "Hello 世界 🌍"
        
        # Set and get
        self.cache.set("unicode_key", unicode_value)
        result = self.cache.get("unicode_key")
        
        # Verify
        self.assertEqual(result, unicode_value)
    
    def test_cache_error_on_invalid_json_file(self) -> None:
        """Test cache raises error on invalid JSON file."""
        # Create invalid JSON file
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
        
        # Try to create cache with invalid file
        with self.assertRaises(CacheError):
            CompilerDetectionCache(cache_file=self.cache_file, ttl=60)
    
    def test_cache_error_on_get_failure(self) -> None:
        """Test cache raises error on get failure."""
        # Manually corrupt cache by setting to None
        setattr(self.cache, "_cache", None)
        
        # Try to get value
        with self.assertRaises(CacheError):
            self.cache.get("test_key")
    
    def test_cache_error_on_set_failure(self) -> None:
        """Test cache raises error on set failure."""
        # Manually corrupt cache by setting to None
        setattr(self.cache, "_cache", None)
        
        # Try to set value
        with self.assertRaises(CacheError):
            self.cache.set("test_key", "test_value")
    
    def test_cache_supports_all_compiler_types(self) -> None:
        """Test cache supports all compiler types."""
        compiler_types = [
            "msvc",
            "msvc_clang",
            "mingw_gcc",
            "mingw_clang",
            "gcc",
            "clang"
        ]
        
        for compiler_type in compiler_types:
            # Set compiler info
            compiler_info = CompilerInfo(
                name=compiler_type.upper(),
                version="1.0.0",
                path=f"/path/to/{compiler_type}",
                target="windows",
                flags=[]
            )
            
            # Generate cache key
            cache_key = self.cache.get_cache_key(compiler_type, "x64")
            
            # Cache and retrieve
            self.cache.set(cache_key, compiler_info)
            result = self.cache.get(cache_key)
            
            # Verify
            self.assertIsNotNone(result)
            self.assertEqual(result["name"], compiler_type.upper())
    
    def test_cache_supports_cross_compilers(self) -> None:
        """Test cache supports cross-compilers."""
        cross_compilers = [
            ("linux", "x86_64"),
            ("wasm", "wasm32"),
            ("android", "arm64-v8a")
        ]
        
        for platform, arch in cross_compilers:
            # Generate cache key
            cache_key = self.cache.get_cache_key("cross", platform, arch)
            
            # Set and get
            self.cache.set(cache_key, {"platform": platform, "arch": arch})
            result = self.cache.get(cache_key)
            
            # Verify
            self.assertIsNotNone(result)
            self.assertEqual(result["platform"], platform)
            self.assertEqual(result["arch"], arch)
    
    def test_cache_supports_all_architectures(self) -> None:
        """Test cache supports all architectures."""
        architectures = ["x64", "x86", "arm", "arm64"]
        
        for arch in architectures:
            # Generate cache key
            cache_key = self.cache.get_cache_key("compiler", arch)
            
            # Set and get
            self.cache.set(cache_key, {"architecture": arch})
            result = self.cache.get(cache_key)
            
            # Verify
            self.assertIsNotNone(result)
            self.assertEqual(result["architecture"], arch)


if __name__ == "__main__":
    unittest.main()
