"""
Unit tests for Linux Cross-Compiler Detection

Tests cover:
- Toolchain detection (x86_64-linux-gnu, aarch64-linux-gnu, arm-linux-gnueabihf, arm-linux-gnueabi)
- Sysroot detection
- Target triple detection
- Environment setup
- CMake generator selection
- Validation
- Full detection workflow
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.linux_cross_compiler import (
    LinuxCrossCompiler,
    ToolchainInfo,
    CrossCompilerInfo,
    ICrossCompiler
)


class TestToolchainInfo(unittest.TestCase):
    """Test cases for ToolchainInfo dataclass"""

    def test_toolchain_info_creation(self):
        """Test ToolchainInfo dataclass creation"""
        toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\msys64\\mingw64\\x86_64-linux-gnu"
        )

        self.assertEqual(toolchain.name, "x86_64-linux-gnu")
        self.assertEqual(toolchain.gcc, "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe")
        self.assertEqual(toolchain.gxx, "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe")
        self.assertEqual(toolchain.ar, "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe")
        self.assertEqual(toolchain.strip, "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe")
        self.assertEqual(toolchain.sysroot, "C:\\msys64\\mingw64\\x86_64-linux-gnu")

    def test_toolchain_info_to_dict(self):
        """Test ToolchainInfo to_dict method"""
        toolchain = ToolchainInfo(
            name="aarch64-linux-gnu",
            gcc="C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe",
            gxx="C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe",
            ar="C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc-ar.exe",
            strip="C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-strip.exe",
            sysroot="C:\\msys64\\mingw64\\aarch64-linux-gnu"
        )

        toolchain_dict = toolchain.to_dict()

        self.assertIsInstance(toolchain_dict, dict)
        self.assertEqual(toolchain_dict["name"], "aarch64-linux-gnu")
        self.assertEqual(toolchain_dict["gcc"], "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe")
        self.assertEqual(toolchain_dict["gxx"], "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe")
        self.assertEqual(toolchain_dict["ar"], "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc-ar.exe")
        self.assertEqual(toolchain_dict["strip"], "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-strip.exe")
        self.assertEqual(toolchain_dict["sysroot"], "C:\\msys64\\mingw64\\aarch64-linux-gnu")

    @patch('os.path.exists')
    def test_toolchain_info_is_valid(self, mock_exists):
        """Test ToolchainInfo is_valid method"""
        mock_exists.return_value = True

        toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\msys64\\mingw64\\x86_64-linux-gnu"
        )

        self.assertTrue(toolchain.is_valid())

    @patch('os.path.exists')
    def test_toolchain_info_is_invalid(self, mock_exists):
        """Test ToolchainInfo is_valid method with missing executables"""
        mock_exists.return_value = False

        toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\nonexistent\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\nonexistent\\x86_64-linux-gnu-g++.exe",
            ar="C:\\nonexistent\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\nonexistent\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\nonexistent\\x86_64-linux-gnu"
        )

        self.assertFalse(toolchain.is_valid())


class TestCrossCompilerInfo(unittest.TestCase):
    """Test cases for CrossCompilerInfo dataclass"""

    def test_cross_compiler_info_creation(self):
        """Test CrossCompilerInfo dataclass creation"""
        info = CrossCompilerInfo(
            target_platform="linux",
            target_architecture="x86_64-linux-gnu",
            toolchain_path="C:\\msys64\\mingw64\\bin",
            sysroot="C:\\msys64\\mingw64\\x86_64-linux-gnu",
            compilers={
                "cc": "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
                "cxx": "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
                "ar": "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
                "strip": "C:\\msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe"
            },
            cmake_generator="Ninja",
            metadata={
                "target_triple": "x86_64-linux-gnu",
                "toolchain_name": "x86_64-linux-gnu"
            }
        )

        self.assertEqual(info.target_platform, "linux")
        self.assertEqual(info.target_architecture, "x86_64-linux-gnu")
        self.assertEqual(info.toolchain_path, "C:\\msys64\\mingw64\\bin")
        self.assertEqual(info.sysroot, "C:\\msys64\\mingw64\\x86_64-linux-gnu")
        self.assertEqual(info.cmake_generator, "Ninja")
        self.assertIn("cc", info.compilers)
        self.assertIn("cxx", info.compilers)

    def test_cross_compiler_info_to_dict(self):
        """Test CrossCompilerInfo to_dict method"""
        info = CrossCompilerInfo(
            target_platform="linux",
            target_architecture="aarch64-linux-gnu",
            toolchain_path="C:\\msys64\\mingw64\\bin",
            sysroot="C:\\msys64\\mingw64\\aarch64-linux-gnu",
            compilers={
                "cc": "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe",
                "cxx": "C:\\msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe"
            },
            cmake_generator="Ninja",
            metadata={}
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["target_platform"], "linux")
        self.assertEqual(info_dict["target_architecture"], "aarch64-linux-gnu")
        self.assertEqual(info_dict["toolchain_path"], "C:\\msys64\\mingw64\\bin")
        self.assertEqual(info_dict["sysroot"], "C:\\msys64\\mingw64\\aarch64-linux-gnu")
        self.assertEqual(info_dict["cmake_generator"], "Ninja")

    @patch('os.path.exists')
    def test_cross_compiler_info_is_valid(self, mock_exists):
        """Test CrossCompilerInfo is_valid method"""
        mock_exists.return_value = True

        info = CrossCompilerInfo(
            target_platform="linux",
            target_architecture="x86_64-linux-gnu",
            toolchain_path="C:\\msys64\\mingw64\\bin",
            sysroot="C:\\msys64\\mingw64\\x86_64-linux-gnu",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )

        self.assertTrue(info.is_valid())

    @patch('os.path.exists')
    def test_cross_compiler_info_is_invalid(self, mock_exists):
        """Test CrossCompilerInfo is_valid method with missing path"""
        mock_exists.return_value = False

        info = CrossCompilerInfo(
            target_platform="linux",
            target_architecture="x86_64-linux-gnu",
            toolchain_path="C:\\nonexistent\\bin",
            sysroot="C:\\nonexistent\\x86_64-linux-gnu",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )

        self.assertFalse(info.is_valid())


class TestLinuxCrossCompilerInitialization(unittest.TestCase):
    """Test cases for LinuxCrossCompiler initialization"""

    def test_initialization_default_target(self):
        """Test initialization with default target architecture"""
        compiler = LinuxCrossCompiler()

        self.assertEqual(compiler._target_architecture, "x86_64-linux-gnu")
        self.assertIsNone(compiler._toolchain)
        self.assertIsNone(compiler._info)
        self.assertIsNotNone(compiler._logger)

    def test_initialization_custom_target(self):
        """Test initialization with custom target architecture"""
        compiler = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")

        self.assertEqual(compiler._target_architecture, "aarch64-linux-gnu")
        self.assertIsNone(compiler._toolchain)
        self.assertIsNone(compiler._info)

    def test_supported_targets(self):
        """Test supported target architectures"""
        self.assertIn("x86_64-linux-gnu", LinuxCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("aarch64-linux-gnu", LinuxCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("arm-linux-gnueabihf", LinuxCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("arm-linux-gnueabi", LinuxCrossCompiler.SUPPORTED_TARGETS)

    def test_toolchain_paths(self):
        """Test toolchain search paths"""
        self.assertIsInstance(LinuxCrossCompiler.TOOLCHAIN_PATHS, list)
        self.assertGreater(len(LinuxCrossCompiler.TOOLCHAIN_PATHS), 0)
        self.assertIn(r"C:\msys64\mingw64\bin", LinuxCrossCompiler.TOOLCHAIN_PATHS)
        self.assertIn(r"C:\msys64\ucrt64\bin", LinuxCrossCompiler.TOOLCHAIN_PATHS)


class TestToolchainDetection(unittest.TestCase):
    """Test cases for toolchain detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_toolchain_x86_64(self, mock_exists):
        """Test detection of x86_64-linux-gnu toolchain"""
        # Mock path existence for toolchain directory
        def exists_side_effect(path):
            return "C:\\test_msys64\\mingw64\\bin" in path

        mock_exists.side_effect = exists_side_effect

        # Override toolchain paths
        self.compiler.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]

        # Create mock toolchain
        mock_toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        with patch.object(self.compiler, '_check_toolchain', return_value=mock_toolchain):
            toolchain = self.compiler.detect_toolchain()

            self.assertIsNotNone(toolchain)
            self.assertEqual(toolchain.name, "x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_toolchain_aarch64(self, mock_exists):
        """Test detection of aarch64-linux-gnu toolchain"""
        compiler = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")

        # Mock path existence for toolchain directory
        def exists_side_effect(path):
            return "C:\\test_msys64\\mingw64\\bin" in path

        mock_exists.side_effect = exists_side_effect

        # Override toolchain paths
        compiler.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]

        # Create mock toolchain
        mock_toolchain = ToolchainInfo(
            name="aarch64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\aarch64-linux-gnu"
        )

        with patch.object(compiler, '_check_toolchain', return_value=mock_toolchain):
            toolchain = compiler.detect_toolchain()

            self.assertIsNotNone(toolchain)
            self.assertEqual(toolchain.name, "aarch64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_toolchain_not_found(self, mock_exists):
        """Test toolchain detection when toolchain not found"""
        mock_exists.return_value = False

        # Override toolchain paths
        self.compiler.TOOLCHAIN_PATHS = ["C:\\nonexistent\\bin"]

        with patch.object(self.compiler, '_check_toolchain', return_value=None):
            toolchain = self.compiler.detect_toolchain()

            self.assertIsNone(toolchain)

    @patch('os.path.exists')
    def test_check_toolchain_success(self, mock_exists):
        """Test _check_toolchain method with valid toolchain"""
        def exists_side_effect(path):
            # All executables and sysroot exist
            return True

        mock_exists.side_effect = exists_side_effect

        toolchain = self.compiler._check_toolchain(
            "C:\\test_msys64\\mingw64\\bin",
            "x86_64-linux-gnu"
        )

        self.assertIsNotNone(toolchain)
        self.assertEqual(toolchain.name, "x86_64-linux-gnu")
        self.assertIn("x86_64-linux-gnu-gcc.exe", toolchain.gcc)
        self.assertIn("x86_64-linux-gnu-g++.exe", toolchain.gxx)

    @patch('os.path.exists')
    def test_check_toolchain_missing_executables(self, mock_exists):
        """Test _check_toolchain method with missing executables"""
        def exists_side_effect(path):
            # Only some executables exist
            return "sysroot" in path

        mock_exists.side_effect = exists_side_effect

        toolchain = self.compiler._check_toolchain(
            "C:\\test_msys64\\mingw64\\bin",
            "x86_64-linux-gnu"
        )

        self.assertIsNone(toolchain)


class TestSysrootDetection(unittest.TestCase):
    """Test cases for sysroot detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_sysroot_success(self, mock_exists):
        """Test successful sysroot detection"""
        mock_exists.return_value = True

        # Create mock toolchain
        mock_toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        with patch.object(self.compiler, 'detect_toolchain', return_value=mock_toolchain):
            sysroot = self.compiler.detect_sysroot()

            self.assertIsNotNone(sysroot)
            self.assertEqual(sysroot, "C:\\test_msys64\\mingw64\\x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_sysroot_not_found(self, mock_exists):
        """Test sysroot detection when sysroot not found"""
        mock_exists.return_value = False

        # Create mock toolchain
        mock_toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        with patch.object(self.compiler, 'detect_toolchain', return_value=mock_toolchain):
            sysroot = self.compiler.detect_sysroot()

            self.assertIsNone(sysroot)

    @patch('os.path.exists')
    def test_detect_sysroot_no_toolchain(self, mock_exists):
        """Test sysroot detection when no toolchain detected"""
        with patch.object(self.compiler, 'detect_toolchain', return_value=None):
            sysroot = self.compiler.detect_sysroot()

            self.assertIsNone(sysroot)


class TestTargetTripleDetection(unittest.TestCase):
    """Test cases for target triple detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    def test_detect_target_triple_x86_64(self):
        """Test target triple detection for x86_64-linux-gnu"""
        target_triple = self.compiler.detect_target_triple()

        self.assertIsNotNone(target_triple)
        self.assertEqual(target_triple, "x86_64-linux-gnu")

    def test_detect_target_triple_aarch64(self):
        """Test target triple detection for aarch64-linux-gnu"""
        compiler = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")
        target_triple = compiler.detect_target_triple()

        self.assertIsNotNone(target_triple)
        self.assertEqual(target_triple, "aarch64-linux-gnu")

    def test_detect_target_triple_arm_gnueabihf(self):
        """Test target triple detection for arm-linux-gnueabihf"""
        compiler = LinuxCrossCompiler(target_architecture="arm-linux-gnueabihf")
        target_triple = compiler.detect_target_triple()

        self.assertIsNotNone(target_triple)
        self.assertEqual(target_triple, "arm-linux-gnueabihf")

    def test_detect_target_triple_unsupported(self):
        """Test target triple detection for unsupported architecture"""
        compiler = LinuxCrossCompiler(target_architecture="riscv64-linux-gnu")
        target_triple = compiler.detect_target_triple()

        self.assertIsNone(target_triple)


class TestEnvironmentSetup(unittest.TestCase):
    """Test cases for environment setup"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_setup_environment_success(self, mock_exists):
        """Test successful environment setup"""
        # Mock os.path.exists to return True for all paths
        mock_exists.return_value = True

        # Create mock toolchain
        self.compiler._toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        env = self.compiler.setup_environment()

        self.assertIsInstance(env, dict)
        self.assertEqual(env["CMAKE_SYSTEM_NAME"], "Linux")
        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "x86_64")
        self.assertEqual(env["CMAKE_C_COMPILER"], "C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe")
        self.assertEqual(env["CMAKE_CXX_COMPILER"], "C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe")
        self.assertEqual(env["CMAKE_AR"], "C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe")
        self.assertEqual(env["CMAKE_STRIP"], "C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe")
        self.assertEqual(env["CMAKE_GENERATOR"], "Ninja")
        self.assertEqual(env["CMAKE_SYSROOT"], "C:\\test_msys64\\mingw64\\x86_64-linux-gnu")
        self.assertEqual(env["CMAKE_FIND_ROOT_PATH"], "C:\\test_msys64\\mingw64\\x86_64-linux-gnu")
        self.assertEqual(env["CMAKE_FIND_ROOT_PATH_MODE_PROGRAM"], "NEVER")
        self.assertEqual(env["CMAKE_FIND_ROOT_PATH_MODE_LIBRARY"], "ONLY")
        self.assertEqual(env["CMAKE_FIND_ROOT_PATH_MODE_INCLUDE"], "ONLY")

    @patch('os.path.exists')
    def test_setup_environment_aarch64(self, mock_exists):
        """Test environment setup for aarch64 target"""
        mock_exists.return_value = True

        compiler = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")

        # Create mock toolchain
        compiler._toolchain = ToolchainInfo(
            name="aarch64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\aarch64-linux-gnu"
        )

        env = compiler.setup_environment()

        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "aarch64")
        self.assertEqual(env["CMAKE_C_COMPILER"], "C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe")
        self.assertEqual(env["CMAKE_CXX_COMPILER"], "C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe")

    @patch('os.path.exists')
    def test_setup_environment_no_sysroot(self, mock_exists):
        """Test environment setup without sysroot"""
        mock_exists.return_value = True

        # Create mock toolchain without sysroot
        self.compiler._toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot=""
        )

        env = self.compiler.setup_environment()

        # Should not have sysroot-related variables
        self.assertNotIn("CMAKE_SYSROOT", env)
        self.assertNotIn("CMAKE_FIND_ROOT_PATH", env)

    def test_setup_environment_no_toolchain(self):
        """Test environment setup when no toolchain detected"""
        self.compiler._toolchain = None

        with self.assertRaises(RuntimeError) as context:
            self.compiler.setup_environment()

        self.assertIn("Toolchain not detected", str(context.exception))


class TestCMakeGenerator(unittest.TestCase):
    """Test cases for CMake generator selection"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    def test_get_cmake_generator(self):
        """Test CMake generator selection"""
        generator = self.compiler.get_cmake_generator()

        self.assertEqual(generator, "Ninja")

    def test_get_cmake_generator_aarch64(self):
        """Test CMake generator selection for aarch64"""
        compiler = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")
        generator = compiler.get_cmake_generator()

        self.assertEqual(generator, "Ninja")


class TestValidation(unittest.TestCase):
    """Test cases for cross-compiler validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_validate_success(self, mock_exists):
        """Test successful validation"""
        mock_exists.return_value = True

        # Create mock toolchain
        self.compiler._toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        result = self.compiler.validate()

        self.assertTrue(result)

    @patch('os.path.exists')
    def test_validate_missing_executables(self, mock_exists):
        """Test validation with missing executables"""
        mock_exists.return_value = False

        # Create mock toolchain
        self.compiler._toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\nonexistent\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\nonexistent\\x86_64-linux-gnu-g++.exe",
            ar="C:\\nonexistent\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\nonexistent\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\nonexistent\\x86_64-linux-gnu"
        )

        result = self.compiler.validate()

        self.assertFalse(result)

    @patch('os.path.exists')
    def test_validate_no_toolchain(self, mock_exists):
        """Test validation when no toolchain detected"""
        self.compiler._toolchain = None

        result = self.compiler.validate()

        self.assertFalse(result)

    @patch('os.path.exists')
    def test_validate_missing_sysroot(self, mock_exists):
        """Test validation with missing sysroot"""
        def exists_side_effect(path):
            # Executables exist but sysroot doesn't
            return "bin" in path

        mock_exists.side_effect = exists_side_effect

        # Create mock toolchain
        self.compiler._toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\nonexistent\\x86_64-linux-gnu"
        )

        result = self.compiler.validate()

        # Should still be valid if executables exist
        self.assertTrue(result)


class TestFullDetection(unittest.TestCase):
    """Test cases for full detection workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")

    @patch('os.path.exists')
    def test_detect_success(self, mock_exists):
        """Test successful cross-compiler detection"""
        mock_exists.return_value = True

        # Override toolchain paths
        self.compiler.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]

        # Mock _check_toolchain
        mock_toolchain = ToolchainInfo(
            name="x86_64-linux-gnu",
            gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
            gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
            ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
            strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
            sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
        )

        with patch.object(self.compiler, '_check_toolchain', return_value=mock_toolchain):
            info = self.compiler.detect()

            self.assertIsNotNone(info)
            self.assertEqual(info.target_platform, "linux")
            self.assertEqual(info.target_architecture, "x86_64-linux-gnu")
            self.assertEqual(info.cmake_generator, "Ninja")
            self.assertIn("cc", info.compilers)
            self.assertIn("cxx", info.compilers)

    @patch('os.path.exists')
    def test_detect_not_found(self, mock_exists):
        """Test detection when cross-compiler not found"""
        mock_exists.return_value = False

        # Override toolchain paths
        self.compiler.TOOLCHAIN_PATHS = ["C:\\nonexistent\\bin"]

        with patch.object(self.compiler, '_check_toolchain', return_value=None):
            info = self.compiler.detect()

            self.assertIsNone(info)

    @patch('os.path.exists')
    def test_detect_multiple_targets(self, mock_exists):
        """Test detection of multiple target architectures"""
        mock_exists.return_value = True

        # Override toolchain paths
        self.compiler.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]

        # Mock _check_toolchain to return different toolchains
        def check_side_effect(path, target):
            if target == "x86_64-linux-gnu":
                return ToolchainInfo(
                    name="x86_64-linux-gnu",
                    gcc="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc.exe",
                    gxx="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-g++.exe",
                    ar="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-gcc-ar.exe",
                    strip="C:\\test_msys64\\mingw64\\bin\\x86_64-linux-gnu-strip.exe",
                    sysroot="C:\\test_msys64\\mingw64\\x86_64-linux-gnu"
                )
            elif target == "aarch64-linux-gnu":
                return ToolchainInfo(
                    name="aarch64-linux-gnu",
                    gcc="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc.exe",
                    gxx="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-g++.exe",
                    ar="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-gcc-ar.exe",
                    strip="C:\\test_msys64\\mingw64\\bin\\aarch64-linux-gnu-strip.exe",
                    sysroot="C:\\test_msys64\\mingw64\\aarch64-linux-gnu"
                )
            return None

        with patch.object(self.compiler, '_check_toolchain', side_effect=check_side_effect):
            # Detect x86_64
            compiler_x86_64 = LinuxCrossCompiler(target_architecture="x86_64-linux-gnu")
            compiler_x86_64.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]
            info_x86_64 = compiler_x86_64.detect()

            self.assertIsNotNone(info_x86_64)
            self.assertEqual(info_x86_64.target_architecture, "x86_64-linux-gnu")

            # Detect aarch64
            compiler_aarch64 = LinuxCrossCompiler(target_architecture="aarch64-linux-gnu")
            compiler_aarch64.TOOLCHAIN_PATHS = ["C:\\test_msys64\\mingw64\\bin"]
            info_aarch64 = compiler_aarch64.detect()

            self.assertIsNotNone(info_aarch64)
            self.assertEqual(info_aarch64.target_architecture, "aarch64-linux-gnu")


class TestICrossCompilerInterface(unittest.TestCase):
    """Test cases for ICrossCompiler interface compliance"""

    def test_linux_cross_compiler_implements_interface(self):
        """Test that LinuxCrossCompiler implements ICrossCompiler"""
        compiler = LinuxCrossCompiler()

        self.assertIsInstance(compiler, ICrossCompiler)
        self.assertTrue(hasattr(compiler, 'detect'))
        self.assertTrue(hasattr(compiler, 'setup_environment'))
        self.assertTrue(hasattr(compiler, 'get_cmake_generator'))
        self.assertTrue(hasattr(compiler, 'validate'))


if __name__ == '__main__':
    unittest.main()
