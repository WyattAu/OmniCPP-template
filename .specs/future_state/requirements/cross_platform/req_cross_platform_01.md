# Cross-Platform Compilation Requirements

**Document ID:** req_cross_platform_01
**Status:** Draft
**Priority:** Critical
**Created:** 2026-01-06

---

## 1. Overview

This document defines requirements for cross-platform compilation support in the OmniCPP template. The system must support multiple platforms, compilers, and build targets with automatic detection and configuration.

---

## 2. Platform Detection Requirements

### 2.1 Host Platform Detection

**REQ-PLATFORM-001:** The system SHALL automatically detect the host operating system at runtime.

**Acceptance Criteria:**

- System identifies Windows, Linux, and macOS
- Detection uses platform-specific APIs (sys.platform, os.name)
- Detection occurs before any compiler operations
- Platform information is logged for debugging

**REQ-PLATFORM-002:** The system SHALL detect host architecture (x86_64, ARM64, etc.).

**Acceptance Criteria:**

- Architecture detection uses platform-specific methods
- Supports x86_64, ARM64, and other common architectures
- Architecture information is available to build configuration

### 2.2 Target Platform Detection

**REQ-PLATFORM-003:** The system SHALL support specifying target platform for cross-compilation.

**Acceptance Criteria:**

- Target platform can be specified via command-line arguments
- Target platform can be specified via configuration files
- Default target platform is host platform if not specified
- Invalid target platforms are rejected with clear error messages

---

## 3. Compiler Detection Requirements

### 3.1 Windows Compiler Detection

**REQ-COMPILER-001:** The system SHALL detect and validate MSVC compiler installations.

**Acceptance Criteria:**

- Detects Visual Studio 2022 installations (Community, Professional, Enterprise)
- Validates vcvars64.bat availability
- Checks MSVC version compatibility with C++23
- Supports both x64 and ARM64 architectures
- Provides clear error messages if MSVC not found

**REQ-COMPILER-002:** The system SHALL detect and validate MSVC-Clang compiler installations.

**Acceptance Criteria:**

- Detects Clang integration with MSVC toolchain
- Validates clang-cl.exe availability
- Checks Clang version compatibility with C++23
- Supports both x64 and ARM64 architectures
- Provides clear error messages if MSVC-Clang not found

**REQ-COMPILER-003:** The system SHALL detect and validate MinGW-GCC compiler installations.

**Acceptance Criteria:**

- Detects MinGW-w64 GCC installations
- Validates gcc.exe and g++.exe availability
- Checks GCC version compatibility with C++23
- Supports both UCRT64 and MSYS2 environments
- Provides clear error messages if MinGW-GCC not found

**REQ-COMPILER-004:** The system SHALL detect and validate MinGW-Clang compiler installations.

**Acceptance Criteria:**

- Detects MinGW-w64 Clang installations
- Validates clang.exe and clang++.exe availability
- Checks Clang version compatibility with C++23
- Supports both UCRT64 and MSYS2 environments
- Provides clear error messages if MinGW-Clang not found

### 3.2 Linux Compiler Detection

**REQ-COMPILER-005:** The system SHALL detect and validate GCC compiler installations on Linux.

**Acceptance Criteria:**

- Detects system GCC installation
- Validates gcc and g++ availability
- Checks GCC version compatibility with C++23
- Supports multiple GCC versions if present
- Provides clear error messages if GCC not found

**REQ-COMPILER-006:** The system SHALL detect and validate Clang compiler installations on Linux.

**Acceptance Criteria:**

- Detects system Clang installation
- Validates clang and clang++ availability
- Checks Clang version compatibility with C++23
- Supports multiple Clang versions if present
- Provides clear error messages if Clang not found

### 3.3 WASM Compiler Detection

**REQ-COMPILER-007:** The system SHALL detect and validate Emscripten compiler installations.

**Acceptance Criteria:**

- Detects Emscripten SDK installation
- Validates emcc and em++ availability
- Checks Emscripten version compatibility with C++23
- Validates emcmake and emconfigure availability
- Provides clear error messages if Emscripten not found

### 3.4 Compiler Selection Logic

**REQ-COMPILER-008:** The system SHALL provide automatic compiler selection based on platform and configuration.

**Acceptance Criteria:**

- Default compiler selection follows platform conventions
- User can override automatic selection
- Selection considers compiler availability and version
- Selection considers C++23 feature support
- Logs selected compiler and reasoning

**REQ-COMPILER-009:** The system SHALL validate compiler C++23 support before use.

