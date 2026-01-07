# Welcome to OmniCppLib

OmniCppLib is a modern C++ template project that demonstrates best practices for building cross-platform C++ applications using CMake 4.0+, C++20 modules, and comprehensive tooling.

## Features

- **C++20 Modules**: Modern module system for better encapsulation and faster compilation
- **Cross-Platform**: Supports Windows, Linux, macOS, and WebAssembly (Emscripten)
- **Comprehensive Tooling**: Includes testing, fuzzing, linting, and CI/CD
- **Qt/Vulkan Integration**: Optional GUI and graphics capabilities
- **Documentation**: Both API docs (Doxygen) and project docs (MkDocs)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# Build the project
cmake -B build -S .
cmake --build build

# Run tests
ctest --test-dir build
```

## Documentation

- [API Documentation](api/overview.md) - Generated from code comments
- [Getting Started](getting-started/installation.md) - Installation and setup
- [Development](development/building.md) - Building and contributing
- [MSVC Builds](msvc-builds.md) - Windows MSVC build instructions
- [MinGW Builds](mingw-builds.md) - Windows MinGW build instructions
- [Linux Builds](linux-builds.md) - Linux build instructions
- [WASM Builds](wasm-builds.md) - WebAssembly build instructions

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](about/license.md) file for details.