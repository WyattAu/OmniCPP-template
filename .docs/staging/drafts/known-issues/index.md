# Known Issues and Limitations

> **TL;DR:** This section documents all known bugs, defects, and design constraints in the OmniCpp template. Understanding these limitations helps you make informed decisions about using this template for your projects.

## Overview

The OmniCpp template is a production-grade C++23 best practice template with a game engine and game example monorepo. However, like any complex software system, it has known issues and limitations that you should be aware of.

This documentation is organized into two main categories:

- **[Known Issues](./known-issues.md)**: Bugs and defects that have been identified but not yet fixed
- **[Limitations](./limitations.md)**: Design constraints and intentional limitations of the system

## Quick Reference

| Category | Severity | Status |
|----------|----------|--------|
| OmniCppController.py bugs | Medium | Open |
| Test execution not implemented | Low | Open |
| Packaging not implemented | Low | Open |
| Platform support (Windows/Linux only) | Medium | By Design |
| C++23 compiler requirements | High | By Design |
| Vulkan-only rendering | Medium | By Design |
| No networking implementation | Low | Open |
| Limited physics engine | Low | By Design |

## Issue Categories

### C++ Issues

- **C++23 Support**: Requires MSVC 19.35+, GCC 13+, or Clang 16+ for full C++23 support
- **ABI Compatibility**: Different compilers may have incompatible ABIs
- **Standard Library**: Different standard library implementations may have varying feature support

### Build System Issues

- **No Parallel Builds**: Build system does not support parallel compilation
- **No Build Caching**: No build caching mechanism implemented
- **Cross-Compilation**: Limited cross-compilation support
- **MinGW Build Pipeline**: Complex inline Python code execution that is error-prone

### Python Issues

- **OmniCppController.py Bugs**: Several bugs in the main controller script
- **Test Execution**: Test execution is not yet implemented
- **Packaging**: Packaging is not yet implemented
- **Python Executable Detection**: Fragile detection logic

### Game Engine Issues

- **Vulkan-Only Rendering**: Only Vulkan is supported (no OpenGL)
- **Single-Threaded Rendering**: Renderer runs on the main thread
- **No Networking**: Network subsystem interface exists but implementation is incomplete
- **Limited Physics**: Physics engine provides basic rigid body simulation only

## Reporting Issues

If you encounter an issue that is not documented here, please:

1. Check the [Troubleshooting Guide](../troubleshooting/index.md) for common problems
2. Search existing issues in the project repository
3. Create a new issue with:
   - A clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, compiler, Python version)

## Contributing Fixes

We welcome contributions to fix known issues. Please see the [Developer Guide](../developer/index.md) for information on how to contribute.

## Related Documentation

- [Troubleshooting Guide](../troubleshooting/index.md)
- [Developer Guide](../developer/index.md)
- [Architecture](../architecture/index.md)
- [Configuration](../configuration/index.md)
