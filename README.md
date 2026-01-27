# OmniCpp - Modern C++ Game Engine Template

A production-ready, modular, cross-platform C++ game engine template with dynamic linking architecture, supporting multiple compilers, toolchains, and platforms.

## Features

- **Dynamic Linking Architecture** - Game executable dynamically loads engine library at runtime
- **Multi-Compiler Support** - MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang
- **Multi-Platform Support** - Windows, Linux, WebAssembly (WASM)
- **Modern C++ Standards** - C++23 best practices without modules
- **CMake 4 Best Practices** - Modern CMake configuration with presets
- **Package Manager Integration** - Conan, vcpkg, and CPM.cmake
- **Comprehensive Logging System** - Structured logging with multiple handlers, formatters, and configuration
- **Platform Detection** - Automatic OS and architecture detection with cross-platform support
- **Compiler Detection** - Automatic compiler detection with C++23 validation
- **Terminal Environment Setup** - Automatic terminal setup for MSVC, MinGW, and Linux environments
- **Code Quality Tools** - clang-format, clang-tidy, pylint, mypy
- **CI/CD Workflows** - GitHub Actions for build, test, and release
- **VSCode Integration** - Seamless development experience with CMake Tools
- **Extensive Documentation** - Architecture, API, user guides, developer guides

## Architecture

OmniCpp follows a dynamic linking architecture where the game executable dynamically loads the engine library at runtime:

```
┌─────────────────────────────────────────────────────────────┐
│                     Game Executable                      │
│                  (omnicpp_game.exe)                    │
│                                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dynamic Library Loader (dlopen/LoadLibrary)    │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                 │
│                         ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Engine Interface (IEngine)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Engine Library (omnicpp_engine.dll)         │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Renderer │  │  Input   │  │  Audio   │          │
│  │ (Vulkan) │  │ Manager  │  │ Manager  │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Physics  │  │ Resource │  │  Logger  │          │
│  │  Engine  │  │ Manager  │  │          │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                           │
│  ┌──────────┐                                           │
│  │ Platform │                                           │
│  │  Layer  │                                           │
│  └──────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
OmniCPP-template/
├── .specs/                # Project specifications and requirements
├── .github/workflows/     # CI/CD workflows (build, test, release)
├── cmake/                 # CMake configuration files
│   ├── CompilerFlags.cmake
│   ├── PlatformConfig.cmake
│   ├── ConanIntegration.cmake
│   ├── VcpkgIntegration.cmake
│   ├── FindDependencies.cmake
│   ├── Testing.cmake
│   ├── Coverage.cmake
│   └── Utils.cmake
├── config/                # Configuration files
│   ├── project.json
│   ├── build.json
│   ├── compilers.json
│   ├── targets.json
│   ├── logging.json
│   ├── logging_cpp.json
│   ├── logging_python.json
│   ├── conanfile.txt
│   └── vcpkg.json
├── conan/profiles/         # Conan profiles for different compilers
├── docs/                  # Documentation
│   ├── architecture/
│   ├── api/
│   ├── user/
│   ├── developer/
│   └── config/
├── examples/               # Example projects
├── include/               # Public headers
│   ├── engine/              # Engine public API
│   │   ├── Engine.hpp
│   │   ├── IRenderer.hpp
│   │   ├── IInputManager.hpp
│   │   ├── IAudioManager.hpp
│   │   ├── IPhysicsEngine.hpp
│   │   ├── IResourceManager.hpp
│   │   ├── ILogger.hpp
│   │   └── IPlatform.hpp
│   ├── game/               # Game public API
│   │   └── Game.hpp
│   └── OmniCppLib/         # Standalone library headers
├── impl/tests/            # Test infrastructure
│   ├── build_consistency.py
│   ├── cross_platform_validation.py
│   ├── performance_monitoring.py
│   ├── platform_checks.py
│   └── test_suite.py
├── omni_scripts/          # Modular Python build scripts
│   ├── __init__.py
│   ├── build.py
│   ├── cmake.py
│   ├── conan.py
│   ├── config.py
│   ├── error_handler.py
│   ├── resilience_manager.py
│   ├── setup_vulkan.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── command_utils.py
│   │   ├── exceptions.py
│   │   ├── file_utils.py
│   │   ├── logging_utils.py
│   │   ├── path_utils.py
│   │   ├── platform_utils.py
│   │   ├── system_utils.py
│   │   └── terminal_utils.py
│   └── validators/
│       ├── __init__.py
│       ├── build_validator.py
│       ├── config_validator.py
│       └── dependency_validator.py
├── packages/              # Build artifacts
├── practices/             # Best practices documentation
├── scripts/               # Build and utility scripts
├── src/                   # Source code
│   ├── engine/              # Engine implementation
│   │   ├── core/
│   │   ├── memory/
│   │   ├── logging/
│   │   ├── events/
│   │   ├── input/
│   │   ├── window/
│   │   ├── graphics/
│   │   ├── audio/
│   │   └── resources/
│   ├── game/               # Game implementation
│   └── platform/            # Platform abstraction
│       ├── windows/
│       ├── linux/
│       └── wasm/
├── tests/                 # Test files
├── validation_reports/     # Validation reports
├── .vscode/              # VSCode configuration
├── OmniCppController.py    # Main build controller
├── CMakeLists.txt         # Root CMake file
├── CMakePresets.json      # CMake presets
├── pyproject.toml         # Python project configuration
├── requirements.txt         # Python dependencies
├── vcpkg.json            # vcpkg dependencies
└── CHANGELOG.md           # Changelog
```

