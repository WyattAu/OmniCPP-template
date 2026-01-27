"""
Unit tests for Scoop Detector

This module contains comprehensive unit tests for Scoop detector,
covering Scoop installation detection, package detection,
package information retrieval, and validation.
"""

import os
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.scoop_detector import (
    ScoopDetector,
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
            package_manager=PackageManagerType.SCOOP
        )
        self.assertEqual(package.name, "llvm")
        self.assertEqual(package.version, "15.0.7")
        self.assertEqual(package.path, "/path/to/llvm")
        self.assertEqual(package.package_manager, PackageManagerType.SCOOP)

    def test_package_info_with_metadata(self):
        """Test PackageInfo with metadata"""
        package = PackageInfo(
            name="mingw",
            version="12.2.0",
            path="/path/to/mingw",
            package_manager=PackageManagerType.SCOOP,
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
            package_manager=PackageManagerType.SCOOP
        )
        result = package.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "gcc")
        self.assertEqual(result["version"], "13.2.0")
        self.assertEqual(result["path"], "/path/to/gcc")
        self.assertEqual(result["package_manager"], "scoop")

    def test_package_info_is_valid(self):
        """Test PackageInfo is_valid method"""
        # Test with non-existent path
        package = PackageInfo(
            name="clang",
            version="16.0.0",
            path="/nonexistent/path/clang",
            package_manager=PackageManagerType.SCOOP
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


class TestScoopDetectorInitialization(unittest.TestCase):
    """Test cases for ScoopDetector initialization"""

    def test_detector_initialization(self):
        """Test ScoopDetector initialization"""
        detector = ScoopDetector()
        self.assertIsNotNone(detector)
        self.assertIsNone(detector._scoop_path)
        self.assertEqual(len(detector._detected_packages), 0)

    def test_detector_with_logger(self):
        """Test ScoopDetector with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        detector = ScoopDetector(logger=logger)
        self.assertIsNotNone(detector)

    def test_detector_compiler_packages(self):
        """Test ScoopDetector compiler packages list"""
        detector = ScoopDetector()
        self.assertIsInstance(detector.COMPILER_PACKAGES, list)
        self.assertGreater(len(detector.COMPILER_PACKAGES), 0)
        self.assertIn("llvm", detector.COMPILER_PACKAGES)
        self.assertIn("mingw", detector.COMPILER_PACKAGES)
        self.assertIn("gcc", detector.COMPILER_PACKAGES)


class TestScoopDetectorDetectScoop(unittest.TestCase):
    """Test cases for Scoop installation detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()

    @patch('os.path.exists')
    def test_detect_scoop_found(self, mock_exists):
        """Test successful Scoop detection"""
        # Mock Scoop exists in first path
        def exists_side_effect(path):
            return "scoop.exe" in path

        mock_exists.side_effect = exists_side_effect

        scoop_path = self.detector.detect_scoop()

        self.assertIsNotNone(scoop_path)
        self.assertTrue("scoop.exe" in scoop_path)

    @patch('os.path.exists')
    def test_detect_scoop_not_found(self, mock_exists):
        """Test Scoop not found"""
        mock_exists.return_value = False

        scoop_path = self.detector.detect_scoop()

        self.assertIsNone(scoop_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_scoop_via_where(self, mock_run, mock_exists):
        """Test Scoop detection via 'where' command"""
        # Mock path doesn't exist in standard locations, but exists for where result
        def exists_side_effect(path):
            return "scoop.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock 'where' command success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = r"C:\Users\test\scoop\shims\scoop.exe"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        scoop_path = self.detector.detect_scoop()

        self.assertIsNotNone(scoop_path)
        self.assertTrue("scoop.exe" in scoop_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_scoop_where_fails(self, mock_run, mock_exists):
        """Test Scoop detection when 'where' fails"""
        mock_exists.return_value = False

        # Mock 'where' command failure
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command not found"
        mock_run.return_value = mock_result

        scoop_path = self.detector.detect_scoop()

        self.assertIsNone(scoop_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_scoop_timeout(self, mock_run, mock_exists):
        """Test Scoop detection with timeout"""
        mock_exists.return_value = False
        mock_run.side_effect = subprocess.TimeoutExpired("where", 10)

        scoop_path = self.detector.detect_scoop()

        self.assertIsNone(scoop_path)


class TestScoopDetectorDetectPackages(unittest.TestCase):
    """Test cases for package detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()
        self.detector._scoop_path = r"C:\Users\test\scoop\shims\scoop.exe"

    @patch('subprocess.run')
    def test_detect_packages_success(self, mock_run):
        """Test successful package detection"""
        # Mock 'scoop list' output
        scoop_list_output = r"""
llvm 15.0.7
mingw 12.2.0
gcc 13.2.0
cmake 3.27.0
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = scoop_list_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package info retrieval
        with patch.object(self.detector, 'get_package_info') as mock_info:
            mock_info.return_value = PackageInfo(
                name="llvm",
                version="15.0.7",
                path="/path/to/llvm",
                package_manager=PackageManagerType.SCOOP
            )

            packages = self.detector.detect_packages()

            self.assertGreater(len(packages), 0)

    @patch('subprocess.run')
    def test_detect_packages_no_scoop(self, mock_run):
        """Test package detection without Scoop"""
        self.detector._scoop_path = None

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
        mock_run.side_effect = subprocess.TimeoutExpired("scoop", 30)

        packages = self.detector.detect_packages()

        self.assertEqual(len(packages), 0)


class TestScoopDetectorGetPackageInfo(unittest.TestCase):
    """Test cases for package information retrieval"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()
        self.detector._scoop_path = r"C:\Users\test\scoop\shims\scoop.exe"

    @patch('subprocess.run')
    def test_get_package_info_success(self, mock_run):
        """Test successful package info retrieval"""
        # Mock 'scoop info' output
        scoop_info_output = r"""
llvm 15.0.7
Description: LLVM
Version: 15.0.7
Install Location: C:\Users\test\scoop\apps\llvm\current
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = scoop_info_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package path finding
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\Users\test\scoop\apps\llvm\current\bin\clang.exe"

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
    def test_get_package_info_no_scoop(self, mock_run):
        """Test package info retrieval without Scoop"""
        self.detector._scoop_path = None

        package_info = self.detector.get_package_info("llvm")

        self.assertIsNone(package_info)

    @patch('subprocess.run')
    def test_get_package_info_timeout(self, mock_run):
        """Test package info retrieval with timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("scoop", 30)

        package_info = self.detector.get_package_info("llvm")

        self.assertIsNone(package_info)


class TestScoopDetectorValidatePackage(unittest.TestCase):
    """Test cases for package validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()
        self.detector._scoop_path = r"C:\Users\test\scoop\shims\scoop.exe"

    @patch('os.path.exists')
    def test_validate_valid_package(self, mock_exists):
        """Test validation of valid package"""
        # Mock path exists
        def exists_side_effect(path):
            return "scoop.exe" in path or "llvm" in path

        mock_exists.side_effect = exists_side_effect

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.SCOOP
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
            package_manager=PackageManagerType.SCOOP
        )

        result = self.detector.validate_package(package)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_no_scoop(self, mock_exists):
        """Test validation when Scoop is not accessible"""
        # Mock package exists but Scoop doesn't
        def exists_side_effect(path):
            return "llvm" in path

        mock_exists.side_effect = exists_side_effect
        self.detector._scoop_path = None

        package = PackageInfo(
            name="llvm",
            version="15.0.7",
            path="/path/to/llvm",
            package_manager=PackageManagerType.SCOOP
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
            package_manager=PackageManagerType.SCOOP
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)


class TestScoopDetectorDetect(unittest.TestCase):
    """Test cases for Scoop detect method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()

    @patch.object(ScoopDetector, 'detect_scoop')
    @patch.object(ScoopDetector, 'detect_packages')
    def test_detect_success(self, mock_packages, mock_scoop):
        """Test successful detection"""
        mock_scoop.return_value = r"C:\Users\test\scoop\shims\scoop.exe"
        mock_packages.return_value = [
            PackageInfo(
                name="llvm",
                version="15.0.7",
                path="/path/to/llvm",
                package_manager=PackageManagerType.SCOOP
            )
        ]

        packages = self.detector.detect()

        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0].name, "llvm")
        mock_scoop.assert_called_once()
        mock_packages.assert_called_once()

    @patch.object(ScoopDetector, 'detect_scoop')
    def test_detect_no_scoop(self, mock_scoop):
        """Test detection when Scoop not found"""
        mock_scoop.return_value = None

        packages = self.detector.detect()

        self.assertEqual(len(packages), 0)
        mock_scoop.assert_called_once()


class TestScoopDetectorParsePackageList(unittest.TestCase):
    """Test cases for parsing Scoop package list"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()

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
        output = """
Name Version
llvm 15.0.7
mingw 12.2.0
"""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 2)
        self.assertNotIn("name", packages)


class TestScoopDetectorParsePackageInfo(unittest.TestCase):
    """Test cases for parsing Scoop package info"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()
        self.detector._scoop_path = r"C:\Users\test\scoop\shims\scoop.exe"

    def test_parse_package_info_success(self):
        """Test successful package info parsing"""
        output = r"""
llvm 15.0.7
Description: LLVM
Version: 15.0.7
Install Location: C:\Users\test\scoop\apps\llvm\current
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\Users\test\scoop\apps\llvm\current\bin\clang.exe"

            package_info = self.detector._parse_package_info("llvm", output)

            self.assertIsNotNone(package_info)
            self.assertEqual(package_info.name, "llvm")
            self.assertEqual(package_info.version, "15.0.7")
            self.assertEqual(package_info.package_manager, PackageManagerType.SCOOP)

    def test_parse_package_info_no_path(self):
        """Test package info parsing when path not found"""
        output = r"""
llvm 15.0.7
Description: LLVM
Version: 15.0.7
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = None

            package_info = self.detector._parse_package_info("llvm", output)

            self.assertIsNone(package_info)


class TestScoopDetectorFindPackagePath(unittest.TestCase):
    """Test cases for finding package installation path"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_find_package_path_current_dir(self, mock_listdir, mock_exists):
        """Test finding package path with current directory"""
        # Mock path exists
        def exists_side_effect(path):
            return "scoop" in path or "llvm" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with executable
        mock_listdir.return_value = ["clang.exe", "lld.exe", "readme.txt"]

        package_path = self.detector._find_package_path("llvm")

        self.assertIsNotNone(package_path)
        self.assertTrue("llvm" in package_path)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_find_package_path_shims_dir(self, mock_listdir, mock_exists):
        """Test finding package path via shims directory"""
        # Mock path exists - return True for shims directory and gcc.exe shim
        # Return False for apps directory so detector falls through to shims check
        def exists_side_effect(path):
            return ("shims" in path and "apps" not in path) or "gcc.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with shim
        mock_listdir.return_value = ["gcc.exe", "clang.exe", "scoop.exe"]

        package_path = self.detector._find_package_path("gcc")

        self.assertIsNotNone(package_path)
        self.assertTrue("gcc.exe" in package_path)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('subprocess.run')
    def test_find_package_path_via_where(self, mock_run, mock_listdir, mock_exists):
        """Test finding package path via 'where' command"""
        # Mock path doesn't exist in scoop apps
        def exists_side_effect(path):
            # Only return True for clang.exe path from 'where' command
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


class TestScoopDetectorGetScoopPaths(unittest.TestCase):
    """Test cases for getting Scoop installation paths"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ScoopDetector()

    def test_get_scoop_paths(self):
        """Test getting Scoop paths"""
        paths = self.detector._get_scoop_paths()

        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertTrue(any("scoop.exe" in path for path in paths))


if __name__ == '__main__':
    unittest.main()
