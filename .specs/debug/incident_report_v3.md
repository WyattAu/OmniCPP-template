# Incident Report v3 - Testing Issues

**Generated:** 2026-01-19T12:44:00.000Z
**Source:** `.specs/debug/COMPREHENSIVE_TESTING_REPORT_ALL_COMPILERS.md`

---

## BUG-012-CONFIGURE-COMPILER-FLAG

### User's Report
The `--compiler` flag is not supported for the `configure` command. All configure tests (msvc, clang-msvc, mingw-gcc, mingw-clang) failed with exit code 2.

### Error Messages

#### configure_msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc
```

#### configure_clang-msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc
```

#### configure_mingw-gcc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc
```

#### configure_mingw-clang
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang
```

### Stack Traces
None (argument parsing error, no stack trace)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler Versions:** N/A (command failed before compiler detection)
- **Exit Code:** 2 for all configure tests

---

## BUG-013-BUILD-VULKAN-LOADER

### User's Report
Build fails due to missing `vulkan-loader/1.3.296.0` package in Conan. Both MSVC and clang-msvc builds failed with exit code 1.

### Error Messages

#### build_msvc
```
ERROR: Package 'vulkan-loader/1.3.296.0' not resolved: Unable to find 'vulkan-loader/1.3.296.0' in remotes.
[ERROR] 2026-01-19T02:09:02.601653 - Build directory does not exist: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
```

#### build_clang-msvc
```
ERROR: Package 'vulkan-loader/1.3.296.0' not resolved: Unable to find 'vulkan-loader/1.3.296.0' in remotes.
[ERROR] 2026-01-19T02:10:19.213046 - Build directory does not exist: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\clang-msvc\engine
```

### Stack Traces
None (Conan dependency resolution error)

### Environment Details

#### build_msvc
- **OS:** Windows 11
- **Compiler:** MSVC 193 (Visual Studio 2022)
- **C++ Standard:** C++20
- **Build Type:** Release
- **Architecture:** x86_64
- **Generator:** Ninja Multi-Config
- **Exit Code:** 1

#### build_clang-msvc
- **OS:** Windows 11
- **Compiler:** clang 19 (clang-cl.exe)
- **C++ Standard:** C++20
- **Build Type:** Release
- **Architecture:** x86_64
- **Generator:** Ninja Multi-Config
- **Exit Code:** 1

### Additional Context
The Conan dependency graph shows the following requirements were successfully resolved:
- catch2/3.7.1
- cpptrace/0.5.4
- fmt/10.2.1
- glm/1.0.1
- gtest/1.15.0
- libdwarf/0.9.1
- nlohmann_json/3.12.0
- openssl/3.2.6
- spdlog/1.14.1
- stb/cci.20240531
- vulkan-headers/1.3.296.0 (headers found, but loader missing)
- zlib/1.3.1
- zstd/1.5.7

---

## BUG-014-INSTALL-COMPILER-FLAG

### User's Report
The `--compiler` flag is not supported for the `install` command. All install tests (msvc, clang-msvc, mingw-gcc, mingw-clang) failed with exit code 2.

### Error Messages

#### install_msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc
```

#### install_clang-msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc
```

#### install_mingw-gcc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc
```

#### install_mingw-clang
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang
```

### Stack Traces
None (argument parsing error, no stack trace)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler Versions:** N/A (command failed before compiler detection)
- **Exit Code:** 2 for all install tests

---

## BUG-015-TEST-COMPILER-FLAG

### User's Report
The `--compiler` flag is not supported for the `test` command. All test tests (msvc, clang-msvc, mingw-gcc, mingw-clang) failed with exit code 2.

### Error Messages

#### test_msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc
```

#### test_clang-msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc
```

#### test_mingw-gcc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc
```

#### test_mingw-clang
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang
```

### Stack Traces
None (argument parsing error, no stack trace)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler Versions:** N/A (command failed before compiler detection)
- **Exit Code:** 2 for all test tests

---

## BUG-016-PACKAGE-COMPILER-FLAG