## Supported Compilers

### Windows

- **MSVC** (Microsoft Visual C++) - Recommended for production
- **MSVC-Clang** - Clang with MSVC ABI
- **MinGW-GCC** - MinGW with GCC
- **MinGW-Clang** - MinGW with Clang

### Linux

- **GCC** - Default compiler
- **Clang** - Alternative compiler

### WebAssembly

- **Emscripten** - LLVM to WebAssembly compiler

## Supported Platforms

### Windows

- Windows 10/11
- MSVC 2019/2022
- MinGW-w64

### Linux

- Ubuntu 20.04+
- Debian 11+
- Fedora 35+

### WebAssembly

- Modern browsers with WASM support
- Node.js environments

## Dependencies

### Core Dependencies

- **Vulkan** - Graphics API
- **Qt6** - UI framework (Core, Gui, Widgets)
- **spdlog** - Fast C++ logging library
- **nlohmann/json** - JSON library for C++

### Package Managers

- **Conan** - C/C++ package manager
- **vcpkg** - C/C++ package manager
- **CPM.cmake** - CMake package manager

### Build Tools

- **CMake** 3.20+ (CMake 4 best practices)
- **Python** 3.11+
- **Ninja** - Build system

## Building

### Prerequisites

1. Install Python 3.11+
2. Install Conan: `pip install conan`
3. Install CMake 3.20+
4. Install a supported compiler (MSVC, GCC, Clang, MinGW)
5. Install Vulkan SDK
6. Install Qt6 (optional, for UI features)

### Logging System

The project includes a comprehensive logging system with the following features:

- **Structured Logging** - Multiple handlers (console, file) with rotation support
- **Custom Formatters** - Colored console output, JSON logging, custom formatting
- **Configuration-Driven** - JSON-based configuration with environment variable overrides
- **Dynamic Log Levels** - Runtime log level changes
- **Backward Compatibility** - Legacy logging functions supported during migration

The logging system is automatically initialized when the controller starts and provides:
- Console output with color-coded messages
- File output with automatic rotation and retention
- Structured JSON logging for CI/CD integration
- Per-module loggers for fine-grained control

### Platform Detection

The project includes automatic platform detection with the following capabilities:

- **OS Detection** - Windows, Linux, macOS
- **Architecture Detection** - x86_64, ARM64, x86
- **Platform Information** - Comprehensive platform details for build decisions
- **Cross-Platform Support** - Platform-specific code paths and configurations

Platform detection is automatically performed on controller initialization and provides:
- Platform-aware compiler selection
- Platform-specific terminal setup
- Cross-platform build configuration
- Architecture-specific optimizations

### Compiler Detection

The project includes automatic compiler detection with the following features:

