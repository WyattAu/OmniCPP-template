# ADR-011: Compiler Detection and Selection Strategy

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Cross-Platform Compilation

---

## Context

The OmniCPP Template project supports multiple compilers (MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang) across different platforms (Windows, Linux, WASM). Automatic compiler detection and selection is essential for a seamless developer experience and consistent builds across different environments.

### Current State

Compiler detection is scattered across multiple scripts:
- **Windows:** Manual detection of MSVC, MinGW-GCC, MinGW-clang
- **Linux:** Manual detection of GCC, Clang
- **WASM:** Manual detection of Emscripten

### Issues

1. **Inconsistent Detection:** Different detection methods for each compiler
2. **No Caching:** Detection runs every time, even if unchanged
3. **No Fallback:** No fallback mechanism if preferred compiler is not found
4. **Platform-Specific:** Hard to maintain cross-platform detection
5. **No Validation:** No validation that detected compiler works correctly
6. **Manual Configuration:** Developers must manually specify compiler

## Decision

Implement **automatic compiler detection and selection** with:
1. **Platform-Specific Detectors:** Each platform has its own detector
2. **Compiler Caching:** Cache detection results to avoid repeated detection
3. **Priority-Based Selection:** Select compiler based on priority
4. **Fallback Mechanism:** Fallback to alternative compilers if preferred is not found
5. **Validation:** Validate that detected compiler works correctly
6. **Configuration Override:** Allow manual override of detected compiler

### 1. Compiler Detection Interface

```python
# omni_scripts/compilers/detector.py
"""Compiler detection interface."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pathlib import Path
import subprocess
import logging

from logging.logger import Logger
from exceptions import CompilerError

class CompilerInfo:
    """Compiler information."""

    def __init__(
        self,
        name: str,
        version: str,
        path: Path,
        type: str,
        architecture: str
    ):
        """Initialize compiler info.

        Args:
            name: Compiler name (e.g., "MSVC", "GCC", "Clang")
            version: Compiler version
            path: Path to compiler executable
            type: Compiler type (e.g., "msvc", "gcc", "clang")
            architecture: Target architecture (e.g., "x64", "arm64")
        """
        self.name = name
        self.version = version
        self.path = path
        self.type = type
        self.architecture = architecture

    def __repr__(self) -> str:
        """String representation."""
        return f"CompilerInfo(name={self.name}, version={self.version}, type={self.type}, arch={self.architecture})"

class CompilerDetector(ABC):
    """Base class for compiler detection."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize compiler detector.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}

    @abstractmethod
    def detect(self) -> List[CompilerInfo]:
        """Detect available compilers.

        Returns:
            List of detected compilers
        """
        pass

    @abstractmethod
    def validate(self, compiler: CompilerInfo) -> bool:
        """Validate compiler.

        Args:
            compiler: Compiler to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    def get_version(self, compiler_path: Path) -> Optional[str]:
        """Get compiler version.

        Args:
            compiler_path: Path to compiler executable

        Returns:
            Compiler version or None
        """
        try:
            result = subprocess.run(
                [str(compiler_path), "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse version from output
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'version' in line.lower():
                        # Extract version number
                        import re
                        match = re.search(r'(\d+\.\d+\.\d+)', line)
                        if match:
                            return match.group(1)

            return None

        except Exception as e:
            self.logger.warning(f"Failed to get version for {compiler_path}: {e}")
            return None
```

### 2. Windows Compiler Detector

