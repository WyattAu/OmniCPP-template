"""
Base package manager interface

This module provides the abstract base class for all package managers,
defining the common interface that all package managers must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PackageInfo:
    """Package information data class.
    
    Attributes:
        name: Package name
        version: Package version
        description: Package description
        location: Package installation location
        dependencies: List of package dependencies
    """
    name: str
    version: str
    description: str = ""
    location: str = ""
    dependencies: Optional[list[str]] = None
    
    def __post_init__(self) -> None:
        """Initialize default values for optional fields."""
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class ExecutionResult:
    """Command execution result data class.
    
    Attributes:
        exit_code: Process exit code
        stdout: Standard output
        stderr: Standard error
        success: Whether execution succeeded
    """
    exit_code: int
    stdout: str
    stderr: str
    success: bool
    
    def __post_init__(self) -> None:
        """Calculate success based on exit code."""
        self.success = self.exit_code == 0


class PackageManagerBase(ABC):
    """Abstract base class for package managers.
    
    This class defines the interface that all package managers must implement.
    It provides common functionality and enforces a consistent API across
    different package managers.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize package manager.
        
        Args:
            config: Configuration dictionary containing package manager settings
        """
        self.config: Dict[str, Any] = config
        self._executable_path: Optional[str] = None
        self._is_initialized: bool = False
    
    @abstractmethod
    def get_name(self) -> str:
        """Get package manager name.
        
        Returns:
            Package manager name (e.g., "conan", "vcpkg", "cpm")
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if package manager is available.
        
        Returns:
            True if package manager is installed and available, False otherwise
        """
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize package manager.
        
        This method should perform any necessary setup, such as:
        - Detecting the package manager executable
        - Setting up paths
        - Validating configuration
        
        Raises:
            DependencyError: If package manager is not available
        """
        pass
    
    @abstractmethod
    def install_package(self, package: str, version: Optional[str] = None) -> bool:
        """Install package.
        
        Args:
            package: Package name
            version: Package version (latest if None)
            
        Returns:
            True if installation succeeded, False otherwise
        """
        pass
    
    @abstractmethod
    def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """Get package information.
        
        Args:
            package: Package name
            
        Returns:
            Package information or None if package not found
        """
        pass
    
    def get_executable_path(self) -> Optional[str]:
        """Get package manager executable path.
        
        Returns:
            Path to package manager executable or None if not found
        """
        return self._executable_path
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def is_initialized(self) -> bool:
        """Check if package manager is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self._is_initialized
    
    def _set_executable_path(self, path: str) -> None:
        """Set package manager executable path.
        
        Args:
            path: Path to executable
        """
        self._executable_path = path
    
    def _mark_initialized(self) -> None:
        """Mark package manager as initialized."""
        self._is_initialized = True
    
    def __repr__(self) -> str:
        """String representation of package manager.
        
        Returns:
            String representation
        """
        return f"{self.__class__.__name__}(name='{self.get_name()}', available={self.is_available()})"
