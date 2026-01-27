# Hypothesis Document v3 - Testing Issues

**Generated:** 2026-01-19T12:56:00.000Z
**Source:** `.specs/debug/incident_report_v3.md`

---

## BUG-012-CONFIGURE-COMPILER-FLAG

### Evidence Summary
- Error: `unrecognized arguments: --compiler <compiler_name>` for all configure tests
- Exit code: 2 (argument parsing error)
- Affects: msvc, clang-msvc, mingw-gcc, mingw-clang
- Suspect files: [`OmniCppController.py`](OmniCppController.py:1105-1125), [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:113-169)

### Theories

#### Theory A: Missing Argument Definition
The `--compiler` flag is not defined in the configure command's argument parser in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:113-169). The `_add_configure_command()` function may not include the `--compiler` argument in its subparser configuration.

**Evidence Supporting:**
- Error message explicitly states "unrecognized arguments"
- Exit code 2 is standard for argparse errors
- All four compiler variants fail identically

#### Theory B: Argument Parser Registration Issue
The configure subparser is registered but the `--compiler` argument is defined in a parent parser that is not properly inherited by the configure subparser.

**Evidence Supporting:**
- The error occurs at argument parsing stage
- Multiple commands may share common arguments through inheritance
- The build command successfully uses `--compiler` (implied by successful build tests)

#### Theory C: Conditional Argument Definition
The `--compiler` argument is conditionally defined based on platform or environment detection, and the condition fails during configure command initialization.

**Evidence Supporting:**
- Different commands may have different argument requirements
- Platform detection may not have completed before argument parsing
- The configure command may have different initialization logic than build

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message "unrecognized arguments" is the definitive signature of an undefined argument in argparse
2. The incident report explicitly states: "The `--compiler` flag is not defined in the configure command argument parser"
3. The suspect file analysis points directly to [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:113-169) where `_add_configure_command()` is responsible for argument definition
4. All four compiler variants fail with identical error patterns, indicating a systematic omission rather than a conditional or inheritance issue

---

## BUG-013-BUILD-VULKAN-LOADER

### Evidence Summary
- Error: `Package 'vulkan-loader/1.3.296.0' not resolved: Unable to find 'vulkan-loader/1.3.296.0' in remotes`
- Exit code: 1
- Affects: msvc, clang-msvc builds
- Other dependencies resolved successfully (catch2, cpptrace, fmt, glm, gtest, etc.)
- Suspect files: [`conan/conanfile.py`](conan/conanfile.py:111), [`omni_scripts/conan.py`](omni_scripts/conan.py:130-271)

### Theories

#### Theory A: Package Version Mismatch
The specific version `vulkan-loader/1.3.296.0` does not exist in Conan Center or configured remotes. The version may have been recently updated or the package name changed.

**Evidence Supporting:**
- Error explicitly states "Unable to find 'vulkan-loader/1.3.296.0' in remotes"
- `vulkan-headers/1.3.296.0` was successfully resolved, suggesting the version number is correct for headers
- All other dependencies resolved without issue

#### Theory B: Missing Conan Remote Configuration
The Conan remote repository containing `vulkan-loader` is not configured in the user's Conan settings, or the remote is temporarily unavailable.

**Evidence Supporting:**
- Error mentions "in remotes" (plural), suggesting multiple remotes were checked
- Other packages resolved successfully, indicating at least some remotes are accessible
- The package may exist in a specific remote not configured for this environment

#### Theory C: Package Name Typo or Deprecation
The package name `vulkan-loader` is incorrect or has been deprecated/renamed in Conan Center. The correct package name may be different (e.g., `vulkan-headers-loader`, `vulkan-loader-sdk`).

**Evidence Supporting:**
- `vulkan-headers` exists and resolves successfully
- The loader package may have a different naming convention
- Conan packages sometimes undergo renaming or consolidation

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message is specific to the version number: `vulkan-loader/1.3.296.0`
2. The incident report states: "The `vulkan-loader/1.3.296.0` package is not available in Conan remotes"
3. The fact that `vulkan-headers/1.3.296.0` resolved successfully indicates the version number format is correct, but the loader package at that specific version may not exist
4. Vulkan packages are frequently updated, and version 1.3.296.0 may be too new or not yet published to Conan Center

---

## BUG-014-INSTALL-COMPILER-FLAG

