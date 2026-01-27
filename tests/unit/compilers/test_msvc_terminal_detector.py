"""
Unit tests for MSVC Terminal Detector

This module contains comprehensive unit tests for MSVC terminal detector,
covering Developer Command Prompt, Native Tools, Cross Tools, and
Start Menu shortcuts detection.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.msvc_terminal_detector import (
    MSVCTerminalDetector,
    TerminalType,
    TerminalInfo,
    ITerminalDetector
)


class TestTerminalType(unittest.TestCase):
    """Test cases for TerminalType enumeration"""

    def test_terminal_type_values(self):
        """Test TerminalType enumeration values"""
        self.assertEqual(TerminalType.MSVC_DEVELOPER_CMD.value, "msvc_developer_cmd")
        self.assertEqual(TerminalType.MSVC_X64_NATIVE.value, "msvc_x64_native")
        self.assertEqual(TerminalType.MSVC_X86_NATIVE.value, "msvc_x86_native")
        self.assertEqual(TerminalType.MSVC_X86_X64_CROSS.value, "msvc_x86_x64_cross")
        self.assertEqual(TerminalType.MSVC_X64_X86_CROSS.value, "msvc_x64_x86_cross")
        self.assertEqual(TerminalType.MSVC_X64_ARM_CROSS.value, "msvc_x64_arm_cross")
        self.assertEqual(TerminalType.MSVC_X64_ARM64_CROSS.value, "msvc_x64_arm64_cross")


class TestTerminalInfo(unittest.TestCase):
    """Test cases for TerminalInfo dataclass"""

    def test_terminal_info_creation(self):
        """Test TerminalInfo creation"""
        terminal = TerminalInfo(
            terminal_id="developer_cmd",
            name="Developer Command Prompt",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat"
        )
        self.assertEqual(terminal.terminal_id, "developer_cmd")
        self.assertEqual(terminal.name, "Developer Command Prompt")
        self.assertEqual(terminal.type, TerminalType.MSVC_DEVELOPER_CMD)
        self.assertEqual(terminal.architecture, "x64")
        self.assertEqual(terminal.environment, "")
        self.assertEqual(terminal.capabilities, [])
        self.assertEqual(terminal.metadata, {})
        self.assertFalse(terminal.recommended)

    def test_terminal_info_with_all_fields(self):
        """Test TerminalInfo with all fields populated"""
        terminal = TerminalInfo(
            terminal_id="x64_native",
            name="x64 Native Tools Command Prompt",
            type=TerminalType.MSVC_X64_NATIVE,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Auxiliary\Build\vcvars64.bat",
            arguments=["-arch=x64"],
            architecture="x64",
            environment="msvc",
            capabilities=["msvc", "native_tools"],
            metadata={"version": "2022"},
            recommended=True
        )
        self.assertEqual(terminal.terminal_id, "x64_native")
        self.assertEqual(terminal.arguments, ["-arch=x64"])
        self.assertEqual(terminal.architecture, "x64")
        self.assertEqual(terminal.environment, "msvc")
        self.assertEqual(len(terminal.capabilities), 2)
        self.assertEqual(terminal.metadata["version"], "2022")
        self.assertTrue(terminal.recommended)

    def test_terminal_info_to_dict(self):
        """Test TerminalInfo to_dict method"""
        terminal = TerminalInfo(
            terminal_id="developer_cmd",
            name="Developer Command Prompt",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat",
            architecture="x64",
            environment="msvc",
            capabilities=["msvc"],
            metadata={"version": "2022"},
            recommended=True
        )
        result = terminal.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["terminal_id"], "developer_cmd")
        self.assertEqual(result["name"], "Developer Command Prompt")
        self.assertEqual(result["type"], "msvc_developer_cmd")
        self.assertEqual(result["architecture"], "x64")
        self.assertEqual(result["environment"], "msvc")
        self.assertEqual(result["capabilities"], ["msvc"])
        self.assertEqual(result["metadata"]["version"], "2022")
        self.assertTrue(result["recommended"])

    def test_terminal_info_is_valid(self):
        """Test TerminalInfo is_valid method"""
        # Test with non-existent path
        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable="/nonexistent/path/batch.bat"
        )
        self.assertFalse(terminal.is_valid())


class TestMSVCTerminalDetectorInitialization(unittest.TestCase):
    """Test cases for MSVCTerminalDetector initialization"""

    def test_detector_initialization(self):
        """Test MSVCTerminalDetector initialization"""
        detector = MSVCTerminalDetector()
        self.assertIsNotNone(detector)
        self.assertIsInstance(detector, ITerminalDetector)

    def test_detector_with_logger(self):
        """Test MSVCTerminalDetector with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        detector = MSVCTerminalDetector(logger=logger)
        self.assertIsNotNone(detector)

    def test_detector_installation_paths(self):
        """Test MSVCTerminalDetector installation paths"""
        detector = MSVCTerminalDetector()
        self.assertIsInstance(detector._installation_paths, list)


