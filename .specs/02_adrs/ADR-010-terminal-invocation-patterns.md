# ADR-010: Terminal Invocation Patterns for Different Compilers

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Cross-Platform Compilation

---

## Context

The OmniCPP Template project supports multiple compilers (MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang) across different platforms (Windows, Linux, WASM). Each compiler requires different terminal invocation patterns, environment setup, and command-line arguments. Without a consistent approach, terminal invocation becomes error-prone and platform-specific.

### Current State

Terminal invocation is handled in multiple places with inconsistent patterns:

- **Windows MSVC:** Uses `cl.exe` with Visual Studio environment
- **Windows MSVC-Clang:** Uses `clang-cl.exe` with Visual Studio environment
- **Windows MinGW-GCC:** Uses `gcc.exe` with MinGW environment
- **Windows MinGW-Clang:** Uses `clang.exe` with MinGW environment
- **Linux GCC:** Uses `gcc` with standard Linux environment
- **Linux Clang:** Uses `clang` with standard Linux environment
- **WASM:** Uses `emcc` with Emscripten environment

### Issues

1. **Inconsistent Patterns:** Different invocation patterns for each compiler
2. **Environment Setup:** Complex environment setup for each compiler
3. **Error Handling:** Inconsistent error handling across compilers
4. **Platform-Specific:** Hard to maintain cross-platform code
5. **No Abstraction:** Direct terminal invocation without abstraction
6. **Hard to Test:** Difficult to test terminal invocation

## Decision

Implement **terminal invocation patterns** with:

1. **Abstract Base Class:** Common interface for all compilers
2. **Compiler-Specific Implementations:** Each compiler has its own implementation
3. **Environment Management:** Automatic environment setup for each compiler
4. **Command Builder:** Build commands with proper arguments
5. **Error Handling:** Consistent error handling across compilers
6. **Logging:** Detailed logging of terminal invocations

### 1. Abstract Base Class

```python
# omni_scripts/compilers/base.py
"""Base class for compiler terminal invocation."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path
import subprocess
import logging

from logging.logger import Logger
from exceptions import CompilerError

class CompilerInvoker(ABC):
    """Base class for compiler terminal invocation."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize compiler invoker.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self._environment: Optional[Dict[str, str]] = None

    @abstractmethod
    def get_compiler_path(self) -> Path:
        """Get path to compiler executable.

        Returns:
            Path to compiler executable
        """
        pass

    @abstractmethod
    def get_environment(self) -> Dict[str, str]:
        """Get environment variables for compiler.

        Returns:
            Dictionary of environment variables
        """
        pass

    @abstractmethod
    def build_compile_command(
        self,
        source: Path,
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build compile command.

        Args:
            source: Source file path
            output: Output file path
            flags: Compiler flags

        Returns:
            List of command arguments
        """
        pass

    @abstractmethod
    def build_link_command(
        self,
        objects: List[Path],
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build link command.

        Args:
            objects: Object file paths
            output: Output file path
            flags: Linker flags

        Returns:
            List of command arguments
        """
        pass

    def invoke(
        self,
        command: List[str],
        cwd: Optional[Path] = None,
        env: Optional[Dict[str, str]] = None
    ) -> subprocess.CompletedProcess:
        """Invoke compiler command.

        Args:
            command: Command to execute
            cwd: Working directory
            env: Environment variables

        Returns:
            Completed process result

        Raises:
            CompilerError: If command fails
        """
        # Use provided environment or compiler environment
        if env is None:
            env = self.get_environment()

        # Log command
        self.logger.debug(f"Invoking: {' '.join(str(c) for c in command)}")

        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                check=False
            )

            # Log output
            if result.stdout:
                self.logger.debug(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                self.logger.debug(f"STDERR:\n{result.stderr}")

            # Check return code
            if result.returncode != 0:
                raise CompilerError(
                    f"Command failed with exit code {result.returncode}: "
                    f"{' '.join(str(c) for c in command)}"
                )

            return result

        except FileNotFoundError as e:
            raise CompilerError(f"Compiler not found: {e}")
        except subprocess.SubprocessError as e:
            raise CompilerError(f"Subprocess error: {e}")

    def compile(
        self,
        source: Path,
        output: Path,
        flags: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """Compile source file.

        Args:
            source: Source file path
            output: Output file path
            flags: Compiler flags

        Returns:
            Completed process result
        """
        command = self.build_compile_command(source, output, flags or [])
        return self.invoke(command)

    def link(
        self,
        objects: List[Path],
        output: Path,
        flags: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """Link object files.

        Args:
            objects: Object file paths
            output: Output file path
            flags: Linker flags

        Returns:
            Completed process result
        """
        command = self.build_link_command(objects, output, flags or [])
        return self.invoke(command)
```

