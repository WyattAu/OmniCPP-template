# OmniCPP Template - Current State Manifest

**Generated:** 2026-01-06  
**Purpose:** Archaeological scan of codebase structure and organization

---

## Python Scripts

### Main Controller

- **OmniCppController.py** - Main build and package management system controller
  - Commands: configure, build, clean, install, test, package, format, lint
  - Supports multiple compilers: MSVC, MSVC-clang, MinGW-GCC, MinGW-Clang, GCC, Clang
  - Coordinates CMake, Conan, and build managers

### Build System Scripts (omni_scripts/)

- **build.py** - Core build operations manager

  - Classes: BuildContext, BuildError, ConfigurationError, ToolchainError, DependencyError, BuildManager
  - Functions: clean_build_directories, install_dependencies, configure_build_system, build_project, install_artifacts, run_clean_build_pipeline

- **build_optimizer.py** - Build optimization and performance tracking

  - Classes: OptimizationLevel, CacheType, BuildPerformanceData, OptimizationRecommendation, CacheEntry
  - Components: HistoricalPerformanceTracker, PredictiveFailurePrevention, AdvancedCacheManager, BuildOptimizer
  - Features: clang-msvc timeout fixes, memory-aware scheduling, two-phase builds

- **cmake.py** - CMake operations manager

  - Classes: CMakeError, CMakeConfigurationError, CMakeBuildError, CMakeManager
  - Functions: configure, build, install, clean, validate_installation
  - Handles Qt6 and Vulkan SDK path detection

- **conan.py** - Conan dependency management

  - Classes: ConanError, ConanProfileError, ConanInstallError, ConanManager
  - Functions: install, get_profile, validate_installation
  - Supports MSYS2 environment setup

- **config.py** - Configuration management

  - Classes: ConfigManager
  - Functions: detect_platform, setup_vulkan

- **error_handler.py** - Centralized error handling

  - Classes: ErrorSeverity, OmniCppError, BuildError, DependencyError, ConfigurationError, ValidationError, SecurityError
  - Classes: RetryConfig, RecoveryAction, ErrorHandler
  - Decorators: retry_on_failure, with_error_handling

- **job_optimizer.py** - Parallel job count optimization

  - Classes: JobOptimizer
  - Functions: get_system_resources, calculate_optimal_jobs, generate_cmake_job_pools, update_preset_jobs
  - Compiler-specific job calculations for clang-msvc, MSVC, GCC, Clang

- **resilience_manager.py** - Build resilience and fallback mechanisms

  - Classes: ResilienceLevel, FailureType, RetryPolicy, DegradationStrategy, BuildRecoveryState, ResilienceMetrics
  - Classes: RetryManager, GracefulDegradationManager, BuildRecoveryManager, TimeoutHandler, ErrorRecoveryManager, ResilienceManager
  - Features: exponential backoff, graceful degradation, build recovery, timeout handling

- **setup_vulkan.py** - Vulkan SDK setup and validation
  - Classes: SetupError, VulkanSDKDetector, EnvironmentManager, Installer
  - Functions: find_vulkan_sdk_installations, validate_vulkan_sdk_installation, setup_vulkan_environment, install_vulkan_sdk, update_vulkan_sdk

### Utility Scripts (omni_scripts/utils/)

- ****init**.py** - Package initialization
- **command_utils.py** - Command execution with retry logic
- **exceptions.py** - Custom exception classes (NotADirectoryError, CommandExecutionError, PathValidationError)
- **file_utils.py** - File operations (FileUtils class)
- **logging_utils.py** - Logging functions (log_info, log_warning, log_error, log_success)
- **path_utils.py** - Path manipulation (PathUtils class)
- **platform_utils.py** - Platform detection (get_workspace_dir, get_system_platform, is_windows, is_linux, is_macos)
- **system_utils.py** - System operations (SystemUtils class)
- **terminal_utils.py** - Terminal environment setup for MSYS2 and Visual Studio

### Validation Scripts (omni_scripts/validators/)

- **build_validator.py** - Build configuration validation
- **config_validator.py** - Configuration file validation
- **dependency_validator.py** - Dependency resolution validation

---

## CMake Configuration Files

### Root Configuration

- **CMakeLists.txt** - Root CMake configuration

  - CMake 4.0+ minimum requirement
  - Project: OmniCppTemplate v1.0.0
  - Build options: OMNICPP_BUILD_ENGINE, OMNICPP_BUILD_GAME, OMNICPP_BUILD_TESTS, OMNICPP_BUILD_EXAMPLES
  - Dependency options: OMNICPP_USE_VULKAN, OMNICPP_USE_OPENGL, OMNICPP_USE_QT6, OMNICPP_USE_SPDLOG, OMNICPP_USE_GLM, OMNICPP_USE_STB
  - Package manager options: OMNICPP_USE_CONAN, OMNICPP_USE_VCPKG, OMNICPP_USE_CPM
  - Code quality options: OMNICPP_ENABLE_COVERAGE, OMNICPP_ENABLE_FORMATTING, OMNICPP_ENABLE_LINTING

