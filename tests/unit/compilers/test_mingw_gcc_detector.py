"""
Unit tests for MinGW-GCC Compiler Detector

Tests cover:
- MSYS2 environment detection (UCRT64, MINGW64, MINGW32, MSYS, CLANG64)
- Standalone MinGW-w64 detection
- TDM-GCC detection
- Package manager detection (Chocolatey, Scoop, winget)
- Version detection
- Capability detection
- Validation
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.mingw_gcc_detector import (
    MinGWDetector,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    CompilerInfo,
    ValidationResult
)


class TestMinGWDetector(unittest.TestCase):
    """Test cases for MinGW-GCC detector"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    def test_detector_initialization(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector._logger)
        self.assertIsInstance(self.detector._msys2_paths, list)
        self.assertIsInstance(self.detector._standalone_paths, list)
        self.assertIsInstance(self.detector._tdm_gcc_paths, list)
        self.assertIsInstance(self.detector._package_manager_paths, dict)

    def test_msys2_environments_config(self):
        """Test MSYS2 environment configurations"""
        self.assertIn("UCRT64", MinGWDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("MINGW64", MinGWDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("MINGW32", MinGWDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("MSYS", MinGWDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("CLANG64", MinGWDetector.MSYS2_ENVIRONMENTS)

        # Check UCRT64 configuration
        ucrt64_config = MinGWDetector.MSYS2_ENVIRONMENTS["UCRT64"]
        self.assertEqual(ucrt64_config["msystem"], "UCRT64")
        self.assertEqual(ucrt64_config["mingw_prefix"], "/ucrt64")
        self.assertEqual(ucrt64_config["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(ucrt64_config["architecture"], Architecture.X64)
        self.assertTrue(ucrt64_config["recommended"])

        # Check MINGW64 configuration
        mingw64_config = MinGWDetector.MSYS2_ENVIRONMENTS["MINGW64"]
        self.assertEqual(mingw64_config["msystem"], "MINGW64")
        self.assertEqual(mingw64_config["mingw_prefix"], "/mingw64")
        self.assertEqual(mingw64_config["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(mingw64_config["architecture"], Architecture.X64)
        self.assertFalse(mingw64_config["recommended"])

        # Check MINGW32 configuration
        mingw32_config = MinGWDetector.MSYS2_ENVIRONMENTS["MINGW32"]
        self.assertEqual(mingw32_config["msystem"], "MINGW32")
        self.assertEqual(mingw32_config["mingw_prefix"], "/mingw32")
        self.assertEqual(mingw32_config["mingw_chost"], "i686-w64-mingw32")
        self.assertEqual(mingw32_config["architecture"], Architecture.X86)
        self.assertFalse(mingw32_config["recommended"])

    def test_get_msys2_paths(self):
        """Test MSYS2 path detection"""
        paths = self.detector._get_msys2_paths()
        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertIn(r"C:\msys64", paths)
        self.assertIn(r"C:\msys32", paths)

    def test_get_standalone_paths(self):
        """Test standalone MinGW path detection"""
        paths = self.detector._get_standalone_paths()
        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertIn(r"C:\mingw64", paths)
        self.assertIn(r"C:\mingw32", paths)
        self.assertIn(r"C:\mingw", paths)

    def test_get_tdm_gcc_paths(self):
        """Test TDM-GCC path detection"""
        paths = self.detector._get_tdm_gcc_paths()
        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertIn(r"C:\TDM-GCC-64", paths)
        self.assertIn(r"C:\TDM-GCC-32", paths)

    def test_get_package_manager_paths(self):
        """Test package manager path detection"""
        paths = self.detector._get_package_manager_paths()
        self.assertIsInstance(paths, dict)
        self.assertIn("chocolatey", paths)
        self.assertIn("scoop", paths)
        self.assertIn("winget", paths)

        # Check Chocolatey paths
        chocolatey_paths = paths["chocolatey"]
        self.assertIsInstance(chocolatey_paths, list)
        self.assertGreater(len(chocolatey_paths), 0)

        # Check Scoop paths
        scoop_paths = paths["scoop"]
        self.assertIsInstance(scoop_paths, list)
        self.assertGreater(len(scoop_paths), 0)

        # Check winget paths
        winget_paths = paths["winget"]
        self.assertIsInstance(winget_paths, list)
        self.assertGreater(len(winget_paths), 0)


class TestVersionDetection(unittest.TestCase):
    """Test cases for version detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    def test_version_info_creation(self):
        """Test VersionInfo dataclass creation"""
        version = VersionInfo(major=13, minor=2, patch=0)
        self.assertEqual(version.major, 13)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(str(version), "13.2.0")

    def test_version_info_with_build(self):
        """Test VersionInfo with build number"""
        version = VersionInfo(major=13, minor=2, patch=0, build="12345")
        self.assertEqual(version.build, "12345")
        self.assertEqual(str(version), "13.2.0.12345")

    def test_version_comparison(self):
        """Test version comparison"""
        v1 = VersionInfo(major=13, minor=2, patch=0)
        v2 = VersionInfo(major=12, minor=3, patch=0)
        v3 = VersionInfo(major=13, minor=2, patch=1)

        self.assertTrue(v2 < v1)
        self.assertTrue(v1 < v3)
        self.assertFalse(v1 < v2)

    @patch('subprocess.run')
    def test_detect_version_success(self, mock_run):
        """Test successful version detection"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="g++.exe (Rev2, Built by MSYS2 project) 13.2.0\nCopyright (C) 2022 Free Software Foundation, Inc.\n",
            stderr=""
        )

        version = self.detector.detect_version("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertIsNotNone(version)
        self.assertEqual(version.major, 13)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(str(version), "13.2.0")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_version_tdm_gcc(self, mock_run, mock_exists):
        """Test version detection for TDM-GCC"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="g++.exe (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 12.2.0\nCopyright (C) 2022 Free Software Foundation, Inc.\n",
            stderr=""
        )

        version = self.detector.detect_version("C:\\TDM-GCC-64\\bin\\g++.exe")

        self.assertIsNotNone(version)
        self.assertEqual(version.major, 12)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)

    @patch('subprocess.run')
    def test_detect_version_file_not_found(self, mock_run):
        """Test version detection when file doesn't exist"""
        version = self.detector.detect_version("C:\\nonexistent\\g++.exe")

        self.assertIsNone(version)
        mock_run.assert_not_called()

    @patch('subprocess.run')
    def test_detect_version_command_fails(self, mock_run):
        """Test version detection when command fails"""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: command failed"
        )

        version = self.detector.detect_version("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertIsNone(version)


class TestCapabilityDetection(unittest.TestCase):
    """Test cases for capability detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    def test_capability_info_creation(self):
        """Test CapabilityInfo dataclass creation"""
        capabilities = CapabilityInfo()
        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertFalse(capabilities.cpp17)
        self.assertFalse(capabilities.cpp14)

    def test_capability_info_to_dict(self):
        """Test CapabilityInfo to_dict method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True
        )
        caps_dict = capabilities.to_dict()

        self.assertIsInstance(caps_dict, dict)
        self.assertTrue(caps_dict["cpp23"])
        self.assertTrue(caps_dict["cpp20"])
        self.assertTrue(caps_dict["cpp17"])
        self.assertTrue(caps_dict["modules"])

    @patch.object(MinGWDetector, 'detect_version')
    def test_detect_capabilities_gcc13(self, mock_detect_version):
        """Test capability detection for GCC 13"""
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)

        capabilities = self.detector.detect_capabilities("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertTrue(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)
        self.assertTrue(capabilities.mingw_compatibility)

    @patch.object(MinGWDetector, 'detect_version')
    def test_detect_capabilities_gcc11(self, mock_detect_version):
        """Test capability detection for GCC 11"""
        mock_detect_version.return_value = VersionInfo(major=11, minor=3, patch=0)

        capabilities = self.detector.detect_capabilities("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch.object(MinGWDetector, 'detect_version')
    def test_detect_capabilities_gcc8(self, mock_detect_version):
        """Test capability detection for GCC 8"""
        mock_detect_version.return_value = VersionInfo(major=8, minor=5, patch=0)

        capabilities = self.detector.detect_capabilities("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch.object(MinGWDetector, 'detect_version')
    def test_detect_capabilities_gcc6(self, mock_detect_version):
        """Test capability detection for GCC 6"""
        mock_detect_version.return_value = VersionInfo(major=6, minor=5, patch=0)

        capabilities = self.detector.detect_capabilities("C:\\msys64\\ucrt64\\bin\\g++.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertFalse(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)


class TestMSYS2Detection(unittest.TestCase):
    """Test cases for MSYS2 environment detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_msys2_ucrt64(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test MSYS2 UCRT64 environment detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override MSYS2 paths to use test path
        self.detector._msys2_paths = ["C:\\test_msys64"]

        compilers = self.detector._detect_via_msys2()

        self.assertGreater(len(compilers), 0)

        # Find UCRT64 compiler
        ucrt64_compilers = [c for c in compilers if c.metadata.get("environment") == "UCRT64"]
        self.assertGreater(len(ucrt64_compilers), 0)

        compiler = ucrt64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "UCRT64")
        self.assertEqual(compiler.metadata["msystem"], "UCRT64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/ucrt64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(compiler.metadata["recommended"], "true")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_msys2_mingw64(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test MSYS2 MINGW64 environment detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override MSYS2 paths to use test path
        self.detector._msys2_paths = ["C:\\test_msys64"]

        compilers = self.detector._detect_via_msys2()

        # Find MINGW64 compiler
        mingw64_compilers = [c for c in compilers if c.metadata.get("environment") == "MINGW64"]
        self.assertGreater(len(mingw64_compilers), 0)

        compiler = mingw64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "MINGW64")
        self.assertEqual(compiler.metadata["msystem"], "MINGW64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/mingw64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(compiler.metadata["recommended"], "false")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_msys2_mingw32(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test MSYS2 MINGW32 environment detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override MSYS2 paths to use test path
        self.detector._msys2_paths = ["C:\\test_msys64"]

        compilers = self.detector._detect_via_msys2()

        # Find MINGW32 compiler
        mingw32_compilers = [c for c in compilers if c.metadata.get("environment") == "MINGW32"]
        self.assertGreater(len(mingw32_compilers), 0)

        compiler = mingw32_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X86)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "MINGW32")
        self.assertEqual(compiler.metadata["msystem"], "MINGW32")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/mingw32")
        self.assertEqual(compiler.metadata["mingw_chost"], "i686-w64-mingw32")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_msys2_msys(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test MSYS2 MSYS environment detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override MSYS2 paths to use test path
        self.detector._msys2_paths = ["C:\\test_msys64"]

        compilers = self.detector._detect_via_msys2()

        # Find MSYS compiler
        msys_compilers = [c for c in compilers if c.metadata.get("environment") == "MSYS"]
        self.assertGreater(len(msys_compilers), 0)

        compiler = msys_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "MSYS")
        self.assertEqual(compiler.metadata["msystem"], "MSYS")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/usr")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-pc-msys")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_msys2_clang64(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test MSYS2 CLANG64 environment detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override MSYS2 paths to use test path
        self.detector._msys2_paths = ["C:\\test_msys64"]

        compilers = self.detector._detect_via_msys2()

        # Find CLANG64 compiler
        clang64_compilers = [c for c in compilers if c.metadata.get("environment") == "CLANG64"]
        self.assertGreater(len(clang64_compilers), 0)

        compiler = clang64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "CLANG64")
        self.assertEqual(compiler.metadata["msystem"], "CLANG64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/clang64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")


class TestStandaloneDetection(unittest.TestCase):
    """Test cases for standalone MinGW-w64 detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_standalone_mingw64(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test standalone MinGW-w64 64-bit detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=12, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override standalone paths to use test path
        self.detector._standalone_paths = ["C:\\mingw64"]

        compilers = self.detector._detect_standalone()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "standalone")
        self.assertEqual(compiler.metadata["detection_method"], "standard_paths")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_standalone_mingw32(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test standalone MinGW-w64 32-bit detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=12, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override standalone paths to use test path
        self.detector._standalone_paths = ["C:\\mingw32"]

        compilers = self.detector._detect_standalone()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X86)
        self.assertEqual(compiler.metadata["installation_type"], "standalone")


class TestTDMGCCDetection(unittest.TestCase):
    """Test cases for TDM-GCC detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_tdm_gcc_64(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test TDM-GCC 64-bit detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=10, minor=3, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override TDM-GCC paths to use test path
        self.detector._tdm_gcc_paths = ["C:\\TDM-GCC-64"]

        compilers = self.detector._detect_tdm_gcc()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "tdm_gcc")
        self.assertEqual(compiler.metadata["detection_method"], "standard_paths")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_tdm_gcc_32(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test TDM-GCC 32-bit detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=10, minor=3, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override TDM-GCC paths to use test path
        self.detector._tdm_gcc_paths = ["C:\\TDM-GCC-32"]

        compilers = self.detector._detect_tdm_gcc()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X86)
        self.assertEqual(compiler.metadata["installation_type"], "tdm_gcc")


class TestPackageManagerDetection(unittest.TestCase):
    """Test cases for package manager detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_chocolatey_mingw(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test Chocolatey MinGW detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=12, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override Chocolatey paths to use test path
        self.detector._package_manager_paths = {
            "chocolatey": ["C:\\ProgramData\\chocolatey\\lib\\mingw\\tools"],
            "scoop": [],
            "winget": []
        }

        compilers = self.detector._detect_chocolatey_mingw()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "chocolatey")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_scoop_mingw(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test Scoop MinGW detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=12, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override Scoop paths to use test path
        self.detector._package_manager_paths = {
            "chocolatey": [],
            "scoop": ["C:\\Users\\test\\scoop\\apps\\mingw\\current"],
            "winget": []
        }

        compilers = self.detector._detect_scoop_mingw()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "scoop")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_winget_mingw(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test winget MinGW detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=12, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override winget paths to use test path
        self.detector._package_manager_paths = {
            "chocolatey": [],
            "scoop": [],
            "winget": ["C:\\Program Files\\mingw-w64"]
        }

        compilers = self.detector._detect_winget_mingw()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_GCC)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "winget")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")


class TestValidation(unittest.TestCase):
    """Test cases for compiler validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_success(self, mock_run, mock_exists):
        """Test successful compiler validation"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="g++.exe (Rev2, Built by MSYS2 project) 13.2.0",
            stderr=""
        )

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_GCC,
            version=VersionInfo(major=13, minor=2, patch=0),
            path="C:\\msys64\\ucrt64\\bin\\g++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(cpp23=True, mingw_compatibility=True),
            environment=EnvironmentInfo(
                path="C:\\msys64",
                environment_variables={"MSYSTEM": "UCRT64"}
            ),
            metadata={"environment": "UCRT64"}
        )

        result = self.detector.validate(compiler_info)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_file_not_found(self, mock_exists):
        """Test validation when compiler file not found"""
        mock_exists.return_value = False

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_GCC,
            version=VersionInfo(major=13, minor=2, patch=0),
            path="C:\\nonexistent\\g++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\nonexistent"),
            metadata={}
        )

        result = self.detector.validate(compiler_info)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Compiler executable not found", result.errors[0])

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_command_fails(self, mock_run, mock_exists):
        """Test validation when compiler command fails"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: command failed"
        )

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_GCC,
            version=VersionInfo(major=13, minor=2, patch=0),
            path="C:\\msys64\\ucrt64\\bin\\g++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\msys64"),
            metadata={"environment": "UCRT64"}
        )

        result = self.detector.validate(compiler_info)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)


class TestFullDetection(unittest.TestCase):
    """Test cases for full detection workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWDetector(logger=self.logger)

    @patch('os.path.exists')
    @patch.object(MinGWDetector, 'detect_version')
    @patch.object(MinGWDetector, 'detect_capabilities')
    def test_detect_all_compilers(self, mock_detect_caps, mock_detect_version, mock_exists):
        """Test full compiler detection"""
        mock_exists.return_value = True
        mock_detect_version.return_value = VersionInfo(major=13, minor=2, patch=0)
        mock_detect_caps.return_value = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            mingw_compatibility=True
        )

        # Override paths to use test paths
        self.detector._msys2_paths = ["C:\\test_msys64"]
        self.detector._standalone_paths = ["C:\\test_mingw64"]
        self.detector._tdm_gcc_paths = ["C:\\test_tdm_gcc"]
        self.detector._package_manager_paths = {
            "chocolatey": ["C:\\test_chocolatey"],
            "scoop": ["C:\\test_scoop"],
            "winget": ["C:\\test_winget"]
        }

        compilers = self.detector.detect()

        self.assertGreater(len(compilers), 0)

        # Check that compilers are sorted by version
        for i in range(len(compilers) - 1):
            self.assertGreaterEqual(
                compilers[i].version.major,
                compilers[i + 1].version.major
            )

        # Check that first compiler is marked as recommended
        self.assertEqual(compilers[0].metadata.get("recommended"), "true")

    @patch('os.path.exists')
    def test_detect_no_compilers(self, mock_exists):
        """Test detection when no compilers are found"""
        mock_exists.return_value = False

        compilers = self.detector.detect()

        self.assertEqual(len(compilers), 0)


if __name__ == '__main__':
    unittest.main()