```python
# omni_scripts/compilers/windows_detector.py
"""Windows compiler detection."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import subprocess
import shutil

from compilers.detector import CompilerDetector, CompilerInfo
from logging.logger import Logger
from exceptions import CompilerError

class WindowsCompilerDetector(CompilerDetector):
    """Windows compiler detector."""

    def detect(self) -> List[CompilerInfo]:
        """Detect Windows compilers.

        Returns:
            List of detected compilers
        """
        compilers = []

        # Detect MSVC
        msvc = self._detect_msvc()
        if msvc:
            compilers.append(msvc)

        # Detect MSVC-Clang
        msvc_clang = self._detect_msvc_clang()
        if msvc_clang:
            compilers.append(msvc_clang)

        # Detect MinGW-GCC
        mingw_gcc = self._detect_mingw_gcc()
        if mingw_gcc:
            compilers.append(mingw_gcc)

        # Detect MinGW-Clang
        mingw_clang = self._detect_mingw_clang()
        if mingw_clang:
            compilers.append(mingw_clang)

        return compilers

    def _detect_msvc(self) -> Optional[CompilerInfo]:
        """Detect MSVC compiler.

        Returns:
            MSVC compiler info or None
        """
        # Find cl.exe
        cl_path = shutil.which("cl.exe")
        if not cl_path:
            return None

        # Get version
        version = self.get_version(Path(cl_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="MSVC",
            version=version,
            path=Path(cl_path),
            type="msvc",
            architecture="x64"
        )

    def _detect_msvc_clang(self) -> Optional[CompilerInfo]:
        """Detect MSVC-Clang compiler.

        Returns:
            MSVC-Clang compiler info or None
        """
        # Find clang-cl.exe
        clang_cl_path = shutil.which("clang-cl.exe")
        if not clang_cl_path:
            return None

        # Get version
        version = self.get_version(Path(clang_cl_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="MSVC-Clang",
            version=version,
            path=Path(clang_cl_path),
            type="msvc-clang",
            architecture="x64"
        )

    def _detect_mingw_gcc(self) -> Optional[CompilerInfo]:
        """Detect MinGW-GCC compiler.

        Returns:
            MinGW-GCC compiler info or None
        """
        # Find gcc.exe
        gcc_path = shutil.which("gcc.exe")
        if not gcc_path:
            return None

        # Check if it's MinGW
        result = subprocess.run(
            [gcc_path, "-v"],
            capture_output=True,
            text=True
        )

        if "mingw" not in result.stdout.lower():
            return None

        # Get version
        version = self.get_version(Path(gcc_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="MinGW-GCC",
            version=version,
            path=Path(gcc_path),
            type="mingw-gcc",
            architecture="x64"
        )

    def _detect_mingw_clang(self) -> Optional[CompilerInfo]:
        """Detect MinGW-Clang compiler.

        Returns:
            MinGW-Clang compiler info or None
        """
        # Find clang.exe
        clang_path = shutil.which("clang.exe")
        if not clang_path:
            return None

        # Check if it's MinGW
        result = subprocess.run(
            [clang_path, "-v"],
            capture_output=True,
            text=True
        )

        if "mingw" not in result.stdout.lower():
            return None

        # Get version
        version = self.get_version(Path(clang_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="MinGW-Clang",
            version=version,
            path=Path(clang_path),
            type="mingw-clang",
            architecture="x64"
        )

    def validate(self, compiler: CompilerInfo) -> bool:
        """Validate compiler.

        Args:
            compiler: Compiler to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Try to compile a simple program
            test_file = Path("test.cpp")
            test_file.write_text("int main() { return 0; }")

            result = subprocess.run(
                [str(compiler.path), "/c", str(test_file)],
                capture_output=True,
                timeout=30
            )

            # Clean up
            test_file.unlink()
            test_obj = Path("test.obj")
            if test_obj.exists():
                test_obj.unlink()

            return result.returncode == 0

        except Exception as e:
            self.logger.warning(f"Failed to validate {compiler.name}: {e}")
            return False
```

### 3. Linux Compiler Detector

