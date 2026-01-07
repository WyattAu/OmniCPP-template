"""
Unit tests for MSVC-Clang Compiler Detector

This module provides comprehensive unit tests for the MSVC-Clang detector,
including bundled LLVM detection, standalone LLVM detection, and package manager detection.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Optional

# Import the detector and related classes
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.msvc_clang_detector import (
    MSVCClangDetector,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    CompilerInfo,
    ValidationResult
)


class TestMSVCClangDetector(unittest.TestCase):
    """Test cases for MSVCClangDetector"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MSVCClangDetector(logger=self.logger)

    def test_initialization(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector._logger)
        self.assertIsInstance(self.detector._vswhere_paths, list)
        self.assertIsInstance(self.detector._standard_paths, list)
        self.assertIsInstance(self.detector._package_manager_paths, dict)
        self.assertEqual(len(self.detector._detected_compilers), 0)

    def test_get_vswhere_paths(self):
        """Test vswhere path detection"""
        paths = self.detector._get_vswhere_paths()
        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertTrue(any("vswhere.exe" in path for path in paths))

    def test_get_standard_paths(self):
        """Test standard LLVM path detection"""
        paths = self.detector._get_standard_paths()
        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertTrue(any("LLVM" in path for path in paths))

    def test_get_package_manager_paths(self):
        """Test package manager path detection"""
        paths = self.detector._get_package_manager_paths()
        self.assertIsInstance(paths, dict)
        self.assertIn("chocolatey", paths)
        self.assertIn("scoop", paths)
        self.assertIn("winget", paths)

    def test_find_vswhere_not_found(self):
        """Test vswhere not found scenario"""
        with patch.object(self.detector, '_vswhere_paths', []):
            result = self.detector._find_vswhere()
            self.assertIsNone(result)

    def test_find_vswhere_found(self):
        """Test vswhere found scenario"""
        with tempfile.NamedTemporaryFile(suffix="vswhere.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with patch.object(self.detector, '_vswhere_paths', [tmp_path]):
                result = self.detector._find_vswhere()
                self.assertEqual(result, tmp_path)
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_detect_version_success(self, mock_run):
        """Test successful version detection"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 18.1.3 (https://github.com/llvm/llvm-project.git)\n"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            version = self.detector.detect_version(tmp_path)
            self.assertIsNotNone(version)
            self.assertEqual(version.major, 18)
            self.assertEqual(version.minor, 1)
            self.assertEqual(version.patch, 3)
            self.assertEqual(str(version), "18.1.3")
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_detect_version_failure(self, mock_run):
        """Test version detection failure"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Error executing clang-cl.exe"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            version = self.detector.detect_version(tmp_path)
            self.assertIsNone(version)
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_detect_version_file_not_found(self, mock_run):
        """Test version detection with non-existent file"""
        version = self.detector.detect_version("nonexistent.exe")
        self.assertIsNone(version)
        mock_run.assert_not_called()

    @patch('subprocess.run')
    def test_detect_capabilities_clang_18(self, mock_run):
        """Test capability detection for Clang 18"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 18.1.3\n"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            capabilities = self.detector.detect_capabilities(tmp_path)
            self.assertTrue(capabilities.cpp23)
            self.assertTrue(capabilities.cpp20)
            self.assertTrue(capabilities.cpp17)
            self.assertTrue(capabilities.cpp14)
            self.assertTrue(capabilities.modules)
            self.assertTrue(capabilities.coroutines)
            self.assertTrue(capabilities.concepts)
            self.assertTrue(capabilities.ranges)
            self.assertTrue(capabilities.std_format)
            self.assertTrue(capabilities.msvc_compatibility)
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_detect_capabilities_clang_17(self, mock_run):
        """Test capability detection for Clang 17"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 17.0.6\n"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            capabilities = self.detector.detect_capabilities(tmp_path)
            self.assertFalse(capabilities.cpp23)
            self.assertTrue(capabilities.cpp20)
            self.assertTrue(capabilities.cpp17)
            self.assertTrue(capabilities.cpp14)
            self.assertTrue(capabilities.modules)
            self.assertTrue(capabilities.coroutines)
            self.assertTrue(capabilities.concepts)
            self.assertTrue(capabilities.ranges)
            self.assertTrue(capabilities.std_format)
            self.assertTrue(capabilities.msvc_compatibility)
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_detect_capabilities_clang_16(self, mock_run):
        """Test capability detection for Clang 16"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 16.0.6\n"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            capabilities = self.detector.detect_capabilities(tmp_path)
            self.assertFalse(capabilities.cpp23)
            self.assertFalse(capabilities.cpp20)
            self.assertTrue(capabilities.cpp17)
            self.assertTrue(capabilities.cpp14)
            self.assertTrue(capabilities.modules)
            self.assertTrue(capabilities.coroutines)
            self.assertTrue(capabilities.concepts)
            self.assertTrue(capabilities.ranges)
            self.assertTrue(capabilities.std_format)
            self.assertTrue(capabilities.msvc_compatibility)
        finally:
            os.unlink(tmp_path)

    @patch('subprocess.run')
    def test_validate_success(self, mock_run):
        """Test successful compiler validation"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 18.1.3\n"
        mock_run.return_value = mock_result

        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            compiler_info = CompilerInfo(
                compiler_type=CompilerType.MSVC_CLANG,
                version=VersionInfo(major=18, minor=1, patch=3),
                path=tmp_path,
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path=os.path.dirname(tmp_path))
            )

            result = self.detector.validate(compiler_info)
            self.assertTrue(result.is_valid)
            self.assertEqual(len(result.errors), 0)
        finally:
            os.unlink(tmp_path)

    def test_validate_file_not_found(self):
        """Test validation with non-existent file"""
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="nonexistent.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="")
        )

        result = self.detector.validate(compiler_info)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertTrue(any("not found" in error for error in result.errors))

    @patch('subprocess.run')
    def test_detect_bundled_llvm_vswhere_not_found(self, mock_run):
        """Test bundled LLVM detection when vswhere not found"""
        with patch.object(self.detector, '_find_vswhere', return_value=None):
            compilers = self.detector._detect_bundled_llvm()
            self.assertEqual(len(compilers), 0)

    @patch('subprocess.run')
    def test_detect_bundled_llvm_vswhere_error(self, mock_run):
        """Test bundled LLVM detection when vswhere fails"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "vswhere error"
        mock_run.return_value = mock_result

        with patch.object(self.detector, '_find_vswhere', return_value="vswhere.exe"):
            compilers = self.detector._detect_bundled_llvm()
            self.assertEqual(len(compilers), 0)

    @patch('subprocess.run')
    def test_detect_bundled_llvm_success(self, mock_run):
        """Test successful bundled LLVM detection"""
        # Create temporary VS installation structure
        with tempfile.TemporaryDirectory() as tmp_dir:
            vs_path = os.path.join(tmp_dir, "VS")
            llvm_path = os.path.join(vs_path, "VC", "Tools", "Llvm")
            x64_bin_path = os.path.join(llvm_path, "x64", "bin")
            os.makedirs(x64_bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(x64_bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            # Mock vswhere output
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps([{
                "installationPath": vs_path,
                "productId": "test.product",
                "displayName": "Visual Studio Community 2022"
            }])
            mock_run.return_value = mock_result

            with patch.object(self.detector, '_find_vswhere', return_value="vswhere.exe"):
                compilers = self.detector._detect_bundled_llvm()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC_CLANG)
                self.assertEqual(compilers[0].architecture, Architecture.X64)
                self.assertEqual(compilers[0].metadata["installation_type"], "bundled")
                self.assertEqual(compilers[0].metadata["vs_version"], "2022")

    def test_detect_standalone_llvm_no_installations(self):
        """Test standalone LLVM detection with no installations"""
        with patch.object(self.detector, '_standard_paths', []):
            compilers = self.detector._detect_standalone_llvm()
            self.assertEqual(len(compilers), 0)

    def test_detect_standalone_llvm_success(self):
        """Test successful standalone LLVM detection"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bin_path = os.path.join(tmp_dir, "bin")
            os.makedirs(bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            with patch.object(self.detector, '_standard_paths', [tmp_dir]):
                compilers = self.detector._detect_standalone_llvm()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC_CLANG)
                self.assertEqual(compilers[0].metadata["installation_type"], "standalone")

    def test_detect_chocolatey_llvm_no_installations(self):
        """Test Chocolatey LLVM detection with no installations"""
        with patch.object(self.detector, '_package_manager_paths', {"chocolatey": []}):
            compilers = self.detector._detect_chocolatey_llvm()
            self.assertEqual(len(compilers), 0)

    def test_detect_chocolatey_llvm_success(self):
        """Test successful Chocolatey LLVM detection"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bin_path = os.path.join(tmp_dir, "bin")
            os.makedirs(bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            with patch.object(self.detector, '_package_manager_paths', {"chocolatey": [tmp_dir]}):
                compilers = self.detector._detect_chocolatey_llvm()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC_CLANG)
                self.assertEqual(compilers[0].metadata["package_manager"], "chocolatey")

    def test_detect_scoop_llvm_no_installations(self):
        """Test Scoop LLVM detection with no installations"""
        with patch.object(self.detector, '_package_manager_paths', {"scoop": []}):
            compilers = self.detector._detect_scoop_llvm()
            self.assertEqual(len(compilers), 0)

    def test_detect_scoop_llvm_success(self):
        """Test successful Scoop LLVM detection"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bin_path = os.path.join(tmp_dir, "bin")
            os.makedirs(bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            with patch.object(self.detector, '_package_manager_paths', {"scoop": [tmp_dir]}):
                compilers = self.detector._detect_scoop_llvm()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC_CLANG)
                self.assertEqual(compilers[0].metadata["package_manager"], "scoop")

    def test_detect_winget_llvm_no_installations(self):
        """Test winget LLVM detection with no installations"""
        with patch.object(self.detector, '_package_manager_paths', {"winget": []}):
            compilers = self.detector._detect_winget_llvm()
            self.assertEqual(len(compilers), 0)

    def test_detect_winget_llvm_success(self):
        """Test successful winget LLVM detection"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bin_path = os.path.join(tmp_dir, "bin")
            os.makedirs(bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            with patch.object(self.detector, '_package_manager_paths', {"winget": [tmp_dir]}):
                compilers = self.detector._detect_winget_llvm()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC_CLANG)
                self.assertEqual(compilers[0].metadata["package_manager"], "winget")

    def test_detect_via_package_managers(self):
        """Test detection via all package managers"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            bin_path = os.path.join(tmp_dir, "bin")
            os.makedirs(bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            with patch.object(self.detector, '_package_manager_paths', {
                "chocolatey": [tmp_dir],
                "scoop": [],
                "winget": []
            }):
                compilers = self.detector._detect_via_package_managers()
                self.assertEqual(len(compilers), 1)
                self.assertEqual(compilers[0].metadata["package_manager"], "chocolatey")

    def test_parse_bundled_llvm_installation_no_path(self):
        """Test parsing bundled LLVM installation with no path"""
        installation = {}
        result = self.detector._parse_bundled_llvm_installation(installation)
        self.assertIsNone(result)

    def test_parse_bundled_llvm_installation_no_llvm(self):
        """Test parsing bundled LLVM installation with no LLVM directory"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            installation = {
                "installationPath": tmp_dir,
                "productId": "test.product",
                "displayName": "Visual Studio Community 2022"
            }
            result = self.detector._parse_bundled_llvm_installation(installation)
            self.assertIsNone(result)

    @patch('subprocess.run')
    def test_parse_bundled_llvm_installation_success(self, mock_run):
        """Test successful parsing of bundled LLVM installation"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            vs_path = os.path.join(tmp_dir, "VS")
            llvm_path = os.path.join(vs_path, "VC", "Tools", "Llvm")
            x64_bin_path = os.path.join(llvm_path, "x64", "bin")
            os.makedirs(x64_bin_path, exist_ok=True)

            # Create dummy clang-cl.exe
            clang_cl_path = os.path.join(x64_bin_path, "clang-cl.exe")
            with open(clang_cl_path, 'w') as f:
                f.write("dummy")

            # Mock version detection
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "clang version 18.1.3\n"
            mock_run.return_value = mock_result

            installation = {
                "installationPath": vs_path,
                "productId": "test.product",
                "displayName": "Visual Studio Community 2022"
            }
            result = self.detector._parse_bundled_llvm_installation(installation)
            self.assertIsNotNone(result)
            self.assertEqual(result.compiler_type, CompilerType.MSVC_CLANG)
            self.assertEqual(result.architecture, Architecture.X64)
            self.assertEqual(result.metadata["installation_type"], "bundled")
            self.assertEqual(result.metadata["vs_version"], "2022")

    @patch('subprocess.run')
    def test_detect_no_compilers(self, mock_run):
        """Test detection when no compilers are found"""
        with patch.object(self.detector, '_find_vswhere', return_value=None):
            with patch.object(self.detector, '_standard_paths', []):
                with patch.object(self.detector, '_package_manager_paths', {
                    "chocolatey": [],
                    "scoop": [],
                    "winget": []
                }):
                    compilers = self.detector.detect()
                    self.assertEqual(len(compilers), 0)

    @patch('subprocess.run')
    def test_detect_multiple_compilers(self, mock_run):
        """Test detection of multiple compilers"""
        # Create temporary installations
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Standalone LLVM
            standalone_path = os.path.join(tmp_dir, "standalone")
            standalone_bin = os.path.join(standalone_path, "bin")
            os.makedirs(standalone_bin, exist_ok=True)
            standalone_clang = os.path.join(standalone_bin, "clang-cl.exe")
            with open(standalone_clang, 'w') as f:
                f.write("dummy")

            # Chocolatey LLVM
            chocolatey_path = os.path.join(tmp_dir, "chocolatey")
            chocolatey_bin = os.path.join(chocolatey_path, "bin")
            os.makedirs(chocolatey_bin, exist_ok=True)
            chocolatey_clang = os.path.join(chocolatey_bin, "clang-cl.exe")
            with open(chocolatey_clang, 'w') as f:
                f.write("dummy")

            # Mock version detection
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "clang version 18.1.3\n"
            mock_run.return_value = mock_result

            with patch.object(self.detector, '_standard_paths', [standalone_path]):
                with patch.object(self.detector, '_package_manager_paths', {
                    "chocolatey": [chocolatey_path],
                    "scoop": [],
                    "winget": []
                }):
                    with patch.object(self.detector, '_find_vswhere', return_value=None):
                        compilers = self.detector.detect()
                        self.assertEqual(len(compilers), 2)
                        # Check that compilers are sorted by version
                        self.assertEqual(compilers[0].metadata["recommended"], "true")

    def test_version_info_comparison(self):
        """Test VersionInfo comparison"""
        v1 = VersionInfo(major=18, minor=1, patch=3)
        v2 = VersionInfo(major=18, minor=1, patch=4)
        v3 = VersionInfo(major=18, minor=2, patch=0)
        v4 = VersionInfo(major=19, minor=0, patch=0)

        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertTrue(v3 < v4)
        self.assertFalse(v4 < v1)

    def test_version_info_string_representation(self):
        """Test VersionInfo string representation"""
        v1 = VersionInfo(major=18, minor=1, patch=3)
        self.assertEqual(str(v1), "18.1.3")

        v2 = VersionInfo(major=18, minor=1, patch=3, build="12345")
        self.assertEqual(str(v2), "18.1.3.12345")

    def test_capability_info_to_dict(self):
        """Test CapabilityInfo to_dict conversion"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            cpp14=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True,
            msvc_compatibility=True
        )
        result = capabilities.to_dict()
        self.assertIsInstance(result, dict)
        self.assertTrue(result["cpp23"])
        self.assertTrue(result["cpp20"])
        self.assertTrue(result["cpp17"])
        self.assertTrue(result["cpp14"])
        self.assertTrue(result["modules"])
        self.assertTrue(result["coroutines"])
        self.assertTrue(result["concepts"])
        self.assertTrue(result["ranges"])
        self.assertTrue(result["std_format"])
        self.assertTrue(result["msvc_compatibility"])

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

    def test_environment_info_to_dict(self):
        """Test EnvironmentInfo to_dict conversion"""
        env_info = EnvironmentInfo(
            path="/path/to/compiler",
            include_paths=["/include/path1", "/include/path2"],
            library_paths=["/lib/path1", "/lib/path2"],
            environment_variables={"VAR1": "value1", "VAR2": "value2"}
        )
        result = env_info.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["path"], "/path/to/compiler")
        self.assertEqual(len(result["include_paths"]), 2)
        self.assertEqual(len(result["library_paths"]), 2)
        self.assertEqual(len(result["environment_variables"]), 2)

    def test_compiler_info_to_dict(self):
        """Test CompilerInfo to_dict conversion"""
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="/path/to/clang-cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="/path/to/compiler"),
            metadata={"key": "value"}
        )
        result = compiler_info.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["compiler_type"], "msvc_clang")
        self.assertEqual(result["version"], "18.1.3")
        self.assertEqual(result["path"], "/path/to/clang-cl.exe")
        self.assertEqual(result["architecture"], "x64")
        self.assertIsInstance(result["capabilities"], dict)
        self.assertIsInstance(result["environment"], dict)
        self.assertEqual(result["metadata"]["key"], "value")

    def test_compiler_info_is_valid(self):
        """Test CompilerInfo is_valid method"""
        with tempfile.NamedTemporaryFile(suffix="clang-cl.exe", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            compiler_info = CompilerInfo(
                compiler_type=CompilerType.MSVC_CLANG,
                version=VersionInfo(major=18, minor=1, patch=3),
                path=tmp_path,
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path=os.path.dirname(tmp_path))
            )
            self.assertTrue(compiler_info.is_valid())
        finally:
            os.unlink(tmp_path)

    def test_compiler_info_is_invalid(self):
        """Test CompilerInfo is_valid method with non-existent file"""
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="nonexistent.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="")
        )
        self.assertFalse(compiler_info.is_valid())

    def test_validation_result_to_dict(self):
        """Test ValidationResult to_dict conversion"""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=["warning1", "warning2"]
        )
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertTrue(result_dict["is_valid"])
        self.assertEqual(len(result_dict["errors"]), 0)
        self.assertEqual(len(result_dict["warnings"]), 2)


if __name__ == '__main__':
    unittest.main()
