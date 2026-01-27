# Phase 1: Preparation - Current State Documentation

**Generated:** 2026-01-07
**Task:** P1-002: Document Current State
**Status:** Completed

---

## Executive Summary

This document provides a comprehensive overview of the OmniCPP Template project's current state as of Phase 1 preparation. The project is a complex C++23 game engine template with extensive Python build automation, supporting multiple compilers (MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang) and cross-platform builds (Windows, Linux, WASM).

**Key Findings:**
- **Three separate Python script directories** requiring consolidation: `scripts/`, `omni_scripts/`, `impl/`
- **Multiple duplicate manager classes** across different script directories
- **Deprecated build targets** still referenced in CMake configuration
- **Extensive cross-platform setup scripts** for different compiler environments
- **Multiple package managers** integrated: Conan, vcpkg, CPM
- **Complex CMake configuration** with 20+ module files and toolchain support

---

## 1. Current Architecture

### 1.1 High-Level Architecture

```
OmniCPP-template/
├── Python Build System (3 directories)
│   ├── scripts/           # Legacy/secondary scripts (~60 files)
│   ├── omni_scripts/      # Primary/modern scripts (~40 files)
│   └── impl/             # Implementation tests (~15 files)
├── C++ Engine & Game
│   ├── include/           # Header files (~80 files)
│   └── src/              # Source files (~30 files)
├── Build System
│   ├── cmake/             # CMake modules (~20 files)
│   ├── conan/             # Conan package manager
│   └── CPM_modules/       # CPM.cmake modules
├── Configuration
│   ├── config/            # Build and logging configs
│   └── .vscode/           # VSCode configuration
├── Documentation
│   ├── docs/              # User documentation
│   ├── doc/               # API documentation
│   └── practices/          # Best practices
└── Testing
    ├── tests/              # Unit and integration tests
    └── impl/tests/         # Implementation tests
```

### 1.2 Python Build System Architecture

**Pattern:** Controller-Manager-Utility

- **Controllers**: Command execution (build, clean, install, test, package, format, lint)
- **Managers**: Resource management (compiler, package manager, target, CMake, Conan)
- **Utilities**: Helper functions (file, path, logging, terminal, platform)

**Current Issues:**
- Duplicate manager classes across directories
- Inconsistent organization between `scripts/` and `omni_scripts/`
- Mixed responsibilities in some modules
- Two separate compiler detection systems

### 1.3 C++ Engine Architecture

**Pattern:** Component-Based Architecture with ECS

- **Engine Core**: IEngine, Engine, Platform, ResourceManager
- **ECS System**: Entity, Component, System
- **Subsystems**: Audio, Input, Physics, Graphics, Network, Scene, Scripting
- **Rendering**: Vulkan renderer with Qt integration
- **Logging**: ConsoleLogger, ILogger

**Current Issues:**
- Mixed interface and implementation files
- Duplicate header files (e.g., AudioManager.hpp vs audio_manager.hpp)
- Inconsistent naming conventions

### 1.4 Build System Architecture

**Pattern:** Modular CMake Configuration

- **Core Modules**: Compiler flags, platform config, testing, coverage
- **User Templates**: Build options, project configuration
- **Toolchains**: Cross-compilation support (ARM64, WASM, Linux)
- **Package Managers**: Conan, vcpkg, CPM integration

**Current Issues:**
- Deprecated target references (qt-vulkan/library, qt-vulkan/standalone)
- Complex module dependencies
- Mixed concerns in some modules

---

## 2. Known Issues

### 2.1 Critical Issues

#### Issue 1: Script Consolidation Required
**Severity:** Critical
**Impact:** High maintenance burden, confusion for developers

**Description:**
Three separate Python script directories with overlapping functionality:
- `scripts/` - Legacy/secondary scripts (~60 files)
- `omni_scripts/` - Primary/modern scripts (~40 files)
- `impl/` - Implementation tests (~15 files)

**Impact:**
- Confusion about which scripts to use
- Duplicate code maintenance burden
- Inconsistent interfaces
- Potential for inconsistencies

**Recommendation:** Consolidate into single `scripts/` directory with clear module structure

---