### 2. MSVC Invoker

```python
# omni_scripts/compilers/msvc.py
"""MSVC compiler terminal invocation."""

from typing import List, Dict, Optional, Any
from pathlib import Path
import os
import subprocess

from compilers.base import CompilerInvoker
from logging.logger import Logger
from exceptions import CompilerError

class MSVCInvoker(CompilerInvoker):
    """MSVC compiler invoker."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize MSVC invoker.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)
        self._vs_env: Optional[Dict[str, str]] = None

    def get_compiler_path(self) -> Path:
        """Get path to MSVC compiler.

        Returns:
            Path to cl.exe
        """
        # Find cl.exe in PATH or Visual Studio installation
        cl_path = self._find_cl_exe()
        if not cl_path:
            raise CompilerError("MSVC compiler (cl.exe) not found")
        return cl_path

    def _find_cl_exe(self) -> Optional[Path]:
        """Find cl.exe executable.

        Returns:
            Path to cl.exe or None
        """
        # Check PATH
        cl_path = shutil.which("cl.exe")
        if cl_path:
            return Path(cl_path)

        # Check Visual Studio installation
        vswhere = Path("C:/Program Files (x86)/Microsoft Visual Studio/Installer/vswhere.exe")
        if vswhere.exists():
            result = subprocess.run(
                [
                    str(vswhere),
                    "-latest",
                    "-products", "*",
                    "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                    "-property", "installationPath"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                vs_path = Path(result.stdout.strip())
                cl_path = vs_path / "VC/Tools/MSVC" / "*" / "bin/Hostx64/x64/cl.exe"
                if cl_path.exists():
                    return cl_path

        return None

    def get_environment(self) -> Dict[str, str]:
        """Get MSVC environment.

        Returns:
            Dictionary of environment variables
        """
        if self._vs_env is None:
            self._vs_env = self._setup_vs_environment()
        return self._vs_env

    def _setup_vs_environment(self) -> Dict[str, str]:
        """Setup Visual Studio environment.

        Returns:
            Dictionary of environment variables
        """
        # Use vcvars64.bat to setup environment
        vcvars_path = self._find_vcvars64()
        if not vcvars_path:
            raise CompilerError("vcvars64.bat not found")

        # Execute vcvars64.bat and capture environment
        result = subprocess.run(
            f'cmd /c "{vcvars_path} && set"',
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode != 0:
            raise CompilerError(f"Failed to setup VS environment: {result.stderr}")

        # Parse environment variables
        env = os.environ.copy()
        for line in result.stdout.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                env[key] = value

        return env

    def _find_vcvars64(self) -> Optional[Path]:
        """Find vcvars64.bat.

        Returns:
            Path to vcvars64.bat or None
        """
        # Check Visual Studio installation
        vswhere = Path("C:/Program Files (x86)/Microsoft Visual Studio/Installer/vswhere.exe")
        if vswhere.exists():
            result = subprocess.run(
                [
                    str(vswhere),
                    "-latest",
                    "-products", "*",
                    "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                    "-property", "installationPath"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                vs_path = Path(result.stdout.strip())
                vcvars_path = vs_path / "VC/Auxiliary/Build/vcvars64.bat"
                if vcvars_path.exists():
                    return vcvars_path

        return None

    def build_compile_command(
        self,
        source: Path,
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build MSVC compile command.

        Args:
            source: Source file path
            output: Output file path
            flags: Compiler flags

        Returns:
            List of command arguments
        """
        command = [
            str(self.get_compiler_path()),
            "/c",  # Compile only
            "/Fo" + str(output),  # Output object file
            source
        ]

        # Add flags
        command.extend(flags)

        return command

    def build_link_command(
        self,
        objects: List[Path],
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build MSVC link command.

        Args:
            objects: Object file paths
            output: Output file path
            flags: Linker flags

        Returns:
            List of command arguments
        """
        command = [
            "link.exe",
            "/OUT:" + str(output)
        ]

        # Add object files
        command.extend(str(obj) for obj in objects)

        # Add flags
        command.extend(flags)

        return command
```

