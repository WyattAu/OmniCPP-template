"""
Unit tests for Chocolatey Detector

This module contains comprehensive unit tests for Chocolatey detector,
covering Chocolatey installation detection, package detection,
package information retrieval, and validation.
"""

import os
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.chocolatey_detector import (
    ChocolateyDetector,
    PackageManagerType,
    PackageInfo,
    ValidationResult
)


class TestPackageManagerType(unittest.TestCase):
    """Test cases for PackageManagerType enumeration"""

    def test_package_manager_type_chocolatey(self):
        """Test PackageManagerType Chocolatey"""
        self.assertEqual(PackageManagerType.CHOCOLATEY.value, "chocolatey")

    def test_package_manager_type_scoop(self):
        """Test PackageManagerType Scoop"""
        self.assertEqual(PackageManagerType.SCOOP.value, "scoop")

    def test_package_manager_type_winget(self):
        """Test PackageManagerType winget"""
        self.assertEqual(PackageManagerType.WINGET.value, "winget")


class TestPackageInfo(unittest.TestCase):
    """Test cases for PackageInfo dataclass"""

    def test_package_info_creation(self):
        """Test PackageInfo creation"""
        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.CHOCOLATEY
        )
        self.assertEqual(package.name, "llvm")
        self.assertEqual(package.version, "15.0.7")
        self.assertEqual(package.path, "/path/to/llvm")
        self.assertEqual(package.package_manager, PackageManagerType.CHOCOLATEY)

    def test_package_info_with_metadata(self):
        """Test PackageInfo with metadata"""
        package = PackageInfo(
            name="mingw",
            version="12.2.0",
            path="/path/to/mingw",
            package_manager=PackageManagerType.CHOCOLATEY,
            metadata={"key": "value"}
        )
        self.assertEqual(len(package.metadata), 1)
        self.assertEqual(package.metadata["key"], "value")

    def test_package_info_to_dict(self):
        """Test PackageInfo to_dict method"""
        package = PackageInfo(
            name="gcc",
            version="13.2.0",
            path="/path/to/gcc",
            package_manager=PackageManagerType.CHOCOLATEY
        )
        result = package.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "gcc")
        self.assertEqual(result["version"], "13.2.0")
        self.assertEqual(result["path"], "/path/to/gcc")
        self.assertEqual(result["package_manager"], "chocolatey")

    def test_package_info_is_valid(self):
        """Test PackageInfo is_valid method"""
        # Test with non-existent path
        package = PackageInfo(
            name="clang",
            version="16.0.0",
            path="/nonexistent/path/clang",
            package_manager=PackageManagerType.CHOCOLATEY
        )
        self.assertFalse(package.is_valid())


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


