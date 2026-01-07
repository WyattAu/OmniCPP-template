# Python Controller Requirements

**Document ID:** req_controller_01
**Component:** OmniCppController
**Status:** Draft
**Last Updated:** 2026-01-06

---

## 1. Overview

The Python Controller serves as the main entry point for the OmniCpp build system, providing a command-line interface for building, testing, packaging, and managing C++ projects. This document defines requirements for refactoring the monolithic controller into a modular, maintainable architecture.

---

## 2. Command-Line Interface Requirements

### 2.1 Argument Parsing

**REQ-CLI-001:** The controller SHALL use Python's `argparse` module for command-line argument parsing.

**REQ-CLI-002:** The controller SHALL support the following top-level commands:

- `configure` - Configure the build system with CMake
- `build` - Build the project
- `clean` - Clean build artifacts
- `install` - Install build artifacts
- `test` - Run tests
- `package` - Create distribution packages
- `format` - Format code with clang-format and black
- `lint` - Run static analysis with clang-tidy, pylint, and mypy
- `help` - Show help information

**REQ-CLI-003:** The controller SHALL support a `--version` flag that displays version information.

**REQ-CLI-004:** Each command SHALL have its own subparser with specific arguments.

**REQ-CLI-005:** The controller SHALL provide detailed help text for each command, including:

- Command description
- Required arguments
- Optional arguments with defaults
- Usage examples

### 2.2 Configure Command

**REQ-CLI-006:** The `configure` command SHALL accept the following arguments:

- `--build-type` (optional, choices: Debug, Release, RelWithDebInfo, MinSizeRel, default: Release)
- `--generator` (optional, CMake generator name)
- `--toolchain` (optional, toolchain file path)
- `--preset` (optional, CMake preset name)

**REQ-CLI-007:** The `configure` command SHALL validate that at least one of generator, toolchain, or preset is specified.

### 2.3 Build Command

**REQ-CLI-008:** The `build` command SHALL require the following positional arguments:

- `target` (choices: engine, game, standalone, all)
- `pipeline` (build pipeline name)
- `preset` (CMake preset name)
- `config` (choices: debug, release)

**REQ-CLI-009:** The `build` command SHALL support the following optional arguments:

- `--compiler` (choices: msvc, clang-msvc, mingw-clang, mingw-gcc, gcc, clang)
- `--clean` (flag, clean before building)

**REQ-CLI-010:** The `build` command SHALL auto-detect the default compiler if not specified.

### 2.4 Clean Command

**REQ-CLI-011:** The `clean` command SHALL accept an optional `target` argument (choices: engine, game, standalone, all).

**REQ-CLI-012:** If no target is specified for `clean`, the controller SHALL clean all targets.

### 2.5 Install Command

**REQ-CLI-013:** The `install` command SHALL require the following arguments:

- `target` (choices: engine, game, standalone, all)
- `config` (choices: debug, release)

### 2.6 Test Command

**REQ-CLI-014:** The `test` command SHALL require the following arguments:

- `target` (choices: engine, game, standalone, all)
- `config` (choices: debug, release)

**REQ-CLI-015:** The `test` command SHALL support additional arguments for test filtering (TBD).

### 2.7 Package Command

**REQ-CLI-016:** The `package` command SHALL require the following arguments:

- `target` (choices: engine, game, standalone, all)
- `config` (choices: debug, release)

**REQ-CLI-017:** The `package` command SHALL support additional arguments for package format (TBD).

### 2.8 Format Command

**REQ-CLI-018:** The `format` command SHALL support the following optional arguments:

- `--files` (list of specific files to format)
- `--directories` (list of directories to scan)
- `--check` (flag, only check formatting without modifying files)
- `--dry-run` (flag, run in dry-run mode)
- `--cpp-only` (flag, only format C++ files)
- `--python-only` (flag, only format Python files)

**REQ-CLI-019:** If no files or directories are specified for `format`, the controller SHALL scan the current directory.

### 2.9 Lint Command

**REQ-CLI-020:** The `lint` command SHALL support the following optional arguments:

- `--files` (list of specific files to lint)
- `--directories` (list of directories to scan)
- `--fix` (flag, apply automatic fixes)
- `--cpp-only` (flag, only lint C++ files)
- `--python-only` (flag, only lint Python files)

**REQ-CLI-021:** If no files or directories are specified for `lint`, the controller SHALL scan the current directory.

---

## 3. Command Dispatching Requirements

### 3.1 Architecture

**REQ-DISP-001:** The controller SHALL implement a command dispatcher pattern to route commands to appropriate handlers.

**REQ-DISP-002:** Each command SHALL have a dedicated handler function or method.

**REQ-DISP-003:** The controller SHALL validate command arguments before dispatching.

