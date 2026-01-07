"""
MSVC compiler detection and configuration
"""

import os
import re
import platform
from typing import Any
from .base import CompilerBase, CompilerInfo


class MSVCCompiler(CompilerBase):
    """Microsoft Visual C++ compiler detection and configuration"""
    
    def __init__(self, version: str | None = None) -> None:
        """Initialize MSVC compiler
        
        Args:
            version: MSVC version (auto-detect if None)
        """
        super().__init__(version)
        self._vswhere_path: str = self._find_vswhere()
        self._installation_path: str | None = None
    
    def get_name(self) -> str:
        """Get compiler name
        
        Returns:
            Compiler name
        """
        return "MSVC"
    
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
        version_info = self._detect_msvc_version()
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
            "/std:c++23",
            "/permissive-",
            "/Zc:__cplusplus",
            "/EHsc",
            "/GR-"
        ])
        
        # Build type specific flags
        build_type_lower = build_type.lower()
        if build_type_lower == "debug":
            flags.extend([
                "/Od",
                "/MDd",
                "/Zi",
                "/RTC1"
            ])
        elif build_type_lower == "release":
            flags.extend([
                "/O2",
                "/MD",
                "/DNDEBUG",
                "/GL"
            ])
        elif build_type_lower == "relwithdebinfo":
            flags.extend([
                "/O2",
                "/MD",
                "/Zi",
                "/DNDEBUG"
            ])
        elif build_type_lower == "minsizerel":
            flags.extend([
                "/O1",
                "/MD",
                "/DNDEBUG",
                "/GL"
            ])
        
        # Warning flags
        flags.extend([
            "/W4",
            "/WX",
            "/wd4100",  # Unreferenced formal parameter
            "/wd4201",  # Nameless struct/union
            "/wd4244",  # Conversion from type1 to type2
            "/wd4267"   # Conversion from size_t to type
        ])
        
        return flags
    
    def setup_environment(self) -> dict[str, str]:
        """Set up MSVC environment
        
        Returns:
            Dictionary of environment variables
        """
        env: dict[str, str] = {}
        
        if platform.system() != "Windows":
            return env
        
        # Find MSVC installation
        installation = self._find_msvc_installation()
        if not installation:
            return env
        
        self._installation_path = installation
        
        # Set up environment variables
        vcvars_path = self._find_vcvars_bat(installation)
        if vcvars_path:
            # Note: In practice, you'd need to run vcvarsall.bat
            # This is a simplified version that sets key variables
            env.update({
                "VCINSTALLDIR": installation,
                "VSINSTALLDIR": os.path.dirname(installation),
                "WindowsSdkDir": self._find_windows_sdk(),
                "INCLUDE": self._build_include_path(installation),
                "LIB": self._build_lib_path(installation)
            })
        
        return env
    
    def _detect_compiler(self) -> bool:
        """Internal method to detect MSVC compiler
        
        Returns:
            True if compiler is detected, False otherwise
        """
        if platform.system() != "Windows":
            return False
        
        # Check for cl.exe
        cl_path = self._find_cl_exe()
        if not cl_path:
            return False
        
        self._compiler_path = cl_path
        
        # Verify it works
        exit_code, stdout, stderr = self._run_command([cl_path, "/?"])
        return exit_code == 0 or "Microsoft" in stdout or "Microsoft" in stderr
    
    def _find_vswhere(self) -> str:
        """Find vswhere.exe utility
        
        Returns:
            Path to vswhere.exe or empty string if not found
        """
        if platform.system() != "Windows":
            return ""
        
        # Common vswhere locations
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
    
    def _find_msvc_installation(self) -> str | None:
        """Find MSVC installation path
        
        Returns:
            Installation path or None if not found
        """
        if not self._vswhere_path:
            return None
        
        # Use vswhere to find installation
        exit_code, stdout, _ = self._run_command([
            self._vswhere_path,
            "-latest",
            "-property", "installationPath",
            "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
        ])
        
        if exit_code == 0 and stdout.strip():
            return stdout.strip()
        
        return None
    
    def _find_cl_exe(self) -> str | None:
        """Find cl.exe compiler
        
        Returns:
            Path to cl.exe or None if not found
        """
        # Check PATH first
        exit_code, stdout, _ = self._run_command(["where", "cl.exe"])
        if exit_code == 0 and stdout.strip():
            return stdout.strip().split("\n")[0]
        
        # Search in common locations
        installation = self._find_msvc_installation()
        if installation:
            cl_paths = [
                os.path.join(installation, "VC", "Tools", "MSVC", "*", "bin", "Hostx64", "x64", "cl.exe"),
                os.path.join(installation, "VC", "Tools", "MSVC", "*", "bin", "Hostx86", "x86", "cl.exe")
            ]
            
            import glob
            for pattern in cl_paths:
                matches = glob.glob(pattern)
                if matches:
                    return matches[0]
        
        return None
    
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
        # Check environment variables
        sdk_path = os.environ.get("WindowsSdkDir")
        if sdk_path and os.path.exists(sdk_path):
            return sdk_path
        
        # Check registry (simplified)
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
    
    def _build_include_path(self, installation: str) -> str:
        """Build INCLUDE path for MSVC
        
        Args:
            installation: MSVC installation path
            
        Returns:
            INCLUDE path string
        """
        import glob
        
        paths: list[str] = []
        
        # MSVC includes
        vc_include = os.path.join(installation, "VC", "Tools", "MSVC", "*", "include")
        matches = glob.glob(vc_include)
        if matches:
            paths.append(matches[0])
        
        # Windows SDK includes
        sdk_path = self._find_windows_sdk()
        if sdk_path:
            paths.extend([
                os.path.join(sdk_path, "Include", "um"),
                os.path.join(sdk_path, "Include", "shared"),
                os.path.join(sdk_path, "Include", "ucrt")
            ])
        
        return ";".join(paths)
    
    def _build_lib_path(self, installation: str) -> str:
        """Build LIB path for MSVC
        
        Args:
            installation: MSVC installation path
            
        Returns:
            LIB path string
        """
        import glob
        
        paths: list[str] = []
        
        # MSVC libs
        vc_lib = os.path.join(installation, "VC", "Tools", "MSVC", "*", "lib", "x64")
        matches = glob.glob(vc_lib)
        if matches:
            paths.append(matches[0])
        
        # Windows SDK libs
        sdk_path = self._find_windows_sdk()
        if sdk_path:
            paths.extend([
                os.path.join(sdk_path, "Lib", "um", "x64"),
                os.path.join(sdk_path, "Lib", "ucrt", "x64")
            ])
        
        return ";".join(paths)
    
    def _detect_msvc_version(self) -> str | None:
        """Detect MSVC version
        
        Returns:
            Version string or None if not detected
        """
        cl_path = self._find_cl_exe()
        if not cl_path:
            return None
        
        # Run cl.exe to get version
        exit_code, stdout, stderr = self._run_command([cl_path])
        output = stdout + stderr
        
        # Parse version from output
        # Example: "Microsoft (R) C/C++ Optimizing Compiler Version 19.40.33807 for x64"
        match = re.search(r"Version (\d+\.\d+)", output)
        if match:
            return match.group(1)
        
        return None
