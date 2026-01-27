"""
Unit tests for winget Detector

This module contains comprehensive unit tests for winget detector,
covering winget installation detection, package detection,
package information retrieval, and validation.
"""

import os
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.winget_detector import (
    WingetDetector,
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
            name="LLVM.LLVM",
            version="17.0.6",
            path="/path/to/llvm",
            package_manager=PackageManagerType.WINGET
        )
        self.assertEqual(package.name, "LLVM.LLVM")
        self.assertEqual(package.version, "17.0.6")
        self.assertEqual(package.path, "/path/to/llvm")
        self.assertEqual(package.package_manager, PackageManagerType.WINGET)

    def test_package_info_with_metadata(self):
        """Test PackageInfo with metadata"""
        package = PackageInfo(
            name="GNU.Mingw",
            version="12.2.0",
            path="/path/to/mingw",
            package_manager=PackageManagerType.WINGET,
            metadata={"key": "value"}
        )
        self.assertEqual(len(package.metadata), 1)
        self.assertEqual(package.metadata["key"], "value")

    def test_package_info_to_dict(self):
        """Test PackageInfo to_dict method"""
        package = PackageInfo(
            name="LLVM.Clang",
            version="16.0.0",
            path="/path/to/clang",
            package_manager=PackageManagerType.WINGET
        )
        result = package.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "LLVM.Clang")
        self.assertEqual(result["version"], "16.0.0")
        self.assertEqual(result["path"], "/path/to/clang")
        self.assertEqual(result["package_manager"], "winget")

    def test_package_info_is_valid(self):
        """Test PackageInfo is_valid method"""
        # Test with non-existent path
        package = PackageInfo(
            name="GCC.GCC",
            version="13.2.0",
            path="/nonexistent/path/gcc",
            package_manager=PackageManagerType.WINGET
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


class TestWingetDetectorInitialization(unittest.TestCase):
    """Test cases for WingetDetector initialization"""

    def test_detector_initialization(self):
        """Test WingetDetector initialization"""
        detector = WingetDetector()
        self.assertIsNotNone(detector)
        self.assertIsNone(detector._winget_path)
        self.assertEqual(len(detector._detected_packages), 0)

    def test_detector_with_logger(self):
        """Test WingetDetector with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        detector = WingetDetector(logger=logger)
        self.assertIsNotNone(detector)

    def test_detector_compiler_packages(self):
        """Test WingetDetector compiler packages list"""
        detector = WingetDetector()
        self.assertIsInstance(detector.COMPILER_PACKAGES, list)
        self.assertGreater(len(detector.COMPILER_PACKAGES), 0)
        self.assertIn("LLVM.LLVM", detector.COMPILER_PACKAGES)
        self.assertIn("GNU.Mingw", detector.COMPILER_PACKAGES)
        self.assertIn("GCC.GCC", detector.COMPILER_PACKAGES)


class TestWingetDetectorDetectWinget(unittest.TestCase):
    """Test cases for winget installation detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()

    @patch('os.path.exists')
    def test_detect_winget_found(self, mock_exists):
        """Test successful winget detection"""
        # Mock winget exists in first path
        def exists_side_effect(path):
            return "winget.exe" in path

        mock_exists.side_effect = exists_side_effect

        winget_path = self.detector.detect_winget()

        self.assertIsNotNone(winget_path)
        self.assertTrue("winget.exe" in winget_path)

    @patch('os.path.exists')
    def test_detect_winget_not_found(self, mock_exists):
        """Test winget not found"""
        mock_exists.return_value = False

        winget_path = self.detector.detect_winget()

        self.assertIsNone(winget_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_winget_via_where(self, mock_run, mock_exists):
        """Test winget detection via 'where' command"""
        # Mock path doesn't exist in standard locations, but exists for where result
        def exists_side_effect(path):
            return "winget.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock 'where' command success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        winget_path = self.detector.detect_winget()

        self.assertIsNotNone(winget_path)
        self.assertTrue("winget.exe" in winget_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_winget_where_fails(self, mock_run, mock_exists):
        """Test winget detection when 'where' fails"""
        mock_exists.return_value = False

        # Mock 'where' command failure
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command not found"
        mock_run.return_value = mock_result

        winget_path = self.detector.detect_winget()

        self.assertIsNone(winget_path)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_winget_timeout(self, mock_run, mock_exists):
        """Test winget detection with timeout"""
        mock_exists.return_value = False
        mock_run.side_effect = subprocess.TimeoutExpired("where", 10)

        winget_path = self.detector.detect_winget()

        self.assertIsNone(winget_path)


class TestWingetDetectorDetectPackages(unittest.TestCase):
    """Test cases for package detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()
        self.detector._winget_path = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"

    @patch('subprocess.run')
    def test_detect_packages_success(self, mock_run):
        """Test successful package detection"""
        # Mock 'winget list' output
        winget_list_output = r"""
Name           Id              Version        Available Source
----------------------------------------------------------------
LLVM           LLVM.LLVM        17.0.6         18.1.0    winget
MinGW          GNU.Mingw        12.2.0         13.0.0    winget
CMake          Kitware.CMake    3.27.0         3.28.0    winget
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = winget_list_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package info retrieval
        with patch.object(self.detector, 'get_package_info') as mock_info:
            mock_info.return_value = PackageInfo(
                name="LLVM.LLVM",
                version="17.0.6",
                path="/path/to/llvm",
                package_manager=PackageManagerType.WINGET
            )

            packages = self.detector.detect_packages()

            self.assertGreater(len(packages), 0)

    @patch('subprocess.run')
    def test_detect_packages_no_winget(self, mock_run):
        """Test package detection without winget"""
        self.detector._winget_path = None

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
        mock_run.side_effect = subprocess.TimeoutExpired("winget", 30)

        packages = self.detector.detect_packages()

        self.assertEqual(len(packages), 0)


class TestWingetDetectorGetPackageInfo(unittest.TestCase):
    """Test cases for package information retrieval"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()
        self.detector._winget_path = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"

    @patch('subprocess.run')
    def test_get_package_info_success(self, mock_run):
        """Test successful package info retrieval"""
        # Mock 'winget show' output
        winget_info_output = r"""
Name: LLVM
Id: LLVM.LLVM
Version: 17.0.6
Install Location: C:\Program Files\LLVM
"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = winget_info_output
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Mock package path finding
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\Program Files\LLVM\bin\clang.exe"

            package_info = self.detector.get_package_info("LLVM.LLVM")

            self.assertIsNotNone(package_info)
            self.assertEqual(package_info.name, "LLVM.LLVM")
            self.assertEqual(package_info.version, "17.0.6")

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
    def test_get_package_info_no_winget(self, mock_run):
        """Test package info retrieval without winget"""
        self.detector._winget_path = None

        package_info = self.detector.get_package_info("LLVM.LLVM")

        self.assertIsNone(package_info)

    @patch('subprocess.run')
    def test_get_package_info_timeout(self, mock_run):
        """Test package info retrieval with timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("winget", 30)

        package_info = self.detector.get_package_info("LLVM.LLVM")

        self.assertIsNone(package_info)


class TestWingetDetectorValidatePackage(unittest.TestCase):
    """Test cases for package validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()
        self.detector._winget_path = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"

    @patch('os.path.exists')
    def test_validate_valid_package(self, mock_exists):
        """Test validation of valid package"""
        # Mock path exists
        def exists_side_effect(path):
            return "winget.exe" in path or "llvm" in path

        mock_exists.side_effect = exists_side_effect

        package = PackageInfo(
            name="LLVM.LLVM",
            version="17.0.6",
            path="/path/to/llvm",
            package_manager=PackageManagerType.WINGET
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_nonexistent_package(self, mock_exists):
        """Test validation of non-existent package"""
        mock_exists.return_value = False

        package = PackageInfo(
            name="LLVM.LLVM",
            version="17.0.6",
            path="/nonexistent/path/llvm",
            package_manager=PackageManagerType.WINGET
        )

        result = self.detector.validate_package(package)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_no_winget(self, mock_exists):
        """Test validation when winget is not accessible"""
        # Mock package exists but winget doesn't
        def exists_side_effect(path):
            return "llvm" in path

        mock_exists.side_effect = exists_side_effect
        self.detector._winget_path = None

        package = PackageInfo(
            name="LLVM.LLVM",
            version="17.0.6",
            path="/path/to/llvm",
            package_manager=PackageManagerType.WINGET
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
            name="LLVM.LLVM",
            version="17.0.6",
            path="/path/to/llvm",
            package_manager=PackageManagerType.WINGET
        )

        result = self.detector.validate_package(package)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)


class TestWingetDetectorDetect(unittest.TestCase):
    """Test cases for winget detect method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()

    @patch.object(WingetDetector, 'detect_winget')
    @patch.object(WingetDetector, 'detect_packages')
    def test_detect_success(self, mock_packages, mock_winget):
        """Test successful detection"""
        mock_winget.return_value = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"
        mock_packages.return_value = [
            PackageInfo(
                name="LLVM.LLVM",
                version="17.0.6",
                path="/path/to/llvm",
                package_manager=PackageManagerType.WINGET
            )
        ]

        packages = self.detector.detect()

        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0].name, "LLVM.LLVM")
        mock_winget.assert_called_once()
        mock_packages.assert_called_once()

    @patch.object(WingetDetector, 'detect_winget')
    def test_detect_no_winget(self, mock_winget):
        """Test detection when winget not found"""
        mock_winget.return_value = None

        packages = self.detector.detect()

        self.assertEqual(len(packages), 0)
        mock_winget.assert_called_once()


class TestWingetDetectorParsePackageList(unittest.TestCase):
    """Test cases for parsing winget package list"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()

    def test_parse_package_list_success(self):
        """Test successful package list parsing"""
        output = """
Name           Id              Version        Available Source
----------------------------------------------------------------
LLVM           LLVM.LLVM        17.0.6         18.1.0    winget
MinGW          GNU.Mingw        12.2.0         13.0.0    winget
CMake          Kitware.CMake    3.27.0         3.28.0    winget
Ninja          Ninja-build.Ninja 1.11.0          1.12.0    winget
"""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 4)
        self.assertIn("LLVM.LLVM", packages)
        self.assertIn("GNU.Mingw", packages)
        self.assertIn("Kitware.CMake", packages)

    def test_parse_package_list_empty(self):
        """Test parsing empty package list"""
        output = ""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 0)

    def test_parse_package_list_with_headers(self):
        """Test parsing package list with headers"""
        output = """
Name           Id              Version        Available Source
----------------------------------------------------------------
LLVM           LLVM.LLVM        17.0.6         18.1.0    winget
MinGW          GNU.Mingw        12.2.0         13.0.0    winget
"""
        packages = self.detector._parse_package_list(output)

        self.assertEqual(len(packages), 2)
        self.assertNotIn("Name", packages)
        self.assertNotIn("Id", packages)


class TestWingetDetectorParsePackageInfo(unittest.TestCase):
    """Test cases for parsing winget package info"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()
        self.detector._winget_path = r"C:\Users\test\AppData\Local\Microsoft\WindowsApps\winget.exe"

    def test_parse_package_info_success(self):
        """Test successful package info parsing"""
        output = r"""
Name: LLVM
Id: LLVM.LLVM
Version: 17.0.6
Install Location: C:\Program Files\LLVM
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = r"C:\Program Files\LLVM\bin\clang.exe"

            package_info = self.detector._parse_package_info("LLVM.LLVM", output)

            self.assertIsNotNone(package_info)
            self.assertEqual(package_info.name, "LLVM.LLVM")
            self.assertEqual(package_info.version, "17.0.6")
            self.assertEqual(package_info.package_manager, PackageManagerType.WINGET)

    def test_parse_package_info_no_path(self):
        """Test package info parsing when path not found"""
        output = r"""
Name: LLVM
Id: LLVM.LLVM
Version: 17.0.6
"""
        with patch.object(self.detector, '_find_package_path') as mock_path:
            mock_path.return_value = None

            package_info = self.detector._parse_package_info("LLVM.LLVM", output)

            self.assertIsNone(package_info)


class TestWingetDetectorFindPackagePath(unittest.TestCase):
    """Test cases for finding package installation path"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_find_package_path_program_files(self, mock_listdir, mock_exists):
        """Test finding package path in Program Files"""
        # Mock path exists
        def exists_side_effect(path):
            return "LLVM" in path or "clang.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock directory listing with executable
        mock_listdir.return_value = ["clang.exe", "lld.exe", "readme.txt"]

        package_path = self.detector._find_package_path("LLVM.LLVM")

        self.assertIsNotNone(package_path)
        self.assertTrue("LLVM" in package_path)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('subprocess.run')
    def test_find_package_path_via_where(self, mock_run, mock_listdir, mock_exists):
        """Test finding package path via 'where' command"""
        # Mock path doesn't exist in standard locations
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

        package_path = self.detector._find_package_path("LLVM.LLVM")

        self.assertIsNotNone(package_path)
        self.assertTrue("clang.exe" in package_path)

    @patch('os.path.exists')
    def test_find_package_path_not_found(self, mock_exists):
        """Test package path not found"""
        mock_exists.return_value = False

        package_path = self.detector._find_package_path("nonexistent")

        self.assertIsNone(package_path)


class TestWingetDetectorGetWingetPaths(unittest.TestCase):
    """Test cases for getting winget installation paths"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = WingetDetector()

    def test_get_winget_paths(self):
        """Test getting winget paths"""
        paths = self.detector._get_winget_paths()

        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertTrue(any("winget.exe" in path for path in paths))


if __name__ == '__main__':
    unittest.main()
