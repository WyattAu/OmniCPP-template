"""
Clean command - Build directory cleanup

This module provides clean command for removing build artifacts,
CMake cache, and temporary files with selective cleaning support.
"""

import argparse
import os
import shutil
from typing import Any, Dict, List

from core.logger import Logger
from core.exception_handler import BuildError, PermissionError


class CleanCommand:
    """Clean build artifacts and cache.
    
    This command handles cleanup including:
    - Build directory removal
    - CMake cache removal
    - Temporary file removal
    - Selective cleaning
    - Dry-run mode
    - Cleanup verification
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize clean command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("clean", config.get("logging", {}))
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute clean command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting cleanup...")
            
            # Get configuration parameters
            build_dir = getattr(args, "build_dir", "build")
            dry_run = getattr(args, "dry_run", False)
            keep_cache = getattr(args, "keep_cache", False)
            _ = getattr(args, "verbose", False)  # type: ignore
            
            # Determine what to clean
            items_to_clean = self._get_items_to_clean(
                build_dir=build_dir,
                keep_cache=keep_cache
            )
            
            if not items_to_clean:
                self.logger.info("Nothing to clean")
                return 0
            
            # Display what will be cleaned
            self._display_cleanup_plan(items_to_clean, dry_run)
            
            # Perform cleanup
            if dry_run:
                self.logger.info("Dry-run mode - no changes made")
                return 0
            
            # Clean items
            cleaned_count = 0
            for item in items_to_clean:
                try:
                    if os.path.exists(item):
                        if os.path.isfile(item):
                            os.remove(item)
                            self.logger.debug(f"Removed file: {item}")
                        elif os.path.isdir(item):
                            shutil.rmtree(item)
                            self.logger.debug(f"Removed directory: {item}")
                        cleaned_count += 1
                except PermissionError as e:
                    raise PermissionError(
                        f"Permission denied removing {item}",
                        {"path": item, "error": str(e)}
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to remove {item}: {e}")
            
            # Verify cleanup
            self._verify_cleanup(items_to_clean)
            
            self.logger.info(f"Cleaned {cleaned_count} item(s)")
            return 0
            
        except (BuildError, PermissionError) as e:
            self.logger.error(f"Cleanup failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during cleanup: {e}")
            return 1
    
    def _get_items_to_clean(
        self,
        build_dir: str,
        keep_cache: bool
    ) -> List[str]:
        """Get list of items to clean.
        
        Args:
            build_dir: Build directory
            keep_cache: Whether to keep CMake cache
            
        Returns:
            List of paths to clean
        """
        items: List[str] = []
        
        # Add build directory
        if os.path.exists(build_dir):
            items.append(build_dir)
        
        # Add CMake cache files
        if not keep_cache:
            cache_files = [
                "CMakeCache.txt",
                "CMakeFiles",
                "cmake_install.cmake",
                "compile_commands.json"
            ]
            
            for cache_file in cache_files:
                cache_path = os.path.join(build_dir, cache_file)
                if os.path.exists(cache_path):
                    items.append(cache_path)
        
        # Add temporary directories
        temp_dirs = ["temp", "tmp", ".tmp"]
        for temp_dir in temp_dirs:
            temp_path = os.path.join(build_dir, temp_dir)
            if os.path.exists(temp_path):
                items.append(temp_path)
        
        # Add package directories
        package_dirs = ["packages", "_CPack_Packages"]
        for package_dir in package_dirs:
            package_path = os.path.join(build_dir, package_dir)
            if os.path.exists(package_path):
                items.append(package_path)
        
        return items
    
    def _display_cleanup_plan(
        self,
        items: List[str],
        dry_run: bool
    ) -> None:
        """Display cleanup plan.
        
        Args:
            items: List of items to clean
            dry_run: Whether this is a dry run
        """
        self.logger.info(f"Items to clean: {len(items)}")
        
        for item in items:
            if os.path.exists(item):
                if os.path.isfile(item):
                    size = os.path.getsize(item)
                    self.logger.info(f"  File: {item} ({size} bytes)")
                elif os.path.isdir(item):
                    dir_size = self._get_directory_size(item)
                    self.logger.info(f"  Directory: {item} ({dir_size} bytes)")
    
    def _get_directory_size(self, directory: str) -> int:
        """Get total size of directory.
        
        Args:
            directory: Directory path
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        
        try:
            for dirpath, _, filenames in os.walk(directory):  # type: ignore
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except OSError:
                        pass
        except Exception:
            pass
        
        return total_size
    
    def _verify_cleanup(self, items: List[str]) -> None:
        """Verify cleanup was successful.
        
        Args:
            items: List of items that were cleaned
        """
        self.logger.info("Verifying cleanup...")
        
        remaining_items = []
        for item in items:
            if os.path.exists(item):
                remaining_items.append(item)  # type: ignore
        
        if remaining_items:
            self.logger.warning(
                f"Some items could not be removed: {len(remaining_items)}"  # type: ignore
            )
            for item in remaining_items:  # type: ignore
                self.logger.warning(f"  Remaining: {item}")
        else:
            self.logger.info("All items cleaned successfully")