- **CMakePresets.json** - CMake presets for different build configurations

  - Configure presets: default, debug, release
  - Build presets: debug, release, engine-debug, engine-release, game-debug, game-release
  - Supports multi-config generators (MSVC, Xcode)

- **dependencies.cmake** - Enterprise-grade CPM dependency management

  - Functions: cpm_add_enterprise_dependency, cpm_deps_log, cpm_deps_validate_version, cpm_deps_perform_health_check
  - Features: verbose logging, health checks, version compatibility, package lock support

- **vcpkg.json** - vcpkg package manifest

  - Dependencies: vulkan, vulkan-headers, vulkan-loader, vulkan-validationlayers, shaderc, spirv-tools, glslang, spirv-cross
  - Dependencies: fmt, nlohmann-json, zlib, spdlog, catch2, gtest, libpq

- **conan/conanfile.py** - Conan package recipe
  - Package: omnicpp-template v0.0.3
  - Dependencies: fmt, nlohmann_json, zlib, spdlog, catch2, gtest
  - Build settings: fPIC, shared options
  - Compiler-specific configurations for clang, gcc, msvc

### CMake Modules (cmake/)

- **CompilerFlags.cmake** - Compiler-specific flags and settings
- **ConanIntegration.cmake** - Conan package manager integration
- **CPM.cmake** - CPM.cmake package manager integration
- **CPM_0.40.2.cmake** - CPM.cmake version 0.40.2
- **VcpkgIntegration.cmake** - vcpkg package manager integration
- **FindDependencies.cmake** - Dependency finding functions
- **ProjectConfig.cmake** - Project configuration
- **PlatformConfig.cmake** - Platform-specific configuration
- **Testing.cmake** - Testing configuration
- **Coverage.cmake** - Code coverage configuration
- **FormatTargets.cmake** - Code formatting targets
- **LintTargets.cmake** - Code linting targets
- **InstallRules.cmake** - Installation rules
- **PackageConfig.cmake** - Packaging configuration
- **OmniCppEngineConfig.cmake.in** - Engine package config template

### CMake User Templates (cmake/user/)

- **build_options.cmake** - Build option definitions
- **project-common.cmake** - Common project configuration
- **project-library.cmake** - Library build configuration
- **project-standalone.cmake** - Standalone build configuration
- **project-tests.cmake** - Tests build configuration
- **tmplt-architecture.cmake** - Architecture template
- **tmplt-assets.cmake** - Assets template
- **tmplt-coverage.cmake** - Coverage template
- **tmplt-debug.cmake** - Debug template
- **tmplt-emscripten.cmake** - Emscripten template
- **tmplt-hardening.cmake** - Hardening template
- **tmplt-ipo.cmake** - IPO template
- **tmplt-runtime.cmake** - Runtime template
- **tmplt-sanitizer.cmake** - Sanitizer template

### CMake Toolchains (cmake/toolchains/)

- **arm64-linux-gnu.cmake** - ARM64 Linux GNU toolchain
- **arm64-windows-msvc.cmake** - ARM64 Windows MSVC toolchain
- **emscripten.cmake** - Emscripten toolchain
- **x86-linux-gnu.cmake** - x86 Linux GNU toolchain

### Generated CMake Files (cmake/generated/)

- Auto-generated dependency configuration files from Conan and vcpkg
- Contains config files for: brotli, BZip2, double-conversion, fmt, freetype, glib, harfbuzz, Iconv, Intl, libffi, md4c, nlohmann_json, OpenSSL, PCRE2, PNG, PostgreSQL, Qt6, spdlog, SQLite3, ZLIB

---

## C++ Source Files by Module

### Engine Module (src/engine/)

**Core:**

- Engine.cpp, Engine.hpp - Main engine class
- ConsoleLogger.cpp, ConsoleLogger.hpp - Console logging
- Logger.cpp, Logger.hpp - Logging implementation

**Audio:**

- AudioManager.cpp, AudioManager.hpp, audio_manager.cpp, AudioManager.hpp - Audio management

**Input:**

- InputManager.cpp, InputManager.hpp, input_manager.cpp, InputManager.hpp - Input handling

**Physics:**

- PhysicsEngine.cpp, PhysicsEngine.hpp, physics_engine.cpp, PhysicsEngine.hpp - Physics simulation

**Graphics/Rendering:**

