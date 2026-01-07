"""
Unified version detection for all compiler types
"""

import logging
import re
import subprocess
from dataclasses import dataclass
from typing import Optional, Tuple, Union, List


@dataclass
class VersionInfo:
    """Compiler version information
    
    Attributes:
        major: Major version number
        minor: Minor version number
        patch: Patch version number
        build: Build number or identifier (optional)
        full_version: Full version string
    """
    major: int
    minor: int
    patch: int
    build: Optional[str] = None
    full_version: str = ""
    
    def __str__(self) -> str:
        """Convert version to string representation
        
        Returns:
            Version string
        """
        if self.build:
            return f"{self.major}.{self.minor}.{self.patch}.{self.build}"
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __lt__(self, other: 'VersionInfo') -> bool:
        """Compare versions for less than
        
        Args:
            other: Other version to compare
            
        Returns:
            True if this version is less than other
        """
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        return False
    
    def __le__(self, other: 'VersionInfo') -> bool:
        """Compare versions for less than or equal
        
        Args:
            other: Other version to compare
            
        Returns:
            True if this version is less than or equal to other
        """
        return self < other or self == other
    
    def __gt__(self, other: 'VersionInfo') -> bool:
        """Compare versions for greater than
        
        Args:
            other: Other version to compare
            
        Returns:
            True if this version is greater than other
        """
        return not self <= other
    
    def __ge__(self, other: 'VersionInfo') -> bool:
        """Compare versions for greater than or equal
        
        Args:
            other: Other version to compare
            
        Returns:
            True if this version is greater than or equal to other
        """
        return not self < other
    
    def __eq__(self, other: object) -> bool:
        """Compare versions for equality
        
        Args:
            other: Other version to compare
            
        Returns:
            True if versions are equal
        """
        if not isinstance(other, VersionInfo):
            return False
        return (self.major == other.major and 
                self.minor == other.minor and 
                self.patch == other.patch)
    
    def __ne__(self, other: object) -> bool:
        """Compare versions for inequality
        
        Args:
            other: Other version to compare
            
        Returns:
            True if versions are not equal
        """
        return not self == other


