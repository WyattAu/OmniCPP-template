# Incident Report V2 - OmniCpp Template

**Report Date:** 2026-01-18T20:20:00Z  
**Report Type:** Incident Report  
**Project:** OmniCpp Template - Production-Grade C++23 Best Practice Template  
**Status:** Complete - Facts Recorded

---

## Executive Summary

This incident report documents 4 new bugs discovered during comprehensive testing of OmniCppController.py. All facts are recorded from the comprehensive testing report at `.specs/debug/COMPREHENSIVE_TESTING_REPORT_V2.md`.

---

## BUG-008-CONFIGURE-ERROR-DETECTION

### Bug Information
- **Bug ID:** BUG-008-CONFIGURE-ERROR-DETECTION
- **Severity:** HIGH
- **Type:** Logic Error
- **Status:** NOT FIXED
- **Affected Commands:** configure

### User's Report
From the comprehensive testing report, the user reported:
- Configure command fails with exit code 1
- CMake configuration appears to complete successfully
- Controller reports "CMake configuration failed" even though CMake completed successfully

### Error Messages
```
[INFO] 2026-01-18T19:42:52.748343 - Configuring CMake for Release build
[INFO] 2026-01-18T19:42:52.761625 - CMake command to execute: cmake -S E:\syncfold\Filen_private\dev\template\OmniCPP-template -B E:\syncfold\Filen_private\dev\template\OmniCPP-template\build -DCMAKE_BUILD_TYPE=Release -DBUILD_LIBRARY=OFF -DBUILD_STANDALONE=ON
[INFO] 2026-01-18T19:42:52.761655 - Using execute_command for non-MSYS2 compiler
[INFO] 2026-01-18T19:42:52.761661 - Executing: cmake -S E:\syncfold\Filen_private\dev\template\OmniCPP-template -B E:\syncfold\Filen_private\dev\template\OmniCPP-template\build -DCMAKE_BUILD_TYPE=Release -DBUILD_LIBRARY=OFF -DBUILD_STANDALONE=ON
[INFO] 2026-01-18T19:47:44.940427 - Command completed: cmake -S E:\syncfold\Filen_private\dev\template\OmniCPP-template -B E:\syncfold\Filen_private\dev\template\OmniCPP-template\build -DCMAKE_BUILD_TYPE=Release -DBUILD_LIBRARY=OFF -DBUILD_STANDALONE=ON
[SUCCESS] 2026-01-18T19:47:44.942858 - CMake configuration completed
2026-01-18 19:47:44 - __main__ - [31m[1mERROR[0m - CMake configuration failed
```

### Stack Traces
No stack traces available.

### Environment Details
- **Operating System:** Windows 11
- **Platform:** Windows x86_64 (64-bit)
- **Shell:** PowerShell 7
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++23 Support:** True
- **CMake Version:** (detected from test output)

### Test Commands
- `python OmniCppController.py configure --preset msvc-debug` - Exit Code: 1
- `python OmniCppController.py configure --preset msvc-release` - Exit Code: 1

### Test Output Files
- `.specs/debug/testing/test_configure_msvc_debug.txt`
- `.specs/debug/testing/test_configure_msvc_release.txt`

### Impact
Configure command always fails even when CMake succeeds, preventing users from proceeding with build.

---

## BUG-009-CONAN-VULKAN-VERSION-CONFLICT

### Bug Information
- **Bug ID:** BUG-009-CONAN-VULKAN-VERSION-CONFLICT
- **Severity:** CRITICAL
- **Type:** Dependency Management Error
- **Status:** NOT FIXED
- **Affected Commands:** build

### User's Report
From the comprehensive testing report, the user reported:
- Build command fails with exit code 1
- Conan dependency version conflict between different versions of vulkan-headers
- The build is attempting to use Conan for Vulkan dependencies instead of the system Vulkan SDK

### Error Messages
```
ERROR: Version conflict: Conflict between vulkan-headers/1.3.290.0 and vulkan-headers/1.3.296.0 in graph.
Conflict originates from vulkan-loader/1.3.290.0
```

### Stack Traces
No stack traces available.

