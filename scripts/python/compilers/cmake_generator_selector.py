"""
CMake Generator Selector Module

This module provides functionality for selecting appropriate CMake generators
based on compiler type, target platform, and system capabilities.
"""

import logging
import platform
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class CMakeGeneratorError(Exception):
    """Exception raised when CMake generator selection fails."""
    pass


class CMakeGeneratorType(Enum):
    """CMake generator type enumeration."""
    NINJA = "Ninja"
    NINJA_MULTI_CONFIG = "Ninja Multi-Config"
    VISUAL_STUDIO_17_2022 = "Visual Studio 17 2022"
    VISUAL_STUDIO_16_2019 = "Visual Studio 16 2019"
    VISUAL_STUDIO_15_2017 = "Visual Studio 15 2017"
    UNIX_MAKEFILES = "Unix Makefiles"
    XCODE = "Xcode"
    BORLAND_MAKEFILES = "Borland Makefiles"
    MSYS_MAKEFILES = "MSYS Makefiles"
    MINGW_MAKEFILES = "MinGW Makefiles"
    NMAKE_MAKEFILES = "NMake Makefiles"
    NMAKE_MAKEFILES_JOM = "NMake Makefiles JOM"
    WATCOM_WMAKE = "Watcom WMake"


class CompilerType(Enum):
    """Compiler type enumeration."""
    MSVC = "msvc"
    MSVC_CLANG = "msvc_clang"
    MINGW_GCC = "mingw_gcc"
    MINGW_CLANG = "mingw_clang"
    GCC = "gcc"
    CLANG = "clang"
    EMSCRIPTEN = "emscripten"
    ANDROID_NDK = "android_ndk"


class TargetPlatform(Enum):
    """Target platform enumeration."""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    WASM = "wasm"
    ANDROID = "android"
    IOS = "ios"


@dataclass
class GeneratorInfo:
    """CMake generator information."""
    name: str
    generator_type: CMakeGeneratorType
    supports_multi_config: bool
    preferred_for: List[CompilerType]
    supported_platforms: List[TargetPlatform]
    requires_toolchain: bool = False
    description: str = ""

    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "generator_type": self.generator_type.value,
            "supports_multi_config": self.supports_multi_config,
            "preferred_for": [ct.value for ct in self.preferred_for],
            "supported_platforms": [tp.value for tp in self.supported_platforms],
            "requires_toolchain": self.requires_toolchain,
            "description": self.description
        }