- **Multi-Compiler Support** - MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang
- **C++23 Validation** - Automatic validation of C++23 support with fallback to C++20
- **Version Detection** - Automatic version detection for all supported compilers
- **Platform-Specific Detection** - Windows (MSVC, MinGW), Linux (GCC, Clang)
- **Compiler Information** - Comprehensive compiler details including path and capabilities

Compiler detection is automatically performed on controller initialization and provides:
- Automatic compiler selection based on platform
- C++23 support validation with warnings
- Fallback to C++20 if C++23 not supported
- Compiler-specific build configurations

### Terminal Environment Setup

The project includes automatic terminal environment setup with the following features:

- **VS Dev Prompt** - Automatic Visual Studio Developer Command Prompt setup for MSVC
- **MSYS2 Integration** - Automatic MSYS2 UCRT64 environment setup for MinGW
- **Linux Environment** - Automatic environment setup for Linux compilers
- **Path Conversion** - Automatic Windows to MSYS2 path conversion
- **Environment Validation** - Verification of terminal environment before builds

Terminal setup is automatically performed for MinGW builds and provides:
- Correct environment variables for each compiler
- Proper PATH configuration
- Working directory preservation
- Cross-platform command execution

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd OmniCPP-template

# Install dependencies
pip install -r requirements.txt

# Configure and build
python OmniCppController.py configure
python OmniCppController.py build engine "Clean Build Pipeline" default release --compiler msvc
```

### Build Commands

```bash
# Configure build system
python OmniCppController.py configure --build-type Release

# Build engine library
python OmniCppController.py build engine "Clean Build Pipeline" default release --compiler msvc

# Build game executable
python OmniCppController.py build game "Clean Build Pipeline" default debug --compiler msvc

# Build standalone library
python OmniCppController.py build standalone "Clean Build Pipeline" default release --compiler msvc

# Build everything
python OmniCppController.py build all "Clean Build Pipeline" default release --compiler msvc

# Clean build artifacts
python OmniCppController.py clean

# Install build artifacts
python OmniCppController.py install engine release

# Run tests
python OmniCppController.py test engine debug

# Format code
python OmniCppController.py format

# Run static analysis
python OmniCppController.py lint

# Show version
python OmniCppController.py --version
```

### Build Configurations

- **Debug** - Debug build with symbols and no optimization
- **Release** - Release build with optimization
- **RelWithDebInfo** - Release with debug information
- **MinSizeRel** - Release optimized for size

### Build Targets

- **engine** - Build the engine library
- **game** - Build the game executable
- **standalone** - Build the standalone library
- **all** - Build all targets

### Build Pipelines

- **Clean Build Pipeline** - Clean, configure, build, install
- **Build Project** - Build project only
- **Configure Build System** - Configure CMake only
- **Install Build Artifacts** - Install artifacts only

## Running the Game

After building, the game executable will be located in the `install/bin/` directory:

```bash
# Windows
install/bin/omnicpp_game.exe

# Linux
install/bin/omnicpp_game
```

The game will automatically load the engine library (`omnicpp_engine.dll` on Windows, `libomnicpp_engine.so` on Linux) from the same directory.

## Development

### Project Structure

The project follows the **fractal sharding principle** - no file exceeds 400 lines, ensuring maintainability and parallel development capability.

### Adding a New Subsystem

1. Create interface in `include/engine/ISubsystem.hpp`
2. Implement subsystem in `src/engine/Subsystem.cpp`
3. Add to `EngineConfig` in `include/engine/Engine.hpp`
4. Initialize in `EngineImpl::initialize()`

### Creating a Game

1. Create game class inheriting from `Game`
2. Implement `initialize()`, `update()`, `render()`, `shutdown()`
3. Add to `src/game/CMakeLists.txt`

### Code Quality

The project includes comprehensive code quality tools:

```bash
# Format C++ code
python OmniCppController.py format --cpp-only

# Format Python code
python OmniCppController.py format --python-only

# Lint C++ code
python OmniCppController.py lint --cpp-only

# Lint Python code
python OmniCppController.py lint --python-only

# Check formatting without modifying
python OmniCppController.py format --check

# Apply automatic fixes
python OmniCppController.py lint --fix
```

## Cross-Platform Development

### Platform Abstraction

The project includes a comprehensive platform abstraction layer:

```cpp
// Platform detection
#include <platform/platform.hpp>