class TestMSVCTerminalDetectorDetectDeveloperCmd(unittest.TestCase):
    """Test cases for Developer Command Prompt detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    def test_detect_developer_cmd_found(self, mock_exists):
        """Test successful Developer Command Prompt detection"""
        # Mock path existence
        def exists_side_effect(path):
            return "VsDevCmd.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminal = self.detector._detect_developer_cmd()

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "developer_cmd")
        self.assertEqual(terminal.type, TerminalType.MSVC_DEVELOPER_CMD)
        self.assertTrue(terminal.recommended)

    @patch('os.path.exists')
    def test_detect_developer_cmd_not_found(self, mock_exists):
        """Test Developer Command Prompt not found"""
        mock_exists.return_value = False

        terminal = self.detector._detect_developer_cmd()

        self.assertIsNone(terminal)

    @patch('os.path.exists')
    def test_detect_developer_cmd_version_extraction(self, mock_exists):
        """Test version extraction from path"""
        def exists_side_effect(path):
            return "VsDevCmd.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        # Set installation path with version
        self.detector._installation_paths = [r"C:\Program Files\Microsoft Visual Studio\2022"]

        terminal = self.detector._detect_developer_cmd()

        self.assertIsNotNone(terminal)
        self.assertIn("2022", terminal.name)


class TestMSVCTerminalDetectorDetectNativeTools(unittest.TestCase):
    """Test cases for Native Tools detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    def test_detect_native_tools_x64(self, mock_exists):
        """Test x64 Native Tools detection"""
        def exists_side_effect(path):
            return "vcvars64.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_native_tools()

        self.assertGreater(len(terminals), 0)
        x64_terminal = next((t for t in terminals if t.terminal_id == "x64_native"), None)
        self.assertIsNotNone(x64_terminal)
        self.assertEqual(x64_terminal.type, TerminalType.MSVC_X64_NATIVE)
        self.assertTrue(x64_terminal.recommended)

    @patch('os.path.exists')
    def test_detect_native_tools_x86(self, mock_exists):
        """Test x86 Native Tools detection"""
        def exists_side_effect(path):
            return "vcvars32.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_native_tools()

        self.assertGreater(len(terminals), 0)
        x86_terminal = next((t for t in terminals if t.terminal_id == "x86_native"), None)
        self.assertIsNotNone(x86_terminal)
        self.assertEqual(x86_terminal.type, TerminalType.MSVC_X86_NATIVE)
        self.assertEqual(x86_terminal.architecture, "x86")

    @patch('os.path.exists')
    def test_detect_native_tools_not_found(self, mock_exists):
        """Test Native Tools not found"""
        mock_exists.return_value = False

        terminals = self.detector._detect_native_tools()

        self.assertEqual(len(terminals), 0)


