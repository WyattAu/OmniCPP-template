"""
MSVC-Clang compiler detection and configuration
"""

import os
import re
import platform
from typing import Any
from .base import CompilerBase, CompilerInfo


class MSVCClangCompiler(CompilerBase):
    """MSVC-Clang compiler detection and configuration"""
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize MSVC-Clang compiler
        
        Args:
            version: Clang version (auto-detect if None)
        """
        super().__init__(version)
        self._clang_path: str | None = None
        self._msvc_path: str | None = None
    
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        return "MSVC-Clang"
    
    def get_version(self) -> str:
        """Get compiler version
        
        Returns:
            Compiler version string
        """
        if self._detected_version:
            return self._detected_version
        
        if self._version:
            return self._version
        
        # Auto-detect version
        version_info = self._detect_clang_version()
        if version_info:
            self._detected_version = version_info
            return version_info
        
        return "unknown"
    
    def get_flags(self, build_type: str) -> list[str]:
        """Get compiler flags
        
        Args:
            build_type: Build type (Debug, Release, RelWithDebInfo, MinSizeRel)
            
        Returns:
            List of compiler flags
        """
        flags: list[str] = []
        
        # Standard flags
        flags.extend([
            "-std=c++23",
            "-fno-exceptions",
            "-fcxx-exceptions",
            "-fms-extensions",
            "-fms-compatibility-version=19.33"
        ])
        
        # Build type specific flags
        build_type_lower = build_type.lower()
        if build_type_lower == "debug":
            flags.extend([
                "-O0",
                "-g",
                "-D_DEBUG"
            ])
        elif build_type_lower == "release":
            flags.extend([
                "-O3",
                "-DNDEBUG",
                "-flto"
            ])
        elif build_type_lower == "relwithdebinfo":
            flags.extend([
                "-O2",
                "-g",
                "-DNDEBUG"
            ])
        elif build_type_lower == "minsizerel":
            flags.extend([
                "-Os",
                "-DNDEBUG",
                "-flto"
            ])
        
        # Warning flags
        flags.extend([
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unused-parameter",
            "-Wno-missing-field-initializers"
        ])
        
        return flags
    
    def setup_environment(self) -> dict[str, str]:
        """Set up MSVC-Clang environment
        
        Returns:
            Dictionary of environment variables
        """
        env: dict[str, str] = {}
        
        if platform.system() != "Windows":
            return env
        
        # Set up MSVC environment
        msvc_env = self._setup_msvc_environment()
        env.update(msvc_env)
        
        # Add Clang-specific environment
        if self._clang_path:
            clang_dir = os.path.dirname(self._clang_path)
            env["PATH"] = f"{clang_dir};{env.get('PATH', os.environ.get('PATH', ''))}"
        
        return env
    
    def _detect_compiler(self) -> bool:
        """Internal method to detect MSVC-Clang compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        if platform.system() != "Windows":
            return False
        
        # Check for clang-cl.exe
        clang_path = self._find_clang_cl_exe()
        if not clang_path:
            return False
        
        self._clang_path = clang_path
        
        # Verify it works
        exit_code, stdout, stderr = self._run_command([clang_path, "--version"])
        return exit_code == 0 and ("clang" in stdout or "clang" in stderr)
    
    def _find_clang_cl_exe(self) -> str | None:
        """Find clang-cl.exe compiler
        
        Returns:
            Path to clang-cl.exe or None if not found
        """
        # Check PATH first
        exit_code, stdout, _ = self._run_command(["where", "clang-cl.exe"])
        if exit_code == 0 and stdout.strip():
            return stdout.strip().split("\n")[0]
        
        # Search in common locations
        clang_paths = [
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "LLVM",
                "bin",
                "clang-cl.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "LLVM",
                "bin",
                "clang-cl.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Microsoft Visual Studio",
                "2022",
                "Community",
                "VC",
                "Tools",
                "Llvm",
                "x64",
                "bin",
                "clang-cl.exe"
            )
        ]
        
        for path in clang_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _setup_msvc_environment(self) -> dict[str, str]:
        """Set up MSVC environment for Clang
        
        Returns:
            Dictionary of MSVC environment variables
        """
        env: dict[str, str] = {}
        
        # Find MSVC installation
        vswhere_path = self._find_vswhere()
        if not vswhere_path:
            return env
        
        exit_code, stdout, _ = self._run_command([
            vswhere_path,
            "-latest",
            "-property", "installationPath",
            "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
        ])
        
        if exit_code != 0 or not stdout.strip():
            return env
        
        installation = stdout.strip()
        self._msvc_path = installation
        
        # Set up environment variables
        vcvars_path = self._find_vcvars_bat(installation)
        if vcvars_path:
            env.update({
                "VCINSTALLDIR": installation,
                "VSINSTALLDIR": os.path.dirname(installation),
                "WindowsSdkDir": self._find_windows_sdk()
            })
        
        return env
    
    def _find_vswhere(self) -> str:
        """Find vswhere.exe utility
        
        Returns:
            Path to vswhere.exe or empty string if not found
        """
        vswhere_paths = [
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Microsoft Visual Studio",
                "Installer",
                "vswhere.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Microsoft Visual Studio",
                "Installer",
                "vswhere.exe"
            )
        ]
        
        for path in vswhere_paths:
            if os.path.exists(path):
                return path
        
        return ""
    
    def _find_vcvars_bat(self, installation: str) -> str | None:
        """Find vcvarsall.bat
        
        Args:
            installation: MSVC installation path
            
        Returns:
            Path to vcvarsall.bat or None if not found
        """
        vcvars_paths = [
            os.path.join(installation, "VC", "Auxiliary", "Build", "vcvarsall.bat"),
            os.path.join(installation, "VC", "vcvarsall.bat")
        ]
        
        for path in vcvars_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _find_windows_sdk(self) -> str:
        """Find Windows SDK path
        
        Returns:
            Windows SDK path or empty string if not found
        """
        sdk_path = os.environ.get("WindowsSdkDir")
        if sdk_path and os.path.exists(sdk_path):
            return sdk_path
        
        import glob
        sdk_patterns = [
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Windows Kits",
                "10",
                "Include",
                "*"
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Windows Kits",
                "10",
                "Include",
                "*"
            )
        ]
        
        for pattern in sdk_patterns:
            matches = glob.glob(pattern)
            if matches:
                return os.path.dirname(os.path.dirname(matches[0]))
        
        return ""
    
    def _detect_clang_version(self) -> str | None:
        """Detect Clang version
        
        Returns:
            Version string or None if not detected
        """
        clang_path = self._find_clang_cl_exe()
        if not clang_path:
            return None
        
        # Run clang-cl.exe to get version
        exit_code, stdout, stderr = self._run_command([clang_path, "--version"])
        output = stdout + stderr
        
        # Parse version from output
        # Example: "clang version 18.1.0"
        match = re.search(r"clang version (\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
        
        return None
