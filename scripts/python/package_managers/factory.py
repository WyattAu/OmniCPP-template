"""
Package manager factory for creating package manager instances

This module provides a factory pattern for creating package manager instances
based on configuration and detecting available package managers.
"""

from typing import Any, Dict, List, Optional

from ..core.exception_handler import ValidationError
from ..core.logger import Logger
from .base import PackageManagerBase
from .conan import ConanPackageManager
from .vcpkg import VcpkgPackageManager
from .cpm import CpmPackageManager


class PackageManagerFactory:
    """Factory for creating package manager instances.
    
    This class provides methods to create package manager instances
    based on type, detect available package managers, and
    provide package manager information.
    """
    
    # Package manager type constants
    TYPE_CONAN: str = "conan"
    TYPE_VCPKG: str = "vcpkg"
    TYPE_CPM: str = "cpm"
    
    # All supported package manager types
    SUPPORTED_TYPES: List[str] = [TYPE_CONAN, TYPE_VCPKG, TYPE_CPM]
    
    # Package manager class mapping
    _MANAGER_CLASSES: Dict[str, type[PackageManagerBase]] = {
        TYPE_CONAN: ConanPackageManager,
        TYPE_VCPKG: VcpkgPackageManager,
        TYPE_CPM: CpmPackageManager,
    }
    
    @staticmethod
    def create(manager_type: str, config: Optional[Dict[str, Any]] = None) -> PackageManagerBase:
        """Create package manager instance.
        
        Args:
            manager_type: Package manager type (conan, vcpkg, cpm)
            config: Configuration dictionary (empty dict if None)
            
        Returns:
            Package manager instance
            
        Raises:
            ValidationError: If manager type is invalid
        """
        if config is None:
            config = {}
        
        # Normalize manager type
        manager_type = manager_type.lower().strip()
        
        # Validate manager type
        if manager_type not in PackageManagerFactory.SUPPORTED_TYPES:
            raise ValidationError(
                f"Unknown package manager type: {manager_type}. "
                f"Supported types: {', '.join(PackageManagerFactory.SUPPORTED_TYPES)}"
            )
        
        # Get manager class
        manager_class = PackageManagerFactory._MANAGER_CLASSES[manager_type]
        
        # Create and return instance
        return manager_class(config)
    
    @staticmethod
    def create_with_logger(manager_type: str, logger: Logger) -> PackageManagerBase:
        """Create package manager instance with logger.
        
        Args:
            manager_type: Package manager type (conan, vcpkg, cpm)
            logger: Logger instance
            
        Returns:
            Package manager instance with logger configured
            
        Raises:
            ValidationError: If manager type is invalid
        """
        config = {"logger": logger}
        return PackageManagerFactory.create(manager_type, config)
    
    @staticmethod
    def detect_available(config: Optional[Dict[str, Any]] = None) -> List[PackageManagerBase]:
        """Detect available package managers.
        
        This method attempts to create instances of all supported
        package managers and returns those that are available.
        
        Args:
            config: Configuration dictionary (empty dict if None)
            
        Returns:
            List of available package manager instances
        """
        if config is None:
            config = {}
        
        available_managers: List[PackageManagerBase] = []
        
        for manager_type in PackageManagerFactory.SUPPORTED_TYPES:
            try:
                manager = PackageManagerFactory.create(manager_type, config)
                if manager.is_available():
                    available_managers.append(manager)
            except Exception:
                # Skip managers that fail to initialize
                pass
        
        return available_managers
    
    @staticmethod
    def get_available_types(config: Optional[Dict[str, Any]] = None) -> List[str]:
        """Get list of available package manager types.
        
        Args:
            config: Configuration dictionary (empty dict if None)
            
        Returns:
            List of available package manager type names
        """
        available_managers = PackageManagerFactory.detect_available(config)
        return [manager.get_name() for manager in available_managers]
    
    @staticmethod
    def get_manager_info(manager_type: str) -> Dict[str, Any]:
        """Get package manager information.
        
        Args:
            manager_type: Package manager type
            
        Returns:
            Dictionary with package manager information
            
        Raises:
            ValidationError: If manager type is invalid
        """
        # Normalize manager type
        manager_type = manager_type.lower().strip()
        
        # Validate manager type
        if manager_type not in PackageManagerFactory.SUPPORTED_TYPES:
            raise ValidationError(
                f"Unknown package manager type: {manager_type}"
            )
        
        # Return manager information
        info: Dict[str, Any] = {
            "type": manager_type,
            "name": manager_type.capitalize(),
            "class": PackageManagerFactory._MANAGER_CLASSES[manager_type].__name__,
        }
        
        # Add type-specific information
        if manager_type == PackageManagerFactory.TYPE_CONAN:
            info.update({
                "description": "Conan package manager for C/C++ dependencies",
                "website": "https://conan.io/",
                "supports_binary_packages": True,
                "supports_source_packages": True,
            })
        elif manager_type == PackageManagerFactory.TYPE_VCPKG:
            info.update({
                "description": "vcpkg package manager for C/C++ libraries",
                "website": "https://vcpkg.io/",
                "supports_binary_packages": True,
                "supports_source_packages": True,
            })
        elif manager_type == PackageManagerFactory.TYPE_CPM:
            info.update({
                "description": "CPM.cmake - CMake package manager",
                "website": "https://github.com/cpm-cmake/CPM.cmake",
                "supports_binary_packages": False,
                "supports_source_packages": True,
            })
        
        return info
    
    @staticmethod
    def get_all_manager_types() -> List[str]:
        """Get all supported package manager types.
        
        Returns:
            List of all supported package manager type names
        """
        return PackageManagerFactory.SUPPORTED_TYPES.copy()
    
    @staticmethod
    def is_supported(manager_type: str) -> bool:
        """Check if package manager type is supported.
        
        Args:
            manager_type: Package manager type
            
        Returns:
            True if supported, False otherwise
        """
        return manager_type.lower().strip() in PackageManagerFactory.SUPPORTED_TYPES
    
    @staticmethod
    def get_preferred_manager(config: Optional[Dict[str, Any]] = None) -> Optional[PackageManagerBase]:
        """Get preferred package manager based on configuration.
        
        This method checks configuration for a preferred package manager
        and returns it if available. Otherwise, it returns the first
        available package manager.
        
        Args:
            config: Configuration dictionary (empty dict if None)
            
        Returns:
            Preferred package manager instance or None if none available
        """
        if config is None:
            config = {}
        
        # Check for preferred package manager in config
        preferred_type = config.get("preferred_package_manager")
        
        if preferred_type and PackageManagerFactory.is_supported(preferred_type):
            try:
                manager = PackageManagerFactory.create(preferred_type, config)
                if manager.is_available():
                    return manager
            except Exception:
                pass
        
        # Return first available manager
        available_managers = PackageManagerFactory.detect_available(config)
        return available_managers[0] if available_managers else None
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate package manager configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check for preferred package manager
        preferred_type = config.get("preferred_package_manager")
        
        if preferred_type:
            # Validate that preferred type is supported
            if not PackageManagerFactory.is_supported(preferred_type):
                return False
        
        # Check for package manager-specific configurations
        for manager_type in PackageManagerFactory.SUPPORTED_TYPES:
            if manager_type in config:
                manager_config = config[manager_type]
                
                # Validate that manager config is a dictionary
                if not isinstance(manager_config, dict):
                    return False
        
        return True
    
    def __repr__(self) -> str:
        """String representation of package manager factory.
        
        Returns:
            String representation
        """
        return f"PackageManagerFactory(supported_types={len(self.SUPPORTED_TYPES)})"