class VersionDetector:
    """Unified version detector for all compiler types
    
    This class provides a unified interface for detecting, parsing, comparing,
    and validating compiler versions across all supported compiler types.
    """
    
    # Compiler type constants
    COMPILER_MSVC = "msvc"
    COMPILER_MSVC_CLANG = "msvc_clang"
    COMPILER_MINGW_GCC = "mingw_gcc"
    COMPILER_MINGW_CLANG = "mingw_clang"
    COMPILER_GCC = "gcc"
    COMPILER_CLANG = "clang"
    
    # Version detection patterns for each compiler type
    VERSION_PATTERNS = {
        COMPILER_MSVC: [
            r"Version\s+(\d+\.\d+\.\d+\.\d+)",
            r"Version\s+(\d+\.\d+)",
            r"(\d{2}\.\d+\.\d+)"  # MSVC 19.x.x.x format
        ],
        COMPILER_MSVC_CLANG: [
            r"clang version (\d+\.\d+\.\d+)",
            r"LLVM version (\d+\.\d+\.\d+)"
        ],
        COMPILER_MINGW_GCC: [
            r"g\+\+.*?(\d+\.\d+\.\d+)",
            r"gcc.*?(\d+\.\d+\.\d+)"
        ],
        COMPILER_MINGW_CLANG: [
            r"clang version (\d+\.\d+\.\d+)",
            r"LLVM version (\d+\.\d+\.\d+)"
        ],
        COMPILER_GCC: [
            r"g\+\+.*?(\d+\.\d+\.\d+)",
            r"gcc.*?(\d+\.\d+\.\d+)"
        ],
        COMPILER_CLANG: [
            r"clang version (\d+\.\d+\.\d+)",
            r"LLVM version (\d+\.\d+\.\d+)"
        ]
    }
    
    # Version flags for each compiler type
    VERSION_FLAGS: dict[str, List[str]] = {
        COMPILER_MSVC: [],
        COMPILER_MSVC_CLANG: ["--version"],
        COMPILER_MINGW_GCC: ["--version"],
        COMPILER_MINGW_CLANG: ["--version"],
        COMPILER_GCC: ["--version"],
        COMPILER_CLANG: ["--version"]
    }
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """Initialize version detector
        
        Args:
            logger: Logger instance (optional)
        """
        self._logger = logger or logging.getLogger(__name__)
    
    def detect_version(self, compiler_path: str, compiler_type: str) -> Optional[VersionInfo]:
        """Detect compiler version by executing the compiler
        
        Args:
            compiler_path: Path to compiler executable
            compiler_type: Type of compiler (msvc, msvc_clang, mingw_gcc, etc.)
            
        Returns:
            VersionInfo if detected, None otherwise
        """
        self._logger.debug(f"Detecting version for {compiler_type} at {compiler_path}")
        
        # Validate compiler type
        if compiler_type not in self.VERSION_PATTERNS:
            self._logger.error(f"Unknown compiler type: {compiler_type}")
            return None
        
        # Get version flags for this compiler
        version_flags: List[str] = self.VERSION_FLAGS.get(compiler_type, [])
        
        # Execute compiler to get version
        try:
            command: List[str] = [compiler_path] + version_flags
            self._logger.debug(f"Executing command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout + result.stderr
            self._logger.debug(f"Compiler output: {output[:200]}...")
            
            # Parse version from output
            version_info = self._parse_version_from_output(
                output, 
                compiler_type
            )
            
            if version_info:
                version_info.full_version = output.strip()
                self._logger.info(
                    f"Detected {compiler_type} version: {version_info}"
                )
                return version_info
            
            self._logger.warning(
                f"Failed to parse version from {compiler_type} output"
            )
            return None
            
        except subprocess.TimeoutExpired:
            self._logger.error(
                f"Timeout while detecting version for {compiler_type}"
            )
            return None
        except FileNotFoundError:
            self._logger.error(
                f"Compiler executable not found: {compiler_path}"
            )
            return None
        except Exception as e:
            self._logger.error(
                f"Error detecting version for {compiler_type}: {e}"
            )
            return None
    
    def parse_version(self, version_string: str) -> Optional[VersionInfo]:
        """Parse version string into VersionInfo
        
        Args:
            version_string: Version string to parse (e.g., "19.40.33807", "13.2.0")
            
        Returns:
            VersionInfo if parsing succeeds, None otherwise
        """
        self._logger.debug(f"Parsing version string: {version_string}")
        
        if not version_string:
            self._logger.error("Empty version string")
            return None
        
        # Try different version formats
        # Format 1: major.minor.patch.build (e.g., "19.40.33807.0")
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$", version_string)
        if match:
            major, minor, patch, build = match.groups()
            version_info = VersionInfo(
                major=int(major),
                minor=int(minor),
                patch=int(patch),
                build=build
            )
            self._logger.debug(f"Parsed version (format 1): {version_info}")
            return version_info
        
        # Format 2: major.minor.patch (e.g., "13.2.0")
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_string)
        if match:
            major, minor, patch = match.groups()
            version_info = VersionInfo(
                major=int(major),
                minor=int(minor),
                patch=int(patch)
            )
            self._logger.debug(f"Parsed version (format 2): {version_info}")
            return version_info
        
        # Format 3: major.minor (e.g., "19.40")
        match = re.match(r"^(\d+)\.(\d+)$", version_string)
        if match:
            major, minor = match.groups()
            version_info = VersionInfo(
                major=int(major),
                minor=int(minor),
                patch=0
            )
            self._logger.debug(f"Parsed version (format 3): {version_info}")
            return version_info
        
        # Format 4: major (e.g., "19")
        match = re.match(r"^(\d+)$", version_string)
        if match:
            major = match.group(1)
            version_info = VersionInfo(
                major=int(major),
                minor=0,
                patch=0
            )
            self._logger.debug(f"Parsed version (format 4): {version_info}")
            return version_info
        
        self._logger.error(f"Failed to parse version string: {version_string}")
        return None
    
    def compare_versions(
        self,
        version1: Union[VersionInfo, str],
        version2: Union[VersionInfo, str]
    ) -> int:
        """Compare two versions
        
        Args:
            version1: First version (VersionInfo or string)
            version2: Second version (VersionInfo or string)
            
        Returns:
            -1 if version1 < version2
             0 if version1 == version2
             1 if version1 > version2
        """
        # Convert strings to VersionInfo if needed
        if isinstance(version1, str):
            parsed1 = self.parse_version(version1)
            if not parsed1:
                self._logger.error(f"Failed to parse version1: {version1}")
                raise ValueError(f"Invalid version string: {version1}")
            version1 = parsed1
        
        if isinstance(version2, str):
            parsed2 = self.parse_version(version2)
            if not parsed2:
                self._logger.error(f"Failed to parse version2: {version2}")
                raise ValueError(f"Invalid version string: {version2}")
            version2 = parsed2
        
        # Compare versions
        if version1 < version2:
            return -1
        elif version1 > version2:
            return 1
        else:
            return 0
    
    def get_version_string(self, version: VersionInfo) -> str:
        """Get version string from VersionInfo
        
        Args:
            version: VersionInfo object
            
        Returns:
            Version string
        """
        return str(version)
    
    def validate_version(self, version: Union[VersionInfo, str]) -> Tuple[bool, list[str]]:
        """Validate version format and values
        
        Args:
            version: Version to validate (VersionInfo or string)
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors: list[str] = []
        
        # Convert string to VersionInfo if needed
        if isinstance(version, str):
            parsed = self.parse_version(version)
            if not parsed:
                errors.append(f"Invalid version string format: {version}")
                return False, errors
            version = parsed
        
        # Validate version components
        if version.major < 0:
            errors.append(f"Major version cannot be negative: {version.major}")
        
        if version.minor < 0:
            errors.append(f"Minor version cannot be negative: {version.minor}")
        
        if version.patch < 0:
            errors.append(f"Patch version cannot be negative: {version.patch}")
        
        # Validate build string if present
        if version.build is not None:
            if not version.build:
                errors.append("Build string cannot be empty")
        
        # Check for reasonable version ranges
        # Note: MSVC uses large patch numbers (e.g., 33807), so we allow larger values
        if version.major > 100:
            errors.append(f"Major version seems too large: {version.major}")
        
        if version.minor > 100:
            errors.append(f"Minor version seems too large: {version.minor}")
        
        # Allow larger patch numbers for MSVC (can be 5 digits)
        if version.patch > 100000:
            errors.append(f"Patch version seems too large: {version.patch}")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            self._logger.debug(f"Version validation passed: {version}")
        else:
            self._logger.warning(
                f"Version validation failed for {version}: {errors}"
            )
        
        return is_valid, errors
    
    def _parse_version_from_output(
        self, 
        output: str, 
        compiler_type: str
    ) -> Optional[VersionInfo]:
        """Parse version from compiler output
        
        Args:
            output: Compiler output text
            compiler_type: Type of compiler
            
        Returns:
            VersionInfo if parsing succeeds, None otherwise
        """
        patterns = self.VERSION_PATTERNS.get(compiler_type, [])
        
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                version_string = match.group(1)
                version_info = self.parse_version(version_string)
                if version_info:
                    return version_info
        
        return None
    
    def get_minimum_required_version(self, compiler_type: str) -> Optional[VersionInfo]:
        """Get minimum required version for a compiler type
        
        Args:
            compiler_type: Type of compiler
            
        Returns:
            Minimum required version or None if not specified
        """
        minimum_versions = {
            self.COMPILER_MSVC: VersionInfo(19, 30, 0),
            self.COMPILER_MSVC_CLANG: VersionInfo(16, 0, 0),
            self.COMPILER_MINGW_GCC: VersionInfo(12, 0, 0),
            self.COMPILER_MINGW_CLANG: VersionInfo(16, 0, 0),
            self.COMPILER_GCC: VersionInfo(11, 0, 0),
            self.COMPILER_CLANG: VersionInfo(16, 0, 0)
        }
        
        return minimum_versions.get(compiler_type)
    
    def is_version_supported(
        self, 
        version: VersionInfo, 
        compiler_type: str
    ) -> bool:
        """Check if version meets minimum requirements
        
        Args:
            version: Version to check
            compiler_type: Type of compiler
            
        Returns:
            True if version is supported, False otherwise
        """
        minimum_version = self.get_minimum_required_version(compiler_type)
        
        if not minimum_version:
            self._logger.warning(
                f"No minimum version specified for {compiler_type}"
            )
            return True
        
        comparison = self.compare_versions(version, minimum_version)
        is_supported = comparison >= 0
        
        if is_supported:
            self._logger.debug(
                f"Version {version} meets minimum requirement for {compiler_type}"
            )
        else:
            self._logger.warning(
                f"Version {version} does not meet minimum requirement "
                f"for {compiler_type} (minimum: {minimum_version})"
            )
        
        return is_supported
