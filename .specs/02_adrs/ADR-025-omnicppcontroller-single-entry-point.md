# ADR-025: OmniCppController.py as Single Entry Point

**Status:** Accepted
**Date:** 2026-01-07
**Context:** VSCode Integration

---

## Context

The OmniCPP Template project requires a single entry point for all build operations to simplify user experience and VSCode integration. The current state (`.specs/00_current_state/manifest.md`) shows multiple entry points scattered across different directories.

### Current State

Entry points are scattered:
- **Multiple Scripts:** Multiple Python scripts in different directories
- **No Single Entry:** No single entry point for all operations
- **Inconsistent CLI:** Inconsistent CLI interfaces
- **No VSCode Integration:** No VSCode integration
- **No Documentation:** No documentation for entry points

### Issues

1. **Multiple Scripts:** Multiple Python scripts in different directories
2. **No Single Entry:** No single entry point for all operations
3. **Inconsistent CLI:** Inconsistent CLI interfaces
4. **No VSCode Integration:** No VSCode integration
5. **No Documentation:** No documentation for entry points
6. **User Confusion:** Users confused about which script to use

## Decision

Implement **OmniCppController.py as single entry point** with:
1. **Single Entry Point:** Single entry point for all operations
2. **Unified CLI:** Unified CLI interface
3. **VSCode Integration:** VSCode integration
4. **Command Routing:** Command routing to controllers
5. **Help System:** Comprehensive help system
6. **Error Handling:** Consistent error handling
7. **Logging:** Integrated logging

### 1. OmniCppController.py Implementation