// Platform-specific implementations
#ifdef _WIN32
    // Windows-specific code
#endif

#ifdef __linux__
    // Linux-specific code
#endif

#ifdef __EMSCRIPTEN__
    // WebAssembly-specific code
#endif
```

### Windows-Specific Code

```cpp
#ifdef _WIN32
    // Windows-specific code
#endif
```

### Linux-Specific Code

```cpp
#ifdef __linux__
    // Linux-specific code
#endif
```

### WebAssembly-Specific Code

```cpp
#ifdef __EMSCRIPTEN__
    // WebAssembly-specific code
#endif
```

## Testing

### Running Tests

```bash
# Run all tests
python OmniCppController.py test all release

# Run engine tests
python OmniCppController.py test engine debug

# Run game tests
python OmniCppController.py test standalone release

# Run unit tests (Google Test)
python OmniCppController.py test unit debug

# Run integration tests
python OmniCppController.py test integration release
```

### Test Infrastructure

The project includes comprehensive test infrastructure:

- **Unit Tests** - Component-level testing using Google Test framework
  - SpdLogLogger tests
  - Engine Core tests
  - Input Manager tests
  - Resource Manager tests
  - Physics Engine tests
  - Audio Manager tests
  - ECS (Entity Component System) tests
- **Integration Tests** - End-to-end testing
- **Coverage Tests** - Code coverage measurement
- **Validation Tests** - Build consistency, cross-platform validation, toolchain validation

### Test Framework

The project uses **Google Test** framework for C++ unit testing:
- Modern C++23 test infrastructure
- Comprehensive test coverage for all major subsystems
- Automated test discovery and execution
- Detailed test reporting with assertions

### Test Reports

Test results are saved to `validation_reports/` directory with detailed JSON reports.

## CI/CD

### GitHub Actions Workflows

The project includes GitHub Actions workflows for:

- **Build** - Automated building on all platforms and compilers
- **Test** - Automated testing on all platforms and compilers
- **Release** - Automated release creation

### Build Matrix

| Platform | Compiler    | Configurations |
| -------- | ----------- | -------------- |
| Windows  | MSVC        | Debug, Release |
| Windows  | MSVC-Clang  | Debug, Release |
| Windows  | MinGW-GCC   | Debug, Release |
| Windows  | MinGW-Clang | Debug, Release |
| Linux    | GCC         | Debug, Release |
| Linux    | Clang       | Debug, Release |

## Documentation

### Available Documentation

- **Architecture Documentation** - System architecture, components, data flow, design decisions
- **API Documentation** - Engine API, Game API, Python build system API
- **User Guides** - Getting started, building, testing, cross-platform development, package managers
- **Developer Guides** - Contributing, coding standards, adding features, debugging
- **Configuration Reference** - CMake options, Python config, logging config

### Documentation Location

Documentation is available in the `docs/` directory and can be built using MkDocs:

```bash
# Build documentation
mkdocs build
```

## Packaging

### Creating Distribution Packages

```bash
# Create distribution packages
python OmniCppController.py package game release

# Create packages for all targets
python OmniCppController.py package all release
```

### Package Formats

- **Windows** - ZIP archives
- **Linux** - tar.gz archives
- **WebAssembly** - WASM files

## Troubleshooting

### Common Issues

1. **Build Failures** - Check compiler installation and PATH
2. **Link Errors** - Verify Vulkan SDK and Qt6 installation
3. **Runtime Errors** - Check dynamic library loading and dependencies
4. **Terminal Issues** - Verify terminal detection and environment setup

### Debug Documentation

Debug documentation is available in `docs/troubleshooting.md`:

- Build issues
- Cross-platform issues
- Compiler-specific issues
- Runtime issues

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please read contributing guidelines before submitting pull requests.

### Contribution Guidelines

- Follow the code style guide
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Follow semantic versioning

## Support

For issues and questions, please use the project's issue tracker.

### Getting Help

- Check the documentation in `docs/`
- Review troubleshooting guides
- Search existing issues
- Create a new issue with detailed information

## Version

Current version: 1.0.0

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
