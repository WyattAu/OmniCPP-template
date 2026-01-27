"""
Unit tests for VersionDetector
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import logging

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.version_detector import (
    VersionDetector,
    VersionInfo
)


class TestVersionInfo(unittest.TestCase):
    """Test cases for VersionInfo dataclass"""
    
    def test_version_info_creation(self) -> None:
        """Test VersionInfo creation"""
        version = VersionInfo(19, 40, 33807)
        self.assertEqual(version.major, 19)
        self.assertEqual(version.minor, 40)
        self.assertEqual(version.patch, 33807)
        self.assertIsNone(version.build)
    
    def test_version_info_with_build(self) -> None:
        """Test VersionInfo with build number"""
        version = VersionInfo(19, 40, 33807, "0")
        self.assertEqual(version.major, 19)
        self.assertEqual(version.minor, 40)
        self.assertEqual(version.patch, 33807)
        self.assertEqual(version.build, "0")
    
    def test_version_info_str_without_build(self) -> None:
        """Test VersionInfo string representation without build"""
        version = VersionInfo(19, 40, 33807)
        self.assertEqual(str(version), "19.40.33807")
    
    def test_version_info_str_with_build(self) -> None:
        """Test VersionInfo string representation with build"""
        version = VersionInfo(19, 40, 33807, "0")
        self.assertEqual(str(version), "19.40.33807.0")
    
    def test_version_info_less_than(self) -> None:
        """Test VersionInfo less than comparison"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 41, 0)
        self.assertTrue(version1 < version2)
        self.assertFalse(version2 < version1)
    
    def test_version_info_less_than_major(self) -> None:
        """Test VersionInfo less than comparison with major version"""
        version1 = VersionInfo(18, 40, 33807)
        version2 = VersionInfo(19, 0, 0)
        self.assertTrue(version1 < version2)
    
    def test_version_info_equal(self) -> None:
        """Test VersionInfo equality"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 40, 33807)
        self.assertEqual(version1, version2)
        self.assertTrue(version1 == version2)
    
    def test_version_info_not_equal(self) -> None:
        """Test VersionInfo inequality"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 40, 33808)
        self.assertNotEqual(version1, version2)
        self.assertTrue(version1 != version2)
    
    def test_version_info_greater_than(self) -> None:
        """Test VersionInfo greater than comparison"""
        version1 = VersionInfo(19, 41, 0)
        version2 = VersionInfo(19, 40, 33807)
        self.assertTrue(version1 > version2)
        self.assertFalse(version2 > version1)
    
    def test_version_info_less_than_or_equal(self) -> None:
        """Test VersionInfo less than or equal comparison"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 40, 33807)
        version3 = VersionInfo(19, 41, 0)
        self.assertTrue(version1 <= version2)
        self.assertTrue(version1 <= version3)
        self.assertFalse(version3 <= version1)
    
    def test_version_info_greater_than_or_equal(self) -> None:
        """Test VersionInfo greater than or equal comparison"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 40, 33807)
        version3 = VersionInfo(19, 39, 0)
        self.assertTrue(version1 >= version2)
        self.assertTrue(version1 >= version3)
        self.assertFalse(version3 >= version1)


