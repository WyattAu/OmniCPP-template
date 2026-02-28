# OmniCPP-Template Coding Standards

**Version:** 1.0.0  
**Last Updated:** 2026-01-27  
**Project:** OmniCPP-Template Monorepo  
**Scope:** Linux Support Expansion

---

## Table of Contents

1. [Overview](#overview)
2. [Python Code Standards](#python-code-standards)
3. [Nix Code Standards](#nix-code-standards)
4. [CMake Code Standards](#cmake-code-standards)
5. [JSON Configuration Standards](#json-configuration-standards)
6. [C/C++ Code Standards](#cc-code-standards)
7. [Cross-Cutting Standards](#cross-cutting-standards)
8. [Linux-Specific Considerations](#linux-specific-considerations)
9. [Code Review Checklist](#code-review-checklist)

---

## Overview

This document defines the coding standards for the OmniCPP-Template monorepo, specifically for the Linux support expansion. These standards ensure consistency, maintainability, and quality across all code in the project.

### Principles

1. **Consistency:** Follow existing patterns and conventions
2. **Clarity:** Write code that is easy to understand
3. **Type Safety:** Use type hints and strict typing where applicable
4. **Defensive Programming:** Validate inputs and handle errors gracefully
5. **Documentation:** Document "why," not "what"
6. **Testing:** Write tests for all new functionality

### Tooling

The project uses the following tools to enforce these standards:

- **Python:** Black (formatter), Pylint (linter), MyPy (type checker), isort (import sorter)
- **C/C++:** clang-format (formatter), clang-tidy (linter), cppcheck (static analyzer)
- **CMake:** cmake-format (formatter)
- **Pre-commit:** Automated checks via pre-commit hooks

---

## Python Code Standards

### File Organization

Python files should follow this structure:

1. Shebang line (for executable scripts)
2. Module docstring
3. Imports (standard library, third-party, local)
4. Constants
5. Classes/Functions
6. Main execution block (if applicable)

### Indentation and Spacing

- **Indentation:** 4 spaces (no tabs)
- **Line Length:** 100 characters maximum
- **Blank Lines:** 2 blank lines between top-level definitions, 1 blank line between method definitions

Example:
```python
#!/usr/bin/env python3
"""
Module docstring describing the purpose of this module.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

# Third-party imports
import yaml

# Local imports
from omni_scripts.logging import get_logger


class ExampleClass:
    """Example class demonstrating coding standards."""

    def __init__(self, name: str) -> None:
        """Initialize the example class.

        Args:
            name: The name of the instance.
        """
        self.name = name
        self.logger = get_logger(__name__)


def example_function(value: int) -> Optional[str]:
    """Example function with type hints.

    Args:
        value: An integer value to process.

    Returns:
        A string representation if value is positive, None otherwise.
    """
    if value > 0:
        return str(value)
    return None
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | `snake_case` | `build_manager.py` |
| Classes | `PascalCase` | `BuildManager` |
| Functions | `snake_case` | `detect_compiler` |
| Variables | `snake_case` | `compiler_info` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private members | `_leading_underscore` | `_internal_method` |
| Protected members | `_leading_underscore` | `_protected_var` |
| Type aliases | `PascalCase` | `CompilerInfo` |

### Type Hints

All functions and methods must have type hints. Use `typing` module for complex types.

```python
from typing import Any, Dict, List, Optional, Union

def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Process input data and return results.

    Args:
        input_data: Dictionary containing input data.
        options: Optional processing options.

    Returns:
        List of processed strings.
    """
    if options is None:
        options = {}
    # Implementation
```

### Import Organization

Imports must be organized in this order:

1. Standard library imports
2. Third-party imports
3. Local imports

Each group separated by a blank line. Use `isort` for automatic sorting.

```python
# Standard library
import argparse
import sys
from pathlib import Path
from typing import Any, Optional

# Third-party
import yaml
from pydantic import BaseModel

# Local
from omni_scripts.logging import get_logger
from omni_scripts.build import BuildManager
```

### Docstring Format

Use Google-style docstrings with triple double quotes.

```python
def build_target(
    target: str,
    config: str,
    compiler: Optional[str] = None,
) -> int:
    """Build the specified target.

    This method builds the project target using the given configuration
    and optional compiler specification.

    Args:
        target: The build target (engine, game, standalone).
        config: Build configuration (debug, release).
        compiler: Optional compiler to use. Defaults to None.

    Returns:
        Exit code (0 for success, non-zero for failure).

    Raises:
        InvalidTargetError: If target is invalid.
        BuildError: If build process fails.

    Example:
        >>> build_target("engine", "debug")
        0
    """
    # Implementation
```

### Error Handling

Use specific exception types and provide meaningful error messages.

```python
class ControllerError(Exception):
    """Base exception for controller-related errors."""

    def __init__(
        self,
        message: str,
        command: Optional[str] = None,
    ) -> None:
        """Initialize controller error.

        Args:
            message: Error message describing the issue.
            command: Optional command that caused the error.
        """
        self.command = command
        super().__init__(message)


def risky_operation(value: int) -> str:
    """Perform a risky operation with proper error handling.

    Args:
        value: The value to process.

    Returns:
        Processed string result.

    Raises:
        ValueError: If value is invalid.
    """
    try:
        if value < 0:
            raise ValueError(f"Value must be non-negative, got {value}")
        return str(value)
    except ValueError as e:
        logger.error(f"Invalid value: {e}")
        raise
```

### Logging Standards

Use the centralized logging system from `omni_scripts.logging`.

```python
from omni_scripts.logging import (
    get_logger,
    log_error,
    log_info,
    log_success,
    log_warning,
    setup_logging,
)

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Use appropriate log levels
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

### Defensive Programming

Validate all inputs and handle edge cases.

```python
def process_path(path: str) -> Path:
    """Process and validate a file path.

    Args:
        path: The path string to process.

    Returns:
        Validated Path object.

    Raises:
        ValueError: If path is empty or invalid.
        FileNotFoundError: If path does not exist.
    """
    # Validate input
    if not path:
        raise ValueError("Path cannot be empty")

    path_obj = Path(path).resolve()

    # Check existence
    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path_obj}")

    return path_obj
```

### Constants

Define constants at module level using UPPER_SNAKE_CASE.

```python
# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0
SUPPORTED_PLATFORMS = ["linux", "windows", "wasm"]
```

---

## Nix Code Standards

### File Structure

Nix files should follow this structure:

1. Description comment
2. Inputs declaration
3. Outputs function
4. Local definitions (let ... in)
5. Output attributes

### Indentation and Spacing

- **Indentation:** 2 spaces
- **Line Length:** No strict limit, but prefer readability
- **Alignment:** Align related attributes vertically where helpful

Example:
```nix
{
  description = "C++ Dev Environment with Qt6, Vulkan, and Clang";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          # Compilers & Tools
          clang
          cmake
          ninja

          # Libraries
          qt6.qtbase
          vulkan-loader
        ];

        shellHook = ''
          echo ">> Loaded C++ Environment"
          export QT_QPA_PLATFORM=wayland
        '';
      };
    };
}
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Inputs | `kebab-case` | `nixpkgs`, `flake-utils` |
| Attributes | `kebab-case` | `devShells`, `packages` |
| Variables | `camelCase` or `kebab-case` | `system`, `buildInputs` |
| Functions | `camelCase` | `mkShell`, `mkDerivation` |

### Comment Style

Use single-line comments for explanations. Place comments above the code they describe.

```nix
{
  description = "Development environment for OmniCPP";

  inputs = {
    # Use unstable branch for latest features
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      # Define system architecture
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        # Core build tools
        buildInputs = with pkgs; [
          clang
          cmake
        ];
      };
    };
}
```

### Attribute Organization

Group related attributes together with section comments.

```nix
{
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      # Development environments
      devShells.${system}.default = pkgs.mkShell { };

      # Packages
      packages.${system}.default = pkgs.stdenv.mkDerivation { };

      # Applications
      apps.${system}.default = {
        type = "app";
        program = "${pkgs.hello}/bin/hello";
      };
    };
}
```

### Function Parameter Ordering

When defining functions, order parameters logically:

1. Required positional parameters
2. Optional positional parameters
3. Named parameters

```nix
# Function definition
mkDevShell = { pkgs, extraPackages ? [ ] }:
  pkgs.mkShell {
    buildInputs = with pkgs; [
      cmake
      ninja
    ] ++ extraPackages;
  };
```

### Module Organization

For complex flakes, use separate modules and import them:

```nix
{
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      # Import modules
      devShell = import ./nix/dev-shell.nix { inherit pkgs; };
      packages = import ./nix/packages.nix { inherit pkgs; };
    in
    {
      devShells.${system}.default = devShell;
      packages.${system} = packages;
    };
}
```

---

## CMake Code Standards

### File Organization

CMake files should follow this structure:

1. File header comment
2. CMake minimum version requirement
3. Project definition
4. Include directories
5. Options/Variables
6. Dependencies
7. Targets
8. Installation rules
9. Testing

Example:
```cmake
# ============================================================================
# OmniCpp Template - Component CMakeLists.txt
# ============================================================================
# CMake 4.0+ Configuration
# ============================================================================

cmake_minimum_required(VERSION 4.0)

# ============================================================================
# Project Configuration
# ============================================================================
project(OmniCppComponent
    VERSION 1.0.0
    DESCRIPTION "Component description"
    LANGUAGES CXX
)

# ============================================================================
# Options
# ============================================================================
option(OMNICPP_ENABLE_FEATURE "Enable feature" ON)

# ============================================================================
# Dependencies
# ============================================================================
find_package(Threads REQUIRED)

# ============================================================================
# Target Definition
# ============================================================================
add_library(omnicpp_component
    src/component.cpp
    src/component_impl.cpp
)

target_include_directories(omnicpp_component
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(omnicpp_component
    PUBLIC
        Threads::Threads
)

# ============================================================================
# Installation
# ============================================================================
install(TARGETS omnicpp_component
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
```

### Variable Naming

| Variable Type | Convention | Example |
|---------------|-----------|---------|
| Cache variables | `UPPER_CASE` | `CMAKE_BUILD_TYPE`, `OMNICPP_BUILD_ENGINE` |
| Internal variables | `lower_case` | `source_files`, `output_dir` |
| Target names | `lower_case` | `omnicpp_engine`, `game_executable` |
| Options | `UPPER_CASE` | `OMNICPP_ENABLE_VULKAN` |

### Target Naming

- Use descriptive, lowercase names with underscores
- Prefix with project name for libraries: `omnicpp_engine`
- Use simple names for executables: `game`, `standalone`

```cmake
# Library targets
add_library(omnicpp_engine ...)
add_library(omnicpp_game ...)

# Executable targets
add_executable(game ...)
add_executable(standalone ...)
```

### Function Ordering

Organize CMake code in logical sections:

1. Configuration (cmake_minimum_required, project)
2. Options and Variables
3. Dependencies (find_package, include)
4. Source file collection
5. Target definitions
6. Target properties
7. Installation rules
8. Testing
9. Packaging

```cmake
# ============================================================================
# Configuration
# ============================================================================
cmake_minimum_required(VERSION 4.0)
project(OmniCppEngine VERSION 1.0.0 LANGUAGES CXX)

# ============================================================================
# Options
# ============================================================================
option(OMNICPP_ENABLE_TESTS "Build tests" ON)

# ============================================================================
# Dependencies
# ============================================================================
find_package(Threads REQUIRED)

# ============================================================================
# Sources
# ============================================================================
set(SOURCES
    src/engine.cpp
    src/renderer.cpp
)

# ============================================================================
# Targets
# ============================================================================
add_library(omnicpp_engine ${SOURCES})

# ============================================================================
# Installation
# ============================================================================
install(TARGETS omnicpp_engine ...)
```

### Comment Style

Use section headers with comment blocks for major sections.

```cmake
# ============================================================================
# Section Title
# ============================================================================
# Detailed description of this section
# ============================================================================

# Single-line comments for specific lines
set(VAR "value")  # Explanation of this line
```

### Conditional Logic

Use clear, readable conditionals with proper indentation.

```cmake
if(OMNICPP_ENABLE_VULKAN)
    find_package(Vulkan)

    if(Vulkan_FOUND)
        target_link_libraries(omnicpp_engine PUBLIC Vulkan::Vulkan)
        message(STATUS "Vulkan support enabled")
    else()
        message(WARNING "Vulkan requested but not found")
        set(OMNICPP_ENABLE_VULKAN OFF)
    endif()
endif()
```

### Modern CMake Practices

- Use target-based commands: `target_include_directories`, `target_link_libraries`
- Use generator expressions: `$<BUILD_INTERFACE:...>`, `$<INSTALL_INTERFACE:...>`
- Use imported targets: `Threads::Threads`, `Vulkan::Vulkan`
- Avoid global commands: `include_directories`, `link_directories`

```cmake
# Modern approach
target_include_directories(omnicpp_engine
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(omnicpp_engine
    PUBLIC
        Threads::Threads
        Vulkan::Vulkan
)
```

---

## JSON Configuration Standards

### File Structure

JSON files should be well-organized with logical grouping of related settings.

### Key Naming

- Use `snake_case` for all keys
- Be descriptive but concise
- Group related keys with common prefixes

Example:
```json
{
  "version": 3,
  "cmakeMinimumRequired": {
    "major": 4,
    "minor": 0,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "debug",
      "displayName": "Debug",
      "description": "Debug build configuration",
      "binaryDir": "${sourceDir}/build/debug",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "OMNICPP_BUILD_ENGINE": "ON"
      }
    }
  ]
}
```

### Sorting Rules

- Maintain logical ordering (not alphabetical)
- Group related settings together
- Keep consistent ordering across similar objects

### Comment Usage

Standard JSON does not support comments. For configurations that need comments:

1. Use JSON5 if supported
2. Add `"description"` fields for documentation
3. Maintain separate documentation files

```json
{
  "name": "debug",
  "description": "Debug build configuration with full debugging symbols",
  "binaryDir": "${sourceDir}/build/debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug"
  }
}
```

### Value Formatting

- Use consistent capitalization for boolean values: `true`, `false`
- Use double quotes for all strings
- Use meaningful default values

```json
{
  "enabled": true,
  "level": "debug",
  "timeout": 30.0,
  "retries": 3
}
```

---

## C/C++ Code Standards

### Indentation and Formatting

- **Indentation:** 2 spaces (GNU style)
- **Line Length:** 100 characters maximum
- **Brace Style:** Allman style (opening brace on new line)
- **Pointer Alignment:** Left (`int* ptr`)

Example:
```cpp
class Engine
{
public:
  Engine();
  ~Engine();

  void initialize();
  void update();

private:
  int* data_;
  bool initialized_;
};
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | `PascalCase` | `Engine`, `Renderer` |
| Structs | `PascalCase` | `Vector3`, `Matrix4` |
| Functions | `camelBack` | `initialize()`, `update()` |
| Variables | `camelBack` | `data_`, `count` |
| Member variables | `camelBack` with trailing underscore | `data_`, `count_` |
| Constants | `UPPER_CASE` | `MAX_SIZE`, `DEFAULT_VALUE` |
| Enum values | `UPPER_CASE` | `STATUS_OK`, `STATUS_ERROR` |
| Macros | `UPPER_CASE` | `LOG_ERROR()`, `MAX_RETRIES` |

### Include Guards and Order

Use `#pragma once` for header files. Organize includes in this order:

1. Associated header
2. Standard library headers
3. Third-party library headers
4. Project headers

```cpp
// engine.hpp
#pragma once

#include <memory>
#include <string>
#include <vector>

#include <vulkan/vulkan.h>

#include "renderer.hpp"
#include "resource_manager.hpp"
```

### Type Usage

- Use `auto` when type is obvious from context
- Use `std::` types instead of C types
- Use `nullptr` instead of `NULL`
- Use `std::uint32_t` etc. for fixed-width integers

```cpp
// Use auto for obvious types
auto result = calculate_value();

// Use std:: types
std::string name = "engine";
std::vector<int> values = {1, 2, 3};

// Use nullptr
int* ptr = nullptr;

// Use fixed-width types
std::uint32_t count = 10;
```

### Const Correctness

- Use `const` for variables that don't change
- Use `const` references for function parameters that won't be modified
- Use `const` member functions that don't modify object state

```cpp
class Engine
{
public:
  void process(const std::string& input) const;
  
private:
  const int max_size_;
};
```

### Exception Handling

- Use exceptions for error conditions
- Catch specific exception types
- Provide meaningful error messages

```cpp
try
{
  initialize_engine();
}
catch (const std::runtime_error& e)
{
  log_error("Failed to initialize engine: " + std::string(e.what()));
  throw;
}
```

### Documentation

Use Doxygen-style comments for public APIs.

```cpp
/**
 * @brief Initialize the graphics engine.
 *
 * This method sets up the graphics pipeline and prepares
 * the engine for rendering.
 *
 * @throws std::runtime_error if initialization fails.
 */
void initialize();
```

---

## Cross-Cutting Standards

### File Naming Conventions

| File Type | Convention | Example |
|-----------|-----------|---------|
| Python modules | `snake_case.py` | `build_manager.py` |
| Python packages | `snake_case` | `omni_scripts/` |
| C++ headers | `PascalCase.hpp` | `Engine.hpp` |
| C++ sources | `PascalCase.cpp` | `Engine.cpp` |
| CMake files | `PascalCase.cmake` | `ProjectConfig.cmake` |
| Nix files | `kebab-case.nix` | `dev-shell.nix` |
| JSON files | `snake_case.json` | `build.json` |
| Markdown files | `kebab-case.md` | `user-guide.md` |

### Directory Structure

Follow this directory structure for consistency:

```
project_root/
├── .specs/                 # Specifications and standards
├── cmake/                  # CMake modules and toolchains
├── config/                 # Configuration files
├── conan/                  # Conan package manager files
├── docs/                   # Documentation
├── examples/               # Example code
├── include/                # Public headers
│   └── engine/            # Engine headers
├── nix/                    # Nix modules
├── scripts/                # Utility scripts
├── src/                    # Source files
│   ├── engine/            # Engine sources
│   └── game/              # Game sources
├── tests/                  # Test files
└── third_party/            # Third-party dependencies
```

### Documentation Requirements

All code must include:

1. **Module docstrings** (Python) or file header comments (C/C++)
2. **Function/method docstrings** with Args, Returns, Raises sections
3. **Inline comments** explaining non-obvious logic
4. **README files** for major components
5. **API documentation** for public interfaces

### Git Commit Message Format

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(build): add Linux compiler detection

Add support for detecting GCC and Clang compilers on Linux
platforms. Includes validation for C++23 support.

Closes #123
```

```
fix(controller): resolve MinGW path corruption

Fix issue where MinGW terminal setup corrupted PATH
environment variables. Use absolute paths for Python
executable to avoid PATH issues.

Fixes #456
```

---

## Linux-Specific Considerations

### POSIX Compliance

- Use POSIX-compliant system calls and APIs
- Avoid platform-specific code where possible
- Use `pathlib` for path operations (Python) or `std::filesystem` (C++)
- Handle file permissions and ownership appropriately

```python
from pathlib import Path

# Use pathlib for cross-platform path handling
config_path = Path.home() / ".config" / "omnicpp" / "config.json"
```

### Shebang Conventions

For executable Python scripts:

```python
#!/usr/bin/env python3
"""
Module docstring.
"""

from __future__ import annotations
```

For executable shell scripts:

```bash
#!/usr/bin/env bash
# Script description
set -euo pipefail
```

### Path Handling

- Always use forward slashes (`/`) in paths
- Use `pathlib.Path` (Python) or `std::filesystem` (C++) for path operations
- Avoid hardcoding paths; use environment variables or configuration
- Handle both absolute and relative paths correctly

```python
from pathlib import Path

# Correct: Use pathlib
project_root = Path(__file__).parent.resolve()
config_file = project_root / "config" / "settings.json"

# Incorrect: Hardcoded paths
config_file = "/home/user/project/config/settings.json"
```

### Environment Variable Usage

- Use environment variables for configuration
- Provide sensible defaults
- Document required environment variables
- Handle missing environment variables gracefully

```python
import os
from pathlib import Path

# Use environment variables with defaults
build_dir = Path(os.getenv("OMNICPP_BUILD_DIR", "build"))
cache_dir = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")) / "omnicpp"

# Validate environment variables
def get_required_env(name: str) -> str:
    """Get required environment variable.

    Args:
        name: Environment variable name.

    Returns:
        Environment variable value.

    Raises:
        ValueError: If environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Required environment variable {name} is not set")
    return value
```

### File Permissions

- Set appropriate file permissions for executables
- Use `chmod +x` for scripts that should be executable
- Consider security implications of file permissions

```python
import os
import stat

# Make script executable
script_path = Path("scripts/build.sh")
script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
```

### Signal Handling

For long-running processes, handle signals appropriately:

```python
import signal
import sys

def signal_handler(signum: int, frame) -> None:
    """Handle termination signals gracefully.

    Args:
        signum: Signal number.
        frame: Current stack frame.
    """
    print(f"Received signal {signum}, shutting down...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

### Process Management

- Use subprocess for external commands
- Handle process exit codes properly
- Provide meaningful error messages for command failures

```python
import subprocess
from pathlib import Path

def run_command(
    command: list[str],
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """Run a command in a subprocess.

    Args:
        command: Command and arguments to execute.
        cwd: Working directory for the command.
        check: Whether to raise exception on non-zero exit.

    Returns:
        CompletedProcess object with result.

    Raises:
        subprocess.CalledProcessError: If command fails and check=True.
    """
    result = subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )
    return result
```

### Logging on Linux

Use appropriate log levels and facilities:

```python
import logging
import sys

# Configure logging for Linux
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/var/log/omnicpp/build.log"),
    ],
)
```

---

## Code Review Checklist

### General

- [ ] Code follows project coding standards
- [ ] Code is readable and self-documenting
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No TODO/FIXME comments without associated issues

### Python

- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Imports are properly organized
- [ ] No unused imports
- [ ] Error handling is appropriate
- [ ] Logging is used instead of print
- [ ] Constants are defined at module level

### Nix

- [ ] Nix formatting is consistent
- [ ] Dependencies are properly declared
- [ ] Shell hooks are documented
- [ ] Build inputs are minimal and necessary

### CMake

- [ ] CMake formatting follows project style
- [ ] Modern CMake practices are used
- [ ] Target-based commands are preferred
- [ ] Cache variables are UPPER_CASE
- [ ] Options are properly documented

### C/C++

- [ ] Code compiles without warnings
- [ ] clang-tidy checks pass
- [ ] cppcheck checks pass
- [ ] Const correctness is maintained
- [ ] Smart pointers are used appropriately
- [ ] Memory leaks are avoided

### Testing

- [ ] Unit tests are included
- [ ] Tests cover edge cases
- [ ] Tests are documented
- [ ] Tests pass locally

### Documentation

- [ ] README is updated if needed
- [ ] API documentation is updated
- [ ] Changes are documented in CHANGELOG
- [ ] New features are documented in user guide

### Linux-Specific

- [ ] POSIX compliance is maintained
- [ ] File paths use forward slashes
- [ ] Environment variables are documented
- [ ] Signal handling is appropriate
- [ ] File permissions are correct

---

## Enforcement

### Pre-Commit Hooks

All code must pass pre-commit hooks before committing:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit manually
pre-commit run --all-files
```

### CI/CD

CI/CD pipelines will enforce:

- Code formatting (Black, clang-format, cmake-format)
- Linting (Pylint, clang-tidy, cppcheck)
- Type checking (MyPy)
- Testing (pytest)

### Violations

- Minor violations: Fix before next commit
- Major violations: Block PR until resolved
- Repeated violations: Escalate to team lead

---

## Appendix: Tool Configuration Reference

### Python Tools

**Black (`.pyproject.toml`):**
```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

**isort (`.pyproject.toml`):**
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
```

**MyPy (`.pyproject.toml`):**
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true
strict = true
```

### C/C++ Tools

**clang-format (`.clang-format`):**
- BasedOnStyle: GNU
- ColumnLimit: 100
- IndentWidth: 2
- PointerAlignment: Left

**clang-tidy (`.clang-tidy`):**
- WarningsAsErrors: "*"
- HeaderFilterRegex: "src/.*|include/.*"

### CMake Tools

**cmake-format (`.cmake-format`):**
```yaml
format:
  tab_size: 4
  line_width: 100
  line_ending: unix
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-27 | Initial version for Linux support expansion |

---

**End of Document**
