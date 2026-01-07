"""
Unit tests for MSVC Detector

This module contains comprehensive unit tests for the MSVC detector,
covering vswhere detection, registry fallback, standard paths, and
Windows SDK detection.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.msvc_detector import (
    MSVCDetector,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    CompilerInfo,
    ValidationResult,
    WindowsSDKInfo,
    ICompilerDetector
)


class TestVersionInfo(unittest.TestCase):
    """Test cases for VersionInfo dataclass"""

    def test_version_info_creation(self):
        """Test VersionInfo creation"""
        version = VersionInfo(major=19, minor=40, patch=0)
        self.assertEqual(version.major, 19)
        self.assertEqual(version.minor, 40)
        self.assertEqual(version.patch, 0)
        self.assertIsNone(version.build)

    def test_version_info_with_build(self):
        """Test VersionInfo with build number"""
        version = VersionInfo(major=19, minor=40, patch=0, build="33811")
        self.assertEqual(version.build, "33811")

    def test_version_info_str_with_build(self):
        """Test VersionInfo string representation with build"""
        version = VersionInfo(major=19, minor=40, patch=0, build="33811")
        self.assertEqual(str(version), "19.40.0.33811")

    def test_version_info_str_without_build(self):
        """Test VersionInfo string representation without build"""
        version = VersionInfo(major=19, minor=40, patch=0)
        self.assertEqual(str(version), "19.40.0")

    def test_version_info_comparison(self):
        """Test VersionInfo comparison"""
        v1 = VersionInfo(major=19, minor=40, patch=0)
        v2 = VersionInfo(major=19, minor=41, patch=0)
        v3 = VersionInfo(major=20, minor=0, patch=0)

        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertFalse(v3 < v1)


class TestCapabilityInfo(unittest.TestCase):
    """Test cases for CapabilityInfo dataclass"""

    def test_capability_info_creation(self):
        """Test CapabilityInfo creation"""
        capabilities = CapabilityInfo()
        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertFalse(capabilities.cpp17)

    def test_capability_info_with_features(self):
        """Test CapabilityInfo with features enabled"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True
        )
        self.assertTrue(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)

    def test_capability_info_to_dict(self):
        """Test CapabilityInfo to_dict method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True
        )
        result = capabilities.to_dict()
        self.assertIsInstance(result, dict)
        self.assertTrue(result["cpp23"])
        self.assertTrue(result["cpp20"])
        self.assertTrue(result["cpp17"])
        self.assertTrue(result["modules"])

    def test_capability_info_supports_cpp_standard(self):
        """Test CapabilityInfo supports_cpp_standard method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True
        )
        self.assertTrue(capabilities.supports_cpp_standard("cpp23"))
        self.assertTrue(capabilities.supports_cpp_standard("cpp20"))
        self.assertTrue(capabilities.supports_cpp_standard("cpp17"))
        self.assertFalse(capabilities.supports_cpp_standard("cpp14"))


class TestEnvironmentInfo(unittest.TestCase):
    """Test cases for EnvironmentInfo dataclass"""

    def test_environment_info_creation(self):
        """Test EnvironmentInfo creation"""
        env = EnvironmentInfo(path="/path/to/compiler")
        self.assertEqual(env.path, "/path/to/compiler")
        self.assertEqual(env.include_paths, [])
        self.assertEqual(env.library_paths, [])
        self.assertEqual(env.environment_variables, {})

    def test_environment_info_with_paths(self):
        """Test EnvironmentInfo with include and library paths"""
        env = EnvironmentInfo(
            path="/path/to/compiler",
            include_paths=["/include/path1", "/include/path2"],
            library_paths=["/lib/path1", "/lib/path2"],
            environment_variables={"VAR1": "value1"}
        )
        self.assertEqual(len(env.include_paths), 2)
        self.assertEqual(len(env.library_paths), 2)
        self.assertEqual(len(env.environment_variables), 1)

    def test_environment_info_to_dict(self):
        """Test EnvironmentInfo to_dict method"""
        env = EnvironmentInfo(
            path="/path/to/compiler",
            include_paths=["/include/path"],
            library_paths=["/lib/path"],
            environment_variables={"VAR": "value"}
        )
        result = env.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["path"], "/path/to/compiler")
        self.assertEqual(len(result["include_paths"]), 1)
        self.assertEqual(len(result["library_paths"]), 1)
        self.assertEqual(len(result["environment_variables"]), 1)