#### Issue 2: Duplicate Manager Classes
**Severity:** High
**Impact:** Code duplication, maintenance burden

**Description:**
Multiple implementations of same manager classes:
- `CompilerManager` in both `scripts/python/compilers/manager.py` and `scripts/python/compilers/compiler_manager.py`
- Duplicate detector interfaces across multiple files
- Duplicate utility functions (logging, file, path)

**Impact:**
- Code duplication
- Maintenance burden
- Potential for inconsistencies

**Recommendation:** Consolidate into single implementation per manager class

---

#### Issue 3: Deprecated Build Targets
**Severity:** Medium
**Impact:** Confusion for users, potential build failures

**Description:**
Deprecated Qt-Vulkan targets still referenced in CMake configuration:
- `targets/qt-vulkan/library` - Deprecated, use 'engine' instead
- `targets/qt-vulkan/standalone` - Deprecated, use 'game' instead

**Impact:**
- Confusion for users
- Potential build failures
- Outdated documentation

**Recommendation:** Remove all references to deprecated targets

---

### 2.2 High Priority Issues

#### Issue 4: Cross-Platform Complexity
**Severity:** High
**Impact:** Difficult to maintain, high cognitive load

**Description:**
Extensive cross-platform setup scripts with overlapping functionality:
- Multiple Conan setup scripts for different compilers (8 scripts)
- Duplicate terminal detection logic
- Complex environment setup

**Impact:**
- Difficult to maintain
- Potential for inconsistencies
- High cognitive load for developers

**Recommendation:** Simplify and consolidate setup scripts

---

#### Issue 5: Configuration File Proliferation
**Severity:** Medium
**Impact:** Confusion, potential inconsistencies

**Description:**
Multiple configuration files for similar purposes:
- Three logging configuration files (logging_cpp.json, logging_python.json, logging.json)
- Multiple CMake configuration files
- Duplicate utility configurations

**Impact:**
- Confusion about which file to use
- Potential for inconsistencies
- Maintenance burden

**Recommendation:** Consolidate configuration files where possible

---

#### Issue 6: Inconsistent Naming Conventions
**Severity:** Medium
**Impact:** Confusion, difficult to locate files

**Description:**
Inconsistent naming across files and directories:
- Mix of snake_case and camelCase
- Inconsistent use of underscores vs hyphens
- Duplicate file names in different directories

**Impact:**
- Confusion for developers
- Difficult to locate files
- Potential for errors

**Recommendation:** Establish and enforce consistent naming conventions

---

### 2.3 Medium Priority Issues

#### Issue 7: Duplicate Header Files
**Severity:** Medium
**Impact:** Confusion, potential for errors

**Description:**
Duplicate header files with different naming:
- `AudioManager.hpp` vs `audio_manager.hpp`
- `InputManager.hpp` vs `input_manager.hpp`
- `ResourceManager.hpp` vs `resource_manager.hpp`

**Impact:**
- Confusion about which file to include
- Potential for errors
- Maintenance burden

**Recommendation:** Standardize naming and remove duplicates

---

#### Issue 8: Mixed Interface and Implementation Files
**Severity:** Low
**Impact:** Code organization issues

**Description:**
Interface and implementation files mixed in same directories:
- `include/engine/` contains both interfaces and implementations
- No clear separation between public API and internal implementation

**Impact:**
- Code organization issues
- Difficult to understand public API
- Potential for exposing internal implementation

**Recommendation:** Separate interface and implementation files

---

## 3. Existing Dependencies

### 3.1 Python Dependencies

**From requirements.txt:**
```
# Build System
cmake>=4.0.0
conan>=2.0.0
ninja>=1.11.0

# Code Quality
black>=23.0.0
mypy>=1.0.0
pylint>=2.17.0
pytest>=7.4.0
pytest-cov>=4.1.0

# Utilities
click>=8.1.0
colorama>=0.4.6
rich>=13.0.0
toml>=0.10.2
```

**From requirements-docs.txt:**
```
# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocstrings[python]>=0.22.0
doxygen>=1.9.0
```

### 3.2 C++ Dependencies