### Environment Details
- **Operating System:** Windows 11
- **Platform:** Windows x86_64 (64-bit)
- **Shell:** PowerShell 7
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++23 Support:** True
- **CMake Version:** (detected from test output)

### Test Commands
- `python OmniCppController.py build all "Clean Build Pipeline" default release --compiler msvc` - Exit Code: 1

### Test Output Files
- `.specs/debug/testing/test_build_msvc.txt`

### Impact
Build command cannot proceed because Conan cannot resolve dependency versions.

### Additional Observations
- **Vulkan SDK Status:** NOT USING SYSTEM SDK - The build is attempting to use Conan for Vulkan dependencies instead of the system Vulkan SDK.
- **Related to Previous Fixes:** This is a NEW bug not documented in the comprehensive debugging report. The previous fix for BUG-004-CONAN-VERSION changed the stb package version but did not address the Vulkan dependency conflict.

---

## BUG-010-FORMAT-TOOLS-NOT-FOUND

### Bug Information
- **Bug ID:** BUG-010-FORMAT-TOOLS-NOT-FOUND
- **Severity:** MEDIUM
- **Type:** Missing Dependencies
- **Status:** NOT FIXED
- **Affected Commands:** format

### User's Report
From the comprehensive testing report, the user reported:
- Format command fails with exit code 1
- clang-format not found, skipping C++ formatting
- black executable not found

### Error Messages
```
2026-01-18 20:02:36 - __main__ - [33m[1mWARNING[0m - clang-format not found, skipping C++ formatting
2026-01-18 20:02:36 - omni_scripts.logging.logger - [31m[1mERROR[0m - Format error: black executable not found
```

### Stack Traces
No stack traces available.

### Environment Details
- **Operating System:** Windows 11
- **Platform:** Windows x86_64 (64-bit)
- **Shell:** PowerShell 7
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++23 Support:** True
- **CMake Version:** (detected from test output)

### Test Commands
- `python OmniCppController.py format` - Exit Code: 1

### Test Output Files
- `.specs/debug/testing/test_format.txt`

### Impact
Format command cannot format C++ or Python code.

### Additional Observations
- Formatting 3898 C++ file(s)...
- Formatting 2441 Python file(s)...

---

## BUG-011-LINT-TOOLS-NOT-FOUND

### Bug Information
- **Bug ID:** BUG-011-LINT-TOOLS-NOT-FOUND
- **Severity:** MEDIUM
- **Type:** Missing Dependencies
- **Status:** NOT FIXED
- **Affected Commands:** lint

### User's Report
From the comprehensive testing report, the user reported:
- Lint command fails with exit code 1
- clang-tidy not found, skipping C++ linting
- pylint executable not found

### Error Messages
```
2026-01-18 20:03:35 - __main__ - [33m[1mWARNING[0m - clang-tidy not found, skipping C++ linting
2026-01-18 20:03:35 - omni_scripts.logging.logger - [31m[1mERROR[0m - Lint error: pylint executable not found
```

### Stack Traces
No stack traces available.

### Environment Details
- **Operating System:** Windows 11
- **Platform:** Windows x86_64 (64-bit)
- **Shell:** PowerShell 7
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++23 Support:** True
- **CMake Version:** (detected from test output)

### Test Commands
- `python OmniCppController.py lint` - Exit Code: 1

### Test Output Files
- `.specs/debug/testing/test_lint.txt`

### Impact
Lint command cannot lint C++ or Python code.

### Additional Observations
- Linting 3898 C++ file(s)...
- Linting 2441 Python file(s)...

---

## Suspect Files Analysis

### BUG-008-CONFIGURE-ERROR-DETECTION

#### Suspect Files

| File Path | Priority | Relevant Functions/Classes | Dependencies |
|-----------|------------|------------------------|--------------|
| `omni_scripts/utils/command_utils.py` | HIGH | `execute_command()` | `subprocess`, `time`, `typing` |
| `omni_scripts/build_system/cmake.py` | HIGH | `CMakeWrapper.configure()` | `execute_command`, `logging`, `pathlib` |
| `omni_scripts/controller/configure_controller.py` | MEDIUM | `ConfigureController.configure_cmake()`, `ConfigureController.validate_configuration()`, `ConfigureController.execute()` | `CMakeWrapper`, `BaseController`, `ConfigurationError` |

