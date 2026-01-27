"""
Unit tests for Compiler-Terminal Mapper

Tests the mapping between compiler types and their appropriate terminals,
ensuring compatibility and proper terminal selection.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import logging
from typing import List, Optional

# Import the module to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.compiler_terminal_mapper import (
    CompilerTerminalMapper,
    TerminalMapping,
    TerminalInfo,
    TerminalType,
    ITerminalDetector,
    CompilerInfo
)


class MockTerminalDetector(ITerminalDetector):
    """Mock terminal detector for testing"""

    def __init__(self, terminals: Optional[List[TerminalInfo]] = None):
        self._terminals = terminals or []
        self.detect_called = False
        self.get_terminal_calls = []
        self.validate_calls = []

    def detect(self) -> List[TerminalInfo]:
        """Detect terminals (mock)"""
        self.detect_called = True
        return self._terminals

    def get_terminal(self, terminal_id: str) -> Optional[TerminalInfo]:
        """Get terminal by ID (mock)"""
        self.get_terminal_calls.append(terminal_id)
        for terminal in self._terminals:
            if terminal.terminal_id == terminal_id:
                return terminal
        return None

    def validate(self, terminal_info: TerminalInfo) -> bool:
        """Validate terminal (mock)"""
        self.validate_calls.append(terminal_info)
        return True


class TestCompilerTerminalMapper(unittest.TestCase):
    """Test cases for CompilerTerminalMapper"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create mock terminals
        self.msvc_terminals = [
            TerminalInfo(
                terminal_id="developer_cmd",
                name="Developer Command Prompt",
                type=TerminalType.MSVC_DEVELOPER_CMD,
                executable="C:\\VS\\Common7\\Tools\\VsDevCmd.bat",
                architecture="x64",
                environment="msvc",
                capabilities=["msvc"],
                metadata={},
                recommended=True
            ),
            TerminalInfo(
                terminal_id="x64_native",
                name="x64 Native Tools Command Prompt",
                type=TerminalType.MSVC_X64_NATIVE,
                executable="C:\\VS\\VC\\Auxiliary\\Build\\vcvars64.bat",
                architecture="x64",
                environment="msvc",
                capabilities=["msvc"],
                metadata={},
                recommended=True
            ),
            TerminalInfo(
                terminal_id="x86_native",
                name="x86 Native Tools Command Prompt",
                type=TerminalType.MSVC_X86_NATIVE,
                executable="C:\\VS\\VC\\Auxiliary\\Build\\vcvars32.bat",
                architecture="x86",
                environment="msvc",
                capabilities=["msvc"],
                metadata={},
                recommended=False
            ),
            TerminalInfo(
                terminal_id="x64_arm_cross",
                name="x64_arm Cross Tools Command Prompt",
                type=TerminalType.MSVC_X64_ARM_CROSS,
                executable="C:\\VS\\VC\\Auxiliary\\Build\\vcvarsamd64_arm.bat",
                architecture="arm",
                environment="msvc",
                capabilities=["msvc"],
                metadata={},
                recommended=False
            ),
            TerminalInfo(
                terminal_id="x64_arm64_cross",
                name="x64_arm64 Cross Tools Command Prompt",
                type=TerminalType.MSVC_X64_ARM64_CROSS,
                executable="C:\\VS\\VC\\Auxiliary\\Build\\vcvarsamd64_arm64.bat",
                architecture="arm64",
                environment="msvc",
                capabilities=["msvc"],
                metadata={},
                recommended=False
            )
        ]

        self.msys2_terminals = [
            TerminalInfo(
                terminal_id="ucrt64",
                name="MSYS2 UCRT64",
                type=TerminalType.MSYS2_UCRT64,
                executable="C:\\msys64\\msys2_shell.cmd",
                architecture="x64",
                environment="UCRT64",
                capabilities=["msys2", "mingw"],
                metadata={},
                recommended=True
            ),
            TerminalInfo(
                terminal_id="mingw64",
                name="MSYS2 MINGW64",
                type=TerminalType.MSYS2_MINGW64,
                executable="C:\\msys64\\msys2_shell.cmd",
                architecture="x64",
                environment="MINGW64",
                capabilities=["msys2", "mingw"],
                metadata={},
                recommended=True
            ),
            TerminalInfo(
                terminal_id="mingw32",
                name="MSYS2 MINGW32",
                type=TerminalType.MSYS2_MINGW32,
                executable="C:\\msys64\\msys2_shell.cmd",
                architecture="x86",
                environment="MINGW32",
                capabilities=["msys2", "mingw"],
                metadata={},
                recommended=False
            ),
            TerminalInfo(
                terminal_id="msys",
                name="MSYS2 MSYS",
                type=TerminalType.MSYS2_MSYS,
                executable="C:\\msys64\\msys2_shell.cmd",
                architecture="x64",
                environment="MSYS",
                capabilities=["msys2"],
                metadata={},
                recommended=False
            ),
            TerminalInfo(
                terminal_id="clang64",
                name="MSYS2 CLANG64",
                type=TerminalType.MSYS2_CLANG64,
                executable="C:\\msys64\\msys2_shell.cmd",
                architecture="x64",
                environment="CLANG64",
                capabilities=["msys2", "clang"],
                metadata={},
                recommended=True
            )
        ]

        # Create combined terminal detector
        self.all_terminals = self.msvc_terminals + self.msys2_terminals
        self.mock_detector = MockTerminalDetector(self.all_terminals)

        # Create mapper
        self.mapper = CompilerTerminalMapper(self.mock_detector, self.logger)

    def test_initialization(self):
        """Test mapper initialization"""
        self.assertIsNotNone(self.mapper)
        self.assertIsInstance(self.mapper, CompilerTerminalMapper)
        self.assertEqual(len(self.mapper.get_supported_compiler_types()), 4)

    def test_map_msvc_to_terminal_x64(self):
        """Test mapping MSVC to x64 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("msvc", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x64_native")
        self.assertEqual(terminal.architecture, "x64")
        self.assertEqual(terminal.type, TerminalType.MSVC_X64_NATIVE)

    def test_map_msvc_to_terminal_x86(self):
        """Test mapping MSVC to x86 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("msvc", "x86")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x86_native")
        self.assertEqual(terminal.architecture, "x86")
        self.assertEqual(terminal.type, TerminalType.MSVC_X86_NATIVE)

    def test_map_msvc_to_terminal_arm(self):
        """Test mapping MSVC to ARM terminal"""
        terminal = self.mapper.map_compiler_to_terminal("msvc", "arm")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x64_arm_cross")
        self.assertEqual(terminal.architecture, "arm")
        self.assertEqual(terminal.type, TerminalType.MSVC_X64_ARM_CROSS)

    def test_map_msvc_to_terminal_arm64(self):
        """Test mapping MSVC to ARM64 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("msvc", "arm64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x64_arm64_cross")
        self.assertEqual(terminal.architecture, "arm64")
        self.assertEqual(terminal.type, TerminalType.MSVC_X64_ARM64_CROSS)

    def test_map_msvc_clang_to_terminal_x64(self):
        """Test mapping MSVC-Clang to x64 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("msvc_clang", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x64_native")
        self.assertEqual(terminal.architecture, "x64")

    def test_map_mingw_gcc_to_terminal_x64(self):
        """Test mapping MinGW-GCC to x64 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("mingw_gcc", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "ucrt64")
        self.assertEqual(terminal.architecture, "x64")
        self.assertEqual(terminal.type, TerminalType.MSYS2_UCRT64)

    def test_map_mingw_gcc_to_terminal_x86(self):
        """Test mapping MinGW-GCC to x86 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("mingw_gcc", "x86")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "mingw32")
        self.assertEqual(terminal.architecture, "x86")
        self.assertEqual(terminal.type, TerminalType.MSYS2_MINGW32)

    def test_map_mingw_clang_to_terminal_x64(self):
        """Test mapping MinGW-Clang to x64 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("mingw_clang", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "clang64")
        self.assertEqual(terminal.architecture, "x64")
        self.assertEqual(terminal.type, TerminalType.MSYS2_CLANG64)

    def test_map_mingw_clang_to_terminal_x86(self):
        """Test mapping MinGW-Clang to x86 terminal"""
        terminal = self.mapper.map_compiler_to_terminal("mingw_clang", "x86")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "mingw32")
        self.assertEqual(terminal.architecture, "x86")

    def test_get_terminal_for_compiler(self):
        """Test get_terminal_for_compiler method"""
        terminal = self.mapper.get_terminal_for_compiler("msvc", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "x64_native")

    def test_get_preferred_terminal(self):
        """Test get_preferred_terminal method"""
        terminal = self.mapper.get_preferred_terminal("mingw_gcc", "x64")

        self.assertIsNotNone(terminal)
        self.assertEqual(terminal.terminal_id, "ucrt64")

    def test_validate_mapping_valid(self):
        """Test validate_mapping with valid mapping"""
        terminal = self.msvc_terminals[1]  # x64_native
        is_valid = self.mapper.validate_mapping("msvc", terminal)

        self.assertTrue(is_valid)

    def test_validate_mapping_invalid_compiler_type(self):
        """Test validate_mapping with invalid compiler type"""
        terminal = self.msvc_terminals[0]
        is_valid = self.mapper.validate_mapping("invalid_compiler", terminal)

        self.assertFalse(is_valid)

    def test_validate_mapping_unsupported_terminal(self):
        """Test validate_mapping with unsupported terminal"""
        # Create a terminal not in the supported list
        terminal = TerminalInfo(
            terminal_id="invalid_terminal",
            name="Invalid Terminal",
            type=TerminalType.CMD,
            executable="cmd.exe",
            architecture="x64",
            environment="",
            capabilities=[],
            metadata={}
        )
        is_valid = self.mapper.validate_mapping("msvc", terminal)

        self.assertFalse(is_valid)

    def test_validate_mapping_wrong_terminal_type(self):
        """Test validate_mapping with wrong terminal type"""
        # Try to use MSYS2 terminal with MSVC compiler
        terminal = self.msys2_terminals[0]  # ucrt64
        is_valid = self.mapper.validate_mapping("msvc", terminal)

        self.assertFalse(is_valid)

    def test_get_supported_terminals_msvc(self):
        """Test get_supported_terminals for MSVC"""
        terminals = self.mapper.get_supported_terminals("msvc")

        self.assertIsNotNone(terminals)
        self.assertGreater(len(terminals), 0)
        terminal_ids = [t.terminal_id for t in terminals]
        self.assertIn("developer_cmd", terminal_ids)
        self.assertIn("x64_native", terminal_ids)

    def test_get_supported_terminals_mingw_gcc(self):
        """Test get_supported_terminals for MinGW-GCC"""
        terminals = self.mapper.get_supported_terminals("mingw_gcc")

        self.assertIsNotNone(terminals)
        self.assertGreater(len(terminals), 0)
        terminal_ids = [t.terminal_id for t in terminals]
        self.assertIn("ucrt64", terminal_ids)
        self.assertIn("mingw64", terminal_ids)

    def test_get_supported_terminals_mingw_clang(self):
        """Test get_supported_terminals for MinGW-Clang"""
        terminals = self.mapper.get_supported_terminals("mingw_clang")

        self.assertIsNotNone(terminals)
        self.assertGreater(len(terminals), 0)
        terminal_ids = [t.terminal_id for t in terminals]
        self.assertIn("ucrt64", terminal_ids)
        self.assertIn("clang64", terminal_ids)

    def test_get_supported_terminals_invalid_compiler(self):
        """Test get_supported_terminals with invalid compiler type"""
        with self.assertRaises(ValueError) as context:
            self.mapper.get_supported_terminals("invalid_compiler")

        self.assertIn("Unsupported compiler type", str(context.exception))

    def test_map_compiler_to_terminal_invalid_compiler(self):
        """Test map_compiler_to_terminal with invalid compiler type"""
        with self.assertRaises(ValueError) as context:
            self.mapper.map_compiler_to_terminal("invalid_compiler", "x64")

        self.assertIn("Unsupported compiler type", str(context.exception))

    def test_is_compiler_supported(self):
        """Test is_compiler_supported method"""
        self.assertTrue(self.mapper.is_compiler_supported("msvc"))
        self.assertTrue(self.mapper.is_compiler_supported("msvc_clang"))
        self.assertTrue(self.mapper.is_compiler_supported("mingw_gcc"))
        self.assertTrue(self.mapper.is_compiler_supported("mingw_clang"))
        self.assertFalse(self.mapper.is_compiler_supported("invalid_compiler"))

    def test_get_supported_compiler_types(self):
        """Test get_supported_compiler_types method"""
        compiler_types = self.mapper.get_supported_compiler_types()

        self.assertIsNotNone(compiler_types)
        self.assertEqual(len(compiler_types), 4)
        self.assertIn("msvc", compiler_types)
        self.assertIn("msvc_clang", compiler_types)
        self.assertIn("mingw_gcc", compiler_types)
        self.assertIn("mingw_clang", compiler_types)

    def test_get_mapping_config(self):
        """Test get_mapping_config method"""
        config = self.mapper.get_mapping_config()

        self.assertIsNotNone(config)
        self.assertIsInstance(config, dict)
        self.assertEqual(len(config), 4)
        self.assertIn("msvc", config)
        self.assertIn("msvc_clang", config)
        self.assertIn("mingw_gcc", config)
        self.assertIn("mingw_clang", config)

    def test_mapping_config_structure(self):
        """Test mapping configuration structure"""
        config = self.mapper.get_mapping_config()
        msvc_mapping = config["msvc"]

        self.assertIsInstance(msvc_mapping, TerminalMapping)
        self.assertEqual(msvc_mapping.compiler_type, "msvc")
        self.assertIsInstance(msvc_mapping.preferred_terminals, list)
        self.assertIsInstance(msvc_mapping.supported_terminals, list)
        self.assertEqual(msvc_mapping.terminal_type, "msvc")
        self.assertTrue(msvc_mapping.requires_additional_setup)

    def test_terminal_mapping_to_dict(self):
        """Test TerminalMapping to_dict method"""
        config = self.mapper.get_mapping_config()
        msvc_mapping = config["msvc"]
        mapping_dict = msvc_mapping.to_dict()

        self.assertIsInstance(mapping_dict, dict)
        self.assertIn("compiler_type", mapping_dict)
        self.assertIn("preferred_terminals", mapping_dict)
        self.assertIn("supported_terminals", mapping_dict)
        self.assertIn("terminal_type", mapping_dict)
        self.assertIn("requires_additional_setup", mapping_dict)

    def test_terminal_info_to_dict(self):
        """Test TerminalInfo to_dict method"""
        terminal = self.msvc_terminals[0]
        terminal_dict = terminal.to_dict()

        self.assertIsInstance(terminal_dict, dict)
        self.assertIn("terminal_id", terminal_dict)
        self.assertIn("name", terminal_dict)
        self.assertIn("type", terminal_dict)
        self.assertIn("executable", terminal_dict)
        self.assertIn("architecture", terminal_dict)
        self.assertIn("environment", terminal_dict)
        self.assertIn("capabilities", terminal_dict)
        self.assertIn("metadata", terminal_dict)
        self.assertIn("recommended", terminal_dict)

    def test_map_compiler_to_terminal_not_found(self):
        """Test mapping when terminal is not found"""
        # Create detector with no terminals
        empty_detector = MockTerminalDetector([])
        mapper = CompilerTerminalMapper(empty_detector, self.logger)

        terminal = mapper.map_compiler_to_terminal("msvc", "x64")

        self.assertIsNone(terminal)

    def test_get_msvc_terminal_id(self):
        """Test _get_msvc_terminal_id method"""
        # Test through public API
        terminal = self.mapper.map_compiler_to_terminal("msvc", "x64")
        self.assertEqual(terminal.terminal_id, "x64_native")

        terminal = self.mapper.map_compiler_to_terminal("msvc", "x86")
        self.assertEqual(terminal.terminal_id, "x86_native")

        terminal = self.mapper.map_compiler_to_terminal("msvc", "arm")
        self.assertEqual(terminal.terminal_id, "x64_arm_cross")

        terminal = self.mapper.map_compiler_to_terminal("msvc", "arm64")
        self.assertEqual(terminal.terminal_id, "x64_arm64_cross")

    def test_get_msys2_terminal_id(self):
        """Test _get_msys2_terminal_id method"""
        # Test through public API
        terminal = self.mapper.map_compiler_to_terminal("mingw_gcc", "x64")
        self.assertEqual(terminal.terminal_id, "ucrt64")

        terminal = self.mapper.map_compiler_to_terminal("mingw_gcc", "x86")
        self.assertEqual(terminal.terminal_id, "mingw32")

        terminal = self.mapper.map_compiler_to_terminal("mingw_clang", "x64")
        self.assertEqual(terminal.terminal_id, "clang64")

    def test_logging_operations(self):
        """Test that operations are logged"""
        with patch.object(self.logger, 'info') as mock_info:
            self.mapper.map_compiler_to_terminal("msvc", "x64")

            # Verify logging was called
            self.assertTrue(mock_info.called)

    def test_all_compiler_types_have_mappings(self):
        """Test that all compiler types have valid mappings"""
        compiler_types = self.mapper.get_supported_compiler_types()

        for compiler_type in compiler_types:
            mapping = self.mapper.get_mapping_config()[compiler_type]
            self.assertIsNotNone(mapping)
            self.assertEqual(mapping.compiler_type, compiler_type)
            self.assertGreater(len(mapping.preferred_terminals), 0)
            self.assertGreater(len(mapping.supported_terminals), 0)

    def test_msvc_mapping_preferred_terminals(self):
        """Test MSVC mapping preferred terminals"""
        config = self.mapper.get_mapping_config()
        msvc_mapping = config["msvc"]

        self.assertIn("x64_native", msvc_mapping.preferred_terminals)
        self.assertIn("developer_cmd", msvc_mapping.preferred_terminals)

    def test_mingw_gcc_mapping_preferred_terminals(self):
        """Test MinGW-GCC mapping preferred terminals"""
        config = self.mapper.get_mapping_config()
        mingw_mapping = config["mingw_gcc"]

        self.assertIn("ucrt64", mingw_mapping.preferred_terminals)
        self.assertIn("mingw64", mingw_mapping.preferred_terminals)

    def test_mingw_clang_mapping_preferred_terminals(self):
        """Test MinGW-Clang mapping preferred terminals"""
        config = self.mapper.get_mapping_config()
        mingw_mapping = config["mingw_clang"]

        self.assertIn("ucrt64", mingw_mapping.preferred_terminals)
        self.assertIn("mingw64", mingw_mapping.preferred_terminals)

    def test_msvc_mapping_supported_terminals(self):
        """Test MSVC mapping supported terminals"""
        config = self.mapper.get_mapping_config()
        msvc_mapping = config["msvc"]

        self.assertIn("developer_cmd", msvc_mapping.supported_terminals)
        self.assertIn("x64_native", msvc_mapping.supported_terminals)
        self.assertIn("x86_native", msvc_mapping.supported_terminals)
        self.assertIn("x86_x64_cross", msvc_mapping.supported_terminals)
        self.assertIn("x64_x86_cross", msvc_mapping.supported_terminals)
        self.assertIn("x64_arm_cross", msvc_mapping.supported_terminals)
        self.assertIn("x64_arm64_cross", msvc_mapping.supported_terminals)

    def test_mingw_gcc_mapping_supported_terminals(self):
        """Test MinGW-GCC mapping supported terminals"""
        config = self.mapper.get_mapping_config()
        mingw_mapping = config["mingw_gcc"]

        self.assertIn("ucrt64", mingw_mapping.supported_terminals)
        self.assertIn("mingw64", mingw_mapping.supported_terminals)
        self.assertIn("mingw32", mingw_mapping.supported_terminals)
        self.assertIn("msys", mingw_mapping.supported_terminals)

    def test_mingw_clang_mapping_supported_terminals(self):
        """Test MinGW-Clang mapping supported terminals"""
        config = self.mapper.get_mapping_config()
        mingw_mapping = config["mingw_clang"]

        self.assertIn("ucrt64", mingw_mapping.supported_terminals)
        self.assertIn("mingw64", mingw_mapping.supported_terminals)
        self.assertIn("mingw32", mingw_mapping.supported_terminals)
        self.assertIn("clang64", mingw_mapping.supported_terminals)


if __name__ == '__main__':
    unittest.main()