```python
# omni_scripts/compilers/linux_detector.py
"""Linux compiler detection."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import subprocess
import shutil

from compilers.detector import CompilerDetector, CompilerInfo
from logging.logger import Logger
from exceptions import CompilerError

class LinuxCompilerDetector(CompilerDetector):
    """Linux compiler detector."""

    def detect(self) -> List[CompilerInfo]:
        """Detect Linux compilers.

        Returns:
            List of detected compilers
        """
        compilers = []

        # Detect GCC
        gcc = self._detect_gcc()
        if gcc:
            compilers.append(gcc)

        # Detect Clang
        clang = self._detect_clang()
        if clang:
            compilers.append(clang)

        return compilers

    def _detect_gcc(self) -> Optional[CompilerInfo]:
        """Detect GCC compiler.

        Returns:
            GCC compiler info or None
        """
        # Find gcc
        gcc_path = shutil.which("gcc")
        if not gcc_path:
            return None

        # Get version
        version = self.get_version(Path(gcc_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="GCC",
            version=version,
            path=Path(gcc_path),
            type="gcc",
            architecture="x64"
        )

    def _detect_clang(self) -> Optional[CompilerInfo]:
        """Detect Clang compiler.

        Returns:
            Clang compiler info or None
        """
        # Find clang
        clang_path = shutil.which("clang")
        if not clang_path:
            return None

        # Get version
        version = self.get_version(Path(clang_path))
        if not version:
            version = "unknown"

        return CompilerInfo(
            name="Clang",
            version=version,
            path=Path(clang_path),
            type="clang",
            architecture="x64"
        )

    def validate(self, compiler: CompilerInfo) -> bool:
        """Validate compiler.

        Args:
            compiler: Compiler to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Try to compile a simple program
            test_file = Path("test.cpp")
            test_file.write_text("int main() { return 0; }")

            result = subprocess.run(
                [str(compiler.path), "-c", str(test_file)],
                capture_output=True,
                timeout=30
            )

            # Clean up
            test_file.unlink()
            test_obj = Path("test.o")
            if test_obj.exists():
                test_obj.unlink()

            return result.returncode == 0

        except Exception as e:
            self.logger.warning(f"Failed to validate {compiler.name}: {e}")
            return False
```

### 4. Compiler Manager

```python
# omni_scripts/compilers/manager.py
"""Compiler manager for detection and selection."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import hashlib

from compilers.detector import CompilerDetector, CompilerInfo
from compilers.windows_detector import WindowsCompilerDetector
from compilers.linux_detector import LinuxCompilerDetector
from logging.logger import Logger
from exceptions import CompilerError

class CompilerManager:
    """Manager for compiler detection and selection."""

    # Compiler priority (higher = more preferred)
    PRIORITY = {
        "msvc": 100,
        "msvc-clang": 90,
        "mingw-gcc": 80,
        "mingw-clang": 70,
        "gcc": 60,
        "clang": 50,
    }

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize compiler manager.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self._detectors: List[CompilerDetector] = []
        self._cache_file = Path(".compiler_cache.json")
        self._cache: Optional[Dict[str, Any]] = None

        # Initialize detectors
        self._init_detectors()

    def _init_detectors(self) -> None:
        """Initialize platform-specific detectors."""
        import platform

        if platform.system() == "Windows":
            self._detectors.append(WindowsCompilerDetector(self.logger, self.config))
        elif platform.system() == "Linux":
            self._detectors.append(LinuxCompilerDetector(self.logger, self.config))

    def detect_compilers(self, force: bool = False) -> List[CompilerInfo]:
        """Detect available compilers.

        Args:
            force: Force re-detection even if cached

        Returns:
            List of detected compilers
        """
        # Check cache
        if not force and self._load_cache():
            cached_compilers = self._get_cached_compilers()
            if cached_compilers:
                self.logger.info("Using cached compiler detection")
                return cached_compilers

        # Detect compilers
        compilers = []
        for detector in self._detectors:
            detected = detector.detect()
            compilers.extend(detected)

        # Validate compilers
        valid_compilers = []
        for compiler in compilers:
            if detector.validate(compiler):
                valid_compilers.append(compiler)
            else:
                self.logger.warning(f"Compiler {compiler.name} failed validation")

        # Sort by priority
        valid_compilers.sort(
            key=lambda c: self.PRIORITY.get(c.type, 0),
            reverse=True
        )

        # Cache results
        self._save_cache(valid_compilers)

        return valid_compilers

    def select_compiler(
        self,
        preferred: Optional[str] = None,
        force: bool = False
    ) -> Optional[CompilerInfo]:
        """Select compiler.

        Args:
            preferred: Preferred compiler type
            force: Force re-detection

        Returns:
            Selected compiler or None
        """
        # Detect compilers
        compilers = self.detect_compilers(force)

        if not compilers:
            self.logger.error("No compilers detected")
            return None

        # Select preferred compiler
        if preferred:
            for compiler in compilers:
                if compiler.type == preferred:
                    self.logger.info(f"Selected preferred compiler: {compiler.name}")
                    return compiler

            self.logger.warning(f"Preferred compiler {preferred} not found, using fallback")

        # Select highest priority compiler
        selected = compilers[0]
        self.logger.info(f"Selected compiler: {selected.name}")
        return selected

    def _load_cache(self) -> bool:
        """Load cache from file.

        Returns:
            True if cache loaded successfully
        """
        if not self._cache_file.exists():
            return False

        try:
            with open(self._cache_file, 'r') as f:
                self._cache = json.load(f)
            return True
        except Exception as e:
            self.logger.warning(f"Failed to load cache: {e}")
            return False

    def _save_cache(self, compilers: List[CompilerInfo]) -> None:
        """Save cache to file.

        Args:
            compilers: List of compilers to cache
        """
        try:
            cache_data = {
                "compilers": [
                    {
                        "name": c.name,
                        "version": c.version,
                        "path": str(c.path),
                        "type": c.type,
                        "architecture": c.architecture
                    }
                    for c in compilers
                ],
                "timestamp": str(Path(__file__).stat().st_mtime)
            }

            with open(self._cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)

            self.logger.info(f"Saved compiler cache to {self._cache_file}")

        except Exception as e:
            self.logger.warning(f"Failed to save cache: {e}")

    def _get_cached_compilers(self) -> Optional[List[CompilerInfo]]:
        """Get compilers from cache.

        Returns:
            List of cached compilers or None
        """
        if not self._cache:
            return None

        try:
            compilers = []
            for c in self._cache["compilers"]:
                compiler = CompilerInfo(
                    name=c["name"],
                    version=c["version"],
                    path=Path(c["path"]),
                    type=c["type"],
                    architecture=c["architecture"]
                )
                compilers.append(compiler)

            return compilers

        except Exception as e:
            self.logger.warning(f"Failed to parse cache: {e}")
            return None
```

