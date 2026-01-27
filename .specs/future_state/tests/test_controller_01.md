# Controller Test Plan

**Document ID:** test_controller_01
**Component:** OmniCppController
**Status:** Draft
**Last Updated:** 2026-01-06

---

## 1. Test Environment Requirements

### 1.1 Hardware Requirements

- CPU: x86_64 or ARM64 processor
- RAM: Minimum 8GB
- Disk: 10GB free space

### 1.2 Software Requirements

- Python 3.10+
- CMake 3.20+
- Git
- VSCode (for integration tests)

### 1.3 Platform Support

- Windows 10/11
- Linux (Ubuntu 20.04+, Debian 11+)
- macOS 12+ (future)

### 1.4 Test Data

- Sample C++ project structure
- Configuration files (config/\*.json)
- Test source files (C++ and Python)

---

## 2. Unit Tests

### 2.1 CLI Argument Parsing Tests

**TC-CLI-001:** Verify argparse module is used

- Input: Import controller module
- Expected: argparse module is imported and used
- Success: Module import succeeds

**TC-CLI-002:** Verify all top-level commands are registered

- Input: List available commands
- Expected: configure, build, clean, install, test, package, format, lint, help
- Success: All 9 commands present

**TC-CLI-003:** Verify --version flag works

- Input: `python OmniCppController.py --version`
- Expected: Version information displayed
- Success: Exit code 0, version shown

**TC-CLI-004:** Verify configure command arguments

- Input: `configure --build-type Debug --generator Ninja`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-005:** Verify configure command validation

- Input: `configure` (no generator/toolchain/preset)
- Expected: Error message requiring at least one option
- Success: Exit code 2, error message shown

**TC-CLI-006:** Verify build command required arguments

- Input: `build engine default_preset debug`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-007:** Verify build command optional arguments

- Input: `build engine default_preset debug --compiler msvc --clean`
- Expected: All arguments parsed correctly
- Success: No validation errors

**TC-CLI-008:** Verify build command auto-detects compiler

- Input: `build engine default_preset debug` (no --compiler)
- Expected: Compiler auto-detected based on platform
- Success: Compiler selected without error

**TC-CLI-009:** Verify clean command with target

- Input: `clean engine`
- Expected: Target argument parsed correctly
- Success: No validation errors

**TC-CLI-010:** Verify clean command without target

- Input: `clean`
- Expected: Defaults to 'all' target
- Success: No validation errors

**TC-CLI-011:** Verify install command arguments

- Input: `install engine debug`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-012:** Verify test command arguments

- Input: `test engine debug`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-013:** Verify package command arguments

- Input: `package standalone release`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-014:** Verify format command with files

- Input: `format --files file1.cpp file2.py`
- Expected: Files list parsed correctly
- Success: No validation errors

**TC-CLI-015:** Verify format command with directories

- Input: `format --directories src/ include/`
- Expected: Directories list parsed correctly
- Success: No validation errors

**TC-CLI-016:** Verify format command flags

- Input: `format --check --dry-run --cpp-only`
- Expected: All flags parsed correctly
- Success: No validation errors

**TC-CLI-017:** Verify format command defaults

- Input: `format` (no files/directories)
- Expected: Scans current directory
- Success: No validation errors

**TC-CLI-018:** Verify lint command arguments

- Input: `lint --files file1.cpp --fix --cpp-only`
- Expected: Arguments parsed correctly
- Success: No validation errors

**TC-CLI-019:** Verify lint command defaults

- Input: `lint` (no files/directories)
- Expected: Scans current directory
- Success: No validation errors

**TC-CLI-020:** Verify help command

- Input: `help` or `--help`
- Expected: Comprehensive help displayed
- Success: Exit code 0, help shown

---

### 2.2 Command Dispatching Tests

**TC-DISP-001:** Verify command dispatcher pattern

- Input: Execute any valid command
- Expected: Command routed to correct handler
- Success: Handler function called

**TC-DISP-002:** Verify each command has dedicated handler

- Input: Execute each command
- Expected: Unique handler for each command
- Success: All commands execute

**TC-DISP-003:** Verify argument validation before dispatch

- Input: Invalid arguments for any command
- Expected: Validation error before handler called
- Success: Handler not called, error shown

**TC-DISP-004:** Verify clear error messages for invalid commands

- Input: `invalid_command`
- Expected: Error message with suggestions
- Success: Exit code 2, error shown

**TC-DISP-005:** Verify sub-script integration for build

- Input: `build engine default_preset debug`
- Expected: Delegates to omni_scripts/build.py
- Success: Build script called

**TC-DISP-006:** Verify sub-script integration for cmake

- Input: `configure --preset default`
- Expected: Delegates to omni_scripts/cmake.py
- Success: CMake script called

**TC-DISP-007:** Verify sub-script integration for conan

- Input: Build with Conan dependencies
- Expected: Delegates to omni_scripts/conan.py
- Success: Conan script called

**TC-DISP-008:** Verify MinGW builds use MSYS2

- Input: `build engine default_preset debug --compiler mingw-gcc`
- Expected: Executes in MSYS2 environment
- Success: Build succeeds

