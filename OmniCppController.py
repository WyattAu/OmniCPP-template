#!/usr/bin/env python3
"""
OmniCpp Controller - Build and Package Management System.

This module provides the main controller for the OmniCpp build system,
supporting multiple compilers, toolchains, and platforms. It supports
MSVC, MSVC-clang, mingw-clang, and mingw-gcc on Windows,
and GCC and Clang on Linux.

Usage:
    python OmniCppController.py <command> [options]

Commands:
    configure   Configure the build system with CMake
    build       Build the project
    clean       Clean build artifacts
    install     Install build artifacts
    test        Run tests
    package     Create distribution packages
    format      Format code with clang-format and black
    lint        Run static analysis with clang-tidy, pylint, and mypy
    help        Show help information

Examples:
    python OmniCppController.py configure
    python OmniCppController.py build --target game --config release
    python OmniCppController.py clean
    python OmniCppController.py format
    python OmniCppController.py lint
"""

from __future__ import annotations

import sys

# Import modular controller system
from omni_scripts.controller.dispatcher import main as dispatcher_main


def main() -> int:
    """Main entry point for OmniCpp controller.

    This function delegates to the modular command dispatcher
    which provides a single source of truth for CLI parsing.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Delegate to modular dispatcher
    return dispatcher_main()


if __name__ == "__main__":
    sys.exit(main())