**From vcpkg.json:**
```json
{
  "dependencies": [
    "vulkan",
    "vulkan-headers",
    "vulkan-loader",
    "vulkan-validationlayers",
    "shaderc",
    "spirv-tools",
    "glslang",
    "spirv-cross",
    "fmt",
    "nlohmann-json",
    "zlib",
    "spdlog",
    "catch2",
    "gtest",
    "libpq"
  ]
}
```

**From conan/conanfile.py:**
```python
requires = [
    "fmt/10.0.0",
    "nlohmann_json/3.11.2",
    "zlib/1.2.13",
    "spdlog/1.12.0",
    "catch2/3.4.0",
    "gtest/1.14.0"
]
```

**From CPM (dependencies.cmake):**
- cpptrace (stack trace library)
- cxxopts (command line parsing)
- json (nlohmann/json)
- OpenSSL (if needed)

### 3.3 Build System Dependencies

**CMake:**
- Minimum version: 4.0.0
- Required modules: FetchContent, ExternalProject, CPack

**Package Managers:**
- Conan 2.0.0+
- vcpkg (latest)
- CPM.cmake 0.40.2

**Build Generators:**
- Ninja (default)
- Visual Studio (MSVC)
- Xcode (macOS)
- Unix Makefiles (fallback)

### 3.4 Optional Dependencies

**Qt6:**
- Used for Qt/Vulkan integration
- Optional: OMNICPP_USE_QT6

**Vulkan SDK:**
- Required for Vulkan rendering
- Optional: OMNICPP_USE_VULKAN

**OpenGL:**
- Alternative to Vulkan
- Optional: OMNICPP_USE_OPENGL

**GLM:**
- Math library
- Optional: OMNICPP_USE_GLM

**STB:**
- Image loading library
- Optional: OMNICPP_USE_STB

---

## 4. Current Build Process

### 4.1 Build Workflow

```
1. Environment Setup
   ├── Detect platform (Windows/Linux/macOS)
   ├── Detect compiler (MSVC/GCC/Clang/MinGW)
   ├── Setup terminal environment (VS Dev Prompt/MSYS2)
   └── Validate dependencies (CMake, Conan, vcpkg)

2. Configuration
   ├── Load CMakePresets.json
   ├── Select build preset (debug/release)
   ├── Select toolchain (if cross-compiling)
   └── Configure CMake

3. Dependency Resolution
   ├── Conan: conan install . --build=missing
   ├── vcpkg: vcpkg install (if enabled)
   └── CPM: Automatic during CMake configure

4. Build
   ├── CMake: cmake --build build --preset <preset>
   ├── Ninja: ninja -C build (if using Ninja)
   └── Parallel: -j<jobs> (auto-detected)

5. Testing
   ├── Unit tests: ctest --preset <preset>
   ├── Integration tests: pytest tests/
   └── Coverage: pytest --cov=omni_scripts

6. Packaging
   ├── CPack: cpack --config build/CPackConfig.cmake
   └── Distribution: packages/_CPack_Packages/
```

### 4.2 Build Commands

**Using OmniCppController.py:**
```bash
# Configure
python OmniCppController.py configure --compiler msvc --preset debug

# Build
python OmniCppController.py build --preset debug

# Test
python OmniCppController.py test --preset debug

# Package
python OmniCppController.py package --preset release
```

**Using CMake directly:**
```bash
# Configure
cmake --preset default

# Build
cmake --build build --preset debug

# Test
ctest --preset debug

# Package
cpack --config build/CPackConfig.cmake
```

**Using scripts:**
```bash
# Configure
python scripts/python/commands/configure.py

# Build
python scripts/build.py

# Test
python scripts/test.py

# Package
python scripts/package.py
```

### 4.3 Build Presets

**Configure Presets:**
- `default` - Default configuration
- `debug` - Debug build with symbols
- `release` - Release build with optimizations

**Build Presets:**
- `debug` - Debug build
- `release` - Release build
- `engine-debug` - Engine library debug build
- `engine-release` - Engine library release build
- `game-debug` - Game executable debug build
- `game-release` - Game executable release build

### 4.4 Build Targets

**CMake Targets:**
- `OmniCppEngine` - Engine library
- `OmniCppGame` - Game executable
- `tests` - Unit tests
- `format` - Code formatting
- `lint` - Code linting
- `package` - Package creation

