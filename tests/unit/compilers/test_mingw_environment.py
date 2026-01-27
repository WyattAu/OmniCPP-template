"""
Unit tests for MinGW Environment Setup

This module provides comprehensive unit tests for MinGWEnvironment class,
including environment setup, restoration, and validation.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from scripts.python.compilers.mingw_environment import (
    MinGWEnvironment,
    MinGWEnvironmentConfig,
    MSYS2Environment,
    EnvironmentValidationResult
)
from scripts.python.compilers.terminal_invoker import TerminalInvoker, CommandResult


class TestMinGWEnvironmentConfig(unittest.TestCase):
    """Test cases for MinGWEnvironmentConfig"""

    def test_default_config(self):
        """Test default configuration values"""
        config = MinGWEnvironmentConfig()
        
        self.assertEqual(config.environment, MSYS2Environment.UCRT64)
        self.assertIsNone(config.msys2_path)
        self.assertEqual(config.architecture, "x64")
        self.assertTrue(config.set_pkg_config)
        self.assertTrue(config.set_aclocal)

    def test_custom_config(self):
        """Test custom configuration values"""
        config = MinGWEnvironmentConfig(
            environment=MSYS2Environment.MINGW64,
            msys2_path=r"C:\msys64",
            architecture="x64",
            set_pkg_config=False,
            set_aclocal=False
        )
        
        self.assertEqual(config.environment, MSYS2Environment.MINGW64)
        self.assertEqual(config.msys2_path, r"C:\msys64")
        self.assertEqual(config.architecture, "x64")
        self.assertFalse(config.set_pkg_config)
        self.assertFalse(config.set_aclocal)


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
            missing_variables=["PATH", "MSYSTEM"],
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


class TestMinGWEnvironment(unittest.TestCase):
    """Test cases for MinGWEnvironment"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_logger = Mock()
        self.mock_terminal_invoker = Mock(spec=TerminalInvoker)
        
        self.env = MinGWEnvironment(
            terminal_invoker=self.mock_terminal_invoker,
            logger=self.mock_logger
        )

    def test_initialization(self):
        """Test MinGWEnvironment initialization"""
        self.assertIsNotNone(self.env._logger)
        self.assertIsNotNone(self.env._terminal_invoker)
        self.assertEqual(self.env._original_environment, {})
        self.assertEqual(self.env._current_environment, {})
        self.assertFalse(self.env._is_setup)
        self.assertIsNone(self.env._msys2_path)
        self.assertIsNone(self.env._current_environment_type)

    def test_setup_with_valid_config(self):
        """Test setup with valid configuration"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            result = self.env.setup(config)

            # Verify setup was called
            self.assertTrue(self.env._is_setup)
            self.assertEqual(self.env._msys2_path, r"C:\msys64")
            self.assertEqual(self.env._current_environment_type, MSYS2Environment.UCRT64)
            self.assertIsInstance(result, dict)

    def test_setup_with_auto_detect_msys2(self):
        """Test setup with auto-detection of MSYS2 path"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.MINGW64,
                msys2_path=None,  # Auto-detect
                architecture="x64"
            )

            result = self.env.setup(config)

            # Verify setup was called
            self.assertTrue(self.env._is_setup)
            self.assertEqual(self.env._msys2_path, r"C:\msys64")
            self.assertEqual(self.env._current_environment_type, MSYS2Environment.MINGW64)

    def test_setup_with_invalid_msys2_path(self):
        """Test setup with invalid MSYS2 path"""
        # Mock MSYS2 path detection to return None
        with patch.object(self.env, '_find_msys2_path', return_value=None):
            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\invalid\path",
                architecture="x64"
            )

            # Should raise RuntimeError
            with self.assertRaises(RuntimeError) as context:
                self.env.setup(config)

            self.assertIn("MSYS2 installation not found", str(context.exception))

    def test_setup_with_invalid_environment_type(self):
        """Test setup with invalid environment type"""
        config = MinGWEnvironmentConfig(
            environment="INVALID_ENV",  # type: ignore - Invalid type
            msys2_path=r"C:\msys64",
            architecture="x64"
        )

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env.setup(config)

        self.assertIn("Invalid environment type", str(context.exception))

    def test_setup_with_invalid_architecture(self):
        """Test setup with invalid architecture"""
        config = MinGWEnvironmentConfig(
            environment=MSYS2Environment.UCRT64,
            msys2_path=r"C:\msys64",
            architecture="invalid_arch"  # Invalid architecture
        )

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env.setup(config)

        self.assertIn("Invalid architecture", str(context.exception))

    def test_setup_msys2_ucrt64(self):
        """Test setup_msys2 with UCRT64 environment"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            # Verify environment variables were set
            self.assertTrue(self.env._is_setup)
            self.assertEqual(os.environ.get("MSYSTEM"), "UCRT64")
            self.assertEqual(os.environ.get("MINGW_PREFIX"), "/ucrt64")
            self.assertEqual(os.environ.get("MINGW_CHOST"), "x86_64-w64-mingw32")
            self.assertEqual(os.environ.get("MSYS2_PATH"), r"C:\msys64")
            self.assertEqual(os.environ.get("MINGW_HOME"), r"C:\msys64")

    def test_setup_msys2_mingw64(self):
        """Test setup_msys2 with MINGW64 environment"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.MINGW64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            # Verify environment variables were set
            self.assertEqual(os.environ.get("MSYSTEM"), "MINGW64")
            self.assertEqual(os.environ.get("MINGW_PREFIX"), "/mingw64")
            self.assertEqual(os.environ.get("MINGW_CHOST"), "x86_64-w64-mingw32")

    def test_setup_msys2_mingw32(self):
        """Test setup_msys2 with MINGW32 environment"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.MINGW32,
                msys2_path=r"C:\msys64",
                architecture="x86"
            )

            # Verify environment variables were set
            self.assertEqual(os.environ.get("MSYSTEM"), "MINGW32")
            self.assertEqual(os.environ.get("MINGW_PREFIX"), "/mingw32")
            self.assertEqual(os.environ.get("MINGW_CHOST"), "i686-w64-mingw32")

    def test_setup_msys2_msys(self):
        """Test setup_msys2 with MSYS environment"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.MSYS,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            # Verify environment variables were set
            self.assertEqual(os.environ.get("MSYSTEM"), "MSYS")
            self.assertEqual(os.environ.get("MINGW_PREFIX"), "/usr")
            self.assertEqual(os.environ.get("MINGW_CHOST"), "x86_64-pc-msys")

    def test_setup_msys2_clang64(self):
        """Test setup_msys2 with CLANG64 environment"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.CLANG64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            # Verify environment variables were set
            self.assertEqual(os.environ.get("MSYSTEM"), "CLANG64")
            self.assertEqual(os.environ.get("MINGW_PREFIX"), "/clang64")
            self.assertEqual(os.environ.get("MINGW_CHOST"), "x86_64-w64-mingw32")

    def test_setup_msys2_without_pkg_config(self):
        """Test setup_msys2 without PKG_CONFIG_PATH"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64",
                set_pkg_config=False
            )

            # Verify PKG_CONFIG_PATH was set
            self.assertIsNotNone(os.environ.get("PKG_CONFIG_PATH"))

    def test_setup_msys2_without_aclocal(self):
        """Test setup_msys2 without ACLOCAL_PATH"""
        # Mock MSYS2 path detection
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            # Mock environment capture
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            result = self.env.setup_msys2(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64",
                set_aclocal=False
            )

            # Verify ACLOCAL_PATH was set
            self.assertIsNotNone(os.environ.get("ACLOCAL_PATH"))

    def test_get_environment_variables(self):
        """Test get_environment_variables"""
        # Setup environment first
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "UCRT64",
                "MINGW_PREFIX": "/ucrt64"
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            self.env.setup(config)

            # Get environment variables
            env_vars = self.env.get_environment_variables()

            # Verify environment variables
            self.assertIsInstance(env_vars, dict)
            self.assertIn("MSYSTEM", env_vars)
            self.assertIn("MINGW_PREFIX", env_vars)

    def test_get_environment_variables_without_setup(self):
        """Test get_environment_variables without setup"""
        # Should raise RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.env.get_environment_variables()

        self.assertIn("Environment has not been setup", str(context.exception))

    def test_restore_environment(self):
        """Test restore_environment"""
        # Setup environment first
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": os.environ.get("PATH", ""),
                "MSYSTEM": "",
                "MINGW_PREFIX": ""
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            self.env.setup(config)

            # Restore environment
            self.env.restore_environment()

            # Verify environment was restored
            self.assertFalse(self.env._is_setup)
            self.mock_terminal_invoker.restore_environment.assert_called_once()

    def test_restore_environment_without_setup(self):
        """Test restore_environment without setup"""
        # Should not raise error, just log warning
        self.env.restore_environment()

        # Verify environment was not restored
        self.assertFalse(self.env._is_setup)

    def test_validate_environment_success(self):
        """Test validate_environment with valid environment"""
        # Setup environment first
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": r"C:\msys64\ucrt64\bin;C:\msys64\usr\bin",
                "MSYSTEM": "UCRT64",
                "MINGW_PREFIX": "/ucrt64",
                "MINGW_CHOST": "x86_64-w64-mingw32",
                "MSYS2_PATH": r"C:\msys64",
                "MINGW_HOME": r"C:\msys64"
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            self.env.setup(config)

            # Validate environment
            result = self.env.validate_environment()

            # Verify validation result
            self.assertIsInstance(result, EnvironmentValidationResult)
            self.assertTrue(result.is_valid)
            self.assertEqual(len(result.errors), 0)

    def test_validate_environment_missing_required_vars(self):
        """Test validate_environment with missing required variables"""
        # Setup environment first
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": r"C:\msys64\ucrt64\bin;C:\msys64\usr\bin",
                "MSYSTEM": "",  # Missing
                "MINGW_PREFIX": ""  # Missing
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            self.env.setup(config)

            # Validate environment
            result = self.env.validate_environment()

            # Verify validation result
            self.assertFalse(result.is_valid)
            self.assertIn("MSYSTEM", result.missing_variables)
            self.assertIn("MINGW_PREFIX", result.missing_variables)

    def test_validate_environment_invalid_paths(self):
        """Test validate_environment with invalid paths"""
        # Setup environment first
        with patch.object(self.env, '_find_msys2_path', return_value=r"C:\msys64"):
            self.mock_terminal_invoker.capture_environment.return_value = {
                "PATH": r"C:\invalid\path;C:\msys64\ucrt64\bin",
                "MSYSTEM": "UCRT64",
                "MINGW_PREFIX": "/ucrt64"
            }

            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture="x64"
            )

            self.env.setup(config)

            # Validate environment
            result = self.env.validate_environment()

            # Verify validation result
            self.assertTrue(len(result.invalid_paths) > 0)
            self.assertTrue(len(result.warnings) > 0)

    def test_find_msys2_path_with_provided_path(self):
        """Test _find_msys2_path with provided path"""
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            result = self.env._find_msys2_path(r"C:\custom\msys64")

            # Verify path was returned
            self.assertEqual(result, r"C:\custom\msys64")

    def test_find_msys2_path_with_invalid_provided_path(self):
        """Test _find_msys2_path with invalid provided path"""
        # Mock os.path.exists to return False
        with patch('os.path.exists', return_value=False):
            result = self.env._find_msys2_path(r"C:\invalid\path")

            # Verify None was returned
            self.assertIsNone(result)

    def test_find_msys2_path_auto_detect(self):
        """Test _find_msys2_path with auto-detection"""
        # Mock os.path.exists to return True for C:\msys64
        def exists_side_effect(path):
            return path == r"C:\msys64" or path == os.path.join(r"C:\msys64", "usr", "bin")

        with patch('os.path.exists', side_effect=exists_side_effect):
            result = self.env._find_msys2_path(None)

            # Verify path was found
            self.assertEqual(result, r"C:\msys64")

    def test_find_msys2_path_not_found(self):
        """Test _find_msys2_path when not found"""
        # Mock os.path.exists to return False
        with patch('os.path.exists', return_value=False):
            result = self.env._find_msys2_path(None)

            # Verify None was returned
            self.assertIsNone(result)

    def test_validate_config_valid(self):
        """Test _validate_config with valid configuration"""
        config = MinGWEnvironmentConfig(
            environment=MSYS2Environment.UCRT64,
            msys2_path=r"C:\msys64",
            architecture="x64"
        )

        # Should not raise error
        self.env._validate_config(config)

    def test_validate_config_invalid_environment(self):
        """Test _validate_config with invalid environment type"""
        config = MinGWEnvironmentConfig(
            environment="INVALID_ENV",  # Invalid type
            msys2_path=r"C:\msys64",
            architecture="x64"
        )

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env._validate_config(config)

        self.assertIn("Invalid environment type", str(context.exception))

    def test_validate_config_invalid_architecture(self):
        """Test _validate_config with invalid architecture"""
        config = MinGWEnvironmentConfig(
            environment=MSYS2Environment.UCRT64,
            msys2_path=r"C:\msys64",
            architecture="invalid_arch"  # Invalid architecture
        )

        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.env._validate_config(config)

        self.assertIn("Invalid architecture", str(context.exception))

    def test_validate_config_valid_architectures(self):
        """Test _validate_config with all valid architectures"""
        valid_architectures = ["x64", "x86", "arm", "arm64"]

        for arch in valid_architectures:
            config = MinGWEnvironmentConfig(
                environment=MSYS2Environment.UCRT64,
                msys2_path=r"C:\msys64",
                architecture=arch
            )

            # Should not raise error
            self.env._validate_config(config)

    def test_environment_prefix_map(self):
        """Test ENVIRONMENT_PREFIX_MAP"""
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_PREFIX_MAP[MSYS2Environment.UCRT64],
            "/ucrt64"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_PREFIX_MAP[MSYS2Environment.MINGW64],
            "/mingw64"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_PREFIX_MAP[MSYS2Environment.MINGW32],
            "/mingw32"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_PREFIX_MAP[MSYS2Environment.MSYS],
            "/usr"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_PREFIX_MAP[MSYS2Environment.CLANG64],
            "/clang64"
        )

    def test_environment_chost_map(self):
        """Test ENVIRONMENT_CHOST_MAP"""
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_CHOST_MAP[MSYS2Environment.UCRT64],
            "x86_64-w64-mingw32"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_CHOST_MAP[MSYS2Environment.MINGW64],
            "x86_64-w64-mingw32"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_CHOST_MAP[MSYS2Environment.MINGW32],
            "i686-w64-mingw32"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_CHOST_MAP[MSYS2Environment.MSYS],
            "x86_64-pc-msys"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_CHOST_MAP[MSYS2Environment.CLANG64],
            "x86_64-w64-mingw32"
        )

    def test_environment_arch_map(self):
        """Test ENVIRONMENT_ARCH_MAP"""
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_ARCH_MAP[MSYS2Environment.UCRT64],
            "x64"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_ARCH_MAP[MSYS2Environment.MINGW64],
            "x64"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_ARCH_MAP[MSYS2Environment.MINGW32],
            "x86"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_ARCH_MAP[MSYS2Environment.MSYS],
            "x64"
        )
        self.assertEqual(
            MinGWEnvironment.ENVIRONMENT_ARCH_MAP[MSYS2Environment.CLANG64],
            "x64"
        )

    def test_required_env_vars(self):
        """Test REQUIRED_ENV_VARS"""
        self.assertIn("PATH", MinGWEnvironment.REQUIRED_ENV_VARS)
        self.assertIn("MSYSTEM", MinGWEnvironment.REQUIRED_ENV_VARS)
        self.assertIn("MINGW_PREFIX", MinGWEnvironment.REQUIRED_ENV_VARS)

    def test_optional_env_vars(self):
        """Test OPTIONAL_ENV_VARS"""
        self.assertIn("MINGW_CHOST", MinGWEnvironment.OPTIONAL_ENV_VARS)
        self.assertIn("MINGW_HOME", MinGWEnvironment.OPTIONAL_ENV_VARS)
        self.assertIn("PKG_CONFIG_PATH", MinGWEnvironment.OPTIONAL_ENV_VARS)
        self.assertIn("ACLOCAL_PATH", MinGWEnvironment.OPTIONAL_ENV_VARS)
        self.assertIn("MSYS2_PATH", MinGWEnvironment.OPTIONAL_ENV_VARS)

    def test_environment_validation_result_to_dict(self):
        """Test EnvironmentValidationResult.to_dict"""
        result = EnvironmentValidationResult(
            is_valid=True,
            errors=["error1"],
            warnings=["warning1"],
            missing_variables=["var1"],
            invalid_paths=["path1"]
        )

        result_dict = result.to_dict()

        self.assertEqual(result_dict["is_valid"], True)
        self.assertEqual(result_dict["errors"], ["error1"])
        self.assertEqual(result_dict["warnings"], ["warning1"])
        self.assertEqual(result_dict["missing_variables"], ["var1"])
        self.assertEqual(result_dict["invalid_paths"], ["path1"])

    def test_msys2_environment_enum(self):
        """Test MSYS2Environment enum"""
        self.assertEqual(MSYS2Environment.UCRT64.value, "UCRT64")
        self.assertEqual(MSYS2Environment.MINGW64.value, "MINGW64")
        self.assertEqual(MSYS2Environment.MINGW32.value, "MINGW32")
        self.assertEqual(MSYS2Environment.MSYS.value, "MSYS")
        self.assertEqual(MSYS2Environment.CLANG64.value, "CLANG64")


if __name__ == '__main__':
    unittest.main()
