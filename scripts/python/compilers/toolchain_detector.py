"""
Toolchain Detection Module

This module provides unified detection and validation for cross-compilation toolchains
for Linux, WASM, and Android targets on Windows systems.
"""

import os
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

from .linux_cross_compiler import (
    LinuxCrossCompiler,
    CrossCompilerInfo as LinuxCrossCompilerInfo
)
from .wasm_cross_compiler import (
    WASMCrossCompiler,
    CrossCompilerInfo as WASMCrossCompilerInfo
)
from .android_cross_compiler import (
    AndroidCrossCompiler,
    CrossCompilerInfo as AndroidCrossCompilerInfo
)


@dataclass
class UnifiedToolchainInfo:
    """Unified toolchain information dataclass
    
    Attributes:
        platform: Target platform (linux, wasm, android)
        architecture: Target architecture
        toolchain_path: Path to toolchain directory
        sysroot: Path to sysroot directory
        compilers: Dictionary of compiler tools
        cmake_generator: CMake generator name
        metadata: Additional metadata including version info
    """
    platform: str
    architecture: str
    toolchain_path: str
    sysroot: str
    compilers: Dict[str, str]
    cmake_generator: str
    metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert unified toolchain info to dictionary
        
        Returns:
            Dictionary representation of toolchain info
        """
        return {
            "platform": self.platform,
            "architecture": self.architecture,
            "toolchain_path": self.toolchain_path,
            "sysroot": self.sysroot,
            "compilers": self.compilers,
            "cmake_generator": self.cmake_generator,
            "metadata": self.metadata
        }

    def is_valid(self) -> bool:
        """Check if toolchain is valid
        
        Returns:
            True if toolchain path exists, False otherwise
        """
        return os.path.exists(self.toolchain_path)


@dataclass
class ToolchainDetectionResult:
    """Toolchain detection result dataclass
    
    Attributes:
        success: Whether detection was successful
        toolchains: List of detected toolchains
        errors: List of error messages
        warnings: List of warning messages
    """
    success: bool
    toolchains: List[UnifiedToolchainInfo]
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert detection result to dictionary
        
        Returns:
            Dictionary representation of detection result
        """
        return {
            "success": self.success,
            "toolchains": [tc.to_dict() for tc in self.toolchains],
            "errors": self.errors,
            "warnings": self.warnings
        }