- Renderer.cpp, Renderer.hpp - Renderer interface
- graphics/renderer.cpp, renderer.hpp - Graphics renderer

**Platform:**

- Platform.cpp, Platform.hpp, platform.cpp, platform.hpp - Platform abstraction

**Resources:**

- ResourceManager.cpp, ResourceManager.hpp, resource_manager.cpp, ResourceManager.hpp - Resource management

**ECS (Entity Component System):**

- Component.cpp, Component.hpp - Base component
- Entity.cpp, Entity.hpp - Entity management
- MeshComponent.cpp, MeshComponent.hpp - Mesh component
- System.cpp, System.hpp - System base
- TransformComponent.cpp, TransformComponent.hpp - Transform component

**Camera:**

- Camera/CameraComponent.hpp - Camera component

**Events:**

- event_manager.cpp, event_manager.hpp - Event system

**Scene:**

- scene_manager.cpp, SceneManager.hpp - Scene management
- Scene.cpp, Scene.hpp - Scene class
- SceneNode.cpp, SceneNode.hpp - Scene node

**Scripting:**

- script_manager.cpp, ScriptManager.hpp - Script management

**Vulkan:**

- Vulkan/VulkanDevice.cpp, VulkanDevice.hpp - Vulkan device
- Vulkan/VulkanInstance.cpp, VulkanInstance.hpp - Vulkan instance
- Vulkan/VulkanRenderer.cpp, VulkanRenderer.hpp - Vulkan renderer
- Vulkan/ShaderManager.cpp, ShaderManager.hpp - Shader management
- Vulkan/PyramidGeometry.cpp, PyramidGeometry.hpp - Geometry

**Window:**

- window/window_manager.cpp, window_manager.hpp - Window management

**Qt Integration:**

- Qt/MainWindow.cpp, MainWindow.hpp - Qt main window
- Qt/ControlPanel.cpp, ControlPanel.hpp - Qt control panel
- Qt/FPSOverlay.cpp, FPSOverlay.hpp - FPS overlay
- Qt/RenderWidget.cpp, RenderWidget.hpp - Qt render widget
- Qt/QtVulkanIntegration.cpp, QtVulkanIntegration.hpp - Qt-Vulkan integration

**Utils:**

- utils/string_utils.cpp, string_utils.hpp - String utilities

### Game Module (src/game/)

**Core:**

- Game.cpp, Game.hpp - Main game class
- core/game.cpp, game.hpp - Game core

**Examples:**

- DemoGame.cpp, DemoGame.hpp - Demo game
- PongGame.cpp, PongGame.hpp - Pong game
- Pong3D.cpp, PongMinimal.cpp, PongStandalone.cpp - Pong variants
- PongMain.cpp - Pong test main
- PongTest1.cpp, PongTest2.cpp, PongTest3.cpp - Pong tests
- SimpleTest.cpp - Simple test
- PongWorking.cpp - Working Pong

**Audio:**

- audio/game_audio.cpp, game_audio.hpp - Game audio

**Graphics:**

- graphics/game_renderer.cpp, game_renderer.hpp - Game renderer

**Input:**

- input/game_input.cpp, game_input.hpp - Game input

**Network:**

- network/game_network.cpp, game_network.hpp - Game networking

**Physics:**

- physics/game_physics.cpp, game_physics.hpp - Game physics

**Platform:**

- platform/game_platform.cpp, game_platform.hpp - Game platform

**Scene:**

- scene/game_scene.cpp, game_scene.hpp - Game scene

**Scripting:**

- scripting/game_script.cpp, game_script.hpp - Game scripting

**Utils:**

- utils/game_utils.cpp, game_utils.hpp - Game utilities

**Qt Integration:**

- Qt/PongMainWindow.cpp, PongMainWindow.hpp - Pong Qt window
- Qt/PongControlPanel.cpp, PongControlPanel.hpp - Pong control panel
- Qt/PongRenderWidget.cpp, PongRenderWidget.hpp - Pong render widget

### OmniCppLib Module (include/OmniCppLib/)

- OmniCppLib.hpp, OmniCppLib/version.h - Library interface and version

### Utility Headers (include/)

- math.hpp - Math utilities
- string_utils.hpp - String utilities

---

## Build System Components

### Package Managers

- **Conan** - C/C++ package manager

  - Profiles: msvc, msvc-debug, msvc-release, clang-msvc, clang-msvc-debug, clang-msvc-release, mingw-clang, mingw-clang-debug, mingw-clang-release, mingw-gcc, mingw-gcc-debug, mingw-gcc-release, emscripten
  - Setup scripts: setup_clang_mingw_ucrt.bat, setup_clang_mingw.bat, setup_clang.bat, setup_gcc_mingw_ucrt.bat, setup_gcc_mingw.bat, setup_msvc.bat, setup_emscripten.bat, setup_emscripten.sh

