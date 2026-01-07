"""
Compiler Manager for coordinating compiler detection and validation

This module provides a high-level manager for coordinating compiler detection,
validation, and selection operations through the CompilerFactory.
"""

import logging
from typing import Dict, List, Optional

from .compiler_factory import CompilerFactory, CompilerRequirements
from .msvc_detector import (
    CompilerInfo,
    Architecture,
    ValidationResult
)


class CompilerManager:
    """Manager for compiler detection and selection
    
    This manager coordinates compiler detection, validation, and provides
    convenient access to detected compilers through the CompilerFactory.
    
    Attributes:
        _factory: CompilerFactory instance for creating and managing compilers
        _detected_compilers: Cache of detected compilers by type
        _logger: Logger instance for logging manager operations
    """

    def __init__(self, factory: CompilerFactory, logger: Optional[logging.Logger] = None):
        """Initialize compiler manager
        
        Args:
            factory: CompilerFactory instance for compiler operations
            logger: Logger instance for logging (optional)
        """
        self._factory = factory
        self._detected_compilers: Dict[str, List[CompilerInfo]] = {}
        self._logger = logger or logging.getLogger(__name__)
        self._logger.debug("CompilerManager initialized")

    def detect_all(self) -> Dict[str, List[CompilerInfo]]:
        """Detect all compilers on the system
        
        Uses the factory to detect all available compilers and caches
        the results for subsequent access.
        
        Returns:
            Dictionary mapping compiler types to lists of CompilerInfo
            
        Raises:
            Exception: If detection fails for any compiler type
        """
        self._logger.info("Starting detection of all compilers")
        
        try:
            self._detected_compilers = self._factory.get_available_compilers()
            
            total_compilers = sum(len(compilers) for compilers in self._detected_compilers.values())
            self._logger.info(
                f"Detection complete: found {total_compilers} compilers "
                f"across {len(self._detected_compilers)} types"
            )
            
            return self._detected_compilers
        except Exception as e:
            self._logger.error(f"Failed to detect all compilers: {e}")
            raise

    def detect_compiler(self, compiler_type: str) -> List[CompilerInfo]:
        """Detect compilers of a specific type
        
        Args:
            compiler_type: Type of compiler to detect (e.g., "msvc", "mingw_gcc")
            
        Returns:
            List of detected CompilerInfo for the specified type
            
        Raises:
            ValueError: If compiler_type is invalid
            Exception: If detection fails
        """
        self._logger.debug(f"Detecting compilers of type: {compiler_type}")
        
        if not compiler_type:
            raise ValueError("Compiler type cannot be empty")
        
        try:
            # Get all compilers and filter by type
            compilers = self._factory.get_available_compilers()
            if compiler_type not in compilers:
                self._logger.warning(f"No detector found for compiler type: {compiler_type}")
                return []
            
            # Cache the result
            self._detected_compilers[compiler_type] = compilers[compiler_type]
            
            self._logger.info(
                f"Detected {len(compilers[compiler_type])} compilers of type: {compiler_type}"
            )
            
            return compilers[compiler_type]
        except Exception as e:
            self._logger.error(f"Failed to detect compiler type {compiler_type}: {e}")
            raise

    def validate_compiler(self, compiler_info: CompilerInfo) -> ValidationResult:
        """Validate a compiler installation
        
        Validates that the compiler executable exists and is functional.
        
        Args:
            compiler_info: Compiler information to validate
            
        Returns:
            ValidationResult with validation status, errors, and warnings
        """
        self._logger.debug(
            f"Validating compiler: {compiler_info.compiler_type.value} "
            f"{compiler_info.architecture.value}"
        )
        
        # Get all compilers and find the detector
        all_compilers = self._factory.get_available_compilers()
        compiler_type_str = compiler_info.compiler_type.value
        
        if compiler_type_str not in all_compilers:
            error_msg = f"No detector found for {compiler_type_str}"
            self._logger.error(error_msg)
            return ValidationResult(
                is_valid=False,
                errors=[error_msg],
                warnings=[]
            )
        
        # Find matching compiler and validate it
        matching_compilers = [
            c for c in all_compilers[compiler_type_str]
            if c.path == compiler_info.path
        ]
        
        if not matching_compilers:
            error_msg = f"Compiler not found in detected compilers: {compiler_info.path}"
            self._logger.error(error_msg)
            return ValidationResult(
                is_valid=False,
                errors=[error_msg],
                warnings=[]
            )
        
        # For now, return a basic validation result
        # In a full implementation, we would call the detector's validate method
        try:
            # Check if compiler executable exists
            import os
            is_valid = os.path.exists(compiler_info.path)
            
            result = ValidationResult(
                is_valid=is_valid,
                errors=[] if is_valid else [f"Compiler executable not found: {compiler_info.path}"],
                warnings=[]
            )
            
            if result.is_valid:
                self._logger.info(
                    f"Compiler validation passed: "
                    f"{compiler_info.compiler_type.value} {compiler_info.architecture.value}"
                )
            else:
                self._logger.warning(
                    f"Compiler validation failed: "
                    f"{compiler_info.compiler_type.value} {compiler_info.architecture.value}"
                )
                for error in result.errors:
                    self._logger.warning(f"  Error: {error}")
                for warning in result.warnings:
                    self._logger.warning(f"  Warning: {warning}")
            
            return result
        except Exception as e:
            error_msg = f"Validation failed with exception: {str(e)}"
            self._logger.error(error_msg)
            return ValidationResult(
                is_valid=False,
                errors=[error_msg],
                warnings=[]
            )

    def get_compiler(
        self,
        compiler_type: str,
        architecture: str = "x64"
    ) -> Optional[CompilerInfo]:
        """Get a specific compiler
        
        Retrieves the best matching compiler for the specified type
        and architecture, using cache if available.
        
        Args:
            compiler_type: Type of compiler (e.g., "msvc", "mingw_gcc")
            architecture: Target architecture (default: "x64")
            
        Returns:
            CompilerInfo if found, None otherwise
        """
        self._logger.debug(f"Getting compiler: {compiler_type} {architecture}")
        
        try:
            compiler = self._factory.create_compiler(compiler_type, architecture)
            
            if compiler:
                self._logger.info(
                    f"Retrieved compiler: {compiler_type} {architecture} "
                    f"version {compiler.version}"
                )
            else:
                self._logger.warning(
                    f"Compiler not found: {compiler_type} {architecture}"
                )
            
            return compiler
        except Exception as e:
            self._logger.error(f"Failed to get compiler {compiler_type} {architecture}: {e}")
            return None

    def get_all_compilers(self) -> Dict[str, List[CompilerInfo]]:
        """Get all detected compilers
        
        Returns the cached list of all detected compilers.
        If no detection has been performed, triggers detection.
        
        Returns:
            Dictionary mapping compiler types to lists of CompilerInfo
        """
        self._logger.debug("Getting all detected compilers")
        
        if not self._detected_compilers:
            self._logger.info("No cached compilers, triggering detection")
            return self.detect_all()
        
        total_compilers = sum(len(compilers) for compilers in self._detected_compilers.values())
        self._logger.debug(
            f"Returning {total_compilers} compilers from cache"
        )
        
        return self._detected_compilers

    def get_recommended_compiler(
        self,
        architecture: str = "x64",
        cpp_standard: Optional[str] = None
    ) -> Optional[CompilerInfo]:
        """Get the recommended compiler for the system
        
        Selects the best compiler based on platform, architecture,
        and C++ standard requirements.
        
        Args:
            architecture: Target architecture (default: "x64")
            cpp_standard: Required C++ standard (optional)
            
        Returns:
            Recommended CompilerInfo or None if no suitable compiler found
        """
        self._logger.info(
            f"Getting recommended compiler for architecture: {architecture}"
        )
        
        # Build requirements
        required_capabilities: List[str] = []
        if cpp_standard:
            required_capabilities.append(cpp_standard.lower())
        
        requirements = CompilerRequirements(
            architecture=Architecture(architecture) if architecture else None,
            required_capabilities=required_capabilities if required_capabilities else None
        )
        
        try:
            compiler = self._factory.select_best_compiler(requirements)
            
            if compiler:
                self._logger.info(
                    f"Recommended compiler: {compiler.compiler_type.value} "
                    f"{compiler.architecture.value} version {compiler.version}"
                )
            else:
                self._logger.warning(
                    f"No suitable compiler found for architecture: {architecture}"
                )
            
            return compiler
        except Exception as e:
            self._logger.error(f"Failed to get recommended compiler: {e}")
            return None

    def get_compilers_by_type(self, compiler_type: str) -> List[CompilerInfo]:
        """Get all compilers of a specific type
        
        Args:
            compiler_type: Type of compiler (e.g., "msvc", "mingw_gcc")
            
        Returns:
            List of CompilerInfo for the specified type
        """
        self._logger.debug(f"Getting compilers by type: {compiler_type}")
        
        # Check cache first
        if compiler_type in self._detected_compilers:
            compilers = self._detected_compilers[compiler_type]
            self._logger.debug(
                f"Found {len(compilers)} compilers of type {compiler_type} in cache"
            )
            return compilers
        
        # Detect if not in cache
        self._logger.info(
            f"Compilers of type {compiler_type} not in cache, detecting"
        )
        return self.detect_compiler(compiler_type)

    def get_compilers_by_architecture(self, architecture: str) -> List[CompilerInfo]:
        """Get all compilers for a specific architecture
        
        Args:
            architecture: Target architecture (e.g., "x64", "x86", "arm64")
            
        Returns:
            List of CompilerInfo for the specified architecture
        """
        self._logger.debug(f"Getting compilers by architecture: {architecture}")
        
        # Ensure we have detected compilers
        if not self._detected_compilers:
            self.detect_all()
        
        try:
            arch_enum = Architecture(architecture)
        except ValueError:
            self._logger.error(f"Invalid architecture: {architecture}")
            return []
        
        # Filter all compilers by architecture
        matching_compilers: List[CompilerInfo] = []
        for compilers in self._detected_compilers.values():
            matching_compilers.extend(
                [c for c in compilers if c.architecture == arch_enum]
            )
        
        self._logger.info(
            f"Found {len(matching_compilers)} compilers for architecture: {architecture}"
        )
        
        return matching_compilers

    def get_compilers_by_capability(
        self,
        capability: str,
        value: bool = True
    ) -> List[CompilerInfo]:
        """Get compilers with a specific capability
        
        Args:
            capability: Capability name (e.g., "cpp23", "modules", "coroutines")
            value: Required capability value (default: True)
            
        Returns:
            List of CompilerInfo with the specified capability
        """
        self._logger.debug(
            f"Getting compilers with capability: {capability}={value}"
        )
        
        # Ensure we have detected compilers
        if not self._detected_compilers:
            self.detect_all()
        
        # Filter compilers by capability
        matching_compilers: List[CompilerInfo] = []
        for compilers in self._detected_compilers.values():
            for compiler in compilers:
                caps = compiler.capabilities.to_dict()
                if caps.get(capability, False) == value:
                    matching_compilers.append(compiler)
        
        self._logger.info(
            f"Found {len(matching_compilers)} compilers with "
            f"capability {capability}={value}"
        )
        
        return matching_compilers

    def refresh_detection(self) -> Dict[str, List[CompilerInfo]]:
        """Refresh compiler detection
        
        Clears the factory cache and re-detects all compilers.
        Use this when the system configuration may have changed.
        
        Returns:
            Dictionary mapping compiler types to lists of CompilerInfo
        """
        self._logger.info("Refreshing compiler detection")
        
        # Clear factory cache
        self._factory.clear_cache()
        
        # Clear local cache
        old_cache_size = sum(len(compilers) for compilers in self._detected_compilers.values())
        self._detected_compilers.clear()
        self._logger.debug(f"Cleared local cache ({old_cache_size} entries)")
        
        # Re-detect
        return self.detect_all()