### Evidence Summary
- Error: `unrecognized arguments: --compiler <compiler_name>` for all install tests
- Exit code: 2 (argument parsing error)
- Affects: msvc, clang-msvc, mingw-gcc, mingw-clang
- Suspect files: [`OmniCppController.py`](OmniCppController.py:1172-1184), [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:281-323)

### Theories

#### Theory A: Missing Argument Definition
The `--compiler` flag is not defined in the install command's argument parser in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:281-323). The `_add_install_command()` function may not include the `--compiler` argument in its subparser configuration.

**Evidence Supporting:**
- Error message explicitly states "unrecognized arguments"
- Exit code 2 is standard for argparse errors
- All four compiler variants fail identically

#### Theory B: Argument Parser Registration Issue
The install subparser is registered but the `--compiler` argument is defined in a parent parser that is not properly inherited by the install subparser.

**Evidence Supporting:**
- The error occurs at argument parsing stage
- Multiple commands may share common arguments through inheritance
- The build command successfully uses `--compiler` (implied by successful build tests)

#### Theory C: Conditional Argument Definition
The `--compiler` argument is conditionally defined based on platform or environment detection, and the condition fails during install command initialization.

**Evidence Supporting:**
- Different commands may have different argument requirements
- Platform detection may not have completed before argument parsing
- The install command may have different initialization logic than build

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message "unrecognized arguments" is the definitive signature of an undefined argument in argparse
2. The incident report explicitly states: "The `--compiler` flag is not defined in the install command argument parser"
3. The suspect file analysis points directly to [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:281-323) where `_add_install_command()` is responsible for argument definition
4. All four compiler variants fail with identical error patterns, indicating a systematic omission rather than a conditional or inheritance issue

---

## BUG-015-TEST-COMPILER-FLAG

### Evidence Summary
- Error: `unrecognized arguments: --compiler <compiler_name>` for all test tests
- Exit code: 2 (argument parsing error)
- Affects: msvc, clang-msvc, mingw-gcc, mingw-clang
- Suspect files: [`OmniCppController.py`](OmniCppController.py:1187-1199), [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:325-368)

### Theories

#### Theory A: Missing Argument Definition
The `--compiler` flag is not defined in the test command's argument parser in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:325-368). The `_add_test_command()` function may not include the `--compiler` argument in its subparser configuration.

**Evidence Supporting:**
- Error message explicitly states "unrecognized arguments"
- Exit code 2 is standard for argparse errors
- All four compiler variants fail identically

#### Theory B: Argument Parser Registration Issue
The test subparser is registered but the `--compiler` argument is defined in a parent parser that is not properly inherited by the test subparser.

**Evidence Supporting:**
- The error occurs at argument parsing stage
- Multiple commands may share common arguments through inheritance
- The build command successfully uses `--compiler` (implied by successful build tests)

#### Theory C: Conditional Argument Definition
The `--compiler` argument is conditionally defined based on platform or environment detection, and the condition fails during test command initialization.

**Evidence Supporting:**
- Different commands may have different argument requirements
- Platform detection may not have completed before argument parsing
- The test command may have different initialization logic than build

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message "unrecognized arguments" is the definitive signature of an undefined argument in argparse
2. The incident report explicitly states: "The `--compiler` flag is not defined in the test command argument parser"
3. The suspect file analysis points directly to [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:325-368) where `_add_test_command()` is responsible for argument definition
4. All four compiler variants fail with identical error patterns, indicating a systematic omission rather than a conditional or inheritance issue

---

## BUG-016-PACKAGE-COMPILER-FLAG

### Evidence Summary
- Error: `unrecognized arguments: --compiler <compiler_name>` for all package tests
- Exit code: 2 (argument parsing error)
- Affects: msvc, clang-msvc, mingw-gcc, mingw-clang
- Suspect files: [`OmniCppController.py`](OmniCppController.py:1202-1214), [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:370-413)

### Theories

#### Theory A: Missing Argument Definition
The `--compiler` flag is not defined in the package command's argument parser in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:370-413). The `_add_package_command()` function may not include the `--compiler` argument in its subparser configuration.

**Evidence Supporting:**
- Error message explicitly states "unrecognized arguments"
- Exit code 2 is standard for argparse errors
- All four compiler variants fail identically

#### Theory B: Argument Parser Registration Issue
The package subparser is registered but the `--compiler` argument is defined in a parent parser that is not properly inherited by the package subparser.

