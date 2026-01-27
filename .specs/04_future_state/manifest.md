# OmniCPP Template - Future State Manifest

**Generated:** 2026-01-07
**Purpose:** Define the consolidated, modular future structure for the OmniCPP Template
**Scope:** Brownfield C++23 template project refactoring plan

---

## Executive Summary

This document defines the future state of the OmniCPP Template codebase, consolidating three separate Python script directories into a single, modular architecture. The refactoring addresses cross-platform compilation issues, eliminates duplicate code, and establishes a clean separation of concerns with zero pylance errors.

**Key Changes:**

- **Single Python script directory** (`omni_scripts/`) consolidating `scripts/`, `omni_scripts/`, and `impl/`
- **Modular architecture** with clear separation of concerns
- **Cross-platform compilation support** for MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang
- **Proper terminal invocation** patterns for each compiler environment
- **Zero pylance errors** with comprehensive type hints
- **Consolidated logging architecture** for both C++ and Python
- **Unified package manager integration** with priority-based selection

---

## Consolidated Directory Structure

```
OmniCPP-template/
├── .specs/                    # Specifications and documentation
│   ├── 00_current_state/     # Current state analysis
│   ├── 01_standards/         # Coding standards and conventions
│   ├── 02_requirements/      # Feature requirements
│   ├── 03_architecture/      # Architecture specifications
│   └── 04_future_state/      # This document
├── .vscode/                   # VSCode configuration
├── assets/                    # Game assets
├── cmake/                     # CMake modules and toolchains
├── conan/                     # Conan package manager configuration
├── config/                    # Build and logging configuration
├── CPM_modules/               # CPM.cmake module files
├── doc/                       # API documentation
├── docs/                      # User documentation
├── examples/                  # Example projects
├── include/                   # C++ header files
├── logs/                      # Build and runtime logs
├── omni_scripts/             # Consolidated Python build scripts
├── packages/                  # Distribution packages
├── practices/                 # Best practices documentation
├── src/                       # C++ source files
├── tests/                     # Test files
└── validation_reports/        # Validation reports
```

---

## 1. omni_scripts/ Directory Structure

### 1.1 Overview

The `omni_scripts/` directory consolidates all Python scripts from `scripts/`, `omni_scripts/`, and `impl/` into a single, modular architecture. This eliminates duplication, provides clear separation of concerns, and ensures zero pylance errors through comprehensive type hints.

### 1.2 Directory Tree

```
omni_scripts/
├── __init__.py                # Package initialization, exports public API
├── main.py                    # Main entry point for CLI
├── build.py                   # Core build operations manager
├── build_optimizer.py         # Build optimization and performance tracking
├── cmake.py                   # CMake operations manager
├── conan.py                   # Conan dependency management
├── config.py                  # Configuration management
├── error_handler.py           # Centralized error handling
├── exceptions.py              # Custom exception classes
├── job_optimizer.py           # Parallel job count optimization
├── resilience_manager.py      # Build resilience and fallback mechanisms
├── setup_vulkan.py            # Vulkan SDK setup and validation
│
├── build_system/              # Build system integration
│   ├── __init__.py
│   ├── base.py                # Base classes for build system
│   ├── cmake.py               # CMake integration
│   ├── conan.py               # Conan integration
│   ├── vcpkg.py               # vcpkg integration
│   └── optimizer.py           # Build optimization strategies
│
├── compilers/                 # Compiler detection and management
│   ├── __init__.py
│   ├── base.py                # Base compiler class
│   ├── clang.py               # Clang compiler (Linux, macOS, MSVC-clang)
│   ├── detector.py            # Compiler detection logic
│   ├── gcc.py                 # GCC compiler (Linux, MinGW-GCC)
│   ├── msvc.py                # MSVC compiler
│   ├── mingw_clang.py         # MinGW-clang compiler
│   ├── mingw_gcc.py           # MinGW-GCC compiler
│   └── terminal_invoker.py    # Terminal invocation for different compilers
│
├── controller/                # Command controllers
│   ├── __init__.py
│   ├── base.py                # Base controller class
│   ├── build_controller.py    # Build command controller
│   ├── clean_controller.py    # Clean command controller
│   ├── cli.py                 # CLI argument parsing and dispatch
│   ├── config_controller.py   # Config command controller
│   ├── configure_controller.py # Configure command controller
│   ├── dispatcher.py          # Command dispatcher
│   ├── format_controller.py   # Format command controller
│   ├── install_controller.py  # Install command controller
│   ├── lint_controller.py     # Lint command controller
│   ├── package_controller.py  # Package command controller
│   └── test_controller.py     # Test command controller
│
├── logging/                   # Logging system
│   ├── __init__.py
│   ├── config.py              # Logging configuration management
│   ├── formatters.py          # Log formatters (colored, structured)
│   ├── handlers.py            # Log handlers (rotating file, console)
│   └── logger.py              # Main logger implementation
│
├── package_managers/          # Package manager operations
│   ├── __init__.py
│   ├── base.py                # Base package manager class
│   ├── conan.py               # Conan package manager
│   ├── cpm.py                 # CPM.cmake package manager
│   ├── factory.py             # Package manager factory
│   ├── manager.py             # Package manager coordinator
│   └── vcpkg.py               # vcpkg package manager
│
├── platform/                  # Platform detection and configuration
│   ├── __init__.py
│   ├── detector.py            # Platform detection logic
│   ├── linux.py               # Linux-specific configuration
│   ├── macos.py               # macOS-specific configuration
│   └── windows.py             # Windows-specific configuration
│
├── targets/                   # Build target configurations
│   ├── __init__.py
│   ├── base.py                # Base target class
│   ├── engine.py              # Engine target configuration
│   ├── game.py                # Game target configuration
│   ├── factory.py             # Target factory
│   └── manager.py             # Target manager
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── command_utils.py       # Command execution utilities
│   ├── exceptions.py          # Utility-specific exceptions
│   ├── file_utils.py          # File operations
│   ├── logging_utils.py       # Logging utilities
│   ├── path_utils.py          # Path operations
│   ├── platform_utils.py      # Platform-specific utilities
│   ├── system_utils.py        # System operations
│   └── terminal_utils.py     # Terminal environment setup
│
└── validators/                # Validation utilities
    ├── __init__.py
    ├── build_validator.py     # Build configuration validation
    ├── config_validator.py    # Configuration file validation
    └── dependency_validator.py # Dependency validation
```

### 1.3 Module Organization Principles

**Separation of Concerns:**