#### Analysis
The root cause is in `omni_scripts/utils/command_utils.py` at line 84-86. When `execute_command()` succeeds (returncode == 0), it returns `None` implicitly. The `CMakeWrapper.configure()` method expects a return value of 0 on success, but receives `None` instead. This causes the controller to interpret the result as a failure.

#### Dependency Graph
```
omni_scripts/controller/configure_controller.py
    ├── omni_scripts/build_system/cmake.py
    │   └── omni_scripts/utils/command_utils.py
    └── omni_scripts/controller/base.py
```

---

### BUG-009-CONAN-VULKAN-VERSION-CONFLICT

#### Suspect Files

| File Path | Priority | Relevant Functions/Classes | Dependencies |
|-----------|------------|------------------------|--------------|
| `conan/conanfile.py` | HIGH | `OmniCppTemplate.requirements()` | `conan`, `json`, `os` |
| `cmake/ConanIntegration.cmake` | HIGH | Conan integration functions | CMake built-in modules |
| `omni_scripts/build_system/conan.py` | MEDIUM | `ConanWrapper.install()`, `ConanWrapper.integrate_cmake()` | `execute_command`, `logging`, `pathlib` |
| `CMakeLists.txt` | MEDIUM | Vulkan configuration section | CMake built-in modules |
| `dependencies.cmake` | LOW | CPM dependency management | CMake built-in modules |

#### Analysis
The version conflict originates from `conan/conanfile.py` lines 109-116. The `vulkan-loader/[~1.3]` package requires `vulkan-headers/1.3.290.0`, while other Vulkan packages require `vulkan-headers/1.3.296.0`. The version range `[~1.3]` allows incompatible versions to be selected.

#### Dependency Graph
```
CMakeLists.txt
    ├── cmake/ConanIntegration.cmake
    │   └── conan/conanfile.py
    └── dependencies.cmake
        └── cmake/CPM.cmake

omni_scripts/build_system/conan.py
    ├── omni_scripts/utils/command_utils.py
    └── conan/conanfile.py
```

---

### BUG-010-FORMAT-TOOLS-NOT-FOUND

#### Suspect Files

| File Path | Priority | Relevant Functions/Classes | Dependencies |
|-----------|------------|------------------------|--------------|
| `omni_scripts/controller/format_controller.py` | HIGH | `FormatController.format_cpp_file()`, `FormatController.format_python_file()`, `FormatController.execute()` | `subprocess`, `BaseController`, `ControllerError` |
| `omni_scripts/utils/command_utils.py` | MEDIUM | `execute_command()` | `subprocess`, `time`, `typing` |
| `cmake/FormatTargets.cmake` | LOW | CMake format targets | CMake built-in modules |

#### Analysis
The format controller attempts to execute `clang-format` and `black` executables without checking if they exist first. When the executables are not found, `subprocess.run()` raises `FileNotFoundError`, which is caught and logged as a warning, but the controller still returns a non-zero exit code.

#### Dependency Graph
```
omni_scripts/controller/format_controller.py
    ├── omni_scripts/controller/base.py
    └── omni_scripts/utils/command_utils.py

cmake/FormatTargets.cmake
    └── CMakeLists.txt
```

---

### BUG-011-LINT-TOOLS-NOT-FOUND

#### Suspect Files

| File Path | Priority | Relevant Functions/Classes | Dependencies |
|-----------|------------|------------------------|--------------|
| `omni_scripts/controller/lint_controller.py` | HIGH | `LintController.lint_cpp_file()`, `LintController.lint_python_file()`, `LintController.execute()` | `subprocess`, `BaseController`, `ControllerError` |
| `omni_scripts/utils/command_utils.py` | MEDIUM | `execute_command()` | `subprocess`, `time`, `typing` |
| `cmake/LintTargets.cmake` | LOW | CMake lint targets | CMake built-in modules |

