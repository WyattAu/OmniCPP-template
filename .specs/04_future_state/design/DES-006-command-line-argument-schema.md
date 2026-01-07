# DES-006: Command-Line Argument Schema

## Overview
Defines the command-line argument schema for the OmniCppController, including all commands, options, and their validation rules.

## Argument Schema

### Python Argument Parser

```python
from argparse import ArgumentParser, Namespace
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class Command(Enum):
    """Available commands"""
    BUILD = "build"
    CLEAN = "clean"
    CONFIGURE = "configure"
    INSTALL = "install"
    TEST = "test"
    LINT = "lint"
    FORMAT = "format"
    PACKAGE = "package"
    CONFIG = "config"
    HELP = "help"
    VERSION = "version"

@dataclass
class CommandArgument:
    """Command argument definition"""
    name: str
    short: Optional[str] = None
    long: Optional[str] = None
    help: str = ""
    required: bool = False
    action: Optional[str] = None
    type: Optional[type] = None
    choices: Optional[List[str]] = None
    default: Any = None
    nargs: Optional[str] = None
    metavar: Optional[str] = None

@dataclass
class CommandDefinition:
    """Command definition"""
    name: str
    help: str
    arguments: List[CommandArgument]
    aliases: List[str] = None

class ArgumentParserBuilder:
    """Builds argument parser for OmniCppController"""

    def __init__(self) -> None:
        """Initialize parser builder"""
        self.parser = ArgumentParser(
            prog="omnicpp",
            description="OmniCppController - Cross-platform C++ build system",
            epilog="For more information, visit: https://github.com/omnicpp/omnicpp"
        )
        self.subparsers = self.parser.add_subparsers(
            dest="command",
            help="Available commands",
            required=True
        )
        self._setup_global_options()
        self._setup_commands()

    def _setup_global_options(self) -> None:
        """Setup global options"""
        self.parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enable verbose output"
        )
        self.parser.add_argument(
            "-q", "--quiet",
            action="store_true",
            help="Suppress output (except errors)"
        )
        self.parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without doing it"
        )
        self.parser.add_argument(
            "--config-file",
            type=str,
            default="config/project.json",
            help="Path to configuration file"
        )
        self.parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default="INFO",
            help="Set logging level"
        )
        self.parser.add_argument(
            "--parallel",
            type=int,
            default=1,
            help="Number of parallel jobs"
        )

    def _setup_commands(self) -> None:
        """Setup all commands"""
        self._setup_build_command()
        self._setup_clean_command()
        self._setup_configure_command()
        self._setup_install_command()
        self._setup_test_command()
        self._setup_lint_command()
        self._setup_format_command()
        self._setup_package_command()
        self._setup_config_command()

    def _setup_build_command(self) -> None:
        """Setup build command"""
        build_parser = self.subparsers.add_parser(
            "build",
            help="Build the project",
            description="Build the project using CMake"
        )
        build_parser.add_argument(
            "--target",
            type=str,
            help="Build specific target"
        )
        build_parser.add_argument(
            "--config",
            choices=["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
            default="Release",
            help="Build configuration"
        )
        build_parser.add_argument(
            "--clean",
            action="store_true",
            help="Clean before building"
        )
        build_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose build output"
        )
        build_parser.add_argument(
            "--jobs",
            type=int,
            help="Number of parallel build jobs"
        )
        build_parser.add_argument(
            "--toolchain",
            type=str,
            help="Toolchain file to use"
        )
        build_parser.add_argument(
            "--generator",
            type=str,
            help="CMake generator to use"
        )

    def _setup_clean_command(self) -> None:
        """Setup clean command"""
        clean_parser = self.subparsers.add_parser(
            "clean",
            help="Clean build artifacts",
            description="Clean build artifacts"
        )
        clean_parser.add_argument(
            "--target",
            type=str,
            help="Clean specific target"
        )
        clean_parser.add_argument(
            "--all",
            action="store_true",
            help="Clean all build artifacts including build directory"
        )
        clean_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

    def _setup_configure_command(self) -> None:
        """Setup configure command"""
        configure_parser = self.subparsers.add_parser(
            "configure",
            help="Configure the build system",
            description="Configure the build system using CMake"
        )
        configure_parser.add_argument(
            "--generator",
            type=str,
            help="CMake generator (e.g., Ninja, Unix Makefiles, Visual Studio)"
        )
        configure_parser.add_argument(
            "--toolchain",
            type=str,
            help="Toolchain file to use"
        )
        configure_parser.add_argument(
            "--build-type",
            choices=["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
            default="Release",
            help="Build type"
        )
        configure_parser.add_argument(
            "--prefix",
            type=str,
            help="Installation prefix"
        )
        configure_parser.add_argument(
            "--define",
            action="append",
            help="Define CMake variable (can be used multiple times)"
        )
        configure_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

    def _setup_install_command(self) -> None:
        """Setup install command"""
        install_parser = self.subparsers.add_parser(
            "install",
            help="Install the project",
            description="Install the project"
        )
        install_parser.add_argument(
            "--prefix",
            type=str,
            help="Installation prefix"
        )
        install_parser.add_argument(
            "--config",
            choices=["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
            default="Release",
            help="Build configuration to install"
        )
        install_parser.add_argument(
            "--component",
            type=str,
            help="Install specific component"
        )
        install_parser.add_argument(
            "--strip",
            action="store_true",
            help="Strip binaries during installation"
        )
        install_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

    def _setup_test_command(self) -> None:
        """Setup test command"""
        test_parser = self.subparsers.add_parser(
            "test",
            help="Run tests",
            description="Run tests using the configured test framework"
        )
        test_parser.add_argument(
            "--filter",
            type=str,
            help="Filter tests by name or pattern"
        )
        test_parser.add_argument(
            "--config",
            choices=["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
            default="Debug",
            help="Build configuration to test"
        )
        test_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose test output"
        )
        test_parser.add_argument(
            "--parallel",
            action="store_true",
            help="Run tests in parallel"
        )
        test_parser.add_argument(
            "--timeout",
            type=int,
            help="Test timeout in seconds"
        )
        test_parser.add_argument(
            "--repeat",
            type=int,
            help="Repeat tests N times"
        )
        test_parser.add_argument(
            "--shuffle",
            action="store_true",
            help="Shuffle test order"
        )
        test_parser.add_argument(
            "--output",
            type=str,
            help="Output file for test results"
        )
        test_parser.add_argument(
            "--coverage",
            action="store_true",
            help="Enable code coverage"
        )

    def _setup_lint_command(self) -> None:
        """Setup lint command"""
        lint_parser = self.subparsers.add_parser(
            "lint",
            help="Run linting",
            description="Run linting tools on the codebase"
        )
        lint_parser.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix linting issues"
        )
        lint_parser.add_argument(
            "--check",
            action="store_true",
            help="Check only, don't fix"
        )
        lint_parser.add_argument(
            "--filter",
            type=str,
            help="Filter files or directories"
        )
        lint_parser.add_argument(
            "--warnings-as-errors",
            action="store_true",
            help="Treat warnings as errors"
        )
        lint_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )
        lint_parser.add_argument(
            "--tool",
            choices=["clang-tidy", "cppcheck", "all"],
            default="all",
            help="Linting tool to use"
        )

    def _setup_format_command(self) -> None:
        """Setup format command"""
        format_parser = self.subparsers.add_parser(
            "format",
            help="Format code",
            description="Format code using clang-format and cmake-format"
        )
        format_parser.add_argument(
            "--check",
            action="store_true",
            help="Check formatting without modifying files"
        )
        format_parser.add_argument(
            "--filter",
            type=str,
            help="Filter files or directories"
        )
        format_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )
        format_parser.add_argument(
            "--tool",
            choices=["clang-format", "cmake-format", "all"],
            default="all",
            help="Formatting tool to use"
        )
        format_parser.add_argument(
            "--style",
            type=str,
            help="Formatting style (overrides config)"
        )

    def _setup_package_command(self) -> None:
        """Setup package command"""
        package_parser = self.subparsers.add_parser(
            "package",
            help="Create package",
            description="Create distribution package"
        )
        package_parser.add_argument(
            "--type",
            choices=["zip", "tar.gz", "deb", "rpm", "msi", "dmg"],
            help="Package type"
        )
        package_parser.add_argument(
            "--config",
            choices=["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
            default="Release",
            help="Build configuration to package"
        )
        package_parser.add_argument(
            "--output",
            type=str,
            help="Output directory for package"
        )
        package_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )
        package_parser.add_argument(
            "--include-source",
            action="store_true",
            help="Include source code in package"
        )
        package_parser.add_argument(
            "--include-tests",
            action="store_true",
            help="Include tests in package"
        )

    def _setup_config_command(self) -> None:
        """Setup config command"""
        config_parser = self.subparsers.add_parser(
            "config",
            help="Manage configuration",
            description="Manage project configuration"
        )
        config_parser.add_argument(
            "action",
            choices=["get", "set", "unset", "list", "validate"],
            help="Configuration action"
        )
        config_parser.add_argument(
            "key",
            nargs="?",
            help="Configuration key"
        )
        config_parser.add_argument(
            "value",
            nargs="?",
            help="Configuration value"
        )
        config_parser.add_argument(
            "--file",
            type=str,
            help="Configuration file to use"
        )
        config_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

    def parse_args(self, args: Optional[List[str]] = None) -> Namespace:
        """Parse command-line arguments"""
        return self.parser.parse_args(args)

    def get_parser(self) -> ArgumentParser:
        """Get the argument parser"""
        return self.parser

# Command-line argument validation
class ArgumentValidator:
    """Validates command-line arguments"""

    @staticmethod
    def validate_build_args(args: Namespace) -> bool:
        """Validate build arguments"""
        if args.jobs and args.jobs < 1:
            raise ValueError("Number of jobs must be at least 1")
        return True

    @staticmethod
    def validate_configure_args(args: Namespace) -> bool:
        """Validate configure arguments"""
        if args.define:
            for define in args.define:
                if "=" not in define:
                    raise ValueError(f"Invalid define format: {define}")
        return True

    @staticmethod
    def validate_test_args(args: Namespace) -> bool:
        """Validate test arguments"""
        if args.timeout and args.timeout < 1:
            raise ValueError("Timeout must be at least 1 second")
        if args.repeat and args.repeat < 1:
            raise ValueError("Repeat count must be at least 1")
        return True

    @staticmethod
    def validate_config_args(args: Namespace) -> bool:
        """Validate config arguments"""
        if args.action in ["get", "set", "unset"] and not args.key:
            raise ValueError(f"Action '{args.action}' requires a key")
        if args.action == "set" and not args.value:
            raise ValueError("Action 'set' requires a value")
        return True

# Command-line argument schema
class CommandLineSchema:
    """Command-line argument schema definition"""

    COMMANDS = {
        "build": {
            "description": "Build the project",
            "arguments": {
                "--target": {"type": str, "help": "Build specific target"},
                "--config": {"type": str, "choices": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"], "default": "Release"},
                "--clean": {"action": "store_true", "help": "Clean before building"},
                "--verbose": {"action": "store_true", "help": "Enable verbose build output"},
                "--jobs": {"type": int, "help": "Number of parallel build jobs"},
                "--toolchain": {"type": str, "help": "Toolchain file to use"},
                "--generator": {"type": str, "help": "CMake generator to use"}
            }
        },
        "clean": {
            "description": "Clean build artifacts",
            "arguments": {
                "--target": {"type": str, "help": "Clean specific target"},
                "--all": {"action": "store_true", "help": "Clean all build artifacts"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"}
            }
        },
        "configure": {
            "description": "Configure the build system",
            "arguments": {
                "--generator": {"type": str, "help": "CMake generator"},
                "--toolchain": {"type": str, "help": "Toolchain file to use"},
                "--build-type": {"type": str, "choices": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"], "default": "Release"},
                "--prefix": {"type": str, "help": "Installation prefix"},
                "--define": {"action": "append", "help": "Define CMake variable"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"}
            }
        },
        "install": {
            "description": "Install the project",
            "arguments": {
                "--prefix": {"type": str, "help": "Installation prefix"},
                "--config": {"type": str, "choices": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"], "default": "Release"},
                "--component": {"type": str, "help": "Install specific component"},
                "--strip": {"action": "store_true", "help": "Strip binaries"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"}
            }
        },
        "test": {
            "description": "Run tests",
            "arguments": {
                "--filter": {"type": str, "help": "Filter tests"},
                "--config": {"type": str, "choices": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"], "default": "Debug"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"},
                "--parallel": {"action": "store_true", "help": "Run tests in parallel"},
                "--timeout": {"type": int, "help": "Test timeout in seconds"},
                "--repeat": {"type": int, "help": "Repeat tests N times"},
                "--shuffle": {"action": "store_true", "help": "Shuffle test order"},
                "--output": {"type": str, "help": "Output file for results"},
                "--coverage": {"action": "store_true", "help": "Enable code coverage"}
            }
        },
        "lint": {
            "description": "Run linting",
            "arguments": {
                "--fix": {"action": "store_true", "help": "Automatically fix issues"},
                "--check": {"action": "store_true", "help": "Check only"},
                "--filter": {"type": str, "help": "Filter files"},
                "--warnings-as-errors": {"action": "store_true", "help": "Treat warnings as errors"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"},
                "--tool": {"type": str, "choices": ["clang-tidy", "cppcheck", "all"], "default": "all"}
            }
        },
        "format": {
            "description": "Format code",
            "arguments": {
                "--check": {"action": "store_true", "help": "Check formatting"},
                "--filter": {"type": str, "help": "Filter files"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"},
                "--tool": {"type": str, "choices": ["clang-format", "cmake-format", "all"], "default": "all"},
                "--style": {"type": str, "help": "Formatting style"}
            }
        },
        "package": {
            "description": "Create package",
            "arguments": {
                "--type": {"type": str, "choices": ["zip", "tar.gz", "deb", "rpm", "msi", "dmg"]},
                "--config": {"type": str, "choices": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"], "default": "Release"},
                "--output": {"type": str, "help": "Output directory"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"},
                "--include-source": {"action": "store_true", "help": "Include source code"},
                "--include-tests": {"action": "store_true", "help": "Include tests"}
            }
        },
        "config": {
            "description": "Manage configuration",
            "arguments": {
                "action": {"choices": ["get", "set", "unset", "list", "validate"]},
                "key": {"nargs": "?"},
                "value": {"nargs": "?"},
                "--file": {"type": str, "help": "Configuration file"},
                "--verbose": {"action": "store_true", "help": "Enable verbose output"}
            }
        }
    }

    GLOBAL_OPTIONS = {
        "-v, --verbose": {"action": "store_true", "help": "Enable verbose output"},
        "-q, --quiet": {"action": "store_true", "help": "Suppress output"},
        "--dry-run": {"action": "store_true", "help": "Show what would be done"},
        "--config-file": {"type": str, "default": "config/project.json", "help": "Configuration file"},
        "--log-level": {"choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "default": "INFO"},
        "--parallel": {"type": int, "default": 1, "help": "Number of parallel jobs"}
    }
```