class TestCompilerInfo(unittest.TestCase):
    """Test cases for CompilerInfo dataclass"""

    def test_compiler_info_creation(self):
        """Test CompilerInfo creation"""
        version = VersionInfo(major=19, minor=40, patch=0)
        capabilities = CapabilityInfo()
        environment = EnvironmentInfo(path="/path/to/compiler")

        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version,
            path="/path/to/cl.exe",
            architecture=Architecture.X64,
            capabilities=capabilities,
            environment=environment
        )
        self.assertEqual(compiler.compiler_type, CompilerType.MSVC)
        self.assertEqual(compiler.architecture, Architecture.X64)

    def test_compiler_info_to_dict(self):
        """Test CompilerInfo to_dict method"""
        version = VersionInfo(major=19, minor=40, patch=0)
        capabilities = CapabilityInfo()
        environment = EnvironmentInfo(path="/path/to/compiler")

        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version,
            path="/path/to/cl.exe",
            architecture=Architecture.X64,
            capabilities=capabilities,
            environment=environment
        )
        result = compiler.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["compiler_type"], "msvc")
        self.assertEqual(result["architecture"], "x64")
        self.assertIn("capabilities", result)
        self.assertIn("environment", result)

    def test_compiler_info_is_valid(self):
        """Test CompilerInfo is_valid method"""
        version = VersionInfo(major=19, minor=40, patch=0)
        capabilities = CapabilityInfo()
        environment = EnvironmentInfo(path="/path/to/compiler")

        # Test with non-existent path
        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version,
            path="/nonexistent/path/cl.exe",
            architecture=Architecture.X64,
            capabilities=capabilities,
            environment=environment
        )
        self.assertFalse(compiler.is_valid())


class TestValidationResult(unittest.TestCase):
    """Test cases for ValidationResult dataclass"""

    def test_validation_result_creation(self):
        """Test ValidationResult creation"""
        result = ValidationResult(is_valid=True)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])

    def test_validation_result_with_errors(self):
        """Test ValidationResult with errors"""
        result = ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"]
        )
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(len(result.warnings), 1)

    def test_validation_result_to_dict(self):
        """Test ValidationResult to_dict method"""
        result = ValidationResult(
            is_valid=False,
            errors=["Error 1"],
            warnings=["Warning 1"]
        )
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertFalse(result_dict["is_valid"])
        self.assertEqual(len(result_dict["errors"]), 1)
        self.assertEqual(len(result_dict["warnings"]), 1)


class TestWindowsSDKInfo(unittest.TestCase):
    """Test cases for WindowsSDKInfo dataclass"""

    def test_windows_sdk_info_creation(self):
        """Test WindowsSDKInfo creation"""
        sdk = WindowsSDKInfo(version="10.0.22621", path="/path/to/sdk")
        self.assertEqual(sdk.version, "10.0.22621")
        self.assertEqual(sdk.path, "/path/to/sdk")

    def test_windows_sdk_info_to_dict(self):
        """Test WindowsSDKInfo to_dict method"""
        sdk = WindowsSDKInfo(
            version="10.0.22621",
            path="/path/to/sdk",
            product_version="10.0.22621.0"
        )
        result = sdk.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["version"], "10.0.22621")
        self.assertEqual(result["path"], "/path/to/sdk")
        self.assertEqual(result["product_version"], "10.0.22621.0")


