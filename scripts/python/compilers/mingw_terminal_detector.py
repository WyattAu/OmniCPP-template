"""
MSYS2 Terminal Detector

This module provides comprehensive detection of MSYS2 shells and all
environment-specific terminal variants (UCRT64, MINGW64, MINGW32, MSYS, CLANG64).
"""

import logging
import os
import subprocess
from abc import ABC, abstractmethod
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
        return os.path.exists(self.executable)


class ITerminalDetector(ABC):
    """Interface for terminal detectors"""

    @abstractmethod
    def detect(self) -> List[TerminalInfo]:
        """
        Detect all terminals of this type

        Returns:
            List of detected terminal information
        """
        pass

    @abstractmethod
    def get_terminal(self, terminal_id: str) -> Optional[TerminalInfo]:
        """
        Get a specific terminal

        Args:
            terminal_id: Terminal identifier

        Returns:
            Terminal information or None if not found
        """
        pass

    @abstractmethod
    def validate(self, terminal_info: TerminalInfo) -> bool:
        """
        Validate terminal installation

        Args:
            terminal_info: Terminal information to validate

        Returns:
            True if valid, False otherwise
        """
        pass


class MSYS2TerminalDetector(ITerminalDetector):
    """Detector for MSYS2 shells and terminals"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize MSYS2 terminal detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._detected_terminals: List[TerminalInfo] = []
        self._msys2_paths: List[str] = self._get_msys2_paths()

    def detect(self) -> List[TerminalInfo]:
        """
        Detect all MSYS2 terminals

        Returns:
            List of detected terminal information
        """
        self._logger.info("Starting MSYS2 terminal detection")
        self._detected_terminals.clear()

        # Detect all terminal types
        terminals: List[TerminalInfo] = []

        # Detect MSYS2 shells
        shell_terminals = self._detect_msys2_shells()
        terminals.extend(shell_terminals)
        self._logger.info(f"Detected {len(shell_terminals)} MSYS2 shell terminals")

        # Detect Start Menu shortcuts
        shortcut_terminals = self._detect_shortcuts()
        terminals.extend(shortcut_terminals)
        self._logger.info(f"Detected {len(shortcut_terminals)} shortcut terminals")

        self._detected_terminals = terminals
        self._logger.info(f"Total detected MSYS2 terminals: {len(terminals)}")

        return terminals

    def get_terminal(self, terminal_id: str) -> Optional[TerminalInfo]:
        """
        Get a specific terminal by ID

        Args:
            terminal_id: Terminal identifier

        Returns:
            Terminal information or None if not found
        """
        self._logger.debug(f"Getting terminal: {terminal_id}")

        for terminal in self._detected_terminals:
            if terminal.terminal_id == terminal_id:
                return terminal

        self._logger.warning(f"Terminal not found: {terminal_id}")
        return None

    def validate(self, terminal_info: TerminalInfo) -> bool:
        """
        Validate terminal installation

        Args:
            terminal_info: Terminal information to validate

        Returns:
            True if valid, False otherwise
        """
        self._logger.debug(f"Validating terminal: {terminal_info.terminal_id}")

        # Check if executable exists
        if not os.path.exists(terminal_info.executable):
            self._logger.error(f"Terminal executable not found: {terminal_info.executable}")
            return False

        # Check if executable is a file
        if not os.path.isfile(terminal_info.executable):
            self._logger.error(f"Terminal path is not a file: {terminal_info.executable}")
            return False

        # Try to execute terminal with help flag
        try:
            # Batch files don't support --help, use /? instead
            if terminal_info.executable.lower().endswith('.cmd') or terminal_info.executable.lower().endswith('.bat'):
                subprocess.run(
                    [terminal_info.executable, "/?"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=True
                )
            else:
                subprocess.run(
                    [terminal_info.executable, "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            # Batch files return 0 even with /?, so we check if it ran
            self._logger.debug(f"Terminal validation successful: {terminal_info.terminal_id}")
            return True
        except subprocess.TimeoutExpired:
            self._logger.error(f"Terminal validation timed out: {terminal_info.executable}")
            return False
        except Exception as e:
            self._logger.error(f"Terminal validation failed: {e}")
            return False

    def _detect_msys2_shells(self) -> List[TerminalInfo]:
        """
        Detect MSYS2 shell terminals

        Returns:
            List of detected terminal information
        """
        self._logger.debug("Detecting MSYS2 shell terminals")

        terminals: List[TerminalInfo] = []

        # MSYS2 shell configurations
        shell_configs: List[Dict[str, Any]] = [
            {
                "terminal_id": "ucrt64",
                "name": "MSYS2 UCRT64",
                "type": TerminalType.MSYS2_UCRT64,
                "architecture": "x64",
                "environment": "UCRT64",
                "msystem": "UCRT64",
                "mingw_prefix": "/ucrt64",
                "mingw_chost": "x86_64-w64-mingw32",
                "recommended": True
            },
            {
                "terminal_id": "mingw64",
                "name": "MSYS2 MINGW64",
                "type": TerminalType.MSYS2_MINGW64,
                "architecture": "x64",
                "environment": "MINGW64",
                "msystem": "MINGW64",
                "mingw_prefix": "/mingw64",
                "mingw_chost": "x86_64-w64-mingw32",
                "recommended": True
            },
            {
                "terminal_id": "mingw32",
                "name": "MSYS2 MINGW32",
                "type": TerminalType.MSYS2_MINGW32,
                "architecture": "x86",
                "environment": "MINGW32",
                "msystem": "MINGW32",
                "mingw_prefix": "/mingw32",
                "mingw_chost": "i686-w64-mingw32",
                "recommended": False
            },
            {
                "terminal_id": "msys",
                "name": "MSYS2 MSYS",
                "type": TerminalType.MSYS2_MSYS,
                "architecture": "x64",
                "environment": "MSYS",
                "msystem": "MSYS",
                "mingw_prefix": "/usr",
                "mingw_chost": "x86_64-pc-msys",
                "recommended": False
            },
            {
                "terminal_id": "clang64",
                "name": "MSYS2 CLANG64",
                "type": TerminalType.MSYS2_CLANG64,
                "architecture": "x64",
                "environment": "CLANG64",
                "msystem": "CLANG64",
                "mingw_prefix": "/clang64",
                "mingw_chost": "x86_64-w64-mingw32",
                "recommended": True
            }
        ]

        for config in shell_configs:
            terminal = self._find_msys2_shell(config)
            if terminal:
                terminals.append(terminal)
                self._logger.debug(f"Found {config['name']}: {terminal.executable}")
            else:
                self._logger.warning(f"MSYS2 shell not found: {config['name']}")

        return terminals

    def _detect_shortcuts(self) -> List[TerminalInfo]:
        """
        Detect MSYS2 terminal shortcuts from Start Menu

        Returns:
            List of detected terminal information
        """
        self._logger.debug("Detecting Start Menu shortcuts")

        terminals: List[TerminalInfo] = []

        # Start Menu paths
        start_menu_paths = [
            os.path.join(
                os.environ.get("APPDATA", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs"
            ),
            os.path.join(
                os.environ.get("ProgramData", ""),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs"
            )
        ]

        for start_menu_path in start_menu_paths:
            if not os.path.exists(start_menu_path):
                continue

            # Look for MSYS2 folders
            for item in os.listdir(start_menu_path):
                if "MSYS2" in item:
                    msys2_folder = os.path.join(start_menu_path, item)
                    if os.path.isdir(msys2_folder):
                        # Look for terminal shortcuts
                        shortcut_terminals = self._scan_msys2_folder(msys2_folder)
                        terminals.extend(shortcut_terminals)

        self._logger.debug(f"Found {len(terminals)} Start Menu shortcuts")
        return terminals

    def _find_msys2_shell(self, config: Dict[str, Any]) -> Optional[TerminalInfo]:
        """
        Find an MSYS2 shell terminal

        Args:
            config: Terminal configuration

        Returns:
            Terminal information or None if not found
        """
        for msys2_path in self._msys2_paths:
            # Look for msys2_shell.cmd
            shell_cmd_path = os.path.join(msys2_path, "msys2_shell.cmd")

            if os.path.exists(shell_cmd_path):
                self._logger.debug(f"Found msys2_shell.cmd: {shell_cmd_path}")

                # Determine shell executable based on environment
                shell_executable = self._get_shell_executable(msys2_path, config["environment"])

                terminal = TerminalInfo(
                    terminal_id=config["terminal_id"],
                    name=config["name"],
                    type=config["type"],
                    executable=shell_cmd_path,
                    arguments=[f"-{config['environment'].lower()}"],
                    architecture=config["architecture"],
                    environment=config["environment"],
                    capabilities=["msys2", "mingw", "gcc", "clang"],
                    metadata={
                        "msys2_path": msys2_path,
                        "shell_executable": shell_executable,
                        "msystem": config["msystem"],
                        "mingw_prefix": config["mingw_prefix"],
                        "mingw_chost": config["mingw_chost"]
                    },
                    recommended=config["recommended"]
                )

                return terminal

        return None

    def _get_shell_executable(self, msys2_path: str, environment: str) -> str:
        """
        Get shell executable path for environment

        Args:
            msys2_path: MSYS2 installation path
            environment: Environment name (UCRT64, MINGW64, etc.)

        Returns:
            Shell executable path
        """
        # Map environment to bin directory
        env_bin_map: Dict[str, str] = {
            "UCRT64": "ucrt64",
            "MINGW64": "mingw64",
            "MINGW32": "mingw32",
            "MSYS": "usr",
            "CLANG64": "clang64"
        }

        bin_dir = env_bin_map.get(environment, "usr")
        shell_path = os.path.join(msys2_path, bin_dir, "bin", "bash.exe")

        if os.path.exists(shell_path):
            return shell_path

        # Fallback to usr/bin/bash.exe
        return os.path.join(msys2_path, "usr", "bin", "bash.exe")

    def _scan_msys2_folder(self, msys2_folder: str) -> List[TerminalInfo]:
        """
        Scan MSYS2 folder for terminal shortcuts

        Args:
            msys2_folder: Path to MSYS2 folder

        Returns:
            List of detected terminal information
        """
        terminals: List[TerminalInfo] = []

        try:
            for item in os.listdir(msys2_folder):
                item_path = os.path.join(msys2_folder, item)

                # Check if it's a shortcut (.lnk)
                if item.lower().endswith(".lnk"):
                    # Parse shortcut to get target
                    target = self._resolve_shortcut(item_path)
                    if target and os.path.exists(target):
                        # Determine terminal type from name
                        terminal = self._create_terminal_from_shortcut(item, target)
                        if terminal:
                            terminals.append(terminal)
        except (PermissionError, OSError) as e:
            self._logger.warning(f"Error scanning MSYS2 folder {msys2_folder}: {e}")

        return terminals

    def _resolve_shortcut(self, shortcut_path: str) -> Optional[str]:
        """
        Resolve Windows shortcut to get target path

        Args:
            shortcut_path: Path to shortcut file

        Returns:
            Target path or None if resolution fails
        """
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            return shortcut.Targetpath
        except ImportError:
            self._logger.debug("win32com not available, cannot resolve shortcuts")
            return None
        except Exception as e:
            self._logger.debug(f"Error resolving shortcut {shortcut_path}: {e}")
            return None

    def _create_terminal_from_shortcut(
        self,
        shortcut_name: str,
        target_path: str
    ) -> Optional[TerminalInfo]:
        """
        Create terminal information from shortcut

        Args:
            shortcut_name: Name of shortcut file
            target_path: Target path of shortcut

        Returns:
            Terminal information or None if not an MSYS2 terminal
        """
        # Remove .lnk extension
        name = shortcut_name[:-4] if shortcut_name.lower().endswith(".lnk") else shortcut_name

        # Determine terminal type from name
        terminal_type = None
        terminal_id = None
        architecture = "x64"
        environment = ""

        if "UCRT64" in name:
            terminal_type = TerminalType.MSYS2_UCRT64
            terminal_id = "ucrt64"
            environment = "UCRT64"
        elif "MINGW64" in name:
            terminal_type = TerminalType.MSYS2_MINGW64
            terminal_id = "mingw64"
            environment = "MINGW64"
        elif "MINGW32" in name:
            terminal_type = TerminalType.MSYS2_MINGW32
            terminal_id = "mingw32"
            architecture = "x86"
            environment = "MINGW32"
        elif "CLANG64" in name:
            terminal_type = TerminalType.MSYS2_CLANG64
            terminal_id = "clang64"
            environment = "CLANG64"
        elif "MSYS" in name and "UCRT64" not in name and "MINGW64" not in name and "MINGW32" not in name and "CLANG64" not in name:
            terminal_type = TerminalType.MSYS2_MSYS
            terminal_id = "msys"
            environment = "MSYS"
        else:
            # Not an MSYS2 terminal shortcut
            return None

        terminal = TerminalInfo(
            terminal_id=terminal_id,
            name=name,
            type=terminal_type,
            executable=target_path,
            arguments=[],
            architecture=architecture,
            environment=environment,
            capabilities=["msys2"],
            metadata={
                "shortcut_path": os.path.join(os.path.dirname(target_path), shortcut_name),
                "source": "start_menu"
            },
            recommended=False
        )

        return terminal

    def _get_msys2_paths(self) -> List[str]:
        """
        Get list of MSYS2 installation paths

        Returns:
            List of installation paths
        """
        paths: List[str] = []

        # Standard installation paths
        standard_paths = [
            r"C:\msys64",
            r"C:\msys32",
            r"C:\mingw64",
            r"C:\mingw",
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "msys64"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "msys32"),
        ]

        # Add paths that exist
        for path in standard_paths:
            if os.path.exists(path):
                paths.append(path)
                self._logger.debug(f"Found MSYS2 installation path: {path}")

        # Check PATH environment variable for MSYS2
        path_env = os.environ.get("PATH", "")
        for path_entry in path_env.split(os.pathsep):
            if "msys64" in path_entry.lower() or "msys32" in path_entry.lower():
                # Extract MSYS2 root from path
                msys2_root = self._extract_msys2_root(path_entry)
                if msys2_root and msys2_root not in paths:
                    paths.append(msys2_root)
                    self._logger.debug(f"Found MSYS2 from PATH: {msys2_root}")

        return paths

    def _extract_msys2_root(self, path: str) -> Optional[str]:
        """
        Extract MSYS2 root directory from a path

        Args:
            path: Path containing MSYS2

        Returns:
            MSYS2 root directory or None
        """
        # Normalize path
        path = os.path.normpath(path)

        # Look for common MSYS2 directories
        if "msys64" in path.lower():
            idx = path.lower().find("msys64")
            root = path[:idx + 7]  # Include "msys64"
            # Remove trailing separators
            return root.rstrip(os.sep)
        elif "msys32" in path.lower():
            idx = path.lower().find("msys32")
            root = path[:idx + 7]  # Include "msys32"
            # Remove trailing separators
            return root.rstrip(os.sep)

        return None