#### Analysis
The lint controller attempts to execute `clang-tidy` and `pylint` executables without checking if they exist first. When the executables are not found, `subprocess.run()` raises `FileNotFoundError`, which is caught and logged as a warning, but the controller still returns a non-zero exit code.

#### Dependency Graph
```
omni_scripts/controller/lint_controller.py
    ├── omni_scripts/controller/base.py
    └── omni_scripts/utils/command_utils.py

cmake/LintTargets.cmake
    └── CMakeLists.txt
```

---

## Comprehensive Dependency Graph

### All Suspect Files by Bug

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         OMNICPP TEMPLATE SUSPECT FILES DEPENDENCY GRAPH              │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ BUG-008: CONFIGURE ERROR DETECTION                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

omni_scripts/controller/configure_controller.py (HIGH)
    ├── omni_scripts/build_system/cmake.py (HIGH)
    │   └── omni_scripts/utils/command_utils.py (HIGH) ← ROOT CAUSE
    └── omni_scripts/controller/base.py (MEDIUM)

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ BUG-009: CONAN VULKAN VERSION CONFLICT                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

CMakeLists.txt (MEDIUM)
    ├── cmake/ConanIntegration.cmake (HIGH)
    │   └── conan/conanfile.py (HIGH) ← ROOT CAUSE
    └── dependencies.cmake (LOW)
        └── cmake/CPM.cmake

omni_scripts/build_system/conan.py (MEDIUM)
    ├── omni_scripts/utils/command_utils.py (MEDIUM)
    └── conan/conanfile.py (HIGH)

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ BUG-010: FORMAT TOOLS NOT FOUND                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

omni_scripts/controller/format_controller.py (HIGH)
    ├── omni_scripts/controller/base.py (MEDIUM)
    └── omni_scripts/utils/command_utils.py (MEDIUM)

cmake/FormatTargets.cmake (LOW)
    └── CMakeLists.txt

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ BUG-011: LINT TOOLS NOT FOUND                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

omni_scripts/controller/lint_controller.py (HIGH)
    ├── omni_scripts/controller/base.py (MEDIUM)
    └── omni_scripts/utils/command_utils.py (MEDIUM)

cmake/LintTargets.cmake (LOW)
    └── CMakeLists.txt

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SHARED DEPENDENCIES ACROSS ALL BUGS                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

omni_scripts/utils/command_utils.py (SHARED - HIGH PRIORITY)
    ├── Used by: configure_controller.py
    ├── Used by: format_controller.py
    ├── Used by: lint_controller.py
    ├── Used by: cmake.py
    └── Used by: conan.py

omni_scripts/controller/base.py (SHARED - MEDIUM PRIORITY)
    ├── Used by: configure_controller.py
    ├── Used by: format_controller.py
    ├── Used by: lint_controller.py
    └── Provides: BaseController class

CMakeLists.txt (SHARED - MEDIUM PRIORITY)
    ├── Includes: cmake/ConanIntegration.cmake
    ├── Includes: dependencies.cmake
    ├── Includes: cmake/FormatTargets.cmake
    └── Includes: cmake/LintTargets.cmake

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PRIORITY SUMMARY BY FILE                                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

HIGH PRIORITY (3 files):
    1. omni_scripts/utils/command_utils.py - Affects ALL 4 bugs
    2. conan/conanfile.py - Affects BUG-009
    3. omni_scripts/build_system/cmake.py - Affects BUG-008

MEDIUM PRIORITY (6 files):
    1. omni_scripts/controller/configure_controller.py - Affects BUG-008
    2. omni_scripts/controller/format_controller.py - Affects BUG-010
    3. omni_scripts/controller/lint_controller.py - Affects BUG-011
    4. omni_scripts/controller/base.py - Affects BUG-008, BUG-010, BUG-011
    5. omni_scripts/build_system/conan.py - Affects BUG-009
    6. CMakeLists.txt - Affects BUG-009, BUG-010, BUG-011

LOW PRIORITY (4 files):
    1. cmake/ConanIntegration.cmake - Affects BUG-009
    2. cmake/FormatTargets.cmake - Affects BUG-010
    3. cmake/LintTargets.cmake - Affects BUG-011
    4. dependencies.cmake - Affects BUG-009

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ BUG INTERSECTION ANALYSIS                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