class TestMSVCDetectorInitialization(unittest.TestCase):
    """Test cases for MSVCDetector initialization"""

    def test_detector_initialization(self):
        """Test MSVCDetector initialization"""
        detector = MSVCDetector()
        self.assertIsNotNone(detector)
        self.assertIsInstance(detector, ICompilerDetector)

    def test_detector_with_logger(self):
        """Test MSVCDetector with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        detector = MSVCDetector(logger=logger)
        self.assertIsNotNone(detector)

    def test_detector_vswhere_paths(self):
        """Test MSVCDetector vswhere paths"""
        detector = MSVCDetector()
        self.assertIsInstance(detector._vswhere_paths, list)
        self.assertGreater(len(detector._vswhere_paths), 0)

    def test_detector_standard_paths(self):
        """Test MSVCDetector standard paths"""
        detector = MSVCDetector()
        self.assertIsInstance(detector._standard_paths, list)
        self.assertGreater(len(detector._standard_paths), 0)


class TestMSVCDetectorVswhereDetection(unittest.TestCase):
    """Test cases for MSVC detection via vswhere"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('subprocess.run')
    def test_detect_via_vswhere_success(self, mock_run):
        """Test successful detection via vswhere"""
        # Mock vswhere output
        vswhere_output = json.dumps([
            {
                "installationPath": r"C:\Program Files\Microsoft Visual Studio\2022",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "displayName": "Visual Studio Community 2022"
            }
        ])

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = vswhere_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock cl.exe detection
        with patch.object(self.detector, '_detect_executables') as mock_exec:
            mock_exec.return_value = {
                "cl_x64": r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe"
            }

            with patch.object(self.detector, 'detect_version') as mock_version:
                mock_version.return_value = VersionInfo(major=19, minor=40, patch=0)

                with patch.object(self.detector, 'detect_capabilities') as mock_caps:
                    mock_caps.return_value = CapabilityInfo()

                    with patch.object(self.detector, '_detect_windows_sdk') as mock_sdk:
                        mock_sdk.return_value = None

                        compilers = self.detector._detect_via_vswhere()

                        self.assertEqual(len(compilers), 1)
                        self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC)

    @patch('subprocess.run')
    def test_detect_via_vswhere_failure(self, mock_run):
        """Test vswhere detection failure"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error"
        mock_run.return_value = mock_result

        compilers = self.detector._detect_via_vswhere()
        self.assertEqual(len(compilers), 0)

    @patch('subprocess.run')
    def test_detect_via_vswhere_not_found(self, mock_run):
        """Test vswhere not found"""
        mock_run.side_effect = FileNotFoundError()

        compilers = self.detector._detect_via_vswhere()
        self.assertEqual(len(compilers), 0)


class TestMSVCDetectorStandardPathsDetection(unittest.TestCase):
    """Test cases for MSVC detection via standard paths"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    def test_detect_via_standard_paths_no_installations(self):
        """Test standard paths detection with no installations"""
        # Mock standard paths to non-existent directories
        self.detector._standard_paths = ["/nonexistent/path"]

        compilers = self.detector._detect_via_standard_paths()
        self.assertEqual(len(compilers), 0)

    @patch('os.path.exists')
    def test_detect_via_standard_paths_with_installation(self, mock_exists):
        """Test standard paths detection with installation"""
        # Mock path existence - need to be more specific about what exists
        def exists_side_effect(path):
            # Standard path exists
            if "Program Files" in path and "Visual Studio" in path:
                return True
            # VC directory exists
            if "VC" in path and "Tools" not in path:
                return True
            # cl.exe exists
            if "cl.exe" in path:
                return True
            # link.exe exists
            if "link.exe" in path:
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        # Mock version and capabilities detection
        with patch.object(self.detector, 'detect_version') as mock_version:
            mock_version.return_value = VersionInfo(major=19, minor=40, patch=0)
            
            with patch.object(self.detector, 'detect_capabilities') as mock_caps:
                mock_caps.return_value = CapabilityInfo()
                
                compilers = self.detector._detect_via_standard_paths()
                
                # Should find compilers for each architecture
                self.assertGreater(len(compilers), 0)


