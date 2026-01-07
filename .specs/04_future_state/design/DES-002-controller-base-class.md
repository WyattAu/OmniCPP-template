# DES-002: Controller Base Class and Derived Controllers

## Overview
Defines the base controller class and derived controllers for modular command handling in the OmniCppController system.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

from .DES-001 import ControllerConfig, CommandResult

@dataclass
class ControllerContext:
    """Context passed to controllers during execution"""
    config: ControllerConfig
    logger: logging.Logger
    platform: str
    compiler: Optional[str]
    build_system: Any
    package_manager: Any

class IController(ABC):
    """Base interface for all controllers"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Controller name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Controller description"""
        pass

    @abstractmethod
    def execute(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute the controller with given arguments"""
        pass

    @abstractmethod
    def validate_args(self, args: List[str]) -> bool:
        """Validate arguments before execution"""
        pass

    @abstractmethod
    def get_help(self) -> str:
        """Get help text for this controller"""
        pass

class BaseController(IController):
    """Base implementation for controllers"""

    def __init__(self, name: str, description: str) -> None:
        """Initialize base controller"""
        self._name = name
        self._description = description
        self._logger = None

    @property
    def name(self) -> str:
        """Controller name"""
        return self._name

    @property
    def description(self) -> str:
        """Controller description"""
        return self._description

    def execute(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute the controller with given arguments"""
        if not self.validate_args(args):
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=f"Invalid arguments for {self.name}",
                execution_time=0.0,
                command=f"{self.name} {' '.join(args)}"
            )

        self._logger = context.logger
        return self._execute_impl(args, context)

    @abstractmethod
    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Implementation-specific execution logic"""
        pass

    def validate_args(self, args: List[str]) -> bool:
        """Validate arguments before execution"""
        return True

    def get_help(self) -> str:
        """Get help text for this controller"""
        return f"{self.name}: {self.description}"

class BuildController(BaseController):
    """Controller for build operations"""

    def __init__(self) -> None:
        """Initialize build controller"""
        super().__init__(
            name="build",
            description="Build the project using CMake"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute build operation"""
        import time
        start_time = time.time()

        try:
            # Parse arguments
            target = None
            config = "Release"

            for i, arg in enumerate(args):
                if arg == "--target" and i + 1 < len(args):
                    target = args[i + 1]
                elif arg == "--config" and i + 1 < len(args):
                    config = args[i + 1]

            # Execute build
            self._logger.info(f"Building target: {target or 'all'} with config: {config}")

            # Delegate to build system
            result = context.build_system.build(
                target=target,
                config=config,
                parallel_jobs=context.config.parallel_jobs
            )

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"build {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Build failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"build {' '.join(args)}"
            )

    def validate_args(self, args: List[str]) -> bool:
        """Validate build arguments"""
        valid_args = ["--target", "--config", "--verbose", "--clean"]

        for i, arg in enumerate(args):
            if arg.startswith("--"):
                if arg not in valid_args:
                    return False
                # Check if argument has a value
                if arg in ["--target", "--config"] and i + 1 >= len(args):
                    return False

        return True

    def get_help(self) -> str:
        """Get help text for build controller"""
        return """build: Build the project using CMake

Usage: build [options]

Options:
  --target <name>    Build specific target
  --config <name>    Build configuration (Debug, Release, RelWithDebInfo)
  --verbose          Enable verbose output
  --clean            Clean before building

Examples:
  build
  build --target all --config Release
  build --target OmniCppEngine --config Debug
"""

