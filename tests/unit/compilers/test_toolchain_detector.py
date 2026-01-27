"""
Unit Tests for Toolchain Detector

This module contains comprehensive unit tests for ToolchainDetector class,
testing toolchain detection for Linux, WASM, and Android targets.
"""

import sys
import unittest
import os
import tempfile
from unittest.mock import Mock, patch

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.toolchain_detector import (
    ToolchainDetector,
    UnifiedToolchainInfo,
    ToolchainDetectionResult
)


class TestUnifiedToolchainInfo(unittest.TestCase):
    """Test cases for UnifiedToolchainInfo dataclass"""

    def test_unified_toolchain_info_creation(self) -> None:
        """Test creating UnifiedToolchainInfo"""
        info = UnifiedToolchainInfo(
            platform="linux",
            architecture="x86_64-linux-gnu",
            toolchain_path=r"C:\msys64\mingw64\bin",
            sysroot=r"C:\msys64\mingw64\x86_64-linux-gnu",
            compilers={
                "cc": r"C:\msys64\mingw64\bin\x86_64-linux-gnu-gcc.exe",
                "cxx": r"C:\msys64\mingw64\bin\x86_64-linux-gnu-g++.exe"
            },
            cmake_generator="Ninja",
            metadata={"version": "1.0.0"}
        )
        
        self.assertEqual(info.platform, "linux")
        self.assertEqual(info.architecture, "x86_64-linux-gnu")
        self.assertEqual(info.cmake_generator, "Ninja")

    def test_unified_toolchain_info_to_dict(self) -> None:
        """Test converting UnifiedToolchainInfo to dictionary"""
        info = UnifiedToolchainInfo(
            platform="wasm",
            architecture="wasm32",
            toolchain_path=r"C:\emsdk\upstream\emscripten",
            sysroot=r"C:\emsdk\upstream\emscripten",
            compilers={"cc": r"C:\emsdk\upstream\emscripten\emcc.exe"},
            cmake_generator="Ninja",
            metadata={"emscripten_version": "3.1.34"}
        )
        
        result = info.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["platform"], "wasm")
        self.assertEqual(result["architecture"], "wasm32")
        self.assertEqual(result["cmake_generator"], "Ninja")
        self.assertIn("metadata", result)

    def test_unified_toolchain_info_is_valid(self) -> None:
        """Test UnifiedToolchainInfo validation"""
        # Test with existing path
        with tempfile.TemporaryDirectory() as temp_dir:
            info = UnifiedToolchainInfo(
                platform="linux",
                architecture="x86_64-linux-gnu",
                toolchain_path=temp_dir,
                sysroot=temp_dir,
                compilers={},
                cmake_generator="Ninja",
                metadata={}
            )
            self.assertTrue(info.is_valid())
        
        # Test with non-existing path
        info = UnifiedToolchainInfo(
            platform="linux",
            architecture="x86_64-linux-gnu",
            toolchain_path=r"C:\nonexistent\path",
            sysroot=r"C:\nonexistent\path",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        self.assertFalse(info.is_valid())


class TestToolchainDetectionResult(unittest.TestCase):
    """Test cases for ToolchainDetectionResult dataclass"""

    def test_detection_result_creation(self) -> None:
        """Test creating ToolchainDetectionResult"""
        result = ToolchainDetectionResult(
            success=True,
            toolchains=[],
            errors=[],
            warnings=[]
        )
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.toolchains), 0)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)

    def test_detection_result_to_dict(self) -> None:
        """Test converting ToolchainDetectionResult to dictionary"""
        toolchain = UnifiedToolchainInfo(
            platform="linux",
            architecture="x86_64-linux-gnu",
            toolchain_path=r"C:\test\path",
            sysroot=r"C:\test\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        
        result = ToolchainDetectionResult(
            success=True,
            toolchains=[toolchain],
            errors=["Error 1"],
            warnings=["Warning 1"]
        )
        
        result_dict = result.to_dict()
        
        self.assertIsInstance(result_dict, dict)
        self.assertTrue(result_dict["success"])
        self.assertEqual(len(result_dict["toolchains"]), 1)
        self.assertEqual(len(result_dict["errors"]), 1)
        self.assertEqual(len(result_dict["warnings"]), 1)


class TestToolchainDetectorInit(unittest.TestCase):
    """Test cases for ToolchainDetector initialization"""

    def test_detector_initialization(self) -> None:
        """Test ToolchainDetector initialization"""
        detector = ToolchainDetector()
        
        self.assertIsNotNone(detector)
        self.assertEqual(detector.SUPPORTED_PLATFORMS, ["linux", "wasm", "android"])

    def test_supported_platforms(self) -> None:
        """Test supported platforms list"""
        self.assertIn("linux", ToolchainDetector.SUPPORTED_PLATFORMS)
        self.assertIn("wasm", ToolchainDetector.SUPPORTED_PLATFORMS)
        self.assertIn("android", ToolchainDetector.SUPPORTED_PLATFORMS)

    def test_supported_architectures(self) -> None:
        """Test supported architectures per platform"""
        archs = ToolchainDetector.SUPPORTED_ARCHITECTURES
        
        # Linux architectures
        self.assertIn("x86_64-linux-gnu", archs["linux"])
        self.assertIn("aarch64-linux-gnu", archs["linux"])
        
        # WASM architectures
        self.assertIn("wasm32", archs["wasm"])
        self.assertIn("wasm64", archs["wasm"])
        
        # Android architectures
        self.assertIn("arm64-v8a", archs["android"])
        self.assertIn("armeabi-v7a", archs["android"])
        self.assertIn("x86_64", archs["android"])
        self.assertIn("x86", archs["android"])


class TestToolchainDetectorDetectToolchain(unittest.TestCase):
    """Test cases for ToolchainDetector.detect_toolchain() method"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    def test_detect_toolchain_unsupported_platform(self) -> None:
        """Test detecting toolchain for unsupported platform"""
        result = self.detector.detect_toolchain("unsupported", "x86_64")
        
        self.assertIsNone(result)

    def test_detect_toolchain_unsupported_architecture(self) -> None:
        """Test detecting toolchain for unsupported architecture"""
        result = self.detector.detect_toolchain("linux", "unsupported-arch")
        
        self.assertIsNone(result)

    @patch('compilers.toolchain_detector.LinuxCrossCompiler')
    def test_detect_toolchain_linux_success(self, mock_linux_compiler: Mock) -> None:
        """Test detecting Linux toolchain successfully"""
        # Mock Linux compiler
        mock_instance = Mock()
        mock_instance.detect.return_value = Mock(
            target_platform="linux",
            target_architecture="x86_64-linux-gnu",
            toolchain_path=r"C:\test\path",
            sysroot=r"C:\test\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        mock_linux_compiler.return_value = mock_instance
        
        # Detect Linux toolchain
        result = self.detector.detect_toolchain("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.platform, "linux")
            self.assertEqual(result.architecture, "x86_64-linux-gnu")

    @patch('compilers.toolchain_detector.WASMCrossCompiler')
    def test_detect_toolchain_wasm_success(self, mock_wasm_compiler: Mock) -> None:
        """Test detecting WASM toolchain successfully"""
        # Mock WASM compiler
        mock_instance = Mock()
        mock_instance.detect.return_value = Mock(
            target_platform="wasm",
            target_architecture="wasm32",
            toolchain_path=r"C:\test\path",
            sysroot=r"C:\test\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        mock_wasm_compiler.return_value = mock_instance
        
        # Detect WASM toolchain
        result = self.detector.detect_toolchain("wasm", "wasm32")
        
        # Verify result
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.platform, "wasm")
            self.assertEqual(result.architecture, "wasm32")

    @patch('compilers.toolchain_detector.AndroidCrossCompiler')
    def test_detect_toolchain_android_success(self, mock_android_compiler: Mock) -> None:
        """Test detecting Android toolchain successfully"""
        # Mock Android compiler
        mock_instance = Mock()
        mock_instance.detect.return_value = Mock(
            target_platform="android",
            target_architecture="arm64-v8a",
            toolchain_path=r"C:\test\path",
            sysroot=r"C:\test\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        mock_android_compiler.return_value = mock_instance
        
        # Detect Android toolchain
        result = self.detector.detect_toolchain("android", "arm64-v8a")
        
        # Verify result
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.platform, "android")
            self.assertEqual(result.architecture, "arm64-v8a")


class TestToolchainDetectorDetectSysroot(unittest.TestCase):
    """Test cases for ToolchainDetector.detect_sysroot() method"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_detect_sysroot_success(self, mock_detect_toolchain: Mock) -> None:
        """Test detecting sysroot successfully"""
        # Mock toolchain with sysroot
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_toolchain = UnifiedToolchainInfo(
                platform="linux",
                architecture="x86_64-linux-gnu",
                toolchain_path=temp_dir,
                sysroot=temp_dir,
                compilers={},
                cmake_generator="Ninja",
                metadata={}
            )
            mock_detect_toolchain.return_value = mock_toolchain
            
            # Detect sysroot
            result = self.detector.detect_sysroot("linux", "x86_64-linux-gnu")
            
            # Verify result
            self.assertEqual(result, temp_dir)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_detect_sysroot_no_toolchain(self, mock_detect_toolchain: Mock) -> None:
        """Test detecting sysroot when toolchain not found"""
        # Mock no toolchain
        mock_detect_toolchain.return_value = None
        
        # Detect sysroot
        result = self.detector.detect_sysroot("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsNone(result)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_detect_sysroot_nonexistent_path(self, mock_detect_toolchain: Mock) -> None:
        """Test detecting sysroot with non-existent path"""
        # Mock toolchain with non-existent sysroot
        mock_toolchain = UnifiedToolchainInfo(
            platform="linux",
            architecture="x86_64-linux-gnu",
            toolchain_path=r"C:\test\path",
            sysroot=r"C:\nonexistent\sysroot",
            compilers={},
            cmake_generator="Ninja",
            metadata={}
        )
        mock_detect_toolchain.return_value = mock_toolchain
        
        # Detect sysroot
        result = self.detector.detect_sysroot("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsNone(result)


class TestToolchainDetectorDetectTargetTriple(unittest.TestCase):
    """Test cases for ToolchainDetector.detect_target_triple() method"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    def test_detect_target_triple_linux(self) -> None:
        """Test detecting target triple for Linux"""
        result = self.detector.detect_target_triple("linux", "x86_64-linux-gnu")
        
        self.assertEqual(result, "x86_64-linux-gnu")

    def test_detect_target_triple_wasm(self) -> None:
        """Test detecting target triple for WASM"""
        result = self.detector.detect_target_triple("wasm", "wasm32")
        
        self.assertEqual(result, "wasm32")

    @patch('compilers.toolchain_detector.AndroidCrossCompiler')
    def test_detect_target_triple_android(self, mock_android_compiler: Mock) -> None:
        """Test detecting target triple for Android"""
        # Mock Android compiler
        mock_instance = Mock()
        mock_instance.detect_target_triple.return_value = "aarch64-linux-android"
        mock_android_compiler.return_value = mock_instance
        
        # Detect target triple
        result = self.detector.detect_target_triple("android", "arm64-v8a")
        
        # Verify result
        self.assertEqual(result, "aarch64-linux-android")

    def test_detect_target_triple_unsupported_platform(self) -> None:
        """Test detecting target triple for unsupported platform"""
        result = self.detector.detect_target_triple("unsupported", "x86_64")
        
        self.assertIsNone(result)

    def test_detect_target_triple_unsupported_architecture(self) -> None:
        """Test detecting target triple for unsupported architecture"""
        result = self.detector.detect_target_triple("linux", "unsupported-arch")
        
        self.assertIsNone(result)


class TestToolchainDetectorValidate(unittest.TestCase):
    """Test cases for ToolchainDetector.validate() method"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_validate_success(self, mock_detect_toolchain: Mock) -> None:
        """Test validating toolchain successfully"""
        # Mock valid toolchain
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_toolchain = UnifiedToolchainInfo(
                platform="linux",
                architecture="x86_64-linux-gnu",
                toolchain_path=temp_dir,
                sysroot=temp_dir,
                compilers={
                    "cc": os.path.join(temp_dir, "gcc.exe"),
                    "cxx": os.path.join(temp_dir, "g++.exe")
                },
                cmake_generator="Ninja",
                metadata={}
            )
            mock_detect_toolchain.return_value = mock_toolchain
            
            # Create dummy executables
            for exe in ["gcc.exe", "g++.exe"]:
                with open(os.path.join(temp_dir, exe), 'w') as f:
                    f.write("dummy")
            
            # Validate toolchain
            result = self.detector.validate("linux", "x86_64-linux-gnu")
            
            # Verify result
            self.assertTrue(result["is_valid"])
            self.assertEqual(len(result["errors"]), 0)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_validate_no_toolchain(self, mock_detect_toolchain: Mock) -> None:
        """Test validating when toolchain not found"""
        # Mock no toolchain
        mock_detect_toolchain.return_value = None
        
        # Validate toolchain
        result = self.detector.validate("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertFalse(result["is_valid"])
        self.assertGreater(len(result["errors"]), 0)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_validate_missing_executables(self, mock_detect_toolchain: Mock) -> None:
        """Test validating toolchain with missing executables"""
        # Mock toolchain with missing executables
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_toolchain = UnifiedToolchainInfo(
                platform="linux",
                architecture="x86_64-linux-gnu",
                toolchain_path=temp_dir,
                sysroot=temp_dir,
                compilers={
                    "cc": os.path.join(temp_dir, "gcc.exe"),
                    "cxx": os.path.join(temp_dir, "g++.exe")
                },
                cmake_generator="Ninja",
                metadata={}
            )
            mock_detect_toolchain.return_value = mock_toolchain
            
            # Don't create executables
            # Validate toolchain
            result = self.detector.validate("linux", "x86_64-linux-gnu")
            
            # Verify result
            self.assertFalse(result["is_valid"])
            self.assertGreater(len(result["errors"]), 0)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_validate_nonexistent_sysroot(self, mock_detect_toolchain: Mock) -> None:
        """Test validating toolchain with non-existent sysroot"""
        # Mock toolchain with non-existent sysroot
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_toolchain = UnifiedToolchainInfo(
                platform="linux",
                architecture="x86_64-linux-gnu",
                toolchain_path=temp_dir,
                sysroot=r"C:\nonexistent\sysroot",
                compilers={},
                cmake_generator="Ninja",
                metadata={}
            )
            mock_detect_toolchain.return_value = mock_toolchain
            
            # Validate toolchain
            result = self.detector.validate("linux", "x86_64-linux-gnu")
            
            # Verify result - validation passes with warning about sysroot
            self.assertTrue(result["is_valid"])
            # Should have warning about sysroot
            self.assertGreater(len(result["warnings"]), 0)


class TestToolchainDetectorGetMethods(unittest.TestCase):
    """Test cases for ToolchainDetector getter methods"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    @patch('compilers.toolchain_detector.ToolchainDetector.detect')
    def test_get_detected_toolchains(self, mock_detect: Mock) -> None:
        """Test getting all detected toolchains"""
        # Mock detection result
        mock_result = ToolchainDetectionResult(
            success=True,
            toolchains=[
                UnifiedToolchainInfo(
                    platform="linux",
                    architecture="x86_64-linux-gnu",
                    toolchain_path=r"C:\test\path",
                    sysroot=r"C:\test\sysroot",
                    compilers={},
                    cmake_generator="Ninja",
                    metadata={}
                )
            ],
            errors=[],
            warnings=[]
        )
        mock_detect.return_value = mock_result
        
        # Detect toolchains
        self.detector.detect()
        
        # Manually set detected toolchains (since mock doesn't populate internal state)
        self.detector._detected_toolchains = mock_result.toolchains
        
        # Get detected toolchains
        toolchains = self.detector.get_detected_toolchains()
        
        # Verify result
        self.assertEqual(len(toolchains), 1)
        self.assertEqual(toolchains[0].platform, "linux")

    @patch('compilers.toolchain_detector.ToolchainDetector.detect')
    def test_get_toolchains_by_platform(self, mock_detect: Mock) -> None:
        """Test getting toolchains by platform"""
        # Mock detection result with multiple platforms
        mock_result = ToolchainDetectionResult(
            success=True,
            toolchains=[
                UnifiedToolchainInfo(
                    platform="linux",
                    architecture="x86_64-linux-gnu",
                    toolchain_path=r"C:\test\path",
                    sysroot=r"C:\test\sysroot",
                    compilers={},
                    cmake_generator="Ninja",
                    metadata={}
                ),
                UnifiedToolchainInfo(
                    platform="wasm",
                    architecture="wasm32",
                    toolchain_path=r"C:\test\path",
                    sysroot=r"C:\test\sysroot",
                    compilers={},
                    cmake_generator="Ninja",
                    metadata={}
                )
            ],
            errors=[],
            warnings=[]
        )
        mock_detect.return_value = mock_result
        
        # Detect toolchains
        self.detector.detect()
        
        # Manually set detected toolchains (since mock doesn't populate internal state)
        self.detector._detected_toolchains = mock_result.toolchains
        
        # Get Linux toolchains
        linux_toolchains = self.detector.get_toolchains_by_platform("linux")
        
        # Verify result
        self.assertEqual(len(linux_toolchains), 1)
        self.assertEqual(linux_toolchains[0].platform, "linux")
        
        # Get WASM toolchains
        wasm_toolchains = self.detector.get_toolchains_by_platform("wasm")
        
        # Verify result
        self.assertEqual(len(wasm_toolchains), 1)
        self.assertEqual(wasm_toolchains[0].platform, "wasm")


class TestToolchainDetectorErrorHandling(unittest.TestCase):
    """Test cases for ToolchainDetector error handling"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.detector = ToolchainDetector()

    @patch('compilers.toolchain_detector.ToolchainDetector._detect_linux_toolchains')
    @patch('compilers.toolchain_detector.ToolchainDetector._detect_wasm_toolchains')
    @patch('compilers.toolchain_detector.ToolchainDetector._detect_android_toolchains')
    def test_detect_with_exception_handling(
        self,
        mock_detect_android_toolchains: Mock,
        mock_detect_wasm_toolchains: Mock,
        mock_detect_linux_toolchains: Mock
    ) -> None:
        """Test that exceptions are handled gracefully"""
        # Mock all platform detections to raise exceptions
        mock_detect_linux_toolchains.side_effect = Exception("Linux detection failed")
        mock_detect_wasm_toolchains.side_effect = Exception("WASM detection failed")
        mock_detect_android_toolchains.side_effect = Exception("Android detection failed")
        
        # Detect all toolchains - should not raise exception
        result = self.detector.detect()
        
        # Verify error was captured and no toolchains were found
        self.assertFalse(result.success)
        self.assertEqual(len(result.toolchains), 0)
        self.assertGreater(len(result.errors), 0)

    @patch('compilers.toolchain_detector.ToolchainDetector.detect_toolchain')
    def test_validate_with_exception_handling(self, mock_detect_toolchain: Mock) -> None:
        """Test that validation exceptions are handled gracefully"""
        # Mock detect_toolchain to raise exception
        mock_detect_toolchain.side_effect = Exception("Detection failed")
        
        # Validate toolchain - should not raise exception
        result = self.detector.validate("linux", "x86_64-linux-gnu")
        
        # Verify error was captured
        self.assertFalse(result["is_valid"])
        self.assertGreater(len(result["errors"]), 0)


if __name__ == '__main__':
    unittest.main()
