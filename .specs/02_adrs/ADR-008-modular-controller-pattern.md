# ADR-008: Modular Controller Pattern for Build Operations

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Python Architecture

---

## Context

The OmniCPP Template project requires a flexible, maintainable build system that can handle multiple operations (build, clean, format, install, lint, package, test, validate). The current implementation has monolithic scripts that are difficult to extend, test, and maintain.

### Current State

Build operations are implemented as standalone scripts:
- `build.py` - Build operations
- `clean.py` - Clean operations
- `format.py` - Format operations
- `install.py` - Install operations
- `lint.py` - Lint operations
- `package.py` - Package operations
- `test.py` - Test operations
- `validate_environment.py` - Environment validation

### Issues

1. **Code Duplication:** Similar logic repeated across scripts
2. **Hard to Extend:** Adding new operations requires creating new scripts
3. **Difficult to Test:** Monolithic scripts are hard to unit test
4. **Inconsistent Interfaces:** Different scripts have different interfaces
5. **No Reusability:** Common functionality cannot be reused
6. **Poor Error Handling:** Inconsistent error handling across scripts
7. **No Logging:** Inconsistent logging across operations

## Decision

Implement a **modular controller pattern** for all build operations using:
1. **Base Controller Class:** Common functionality in base class
2. **Specific Controllers:** Each operation has its own controller
3. **Dispatcher Pattern:** Central dispatcher routes commands to controllers
4. **Consistent Interface:** All controllers implement same interface
5. **Dependency Injection:** Controllers receive dependencies through constructor

### 1. Base Controller Class

```python
# omni_scripts/controller/base.py
"""Base controller class for all build operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import logging

from logging.logger import Logger
from exceptions import OmniError

class BaseController(ABC):
    """Base controller for all build operations."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize base controller.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self.project_root = Path(__file__).parent.parent.parent

    @abstractmethod
    def run(self, args: Any) -> int:
        """Run the controller operation.

        Args:
            args: Command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass

    def validate_args(self, args: Any) -> bool:
        """Validate command-line arguments.

        Args:
            args: Command-line arguments

        Returns:
            True if valid, False otherwise
        """
        return True

    def log_start(self, operation: str) -> None:
        """Log operation start.

        Args:
            operation: Operation name
        """
        self.logger.info(f"Starting {operation}...")

    def log_success(self, operation: str) -> None:
        """Log operation success.

        Args:
            operation: Operation name
        """
        self.logger.info(f"{operation} completed successfully")

    def log_error(self, operation: str, error: Exception) -> None:
        """Log operation error.

        Args:
            operation: Operation name
            error: Exception that occurred
        """
        self.logger.error(f"{operation} failed: {error}")

    def handle_error(self, error: Exception) -> int:
        """Handle error and return exit code.

        Args:
            error: Exception that occurred

        Returns:
            Exit code (1 for error)
        """
        if isinstance(error, OmniError):
            self.logger.error(str(error))
            return error.exit_code
        else:
            self.logger.error(f"Unexpected error: {error}")
            return 1
```

### 2. Build Controller

```python
# omni_scripts/controller/build_controller.py
"""Build controller for build operations."""

from typing import Any, Optional
import subprocess
from pathlib import Path

from controller.base import BaseController
from build_system.cmake import CMakeManager
from logging.logger import Logger
from exceptions import BuildError

class BuildController(BaseController):
    """Controller for build operations."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[dict] = None
    ):
        """Initialize build controller.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)
        self.cmake_manager = CMakeManager(logger, config)

    def run(self, args: Any) -> int:
        """Run build operation.

        Args:
            args: Command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.log_start("build")

            # Validate arguments
            if not self.validate_args(args):
                return 1

            # Clean if requested
            if getattr(args, 'clean', False):
                self._clean()

            # Configure
            preset = getattr(args, 'preset', 'default')
            self._configure(preset)

            # Build
            target = getattr(args, 'target', None)
            self._build(target)

            self.log_success("build")
            return 0

        except Exception as e:
            self.log_error("build", e)
            return self.handle_error(e)

    def _configure(self, preset: str) -> None:
        """Configure project.

        Args:
            preset: CMake preset to use

        Raises:
            BuildError: If configuration fails
        """
        self.logger.info(f"Configuring with preset: {preset}")
        result = self.cmake_manager.configure(preset)

        if not result.success:
            raise BuildError(f"Configuration failed: {result.error}")

    def _build(self, target: Optional[str] = None) -> None:
        """Build project.

        Args:
            target: Target to build (None for all)

        Raises:
            BuildError: If build fails
        """
        self.logger.info(f"Building target: {target or 'all'}")
        result = self.cmake_manager.build(target)

        if not result.success:
            raise BuildError(f"Build failed: {result.error}")

    def _clean(self) -> None:
        """Clean build artifacts.

        Raises:
            BuildError: If clean fails
        """
        self.logger.info("Cleaning build artifacts")
        result = self.cmake_manager.clean()

        if not result.success:
            raise BuildError(f"Clean failed: {result.error}")
```

### 3. Clean Controller

