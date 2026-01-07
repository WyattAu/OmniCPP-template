"""
Compiler-Terminal Mapper

This module provides mapping between compiler types and their appropriate terminals,
ensuring compatibility and providing preferred terminal selection for each compiler.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class TerminalType(Enum):
    """Terminal type enumeration"""
    MSVC_DEVELOPER_CMD = "msvc_developer_cmd"
    MSVC_X64_NATIVE = "msvc_x64_native"
    MSVC_X86_NATIVE = "msvc_x86_native"
    MSVC_X86_X64_CROSS = "msvc_x86_x64_cross"
    MSVC_X64_X86_CROSS = "msvc_x64_x86_cross"
    MSVC_X64_ARM_CROSS = "msvc_x64_arm_cross"
    MSVC_X64_ARM64_CROSS = "msvc_x64_arm64_cross"
    MSYS2_UCRT64 = "msys2_ucrt64"
    MSYS2_MINGW64 = "msys2_mingw64"
    MSYS2_MINGW32 = "msys2_mingw32"
    MSYS2_MSYS = "msys2_msys"
    MSYS2_CLANG64 = "msys2_clang64"
    POWERSHELL = "powershell"
    CMD = "cmd"
    GIT_BASH = "git_bash"
    WSL = "wsl"
    BASH = "bash"
    ZSH = "zsh"


@dataclass
class TerminalInfo:
    """Terminal information"""
    terminal_id: str
    name: str
    type: TerminalType
    executable: str
    arguments: List[str] = field(default_factory=list)
    architecture: str = "x64"
    environment: str = ""
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    recommended: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "terminal_id": self.terminal_id,
            "name": self.name,
            "type": self.type.value,
            "executable": self.executable,
            "arguments": self.arguments,
            "architecture": self.architecture,
            "environment": self.environment,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
            "recommended": self.recommended
        }

    def is_valid(self) -> bool:
        """Check if terminal is valid"""
        import os
        return os.path.exists(self.executable)


@dataclass
class TerminalMapping:
    """Terminal mapping configuration"""
    compiler_type: str
    preferred_terminals: List[str]
    supported_terminals: List[str]
    terminal_type: str
    requires_additional_setup: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compiler_type": self.compiler_type,
            "preferred_terminals": self.preferred_terminals,
            "supported_terminals": self.supported_terminals,
            "terminal_type": self.terminal_type,
            "requires_additional_setup": self.requires_additional_setup
        }


class ITerminalDetector:
    """Interface for terminal detectors"""

    def detect(self) -> List[TerminalInfo]:
        """
        Detect all terminals of this type

        Returns:
            List of detected terminal information
        """
        raise NotImplementedError

    def get_terminal(self, terminal_id: str) -> Optional[TerminalInfo]:
        """
        Get a specific terminal

        Args:
            terminal_id: Terminal identifier

        Returns:
            Terminal information or None if not found
        """
        raise NotImplementedError

    def validate(self, terminal_info: TerminalInfo) -> bool:
        """
        Validate terminal installation

        Args:
            terminal_info: Terminal information to validate

        Returns:
            True if valid, False otherwise
        """
        raise NotImplementedError


@dataclass
class CompilerInfo:
    """Compiler information"""
    compiler_type: str
    version: str
    path: str
    architecture: str
    capabilities: Dict[str, bool]
    environment: Dict[str, str]
    metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compiler_type": self.compiler_type,
            "version": self.version,
            "path": self.path,
            "architecture": self.architecture,
            "capabilities": self.capabilities,
            "environment": self.environment,
            "metadata": self.metadata
        }


class CompilerTerminalMapper:
    """Mapper for compilers to terminals"""

    def __init__(self, terminal_detector: ITerminalDetector, logger: Optional[logging.Logger] = None):
        """
        Initialize compiler-terminal mapper

        Args:
            terminal_detector: Terminal detector instance
            logger: Logger instance for logging operations
        """
        self._logger = logger or logging.getLogger(__name__)
        self._terminal_detector = terminal_detector
        self._compiler_terminal_map: Dict[str, TerminalMapping] = {}
        self._load_mapping_config()
        self._logger.info("CompilerTerminalMapper initialized")

    def map_compiler_to_terminal(self, compiler_type: str, architecture: str) -> Optional[TerminalInfo]:
        """
        Map compiler to terminal

        Args:
            compiler_type: Type of compiler (msvc, msvc_clang, mingw_gcc, mingw_clang)
            architecture: Target architecture (x64, x86, arm, arm64)

        Returns:
            Terminal information or None if not found

        Raises:
            ValueError: If compiler_type is not supported
        """
        self._logger.debug(f"Mapping compiler {compiler_type} ({architecture}) to terminal")

        # Validate compiler type
        if compiler_type not in self._compiler_terminal_map:
            error_msg = f"Unsupported compiler type: {compiler_type}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        mapping = self._compiler_terminal_map[compiler_type]

        # Select terminal based on architecture and terminal type
        if mapping.terminal_type == "msvc":
            terminal_id = self._get_msvc_terminal_id(architecture)
        elif mapping.terminal_type == "msys2":
            terminal_id = self._get_msys2_terminal_id(compiler_type, architecture)
        else:
            # Use first preferred terminal
            terminal_id = mapping.preferred_terminals[0]

        self._logger.debug(f"Selected terminal ID: {terminal_id}")

        # Get terminal from detector
        terminal = self._terminal_detector.get_terminal(terminal_id)
        if terminal:
            self._logger.info(f"Mapped {compiler_type} ({architecture}) to {terminal.name}")
        else:
            self._logger.warning(f"Terminal not found: {terminal_id}")

        return terminal

    def get_terminal_for_compiler(self, compiler_type: str, architecture: str = "x64") -> Optional[TerminalInfo]:
        """
        Get terminal for compiler (alias for map_compiler_to_terminal)

        Args:
            compiler_type: Type of compiler
            architecture: Target architecture

        Returns:
            Terminal information or None if not found
        """
        return self.map_compiler_to_terminal(compiler_type, architecture)

    def validate_mapping(self, compiler_type: str, terminal_info: TerminalInfo) -> bool:
        """
        Validate compiler-terminal compatibility

        Args:
            compiler_type: Type of compiler
            terminal_info: Terminal information to validate

        Returns:
            True if compatible, False otherwise
        """
        self._logger.debug(f"Validating mapping for {compiler_type} to {terminal_info.terminal_id}")

        # Check if compiler type is supported
        if compiler_type not in self._compiler_terminal_map:
            self._logger.error(f"Unsupported compiler type: {compiler_type}")
            return False

        mapping = self._compiler_terminal_map[compiler_type]

        # Check if terminal is in supported list
        if terminal_info.terminal_id not in mapping.supported_terminals:
            self._logger.warning(
                f"Terminal {terminal_info.terminal_id} not in supported list for {compiler_type}"
            )
            return False

        # Check terminal type compatibility
        if mapping.terminal_type == "msvc":
            if not terminal_info.type.value.startswith("msvc"):
                self._logger.warning(
                    f"Terminal type {terminal_info.type.value} not compatible with MSVC compiler"
                )
                return False
        elif mapping.terminal_type == "msys2":
            if not terminal_info.type.value.startswith("msys2"):
                self._logger.warning(
                    f"Terminal type {terminal_info.type.value} not compatible with MinGW compiler"
                )
                return False

        self._logger.info(f"Mapping validated: {compiler_type} -> {terminal_info.terminal_id}")
        return True

    def get_supported_terminals(self, compiler_type: str) -> List[TerminalInfo]:
        """
        Get supported terminals for compiler

        Args:
            compiler_type: Type of compiler

        Returns:
            List of terminal information

        Raises:
            ValueError: If compiler_type is not supported
        """
        self._logger.debug(f"Getting supported terminals for {compiler_type}")

        # Validate compiler type
        if compiler_type not in self._compiler_terminal_map:
            error_msg = f"Unsupported compiler type: {compiler_type}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        mapping = self._compiler_terminal_map[compiler_type]

        terminals: List[TerminalInfo] = []
        for terminal_id in mapping.supported_terminals:
            terminal = self._terminal_detector.get_terminal(terminal_id)
            if terminal:
                terminals.append(terminal)
            else:
                self._logger.warning(f"Terminal not found: {terminal_id}")

        self._logger.info(f"Found {len(terminals)} supported terminals for {compiler_type}")
        return terminals

    def get_preferred_terminal(self, compiler_type: str, architecture: str = "x64") -> Optional[TerminalInfo]:
        """
        Get preferred terminal for compiler

        Args:
            compiler_type: Type of compiler
            architecture: Target architecture

        Returns:
            Terminal information or None if not found
        """
        return self.map_compiler_to_terminal(compiler_type, architecture)

    def _load_mapping_config(self) -> None:
        """Load compiler-terminal mapping configuration"""
        self._logger.debug("Loading compiler-terminal mapping configuration")

        self._compiler_terminal_map = {
            "msvc": TerminalMapping(
                compiler_type="msvc",
                preferred_terminals=["x64_native", "developer_cmd"],
                supported_terminals=[
                    "developer_cmd",
                    "x64_native",
                    "x86_native",
                    "x86_x64_cross",
                    "x64_x86_cross",
                    "x64_arm_cross",
                    "x64_arm64_cross"
                ],
                terminal_type="msvc",
                requires_additional_setup=True
            ),
            "msvc_clang": TerminalMapping(
                compiler_type="msvc_clang",
                preferred_terminals=["x64_native", "developer_cmd"],
                supported_terminals=[
                    "developer_cmd",
                    "x64_native",
                    "x86_native",
                    "x86_x64_cross",
                    "x64_x86_cross"
                ],
                terminal_type="msvc",
                requires_additional_setup=True
            ),
            "mingw_gcc": TerminalMapping(
                compiler_type="mingw_gcc",
                preferred_terminals=["ucrt64", "mingw64"],
                supported_terminals=[
                    "ucrt64",
                    "mingw64",
                    "mingw32",
                    "msys"
                ],
                terminal_type="msys2",
                requires_additional_setup=True
            ),
            "mingw_clang": TerminalMapping(
                compiler_type="mingw_clang",
                preferred_terminals=["ucrt64", "mingw64"],
                supported_terminals=[
                    "ucrt64",
                    "mingw64",
                    "mingw32",
                    "clang64"
                ],
                terminal_type="msys2",
                requires_additional_setup=True
            )
        }

        self._logger.info(f"Loaded {len(self._compiler_terminal_map)} compiler-terminal mappings")

    def _get_msvc_terminal_id(self, architecture: str) -> str:
        """
        Get MSVC terminal ID for architecture

        Args:
            architecture: Target architecture

        Returns:
            Terminal ID
        """
        architecture_map: Dict[str, str] = {
            "x64": "x64_native",
            "x86": "x86_native",
            "arm": "x64_arm_cross",
            "arm64": "x64_arm64_cross"
        }

        terminal_id = architecture_map.get(architecture, "developer_cmd")
        self._logger.debug(f"MSVC terminal ID for {architecture}: {terminal_id}")
        return terminal_id

    def _get_msys2_terminal_id(self, compiler_type: str, architecture: str) -> str:
        """
        Get MSYS2 terminal ID for compiler and architecture

        Args:
            compiler_type: Type of compiler
            architecture: Target architecture

        Returns:
            Terminal ID
        """
        # Default to ucrt64 for x64
        if architecture == "x64":
            terminal_id = "ucrt64"
        # Use mingw32 for x86
        elif architecture == "x86":
            terminal_id = "mingw32"
        # Default to ucrt64 for other architectures
        else:
            terminal_id = "ucrt64"

        # For clang compilers, prefer clang64 if available
        if compiler_type == "mingw_clang" and architecture == "x64":
            terminal_id = "clang64"

        self._logger.debug(f"MSYS2 terminal ID for {compiler_type} ({architecture}): {terminal_id}")
        return terminal_id

    def get_mapping_config(self) -> Dict[str, TerminalMapping]:
        """
        Get current mapping configuration

        Returns:
            Dictionary of compiler type to terminal mapping
        """
        return self._compiler_terminal_map.copy()

    def is_compiler_supported(self, compiler_type: str) -> bool:
        """
        Check if compiler type is supported

        Args:
            compiler_type: Type of compiler

        Returns:
            True if supported, False otherwise
        """
        return compiler_type in self._compiler_terminal_map

    def get_supported_compiler_types(self) -> List[str]:
        """
        Get list of supported compiler types

        Returns:
            List of compiler type strings
        """
        return list(self._compiler_terminal_map.keys())