class TestMSVCDetectorRegistryDetection(unittest.TestCase):
    """Test cases for MSVC detection via registry"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    def test_detect_via_registry_no_installations(self, mock_exists):
        """Test registry detection with no installations"""
        mock_exists.return_value = False

        compilers = self.detector._detect_via_registry()
        self.assertEqual(len(compilers), 0)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_via_registry_with_installation(self, mock_run, mock_exists):
        """Test registry detection with installation"""
        # Mock path existence
        def exists_side_effect(path):
            return "cl.exe" in path or "VC" in path

        mock_exists.side_effect = exists_side_effect

        # Mock cl.exe execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Microsoft (R) C/C++ Optimizing Compiler Version 19.40.33811 for x64"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Note: This test will only work on Windows with winreg
        # On other platforms, it will return empty list
        compilers = self.detector._detect_via_registry()
        self.assertIsInstance(compilers, list)


class TestMSVCDetectorVersionDetection(unittest.TestCase):
    """Test cases for MSVC version detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_version_success(self, mock_run, mock_exists):
        """Test successful version detection"""
        mock_exists.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Microsoft (R) C/C++ Optimizing Compiler Version 19.40.33811 for x64"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        version = self.detector.detect_version("/path/to/cl.exe")

        self.assertIsNotNone(version)
        self.assertEqual(version.major, 19)
        self.assertEqual(version.minor, 40)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.build, "33811")

    @patch('os.path.exists')
    def test_detect_version_file_not_found(self, mock_exists):
        """Test version detection with file not found"""
        mock_exists.return_value = False

        version = self.detector.detect_version("/nonexistent/cl.exe")
        self.assertIsNone(version)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_version_timeout(self, mock_run, mock_exists):
        """Test version detection with timeout"""
        mock_exists.return_value = True
        mock_run.side_effect = subprocess.TimeoutExpired("cl.exe", 10)

        version = self.detector.detect_version("/path/to/cl.exe")
        self.assertIsNone(version)


class TestMSVCDetectorCapabilityDetection(unittest.TestCase):
    """Test cases for MSVC capability detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch.object(MSVCDetector, 'detect_version')
    def test_detect_capabilities_cpp23(self, mock_version):
        """Test capability detection for C++23"""
        mock_version.return_value = VersionInfo(major=19, minor=40, patch=0)

        capabilities = self.detector.detect_capabilities("/path/to/cl.exe")

        self.assertTrue(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch.object(MSVCDetector, 'detect_version')
    def test_detect_capabilities_cpp20(self, mock_version):
        """Test capability detection for C++20"""
        mock_version.return_value = VersionInfo(major=19, minor=28, patch=0)

        capabilities = self.detector.detect_capabilities("/path/to/cl.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch.object(MSVCDetector, 'detect_version')
    def test_detect_capabilities_cpp17(self, mock_version):
        """Test capability detection for C++17"""
        mock_version.return_value = VersionInfo(major=19, minor=14, patch=0)

        capabilities = self.detector.detect_capabilities("/path/to/cl.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)

    @patch.object(MSVCDetector, 'detect_version')
    def test_detect_capabilities_cpp14(self, mock_version):
        """Test capability detection for C++14"""
        mock_version.return_value = VersionInfo(major=19, minor=0, patch=0)

        capabilities = self.detector.detect_capabilities("/path/to/cl.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertFalse(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)

    @patch.object(MSVCDetector, 'detect_version')
    def test_detect_capabilities_no_version(self, mock_version):
        """Test capability detection with no version"""
        mock_version.return_value = None

        capabilities = self.detector.detect_capabilities("/path/to/cl.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertFalse(capabilities.cpp17)
        self.assertFalse(capabilities.cpp14)
        self.assertTrue(capabilities.msvc_compatibility)


class TestMSVCDetectorValidation(unittest.TestCase):
    """Test cases for MSVC compiler validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    def test_validate_nonexistent_compiler(self, mock_exists):
        """Test validation of non-existent compiler"""
        mock_exists.return_value = False

        version = VersionInfo(major=19, minor=40, patch=0)
        capabilities = CapabilityInfo()
        environment = EnvironmentInfo(path="/path/to/compiler")

        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version,
            path="/nonexistent/cl.exe",
            architecture=Architecture.X64,
            capabilities=capabilities,
            environment=environment
        )

        result = self.detector.validate(compiler)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_valid_compiler(self, mock_run, mock_exists):
        """Test validation of valid compiler"""
        # Mock path existence
        def exists_side_effect(path):
            return "cl.exe" in path or "vcvarsall.bat" in path

        mock_exists.side_effect = exists_side_effect

        # Mock cl.exe execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Microsoft (R) C/C++ Optimizing Compiler"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        version = VersionInfo(major=19, minor=40, patch=0)
        capabilities = CapabilityInfo()
        environment = EnvironmentInfo(path="/path/to/compiler")

        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=version,
            path="/path/to/cl.exe",
            architecture=Architecture.X64,
            capabilities=capabilities,
            environment=environment
        )

        result = self.detector.validate(compiler)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)


