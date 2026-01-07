"""
MSVC Architecture Variants for vcvarsall.bat

This module provides comprehensive support for MSVC architecture variants
used with vcvarsall.bat for setting up the MSVC build environment.
"""

import logging
from enum import Enum
from typing import Dict, List, Optional, Tuple


class MSVCArchitecture(Enum):
    """
    MSVC architecture variants for vcvarsall.bat
    
    These architectures correspond to the arguments passed to vcvarsall.bat
    to set up the MSVC build environment for different host and target
    architecture combinations.
    """
    
    # Native 64-bit (host and target are both x64)
    X64 = "amd64"
    
    # Native 32-bit (host and target are both x86)
    X86 = "x86"
    
    # Cross-compile: 32-bit host, 64-bit target
    X86_AMD64 = "x86_amd64"
    
    # Cross-compile: 64-bit host, 32-bit target
    AMD64_X86 = "amd64_x86"
    
    # Cross-compile: 64-bit host, ARM target
    AMD64_ARM = "amd64_arm"
    
    # Cross-compile: 64-bit host, ARM64 target
    AMD64_ARM64 = "amd64_arm64"
    
    @property
    def host_architecture(self) -> str:
        """
        Get the host architecture (the architecture of the compiler itself)
        
        Returns:
            Host architecture string (x64 or x86)
        """
        host_map = {
            MSVCArchitecture.X64: "x64",
            MSVCArchitecture.X86: "x86",
            MSVCArchitecture.X86_AMD64: "x86",
            MSVCArchitecture.AMD64_X86: "x64",
            MSVCArchitecture.AMD64_ARM: "x64",
            MSVCArchitecture.AMD64_ARM64: "x64"
        }
        return host_map[self]
    
    @property
    def target_architecture(self) -> str:
        """
        Get the target architecture (the architecture of the compiled code)
        
        Returns:
            Target architecture string (x64, x86, arm, or arm64)
        """
        target_map = {
            MSVCArchitecture.X64: "x64",
            MSVCArchitecture.X86: "x86",
            MSVCArchitecture.X86_AMD64: "x64",
            MSVCArchitecture.AMD64_X86: "x86",
            MSVCArchitecture.AMD64_ARM: "arm",
            MSVCArchitecture.AMD64_ARM64: "arm64"
        }
        return target_map[self]
    
    @property
    def is_native(self) -> bool:
        """
        Check if this is a native compilation (host == target)
        
        Returns:
            True if native, False if cross-compilation
        """
        return self in [MSVCArchitecture.X64, MSVCArchitecture.X86]
    
    @property
    def is_cross_compilation(self) -> bool:
        """
        Check if this is a cross-compilation (host != target)
        
        Returns:
            True if cross-compilation, False if native
        """
        return not self.is_native
    
    @property
    def is_arm_target(self) -> bool:
        """
        Check if the target architecture is ARM-based
        
        Returns:
            True if target is ARM or ARM64
        """
        return self in [MSVCArchitecture.AMD64_ARM, MSVCArchitecture.AMD64_ARM64]
    
    @property
    def is_x86_target(self) -> bool:
        """
        Check if the target architecture is x86-based
        
        Returns:
            True if target is x86 or x64
        """
        return not self.is_arm_target
    
    @classmethod
    def from_string(cls, arch_str: str) -> "MSVCArchitecture":
        """
        Parse architecture from string
        
        Args:
            arch_str: Architecture string (e.g., "x64", "x86_amd64", "amd64")
        
        Returns:
            MSVCArchitecture enum value
        
        Raises:
            ValueError: If architecture string is invalid
        """
        normalized = arch_str.lower().strip()
        
        # Map common aliases to enum values
        alias_map = {
            "x64": cls.X64,
            "amd64": cls.X64,
            "x86": cls.X86,
            "32": cls.X86,
            "x86_amd64": cls.X86_AMD64,
            "x86-x64": cls.X86_AMD64,
            "amd64_x86": cls.AMD64_X86,
            "amd64-x86": cls.AMD64_X86,
            "amd64_arm": cls.AMD64_ARM,
            "amd64-arm": cls.AMD64_ARM,
            "amd64_arm64": cls.AMD64_ARM64,
            "amd64-arm64": cls.AMD64_ARM64
        }
        
        if normalized in alias_map:
            return alias_map[normalized]
        
        raise ValueError(
            f"Invalid MSVC architecture: '{arch_str}'. "
            f"Valid architectures are: {', '.join([a.value for a in cls])}"
        )
    
    @classmethod
    def from_host_target(cls, host: str, target: str) -> "MSVCArchitecture":
        """
        Get architecture from host and target architecture strings
        
        Args:
            host: Host architecture (x64 or x86)
            target: Target architecture (x64, x86, arm, or arm64)
        
        Returns:
            MSVCArchitecture enum value
        
        Raises:
            ValueError: If host/target combination is invalid
        """
        host = host.lower().strip()
        target = target.lower().strip()
        
        # Normalize host
        if host in ["amd64", "x64"]:
            host = "x64"
        elif host in ["x86", "32", "i386"]:
            host = "x86"
        else:
            raise ValueError(f"Invalid host architecture: '{host}'")
        
        # Normalize target
        if target in ["amd64", "x64"]:
            target = "x64"
        elif target in ["x86", "32", "i386"]:
            target = "x86"
        elif target in ["arm"]:
            target = "arm"
        elif target in ["arm64", "aarch64"]:
            target = "arm64"
        else:
            raise ValueError(f"Invalid target architecture: '{target}'")
        
        # Map host/target to architecture
        host_target_map = {
            ("x64", "x64"): cls.X64,
            ("x86", "x86"): cls.X86,
            ("x86", "x64"): cls.X86_AMD64,
            ("x64", "x86"): cls.AMD64_X86,
            ("x64", "arm"): cls.AMD64_ARM,
            ("x64", "arm64"): cls.AMD64_ARM64
        }
        
        key = (host, target)
        if key in host_target_map:
            return host_target_map[key]
        
        raise ValueError(
            f"Invalid host/target combination: host='{host}', target='{target}'. "
            f"Valid combinations are: {', '.join([str(k) for k in host_target_map.keys()])}"
        )
    
    @classmethod
    def get_all_architectures(cls) -> List["MSVCArchitecture"]:
        """
        Get all available MSVC architectures
        
        Returns:
            List of all MSVCArchitecture enum values
        """
        return list(cls)
    
    @classmethod
    def get_native_architectures(cls) -> List["MSVCArchitecture"]:
        """
        Get native architectures (host == target)
        
        Returns:
            List of native MSVCArchitecture enum values
        """
        return [cls.X64, cls.X86]
    
    @classmethod
    def get_cross_compilation_architectures(cls) -> List["MSVCArchitecture"]:
        """
        Get cross-compilation architectures (host != target)
        
        Returns:
            List of cross-compilation MSVCArchitecture enum values
        """
        return [cls.X86_AMD64, cls.AMD64_X86, cls.AMD64_ARM, cls.AMD64_ARM64]
    
    @classmethod
    def get_arm_architectures(cls) -> List["MSVCArchitecture"]:
        """
        Get ARM target architectures
        
        Returns:
            List of ARM target MSVCArchitecture enum values
        """
        return [cls.AMD64_ARM, cls.AMD64_ARM64]
    
    @classmethod
    def get_x86_architectures(cls) -> List["MSVCArchitecture"]:
        """
        Get x86 target architectures
        
        Returns:
            List of x86 target MSVCArchitecture enum values
        """
        return [cls.X64, cls.X86, cls.X86_AMD64, cls.AMD64_X86]


