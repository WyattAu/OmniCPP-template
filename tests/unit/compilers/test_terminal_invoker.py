"""
Unit tests for Terminal Invoker

This module contains comprehensive unit tests for Terminal Invoker,
covering command execution, environment setup, batch file execution,
and compiler-specific environment configuration.
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

from compilers.terminal_invoker import (
    TerminalInvoker,
    CommandResult,
    CompilerInfo
)


class TestCommandResult(unittest.TestCase):
    """Test cases for CommandResult dataclass"""

    def test_command_result_creation(self):
        """Test CommandResult creation"""
        result = CommandResult(
            exit_code=0,
            stdout="output",
            stderr="error"
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "output")
        self.assertEqual(result.stderr, "error")
        self.assertEqual(result.execution_time, 0.0)

    def test_command_result_with_environment(self):
        """Test CommandResult with environment"""
        env = {"VAR1": "value1", "VAR2": "value2"}
        result = CommandResult(
            exit_code=0,
            stdout="output",
            stderr="error",
            environment=env,
            execution_time=1.5
        )
        self.assertEqual(len(result.environment), 2)
        self.assertEqual(result.execution_time, 1.5)

    def test_command_result_success_property(self):
        """Test CommandResult success property"""
        result_success = CommandResult(
            exit_code=0,
            stdout="output",
            stderr=""
        )
        result_failure = CommandResult(
            exit_code=1,
            stdout="output",
            stderr="error"
        )
        self.assertTrue(result_success.success)
        self.assertFalse(result_failure.success)

    def test_command_result_to_dict(self):
        """Test CommandResult to_dict method"""
        env = {"VAR": "value"}
        result = CommandResult(
            exit_code=0,
            stdout="output",
            stderr="error",
            environment=env,
            execution_time=2.5
        )
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict["exit_code"], 0)
        self.assertEqual(result_dict["stdout"], "output")
        self.assertEqual(result_dict["stderr"], "error")
        self.assertEqual(result_dict["execution_time"], 2.5)


class TestCompilerInfo(unittest.TestCase):
    """Test cases for CompilerInfo dataclass"""

    def test_compiler_info_creation(self):
        """Test CompilerInfo creation"""
        compiler = CompilerInfo(
            compiler_type="msvc",
            version="19.40.0",
            path="/path/to/cl.exe",
            architecture="x64"
        )
        self.assertEqual(compiler.compiler_type, "msvc")
        self.assertEqual(compiler.version, "19.40.0")
        self.assertEqual(compiler.path, "/path/to/cl.exe")
        self.assertEqual(compiler.architecture, "x64")

    def test_compiler_info_with_metadata(self):
        """Test CompilerInfo with metadata"""
        metadata = {"msys2_path": "/path/to/msys64"}
        compiler = CompilerInfo(
            compiler_type="mingw_gcc",
            version="13.2.0",
            path="/path/to/gcc.exe",
            architecture="x64",
            metadata=metadata
        )
        self.assertEqual(len(compiler.metadata), 1)
        self.assertEqual(compiler.metadata["msys2_path"], "/path/to/msys64")


class TestTerminalInvokerInitialization(unittest.TestCase):
    """Test cases for TerminalInvoker initialization"""

    def test_invoker_initialization(self):
        """Test TerminalInvoker initialization"""
        invoker = TerminalInvoker()
        self.assertIsNotNone(invoker)
        self.assertIsInstance(invoker._environment, dict)
        self.assertIsInstance(invoker._original_environment, dict)

    def test_invoker_with_logger(self):
        """Test TerminalInvoker with custom logger"""
        import logging
        logger = logging.getLogger("test_logger")
        invoker = TerminalInvoker(logger=logger)
        self.assertIsNotNone(invoker)


class TestTerminalInvokerExecuteCommand(unittest.TestCase):
    """Test cases for TerminalInvoker execute_command method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test successful command execution"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "command output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = self.invoker.execute_command("echo test")

        self.assertTrue(result.success)
        self.assertEqual(result.stdout, "command output")
        self.assertEqual(result.stderr, "")
        self.assertGreater(result.execution_time, 0)

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        """Test failed command execution"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "command failed"
        mock_run.return_value = mock_result

        result = self.invoker.execute_command("exit 1")

        self.assertFalse(result.success)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.stderr, "command failed")

    @patch('subprocess.run')
    def test_execute_command_timeout(self, mock_run):
        """Test command execution with timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired("test", 5)

        result = self.invoker.execute_command("sleep 10", timeout=5)

        self.assertEqual(result.exit_code, -1)
        self.assertIn("timed out", result.stderr)

    @patch('subprocess.run')
    def test_execute_command_not_found(self, mock_run):
        """Test command execution with file not found"""
        mock_run.side_effect = FileNotFoundError("command not found")

        result = self.invoker.execute_command("nonexistent_command")

        self.assertEqual(result.exit_code, -1)
        self.assertIn("not found", result.stderr)

    @patch('subprocess.run')
    def test_execute_command_permission_denied(self, mock_run):
        """Test command execution with permission denied"""
        mock_run.side_effect = PermissionError("permission denied")

        result = self.invoker.execute_command("protected_command")

        self.assertEqual(result.exit_code, -1)
        self.assertIn("Permission denied", result.stderr)

    @patch('subprocess.run')
    def test_execute_command_with_custom_timeout(self, mock_run):
        """Test command execution with custom timeout"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = self.invoker.execute_command("echo test", timeout=60)

        mock_run.assert_called_once()
        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs["timeout"], 60)

    @patch('subprocess.run')
    def test_execute_command_with_cwd(self, mock_run):
        """Test command execution with custom working directory"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = self.invoker.execute_command("echo test", cwd="/tmp")

        mock_run.assert_called_once()
        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs["cwd"], "/tmp")

    def test_execute_command_empty_command(self):
        """Test command execution with empty command"""
        with self.assertRaises(ValueError) as context:
            self.invoker.execute_command("")
        self.assertIn("empty", str(context.exception))

    def test_execute_command_whitespace_only(self):
        """Test command execution with whitespace only"""
        with self.assertRaises(ValueError) as context:
            self.invoker.execute_command("   ")
        self.assertIn("empty", str(context.exception))


class TestTerminalInvokerSetupEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker setup_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.object(TerminalInvoker, '_setup_msvc_environment')
    def test_setup_msvc_environment(self, mock_setup):
        """Test MSVC environment setup"""
        compiler = CompilerInfo(
            compiler_type="msvc",
            version="19.40.0",
            path="/path/to/cl.exe",
            architecture="x64"
        )

        env = self.invoker.setup_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIsInstance(env, dict)

    @patch.object(TerminalInvoker, '_setup_msvc_clang_environment')
    def test_setup_msvc_clang_environment(self, mock_setup):
        """Test MSVC-Clang environment setup"""
        compiler = CompilerInfo(
            compiler_type="msvc_clang",
            version="19.40.0",
            path="/path/to/clang.exe",
            architecture="x64"
        )

        env = self.invoker.setup_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIsInstance(env, dict)

    @patch.object(TerminalInvoker, '_setup_mingw_gcc_environment')
    def test_setup_mingw_gcc_environment(self, mock_setup):
        """Test MinGW-GCC environment setup"""
        compiler = CompilerInfo(
            compiler_type="mingw_gcc",
            version="13.2.0",
            path="/path/to/gcc.exe",
            architecture="x64"
        )

        env = self.invoker.setup_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIsInstance(env, dict)

    @patch.object(TerminalInvoker, '_setup_mingw_clang_environment')
    def test_setup_mingw_clang_environment(self, mock_setup):
        """Test MinGW-Clang environment setup"""
        compiler = CompilerInfo(
            compiler_type="mingw_clang",
            version="18.1.0",
            path="/path/to/clang.exe",
            architecture="x64"
        )

        env = self.invoker.setup_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIsInstance(env, dict)

    def test_setup_unsupported_compiler_type(self):
        """Test environment setup with unsupported compiler type"""
        compiler = CompilerInfo(
            compiler_type="unsupported",
            version="1.0.0",
            path="/path/to/compiler.exe",
            architecture="x64"
        )

        with self.assertRaises(ValueError) as context:
            self.invoker.setup_environment(compiler)
        self.assertIn("Unsupported", str(context.exception))


class TestTerminalInvokerCaptureEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker capture_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.dict(os.environ, {"TEST_VAR": "test_value"}, clear=True)
    def test_capture_environment(self):
        """Test environment capture"""
        env = self.invoker.capture_environment()

        self.assertIsInstance(env, dict)
        self.assertIn("TEST_VAR", env)
        self.assertEqual(env["TEST_VAR"], "test_value")


class TestTerminalInvokerRestoreEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker restore_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.dict(os.environ, {"ORIGINAL_VAR": "original_value"}, clear=True)
    def test_restore_environment(self):
        """Test environment restore"""
        # Capture original environment
        original_env = dict(os.environ)

        # Modify environment
        os.environ["NEW_VAR"] = "new_value"

        # Restore environment
        self.invoker.restore_environment(original_env)

        self.assertEqual(os.environ.get("ORIGINAL_VAR"), "original_value")
        self.assertIsNone(os.environ.get("NEW_VAR"))


class TestTerminalInvokerExecuteBatchFile(unittest.TestCase):
    """Test cases for TerminalInvoker execute_batch_file method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch('os.path.exists')
    @patch.object(TerminalInvoker, 'execute_command')
    def test_execute_batch_file_success(self, mock_execute, mock_exists):
        """Test successful batch file execution"""
        mock_exists.return_value = True
        mock_execute.return_value = CommandResult(
            exit_code=0,
            stdout="output",
            stderr=""
        )

        with tempfile.NamedTemporaryFile(suffix=".bat", delete=False) as tmp:
            tmp_path = tmp.name

            result = self.invoker.execute_batch_file(tmp_path, ["arg1", "arg2"])

            mock_execute.assert_called_once()
            call_args = mock_execute.call_args[0][0]
            self.assertIn(tmp_path, call_args)
            self.assertIn("arg1", call_args)
            self.assertIn("arg2", call_args)

            # Clean up (handle Windows file locking)
            try:
                os.unlink(tmp_path)
            except (PermissionError, OSError):
                pass

    def test_execute_batch_file_not_found(self):
        """Test batch file execution with file not found"""
        with self.assertRaises(FileNotFoundError) as context:
            self.invoker.execute_batch_file("/nonexistent/batch.bat", [])
        self.assertIn("not found", str(context.exception))

    def test_execute_batch_file_empty_path(self):
        """Test batch file execution with empty path"""
        with self.assertRaises(ValueError) as context:
            self.invoker.execute_batch_file("", [])
        self.assertIn("empty", str(context.exception))

    @patch('os.path.exists')
    @patch.object(TerminalInvoker, 'execute_command')
    def test_execute_batch_file_with_timeout(self, mock_execute, mock_exists):
        """Test batch file execution with custom timeout"""
        mock_exists.return_value = True
        mock_execute.return_value = CommandResult(
            exit_code=0,
            stdout="output",
            stderr=""
        )

        with tempfile.NamedTemporaryFile(suffix=".bat", delete=False) as tmp:
            tmp_path = tmp.name

            result = self.invoker.execute_batch_file(
                tmp_path,
                ["arg1"],
                timeout=60
            )

            mock_execute.assert_called_once()
            call_kwargs = mock_execute.call_args[1]
            self.assertEqual(call_kwargs["timeout"], 60)

            # Clean up (handle Windows file locking)
            try:
                os.unlink(tmp_path)
            except (PermissionError, OSError):
                pass


class TestTerminalInvokerSetupMSVCEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker _setup_msvc_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.object(TerminalInvoker, '_find_vcvarsall')
    @patch.object(TerminalInvoker, 'execute_batch_file')
    def test_setup_msvc_environment_success(self, mock_execute, mock_find):
        """Test successful MSVC environment setup"""
        mock_find.return_value = "/path/to/vcvarsall.bat"
        mock_execute.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr=""
        )

        compiler = CompilerInfo(
            compiler_type="msvc",
            version="19.40.0",
            path="/path/to/cl.exe",
            architecture="x64"
        )

        self.invoker._setup_msvc_environment(compiler)

        mock_find.assert_called_once_with(compiler.path)
        mock_execute.assert_called_once()

    @patch.object(TerminalInvoker, '_find_vcvarsall')
    def test_setup_msvc_environment_vcvarsall_not_found(self, mock_find):
        """Test MSVC environment setup when vcvarsall not found"""
        mock_find.return_value = None

        compiler = CompilerInfo(
            compiler_type="msvc",
            version="19.40.0",
            path="/path/to/cl.exe",
            architecture="x64"
        )

        # Should not raise exception, just log warning
        self.invoker._setup_msvc_environment(compiler)

        mock_find.assert_called_once()


class TestTerminalInvokerSetupMSVCCLangEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker _setup_msvc_clang_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.object(TerminalInvoker, '_setup_msvc_environment')
    @patch('os.path.exists')
    @patch.dict(os.environ, {"PATH": "original_path"}, clear=False)
    def test_setup_msvc_clang_environment_success(self, mock_exists, mock_setup):
        """Test successful MSVC-Clang environment setup"""
        mock_exists.return_value = True

        compiler = CompilerInfo(
            compiler_type="msvc_clang",
            version="19.40.0",
            path="/path/to/clang.exe",
            architecture="x64"
        )

        self.invoker._setup_msvc_clang_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIn("/path/to", os.environ["PATH"])
        self.assertEqual(os.environ["LLVM_DIR"], "/path/to")

    @patch.object(TerminalInvoker, '_setup_msvc_environment')
    @patch('os.path.exists')
    @patch.dict(os.environ, {"PATH": "original_path"}, clear=False)
    def test_setup_msvc_clang_environment_llvm_not_found(self, mock_exists, mock_setup):
        """Test MSVC-Clang environment setup when LLVM path not found"""
        mock_exists.return_value = False

        compiler = CompilerInfo(
            compiler_type="msvc_clang",
            version="19.40.0",
            path="/path/to/clang.exe",
            architecture="x64"
        )

        self.invoker._setup_msvc_clang_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        # PATH should not be modified
        self.assertEqual(os.environ["PATH"], "original_path")


class TestTerminalInvokerSetupMinGWGCCEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker _setup_mingw_gcc_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch('os.path.exists')
    @patch.dict(os.environ, {}, clear=True)
    def test_setup_mingw_gcc_environment_success(self, mock_exists):
        """Test successful MinGW-GCC environment setup"""
        mock_exists.return_value = True

        compiler = CompilerInfo(
            compiler_type="mingw_gcc",
            version="13.2.0",
            path="/path/to/gcc.exe",
            architecture="x64",
            metadata={
                "msys2_path": "/path/to/msys64",
                "environment": "UCRT64"
            }
        )

        self.invoker._setup_mingw_gcc_environment(compiler)

        self.assertEqual(os.environ["MSYSTEM"], "UCRT64")
        self.assertEqual(os.environ["MINGW_PREFIX"], "/ucrt64")
        # Check that path is in PATH (handle Windows path separators)
        # The PATH will have the ucrt64/bin path added
        self.assertTrue(
            "ucrt64" in os.environ["PATH"].lower()
        )

    @patch('os.path.exists')
    @patch.dict(os.environ, {}, clear=True)
    def test_setup_mingw_gcc_environment_no_msys2_path(self, mock_exists):
        """Test MinGW-GCC environment setup without MSYS2 path"""
        mock_exists.return_value = True

        compiler = CompilerInfo(
            compiler_type="mingw_gcc",
            version="13.2.0",
            path="/path/to/gcc.exe",
            architecture="x64",
            metadata={}
        )

        # Should not raise exception, just log warning
        self.invoker._setup_mingw_gcc_environment(compiler)

    @patch('os.path.exists')
    @patch.dict(os.environ, {}, clear=True)
    def test_setup_mingw_gcc_environment_msys2_not_found(self, mock_exists):
        """Test MinGW-GCC environment setup when MSYS2 path not found"""
        mock_exists.return_value = False

        compiler = CompilerInfo(
            compiler_type="mingw_gcc",
            version="13.2.0",
            path="/path/to/gcc.exe",
            architecture="x64",
            metadata={
                "msys2_path": "/nonexistent/msys64",
                "environment": "UCRT64"
            }
        )

        # Should not raise exception, just log warning
        self.invoker._setup_mingw_gcc_environment(compiler)


class TestTerminalInvokerSetupMinGWClangEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker _setup_mingw_clang_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.object(TerminalInvoker, '_setup_mingw_gcc_environment')
    @patch('os.path.exists')
    @patch.dict(os.environ, {"PATH": "original_path"}, clear=False)
    def test_setup_mingw_clang_environment_success(self, mock_exists, mock_setup):
        """Test successful MinGW-Clang environment setup"""
        mock_exists.return_value = True

        compiler = CompilerInfo(
            compiler_type="mingw_clang",
            version="18.1.0",
            path="/path/to/clang.exe",
            architecture="x64",
            metadata={
                "msys2_path": "/path/to/msys64",
                "environment": "UCRT64"
            }
        )

        self.invoker._setup_mingw_clang_environment(compiler)

        mock_setup.assert_called_once_with(compiler)
        self.assertIn("/path/to", os.environ["PATH"])
        self.assertEqual(os.environ["LLVM_DIR"], "/path/to")


class TestTerminalInvokerFindVcvarsall(unittest.TestCase):
    """Test cases for TerminalInvoker _find_vcvarsall method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch('os.path.exists')
    def test_find_vcvarsall_found(self, mock_exists):
        """Test finding vcvarsall.bat"""
        def exists_side_effect(path):
            return "vcvarsall.bat" in path

        mock_exists.side_effect = exists_side_effect

        compiler_path = "/path/to/cl.exe"
        vcvarsall_path = self.invoker._find_vcvarsall(compiler_path)

        self.assertIsNotNone(vcvarsall_path)
        self.assertIn("vcvarsall.bat", vcvarsall_path)

    @patch('os.path.exists')
    def test_find_vcvarsall_not_found(self, mock_exists):
        """Test vcvarsall.bat not found"""
        mock_exists.return_value = False

        compiler_path = "/path/to/cl.exe"
        vcvarsall_path = self.invoker._find_vcvarsall(compiler_path)

        self.assertIsNone(vcvarsall_path)


