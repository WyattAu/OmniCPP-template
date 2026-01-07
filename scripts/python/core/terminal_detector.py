"""
Terminal Detector - Detect available developer terminals

This module provides terminal detection for PowerShell, CMD, Git Bash,
WSL, Bash, and Zsh on Windows and Linux platforms.
"""

import os
import shutil
import platform
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TerminalInfo:
    """Terminal information data class."""
    
    name: str
    path: str
    type: str  # powershell, cmd, bash, zsh, wsl


class TerminalDetector:
    """Detect available developer terminals."""
    
    def __init__(self) -> None:
        """Initialize terminal detector."""
        self.system = platform.system()
    
    def detect(self) -> List[TerminalInfo]:
        """Detect available terminals.
        
        Returns:
            List of detected terminals
        """
        terminals = []
        
        if self.system == "Windows":
            terminals.extend(self._detect_windows_terminals())
        elif self.system == "Linux":
            terminals.extend(self._detect_linux_terminals())
        
        return terminals
    
    def get_default(self) -> Optional[TerminalInfo]:
        """Get default terminal.
        
        Returns:
            Default terminal or None
        """
        terminals = self.detect()
        
        if not terminals:
            return None
        
        # Prefer PowerShell on Windows, Bash on Linux
        if self.system == "Windows":
            for terminal in terminals:
                if terminal.type == "powershell":
                    return terminal
            # Fallback to CMD
            for terminal in terminals:
                if terminal.type == "cmd":
                    return terminal
        elif self.system == "Linux":
            for terminal in terminals:
                if terminal.type == "bash":
                    return terminal
            # Fallback to Zsh
            for terminal in terminals:
                if terminal.type == "zsh":
                    return terminal
        
        return terminals[0]
    
    def _detect_windows_terminals(self) -> List[TerminalInfo]:
        """Detect Windows terminals.
        
        Returns:
            List of detected Windows terminals
        """
        terminals = []
        
        # Detect PowerShell
        powershell_path = shutil.which("powershell.exe")
        if powershell_path:
            terminals.append(TerminalInfo(
                name="PowerShell",
                path=powershell_path,
                type="powershell"
            ))
        
        # Detect PowerShell Core (pwsh)
        pwsh_path = shutil.which("pwsh.exe")
        if pwsh_path:
            terminals.append(TerminalInfo(
                name="PowerShell Core",
                path=pwsh_path,
                type="powershell"
            ))
        
        # Detect CMD
        cmd_path = shutil.which("cmd.exe")
        if cmd_path:
            terminals.append(TerminalInfo(
                name="Command Prompt",
                path=cmd_path,
                type="cmd"
            ))
        
        # Detect Git Bash
        git_bash_paths = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Git\bin\bash.exe"),
        ]
        
        for bash_path in git_bash_paths:
            if os.path.exists(bash_path):
                terminals.append(TerminalInfo(
                    name="Git Bash",
                    path=bash_path,
                    type="bash"
                ))
                break
        
        # Detect WSL
        wsl_path = shutil.which("wsl.exe")
        if wsl_path:
            terminals.append(TerminalInfo(
                name="Windows Subsystem for Linux",
                path=wsl_path,
                type="wsl"
            ))
        
        return terminals
    
    def _detect_linux_terminals(self) -> List[TerminalInfo]:
        """Detect Linux terminals.
        
        Returns:
            List of detected Linux terminals
        """
        terminals = []
        
        # Detect Bash
        bash_path = shutil.which("bash")
        if bash_path:
            terminals.append(TerminalInfo(
                name="Bash",
                path=bash_path,
                type="bash"
            ))
        
        # Detect Zsh
        zsh_path = shutil.which("zsh")
        if zsh_path:
            terminals.append(TerminalInfo(
                name="Zsh",
                path=zsh_path,
                type="zsh"
            ))
        
        return terminals
    
    def find_terminal(self, terminal_type: str) -> Optional[TerminalInfo]:
        """Find terminal by type.
        
        Args:
            terminal_type: Terminal type to find
            
        Returns:
            Terminal info or None
        """
        terminals = self.detect()
        
        for terminal in terminals:
            if terminal.type == terminal_type:
                return terminal
        
        return None
