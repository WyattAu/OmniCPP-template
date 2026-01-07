# DES-007: Platform Detection Interface

## Overview
Defines the platform detection interface for identifying the operating system, architecture, and environment characteristics.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import platform
import os
import sys

class OSType(Enum):
    """Operating system types"""
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    FREEBSD = "FreeBSD"
    ANDROID = "Android"
    IOS = "iOS"
    UNKNOWN = "Unknown"

class Architecture(Enum):
    """CPU architectures"""
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    AARCH64 = "aarch64"
    MIPS = "mips"
    MIPS64 = "mips64"
    POWERPC = "powerpc"
    POWERPC64 = "powerpc64"
    RISCV = "riscv"
    RISCV64 = "riscv64"
    UNKNOWN = "Unknown"

class CompilerABI(Enum):
    """Compiler ABI types"""
    MSVC = "msvc"
    GCC = "gcc"
    CLANG = "clang"
    MINGW = "mingw"
    MUSL = "musl"
    GLIBC = "glibc"
    UNKNOWN = "Unknown"

@dataclass
class PlatformInfo:
    """Platform information"""
    os_type: OSType
    os_version: str
    os_release: str
    architecture: Architecture
    compiler_abi: CompilerABI
    is_64bit: bool
    is_little_endian: bool
    python_version: str
    python_implementation: str
    platform_name: str
    platform_version: str
    additional_info: Dict[str, str]

@dataclass
class EnvironmentInfo:
    """Environment information"""
    env_vars: Dict[str, str]
    path: List[str]
    shell: str
    terminal: str
    home_dir: str
    temp_dir: str
    user: str
    hostname: str

class IPlatformDetector(ABC):
    """Interface for platform detection"""

    @abstractmethod
    def detect_platform(self) -> PlatformInfo:
        """Detect platform information"""
        pass

    @abstractmethod
    def detect_environment(self) -> EnvironmentInfo:
        """Detect environment information"""
        pass

    @abstractmethod
    def get_os_type(self) -> OSType:
        """Get operating system type"""
        pass

    @abstractmethod
    def get_architecture(self) -> Architecture:
        """Get CPU architecture"""
        pass

    @abstractmethod
    def get_compiler_abi(self) -> CompilerABI:
        """Get compiler ABI"""
        pass

    @abstractmethod
    def is_windows(self) -> bool:
        """Check if running on Windows"""
        pass

    @abstractmethod
    def is_linux(self) -> bool:
        """Check if running on Linux"""
        pass

    @abstractmethod
    def is_macos(self) -> bool:
        """Check if running on macOS"""
        pass

    @abstractmethod
    def is_unix(self) -> bool:
        """Check if running on Unix-like system"""
        pass

    @abstractmethod
    def get_supported_platforms(self) -> List[OSType]:
        """Get list of supported platforms"""
        pass