**Evidence Supporting:**
- The error occurs at argument parsing stage
- Multiple commands may share common arguments through inheritance
- The build command successfully uses `--compiler` (implied by successful build tests)

#### Theory C: Conditional Argument Definition
The `--compiler` argument is conditionally defined based on platform or environment detection, and the condition fails during package command initialization.

**Evidence Supporting:**
- Different commands may have different argument requirements
- Platform detection may not have completed before argument parsing
- The package command may have different initialization logic than build

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message "unrecognized arguments" is the definitive signature of an undefined argument in argparse
2. The incident report explicitly states: "The `--compiler` flag is not defined in the package command argument parser"
3. The suspect file analysis points directly to [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:370-413) where `_add_package_command()` is responsible for argument definition
4. All four compiler variants fail with identical error patterns, indicating a systematic omission rather than a conditional or inheritance issue

---

## BUG-017-FORMAT-TOOLS-NOT-FOUND

### Evidence Summary
- Error: `Format error: black executable not found`
- Exit code: 1
- Affects: format command only
- C++ formatting skipped due to clang-format not found (warning)
- Python formatting failed due to black not found (error)
- Suspect files: [`OmniCppController.py`](OmniCppController.py:827-878), [`omni_scripts/controller/format_controller.py`](omni_scripts/controller/format_controller.py)

### Theories

#### Theory A: Tool Not Installed
The `black` Python code formatter is not installed in the system's Python environment or virtual environment.

**Evidence Supporting:**
- Error message explicitly states "black executable not found"
- The command attempted to process 2442 Python files
- clang-format was also not found (warning), suggesting missing tools

#### Theory B: PATH Configuration Issue
The `black` executable is installed but not in the system PATH or the virtual environment's PATH, preventing the command from locating it.

**Evidence Supporting:**
- The error is "executable not found" rather than "package not installed"
- The `_command_exists()` function in [`OmniCppController.py`](OmniCppController.py:827-878) may be checking PATH incorrectly
- Virtual environment activation may not have propagated PATH changes

#### Theory C: Tool Detection Logic Failure
The `_command_exists()` function in [`OmniCppController.py`](OmniCppController.py:827-878) has a bug that incorrectly reports `black` as not found even when it is installed.

**Evidence Supporting:**
- The function is responsible for detecting executables
- Both black and clang-format are reported as not found, suggesting a common detection issue
- The detection logic may use `shutil.which()` incorrectly or have platform-specific issues

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message is straightforward: "black executable not found"
2. The incident report states: "The black executable is not installed on the system"
3. The log shows "clang-format not found, skipping C++ formatting" as a warning, but black causes an error, suggesting different handling for required vs optional tools
4. The format command is attempting to process 2442 Python files, which would require black to be installed
5. This is a common development environment setup issue where formatting tools are not included in the base requirements

---

## BUG-018-LINT-TOOLS-NOT-FOUND

### Evidence Summary
- Error: `Lint error: pylint executable not found`
- Exit code: 1
- Affects: lint command only
- C++ linting skipped due to clang-tidy not found (warning)
- Python linting failed due to pylint not found (error)
- Suspect files: [`OmniCppController.py`](OmniCppController.py:933-984), [`omni_scripts/controller/lint_controller.py`](omni_scripts/controller/lint_controller.py)

### Theories

#### Theory A: Tool Not Installed
The `pylint` Python linter is not installed in the system's Python environment or virtual environment.

**Evidence Supporting:**
- Error message explicitly states "pylint executable not found"
- The command attempted to process 2442 Python files
- clang-tidy was also not found (warning), suggesting missing tools

#### Theory B: PATH Configuration Issue
The `pylint` executable is installed but not in the system PATH or the virtual environment's PATH, preventing the command from locating it.

**Evidence Supporting:**
- The error is "executable not found" rather than "package not installed"
- The `_command_exists()` function in [`OmniCppController.py`](OmniCppController.py:933-984) may be checking PATH incorrectly
- Virtual environment activation may not have propagated PATH changes

#### Theory C: Tool Detection Logic Failure
The `_command_exists()` function in [`OmniCppController.py`](OmniCppController.py:933-984) has a bug that incorrectly reports `pylint` as not found even when it is installed.