class TestMSVCTerminalDetectorDetectCrossTools(unittest.TestCase):
    """Test cases for Cross Tools detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    def test_detect_cross_tools_x86_x64(self, mock_exists):
        """Test x86_x64 Cross Tools detection"""
        def exists_side_effect(path):
            return "vcvarsx86_amd64.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_cross_tools()

        self.assertGreater(len(terminals), 0)
        cross_terminal = next((t for t in terminals if t.terminal_id == "x86_x64_cross"), None)
        self.assertIsNotNone(cross_terminal)
        self.assertEqual(cross_terminal.type, TerminalType.MSVC_X86_X64_CROSS)
        self.assertEqual(cross_terminal.architecture, "x64")

    @patch('os.path.exists')
    def test_detect_cross_tools_x64_x86(self, mock_exists):
        """Test x64_x86 Cross Tools detection"""
        def exists_side_effect(path):
            return "vcvarsamd64_x86.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_cross_tools()

        self.assertGreater(len(terminals), 0)
        cross_terminal = next((t for t in terminals if t.terminal_id == "x64_x86_cross"), None)
        self.assertIsNotNone(cross_terminal)
        self.assertEqual(cross_terminal.type, TerminalType.MSVC_X64_X86_CROSS)
        self.assertEqual(cross_terminal.architecture, "x86")

    @patch('os.path.exists')
    def test_detect_cross_tools_x64_arm(self, mock_exists):
        """Test x64_arm Cross Tools detection"""
        def exists_side_effect(path):
            return "vcvarsamd64_arm.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_cross_tools()

        self.assertGreater(len(terminals), 0)
        cross_terminal = next((t for t in terminals if t.terminal_id == "x64_arm_cross"), None)
        self.assertIsNotNone(cross_terminal)
        self.assertEqual(cross_terminal.type, TerminalType.MSVC_X64_ARM_CROSS)
        self.assertEqual(cross_terminal.architecture, "arm")

    @patch('os.path.exists')
    def test_detect_cross_tools_x64_arm64(self, mock_exists):
        """Test x64_arm64 Cross Tools detection"""
        def exists_side_effect(path):
            return "vcvarsamd64_arm64.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_cross_tools()

        self.assertGreater(len(terminals), 0)
        cross_terminal = next((t for t in terminals if t.terminal_id == "x64_arm64_cross"), None)
        self.assertIsNotNone(cross_terminal)
        self.assertEqual(cross_terminal.type, TerminalType.MSVC_X64_ARM64_CROSS)
        self.assertEqual(cross_terminal.architecture, "arm64")

    @patch('os.path.exists')
    def test_detect_cross_tools_not_found(self, mock_exists):
        """Test Cross Tools not found"""
        mock_exists.return_value = False

        terminals = self.detector._detect_cross_tools()

        self.assertEqual(len(terminals), 0)


class TestMSVCTerminalDetectorDetectShortcuts(unittest.TestCase):
    """Test cases for Start Menu shortcuts detection"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_detect_shortcuts_found(self, mock_listdir, mock_exists):
        """Test successful shortcuts detection"""
        def exists_side_effect(path):
            return "Start Menu" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect
        mock_listdir.return_value = ["Developer Command Prompt for VS 2022.lnk"]

        terminals = self.detector._detect_shortcuts()

        self.assertIsInstance(terminals, list)

    @patch('os.path.exists')
    def test_detect_shortcuts_not_found(self, mock_exists):
        """Test shortcuts not found"""
        mock_exists.return_value = False

        terminals = self.detector._detect_shortcuts()

        self.assertEqual(len(terminals), 0)


class TestMSVCTerminalDetectorValidate(unittest.TestCase):
    """Test cases for terminal validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('subprocess.run')
    def test_validate_valid_terminal(self, mock_run, mock_exists, mock_isfile):
        """Test validation of valid terminal"""
        # Mock path existence
        def exists_side_effect(path):
            return ".bat" in path or ".exe" in path

        def isfile_side_effect(path):
            return ".bat" in path or ".exe" in path

        mock_exists.side_effect = exists_side_effect
        mock_isfile.side_effect = isfile_side_effect

        # Mock subprocess execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat"
        )

        result = self.detector.validate(terminal)

        self.assertTrue(result)

    @patch('os.path.exists')
    def test_validate_nonexistent_terminal(self, mock_exists):
        """Test validation of non-existent terminal"""
        mock_exists.return_value = False

        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable="/nonexistent/path/batch.bat"
        )

        result = self.detector.validate(terminal)

        self.assertFalse(result)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_timeout(self, mock_run, mock_exists):
        """Test validation with timeout"""
        mock_exists.return_value = True
        mock_run.side_effect = subprocess.TimeoutExpired("batch.bat", 10)

        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat"
        )

        result = self.detector.validate(terminal)

        self.assertFalse(result)


class TestMSVCTerminalDetectorGetTerminal(unittest.TestCase):
    """Test cases for get_terminal method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    def test_get_terminal_found(self):
        """Test getting existing terminal"""
        # Add a terminal to detected list
        terminal = TerminalInfo(
            terminal_id="developer_cmd",
            name="Developer Command Prompt",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat"
        )
        self.detector._detected_terminals = [terminal]

        result = self.detector.get_terminal("developer_cmd")

        self.assertIsNotNone(result)
        self.assertEqual(result.terminal_id, "developer_cmd")

    def test_get_terminal_not_found(self):
        """Test getting non-existent terminal"""
        self.detector._detected_terminals = []

        result = self.detector.get_terminal("nonexistent")

        self.assertIsNone(result)


