"""
Unit tests for Compiler Detection System

Tests the unified compiler detection system that integrates all
previously implemented components.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys
import os
import logging
from typing import Dict, List, Optional, Any

# Add scripts/python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

# Import the system under test
from compilers.compiler_detection_system import (
    CompilerDetectionSystem,
    DetectionError,
    DetectionResult
)

# Import dependencies for mocking
from compilers.compiler_factory import CompilerFactory
from compilers.compiler_manager import CompilerManager
from compilers.compiler_terminal_mapper import (
    CompilerTerminalMapper,
    TerminalInfo,
    ITerminalDetector
)
from compilers.terminal_invoker import TerminalInvoker, CommandResult
from compilers.msvc_detector import (
    CompilerInfo as MSVCCompilerInfo,
    ValidationResult
)
from compilers.linux_cross_compiler import LinuxCrossCompiler
from compilers.wasm_cross_compiler import WASMCrossCompiler
from compilers.android_cross_compiler import AndroidCrossCompiler
from compilers.toolchain_detector import (
    ToolchainDetector,
    UnifiedToolchainInfo
)
from compilers.cmake_generator_selector import (
    CMakeGeneratorSelector,
    GeneratorSelectionResult
)


class TestDetectionError(unittest.TestCase):
    """Test DetectionError dataclass"""

    def test_detection_error_creation(self) -> None:
        """Test creating a DetectionError"""
        error = DetectionError(
            component="test_component",
            error_type="test_error",
            message="Test error message",
            details={"key": "value"},
            suggestion="Fix the issue"
        )
        
        self.assertEqual(error.component, "test_component")
        self.assertEqual(error.error_type, "test_error")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.details, {"key": "value"})
        self.assertEqual(error.suggestion, "Fix the issue")

    def test_detection_error_optional_fields(self) -> None:
        """Test DetectionError with optional fields"""
        error = DetectionError(
            component="test_component",
            error_type="test_error",
            message="Test error message"
        )
        
        self.assertIsNone(error.details)
        self.assertIsNone(error.suggestion)

    def test_detection_error_to_dict(self) -> None:
        """Test converting DetectionError to dictionary"""
        error = DetectionError(
            component="test_component",
            error_type="test_error",
            message="Test error message",
            details={"key": "value"},
            suggestion="Fix the issue"
        )
        
        result = error.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["component"], "test_component")
        self.assertEqual(result["error_type"], "test_error")
        self.assertEqual(result["message"], "Test error message")
        self.assertEqual(result["details"], {"key": "value"})
        self.assertEqual(result["suggestion"], "Fix the issue")


class TestDetectionResult(unittest.TestCase):
    """Test DetectionResult dataclass"""

    def test_detection_result_creation(self) -> None:
        """Test creating a DetectionResult"""
        result = DetectionResult(
            compilers={"msvc": []},
            terminals={"msvc": []},
            cross_compilers={},
            errors=[],
            warnings=[],
            success=True
        )
        
        self.assertEqual(result.compilers, {"msvc": []})
        self.assertEqual(result.terminals, {"msvc": []})
        self.assertEqual(result.cross_compilers, {})
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])
        self.assertTrue(result.success)

    def test_detection_result_defaults(self) -> None:
        """Test DetectionResult with default values"""
        result = DetectionResult()
        
        self.assertEqual(result.compilers, {})
        self.assertEqual(result.terminals, {})
        self.assertEqual(result.cross_compilers, {})
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])
        self.assertTrue(result.success)

    def test_detection_result_has_errors(self) -> None:
        """Test has_errors property"""
        result = DetectionResult()
        self.assertFalse(result.has_errors)
        
        result.errors.append(DetectionError(
            component="test",
            error_type="test",
            message="Test error"
        ))
        self.assertTrue(result.has_errors)

    def test_detection_result_has_warnings(self) -> None:
        """Test has_warnings property"""
        result = DetectionResult()
        self.assertFalse(result.has_warnings)
        
        result.warnings.append("Test warning")
        self.assertTrue(result.has_warnings)

    def test_detection_result_to_dict(self) -> None:
        """Test converting DetectionResult to dictionary"""
        # Create mock compiler info
        mock_compiler = Mock(spec=MSVCCompilerInfo)
        mock_compiler.to_dict.return_value = {
            "compiler_type": "msvc",
            "version": "19.0",
            "path": "C:/Program Files/..."
        }
        
        # Create mock terminal info
        mock_terminal = Mock(spec=TerminalInfo)
        mock_terminal.to_dict.return_value = {
            "name": "Developer Command Prompt",
            "terminal_id": "msvc_x64"
        }
        
        # Create mock toolchain info
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.to_dict.return_value = {
            "platform": "linux",
            "architecture": "x86_64-linux-gnu"
        }
        
        result = DetectionResult(
            compilers={"msvc": [mock_compiler]},
            terminals={"msvc": [mock_terminal]},
            cross_compilers={"linux_x86_64": mock_toolchain},
            errors=[],
            warnings=[],
            success=True
        )
        
        result_dict = result.to_dict()
        
        self.assertIsInstance(result_dict, dict)
        self.assertIn("compilers", result_dict)
        self.assertIn("terminals", result_dict)
        self.assertIn("cross_compilers", result_dict)
        self.assertIn("errors", result_dict)
        self.assertIn("warnings", result_dict)
        self.assertIn("success", result_dict)
        self.assertTrue(result_dict["success"])


class TestCompilerDetectionSystem(unittest.TestCase):
    """Test CompilerDetectionSystem class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Create mock terminal detector
        self.mock_terminal_detector = Mock(spec=ITerminalDetector)
        
        # Create system with mock terminal detector
        self.system = CompilerDetectionSystem(
            logger=self.logger,
            terminal_detector=self.mock_terminal_detector
        )

    def test_initialization(self) -> None:
        """Test system initialization"""
        self.assertIsNotNone(self.system._logger)
        self.assertIsNotNone(self.system._factory)
        self.assertIsNotNone(self.system._compiler_manager)
        self.assertIsNotNone(self.system._terminal_invoker)
        self.assertIsNotNone(self.system._mapper)
        self.assertIsNotNone(self.system._cross_compilers)
        self.assertIsNotNone(self.system._toolchain_detector)
        self.assertIsNotNone(self.system._cmake_selector)

    def test_initialization_without_terminal_detector(self) -> None:
        """Test system initialization without terminal detector"""
        system = CompilerDetectionSystem(logger=self.logger)
        
        self.assertIsNotNone(system._logger)
        self.assertIsNotNone(system._factory)
        self.assertIsNotNone(system._compiler_manager)
        self.assertIsNotNone(system._terminal_invoker)
        self.assertIsNone(system._mapper)

    def test_detect_all_success(self) -> None:
        """Test detect_all with successful detection"""
        # Mock compiler manager
        self.system._compiler_manager.detect_all = Mock(return_value={
            "msvc": [Mock(spec=MSVCCompilerInfo)],
            "mingw_gcc": []
        })
        
        # Mock terminal detector
        mock_terminal = Mock(spec=TerminalInfo)
        mock_terminal.type = Mock()
        mock_terminal.type.value = "msvc"
        self.mock_terminal_detector.detect = Mock(return_value=[mock_terminal])
        
        # Mock toolchain detector
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.platform = "linux"
        mock_toolchain.architecture = "x86_64-linux-gnu"
        
        mock_toolchain_result = Mock()
        mock_toolchain_result.success = True
        mock_toolchain_result.toolchains = [mock_toolchain]
        mock_toolchain_result.errors = []
        mock_toolchain_result.warnings = []
        
        self.system._toolchain_detector.detect = Mock(return_value=mock_toolchain_result)
        
        # Run detection
        result = self.system.detect_all()
        
        # Verify result
        self.assertIsInstance(result, DetectionResult)
        self.assertTrue(result.success)
        self.assertEqual(len(result.errors), 0)
        self.assertIn("msvc", result.compilers)
        self.assertIn("msvc", result.terminals)
        self.assertIn("linux_x86_64-linux-gnu", result.cross_compilers)

    def test_detect_all_with_errors(self) -> None:
        """Test detect_all with detection errors"""
        # Mock compiler manager to raise exception
        self.system._compiler_manager.detect_all = Mock(
            side_effect=Exception("Detection failed")
        )
        
        # Mock terminal detector
        self.mock_terminal_detector.detect = Mock(
            side_effect=Exception("Terminal detection failed")
        )
        
        # Mock toolchain detector
        mock_toolchain_result = Mock()
        mock_toolchain_result.success = False
        mock_toolchain_result.toolchains = []
        mock_toolchain_result.errors = ["Toolchain error"]
        mock_toolchain_result.warnings = []
        
        self.system._toolchain_detector.detect = Mock(return_value=mock_toolchain_result)
        
        # Run detection
        result = self.system.detect_all()
        
        # Verify result
        self.assertIsInstance(result, DetectionResult)
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
        self.assertEqual(result.compilers, {})
        self.assertEqual(result.terminals, {})

    def test_detect_compiler_found(self) -> None:
        """Test detect_compiler when compiler is found"""
        # Mock compiler info
        mock_compiler = Mock(spec=MSVCCompilerInfo)
        mock_compiler.compiler_type = Mock()
        mock_compiler.compiler_type.value = "msvc"
        mock_compiler.architecture = Mock()
        mock_compiler.architecture.value = "x64"
        mock_compiler.version = "19.0"
        
        # Mock compiler manager
        self.system._compiler_manager.get_compiler = Mock(return_value=mock_compiler)
        
        # Run detection
        result = self.system.detect_compiler("msvc", "x64")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.compiler_type.value, "msvc")
        self.assertEqual(result.architecture.value, "x64")
        self.assertEqual(result.version, "19.0")

    def test_detect_compiler_not_found(self) -> None:
        """Test detect_compiler when compiler is not found"""
        # Mock compiler manager
        self.system._compiler_manager.get_compiler = Mock(return_value=None)
        
        # Run detection
        result = self.system.detect_compiler("msvc", "x64")
        
        # Verify result
        self.assertIsNone(result)

    def test_detect_compiler_invalid_type(self) -> None:
        """Test detect_compiler with invalid compiler type"""
        # Mock compiler manager to raise ValueError
        self.system._compiler_manager.get_compiler = Mock(
            side_effect=ValueError("Invalid compiler type")
        )
        
        # Run detection and expect ValueError
        with self.assertRaises(ValueError):
            self.system.detect_compiler("invalid", "x64")

    def test_detect_cross_compiler_found(self) -> None:
        """Test detect_cross_compiler when cross-compiler is found"""
        # Mock toolchain info
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.platform = "linux"
        mock_toolchain.architecture = "x86_64-linux-gnu"
        
        # Mock toolchain detector
        self.system._toolchain_detector.detect_toolchain = Mock(
            return_value=mock_toolchain
        )
        
        # Run detection
        result = self.system.detect_cross_compiler("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.platform, "linux")
        self.assertEqual(result.architecture, "x86_64-linux-gnu")

    def test_detect_cross_compiler_not_found(self) -> None:
        """Test detect_cross_compiler when cross-compiler is not found"""
        # Mock toolchain detector
        self.system._toolchain_detector.detect_toolchain = Mock(return_value=None)
        
        # Run detection
        result = self.system.detect_cross_compiler("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsNone(result)

    def test_detect_cross_compiler_invalid_platform(self) -> None:
        """Test detect_cross_compiler with invalid platform"""
        # Mock toolchain detector to raise ValueError
        self.system._toolchain_detector.detect_toolchain = Mock(
            side_effect=ValueError("Invalid platform")
        )
        
        # Run detection and expect ValueError
        with self.assertRaises(ValueError):
            self.system.detect_cross_compiler("invalid", "x86_64")

    def test_get_recommended_compiler_found(self) -> None:
        """Test get_recommended_compiler when compiler is found"""
        # Mock compiler info
        mock_compiler = Mock(spec=MSVCCompilerInfo)
        mock_compiler.compiler_type = Mock()
        mock_compiler.compiler_type.value = "msvc"
        mock_compiler.architecture = Mock()
        mock_compiler.architecture.value = "x64"
        mock_compiler.version = "19.0"
        
        # Mock compiler manager
        self.system._compiler_manager.get_recommended_compiler = Mock(
            return_value=mock_compiler
        )
        
        # Run detection
        result = self.system.get_recommended_compiler("x64", "C++20")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.compiler_type.value, "msvc")
        self.assertEqual(result.architecture.value, "x64")

    def test_get_recommended_compiler_not_found(self) -> None:
        """Test get_recommended_compiler when compiler is not found"""
        # Mock compiler manager
        self.system._compiler_manager.get_recommended_compiler = Mock(
            return_value=None
        )
        
        # Run detection
        result = self.system.get_recommended_compiler("x64")
        
        # Verify result
        self.assertIsNone(result)

    def test_validate_system_success(self) -> None:
        """Test validate_system when system is valid"""
        # Mock compiler factory
        self.system._factory.get_available_compilers = Mock(
            return_value={"msvc": [Mock(spec=MSVCCompilerInfo)]}
        )
        
        # Mock compiler manager
        self.system._compiler_manager.get_all_compilers = Mock(
            return_value={"msvc": [Mock(spec=MSVCCompilerInfo)]}
        )
        
        # Mock terminal detector
        mock_terminal = Mock(spec=TerminalInfo)
        self.mock_terminal_detector.detect = Mock(return_value=[mock_terminal])
        
        # Mock toolchain detector
        mock_toolchain_result = Mock()
        mock_toolchain_result.success = True
        mock_toolchain_result.toolchains = [Mock(spec=UnifiedToolchainInfo)]
        self.system._toolchain_detector.detect = Mock(return_value=mock_toolchain_result)
        
        # Run validation
        result = self.system.validate_system()
        
        # Verify result
        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_system_with_errors(self) -> None:
        """Test validate_system when system has errors"""
        # Mock compiler factory to return empty
        self.system._factory.get_available_compilers = Mock(return_value={})
        
        # Mock compiler manager to return empty
        self.system._compiler_manager.get_all_compilers = Mock(return_value={})
        
        # Mock terminal detector to return empty
        self.mock_terminal_detector.detect = Mock(return_value=[])
        
        # Mock toolchain detector to return empty
        mock_toolchain_result = Mock()
        mock_toolchain_result.success = False
        mock_toolchain_result.toolchains = []
        self.system._toolchain_detector.detect = Mock(return_value=mock_toolchain_result)
        
        # Run validation
        result = self.system.validate_system()
        
        # Verify result
        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

    def test_get_terminal_found(self) -> None:
        """Test get_terminal when terminal is found"""
        # Mock terminal info
        mock_terminal = Mock(spec=TerminalInfo)
        mock_terminal.name = "Developer Command Prompt"
        mock_terminal.terminal_id = "msvc_x64"
        
        # Mock mapper
        self.system._mapper.get_preferred_terminal = Mock(return_value=mock_terminal)
        
        # Run detection
        result = self.system.get_terminal("msvc", "x64")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Developer Command Prompt")
        self.assertEqual(result.terminal_id, "msvc_x64")

    def test_get_terminal_not_found(self) -> None:
        """Test get_terminal when terminal is not found"""
        # Mock mapper
        self.system._mapper.get_preferred_terminal = Mock(return_value=None)
        
        # Run detection
        result = self.system.get_terminal("msvc", "x64")
        
        # Verify result
        self.assertIsNone(result)

    def test_get_terminal_without_mapper(self) -> None:
        """Test get_terminal when mapper is not available"""
        # Create system without terminal detector
        system = CompilerDetectionSystem(logger=self.logger)
        
        # Run detection
        result = system.get_terminal("msvc", "x64")
        
        # Verify result
        self.assertIsNone(result)

    def test_setup_environment_success(self) -> None:
        """Test setup_environment when setup succeeds"""
        # Mock compiler info
        mock_compiler = Mock(spec=MSVCCompilerInfo)
        mock_compiler.compiler_type = Mock()
        mock_compiler.compiler_type.value = "msvc"
        mock_compiler.version = "19.0"
        mock_compiler.path = "C:/Program Files/..."
        mock_compiler.architecture = Mock()
        mock_compiler.architecture.value = "x64"
        mock_compiler.metadata = {}
        
        # Mock compiler manager
        self.system._compiler_manager.get_compiler = Mock(return_value=mock_compiler)
        
        # Mock terminal invoker
        env = {"PATH": "C:/Program Files/..."}
        self.system._terminal_invoker.setup_environment = Mock(return_value=env)
        
        # Run setup
        result = self.system.setup_environment("msvc", "x64")
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertEqual(result, env)

    def test_setup_environment_compiler_not_found(self) -> None:
        """Test setup_environment when compiler is not found"""
        # Mock compiler manager
        self.system._compiler_manager.get_compiler = Mock(return_value=None)
        
        # Run setup and expect ValueError
        with self.assertRaises(ValueError):
            self.system.setup_environment("msvc", "x64")

    def test_setup_environment_setup_fails(self) -> None:
        """Test setup_environment when environment setup fails"""
        # Mock compiler info
        mock_compiler = Mock(spec=MSVCCompilerInfo)
        mock_compiler.compiler_type = Mock()
        mock_compiler.compiler_type.value = "msvc"
        mock_compiler.version = "19.0"
        mock_compiler.path = "C:/Program Files/..."
        mock_compiler.architecture = Mock()
        mock_compiler.architecture.value = "x64"
        mock_compiler.metadata = {}
        
        # Mock compiler manager
        self.system._compiler_manager.get_compiler = Mock(return_value=mock_compiler)
        
        # Mock terminal invoker to raise exception
        self.system._terminal_invoker.setup_environment = Mock(
            side_effect=Exception("Setup failed")
        )
        
        # Run setup and expect RuntimeError
        with self.assertRaises(RuntimeError):
            self.system.setup_environment("msvc", "x64")

    def test_execute_command_success(self) -> None:
        """Test execute_command when command succeeds"""
        # Mock command result
        mock_result = Mock(spec=CommandResult)
        mock_result.success = True
        mock_result.exit_code = 0
        mock_result.stdout = "Output"
        mock_result.stderr = ""
        mock_result.execution_time = 1.5
        
        # Mock terminal invoker
        self.system._terminal_invoker.execute_command = Mock(return_value=mock_result)
        
        # Run command
        result = self.system.execute_command("msvc", "x64", "echo test")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertEqual(result.exit_code, 0)

    def test_execute_command_failure(self) -> None:
        """Test execute_command when command fails"""
        # Mock command result
        mock_result = Mock(spec=CommandResult)
        mock_result.success = False
        mock_result.exit_code = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error"
        mock_result.execution_time = 0.5
        
        # Mock terminal invoker
        self.system._terminal_invoker.execute_command = Mock(return_value=mock_result)
        
        # Run command
        result = self.system.execute_command("msvc", "x64", "invalid_command")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertFalse(result.success)
        self.assertEqual(result.exit_code, 1)

    def test_execute_command_exception(self) -> None:
        """Test execute_command when exception occurs"""
        # Mock terminal invoker to raise exception
        self.system._terminal_invoker.execute_command = Mock(
            side_effect=Exception("Command failed")
        )
        
        # Run command
        result = self.system.execute_command("msvc", "x64", "test")
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.exit_code, -1)
        self.assertEqual(result.stderr, "Command failed")

    def test_setup_cross_compilation_success(self) -> None:
        """Test setup_cross_compilation when setup succeeds"""
        # Mock toolchain info
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.platform = "linux"
        mock_toolchain.architecture = "x86_64-linux-gnu"
        
        # Mock toolchain detector
        self.system._toolchain_detector.detect_toolchain = Mock(
            return_value=mock_toolchain
        )
        
        # Mock cross-compiler
        mock_cross_compiler = Mock()
        mock_cross_compiler.setup_environment = Mock(return_value={"CC": "gcc"})
        
        # Patch cross-compilers dict
        self.system._cross_compilers["linux_x86_64-linux-gnu"] = mock_cross_compiler
        
        # Run setup
        result = self.system.setup_cross_compilation("linux", "x86_64-linux-gnu")
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"CC": "gcc"})

    def test_setup_cross_compilation_not_found(self) -> None:
        """Test setup_cross_compilation when cross-compiler is not found"""
        # Mock toolchain detector
        self.system._toolchain_detector.detect_toolchain = Mock(return_value=None)
        
        # Run setup and expect ValueError
        with self.assertRaises(ValueError):
            self.system.setup_cross_compilation("linux", "x86_64-linux-gnu")

    def test_setup_cross_compilation_instance_not_found(self) -> None:
        """Test setup_cross_compilation when cross-compiler instance is not found"""
        # Mock toolchain info
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.platform = "linux"
        mock_toolchain.architecture = "x86_64-linux-gnu"
        
        # Mock toolchain detector
        self.system._toolchain_detector.detect_toolchain = Mock(
            return_value=mock_toolchain
        )
        
        # Run setup and expect RuntimeError
        with self.assertRaises(RuntimeError):
            self.system.setup_cross_compilation("linux", "x86_64-linux-gnu")

    def test_get_cmake_generator_success(self) -> None:
        """Test get_cmake_generator when selection succeeds"""
        # Mock selection result
        mock_result = Mock(spec=GeneratorSelectionResult)
        mock_result.generator = "Ninja"
        mock_result.generator_type = Mock()
        mock_result.generator_type.value = "Ninja"
        mock_result.compiler_type = Mock()
        mock_result.compiler_type.value = "msvc"
        mock_result.target_platform = Mock()
        mock_result.target_platform.value = "windows"
        mock_result.fallback_used = False
        mock_result.warnings = []
        
        # Mock CMake selector
        self.system._cmake_selector.select_generator = Mock(return_value=mock_result)
        
        # Run selection
        result = self.system.get_cmake_generator("msvc", "windows", False)
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.generator, "Ninja")

    def test_get_cmake_generator_exception(self) -> None:
        """Test get_cmake_generator when exception occurs"""
        # Mock CMake selector to raise exception
        self.system._cmake_selector.select_generator = Mock(
            side_effect=Exception("Selection failed")
        )
        
        # Run selection
        result = self.system.get_cmake_generator("msvc", "windows", False)
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertTrue(result.fallback_used)
        self.assertGreater(len(result.warnings), 0)

    def test_get_all_compilers(self) -> None:
        """Test get_all_compilers"""
        # Mock compiler manager
        compilers = {
            "msvc": [Mock(spec=MSVCCompilerInfo)],
            "mingw_gcc": []
        }
        self.system._compiler_manager.get_all_compilers = Mock(return_value=compilers)
        
        # Run detection
        result = self.system.get_all_compilers()
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertEqual(result, compilers)

    def test_get_all_terminals(self) -> None:
        """Test get_all_terminals"""
        # Mock terminal info
        mock_terminal = Mock(spec=TerminalInfo)
        mock_terminal.type = Mock()
        mock_terminal.type.value = "msvc"
        
        # Mock terminal detector
        self.mock_terminal_detector.detect = Mock(return_value=[mock_terminal])
        
        # Run detection
        result = self.system.get_all_terminals()
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn("msvc", result)
        self.assertEqual(len(result["msvc"]), 1)

    def test_get_all_terminals_without_detector(self) -> None:
        """Test get_all_terminals when detector is not available"""
        # Create system without terminal detector
        system = CompilerDetectionSystem(logger=self.logger)
        
        # Run detection
        result = system.get_all_terminals()
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_get_all_cross_compilers(self) -> None:
        """Test get_all_cross_compilers"""
        # Mock toolchain info
        mock_toolchain = Mock(spec=UnifiedToolchainInfo)
        mock_toolchain.platform = "linux"
        mock_toolchain.architecture = "x86_64-linux-gnu"
        
        # Mock toolchain detector
        mock_toolchain_result = Mock()
        mock_toolchain_result.success = True
        mock_toolchain_result.toolchains = [mock_toolchain]
        self.system._toolchain_detector.detect = Mock(return_value=mock_toolchain_result)
        
        # Run detection
        result = self.system.get_all_cross_compilers()
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn("linux_x86_64-linux-gnu", result)

    def test_refresh_detection(self) -> None:
        """Test refresh_detection"""
        # Mock factory clear_cache
        self.system._factory.clear_cache = Mock()
        
        # Mock detect_all
        mock_result = Mock(spec=DetectionResult)
        self.system.detect_all = Mock(return_value=mock_result)
        
        # Run refresh
        result = self.system.refresh_detection()
        
        # Verify result
        self.system._factory.clear_cache.assert_called_once()
        self.system.detect_all.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_get_system_info(self) -> None:
        """Test get_system_info"""
        # Mock detect_all
        mock_detection_result = Mock(spec=DetectionResult)
        mock_detection_result.to_dict.return_value = {
            "compilers": {},
            "terminals": {},
            "cross_compilers": {},
            "errors": [],
            "warnings": [],
            "success": True
        }
        mock_detection_result.compilers = {}
        mock_detection_result.terminals = {}
        mock_detection_result.cross_compilers = {}
        mock_detection_result.has_errors = False
        mock_detection_result.has_warnings = False
        
        # Mock validate_system
        mock_validation_result = Mock(spec=ValidationResult)
        mock_validation_result.to_dict.return_value = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        mock_validation_result.is_valid = True
        
        # Mock methods
        self.system.detect_all = Mock(return_value=mock_detection_result)
        self.system.validate_system = Mock(return_value=mock_validation_result)
        
        # Run detection
        result = self.system.get_system_info()
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn("detection", result)
        self.assertIn("validation", result)
        self.assertIn("compilers_count", result)
        self.assertIn("terminals_count", result)
        self.assertIn("cross_compilers_count", result)
        self.assertIn("has_errors", result)
        self.assertIn("has_warnings", result)
        self.assertIn("is_valid", result)


if __name__ == "__main__":
    unittest.main()