```python
# OmniCppController.py
# Single entry point for all build operations

#!/usr/bin/env python3
"""
OmniCppController.py - Single entry point for all build operations

This script provides a unified CLI interface for all build operations including:
- Build: Build the project
- Clean: Clean build artifacts
- Configure: Configure the project
- Format: Format code
- Install: Install dependencies
- Lint: Lint code
- Package: Package the project
- Test: Run tests
- Validate: Validate configuration

Usage:
    python OmniCppController.py <command> [options]

Commands:
    build       Build the project
    clean       Clean build artifacts
    configure   Configure the project
    format      Format code
    install     Install dependencies
    lint        Lint code
    package     Package the project
    test        Run tests
    validate    Validate configuration

Options:
    -h, --help  Show help message
    -v, --verbose  Enable verbose output
    --version   Show version information

Examples:
    python OmniCppController.py build
    python OmniCppController.py build --preset debug
    python OmniCppController.py clean
    python OmniCppController.py test --coverage
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, List

# Add omni_scripts to path
sys.path.insert(0, str(Path(__file__).parent / "omni_scripts"))

from controller.dispatcher import CommandDispatcher
from logging.logger import Logger
from exceptions import OmniCppError


class OmniCppController:
    """Single entry point for all build operations."""

    VERSION = "1.0.0"

    def __init__(self):
        """Initialize OmniCppController."""
        self.logger = Logger()
        self.dispatcher = CommandDispatcher(self.logger)

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run OmniCppController.

        Args:
            args: Command line arguments

        Returns:
            Exit code
        """
        # Parse arguments
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)

        # Set log level
        if parsed_args.verbose:
            self.logger.set_level(logging.DEBUG)

        # Handle version
        if parsed_args.version:
            print(f"OmniCppController v{self.VERSION}")
            return 0

        # Handle help
        if not parsed_args.command:
            parser.print_help()
            return 0

        # Dispatch command
        try:
            return self.dispatcher.dispatch(
                command=parsed_args.command,
                args=parsed_args
            )
        except OmniCppError as e:
            self.logger.error(f"Error: {e}")
            return 1
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
            return 130
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return 1

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser.

        Returns:
            Argument parser
        """
        parser = argparse.ArgumentParser(
            prog="OmniCppController",
            description="Single entry point for all build operations",
            epilog="For more information, visit https://github.com/omnicpp/template"
        )

        # Add version argument
        parser.add_argument(
            "--version",
            action="store_true",
            help="Show version information"
        )

        # Add verbose argument
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

        # Add subcommands
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands"
        )

        # Build command
        build_parser = subparsers.add_parser(
            "build",
            help="Build the project"
        )
        build_parser.add_argument(
            "--preset",
            default="default",
            help="Build preset (default, debug, release)"
        )
        build_parser.add_argument(
            "--target",
            help="Build target"
        )
        build_parser.add_argument(
            "--jobs",
            type=int,
            help="Number of parallel jobs"
        )

        # Clean command
        clean_parser = subparsers.add_parser(
            "clean",
            help="Clean build artifacts"
        )
        clean_parser.add_argument(
            "--all",
            action="store_true",
            help="Clean all artifacts including dependencies"
        )

        # Configure command
        configure_parser = subparsers.add_parser(
            "configure",
            help="Configure the project"
        )
        configure_parser.add_argument(
            "--preset",
            default="default",
            help="Configure preset (default, debug, release)"
        )
        configure_parser.add_argument(
            "--generator",
            help="CMake generator"
        )

        # Format command
        format_parser = subparsers.add_parser(
            "format",
            help="Format code"
        )
        format_parser.add_argument(
            "--check",
            action="store_true",
            help="Check formatting without modifying files"
        )
        format_parser.add_argument(
            "--fix",
            action="store_true",
            help="Fix formatting issues"
        )

        # Install command
        install_parser = subparsers.add_parser(
            "install",
            help="Install dependencies"
        )
        install_parser.add_argument(
            "--package-manager",
            choices=["conan", "vcpkg", "cpm"],
            help="Package manager to use"
        )
        install_parser.add_argument(
            "--update",
            action="store_true",
            help="Update dependencies"
        )

        # Lint command
        lint_parser = subparsers.add_parser(
            "lint",
            help="Lint code"
        )
        lint_parser.add_argument(
            "--fix",
            action="store_true",
            help="Fix linting issues"
        )
        lint_parser.add_argument(
            "--check",
            action="store_true",
            help="Check linting without modifying files"
        )

        # Package command
        package_parser = subparsers.add_parser(
            "package",
            help="Package the project"
        )
        package_parser.add_argument(
            "--type",
            choices=["zip", "tgz", "deb", "rpm"],
            help="Package type"
        )
        package_parser.add_argument(
            "--output",
            help="Output directory"
        )

        # Test command
        test_parser = subparsers.add_parser(
            "test",
            help="Run tests"
        )
        test_parser.add_argument(
            "--coverage",
            action="store_true",
            help="Enable code coverage"
        )
        test_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose test output"
        )
        test_parser.add_argument(
            "--filter",
            help="Test filter"
        )

        # Validate command
        validate_parser = subparsers.add_parser(
            "validate",
            help="Validate configuration"
        )
        validate_parser.add_argument(
            "--config",
            help="Configuration file to validate"
        )
        validate_parser.add_argument(
            "--strict",
            action="store_true",
            help="Enable strict validation"
        )

        return parser


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    controller = OmniCppController()
    return controller.run()


if __name__ == "__main__":
    sys.exit(main())
```

### 2. Command Dispatcher

```python
# omni_scripts/controller/dispatcher.py
# Command dispatcher for routing commands to controllers

import logging
from typing import Dict, Any, Optional
import argparse

from controller.build_controller import BuildController
from controller.clean_controller import CleanController
from controller.configure_controller import ConfigureController
from controller.format_controller import FormatController
from controller.install_controller import InstallController
from controller.lint_controller import LintController
from controller.package_controller import PackageController
from controller.test_controller import TestController
from controller.config_controller import ConfigController
from exceptions import OmniCppError


class CommandDispatcher:
    """Command dispatcher for routing commands to controllers."""

    def __init__(self, logger: logging.Logger):
        """Initialize command dispatcher.

        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.controllers: Dict[str, Any] = {
            "build": BuildController(logger),
            "clean": CleanController(logger),
            "configure": ConfigureController(logger),
            "format": FormatController(logger),
            "install": InstallController(logger),
            "lint": LintController(logger),
            "package": PackageController(logger),
            "test": TestController(logger),
            "validate": ConfigController(logger),
        }

    def dispatch(self, command: str, args: argparse.Namespace) -> int:
        """Dispatch command to controller.

        Args:
            command: Command to dispatch
            args: Command arguments

        Returns:
            Exit code

        Raises:
            OmniCppError: If command is not found
        """
        self.logger.info(f"Dispatching command: {command}")

        # Get controller
        controller = self.controllers.get(command)

        if not controller:
            raise OmniCppError(f"Unknown command: {command}")

        # Execute command
        return controller.execute(args)
```