class CleanController(BaseController):
    """Controller for clean operations"""

    def __init__(self) -> None:
        """Initialize clean controller"""
        super().__init__(
            name="clean",
            description="Clean build artifacts"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute clean operation"""
        import time
        import shutil
        start_time = time.time()

        try:
            target = None
            all_artifacts = False

            for i, arg in enumerate(args):
                if arg == "--target" and i + 1 < len(args):
                    target = args[i + 1]
                elif arg == "--all":
                    all_artifacts = True

            self._logger.info(f"Cleaning: {target or 'all'}")

            if all_artifacts:
                # Clean entire build directory
                build_dir = context.config.build_dir
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                    self._logger.info(f"Removed build directory: {build_dir}")
            else:
                # Clean specific target
                result = context.build_system.clean(target=target)

            execution_time = time.time() - start_time

            return CommandResult(
                success=True,
                exit_code=0,
                stdout=f"Clean completed successfully",
                stderr="",
                execution_time=execution_time,
                command=f"clean {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Clean failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"clean {' '.join(args)}"
            )

    def validate_args(self, args: List[str]) -> bool:
        """Validate clean arguments"""
        valid_args = ["--target", "--all"]

        for i, arg in enumerate(args):
            if arg.startswith("--"):
                if arg not in valid_args:
                    return False
                if arg == "--target" and i + 1 >= len(args):
                    return False

        return True

class ConfigureController(BaseController):
    """Controller for configure operations"""

    def __init__(self) -> None:
        """Initialize configure controller"""
        super().__init__(
            name="configure",
            description="Configure the build system"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute configure operation"""
        import time
        start_time = time.time()

        try:
            generator = None
            toolchain = None
            build_type = "Release"

            for i, arg in enumerate(args):
                if arg == "--generator" and i + 1 < len(args):
                    generator = args[i + 1]
                elif arg == "--toolchain" and i + 1 < len(args):
                    toolchain = args[i + 1]
                elif arg == "--build-type" and i + 1 < len(args):
                    build_type = args[i + 1]

            self._logger.info(f"Configuring with generator: {generator or 'default'}")

            result = context.build_system.configure(
                generator=generator,
                toolchain=toolchain,
                build_type=build_type
            )

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"configure {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Configure failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"configure {' '.join(args)}"
            )

class InstallController(BaseController):
    """Controller for install operations"""

    def __init__(self) -> None:
        """Initialize install controller"""
        super().__init__(
            name="install",
            description="Install the project"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute install operation"""
        import time
        start_time = time.time()

        try:
            prefix = None

            for i, arg in enumerate(args):
                if arg == "--prefix" and i + 1 < len(args):
                    prefix = args[i + 1]

            self._logger.info(f"Installing to: {prefix or 'default location'}")

            result = context.build_system.install(prefix=prefix)

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"install {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Install failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"install {' '.join(args)}"
            )

class TestController(BaseController):
    """Controller for test operations"""

    def __init__(self) -> None:
        """Initialize test controller"""
        super().__init__(
            name="test",
            description="Run tests"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute test operation"""
        import time
        start_time = time.time()

        try:
            filter_pattern = None
            verbose = False

            for i, arg in enumerate(args):
                if arg == "--filter" and i + 1 < len(args):
                    filter_pattern = args[i + 1]
                elif arg == "--verbose":
                    verbose = True

            self._logger.info(f"Running tests: {filter_pattern or 'all'}")

            result = context.build_system.test(
                filter=filter_pattern,
                verbose=verbose
            )

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"test {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Test failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"test {' '.join(args)}"
            )

class LintController(BaseController):
    """Controller for lint operations"""

    def __init__(self) -> None:
        """Initialize lint controller"""
        super().__init__(
            name="lint",
            description="Run linting"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute lint operation"""
        import time
        start_time = time.time()

        try:
            fix = False
            check_only = False

            for arg in args:
                if arg == "--fix":
                    fix = True
                elif arg == "--check":
                    check_only = True

            self._logger.info(f"Running lint: fix={fix}, check_only={check_only}")

            result = context.build_system.lint(fix=fix, check_only=check_only)

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"lint {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Lint failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"lint {' '.join(args)}"
            )

class FormatController(BaseController):
    """Controller for format operations"""

    def __init__(self) -> None:
        """Initialize format controller"""
        super().__init__(
            name="format",
            description="Format code"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute format operation"""
        import time
        start_time = time.time()

        try:
            check = False

            for arg in args:
                if arg == "--check":
                    check = True

            self._logger.info(f"Formatting code: check={check}")

            result = context.build_system.format(check=check)

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"format {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Format failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"format {' '.join(args)}"
            )