### 3. GCC Invoker

```python
# omni_scripts/compilers/gcc.py
"""GCC compiler terminal invocation."""

from typing import List, Dict, Optional, Any
from pathlib import Path
import shutil

from compilers.base import CompilerInvoker
from logging.logger import Logger
from exceptions import CompilerError

class GCCInvoker(CompilerInvoker):
    """GCC compiler invoker."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize GCC invoker.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)

    def get_compiler_path(self) -> Path:
        """Get path to GCC compiler.

        Returns:
            Path to gcc
        """
        gcc_path = shutil.which("gcc")
        if not gcc_path:
            raise CompilerError("GCC compiler not found")
        return Path(gcc_path)

    def get_environment(self) -> Dict[str, str]:
        """Get GCC environment.

        Returns:
            Dictionary of environment variables
        """
        # GCC doesn't require special environment
        return {}

    def build_compile_command(
        self,
        source: Path,
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build GCC compile command.

        Args:
            source: Source file path
            output: Output file path
            flags: Compiler flags

        Returns:
            List of command arguments
        """
        command = [
            str(self.get_compiler_path()),
            "-c",  # Compile only
            "-o", str(output),  # Output object file
            source
        ]

        # Add flags
        command.extend(flags)

        return command

    def build_link_command(
        self,
        objects: List[Path],
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build GCC link command.

        Args:
            objects: Object file paths
            output: Output file path
            flags: Linker flags

        Returns:
            List of command arguments
        """
        command = [
            str(self.get_compiler_path()),
            "-o", str(output)
        ]

        # Add object files
        command.extend(str(obj) for obj in objects)

        # Add flags
        command.extend(flags)

        return command
```

### 4. Clang Invoker

```python
# omni_scripts/compilers/clang.py
"""Clang compiler terminal invocation."""

from typing import List, Dict, Optional, Any
from pathlib import Path
import shutil

from compilers.base import CompilerInvoker
from logging.logger import Logger
from exceptions import CompilerError

class ClangInvoker(CompilerInvoker):
    """Clang compiler invoker."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Clang invoker.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)

    def get_compiler_path(self) -> Path:
        """Get path to Clang compiler.

        Returns:
            Path to clang
        """
        clang_path = shutil.which("clang")
        if not clang_path:
            raise CompilerError("Clang compiler not found")
        return Path(clang_path)

    def get_environment(self) -> Dict[str, str]:
        """Get Clang environment.

        Returns:
            Dictionary of environment variables
        """
        # Clang doesn't require special environment
        return {}

    def build_compile_command(
        self,
        source: Path,
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build Clang compile command.

        Args:
            source: Source file path
            output: Output file path
            flags: Compiler flags

        Returns:
            List of command arguments
        """
        command = [
            str(self.get_compiler_path()),
            "-c",  # Compile only
            "-o", str(output),  # Output object file
            source
        ]

        # Add flags
        command.extend(flags)

        return command

    def build_link_command(
        self,
        objects: List[Path],
        output: Path,
        flags: List[str]
    ) -> List[str]:
        """Build Clang link command.

        Args:
            objects: Object file paths
            output: Output file path
            flags: Linker flags

        Returns:
            List of command arguments
        """
        command = [
            str(self.get_compiler_path()),
            "-o", str(output)
        ]

        # Add object files
        command.extend(str(obj) for obj in objects)

        # Add flags
        command.extend(flags)

        return command
```

### 5. Compiler Factory

