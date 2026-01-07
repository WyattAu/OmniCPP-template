"""
Package manager manager for coordinating multiple package managers

This module provides a high-level manager that coordinates multiple package managers,
handles dependency resolution, conflict detection, and fallback mechanisms.
"""

from typing import Any, Dict, List, Optional

from ..core.exception_handler import DependencyError
from ..core.logger import Logger
from .base import PackageManagerBase, PackageInfo
from .factory import PackageManagerFactory


class PackageManagerManager:
    """Manager for coordinating multiple package managers.
    
    This class provides high-level coordination of multiple package managers,
    including dependency resolution, conflict detection, and fallback mechanisms.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize package manager manager.
        
        Args:
            config: Configuration dictionary containing package manager settings
        """
        self.config: Dict[str, Any] = config
        self.logger: Optional[Logger] = None
        self._managers: Dict[str, PackageManagerBase] = {}
        self._active_manager: Optional[PackageManagerBase] = None
        self._dependency_graph: Dict[str, List[str]] = {}
    
    def initialize(self) -> None:
        """Initialize package manager manager.
        
        This method initializes all available package managers
        and selects the active package manager based on configuration.
        
        Raises:
            DependencyError: If no package managers are available
        """
        # Initialize logger if available
        if "logger" in self.config:
            self.logger = self.config["logger"]
        
        # Detect available package managers
        available_managers = PackageManagerFactory.detect_available(self.config)
        
        if not available_managers:
            raise DependencyError(
                "No package managers available. Please install Conan, vcpkg, or use CPM.cmake."
            )
        
        if self.logger:
            self.logger.info(f"Available package managers: {[m.get_name() for m in available_managers]}")
        
        # Store available managers
        for manager in available_managers:
            self._managers[manager.get_name()] = manager
        
        # Select active manager
        self._active_manager = PackageManagerFactory.get_preferred_manager(self.config)
        
        if self._active_manager is None:
            raise DependencyError(
                "No preferred package manager available. "
                f"Available: {list(self._managers.keys())}"
            )
        
        if self.logger:
            self.logger.info(f"Active package manager: {self._active_manager.get_name()}")
    
    def get_active_manager(self) -> Optional[PackageManagerBase]:
        """Get active package manager.
        
        Returns:
            Active package manager instance or None if not initialized
        """
        return self._active_manager
    
    def get_manager(self, manager_type: str) -> Optional[PackageManagerBase]:
        """Get package manager by type.
        
        Args:
            manager_type: Package manager type (conan, vcpkg, cpm)
            
        Returns:
            Package manager instance or None if not available
        """
        return self._managers.get(manager_type.lower())
    
    def get_all_managers(self) -> Dict[str, PackageManagerBase]:
        """Get all available package managers.
        
        Returns:
            Dictionary of package manager instances by type
        """
        return self._managers.copy()
    
    def install_package(self, package: str, version: Optional[str] = None, 
                     manager_type: Optional[str] = None) -> bool:
        """Install package using active or specified package manager.
        
        Args:
            package: Package name
            version: Package version (latest if None)
            manager_type: Package manager type to use (active if None)
            
        Returns:
            True if installation succeeded, False otherwise
        """
        # Get package manager to use
        manager = self._get_manager_for_install(manager_type)
        
        if manager is None:
            if self.logger:
                self.logger.error(f"No package manager available for type: {manager_type}")
            return False
        
        # Install package
        if self.logger:
            self.logger.info(f"Installing {package} using {manager.get_name()}")
        
        success = manager.install_package(package, version)
        
        # Update dependency graph
        if success:
            self._add_to_dependency_graph(package, manager.get_name())
        
        return success
    
    def get_package_info(self, package: str, 
                       manager_type: Optional[str] = None) -> Optional[PackageInfo]:
        """Get package information from active or specified package manager.
        
        Args:
            package: Package name
            manager_type: Package manager type to use (active if None)
            
        Returns:
            Package information or None if not found
        """
        # Get package manager to use
        manager = self._get_manager_for_install(manager_type)
        
        if manager is None:
            if self.logger:
                self.logger.error(f"No package manager available for type: {manager_type}")
            return None
        
        # Get package info
        return manager.get_package_info(package)
    
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Detect package manager conflicts.
        
        This method checks for conflicts between different package managers,
        such as the same package being managed by multiple managers.
        
        Returns:
            List of conflict dictionaries
        """
        conflicts: List[Dict[str, Any]] = []
        
        # Check for packages managed by multiple managers
        package_managers: Dict[str, List[str]] = {}
        
        for manager_name, manager in self._managers.items():
            # Get list of installed packages (if supported)
            if hasattr(manager, "list_installed_packages"):
                packages = manager.list_installed_packages()  # type: ignore[attr-defined]
                for pkg in packages:
                    if pkg not in package_managers:
                        package_managers[pkg] = []
                    package_managers[pkg].append(manager_name)
        
        # Detect conflicts
        for package, managers in package_managers.items():
            if len(managers) > 1:
                conflicts.append({
                    "package": package,
                    "managers": managers,
                    "type": "multiple_managers",
                    "description": f"Package {package} is managed by multiple package managers: {', '.join(managers)}"
                })
        
        return conflicts
    
    def resolve_conflicts(self, conflicts: List[Dict[str, Any]]) -> bool:
        """Resolve package manager conflicts.
        
        This method attempts to resolve conflicts by selecting a preferred
        package manager for conflicting packages.
        
        Args:
            conflicts: List of conflict dictionaries
            
        Returns:
            True if conflicts were resolved, False otherwise
        """
        if not conflicts:
            return True
        
        if self.logger:
            self.logger.warning(f"Found {len(conflicts)} package manager conflicts")
        
        # Resolve each conflict
        for conflict in conflicts:
            if self.logger:
                self.logger.warning(f"Conflict: {conflict['description']}")
            
            # Use active manager for conflicting packages
            if self._active_manager:
                package = conflict["package"]
                if self.logger:
                    self.logger.info(f"Using {self._active_manager.get_name()} for {package}")
        
        return True
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get dependency graph.
        
        Returns:
            Dictionary mapping packages to their dependencies
        """
        return self._dependency_graph.copy()
    
    def add_dependency(self, package: str, dependencies: List[str]) -> None:
        """Add dependency to graph.
        
        Args:
            package: Package name
            dependencies: List of dependency package names
        """
        self._dependency_graph[package] = dependencies
    
    def validate_dependencies(self) -> List[Dict[str, Any]]:
        """Validate dependencies for circular dependencies.
        
        Returns:
            List of validation errors
        """
        errors: List[Dict[str, Any]] = []
        
        # Check for circular dependencies
        visited: set[str] = set()
        recursion_stack: set[str] = set()
        
        def check_circular(package: str) -> bool:
            """Check for circular dependencies."""
            if package in recursion_stack:
                return True
            
            if package in visited:
                return False
            
            visited.add(package)
            recursion_stack.add(package)
            
            # Check dependencies
            deps = self._dependency_graph.get(package, [])
            for dep in deps:
                if check_circular(dep):
                    return True
            
            recursion_stack.remove(package)
            return False
        
        # Check all packages
        for package in self._dependency_graph:
            visited.clear()
            recursion_stack.clear()
            
            if check_circular(package):
                errors.append({
                    "package": package,
                    "type": "circular_dependency",
                    "description": f"Circular dependency detected for package {package}"
                })
        
        return errors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get package manager statistics.
        
        Returns:
            Dictionary with statistics about package managers
        """
        stats: Dict[str, Any] = {
            "total_managers": len(self._managers),
            "active_manager": self._active_manager.get_name() if self._active_manager else None,
            "available_managers": list(self._managers.keys()),
            "total_dependencies": len(self._dependency_graph),
            "conflicts": len(self.detect_conflicts()),
        }
        
        # Add manager-specific statistics
        for manager_name, manager in self._managers.items():
            manager_stats: Dict[str, Any] = {
                "name": manager_name,
                "available": manager.is_available(),
                "initialized": manager.is_initialized(),
            }
            
            # Add version if available
            if hasattr(manager, "_version"):
                manager_stats["version"] = manager._version  # type: ignore[attr-defined]
            
            stats[f"manager_{manager_name}"] = manager_stats
        
        return stats
    
    def switch_manager(self, manager_type: str) -> bool:
        """Switch to different package manager.
        
        Args:
            manager_type: Package manager type to switch to
            
        Returns:
            True if switch succeeded, False otherwise
        """
        # Get manager
        manager = self.get_manager(manager_type)
        
        if manager is None:
            if self.logger:
                self.logger.error(f"Package manager not available: {manager_type}")
            return False
        
        if not manager.is_available():
            if self.logger:
                self.logger.error(f"Package manager not available: {manager_type}")
            return False
        
        # Switch manager
        old_manager = self._active_manager
        self._active_manager = manager
        
        if self.logger:
            old_name = old_manager.get_name() if old_manager else "None"
            new_name = manager.get_name()
            self.logger.info(f"Switched package manager: {old_name} -> {new_name}")
        
        return True
    
    def _get_manager_for_install(self, manager_type: Optional[str]) -> Optional[PackageManagerBase]:
        """Get package manager for installation.
        
        Args:
            manager_type: Package manager type or None for active
            
        Returns:
            Package manager instance or None if not available
        """
        if manager_type is None:
            return self._active_manager
        
        return self.get_manager(manager_type)
    
    def _add_to_dependency_graph(self, package: str, manager_name: str) -> None:
        """Add package to dependency graph.
        
        Args:
            package: Package name
            manager_name: Package manager that manages the package
        """
        if package not in self._dependency_graph:
            self._dependency_graph[package] = []
    
    def __repr__(self) -> str:
        """String representation of package manager manager.
        
        Returns:
            String representation
        """
        active_name = self._active_manager.get_name() if self._active_manager else "None"
        return f"PackageManagerManager(active='{active_name}', total_managers={len(self._managers)})"