class PackageController(BaseController):
    """Controller for package operations"""

    def __init__(self) -> None:
        """Initialize package controller"""
        super().__init__(
            name="package",
            description="Create package"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute package operation"""
        import time
        start_time = time.time()

        try:
            package_type = None

            for i, arg in enumerate(args):
                if arg == "--type" and i + 1 < len(args):
                    package_type = args[i + 1]

            self._logger.info(f"Creating package: {package_type or 'default'}")

            result = context.build_system.package(type=package_type)

            execution_time = time.time() - start_time

            return CommandResult(
                success=result.success,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                command=f"package {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Package failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"package {' '.join(args)}"
            )

class ConfigController(BaseController):
    """Controller for config operations"""

    def __init__(self) -> None:
        """Initialize config controller"""
        super().__init__(
            name="config",
            description="Manage configuration"
        )

    def _execute_impl(self, args: List[str], context: ControllerContext) -> CommandResult:
        """Execute config operation"""
        import time
        start_time = time.time()

        try:
            if not args:
                # Show all config
                result = context.config.show_all()
            else:
                action = args[0]
                key = args[1] if len(args) > 1 else None
                value = args[2] if len(args) > 2 else None

                if action == "get":
                    result = context.config.get(key)
                elif action == "set":
                    result = context.config.set(key, value)
                elif action == "unset":
                    result = context.config.unset(key)
                elif action == "list":
                    result = context.config.list_all()
                else:
                    raise ValueError(f"Unknown action: {action}")

            execution_time = time.time() - start_time

            return CommandResult(
                success=True,
                exit_code=0,
                stdout=str(result),
                stderr="",
                execution_time=execution_time,
                command=f"config {' '.join(args)}"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Config failed: {str(e)}")
            return CommandResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                execution_time=execution_time,
                command=f"config {' '.join(args)}"
            )
```

## Dependencies

### Internal Dependencies
- `DES-001` - ControllerConfig and CommandResult
- `omni_scripts.logging.logger` - Logging functionality
- `omni_scripts.build_system.cmake` - Build system integration

### External Dependencies
- `abc` - Abstract base classes
- `typing` - Type hints
- `dataclasses` - Data structures
- `logging` - Logging
- `time` - Timing
- `shutil` - File operations

## Related Requirements
- REQ-001: OmniCpp Controller Entry Point
- REQ-002: Modular Controller Pattern
- REQ-003: Type Hints Enforcement
- REQ-004: Python Script Consolidation

## Related ADRs
- ADR-001: Python Build System Architecture
- ADR-002: Modular Controller Pattern

## Implementation Notes

### Controller Registration
Controllers should be registered with a dispatcher that maps command names to controller instances.

### Error Handling
- All controllers should catch exceptions and return CommandResult
- Log errors before returning
- Provide meaningful error messages

### Extensibility
- New controllers can be added by extending BaseController
- Controllers can be dynamically loaded from plugins

### Testing
- Each controller should have unit tests
- Test with valid and invalid arguments
- Test error conditions

## Usage Example

```python
from omni_scripts.controller import BuildController, CleanController, ControllerContext

# Create controllers
build_controller = BuildController()
clean_controller = CleanController()

# Execute with context
context = ControllerContext(
    config=config,
    logger=logger,
    platform="Windows",
    compiler="MSVC",
    build_system=build_system,
    package_manager=package_manager
)

result = build_controller.execute(["--target", "all", "--config", "Release"], context)
if result.success:
    print("Build successful!")
```
