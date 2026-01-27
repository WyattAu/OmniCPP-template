"""
Unit tests for WASM Cross-Compiler Detection Module

This module contains comprehensive tests for WASM cross-compiler detection
system, including Emscripten detection, version detection, and validation.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.wasm_cross_compiler import (
    WASMCrossCompiler,
    EmscriptenInfo,
    CrossCompilerInfo,
    ICrossCompiler
)


class TestEmscriptenInfo(unittest.TestCase):
    """Test cases for EmscriptenInfo dataclass"""

    def test_emscripten_info_creation(self):
        """Test creating EmscriptenInfo instance"""
        info = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        self.assertEqual(info.version, "3.1.34")
        self.assertEqual(info.root_path, r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info.emcc_path, r"C:\emsdk\upstream\emscripten\emcc.bat")
        self.assertEqual(info.emxx_path, r"C:\emsdk\upstream\emscripten\em++.bat")
        self.assertEqual(info.emar_path, r"C:\emsdk\upstream\emscripten\emar.bat")
        self.assertEqual(info.emcmake_path, r"C:\emsdk\upstream\emscripten\emcmake.bat")
        self.assertEqual(info.emconfigure_path, r"C:\emsdk\upstream\emscripten\emconfigure.bat")

    def test_emscripten_info_to_dict(self):
        """Test converting EmscriptenInfo to dictionary"""
        info = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["version"], "3.1.34")
        self.assertEqual(info_dict["root_path"], r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info_dict["emcc_path"], r"C:\emsdk\upstream\emscripten\emcc.bat")
        self.assertEqual(info_dict["emxx_path"], r"C:\emsdk\upstream\emscripten\em++.bat")
        self.assertEqual(info_dict["emar_path"], r"C:\emsdk\upstream\emscripten\emar.bat")
        self.assertEqual(info_dict["emcmake_path"], r"C:\emsdk\upstream\emscripten\emcmake.bat")
        self.assertEqual(info_dict["emconfigure_path"], r"C:\emsdk\upstream\emscripten\emconfigure.bat")

    @patch('os.path.exists')
    def test_emscripten_info_is_valid(self, mock_exists):
        """Test EmscriptenInfo.is_valid() with all executables present"""
        mock_exists.return_value = True

        info = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        self.assertTrue(info.is_valid())

    @patch('os.path.exists')
    def test_emscripten_info_is_invalid(self, mock_exists):
        """Test EmscriptenInfo.is_valid() with missing executables"""
        # Mock exists to return False for some paths
        def exists_side_effect(path):
            return "emcc" in path or "em++" in path

        mock_exists.side_effect = exists_side_effect

        info = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        self.assertFalse(info.is_valid())


class TestCrossCompilerInfo(unittest.TestCase):
    """Test cases for CrossCompilerInfo dataclass"""

    def test_cross_compiler_info_creation(self):
        """Test creating CrossCompilerInfo instance"""
        info = CrossCompilerInfo(
            target_platform="wasm",
            target_architecture="wasm32",
            toolchain_path=r"C:\emsdk\upstream\emscripten",
            sysroot=r"C:\emsdk\upstream\emscripten",
            compilers={
                "cc": r"C:\emsdk\upstream\emscripten\emcc.bat",
                "cxx": r"C:\emsdk\upstream\emscripten\em++.bat",
                "ar": r"C:\emsdk\upstream\emscripten\emar.bat"
            },
            cmake_generator="Ninja",
            metadata={
                "emscripten_version": "3.1.34",
                "emscripten_root": r"C:\emsdk\upstream\emscripten"
            }
        )

        self.assertEqual(info.target_platform, "wasm")
        self.assertEqual(info.target_architecture, "wasm32")
        self.assertEqual(info.toolchain_path, r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info.sysroot, r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info.cmake_generator, "Ninja")
        self.assertIn("cc", info.compilers)
        self.assertIn("cxx", info.compilers)
        self.assertIn("ar", info.compilers)

    def test_cross_compiler_info_to_dict(self):
        """Test converting CrossCompilerInfo to dictionary"""
        info = CrossCompilerInfo(
            target_platform="wasm",
            target_architecture="wasm32",
            toolchain_path=r"C:\emsdk\upstream\emscripten",
            sysroot=r"C:\emsdk\upstream\emscripten",
            compilers={
                "cc": r"C:\emsdk\upstream\emscripten\emcc.bat",
                "cxx": r"C:\emsdk\upstream\emscripten\em++.bat",
                "ar": r"C:\emsdk\upstream\emscripten\emar.bat"
            },
            cmake_generator="Ninja",
            metadata={
                "emscripten_version": "3.1.34",
                "emscripten_root": r"C:\emsdk\upstream\emscripten"
            }
        )

        info_dict = info.to_dict()

        self.assertIsInstance(info_dict, dict)
        self.assertEqual(info_dict["target_platform"], "wasm")
        self.assertEqual(info_dict["target_architecture"], "wasm32")
        self.assertEqual(info_dict["toolchain_path"], r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info_dict["sysroot"], r"C:\emsdk\upstream\emscripten")
        self.assertEqual(info_dict["cmake_generator"], "Ninja")
        self.assertIn("compilers", info_dict)
        self.assertIn("metadata", info_dict)

    @patch('os.path.exists')
    def test_cross_compiler_info_is_valid(self, mock_exists):
        """Test CrossCompilerInfo.is_valid() with valid path"""
        mock_exists.return_value = True

        info = CrossCompilerInfo(
            target_platform="wasm",
            target_architecture="wasm32",
            toolchain_path=r"C:\emsdk\upstream\emscripten",
            sysroot=r"C:\emsdk\upstream\emscripten",
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
            target_platform="wasm",
            target_architecture="wasm32",
            toolchain_path=r"C:\emsdk\upstream\emscripten",
            sysroot=r"C:\emsdk\upstream\emscripten",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )

        self.assertFalse(info.is_valid())


class TestWASMCrossCompiler(unittest.TestCase):
    """Test cases for WASMCrossCompiler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.compiler = WASMCrossCompiler()

    def test_initialization_default(self):
        """Test WASMCrossCompiler initialization with default architecture"""
        compiler = WASMCrossCompiler()
        self.assertEqual(compiler._target_architecture, "wasm32")
        self.assertIsNone(compiler._emscripten)
        self.assertIsNone(compiler._info)

    def test_initialization_custom_architecture(self):
        """Test WASMCrossCompiler initialization with custom architecture"""
        compiler = WASMCrossCompiler("wasm64")
        self.assertEqual(compiler._target_architecture, "wasm64")

    def test_supported_targets(self):
        """Test supported target architectures"""
        self.assertIn("wasm32", WASMCrossCompiler.SUPPORTED_TARGETS)
        self.assertIn("wasm64", WASMCrossCompiler.SUPPORTED_TARGETS)

    def test_emscripten_paths(self):
        """Test Emscripten search paths"""
        self.assertIsInstance(WASMCrossCompiler.EMSCRIPTEN_PATHS, list)
        self.assertGreater(len(WASMCrossCompiler.EMSCRIPTEN_PATHS), 0)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_detect_emscripten_from_env(self, mock_env_get, mock_exists):
        """Test detecting Emscripten from environment variable"""
        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True

        # Mock subprocess.run for version detection
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
            )

            emscripten = self.compiler.detect_emscripten()

            self.assertIsNotNone(emscripten)
            self.assertEqual(emscripten.root_path, r"C:\emsdk\upstream\emscripten")
            self.assertEqual(emscripten.version, "3.1.34")

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_detect_emscripten_not_found(self, mock_env_get, mock_exists):
        """Test detecting Emscripten when not found"""
        mock_env_get.return_value = None
        mock_exists.return_value = False

        # Mock subprocess.run for PATH search
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=1)

            emscripten = self.compiler.detect_emscripten()

            self.assertIsNone(emscripten)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_emcc(self, mock_run, mock_exists):
        """Test detecting emcc compiler"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout=r"C:\emsdk\upstream\emscripten\emcc.bat"
        )

        # Set up Emscripten info
        self.compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        emcc_path = self.compiler.detect_emcc()

        self.assertEqual(emcc_path, r"C:\emsdk\upstream\emscripten\emcc.bat")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_emar(self, mock_run, mock_exists):
        """Test detecting emar archiver"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout=r"C:\emsdk\upstream\emscripten\emar.bat"
        )

        # Set up Emscripten info
        self.compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        emar_path = self.compiler.detect_emar()

        self.assertEqual(emar_path, r"C:\emsdk\upstream\emscripten\emar.bat")

    def test_setup_environment(self):
        """Test setting up WASM cross-compilation environment"""
        # Set up Emscripten info
        self.compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        env = self.compiler.setup_environment()

        self.assertIsInstance(env, dict)
        self.assertEqual(env["CMAKE_SYSTEM_NAME"], "Emscripten")
        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "wasm32")
        self.assertEqual(env["CMAKE_C_COMPILER"], r"C:\emsdk\upstream\emscripten\emcc.bat")
        self.assertEqual(env["CMAKE_CXX_COMPILER"], r"C:\emsdk\upstream\emscripten\em++.bat")
        self.assertEqual(env["CMAKE_AR"], r"C:\emsdk\upstream\emscripten\emar.bat")
        self.assertEqual(env["EMSCRIPTEN_ROOT_PATH"], r"C:\emsdk\upstream\emscripten")
        self.assertEqual(env["EMSCRIPTEN"], r"C:\emsdk\upstream\emscripten")
        self.assertEqual(env["CMAKE_GENERATOR"], "Ninja")
        self.assertEqual(env["CMAKE_EXECUTABLE_SUFFIX"], ".html")
        self.assertEqual(env["CMAKE_POSITION_INDEPENDENT_CODE"], "ON")

    def test_setup_environment_wasm64(self):
        """Test setting up WASM64 cross-compilation environment"""
        compiler = WASMCrossCompiler("wasm64")

        # Set up Emscripten info
        compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        env = compiler.setup_environment()

        self.assertEqual(env["CMAKE_SYSTEM_PROCESSOR"], "wasm64")

    def test_setup_environment_no_emscripten(self):
        """Test setup_environment raises error when Emscripten not detected"""
        with self.assertRaises(RuntimeError) as context:
            self.compiler.setup_environment()

        self.assertIn("Emscripten not detected", str(context.exception))

    def test_get_cmake_generator(self):
        """Test getting CMake generator"""
        generator = self.compiler.get_cmake_generator()
        self.assertEqual(generator, "Ninja")

    @patch('os.path.exists')
    def test_validate_success(self, mock_exists):
        """Test successful validation of WASM cross-compiler"""
        mock_exists.return_value = True

        # Set up Emscripten info
        self.compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        result = self.compiler.validate()

        self.assertTrue(result)

    @patch('os.path.exists')
    def test_validate_failure(self, mock_exists):
        """Test failed validation of WASM cross-compiler"""
        # Mock exists to return False for some paths
        def exists_side_effect(path):
            return "root_path" in path or "emcc" in path

        mock_exists.side_effect = exists_side_effect

        # Set up Emscripten info
        self.compiler._emscripten = EmscriptenInfo(
            version="3.1.34",
            root_path=r"C:\emsdk\upstream\emscripten",
            emcc_path=r"C:\emsdk\upstream\emscripten\emcc.bat",
            emxx_path=r"C:\emsdk\upstream\emscripten\em++.bat",
            emar_path=r"C:\emsdk\upstream\emscripten\emar.bat",
            emcmake_path=r"C:\emsdk\upstream\emscripten\emcmake.bat",
            emconfigure_path=r"C:\emsdk\upstream\emscripten\emconfigure.bat"
        )

        result = self.compiler.validate()

        self.assertFalse(result)

    def test_validate_no_emscripten(self):
        """Test validate returns False when Emscripten not detected"""
        result = self.compiler.validate()
        self.assertFalse(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_detect_success(self, mock_run, mock_env_get, mock_exists):
        """Test successful detection of WASM cross-compiler"""
        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        result = self.compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_platform, "wasm")
        self.assertEqual(result.target_architecture, "wasm32")
        self.assertEqual(result.cmake_generator, "Ninja")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_detect_wasm64(self, mock_run, mock_env_get, mock_exists):
        """Test detection of WASM64 cross-compiler"""
        compiler = WASMCrossCompiler("wasm64")

        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        result = compiler.detect()

        self.assertIsNotNone(result)
        self.assertEqual(result.target_architecture, "wasm64")

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_detect_unsupported_architecture(self, mock_run, mock_env_get, mock_exists):
        """Test detection with unsupported architecture"""
        compiler = WASMCrossCompiler("arm64")

        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        result = compiler.detect()

        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_detect_no_emscripten(self, mock_run, mock_env_get, mock_exists):
        """Test detection when Emscripten not found"""
        mock_env_get.return_value = None
        mock_exists.return_value = False
        mock_run.return_value = Mock(returncode=1)

        result = self.compiler.detect()

        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_detect_creates_cross_compiler_info(self, mock_run, mock_env_get, mock_exists):
        """Test that detect creates proper CrossCompilerInfo"""
        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        result = self.compiler.detect()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, CrossCompilerInfo)
        self.assertIn("cc", result.compilers)
        self.assertIn("cxx", result.compilers)
        self.assertIn("ar", result.compilers)
        self.assertIn("emscripten_version", result.metadata)
        self.assertEqual(result.metadata["emscripten_version"], "3.1.34")