class TestMSVCDetectorExecutableDetection(unittest.TestCase):
    """Test cases for MSVC executable detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    def test_detect_executables_no_installation(self, mock_exists):
        """Test executable detection with no installation"""
        mock_exists.return_value = False

        installation = {"installationPath": "/nonexistent/path"}
        executables = self.detector._detect_executables(installation)

        self.assertEqual(len(executables), 0)

    @patch('os.path.exists')
    def test_detect_executables_with_installation(self, mock_exists):
        """Test executable detection with installation"""
        # Mock path existence
        def exists_side_effect(path):
            return "cl.exe" in path or "link.exe" in path or "VC" in path

        mock_exists.side_effect = exists_side_effect

        installation = {"installationPath": r"C:\Program Files\Microsoft Visual Studio\2022"}
        executables = self.detector._detect_executables(installation)

        # Should find executables for various architectures
        self.assertGreater(len(executables), 0)


class TestMSVCDetectorWindowsSDKDetection(unittest.TestCase):
    """Test cases for Windows SDK detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_detect_windows_sdk_success(self, mock_listdir, mock_exists):
        """Test successful Windows SDK detection"""
        # Mock path existence
        def exists_side_effect(path):
            return "KitsRoot10" in path or "10." in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing
        mock_listdir.return_value = ["10.0.22621", "10.0.19041"]

        # Note: This test will only work on Windows with winreg
        # On other platforms, it will return None
        sdk_info = self.detector._detect_windows_sdk()

        # On non-Windows platforms, this will be None
        # On Windows, it should return SDK info
        self.assertIsInstance(sdk_info, (WindowsSDKInfo, type(None)))

    @patch('os.path.exists')
    def test_detect_windows_sdk_not_found(self, mock_exists):
        """Test Windows SDK detection when not found"""
        mock_exists.return_value = False

        sdk_info = self.detector._detect_windows_sdk()
        self.assertIsNone(sdk_info)


