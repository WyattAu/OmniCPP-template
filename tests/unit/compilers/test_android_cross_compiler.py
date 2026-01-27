"""
Unit tests for Android Cross-Compiler Detection Module

This module contains comprehensive tests for Android cross-compiler detection
system, including NDK detection, toolchain detection, and validation.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, mock_open

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.android_cross_compiler import (
    AndroidCrossCompiler,
    NDKInfo,
    ToolchainInfo,
    CrossCompilerInfo,
    ICrossCompiler
)


class TestNDKInfo(unittest.TestCase):
    """Test cases for NDKInfo dataclass"""

    def test_ndk_info_creation(self):
        """Test creating NDKInfo instance"""
        info = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertEqual(info.version, "25.2.9519653")
        self.assertEqual(info.root_path, r"C:\Android\Sdk\ndk\25.2.9519653")
        self.assertEqual(info.toolchain_path, r"C:\Android\Sdk\ndk\25.2.9519653\toolchains")
        self.assertEqual(info.platforms_path, r"C:\Android\Sdk\ndk\25.2.9519653\platforms")
        self.assertEqual(info.sysroot_path, r"C:\Android\Sdk\ndk\25.2.9519653\sysroot")

    def test_ndk_info_to_dict(self):
        """Test converting NDKInfo to dictionary"""
        info = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["version"], "25.2.9519653")
        self.assertEqual(info_dict["root_path"], r"C:\Android\Sdk\ndk\25.2.9519653")
        self.assertEqual(info_dict["toolchain_path"], r"C:\Android\Sdk\ndk\25.2.9519653\toolchains")
        self.assertEqual(info_dict["platforms_path"], r"C:\Android\Sdk\ndk\25.2.9519653\platforms")
        self.assertEqual(info_dict["sysroot_path"], r"C:\Android\Sdk\ndk\25.2.9519653\sysroot")

    @patch('os.path.exists')
    def test_ndk_info_is_valid(self, mock_exists):
        """Test NDKInfo.is_valid() with all paths present"""
        mock_exists.return_value = True

        info = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertTrue(info.is_valid())

    @patch('os.path.exists')
    def test_ndk_info_is_invalid(self, mock_exists):
        """Test NDKInfo.is_valid() with missing paths"""
        # Mock exists to return False for some paths
        def exists_side_effect(path):
            return "root_path" in path or "toolchain_path" in path

        mock_exists.side_effect = exists_side_effect

        info = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertFalse(info.is_valid())


class TestToolchainInfo(unittest.TestCase):
    """Test cases for ToolchainInfo dataclass"""

    def test_toolchain_info_creation(self):
        """Test creating ToolchainInfo instance"""
        info = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertEqual(info.name, "arm64-v8a")
        self.assertEqual(info.clang, r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang")
        self.assertEqual(info.clangxx, r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++")
        self.assertEqual(info.ar, r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar")
        self.assertEqual(info.strip, r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip")
        self.assertEqual(info.sysroot, r"C:\Android\Sdk\ndk\25.2.9519653\sysroot")

    def test_toolchain_info_to_dict(self):
        """Test converting ToolchainInfo to dictionary"""
        info = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["name"], "arm64-v8a")
        self.assertEqual(info_dict["clang"], r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang")
        self.assertEqual(info_dict["clangxx"], r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++")
        self.assertEqual(info_dict["ar"], r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar")
        self.assertEqual(info_dict["strip"], r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip")
        self.assertEqual(info_dict["sysroot"], r"C:\Android\Sdk\ndk\25.2.9519653\sysroot")

    @patch('os.path.exists')
    def test_toolchain_info_is_valid(self, mock_exists):
        """Test ToolchainInfo.is_valid() with all executables present"""
        mock_exists.return_value = True

        info = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertTrue(info.is_valid())

    @patch('os.path.exists')
    def test_toolchain_info_is_invalid(self, mock_exists):
        """Test ToolchainInfo.is_valid() with missing executables"""
        # Mock exists to return False for some paths
        def exists_side_effect(path):
            return "clang" in path or "clangxx" in path

        mock_exists.side_effect = exists_side_effect

        info = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.assertFalse(info.is_valid())


class TestCrossCompilerInfo(unittest.TestCase):
    """Test cases for CrossCompilerInfo dataclass"""

    def test_cross_compiler_info_creation(self):
        """Test creating CrossCompilerInfo instance"""
        info = CrossCompilerInfo(
            target_platform="android",
            target_architecture="arm64-v8a",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot",
            compilers={
                "cc": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
                "cxx": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
                "ar": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
                "strip": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip"
            },
            cmake_generator="Ninja",
            metadata={
                "ndk_version": "25.2.9519653",
                "ndk_root": r"C:\Android\Sdk\ndk\25.2.9519653",
                "target_architecture": "arm64-v8a"
            }
        )

        self.assertEqual(info.target_platform, "android")
        self.assertEqual(info.target_architecture, "arm64-v8a")
        self.assertEqual(info.cmake_generator, "Ninja")
        self.assertIn("cc", info.compilers)
        self.assertIn("cxx", info.compilers)
        self.assertIn("ar", info.compilers)
        self.assertIn("strip", info.compilers)

    def test_cross_compiler_info_to_dict(self):
        """Test converting CrossCompilerInfo to dictionary"""
        info = CrossCompilerInfo(
            target_platform="android",
            target_architecture="arm64-v8a",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot",
            compilers={
                "cc": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
                "cxx": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
                "ar": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
                "strip": r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip"
            },
            cmake_generator="Ninja",
            metadata={
                "ndk_version": "25.2.9519653",
                "ndk_root": r"C:\Android\Sdk\ndk\25.2.9519653",
                "target_architecture": "arm64-v8a"
            }
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["target_platform"], "android")
        self.assertEqual(info_dict["target_architecture"], "arm64-v8a")
        self.assertEqual(info_dict["cmake_generator"], "Ninja")
        self.assertIn("compilers", info_dict)
        self.assertIn("metadata", info_dict)

    @patch('os.path.exists')
    def test_cross_compiler_info_is_valid(self, mock_exists):
        """Test CrossCompilerInfo.is_valid() with valid path"""
        mock_exists.return_value = True

        info = CrossCompilerInfo(
            target_platform="android",
            target_architecture="arm64-v8a",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )

        self.assertTrue(info.is_valid())

    @patch('os.path.exists')
    def test_cross_compiler_info_is_invalid(self, mock_exists):
        """Test CrossCompilerInfo.is_valid() with invalid path"""
        mock_exists.return_value = False

        info = CrossCompilerInfo(
            target_platform="android",
            target_architecture="arm64-v8a",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )

        self.assertFalse(info.is_valid())


class TestAndroidCrossCompiler(unittest.TestCase):
    """Test cases for AndroidCrossCompiler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = AndroidCrossCompiler()

    def test_initialization_default(self):
        """Test AndroidCrossCompiler initialization with default architecture"""
        compiler = AndroidCrossCompiler()
        self.assertEqual(compiler._target_architecture, "arm64-v8a")
        self.assertIsNone(compiler._ndk)
        self.assertIsNone(compiler._toolchain)
        self.assertIsNone(compiler._info)

    def test_initialization_custom_architecture(self):
        """Test AndroidCrossCompiler initialization with custom architecture"""
        compiler = AndroidCrossCompiler("armeabi-v7a")
        self.assertEqual(compiler._target_architecture, "armeabi-v7a")

    def test_supported_targets(self):
        """Test supported target architectures"""
        self.assertIn("arm64-v8a", AndroidCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("armeabi-v7a", AndroidCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("x86_64", AndroidCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("x86", AndroidCrossCompiler.SUPPORTED_TARGETS)

    def test_ndk_paths(self):
        """Test NDK search paths"""
        self.assertIsInstance(AndroidCrossCompiler.NDK_PATHS, list)
        self.assertGreater(len(AndroidCrossCompiler.NDK_PATHS), 0)

    def test_arch_triple_map(self):
        """Test architecture to LLVM triple mapping"""
        self.assertEqual(
            AndroidCrossCompiler.ARCH_TRIPLE_MAP["arm64-v8a"],
            "aarch64-linux-android"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_TRIPLE_MAP["armeabi-v7a"],
            "armv7a-linux-androideabi"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_TRIPLE_MAP["x86_64"],
            "x86_64-linux-android"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_TRIPLE_MAP["x86"],
            "i686-linux-android"
        )

    def test_arch_processor_map(self):
        """Test architecture to CMake processor mapping"""
        self.assertEqual(
            AndroidCrossCompiler.ARCH_PROCESSOR_MAP["arm64-v8a"],
            "aarch64"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_PROCESSOR_MAP["armeabi-v7a"],
            "armv7-a"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_PROCESSOR_MAP["x86_64"],
            "x86_64"
        )
        self.assertEqual(
            AndroidCrossCompiler.ARCH_PROCESSOR_MAP["x86"],
            "i686"
        )

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_detect_ndk_from_env(self, mock_env_get, mock_exists):
        """Test detecting NDK from environment variable"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True

        ndk = self.compiler.detect_ndk()

        self.assertIsNotNone(ndk)
        self.assertEqual(ndk.root_path, r"C:\Android\Sdk\ndk\25.2.9519653")

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_detect_ndk_not_found(self, mock_env_get, mock_exists):
        """Test detecting NDK when not found"""
        mock_env_get.return_value = None
        mock_exists.return_value = False

        ndk = self.compiler.detect_ndk()

        self.assertIsNone(ndk)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_ndk_from_paths(self, mock_listdir, mock_env_get, mock_exists):
        """Test detecting NDK from standard paths"""
        mock_env_get.return_value = None
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        ndk = self.compiler.detect_ndk()

        self.assertIsNotNone(ndk)

    @patch('os.path.exists')
    def test_detect_toolchain(self, mock_exists):
        """Test detecting toolchain for architecture"""
        mock_exists.return_value = True

        # Set up NDK info
        self.compiler._ndk = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        toolchain = self.compiler.detect_toolchain()

        self.assertIsNotNone(toolchain)
        self.assertEqual(toolchain.name, "arm64-v8a")

    @patch('os.path.exists')
    def test_detect_toolchain_no_ndk(self, mock_exists):
        """Test detecting toolchain when NDK not detected"""
        mock_exists.return_value = True

        toolchain = self.compiler.detect_toolchain()

        self.assertIsNone(toolchain)

    def test_detect_target_triple(self):
        """Test detecting target triple for architecture"""
        triple = self.compiler.detect_target_triple()

        self.assertEqual(triple, "aarch64-linux-android")

    def test_detect_target_triple_unsupported(self):
        """Test detecting target triple for unsupported architecture"""
        compiler = AndroidCrossCompiler("invalid-arch")
        triple = compiler.detect_target_triple()

        self.assertIsNone(triple)

    @patch('os.path.exists')
    def test_setup_environment(self, mock_exists):
        """Test setting up Android cross-compilation environment"""
        mock_exists.return_value = True

        # Set up NDK and toolchain
        self.compiler._ndk = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.compiler._toolchain = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        env = self.compiler.setup_environment()

        self.assertIsInstance(env, dict)
        self.assertEqual(env["CMAKE_SYSTEM_NAME"], "Android")
        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "aarch64")
        self.assertEqual(env["CMAKE_ANDROID_NDK"], r"C:\Android\Sdk\ndk\25.2.9519653")
        self.assertEqual(env["CMAKE_ANDROID_STL"], "c++_shared")
        self.assertEqual(env["CMAKE_ANDROID_ARCH_ABI"], "arm64-v8a")
        self.assertEqual(env["CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION"], "clang")
        self.assertEqual(env["CMAKE_GENERATOR"], "Ninja")
        self.assertEqual(env["CMAKE_ANDROID_ARM_MODE"], "arm")
        self.assertEqual(env["CMAKE_ANDROID_ARM_NEON"], "ON")

    @patch('os.path.exists')
    def test_setup_environment_armeabi_v7a(self, mock_exists):
        """Test setting up environment for armeabi-v7a"""
        mock_exists.return_value = True

        compiler = AndroidCrossCompiler("armeabi-v7a")

        # Set up NDK and toolchain
        compiler._ndk = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        compiler._toolchain = ToolchainInfo(
            name="armeabi-v7a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        env = compiler.setup_environment()

        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "armv7-a")
        self.assertEqual(env["CMAKE_ANDROID_ARCH_ABI"], "armeabi-v7a")
        self.assertNotIn("CMAKE_ANDROID_ARM_MODE", env)
        self.assertNotIn("CMAKE_ANDROID_ARM_NEON", env)

    def test_setup_environment_no_ndk(self):
        """Test setup_environment raises error when NDK not detected"""
        with self.assertRaises(RuntimeError) as context:
            self.compiler.setup_environment()

        self.assertIn("NDK or toolchain not detected", str(context.exception))

    def test_get_cmake_generator(self):
        """Test getting CMake generator"""
        generator = self.compiler.get_cmake_generator()
        self.assertEqual(generator, "Ninja")

    @patch('os.path.exists')
    def test_validate_success(self, mock_exists):
        """Test successful validation of Android cross-compiler"""
        mock_exists.return_value = True

        # Set up NDK and toolchain
        self.compiler._ndk = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.compiler._toolchain = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        result = self.compiler.validate()

        self.assertTrue(result)

    @patch('os.path.exists')
    def test_validate_failure(self, mock_exists):
        """Test failed validation of Android cross-compiler"""
        # Mock exists to return False for some paths
        def exists_side_effect(path):
            return "root_path" in path or "clang" in path

        mock_exists.side_effect = exists_side_effect

        # Set up NDK and toolchain
        self.compiler._ndk = NDKInfo(
            version="25.2.9519653",
            root_path=r"C:\Android\Sdk\ndk\25.2.9519653",
            toolchain_path=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains",
            platforms_path=r"C:\Android\Sdk\ndk\25.2.9519653\platforms",
            sysroot_path=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        self.compiler._toolchain = ToolchainInfo(
            name="arm64-v8a",
            clang=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang",
            clangxx=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\clang++",
            ar=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-ar",
            strip=r"C:\Android\Sdk\ndk\25.2.9519653\toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-strip",
            sysroot=r"C:\Android\Sdk\ndk\25.2.9519653\sysroot"
        )

        result = self.compiler.validate()

        self.assertFalse(result)

    def test_validate_no_ndk(self):
        """Test validate returns False when NDK not detected"""
        result = self.compiler.validate()
        self.assertFalse(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_success(self, mock_listdir, mock_env_get, mock_exists):
        """Test successful detection of Android cross-compiler"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = self.compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_platform, "android")
        self.assertEqual(result.target_architecture, "arm64-v8a")
        self.assertEqual(result.cmake_generator, "Ninja")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_armeabi_v7a(self, mock_listdir, mock_env_get, mock_exists):
        """Test detection of armeabi-v7a cross-compiler"""
        compiler = AndroidCrossCompiler("armeabi-v7a")

        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_architecture, "armeabi-v7a")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_x86_64(self, mock_listdir, mock_env_get, mock_exists):
        """Test detection of x86_64 cross-compiler"""
        compiler = AndroidCrossCompiler("x86_64")

        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_architecture, "x86_64")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_x86(self, mock_listdir, mock_env_get, mock_exists):
        """Test detection of x86 cross-compiler"""
        compiler = AndroidCrossCompiler("x86")

        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_architecture, "x86")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_unsupported_architecture(self, mock_listdir, mock_env_get, mock_exists):
        """Test detection with unsupported architecture"""
        compiler = AndroidCrossCompiler("invalid-arch")

        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = compiler.detect()

        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_detect_no_ndk(self, mock_env_get, mock_exists):
        """Test detection when NDK not found"""
        mock_env_get.return_value = None
        mock_exists.return_value = False

        result = self.compiler.detect()

        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_detect_creates_cross_compiler_info(self, mock_listdir, mock_env_get, mock_exists):
        """Test that detect creates proper CrossCompilerInfo"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = self.compiler.detect()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, CrossCompilerInfo)
        self.assertIn("cc", result.compilers)
        self.assertIn("cxx", result.compilers)
        self.assertIn("ar", result.compilers)
        self.assertIn("strip", result.compilers)
        self.assertIn("ndk_version", result.metadata)
        self.assertIn("ndk_root", result.metadata)
        self.assertIn("target_architecture", result.metadata)
        self.assertIn("llvm_triple", result.metadata)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_get_host_tag_windows(self, mock_listdir, mock_env_get, mock_exists):
        """Test getting host tag for Windows"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        result = self.compiler.detect()

        self.assertIsNotNone(result)
        # Verify toolchain path includes windows-x86_64
        self.assertIn("windows-x86_64", result.toolchain_path)