class ToolchainDetector:
    """Unified toolchain detector for cross-compilation targets
    
    This class provides a unified interface for detecting and validating
    cross-compilation toolchains for Linux, WASM, and Android targets.
    
    Supported platforms:
    - Linux (x86_64-linux-gnu, aarch64-linux-gnu)
    - WASM (wasm32, wasm64)
    - Android (arm64-v8a, armeabi-v7a, x86_64, x86)
    """

    # Supported platforms
    SUPPORTED_PLATFORMS = ["linux", "wasm", "android"]

    # Supported architectures per platform
    SUPPORTED_ARCHITECTURES = {
        "linux": ["x86_64-linux-gnu", "aarch64-linux-gnu"],
        "wasm": ["wasm32", "wasm64"],
        "android": ["arm64-v8a", "armeabi-v7a", "x86_64", "x86"]
    }

    def __init__(self) -> None:
        """Initialize toolchain detector"""
        self._logger = logging.getLogger(__name__)
        self._linux_compilers: Dict[str, LinuxCrossCompiler] = {}
        self._wasm_compilers: Dict[str, WASMCrossCompiler] = {}
        self._android_compilers: Dict[str, AndroidCrossCompiler] = {}
        self._detected_toolchains: List[UnifiedToolchainInfo] = []

    def detect(self) -> ToolchainDetectionResult:
        """Detect all available cross-compilation toolchains
        
        This method searches for all supported cross-compilation toolchains
        on the system and returns a unified result.
        
        Returns:
            ToolchainDetectionResult containing all detected toolchains
        """
        self._logger.info("Starting toolchain detection")
        
        errors: List[str] = []
        warnings: List[str] = []
        toolchains: List[UnifiedToolchainInfo] = []
        
        # Detect Linux toolchains
        try:
            linux_toolchains = self._detect_linux_toolchains()
            toolchains.extend(linux_toolchains)
            self._logger.info(f"Detected {len(linux_toolchains)} Linux toolchains")
        except Exception as e:
            error_msg = f"Error detecting Linux toolchains: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Detect WASM toolchains
        try:
            wasm_toolchains = self._detect_wasm_toolchains()
            toolchains.extend(wasm_toolchains)
            self._logger.info(f"Detected {len(wasm_toolchains)} WASM toolchains")
        except Exception as e:
            error_msg = f"Error detecting WASM toolchains: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Detect Android toolchains
        try:
            android_toolchains = self._detect_android_toolchains()
            toolchains.extend(android_toolchains)
            self._logger.info(f"Detected {len(android_toolchains)} Android toolchains")
        except Exception as e:
            error_msg = f"Error detecting Android toolchains: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
        
        # Store detected toolchains
        self._detected_toolchains = toolchains
        
        # Determine overall success
        success = len(toolchains) > 0
        
        if success:
            self._logger.info(f"Toolchain detection complete: {len(toolchains)} toolchains found")
        else:
            self._logger.warning("No toolchains detected")
            warnings.append("No cross-compilation toolchains found")
        
        return ToolchainDetectionResult(
            success=success,
            toolchains=toolchains,
            errors=errors,
            warnings=warnings
        )

    def detect_toolchain(self, platform: str, architecture: str) -> Optional[UnifiedToolchainInfo]:
        """Detect a specific toolchain for platform and architecture
        
        This method detects a specific cross-compilation toolchain for the
        specified platform and architecture.
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            UnifiedToolchainInfo if found, None otherwise
        """
        self._logger.info(f"Detecting toolchain for {platform} {architecture}")
        
        # Validate platform
        if platform not in self.SUPPORTED_PLATFORMS:
            self._logger.error(f"Unsupported platform: {platform}")
            return None
        
        # Validate architecture for platform
        if architecture not in self.SUPPORTED_ARCHITECTURES.get(platform, []):
            self._logger.error(
                f"Unsupported architecture {architecture} for platform {platform}"
            )
            return None
        
        try:
            # Detect based on platform
            if platform == "linux":
                return self._detect_linux_toolchain(architecture)
            elif platform == "wasm":
                return self._detect_wasm_toolchain(architecture)
            elif platform == "android":
                return self._detect_android_toolchain(architecture)
            else:
                self._logger.error(f"Unknown platform: {platform}")
                return None
                
        except Exception as e:
            self._logger.error(
                f"Error detecting toolchain for {platform} {architecture}: {str(e)}"
            )
            return None

    def detect_sysroot(self, platform: str, architecture: str) -> Optional[str]:
        """Detect sysroot for platform and architecture
        
        This method detects the sysroot directory for the specified
        platform and architecture.
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            Sysroot path if found, None otherwise
        """
        self._logger.info(f"Detecting sysroot for {platform} {architecture}")
        
        try:
            # Detect toolchain first
            toolchain = self.detect_toolchain(platform, architecture)
            
            if toolchain and toolchain.sysroot:
                if os.path.exists(toolchain.sysroot):
                    self._logger.info(
                        f"Successfully detected sysroot: {toolchain.sysroot}"
                    )
                    return toolchain.sysroot
                else:
                    self._logger.warning(
                        f"Sysroot path does not exist: {toolchain.sysroot}"
                    )
                    return None
            else:
                self._logger.warning(
                    f"No sysroot found for {platform} {architecture}"
                )
                return None
                
        except Exception as e:
            self._logger.error(
                f"Error detecting sysroot for {platform} {architecture}: {str(e)}"
            )
            return None

    def detect_target_triple(self, platform: str, architecture: str) -> Optional[str]:
        """Detect target triple for platform and architecture
        
        This method returns the target triple for the specified
        platform and architecture.
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            Target triple string if supported, None otherwise
        """
        self._logger.info(f"Detecting target triple for {platform} {architecture}")
        
        try:
            # Validate platform and architecture
            if platform not in self.SUPPORTED_PLATFORMS:
                self._logger.error(f"Unsupported platform: {platform}")
                return None
            
            if architecture not in self.SUPPORTED_ARCHITECTURES.get(platform, []):
                self._logger.error(
                    f"Unsupported architecture {architecture} for platform {platform}"
                )
                return None
            
            # Return target triple based on platform
            if platform == "linux":
                # Linux uses architecture as target triple
                self._logger.info(f"Target triple: {architecture}")
                return architecture
            elif platform == "wasm":
                # WASM uses architecture as target triple
                self._logger.info(f"Target triple: {architecture}")
                return architecture
            elif platform == "android":
                # Android uses LLVM triple mapping
                from .android_cross_compiler import AndroidCrossCompiler
                android_compiler = AndroidCrossCompiler(architecture)
                target_triple = android_compiler.detect_target_triple()
                if target_triple:
                    self._logger.info(f"Target triple: {target_triple}")
                    return target_triple
                else:
                    self._logger.warning(
                        f"Could not determine target triple for {architecture}"
                    )
                    return None
            else:
                self._logger.error(f"Unknown platform: {platform}")
                return None
                
        except Exception as e:
            self._logger.error(
                f"Error detecting target triple for {platform} {architecture}: {str(e)}"
            )
            return None

    def validate(self, platform: str, architecture: str) -> Dict[str, Any]:
        """Validate toolchain for platform and architecture
        
        This method validates that the toolchain for the specified platform
        and architecture is properly installed and functional.
        
        Args:
            platform: Target platform (linux, wasm, android)
            architecture: Target architecture
            
        Returns:
            Dictionary with validation results (is_valid, errors, warnings)
        """
        self._logger.info(f"Validating toolchain for {platform} {architecture}")
        
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            # Detect toolchain
            toolchain = self.detect_toolchain(platform, architecture)
            
            if not toolchain:
                errors.append(f"No toolchain found for {platform} {architecture}")
                return {
                    "is_valid": False,
                    "errors": errors,
                    "warnings": warnings
                }
            
            # Check toolchain path
            if not os.path.exists(toolchain.toolchain_path):
                errors.append(
                    f"Toolchain path does not exist: {toolchain.toolchain_path}"
                )
            
            # Check sysroot if specified
            if toolchain.sysroot:
                if os.path.exists(toolchain.sysroot):
                    self._logger.debug(f"Sysroot found: {toolchain.sysroot}")
                else:
                    warnings.append(
                        f"Sysroot does not exist: {toolchain.sysroot}"
                    )
            
            # Check compiler executables
            for tool_name, tool_path in toolchain.compilers.items():
                if os.path.exists(tool_path):
                    self._logger.debug(f"Found {tool_name}: {tool_path}")
                else:
                    errors.append(f"Missing {tool_name}: {tool_path}")
            
            # Determine overall validity
            is_valid = len(errors) == 0
            
            if is_valid:
                self._logger.info(
                    f"Toolchain validation successful for {platform} {architecture}"
                )
            else:
                self._logger.error(
                    f"Toolchain validation failed for {platform} {architecture}"
                )
            
            return {
                "is_valid": is_valid,
                "errors": errors,
                "warnings": warnings
            }
            
        except Exception as e:
            error_msg = f"Error validating toolchain: {str(e)}"
            self._logger.error(error_msg)
            errors.append(error_msg)
            
            return {
                "is_valid": False,
                "errors": errors,
                "warnings": warnings
            }

    def get_detected_toolchains(self) -> List[UnifiedToolchainInfo]:
        """Get all detected toolchains
        
        Returns:
            List of all detected toolchains
        """
        return self._detected_toolchains

    def get_toolchains_by_platform(self, platform: str) -> List[UnifiedToolchainInfo]:
        """Get detected toolchains for a specific platform
        
        Args:
            platform: Target platform (linux, wasm, android)
            
        Returns:
            List of toolchains for the specified platform
        """
        return [
            tc for tc in self._detected_toolchains
            if tc.platform == platform
        ]

    def _detect_linux_toolchains(self) -> List[UnifiedToolchainInfo]:
        """Detect all Linux cross-compilation toolchains
        
        Returns:
            List of detected Linux toolchains
        """
        self._logger.info("Detecting Linux toolchains")
        
        toolchains: List[UnifiedToolchainInfo] = []
        
        for architecture in self.SUPPORTED_ARCHITECTURES["linux"]:
            try:
                # Create Linux cross-compiler instance
                compiler = LinuxCrossCompiler(architecture)
                
                # Detect toolchain
                info = compiler.detect()
                
                if info:
                    # Convert to unified format
                    unified = self._convert_linux_to_unified(info)
                    toolchains.append(unified)
                    self._logger.debug(
                        f"Detected Linux toolchain: {architecture}"
                    )
                    
            except Exception as e:
                self._logger.warning(
                    f"Failed to detect Linux toolchain {architecture}: {str(e)}"
                )
        
        return toolchains

    def _detect_wasm_toolchains(self) -> List[UnifiedToolchainInfo]:
        """Detect all WASM cross-compilation toolchains
        
        Returns:
            List of detected WASM toolchains
        """
        self._logger.info("Detecting WASM toolchains")
        
        toolchains: List[UnifiedToolchainInfo] = []
        
        for architecture in self.SUPPORTED_ARCHITECTURES["wasm"]:
            try:
                # Create WASM cross-compiler instance
                compiler = WASMCrossCompiler(architecture)
                
                # Detect toolchain
                info = compiler.detect()
                
                if info:
                    # Convert to unified format
                    unified = self._convert_wasm_to_unified(info)
                    toolchains.append(unified)
                    self._logger.debug(
                        f"Detected WASM toolchain: {architecture}"
                    )
                    
            except Exception as e:
                self._logger.warning(
                    f"Failed to detect WASM toolchain {architecture}: {str(e)}"
                )
        
        return toolchains

    def _detect_android_toolchains(self) -> List[UnifiedToolchainInfo]:
        """Detect all Android cross-compilation toolchains
        
        Returns:
            List of detected Android toolchains
        """
        self._logger.info("Detecting Android toolchains")
        
        toolchains: List[UnifiedToolchainInfo] = []
        
        for architecture in self.SUPPORTED_ARCHITECTURES["android"]:
            try:
                # Create Android cross-compiler instance
                compiler = AndroidCrossCompiler(architecture)
                
                # Detect toolchain
                info = compiler.detect()
                
                if info:
                    # Convert to unified format
                    unified = self._convert_android_to_unified(info)
                    toolchains.append(unified)
                    self._logger.debug(
                        f"Detected Android toolchain: {architecture}"
                    )
                    
            except Exception as e:
                self._logger.warning(
                    f"Failed to detect Android toolchain {architecture}: {str(e)}"
                )
        
        return toolchains

    def _detect_linux_toolchain(self, architecture: str) -> Optional[UnifiedToolchainInfo]:
        """Detect a specific Linux toolchain
        
        Args:
            architecture: Target architecture
            
        Returns:
            UnifiedToolchainInfo if found, None otherwise
        """
        try:
            # Create Linux cross-compiler instance
            compiler = LinuxCrossCompiler(architecture)
            
            # Detect toolchain
            info = compiler.detect()
            
            if info:
                return self._convert_linux_to_unified(info)
            
            return None
            
        except Exception as e:
            self._logger.error(
                f"Error detecting Linux toolchain {architecture}: {str(e)}"
            )
            return None

    def _detect_wasm_toolchain(self, architecture: str) -> Optional[UnifiedToolchainInfo]:
        """Detect a specific WASM toolchain
        
        Args:
            architecture: Target architecture
            
        Returns:
            UnifiedToolchainInfo if found, None otherwise
        """
        try:
            # Create WASM cross-compiler instance
            compiler = WASMCrossCompiler(architecture)
            
            # Detect toolchain
            info = compiler.detect()
            
            if info:
                return self._convert_wasm_to_unified(info)
            
            return None
            
        except Exception as e:
            self._logger.error(
                f"Error detecting WASM toolchain {architecture}: {str(e)}"
            )
            return None

    def _detect_android_toolchain(self, architecture: str) -> Optional[UnifiedToolchainInfo]:
        """Detect a specific Android toolchain
        
        Args:
            architecture: Target architecture
            
        Returns:
            UnifiedToolchainInfo if found, None otherwise
        """
        try:
            # Create Android cross-compiler instance
            compiler = AndroidCrossCompiler(architecture)
            
            # Detect toolchain
            info = compiler.detect()
            
            if info:
                return self._convert_android_to_unified(info)
            
            return None
            
        except Exception as e:
            self._logger.error(
                f"Error detecting Android toolchain {architecture}: {str(e)}"
            )
            return None

    def _convert_linux_to_unified(
        self,
        info: LinuxCrossCompilerInfo
    ) -> UnifiedToolchainInfo:
        """Convert Linux cross-compiler info to unified format
        
        Args:
            info: Linux cross-compiler info
            
        Returns:
            Unified toolchain info
        """
        return UnifiedToolchainInfo(
            platform=info.target_platform,
            architecture=info.target_architecture,
            toolchain_path=info.toolchain_path,
            sysroot=info.sysroot,
            compilers=info.compilers,
            cmake_generator=info.cmake_generator,
            metadata=info.metadata
        )

    def _convert_wasm_to_unified(
        self,
        info: WASMCrossCompilerInfo
    ) -> UnifiedToolchainInfo:
        """Convert WASM cross-compiler info to unified format
        
        Args:
            info: WASM cross-compiler info
            
        Returns:
            Unified toolchain info
        """
        return UnifiedToolchainInfo(
            platform=info.target_platform,
            architecture=info.target_architecture,
            toolchain_path=info.toolchain_path,
            sysroot=info.sysroot,
            compilers=info.compilers,
            cmake_generator=info.cmake_generator,
            metadata=info.metadata
        )

    def _convert_android_to_unified(
        self,
        info: AndroidCrossCompilerInfo
    ) -> UnifiedToolchainInfo:
        """Convert Android cross-compiler info to unified format
        
        Args:
            info: Android cross-compiler info
            
        Returns:
            Unified toolchain info
        """
        return UnifiedToolchainInfo(
            platform=info.target_platform,
            architecture=info.target_architecture,
            toolchain_path=info.toolchain_path,
            sysroot=info.sysroot,
            compilers=info.compilers,
            cmake_generator=info.cmake_generator,
            metadata=info.metadata
        )
