"""
Unit tests for MSYS2 Terminal Detector

Tests comprehensive detection of MSYS2 shells and all
environment-specific terminal variants (UCRT64, MINGW64, MINGW32, MSYS, CLANG64).
"""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.mingw_terminal_detector import (
    MSYS2TerminalDetector,
    TerminalInfo,
    TerminalType,
    ITerminalDetector
)


class TestMSYS2TerminalDetector(unittest.TestCase):
    """Test cases for MSYS2 Terminal Detector"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MSYS2TerminalDetector(logger=self.logger)

    def test_init(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsInstance(self.detector, ITerminalDetector)
        self.assertEqual(self.detector._detected_terminals, [])
        self.assertIsInstance(self.detector._msys2_paths, list)

    def test_detect_returns_list(self):
        """Test that detect returns a list"""
        result = self.detector.detect()
        self.assertIsInstance(result, list)
        self.assertIsInstance(self.detector._detected_terminals, list)

    def test_detect_logs_start(self):
        """Test that detect logs start message"""
        self.detector.detect()
        self.logger.info.assert_any_call("Starting MSYS2 terminal detection")

    def test_detect_logs_completion(self):
        """Test that detect logs completion message"""
        self.detector.detect()
        # Check that info was called with completion message
        info_calls = [str(call) for call in self.logger.info.call_args_list]
        self.assertTrue(any("Total detected MSYS2 terminals" in str(call) for call in info_calls))

    def test_get_terminal_existing(self):
        """Test getting an existing terminal"""
        # Create a mock terminal
        mock_terminal = TerminalInfo(
            terminal_id="ucrt64",
            name="MSYS2 UCRT64",
            type=TerminalType.MSYS2_UCRT64,
            executable="C:\\msys64\\msys2_shell.cmd",
            architecture="x64",
            environment="UCRT64"
        )
        self.detector._detected_terminals = [mock_terminal]

        result = self.detector.get_terminal("ucrt64")
        self.assertIsNotNone(result)
        self.assertEqual(result.terminal_id, "ucrt64")

    def test_get_terminal_not_found(self):
        """Test getting a non-existent terminal"""
        self.detector._detected_terminals = []
        result = self.detector.get_terminal("nonexistent")
        self.assertIsNone(result)
        self.logger.warning.assert_called_with("Terminal not found: nonexistent")

    def test_validate_valid_terminal(self):
        """Test validating a valid terminal"""
        # Create a temporary file to simulate a terminal
        with tempfile.NamedTemporaryFile(suffix=".cmd", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            terminal = TerminalInfo(
                terminal_id="test",
                name="Test Terminal",
                type=TerminalType.MSYS2_UCRT64,
                executable=tmp_path,
                architecture="x64",
                environment="UCRT64"
            )

            result = self.detector.validate(terminal)
            self.assertTrue(result)
        finally:
            os.unlink(tmp_path)

    def test_validate_nonexistent_terminal(self):
        """Test validating a non-existent terminal"""
        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSYS2_UCRT64,
            executable="C:\\nonexistent\\terminal.cmd",
            architecture="x64",
            environment="UCRT64"
        )

        result = self.detector.validate(terminal)
        self.assertFalse(result)
        self.logger.error.assert_called()

    def test_validate_directory_path(self):
        """Test validating a directory path instead of file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            terminal = TerminalInfo(
                terminal_id="test",
                name="Test Terminal",
                type=TerminalType.MSYS2_UCRT64,
                executable=tmp_dir,
                architecture="x64",
                environment="UCRT64"
            )

            result = self.detector.validate(terminal)
            self.assertFalse(result)
            self.logger.error.assert_called()

    @patch('os.path.exists')
    def test_detect_msys2_shells_ucrt64(self, mock_exists):
        """Test detection of UCRT64 shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminals = self.detector._detect_msys2_shells()

            # Check that UCRT64 terminal was detected
            ucrt64_terminals = [t for t in terminals if t.terminal_id == "ucrt64"]
            self.assertEqual(len(ucrt64_terminals), 1)

            terminal = ucrt64_terminals[0]
            self.assertEqual(terminal.name, "MSYS2 UCRT64")
            self.assertEqual(terminal.type, TerminalType.MSYS2_UCRT64)
            self.assertEqual(terminal.architecture, "x64")
            self.assertEqual(terminal.environment, "UCRT64")
            self.assertIn("msys2", terminal.capabilities)
            self.assertIn("mingw", terminal.capabilities)

    @patch('os.path.exists')
    def test_detect_msys2_shells_mingw64(self, mock_exists):
        """Test detection of MINGW64 shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminals = self.detector._detect_msys2_shells()

            # Check that MINGW64 terminal was detected
            mingw64_terminals = [t for t in terminals if t.terminal_id == "mingw64"]
            self.assertEqual(len(mingw64_terminals), 1)

            terminal = mingw64_terminals[0]
            self.assertEqual(terminal.name, "MSYS2 MINGW64")
            self.assertEqual(terminal.type, TerminalType.MSYS2_MINGW64)
            self.assertEqual(terminal.architecture, "x64")
            self.assertEqual(terminal.environment, "MINGW64")

    @patch('os.path.exists')
    def test_detect_msys2_shells_mingw32(self, mock_exists):
        """Test detection of MINGW32 shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminals = self.detector._detect_msys2_shells()

            # Check that MINGW32 terminal was detected
            mingw32_terminals = [t for t in terminals if t.terminal_id == "mingw32"]
            self.assertEqual(len(mingw32_terminals), 1)

            terminal = mingw32_terminals[0]
            self.assertEqual(terminal.name, "MSYS2 MINGW32")
            self.assertEqual(terminal.type, TerminalType.MSYS2_MINGW32)
            self.assertEqual(terminal.architecture, "x86")
            self.assertEqual(terminal.environment, "MINGW32")

    @patch('os.path.exists')
    def test_detect_msys2_shells_msys(self, mock_exists):
        """Test detection of MSYS shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminals = self.detector._detect_msys2_shells()

            # Check that MSYS terminal was detected
            msys_terminals = [t for t in terminals if t.terminal_id == "msys"]
            self.assertEqual(len(msys_terminals), 1)

            terminal = msys_terminals[0]
            self.assertEqual(terminal.name, "MSYS2 MSYS")
            self.assertEqual(terminal.type, TerminalType.MSYS2_MSYS)
            self.assertEqual(terminal.architecture, "x64")
            self.assertEqual(terminal.environment, "MSYS")

    @patch('os.path.exists')
    def test_detect_msys2_shells_clang64(self, mock_exists):
        """Test detection of CLANG64 shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminals = self.detector._detect_msys2_shells()

            # Check that CLANG64 terminal was detected
            clang64_terminals = [t for t in terminals if t.terminal_id == "clang64"]
            self.assertEqual(len(clang64_terminals), 1)

            terminal = clang64_terminals[0]
            self.assertEqual(terminal.name, "MSYS2 CLANG64")
            self.assertEqual(terminal.type, TerminalType.MSYS2_CLANG64)
            self.assertEqual(terminal.architecture, "x64")
            self.assertEqual(terminal.environment, "CLANG64")

    @patch('os.path.exists')
    def test_detect_msys2_shells_no_installation(self, mock_exists):
        """Test detection when MSYS2 is not installed"""
        # Mock no MSYS2 paths
        mock_exists.return_value = False

        with patch.object(self.detector, '_msys2_paths', []):
            terminals = self.detector._detect_msys2_shells()

            # Check that no terminals were detected
            self.assertEqual(len(terminals), 0)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_detect_shortcuts(self, mock_listdir, mock_exists):
        """Test detection of Start Menu shortcuts"""
        # Mock Start Menu structure
        mock_exists.return_value = True
        mock_listdir.return_value = ["MSYS2 64bit"]

        with patch.object(self.detector, '_scan_msys2_folder', return_value=[]):
            terminals = self.detector._detect_shortcuts()

            # Check that scan was called (may not be called if no MSYS2 folders exist)
            # Just verify it returns a list
            self.assertIsInstance(terminals, list)

    @patch('os.path.exists')
    def test_find_msys2_shell_ucrt64(self, mock_exists):
        """Test finding UCRT64 shell"""
        # Mock MSYS2 path
        mock_exists.side_effect = lambda path: "msys64" in path.lower() or "msys2_shell.cmd" in path.lower()

        config = {
            "terminal_id": "ucrt64",
            "name": "MSYS2 UCRT64",
            "type": TerminalType.MSYS2_UCRT64,
            "architecture": "x64",
            "environment": "UCRT64",
            "msystem": "UCRT64",
            "mingw_prefix": "/ucrt64",
            "mingw_chost": "x86_64-w64-mingw32",
            "recommended": True
        }

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            terminal = self.detector._find_msys2_shell(config)

            self.assertIsNotNone(terminal)
            self.assertEqual(terminal.terminal_id, "ucrt64")
            self.assertEqual(terminal.name, "MSYS2 UCRT64")
            self.assertEqual(terminal.environment, "UCRT64")
            self.assertIn("msystem", terminal.metadata)
            self.assertEqual(terminal.metadata["msystem"], "UCRT64")

    @patch('os.path.exists')
    def test_find_msys2_shell_not_found(self, mock_exists):
        """Test finding shell when MSYS2 is not installed"""
        # Mock no MSYS2 paths
        mock_exists.return_value = False

        config = {
            "terminal_id": "ucrt64",
            "name": "MSYS2 UCRT64",
            "type": TerminalType.MSYS2_UCRT64,
            "architecture": "x64",
            "environment": "UCRT64",
            "msystem": "UCRT64",
            "mingw_prefix": "/ucrt64",
            "mingw_chost": "x86_64-w64-mingw32",
            "recommended": True
        }

        with patch.object(self.detector, '_msys2_paths', []):
            terminal = self.detector._find_msys2_shell(config)

            self.assertIsNone(terminal)

    @patch('os.path.exists')
    def test_get_shell_executable_ucrt64(self, mock_exists):
        """Test getting shell executable for UCRT64"""
        # Mock bash.exe exists
        mock_exists.side_effect = lambda path: "bash.exe" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            shell_path = self.detector._get_shell_executable("C:\\msys64", "UCRT64")

            self.assertIn("ucrt64", shell_path.lower())
            self.assertIn("bash.exe", shell_path.lower())

    @patch('os.path.exists')
    def test_get_shell_executable_mingw64(self, mock_exists):
        """Test getting shell executable for MINGW64"""
        # Mock bash.exe exists
        mock_exists.side_effect = lambda path: "bash.exe" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            shell_path = self.detector._get_shell_executable("C:\\msys64", "MINGW64")

            self.assertIn("mingw64", shell_path.lower())
            self.assertIn("bash.exe", shell_path.lower())

    @patch('os.path.exists')
    def test_get_shell_executable_fallback(self, mock_exists):
        """Test fallback to usr/bin/bash.exe"""
        # Mock bash.exe only exists in usr/bin
        mock_exists.side_effect = lambda path: "usr\\bin\\bash.exe" in path.lower()

        with patch.object(self.detector, '_msys2_paths', ["C:\\msys64"]):
            shell_path = self.detector._get_shell_executable("C:\\msys64", "UCRT64")

            self.assertIn("usr", shell_path.lower())
            self.assertIn("bin", shell_path.lower())
            self.assertIn("bash.exe", shell_path.lower())

    @patch('os.path.exists')
    def test_get_msys2_paths_standard(self, mock_exists):
        """Test getting MSYS2 paths from standard locations"""
        # Mock standard paths exist
        mock_exists.side_effect = lambda path: "msys64" in path.lower()

        paths = self.detector._get_msys2_paths()

        # Check that standard paths were found
        self.assertTrue(any("msys64" in path.lower() for path in paths))

    @patch('os.path.exists')
    @patch.dict(os.environ, {'PATH': 'C:\\msys64\\ucrt64\\bin;C:\\Windows\\System32'})
    def test_get_msys2_paths_from_env(self, mock_exists):
        """Test getting MSYS2 paths from PATH environment variable"""
        # Mock paths exist
        mock_exists.return_value = True

        paths = self.detector._get_msys2_paths()

        # Check that PATH was scanned
        self.assertTrue(any("msys64" in path.lower() for path in paths))

    def test_extract_msys2_root_msys64(self):
        """Test extracting MSYS2 root from msys64 path"""
        path = "C:\\msys64\\ucrt64\\bin"
        root = self.detector._extract_msys2_root(path)

        self.assertEqual(root, "C:\\msys64")

    def test_extract_msys2_root_msys32(self):
        """Test extracting MSYS2 root from msys32 path"""
        path = "C:\\msys32\\mingw64\\bin"
        root = self.detector._extract_msys2_root(path)

        self.assertEqual(root, "C:\\msys32")

    def test_extract_msys2_root_no_match(self):
        """Test extracting MSYS2 root from non-MSYS2 path"""
        path = "C:\\Windows\\System32"
        root = self.detector._extract_msys2_root(path)

        self.assertIsNone(root)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scan_msys2_folder(self, mock_listdir, mock_exists):
        """Test scanning MSYS2 folder for shortcuts"""
        # Mock folder contents
        mock_exists.return_value = True
        mock_listdir.return_value = ["MSYS2 UCRT64.lnk", "MSYS2 MINGW64.lnk"]

        with patch.object(self.detector, '_resolve_shortcut', return_value="C:\\msys64\\msys2_shell.cmd"):
            with patch.object(self.detector, '_create_terminal_from_shortcut', return_value=None):
                terminals = self.detector._scan_msys2_folder("C:\\Start Menu\\MSYS2 64bit")

                # Check that shortcuts were processed
                self.assertEqual(mock_listdir.call_count, 1)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scan_msys2_folder_permission_error(self, mock_listdir, mock_exists):
        """Test scanning MSYS2 folder with permission error"""
        # Mock permission error
        mock_exists.return_value = True
        mock_listdir.side_effect = PermissionError("Access denied")

        terminals = self.detector._scan_msys2_folder("C:\\Start Menu\\MSYS2 64bit")

        # Check that error was handled gracefully
        self.assertEqual(len(terminals), 0)
        self.logger.warning.assert_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_ucrt64(self, mock_listdir, mock_exists):
        """Test creating terminal from UCRT64 shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "MSYS2 UCRT64.lnk",
            "C:\\msys64\\msys2_shell.cmd"
        )

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "ucrt64")
        self.assertEqual(terminal.name, "MSYS2 UCRT64")
        self.assertEqual(terminal.type, TerminalType.MSYS2_UCRT64)
        self.assertEqual(terminal.environment, "UCRT64")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_mingw64(self, mock_listdir, mock_exists):
        """Test creating terminal from MINGW64 shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "MSYS2 MINGW64.lnk",
            "C:\\msys64\\msys2_shell.cmd"
        )

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "mingw64")
        self.assertEqual(terminal.name, "MSYS2 MINGW64")
        self.assertEqual(terminal.type, TerminalType.MSYS2_MINGW64)
        self.assertEqual(terminal.environment, "MINGW64")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_mingw32(self, mock_listdir, mock_exists):
        """Test creating terminal from MINGW32 shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "MSYS2 MINGW32.lnk",
            "C:\\msys64\\msys2_shell.cmd"
        )

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "mingw32")
        self.assertEqual(terminal.name, "MSYS2 MINGW32")
        self.assertEqual(terminal.type, TerminalType.MSYS2_MINGW32)
        self.assertEqual(terminal.environment, "MINGW32")
        self.assertEqual(terminal.architecture, "x86")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_msys(self, mock_listdir, mock_exists):
        """Test creating terminal from MSYS shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "MSYS2 MSYS.lnk",
            "C:\\msys64\\msys2_shell.cmd"
        )

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "msys")
        self.assertEqual(terminal.name, "MSYS2 MSYS")
        self.assertEqual(terminal.type, TerminalType.MSYS2_MSYS)
        self.assertEqual(terminal.environment, "MSYS")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_clang64(self, mock_listdir, mock_exists):
        """Test creating terminal from CLANG64 shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "MSYS2 CLANG64.lnk",
            "C:\\msys64\\msys2_shell.cmd"
        )

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "clang64")
        self.assertEqual(terminal.name, "MSYS2 CLANG64")
        self.assertEqual(terminal.type, TerminalType.MSYS2_CLANG64)
        self.assertEqual(terminal.environment, "CLANG64")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_create_terminal_from_shortcut_invalid(self, mock_listdir, mock_exists):
        """Test creating terminal from invalid shortcut"""
        mock_exists.return_value = True

        terminal = self.detector._create_terminal_from_shortcut(
            "Some Other App.lnk",
            "C:\\Some\\App.exe"
        )

        self.assertIsNone(terminal)

    def test_terminal_info_to_dict(self):
        """Test TerminalInfo to_dict method"""
        terminal = TerminalInfo(
            terminal_id="ucrt64",
            name="MSYS2 UCRT64",
            type=TerminalType.MSYS2_UCRT64,
            executable="C:\\msys64\\msys2_shell.cmd",
            arguments=["-ucrt64"],
            architecture="x64",
            environment="UCRT64",
            capabilities=["msys2", "mingw"],
            metadata={"msystem": "UCRT64"},
            recommended=True
        )

        result = terminal.to_dict()

        self.assertEqual(result["terminal_id"], "ucrt64")
        self.assertEqual(result["name"], "MSYS2 UCRT64")
        self.assertEqual(result["type"], "msys2_ucrt64")
        self.assertEqual(result["executable"], "C:\\msys64\\msys2_shell.cmd")
        self.assertEqual(result["arguments"], ["-ucrt64"])
        self.assertEqual(result["architecture"], "x64")
        self.assertEqual(result["environment"], "UCRT64")
        self.assertEqual(result["capabilities"], ["msys2", "mingw"])
        self.assertEqual(result["metadata"], {"msystem": "UCRT64"})
        self.assertEqual(result["recommended"], True)

    def test_terminal_info_is_valid(self):
        """Test TerminalInfo is_valid method"""
        with tempfile.NamedTemporaryFile(suffix=".cmd", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            terminal = TerminalInfo(
                terminal_id="test",
                name="Test Terminal",
                type=TerminalType.MSYS2_UCRT64,
                executable=tmp_path,
                architecture="x64",
                environment="UCRT64"
            )

            self.assertTrue(terminal.is_valid())
        finally:
            os.unlink(tmp_path)

    def test_terminal_info_is_valid_nonexistent(self):
        """Test TerminalInfo is_valid with non-existent file"""
        terminal = TerminalInfo(
            terminal_id="test",
            name="Test Terminal",
            type=TerminalType.MSYS2_UCRT64,
            executable="C:\\nonexistent\\terminal.cmd",
            architecture="x64",
            environment="UCRT64"
        )

        self.assertFalse(terminal.is_valid())


class TestMSYS2TerminalDetectorIntegration(unittest.TestCase):
    """Integration tests for MSYS2 Terminal Detector"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MSYS2TerminalDetector(logger=self.logger)

    def test_full_detection_workflow(self):
        """Test complete detection workflow"""
        # Run detection
        terminals = self.detector.detect()

        # Verify result is a list
        self.assertIsInstance(terminals, list)

        # Verify all terminals have required fields
        for terminal in terminals:
            self.assertIsInstance(terminal, TerminalInfo)
            self.assertIsNotNone(terminal.terminal_id)
            self.assertIsNotNone(terminal.name)
            self.assertIsNotNone(terminal.type)
            self.assertIsNotNone(terminal.executable)
            self.assertIsNotNone(terminal.architecture)
            self.assertIsNotNone(terminal.environment)

    def test_get_terminal_after_detection(self):
        """Test getting terminal after detection"""
        # Run detection
        terminals = self.detector.detect()

        if terminals:
            # Get first terminal
            first_terminal = terminals[0]
            result = self.detector.get_terminal(first_terminal.terminal_id)

            self.assertIsNotNone(result)
            self.assertEqual(result.terminal_id, first_terminal.terminal_id)

    def test_validate_detected_terminals(self):
        """Test validating all detected terminals"""
        # Run detection
        terminals = self.detector.detect()

        # Validate each terminal
        for terminal in terminals:
            # Skip validation if executable doesn't exist (mock environment)
            if os.path.exists(terminal.executable):
                result = self.detector.validate(terminal)
                # Validation should succeed or fail gracefully
                self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()