**REQ-DISP-004:** The controller SHALL provide clear error messages for invalid commands or arguments.

### 3.2 Sub-Script Integration

**REQ-DISP-005:** The controller SHALL delegate complex operations to specialized sub-scripts:

- `omni_scripts/build.py` - Build operations
- `omni_scripts/cmake.py` - CMake operations
- `omni_scripts/conan.py` - Conan operations
- `omni_scripts/format.py` - Code formatting (TBD)
- `omni_scripts/lint.py` - Static analysis (TBD)

**REQ-DISP-006:** The controller SHALL maintain a consistent interface with sub-scripts using shared data structures.

**REQ-DISP-007:** The controller SHALL handle MinGW compiler builds by executing pipelines in MSYS2 environment.

---

## 4. Error Handling Requirements

### 4.1 Exception Hierarchy

**REQ-ERR-001:** The controller SHALL define a custom exception hierarchy:

- `ControllerError` - Base exception for controller-related errors
- `InvalidTargetError` - Raised when an invalid target is specified
- `InvalidPipelineError` - Raised when an invalid pipeline is specified
- `ConfigurationError` - Raised when configuration is invalid (TBD)
- `ToolchainError` - Raised when toolchain is not available

**REQ-ERR-002:** Each exception SHALL include contextual information (e.g., command, target, pipeline).

### 4.2 Error Reporting

**REQ-ERR-003:** The controller SHALL log all errors with appropriate severity levels.

**REQ-ERR-004:** The controller SHALL provide user-friendly error messages that explain:

- What went wrong
- Why it went wrong
- How to fix it (if applicable)

**REQ-ERR-005:** The controller SHALL return appropriate exit codes:

- 0 for success
- Non-zero for failure

**REQ-ERR-006:** The controller SHALL handle unexpected exceptions gracefully and provide stack traces in debug mode.

### 4.3 Validation

**REQ-ERR-007:** The controller SHALL validate all inputs before processing.

**REQ-ERR-008:** The controller SHALL validate that required tools are available before executing commands.

**REQ-ERR-009:** The controller SHALL validate file paths and directories before operations.

---

## 5. Logging Integration Requirements

### 5.1 Logging Configuration

**REQ-LOG-001:** The controller SHALL use Python's `logging` module for all logging operations.

**REQ-LOG-002:** The controller SHALL load logging configuration from `config/logging_python.json`.

**REQ-LOG-003:** The controller SHALL support the following log levels:

- DEBUG - Detailed diagnostic information
- INFO - General informational messages
- WARNING - Warning messages for potential issues
- ERROR - Error messages for failures
- CRITICAL - Critical errors that prevent operation

### 5.2 Custom Formatters

**REQ-LOG-004:** The controller SHALL implement custom log formatters that include:

- Timestamp
- Log level
- Module name
- Function name
- Message

**REQ-LOG-005:** The controller SHALL support colored console output for different log levels (TBD).

**REQ-LOG-006:** The controller SHALL support structured logging (JSON format) for machine-readable output (TBD).

### 5.3 Log Output

**REQ-LOG-007:** The controller SHALL write logs to both console and file.

**REQ-LOG-008:** The controller SHALL rotate log files to prevent excessive disk usage.

**REQ-LOG-009:** The controller SHALL store logs in the `logs/` directory.

---

## 6. VSCode Integration Requirements

### 6.1 Launch Configuration

**REQ-VSC-001:** The controller SHALL provide a `.vscode/launch.json` configuration for debugging the controller.

**REQ-VSC-002:** The launch configuration SHALL support:

- Running the controller with different commands
- Attaching debugger to controller execution
- Setting breakpoints in controller code

**REQ-VSC-003:** The launch configuration SHALL include configurations for:

- Build engine (debug/release)
- Build game (debug/release)
- Build standalone (debug/release)
- Run tests
- Format code
- Lint code

### 6.2 Task Configuration

**REQ-VSC-004:** The controller SHALL provide a `.vscode/tasks.json` configuration for running controller commands.

**REQ-VSC-005:** The task configuration SHALL include tasks for:

- Configure build system
- Build all targets
- Clean build artifacts
- Run tests
- Format code
- Lint code
- Package distribution

**REQ-VSC-006:** Tasks SHALL be grouped logically (e.g., build, test, quality).

**REQ-VSC-007:** Tasks SHALL support problem matching for error output.

### 6.3 Settings

**REQ-VSC-008:** The controller SHALL provide `.vscode/settings.json` with Python-specific settings:

- Python interpreter path
- Linting configuration
- Formatting configuration
- Testing configuration

---

## 7. Cross-Platform Compatibility Requirements

### 7.1 Platform Detection

**REQ-PLAT-001:** The controller SHALL detect the current platform (Windows, Linux, macOS).