@dataclass
class GeneratorSelectionResult:
    """Result of CMake generator selection."""
    generator: str
    generator_type: CMakeGeneratorType
    compiler_type: CompilerType
    target_platform: TargetPlatform
    fallback_used: bool = False
    warnings: List[str] = None

    def __post_init__(self) -> None:
        """Initialize warnings list if not provided."""
        if self.warnings is None:
            self.warnings = []

    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary."""
        return {
            "generator": self.generator,
            "generator_type": self.generator_type.value,
            "compiler_type": self.compiler_type.value,
            "target_platform": self.target_platform.value,
            "fallback_used": self.fallback_used,
            "warnings": self.warnings
        }


class CMakeGeneratorSelector:
    """
    Selector for CMake generators based on compiler and platform.

    This class provides intelligent selection of CMake generators
    considering compiler type, target platform, and system capabilities.
    """

    # Generator mappings for different compiler-platform combinations
    _GENERATOR_MAP: Dict[Tuple[CompilerType, TargetPlatform], List[CMakeGeneratorType]] = {
        # Windows MSVC
        (CompilerType.MSVC, TargetPlatform.WINDOWS): [
            CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            CMakeGeneratorType.VISUAL_STUDIO_16_2019,
            CMakeGeneratorType.VISUAL_STUDIO_15_2017,
            CMakeGeneratorType.NINJA_MULTI_CONFIG,
            CMakeGeneratorType.NINJA
        ],
        # Windows MSVC-Clang
        (CompilerType.MSVC_CLANG, TargetPlatform.WINDOWS): [
            CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            CMakeGeneratorType.VISUAL_STUDIO_16_2019,
            CMakeGeneratorType.NINJA_MULTI_CONFIG,
            CMakeGeneratorType.NINJA
        ],
        # Windows MinGW-GCC
        (CompilerType.MINGW_GCC, TargetPlatform.WINDOWS): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.MINGW_MAKEFILES,
            CMakeGeneratorType.MSYS_MAKEFILES,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # Windows MinGW-Clang
        (CompilerType.MINGW_CLANG, TargetPlatform.WINDOWS): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.MINGW_MAKEFILES,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # Linux GCC
        (CompilerType.GCC, TargetPlatform.LINUX): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # Linux Clang
        (CompilerType.CLANG, TargetPlatform.LINUX): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # macOS GCC
        (CompilerType.GCC, TargetPlatform.MACOS): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # macOS Clang
        (CompilerType.CLANG, TargetPlatform.MACOS): [
            CMakeGeneratorType.XCODE,
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # WASM Emscripten
        (CompilerType.EMSCRIPTEN, TargetPlatform.WASM): [
            CMakeGeneratorType.NINJA
        ],
        # Android NDK
        (CompilerType.ANDROID_NDK, TargetPlatform.ANDROID): [
            CMakeGeneratorType.NINJA,
            CMakeGeneratorType.UNIX_MAKEFILES
        ],
        # iOS Clang
        (CompilerType.CLANG, TargetPlatform.IOS): [
            CMakeGeneratorType.XCODE,
            CMakeGeneratorType.NINJA
        ]
    }

    # Platform-specific default generators
    _PLATFORM_DEFAULTS: Dict[TargetPlatform, CMakeGeneratorType] = {
        TargetPlatform.WINDOWS: CMakeGeneratorType.NINJA,
        TargetPlatform.LINUX: CMakeGeneratorType.NINJA,
        TargetPlatform.MACOS: CMakeGeneratorType.NINJA,
        TargetPlatform.WASM: CMakeGeneratorType.NINJA,
        TargetPlatform.ANDROID: CMakeGeneratorType.NINJA,
        TargetPlatform.IOS: CMakeGeneratorType.XCODE
    }

    # Generator information
    _GENERATOR_INFO: Dict[CMakeGeneratorType, GeneratorInfo] = {
        CMakeGeneratorType.NINJA: GeneratorInfo(
            name="Ninja",
            generator_type=CMakeGeneratorType.NINJA,
            supports_multi_config=False,
            preferred_for=[
                CompilerType.MINGW_GCC,
                CompilerType.MINGW_CLANG,
                CompilerType.GCC,
                CompilerType.CLANG,
                CompilerType.EMSCRIPTEN,
                CompilerType.ANDROID_NDK
            ],
            supported_platforms=[
                TargetPlatform.WINDOWS,
                TargetPlatform.LINUX,
                TargetPlatform.MACOS,
                TargetPlatform.WASM,
                TargetPlatform.ANDROID,
                TargetPlatform.IOS
            ],
            requires_toolchain=False,
            description="Fast, low-overhead build system"
        ),
        CMakeGeneratorType.NINJA_MULTI_CONFIG: GeneratorInfo(
            name="Ninja Multi-Config",
            generator_type=CMakeGeneratorType.NINJA_MULTI_CONFIG,
            supports_multi_config=True,
            preferred_for=[
                CompilerType.MSVC,
                CompilerType.MSVC_CLANG
            ],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=False,
            description="Ninja with multi-configuration support"
        ),
        CMakeGeneratorType.VISUAL_STUDIO_17_2022: GeneratorInfo(
            name="Visual Studio 17 2022",
            generator_type=CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            supports_multi_config=True,
            preferred_for=[CompilerType.MSVC, CompilerType.MSVC_CLANG],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=True,
            description="Visual Studio 2022 project files"
        ),
        CMakeGeneratorType.VISUAL_STUDIO_16_2019: GeneratorInfo(
            name="Visual Studio 16 2019",
            generator_type=CMakeGeneratorType.VISUAL_STUDIO_16_2019,
            supports_multi_config=True,
            preferred_for=[CompilerType.MSVC, CompilerType.MSVC_CLANG],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=True,
            description="Visual Studio 2019 project files"
        ),
        CMakeGeneratorType.VISUAL_STUDIO_15_2017: GeneratorInfo(
            name="Visual Studio 15 2017",
            generator_type=CMakeGeneratorType.VISUAL_STUDIO_15_2017,
            supports_multi_config=True,
            preferred_for=[CompilerType.MSVC, CompilerType.MSVC_CLANG],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=True,
            description="Visual Studio 2017 project files"
        ),
        CMakeGeneratorType.UNIX_MAKEFILES: GeneratorInfo(
            name="Unix Makefiles",
            generator_type=CMakeGeneratorType.UNIX_MAKEFILES,
            supports_multi_config=False,
            preferred_for=[CompilerType.GCC, CompilerType.CLANG],
            supported_platforms=[
                TargetPlatform.LINUX,
                TargetPlatform.MACOS,
                TargetPlatform.WINDOWS
            ],
            requires_toolchain=False,
            description="Standard Unix makefiles"
        ),
        CMakeGeneratorType.XCODE: GeneratorInfo(
            name="Xcode",
            generator_type=CMakeGeneratorType.XCODE,
            supports_multi_config=True,
            preferred_for=[CompilerType.CLANG],
            supported_platforms=[TargetPlatform.MACOS, TargetPlatform.IOS],
            requires_toolchain=True,
            description="Xcode project files"
        ),
        CMakeGeneratorType.MINGW_MAKEFILES: GeneratorInfo(
            name="MinGW Makefiles",
            generator_type=CMakeGeneratorType.MINGW_MAKEFILES,
            supports_multi_config=False,
            preferred_for=[CompilerType.MINGW_GCC, CompilerType.MINGW_CLANG],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=False,
            description="MinGW makefiles"
        ),
        CMakeGeneratorType.MSYS_MAKEFILES: GeneratorInfo(
            name="MSYS Makefiles",
            generator_type=CMakeGeneratorType.MSYS_MAKEFILES,
            supports_multi_config=False,
            preferred_for=[CompilerType.MINGW_GCC],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=False,
            description="MSYS makefiles"
        ),
        CMakeGeneratorType.NMAKE_MAKEFILES: GeneratorInfo(
            name="NMake Makefiles",
            generator_type=CMakeGeneratorType.NMAKE_MAKEFILES,
            supports_multi_config=False,
            preferred_for=[CompilerType.MSVC],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=True,
            description="NMake makefiles"
        ),
        CMakeGeneratorType.NMAKE_MAKEFILES_JOM: GeneratorInfo(
            name="NMake Makefiles JOM",
            generator_type=CMakeGeneratorType.NMAKE_MAKEFILES_JOM,
            supports_multi_config=False,
            preferred_for=[CompilerType.MSVC],
            supported_platforms=[TargetPlatform.WINDOWS],
            requires_toolchain=True,
            description="NMake makefiles with JOM"
        )
    }

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize CMake generator selector.

        Args:
            logger: Optional logger instance
        """
        self._logger = logger or logging.getLogger(__name__)
        self._current_platform: TargetPlatform = self._detect_current_platform()

    def select_generator(
        self,
        compiler_type: str,
        target_platform: Optional[str] = None,
        prefer_multi_config: bool = False,
        allow_fallback: bool = True
    ) -> GeneratorSelectionResult:
        """
        Select appropriate CMake generator for compiler and platform.

        Args:
            compiler_type: Compiler type (msvc, mingw_gcc, gcc, clang, etc.)
            target_platform: Target platform (windows, linux, macos, wasm, android, ios)
            prefer_multi_config: Prefer multi-config generators
            allow_fallback: Allow fallback to alternative generators

        Returns:
            Generator selection result

        Raises:
            CMakeGeneratorError: If generator selection fails
        """
        self._logger.info(
            f"Selecting CMake generator for compiler={compiler_type}, "
            f"platform={target_platform or 'auto'}, "
            f"prefer_multi_config={prefer_multi_config}"
        )

        # Parse compiler type
        try:
            compiler_enum = CompilerType(compiler_type.lower())
        except ValueError as e:
            raise CMakeGeneratorError(
                f"Unknown compiler type: {compiler_type}. "
                f"Valid types: {[ct.value for ct in CompilerType]}"
            ) from e

        # Determine target platform
        if target_platform is None:
            target_platform_enum = self._current_platform
            self._logger.debug(f"Using current platform: {target_platform_enum.value}")
        else:
            try:
                target_platform_enum = TargetPlatform(target_platform.lower())
            except ValueError as e:
                raise CMakeGeneratorError(
                    f"Unknown target platform: {target_platform}. "
                    f"Valid platforms: {[tp.value for tp in TargetPlatform]}"
                ) from e

        # Select generator for compiler
        generator_type = self.select_generator_for_compiler(
            compiler_enum,
            target_platform_enum,
            prefer_multi_config
        )

        # Validate generator
        validation_result = self.validate_generator(
            generator_type,
            target_platform_enum
        )

        if not validation_result["is_valid"]:
            if allow_fallback:
                self._logger.warning(
                    f"Primary generator {generator_type.value} validation failed: "
                    f"{validation_result['errors']}. Attempting fallback."
                )
                generator_type = self._get_fallback_generator(
                    compiler_enum,
                    target_platform_enum,
                    generator_type
                )
                validation_result = self.validate_generator(
                    generator_type,
                    target_platform_enum
                )
            else:
                raise CMakeGeneratorError(
                    f"Generator {generator_type.value} validation failed: "
                    f"{validation_result['errors']}"
                )

        # Create result
        result = GeneratorSelectionResult(
            generator=generator_type.value,
            generator_type=generator_type,
            compiler_type=compiler_enum,
            target_platform=target_platform_enum,
            fallback_used=allow_fallback and not self._is_primary_generator(
                compiler_enum,
                target_platform_enum,
                generator_type
            ),
            warnings=validation_result.get("warnings", [])
        )

        self._logger.info(
            f"Selected CMake generator: {result.generator} "
            f"(fallback_used={result.fallback_used})"
        )

        return result

    def select_generator_for_compiler(
        self,
        compiler_type: CompilerType,
        target_platform: TargetPlatform,
        prefer_multi_config: bool = False
    ) -> CMakeGeneratorType:
        """
        Select CMake generator for specific compiler and platform.

        Args:
            compiler_type: Compiler type enum
            target_platform: Target platform enum
            prefer_multi_config: Prefer multi-config generators

        Returns:
            Selected CMake generator type

        Raises:
            CMakeGeneratorError: If no suitable generator found
        """
        self._logger.debug(
            f"Selecting generator for compiler={compiler_type.value}, "
            f"platform={target_platform.value}, "
            f"prefer_multi_config={prefer_multi_config}"
        )

        # Get available generators for compiler-platform combination
        key = (compiler_type, target_platform)
        available_generators = self._GENERATOR_MAP.get(key)

        if not available_generators:
            self._logger.warning(
                f"No specific generators for {compiler_type.value} on "
                f"{target_platform.value}, using platform default"
            )
            return self._PLATFORM_DEFAULTS.get(target_platform, CMakeGeneratorType.NINJA)

        # Filter by multi-config preference
        if prefer_multi_config:
            multi_config_generators = [
                gen for gen in available_generators
                if self._GENERATOR_INFO[gen].supports_multi_config
            ]
            if multi_config_generators:
                self._logger.debug("Using multi-config generator")
                return multi_config_generators[0]

        # Return first available generator
        return available_generators[0]

    def select_generator_for_platform(
        self,
        target_platform: TargetPlatform,
        prefer_multi_config: bool = False,
        prefer_native: bool = True
    ) -> CMakeGeneratorType:
        """
        Select CMake generator for specific platform.

        Args:
            target_platform: Target platform enum
            prefer_multi_config: Prefer multi-config generators
            prefer_native: Prefer platform-native generators

        Returns:
            Selected CMake generator type
        """
        self._logger.debug(
            f"Selecting generator for platform={target_platform.value}, "
            f"prefer_multi_config={prefer_multi_config}, "
            f"prefer_native={prefer_native}"
        )

        # Get platform default
        default_generator = self._PLATFORM_DEFAULTS.get(
            target_platform,
            CMakeGeneratorType.NINJA
        )

        # If preferring native generators, check for platform-specific options
        if prefer_native:
            if target_platform == TargetPlatform.WINDOWS:
                # Check if Visual Studio is available
                if self._is_visual_studio_available():
                    return CMakeGeneratorType.VISUAL_STUDIO_17_2022
            elif target_platform in (TargetPlatform.MACOS, TargetPlatform.IOS):
                # Check if Xcode is available
                if self._is_xcode_available():
                    return CMakeGeneratorType.XCODE

        # If preferring multi-config, check for multi-config generators
        if prefer_multi_config:
            multi_config_generators = [
                gen_type for gen_type, gen_info in self._GENERATOR_INFO.items()
                if gen_info.supports_multi_config and
                target_platform in gen_info.supported_platforms
            ]
            if multi_config_generators:
                return multi_config_generators[0]

        return default_generator

    def validate_generator(
        self,
        generator_type: CMakeGeneratorType,
        target_platform: TargetPlatform
    ) -> Dict[str, any]:
        """
        Validate CMake generator for target platform.

        Args:
            generator_type: CMake generator type to validate
            target_platform: Target platform

        Returns:
            Validation result with is_valid, errors, and warnings
        """
        self._logger.debug(
            f"Validating generator={generator_type.value} for "
            f"platform={target_platform.value}"
        )

        errors: List[str] = []
        warnings: List[str] = []

        # Check if generator is supported for platform
        if generator_type not in self._GENERATOR_INFO:
            errors.append(f"Unknown generator type: {generator_type.value}")
            return {"is_valid": False, "errors": errors, "warnings": warnings}

        generator_info = self._GENERATOR_INFO[generator_type]

        # Check platform support
        if target_platform not in generator_info.supported_platforms:
            errors.append(
                f"Generator {generator_type.value} is not supported on "
                f"{target_platform.value}. Supported platforms: "
                f"{[tp.value for tp in generator_info.supported_platforms]}"
            )

        # Check if generator requires toolchain
        if generator_info.requires_toolchain:
            if not self._check_toolchain_availability(generator_type, target_platform):
                warnings.append(
                    f"Generator {generator_type.value} requires a toolchain. "
                    f"Ensure toolchain is properly configured."
                )

        # Check if generator executable is available
        if not self._check_generator_executable(generator_type):
            warnings.append(
                f"Generator {generator_type.value} executable may not be available. "
                f"Ensure it is installed and in PATH."
            )

        is_valid = len(errors) == 0

        self._logger.debug(
            f"Generator validation result: is_valid={is_valid}, "
            f"errors={len(errors)}, warnings={len(warnings)}"
        )

        return {
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings
        }

    def get_generator_info(self, generator_type: CMakeGeneratorType) -> Optional[GeneratorInfo]:
        """
        Get information about a CMake generator.

        Args:
            generator_type: CMake generator type

        Returns:
            Generator information or None if not found
        """
        return self._GENERATOR_INFO.get(generator_type)

    def list_available_generators(
        self,
        target_platform: Optional[TargetPlatform] = None
    ) -> List[GeneratorInfo]:
        """
        List all available CMake generators.

        Args:
            target_platform: Optional platform filter

        Returns:
            List of generator information
        """
        generators = list(self._GENERATOR_INFO.values())

        if target_platform:
            generators = [
                gen for gen in generators
                if target_platform in gen.supported_platforms
            ]

        return generators

    def _detect_current_platform(self) -> TargetPlatform:
        """
        Detect current platform.

        Returns:
            Detected platform enum
        """
        system = platform.system().lower()

        if system == "windows":
            return TargetPlatform.WINDOWS
        elif system == "linux":
            return TargetPlatform.LINUX
        elif system == "darwin":
            return TargetPlatform.MACOS
        else:
            self._logger.warning(f"Unknown platform: {system}, defaulting to Linux")
            return TargetPlatform.LINUX

    def _is_primary_generator(
        self,
        compiler_type: CompilerType,
        target_platform: TargetPlatform,
        generator_type: CMakeGeneratorType
    ) -> bool:
        """
        Check if generator is the primary choice for compiler-platform.

        Args:
            compiler_type: Compiler type
            target_platform: Target platform
            generator_type: Generator type to check

        Returns:
            True if generator is primary choice
        """
        key = (compiler_type, target_platform)
        available_generators = self._GENERATOR_MAP.get(key, [])

        return len(available_generators) > 0 and available_generators[0] == generator_type

    def _get_fallback_generator(
        self,
        compiler_type: CompilerType,
        target_platform: TargetPlatform,
        primary_generator: CMakeGeneratorType
    ) -> CMakeGeneratorType:
        """
        Get fallback generator when primary fails.

        Args:
            compiler_type: Compiler type
            target_platform: Target platform
            primary_generator: Primary generator that failed

        Returns:
            Fallback generator type
        """
        key = (compiler_type, target_platform)
        available_generators = self._GENERATOR_MAP.get(key, [])

        # Find next available generator after primary
        try:
            primary_index = available_generators.index(primary_generator)
            if primary_index + 1 < len(available_generators):
                fallback = available_generators[primary_index + 1]
                self._logger.info(
                    f"Using fallback generator: {fallback.value}"
                )
                return fallback
        except ValueError:
            pass

        # Use platform default as final fallback
        fallback = self._PLATFORM_DEFAULTS.get(
            target_platform,
            CMakeGeneratorType.NINJA
        )
        self._logger.info(
            f"Using platform default fallback generator: {fallback.value}"
        )
        return fallback

    def _is_visual_studio_available(self) -> bool:
        """
        Check if Visual Studio is available.

        Returns:
            True if Visual Studio is available
        """
        import shutil

        # Check for common Visual Studio indicators
        vswhere_path = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
        if shutil.which(vswhere_path) or shutil.which("vswhere"):
            return True

        # Check for devenv
        if shutil.which("devenv"):
            return True

        return False

    def _is_xcode_available(self) -> bool:
        """
        Check if Xcode is available.

        Returns:
            True if Xcode is available
        """
        import shutil

        return shutil.which("xcodebuild") is not None

    def _check_toolchain_availability(
        self,
        generator_type: CMakeGeneratorType,
        target_platform: TargetPlatform
    ) -> bool:
        """
        Check if required toolchain is available for generator.

        Args:
            generator_type: Generator type
            target_platform: Target platform

        Returns:
            True if toolchain is available
        """
        import shutil

        if generator_type in (
            CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            CMakeGeneratorType.VISUAL_STUDIO_16_2019,
            CMakeGeneratorType.VISUAL_STUDIO_15_2017,
            CMakeGeneratorType.NMAKE_MAKEFILES,
            CMakeGeneratorType.NMAKE_MAKEFILES_JOM
        ):
            # Check for MSVC toolchain
            return shutil.which("cl") is not None

        if generator_type == CMakeGeneratorType.XCODE:
            # Check for Xcode toolchain
            return shutil.which("clang") is not None

        return True

    def _check_generator_executable(self, generator_type: CMakeGeneratorType) -> bool:
        """
        Check if generator executable is available.

        Args:
            generator_type: Generator type

        Returns:
            True if executable is available
        """
        import shutil

        if generator_type == CMakeGeneratorType.NINJA:
            return shutil.which("ninja") is not None

        if generator_type == CMakeGeneratorType.XCODE:
            return shutil.which("xcodebuild") is not None

        # For Visual Studio generators, check vswhere or devenv
        if generator_type in (
            CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            CMakeGeneratorType.VISUAL_STUDIO_16_2019,
            CMakeGeneratorType.VISUAL_STUDIO_15_2017
        ):
            return self._is_visual_studio_available()

        # For makefile generators, check for make
        if generator_type in (
            CMakeGeneratorType.UNIX_MAKEFILES,
            CMakeGeneratorType.MINGW_MAKEFILES,
            CMakeGeneratorType.MSYS_MAKEFILES
        ):
            return shutil.which("make") is not None or shutil.which("mingw32-make") is not None

        # For NMake generators, check for nmake
        if generator_type in (
            CMakeGeneratorType.NMAKE_MAKEFILES,
            CMakeGeneratorType.NMAKE_MAKEFILES_JOM
        ):
            return shutil.which("nmake") is not None

        return True
