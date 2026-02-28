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
- **Mixed interface and implementation files** in same directories
- **Inconsistent naming conventions** across files and directories

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
├── Testing
│   ├── tests/              # Unit and integration tests
│   └── impl/tests/         # Implementation tests
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
- **Platform**: Cross-platform support (Windows, Linux, WASM)

**Current Issues:**

- Mixed interface and implementation files
- Duplicate header files with different naming
- Inconsistent naming conventions

### 1.4 Build System Architecture

**Pattern:** Modular CMake Configuration

- **Core Modules**: Compiler flags, platform config, testing, coverage
- **User Templates**: Build options, project configuration
- **Toolchains**: Cross-compilation support (ARM64, WASM, Linux)
- **Package Managers**: Conan, vcpkg, CPM integration
- **Build Generators**: Ninja (default), Visual Studio, Xcode, Unix Makefiles

**Current Issues:**

- Deprecated target references (qt-vulkan/library, qt-vulkan/standalone)
- Complex module dependencies
- Mixed concerns in some modules

### 1.5 Cross-Platform Build Process

**Windows (MSVC):**
- Setup: VS Dev Prompt activation
- Configure: CMake preset selection
- Build: cmake --build build --preset <preset>
- Test: ctest --preset <preset>
- Package: CPack

**Windows (MinGW-GCC):**
- Setup: MSYS2 environment variables
- Configure: CMake with MinGW toolchain
- Build: cmake --build build --preset <preset>
- Test: ctest --preset <preset>

**Windows (MinGW-Clang):**
- Setup: MSYS2 environment variables
- Configure: CMake with Clang toolchain
- Build: cmake --build build --preset <preset>
- Test: ctest --preset <preset>

**Linux:**
- Setup: Nix environment or system packages
- Configure: CMake with appropriate toolchain
- Build: cmake --build build --preset <preset>
- Test: ctest --preset <preset>

**WASM:**
- Setup: Emscripten toolchain
- Configure: CMake with Emscripten toolchain
- Build: cmake --build build --preset <preset>
- Test: ctest --preset <preset>

**Current Issues:**

- Multiple setup scripts for different compilers
- Duplicate terminal detection logic
- Complex environment setup
- High cognitive load for developers

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

**Recommendation:**

Consolidate into single `scripts/` directory with clear module structure

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

**Recommendation:**

Consolidate into single implementation per manager class

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

**Recommendation:**

Remove all references to deprecated targets

---

#### Issue 4: Cross-Platform Complexity

**Severity:** High
**Impact:** Difficult to maintain, high cognitive load

**Description:**

Extensive cross-platform setup scripts with overlapping functionality:

- Multiple Conan setup scripts for different compilers (8 scripts)
- Duplicate terminal detection logic
- Complex environment setup
- Multiple package manager integration points

**Impact:**

- Difficult to maintain
- High cognitive load for developers
- Potential for inconsistencies

**Recommendation:**

Simplify and consolidate setup scripts

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

**Recommendation:**

Consolidate configuration files where possible

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

**Recommendation:**

Establish and enforce consistent naming conventions

---

#### Issue 7: Duplicate Header Files (RESOLVED)

**Severity:** Medium
**Impact:** Confusion, potential for errors

**Description:**

Duplicate header files with different naming were identified and resolved:

- Removed: `audio_manager.hpp` (kept `AudioManager.hpp`)
- Removed: `input_manager.hpp` (kept `InputManager.hpp`)
- Removed: `physics_engine.hpp` (kept `PhysicsEngine.hpp`)
- Removed: `resource_manager.hpp` (kept `ResourceManager.hpp`)
- Removed: `scene_manager.hpp` (kept `SceneManager.hpp`)
- Removed: `script_manager.hpp` (kept `ScriptManager.hpp`)

**Impact:**

- Confusion eliminated
- No potential for errors
- Maintenance burden reduced

**Recommendation:**

Naming standardized to PascalCase (omnicpp namespace)

---

### 2.3 Medium Priority Issues

#### Issue 8: Mixed Interface and Implementation Files

**Severity:** Low
**Impact:** Code organization issues

**Description:**

Interface and implementation files mixed in same directories:

- `include/engine/` contains both interfaces and implementations
- No clear separation between public API and internal implementation
- Potential for exposing internal implementation

**Impact:**

- Code organization issues
- Difficult to understand public API
- Potential for exposing internal implementation

**Recommendation:**

Separate interface and implementation files

---

### 3.1 Python Dependencies

### 3.2 C++ Dependencies

### 3.3 Build System Dependencies

### 3.4 Optional Dependencies

### 3.5 Build Workflow

### 4.1 Build Commands

### 4.2 Build Presets

### 4.3 Build Targets

### 4.4 Cross-Platform Build Process

### 4.5 Build System Dependencies

### 4.6 Build System Dependencies

---

## 2. Known Issues

### 2.1 Critical Issues

#### Issue 1: Script Consolidation Required

**Status:** RESOLVED

---

#### Issue 2: Duplicate Manager Classes

**Status:** RESOLVED

---

#### Issue 3: Deprecated Build Targets

**Status:** RESOLVED

---

#### Issue 4: Cross-Platform Complexity

**Status:** ONGOING

---

#### Issue 5: Configuration File Proliferation

**Status:** ONGOING

---

#### Issue 6: Inconsistent Naming Conventions

**Status:** ONGOING

---

#### Issue 7: Duplicate Header Files

**Status:** RESOLVED

---

### 2.2 High Priority Issues

#### Issue 8: Mixed Interface and Implementation Files

**Status:** RESOLVED

---

## 3. Existing Dependencies

### 3.1 Python Dependencies

### 3.2 C++ Dependencies

### 3.3 Build System Dependencies

### 3.4 Optional Dependencies

### 3.5 Build Workflow

### 4.1 Build Commands

### 4.2 Build Presets

### 4.3 Build Targets

### 4.4 Cross-Platform Build Process

### 4.5 Build System Dependencies

---

## 4. Current Build Process

### 4.1 Build Workflow

### 4.2 Build Commands

### 4.3 Build Presets

### 4.4 Build Targets

### 4.5 Cross-Platform Build Process

---

## 5. Migration Strategy

---

## 6. Implementation Roadmap

---

## 7. Testing Strategy

---

## 8. Documentation Strategy

---

## 9. Future State

---

## 10. Conclusion

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |