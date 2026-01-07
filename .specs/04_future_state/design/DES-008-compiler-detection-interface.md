# DES-008: Compiler Detection Interface

## Overview
Defines the compiler detection interface for identifying available compilers, their versions, and capabilities.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import subprocess
import re
from pathlib import Path

class CompilerType(Enum):
    """Compiler types"""
    GCC = "gcc"
    CLANG = "clang"
    MSVC = "msvc"
    MINGW = "mingw"
    UNKNOWN = "unknown"

class CompilerStatus(Enum):
    """Compiler status"""
    AVAILABLE = "available"
    NOT_FOUND = "not_found"
    INCOMPATIBLE_VERSION = "incompatible_version"
    MISSING_DEPENDENCIES = "missing_dependencies"

@dataclass
class CompilerInfo:
    """Compiler information"""
    compiler_type: CompilerType
    executable: str
    version: str
    version_tuple: Tuple[int, int, int]
    target: str
    is_default: bool
    status: CompilerStatus
    capabilities: List[str]
    flags: List[str]
    include_paths: List[str]
    library_paths: List[str]

@dataclass
class CompilerCapability:
    """Compiler capability"""
    name: str
    supported: bool
    version_required: Optional[str] = None
    flags_required: Optional[List[str]] = None

class ICompilerDetector(ABC):
    """Interface for compiler detection"""

    @abstractmethod
    def detect_compilers(self) -> List[CompilerInfo]:
        """Detect all available compilers"""
        pass

    @abstractmethod
    def detect_compiler(self, compiler_type: CompilerType) -> Optional[CompilerInfo]:
        """Detect specific compiler"""
        pass

    @abstractmethod
    def get_default_compiler(self) -> Optional[CompilerInfo]:
        """Get default compiler"""
        pass

    @abstractmethod
    def get_compiler_version(self, executable: str) -> Optional[str]:
        """Get compiler version"""
        pass

    @abstractmethod
    def check_compiler_capability(self, compiler_info: CompilerInfo, capability: str) -> bool:
        """Check if compiler supports a capability"""
        pass

    @abstractmethod
    def get_compiler_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get compiler flags"""
        pass

    @abstractmethod
    def validate_compiler(self, compiler_info: CompilerInfo) -> bool:
        """Validate compiler"""
        pass

class CompilerDetector(ICompilerDetector):
    """Implementation of compiler detector"""

    def __init__(self, min_gcc_version: Tuple[int, int, int] = (9, 0, 0),
                 min_clang_version: Tuple[int, int, int] = (10, 0, 0),
                 min_msvc_version: int = 193) -> None:
        """Initialize compiler detector"""
        self._min_gcc_version = min_gcc_version
        self._min_clang_version = min_clang_version
        self._min_msvc_version = min_msvc_version
        self._detected_compilers: Optional[List[CompilerInfo]] = None
        self._cache_enabled = True

    def detect_compilers(self) -> List[CompilerInfo]:
        """Detect all available compilers"""
        if self._cache_enabled and self._detected_compilers:
            return self._detected_compilers

        compilers = []

        # Detect GCC
        gcc_info = self._detect_gcc()
        if gcc_info:
            compilers.append(gcc_info)

        # Detect Clang
        clang_info = self._detect_clang()
        if clang_info:
            compilers.append(clang_info)

        # Detect MSVC (Windows only)
        msvc_info = self._detect_msvc()
        if msvc_info:
            compilers.append(msvc_info)

        # Detect MinGW (Windows only)
        mingw_info = self._detect_mingw()
        if mingw_info:
            compilers.append(mingw_info)

        # Set default compiler
        if compilers:
            compilers[0].is_default = True

        self._detected_compilers = compilers
        return compilers

    def detect_compiler(self, compiler_type: CompilerType) -> Optional[CompilerInfo]:
        """Detect specific compiler"""
        if compiler_type == CompilerType.GCC:
            return self._detect_gcc()
        elif compiler_type == CompilerType.CLANG:
            return self._detect_clang()
        elif compiler_type == CompilerType.MSVC:
            return self._detect_msvc()
        elif compiler_type == CompilerType.MINGW:
            return self._detect_mingw()
        else:
            return None

    def get_default_compiler(self) -> Optional[CompilerInfo]:
        """Get default compiler"""
        compilers = self.detect_compilers()
        return compilers[0] if compilers else None

    def get_compiler_version(self, executable: str) -> Optional[str]:
        """Get compiler version"""
        try:
            result = subprocess.run(
                [executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return self._parse_version(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def check_compiler_capability(self, compiler_info: CompilerInfo, capability: str) -> bool:
        """Check if compiler supports a capability"""
        capabilities = self._get_compiler_capabilities(compiler_info)
        return capability in capabilities

    def get_compiler_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get compiler flags"""
        if compiler_info.compiler_type == CompilerType.GCC:
            return self._get_gcc_flags(compiler_info)
        elif compiler_info.compiler_type == CompilerType.CLANG:
            return self._get_clang_flags(compiler_info)
        elif compiler_info.compiler_type == CompilerType.MSVC:
            return self._get_msvc_flags(compiler_info)
        elif compiler_info.compiler_type == CompilerType.MINGW:
            return self._get_mingw_flags(compiler_info)
        else:
            return []

    def validate_compiler(self, compiler_info: CompilerInfo) -> bool:
        """Validate compiler"""
        if compiler_info.status != CompilerStatus.AVAILABLE:
            return False

        # Check version requirements
        if compiler_info.compiler_type == CompilerType.GCC:
            return compiler_info.version_tuple >= self._min_gcc_version
        elif compiler_info.compiler_type == CompilerType.CLANG:
            return compiler_info.version_tuple >= self._min_clang_version
        elif compiler_info.compiler_type == CompilerType.MSVC:
            return int(compiler_info.version) >= self._min_msvc_version

        return True

    def _detect_gcc(self) -> Optional[CompilerInfo]:
        """Detect GCC compiler"""
        executable = self._find_executable("gcc")
        if not executable:
            return None

        version = self.get_compiler_version(executable)
        if not version:
            return None

        version_tuple = self._parse_version_tuple(version)

        # Check minimum version
        if version_tuple < self._min_gcc_version:
            return CompilerInfo(
                compiler_type=CompilerType.GCC,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.INCOMPATIBLE_VERSION,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )

        capabilities = self._get_compiler_capabilities(
            CompilerInfo(
                compiler_type=CompilerType.GCC,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )
        )

        return CompilerInfo(
            compiler_type=CompilerType.GCC,
            executable=executable,
            version=version,
            version_tuple=version_tuple,
            target=self._get_compiler_target(executable),
            is_default=False,
            status=CompilerStatus.AVAILABLE,
            capabilities=capabilities,
            flags=self._get_gcc_flags(CompilerInfo(
                compiler_type=CompilerType.GCC,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )),
            include_paths=self._get_include_paths(executable),
            library_paths=self._get_library_paths(executable)
        )

    def _detect_clang(self) -> Optional[CompilerInfo]:
        """Detect Clang compiler"""
        executable = self._find_executable("clang")
        if not executable:
            return None

        version = self.get_compiler_version(executable)
        if not version:
            return None

        version_tuple = self._parse_version_tuple(version)

        # Check minimum version
        if version_tuple < self._min_clang_version:
            return CompilerInfo(
                compiler_type=CompilerType.CLANG,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.INCOMPATIBLE_VERSION,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )

        capabilities = self._get_compiler_capabilities(
            CompilerInfo(
                compiler_type=CompilerType.CLANG,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )
        )

        return CompilerInfo(
            compiler_type=CompilerType.CLANG,
            executable=executable,
            version=version,
            version_tuple=version_tuple,
            target=self._get_compiler_target(executable),
            is_default=False,
            status=CompilerStatus.AVAILABLE,
            capabilities=capabilities,
            flags=self._get_clang_flags(CompilerInfo(
                compiler_type=CompilerType.CLANG,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )),
            include_paths=self._get_include_paths(executable),
            library_paths=self._get_library_paths(executable)
        )

    def _detect_msvc(self) -> Optional[CompilerInfo]:
        """Detect MSVC compiler"""
        # MSVC detection is platform-specific
        import os
        if os.name != 'nt':
            return None

        # Check for Visual Studio environment
        vs_install_dir = os.environ.get('VSINSTALLDIR')
        if not vs_install_dir:
            return None

        # Find cl.exe
        cl_path = self._find_executable("cl")
        if not cl_path:
            return None

        version = os.environ.get('VisualStudioVersion', 'unknown')

        return CompilerInfo(
            compiler_type=CompilerType.MSVC,
            executable=cl_path,
            version=version,
            version_tuple=(int(version) if version.isdigit() else 0, 0, 0),
            target=self._get_msvc_target(),
            is_default=False,
            status=CompilerStatus.AVAILABLE,
            capabilities=self._get_msvc_capabilities(),
            flags=self._get_msvc_flags(CompilerInfo(
                compiler_type=CompilerType.MSVC,
                executable=cl_path,
                version=version,
                version_tuple=(int(version) if version.isdigit() else 0, 0, 0),
                target=self._get_msvc_target(),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )),
            include_paths=self._get_msvc_include_paths(),
            library_paths=self._get_msvc_library_paths()
        )

    def _detect_mingw(self) -> Optional[CompilerInfo]:
        """Detect MinGW compiler"""
        executable = self._find_executable("mingw32-gcc")
        if not executable:
            executable = self._find_executable("x86_64-w64-mingw32-gcc")

        if not executable:
            return None

        version = self.get_compiler_version(executable)
        if not version:
            return None

        version_tuple = self._parse_version_tuple(version)

        return CompilerInfo(
            compiler_type=CompilerType.MINGW,
            executable=executable,
            version=version,
            version_tuple=version_tuple,
            target=self._get_compiler_target(executable),
            is_default=False,
            status=CompilerStatus.AVAILABLE,
            capabilities=self._get_gcc_capabilities(),
            flags=self._get_mingw_flags(CompilerInfo(
                compiler_type=CompilerType.MINGW,
                executable=executable,
                version=version,
                version_tuple=version_tuple,
                target=self._get_compiler_target(executable),
                is_default=False,
                status=CompilerStatus.AVAILABLE,
                capabilities=[],
                flags=[],
                include_paths=[],
                library_paths=[]
            )),
            include_paths=self._get_include_paths(executable),
            library_paths=self._get_library_paths(executable)
        )

    def _find_executable(self, name: str) -> Optional[str]:
        """Find executable in PATH"""
        from shutil import which
        return which(name)

    def _parse_version(self, output: str) -> Optional[str]:
        """Parse version from compiler output"""
        # Try common version patterns
        patterns = [
            r'gcc.*?(\d+\.\d+\.\d+)',
            r'clang.*?(\d+\.\d+\.\d+)',
            r'Microsoft.*?(\d+\.\d+\.\d+)',
            r'version\s+(\d+\.\d+\.\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _parse_version_tuple(self, version: str) -> Tuple[int, int, int]:
        """Parse version string to tuple"""
        parts = version.split('.')
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return (major, minor, patch)

    def _get_compiler_target(self, executable: str) -> str:
        """Get compiler target"""
        try:
            result = subprocess.run(
                [executable, "-dumpmachine"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return "unknown"

    def _get_include_paths(self, executable: str) -> List[str]:
        """Get compiler include paths"""
        try:
            result = subprocess.run(
                [executable, "-E", "-x", "c++", "-v", "-"],
                capture_output=True,
                text=True,
                input="",
                timeout=10
            )
            if result.returncode == 0:
                paths = []
                in_include_section = False
                for line in result.stderr.split('\n'):
                    if "include <...> search starts here:" in line:
                        in_include_section = True
                    elif in_include_section and line.strip().startswith('/'):
                        paths.append(line.strip())
                    elif in_include_section and "End of search list" in line:
                        break
                return paths
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return []

    def _get_library_paths(self, executable: str) -> List[str]:
        """Get compiler library paths"""
        try:
            result = subprocess.run(
                [executable, "-print-search-dirs"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                paths = []
                for line in result.stdout.split('\n'):
                    if line.startswith("libraries:"):
                        paths_str = line.split("=", 1)[1].strip()
                        paths.extend(paths_str.split(":"))
                return paths
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return []

    def _get_compiler_capabilities(self, compiler_info: CompilerInfo) -> List[str]:
        """Get compiler capabilities"""
        capabilities = []

        # Common capabilities
        capabilities.extend([
            "c++11",
            "c++14",
            "c++17",
            "c++20",
            "c++23",
            "threads",
            "shared",
            "static"
        ])

        # Compiler-specific capabilities
        if compiler_info.compiler_type in [CompilerType.GCC, CompilerType.CLANG, CompilerType.MINGW]:
            capabilities.extend([
                "lto",
                "profile",
                "coverage",
                "sanitizer",
                "rpath"
            ])
        elif compiler_info.compiler_type == CompilerType.MSVC:
            capabilities.extend([
                "lto",
                "profile",
                "coverage",
                "static_analysis"
            ])

        return capabilities

    def _get_gcc_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get GCC compiler flags"""
        flags = [
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-std=c++23",
            "-fPIC"
        ]

        # Add optimization flags based on version
        if compiler_info.version_tuple >= (9, 0, 0):
            flags.extend([
                "-O3",
                "-march=native"
            ])

        return flags

    def _get_clang_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get Clang compiler flags"""
        flags = [
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-std=c++23",
            "-fPIC"
        ]

        # Add optimization flags based on version
        if compiler_info.version_tuple >= (10, 0, 0):
            flags.extend([
                "-O3",
                "-march=native"
            ])

        return flags

    def _get_msvc_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get MSVC compiler flags"""
        flags = [
            "/W4",
            "/permissive-",
            "/std:c++23",
            "/EHsc"
        ]

        # Add optimization flags
        flags.extend([
            "/O2",
            "/GL"
        ])

        return flags

    def _get_mingw_flags(self, compiler_info: CompilerInfo) -> List[str]:
        """Get MinGW compiler flags"""
        return self._get_gcc_flags(compiler_info)

    def _get_gcc_capabilities(self) -> List[str]:
        """Get GCC-specific capabilities"""
        return [
            "lto",
            "profile",
            "coverage",
            "sanitizer",
            "rpath",
            "plugins"
        ]

    def _get_msvc_capabilities(self) -> List[str]:
        """Get MSVC-specific capabilities"""
        return [
            "lto",
            "profile",
            "coverage",
            "static_analysis",
            "precompiled_headers"
        ]

    def _get_msvc_target(self) -> str:
        """Get MSVC target"""
        import os
        arch = os.environ.get('VSCMD_ARG_TGT_ARCH', 'x64')
        return f"x64-windows-msvc" if arch == "x64" else "x86-windows-msvc"

    def _get_msvc_include_paths(self) -> List[str]:
        """Get MSVC include paths"""
        import os
        paths = []

        vs_install_dir = os.environ.get('VSINSTALLDIR')
        if vs_install_dir:
            paths.append(os.path.join(vs_install_dir, "VC", "Tools", "MSVC"))

        windows_sdk = os.environ.get('WindowsSdkDir')
        if windows_sdk:
            paths.append(os.path.join(windows_sdk, "Include"))

        return paths

    def _get_msvc_library_paths(self) -> List[str]:
        """Get MSVC library paths"""
        import os
        paths = []

        vs_install_dir = os.environ.get('VSINSTALLDIR')
        if vs_install_dir:
            paths.append(os.path.join(vs_install_dir, "VC", "Tools", "MSVC"))

        windows_sdk = os.environ.get('WindowsSdkDir')
        if windows_sdk:
            paths.append(os.path.join(windows_sdk, "Lib"))

        return paths

    def clear_cache(self) -> None:
        """Clear cached compiler information"""
        self._detected_compilers = None

    def set_cache_enabled(self, enabled: bool) -> None:
        """Enable or disable caching"""
        self._cache_enabled = enabled
        if not enabled:
            self.clear_cache()
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-007` - Platform detection

### External Dependencies
- `subprocess` - Process execution
- `re` - Regular expressions
- `pathlib` - Path handling
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-010: Compiler Detection
- REQ-015: Compiler Selection Fallback

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Compiler Detection Strategy
1. Search for compiler executables in PATH
2. Execute compiler with --version flag
3. Parse version information
4. Check minimum version requirements
5. Detect compiler capabilities

### Version Parsing
- Use regex to extract version from output
- Handle different version formats
- Convert to tuple for comparison

### Capability Detection
- Use compiler-specific flags
- Test compilation with feature flags
- Cache capability results

### Error Handling
- Handle missing compilers gracefully
- Provide clear error messages
- Log detection failures

## Usage Example

```python
from omni_scripts.compilers import CompilerDetector, CompilerType

# Create detector
detector = CompilerDetector()

# Detect all compilers
compilers = detector.detect_compilers()
for compiler in compilers:
    print(f"Compiler: {compiler.compiler_type}")
    print(f"Version: {compiler.version}")
    print(f"Status: {compiler.status}")

# Detect specific compiler
gcc_info = detector.detect_compiler(CompilerType.GCC)
if gcc_info:
    print(f"GCC found: {gcc_info.version}")

# Get default compiler
default = detector.get_default_compiler()
if default:
    print(f"Default compiler: {default.compiler_type}")

# Check capability
if detector.check_compiler_capability(default, "lto"):
    print("LTO is supported")
```