**Deprecated Targets:**
- `qt-vulkan/library` - Use 'engine' instead
- `qt-vulkan/standalone` - Use 'game' instead

### 4.5 Cross-Platform Build Process

**Windows (MSVC):**
```bash
# Setup VS Dev Prompt
conan/setup_msvc.bat

# Configure and build
cmake --preset default
cmake --build build --preset release
```

**Windows (MinGW-GCC):**
```bash
# Setup MinGW environment
conan/setup_gcc_mingw.bat

# Configure and build
cmake --preset default
cmake --build build --preset release
```

**Windows (MinGW-Clang):**
```bash
# Setup MinGW-Clang environment
conan/setup_clang_mingw.bat

# Configure and build
cmake --preset default
cmake --build build --preset release
```

**Linux (GCC):**
```bash
# Configure and build
cmake --preset default
cmake --build build --preset release
```

**Linux (Clang):**
```bash
# Configure and build
CC=clang CXX=clang++ cmake --preset default
cmake --build build --preset release
```

**WASM (Emscripten):**
```bash
# Setup Emscripten
source emsdk_env.sh

# Configure and build
cmake --preset emscripten
cmake --build build --preset emscripten-release
```

---

## 5. File Statistics

### 5.1 Total Files by Category

| Category | Count | Notes |
|----------|-------|-------|
| Python Scripts | ~140 | scripts/, omni_scripts/, impl/ |
| C++ Source Files | ~30 | src/ |
| C++ Header Files | ~80 | include/ |
| CMake Files | ~40 | cmake/, cmake/user/, cmake/toolchains/ |
| Configuration Files | ~25 | config/, .vscode/, root configs |
| Documentation Files | ~50 | docs/, doc/, practices/, examples/ |
| Test Files | ~40 | tests/, impl/tests/ |
| **Total** | **~405** | |

### 5.2 Directories by Type

| Type | Count | Directories |
|------|-------|------------|
| Python Script Directories | 3 | scripts/, omni_scripts/, impl/ |
| C++ Directories | 2 | src/, include/ |
| CMake Directories | 3 | cmake/, cmake/user/, cmake/toolchains/ |
| Configuration Directories | 2 | config/, .vscode/ |
| Documentation Directories | 4 | docs/, doc/, practices/, examples/ |
| Test Directories | 2 | tests/, impl/tests/ |
| Package Manager Directories | 3 | conan/, CPM_modules/, vcpkg.json |

### 5.3 Duplicate Files Identified

| Type | Count | Examples |
|------|-------|----------|
| Duplicate Manager Classes | 2 | CompilerManager (2 locations) |
| Duplicate Detector Interfaces | 4 | ICompilerDetector, ITerminalDetector |
| Duplicate Utility Functions | 3 | logging, file, path utilities |
| Duplicate Compiler Detection | 2 | scripts/ vs omni_scripts/ systems |
| Duplicate Header Files | 6 | AudioManager, InputManager, etc. |

### 5.4 Deprecated Files Identified

| Type | Count | Examples |
|------|-------|----------|
| Deprecated Build Targets | 2 | qt-vulkan/library, qt-vulkan/standalone |
| Deprecated Directory | 1 | targets/ |
| Deprecated Features | 1 | Asyncify in Emscripten |

---

## 6. Cross-Platform Support

### 6.1 Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| Windows (MSVC) | ✅ Fully Supported | Primary development platform |
| Windows (MinGW-GCC) | ✅ Fully Supported | Alternative Windows compiler |
| Windows (MinGW-Clang) | ✅ Fully Supported | Alternative Windows compiler |
| Linux (GCC) | ✅ Fully Supported | Primary Linux compiler |
| Linux (Clang) | ✅ Fully Supported | Alternative Linux compiler |
| macOS (Clang) | ⚠️ Partially Supported | Needs testing |
| WASM (Emscripten) | ✅ Fully Supported | WebAssembly builds |

### 6.2 Supported Compilers

