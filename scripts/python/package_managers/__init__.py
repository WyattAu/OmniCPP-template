"""
Package manager integration

This module provides unified integration for Conan, vcpkg, and CPM.cmake
package managers. It enables seamless dependency management across different
package managers while allowing them to work together without conflicts.
"""

from typing import Any, Dict, List, Optional

from .base import ExecutionResult, PackageInfo, PackageManagerBase
from .conan import ConanPackageManager
from .vcpkg import VcpkgPackageManager
from .cpm import CpmPackageManager
from .factory import PackageManagerFactory
from .manager import PackageManagerManager

__all__ = [
    # Base classes and data types
    "PackageManagerBase",
    "PackageInfo",
    "ExecutionResult",
    
    # Package manager implementations
    "ConanPackageManager",
    "VcpkgPackageManager",
    "CpmPackageManager",
    
    # Factory and manager
    "PackageManagerFactory",
    "PackageManagerManager",
]


def create_package_manager(manager_type: str, config: Optional[Dict[str, Any]] = None) -> PackageManagerBase:
    """Create a package manager instance.
    
    This is a convenience function that uses PackageManagerFactory
    to create a package manager instance.
    
    Args:
        manager_type: Package manager type (conan, vcpkg, cpm)
        config: Configuration dictionary (empty dict if None)
        
    Returns:
        Package manager instance
        
    Raises:
        ValidationError: If manager type is invalid
    """
    return PackageManagerFactory.create(manager_type, config)


def detect_available_managers(config: Optional[Dict[str, Any]] = None) -> List[PackageManagerBase]:
    """Detect available package managers.
    
    This is a convenience function that uses PackageManagerFactory
    to detect all available package managers.
    
    Args:
        config: Configuration dictionary (empty dict if None)
        
    Returns:
        List of available package manager instances
    """
    return PackageManagerFactory.detect_available(config)


def get_package_manager_manager(config: Dict[str, Any]) -> PackageManagerManager:
    """Get package manager manager instance.
    
    This is a convenience function that creates a PackageManagerManager
    instance with the given configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Package manager manager instance
    """
    return PackageManagerManager(config)