### User's Report
The `--compiler` flag is not supported for the `package` command. All package tests (msvc, clang-msvc, mingw-gcc, mingw-clang) failed with exit code 2.

### Error Messages

#### package_msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc
```

#### package_clang-msvc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc
```

#### package_mingw-gcc
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc
```

#### package_mingw-clang
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang
```

### Stack Traces
None (argument parsing error, no stack trace)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler Versions:** N/A (command failed before compiler detection)
- **Exit Code:** 2 for all package tests

---

## BUG-017-FORMAT-TOOLS-NOT-FOUND

### User's Report
Format command fails because black executable is not installed. The format test failed with exit code 1.

### Error Messages
```
2026-01-19 02:08:13 - omni_scripts.logging.logger - [ERROR] - Format error: black executable not found
```

### Stack Traces
None (tool not found error)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++ Standard Support:** C++23
- **Exit Code:** 1

### Additional Context
The format command attempted to process:
- 3898 C++ file(s) - skipped due to clang-format not found
- 2442 Python file(s) - failed due to black executable not found

Log output shows:
```
2026-01-19 02:08:13 - __main__ - [WARNING] - clang-format not found, skipping C++ formatting
2026-01-19 02:08:13 - omni_scripts.logging.logger - [ERROR] - Format error: black executable not found
```

---

## BUG-018-LINT-TOOLS-NOT-FOUND

### User's Report
Lint command fails because pylint executable is not installed. The lint test failed with exit code 1.

### Error Messages
```
2026-01-19 02:08:22 - omni_scripts.logging.logger - [ERROR] - Lint error: pylint executable not found
```

### Stack Traces
None (tool not found error)

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler:** MSVC 19.44 (BuildTools 2022)
- **C++ Standard Support:** C++23
- **Exit Code:** 1

### Additional Context
The lint command attempted to process:
- 3898 C++ file(s) - skipped due to clang-tidy not found
- 2442 Python file(s) - failed due to pylint executable not found

Log output shows:
```
2026-01-19 02:08:22 - __main__ - [WARNING] - clang-tidy not found, skipping C++ linting
2026-01-19 02:08:22 - omni_scripts.logging.logger - [ERROR] - Lint error: pylint executable not found
```

---

## BUG-019-MINGW-GCC-PROFILE

### User's Report
mingw-gcc build fails due to missing Conan profile. The build_mingw-gcc test failed with exit code 1.

### Error Messages
```
[ERROR] 2026-01-19T02:10:22.831466 - Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release
```

### Stack Traces
```
Traceback (most recent call last):
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 311, in install_dependencies
    self.conan_manager.install(
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/conan.py", line 166, in install
    raise ConanProfileError(
omni_scripts.conan.ConanProfileError: Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 545, in run_clean_build_pipeline
    self.install_dependencies(context, terminal_env)
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 330, in install_dependencies
    raise DependencyError(
omni_scripts.build.DependencyError: BuildError: Failed to install dependencies for engine Context: {'dependency': 'engine'}
```

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler:** mingw-gcc (not detected due to profile error)
- **Exit Code:** 1

### Additional Context
The error originates from:
- File: `omni_scripts/build.py`, line 311 in `install_dependencies`
- File: `omni_scripts/conan.py`, line 166 in `install`
- Exception: `omni_scripts.conan.ConanProfileError`

The expected profile path: `E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release`

---

## BUG-020-MINGW-CLANG-BUILD

### User's Report
mingw-clang build fails due to directory structure issues. The build_mingw-clang test failed with exit code 1.

### Error Messages
```
/usr/bin/bash: line 1: cd: /e/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine: No such file or directory

[ERROR] 2026-01-19T02:10:30.754619 - Build directory does not exist: E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine
```

### Stack Traces
```
Traceback (most recent call last):
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 311, in install_dependencies
    self.conan_manager.install(
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/conan.py", line 247, in install
    raise ConanInstallError(
omni_scripts.conan.ConanInstallError: Failed to install Conan dependencies: validation failed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 545, in run_clean_build_pipeline
    self.install_dependencies(context, terminal_env)
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 330, in install_dependencies
    raise DependencyError(
omni_scripts.build.DependencyError: BuildError: Failed to install dependencies for engine Context: {'dependency': 'engine'}
```

