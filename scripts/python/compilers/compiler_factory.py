"""
Compiler Factory for creating and managing compiler instances

This module provides a factory pattern for creating compiler instances,
managing compiler detectors, and selecting the best compiler based on requirements.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .msvc_detector import (
    MSVCDetector,
    CompilerType,
    Architecture,
    CompilerInfo,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    ICompilerDetector
)
from .msvc_clang_detector import MSVCClangDetector
from .mingw_gcc_detector import MinGWDetector
from .mingw_clang_detector import MinGWClangDetector


@dataclass
class CompilerRequirements:
    """Compiler selection requirements
    
    Attributes:
        compiler_type: Type of compiler (optional)
        architecture: Target architecture (optional)
        cpp_standard: C++ standard requirement (optional)
        required_capabilities: List of required capabilities (optional)
        preferred_version: Preferred compiler version (optional)
    """
    compiler_type: Optional[CompilerType] = None
    architecture: Optional[Architecture] = None
    cpp_standard: Optional[str] = None
    required_capabilities: Optional[List[str]] = None
    preferred_version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert requirements to dictionary"""
        return {
            "compiler_type": self.compiler_type.value if self.compiler_type else None,
            "architecture": self.architecture.value if self.architecture else None,
            "cpp_standard": self.cpp_standard,
            "required_capabilities": self.required_capabilities,
            "preferred_version": self.preferred_version
        }