class TestMSVCTerminalDetectorDetect(unittest.TestCase):
    """Test cases for detect method"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch.object(MSVCTerminalDetector, '_detect_developer_cmd')
    @patch.object(MSVCTerminalDetector, '_detect_native_tools')
    @patch.object(MSVCTerminalDetector, '_detect_cross_tools')
    @patch.object(MSVCTerminalDetector, '_detect_shortcuts')
    def test_detect_all_terminals(self, mock_shortcuts, mock_cross, mock_native, mock_dev):
        """Test detection of all terminals"""
        # Mock terminal detections
        mock_dev.return_value = TerminalInfo(
            terminal_id="developer_cmd",
            name="Developer Command Prompt",
            type=TerminalType.MSVC_DEVELOPER_CMD,
            executable=r"C:\Program Files\Microsoft Visual Studio\2022\Common7\Tools\VsDevCmd.bat"
        )
        mock_native.return_value = [
            TerminalInfo(
                terminal_id="x64_native",
                name="x64 Native Tools",
                type=TerminalType.MSVC_X64_NATIVE,
                executable=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Auxiliary\Build\vcvars64.bat"
            )
        ]
        mock_cross.return_value = [
            TerminalInfo(
                terminal_id="x86_x64_cross",
                name="x86_x64 Cross Tools",
                type=TerminalType.MSVC_X86_X64_CROSS,
                executable=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Auxiliary\Build\vcvarsx86_amd64.bat"
            )
        ]
        mock_shortcuts.return_value = []

        terminals = self.detector.detect()

        self.assertEqual(len(terminals), 3)
        mock_dev.assert_called_once()
        mock_native.assert_called_once()
        mock_cross.assert_called_once()
        mock_shortcuts.assert_called_once()

    @patch.object(MSVCTerminalDetector, '_detect_developer_cmd')
    @patch.object(MSVCTerminalDetector, '_detect_native_tools')
    @patch.object(MSVCTerminalDetector, '_detect_cross_tools')
    @patch.object(MSVCTerminalDetector, '_detect_shortcuts')
    def test_detect_no_terminals(self, mock_shortcuts, mock_cross, mock_native, mock_dev):
        """Test detection with no terminals found"""
        mock_dev.return_value = None
        mock_native.return_value = []
        mock_cross.return_value = []
        mock_shortcuts.return_value = []

        terminals = self.detector.detect()

        self.assertEqual(len(terminals), 0)


class TestMSVCTerminalDetectorExtractVersion(unittest.TestCase):
    """Test cases for version extraction from path"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    def test_extract_version_2022(self):
        """Test extracting version 2022 from path"""
        path = r"C:\Program Files\Microsoft Visual Studio\2022"
        version = self.detector._extract_version_from_path(path)
        self.assertEqual(version, "2022")

    def test_extract_version_2019(self):
        """Test extracting version 2019 from path"""
        path = r"C:\Program Files\Microsoft Visual Studio\2019"
        version = self.detector._extract_version_from_path(path)
        self.assertEqual(version, "2019")

    def test_extract_version_2017(self):
        """Test extracting version 2017 from path"""
        path = r"C:\Program Files\Microsoft Visual Studio\2017"
        version = self.detector._extract_version_from_path(path)
        self.assertEqual(version, "2017")

    def test_extract_version_unknown(self):
        """Test extracting unknown version from path"""
        path = r"C:\Program Files\Microsoft Visual Studio\BuildTools"
        version = self.detector._extract_version_from_path(path)
        self.assertEqual(version, "unknown")


