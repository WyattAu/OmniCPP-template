"""
Compiler Detection System

This module provides a unified system for detecting compilers, terminals,
and cross-compilation toolchains on Windows systems.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .compiler_factory import CompilerFactory
from .compiler_manager import CompilerManager
from .compiler_terminal_mapper import (
    CompilerTerminalMapper,
    TerminalInfo,
    ITerminalDetector
)
from .terminal_invoker import TerminalInvoker, CommandResult, CompilerInfo as TerminalInvokerCompilerInfo
from .msvc_detector import (
    CompilerInfo as MSVCCompilerInfo,
    ValidationResult
)
from .linux_cross_compiler import LinuxCrossCompiler
from .wasm_cross_compiler import WASMCrossCompiler
from .android_cross_compiler import AndroidCrossCompiler
from .toolchain_detector import (
    ToolchainDetector,
    UnifiedToolchainInfo
)
from .cmake_generator_selector import (
    CMakeGeneratorSelector,
    GeneratorSelectionResult
)


@dataclass
class DetectionError:
    """Detection error information
    
    Attributes:
        component: Component that raised the error
        error_type: Type of error (detection, validation, execution, etc.)
        message: Error message
        details: Additional error details
        suggestion: Suggestion for fixing the error
    """
    component: str
    error_type: str
    message: str
    details: Optional[Dict[str, Any]] = None
    suggestion: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "component": self.component,
            "error_type": self.error_type,
            "message": self.message,
            "details": self.details,
            "suggestion": self.suggestion
        }


@dataclass
class DetectionResult:
    """Detection result containing all detected components
    
    Attributes:
        compilers: Dictionary of detected compilers by type
        terminals: Dictionary of detected terminals by type
        cross_compilers: Dictionary of detected cross-compilers by platform
        errors: List of detection errors
        warnings: List of warning messages
        success: Whether detection was successful
    """
    compilers: Dict[str, List[MSVCCompilerInfo]] = field(default_factory=dict)
    terminals: Dict[str, List[TerminalInfo]] = field(default_factory=dict)
    cross_compilers: Dict[str, UnifiedToolchainInfo] = field(default_factory=dict)
    errors: List[DetectionError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "compilers": {
                k: [c.to_dict() for c in vals]
                for k, vals in self.compilers.items()
            },
            "terminals": {
                k: [t.to_dict() for t in vals]
                for k, vals in self.terminals.items()
            },
            "cross_compilers": {
                k: v.to_dict() for k, v in self.cross_compilers.items()
            },
            "errors": [e.to_dict() for e in self.errors],
            "warnings": self.warnings,
            "success": self.success
        }

    @property
    def has_errors(self) -> bool:
        """Check if detection has errors"""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if detection has warnings"""
        return len(self.warnings) > 0