### 3. VSCode Integration

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build (Default)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": "$gcc"
    },
    {
      "label": "Build (Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build",
        "--preset",
        "debug"
      ],
      "group": "build",
      "problemMatcher": "$gcc"
    },
    {
      "label": "Build (Release)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build",
        "--preset",
        "release"
      ],
      "group": "build",
      "problemMatcher": "$gcc"
    },
    {
      "label": "Clean",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "clean"
      ],
      "problemMatcher": []
    },
    {
      "label": "Configure",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "configure"
      ],
      "problemMatcher": []
    },
    {
      "label": "Format",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "format",
        "--fix"
      ],
      "problemMatcher": []
    },
    {
      "label": "Lint",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "lint"
      ],
      "problemMatcher": []
    },
    {
      "label": "Test",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "test"
      ],
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "problemMatcher": []
    },
    {
      "label": "Test (Coverage)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "test",
        "--coverage"
      ],
      "group": "test",
      "problemMatcher": []
    }
  ]
}
```

### 4. Usage Examples

```bash
# Build project
python OmniCppController.py build

# Build with preset
python OmniCppController.py build --preset debug

# Clean build artifacts
python OmniCppController.py clean

# Configure project
python OmniCppController.py configure

# Format code
python OmniCppController.py format --fix

# Install dependencies
python OmniCppController.py install

# Lint code
python OmniCppController.py lint

# Package project
python OmniCppController.py package --type zip

# Run tests
python OmniCppController.py test

# Run tests with coverage
python OmniCppController.py test --coverage

# Validate configuration
python OmniCppController.py validate

# Show help
python OmniCppController.py --help

# Show version
python OmniCppController.py --version

# Enable verbose output
python OmniCppController.py build --verbose
```

## Consequences

### Positive

1. **Single Entry:** Single entry point for all operations
2. **Unified CLI:** Unified CLI interface
3. **VSCode Integration:** VSCode integration
4. **User Experience:** Improved user experience
5. **Documentation:** Easier to document
6. **Maintenance:** Easier to maintain
7. **Consistency:** Consistent error handling and logging

### Negative

1. **Complexity:** More complex than multiple scripts
2. **Learning Curve:** Learning curve for new CLI
3. **Migration:** Migration from old scripts
4. **Testing:** Need to test all commands

### Neutral

1. **Documentation:** Requires documentation for new CLI
2. **Training:** Need to train users on new CLI

## Alternatives Considered

### Alternative 1: Multiple Entry Points

**Description:** Keep multiple entry points

**Pros:**
- Simpler implementation
- No migration needed

**Cons:**
- User confusion
- Inconsistent CLI
- No VSCode integration

**Rejected:** User confusion and inconsistent CLI

### Alternative 2: Makefile

**Description:** Use Makefile as entry point

**Pros:**
- Standard build tool
- Familiar to developers

**Cons:**
- Platform-specific
- Limited functionality
- No Python integration

**Rejected:** Platform-specific and limited functionality

### Alternative 3: CMake Targets

**Description:** Use CMake targets as entry points

**Pros:**
- Integrated with CMake
- Cross-platform

**Cons:**
- Limited functionality
- No Python integration
- Complex configuration

**Rejected:** Limited functionality and no Python integration

## Related ADRs

- [ADR-008: Modular controller pattern for build operations](ADR-008-modular-controller-pattern.md)
- [ADR-026: VSCode tasks.json and launch.json configuration](ADR-026-vscode-tasks-launch-configuration.md)

## References

- [argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [VSCode Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [CLI Design](https://clig.dev/)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