- **build_system/**: Integration with CMake, Conan, vcpkg, and build optimization
- **compilers/**: Compiler detection, configuration, and terminal invocation
- **controller/**: Command-line interface and command execution
- **logging/**: Logging configuration, formatters, and handlers
- **package_managers/**: Package manager abstraction and coordination
- **platform/**: Platform-specific detection and configuration
- **targets/**: Build target definitions and management
- **utils/**: Reusable utility functions
- **validators/**: Configuration and dependency validation

**Type Safety:**

- All modules use comprehensive type hints
- Strict typing with `from __future__ import annotations`
- No `Any` types unless absolutely necessary
- All functions have return type annotations
- All parameters have type annotations

**Zero Pylance Errors:**

- All imports are properly typed
- No circular dependencies
- Proper `__init__.py` files for package structure
- Clear public API exports in `__init__.py` files

---

## 2. cmake/ Directory Structure

### 2.1 Overview

The `cmake/` directory contains all CMake modules, toolchains, and configuration files. The structure is modular and supports cross-platform compilation.

### 2.2 Directory Tree

```
cmake/
├── CompilerFlags.cmake        # Compiler-specific flags and settings
├── ConanIntegration.cmake     # Conan package manager integration
├── Coverage.cmake             # Code coverage configuration
├── CPM.cmake                  # CPM.cmake package manager integration
├── CPM_0.40.2.cmake           # CPM.cmake version 0.40.2
├── FindDependencies.cmake     # Dependency finding functions
├── FormatTargets.cmake        # Code formatting targets
├── InstallRules.cmake        # Installation rules
├── LintTargets.cmake          # Code linting targets
├── OmniCppEngineConfig.cmake.in # Engine package config template
├── PackageConfig.cmake        # Packaging configuration
├── PlatformConfig.cmake       # Platform-specific configuration
├── ProjectConfig.cmake        # Project configuration
├── Testing.cmake              # Testing configuration
├── VcpkgIntegration.cmake     # vcpkg package manager integration
│
├── toolchains/                # Toolchain files for cross-compilation
│   ├── arm64-linux-gnu.cmake # ARM64 Linux GNU toolchain
│   ├── arm64-windows-msvc.cmake # ARM64 Windows MSVC toolchain
│   ├── emscripten.cmake       # Emscripten toolchain
│   └── x86-linux-gnu.cmake    # x86 Linux GNU toolchain
│
└── user/                      # User-configurable templates
    ├── build_options.cmake    # Build option definitions
    ├── project-common.cmake   # Common project configuration
    ├── project-library.cmake  # Library build configuration
    ├── project-standalone.cmake # Standalone build configuration
    ├── project-tests.cmake    # Tests build configuration
    ├── tmplt-architecture.cmake # Architecture template
    ├── tmplt-assets.cmake     # Assets template
    ├── tmplt-coverage.cmake   # Coverage template
    ├── tmplt-debug.cmake      # Debug template
    ├── tmplt-emscripten.cmake # Emscripten template
    ├── tmplt-hardening.cmake  # Hardening template
    ├── tmplt-ipo.cmake        # IPO template
    ├── tmplt-runtime.cmake    # Runtime template
    └── tmplt-sanitizer.cmake  # Sanitizer template
```

### 2.3 Module Organization

**Core Modules:**

- **CompilerFlags.cmake**: Compiler-specific flags for MSVC, GCC, Clang
- **PlatformConfig.cmake**: Platform-specific configuration (Windows, Linux, macOS)
- **ProjectConfig.cmake**: Project-wide configuration
- **Testing.cmake**: Test configuration and targets
- **Coverage.cmake**: Code coverage configuration

**Package Manager Integration:**

- **ConanIntegration.cmake**: Conan integration
- **VcpkgIntegration.cmake**: vcpkg integration
- **CPM.cmake**: CPM.cmake integration

**Code Quality:**

- **FormatTargets.cmake**: Code formatting targets (clang-format)
- **LintTargets.cmake**: Code linting targets (clang-tidy)

**Toolchains:**

- Cross-compilation support for ARM64, x86, Emscripten

---

## 3. conan/ Directory Structure

### 3.1 Overview

The `conan/` directory contains Conan package manager configuration, profiles, and setup scripts for different compiler environments.

### 3.2 Directory Tree

```
conan/
├── conanfile.py               # Conan package recipe
├── conan_toolchain.cmake      # Conan toolchain configuration
│
├── profiles/                  # Conan profiles for different configurations
│   ├── clang-msvc             # Clang with MSVC compatibility
│   ├── clang-msvc-debug       # Debug configuration
│   ├── clang-msvc-release     # Release configuration
│   ├── emscripten             # Emscripten/WASM
│   ├── gcc-mingw-ucrt         # MinGW-GCC with UCRT
│   ├── mingw-clang-debug      # MinGW-Clang debug
│   ├── mingw-clang-release    # MinGW-Clang release
│   ├── msvc                   # Microsoft Visual C++
│   ├── msvc-debug             # MSVC debug
│   ├── msvc-release           # MSVC release
│   ├── test_profile           # Testing profile
│   └── test_validate          # Validation profile
│
└── setup/                     # Setup scripts for different compilers
    ├── setup_clang_mingw_ucrt.bat # Clang with MinGW UCRT setup
    ├── setup_clang_mingw.bat       # Clang with MinGW setup
    ├── setup_clang.bat             # Clang setup
    ├── setup_emscripten.bat       # Emscripten setup (Windows)
    ├── setup_emscripten.sh        # Emscripten setup (Unix)
    ├── setup_gcc_mingw_ucrt.bat   # GCC with MinGW UCRT setup
    ├── setup_gcc_mingw.bat        # GCC with MinGW setup
    └── setup_msvc.bat             # MSVC setup
```

### 3.3 Profile Organization

**Compiler-Specific Profiles:**

- **msvc/**: MSVC compiler profiles (debug, release)
- **clang-msvc/**: Clang with MSVC compatibility profiles
- **mingw-clang/**: MinGW-clang profiles (debug, release)
- **gcc-mingw-ucrt/**: MinGW-GCC with UCRT profile
- **emscripten/**: Emscripten/WASM profile

**Testing Profiles:**

- **test_profile**: General testing profile
- **test_validate**: Validation profile

---

## 4. config/ Directory Structure

### 4.1 Overview

The `config/` directory contains all configuration files for build, logging, and project settings.

### 4.2 Directory Tree

```
config/
├── build.json                 # Build configuration
├── compilers.json             # Compiler settings
├── logging_cpp.json           # C++ logging configuration
├── logging_python.json        # Python logging configuration
├── logging.json               # General logging configuration
├── project.json               # Project metadata
└── targets.json               # Build target definitions
```

### 4.3 Configuration File Organization

**Build Configuration:**

- **build.json**: Build options, compiler selection, target configuration

**Compiler Configuration:**

- **compilers.json**: Compiler paths, flags, and settings

**Logging Configuration:**

- **logging_cpp.json**: C++ logging (spdlog) configuration
- **logging_python.json**: Python logging configuration
- **logging.json**: General logging settings

**Project Configuration:**

- **project.json**: Project metadata, version, dependencies

**Target Configuration:**

- **targets.json**: Build target definitions (engine, game, tests)

---

## 5. include/ Directory Structure

### 5.1 Overview

The `include/` directory contains all C++ header files organized by module and subsystem.

### 5.2 Directory Tree

```
include/
├── math.hpp                   # Math utilities
├── string_utils.hpp           # String utilities
│
├── engine/                    # Engine headers
│   ├── ConsoleLogger.hpp
│   ├── Engine.hpp
│   ├── IAudioManager.hpp
│   ├── IEngine.hpp
│   ├── IInputManager.hpp
│   ├── ILogger.hpp
│   ├── IPhysicsEngine.hpp
│   ├── IPlatform.hpp
│   ├── IRenderer.hpp
│   ├── IResourceManager.hpp
│   ├── version.h
│   ├── audio/
│   │   ├── audio_manager.hpp
│   │   └── AudioManager.hpp
│   ├── core/
│   │   └── engine.hpp
│   ├── ecs/
│   │   ├── Camera/
│   │   │   └── CameraComponent.hpp
│   │   ├── Component.hpp
│   │   ├── Entity.hpp
│   │   ├── MeshComponent.hpp
│   │   ├── System.hpp
│   │   └── TransformComponent.hpp
│   ├── events/
│   │   └── event_manager.hpp
│   ├── graphics/
│   │   └── renderer.hpp
│   ├── input/
│   │   ├── input_manager.hpp
│   │   └── InputManager.hpp
│   ├── logging/
│   │   └── logger.hpp
│   ├── math/
│   │   ├── Mat4.hpp
│   │   └── Vec3.hpp
│   ├── memory/
│   │   └── memory_manager.hpp
│   ├── network/
│   │   └── network_manager.hpp
│   ├── physics/
│   │   ├── physics_engine.hpp
│   │   └── PhysicsEngine.hpp
│   ├── platform/
│   │   └── platform.hpp
│   ├── render/
│   │   ├── RenderPipeline.hpp
│   │   ├── ShaderManager.hpp
│   │   └── VulkanRenderer.hpp
│   ├── resources/
│   │   ├── resource_manager.hpp
│   │   └── ResourceManager.hpp
│   ├── scene/
│   │   ├── Scene.hpp
│   │   ├── SceneManager.hpp
│   │   ├── scene_manager.hpp
│   │   └── SceneNode.hpp
│   ├── scripting/
│   │   ├── script_manager.hpp
│   │   └── ScriptManager.hpp
│   ├── utils/
│   │   └── string_utils.hpp
│   └── window/
│       └── window_manager.hpp
│
├── game/                      # Game headers
│   ├── DemoGame.hpp
│   ├── Game.hpp
│   ├── PongGame.hpp
│   ├── audio/
│   │   └── game_audio.hpp
│   ├── core/
│   │   └── game.hpp
│   ├── graphics/
│   │   └── game_renderer.hpp
│   ├── input/
│   │   └── game_input.hpp
│   ├── network/
│   │   └── game_network.hpp
│   ├── physics/
│   │   └── game_physics.hpp
│   ├── platform/
│   │   └── game_platform.hpp
│   ├── scene/
│   │   └── game_scene.hpp
│   ├── scripting/
│   │   └── game_script.hpp
│   └── utils/
│       └── game_utils.hpp
│
└── OmniCppLib/                # Library headers
    ├── OmniCppLib.hpp
    └── version.h
```

### 5.3 Header Organization

**Engine Headers:**

- **core/**: Core engine functionality
- **ecs/**: Entity-Component-System
- **audio/**: Audio management
- **input/**: Input handling
- **physics/**: Physics engine
- **graphics/**: Graphics rendering
- **render/**: Rendering pipeline
- **resources/**: Resource management
- **scene/**: Scene management
- **scripting/**: Scripting system
- **platform/**: Platform abstraction
- **window/**: Window management
- **network/**: Networking
- **memory/**: Memory management
- **events/**: Event system
- **logging/**: Logging system
- **math/**: Math utilities
- **utils/**: Utility functions

**Game Headers:**

- **core/**: Core game functionality
- **audio/**: Game audio
- **input/**: Game input
- **physics/**: Game physics
- **graphics/**: Game graphics
- **scene/**: Game scenes
- **scripting/**: Game scripting
- **platform/**: Game platform
- **network/**: Game networking
- **utils/**: Game utilities

---

## 6. src/ Directory Structure

### 6.1 Overview

The `src/` directory contains all C++ source files organized by module and subsystem.

### 6.2 Directory Tree

```
src/
├── main.cpp                   # Main entry point
│
├── engine/                    # Engine source files
│   ├── audio/
│   │   └── audio_manager.cpp
│   ├── core/
│   │   └── engine.cpp
│   ├── ecs/
│   │   ├── Camera/
│   │   │   └── CameraComponent.cpp
│   │   ├── Component.cpp
│   │   ├── Entity.cpp
│   │   ├── MeshComponent.cpp
│   │   ├── System.cpp
│   │   └── TransformComponent.cpp
│   ├── events/
│   │   └── event_manager.cpp
│   ├── graphics/
│   │   └── renderer.cpp
│   ├── input/
│   │   ├── input_manager.cpp
│   │   └── InputManager.cpp
│   ├── logging/
│   │   └── logger.cpp
│   ├── math/
│   │   ├── Mat4.cpp
│   │   └── Vec3.cpp
│   ├── memory/
│   │   └── memory_manager.cpp
│   ├── network/
│   │   └── network_manager.cpp
│   ├── physics/
│   │   ├── physics_engine.cpp
│   │   └── PhysicsEngine.cpp
│   ├── platform/
│   │   └── platform.cpp
│   ├── render/
│   │   ├── RenderPipeline.cpp
│   │   ├── ShaderManager.cpp
│   │   └── VulkanRenderer.cpp
│   ├── resources/
│   │   ├── resource_manager.cpp
│   │   └── ResourceManager.cpp
│   ├── scene/
│   │   ├── Scene.cpp
│   │   ├── SceneManager.cpp
│   │   ├── scene_manager.cpp
│   │   └── SceneNode.cpp
│   ├── scripting/
│   │   ├── script_manager.cpp
│   │   └── ScriptManager.cpp
│   ├── utils/
│   │   └── string_utils.cpp
│   └── window/
│       └── window_manager.cpp
│
└── game/                      # Game source files
    ├── CMakeLists.txt
    ├── DemoGame.cpp
    ├── DemoMain.cpp
    ├── Game.cpp
    ├── Pong3D.cpp
    ├── PongGame.cpp
    ├── PongMain.cpp
    ├── PongMinimal.cpp
    ├── PongStandalone.cpp
    ├── PongTest1.cpp
    ├── PongTest2.cpp
    ├── PongTest3.cpp
    ├── PongWorking.cpp
    ├── SimpleTest.cpp
    ├── audio/
    │   └── game_audio.cpp
    ├── core/
    │   └── game.cpp
    ├── graphics/
    │   └── game_renderer.cpp
    ├── input/
    │   └── game_input.cpp
    ├── network/
    │   └── game_network.cpp
    ├── physics/
    │   └── game_physics.cpp
    ├── platform/
    │   └── game_platform.cpp
    ├── Qt/
    │   ├── PongControlPanel.cpp
    │   ├── PongControlPanel.hpp
    │   ├── PongMainWindow.cpp
    │   ├── PongMainWindow.hpp
    │   ├── PongRenderWidget.cpp
    │   └── PongRenderWidget.hpp
    ├── scene/
    │   └── game_scene.cpp
    ├── scripting/
    │   └── game_script.cpp
    └── utils/
        └── game_utils.cpp
```

### 6.3 Source Organization

**Engine Sources:**

- Mirror the header structure in `include/engine/`
- Implementation files for all engine components

**Game Sources:**

- Mirror the header structure in `include/game/`
- Implementation files for all game components
- Qt integration files in `Qt/` subdirectory

---

## 7. tests/ Directory Structure

### 7.1 Overview

The `tests/` directory contains all test files organized by type and module.

### 7.2 Directory Tree

```
tests/
├── CMakeLists.txt
├── __init__.py
├── run_all_tests.py
├── test_report.json
│
├── cpp/                       # C++ test files
│   ├── test_engine.cpp
│   ├── test_game.cpp
│   ├── test_main.cpp
│   ├── test_math.cpp
│   ├── test_string_utils.cpp
│   ├── test_system.cpp
│   ├── fuzz_string_utils.cpp
│   ├── fuzz/
│   │   └── test_fuzz.cpp
│   ├── integration/
│   │   └── test_integration.cpp
│   └── performance/
│       └── test_performance.cpp
│
├── python/                    # Python test files
│   ├── test_build_system.py
│   ├── test_integration_build.py
│   ├── build_consistency.py
│   ├── cross_platform_validation.py
│   ├── performance_monitoring.py
│   ├── platform_checks.py
│   ├── test_build_system_integration.py
│   ├── test_controller_integration.py
│   ├── test_cross_platform_integration.py
│   ├── test_full_integration.py
│   ├── test_logging_integration.py
│   ├── test_platform_compiler_detection.py
│   ├── test_suite.py
│   ├── test_terminal_setup.py
│   └── toolchain_validation.py
│
└── unit/                      # Unit tests
    └── compilers/
        ├── test_android_cross_compiler.py
        ├── test_capability_detector.py
        ├── test_chocolatey_detector.py
        ├── test_cmake_generator_selector.py
        ├── test_compiler_detection_cache.py
        ├── test_compiler_detection_system.py
        ├── test_compiler_factory.py
        ├── test_compiler_manager.py
        ├── test_compiler_terminal_mapper.py
        ├── test_error_handler.py
        ├── test_fallback_mechanism.py
        ├── test_linux_cross_compiler.py
        ├── test_logging_integration.py
        ├── test_mingw_clang_detector.py
        ├── test_mingw_gcc_detector.py
        ├── test_mingw_terminal_detector.py
        ├── test_msvc_clang_detector.py
        ├── test_msvc_detector.py
        ├── test_msvc_terminal_detector.py
        ├── test_parallel_detector.py
        ├── test_scoop_detector.py
        ├── test_toolchain_detector.py
        ├── test_version_detector.py
        └── test_winget_detector.py
```

### 7.3 Test Organization

**C++ Tests:**

- **cpp/**: All C++ test files
- **cpp/fuzz/**: Fuzzing tests
- **cpp/integration/**: Integration tests
- **cpp/performance/**: Performance tests

**Python Tests:**

- **python/**: All Python test files
- Integration tests for build system, controller, cross-platform, logging
- Platform and compiler detection tests
- Terminal setup validation
- Toolchain validation
- Performance monitoring

**Unit Tests:**

- **unit/compilers/**: Compiler-specific unit tests

---

## 8. Cross-Platform Compilation Structure

### 8.1 Overview

The cross-platform compilation structure defines how different compilers are detected, configured, and invoked on different platforms.

### 8.2 Supported Compilers

**Windows:**

- **MSVC**: Microsoft Visual C++ (cl.exe)
- **MSVC-clang**: Clang with MSVC compatibility (clang-cl.exe)
- **MinGW-GCC**: GCC with MinGW-w64 (gcc.exe)
- **MinGW-clang**: Clang with MinGW-w64 (clang.exe)

**Linux:**

- **GCC**: GNU Compiler Collection (gcc)
- **Clang**: LLVM Clang (clang)

**macOS:**

- **Clang**: Apple Clang (clang)

**WASM:**

- **Emscripten**: emcc

### 8.3 Terminal Invocation Patterns

#### 8.3.1 MSVC (Developer Command Prompt)

**Detection:**

```python
# omni_scripts/compilers/msvc.py
def detect_msvc() -> Optional[MSVCCompiler]:
    """Detect MSVC compiler installation."""
    # Check for VsDevCmd.bat in standard locations
    # Community: C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\VsDevCmd.bat
    # Professional: C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\VsDevCmd.bat
    # Enterprise: C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\VsDevCmd.bat
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_msvc_terminal() -> subprocess.Popen:
    """
    Invoke MSVC Developer Command Prompt.

    Returns:
        subprocess.Popen: Process with MSVC environment
    """
    # Find VsDevCmd.bat
    vsdevcmd_path = find_vsdevcmd()

    # Invoke with proper architecture
    cmd = [
        'cmd.exe',
        '/c',
        f'"{vsdevcmd_path}"',
        '-arch=x64',
        '-host_arch=x64',
        '&&',
        'cmd.exe'
    ]

    return subprocess.Popen(cmd, shell=True)
```

**Environment Variables:**

```python
MSVC_ENV = {
    'CC': 'cl.exe',
    'CXX': 'cl.exe',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'cl.exe',
    'CMAKE_CXX_COMPILER': 'cl.exe',
}
```

#### 8.3.2 MSVC-clang (Developer Command Prompt)

**Detection:**

```python
# omni_scripts/compilers/clang.py
def detect_msvc_clang() -> Optional[ClangCompiler]:
    """Detect Clang with MSVC compatibility."""
    # Check for clang-cl.exe in VS 2022 installation
    # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\x64\bin\clang-cl.exe
    # Or check PATH for clang-cl.exe
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_msvc_clang_terminal() -> subprocess.Popen:
    """
    Invoke MSVC Developer Command Prompt with Clang.

    Returns:
        subprocess.Popen: Process with MSVC-clang environment
    """
    # Find VsDevCmd.bat
    vsdevcmd_path = find_vsdevcmd()

    # Invoke with Clang environment
    cmd = [
        'cmd.exe',
        '/c',
        f'"{vsdevcmd_path}"',
        '-arch=x64',
        '-host_arch=x64',
        '&&',
        'set',
        'CC=clang-cl.exe',
        '&&',
        'set',
        'CXX=clang-cl.exe',
        '&&',
        'cmd.exe'
    ]

    return subprocess.Popen(cmd, shell=True)
```

**Environment Variables:**

```python
MSVC_CLANG_ENV = {
    'CC': 'clang-cl.exe',
    'CXX': 'clang-cl.exe',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'clang-cl.exe',
    'CMAKE_CXX_COMPILER': 'clang-cl.exe',
}
```

#### 8.3.3 MinGW-GCC (MSYS2)

**Detection:**

```python
# omni_scripts/compilers/mingw_gcc.py
def detect_mingw_gcc() -> Optional[MinGWGCCCompiler]:
    """Detect MinGW-GCC compiler installation."""
    # Check for MSYS2 UCRT64: C:\msys64\ucrt64\bin\gcc.exe
    # Check for MSYS2 mingw64: C:\msys64\mingw64\bin\gcc.exe
    # Check PATH for gcc.exe
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_mingw_gcc_terminal() -> subprocess.Popen:
    """
    Invoke MSYS2 UCRT64 terminal with MinGW-GCC.

    Returns:
        subprocess.Popen: Process with MinGW-GCC environment
    """
    # Find MSYS2 installation
    msys2_path = find_msys2()

    # Invoke UCRT64 terminal
    cmd = [
        f'{msys2_path}\\msys2_shell.cmd',
        '-ucrt64',
        '-defterm',
        '-no-start',
        '-here'
    ]

    return subprocess.Popen(cmd, shell=True)
```

**Environment Variables:**

```python
MINGW_GCC_ENV = {
    'CC': 'gcc.exe',
    'CXX': 'g++.exe',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'gcc.exe',
    'CMAKE_CXX_COMPILER': 'g++.exe',
    'MSYSTEM': 'UCRT64',
}
```

#### 8.3.4 MinGW-clang (MSYS2)

**Detection:**

```python
# omni_scripts/compilers/mingw_clang.py
def detect_mingw_clang() -> Optional[MinGWClangCompiler]:
    """Detect MinGW-clang compiler installation."""
    # Check for MSYS2 UCRT64: C:\msys64\ucrt64\bin\clang.exe
    # Check for MSYS2 mingw64: C:\msys64\mingw64\bin\clang.exe
    # Check PATH for clang.exe
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_mingw_clang_terminal() -> subprocess.Popen:
    """
    Invoke MSYS2 UCRT64 terminal with MinGW-clang.

    Returns:
        subprocess.Popen: Process with MinGW-clang environment
    """
    # Find MSYS2 installation
    msys2_path = find_msys2()

    # Invoke UCRT64 terminal
    cmd = [
        f'{msys2_path}\\msys2_shell.cmd',
        '-ucrt64',
        '-defterm',
        '-no-start',
        '-here'
    ]

    return subprocess.Popen(cmd, shell=True)
```

**Environment Variables:**

```python
MINGW_CLANG_ENV = {
    'CC': 'clang.exe',
    'CXX': 'clang++.exe',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'clang.exe',
    'CMAKE_CXX_COMPILER': 'clang++.exe',
    'MSYSTEM': 'UCRT64',
}
```

#### 8.3.5 GCC (Linux)

**Detection:**

```python
# omni_scripts/compilers/gcc.py
def detect_gcc() -> Optional[GCCCompiler]:
    """Detect GCC compiler installation."""
    # Check for gcc in /usr/bin/gcc
    # Check PATH for gcc
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_gcc_terminal() -> subprocess.Popen:
    """
    Invoke Linux terminal with GCC.

    Returns:
        subprocess.Popen: Process with GCC environment
    """
    # Use default shell
    cmd = ['/bin/bash']

    return subprocess.Popen(cmd)
```

**Environment Variables:**

```python
GCC_ENV = {
    'CC': 'gcc',
    'CXX': 'g++',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'gcc',
    'CMAKE_CXX_COMPILER': 'g++',
}
```

#### 8.3.6 Clang (Linux/macOS)

**Detection:**

```python
# omni_scripts/compilers/clang.py
def detect_clang() -> Optional[ClangCompiler]:
    """Detect Clang compiler installation."""
    # Check for clang in /usr/bin/clang
    # Check PATH for clang
```

**Terminal Invocation:**

```python
# omni_scripts/compilers/terminal_invoker.py
def invoke_clang_terminal() -> subprocess.Popen:
    """
    Invoke Linux/macOS terminal with Clang.

    Returns:
        subprocess.Popen: Process with Clang environment
    """
    # Use default shell
    cmd = ['/bin/bash']

    return subprocess.Popen(cmd)
```

**Environment Variables:**

```python
CLANG_ENV = {
    'CC': 'clang',
    'CXX': 'clang++',
    'CMAKE_GENERATOR': 'Ninja',
    'CMAKE_C_COMPILER': 'clang',
    'CMAKE_CXX_COMPILER': 'clang++',
}
```

### 8.4 Platform Detection Logic

```python
# omni_scripts/platform/detector.py
from enum import Enum
from typing import Optional

class Platform(Enum):
    """Supported platforms."""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"

class Architecture(Enum):
    """Supported architectures."""
    X86_64 = "x86_64"
    ARM64 = "arm64"

def detect_platform() -> Platform:
    """Detect the current platform."""
    import platform
    system = platform.system().lower()
    if system == "windows":
        return Platform.WINDOWS
    elif system == "linux":
        return Platform.LINUX
    elif system == "darwin":
        return Platform.MACOS
    else:
        raise ValueError(f"Unsupported platform: {system}")

def detect_architecture() -> Architecture:
    """Detect the current architecture."""
    import platform
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return Architecture.X86_64
    elif machine in ("arm64", "aarch64"):
        return Architecture.ARM64
    else:
        raise ValueError(f"Unsupported architecture: {machine}")
```

### 8.5 Compiler Detection and Selection

```python
# omni_scripts/compilers/detector.py
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class CompilerInfo:
    """Compiler information."""
    name: str
    version: str
    path: str
    platform: Platform
    architecture: Architecture

class CompilerDetector:
    """Compiler detection and selection."""

    def __init__(self) -> None:
        self.platform = detect_platform()
        self.architecture = detect_architecture()

    def detect_all(self) -> List[CompilerInfo]:
        """Detect all available compilers."""
        compilers = []

        if self.platform == Platform.WINDOWS:
            # Detect MSVC
            msvc = self._detect_msvc()
            if msvc:
                compilers.append(msvc)

            # Detect MSVC-clang
            msvc_clang = self._detect_msvc_clang()
            if msvc_clang:
                compilers.append(msvc_clang)

            # Detect MinGW-GCC
            mingw_gcc = self._detect_mingw_gcc()
            if mingw_gcc:
                compilers.append(mingw_gcc)

            # Detect MinGW-clang
            mingw_clang = self._detect_mingw_clang()
            if mingw_clang:
                compilers.append(mingw_clang)

        elif self.platform == Platform.LINUX:
            # Detect GCC
            gcc = self._detect_gcc()
            if gcc:
                compilers.append(gcc)

            # Detect Clang
            clang = self._detect_clang()
            if clang:
                compilers.append(clang)

        elif self.platform == Platform.MACOS:
            # Detect Clang
            clang = self._detect_clang()
            if clang:
                compilers.append(clang)

        return compilers

    def select_best(self, preferred: Optional[str] = None) -> Optional[CompilerInfo]:
        """Select the best compiler based on preference and availability."""
        compilers = self.detect_all()

        if not compilers:
            return None

        if preferred:
            # Try to find preferred compiler
            for compiler in compilers:
                if compiler.name.lower() == preferred.lower():
                    return compiler

        # Default selection based on platform
        if self.platform == Platform.WINDOWS:
            # Prefer MSVC, then MSVC-clang, then MinGW-GCC, then MinGW-clang
            for compiler in compilers:
                if compiler.name.lower() == "msvc":
                    return compiler
            for compiler in compilers:
                if compiler.name.lower() == "msvc-clang":
                    return compiler
            for compiler in compilers:
                if compiler.name.lower() == "mingw-gcc":
                    return compiler
            for compiler in compilers:
                if compiler.name.lower() == "mingw-clang":
                    return compiler

        elif self.platform == Platform.LINUX:
            # Prefer GCC, then Clang
            for compiler in compilers:
                if compiler.name.lower() == "gcc":
                    return compiler
            for compiler in compilers:
                if compiler.name.lower() == "clang":
                    return compiler

        elif self.platform == Platform.MACOS:
            # Prefer Clang
            for compiler in compilers:
                if compiler.name.lower() == "clang":
                    return compiler

        # Return first available if no preference matches
        return compilers[0]
```

---

## 9. Logging Architecture

### 9.1 Overview

The logging architecture provides a unified logging system for both C++ and Python, with file rotation, colored output, and configurable log levels.

### 9.2 C++ Logging (spdlog)

**Configuration File:** `config/logging_cpp.json`

```json
{
  "version": 1,
  "loggers": {
    "default": {
      "level": "info",
      "sinks": ["console", "file"],
      "pattern": "[%Y-%m-%d %H:%M:%S.%e] [%l] [%n] %v"
    }
  },
  "sinks": {
    "console": {
      "type": "console_color_sink",
      "level": "info",
      "pattern": "[%^%l%$] %v"
    },
    "file": {
      "type": "rotating_file_sink",
      "level": "debug",
      "filename": "logs/omnicpp.log",
      "max_size": 10485760,
      "max_files": 5,
      "pattern": "[%Y-%m-%d %H:%M:%S.%e] [%l] [%n] %v"
    }
  }
}
```

**Integration:**

```cpp
// include/engine/logging/logger.hpp
#pragma once

#include <spdlog/spdlog.h>
#include <memory>

namespace engine {
namespace logging {

class Logger {
public:
    static void initialize(const std::string& config_path);
    static std::shared_ptr<spdlog::logger> get_logger(const std::string& name = "default");

private:
    static std::shared_ptr<spdlog::logger> default_logger_;
};

} // namespace logging
} // namespace engine
```

### 9.3 Python Logging

**Configuration File:** `config/logging_python.json`

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "colored": {
      "()": "omni_scripts.logging.formatters.ColoredFormatter",
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    },
    "detailed": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "colored",
      "stream": "ext://sys.stdout"
    },
    "file": {
      "class": "omni_scripts.logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "detailed",
      "filename": "logs/omnicpp_python.log",
      "maxBytes": 10485760,
      "backupCount": 5,
      "encoding": "utf-8"
    }
  },
  "loggers": {
    "omni_scripts": {
      "level": "DEBUG",
      "handlers": ["console", "file"],
      "propagate": false
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console"]
  }
}
```

**Implementation:**

```python
# omni_scripts/logging/logger.py
import logging
import logging.config
from pathlib import Path
from typing import Optional

class Logger:
    """Main logger implementation."""

    _initialized: bool = False
    _config_path: Optional[Path] = None

    @classmethod
    def initialize(cls, config_path: Optional[Path] = None) -> None:
        """
        Initialize the logging system.

        Args:
            config_path: Path to logging configuration file
        """
        if cls._initialized:
            return

        if config_path is None:
            config_path = Path("config/logging_python.json")

        cls._config_path = config_path

        # Load configuration
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Configure logging
        logging.config.dictConfig(config)

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str = "omni_scripts") -> logging.Logger:
        """
        Get a logger instance.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        if not cls._initialized:
            cls.initialize()

        return logging.getLogger(name)
```

**Custom Formatters:**

```python
# omni_scripts/logging/formatters.py
import logging
from typing import Dict

class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    COLORS: Dict[int, str] = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)
```

**Custom Handlers:**

```python
# omni_scripts/logging/handlers.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class RotatingFileHandler(RotatingFileHandler):
    """Rotating file handler with automatic directory creation."""

    def __init__(self, filename: str, maxBytes: int = 10485760, backupCount: int = 5, **kwargs):
        """
        Initialize rotating file handler.

        Args:
            filename: Log file path
            maxBytes: Maximum file size in bytes
            backupCount: Number of backup files to keep
            **kwargs: Additional arguments for RotatingFileHandler
        """
        # Create log directory if it doesn't exist
        log_path = Path(filename)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, **kwargs)
```

### 9.4 Logging Configuration Management

```python
# omni_scripts/logging/config.py
import json
from pathlib import Path
from typing import Dict, Any

class LoggingConfig:
    """Logging configuration management."""

    def __init__(self, config_path: Path) -> None:
        """
        Initialize logging configuration.

        Args:
            config_path: Path to logging configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load logging configuration from file."""
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self) -> None:
        """Save logging configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_logger_level(self, logger_name: str) -> str:
        """Get logger level."""
        return self.config["loggers"].get(logger_name, {}).get("level", "INFO")

    def set_logger_level(self, logger_name: str, level: str) -> None:
        """Set logger level."""
        if logger_name not in self.config["loggers"]:
            self.config["loggers"][logger_name] = {}
        self.config["loggers"][logger_name]["level"] = level

    def get_handler_level(self, handler_name: str) -> str:
        """Get handler level."""
        return self.config["handlers"].get(handler_name, {}).get("level", "INFO")

    def set_handler_level(self, handler_name: str, level: str) -> None:
        """Set handler level."""
        if handler_name not in self.config["handlers"]:
            self.config["handlers"][handler_name] = {}
        self.config["handlers"][handler_name]["level"] = level
```

---

## 10. Package Manager Integration

### 10.1 Overview

The package manager integration provides a unified interface for Conan, vcpkg, and CPM, with priority-based selection and automatic fallback.

### 10.2 Priority-Based Selection

**Priority Order:**

1. **Conan** (highest priority)
2. **vcpkg**
3. **CPM** (lowest priority)

**Selection Logic:**

```python
# omni_scripts/package_managers/manager.py
from typing import Optional, List
from enum import Enum

class PackageManagerType(Enum):
    """Package manager types."""
    CONAN = "conan"
    VCPKG = "vcpkg"
    CPM = "cpm"

class PackageManagerManager:
    """Package manager coordinator."""

    def __init__(self) -> None:
        self.available_managers: List[PackageManagerType] = []
        self._detect_available()

    def _detect_available(self) -> None:
        """Detect available package managers."""
        # Check for Conan
        if self._is_conan_available():
            self.available_managers.append(PackageManagerType.CONAN)

        # Check for vcpkg
        if self._is_vcpkg_available():
            self.available_managers.append(PackageManagerType.VCPKG)

        # CPM is always available (it's a CMake module)
        self.available_managers.append(PackageManagerType.CPM)

    def select_manager(self, preferred: Optional[PackageManagerType] = None) -> Optional[PackageManagerType]:
        """
        Select package manager based on priority and preference.

        Args:
            preferred: Preferred package manager

        Returns:
            Selected package manager
        """
        if not self.available_managers:
            return None

        if preferred and preferred in self.available_managers:
            return preferred

        # Return highest priority available
        return self.available_managers[0]

    def _is_conan_available(self) -> bool:
        """Check if Conan is available."""
        import shutil
        return shutil.which("conan") is not None

    def _is_vcpkg_available(self) -> bool:
        """Check if vcpkg is available."""
        import shutil
        return shutil.which("vcpkg") is not None
```

### 10.3 Conan Integration

```python
# omni_scripts/package_managers/conan.py
from typing import List, Dict, Any
from pathlib import Path

class ConanManager:
    """Conan package manager integration."""

    def __init__(self, config_path: Path = Path("conan/conanfile.py")) -> None:
        """
        Initialize Conan manager.

        Args:
            config_path: Path to conanfile.py
        """
        self.config_path = config_path
        self.profiles_dir = Path("conan/profiles")

    def install(self, profile: str = "default") -> None:
        """
        Install Conan dependencies.

        Args:
            profile: Conan profile to use
        """
        import subprocess

        profile_path = self.profiles_dir / profile

        cmd = [
            "conan",
            "install",
            ".",
            "--profile:build=default",
            f"--profile:host={profile_path}",
            "--build=missing",
            "--settings=build_type=Release"
        ]

        subprocess.run(cmd, check=True)

    def create_profile(self, name: str, settings: Dict[str, Any]) -> None:
        """
        Create Conan profile.

        Args:
            name: Profile name
            settings: Profile settings
        """
        profile_path = self.profiles_dir / name

        with open(profile_path, 'w') as f:
            f.write("[settings]\n")
            for key, value in settings.items():
                f.write(f"{key}={value}\n")
```

### 10.4 vcpkg Integration

```python
# omni_scripts/package_managers/vcpkg.py
from typing import List, Dict, Any
from pathlib import Path

class VcpkgManager:
    """vcpkg package manager integration."""

    def __init__(self, config_path: Path = Path("vcpkg.json")) -> None:
        """
        Initialize vcpkg manager.

        Args:
            config_path: Path to vcpkg.json
        """
        self.config_path = config_path

    def install(self, triplet: str = "x64-windows") -> None:
        """
        Install vcpkg dependencies.

        Args:
            triplet: vcpkg triplet
        """
        import subprocess

        cmd = [
            "vcpkg",
            "install",
            "--triplet",
            triplet
        ]

        subprocess.run(cmd, check=True)

    def integrate(self) -> None:
        """Integrate vcpkg with CMake."""
        import subprocess

        cmd = ["vcpkg", "integrate", "install"]
        subprocess.run(cmd, check=True)
```

### 10.5 CPM Integration

```python
# omni_scripts/package_managers/cpm.py
from typing import Dict, Any

class CPMManager:
    """CPM.cmake package manager integration."""

    def __init__(self) -> None:
        """Initialize CPM manager."""
        self.cmake_file = Path("cmake/CPM.cmake")

    def add_dependency(self, name: str, version: str, git_repo: Optional[str] = None) -> str:
        """
        Add CPM dependency.

        Args:
            name: Package name
            version: Package version
            git_repo: Git repository URL (optional)

        Returns:
            CPM add command
        """
        if git_repo:
            return f'CPMAddPackage("NAME={name} GIT_REPOSITORY={git_repo} GIT_TAG={version}")'
        else:
            return f'CPMAddPackage("NAME={name} VERSION={version}")'
```

---

## 11. Files to Keep, Consolidate, and Remove

### 11.1 Files to Keep

**Root Level:**

- `CMakeLists.txt` - Root CMake configuration
- `CMakePresets.json` - CMake presets
- `dependencies.cmake` - CPM dependency management
- `vcpkg.json` - vcpkg package manifest
- `pyproject.toml` - Python project configuration
- `requirements.txt` - Python dependencies
- `requirements-docs.txt` - Documentation dependencies
- `README.md` - Project README
- `LICENSE` - License file
- `CHANGELOG.md` - Changelog
- `.gitignore` - Git ignore patterns
- `.clang-format` - Clang-format configuration
- `.clang-format-ignore` - Clang-format ignore patterns
- `.clang-tidy` - Clang-tidy configuration
- `.clangd` - Clangd language server configuration
- `.ccls` - CCLS language server configuration
- `.cmake-format` - CMake-format configuration
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `mkdocs.yml` - MkDocs documentation configuration
- `Doxyfile` - Doxygen documentation configuration

**omni_scripts/ (Consolidated):**

- All files from `omni_scripts/` directory
- Useful files from `scripts/python/` directory (consolidated)
- Useful files from `impl/tests/` directory (consolidated)

**cmake/:**

- All CMake modules and toolchains

**conan/:**

- All Conan configuration files, profiles, and setup scripts

**config/:**

- All configuration files

**include/:**

- All C++ header files

**src/:**

- All C++ source files

**tests/:**

- All test files

**docs/:**

- All documentation files

**practices/:**

- All best practices documentation

**examples/:**

- All example projects

### 11.2 Files to Consolidate

**Python Scripts:**

- **scripts/python/** → **omni_scripts/**
  - Consolidate all useful scripts from `scripts/python/` into `omni_scripts/`
  - Remove duplicates
  - Merge similar functionality

- **impl/tests/** → **tests/python/**
  - Move all implementation tests to `tests/python/`
  - Remove duplicates

**Duplicate Manager Classes:**

- **CompilerManager**: Keep `omni_scripts/compilers/detector.py`, remove `scripts/python/compilers/manager.py` and `scripts/python/compilers/compiler_manager.py`

- **Duplicate Detector Interfaces**: Keep single interface definition in `omni_scripts/compilers/base.py`, remove duplicates

- **Duplicate Utility Functions**: Keep implementations in `omni_scripts/utils/`, remove duplicates from `scripts/python/core/`

**Duplicate Compiler Detection:**

- Keep comprehensive compiler detection in `omni_scripts/compilers/`
- Remove simplified detection from `scripts/python/compilers/`

### 11.3 Files to Remove

**Deprecated Build Targets:**

- Remove all references to `targets/qt-vulkan/library` and `targets/qt-vulkan/standalone`
- Update CMake configuration files to remove deprecated target references

**Deprecated Directory:**

- `targets/` directory (already deleted, remove any remaining references)

**Deprecated Emscripten Features:**

- Remove references to deprecated Asyncify in `cmake/user/tmplt-emscripten.cmake`

**Duplicate Files:**

- `scripts/python/compilers/manager.py` - Duplicate CompilerManager
- `scripts/python/compilers/compiler_manager.py` - Duplicate CompilerManager
- `scripts/python/compilers/mingw_gcc_detector.py` - Duplicate ICompilerDetector interface
- `scripts/python/compilers/mingw_clang_detector.py` - Duplicate ICompilerDetector interface
- `scripts/python/compilers/msvc_detector.py` - Duplicate ICompilerDetector interface
- `scripts/python/compilers/msvc_clang_detector.py` - Duplicate ICompilerDetector interface
- `scripts/python/compilers/msvc_terminal_detector.py` - Duplicate ITerminalDetector interface
- `scripts/python/compilers/mingw_terminal_detector.py` - Duplicate ITerminalDetector interface
- `scripts/python/compilers/compiler_terminal_mapper.py` - Duplicate ITerminalDetector interface

**Legacy Scripts:**

- `scripts/build.py` - Consolidated into `omni_scripts/build.py`
- `scripts/clean.py` - Consolidated into `omni_scripts/controller/clean_controller.py`
- `scripts/format.py` - Consolidated into `omni_scripts/controller/format_controller.py`
- `scripts/lint.py` - Consolidated into `omni_scripts/controller/lint_controller.py`
- `scripts/package.py` - Consolidated into `omni_scripts/controller/package_controller.py`
- `scripts/test.py` - Consolidated into `omni_scripts/controller/test_controller.py`
- `scripts/install.py` - Consolidated into `omni_scripts/controller/install_controller.py`
- `scripts/setup_environment.bat` - Consolidated into `conan/setup/`
- `scripts/setup_environment.ps1` - Consolidated into `conan/setup/`
- `scripts/validate_environment.py` - Consolidated into `omni_scripts/validators/`
- `scripts/detect_msvc_version.ps1` - Consolidated into `omni_scripts/compilers/msvc.py`

**Duplicate Logging Functions:**

- `omni_scripts/utils/logging_utils.py` - Keep, remove duplicate exports from `omni_scripts/logging/__init__.py`

**Duplicate Utility Functions:**

- `scripts/python/core/file_utils.py` - Consolidated into `omni_scripts/utils/file_utils.py`
- `scripts/python/core/` path operations - Consolidated into `omni_scripts/utils/path_utils.py`

**impl/ Directory:**

- `impl/errors.md` - Move to `docs/troubleshooting.md`
- `impl/tests/` - Move to `tests/python/`
- `impl/` directory - Remove after consolidation

**scripts/ Directory:**

- After consolidation, remove entire `scripts/` directory

---

## 12. Migration Plan

### 12.1 Phase 1: Preparation

1. **Backup Current State**
   - Create backup of entire project
   - Document current file structure

2. **Create New Directory Structure**
   - Create `omni_scripts/` subdirectories
   - Create `tests/python/` directory
   - Create `conan/setup/` directory

### 12.2 Phase 2: Consolidation

1. **Consolidate Python Scripts**
   - Move useful scripts from `scripts/python/` to `omni_scripts/`
   - Move implementation tests from `impl/tests/` to `tests/python/`
   - Move setup scripts from `scripts/` to `conan/setup/`

2. **Remove Duplicates**
   - Remove duplicate manager classes
   - Remove duplicate detector interfaces
   - Remove duplicate utility functions

3. **Update Imports**
   - Update all import statements to use new structure
   - Update CMake configuration files
   - Update documentation

### 12.3 Phase 3: Cleanup

1. **Remove Deprecated Files**
   - Remove references to deprecated build targets
   - Remove deprecated Emscripten features
   - Remove duplicate files

2. **Remove Legacy Directories**
   - Remove `scripts/` directory
   - Remove `impl/` directory

3. **Update Documentation**
   - Update all documentation to reflect new structure
   - Update README.md
   - Update migration guide

### 12.4 Phase 4: Validation

1. **Run Tests**
   - Run all Python tests
   - Run all C++ tests
   - Run integration tests

2. **Validate Build System**
   - Test build with all compilers
   - Test cross-platform compilation
   - Test package manager integration

3. **Validate Logging**
   - Test C++ logging
   - Test Python logging
   - Test log rotation

4. **Zero Pylance Errors**
   - Run pylance on all Python files
   - Fix any type errors
   - Ensure all imports are properly typed

---

## 13. Definition of Done

The future state is considered complete when:

- [ ] `.specs/04_future_state/manifest.md` is created
- [ ] Complete directory tree is defined
- [ ] All Python scripts are consolidated into `omni_scripts/`
- [ ] Cross-platform compilation structure is defined
- [ ] Terminal invocation patterns are defined for all compilers
- [ ] Logging architecture is defined for both C++ and Python
- [ ] Package manager integration is defined with priority-based selection
- [ ] Files to keep are identified
- [ ] Files to consolidate are identified
- [ ] Files to remove are identified
- [ ] Migration plan is defined
- [ ] All documentation is updated to reflect new structure

---

## 14. Conclusion

This document defines the future state of the OmniCPP Template codebase, consolidating three separate Python script directories into a single, modular architecture. The refactoring addresses cross-platform compilation issues, eliminates duplicate code, and establishes a clean separation of concerns with zero pylance errors.

The key improvements are:

1. **Single Python script directory** (`omni_scripts/`) eliminates confusion and duplication
2. **Modular architecture** with clear separation of concerns
3. **Cross-platform compilation support** for MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang
4. **Proper terminal invocation** patterns for each compiler environment
5. **Zero pylance errors** with comprehensive type hints
6. **Consolidated logging architecture** for both C++ and Python
7. **Unified package manager integration** with priority-based selection

The migration plan provides a clear path from the current state to the future state, with validation steps to ensure all functionality is preserved during the consolidation process.