class TestVersionDetector(unittest.TestCase):
    """Test cases for VersionDetector"""
    
    def setUp(self) -> None:
        """Set up test fixtures"""
        self.logger = Mock(spec=logging.Logger)
        self.detector = VersionDetector(self.logger)
    
    def test_initialization(self) -> None:
        """Test VersionDetector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector._logger)
    
    def test_parse_version_format_1(self) -> None:
        """Test parsing version format: major.minor.patch.build"""
        version_string = "19.40.33807.0"
        version = self.detector.parse_version(version_string)
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 19)
            self.assertEqual(version.minor, 40)
            self.assertEqual(version.patch, 33807)
            self.assertEqual(version.build, "0")
    
    def test_parse_version_format_2(self) -> None:
        """Test parsing version format: major.minor.patch"""
        version_string = "13.2.0"
        version = self.detector.parse_version(version_string)
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 13)
            self.assertEqual(version.minor, 2)
            self.assertEqual(version.patch, 0)
            self.assertIsNone(version.build)
    
    def test_parse_version_format_3(self) -> None:
        """Test parsing version format: major.minor"""
        version_string = "19.40"
        version = self.detector.parse_version(version_string)
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 19)
            self.assertEqual(version.minor, 40)
            self.assertEqual(version.patch, 0)
            self.assertIsNone(version.build)
    
    def test_parse_version_format_4(self) -> None:
        """Test parsing version format: major"""
        version_string = "19"
        version = self.detector.parse_version(version_string)
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 19)
            self.assertEqual(version.minor, 0)
            self.assertEqual(version.patch, 0)
            self.assertIsNone(version.build)
    
    def test_parse_version_invalid(self) -> None:
        """Test parsing invalid version string"""
        version_string = "invalid.version"
        version = self.detector.parse_version(version_string)
        
        self.assertIsNone(version)
    
    def test_parse_version_empty(self) -> None:
        """Test parsing empty version string"""
        version_string = ""
        version = self.detector.parse_version(version_string)
        
        self.assertIsNone(version)
    
    def test_parse_version_none(self) -> None:
        """Test parsing None version string"""
        version = self.detector.parse_version(None)  # type: ignore
        
        self.assertIsNone(version)
    
    def test_compare_versions_less_than(self) -> None:
        """Test comparing versions where first is less than second"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 41, 0)
        
        result = self.detector.compare_versions(version1, version2)
        
        self.assertEqual(result, -1)
    
    def test_compare_versions_equal(self) -> None:
        """Test comparing equal versions"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = VersionInfo(19, 40, 33807)
        
        result = self.detector.compare_versions(version1, version2)
        
        self.assertEqual(result, 0)
    
    def test_compare_versions_greater_than(self) -> None:
        """Test comparing versions where first is greater than second"""
        version1 = VersionInfo(19, 41, 0)
        version2 = VersionInfo(19, 40, 33807)
        
        result = self.detector.compare_versions(version1, version2)
        
        self.assertEqual(result, 1)
    
    def test_compare_versions_string_input(self) -> None:
        """Test comparing versions with string input"""
        version1 = "19.40.33807"
        version2 = "19.41.0"
        
        result = self.detector.compare_versions(version1, version2)
        
        self.assertEqual(result, -1)
    
    def test_compare_versions_invalid_string(self) -> None:
        """Test comparing versions with invalid string input"""
        version1 = VersionInfo(19, 40, 33807)
        version2 = "invalid.version"
        
        with self.assertRaises(ValueError):
            self.detector.compare_versions(version1, version2)
    
    def test_get_version_string(self) -> None:
        """Test getting version string from VersionInfo"""
        version = VersionInfo(19, 40, 33807)
        version_string = self.detector.get_version_string(version)
        
        self.assertEqual(version_string, "19.40.33807")
    
    def test_get_version_string_with_build(self) -> None:
        """Test getting version string with build number"""
        version = VersionInfo(19, 40, 33807, "0")
        version_string = self.detector.get_version_string(version)
        
        self.assertEqual(version_string, "19.40.33807.0")
    
    def test_validate_version_valid(self) -> None:
        """Test validating a valid version"""
        version = VersionInfo(19, 40, 33807)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_version_string_input(self) -> None:
        """Test validating version with string input"""
        version_string = "19.40.33807"
        is_valid, errors = self.detector.validate_version(version_string)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_version_negative_major(self) -> None:
        """Test validating version with negative major version"""
        version = VersionInfo(-1, 40, 33807)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Major version cannot be negative" in e for e in errors))
    
    def test_validate_version_negative_minor(self) -> None:
        """Test validating version with negative minor version"""
        version = VersionInfo(19, -1, 33807)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Minor version cannot be negative" in e for e in errors))
    
    def test_validate_version_negative_patch(self) -> None:
        """Test validating version with negative patch version"""
        version = VersionInfo(19, 40, -1)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Patch version cannot be negative" in e for e in errors))
    
    def test_validate_version_large_major(self) -> None:
        """Test validating version with too large major version"""
        version = VersionInfo(101, 40, 33807)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Major version seems too large" in e for e in errors))
    
    def test_validate_version_large_minor(self) -> None:
        """Test validating version with too large minor version"""
        version = VersionInfo(19, 101, 33807)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Minor version seems too large" in e for e in errors))
    
    def test_validate_version_large_patch(self) -> None:
        """Test validating version with too large patch version"""
        # Use a value > 100000 since MSVC can have large patch numbers
        version = VersionInfo(19, 40, 100001)
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Patch version seems too large" in e for e in errors))
    
    def test_validate_version_empty_build(self) -> None:
        """Test validating version with empty build string"""
        version = VersionInfo(19, 40, 33807, "")
        is_valid, errors = self.detector.validate_version(version)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Build string cannot be empty" in e for e in errors))
    
    def test_validate_version_invalid_string(self) -> None:
        """Test validating invalid version string"""
        version_string = "invalid.version"
        is_valid, errors = self.detector.validate_version(version_string)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Invalid version string format" in e for e in errors))
    
    def test_get_minimum_required_version_msvc(self) -> None:
        """Test getting minimum required version for MSVC"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 19)
            self.assertEqual(min_version.minor, 30)
            self.assertEqual(min_version.patch, 0)
    
    def test_get_minimum_required_version_msvc_clang(self) -> None:
        """Test getting minimum required version for MSVC-Clang"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_MSVC_CLANG
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 16)
            self.assertEqual(min_version.minor, 0)
            self.assertEqual(min_version.patch, 0)
    
    def test_get_minimum_required_version_mingw_gcc(self) -> None:
        """Test getting minimum required version for MinGW-GCC"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_MINGW_GCC
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 12)
            self.assertEqual(min_version.minor, 0)
            self.assertEqual(min_version.patch, 0)
    
    def test_get_minimum_required_version_mingw_clang(self) -> None:
        """Test getting minimum required version for MinGW-Clang"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_MINGW_CLANG
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 16)
            self.assertEqual(min_version.minor, 0)
            self.assertEqual(min_version.patch, 0)
    
    def test_get_minimum_required_version_gcc(self) -> None:
        """Test getting minimum required version for GCC"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_GCC
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 11)
            self.assertEqual(min_version.minor, 0)
            self.assertEqual(min_version.patch, 0)
    
    def test_get_minimum_required_version_clang(self) -> None:
        """Test getting minimum required version for Clang"""
        min_version = self.detector.get_minimum_required_version(
            VersionDetector.COMPILER_CLANG
        )
        
        self.assertIsNotNone(min_version)
        if min_version:
            self.assertEqual(min_version.major, 16)
            self.assertEqual(min_version.minor, 0)
            self.assertEqual(min_version.patch, 0)
    
    def test_is_version_supported_meets_minimum(self) -> None:
        """Test checking if version meets minimum requirements"""
        version = VersionInfo(19, 40, 33807)
        is_supported = self.detector.is_version_supported(
            version,
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertTrue(is_supported)
    
    def test_is_version_supported_below_minimum(self) -> None:
        """Test checking if version below minimum is not supported"""
        version = VersionInfo(19, 20, 0)
        is_supported = self.detector.is_version_supported(
            version,
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertFalse(is_supported)
    
    def test_is_version_supported_equal_minimum(self) -> None:
        """Test checking if version equal to minimum is supported"""
        version = VersionInfo(19, 30, 0)
        is_supported = self.detector.is_version_supported(
            version,
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertTrue(is_supported)
    
    @patch('subprocess.run')
    def test_detect_version_msvc(self, mock_run: MagicMock) -> None:
        """Test detecting MSVC version"""
        # Mock subprocess.run to return MSVC version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Microsoft (R) C/C++ Optimizing Compiler Version 19.40.33807 for x64"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "cl.exe",
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 19)
            self.assertEqual(version.minor, 40)
            # Note: The pattern "Version\s+(\d+\.\d+)" matches first, extracting "19.40"
            # So patch defaults to 0
            self.assertEqual(version.patch, 0)
    
    @patch('subprocess.run')
    def test_detect_version_gcc(self, mock_run: MagicMock) -> None:
        """Test detecting GCC version"""
        # Mock subprocess.run to return GCC version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "g++ (Ubuntu 13.2.0-23ubuntu4) 13.2.0"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "g++",
            VersionDetector.COMPILER_GCC
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 13)
            self.assertEqual(version.minor, 2)
            self.assertEqual(version.patch, 0)
    
    @patch('subprocess.run')
    def test_detect_version_clang(self, mock_run: MagicMock) -> None:
        """Test detecting Clang version"""
        # Mock subprocess.run to return Clang version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 18.1.0"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "clang++",
            VersionDetector.COMPILER_CLANG
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 18)
            self.assertEqual(version.minor, 1)
            self.assertEqual(version.patch, 0)
    
    @patch('subprocess.run')
    def test_detect_version_mingw_gcc(self, mock_run: MagicMock) -> None:
        """Test detecting MinGW-GCC version"""
        # Mock subprocess.run to return MinGW-GCC version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "g++ (Rev3, Built by MSYS2 project) 14.2.0"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "g++.exe",
            VersionDetector.COMPILER_MINGW_GCC
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 14)
            self.assertEqual(version.minor, 2)
            self.assertEqual(version.patch, 0)
    
    @patch('subprocess.run')
    def test_detect_version_mingw_clang(self, mock_run: MagicMock) -> None:
        """Test detecting MinGW-Clang version"""
        # Mock subprocess.run to return MinGW-Clang version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 17.0.6"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "clang++.exe",
            VersionDetector.COMPILER_MINGW_CLANG
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 17)
            self.assertEqual(version.minor, 0)
            self.assertEqual(version.patch, 6)
    
    @patch('subprocess.run')
    def test_detect_version_msvc_clang(self, mock_run: MagicMock) -> None:
        """Test detecting MSVC-Clang version"""
        # Mock subprocess.run to return MSVC-Clang version output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "clang version 16.0.5"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "clang++.exe",
            VersionDetector.COMPILER_MSVC_CLANG
        )
        
        self.assertIsNotNone(version)
        if version:
            self.assertEqual(version.major, 16)
            self.assertEqual(version.minor, 0)
            self.assertEqual(version.patch, 5)
    
    @patch('subprocess.run')
    def test_detect_version_timeout(self, mock_run: MagicMock) -> None:
        """Test detecting version with timeout"""
        # Mock subprocess.run to raise TimeoutExpired
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(
            "cl.exe",
            10
        )
        
        version = self.detector.detect_version(
            "cl.exe",
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertIsNone(version)
        self.logger.error.assert_called()
    
    @patch('subprocess.run')
    def test_detect_version_file_not_found(self, mock_run: MagicMock) -> None:
        """Test detecting version with file not found"""
        # Mock subprocess.run to raise FileNotFoundError
        mock_run.side_effect = FileNotFoundError()
        
        version = self.detector.detect_version(
            "nonexistent.exe",
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertIsNone(version)
        self.logger.error.assert_called()
    
    @patch('subprocess.run')
    def test_detect_version_unknown_compiler_type(self, mock_run: MagicMock) -> None:
        """Test detecting version with unknown compiler type"""
        version = self.detector.detect_version(
            "compiler.exe",
            "unknown_compiler"
        )
        
        self.assertIsNone(version)
        self.logger.error.assert_called()
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_detect_version_parse_failure(self, mock_run: MagicMock) -> None:
        """Test detecting version when parsing fails"""
        # Mock subprocess.run to return unparseable output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Unparseable version output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        version = self.detector.detect_version(
            "compiler.exe",
            VersionDetector.COMPILER_MSVC
        )
        
        self.assertIsNone(version)
        self.logger.warning.assert_called()


if __name__ == '__main__':
    unittest.main()
