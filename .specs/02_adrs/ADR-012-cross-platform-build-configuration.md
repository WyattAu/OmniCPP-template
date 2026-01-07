# ADR-012: Cross-Platform Build Configuration

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Cross-Platform Compilation

---

## Context

The OmniCPP Template project supports cross-platform compilation for Windows, Linux, and WASM. Each platform requires different build configurations, compiler flags, and system libraries. Without a unified approach, cross-platform builds become error-prone and difficult to maintain.

### Current State

Build configuration is scattered across multiple files:
- **CMakeLists.txt:** Main CMake configuration
- **CMakePresets.json:** CMake presets for different platforms
- **cmake/PlatformConfig.cmake:** Platform-specific configuration
- **cmake/toolchains/**: Toolchain files for cross-compilation

### Issues

1. **Inconsistent Configuration:** Different configuration approaches for each platform
2. **Hardcoded Paths:** Platform-specific paths hardcoded in configuration
3. **No Validation:** No validation that configuration is correct for platform
4. **Duplicate Code:** Similar configuration repeated across platforms
5. **Hard to Extend:** Adding new platforms requires modifying multiple files
6. **No Abstraction:** Direct platform checks throughout code

## Decision

Implement **unified cross-platform build configuration** with:
1. **Platform Abstraction Layer:** Abstract platform-specific details
2. **Configuration Templates:** Template-based configuration for each platform
3. **Automatic Detection:** Automatic platform detection and configuration
4. **Validation:** Validate configuration for each platform
5. **Extensibility:** Easy to add new platforms
6. **Consistent Interface:** Consistent interface across all platforms

### 1. Platform Abstraction Layer

```python
# omni_scripts/platform/base.py
"""Base class for platform configuration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
import platform as sys_platform

from logging.logger import Logger
from exceptions import PlatformError

class PlatformConfig(ABC):
    """Base class for platform configuration."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize platform configuration.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self._system_info = self._get_system_info()

    @abstractmethod
    def get_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        pass

    @abstractmethod
    def get_cmake_generator(self) -> str:
        """Get CMake generator.

        Returns:
            CMake generator name
        """
        pass

    @abstractmethod
    def get_compiler_flags(self) -> List[str]:
        """Get compiler flags.

        Returns:
            List of compiler flags
        """
        pass

    @abstractmethod
    def get_linker_flags(self) -> List[str]:
        """Get linker flags.

        Returns:
            List of linker flags
        """
        pass

    @abstractmethod
    def get_libraries(self) -> List[str]:
        """Get required libraries.

        Returns:
            List of library names
        """
        pass

    @abstractmethod
    def get_include_paths(self) -> List[Path]:
        """Get include paths.

        Returns:
            List of include paths
        """
        pass

    @abstractmethod
    def get_library_paths(self) -> List[Path]:
        """Get library paths.

        Returns:
            List of library paths
        """
        pass

    def _get_system_info(self) -> Dict[str, str]:
        """Get system information.

        Returns:
            Dictionary of system information
        """
        return {
            "system": sys_platform.system(),
            "machine": sys_platform.machine(),
            "processor": sys_platform.processor(),
            "python_version": sys_platform.python_version(),
        }

    def validate(self) -> bool:
        """Validate platform configuration.

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if platform matches
            if self.get_name() != sys_platform.system():
                self.logger.warning(
                    f"Platform mismatch: expected {self.get_name()}, "
                    f"got {sys_platform.system()}"
                )
                return False

            # Check if CMake generator is available
            generator = self.get_cmake_generator()
            if not generator:
                self.logger.error("CMake generator not specified")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
```

### 2. Windows Platform Configuration

```python
# omni_scripts/platform/windows.py
"""Windows platform configuration."""

from typing import Dict, List, Optional, Any
from pathlib import Path

from platform.base import PlatformConfig
from logging.logger import Logger
from exceptions import PlatformError

class WindowsPlatformConfig(PlatformConfig):
    """Windows platform configuration."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Windows platform configuration.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)
        self._compiler_type = self._detect_compiler()

    def get_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        return "Windows"

    def get_cmake_generator(self) -> str:
        """Get CMake generator.

        Returns:
            CMake generator name
        """
        return "Ninja"

    def get_compiler_flags(self) -> List[str]:
        """Get compiler flags.

        Returns:
            List of compiler flags
        """
        flags = [
            "/std:c++23",
            "/W4",
            "/WX",
            "/permissive-",
            "/Zc:__cplusplus",
            "/EHsc",
            "/GR",
        ]

        # Add compiler-specific flags
        if self._compiler_type == "msvc":
            flags.extend([
                "/MP",
                "/GL",
                "/Gy",
            ])
        elif self._compiler_type == "gcc":
            flags.extend([
                "-std=c++23",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-Werror",
            ])
        elif self._compiler_type == "clang":
            flags.extend([
                "-std=c++23",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-Werror",
            ])

        return flags

    def get_linker_flags(self) -> List[str]:
        """Get linker flags.

        Returns:
            List of linker flags
        """
        flags = []

        if self._compiler_type == "msvc":
            flags.extend([
                "/LTCG",
                "/OPT:REF",
                "/OPT:ICF",
            ])

        return flags

    def get_libraries(self) -> List[str]:
        """Get required libraries.

        Returns:
            List of library names
        """
        return [
            "kernel32",
            "user32",
            "gdi32",
            "winspool",
            "comdlg32",
            "advapi32",
            "shell32",
            "ole32",
            "oleaut32",
            "uuid",
            "odbc32",
            "odbccp32",
        ]

    def get_include_paths(self) -> List[Path]:
        """Get include paths.

        Returns:
            List of include paths
        """
        paths = []

        # Add Windows SDK include paths
        paths.append(Path("C:/Program Files (x86)/Windows Kits/10/Include/10.0.22000.0/ucrt"))
        paths.append(Path("C:/Program Files (x86)/Windows Kits/10/Include/10.0.22000.0/shared"))
        paths.append(Path("C:/Program Files (x86)/Windows Kits/10/Include/10.0.22000.0/um"))

        return paths

    def get_library_paths(self) -> List[Path]:
        """Get library paths.

        Returns:
            List of library paths
        """
        paths = []

        # Add Windows SDK library paths
        paths.append(Path("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.22000.0/ucrt/x64"))
        paths.append(Path("C:/Program Files (x86)/Windows Kits/10/Lib/10.0.22000.0/um/x64"))

        return paths

    def _detect_compiler(self) -> str:
        """Detect compiler type.

        Returns:
            Compiler type
        """
        import shutil

        # Check for MSVC
        if shutil.which("cl.exe"):
            return "msvc"

        # Check for GCC
        if shutil.which("gcc.exe"):
            return "gcc"

        # Check for Clang
        if shutil.which("clang.exe"):
            return "clang"

        return "unknown"
```

### 3. Linux Platform Configuration

```python
# omni_scripts/platform/linux.py
"""Linux platform configuration."""

from typing import Dict, List, Optional, Any
from pathlib import Path

from platform.base import PlatformConfig
from logging.logger import Logger
from exceptions import PlatformError

class LinuxPlatformConfig(PlatformConfig):
    """Linux platform configuration."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Linux platform configuration.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)
        self._compiler_type = self._detect_compiler()

    def get_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        return "Linux"

    def get_cmake_generator(self) -> str:
        """Get CMake generator.

        Returns:
            CMake generator name
        """
        return "Ninja"

    def get_compiler_flags(self) -> List[str]:
        """Get compiler flags.

        Returns:
            List of compiler flags
        """
        flags = [
            "-std=c++23",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            "-fPIC",
            "-fvisibility=hidden",
        ]

        # Add compiler-specific flags
        if self._compiler_type == "gcc":
            flags.extend([
                "-fno-exceptions",
                "-fno-rtti",
            ])
        elif self._compiler_type == "clang":
            flags.extend([
                "-fno-exceptions",
                "-fno-rtti",
            ])

        return flags

    def get_linker_flags(self) -> List[str]:
        """Get linker flags.

        Returns:
            List of linker flags
        """
        flags = [
            "-Wl,--as-needed",
            "-Wl,--no-undefined",
        ]

        return flags

    def get_libraries(self) -> List[str]:
        """Get required libraries.

        Returns:
            List of library names
        """
        return [
            "pthread",
            "dl",
            "rt",
        ]

    def get_include_paths(self) -> List[Path]:
        """Get include paths.

        Returns:
            List of include paths
        """
        paths = []

        # Add standard include paths
        paths.append(Path("/usr/include"))
        paths.append(Path("/usr/local/include"))

        return paths

    def get_library_paths(self) -> List[Path]:
        """Get library paths.

        Returns:
            List of library paths
        """
        paths = []

        # Add standard library paths
        paths.append(Path("/usr/lib"))
        paths.append(Path("/usr/local/lib"))
        paths.append(Path("/lib/x86_64-linux-gnu"))

        return paths

    def _detect_compiler(self) -> str:
        """Detect compiler type.

        Returns:
            Compiler type
        """
        import shutil

        # Check for GCC
        if shutil.which("gcc"):
            return "gcc"

        # Check for Clang
        if shutil.which("clang"):
            return "clang"

        return "unknown"
```

### 4. WASM Platform Configuration

```python
# omni_scripts/platform/wasm.py
"""WASM platform configuration."""

from typing import Dict, List, Optional, Any
from pathlib import Path

from platform.base import PlatformConfig
from logging.logger import Logger
from exceptions import PlatformError

class WASMPlatformConfig(PlatformConfig):
    """WASM platform configuration."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize WASM platform configuration.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)

    def get_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        return "WASM"

    def get_cmake_generator(self) -> str:
        """Get CMake generator.

        Returns:
            CMake generator name
        """
        return "Ninja"

    def get_compiler_flags(self) -> List[str]:
        """Get compiler flags.

        Returns:
            List of compiler flags
        """
        flags = [
            "-std=c++23",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            "-fPIC",
            "-fvisibility=hidden",
            "-s WASM=1",
            "-s USE_SDL=2",
            "-s USE_VULKAN=1",
        ]

        return flags

    def get_linker_flags(self) -> List[str]:
        """Get linker flags.

        Returns:
            List of linker flags
        """
        flags = [
            "-s WASM=1",
            "-s USE_SDL=2",
            "-s USE_VULKAN=1",
            "-s ALLOW_MEMORY_GROWTH=1",
        ]

        return flags

    def get_libraries(self) -> List[str]:
        """Get required libraries.

        Returns:
            List of library names
        """
        return []

    def get_include_paths(self) -> List[Path]:
        """Get include paths.

        Returns:
            List of include paths
        """
        paths = []

        # Add Emscripten include paths
        paths.append(Path("/usr/local/include"))

        return paths

    def get_library_paths(self) -> List[Path]:
        """Get library paths.

        Returns:
            List of library paths
        """
        paths = []

        # Add Emscripten library paths
        paths.append(Path("/usr/local/lib"))

        return paths
```

### 5. Platform Manager

```python
# omni_scripts/platform/manager.py
"""Platform manager for cross-platform configuration."""

from typing import Dict, Optional, Any
import platform as sys_platform

from platform.base import PlatformConfig
from platform.windows import WindowsPlatformConfig
from platform.linux import LinuxPlatformConfig
from platform.wasm import WASMPlatformConfig
from logging.logger import Logger
from exceptions import PlatformError

class PlatformManager:
    """Manager for platform configuration."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize platform manager.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self._platform_config: Optional[PlatformConfig] = None

    def get_platform_config(self, platform: Optional[str] = None) -> PlatformConfig:
        """Get platform configuration.

        Args:
            platform: Platform name (None for auto-detect)

        Returns:
            Platform configuration

        Raises:
            PlatformError: If platform is not supported
        """
        if self._platform_config is None:
            self._platform_config = self._create_platform_config(platform)

        return self._platform_config

    def _create_platform_config(self, platform: Optional[str] = None) -> PlatformConfig:
        """Create platform configuration.

        Args:
            platform: Platform name (None for auto-detect)

        Returns:
            Platform configuration

        Raises:
            PlatformError: If platform is not supported
        """
        # Auto-detect platform if not specified
        if platform is None:
            platform = sys_platform.system()

        # Create platform configuration
        if platform == "Windows":
            return WindowsPlatformConfig(self.logger, self.config)
        elif platform == "Linux":
            return LinuxPlatformConfig(self.logger, self.config)
        elif platform == "WASM":
            return WASMPlatformConfig(self.logger, self.config)
        else:
            raise PlatformError(f"Unsupported platform: {platform}")

    def validate_platform(self, platform: Optional[str] = None) -> bool:
        """Validate platform configuration.

        Args:
            platform: Platform name (None for auto-detect)

        Returns:
            True if valid, False otherwise
        """
        try:
            config = self.get_platform_config(platform)
            return config.validate()
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
```

### 6. Usage Example

```python
# Example usage
from platform.manager import PlatformManager
from logging.logger import Logger
from config import load_config

# Load configuration
config = load_config()

# Initialize logger
logger = Logger(config)

# Create platform manager
manager = PlatformManager(logger, config)

# Get platform configuration
platform_config = manager.get_platform_config()

# Get platform information
print(f"Platform: {platform_config.get_name()}")
print(f"CMake Generator: {platform_config.get_cmake_generator()}")
print(f"Compiler Flags: {platform_config.get_compiler_flags()}")
print(f"Linker Flags: {platform_config.get_linker_flags()}")
print(f"Libraries: {platform_config.get_libraries()}")
```

## Consequences

### Positive

1. **Unified Configuration:** Consistent configuration across all platforms
2. **Abstraction:** Abstracts away platform-specific details
3. **Automatic Detection:** Automatic platform detection and configuration
4. **Validation:** Validates configuration for each platform
5. **Extensibility:** Easy to add new platforms
6. **Consistent Interface:** Consistent interface across all platforms
7. **Reduced Duplication:** Eliminates duplicate configuration code

### Negative

1. **Complexity:** More complex than direct platform checks
2. **Learning Curve:** Developers need to understand abstraction
3. **Overhead:** Additional abstraction layer
4. **File Count:** More files to maintain

### Neutral

1. **Documentation:** Requires documentation for each platform
2. **Testing:** Need to test all platform configurations

## Alternatives Considered

### Alternative 1: Direct Platform Checks

**Description:** Use direct platform checks throughout code

**Pros:**
- Simpler implementation
- Less abstraction

**Cons:**
- Inconsistent configuration
- Hard to maintain
- Platform-specific code scattered

**Rejected:** Too inconsistent and hard to maintain

### Alternative 2: CMake Platform Detection

**Description:** Let CMake handle platform detection

**Pros:**
- CMake handles complexity
- Less custom code

**Cons:**
- Less control
- CMake limitations
- Harder to customize

**Rejected:** Less control and harder to customize

### Alternative 3: Configuration Files

**Description:** Use configuration files for each platform

**Pros:**
- Simple to implement
- Easy to modify

**Cons:**
- No validation
- Hard to maintain
- No abstraction

**Rejected:** No validation and hard to maintain

## Related ADRs

- [ADR-004: CMake 4 with Ninja as default generator](ADR-004-cmake-4-ninja-default-generator.md)
- [ADR-005: CMake Presets for cross-platform configuration](ADR-005-cmake-presets-cross-platform-configuration.md)
- [ADR-006: Toolchain file organization](ADR-006-toolchain-file-organization.md)
- [ADR-010: Terminal invocation patterns for different compilers](ADR-010-terminal-invocation-patterns.md)
- [ADR-011: Compiler detection and selection strategy](ADR-011-compiler-detection-selection.md)

## References

- [CMake Cross-Compiling](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)
- [CMake Platform Variables](https://cmake.org/cmake/help/latest/manual/cmake-variables.7.html)
- [Python Platform Module](https://docs.python.org/3/library/platform.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
