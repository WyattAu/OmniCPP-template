"""
MSVC Terminal Detector

This module provides comprehensive detection of Microsoft Visual C++ Developer Command Prompts
and all architecture-specific terminal variants.
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


class MSVCTerminalDetector(ITerminalDetector):
    """Detector for Microsoft Visual C++ Developer Command Prompts"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize MSVC terminal detector

        Args:
            logger: Logger instance for logging detection steps
        """
        self._logger = logger or logging.getLogger(__name__)
        self._detected_terminals: List[TerminalInfo] = []
        self._installation_paths: List[str] = self._get_installation_paths()

    def detect(self) -> List[TerminalInfo]:
        """
        Detect all MSVC Developer Command Prompts

        Returns:
            List of detected terminal information
        """
        self._logger.info("Starting MSVC terminal detection")
        self._detected_terminals.clear()

        # Detect all terminal types
        terminals: List[TerminalInfo] = []

        # Detect Developer Command Prompt
        dev_cmd = self._detect_developer_cmd()
        if dev_cmd:
            terminals.append(dev_cmd)
            self._logger.info(f"Detected Developer Command Prompt: {dev_cmd.executable}")

        # Detect Native Tools
        native_terminals = self._detect_native_tools()
        terminals.extend(native_terminals)
        self._logger.info(f"Detected {len(native_terminals)} native tool terminals")

        # Detect Cross Tools
        cross_terminals = self._detect_cross_tools()
        terminals.extend(cross_terminals)
        self._logger.info(f"Detected {len(cross_terminals)} cross tool terminals")

        # Detect Start Menu shortcuts
        shortcut_terminals = self._detect_shortcuts()
        terminals.extend(shortcut_terminals)
        self._logger.info(f"Detected {len(shortcut_terminals)} shortcut terminals")

        self._detected_terminals = terminals
        self._logger.info(f"Total detected MSVC terminals: {len(terminals)}")

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

        # Try to execute the terminal
        try:
            result = subprocess.run(
                [terminal_info.executable, "/?"],
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

    def _detect_developer_cmd(self) -> Optional[TerminalInfo]:
        """
        Detect MSVC Developer Command Prompt

        Returns:
            Terminal information or None if not found
        """
        self._logger.debug("Detecting Developer Command Prompt")

        for installation_path in self._installation_paths:
            # Look for VsDevCmd.bat
            vsdevcmd_path = os.path.join(
                installation_path,
                "Common7",
                "Tools",
                "VsDevCmd.bat"
            )

            if os.path.exists(vsdevcmd_path):
                self._logger.debug(f"Found VsDevCmd.bat: {vsdevcmd_path}")

                # Determine VS version from path
                version = self._extract_version_from_path(installation_path)

                terminal = TerminalInfo(
                    terminal_id="developer_cmd",
                    name=f"Developer Command Prompt for VS {version}",
                    type=TerminalType.MSVC_DEVELOPER_CMD,
                    executable=vsdevcmd_path,
                    arguments=[],
                    architecture="x64",
                    environment="msvc",
                    capabilities=["msvc", "developer_tools"],
                    metadata={
                        "installation_path": installation_path,
                        "version": version,
                        "batch_file": "VsDevCmd.bat"
                    },
                    recommended=True
                )

                return terminal

        self._logger.warning("Developer Command Prompt not found")
        return None

    def _detect_native_tools(self) -> List[TerminalInfo]:
        """
        Detect MSVC Native Tools Command Prompts

        Returns:
            List of detected terminal information
        """
        self._logger.debug("Detecting Native Tools Command Prompts")

        terminals: List[TerminalInfo] = []

        # Native tool configurations
        native_configs = [
            {
                "terminal_id": "x64_native",
                "name": "x64 Native Tools Command Prompt",
                "type": TerminalType.MSVC_X64_NATIVE,
                "architecture": "x64",
                "batch_file": "vcvars64.bat",
                "recommended": True
            },
            {
                "terminal_id": "x86_native",
                "name": "x86 Native Tools Command Prompt",
                "type": TerminalType.MSVC_X86_NATIVE,
                "architecture": "x86",
                "batch_file": "vcvars32.bat",
                "recommended": False
            }
        ]

        for config in native_configs:
            terminal = self._find_native_terminal(config)
            if terminal:
                terminals.append(terminal)
                self._logger.debug(f"Found {config['name']}: {terminal.executable}")

        return terminals

    def _detect_cross_tools(self) -> List[TerminalInfo]:
        """
        Detect MSVC Cross Tools Command Prompts

        Returns:
            List of detected terminal information
        """
        self._logger.debug("Detecting Cross Tools Command Prompts")

        terminals: List[TerminalInfo] = []

        # Cross tool configurations
        cross_configs = [
            {
                "terminal_id": "x86_x64_cross",
                "name": "x86_x64 Cross Tools Command Prompt",
                "type": TerminalType.MSVC_X86_X64_CROSS,
                "architecture": "x64",
                "batch_file": "vcvarsx86_amd64.bat",
                "recommended": False
            },
            {
                "terminal_id": "x64_x86_cross",
                "name": "x64_x86 Cross Tools Command Prompt",
                "type": TerminalType.MSVC_X64_X86_CROSS,
                "architecture": "x86",
                "batch_file": "vcvarsamd64_x86.bat",
                "recommended": False
            },
            {
                "terminal_id": "x64_arm_cross",
                "name": "x64_arm Cross Tools Command Prompt",
                "type": TerminalType.MSVC_X64_ARM_CROSS,
                "architecture": "arm",
                "batch_file": "vcvarsamd64_arm.bat",
                "recommended": False
            },
            {
                "terminal_id": "x64_arm64_cross",
                "name": "x64_arm64 Cross Tools Command Prompt",
                "type": TerminalType.MSVC_X64_ARM64_CROSS,
                "architecture": "arm64",
                "batch_file": "vcvarsamd64_arm64.bat",
                "recommended": False
            }
        ]

        for config in cross_configs:
            terminal = self._find_cross_terminal(config)
            if terminal:
                terminals.append(terminal)
                self._logger.debug(f"Found {config['name']}: {terminal.executable}")

        return terminals

    def _detect_shortcuts(self) -> List[TerminalInfo]:
        """
        Detect MSVC terminal shortcuts from Start Menu

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

            # Look for Visual Studio folders
            for item in os.listdir(start_menu_path):
                if "Visual Studio" in item:
                    vs_folder = os.path.join(start_menu_path, item)
                    if os.path.isdir(vs_folder):
                        # Look for terminal shortcuts
                        shortcut_terminals = self._scan_vs_folder(vs_folder)
                        terminals.extend(shortcut_terminals)

        self._logger.debug(f"Found {len(terminals)} Start Menu shortcuts")
        return terminals

    def _find_native_terminal(self, config: Dict[str, any]) -> Optional[TerminalInfo]:
        """
        Find a native tool terminal

        Args:
            config: Terminal configuration

        Returns:
            Terminal information or None if not found
        """
        for installation_path in self._installation_paths:
            # Look for batch file in Auxiliary/Build
            batch_path = os.path.join(
                installation_path,
                "VC",
                "Auxiliary",
                "Build",
                config["batch_file"]
            )

            if os.path.exists(batch_path):
                version = self._extract_version_from_path(installation_path)

                terminal = TerminalInfo(
                    terminal_id=config["terminal_id"],
                    name=config["name"],
                    type=config["type"],
                    executable=batch_path,
                    arguments=[],
                    architecture=config["architecture"],
                    environment="msvc",
                    capabilities=["msvc", "native_tools"],
                    metadata={
                        "installation_path": installation_path,
                        "version": version,
                        "batch_file": config["batch_file"]
                    },
                    recommended=config["recommended"]
                )

                return terminal

        return None

    def _find_cross_terminal(self, config: Dict[str, Any]) -> Optional[TerminalInfo]:
        """
        Find a cross tool terminal

        Args:
            config: Terminal configuration

        Returns:
            Terminal information or None if not found
        """
        for installation_path in self._installation_paths:
            # Look for batch file in Auxiliary/Build
            batch_path = os.path.join(
                installation_path,
                "VC",
                "Auxiliary",
                "Build",
                config["batch_file"]
            )

            if os.path.exists(batch_path):
                version = self._extract_version_from_path(installation_path)

                terminal = TerminalInfo(
                    terminal_id=config["terminal_id"],
                    name=config["name"],
                    type=config["type"],
                    executable=batch_path,
                    arguments=[],
                    architecture=config["architecture"],
                    environment="msvc",
                    capabilities=["msvc", "cross_tools"],
                    metadata={
                        "installation_path": installation_path,
                        "version": version,
                        "batch_file": config["batch_file"]
                    },
                    recommended=config["recommended"]
                )

                return terminal

        return None

    def _scan_vs_folder(self, vs_folder: str) -> List[TerminalInfo]:
        """
        Scan Visual Studio folder for terminal shortcuts

        Args:
            vs_folder: Path to Visual Studio folder

        Returns:
            List of detected terminal information
        """
        terminals: List[TerminalInfo] = []

        try:
            for item in os.listdir(vs_folder):
                item_path = os.path.join(vs_folder, item)

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
            self._logger.warning(f"Error scanning VS folder {vs_folder}: {e}")

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
            Terminal information or None if not an MSVC terminal
        """
        # Remove .lnk extension
        name = shortcut_name[:-4] if shortcut_name.lower().endswith(".lnk") else shortcut_name

        # Determine terminal type from name
        terminal_type = None
        terminal_id = None
        architecture = "x64"

        if "Developer" in name:
            terminal_type = TerminalType.MSVC_DEVELOPER_CMD
            terminal_id = "developer_cmd"
        elif "x64 Native" in name:
            terminal_type = TerminalType.MSVC_X64_NATIVE
            terminal_id = "x64_native"
        elif "x86 Native" in name:
            terminal_type = TerminalType.MSVC_X86_NATIVE
            terminal_id = "x86_native"
            architecture = "x86"
        elif "x86_x64" in name:
            terminal_type = TerminalType.MSVC_X86_X64_CROSS
            terminal_id = "x86_x64_cross"
        elif "x64_x86" in name:
            terminal_type = TerminalType.MSVC_X64_X86_CROSS
            terminal_id = "x64_x86_cross"
            architecture = "x86"
        elif "x64_arm" in name and "arm64" not in name:
            terminal_type = TerminalType.MSVC_X64_ARM_CROSS
            terminal_id = "x64_arm_cross"
            architecture = "arm"
        elif "x64_arm64" in name:
            terminal_type = TerminalType.MSVC_X64_ARM64_CROSS
            terminal_id = "x64_arm64_cross"
            architecture = "arm64"
        else:
            # Not an MSVC terminal shortcut
            return None

        terminal = TerminalInfo(
            terminal_id=terminal_id,
            name=name,
            type=terminal_type,
            executable=target_path,
            arguments=[],
            architecture=architecture,
            environment="msvc",
            capabilities=["msvc"],
            metadata={
                "shortcut_path": os.path.join(os.path.dirname(target_path), shortcut_name),
                "source": "start_menu"
            },
            recommended=False
        )

        return terminal

    def _extract_version_from_path(self, path: str) -> str:
        """
        Extract Visual Studio version from installation path

        Args:
            path: Installation path

        Returns:
            Version string (e.g., "2022", "2019")
        """
        # Look for version in path
        if "2022" in path:
            return "2022"
        elif "2019" in path:
            return "2019"
        elif "2017" in path:
            return "2017"
        else:
            return "unknown"

    def _get_installation_paths(self) -> List[str]:
        """
        Get list of Visual Studio installation paths

        Returns:
            List of installation paths
        """
        paths: List[str] = []

        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

        # Standard installation paths
        standard_paths = [
            os.path.join(program_files, r"Microsoft Visual Studio\2022"),
            os.path.join(program_files, r"Microsoft Visual Studio\2019"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2022"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2019"),
            os.path.join(program_files, r"Microsoft Visual Studio\2022\BuildTools"),
            os.path.join(program_files, r"Microsoft Visual Studio\2019\BuildTools"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2022\BuildTools"),
            os.path.join(program_files_x86, r"Microsoft Visual Studio\2019\BuildTools"),
        ]

        # Add paths that exist
        for path in standard_paths:
            if os.path.exists(path):
                paths.append(path)
                self._logger.debug(f"Found installation path: {path}")

        # Try to detect via vswhere
        vswhere_paths = self._get_vswhere_paths()
        for vswhere_path in vswhere_paths:
            if os.path.exists(vswhere_path):
                try:
                    result = subprocess.run(
                        [vswhere_path, "-all", "-property", "installationPath"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            line = line.strip()
                            if line and line not in paths:
                                paths.append(line)
                                self._logger.debug(f"Found vswhere path: {line}")
                except Exception as e:
                    self._logger.warning(f"Error running vswhere: {e}")

        return paths

    def _get_vswhere_paths(self) -> List[str]:
        """
        Get list of possible vswhere.exe paths

        Returns:
            List of vswhere.exe paths
        """
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        program_data = os.environ.get("ProgramData", r"C:\ProgramData")

        return [
            os.path.join(program_files_x86, r"Microsoft Visual Studio\Installer\vswhere.exe"),
            os.path.join(program_data, r"Microsoft Visual Studio\Installer\vswhere.exe"),
        ]
