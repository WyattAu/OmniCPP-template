"""
Base compiler interface for all compiler implementations
"""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass


@dataclass
class CompilerInfo:
    """Compiler information dataclass
    
    Attributes:
        name: Compiler name (e.g., "MSVC", "GCC", "Clang")
        version: Compiler version string
        path: Path to compiler executable
        target: Target platform (e.g., "windows", "linux")
        flags: List of compiler flags
    """
    name: str
    version: str
    path: str
    target: str
    flags: list[str]


class CompilerBase(ABC):
    """Abstract base class for compiler interfaces
    
    All compiler implementations must inherit from this class and implement
    the abstract methods defined below.
    """
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize compiler
        
        Args:
            version: Compiler version (auto-detect if None)
        """
        self._version: str | None = version
        self._detected_version: str | None = None
        self._compiler_path: str | None = None
    
    @abstractmethod
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get compiler version
        
        Returns:
            Compiler version string
        """
        pass
    
    @abstractmethod
    def get_flags(self, build_type: str) -> list[str]:
        """Get compiler flags
        
        Args:
            build_type: Build type (Debug, Release, RelWithDebInfo, MinSizeRel)
            
        Returns:
            List of compiler flags
        """
        pass
    
    @abstractmethod
    def setup_environment(self) -> dict[str, str]:
        """Set up compiler environment
        
        Returns:
            Dictionary of environment variables
        """
        pass
    
    def detect(self) -> bool:
        """Detect if compiler is available
        
        Returns:
            True if compiler is detected, False otherwise
        """
        return self._detect_compiler()
    
    def get_info(self) -> CompilerInfo | None:
        """Get compiler information
        
        Returns:
            CompilerInfo if detected, None otherwise
        """
        if not self.detect():
            return None
        
        return CompilerInfo(
            name=self.get_name(),
            version=self.get_version(),
            path=self._compiler_path or "",
            target=self._get_target_platform(),
            flags=self.get_flags("Release")
        )
    
    @abstractmethod
    def _detect_compiler(self) -> bool:
        """Internal method to detect compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        pass
    
    def _get_target_platform(self) -> str:
        """Get target platform for this compiler
        
        Returns:
            Target platform string
        """
        import platform
        return platform.system().lower()
    
    def _run_command(self, command: list[str]) -> tuple[int, str, str]:
        """Run a command and return result
        
        Args:
            command: Command to execute as list of strings
            
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        import subprocess
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return -1, "", ""