### Environment Details
- **OS:** Windows 11
- **Language Version:** Python 3.x
- **Compiler:** mingw-clang (not detected due to directory error)
- **Exit Code:** 1

### Additional Context
The error originates from:
- File: `omni_scripts/build.py`, line 311 in `install_dependencies`
- File: `omni_scripts/conan.py`, line 247 in `install`
- Exception: `omni_scripts.conan.ConanInstallError`

The bash command attempted to change directory to:
`/e/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine`

This directory does not exist, indicating a path conversion issue between Windows and Unix-style paths when using bash on Windows.

---

## Suspect Files Analysis

### BUG-012-CONFIGURE-COMPILER-FLAG

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:1105-1125) | `main()`, `configure()` | `argparse` | **High** |
| [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:113-169) | `_add_configure_command()` | `argparse`, `BaseController` | **High** |
| [`omni_scripts/controller/configure_controller.py`](omni_scripts/controller/configure_controller.py) | `ConfigureController` | `BaseController` | **Medium** |

**Root Cause:** The `--compiler` flag is not defined in the configure command argument parser.

---

### BUG-013-BUILD-VULKAN-LOADER

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`conan/conanfile.py`](conan/conanfile.py:111) | `OmniCppTemplate.requirements()` | `conan` | **High** |
| [`omni_scripts/conan.py`](omni_scripts/conan.py:130-271) | `ConanManager.install()` | `ConanManager`, `TerminalEnvironment` | **High** |
| [`omni_scripts/build.py`](omni_scripts/build.py:271-335) | `BuildManager.install_dependencies()` | `ConanManager`, `CMakeManager` | **High** |

**Root Cause:** The `vulkan-loader/1.3.296.0` package is not available in Conan remotes.

---

### BUG-014-INSTALL-COMPILER-FLAG

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:1172-1184) | `main()`, `install()` | `argparse` | **High** |
| [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:281-323) | `_add_install_command()` | `argparse`, `BaseController` | **High** |
| [`omni_scripts/controller/install_controller.py`](omni_scripts/controller/install_controller.py) | `InstallController` | `BaseController` | **Medium** |

**Root Cause:** The `--compiler` flag is not defined in the install command argument parser.

---

### BUG-015-TEST-COMPILER-FLAG

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:1187-1199) | `main()`, `test()` | `argparse` | **High** |
| [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:325-368) | `_add_test_command()` | `argparse`, `BaseController` | **High** |
| [`omni_scripts/controller/test_controller.py`](omni_scripts/controller/test_controller.py) | `TestController` | `BaseController` | **Medium** |

**Root Cause:** The `--compiler` flag is not defined in the test command argument parser.

---

### BUG-016-PACKAGE-COMPILER-FLAG

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:1202-1214) | `main()`, `package()` | `argparse` | **High** |
| [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py:370-413) | `_add_package_command()` | `argparse`, `BaseController` | **High** |
| [`omni_scripts/controller/package_controller.py`](omni_scripts/controller/package_controller.py) | `PackageController` | `BaseController` | **Medium** |

**Root Cause:** The `--compiler` flag is not defined in the package command argument parser.

---

### BUG-017-FORMAT-TOOLS-NOT-FOUND

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:827-878) | `_format_python_files()`, `_command_exists()` | `subprocess`, `shutil` | **High** |
| [`omni_scripts/controller/format_controller.py`](omni_scripts/controller/format_controller.py) | `FormatController` | `BaseController` | **Medium** |

**Root Cause:** The black executable is not installed on the system.

---

### BUG-018-LINT-TOOLS-NOT-FOUND

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`OmniCppController.py`](OmniCppController.py:933-984) | `_lint_python_files_pylint()`, `_command_exists()` | `subprocess`, `shutil` | **High** |
| [`omni_scripts/controller/lint_controller.py`](omni_scripts/controller/lint_controller.py) | `LintController` | `BaseController` | **Medium** |