## Dependencies

### Internal Dependencies
- `DES-001` - ControllerConfig
- `DES-003` - Configuration schema

### External Dependencies
- `argparse` - Command-line argument parsing
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-008: Command Line Interface
- REQ-007: Configuration Management

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Argument Parsing Flow
1. Create ArgumentParserBuilder
2. Parse command-line arguments
3. Validate arguments
4. Execute command with validated arguments

### Argument Validation
- Validate argument types
- Validate argument ranges
- Validate argument combinations
- Provide clear error messages

### Help Generation
- Automatically generate help from schema
- Include examples in help text
- Provide command-specific help

### Error Handling
- Catch argument parsing errors
- Provide helpful error messages
- Suggest corrections for typos

## Usage Example

```python
from omni_scripts.cli import ArgumentParserBuilder, ArgumentValidator

# Create parser
builder = ArgumentParserBuilder()

# Parse arguments
args = builder.parse_args()

# Validate arguments
validator = ArgumentValidator()
if args.command == "build":
    validator.validate_build_args(args)
elif args.command == "configure":
    validator.validate_configure_args(args)
elif args.command == "test":
    validator.validate_test_args(args)
elif args.command == "config":
    validator.validate_config_args(args)

# Execute command
print(f"Command: {args.command}")
print(f"Arguments: {vars(args)}")
```