class CompilerFactory:
    """Factory for creating and managing compiler instances
    
    This factory manages compiler detectors, creates compiler instances,
    caches results for performance, and selects the best compiler
    based on requirements.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize compiler factory
        
        Args:
            logger: Logger instance for logging factory operations
        """
        self._logger = logger or logging.getLogger(__name__)
        self._detectors: Dict[str, ICompilerDetector] = {}
        self._cache: Dict[str, CompilerInfo] = {}
        self._logger.debug("CompilerFactory initialized")

    def register_detector(self, compiler_type: str, detector: ICompilerDetector) -> None:
        """Register a compiler detector
        
        Args:
            compiler_type: Type of compiler (e.g., "msvc", "mingw_gcc")
            detector: Detector instance implementing ICompilerDetector interface
            
        Raises:
            ValueError: If compiler_type is invalid or detector is None
        """
        if not compiler_type:
            raise ValueError("Compiler type cannot be empty")
        
        if detector is None:
            raise ValueError("Detector cannot be None")
        
        self._detectors[compiler_type] = detector
        self._logger.info(f"Registered detector for compiler type: {compiler_type}")

    def create_compiler(self, compiler_type: str, architecture: str) -> Optional[CompilerInfo]:
        """Create a compiler instance
        
        Detects compilers of the specified type and returns the best
        matching compiler for the given architecture.
        
        Args:
            compiler_type: Type of compiler (e.g., "msvc", "mingw_gcc")
            architecture: Target architecture (e.g., "x64", "x86")
            
        Returns:
            CompilerInfo if found, None otherwise
            
        Raises:
            ValueError: If compiler_type is invalid
        """
        self._logger.debug(f"Creating compiler: {compiler_type} {architecture}")
        
        # Check cache first
        cache_key = f"{compiler_type}_{architecture}"
        if cache_key in self._cache:
            self._logger.debug(f"Cache hit for: {cache_key}")
            return self._cache[cache_key]
        
        # Get detector
        detector = self._get_detector(compiler_type)
        if not detector:
            self._logger.error(f"No detector registered for compiler type: {compiler_type}")
            return None
        
        # Detect compilers
        compilers = detector.detect()
        if not compilers:
            self._logger.warning(f"No compilers detected for type: {compiler_type}")
            return None
        
        # Filter by architecture
        try:
            arch_enum = Architecture(architecture)
        except ValueError:
            self._logger.error(f"Invalid architecture: {architecture}")
            return None
        
        filtered = [c for c in compilers if c.architecture == arch_enum]
        
        if not filtered:
            self._logger.warning(
                f"No compilers found for {compiler_type} with architecture {architecture}"
            )
            return None
        
        # Select best compiler (highest version)
        best = max(filtered, key=lambda c: (c.version.major, c.version.minor, c.version.patch))
        
        # Cache the result
        self._cache[cache_key] = best
        self._logger.info(
            f"Created compiler: {compiler_type} {architecture} "
            f"version {best.version}"
        )
        
        return best

    def get_available_compilers(self) -> Dict[str, List[CompilerInfo]]:
        """Get all available compilers
        
        Returns a dictionary mapping compiler types to lists of
        detected compiler information.
        
        Returns:
            Dictionary mapping compiler types to lists of CompilerInfo
        """
        self._logger.debug("Getting all available compilers")
        
        result: Dict[str, List[CompilerInfo]] = {}
        
        for compiler_type, detector in self._detectors.items():
            try:
                compilers = detector.detect()
                result[compiler_type] = compilers
                self._logger.debug(
                    f"Found {len(compilers)} compilers for type: {compiler_type}"
                )
            except Exception as e:
                self._logger.error(
                    f"Error detecting compilers for type {compiler_type}: {e}"
                )
                result[compiler_type] = []
        
        return result

    def select_best_compiler(
        self,
        requirements: CompilerRequirements
    ) -> Optional[CompilerInfo]:
        """Select the best compiler based on requirements
        
        Filters and ranks compilers based on the specified requirements
        including compiler type, architecture, capabilities, and version.
        
        Args:
            requirements: Compiler selection requirements
            
        Returns:
            Best matching CompilerInfo or None if no match found
        """
        self._logger.debug(f"Selecting best compiler with requirements: {requirements.to_dict()}")
        
        # Get all compilers of the specified type
        if requirements.compiler_type:
            compiler_type_str = requirements.compiler_type.value
            detector = self._detectors.get(compiler_type_str)
            if not detector:
                self._logger.error(f"No detector for compiler type: {compiler_type_str}")
                return None
            
            all_compilers = detector.detect()
        else:
            # Get all compilers from all detectors
            all_compilers: List[CompilerInfo] = []
            for detector in self._detectors.values():
                try:
                    all_compilers.extend(detector.detect())
                except Exception as e:
                    self._logger.error(f"Error detecting compilers: {e}")
        
        if not all_compilers:
            self._logger.warning("No compilers available for selection")
            return None
        
        # Filter by architecture
        if requirements.architecture:
            all_compilers = [
                c for c in all_compilers
                if c.architecture == requirements.architecture
            ]
            self._logger.debug(
                f"After architecture filter: {len(all_compilers)} compilers"
            )
        
        # Filter by capabilities
        if requirements.required_capabilities:
            for compiler in all_compilers[:]:
                caps = compiler.capabilities.to_dict()
                if not all(caps.get(cap, False) for cap in requirements.required_capabilities):
                    all_compilers.remove(compiler)
            self._logger.debug(
                f"After capability filter: {len(all_compilers)} compilers"
            )
        
        # Filter by version
        if requirements.preferred_version:
            all_compilers = [
                c for c in all_compilers
                if str(c.version) == requirements.preferred_version
            ]
            self._logger.debug(
                f"After version filter: {len(all_compilers)} compilers"
            )
        
        # Return best match (highest version)
        if all_compilers:
            best = max(
                all_compilers,
                key=lambda c: (c.version.major, c.version.minor, c.version.patch)
            )
            self._logger.info(
                f"Selected best compiler: {best.compiler_type.value} "
                f"{best.architecture.value} version {best.version}"
            )
            return best
        
        self._logger.warning("No compiler matches requirements")
        return None

    def _get_detector(self, compiler_type: str) -> Optional[ICompilerDetector]:
        """Get detector for compiler type
        
        Args:
            compiler_type: Type of compiler
            
        Returns:
            Detector instance or None if not found
        """
        return self._detectors.get(compiler_type)

    def clear_cache(self) -> None:
        """Clear compiler cache
        
        Removes all cached compiler instances, forcing subsequent
        create_compiler() calls to re-detect compilers.
        """
        cache_size = len(self._cache)
        self._cache.clear()
        self._logger.info(f"Cleared compiler cache ({cache_size} entries)")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "size": len(self._cache),
            "keys": list(self._cache.keys()),
            "compilers": [
                {
                    "type": info.compiler_type.value,
                    "architecture": info.architecture.value,
                    "version": str(info.version)
                }
                for info in self._cache.values()
            ]
        }

    def initialize_default_detectors(self) -> None:
        """Initialize default compiler detectors
        
        Registers detectors for all supported compiler types:
        - MSVC
        - MSVC-Clang
        - MinGW-GCC
        - MinGW-Clang
        """
        self._logger.info("Initializing default compiler detectors")
        
        # Register MSVC detector
        self.register_detector("msvc", MSVCDetector(self._logger))
        
        # Register MSVC-Clang detector
        self.register_detector("msvc_clang", MSVCClangDetector(self._logger))
        
        # Register MinGW-GCC detector
        self.register_detector("mingw_gcc", MinGWDetector(self._logger))
        
        # Register MinGW-Clang detector
        self.register_detector("mingw_clang", MinGWClangDetector(self._logger))
        
        self._logger.info("Default compiler detectors initialized")
