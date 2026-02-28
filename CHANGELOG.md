# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Complete Python build system with OmniCppController.py
- Support for multiple compilers: MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang
- Support for multiple platforms: Windows, Linux, WebAssembly (WASM)
- Dynamic linking architecture for engine library
- CMake 4 best practices implementation
- Conan package manager integration
- vcpkg package manager integration
- CPM.cmake integration
- Comprehensive logging system with spdlog for C++ and custom formatting for Python
- Terminal detection and invocation for Windows (PowerShell, CMD, Git Bash, WSL)
- Platform abstraction layer for cross-platform development
- Code formatting support (clang-format for C++, black for Python)
- Static analysis support (clang-tidy for C++, pylint and mypy for Python)
- CI/CD workflows for GitHub Actions (build, test, release)
- Comprehensive test infrastructure
- VSCode integration with launch configurations and tasks
- Extensive documentation (architecture, API, user guides, developer guides)
- **Nix package manager integration** with [`flake.nix`](flake.nix:1) and [`flake.lock`](flake.lock:1) for reproducible builds
- **CachyOS primary Linux target** with performance-optimized compiler flags
- **Direnv integration** with [`.envrc`](.envrc:1) for automatic environment loading
- **Linux-specific Conan profiles** for GCC 13 and Clang 19
- **Comprehensive Linux documentation** including Nix, CachyOS, troubleshooting, and VSCode setup
- **Nix development environment** with GCC 13 and Clang 19 toolchains
- **CachyOS-specific optimizations** with `-march=native -O3 -flto` flags
- **Linux VSCode configuration** with platform-specific tasks and debug configurations
- **Linux troubleshooting guide** with common issues and solutions
- **Archived Windows support** moved to [`.archive/windows_scripts/`](.archive/windows_scripts/)

### Changed

- Refactored build system from monolithic scripts to modular Python architecture
- Updated CMake configuration to use modern CMake 4 practices
- Improved error handling and logging throughout the build system
- Enhanced cross-platform compatibility

### Fixed

- Fixed terminal environment setup for MinGW compilers on Windows
- Fixed PATH corruption issues in terminal invocation
- Improved compiler detection and toolchain setup

### Removed

- Removed deprecated build scripts and temporary files
- Removed debug documentation files
- Removed orphaned test files from repository root

## [1.0.0] - 2026-01-05

### Added

- Initial release of OmniCPP-template
- Dynamic linking architecture with engine library and game executable
- Support for MSVC, MSVC-Clang, MinGW-GCC, and MinGW-Clang on Windows
- Support for GCC and Clang on Linux
- Vulkan graphics API integration
- Qt6 framework integration (Core, Gui, Widgets)
- Conan package manager for dependency management
- CMake-based build system with presets
- VSCode integration with CMake Tools
- Comprehensive documentation and examples

### Changed

- Migrated from monolithic build system to modular Python controller
- Implemented fractal sharding principle for maintainability
- Added comprehensive error handling and logging

### Fixed

- Fixed cross-platform build issues
- Fixed dynamic loading on Windows and Linux
- Fixed CMake configuration for multiple compilers

## [0.1.0] - Initial Development

### Added

- Project initialization
- Basic CMake configuration
- Engine and game structure
- Initial documentation