class TestMSVCTerminalDetectorGetInstallationPaths(unittest.TestCase):
    """Test cases for getting installation paths"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_get_installation_paths_with_vswhere(self, mock_run, mock_exists):
        """Test getting installation paths with vswhere"""
        def exists_side_effect(path):
            return "Visual Studio" in path or "vswhere.exe" in path

        mock_exists.side_effect = exists_side_effect

        # Mock vswhere output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = r"C:\Program Files\Microsoft Visual Studio\2022"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        paths = self.detector._get_installation_paths()

        self.assertGreater(len(paths), 0)

    @patch('os.path.exists')
    def test_get_installation_paths_no_installations(self, mock_exists):
        """Test getting installation paths with no installations"""
        mock_exists.return_value = False

        paths = self.detector._get_installation_paths()

        self.assertEqual(len(paths), 0)


class TestMSVCTerminalDetectorInterface(unittest.TestCase):
    """Test cases for MSVCTerminalDetector interface compliance"""

    def test_implements_iterminal_detector(self):
        """Test MSVCTerminalDetector implements ITerminalDetector"""
        detector = MSVCTerminalDetector()
        self.assertIsInstance(detector, ITerminalDetector)

    def test_has_detect_method(self):
        """Test MSVCTerminalDetector has detect method"""
        detector = MSVCTerminalDetector()
        self.assertTrue(hasattr(detector, 'detect'))
        self.assertTrue(callable(getattr(detector, 'detect')))

    def test_has_get_terminal_method(self):
        """Test MSVCTerminalDetector has get_terminal method"""
        detector = MSVCTerminalDetector()
        self.assertTrue(hasattr(detector, 'get_terminal'))
        self.assertTrue(callable(getattr(detector, 'get_terminal')))

    def test_has_validate_method(self):
        """Test MSVCTerminalDetector has validate method"""
        detector = MSVCTerminalDetector()
        self.assertTrue(hasattr(detector, 'validate'))
        self.assertTrue(callable(getattr(detector, 'validate')))


class TestMSVCTerminalDetectorTerminalTypes(unittest.TestCase):
    """Test cases for all MSVC terminal types"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    def test_all_terminal_types_detected(self, mock_exists):
        """Test that all terminal types can be detected"""
        def exists_side_effect(path):
            return ".bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        # Set installation path
        self.detector._installation_paths = [r"C:\Program Files\Microsoft Visual Studio\2022"]

        # Detect all terminals
        dev_cmd = self.detector._detect_developer_cmd()
        native_terminals = self.detector._detect_native_tools()
        cross_terminals = self.detector._detect_cross_tools()

        # Verify all terminal types
        self.assertIsNotNone(dev_cmd)
        self.assertEqual(dev_cmd.type, TerminalType.MSVC_DEVELOPER_CMD)

        # Check native terminals
        terminal_ids = [t.terminal_id for t in native_terminals]
        self.assertIn("x64_native", terminal_ids)
        self.assertIn("x86_native", terminal_ids)

        # Check cross terminals
        terminal_ids = [t.terminal_id for t in cross_terminals]
        self.assertIn("x86_x64_cross", terminal_ids)
        self.assertIn("x64_x86_cross", terminal_ids)
        self.assertIn("x64_arm_cross", terminal_ids)
        self.assertIn("x64_arm64_cross", terminal_ids)


class TestMSVCTerminalDetectorTerminalMetadata(unittest.TestCase):
    """Test cases for terminal metadata"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = MSVCTerminalDetector()

    @patch('os.path.exists')
    def test_terminal_metadata_complete(self, mock_exists):
        """Test that terminal metadata is complete"""
        def exists_side_effect(path):
            return "VsDevCmd.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminal = self.detector._detect_developer_cmd()

        self.assertIsNotNone(terminal)
        self.assertIn("installation_path", terminal.metadata)
        self.assertIn("version", terminal.metadata)
        self.assertIn("batch_file", terminal.metadata)

    @patch('os.path.exists')
    def test_terminal_capabilities_set(self, mock_exists):
        """Test that terminal capabilities are set correctly"""
        def exists_side_effect(path):
            return "vcvars64.bat" in path or "Visual Studio" in path

        mock_exists.side_effect = exists_side_effect

        terminals = self.detector._detect_native_tools()

        self.assertGreater(len(terminals), 0)
        for terminal in terminals:
            self.assertIn("msvc", terminal.capabilities)
            self.assertIn("native_tools", terminal.capabilities)


if __name__ == '__main__':
    unittest.main()