- **vcpkg** - C++ package manager

  - Manifest: vcpkg.json
  - Dependencies: Vulkan ecosystem, fmt, nlohmann-json, zlib, spdlog, catch2, gtest, libpq

- **CPM** - CPM.cmake package manager
  - Version: 0.40.2
  - Module: CPM_0.40.2.cmake
  - CPM Modules: FindCPMLicenses.cmake.cmake, Findcxxopts.cmake, Findjson.cmake, FindOpenSSL.cmake

### Build Scripts (scripts/)

- **build.py** - Build operations
- **clean.py** - Clean build artifacts
- **format.py** - Code formatting
- **lint.py** - Code linting
- **package.py** - Package creation
- **test.py** - Test execution
- **install.py** - Installation
- **setup_environment.bat** - Environment setup (Windows)
- **setup_environment.ps1** - Environment setup (PowerShell)
- **validate_environment.py** - Environment validation
- **detect_msvc_version.ps1** - MSVC version detection

### Python Scripts (scripts/python/)

- **omnicppcontroller.py** - Controller wrapper
- **cmake/** - CMake operations
- **commands/** - Command utilities
- **compilers/** - Compiler configurations
- **core/** - Core utilities
- **package_managers/** - Package manager operations
- **targets/** - Target configurations

---

## Configuration Files

### Build Configuration (config/)

- **build.json** - Build configuration
- **compilers.json** - Compiler settings
- **logging_cpp.json** - C++ logging configuration
- **logging_python.json** - Python logging configuration
- **logging.json** - General logging configuration
- **project.json** - Project metadata
- **targets.json** - Build target definitions

### Project Configuration

- **pyproject.toml** - Python project configuration
- **requirements.txt** - Python dependencies
- **requirements-docs.txt** - Documentation dependencies

### Documentation Configuration

- **mkdocs.yml** - MkDocs documentation configuration
- **Doxyfile** - Doxygen documentation configuration

### Code Quality Configuration

- **.clang-format** - Clang-format configuration
- **.clang-format-ignore** - Clang-format ignore patterns
- **.clang-tidy** - Clang-tidy configuration
- **.clangd** - Clangd language server configuration
- **.ccls** - CCLS language server configuration
- **.cmake-format** - CMake-format configuration
- **.pre-commit-config.yaml** - Pre-commit hooks configuration

### Version Control

- **.gitignore** - Git ignore patterns

---

## VSCode Configuration Files (.vscode/)

- **c_cpp_properties.json** - C/C++ IntelliSense configuration
- **cmake-kits.json** - CMake kits configuration
- **cmake-variants.json** - CMake variants configuration
- **extensions.json** - VSCode extensions
- **keybindings.json** - Keyboard shortcuts
- **launch-windows.json** - Launch configurations (Windows)
- **launch.json** - Launch configurations
- **settings.json** - VSCode settings
- **tasks.json** - Build tasks

---

## Deprecated or Duplicate Files

### Potential Duplicates

- **terminal_utils_backup.py** - Backup of terminal utilities
- **terminal_utils_fixed.py** - Fixed version of terminal utilities
- **terminal_utils_v2.py** - Version 2 of terminal utilities
- **omnicppcontroller.py** (scripts/python/) - Duplicate of main controller

### Deprecated Targets

- **targets/qt-vulkan/library** - Deprecated, use 'engine' instead
- **targets/qt-vulkan/standalone** - Deprecated, use 'game' instead

---

## Build Artifacts

- **build_test/** - Test build directory
- **packages/** - Distribution packages
- **cmake/generated/** - Auto-generated CMake files
- **.mypy_cache/** - MyPy type checking cache
- **.pytest_cache/** - Pytest cache
- **logs/** - Build and runtime logs

---

## Documentation Structure

- **docs/** - User documentation
- **doc/** - API documentation
- **practices/** - Best practices and guides
- **examples/** - Example projects

---

## Testing Structure

- **tests/** - Test source files
- **impl/tests/** - Implementation tests
- **validation_reports/** - Validation reports

---

## Notes

- Project uses CMake 4.0+ as build system
- Supports Windows, Linux, and WASM platforms
- Multiple compiler support: MSVC, MSVC-clang, MinGW-GCC, MinGW-Clang, GCC, Clang
- Multiple package managers: Conan, vcpkg, CPM
- Graphics APIs: Vulkan (primary), OpenGL (optional), Qt6 (optional)
- Logging: spdlog for C++, custom for Python
- Testing: Catch2, Google Test
- Math: GLM library
- JSON: nlohmann/json
- Compression: zlib, BZip2
- Image: STB library
- Database: PostgreSQL (optional)