class TestMSVCDetectorFindVswhere(unittest.TestCase):
    """Test cases for finding vswhere.exe"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch('os.path.exists')
    def test_find_vswhere_found(self, mock_exists):
        """Test finding vswhere.exe"""
        # Mock vswhere exists in first path
        def exists_side_effect(path):
            return "vswhere.exe" in path

        mock_exists.side_effect = exists_side_effect

        vswhere_path = self.detector._find_vswhere()
        self.assertIsNotNone(vswhere_path)
        self.assertTrue("vswhere.exe" in vswhere_path)

    @patch('os.path.exists')
    def test_find_vswhere_not_found(self, mock_exists):
        """Test vswhere.exe not found"""
        mock_exists.return_value = False

        vswhere_path = self.detector._find_vswhere()
        self.assertIsNone(vswhere_path)


class TestMSVCDetectorDetect(unittest.TestCase):
    """Test cases for MSVC detect method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCDetector()

    @patch.object(MSVCDetector, '_detect_via_vswhere')
    @patch.object(MSVCDetector, '_detect_via_standard_paths')
    @patch.object(MSVCDetector, '_detect_via_registry')
    def test_detect_vswhere_success(self, mock_registry, mock_standard, mock_vswhere):
        """Test detect with vswhere success"""
        mock_vswhere.return_value = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="/path/to/cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="/path")
            )
        ]

        compilers = self.detector.detect()

        self.assertEqual(len(compilers), 1)
        mock_vswhere.assert_called_once()
        mock_standard.assert_not_called()
        mock_registry.assert_not_called()

    @patch.object(MSVCDetector, '_detect_via_vswhere')
    @patch.object(MSVCDetector, '_detect_via_standard_paths')
    @patch.object(MSVCDetector, '_detect_via_registry')
    def test_detect_fallback_to_standard_paths(self, mock_registry, mock_standard, mock_vswhere):
        """Test detect fallback to standard paths"""
        mock_vswhere.return_value = []
        mock_standard.return_value = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="/path/to/cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="/path")
            )
        ]

        compilers = self.detector.detect()

        self.assertEqual(len(compilers), 1)
        mock_vswhere.assert_called_once()
        mock_standard.assert_called_once()
        mock_registry.assert_not_called()

    @patch.object(MSVCDetector, '_detect_via_vswhere')
    @patch.object(MSVCDetector, '_detect_via_standard_paths')
    @patch.object(MSVCDetector, '_detect_via_registry')
    def test_detect_fallback_to_registry(self, mock_registry, mock_standard, mock_vswhere):
        """Test detect fallback to registry"""
        mock_vswhere.return_value = []
        mock_standard.return_value = []
        mock_registry.return_value = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="/path/to/cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="/path")
            )
        ]

        compilers = self.detector.detect()

        self.assertEqual(len(compilers), 1)
        mock_vswhere.assert_called_once()
        mock_standard.assert_called_once()
        mock_registry.assert_called_once()

    @patch.object(MSVCDetector, '_detect_via_vswhere')
    @patch.object(MSVCDetector, '_detect_via_standard_paths')
    @patch.object(MSVCDetector, '_detect_via_registry')
    def test_detect_no_compilers_found(self, mock_registry, mock_standard, mock_vswhere):
        """Test detect with no compilers found"""
        mock_vswhere.return_value = []
        mock_standard.return_value = []
        mock_registry.return_value = []

        compilers = self.detector.detect()

        self.assertEqual(len(compilers), 0)


class TestMSVCDetectorInterface(unittest.TestCase):
    """Test cases for MSVCDetector interface compliance"""

    def test_implements_icompiler_detector(self):
        """Test MSVCDetector implements ICompilerDetector"""
        detector = MSVCDetector()
        self.assertIsInstance(detector, ICompilerDetector)

    def test_has_detect_method(self):
        """Test MSVCDetector has detect method"""
        detector = MSVCDetector()
        self.assertTrue(hasattr(detector, 'detect'))
        self.assertTrue(callable(getattr(detector, 'detect')))

    def test_has_detect_version_method(self):
        """Test MSVCDetector has detect_version method"""
        detector = MSVCDetector()
        self.assertTrue(hasattr(detector, 'detect_version'))
        self.assertTrue(callable(getattr(detector, 'detect_version')))

    def test_has_detect_capabilities_method(self):
        """Test MSVCDetector has detect_capabilities method"""
        detector = MSVCDetector()
        self.assertTrue(hasattr(detector, 'detect_capabilities'))
        self.assertTrue(callable(getattr(detector, 'detect_capabilities')))

    def test_has_validate_method(self):
        """Test MSVCDetector has validate method"""
        detector = MSVCDetector()
        self.assertTrue(hasattr(detector, 'validate'))
        self.assertTrue(callable(getattr(detector, 'validate')))


if __name__ == '__main__':
    unittest.main()