**TC-DISP-009:** Verify consistent interface with sub-scripts

- Input: Any command using sub-scripts
- Expected: Shared data structures used
- Success: Data passed correctly

---

### 2.3 Error Handling Tests

**TC-ERR-001:** Verify ControllerError exception

- Input: Trigger controller error
- Expected: ControllerError raised with context
- Success: Exception caught and logged

**TC-ERR-002:** Verify InvalidTargetError exception

- Input: Invalid target specified
- Expected: InvalidTargetError raised
- Success: Error message shows invalid target

**TC-ERR-003:** Verify InvalidPipelineError exception

- Input: Invalid pipeline specified
- Expected: InvalidPipelineError raised
- Success: Error message shows invalid pipeline

**TC-ERR-004:** Verify ConfigurationError exception

- Input: Invalid configuration
- Expected: ConfigurationError raised
- Success: Error message shows config issue

**TC-ERR-005:** Verify ToolchainError exception

- Input: Toolchain not available
- Expected: ToolchainError raised
- Success: Error message shows missing toolchain

**TC-ERR-006:** Verify exception includes contextual info

- Input: Any exception raised
- Expected: Exception includes command, target, pipeline
- Success: Context present in error

**TC-ERR-007:** Verify error logging with severity

- Input: Trigger errors of different types
- Expected: Errors logged with appropriate levels
- Success: Logs show correct severity

**TC-ERR-008:** Verify user-friendly error messages

- Input: Any error condition
- Expected: Message explains what, why, how to fix
- Success: Error message is actionable

**TC-ERR-009:** Verify exit code 0 for success

- Input: Successful command execution
- Expected: Exit code 0
- Success: Exit code is 0

**TC-ERR-010:** Verify non-zero exit code for failure

- Input: Failed command execution
- Expected: Exit code non-zero
- Success: Exit code matches error type

**TC-ERR-011:** Verify graceful exception handling

- Input: Unexpected exception
- Expected: Caught and logged with stack trace in debug
- Success: No crash, error logged

**TC-ERR-012:** Verify input validation

- Input: Invalid user input
- Expected: Validation error before processing
- Success: Error shown, no processing

**TC-ERR-013:** Verify tool availability validation

- Input: Command requiring missing tool
- Expected: Error before execution
- Success: Tool not found error shown

**TC-ERR-014:** Verify file path validation

- Input: Invalid file path
- Expected: Validation error
- Success: Invalid path error shown

---

### 2.4 Logging Integration Tests

**TC-LOG-001:** Verify logging module usage

- Input: Execute any command
- Expected: Python logging module used
- Success: Logs generated

**TC-LOG-002:** Verify logging config loaded

- Input: Start controller
- Expected: config/logging_python.json loaded
- Success: Config applied

**TC-LOG-003:** Verify DEBUG level logging

- Input: Run with debug verbosity
- Expected: Detailed diagnostic messages
- Success: DEBUG messages present

**TC-LOG-004:** Verify INFO level logging

- Input: Normal operation
- Expected: General informational messages
- Success: INFO messages present

**TC-LOG-005:** Verify WARNING level logging

- Input: Potential issue scenario
- Expected: Warning messages
- Success: WARNING messages present

**TC-LOG-006:** Verify ERROR level logging

- Input: Error scenario
- Expected: Error messages
- Success: ERROR messages present

**TC-LOG-007:** Verify CRITICAL level logging

- Input: Critical failure
- Expected: Critical error messages
- Success: CRITICAL messages present

**TC-LOG-008:** Verify custom formatter includes timestamp

- Input: Any log message
- Expected: Timestamp in log format
- Success: Timestamp present

**TC-LOG-009:** Verify custom formatter includes level

- Input: Any log message
- Expected: Log level in format
- Success: Level present

**TC-LOG-010:** Verify custom formatter includes module

- Input: Any log message
- Expected: Module name in format
- Success: Module present

**TC-LOG-011:** Verify custom formatter includes function

- Input: Any log message
- Expected: Function name in format
- Success: Function present

**TC-LOG-012:** Verify console output

- Input: Execute command
- Expected: Logs written to console
- Success: Console logs visible

**TC-LOG-013:** Verify file output

- Input: Execute command
- Expected: Logs written to file
- Success: Log file created in logs/

**TC-LOG-014:** Verify log rotation

- Input: Generate large log file
- Expected: Log rotated when size limit reached
- Success: Multiple log files present

---

### 2.5 Platform Detection Tests

**TC-PLAT-001:** Verify Windows platform detection

- Input: Run on Windows
- Expected: Platform detected as Windows
- Success: Platform variable set correctly

**TC-PLAT-002:** Verify Linux platform detection

- Input: Run on Linux
- Expected: Platform detected as Linux
- Success: Platform variable set correctly

**TC-PLAT-003:** Verify macOS platform detection

- Input: Run on macOS
- Expected: Platform detected as macOS
- Success: Platform variable set correctly

**TC-PLAT-004:** Verify platform_utils usage

- Input: Any platform operation
- Expected: Uses omni_scripts/utils/platform_utils.py
- Success: Platform utilities called