class TestICrossCompilerInterface(unittest.TestCase):
    """Test cases for ICrossCompiler interface"""

    def test_interface_is_abstract(self):
        """Test that ICrossCompiler is abstract"""
        with self.assertRaises(TypeError):
            ICrossCompiler()


class TestWASMCrossCompilerIntegration(unittest.TestCase):
    """Integration tests for WASMCrossCompiler"""

    @patch('os.path.exists')
    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_full_detection_workflow(self, mock_run, mock_env_get, mock_exists):
        """Test complete detection workflow"""
        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        compiler = WASMCrossCompiler("wasm32")

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
    @patch('subprocess.run')
    def test_wasm32_and_wasm64_detection(self, mock_run, mock_env_get, mock_exists):
        """Test detection for both wasm32 and wasm64"""
        mock_env_get.return_value = r"C:\emsdk\upstream\emscripten"
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="emcc (Emscripten gcc-like replacement) 3.1.34"
        )

        # Test wasm32
        compiler32 = WASMCrossCompiler("wasm32")
        info32 = compiler32.detect()
        self.assertIsNotNone(info32)
        self.assertEqual(info32.target_architecture, "wasm32")

        # Test wasm64
        compiler64 = WASMCrossCompiler("wasm64")
        info64 = compiler64.detect()
        self.assertIsNotNone(info64)
        self.assertEqual(info64.target_architecture, "wasm64")


if __name__ == '__main__':
    unittest.main()