**Root Cause:** The pylint executable is not installed on the system.

---

### BUG-019-MINGW-GCC-PROFILE

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`omni_scripts/conan.py`](omni_scripts/conan.py:163-170) | `ConanManager.install()` | `ConanProfileError` | **High** |
| [`omni_scripts/build.py`](omni_scripts/build.py:297-299) | `BuildManager.install_dependencies()`, `_get_conan_profile()` | `ConanManager` | **High** |
| [`conan/profiles/`](conan/profiles/) | Directory | N/A | **High** |

**Root Cause:** The `mingw-gcc-release` Conan profile file does not exist.

---

### BUG-020-MINGW-CLANG-BUILD

| File Path | Functions/Classes | Dependencies | Priority |
|-----------|-----------------|-------------|----------|
| [`omni_scripts/conan.py`](omni_scripts/conan.py:218-234) | `ConanManager.install()` | `TerminalEnvironment` | **High** |
| [`omni_scripts/build.py`](omni_scripts/build.py:561-643) | `BuildManager._get_build_dir()` | `Path` | **High** |
| [`omni_scripts/utils/terminal_utils.py`](omni_scripts/utils/terminal_utils.py:200-255) | `TerminalEnvironment._convert_path_to_msys2()`, `_convert_path_to_msys2_manual()` | `subprocess`, `ctypes` | **High** |

**Root Cause:** Path conversion between Windows and MSYS2 format fails, causing directory not found errors.

---

## Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         OmniCppController.py (Main Entry Point)                │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │ Argument Parsers (configure, install, test, package)              │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         omni_scripts/controller/cli.py                      │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ Command Subparsers (configure, install, test, package) │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         omni_scripts/controller/*.py (Controllers)              │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ configure_controller.py, install_controller.py,      │   │   │
│  │  │ test_controller.py, package_controller.py,            │   │   │
│  │  │ format_controller.py, lint_controller.py            │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         omni_scripts/build.py (BuildManager)                   │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ install_dependencies(), configure_build_system(),      │   │   │
│  │  │ build_project(), install_artifacts(),               │   │   │
│  │  │ _get_build_dir(), _get_conan_profile()            │   │   │
│  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         omni_scripts/conan.py (ConanManager)                   │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ install(), get_profile(), validate_installation()    │   │   │
│  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         omni_scripts/utils/terminal_utils.py                     │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ TerminalEnvironment, execute_with_terminal_setup()  │   │   │
│  │  │ _convert_path_to_msys2(), _get_long_path_name() │   │   │
│  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         conan/conanfile.py (Conan Recipe)                     │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ requirements(), configure(), generate()              │   │   │
│  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         conan/profiles/ (Profile Directory)                      │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ msvc, clang-msvc, mingw-clang, mingw-gcc,     │   │   │
│  │  │ emscripten, gcc-mingw-ucrt, etc.            │   │   │
│  └────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

| Bug ID | Affected Commands | Exit Code | Root Cause Category |
|--------|-------------------|-----------|---------------------|
| BUG-012 | configure (all compilers) | 2 | Missing CLI argument |
| BUG-013 | build (msvc, clang-msvc) | 1 | Missing Conan dependency |
| BUG-014 | install (all compilers) | 2 | Missing CLI argument |
| BUG-015 | test (all compilers) | 2 | Missing CLI argument |
| BUG-016 | package (all compilers) | 2 | Missing CLI argument |
| BUG-017 | format | 1 | Missing tool (black) |
| BUG-018 | lint | 1 | Missing tool (pylint) |
| BUG-019 | build (mingw-gcc) | 1 | Missing Conan profile |
| BUG-020 | build (mingw-clang) | 1 | Directory structure issue |

**Total Bugs:** 9
**Total Test Failures:** 22 (4 configure + 2 build + 4 install + 4 test + 4 package + 1 format + 1 lint + 1 mingw-gcc + 1 mingw-clang)