class TestICrossCompilerInterface(unittest.TestCase):
    """Test cases for ICrossCompiler interface"""

    def test_interface_is_abstract(self):
        """Test that ICrossCompiler is abstract"""
        with self.assertRaises(TypeError):
            ICrossCompiler()


class TestAndroidCrossCompilerIntegration(unittest.TestCase):
    """Integration tests for AndroidCrossCompiler"""

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_full_detection_workflow(self, mock_listdir, mock_env_get, mock_exists):
        """Test complete detection workflow"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        compiler = AndroidCrossCompiler("arm64-v8a")

        # Detect
        info = compiler.detect()
        self.assertIsNotNone(info)

        # Validate
        self.assertTrue(compiler.validate())

        # Setup environment
        env = compiler.setup_environment()
        self.assertIsInstance(env, dict)

        # Get CMake generator
        generator = compiler.get_cmake_generator()
        self.assertEqual(generator, "Ninja")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_all_architectures_detection(self, mock_listdir, mock_env_get, mock_exists):
        """Test detection for all supported architectures"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        architectures = ["arm64-v8a", "armeabi-v7a", "x86_64", "x86"]

        for arch in architectures:
            compiler = AndroidCrossCompiler(arch)
            info = compiler.detect()

            self.assertIsNotNone(info, f"Failed to detect {arch}")
            self.assertEqual(info.target_architecture, arch)
            self.assertTrue(compiler.validate(), f"Failed to validate {arch}")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('os.listdir')
    def test_environment_setup_for_all_architectures(self, mock_listdir, mock_env_get, mock_exists):
        """Test environment setup for all supported architectures"""
        mock_env_get.return_value = r"C:\Android\Sdk\ndk\25.2.9519653"
        mock_exists.return_value = True
        mock_listdir.return_value = ["25.2.9519653"]

        architectures = ["arm64-v8a", "armeabi-v7a", "x86_64", "x86"]

        for arch in architectures:
            compiler = AndroidCrossCompiler(arch)
            compiler.detect()

            env = compiler.setup_environment()

            self.assertEqual(env["CMAKE_SYSTEM_NAME"], "Android")
            self.assertEqual(env["CMAKE_ANDROID_ARCH_ABI"], arch)
            self.assertEqual(env["CMAKE_GENERATOR"], "Ninja")


if __name__ == '__main__':
    unittest.main()