```python
# omni_scripts/compilers/factory.py
"""Factory for creating compiler invokers."""

from typing import Dict, Type, Optional, Any
from pathlib import Path

from compilers.base import CompilerInvoker
from compilers.msvc import MSVCInvoker
from compilers.gcc import GCCInvoker
from compilers.clang import ClangInvoker
from logging.logger import Logger
from exceptions import CompilerError

class CompilerFactory:
    """Factory for creating compiler invokers."""

    _compilers: Dict[str, Type[CompilerInvoker]] = {
        "msvc": MSVCInvoker,
        "msvc-clang": ClangInvoker,  # Uses clang-cl.exe
        "mingw-gcc": GCCInvoker,
        "mingw-clang": ClangInvoker,
        "gcc": GCCInvoker,
        "clang": ClangInvoker,
    }

    @classmethod
    def create(
        cls,
        compiler_type: str,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> CompilerInvoker:
        """Create compiler invoker.

        Args:
            compiler_type: Type of compiler
            logger: Logger instance
            config: Configuration dictionary

        Returns:
            Compiler invoker instance

        Raises:
            CompilerError: If compiler type is not supported
        """
        compiler_type = compiler_type.lower()

        if compiler_type not in cls._compilers:
            raise CompilerError(f"Unsupported compiler type: {compiler_type}")

        compiler_class = cls._compilers[compiler_type]
        return compiler_class(logger, config)

    @classmethod
    def list_compilers(cls) -> list:
        """List supported compilers.

        Returns:
            List of supported compiler types
        """
        return list(cls._compilers.keys())
```

### 6. Usage Example

```python
# Example usage
from compilers.factory import CompilerFactory
from logging.logger import Logger
from config import load_config

# Load configuration
config = load_config()

# Initialize logger
logger = Logger(config)

# Create compiler invoker
invoker = CompilerFactory.create("msvc", logger, config)

# Compile source file
source = Path("src/main.cpp")
output = Path("build/main.o")
flags = ["/std:c++23", "/W4", "/WX"]

result = invoker.compile(source, output, flags)
print(f"Compilation successful: {result.returncode}")
```

## Consequences

### Positive

1. **Consistency:** Consistent interface for all compilers
2. **Abstraction:** Abstracts away compiler-specific details
3. **Environment Management:** Automatic environment setup
4. **Error Handling:** Consistent error handling across compilers
5. **Logging:** Detailed logging of terminal invocations
6. **Testability:** Easy to test with mock implementations
7. **Extensibility:** Easy to add new compilers

### Negative

1. **Complexity:** More complex than direct invocation
2. **Learning Curve:** Developers need to understand the abstraction
3. **Overhead:** Additional abstraction layer
4. **File Count:** More files to maintain

### Neutral

1. **Documentation:** Requires documentation for each compiler
2. **Testing:** Need to test all compiler invokers

## Alternatives Considered

### Alternative 1: Direct Terminal Invocation

**Description:** Invoke compilers directly without abstraction

**Pros:**

- Simpler implementation
- Less code

**Cons:**

- Inconsistent patterns
- No environment management
- Hard to test
- Platform-specific

**Rejected:** Too inconsistent and hard to maintain

### Alternative 2: Shell Scripts

**Description:** Use shell scripts for each compiler

**Pros:**

- Simple to implement
- Platform-specific optimizations

**Cons:**

- Hard to maintain
- No abstraction
- Platform-specific
- Hard to test

**Rejected:** Hard to maintain and no abstraction

### Alternative 3: Build System Integration

**Description:** Let build system handle terminal invocation

**Pros:**

- Build system handles complexity
- Less custom code

**Cons:**

- Less control
- Build system limitations
- Harder to customize

**Rejected:** Less control and harder to customize

## Related ADRs

- [ADR-011: Compiler detection and selection strategy](ADR-011-compiler-detection-selection.md)
- [ADR-012: Cross-platform build configuration](ADR-012-cross-platform-build-configuration.md)
- [ADR-021: Secure terminal invocation](ADR-021-secure-terminal-invocation.md)

## References

- [MSVC Compiler Options](https://docs.microsoft.com/en-us/cpp/build/reference/compiler-options)
- [GCC Command Options](https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html)
- [Clang Command Line Arguments](https://clang.llvm.org/docs/CommandGuide.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)

---

**Document Control**

| Version | Date       | Author           | Changes         |
| ------- | ---------- | ---------------- | --------------- |
| 1.0     | 2026-01-07 | System Architect | Initial version |