**Evidence Supporting:**
- The function is responsible for detecting executables
- Both pylint and clang-tidy are reported as not found, suggesting a common detection issue
- The detection logic may use `shutil.which()` incorrectly or have platform-specific issues

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message is straightforward: "pylint executable not found"
2. The incident report states: "The pylint executable is not installed on the system"
3. The log shows "clang-tidy not found, skipping C++ linting" as a warning, but pylint causes an error, suggesting different handling for required vs optional tools
4. The lint command is attempting to process 2442 Python files, which would require pylint to be installed
5. This is a common development environment setup issue where linting tools are not included in the base requirements

---

## BUG-019-MINGW-GCC-PROFILE

### Evidence Summary
- Error: `Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release`
- Exit code: 1
- Stack trace: Exception raised in [`omni_scripts/conan.py`](omni_scripts/conan.py:166) and [`omni_scripts/build.py`](omni_scripts/build.py:311)
- Exception type: `ConanProfileError`
- Suspect files: [`omni_scripts/conan.py`](omni_scripts/conan.py:163-170), [`omni_scripts/build.py`](omni_scripts/build.py:297-299), [`conan/profiles/`](conan/profiles/)

### Theories

#### Theory A: Missing Profile File
The `mingw-gcc-release` profile file does not exist in the [`conan/profiles/`](conan/profiles/) directory. The profile may have been omitted during project setup or never created.

**Evidence Supporting:**
- Error explicitly states "Conan profile not found" with full path
- The expected profile path is clearly specified
- Other profiles (msvc, clang-msvc, mingw-clang) exist and work

#### Theory B: Profile Naming Convention Mismatch
The profile file exists but has a different name than expected (e.g., `mingw-gcc-release` vs `mingw-gcc` vs `gcc-mingw-release`). The code may be constructing the profile name incorrectly.

**Evidence Supporting:**
- The error includes the full expected path
- Profile naming conventions can vary between projects
- The code in [`omni_scripts/build.py`](omni_scripts/build.py:297-299) constructs the profile name dynamically

#### Theory C: Profile Path Construction Error
The code in [`omni_scripts/build.py`](omni_scripts/build.py:297-299) constructs the profile path incorrectly, using the wrong directory separator or base path, causing the lookup to fail even if the file exists.

**Evidence Supporting:**
- The error shows a Windows-style path with forward slashes
- Path construction logic in `_get_conan_profile()` may have bugs
- The profile may exist but at a different constructed path

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The error message is explicit: "Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release"
2. The incident report states: "The `mingw-gcc-release` Conan profile file does not exist"
3. The stack trace shows the exception is raised in [`omni_scripts/conan.py`](omni_scripts/conan.py:166) when attempting to access the profile
4. Other profiles (msvc, clang-msvc, mingw-clang) are listed in the dependency graph and presumably work, indicating the profile lookup mechanism is functional
5. The profile directory structure is documented, and `mingw-gcc-release` is notably absent from the expected profile list

---

## BUG-020-MINGW-CLANG-BUILD

### Evidence Summary
- Error: `/usr/bin/bash: line 1: cd: /e/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine: No such file or directory`
- Exit code: 1
- Stack trace: Exception raised in [`omni_scripts/conan.py`](omni_scripts/conan.py:247) and [`omni_scripts/build.py`](omni_scripts/build.py:311)
- Exception type: `ConanInstallError`
- Bash command attempted to change to Unix-style path on Windows
- Suspect files: [`omni_scripts/conan.py`](omni_scripts/conan.py:218-234), [`omni_scripts/build.py`](omni_scripts/build.py:561-643), [`omni_scripts/utils/terminal_utils.py`](omni_scripts/utils/terminal_utils.py:200-255)

### Theories

#### Theory A: Path Conversion Failure
The path conversion from Windows format to MSYS2 format in [`omni_scripts/utils/terminal_utils.py`](omni_scripts/utils/terminal_utils.py:200-255) fails, producing an incorrect Unix-style path that doesn't exist.

**Evidence Supporting:**
- Error shows bash attempting to use Unix-style path `/e/syncfold/...`
- The Windows path `E:/syncfold/...` was converted to `/e/syncfold/...`
- The directory doesn't exist in either format
- The incident report states: "Path conversion between Windows and MSYS2 format fails"

#### Theory B: Directory Not Created
The build directory `build/release/mingw-clang/engine` was never created because the Conan dependency installation failed before directory creation. The path conversion may be correct, but the directory simply doesn't exist.