**Acceptance Criteria:**

- Checks compiler version against minimum requirements
- Tests C++23 feature availability
- Provides warnings for partial C++23 support
- Falls back to C++20 if C++23 not available (configurable)
- Logs validation results

---

## 4. Terminal Environment Setup Requirements

### 4.1 Windows Terminal Setup

**REQ-TERMINAL-001:** The system SHALL set up Visual Studio Developer Command Prompt environment for MSVC and MSVC-Clang.

**Acceptance Criteria:**

- Locates vcvars64.bat automatically
- Supports multiple Visual Studio editions and versions
- Sets required environment variables (INCLUDE, LIB, PATH, etc.)
- Supports both x64 and ARM64 architectures
- Provides clear error messages if setup fails

**REQ-TERMINAL-002:** The system SHALL set up MSYS2 UCRT64 environment for MinGW-GCC and MinGW-Clang.

**Acceptance Criteria:**

- Locates MSYS2 installation automatically
- Sets MSYSTEM, MSYSTEM_PREFIX, and related variables
- Configures PATH for UCRT64 tools
- Converts Windows paths to MSYS2 format correctly
- Supports both UCRT64 and MSYS2 environments
- Provides clear error messages if setup fails

### 4.2 Linux Terminal Setup

**REQ-TERMINAL-003:** The system SHALL set up appropriate environment for Linux compilers.

**Acceptance Criteria:**

- Preserves existing environment variables
- Adds compiler-specific paths to PATH if needed
- Supports custom environment variable overrides
- Validates environment setup before proceeding
- Provides clear error messages if setup fails

### 4.3 Environment Validation

**REQ-TERMINAL-004:** The system SHALL validate terminal environment setup before executing commands.

**Acceptance Criteria:**

- Verifies required environment variables are set
- Checks compiler executables are accessible
- Validates PATH configuration
- Tests compiler invocation with simple command
- Provides detailed error messages if validation fails

---

## 5. Cross-Compilation Requirements

### 5.1 Cross-Compilation Targets

**REQ-CROSS-001:** The system SHALL support cross-compilation from Windows to Linux.

**Acceptance Criteria:**

- Supports x86_64-linux-gnu target
- Supports ARM64-linux-gnu target
- Uses appropriate toolchain files
- Configures sysroot and cross-compiler paths
- Validates cross-compiler availability

**REQ-CROSS-002:** The system SHALL support cross-compilation from Windows to WASM.

**Acceptance Criteria:**

- Uses Emscripten toolchain
- Configures WASM-specific build options
- Supports both WASM and ASM.js output
- Validates Emscripten SDK availability
- Provides WASM-specific error messages

### 5.2 Toolchain File Selection

**REQ-CROSS-003:** The system SHALL automatically select appropriate CMake toolchain files for cross-compilation.

**Acceptance Criteria:**

- Selects toolchain file based on target platform
- Supports custom toolchain file paths
- Validates toolchain file syntax
- Passes toolchain file to CMake correctly
- Logs selected toolchain file

**REQ-CROSS-004:** The system SHALL support custom toolchain file configuration.

**Acceptance Criteria:**

- Allows user to specify custom toolchain file
- Validates custom toolchain file exists
- Validates custom toolchain file syntax
- Provides clear error messages for invalid toolchain files
- Logs custom toolchain file usage

---

## 6. Build Target Selection Requirements

**REQ-BUILD-001:** The system SHALL support native build target compilation.

**Acceptance Criteria:**

- Compiles for host platform and architecture
- Uses host compiler and toolchain
- No cross-compilation configuration needed
- Default behavior when no target specified

**REQ-BUILD-002:** The system SHALL support cross-compile build target selection.

**Acceptance Criteria:**

- Target specified via command-line arguments
- Target specified via configuration files
- Validates target platform compatibility
- Provides clear error messages for invalid targets
- Logs selected build target

**REQ-BUILD-003:** The system SHALL support multiple build targets in single configuration.

**Acceptance Criteria:**

- Allows specifying multiple targets
- Builds each target with appropriate toolchain
- Separates build artifacts by target
- Supports parallel builds for different targets
- Provides clear progress reporting

---

## 7. Error Handling Requirements

### 7.1 Missing Compiler Errors

**REQ-ERROR-001:** The system SHALL provide clear error messages when required compiler is not found.

**Acceptance Criteria:**

- Identifies which compiler is missing
- Provides installation instructions
- Suggests alternative compilers if available
- Links to documentation for setup
- Exits with appropriate error code