| Compiler | Version | Status |
|----------|---------|--------|
| MSVC | 19.35+ (VS 2022) | ✅ Primary |
| MSVC-Clang | 16.0+ | ✅ Supported |
| MinGW-GCC | 13.0+ | ✅ Supported |
| MinGW-Clang | 16.0+ | ✅ Supported |
| GCC | 13.0+ | ✅ Primary Linux |
| Clang | 16.0+ | ✅ Primary Linux/macOS |
| Emscripten | 3.1+ | ✅ WASM |

### 6.3 Cross-Compilation Targets

| Target | Toolchain | Status |
|--------|-----------|--------|
| Windows x64 | MSVC/MinGW | ✅ Native |
| Linux x64 | GCC/Clang | ✅ Native |
| Linux ARM64 | arm64-linux-gnu.cmake | ✅ Cross-compile |
| Windows ARM64 | arm64-windows-msvc.cmake | ✅ Cross-compile |
| WASM | emscripten.cmake | ✅ Cross-compile |

---

## 7. Testing Infrastructure

### 7.1 Test Types

**Unit Tests:**
- C++ unit tests (Google Test)
- Python unit tests (pytest)
- Compiler detection tests
- Platform detection tests

**Integration Tests:**
- Build system integration tests
- Controller integration tests
- Cross-platform integration tests
- Logging integration tests

**Performance Tests:**
- Build performance monitoring
- Runtime performance tests

**Fuzz Tests:**
- String utilities fuzzing
- Input validation fuzzing

### 7.2 Test Coverage

**Current Coverage:** Not measured
**Target Coverage:** >80% (per requirements)

### 7.3 Test Execution

**Run all tests:**
```bash
# Python tests
pytest tests/

# C++ tests
ctest --preset debug

# All tests
python tests/run_all_tests.py
```