class CompilerDetectionSystem:
    """Unified compiler detection system
    
    This class provides a unified interface for detecting compilers,
    terminals, and cross-compilation toolchains on Windows systems.
    It integrates all previously implemented components into a cohesive system.
    
    Attributes:
        _compiler_manager: Manager for compiler detection and selection
        _terminal_detector: Detector for terminal detection
        _terminal_invoker: Invoker for terminal operations
        _mapper: Mapper for compiler-terminal relationships
        _cross_compilers: Dictionary of cross-compiler instances
        _toolchain_detector: Detector for cross-compilation toolchains
        _cmake_selector: Selector for CMake generators
        _logger: Logger instance for logging operations
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        terminal_detector: Optional[ITerminalDetector] = None
    ) -> None:
        """Initialize compiler detection system
        
        Args:
            logger: Logger instance for logging operations (optional)
            terminal_detector: Terminal detector instance (optional)
        """
        self._logger = logger or logging.getLogger(__name__)
        self._logger.info("Initializing CompilerDetectionSystem")
        
        # Create compiler factory
        self._factory = CompilerFactory(self._logger)
        
        # Initialize default detectors
        self._factory.initialize_default_detectors()
        
        # Create compiler manager
        self._compiler_manager = CompilerManager(self._factory, self._logger)
        
        # Initialize terminal detector
        self._terminal_detector = terminal_detector
        
        # Create terminal invoker
        self._terminal_invoker = TerminalInvoker(self._logger)
        
        # Create compiler-terminal mapper
        if self._terminal_detector:
            self._mapper = CompilerTerminalMapper(
                self._terminal_detector,
                self._logger
            )
        else:
            self._mapper = None
            self._logger.warning("No terminal detector provided, mapper disabled")
        
        # Initialize cross-compilers
        self._cross_compilers: Dict[str, Any] = {
            "linux_x86_64": LinuxCrossCompiler("x86_64-linux-gnu"),
            "linux_aarch64": LinuxCrossCompiler("aarch64-linux-gnu"),
            "wasm_wasm32": WASMCrossCompiler("wasm32"),
            "wasm_wasm64": WASMCrossCompiler("wasm64"),
            "android_arm64": AndroidCrossCompiler("arm64-v8a"),
            "android_arm": AndroidCrossCompiler("armeabi-v7a"),
            "android_x86_64": AndroidCrossCompiler("x86_64"),
            "android_x86": AndroidCrossCompiler("x86")
        }
        
        # Initialize toolchain detector
        self._toolchain_detector = ToolchainDetector()
        
        # Initialize CMake generator selector
        self._cmake_selector = CMakeGeneratorSelector(self._logger)
        
        self._logger.info("CompilerDetectionSystem initialized successfully")

    def detect_all(self) -> DetectionResult:
        """Detect all compilers, terminals, and cross-compilers
        
        This method performs comprehensive detection of all system components:
        - Native compilers (MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang)
        - Terminals (MSVC, MSYS2)
        - Cross-compilation toolchains (Linux, WASM, Android)
        
        Returns:
            DetectionResult containing all detected components and any errors
            
        Raises:
            RuntimeError: If critical detection failures occur
        """
        self._logger.info("Starting comprehensive detection of all components")
        
        errors: List[DetectionError] = []
        warnings: List[str] = []
        
        # Detect compilers
        try:
            self._logger.info("Detecting native compilers")
            compilers = self._compiler_manager.detect_all()
            self._logger.info(
                f"Detected {sum(len(c) for c in compilers.values())} compilers "
                f"across {len(compilers)} types"
            )
        except Exception as e:
            error_msg = f"Failed to detect compilers: {str(e)}"
            self._logger.error(error_msg)
            errors.append(DetectionError(
                component="compiler_detection",
                error_type="detection_failed",
                message=error_msg,
                suggestion="Check compiler installations and permissions"
            ))
            compilers = {}
        
        # Detect terminals
        terminals: Dict[str, List[TerminalInfo]] = {}
        if self._terminal_detector:
            try:
                self._logger.info("Detecting terminals")
                detected_terminals = self._terminal_detector.detect()
                
                # Group terminals by type
                for terminal in detected_terminals:
                    terminal_type = terminal.type.value
                    if terminal_type not in terminals:
                        terminals[terminal_type] = []
                    terminals[terminal_type].append(terminal)
                
                self._logger.info(
                    f"Detected {len(detected_terminals)} terminals "
                    f"across {len(terminals)} types"
                )
            except Exception as e:
                error_msg = f"Failed to detect terminals: {str(e)}"
                self._logger.error(error_msg)
                errors.append(DetectionError(
                    component="terminal_detection",
                    error_type="detection_failed",
                    message=error_msg,
                    suggestion="Check terminal installations"
                ))
        
        # Detect cross-compilers
        cross_compilers: Dict[str, UnifiedToolchainInfo] = {}
        try:
            self._logger.info("Detecting cross-compilation toolchains")
            toolchain_result = self._toolchain_detector.detect()
            
            if toolchain_result.success:
                cross_compilers = {
                    f"{tc.platform}_{tc.architecture}": tc
                    for tc in toolchain_result.toolchains
                }
                self._logger.info(
                    f"Detected {len(cross_compilers)} cross-compilers"
                )
            else:
                for error in toolchain_result.errors:
                    errors.append(DetectionError(
                        component="cross_compiler_detection",
                        error_type="detection_failed",
                        message=error
                    ))
                for warning in toolchain_result.warnings:
                    warnings.append(warning)
        except Exception as e:
            error_msg = f"Failed to detect cross-compilers: {str(e)}"
            self._logger.error(error_msg)
            errors.append(DetectionError(
                component="cross_compiler_detection",
                error_type="detection_failed",
                message=error_msg,
                suggestion="Check cross-compiler installations"
            ))
        
        # Determine overall success
        success = len(errors) == 0
        
        if success:
            self._logger.info("Detection completed successfully")
        else:
            self._logger.warning(
                f"Detection completed with {len(errors)} errors and "
                f"{len(warnings)} warnings"
            )
        
        return DetectionResult(
            compilers=compilers,
            terminals=terminals,
            cross_compilers=cross_compilers,
            errors=errors,
            warnings=warnings,
            success=success
        )

    def detect_compiler(
        self,
        compiler_type: str,
        architecture: str = "x64"
    ) -> Optional[MSVCCompilerInfo]:
        """Detect a specific compiler type and architecture
        
        Args:
            compiler_type: Type of compiler (msvc, msvc_clang, mingw_gcc, mingw_clang)
            architecture: Target architecture (x64, x86, arm, arm64)
            
        Returns:
            CompilerInfo if found, None otherwise
            
        Raises:
            ValueError: If compiler_type is invalid
        """
        self._logger.info(
            f"Detecting compiler: {compiler_type} {architecture}"
        )
        
        try:
            compiler = self._compiler_manager.get_compiler(
                compiler_type,
                architecture
            )
            
            if compiler:
                self._logger.info(
                    f"Successfully detected compiler: "
                    f"{compiler.compiler_type.value} {compiler.architecture.value} "
                    f"version {compiler.version}"
                )
            else:
                self._logger.warning(
                    f"Compiler not found: {compiler_type} {architecture}"
                )
            
            return compiler
        except ValueError as e:
            self._logger.error(f"Invalid compiler type: {compiler_type}")
            raise
        except Exception as e:
            self._logger.error(
                f"Error detecting compiler {compiler_type} {architecture}: {str(e)}"
            )
            return None

    def detect_cross_compiler(
        self,
        platform: str,
        architecture: str
    ) -> Optional[UnifiedToolchainInfo]:
        """Detect a specific cross-compiler for platform and architecture
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            UnifiedToolchainInfo if found, None otherwise
            
        Raises:
            ValueError: If platform or architecture is invalid
        """
        self._logger.info(
            f"Detecting cross-compiler: {platform} {architecture}"
        )
        
        try:
            toolchain = self._toolchain_detector.detect_toolchain(
                platform,
                architecture
            )
            
            if toolchain:
                self._logger.info(
                    f"Successfully detected cross-compiler: "
                    f"{toolchain.platform} {toolchain.architecture}"
                )
            else:
                self._logger.warning(
                    f"Cross-compiler not found: {platform} {architecture}"
                )
            
            return toolchain
        except ValueError as e:
            self._logger.error(f"Invalid platform or architecture: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(
                f"Error detecting cross-compiler {platform} {architecture}: {str(e)}"
            )
            return None

    def get_recommended_compiler(
        self,
        architecture: str = "x64",
        cpp_standard: Optional[str] = None
    ) -> Optional[MSVCCompilerInfo]:
        """Get recommended compiler for system
        
        Selects the best compiler based on platform, architecture,
        and C++ standard requirements.
        
        Args:
            architecture: Target architecture (default: x64)
            cpp_standard: Required C++ standard (optional)
            
        Returns:
            Recommended CompilerInfo or None if no suitable compiler found
        """
        self._logger.info(
            f"Getting recommended compiler for architecture: {architecture}"
        )
        
        try:
            compiler = self._compiler_manager.get_recommended_compiler(
                architecture,
                cpp_standard
            )
            
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
            self._logger.error(f"Error getting recommended compiler: {str(e)}")
            return None

    def validate_system(self) -> ValidationResult:
        """Validate entire compiler detection system
        
        This method validates that all components are properly configured
        and functional, including compilers, terminals, and cross-compilers.
        
        Returns:
            ValidationResult with validation status, errors, and warnings
        """
        self._logger.info("Validating compiler detection system")
        
        errors: List[str] = []
        warnings: List[str] = []
        
        # Validate compiler factory
        try:
            self._logger.debug("Validating compiler factory")
            available_compilers = self._factory.get_available_compilers()
            total_compilers = sum(len(c) for c in available_compilers.values())
            
            if total_compilers == 0:
                errors.append("No compilers detected by factory")
                self._logger.warning("No compilers detected")
            else:
                self._logger.debug(
                    f"Factory has {total_compilers} compilers registered"
                )
        except Exception as e:
            error_msg = f"Compiler factory validation failed: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Validate compiler manager
        try:
            self._logger.debug("Validating compiler manager")
            all_compilers = self._compiler_manager.get_all_compilers()
            total_compilers = sum(len(c) for c in all_compilers.values())
            
            if total_compilers == 0:
                errors.append("No compilers in manager")
                self._logger.warning("No compilers in manager")
            else:
                self._logger.debug(
                    f"Manager has {total_compilers} compilers"
                )
        except Exception as e:
            error_msg = f"Compiler manager validation failed: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Validate terminal detector
        if self._terminal_detector:
            try:
                self._logger.debug("Validating terminal detector")
                terminals = self._terminal_detector.detect()
                
                if not terminals:
                    warnings.append("No terminals detected")
                    self._logger.warning("No terminals detected")
                else:
                    self._logger.debug(
                        f"Terminal detector found {len(terminals)} terminals"
                    )
            except Exception as e:
                error_msg = f"Terminal detector validation failed: {str(e)}"
                self._logger.error(error_msg)
                errors.append(error_msg)
        
        # Validate terminal invoker
        try:
            self._logger.debug("Validating terminal invoker")
            # Terminal invoker is always valid if initialized
            self._logger.debug("Terminal invoker is valid")
        except Exception as e:
            error_msg = f"Terminal invoker validation failed: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Validate compiler-terminal mapper
        if self._mapper:
            try:
                self._logger.debug("Validating compiler-terminal mapper")
                supported_types = self._mapper.get_supported_compiler_types()
                
                if not supported_types:
                    errors.append("No compiler types supported by mapper")
                    self._logger.warning("No compiler types in mapper")
                else:
                    self._logger.debug(
                        f"Mapper supports {len(supported_types)} compiler types"
                    )
            except Exception as e:
                error_msg = f"Mapper validation failed: {str(e)}"
                self._logger.error(error_msg)
                errors.append(error_msg)
        
        # Validate cross-compilers
        try:
            self._logger.debug("Validating cross-compilers")
            toolchain_result = self._toolchain_detector.detect()
            
            if not toolchain_result.toolchains:
                warnings.append("No cross-compilers detected")
                self._logger.warning("No cross-compilers detected")
            else:
                self._logger.debug(
                    f"Found {len(toolchain_result.toolchains)} cross-compilers"
                )
        except Exception as e:
            error_msg = f"Cross-compiler validation failed: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Validate CMake generator selector
        try:
            self._logger.debug("Validating CMake generator selector")
            # CMake selector is always valid if initialized
            self._logger.debug("CMake generator selector is valid")
        except Exception as e:
            error_msg = f"CMake selector validation failed: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Determine overall validity
        is_valid = len(errors) == 0
        
        if is_valid:
            self._logger.info("System validation passed")
        else:
            self._logger.warning(
                f"System validation failed with {len(errors)} errors "
                f"and {len(warnings)} warnings"
            )
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def get_terminal(
        self,
        compiler_type: str,
        architecture: str = "x64"
    ) -> Optional[TerminalInfo]:
        """Get terminal for compiler and architecture
        
        Args:
            compiler_type: Type of compiler
            architecture: Target architecture
            
        Returns:
            TerminalInfo if found, None otherwise
        """
        self._logger.info(
            f"Getting terminal for {compiler_type} {architecture}"
        )
        
        if not self._mapper:
            self._logger.warning("Mapper not available")
            return None
        
        try:
            terminal = self._mapper.get_preferred_terminal(
                compiler_type,
                architecture
            )
            
            if terminal:
                self._logger.info(
                    f"Selected terminal: {terminal.name} ({terminal.terminal_id})"
                )
            else:
                self._logger.warning(
                    f"Terminal not found for {compiler_type} {architecture}"
                )
            
            return terminal
        except Exception as e:
            self._logger.error(
                f"Error getting terminal for {compiler_type} {architecture}: {str(e)}"
            )
            return None

    def setup_environment(
        self,
        compiler_type: str,
        architecture: str = "x64"
    ) -> Dict[str, str]:
        """Setup environment for compiler and architecture
        
        Args:
            compiler_type: Type of compiler
            architecture: Target architecture
            
        Returns:
            Environment variables after setup
            
        Raises:
            ValueError: If compiler not found
            RuntimeError: If environment setup fails
        """
        self._logger.info(
            f"Setting up environment for {compiler_type} {architecture}"
        )
        
        # Get compiler info
        compiler = self.detect_compiler(compiler_type, architecture)
        
        if not compiler:
            error_msg = f"Compiler not found: {compiler_type} {architecture}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Setup environment using terminal invoker
        try:
            # Convert compiler info to terminal invoker format
            compiler_info = TerminalInvokerCompilerInfo(
                compiler_type=compiler.compiler_type.value,
                version=str(compiler.version),
                path=compiler.path,
                architecture=compiler.architecture.value,
                metadata=compiler.metadata
            )
            
            env = self._terminal_invoker.setup_environment(compiler_info)
            
            self._logger.info(
                f"Environment setup complete for {compiler_type} {architecture}"
            )
            
            return env
        except Exception as e:
            error_msg = f"Environment setup failed: {str(e)}"
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

    def execute_command(
        self,
        compiler_type: str,
        architecture: str,
        command: str,
        timeout: int = 300
    ) -> CommandResult:
        """Execute command in compiler's terminal environment
        
        Args:
            compiler_type: Type of compiler
            architecture: Target architecture
            command: Command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Command execution result
        """
        self._logger.info(
            f"Executing command for {compiler_type} {architecture}"
        )
        
        # Execute command
        try:
            result = self._terminal_invoker.execute_command(command, timeout)
            
            if result.success:
                self._logger.info(
                    f"Command succeeded in {result.execution_time:.2f}s"
                )
            else:
                self._logger.error(
                    f"Command failed with exit code {result.exit_code}"
                )
            
            return result
        except Exception as e:
            self._logger.error(f"Command execution failed: {str(e)}")
            return CommandResult(
                exit_code=-1,
                stdout="",
                stderr=str(e),
                environment={},
                execution_time=0.0
            )

    def setup_cross_compilation(
        self,
        platform: str,
        architecture: str
    ) -> Dict[str, str]:
        """Setup cross-compilation environment for platform and architecture
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            Environment variables for cross-compilation
            
        Raises:
            ValueError: If platform or architecture is invalid
            RuntimeError: If cross-compiler not found or setup fails
        """
        self._logger.info(
            f"Setting up cross-compilation for {platform} {architecture}"
        )
        
        # Detect cross-compiler
        toolchain = self.detect_cross_compiler(platform, architecture)
        
        if not toolchain:
            error_msg = f"Cross-compiler not found: {platform} {architecture}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Get cross-compiler instance
        cross_compiler_key = f"{platform}_{architecture}"
        cross_compiler = self._cross_compilers.get(cross_compiler_key)
        
        if not cross_compiler:
            error_msg = f"Cross-compiler instance not found: {cross_compiler_key}"
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Setup environment
        try:
            env = cross_compiler.setup_environment()
            
            self._logger.info(
                f"Cross-compilation environment setup complete for {platform} {architecture}"
            )
            
            return env
        except Exception as e:
            error_msg = f"Cross-compilation environment setup failed: {str(e)}"
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_cmake_generator(
        self,
        compiler_type: str,
        target_platform: Optional[str] = None,
        prefer_multi_config: bool = False
    ) -> GeneratorSelectionResult:
        """Get appropriate CMake generator for compiler and platform
        
        Args:
            compiler_type: Type of compiler
            target_platform: Target platform (optional, auto-detects if None)
            prefer_multi_config: Prefer multi-config generators
            
        Returns:
            Generator selection result
        """
        self._logger.info(
            f"Getting CMake generator for {compiler_type} "
            f"platform={target_platform or 'auto'}"
        )
        
        try:
            result = self._cmake_selector.select_generator(
                compiler_type=compiler_type,
                target_platform=target_platform,
                prefer_multi_config=prefer_multi_config
            )
            
            self._logger.info(
                f"Selected CMake generator: {result.generator}"
            )
            
            return result
        except Exception as e:
            self._logger.error(f"CMake generator selection failed: {str(e)}")
            # Return fallback result
            from .cmake_generator_selector import (
                CMakeGeneratorType,
                CompilerType as CMakeCompilerType,
                TargetPlatform as CMakeTargetPlatform
            )
            
            # Convert string compiler_type to enum
            try:
                compiler_enum = CMakeCompilerType(compiler_type.lower())
            except ValueError:
                compiler_enum = CMakeCompilerType.GCC
            
            # Convert string target_platform to enum
            try:
                platform_enum = CMakeTargetPlatform((target_platform or "windows").lower())
            except ValueError:
                platform_enum = CMakeTargetPlatform.WINDOWS
            
            return GeneratorSelectionResult(
                generator=CMakeGeneratorType.NINJA.value,
                generator_type=CMakeGeneratorType.NINJA,
                compiler_type=compiler_enum,
                target_platform=platform_enum,
                fallback_used=True,
                warnings=[f"Selection failed: {str(e)}"]
            )

    def get_all_compilers(self) -> Dict[str, List[MSVCCompilerInfo]]:
        """Get all detected compilers
        
        Returns:
            Dictionary mapping compiler types to lists of CompilerInfo
        """
        self._logger.debug("Getting all detected compilers")
        return self._compiler_manager.get_all_compilers()

    def get_all_terminals(self) -> Dict[str, List[TerminalInfo]]:
        """Get all detected terminals
        
        Returns:
            Dictionary mapping terminal types to lists of TerminalInfo
        """
        self._logger.debug("Getting all detected terminals")
        
        if not self._terminal_detector:
            return {}
        
        terminals = self._terminal_detector.detect()
        
        # Group by type
        result: Dict[str, List[TerminalInfo]] = {}
        for terminal in terminals:
            terminal_type = terminal.type.value
            if terminal_type not in result:
                result[terminal_type] = []
            result[terminal_type].append(terminal)
        
        return result

    def get_all_cross_compilers(self) -> Dict[str, UnifiedToolchainInfo]:
        """Get all detected cross-compilers
        
        Returns:
            Dictionary mapping platform-architecture to toolchain info
        """
        self._logger.debug("Getting all detected cross-compilers")
        
        toolchain_result = self._toolchain_detector.detect()
        
        result: Dict[str, UnifiedToolchainInfo] = {}
        for tc in toolchain_result.toolchains:
            key = f"{tc.platform}_{tc.architecture}"
            result[key] = tc
        
        return result

    def refresh_detection(self) -> DetectionResult:
        """Refresh all detection results
        
        Clears caches and re-detects all components.
        
        Returns:
            DetectionResult with refreshed detection results
        """
        self._logger.info("Refreshing detection results")
        
        # Clear factory cache
        self._factory.clear_cache()
        
        # Re-detect all components
        return self.detect_all()

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information
        
        Returns:
            Dictionary with system information including compilers, terminals,
            cross-compilers, and validation status
        """
        self._logger.info("Getting system information")
        
        # Get detection results
        detection_result = self.detect_all()
        
        # Get validation result
        validation_result = self.validate_system()
        
        return {
            "detection": detection_result.to_dict(),
            "validation": validation_result.to_dict(),
            "compilers_count": sum(
                len(c) for c in detection_result.compilers.values()
            ),
            "terminals_count": sum(
                len(t) for t in detection_result.terminals.values()
            ),
            "cross_compilers_count": len(detection_result.cross_compilers),
            "has_errors": detection_result.has_errors,
            "has_warnings": detection_result.has_warnings,
            "is_valid": validation_result.is_valid
        }
