"""
Unit tests for MSVC Environment Setup

This module provides comprehensive unit tests for MSVC environment setup,
including vcvarsall.bat invocation, environment variable management, and validation.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from scripts.python.compilers.msvc_environment import (
    MSVCEnvironment,
    MSVCEnvironmentConfig,
    EnvironmentValidationResult
)
from scripts.python.compilers.msvc_architecture import MSVCArchitecture
from scripts.python.compilers.terminal_invoker import (
    TerminalInvoker,
    CommandResult
)


class TestMSVCEnvironmentConfig(unittest.TestCase):
    """Test cases for MSVCEnvironmentConfig"""

    def test_default_config(self):
        """Test default configuration values"""
        config = MSVCEnvironmentConfig()
        
        self.assertEqual(config.architecture, MSVCArchitecture.X64)
        self.assertEqual(config.platform_type, "desktop")
        self.assertFalse(config.spectre_mitigation)
        self.assertIsNone(config.windows_sdk_version)
        self.assertIsNone(config.vc_install_path)

    def test_custom_config(self):
        """Test custom configuration values"""
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X86,
            platform_type="uwp",
            spectre_mitigation=True,
            windows_sdk_version="10.0.22621",
            vc_install_path=r"C:\VS2022"
        )
        
        self.assertEqual(config.architecture, MSVCArchitecture.X86)
        self.assertEqual(config.platform_type, "uwp")
        self.assertTrue(config.spectre_mitigation)
        self.assertEqual(config.windows_sdk_version, "10.0.22621")
        self.assertEqual(config.vc_install_path, r"C:\VS2022")


class TestEnvironmentValidationResult(unittest.TestCase):
    """Test cases for EnvironmentValidationResult"""

    def test_valid_result(self):
        """Test valid validation result"""
        result = EnvironmentValidationResult(is_valid=True)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])
        self.assertEqual(result.missing_variables, [])
        self.assertEqual(result.invalid_paths, [])

    def test_invalid_result(self):
        """Test invalid validation result"""
        result = EnvironmentValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            missing_variables=["PATH", "INCLUDE"],
            invalid_paths=["C:\\invalid\\path"]
        )
        
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(len(result.warnings), 1)
        self.assertEqual(len(result.missing_variables), 2)
        self.assertEqual(len(result.invalid_paths), 1)

    def test_to_dict(self):
        """Test conversion to dictionary"""
        result = EnvironmentValidationResult(
            is_valid=True,
            errors=["Error"],
            warnings=["Warning"],
            missing_variables=["VAR"],
            invalid_paths=["path"]
        )
        
        result_dict = result.to_dict()
        
        self.assertIsInstance(result_dict, dict)
        self.assertTrue(result_dict["is_valid"])
        self.assertEqual(result_dict["errors"], ["Error"])
        self.assertEqual(result_dict["warnings"], ["Warning"])
        self.assertEqual(result_dict["missing_variables"], ["VAR"])
        self.assertEqual(result_dict["invalid_paths"], ["path"])


class TestMSVCEnvironment(unittest.TestCase):
    """Test cases for MSVCEnvironment"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_logger = Mock()
        self.mock_terminal_invoker = Mock(spec=TerminalInvoker)
        
        self.env = MSVCEnvironment(
            terminal_invoker=self.mock_terminal_invoker,
            logger=self.mock_logger
        )

    def test_initialization(self):
        """Test MSVCEnvironment initialization"""
        self.assertIsNotNone(self.env._logger)
        self.assertIsNotNone(self.env._terminal_invoker)
        self.assertIsNotNone(self.env._arch_mapper)
        self.assertEqual(self.env._original_environment, {})
        self.assertEqual(self.env._current_environment, {})
        self.assertFalse(self.env._is_setup)
        self.assertIsNone(self.env._vcvarsall_path)

    def test_setup_with_valid_config(self):
        """Test environment setup with valid configuration"""
        # Mock terminal invoker methods
        self.mock_terminal_invoker.capture_environment.return_value = {
            "PATH": "original_path",
            "INCLUDE": "original_include"
        }
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr="",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            config = MSVCEnvironmentConfig(
                architecture=MSVCArchitecture.X64
            )
            
            result = self.env.setup(config)
            
            # Verify setup was called
            self.assertTrue(self.env._is_setup)
            self.assertIsNotNone(self.env._vcvarsall_path)
            self.mock_terminal_invoker.capture_environment.assert_called()
            mock_find.assert_called_once()

    def test_setup_with_invalid_config(self):
        """Test environment setup with invalid configuration"""
        # Create invalid config with wrong platform type
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X64,
            platform_type="invalid_platform"
        )
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env.setup(config)
        
        self.assertIn("Invalid platform type", str(context.exception))

    def test_setup_with_invalid_sdk_version(self):
        """Test environment setup with invalid SDK version"""
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X64,
            windows_sdk_version="invalid_version"
        )
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env.setup(config)
        
        self.assertIn("Invalid Windows SDK version format", str(context.exception))

    def test_setup_vcvarsall_not_found(self):
        """Test setup when vcvarsall.bat is not found"""
        # Mock vcvarsall.bat not found
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = None
            
            config = MSVCEnvironmentConfig(
                architecture=MSVCArchitecture.X64
            )
            
            # Should raise RuntimeError
            with self.assertRaises(RuntimeError) as context:
                self.env.setup(config)
            
            self.assertIn("vcvarsall.bat not found", str(context.exception))

    def test_setup_vcvarsall_execution_failure(self):
        """Test setup when vcvarsall.bat execution fails"""
        # Mock terminal invoker methods
        self.mock_terminal_invoker.capture_environment.return_value = {}
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=1,
            stdout="",
            stderr="Error executing vcvarsall.bat",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            config = MSVCEnvironmentConfig(
                architecture=MSVCArchitecture.X64
            )
            
            # Should raise RuntimeError
            with self.assertRaises(RuntimeError) as context:
                self.env.setup(config)
            
            self.assertIn("vcvarsall.bat execution failed", str(context.exception))

    def test_setup_vcvarsall(self):
        """Test vcvarsall.bat invocation"""
        # Mock terminal invoker
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr="",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            result = self.env.setup_vcvarsall(
                architecture=MSVCArchitecture.X64,
                platform_type="desktop",
                spectre_mitigation=False,
                windows_sdk_version=None
            )
            
            # Verify vcvarsall.bat was called with correct arguments
            self.mock_terminal_invoker.execute_batch_file.assert_called_once()
            call_args = self.mock_terminal_invoker.execute_batch_file.call_args
            
            # Check that vcvarsall.bat path was passed
            self.assertEqual(
                call_args[0][0],
                r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            )
            
            # Check that architecture argument was passed
            self.assertIn("amd64", call_args[0][1])

    def test_setup_vcvarsall_with_spectre(self):
        """Test vcvarsall.bat invocation with Spectre mitigation"""
        # Mock terminal invoker
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr="",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            result = self.env.setup_vcvarsall(
                architecture=MSVCArchitecture.X64,
                platform_type="desktop",
                spectre_mitigation=True,
                windows_sdk_version=None
            )
            
            # Verify spectre argument was passed
            call_args = self.mock_terminal_invoker.execute_batch_file.call_args
            self.assertIn("spectre", call_args[0][1])

    def test_setup_vcvarsall_with_uwp(self):
        """Test vcvarsall.bat invocation with UWP platform"""
        # Mock terminal invoker
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr="",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            result = self.env.setup_vcvarsall(
                architecture=MSVCArchitecture.X64,
                platform_type="uwp",
                spectre_mitigation=False,
                windows_sdk_version=None
            )
            
            # Verify uwp argument was passed
            call_args = self.mock_terminal_invoker.execute_batch_file.call_args
            self.assertIn("uwp", call_args[0][1])

    def test_setup_vcvarsall_with_sdk_version(self):
        """Test vcvarsall.bat invocation with Windows SDK version"""
        # Mock terminal invoker
        self.mock_terminal_invoker.execute_batch_file.return_value = CommandResult(
            exit_code=0,
            stdout="",
            stderr="",
            environment={},
            execution_time=1.0
        )

        # Mock vcvarsall.bat path
        with patch.object(self.env, '_find_vcvarsall') as mock_find:
            mock_find.return_value = r"C:\VS2022\VC\Auxiliary\Build\vcvarsall.bat"
            
            result = self.env.setup_vcvarsall(
                architecture=MSVCArchitecture.X64,
                platform_type="desktop",
                spectre_mitigation=False,
                windows_sdk_version="10.0.22621"
            )
            
            # Verify SDK version argument was passed
            call_args = self.mock_terminal_invoker.execute_batch_file.call_args
            sdk_arg = [arg for arg in call_args[0][1] if "vcvars_ver" in arg]
            self.assertTrue(len(sdk_arg) > 0)

    def test_get_environment_variables(self):
        """Test getting environment variables"""
        # Setup environment
        self.env._is_setup = True
        self.env._current_environment = {
            "PATH": "test_path",
            "INCLUDE": "test_include",
            "LIB": "test_lib"
        }
        
        # Get environment variables
        result = self.env.get_environment_variables()
        
        # Verify result
        self.assertEqual(result["PATH"], "test_path")
        self.assertEqual(result["INCLUDE"], "test_include")
        self.assertEqual(result["LIB"], "test_lib")

    def test_get_environment_variables_not_setup(self):
        """Test getting environment variables when not setup"""
        self.env._is_setup = False
        
        # Should raise RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.env.get_environment_variables()
        
        self.assertIn("Environment has not been setup", str(context.exception))

    def test_restore_environment(self):
        """Test restoring environment"""
        # Setup environment
        self.env._is_setup = True
        self.env._original_environment = {
            "PATH": "original_path",
            "INCLUDE": "original_include"
        }
        
        # Restore environment
        self.env.restore_environment()
        
        # Verify restore was called
        self.mock_terminal_invoker.restore_environment.assert_called_once_with(
            self.env._original_environment
        )
        self.assertFalse(self.env._is_setup)

    def test_restore_environment_not_setup(self):
        """Test restoring environment when not setup"""
        self.env._is_setup = False
        
        # Should not raise error, just log warning
        self.env.restore_environment()
        
        # Verify restore was not called
        self.mock_terminal_invoker.restore_environment.assert_not_called()

    def test_validate_environment_valid(self):
        """Test environment validation with valid environment"""
        # Mock environment
        self.mock_terminal_invoker.capture_environment.return_value = {
            "PATH": r"C:\VS2022\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64",
            "INCLUDE": r"C:\Windows Kits\10\Include\10.0.22621.0\ucrt",
            "LIB": r"C:\Windows Kits\10\Lib\10.0.22621.0\ucrt\x64",
            "LIBPATH": r"C:\Windows Kits\10\References\10.0.22621.0",
            "WindowsSDKVersion": "10.0.22621.0",
            "VCINSTALLDIR": r"C:\VS2022\VC",
            "VSINSTALLDIR": r"C:\VS2022"
        }

        # Mock os.path.exists to return True for all paths
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            
            # Validate environment
            result = self.env.validate_environment()
            
            # Verify result
            self.assertTrue(result.is_valid)
            self.assertEqual(len(result.errors), 0)
            self.assertEqual(len(result.missing_variables), 0)

    def test_validate_environment_missing_required_vars(self):
        """Test environment validation with missing required variables"""
        # Mock environment with missing variables
        self.mock_terminal_invoker.capture_environment.return_value = {
            "PATH": "test_path"
        }

        # Validate environment
        result = self.env.validate_environment()
        
        # Verify result
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.missing_variables), 0)
        self.assertIn("INCLUDE", result.missing_variables)
        self.assertIn("LIB", result.missing_variables)

    def test_validate_environment_invalid_paths(self):
        """Test environment validation with invalid paths"""
        # Mock environment with invalid paths
        self.mock_terminal_invoker.capture_environment.return_value = {
            "PATH": "test_path",
            "INCLUDE": r"C:\invalid\path;C:\Windows Kits\10\Include",
            "LIB": r"C:\invalid\lib",
            "LIBPATH": "test_libpath",
            "WindowsSDKVersion": "10.0.22621.0"
        }

        # Validate environment
        result = self.env.validate_environment()
        
        # Verify result
        self.assertGreater(len(result.invalid_paths), 0)
        self.assertGreater(len(result.warnings), 0)

    def test_validate_environment_cl_not_in_path(self):
        """Test environment validation when cl.exe is not in PATH"""
        # Mock environment without cl.exe in PATH
        self.mock_terminal_invoker.capture_environment.return_value = {
            "PATH": r"C:\some\other\path",
            "INCLUDE": "test_include",
            "LIB": "test_lib",
            "LIBPATH": "test_libpath",
            "WindowsSDKVersion": "10.0.22621.0"
        }

        # Validate environment
        result = self.env.validate_environment()
        
        # Verify result
        self.assertFalse(result.is_valid)
        self.assertIn("cl.exe not found in PATH", result.errors)

    def test_find_vcvarsall_with_install_path(self):
        """Test finding vcvarsall.bat with installation path"""
        # Mock os.path.exists to return True for our test path
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = lambda path: path.endswith("vcvarsall.bat")
            
            result = self.env._find_vcvarsall(r"C:\VS2022")
            
            # Verify result
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith("vcvarsall.bat"))

    def test_find_vcvarsall_without_install_path(self):
        """Test finding vcvarsall.bat without installation path"""
        # Mock os.path.exists to return True for common paths
        with patch('os.path.exists') as mock_exists:
            def exists_side_effect(path):
                return "vcvarsall.bat" in path and "2022" in path
            
            mock_exists.side_effect = exists_side_effect
            
            result = self.env._find_vcvarsall(None)
            
            # Verify result
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith("vcvarsall.bat"))

    def test_find_vcvarsall_not_found(self):
        """Test finding vcvarsall.bat when not found"""
        # Mock os.path.exists to return False
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            result = self.env._find_vcvarsall(None)
            
            # Verify result
            self.assertIsNone(result)

    def test_build_vcvarsall_args_x64(self):
        """Test building vcvarsall.bat arguments for x64"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X64,
            "desktop",
            False,
            None
        )
        
        self.assertIn("amd64", args)
        self.assertNotIn("uwp", args)
        self.assertNotIn("store", args)
        self.assertNotIn("spectre", args)

    def test_build_vcvarsall_args_x86(self):
        """Test building vcvarsall.bat arguments for x86"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X86,
            "desktop",
            False,
            None
        )
        
        self.assertIn("x86", args)

    def test_build_vcvarsall_args_cross_compilation(self):
        """Test building vcvarsall.bat arguments for cross-compilation"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X86_AMD64,
            "desktop",
            False,
            None
        )
        
        self.assertIn("x86_amd64", args)

    def test_build_vcvarsall_args_with_spectre(self):
        """Test building vcvarsall.bat arguments with Spectre mitigation"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X64,
            "desktop",
            True,
            None
        )
        
        self.assertIn("spectre", args)

    def test_build_vcvarsall_args_with_uwp(self):
        """Test building vcvarsall.bat arguments with UWP platform"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X64,
            "uwp",
            False,
            None
        )
        
        self.assertIn("uwp", args)

    def test_build_vcvarsall_args_with_store(self):
        """Test building vcvarsall.bat arguments with Store platform"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X64,
            "store",
            False,
            None
        )
        
        self.assertIn("store", args)

    def test_build_vcvarsall_args_with_sdk_version(self):
        """Test building vcvarsall.bat arguments with SDK version"""
        args = self.env._build_vcvarsall_args(
            MSVCArchitecture.X64,
            "desktop",
            False,
            "10.0.22621"
        )
        
        sdk_arg = [arg for arg in args if "vcvars_ver" in arg]
        self.assertTrue(len(sdk_arg) > 0)

    def test_set_additional_environment_variables(self):
        """Test setting additional environment variables"""
        # Mock os.environ
        with patch.dict(os.environ, {}, clear=True):
            self.env._set_additional_environment_variables(
                MSVCArchitecture.X64,
                "desktop",
                True,
                "10.0.22621"
            )
            
            # Verify variables were set
            self.assertEqual(os.environ.get("SPECTRE_MITIGATION"), "1")
            self.assertEqual(os.environ.get("WindowsSDKVersion"), "10.0.22621")
            self.assertEqual(os.environ.get("VSCMD_ARG_app_plat"), "desktop")
            self.assertEqual(os.environ.get("VSCMD_ARG_HOST_ARCH"), "x64")
            self.assertEqual(os.environ.get("VSCMD_ARG_TGT_ARCH"), "x64")

    def test_validate_config_valid(self):
        """Test validating valid configuration"""
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X64,
            platform_type="desktop",
            spectre_mitigation=False,
            windows_sdk_version="10.0.22621"
        )
        
        # Should not raise
        try:
            self.env._validate_config(config)
        except ValueError:
            self.fail("Valid configuration raised ValueError")

    def test_validate_config_invalid_architecture(self):
        """Test validating configuration with invalid architecture"""
        config = MSVCEnvironmentConfig(
            architecture="invalid_arch",  # type: ignore
            platform_type="desktop"
        )
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env._validate_config(config)
        
        self.assertIn("Invalid architecture type", str(context.exception))

    def test_validate_config_invalid_platform(self):
        """Test validating configuration with invalid platform type"""
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X64,
            platform_type="invalid_platform"
        )
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env._validate_config(config)
        
        self.assertIn("Invalid platform type", str(context.exception))

    def test_validate_config_invalid_sdk_version(self):
        """Test validating configuration with invalid SDK version"""
        config = MSVCEnvironmentConfig(
            architecture=MSVCArchitecture.X64,
            windows_sdk_version="invalid_version"
        )
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env._validate_config(config)
        
        self.assertIn("Invalid Windows SDK version format", str(context.exception))


if __name__ == '__main__':
    unittest.main()