**TC-PLAT-005:** Verify Windows compiler support

- Input: List compilers on Windows
- Expected: MSVC, MSVC-Clang, MinGW-Clang, MinGW-GCC
- Success: All compilers detected

**TC-PLAT-006:** Verify VS Dev Prompt activation

- Input: Build with MSVC on Windows
- Expected: VS Dev Prompt activated
- Success: Build succeeds

**TC-PLAT-007:** Verify MSYS2 activation

- Input: Build with MinGW on Windows
- Expected: MSYS2 environment activated
- Success: Build succeeds

**TC-PLAT-008:** Verify Windows path handling

- Input: Use Windows paths
- Expected: Backslashes handled correctly
- Success: Paths work correctly

**TC-PLAT-009:** Verify Linux compiler support

- Input: List compilers on Linux
- Expected: GCC, Clang
- Success: Both compilers detected

**TC-PLAT-010:** Verify Linux path handling

- Input: Use Linux paths
- Expected: Forward slashes handled correctly
- Success: Paths work correctly

**TC-PLAT-011:** Verify pathlib.Path usage

- Input: Any path operation
- Expected: Uses pathlib.Path
- Success: Cross-platform compatible

**TC-PLAT-012:** Verify path normalization

- Input: Mixed slash paths
- Expected: Paths normalized
- Success: Consistent path format

---

## 3. Integration Tests

### 3.1 End-to-End Workflow Tests

**TC-E2E-001:** Verify configure -> build workflow

- Input: Configure then build
- Expected: Successful build
- Success: Build artifacts created

**TC-E2E-002:** Verify build -> test workflow

- Input: Build then test
- Expected: Tests run successfully
- Success: All tests pass

**TC-E2E-003:** Verify build -> package workflow

- Input: Build then package
- Expected: Package created
- Success: Package file exists

**TC-E2E-004:** Verify clean -> build workflow

- Input: Clean then build
- Expected: Fresh build
- Success: No stale artifacts

**TC-E2E-005:** Verify format -> lint workflow

- Input: Format then lint
- Expected: No lint errors
- Success: Code passes linting

**TC-E2E-006:** Verify full workflow (configure, build, test, package)

- Input: Execute all commands in sequence
- Expected: All steps succeed
- Success: Complete pipeline works

---

### 3.2 VSCode Integration Tests

**TC-VSC-001:** Verify launch.json exists

- Input: Check .vscode/launch.json
- Expected: File exists with valid JSON
- Success: File present and valid

**TC-VSC-002:** Verify launch configurations

- Input: Inspect launch.json
- Expected: Configurations for all commands
- Success: All configs present

**TC-VSC-003:** Verify tasks.json exists

- Input: Check .vscode/tasks.json
- Expected: File exists with valid JSON
- Success: File present and valid

**TC-VSC-004:** Verify task configurations

- Input: Inspect tasks.json
- Expected: Tasks for all commands
- Success: All tasks present

**TC-VSC-005:** Verify settings.json exists

- Input: Check .vscode/settings.json
- Expected: File exists with valid JSON
- Success: File present and valid

**TC-VSC-006:** Verify Python settings

- Input: Inspect settings.json
- Expected: Python-specific settings
- Success: Settings configured

**TC-VSC-007:** Verify debugging works

- Input: Debug controller in VSCode
- Expected: Breakpoints hit
- Success: Debugging functional

---

## 4. Performance Tests

**TC-PERF-001:** Verify initialization time

- Input: Start controller
- Expected: Initializes within 2 seconds
- Success: Time < 2s

**TC-PERF-002:** Verify progress indicators

- Input: Long-running operation
- Expected: Progress shown
- Success: Progress visible

---

## 5. Security Tests

**TC-SEC-001:** Verify path traversal prevention

- Input: Path with ../ sequences
- Expected: Path validated and rejected
- Success: Error shown

**TC-SEC-002:** Verify input sanitization

- Input: Malicious input
- Expected: Input sanitized
- Success: No code execution

**TC-SEC-003:** Verify config file safety

- Input: Malicious config file
- Expected: No arbitrary code execution
- Success: Safe execution

---

## 6. Success Criteria

The controller test plan is considered successful when:

1. All unit tests pass (100% coverage of requirements)
2. All integration tests pass
3. All performance tests meet requirements
4. All security tests pass
5. Tests run on all supported platforms
6. Test execution time is acceptable
7. Test results are reproducible
8. Test documentation is complete

---

## 7. Test Execution Summary

| Test Category       | Test Cases | Pass/Fail | Coverage |
| ------------------- | ---------- | --------- | -------- |
| CLI Parsing         | 20         | TBD       | 100%     |
| Command Dispatching | 9          | TBD       | 100%     |
| Error Handling      | 14         | TBD       | 100%     |
| Logging             | 14         | TBD       | 100%     |
| Platform Detection  | 12         | TBD       | 100%     |
| Integration         | 7          | TBD       | 100%     |
| VSCode Integration  | 7          | TBD       | 100%     |
| Performance         | 2          | TBD       | 100%     |
| Security            | 3          | TBD       | 100%     |
| **Total**           | **88**     | **TBD**   | **100%** |