**REQ-PLAT-002:** The controller SHALL use platform-specific utilities from `omni_scripts/utils/platform_utils.py`.

### 7.2 Windows Support

**REQ-PLAT-003:** The controller SHALL support the following compilers on Windows:

- MSVC
- MSVC-Clang
- MinGW-Clang
- MinGW-GCC

**REQ-PLAT-004:** The controller SHALL handle Visual Studio Developer Command Prompt activation.

**REQ-PLAT-005:** The controller SHALL handle MSYS2 environment activation for MinGW compilers.

**REQ-PLAT-006:** The controller SHALL use Windows-specific path separators and environment variables.

### 7.3 Linux Support

**REQ-PLAT-007:** The controller SHALL support the following compilers on Linux:

- GCC
- Clang

**REQ-PLAT-008:** The controller SHALL use POSIX-compliant path separators and environment variables.

**REQ-PLAT-009:** The controller SHALL handle Linux-specific toolchain detection.

### 7.4 Path Handling

**REQ-PLAT-010:** The controller SHALL use `pathlib.Path` for all path operations to ensure cross-platform compatibility.

**REQ-PLAT-011:** The controller SHALL normalize paths before use.

**REQ-PLAT-012:** The controller SHALL handle both forward slashes and backslashes in paths.

---

## 8. Help and Documentation Requirements

### 8.1 Command Help

**REQ-HELP-001:** The controller SHALL provide comprehensive help for each command.

**REQ-HELP-002:** Help text SHALL include:

- Command description
- Required arguments
- Optional arguments with defaults
- Usage examples

**REQ-HELP-003:** The controller SHALL support `--help` flag for each command.

### 8.2 Documentation Generation

**REQ-HELP-004:** The controller SHALL generate documentation from docstrings (TBD).

**REQ-HELP-005:** The controller SHALL provide a `--generate-docs` command to export documentation (TBD).

**REQ-HELP-006:** Documentation SHALL be generated in Markdown format (TBD).

### 8.3 Examples

**REQ-HELP-007:** The controller SHALL provide usage examples in help text.

**REQ-HELP-008:** Examples SHALL cover common use cases:

- Basic build
- Clean build
- Configuration
- Testing
- Packaging
- Code formatting
- Static analysis

---

## 9. Performance Requirements

**REQ-PERF-001:** The controller SHALL initialize within 2 seconds on typical hardware.

**REQ-PERF-002:** The controller SHALL display progress indicators for long-running operations.

**REQ-PERF-003:** The controller SHALL support parallel execution where applicable (TBD).

---

## 10. Security Requirements

**REQ-SEC-001:** The controller SHALL validate all file paths to prevent directory traversal attacks.

**REQ-SEC-002:** The controller SHALL sanitize user input before use.

**REQ-SEC-003:** The controller SHALL not execute arbitrary code from configuration files.

---

## 11. Testing Requirements

**REQ-TEST-001:** The controller SHALL have unit tests for all command handlers.

**REQ-TEST-002:** The controller SHALL have integration tests for end-to-end workflows.

**REQ-TEST-003:** The controller SHALL have tests for error handling and edge cases.

**REQ-TEST-004:** The controller SHALL have tests for cross-platform compatibility.

---

## 12. Future Enhancements (TBD)

**REQ-FUTURE-001:** The controller SHALL support plugin architecture for custom commands (TBD).

**REQ-FUTURE-002:** The controller SHALL support configuration profiles (TBD).

**REQ-FUTURE-003:** The controller SHALL support remote build execution (TBD).

**REQ-FUTURE-004:** The controller SHALL support build caching and incremental builds (TBD).

---

## Appendix A: Exit Codes

| Code | Meaning             |
| ---- | ------------------- |
| 0    | Success             |
| 1    | General error       |
| 2    | Invalid arguments   |
| 3    | Configuration error |
| 4    | Toolchain error     |
| 5    | Build error         |
| 6    | Test failure        |
| 7    | Lint failure        |

---

## Appendix B: File Structure

```
OmniCppController.py          # Main controller entry point
omni_scripts/
  controller/
    __init__.py              # Controller module initialization
    dispatcher.py            # Command dispatcher
    cli.py                   # CLI argument parsing
    exceptions.py            # Custom exceptions
  build.py                   # Build operations
  cmake.py                   # CMake operations
  conan.py                   # Conan operations
  format.py                  # Code formatting (TBD)
  lint.py                    # Static analysis (TBD)
  utils/
    logging_utils.py         # Logging utilities
    platform_utils.py        # Platform detection
    terminal_utils.py        # Terminal environment setup
config/
  logging_python.json        # Logging configuration
.vscode/
  launch.json                # Debug configurations
  tasks.json                 # Task configurations
  settings.json              # VSCode settings
```