class TestChocolateyDetectorInitialization(unittest.TestCase):
    """Test cases for ChocolateyDetector initialization"""

    def test_detector_initialization(self):
        """Test ChocolateyDetector initialization"""
        detector = ChocolateyDetector()
        self.assertIsNotNone(detector)
        self.assertIsNone(detector._choco_path)
        self.assertEqual(len(detector._detected_packages), 0)

    def test_detector_with_logger(self):
        """Test ChocolateyDetector with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        detector = ChocolateyDetector(logger=logger)
        self.assertIsNotNone(detector)

    def test_detector_compiler_packages(self):
        """Test ChocolateyDetector compiler packages list"""
        detector = ChocolateyDetector()
        self.assertIsInstance(detector.COMPILER_PACKAGES, list)
        self.assertGreater(len(detector.COMPILER_PACKAGES), 0)
        self.assertIn("llvm", detector.COMPILER_PACKAGES)
        self.assertIn("mingw", detector.COMPILER_PACKAGES)
        self.assertIn("gcc", detector.COMPILER_PACKAGES)


class TestChocolateyDetectorDetectChoco(unittest.TestCase):
    """Test cases for Chocolatey installation detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()

    @patch('os.path.exists')
    def test_detect_choco_found(self, mock_exists):
        """Test successful Chocolatey detection"""
        # Mock Chocolatey exists in first path
        def exists_side_effect(path):
            return "choco.exe" in path

        mock_exists.side_effect = exists_side_effect

        choco_path = self.detector.detect_choco()

        self.assertIsNotNone(choco_path)
        self.assertTrue("choco.exe" in choco_path)

    @patch('os.path.exists')
    def test_detect_choco_not_found(self, mock_exists):
        """Test Chocolatey not found"""
        mock_exists.return_value = False

        choco_path = self.detector.detect_choco()

        self.assertIsNone(choco_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_choco_via_where(self, mock_run, mock_exists):
        """Test Chocolatey detection via 'where' command"""
        # Mock path doesn't exist in standard locations, but exists for where result
        def exists_side_effect(path):
            return "choco.exe" in path
        
        mock_exists.side_effect = exists_side_effect

        # Mock 'where' command success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = r"C:\ProgramData\chocolatey\bin\choco.exe"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        choco_path = self.detector.detect_choco()

        self.assertIsNotNone(choco_path)
        self.assertTrue("choco.exe" in choco_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_choco_where_fails(self, mock_run, mock_exists):
        """Test Chocolatey detection when 'where' fails"""
        mock_exists.return_value = False

        # Mock 'where' command failure
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command not found"
        mock_run.return_value = mock_result

        choco_path = self.detector.detect_choco()

        self.assertIsNone(choco_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_choco_timeout(self, mock_run, mock_exists):
        """Test Chocolatey detection with timeout"""
        mock_exists.return_value = False
        mock_run.side_effect = subprocess.TimeoutExpired("where", 10)

        choco_path = self.detector.detect_choco()

        self.assertIsNone(choco_path)


class TestChocolateyDetectorDetectPackages(unittest.TestCase):
    """Test cases for package detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()
        self.detector._choco_path = r"C:\ProgramData\chocolatey\bin\choco.exe"

    @patch('subprocess.run')
    def test_detect_packages_success(self, mock_run):
        """Test successful package detection"""
        # Mock 'choco list' output
        choco_list_output = """
llvm 15.0.7
mingw 12.2.0
gcc 13.2.0
cmake 3.27.0
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = choco_list_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package info retrieval
        with patch.object(self.detector, 'get_package_info') as mock_info:
            mock_info.return_value = PackageInfo(
                name="llvm",
                version="15.0.7",
                path="/path/to/llvm",
                package_manager=PackageManagerType.CHOCOLATEY
            )

            packages = self.detector.detect_packages()

            self.assertGreater(len(packages), 0)

    @patch('subprocess.run')
    def test_detect_packages_no_choco(self, mock_run):
        """Test package detection without Chocolatey"""
        self.detector._choco_path = None

        packages = self.detector.detect_packages()

        self.assertEqual(len(packages), 0)

    @patch('subprocess.run')
    def test_detect_packages_list_fails(self, mock_run):
        """Test package detection when list fails"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error listing packages"
        mock_run.return_value = mock_result

        packages = self.detector.detect_packages()

        self.assertEqual(len(packages), 0)

    @patch('subprocess.run')
    def test_detect_packages_timeout(self, mock_run):
        """Test package detection with timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("choco", 30)

        packages = self.detector.detect_packages()

        self.assertEqual(len(packages), 0)


class TestChocolateyDetectorGetPackageInfo(unittest.TestCase):
    """Test cases for package information retrieval"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()
        self.detector._choco_path = r"C:\ProgramData\chocolatey\bin\choco.exe"

    @patch('subprocess.run')
    def test_get_package_info_success(self, mock_run):
        """Test successful package info retrieval"""
        # Mock 'choco info' output
        choco_info_output = """
llvm 15.0.7
Title: LLVM
Version: 15.0.7
Install Location: C:\ProgramData\chocolatey\lib\llvm\tools
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = choco_info_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package path finding
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\ProgramData\chocolatey\lib\llvm\tools\clang.exe"

            package_info = self.detector.get_package_info("llvm")

            self.assertIsNotNone(package_info)
            self.assertEqual(package_info.name, "llvm")
            self.assertEqual(package_info.version, "15.0.7")

    @patch('subprocess.run')
    def test_get_package_info_not_found(self, mock_run):
        """Test package info retrieval when package not found"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Package not found"
        mock_run.return_value = mock_result

        package_info = self.detector.get_package_info("nonexistent")

        self.assertIsNone(package_info)

    @patch('subprocess.run')
    def test_get_package_info_no_choco(self, mock_run):
        """Test package info retrieval without Chocolatey"""
        self.detector._choco_path = None

        package_info = self.detector.get_package_info("llvm")

        self.assertIsNone(package_info)

    @patch('subprocess.run')
    def test_get_package_info_timeout(self, mock_run):
        """Test package info retrieval with timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("choco", 30)

        package_info = self.detector.get_package_info("llvm")

        self.assertIsNone(package_info)


class TestChocolateyDetectorValidatePackage(unittest.TestCase):
    """Test cases for package validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()
        self.detector._choco_path = r"C:\ProgramData\chocolatey\bin\choco.exe"

    @patch('os.path.exists')
    def test_validate_valid_package(self, mock_exists):
        """Test validation of valid package"""
        # Mock path exists
        def exists_side_effect(path):
            return "choco.exe" in path or "llvm" in path

        mock_exists.side_effect = exists_side_effect

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.CHOCOLATEY
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_nonexistent_package(self, mock_exists):
        """Test validation of non-existent package"""
        mock_exists.return_value = False

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/nonexistent/path/llvm",
            package_manager=PackageManagerType.CHOCOLATEY
        )

        result = self.detector.validate_package(package)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_no_choco(self, mock_exists):
        """Test validation when Chocolatey is not accessible"""
        # Mock package exists but Chocolatey doesn't
        def exists_side_effect(path):
            return "llvm" in path

        mock_exists.side_effect = exists_side_effect
        self.detector._choco_path = None

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.CHOCOLATEY
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_validate_directory_no_executables(self, mock_listdir, mock_exists):
        """Test validation of directory with no executables"""
        # Mock path exists
        def exists_side_effect(path):
            return "llvm" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with no executables
        mock_listdir.return_value = ["readme.txt", "license.txt"]

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.CHOCOLATEY
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)


class TestChocolateyDetectorDetect(unittest.TestCase):
    """Test cases for Chocolatey detect method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()

    @patch.object(ChocolateyDetector, 'detect_choco')
    @patch.object(ChocolateyDetector, 'detect_packages')
    def test_detect_success(self, mock_packages, mock_choco):
        """Test successful detection"""
        mock_choco.return_value = r"C:\ProgramData\chocolatey\bin\choco.exe"
        mock_packages.return_value = [
            PackageInfo(
                name="llvm",
                version="15.0.7",
                path="/path/to/llvm",
                package_manager=PackageManagerType.CHOCOLATEY
            )
        ]

        packages = self.detector.detect()

        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0].name, "llvm")
        mock_choco.assert_called_once()
        mock_packages.assert_called_once()

    @patch.object(ChocolateyDetector, 'detect_choco')
    def test_detect_no_choco(self, mock_choco):
        """Test detection when Chocolatey not found"""
        mock_choco.return_value = None

        packages = self.detector.detect()

        self.assertEqual(len(packages), 0)
        mock_choco.assert_called_once()


class TestChocolateyDetectorParsePackageList(unittest.TestCase):
    """Test cases for parsing Chocolatey package list"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()

    def test_parse_package_list_success(self):
        """Test successful package list parsing"""
        output = """
llvm 15.0.7
mingw 12.2.0
gcc 13.2.0
cmake 3.27.0
ninja 1.11.0
"""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 5)
        self.assertIn("llvm", packages)
        self.assertIn("mingw", packages)
        self.assertIn("gcc", packages)

    def test_parse_package_list_empty(self):
        """Test parsing empty package list"""
        output = ""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 0)

    def test_parse_package_list_with_headers(self):
        """Test parsing package list with headers"""
        output = r"""
Chocolatey v0.10.15
llvm 15.0.7
mingw 12.2.0
"""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 2)
        self.assertNotIn("chocolatey", packages)


class TestChocolateyDetectorParsePackageInfo(unittest.TestCase):
    """Test cases for parsing Chocolatey package info"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()
        self.detector._choco_path = r"C:\ProgramData\chocolatey\bin\choco.exe"

    def test_parse_package_info_success(self):
        """Test successful package info parsing"""
        output = """
llvm 15.0.7
Title: LLVM
Version: 15.0.7
Install Location: C:\ProgramData\chocolatey\lib\llvm\tools
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\ProgramData\chocolatey\lib\llvm\tools\clang.exe"

            package_info = self.detector._parse_package_info("llvm", output)

            self.assertIsNotNone(package_info)
            self.assertEqual(package_info.name, "llvm")
            self.assertEqual(package_info.version, "15.0.7")
            self.assertEqual(package_info.package_manager, PackageManagerType.CHOCOLATEY)

    def test_parse_package_info_no_path(self):
        """Test package info parsing when path not found"""
        output = """
llvm 15.0.7
Title: LLVM
Version: 15.0.7
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = None

            package_info = self.detector._parse_package_info("llvm", output)

            self.assertIsNone(package_info)


class TestChocolateyDetectorFindPackagePath(unittest.TestCase):
    """Test cases for finding package installation path"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_find_package_path_tools_dir(self, mock_listdir, mock_exists):
        """Test finding package path with tools directory"""
        # Mock path exists
        def exists_side_effect(path):
            return "chocolatey" in path or "llvm" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with executable
        mock_listdir.return_value = ["clang.exe", "lld.exe", "readme.txt"]

        package_path = self.detector._find_package_path("llvm")

        self.assertIsNotNone(package_path)
        self.assertTrue("llvm" in package_path)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_find_package_path_bin_dir(self, mock_listdir, mock_exists):
        """Test finding package path with bin directory"""
        # Mock path exists
        def exists_side_effect(path):
            return "chocolatey" in path or "mingw" in path or "bin" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with executable
        mock_listdir.return_value = ["gcc.exe", "g++.exe"]

        package_path = self.detector._find_package_path("mingw")

        self.assertIsNotNone(package_path)
        self.assertTrue("mingw" in package_path)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('subprocess.run')
    def test_find_package_path_via_where(self, mock_run, mock_listdir, mock_exists):
        """Test finding package path via 'where' command"""
        # Mock path doesn't exist in chocolatey lib
        def exists_side_effect(path):
            # Only return True for the clang.exe path from 'where' command
            return "clang.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock 'where' command success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = r"C:\Program Files\LLVM\bin\clang.exe"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        package_path = self.detector._find_package_path("clang")

        self.assertIsNotNone(package_path)
        self.assertTrue("clang.exe" in package_path)

    @patch('os.path.exists')
    def test_find_package_path_not_found(self, mock_exists):
        """Test package path not found"""
        mock_exists.return_value = False

        package_path = self.detector._find_package_path("nonexistent")

        self.assertIsNone(package_path)


class TestChocolateyDetectorGetChocoPaths(unittest.TestCase):
    """Test cases for getting Chocolatey installation paths"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ChocolateyDetector()

    def test_get_choco_paths(self):
        """Test getting Chocolatey paths"""
        paths = self.detector._get_choco_paths()

        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertTrue(any("choco.exe" in path for path in paths))


if __name__ == '__main__':
    unittest.main()