class TestTerminalInvokerResetEnvironment(unittest.TestCase):
    """Test cases for TerminalInvoker reset_environment method"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch.dict(os.environ, {"ORIGINAL_VAR": "original_value"}, clear=True)
    def test_reset_environment(self):
        """Test environment reset"""
        # Set original environment
        original_env = dict(os.environ)
        self.invoker._original_environment = original_env

        # Modify environment
        os.environ["NEW_VAR"] = "new_value"

        # Reset environment
        self.invoker.reset_environment()

        self.assertEqual(os.environ.get("ORIGINAL_VAR"), "original_value")
        self.assertIsNone(os.environ.get("NEW_VAR"))

    def test_reset_environment_no_original(self):
        """Test environment reset without original environment"""
        # No original environment set
        self.invoker._original_environment = {}

        # Should not raise exception, just log warning
        self.invoker.reset_environment()


class TestTerminalInvokerIntegration(unittest.TestCase):
    """Integration tests for TerminalInvoker"""

    def setUp(self):
        """Set up test fixtures"""
        self.invoker = TerminalInvoker()

    @patch('subprocess.run')
    def test_full_workflow(self, mock_run):
        """Test full workflow: setup environment and execute command"""
        # Mock successful command execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create compiler info
        compiler = CompilerInfo(
            compiler_type="msvc",
            version="19.40.0",
            path="/path/to/cl.exe",
            architecture="x64"
        )

        # Setup environment (will be mocked)
        with patch.object(self.invoker, '_find_vcvarsall') as mock_find:
            mock_find.return_value = None

            with patch.object(self.invoker, 'execute_batch_file') as mock_batch:
                mock_batch.return_value = CommandResult(
                    exit_code=0,
                    stdout="",
                    stderr=""
                )

                # Setup environment
                env = self.invoker.setup_environment(compiler)

                # Execute command
                result = self.invoker.execute_command("echo test")

                # Verify
                self.assertTrue(result.success)
                self.assertEqual(result.stdout, "test output")


if __name__ == '__main__':
    unittest.main()