### 7.2 Environment Setup Errors

**REQ-ERROR-002:** The system SHALL provide clear error messages when terminal environment setup fails.

**Acceptance Criteria:**

- Identifies which environment setup failed
- Provides specific error details
- Suggests troubleshooting steps
- Links to documentation for resolution
- Exits with appropriate error code

### 7.3 Cross-Compilation Errors

**REQ-ERROR-003:** The system SHALL provide clear error messages when cross-compilation setup fails.

**Acceptance Criteria:**

- Identifies which cross-compilation target failed
- Provides specific error details
- Validates cross-compiler availability
- Suggests alternative approaches
- Exits with appropriate error code

### 7.4 Compiler Validation Errors

**REQ-ERROR-004:** The system SHALL provide clear error messages when compiler validation fails.

**Acceptance Criteria:**

- Identifies which validation check failed
- Provides compiler version information
- Explains C++23 support requirements
- Suggests compiler upgrade or alternative
- Exits with appropriate error code

### 7.5 Graceful Degradation

**REQ-ERROR-005:** The system SHALL support graceful degradation when optional features are unavailable.

**Acceptance Criteria:**

- Logs warnings for missing optional compilers
- Continues with available compilers
- Provides clear information about reduced functionality
- Allows user to configure strict mode
- Exits with error in strict mode

---

## 8. Configuration Requirements

**REQ-CONFIG-001:** The system SHALL support compiler configuration via JSON configuration files.

**Acceptance Criteria:**

- Configuration stored in config/compilers.json
- Supports platform-specific compiler settings
- Supports compiler-specific flags and options
- Validates configuration schema
- Provides clear error messages for invalid configuration

**REQ-CONFIG-002:** The system SHALL support environment variable overrides for compiler configuration.

**Acceptance Criteria:**

- Allows overriding compiler paths via environment variables
- Allows overriding compiler flags via environment variables
- Environment variables take precedence over config files
- Documents supported environment variables
- Validates environment variable values

---

## 9. Logging and Debugging Requirements

**REQ-LOG-001:** The system SHALL provide detailed logging for platform and compiler detection.

**Acceptance Criteria:**

- Logs detected platform and architecture
- Logs detected compilers and versions
- Logs compiler validation results
- Logs selected compiler and reasoning
- Logs environment setup details

**REQ-LOG-002:** The system SHALL provide debug mode for troubleshooting cross-platform issues.

**Acceptance Criteria:**

- Debug mode enables verbose logging
- Logs all environment variables
- Logs all compiler detection attempts
- Logs all toolchain file selections
- Logs all command executions

---

## 10. Non-Functional Requirements

### 10.1 Performance

**REQ-NF-001:** Platform and compiler detection SHALL complete within 5 seconds.

**REQ-NF-002:** Terminal environment setup SHALL complete within 10 seconds.

### 10.2 Reliability

**REQ-NF-003:** The system SHALL handle missing compilers gracefully without crashing.

**REQ-NF-004:** The system SHALL provide consistent behavior across all supported platforms.

### 10.3 Usability

**REQ-NF-005:** Error messages SHALL be clear and actionable.

**REQ-NF-006:** The system SHALL provide helpful suggestions for common issues.

### 10.4 Maintainability

**REQ-NF-007:** Compiler detection logic SHALL be modular and extensible.

**REQ-NF-008:** Terminal setup logic SHALL be separated by platform and compiler.

---

## 11. Future Enhancements (TBD)

**REQ-FUTURE-001:** Support for macOS compiler detection (Clang with Apple SDK).

**REQ-FUTURE-002:** Support for additional cross-compilation targets (Android, iOS).

**REQ-FUTURE-003:** Support for containerized build environments.

**REQ-FUTURE-004:** Support for remote compilation and distributed builds.

**REQ-FUTURE-005:** Support for compiler cache integration (ccache, sccache).

---

## 12. Dependencies

This document depends on:

- Migration Strategy (.specs/migration/strategy.md)
- Terminal Utilities (omni_scripts/utils/terminal_utils.py)
- CMake Configuration (CMakeLists.txt, CMakePresets.json)
- Compiler Configuration (config/compilers.json)

---

## 13. Success Criteria

The cross-platform compilation system is considered successful when:

1. All supported platforms can be detected automatically
2. All supported compilers can be detected and validated
3. Terminal environments can be set up correctly for all compilers
4. Cross-compilation works for supported targets
5. Error messages are clear and actionable
6. System is reliable and performs within specified limits