class PlatformDetector(IPlatformDetector):
    """Implementation of platform detector"""

    def __init__(self) -> None:
        """Initialize platform detector"""
        self._platform_info: Optional[PlatformInfo] = None
        self._environment_info: Optional[EnvironmentInfo] = None
        self._cache_enabled = True

    def detect_platform(self) -> PlatformInfo:
        """Detect platform information"""
        if self._cache_enabled and self._platform_info:
            return self._platform_info

        os_type = self._detect_os_type()
        os_version = self._detect_os_version()
        os_release = self._detect_os_release()
        architecture = self._detect_architecture()
        compiler_abi = self._detect_compiler_abi()
        is_64bit = sys.maxsize > 2**32
        is_little_endian = sys.byteorder == 'little'
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        python_implementation = platform.python_implementation()
        platform_name = platform.system()
        platform_version = platform.version()
        additional_info = self._detect_additional_info()

        self._platform_info = PlatformInfo(
            os_type=os_type,
            os_version=os_version,
            os_release=os_release,
            architecture=architecture,
            compiler_abi=compiler_abi,
            is_64bit=is_64bit,
            is_little_endian=is_little_endian,
            python_version=python_version,
            python_implementation=python_implementation,
            platform_name=platform_name,
            platform_version=platform_version,
            additional_info=additional_info
        )

        return self._platform_info

    def detect_environment(self) -> EnvironmentInfo:
        """Detect environment information"""
        if self._cache_enabled and self._environment_info:
            return self._environment_info

        env_vars = dict(os.environ)
        path = os.environ.get('PATH', '').split(os.pathsep)
        shell = os.environ.get('SHELL', os.environ.get('COMSPEC', ''))
        terminal = os.environ.get('TERM', os.environ.get('WT_SESSION', ''))
        home_dir = os.path.expanduser('~')
        temp_dir = os.environ.get('TEMP', os.environ.get('TMP', '/tmp'))
        user = os.environ.get('USER', os.environ.get('USERNAME', ''))
        hostname = platform.node()

        self._environment_info = EnvironmentInfo(
            env_vars=env_vars,
            path=path,
            shell=shell,
            terminal=terminal,
            home_dir=home_dir,
            temp_dir=temp_dir,
            user=user,
            hostname=hostname
        )

        return self._environment_info

    def get_os_type(self) -> OSType:
        """Get operating system type"""
        return self.detect_platform().os_type

    def get_architecture(self) -> Architecture:
        """Get CPU architecture"""
        return self.detect_platform().architecture

    def get_compiler_abi(self) -> CompilerABI:
        """Get compiler ABI"""
        return self.detect_platform().compiler_abi

    def is_windows(self) -> bool:
        """Check if running on Windows"""
        return self.get_os_type() == OSType.WINDOWS

    def is_linux(self) -> bool:
        """Check if running on Linux"""
        return self.get_os_type() == OSType.LINUX

    def is_macos(self) -> bool:
        """Check if running on macOS"""
        return self.get_os_type() == OSType.MACOS

    def is_unix(self) -> bool:
        """Check if running on Unix-like system"""
        return self.is_linux() or self.is_macos() or self.get_os_type() in [OSType.FREEBSD, OSType.ANDROID]

    def get_supported_platforms(self) -> List[OSType]:
        """Get list of supported platforms"""
        return [
            OSType.WINDOWS,
            OSType.LINUX,
            OSType.MACOS,
            OSType.FREEBSD
        ]

    def _detect_os_type(self) -> OSType:
        """Detect operating system type"""
        system = platform.system().lower()

        if system == 'windows':
            return OSType.WINDOWS
        elif system == 'linux':
            return OSType.LINUX
        elif system == 'darwin':
            return OSType.MACOS
        elif system == 'freebsd':
            return OSType.FREEBSD
        elif 'android' in system:
            return OSType.ANDROID
        elif 'ios' in system:
            return OSType.IOS
        else:
            return OSType.UNKNOWN

    def _detect_os_version(self) -> str:
        """Detect operating system version"""
        if self.is_windows():
            return platform.version()
        elif self.is_linux():
            return self._get_linux_version()
        elif self.is_macos():
            return platform.mac_ver()[0]
        else:
            return platform.version()

    def _detect_os_release(self) -> str:
        """Detect operating system release"""
        if self.is_linux():
            return self._get_linux_release()
        elif self.is_macos():
            return platform.mac_ver()[1]
        else:
            return ""

    def _detect_architecture(self) -> Architecture:
        """Detect CPU architecture"""
        machine = platform.machine().lower()

        if machine in ['x86_64', 'amd64']:
            return Architecture.X86_64
        elif machine in ['x86', 'i386', 'i686']:
            return Architecture.X86
        elif machine in ['arm64', 'aarch64']:
            return Architecture.ARM64
        elif machine in ['armv7l', 'armv6l']:
            return Architecture.ARM
        elif machine in ['mips64']:
            return Architecture.MIPS64
        elif machine in ['mips']:
            return Architecture.MIPS
        elif machine in ['ppc64le', 'powerpc64le']:
            return Architecture.POWERPC64
        elif machine in ['ppc', 'powerpc']:
            return Architecture.POWERPC
        elif machine in ['riscv64']:
            return Architecture.RISCV64
        elif machine in ['riscv']:
            return Architecture.RISCV
        else:
            return Architecture.UNKNOWN

    def _detect_compiler_abi(self) -> CompilerABI:
        """Detect compiler ABI"""
        if self.is_windows():
            # Check for MSVC
            if os.environ.get('VSINSTALLDIR') or os.environ.get('VisualStudioVersion'):
                return CompilerABI.MSVC
            # Check for MinGW
            if 'mingw' in platform.system().lower() or 'mingw' in os.environ.get('PATH', '').lower():
                return CompilerABI.MINGW
        elif self.is_linux():
            # Check for musl
            if 'musl' in platform.libc_ver()[0]:
                return CompilerABI.MUSL
            # Default to glibc
            return CompilerABI.GLIBC
        elif self.is_macos():
            # macOS uses clang by default
            return CompilerABI.CLANG

        return CompilerABI.UNKNOWN

    def _detect_additional_info(self) -> Dict[str, str]:
        """Detect additional platform information"""
        info = {}

        if self.is_linux():
            info['distribution'] = self._get_linux_distribution()
            info['libc'] = platform.libc_ver()[0]
            info['libc_version'] = platform.libc_ver()[1]
        elif self.is_macos():
            info['macos_version'] = platform.mac_ver()[0]
            info['macos_build'] = platform.mac_ver()[2]
        elif self.is_windows():
            info['windows_edition'] = platform.win32_edition()
            info['windows_version'] = platform.win32_ver()[1]

        return info

    def _get_linux_version(self) -> str:
        """Get Linux kernel version"""
        try:
            with open('/proc/version', 'r') as f:
                return f.read().split()[2]
        except (IOError, IndexError):
            return platform.release()

    def _get_linux_release(self) -> str:
        """Get Linux distribution release"""
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=', 1)[1].strip('"')
        except IOError:
            pass

        try:
            with open('/etc/lsb-release', 'r') as f:
                for line in f:
                    if line.startswith('DISTRIB_DESCRIPTION='):
                        return line.split('=', 1)[1].strip('"')
        except IOError:
            pass

        return ""

    def _get_linux_distribution(self) -> str:
        """Get Linux distribution name"""
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('NAME='):
                        return line.split('=', 1)[1].strip('"')
        except IOError:
            pass

        try:
            with open('/etc/lsb-release', 'r') as f:
                for line in f:
                    if line.startswith('DISTRIB_ID='):
                        return line.split('=', 1)[1].strip('"')
        except IOError:
            pass

        return "Unknown"

    def clear_cache(self) -> None:
        """Clear cached platform information"""
        self._platform_info = None
        self._environment_info = None

    def set_cache_enabled(self, enabled: bool) -> None:
        """Enable or disable caching"""
        self._cache_enabled = enabled
        if not enabled:
            self.clear_cache()
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy

### External Dependencies
- `platform` - Platform detection
- `os` - Operating system interface
- `sys` - System-specific parameters
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-009: Platform Detection
- REQ-014: Cross-Compilation Support

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Platform Detection Strategy
1. Use Python's `platform` module for basic detection
2. Use OS-specific files for detailed information
3. Cache results to avoid repeated detection
4. Provide fallback mechanisms for unknown platforms

### Cross-Platform Considerations
- Windows: Use registry and environment variables
- Linux: Use /proc and /etc files
- macOS: Use system commands and frameworks

### Error Handling
- Handle missing files gracefully
- Provide default values for unknown platforms
- Log detection failures

### Performance
- Cache detection results
- Lazy load additional information
- Minimize system calls

## Usage Example

```python
from omni_scripts.platform import PlatformDetector, OSType, Architecture

# Create detector
detector = PlatformDetector()

# Detect platform
platform_info = detector.detect_platform()
print(f"OS: {platform_info.os_type}")
print(f"Architecture: {platform_info.architecture}")
print(f"64-bit: {platform_info.is_64bit}")

# Check platform type
if detector.is_windows():
    print("Running on Windows")
elif detector.is_linux():
    print("Running on Linux")
elif detector.is_macos():
    print("Running on macOS")

# Detect environment
env_info = detector.detect_environment()
print(f"Shell: {env_info.shell}")
print(f"Home: {env_info.home_dir}")
```