class MSVCArchitectureValidator:
    """
    Validator for MSVC architecture configurations
    
    This class provides validation and error checking for MSVC architecture
    configurations used with vcvarsall.bat.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the architecture validator
        
        Args:
            logger: Logger instance for logging validation results
        """
        self._logger = logger or logging.getLogger(__name__)
    
    def validate_architecture(self, architecture: MSVCArchitecture) -> Tuple[bool, List[str]]:
        """
        Validate an MSVC architecture
        
        Args:
            architecture: MSVCArchitecture to validate
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check if architecture is a valid enum value
        if not isinstance(architecture, MSVCArchitecture):
            errors.append(f"Invalid architecture type: {type(architecture)}")
            return (False, errors)
        
        # Validate host/target combination
        if architecture.is_cross_compilation:
            self._logger.debug(f"Validating cross-compilation architecture: {architecture.value}")
            
            # Check for ARM cross-compilation requirements
            if architecture.is_arm_target:
                self._logger.debug(f"ARM target detected: {architecture.target_architecture}")
        
        return (len(errors) == 0, errors)
    
    def validate_architecture_string(self, arch_str: str) -> Tuple[bool, List[str], Optional[MSVCArchitecture]]:
        """
        Validate and parse an architecture string
        
        Args:
            arch_str: Architecture string to validate
        
        Returns:
            Tuple of (is_valid, list of error messages, parsed architecture or None)
        """
        errors = []
        
        try:
            architecture = MSVCArchitecture.from_string(arch_str)
            self._logger.info(f"Successfully parsed architecture: {arch_str} -> {architecture.value}")
            return (True, [], architecture)
        except ValueError as e:
            errors.append(str(e))
            self._logger.error(f"Failed to parse architecture string: {arch_str}")
            return (False, errors, None)
    
    def validate_host_target(self, host: str, target: str) -> Tuple[bool, List[str], Optional[MSVCArchitecture]]:
        """
        Validate host and target architecture combination
        
        Args:
            host: Host architecture string
            target: Target architecture string
        
        Returns:
            Tuple of (is_valid, list of error messages, parsed architecture or None)
        """
        errors = []
        
        try:
            architecture = MSVCArchitecture.from_host_target(host, target)
            self._logger.info(
                f"Successfully parsed host/target: host={host}, target={target} -> {architecture.value}"
            )
            return (True, [], architecture)
        except ValueError as e:
            errors.append(str(e))
            self._logger.error(f"Failed to parse host/target: host={host}, target={target}")
            return (False, errors, None)
    
    def get_supported_architectures_for_host(self, host_arch: str) -> List[MSVCArchitecture]:
        """
        Get all supported architectures for a given host architecture
        
        Args:
            host_arch: Host architecture (x64 or x86)
        
        Returns:
            List of supported MSVCArchitecture enum values
        """
        host_arch = host_arch.lower().strip()
        
        if host_arch in ["x64", "amd64"]:
            return [
                MSVCArchitecture.X64,
                MSVCArchitecture.AMD64_X86,
                MSVCArchitecture.AMD64_ARM,
                MSVCArchitecture.AMD64_ARM64
            ]
        elif host_arch in ["x86", "32"]:
            return [
                MSVCArchitecture.X86,
                MSVCArchitecture.X86_AMD64
            ]
        else:
            self._logger.warning(f"Unknown host architecture: {host_arch}")
            return []


class MSVCArchitectureMapper:
    """
    Mapper for MSVC architectures to vcvarsall.bat arguments and paths
    
    This class provides mapping between architecture enums and the actual
    arguments and paths used by vcvarsall.bat and the MSVC toolchain.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the architecture mapper
        
        Args:
            logger: Logger instance for logging mapping operations
        """
        self._logger = logger or logging.getLogger(__name__)
        
        # Architecture to vcvarsall.bat argument mapping
        self._vcvarsall_args: Dict[MSVCArchitecture, str] = {
            MSVCArchitecture.X64: "amd64",
            MSVCArchitecture.X86: "x86",
            MSVCArchitecture.X86_AMD64: "x86_amd64",
            MSVCArchitecture.AMD64_X86: "amd64_x86",
            MSVCArchitecture.AMD64_ARM: "amd64_arm",
            MSVCArchitecture.AMD64_ARM64: "amd64_arm64"
        }
        
        # Architecture to cl.exe path mapping
        self._cl_paths: Dict[MSVCArchitecture, str] = {
            MSVCArchitecture.X64: "Hostx64/x64",
            MSVCArchitecture.X86: "Hostx86/x86",
            MSVCArchitecture.X86_AMD64: "Hostx86/x64",
            MSVCArchitecture.AMD64_X86: "Hostx64/x86",
            MSVCArchitecture.AMD64_ARM: "Hostx64/arm",
            MSVCArchitecture.AMD64_ARM64: "Hostx64/arm64"
        }
        
        # Architecture to batch file mapping
        self._batch_files: Dict[MSVCArchitecture, str] = {
            MSVCArchitecture.X64: "vcvars64.bat",
            MSVCArchitecture.X86: "vcvars32.bat",
            MSVCArchitecture.X86_AMD64: "vcvarsx86_amd64.bat",
            MSVCArchitecture.AMD64_X86: "vcvarsamd64_x86.bat",
            MSVCArchitecture.AMD64_ARM: "vcvarsamd64_arm.bat",
            MSVCArchitecture.AMD64_ARM64: "vcvarsamd64_arm64.bat"
        }
    
    def get_vcvarsall_argument(self, architecture: MSVCArchitecture) -> str:
        """
        Get the vcvarsall.bat argument for an architecture
        
        Args:
            architecture: MSVCArchitecture enum value
        
        Returns:
            vcvarsall.bat argument string
        
        Raises:
            ValueError: If architecture is not supported
        """
        if architecture not in self._vcvarsall_args:
            raise ValueError(f"Unsupported architecture: {architecture}")
        
        arg = self._vcvarsall_args[architecture]
        self._logger.debug(f"vcvarsall argument for {architecture.value}: {arg}")
        return arg
    
    def get_cl_path(self, architecture: MSVCArchitecture) -> str:
        """
        Get the relative path to cl.exe for an architecture
        
        Args:
            architecture: MSVCArchitecture enum value
        
        Returns:
            Relative path to cl.exe (e.g., "Hostx64/x64")
        
        Raises:
            ValueError: If architecture is not supported
        """
        if architecture not in self._cl_paths:
            raise ValueError(f"Unsupported architecture: {architecture}")
        
        path = self._cl_paths[architecture]
        self._logger.debug(f"cl.exe path for {architecture.value}: {path}")
        return path
    
    def get_batch_file(self, architecture: MSVCArchitecture) -> str:
        """
        Get the architecture-specific batch file name
        
        Args:
            architecture: MSVCArchitecture enum value
        
        Returns:
            Batch file name (e.g., "vcvars64.bat")
        
        Raises:
            ValueError: If architecture is not supported
        """
        if architecture not in self._batch_files:
            raise ValueError(f"Unsupported architecture: {architecture}")
        
        batch_file = self._batch_files[architecture]
        self._logger.debug(f"Batch file for {architecture.value}: {batch_file}")
        return batch_file
    
    def get_full_cl_path(self, architecture: MSVCArchitecture, vs_install_path: str) -> str:
        """
        Get the full path to cl.exe for an architecture
        
        Args:
            architecture: MSVCArchitecture enum value
            vs_install_path: Visual Studio installation path
        
        Returns:
            Full path to cl.exe
        """
        import os
        
        cl_rel_path = self.get_cl_path(architecture)
        full_path = os.path.join(vs_install_path, "VC", "Tools", "MSVC", cl_rel_path, "cl.exe")
        
        self._logger.debug(f"Full cl.exe path for {architecture.value}: {full_path}")
        return full_path
    
    def get_vcvarsall_path(self, vs_install_path: str) -> str:
        """
        Get the path to vcvarsall.bat
        
        Args:
            vs_install_path: Visual Studio installation path
        
        Returns:
            Full path to vcvarsall.bat
        """
        import os
        
        # Try VC\Auxiliary\Build first (VS 2017+)
        vcvarsall_path = os.path.join(vs_install_path, "VC", "Auxiliary", "Build", "vcvarsall.bat")
        
        # Fallback to VC directory (older versions)
        if not os.path.exists(vcvarsall_path):
            vcvarsall_path = os.path.join(vs_install_path, "VC", "vcvarsall.bat")
        
        self._logger.debug(f"vcvarsall.bat path: {vcvarsall_path}")
        return vcvarsall_path
    
    def get_all_mappings(self) -> Dict[MSVCArchitecture, Dict[str, str]]:
        """
        Get all mappings for all architectures
        
        Returns:
            Dictionary mapping architectures to their vcvarsall argument,
            cl.exe path, and batch file name
        """
        mappings = {}
        
        for arch in MSVCArchitecture:
            mappings[arch] = {
                "vcvarsall_arg": self.get_vcvarsall_argument(arch),
                "cl_path": self.get_cl_path(arch),
                "batch_file": self.get_batch_file(arch),
                "host_arch": arch.host_architecture,
                "target_arch": arch.target_architecture,
                "is_native": arch.is_native,
                "is_cross_compilation": arch.is_cross_compilation
            }
        
        return mappings


def detect_system_architecture() -> str:
    """
    Detect the system's native architecture
    
    Returns:
        System architecture string (x64 or x86)
    """
    import platform
    import sys
    
    machine = platform.machine().lower()
    
    if machine in ["amd64", "x86_64", "x64"]:
        return "x64"
    elif machine in ["i386", "i686", "x86"]:
        return "x86"
    else:
        # Fallback to Python architecture
        if sys.maxsize > 2**32:
            return "x64"
        else:
            return "x86"


def get_recommended_architecture() -> MSVCArchitecture:
    """
    Get the recommended architecture for the current system
    
    Returns:
        Recommended MSVCArchitecture for the system
    """
    system_arch = detect_system_architecture()
    
    if system_arch == "x64":
        return MSVCArchitecture.X64
    else:
        return MSVCArchitecture.X86
