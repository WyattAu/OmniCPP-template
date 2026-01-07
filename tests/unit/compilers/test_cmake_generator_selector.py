"""
Unit tests for CMake Generator Selector

Tests CMakeGeneratorSelector class which selects appropriate CMake generators
based on compiler type, target platform, and system capabilities.
"""

import unittest
from unittest.mock import Mock, patch
import logging
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python')))

from compilers.cmake_generator_selector import (
    CMakeGeneratorSelector,
    CMakeGeneratorType,
    CompilerType,
    TargetPlatform,
    GeneratorInfo,
    GeneratorSelectionResult,
    CMakeGeneratorError
)


class TestCMakeGeneratorSelector(unittest.TestCase):
    """Test cases for CMakeGeneratorSelector class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.logger = logging.getLogger(__name__)
        self.selector = CMakeGeneratorSelector(logger=self.logger)

    def test_initialization(self) -> None:
        """Test selector initialization."""
        self.assertIsNotNone(self.selector)
        self.assertIsInstance(self.selector, CMakeGeneratorSelector)
        self.assertIsNotNone(self.selector._current_platform)

    def test_select_generator_msvc_windows(self) -> None:
        """Test generator selection for MSVC on Windows."""
        result = self.selector.select_generator(
            compiler_type="msvc",
            target_platform="windows"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.MSVC)
        self.assertEqual(result.target_platform, TargetPlatform.WINDOWS)
        self.assertIn(
            result.generator_type,
            [
                CMakeGeneratorType.VISUAL_STUDIO_17_2022,
                CMakeGeneratorType.VISUAL_STUDIO_16_2019,
                CMakeGeneratorType.VISUAL_STUDIO_15_2017,
                CMakeGeneratorType.NINJA_MULTI_CONFIG,
                CMakeGeneratorType.NINJA
            ]
        )

    def test_select_generator_mingw_gcc_windows(self) -> None:
        """Test generator selection for MinGW-GCC on Windows."""
        result = self.selector.select_generator(
            compiler_type="mingw_gcc",
            target_platform="windows"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(result.target_platform, TargetPlatform.WINDOWS)
        self.assertIn(
            result.generator_type,
            [
                CMakeGeneratorType.NINJA,
                CMakeGeneratorType.MINGW_MAKEFILES,
                CMakeGeneratorType.MSYS_MAKEFILES,
                CMakeGeneratorType.UNIX_MAKEFILES
            ]
        )

    def test_select_generator_gcc_linux(self) -> None:
        """Test generator selection for GCC on Linux."""
        result = self.selector.select_generator(
            compiler_type="gcc",
            target_platform="linux"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.GCC)
        self.assertEqual(result.target_platform, TargetPlatform.LINUX)
        self.assertIn(
            result.generator_type,
            [CMakeGeneratorType.NINJA, CMakeGeneratorType.UNIX_MAKEFILES]
        )

    def test_select_generator_clang_macos(self) -> None:
        """Test generator selection for Clang on macOS."""
        result = self.selector.select_generator(
            compiler_type="clang",
            target_platform="macos"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.CLANG)
        self.assertEqual(result.target_platform, TargetPlatform.MACOS)
        self.assertIn(
            result.generator_type,
            [CMakeGeneratorType.XCODE, CMakeGeneratorType.NINJA, CMakeGeneratorType.UNIX_MAKEFILES]
        )

    def test_select_generator_emscripten_wasm(self) -> None:
        """Test generator selection for Emscripten on WASM."""
        result = self.selector.select_generator(
            compiler_type="emscripten",
            target_platform="wasm"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.EMSCRIPTEN)
        self.assertEqual(result.target_platform, TargetPlatform.WASM)
        self.assertEqual(result.generator_type, CMakeGeneratorType.NINJA)

    def test_select_generator_android_ndk_android(self) -> None:
        """Test generator selection for Android NDK on Android."""
        result = self.selector.select_generator(
            compiler_type="android_ndk",
            target_platform="android"
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        self.assertEqual(result.compiler_type, CompilerType.ANDROID_NDK)
        self.assertEqual(result.target_platform, TargetPlatform.ANDROID)
        self.assertIn(
            result.generator_type,
            [CMakeGeneratorType.NINJA, CMakeGeneratorType.UNIX_MAKEFILES]
        )

    def test_select_generator_invalid_compiler_type(self) -> None:
        """Test generator selection with invalid compiler type."""
        with self.assertRaises(CMakeGeneratorError) as context:
            self.selector.select_generator(
                compiler_type="invalid_compiler",
                target_platform="windows"
            )

        self.assertIn("Unknown compiler type", str(context.exception))

    def test_select_generator_invalid_platform(self) -> None:
        """Test generator selection with invalid platform."""
        with self.assertRaises(CMakeGeneratorError) as context:
            self.selector.select_generator(
                compiler_type="gcc",
                target_platform="invalid_platform"
            )

        self.assertIn("Unknown target platform", str(context.exception))

    def test_select_generator_prefer_multi_config(self) -> None:
        """Test generator selection with multi-config preference."""
        result = self.selector.select_generator(
            compiler_type="msvc",
            target_platform="windows",
            prefer_multi_config=True
        )

        self.assertIsInstance(result, GeneratorSelectionResult)
        # Should prefer multi-config generators
        self.assertTrue(
            self.selector._GENERATOR_INFO[result.generator_type].supports_multi_config
        )

    def test_select_generator_no_fallback(self) -> None:
        """Test generator selection without fallback."""
        # This test verifies that when allow_fallback=False,
        # selector will raise an error if validation fails
        # For now, we just test that the parameter is accepted
        result = self.selector.select_generator(
            compiler_type="gcc",
            target_platform="linux",
            allow_fallback=False
        )

        self.assertIsInstance(result, GeneratorSelectionResult)

    def test_select_generator_for_compiler_msvc_windows(self) -> None:
        """Test select_generator_for_compiler for MSVC on Windows."""
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.MSVC,
            target_platform=TargetPlatform.WINDOWS
        )

        self.assertIn(
            generator_type,
            [
                CMakeGeneratorType.VISUAL_STUDIO_17_2022,
                CMakeGeneratorType.VISUAL_STUDIO_16_2019,
                CMakeGeneratorType.VISUAL_STUDIO_15_2017,
                CMakeGeneratorType.NINJA_MULTI_CONFIG,
                CMakeGeneratorType.NINJA
            ]
        )

    def test_select_generator_for_compiler_mingw_clang_windows(self) -> None:
        """Test select_generator_for_compiler for MinGW-Clang on Windows."""
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.MINGW_CLANG,
            target_platform=TargetPlatform.WINDOWS
        )

        self.assertIn(
            generator_type,
            [
                CMakeGeneratorType.NINJA,
                CMakeGeneratorType.MINGW_MAKEFILES,
                CMakeGeneratorType.UNIX_MAKEFILES
            ]
        )

    def test_select_generator_for_compiler_gcc_linux(self) -> None:
        """Test select_generator_for_compiler for GCC on Linux."""
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.GCC,
            target_platform=TargetPlatform.LINUX
        )

        self.assertIn(
            generator_type,
            [CMakeGeneratorType.NINJA, CMakeGeneratorType.UNIX_MAKEFILES]
        )

    def test_select_generator_for_compiler_clang_macos(self) -> None:
        """Test select_generator_for_compiler for Clang on macOS."""
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.CLANG,
            target_platform=TargetPlatform.MACOS
        )

        self.assertIn(
            generator_type,
            [CMakeGeneratorType.XCODE, CMakeGeneratorType.NINJA, CMakeGeneratorType.UNIX_MAKEFILES]
        )

    def test_select_generator_for_compiler_unknown_combination(self) -> None:
        """Test select_generator_for_compiler with unknown combination."""
        # Test a combination that might not have specific mappings
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.GCC,
            target_platform=TargetPlatform.WINDOWS
        )

        # Should fall back to platform default
        self.assertIsNotNone(generator_type)

    def test_select_generator_for_compiler_prefer_multi_config(self) -> None:
        """Test select_generator_for_compiler with multi-config preference."""
        generator_type = self.selector.select_generator_for_compiler(
            compiler_type=CompilerType.MSVC,
            target_platform=TargetPlatform.WINDOWS,
            prefer_multi_config=True
        )

        # Should return a multi-config generator
        self.assertTrue(
            self.selector._GENERATOR_INFO[generator_type].supports_multi_config
        )

    def test_select_generator_for_platform_windows(self) -> None:
        """Test select_generator_for_platform for Windows."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.WINDOWS
        )

        self.assertIn(
            generator_type,
            [
                CMakeGeneratorType.VISUAL_STUDIO_17_2022,
                CMakeGeneratorType.NINJA
            ]
        )

    def test_select_generator_for_platform_linux(self) -> None:
        """Test select_generator_for_platform for Linux."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.LINUX
        )

        self.assertEqual(generator_type, CMakeGeneratorType.NINJA)

    def test_select_generator_for_platform_macos(self) -> None:
        """Test select_generator_for_platform for macOS."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.MACOS
        )

        self.assertIn(
            generator_type,
            [CMakeGeneratorType.XCODE, CMakeGeneratorType.NINJA]
        )

    def test_select_generator_for_platform_wasm(self) -> None:
        """Test select_generator_for_platform for WASM."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.WASM
        )

        self.assertEqual(generator_type, CMakeGeneratorType.NINJA)

    def test_select_generator_for_platform_android(self) -> None:
        """Test select_generator_for_platform for Android."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.ANDROID
        )

        self.assertEqual(generator_type, CMakeGeneratorType.NINJA)

    def test_select_generator_for_platform_ios(self) -> None:
        """Test select_generator_for_platform for iOS."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.IOS
        )

        self.assertIn(
            generator_type,
            [CMakeGeneratorType.XCODE, CMakeGeneratorType.NINJA]
        )

    def test_select_generator_for_platform_prefer_multi_config(self) -> None:
        """Test select_generator_for_platform with multi-config preference."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.WINDOWS,
            prefer_multi_config=True
        )

        # Should prefer multi-config generators
        self.assertTrue(
            self.selector._GENERATOR_INFO[generator_type].supports_multi_config
        )

    def test_select_generator_for_platform_prefer_native(self) -> None:
        """Test select_generator_for_platform with native preference."""
        generator_type = self.selector.select_generator_for_platform(
            target_platform=TargetPlatform.WINDOWS,
            prefer_native=True
        )

        # Should prefer native generators (Visual Studio on Windows)
        self.assertIn(
            generator_type,
            [
                CMakeGeneratorType.VISUAL_STUDIO_17_2022,
                CMakeGeneratorType.NINJA
            ]
        )

    def test_validate_generator_ninja_linux(self) -> None:
        """Test validate_generator for Ninja on Linux."""
        result = self.selector.validate_generator(
            generator_type=CMakeGeneratorType.NINJA,
            target_platform=TargetPlatform.LINUX
        )

        self.assertIsInstance(result, dict)
        self.assertIn("is_valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)
        self.assertIsInstance(result["is_valid"], bool)
        self.assertIsInstance(result["errors"], list)
        self.assertIsInstance(result["warnings"], list)

    def test_validate_generator_visual_studio_windows(self) -> None:
        """Test validate_generator for Visual Studio on Windows."""
        result = self.selector.validate_generator(
            generator_type=CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            target_platform=TargetPlatform.WINDOWS
        )

        self.assertIsInstance(result, dict)
        self.assertIn("is_valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)

    def test_validate_generator_xcode_macos(self) -> None:
        """Test validate_generator for Xcode on macOS."""
        result = self.selector.validate_generator(
            generator_type=CMakeGeneratorType.XCODE,
            target_platform=TargetPlatform.MACOS
        )

        self.assertIsInstance(result, dict)
        self.assertIn("is_valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)

    def test_validate_generator_invalid_platform_combination(self) -> None:
        """Test validate_generator with invalid platform combination."""
        result = self.selector.validate_generator(
            generator_type=CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            target_platform=TargetPlatform.LINUX
        )

        # Visual Studio is not supported on Linux
        self.assertFalse(result["is_valid"])
        self.assertTrue(len(result["errors"]) > 0)

    def test_get_generator_info_ninja(self) -> None:
        """Test get_generator_info for Ninja."""
        info = self.selector.get_generator_info(CMakeGeneratorType.NINJA)

        self.assertIsNotNone(info)
        self.assertIsInstance(info, GeneratorInfo)
        self.assertEqual(info.name, "Ninja")
        self.assertEqual(info.generator_type, CMakeGeneratorType.NINJA)
        self.assertFalse(info.supports_multi_config)
        self.assertIn(CompilerType.GCC, info.preferred_for)
        self.assertIn(CompilerType.CLANG, info.preferred_for)

    def test_get_generator_info_visual_studio(self) -> None:
        """Test get_generator_info for Visual Studio."""
        info = self.selector.get_generator_info(CMakeGeneratorType.VISUAL_STUDIO_17_2022)

        self.assertIsNotNone(info)
        self.assertIsInstance(info, GeneratorInfo)
        self.assertEqual(info.name, "Visual Studio 17 2022")
        self.assertEqual(info.generator_type, CMakeGeneratorType.VISUAL_STUDIO_17_2022)
        self.assertTrue(info.supports_multi_config)
        self.assertTrue(info.requires_toolchain)

    def test_get_generator_info_xcode(self) -> None:
        """Test get_generator_info for Xcode."""
        info = self.selector.get_generator_info(CMakeGeneratorType.XCODE)

        self.assertIsNotNone(info)
        self.assertIsInstance(info, GeneratorInfo)
        self.assertEqual(info.name, "Xcode")
        self.assertEqual(info.generator_type, CMakeGeneratorType.XCODE)
        self.assertTrue(info.supports_multi_config)
        self.assertTrue(info.requires_toolchain)

    def test_list_available_generators_all(self) -> None:
        """Test list_available_generators without platform filter."""
        generators = self.selector.list_available_generators()

        self.assertIsInstance(generators, list)
        self.assertTrue(len(generators) > 0)
        for gen in generators:
            self.assertIsInstance(gen, GeneratorInfo)

    def test_list_available_generators_windows(self) -> None:
        """Test list_available_generators with Windows filter."""
        generators = self.selector.list_available_generators(
            target_platform=TargetPlatform.WINDOWS
        )

        self.assertIsInstance(generators, list)
        self.assertTrue(len(generators) > 0)
        for gen in generators:
            self.assertIsInstance(gen, GeneratorInfo)
            self.assertIn(TargetPlatform.WINDOWS, gen.supported_platforms)

    def test_list_available_generators_linux(self) -> None:
        """Test list_available_generators with Linux filter."""
        generators = self.selector.list_available_generators(
            target_platform=TargetPlatform.LINUX
        )

        self.assertIsInstance(generators, list)
        self.assertTrue(len(generators) > 0)
        for gen in generators:
            self.assertIsInstance(gen, GeneratorInfo)
            self.assertIn(TargetPlatform.LINUX, gen.supported_platforms)

    def test_list_available_generators_macos(self) -> None:
        """Test list_available_generators with macOS filter."""
        generators = self.selector.list_available_generators(
            target_platform=TargetPlatform.MACOS
        )

        self.assertIsInstance(generators, list)
        self.assertTrue(len(generators) > 0)
        for gen in generators:
            self.assertIsInstance(gen, GeneratorInfo)
            self.assertIn(TargetPlatform.MACOS, gen.supported_platforms)

    def test_generator_info_to_dict(self) -> None:
        """Test GeneratorInfo.to_dict method."""
        info = self.selector.get_generator_info(CMakeGeneratorType.NINJA)
        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertIn("name", info_dict)
        self.assertIn("generator_type", info_dict)
        self.assertIn("supports_multi_config", info_dict)
        self.assertIn("preferred_for", info_dict)
        self.assertIn("supported_platforms", info_dict)
        self.assertIn("requires_toolchain", info_dict)
        self.assertIn("description", info_dict)

    def test_generator_selection_result_to_dict(self) -> None:
        """Test GeneratorSelectionResult.to_dict method."""
        result = self.selector.select_generator(
            compiler_type="gcc",
            target_platform="linux"
        )
        result_dict = result.to_dict()

        self.assertIsInstance(result_dict, dict)
        self.assertIn("generator", result_dict)
        self.assertIn("generator_type", result_dict)
        self.assertIn("compiler_type", result_dict)
        self.assertIn("target_platform", result_dict)
        self.assertIn("fallback_used", result_dict)
        self.assertIn("warnings", result_dict)

    def test_all_generator_types_have_info(self) -> None:
        """Test that all generator types have associated info."""
        for gen_type in CMakeGeneratorType:
            info = self.selector.get_generator_info(gen_type)
            self.assertIsNotNone(
                info,
                f"Generator type {gen_type} should have associated info"
            )
            self.assertIsInstance(info, GeneratorInfo)

    def test_all_compiler_types_have_mappings(self) -> None:
        """Test that all compiler types have generator mappings."""
        # Test a subset of compiler types with common platforms
        test_combinations = [
            (CompilerType.MSVC, TargetPlatform.WINDOWS),
            (CompilerType.GCC, TargetPlatform.LINUX),
            (CompilerType.CLANG, TargetPlatform.MACOS),
            (CompilerType.EMSCRIPTEN, TargetPlatform.WASM),
            (CompilerType.ANDROID_NDK, TargetPlatform.ANDROID),
        ]

        for compiler_type, platform in test_combinations:
            generator_type = self.selector.select_generator_for_compiler(
                compiler_type=compiler_type,
                target_platform=platform
            )
            self.assertIsNotNone(
                generator_type,
                f"Compiler {compiler_type} on {platform} should have a generator"
            )

    def test_all_platforms_have_defaults(self) -> None:
        """Test that all platforms have default generators."""
        for platform in TargetPlatform:
            default = self.selector._PLATFORM_DEFAULTS.get(platform)
            self.assertIsNotNone(
                default,
                f"Platform {platform} should have a default generator"
            )
            self.assertIsInstance(default, CMakeGeneratorType)

    @patch('shutil.which')
    def test_check_generator_executable_ninja(self, mock_which: Mock) -> None:
        """Test _check_generator_executable for Ninja."""
        mock_which.return_value = "/usr/bin/ninja"

        result = self.selector._check_generator_executable(CMakeGeneratorType.NINJA)

        self.assertTrue(result)
        mock_which.assert_called_once_with("ninja")

    @patch('shutil.which')
    def test_check_generator_executable_ninja_not_found(self, mock_which: Mock) -> None:
        """Test _check_generator_executable when Ninja is not found."""
        mock_which.return_value = None

        result = self.selector._check_generator_executable(CMakeGeneratorType.NINJA)

        self.assertFalse(result)
        mock_which.assert_called_once_with("ninja")

    @patch('shutil.which')
    def test_check_generator_executable_xcode(self, mock_which: Mock) -> None:
        """Test _check_generator_executable for Xcode."""
        mock_which.return_value = "/usr/bin/xcodebuild"

        result = self.selector._check_generator_executable(CMakeGeneratorType.XCODE)

        self.assertTrue(result)
        mock_which.assert_called_once_with("xcodebuild")

    @patch('shutil.which')
    def test_check_generator_executable_make(self, mock_which: Mock) -> None:
        """Test _check_generator_executable for Unix Makefiles."""
        mock_which.return_value = "/usr/bin/make"

        result = self.selector._check_generator_executable(
            CMakeGeneratorType.UNIX_MAKEFILES
        )

        self.assertTrue(result)
        mock_which.assert_called_once_with("make")

    @patch('shutil.which')
    def test_check_toolchain_availability_msvc(self, mock_which: Mock) -> None:
        """Test _check_toolchain_availability for MSVC."""
        mock_which.return_value = "C:\\Program Files\\Microsoft Visual Studio\\cl.exe"

        result = self.selector._check_toolchain_availability(
            CMakeGeneratorType.VISUAL_STUDIO_17_2022,
            TargetPlatform.WINDOWS
        )

        self.assertTrue(result)
        mock_which.assert_called_once_with("cl")

    @patch('shutil.which')
    def test_check_toolchain_availability_xcode(self, mock_which: Mock) -> None:
        """Test _check_toolchain_availability for Xcode."""
        mock_which.return_value = "/usr/bin/clang"

        result = self.selector._check_toolchain_availability(
            CMakeGeneratorType.XCODE,
            TargetPlatform.MACOS
        )

        self.assertTrue(result)
        mock_which.assert_called_once_with("clang")

    def test_is_primary_generator(self) -> None:
        """Test _is_primary_generator method."""
        # Test primary generator
        is_primary = self.selector._is_primary_generator(
            CompilerType.MSVC,
            TargetPlatform.WINDOWS,
            CMakeGeneratorType.VISUAL_STUDIO_17_2022
        )
        self.assertTrue(is_primary)

        # Test non-primary generator
        is_primary = self.selector._is_primary_generator(
            CompilerType.MSVC,
            TargetPlatform.WINDOWS,
            CMakeGeneratorType.NINJA
        )
        self.assertFalse(is_primary)

    def test_get_fallback_generator(self) -> None:
        """Test _get_fallback_generator method."""
        # Test fallback from Visual Studio to Ninja
        fallback = self.selector._get_fallback_generator(
            CompilerType.MSVC,
            TargetPlatform.WINDOWS,
            CMakeGeneratorType.VISUAL_STUDIO_17_2022
        )

        # Should return next in list or platform default
        self.assertIsNotNone(fallback)
        self.assertIsInstance(fallback, CMakeGeneratorType)

    def test_compiler_type_enum_values(self) -> None:
        """Test CompilerType enum values."""
        self.assertEqual(CompilerType.MSVC.value, "msvc")
        self.assertEqual(CompilerType.MINGW_GCC.value, "mingw_gcc")
        self.assertEqual(CompilerType.GCC.value, "gcc")
        self.assertEqual(CompilerType.CLANG.value, "clang")
        self.assertEqual(CompilerType.EMSCRIPTEN.value, "emscripten")
        self.assertEqual(CompilerType.ANDROID_NDK.value, "android_ndk")

    def test_target_platform_enum_values(self) -> None:
        """Test TargetPlatform enum values."""
        self.assertEqual(TargetPlatform.WINDOWS.value, "windows")
        self.assertEqual(TargetPlatform.LINUX.value, "linux")
        self.assertEqual(TargetPlatform.MACOS.value, "macos")
        self.assertEqual(TargetPlatform.WASM.value, "wasm")
        self.assertEqual(TargetPlatform.ANDROID.value, "android")
        self.assertEqual(TargetPlatform.IOS.value, "ios")

    def test_cmake_generator_type_enum_values(self) -> None:
        """Test CMakeGeneratorType enum values."""
        self.assertEqual(CMakeGeneratorType.NINJA.value, "Ninja")
        self.assertEqual(CMakeGeneratorType.NINJA_MULTI_CONFIG.value, "Ninja Multi-Config")
        self.assertEqual(CMakeGeneratorType.VISUAL_STUDIO_17_2022.value, "Visual Studio 17 2022")
        self.assertEqual(CMakeGeneratorType.UNIX_MAKEFILES.value, "Unix Makefiles")
        self.assertEqual(CMakeGeneratorType.XCODE.value, "Xcode")


if __name__ == '__main__':
    unittest.main()