Files affecting MULTIPLE bugs:
    1. omni_scripts/utils/command_utils.py - Affects ALL 4 bugs (BUG-008, BUG-009, BUG-010, BUG-011)
    2. omni_scripts/controller/base.py - Affects 3 bugs (BUG-008, BUG-010, BUG-011)
    3. CMakeLists.txt - Affects 3 bugs (BUG-009, BUG-010, BUG-011)

Files affecting SINGLE bug:
    1. conan/conanfile.py - Affects only BUG-009
    2. omni_scripts/build_system/cmake.py - Affects only BUG-008
    3. omni_scripts/controller/configure_controller.py - Affects only BUG-008
    4. omni_scripts/controller/format_controller.py - Affects only BUG-010
    5. omni_scripts/controller/lint_controller.py - Affects only BUG-011
    6. cmake/ConanIntegration.cmake - Affects only BUG-009
    7. cmake/FormatTargets.cmake - Affects only BUG-010
    8. cmake/LintTargets.cmake - Affects only BUG-011
    9. dependencies.cmake - Affects only BUG-009
    10. omni_scripts/build_system/conan.py - Affects only BUG-009

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ RECOMMENDED FIX ORDER                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

Phase 1: Fix shared infrastructure (affects all bugs)
    1. omni_scripts/utils/command_utils.py - Fix return value handling
    2. omni_scripts/controller/base.py - Add tool detection utilities

Phase 2: Fix individual bugs
    3. conan/conanfile.py - Fix Vulkan version constraints (BUG-009)
    4. omni_scripts/build_system/cmake.py - Fix return value handling (BUG-008)
    5. omni_scripts/controller/configure_controller.py - Fix error detection (BUG-008)
    6. omni_scripts/controller/format_controller.py - Add tool detection (BUG-010)
    7. omni_scripts/controller/lint_controller.py - Add tool detection (BUG-011)

Phase 3: Update CMake integration
    8. cmake/ConanIntegration.cmake - Update Conan integration (BUG-009)
    9. cmake/FormatTargets.cmake - Update format targets (BUG-010)
    10. cmake/LintTargets.cmake - Update lint targets (BUG-011)
```

---

## Summary Table

| Bug ID | Description | Severity | Status | Affected Commands |
|--------|-------------|----------|--------|-------------------|
| BUG-008-CONFIGURE-ERROR-DETECTION | Configure command error detection logic bug | HIGH | NOT FIXED | configure |
| BUG-009-CONAN-VULKAN-VERSION-CONFLICT | Conan Vulkan dependency version conflict | CRITICAL | NOT FIXED | build |
| BUG-010-FORMAT-TOOLS-NOT-FOUND | Format command missing tools | MEDIUM | NOT FIXED | format |
| BUG-011-LINT-TOOLS-NOT-FOUND | Lint command missing tools | MEDIUM | NOT FIXED | lint |

---

## Test Environment Details

### System Information
- **Operating System:** Windows 11
- **Platform:** Windows x86_64 (64-bit)
- **Shell:** PowerShell 7
- **Python Version:** (detected from test output)
- **CMake Version:** (detected from test output)

### Compiler Information
- **MSVC Version:** 19.44 (BuildTools 2022)
- **MSVC Location:** C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
- **C++23 Support:** True

### Available Compilers (Not Tested)
- **MSVC-clang:** Available but not tested
- **mingw-gcc:** Available but not tested
- **mingw-clang:** Available but not tested

---

## Related Test Output Files

All test outputs referenced in this incident report are located in the [`.specs/debug/testing/`](.specs/debug/testing/) directory:

| File | Description |
|------|-------------|
| test_configure_msvc_debug.txt | Configure MSVC debug preset output |
| test_configure_msvc_release.txt | Configure MSVC release preset output |
| test_build_msvc.txt | Build MSVC output |
| test_format.txt | Format command output |
| test_lint.txt | Lint command output |

---

**End of Incident Report V2**

**Report Generated:** 2026-01-18T20:20:00Z  
**Report Version:** 2.0  
**Total Bugs Documented:** 4
