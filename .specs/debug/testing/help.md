# Test: help
# Command: python OmniCppController.py --help
# Timestamp: 2026-01-19T02:07:49.430929
# Exit Code: 0

## STDOUT
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...

OmniCpp Controller - Build and Package Management System

positional arguments:
  {configure,build,clean,install,test,package,format,lint}
                        Available commands
    configure           Configure the build system with CMake
    build               Build the project
    clean               Clean build artifacts
    install             Install build artifacts
    test                Run tests
    package             Create distribution packages
    format              Format code with clang-format and black
    lint                Run static analysis with clang-tidy, pylint, and mypy

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Examples:
    python OmniCppController.py configure
    python OmniCppController.py build engine "Clean Build Pipeline" default release --compiler msvc
    python OmniCppController.py build game "Clean Build Pipeline" default debug --compiler clang-msvc
    python OmniCppController.py build standalone "Clean Build Pipeline" default release
    python OmniCppController.py clean
    python OmniCppController.py install engine release
    python OmniCppController.py format
    python OmniCppController.py lint
        


## STDERR