### 5. Usage Example

```python
# Example usage
from compilers.manager import CompilerManager
from logging.logger import Logger
from config import load_config

# Load configuration
config = load_config()

# Initialize logger
logger = Logger(config)

# Create compiler manager
manager = CompilerManager(logger, config)

# Detect compilers
compilers = manager.detect_compilers()
print(f"Detected compilers: {compilers}")

# Select compiler
compiler = manager.select_compiler(preferred="msvc")
print(f"Selected compiler: {compiler}")
```

## Consequences

### Positive

1. **Automatic Detection:** Automatic detection of available compilers
2. **Caching:** Cache detection results to avoid repeated detection
3. **Priority-Based Selection:** Select compiler based on priority
4. **Fallback Mechanism:** Fallback to alternative compilers
5. **Validation:** Validate that detected compiler works
6. **Configuration Override:** Allow manual override
7. **Cross-Platform:** Works on Windows and Linux

### Negative

1. **Complexity:** More complex than manual configuration
2. **Detection Time:** Initial detection takes time
3. **Cache Invalidation:** Need to invalidate cache when compilers change
4. **False Positives:** May detect compilers that don't work

### Neutral

1. **Documentation:** Requires documentation for detection
2. **Testing:** Need to test detection on all platforms

## Alternatives Considered

### Alternative 1: Manual Configuration

**Description:** Require manual compiler configuration

**Pros:**
- Simpler implementation
- No detection overhead

**Cons:**
- Manual configuration required
- No automatic detection
- Poor developer experience

**Rejected:** Poor developer experience

### Alternative 2: Build System Detection

**Description:** Let build system handle detection

**Pros:**
- Build system handles complexity
- Less custom code

**Cons:**
- Less control
- Build system limitations
- Harder to customize

**Rejected:** Less control and harder to customize

### Alternative 3: Environment Variables

**Description:** Use environment variables for compiler selection

**Pros:**
- Simple to implement
- Standard approach

**Cons:**
- Manual configuration required
- No automatic detection
- Environment pollution

**Rejected:** Manual configuration required

## Related ADRs

- [ADR-010: Terminal invocation patterns for different compilers](ADR-010-terminal-invocation-patterns.md)
- [ADR-012: Cross-platform build configuration](ADR-012-cross-platform-build-configuration.md)

## References

- [MSVC Compiler Detection](https://docs.microsoft.com/en-us/cpp/build/how-to-detect-compiler-version)
- [GCC Version Detection](https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html)
- [Clang Version Detection](https://clang.llvm.org/docs/CommandGuide.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