**Evidence Supporting:**
- Error states "No such file or directory"
- The stack trace shows `ConanInstallError: Failed to install Conan dependencies: validation failed`
- The build process may have failed before creating the directory
- The error occurs during dependency installation, not build

#### Theory C: MSYS2 Environment Not Initialized
The bash environment is not properly initialized with MSYS2 path mappings, causing the Unix-style path to be interpreted literally rather than as a mapped Windows path.

**Evidence Supporting:**
- The error shows `/usr/bin/bash` executing the command
- MSYS2 uses path mapping (e.g., `/e/` maps to `E:/`)
- If MSYS2 is not initialized, `/e/` would be interpreted as a literal Unix path
- The path conversion function may assume MSYS2 is active

### Most Likely Theory: **Theory A**

**Reasoning:**
1. The incident report explicitly states: "Path conversion between Windows and MSYS2 format fails, causing directory not found errors"
2. The error shows a converted path `/e/syncfold/...` that doesn't exist, while the original Windows path `E:/syncfold/...` also doesn't exist
3. The suspect file analysis points to [`omni_scripts/utils/terminal_utils.py`](omni_scripts/utils/terminal_utils.py:200-255) where `_convert_path_to_msys2()` and `_convert_path_to_msys2_manual()` are responsible for path conversion
4. The error occurs during Conan dependency installation, which requires executing commands in the build directory
5. The path conversion is a complex operation involving subprocess calls and ctypes, making it prone to platform-specific bugs

---

## Summary of Most Likely Theories

| Bug ID | Most Likely Theory | Root Cause Category |
|--------|-------------------|---------------------|
| BUG-012 | Theory A: Missing Argument Definition | Missing CLI argument |
| BUG-013 | Theory A: Package Version Mismatch | Missing Conan dependency |
| BUG-014 | Theory A: Missing Argument Definition | Missing CLI argument |
| BUG-015 | Theory A: Missing Argument Definition | Missing CLI argument |
| BUG-016 | Theory A: Missing Argument Definition | Missing CLI argument |
| BUG-017 | Theory A: Tool Not Installed | Missing tool (black) |
| BUG-018 | Theory A: Tool Not Installed | Missing tool (pylint) |
| BUG-019 | Theory A: Missing Profile File | Missing Conan profile |
| BUG-020 | Theory A: Path Conversion Failure | Directory structure issue |

---

## Pattern Analysis

### Common Patterns Across Bugs

1. **CLI Argument Bugs (BUG-012, BUG-014, BUG-015, BUG-016):**
   - All four bugs share the same root cause pattern: missing `--compiler` flag definition
   - All fail with exit code 2 (argparse error)
   - All affect the same four compiler variants
   - Root cause is in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py)

2. **Tool Availability Bugs (BUG-017, BUG-018):**
   - Both involve missing Python development tools
   - Both fail with exit code 1
   - Both have similar error patterns: "executable not found"
   - Both involve the `_command_exists()` function in [`OmniCppController.py`](OmniCppController.py)

3. **MinGW Build Bugs (BUG-019, BUG-020):**
   - Both affect MinGW compiler configurations
   - Both fail with exit code 1
   - Both involve Conan integration issues
   - Both have stack traces originating in [`omni_scripts/conan.py`](omni_scripts/conan.py)

### Dependency Chain

```
Missing CLI Arguments (BUG-012, 014, 015, 016)
    ↓
Prevents configure, install, test, package commands
    ↓
Cannot test build system functionality
    ↓
Build failures (BUG-013, 019, 020) not discovered until manual testing
```

---

## Testing Recommendations

Based on the hypotheses, the following testing approach is recommended:

1. **For CLI Argument Bugs (BUG-012, 014, 015, 016):**
   - Verify argument parser definitions in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py)
   - Test each command with `--help` to confirm argument availability
   - Add unit tests for argument parser configuration

2. **For Tool Availability Bugs (BUG-017, 018):**
   - Verify tool installation in development environment
   - Test `_command_exists()` function with known executables
   - Add pre-flight checks for required tools

3. **For MinGW Build Bugs (BUG-019, 020):**
   - Verify profile file existence in [`conan/profiles/`](conan/profiles/)
   - Test path conversion logic with various Windows paths
   - Add validation for profile existence before Conan operations

4. **For Conan Dependency Bug (BUG-013):**
   - Verify package availability in Conan Center
   - Test with alternative package versions
   - Add fallback logic for missing packages