```python
# omni_scripts/controller/clean_controller.py
"""Clean controller for clean operations."""

from typing import Any, Optional
import shutil
from pathlib import Path

from controller.base import BaseController
from logging.logger import Logger
from exceptions import CleanError

class CleanController(BaseController):
    """Controller for clean operations."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[dict] = None
    ):
        """Initialize clean controller.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)

    def run(self, args: Any) -> int:
        """Run clean operation.

        Args:
            args: Command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.log_start("clean")

            # Validate arguments
            if not self.validate_args(args):
                return 1

            # Clean
            clean_all = getattr(args, 'all', False)
            self._clean(clean_all)

            self.log_success("clean")
            return 0

        except Exception as e:
            self.log_error("clean", e)
            return self.handle_error(e)

    def _clean(self, clean_all: bool = False) -> None:
        """Clean build artifacts.

        Args:
            clean_all: If True, clean all artifacts including dependencies

        Raises:
            CleanError: If clean fails
        """
        build_dir = self.project_root / "build"

        if build_dir.exists():
            self.logger.info(f"Removing build directory: {build_dir}")
            shutil.rmtree(build_dir)

        if clean_all:
            self._clean_dependencies()

    def _clean_dependencies(self) -> None:
        """Clean dependency artifacts.

        Raises:
            CleanError: If clean fails
        """
        # Clean Conan cache
        conan_cache = self.project_root / "conan" / "cache"
        if conan_cache.exists():
            self.logger.info(f"Removing Conan cache: {conan_cache}")
            shutil.rmtree(conan_cache)

        # Clean vcpkg cache
        vcpkg_cache = self.project_root / "vcpkg" / "installed"
        if vcpkg_cache.exists():
            self.logger.info(f"Removing vcpkg cache: {vcpkg_cache}")
            shutil.rmtree(vcpkg_cache)
```

### 4. Dispatcher Pattern

```python
# omni_scripts/controller/dispatcher.py
"""Dispatcher for routing commands to controllers."""

from typing import Any, Dict, Type
import logging

from controller.base import BaseController
from controller.build_controller import BuildController
from controller.clean_controller import CleanController
from controller.format_controller import FormatController
from controller.install_controller import InstallController
from controller.lint_controller import LintController
from controller.package_controller import PackageController
from controller.test_controller import TestController
from controller.config_controller import ConfigController
from logging.logger import Logger
from exceptions import OmniError

class ControllerDispatcher:
    """Dispatcher for routing commands to controllers."""

    def __init__(self, logger: Optional[Logger] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize dispatcher.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}

        # Register controllers
        self.controllers: Dict[str, Type[BaseController]] = {
            "build": BuildController,
            "clean": CleanController,
            "format": FormatController,
            "install": InstallController,
            "lint": LintController,
            "package": PackageController,
            "test": TestController,
            "validate": ConfigController,
        }

    def dispatch(self, command: str, args: Any) -> int:
        """Dispatch command to appropriate controller.

        Args:
            command: Command to execute
            args: Command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        if command not in self.controllers:
            self.logger.error(f"Unknown command: {command}")
            return 1

        controller_class = self.controllers[command]
        controller = controller_class(self.logger, self.config)

        return controller.run(args)

    def list_commands(self) -> list:
        """List available commands.

        Returns:
            List of available commands
        """
        return list(self.controllers.keys())
```

### 5. Usage Example

```python
# omni_scripts/OmniCppController.py
#!/usr/bin/env python3
"""Main entry point for OmniCppController."""

import sys
from pathlib import Path

# Add omni_scripts to path
omni_scripts_dir = Path(__file__).parent
sys.path.insert(0, str(omni_scripts_dir))

from controller.dispatcher import ControllerDispatcher
from logging.logger import Logger
from config import load_config

def main():
    """Main entry point."""
    # Load configuration
    config = load_config()

    # Initialize logger
    logger = Logger(config)

    # Initialize dispatcher
    dispatcher = ControllerDispatcher(logger, config)

    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Available commands:")
        for command in dispatcher.list_commands():
            print(f"  {command}")
        return 1

    command = sys.argv[1]
    args = sys.argv[2:]

    # Dispatch command
    return dispatcher.dispatch(command, args)

if __name__ == "__main__":
    sys.exit(main())
```

## Consequences

### Positive

1. **Modularity:** Each operation is isolated in its own controller
2. **Reusability:** Common functionality in base controller
3. **Testability:** Controllers can be unit tested independently
4. **Extensibility:** Easy to add new operations
5. **Consistency:** All controllers implement same interface
6. **Maintainability:** Changes to one operation don't affect others
7. **Error Handling:** Consistent error handling across all operations
8. **Logging:** Consistent logging across all operations

### Negative

1. **Complexity:** More complex than simple scripts
2. **Learning Curve:** Developers need to understand controller pattern
3. **Overhead:** Additional abstraction layer
4. **File Count:** More files to maintain

### Neutral

1. **Documentation:** Requires documentation for controller pattern
2. **Testing:** Need to test all controllers

## Alternatives Considered

### Alternative 1: Monolithic Scripts

**Description:** Keep current monolithic scripts

**Pros:**
- Simpler structure
- Less code

**Cons:**
- Code duplication
- Hard to test
- Hard to extend
- Inconsistent interfaces

**Rejected:** Too much duplication and poor maintainability

### Alternative 2: Function-Based Approach

**Description:** Use functions instead of classes

**Pros:**
- Simpler than classes
- Less boilerplate

**Cons:**
- No shared state
- Harder to test
- Less flexible

**Rejected:** Less flexible and harder to test

### Alternative 3: Plugin System

**Description:** Use plugin system for operations

**Pros:**
- Very flexible
- Easy to extend

**Cons:**
- Complex to implement
- Overkill for current needs
- Harder to debug

**Rejected:** Too complex for current needs

## Related ADRs

- [ADR-007: Consolidation of Python scripts into omni_scripts/](ADR-007-python-scripts-consolidation.md)
- [ADR-009: Type hints enforcement for zero pylance errors](ADR-009-type-hints-enforcement.md)
- [ADR-025: OmniCppController.py as single entry point](ADR-025-omnicppcontroller-single-entry-point.md)

## References

- [Controller Pattern](https://refactoring.guru/design-patterns/controller-pattern)
- [Python ABC](https://docs.python.org/3/library/abc.html)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