**Run specific tests:**
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Performance tests
pytest tests/performance/
```

---

## 8. Documentation

### 8.1 User Documentation

**Location:** `docs/`

**Key Documents:**
- `index.md` - Main documentation index
- `getting-started/installation.md` - Installation guide
- `guides/quick_start.md` - Quick start guide
- `user-guide-build-system.md` - Build system guide
- `user-guide-game-engine.md` - Game engine guide
- `troubleshooting.md` - Troubleshooting guide

### 8.2 Developer Documentation

**Location:** `docs/`, `practices/`

**Key Documents:**
- `developer-guide.md` - Developer guide
- `compiler-detection.md` - Compiler detection documentation
- `compiler-detection-tests.md` - Compiler detection tests
- `practices/` - Best practices documentation

### 8.3 API Documentation

**Location:** `doc/`, `docs/api/`

**Tools:**
- Doxygen (C++ API)
- MkDocStrings (Python API)

### 8.4 Migration Documentation

**Location:** `docs/migration-guide.md`

**Status:** Needs update for refactoring

---

## 9. Code Quality Tools

### 9.1 Formatting

**C++:**
- Tool: clang-format
- Config: `.clang-format`
- Command: `python scripts/format.py` or `cmake --build build --target format`

**Python:**
- Tool: black
- Config: pyproject.toml
- Command: `black omni_scripts/ scripts/`

**CMake:**
- Tool: cmake-format
- Config: `.cmake-format`
- Command: `cmake-format -i cmake/`

### 9.2 Linting

**C++:**
- Tool: clang-tidy
- Config: `.clang-tidy`
- Command: `python scripts/lint.py` or `cmake --build build --target lint`

**Python:**
- Tool: pylint, mypy
- Config: pyproject.toml
- Command: `pylint omni_scripts/ scripts/` or `mypy omni_scripts/ scripts/`

### 9.3 Static Analysis

**C++:**
- clang-tidy (linting)
- clangd (language server)

**Python:**
- mypy (type checking)
- pylint (code quality)

---

## 10. CI/CD Infrastructure

### 10.1 GitHub Actions

**Workflows:**
- `.github/workflows/build.yml` - Build and test
- `.github/workflows/test.yml` - Test execution
- `.github/workflows/release.yml` - Release automation
- `.github/dependabot.yml` - Dependency updates

**Status:** Configured but needs testing

### 10.2 Pre-Commit Hooks

**Config:** `.pre-commit-config.yaml`

**Hooks:**
- Python formatting (black)
- Python linting (pylint)
- C++ formatting (clang-format)
- C++ linting (clang-tidy)
- CMake formatting (cmake-format)

**Status:** Configured but needs testing

---

## 11. Security Considerations

### 11.1 Current Security Measures

- Package integrity verification (Conan, vcpkg)
- Secure terminal invocation (planned)
- Secure logging (planned)
- Build system security (planned)

### 11.2 Security Gaps

- No dependency vulnerability scanning
- No secure terminal invocation implementation
- No secure logging implementation
- No build system security hardening

### 11.3 Security Requirements

See [`.specs/04_future_state/reqs/`](.specs/04_future_state/reqs/) for security requirements:
- REQ-043: Secure Terminal Invocation
- REQ-044: Dependency Integrity Verification
- REQ-045: Secure Logging
- REQ-046: Build System Security
- REQ-047: Package Manager Security

---

## 12. Performance Considerations

### 12.1 Build Performance

**Current Build Times:**
- Debug build: ~5-10 minutes
- Release build: ~10-20 minutes
- Full clean build: ~20-30 minutes

**Optimization Opportunities:**
- ccache integration (planned)
- Build caching (planned)
- Parallel builds (already implemented)
- Incremental builds (already implemented)

### 12.2 Runtime Performance

**Current Status:** Not measured
**Target:** Establish performance benchmarks

---

## 13. Recommendations

### 13.1 Immediate Actions (Phase 1)

1. ✅ **Create Backup Branch** - Completed
2. ✅ **Document Current State** - Completed (this document)
3. ⏳ **Set Up Development Environment** - In Progress
4. ⏳ **Install Required Tools** - Pending
5. ⏳ **Configure Pre-Commit Hooks** - Pending
6. ⏳ **Create Development Branch** - Pending
7. ⏳ **Set Up CI/CD Pipeline** - Pending
8. ⏳ **Create Project Tracking Board** - Pending

### 13.2 Short-term Actions (Phase 2-3)

1. **Consolidate Python Scripts**
   - Merge `scripts/`, `omni_scripts/`, and `impl/` into single `scripts/` directory
   - Establish clear module structure
   - Remove duplicate code

2. **Remove Deprecated Targets**
   - Remove all references to `targets/qt-vulkan/`
   - Update CMake configuration files
   - Update documentation

3. **Consolidate Manager Classes**
   - Choose single implementation for each manager class
   - Remove duplicates
   - Update all references

### 13.3 Medium-term Actions (Phase 4-7)

1. **Simplify Compiler Detection**
   - Consolidate into single detection system
   - Remove duplicate interfaces
   - Standardize detection logic

2. **Consolidate Configuration Files**
   - Merge logging configuration files
   - Reduce CMake configuration complexity
   - Standardize configuration format

3. **Standardize Naming Conventions**
   - Establish naming convention guidelines
   - Rename files to match conventions
   - Update all references

### 13.4 Long-term Actions (Phase 8-12)

1. **Simplify Cross-Platform Setup**
   - Consolidate setup scripts
   - Reduce environment complexity
   - Improve documentation

2. **Improve Architecture**
   - Establish clear separation of concerns
   - Reduce coupling between modules
   - Improve testability

3. **Enhance Documentation**
   - Update all documentation to reflect new structure
   - Add architecture diagrams
   - Improve onboarding materials

---

## 14. Conclusion

The OmniCPP Template project is a complex, feature-rich C++23 game engine template with extensive Python build automation. However, the current structure suffers from significant issues:

1. **Three separate Python script directories** requiring consolidation
2. **Multiple duplicate manager classes** and interfaces
3. **Deprecated build targets** still referenced in configuration
4. **Extensive cross-platform setup scripts** with overlapping functionality
5. **Configuration file proliferation** causing confusion

These issues make the codebase difficult to maintain, extend, and understand. A comprehensive refactoring effort is required to consolidate scripts, remove duplicates, simplify configuration, and improve overall architecture.

This document serves as a comprehensive baseline for the refactoring effort, ensuring that all important functionality is preserved during the consolidation process.

---

**Document Version:** 1.0
**Last Updated:** 2026-01-07
**Next Review:** After Phase 1 completion
