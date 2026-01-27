# OmniCPP Coding Standards

**Version:** 1.0.0
**Last Updated:** 2026-01-07
**Status:** Active

---

## Table of Contents

1. [Overview](#overview)
2. [C++23 Standards](#c23-standards)
3. [Python Standards](#python-standards)
4. [CMake 4 Standards](#cmake-4-standards)
5. [Naming Conventions](#naming-conventions)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Logging Standards](#logging-standards)
8. [Cross-Platform Guidelines](#cross-platform-guidelines)
9. [Package Manager Integration](#package-manager-integration)
10. [Testing Standards](#testing-standards)
11. [Code Quality Enforcement](#code-quality-enforcement)

---

## Overview

This document establishes the coding standards for the OmniCPP template project, a C++23 game engine and game powered by Qt6 and Vulkan. These standards ensure code quality, maintainability, and consistency across the entire codebase.

### Project Characteristics

- **Language:** C++23 (NO modules - not fully implemented)
- **Python Version:** 3.11+
- **Build System:** CMake 4.0+
- **Package Managers:** Conan, vcpkg, CPM.cmake
- **Platforms:** Windows, Linux, WASM
- **Compilers:** MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang
- **Graphics:** Vulkan, OpenGL
- **Frameworks:** Qt6 (optional)

### Core Principles

1. **Zero Pylance Errors:** All Python code must pass strict type checking
2. **Modular Architecture:** Clear separation of concerns with well-defined interfaces
3. **Cross-Platform Compatibility:** Code must work on all supported platforms
4. **Defensive Programming:** Validate inputs, handle errors gracefully
5. **Performance Awareness:** Optimize critical paths without premature optimization
6. **Documentation:** Self-documenting code with clear comments where necessary

---

## C++23 Standards

### Language Standard

- **Standard:** C++23 (ISO/IEC 14882:2023)
- **Modules:** **NOT ALLOWED** - Use traditional header/source files
- **Compiler Flags:** `-std=c++23` (or `/std:c++23` for MSVC)

### File Organization

#### Header Files (`.hpp`)

```cpp
// File: include/engine/core/engine.hpp
#pragma once

// 1. Standard library includes (alphabetical)
#include <memory>
#include <string>
#include <vector>

// 2. Third-party includes (alphabetical)
#include <spdlog/spdlog.h>
#include <vulkan/vulkan.h>

// 3. Project includes (relative to include/)
#include "engine/graphics/renderer.hpp"
#include "engine/logging/logger.hpp"

// 4. Forward declarations
namespace engine {
    class Renderer;
    class ResourceManager;
}

// 5. Class/Interface definition
class Engine {
public:
    // Public interface
private:
    // Private implementation
};
```

#### Source Files (`.cpp`)

```cpp
// File: src/engine/core/engine.cpp
#include "engine/core/engine.hpp"

// Implementation follows header order
```

### Formatting Rules

- **Style:** GNU (as defined in [`.clang-format`](../../.clang-format))
- **Indentation:** 2 spaces (NO tabs)
- **Line Length:** 100 characters maximum
- **Brace Style:** Allman (opening brace on new line)
- **Pointer Alignment:** Left (`Type* ptr` not `Type *ptr`)
- **Reference Alignment:** Same as pointers (`Type& ref`)

### Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Classes | `CamelCase` | `class EngineManager` |
| Structs | `CamelCase` | `struct VertexData` |
| Functions | `camelBack` | `void initializeEngine()` |
| Variables | `camelBack` | `int frameCount` |
| Member Variables | `camelBack` (no prefix) | `int currentFrame` |
| Constants | `UPPER_CASE` | `const int MAX_ENTITIES = 1000` |
| Enum Classes | `CamelCase` | `enum class RenderMode` |
| Enum Values | `UPPER_CASE` | `RenderMode::DEFERRED` |
| Namespaces | `lower_case` | `namespace engine { }` |
| Macros | `UPPER_CASE` | `#define OMNICPP_VERSION` |
| Template Parameters | `CamelCase` | `template<typename T>` |

### Modern C++23 Best Practices

#### Use `auto` Judiciously

```cpp
// GOOD: Type is obvious from context
auto entity = createEntity();
auto it = entities.begin();

// GOOD: Complex types
auto result = std::make_unique<ResourceManager>();

// BAD: Type is not obvious
auto value = calculate();  // What type is value?

// GOOD: Explicit type when clarity is needed
std::vector<Entity> entities;
```

#### Use `nullptr` Instead of `NULL`

```cpp
// GOOD
Renderer* renderer = nullptr;

// BAD
Renderer* renderer = NULL;
```

#### Use `override` and `final`

```cpp
class Renderer : public IRenderer {
public:
    void render() override;  // Explicitly marked override
    void update() final;     // Cannot be overridden further
};
```

#### Use `[[nodiscard]]` for Return Values

```cpp
[[nodiscard]] bool initialize();  // Caller must check return value
[[nodiscard]] std::unique_ptr<Renderer> createRenderer();
```

#### Use `[[maybe_unused]]` to Suppress Warnings

```cpp
void processEvent([[maybe_unused]] Event& event) {
    // Implementation may not use event
}
```

#### Use `std::unique_ptr` and `std::shared_ptr`

```cpp
// GOOD: Unique ownership
auto renderer = std::make_unique<VulkanRenderer>();

// GOOD: Shared ownership
auto texture = std::make_shared<Texture>(width, height);

// BAD: Raw pointers for ownership
Renderer* renderer = new VulkanRenderer();  // Memory leak risk
```

#### Use `std::span` for Array Views

```cpp
void processVertices(std::span<const Vertex> vertices) {
    for (const auto& vertex : vertices) {
        // Process vertex
    }
}
```

#### Use `std::string_view` for Read-Only Strings

```cpp
void logMessage(std::string_view message) {
    // No string allocation for string literals
    spdlog::info("{}", message);
}
```

#### Use `std::expected` for Error Handling (C++23)

```cpp
std::expected<Renderer, Error> createRenderer() {
    if (!vulkanAvailable) {
        return std::unexpected(Error::VulkanNotAvailable);
    }
    return VulkanRenderer{};
}
```

#### Use `std::optional` for Optional Values

```cpp
std::optional<Texture> loadTexture(const std::string& path) {
    if (!fileExists(path)) {
        return std::nullopt;
    }
    return Texture{path};
}
```

#### Use Concepts for Template Constraints

```cpp
template<typename T>
concept Renderable = requires(T t) {
    { t.render() } -> std::same_as<void>;
};

void renderAll(std::span<Renderable auto> objects) {
    for (auto& obj : objects) {
        obj.render();
    }
}
```

### Memory Management

#### RAII (Resource Acquisition Is Initialization)

```cpp
class VulkanBuffer {
public:
    VulkanBuffer(VkDevice device, VkDeviceSize size);
    ~VulkanBuffer() {
        vkDestroyBuffer(device_, buffer_, nullptr);
    }

    // Delete copy operations
    VulkanBuffer(const VulkanBuffer&) = delete;
    VulkanBuffer& operator=(const VulkanBuffer&) = delete;

    // Allow move operations
    VulkanBuffer(VulkanBuffer&& other) noexcept;
    VulkanBuffer& operator=(VulkanBuffer&& other) noexcept;

private:
    VkDevice device_;
    VkBuffer buffer_;
};
```

#### Smart Pointer Guidelines

```cpp
// Use unique_ptr for exclusive ownership
class ResourceManager {
private:
    std::unordered_map<std::string, std::unique_ptr<Resource>> resources_;
};

// Use shared_ptr for shared ownership
class TextureCache {
private:
    std::unordered_map<std::string, std::shared_ptr<Texture>> cache_;
};

// Use weak_ptr to break cycles
class Entity {
private:
    std::weak_ptr<Entity> parent_;  // Avoid circular reference
};
```

### Const Correctness

```cpp
// GOOD: Const member functions
class Vector3 {
public:
    float length() const { return std::sqrt(x*x + y*y + z*z); }

    // GOOD: Const references for parameters
    void add(const Vector3& other);

    // GOOD: Const return values
    const std::string& getName() const { return name_; }
};

// GOOD: Const iterators
for (const auto& entity : entities) {
    entity.update();
}
```

### Exception Safety

```cpp
// Provide strong exception guarantee
class ResourceManager {
public:
    void loadResource(const std::string& path) {
        auto temp = std::make_unique<Resource>(path);  // May throw
        resources_[path] = std::move(temp);  // No-throw
    }
};
```

### Performance Guidelines

#### Move Semantics

```cpp
// GOOD: Pass by value and move
void addTexture(Texture texture) {
    textures_.push_back(std::move(texture));
}

// GOOD: Return by value (RVO/move)
Texture createTexture() {
    return Texture{width, height};
}
```

#### Avoid Unnecessary Copies

```cpp
// GOOD: Use references for large objects
void processMesh(const Mesh& mesh);

// GOOD: Use string_view for read-only strings
bool isValidName(std::string_view name);
```

#### Reserve Container Capacity

```cpp
// GOOD: Reserve when size is known
std::vector<Entity> entities;
entities.reserve(1000);  // Avoid reallocations
```

### Thread Safety

```cpp
// Use std::mutex for mutual exclusion
class ThreadPool {
private:
    std::mutex queue_mutex_;
    std::queue<Task> tasks_;

public:
    void addTask(Task task) {
        std::lock_guard<std::mutex> lock(queue_mutex_);
        tasks_.push(std::move(task));
    }
};

// Use std::atomic for simple types
class FrameCounter {
private:
    std::atomic<int> frame_count_{0};

public:
    void increment() { frame_count_++; }
    int get() const { return frame_count_; }
};
```

### Documentation

```cpp
/**
 * @brief Initializes the Vulkan renderer with the specified window.
 *
 * This function sets up the Vulkan instance, physical device selection,
 * logical device creation, and swapchain initialization.
 *
 * @param window The window to render to
 * @return true if initialization succeeded, false otherwise
 * @throws VulkanInitializationException if Vulkan setup fails
 *
 * @note This function must be called before any rendering operations
 * @see shutdown()
 */
bool initializeRenderer(Window& window);
```

---

## Python Standards

### Language Version

- **Minimum Version:** Python 3.11
- **Target Version:** Python 3.11+
- **Type Checking:** Strict mode (mypy)

### File Organization

#### Module Structure

```python
"""
Module docstring describing the purpose of this module.

This module provides functionality for X, Y, and Z operations.
"""

# 1. Standard library imports (alphabetical)
import argparse
import logging
from pathlib import Path
from typing import Optional

# 2. Third-party imports (alphabetical)
import numpy as np
from pydantic import BaseModel

# 3. Local imports (relative)
from .config import load_config
from .exceptions import ControllerError

# 4. Module-level constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0

# 5. Class and function definitions
class MyClass:
    """Class docstring."""
    pass
```

### Formatting Rules

- **Formatter:** Black (as defined in [`pyproject.toml`](../../pyproject.toml))
- **Line Length:** 100 characters maximum
- **Indentation:** 4 spaces
- **Quotes:** Double quotes for strings, single quotes for dict keys
- **Import Sorting:** isort with black profile

### Type Hints

**MANDATORY:** All functions must have complete type hints.

```python
# GOOD: Complete type hints
def process_data(
    data: list[dict[str, Any]],
    config: Config,
    *,
    verbose: bool = False
) -> dict[str, Any]:
    """Process the input data with the given configuration."""
    result: dict[str, Any] = {}
    for item in data:
        result[item["id"]] = item["value"]
    return result

# BAD: Missing type hints
def process_data(data, config, verbose=False):
    result = {}
    for item in data:
        result[item["id"]] = item["value"]
    return result
```

### Type Hint Best Practices

```python
from typing import Optional, Union, Callable, TypeAlias
from collections.abc import Sequence, Mapping

# Use TypeAlias for complex types
Vector3D: TypeAlias = tuple[float, float, float]
EntityId: TypeAlias = int

# Use Optional for nullable values
def find_entity(entity_id: EntityId) -> Optional[Entity]:
    """Find an entity by ID, returning None if not found."""
    return entities.get(entity_id)

# Use Union for multiple types
def process_value(value: Union[int, float, str]) -> str:
    """Process a value that can be int, float, or str."""
    return str(value)

# Use Callable for function parameters
def execute_callback(callback: Callable[[int], None], value: int) -> None:
    """Execute the callback with the given value."""
    callback(value)

# Use Sequence for generic sequences
def sum_values(values: Sequence[float]) -> float:
    """Sum all values in the sequence."""
    return sum(values)

# Use Mapping for generic mappings
def get_config(config: Mapping[str, Any], key: str) -> Any:
    """Get a configuration value by key."""
    return config.get(key)
```

### Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Classes | `CamelCase` | `class BuildController` |
| Functions | `snake_case` | `def build_target()` |
| Variables | `snake_case` | `frame_count = 0` |
| Constants | `UPPER_CASE` | `MAX_RETRIES = 3` |
| Modules | `snake_case` | `build_controller.py` |
| Packages | `snake_case` | `omni_scripts/` |
| Private Members | `_leading_underscore` | `def _internal_method()` |
| Protected Members | `_leading_underscore` | `def _protected_method()` |

### PEP 8 Compliance

All Python code must comply with PEP 8 standards:

```python
# GOOD: Proper spacing around operators
result = a + b * c

# GOOD: Proper spacing after commas
items = [1, 2, 3, 4, 5]

# GOOD: Proper spacing in function definitions
def function_name(param1: int, param2: str) -> bool:
    return True

# GOOD: Blank lines between functions
def function_one():
    pass


def function_two():
    pass
```

### Docstrings

All public functions, classes, and modules must have docstrings following the Google style:

```python
def build_target(
    target: str,
    config: str,
    compiler: Optional[str] = None,
    *,
    verbose: bool = False
) -> int:
    """Build the specified target with the given configuration.

    This function orchestrates the build process for the target,
    including dependency resolution, compilation, and linking.

    Args:
        target: The target to build (e.g., 'engine', 'game').
        config: The build configuration ('debug' or 'release').
        compiler: Optional compiler to use. If None, uses default.
        verbose: Enable verbose output for debugging.

    Returns:
        Exit code (0 for success, non-zero for failure).

    Raises:
        InvalidTargetError: If the target is not valid.
        BuildError: If the build process fails.

    Example:
        >>> build_target('engine', 'debug', verbose=True)
        0
    """
    pass
```

### Error Handling

```python
# GOOD: Use custom exceptions
class ControllerError(Exception):
    """Base exception for controller errors."""

    def __init__(
        self,
        message: str,
        command: str,
        context: Optional[dict[str, Any]] = None,
        exit_code: int = 1
    ) -> None:
        self.message = message
        self.command = command
        self.context = context or {}
        self.exit_code = exit_code
        super().__init__(self.message)

# GOOD: Specific exception handling
try:
    result = build_target(target, config)
except InvalidTargetError as e:
    logger.error(f"Invalid target: {e.message}")
    return e.exit_code
except BuildError as e:
    logger.error(f"Build failed: {e.message}")
    return e.exit_code
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    return 1

# BAD: Bare except
try:
    result = build_target(target, config)
except:
    pass  # Never do this!
```

### Logging

```python
from omni_scripts.logging.logger import get_logger

logger = get_logger(__name__)

# GOOD: Use appropriate log levels
logger.debug("Detailed debugging information")
logger.info("General informational message")
logger.warning("Warning about potential issues")
logger.error("Error occurred but execution continues")
logger.critical("Critical error that may cause failure")

# GOOD: Use structured logging with extra context
logger.error(
    "Build failed",
    extra={
        "target": target,
        "config": config,
        "error": str(error)
    }
)

# GOOD: Log exceptions with traceback
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")
```

### Path Handling

```python
from pathlib import Path

# GOOD: Use pathlib.Path
project_root = Path(__file__).parent.parent
config_path = project_root / "config" / "build.json"

# GOOD: Check existence
if config_path.exists():
    config = load_config(config_path)

# GOOD: Create directories
logs_dir = project_root / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

# BAD: Use os.path
import os.path
config_path = os.path.join("config", "build.json")  # Don't do this
```

### Context Managers

```python
# GOOD: Use context managers for resource management
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# GOOD: Custom context managers
from contextlib import contextmanager

@contextmanager
def change_directory(path: Path):
    """Context manager for changing directory."""
    original = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original)
```

### Data Classes

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class BuildConfig:
    """Configuration for build operations."""

    target: str
    config: str
    compiler: Optional[str] = None
    verbose: bool = False

    # Class variable
    DEFAULT_CONFIG: ClassVar[str] = "debug"

    # Factory method
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BuildConfig":
        """Create BuildConfig from dictionary."""
        return cls(**data)
```

### Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict[str, Any]:
    """Fetch data from URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main() -> None:
    """Main async function."""
    data = await fetch_data("https://api.example.com/data")
    print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Zero Pylance Errors Requirement

**CRITICAL:** All Python code must pass strict type checking with zero Pylance errors.

```python
# GOOD: Properly typed
def process_items(items: list[int]) -> list[int]:
    """Process a list of integers."""
    return [item * 2 for item in items]

# BAD: Type error - Pylance will catch this
def process_items(items: list[int]) -> list[str]:
    """Process a list of integers."""
    return [item * 2 for item in items]  # Type mismatch!
```

### Modular Architecture

All Python scripts must be organized in the `omni_scripts/` directory with clear module boundaries:

```
omni_scripts/
├── __init__.py
├── build_system/
│   ├── __init__.py
│   ├── cmake.py
│   ├── conan.py
│   └── vcpkg.py
├── compilers/
│   ├── __init__.py
│   ├── base.py
│   ├── msvc.py
│   └── gcc.py
├── controller/
│   ├── __init__.py
│   ├── base.py
│   └── build_controller.py
└── logging/
    ├── __init__.py
    ├── logger.py
    └── config.py
```

### Terminal Invocation Patterns

Different compilers require different terminal invocation patterns:

```python
# MSVC (Developer Command Prompt)
def invoke_msvc(command: list[str]) -> int:
    """Invoke MSVC compiler in Developer Command Prompt."""
    # MSVC requires specific environment setup
    env = setup_msvc_environment()
    return subprocess.run(command, env=env).returncode

# MinGW-GCC
def invoke_mingw_gcc(command: list[str]) -> int:
    """Invoke MinGW-GCC compiler."""
    # MinGW-GCC can use standard environment
    return subprocess.run(command).returncode

# MinGW-Clang
def invoke_mingw_clang(command: list[str]) -> int:
    """Invoke MinGW-Clang compiler."""
    # MinGW-Clang requires specific environment
    env = setup_mingw_clang_environment()
    return subprocess.run(command, env=env).returncode
```

---

## CMake 4 Standards

### CMake Version

- **Minimum Version:** CMake 4.0
- **Target Version:** CMake 4.0+
- **Generator:** Ninja (preferred), Makefiles, or Visual Studio

### File Organization

```
cmake/
├── ProjectConfig.cmake          # Project-wide configuration
├── PlatformConfig.cmake         # Platform detection and setup
├── CompilerFlags.cmake          # Compiler-specific flags
├── FindDependencies.cmake      # Dependency management
├── CPM.cmake                   # CPM package manager
├── ConanIntegration.cmake      # Conan integration
├── VcpkgIntegration.cmake      # vcpkg integration
├── Testing.cmake                # Test configuration
├── Coverage.cmake               # Code coverage setup
├── FormatTargets.cmake         # Code formatting targets
├── LintTargets.cmake           # Code linting targets
├── InstallRules.cmake          # Installation rules
└── PackageConfig.cmake         # Packaging configuration
```

### Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Variables | `UPPER_CASE` | `set(CMAKE_CXX_STANDARD 23)` |
| Functions | `lower_case` | `function(setup_project)` |
| Macros | `UPPER_CASE` | `macro(add_custom_target)` |
| Targets | `lower_case` | `add_library(engine)` |
| Options | `UPPER_CASE` | `option(OMNICPP_BUILD_ENGINE)` |
| Cache Variables | `UPPER_CASE` | `set(OMNICPP_VERSION "1.0.0" CACHE STRING)` |

### Project Configuration

```cmake
# GOOD: Clear project setup
cmake_minimum_required(VERSION 4.0)
project(OmniCppTemplate
    VERSION 1.0.0
    DESCRIPTION "OmniCpp Template Project"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
```

### Target Configuration

```cmake
# GOOD: Modern target-based approach
add_library(engine
    src/engine/core/engine.cpp
    src/engine/graphics/renderer.cpp
)

target_include_directories(engine
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(engine
    PUBLIC
        cxx_std_23
)

target_link_libraries(engine
    PUBLIC
        Vulkan::Vulkan
        spdlog::spdlog
)

# Set target properties
set_target_properties(engine PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    OUTPUT_NAME "omnicpp_engine"
    POSITION_INDEPENDENT_CODE ON
)
```

### Compiler Flags

```cmake
# GOOD: Platform-specific flags
if(MSVC)
    target_compile_options(engine PRIVATE
        /W4          # Warning level 4
        /WX          # Treat warnings as errors
        /permissive- # Disable non-standard extensions
        /Zc:__cplusplus # Enable correct __cplusplus macro
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(engine PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Werror
        -Wno-unused-parameter
    )
endif()
```

### Package Manager Integration

#### CPM.cmake

```cmake
# GOOD: Use CPM for header-only libraries
CPMAddPackage(
    NAME spdlog
    VERSION 1.12.0
    GITHUB_REPOSITORY gabime/spdlog
    OPTIONS
        SPDLOG_BUILD_SHARED OFF
        SPDLOG_BUILD_EXAMPLE OFF
)

# Link to CPM package
target_link_libraries(engine PRIVATE spdlog::spdlog)
```

#### Conan

```cmake
# GOOD: Conan integration
if(OMNICPP_USE_CONAN)
    include(cmake/ConanIntegration.cmake)

    conan_cmake_install(
        PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}
        BUILD missing
        SETTINGS build_type=${CMAKE_BUILD_TYPE}
    )
endif()
```

#### vcpkg

```cmake
# GOOD: vcpkg integration
if(OMNICPP_USE_VCPKG)
    include(cmake/VcpkgIntegration.cmake)

    find_package(Vulkan REQUIRED)
    find_package(spdlog REQUIRED)
endif()
```

### Conditional Compilation

```cmake
# GOOD: Use feature-based options
option(OMNICPP_USE_VULKAN "Use Vulkan graphics API" ON)
option(OMNICPP_USE_OPENGL "Use OpenGL graphics API" OFF)
option(OMNICPP_USE_QT6 "Use Qt6 framework" OFF)

if(OMNICPP_USE_VULKAN)
    find_package(Vulkan REQUIRED)
    target_compile_definitions(engine PUBLIC OMNICPP_USE_VULKAN)
    target_link_libraries(engine PUBLIC Vulkan::Vulkan)
endif()
```

### Testing Configuration

```cmake
# GOOD: Enable testing
enable_testing()

# Add test executable
add_executable(engine_tests
    tests/engine/test_engine.cpp
    tests/engine/test_renderer.cpp
)

target_link_libraries(engine_tests
    PRIVATE
        engine
        GTest::gtest
        GTest::gtest_main
)

# Register tests
include(GoogleTest)
gtest_discover_tests(engine_tests)
```

### Installation Rules

```cmake
# GOOD: Proper installation
install(TARGETS engine
    EXPORT OmniCppTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.hpp"
)

install(EXPORT OmniCppTargets
    FILE OmniCppTargets.cmake
    NAMESPACE OmniCpp::
    DESTINATION lib/cmake/OmniCpp
)
```

### CMake Presets

```json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "default",
      "displayName": "Default Config",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_STANDARD": "23"
      }
    }
  ]
}
```

### Formatting

- **Formatter:** cmake-format (as defined in [`.cmake-format`](../../.cmake-format))
- **Tab Size:** 4 spaces
- **Line Width:** 100 characters maximum

---

## Naming Conventions

### C++ Naming

| Entity | Convention | Example |
|--------|------------|---------|
| Classes | `CamelCase` | `class EngineManager` |
| Structs | `CamelCase` | `struct VertexData` |
| Functions | `camelBack` | `void initializeEngine()` |
| Variables | `camelBack` | `int frameCount` |
| Member Variables | `camelBack` (no prefix) | `int currentFrame` |
| Constants | `UPPER_CASE` | `const int MAX_ENTITIES = 1000` |
| Enum Classes | `CamelCase` | `enum class RenderMode` |
| Enum Values | `UPPER_CASE` | `RenderMode::DEFERRED` |
| Namespaces | `lower_case` | `namespace engine { }` |
| Macros | `UPPER_CASE` | `#define OMNICPP_VERSION` |
| Template Parameters | `CamelCase` | `template<typename T>` |
| Files | `snake_case.hpp/.cpp` | `engine_manager.hpp` |

### Python Naming

| Entity | Convention | Example |
|--------|------------|---------|
| Classes | `CamelCase` | `class BuildController` |
| Functions | `snake_case` | `def build_target()` |
| Variables | `snake_case` | `frame_count = 0` |
| Constants | `UPPER_CASE` | `MAX_RETRIES = 3` |
| Modules | `snake_case` | `build_controller.py` |
| Packages | `snake_case` | `omni_scripts/` |
| Private Members | `_leading_underscore` | `def _internal_method()` |
| Protected Members | `_leading_underscore` | `def _protected_method()` |
| Type Aliases | `CamelCase` | `Vector3D: TypeAlias = ...` |

### CMake Naming

| Entity | Convention | Example |
|--------|------------|---------|
| Variables | `UPPER_CASE` | `set(CMAKE_CXX_STANDARD 23)` |
| Functions | `lower_case` | `function(setup_project)` |
| Macros | `UPPER_CASE` | `macro(add_custom_target)` |
| Targets | `lower_case` | `add_library(engine)` |
| Options | `UPPER_CASE` | `option(OMNICPP_BUILD_ENGINE)` |
| Cache Variables | `UPPER_CASE` | `set(OMNICPP_VERSION "1.0.0" CACHE STRING)` |
| Files | `lower_case.cmake` | `project_config.cmake` |

### File Naming

#### C++ Files

```
include/
├── engine/
│   ├── core/
│   │   └── engine.hpp
│   ├── graphics/
│   │   └── renderer.hpp
│   └── logging/
│       └── logger.hpp
src/
└── engine/
    ├── core/
    │   └── engine.cpp
    ├── graphics/
    │   └── renderer.cpp
    └── logging/
        └── logger.cpp
```

#### Python Files

```
omni_scripts/
├── build_system/
│   ├── __init__.py
│   ├── cmake.py
│   └── conan.py
├── compilers/
│   ├── __init__.py
│   ├── base.py
│   └── msvc.py
└── controller/
    ├── __init__.py
    └── build_controller.py
```

#### CMake Files

```
cmake/
├── ProjectConfig.cmake
├── PlatformConfig.cmake
├── CompilerFlags.cmake
└── FindDependencies.cmake
```

---

## Error Handling Patterns

### C++ Error Handling

#### Use Exceptions for Error Conditions

```cpp
// GOOD: Use exceptions for error conditions
class VulkanInitializationException : public std::runtime_error {
public:
    VulkanInitializationException(const std::string& message)
        : std::runtime_error(message) {}
};

bool initializeVulkan() {
    if (!vulkanAvailable) {
        throw VulkanInitializationException("Vulkan not available");
    }
    return true;
}
```

#### Use `std::expected` for Expected Failures (C++23)

```cpp
// GOOD: Use std::expected for operations that may fail
std::expected<Renderer, Error> createRenderer() {
    if (!vulkanAvailable) {
        return std::unexpected(Error::VulkanNotAvailable);
    }
    return VulkanRenderer{};
}

// Usage
auto renderer = createRenderer();
if (!renderer) {
    std::cerr << "Error: " << renderer.error().message() << std::endl;
    return;
}
renderer->render();
```

#### Use `std::optional` for Optional Values

```cpp
// GOOD: Use std::optional for optional return values
std::optional<Texture> loadTexture(const std::string& path) {
    if (!fileExists(path)) {
        return std::nullopt;
    }
    return Texture{path};
}

// Usage
auto texture = loadTexture("texture.png");
if (texture) {
    texture->bind();
}
```

#### RAII for Resource Management

```cpp
// GOOD: RAII ensures cleanup
class VulkanBuffer {
public:
    VulkanBuffer(VkDevice device, VkDeviceSize size)
        : device_(device) {
        VkBufferCreateInfo createInfo{};
        // ... setup createInfo
        vkCreateBuffer(device_, &createInfo, nullptr, &buffer_);
    }

    ~VulkanBuffer() {
        vkDestroyBuffer(device_, buffer_, nullptr);
    }

    // Delete copy operations
    VulkanBuffer(const VulkanBuffer&) = delete;
    VulkanBuffer& operator=(const VulkanBuffer&) = delete;

    // Allow move operations
    VulkanBuffer(VulkanBuffer&& other) noexcept
        : device_(other.device_), buffer_(other.buffer_) {
        other.buffer_ = VK_NULL_HANDLE;
    }

    VulkanBuffer& operator=(VulkanBuffer&& other) noexcept {
        if (this != &other) {
            vkDestroyBuffer(device_, buffer_, nullptr);
            device_ = other.device_;
            buffer_ = other.buffer_;
            other.buffer_ = VK_NULL_HANDLE;
        }
        return *this;
    }

private:
    VkDevice device_;
    VkBuffer buffer_;
};
```

### Python Error Handling

#### Use Custom Exceptions

```python
# GOOD: Define custom exceptions
class ControllerError(Exception):
    """Base exception for controller errors."""

    def __init__(
        self,
        message: str,
        command: str,
        context: Optional[dict[str, Any]] = None,
        exit_code: int = 1
    ) -> None:
        self.message = message
        self.command = command
        self.context = context or {}
        self.exit_code = exit_code
        super().__init__(self.message)


class InvalidTargetError(ControllerError):
    """Exception raised when an invalid target is specified."""

    def __init__(
        self,
        message: str,
        command: str,
        target: str,
        valid_targets: list[str]
    ) -> None:
        super().__init__(
            message=message,
            command=command,
            context={"target": target, "valid_targets": valid_targets},
            exit_code=2
        )
```

#### Specific Exception Handling

```python
# GOOD: Handle specific exceptions
try:
    result = build_target(target, config)
except InvalidTargetError as e:
    logger.error(f"Invalid target: {e.message}")
    return e.exit_code
except BuildError as e:
    logger.error(f"Build failed: {e.message}")
    return e.exit_code
except FileNotFoundError as e:
    logger.error(f"File not found: {e.filename}")
    return 3
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    return 1
```

#### Use Context Managers for Resource Management

```python
# GOOD: Use context managers
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    """Create a temporary directory and clean it up."""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Usage
with temporary_directory() as temp_dir:
    # Use temp_dir
    pass
# Automatically cleaned up
```

#### Validate Inputs Early

```python
# GOOD: Validate inputs early
def build_target(
    target: str,
    config: str,
    compiler: Optional[str] = None
) -> int:
    """Build the specified target."""
    # Validate target
    if target not in VALID_TARGETS:
        raise InvalidTargetError(
            message=f"Invalid target '{target}'",
            command="build",
            target=target,
            valid_targets=VALID_TARGETS
        )

    # Validate config
    if config.lower() not in VALID_CONFIGS:
        raise ControllerError(
            message=f"Invalid configuration '{config}'",
            command="build",
            context={"config": config, "valid_configs": VALID_CONFIGS},
            exit_code=2
        )

    # Proceed with build
    return execute_build(target, config, compiler)
```

### CMake Error Handling

```cmake
# GOOD: Use find_package with REQUIRED
find_package(Vulkan REQUIRED)
find_package(spdlog REQUIRED)

# GOOD: Check for required features
if(NOT CMAKE_CXX_STANDARD_COMPILES)
    message(FATAL_ERROR "C++23 is not supported by this compiler")
endif()

# GOOD: Provide helpful error messages
if(OMNICPP_USE_QT6 AND NOT Qt6_FOUND)
    message(FATAL_ERROR
        "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
        "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6."
    )
endif()
```

---

## Logging Standards

### C++ Logging (spdlog)

#### Configuration

```cpp
// Load logging configuration from JSON
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>

void setupLogging() {
    // Create console sink
    auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    console_sink->set_level(spdlog::level::info);
    console_sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] %v");

    // Create file sink
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(
        "logs/omnicpp_engine.log", true
    );
    file_sink->set_level(spdlog::level::debug);
    file_sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] [%t] %v");

    // Create logger with multiple sinks
    std::vector<spdlog::sink_ptr> sinks = {console_sink, file_sink};
    auto logger = std::make_shared<spdlog::logger>(
        "omnicpp", sinks.begin(), sinks.end()
    );

    // Set default logger
    spdlog::set_default_logger(logger);
    spdlog::set_level(spdlog::level::debug);
}
```

#### Logging Levels

```cpp
// DEBUG: Detailed debugging information
spdlog::debug("Initializing Vulkan instance with {} extensions", extensions.size());

// INFO: General informational messages
spdlog::info("Engine initialized successfully");

// WARNING: Warning about potential issues
spdlog::warn("Texture not found: {}, using default", texture_path);

// ERROR: Error occurred but execution continues
spdlog::error("Failed to load shader: {}", shader_path);

// CRITICAL: Critical error that may cause failure
spdlog::critical("Vulkan initialization failed, cannot continue");
```

#### Structured Logging

```cpp
// GOOD: Use structured logging with key-value pairs
spdlog::info("Build started",
    "target"_a = target,
    "config"_a = config,
    "compiler"_a = compiler
);

// GOOD: Log errors with context
spdlog::error("Shader compilation failed",
    "shader"_a = shader_path,
    "error"_a = error_message,
    "line"_a = error_line
);
```

#### Performance Logging

```cpp
// GOOD: Log performance metrics
#include <chrono>

auto start = std::chrono::high_resolution_clock::now();

// ... perform operation ...

auto end = std::chrono::high_resolution_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
spdlog::info("Operation completed in {} ms", duration.count());
```

### Python Logging

#### Configuration

```python
# Load logging configuration from JSON
import logging
import json
from pathlib import Path

def setup_logging(config_path: Path = Path("config/logging_python.json")) -> None:
    """Set up logging with the specified configuration."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config["level"]))

    # Clear existing handlers
    logger.handlers.clear()

    # Create console handler
    if config["console_handler_enabled"]:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config["level"]))
        console_handler.setFormatter(logging.Formatter(
            fmt=config["format"],
            datefmt=config["datefmt"]
        ))
        logger.addHandler(console_handler)

    # Create file handler
    if config["file_handler_enabled"]:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            config["file_path"],
            maxBytes=config["max_bytes"],
            backupCount=config["backup_count"]
        )
        file_handler.setLevel(getattr(logging, config["level"]))
        file_handler.setFormatter(logging.Formatter(
            fmt=config["format"],
            datefmt=config["datefmt"]
        ))
        logger.addHandler(file_handler)
```

#### Logging Levels

```python
from omni_scripts.logging.logger import get_logger

logger = get_logger(__name__)

# DEBUG: Detailed debugging information
logger.debug("Initializing build system with target: %s", target)

# INFO: General informational messages
logger.info("Build completed successfully")

# WARNING: Warning about potential issues
logger.warning("Configuration file not found, using defaults")

# ERROR: Error occurred but execution continues
logger.error("Failed to compile shader: %s", shader_path)

# CRITICAL: Critical error that may cause failure
logger.critical("Build system initialization failed")
```

#### Structured Logging

```python
# GOOD: Use structured logging with extra context
logger.error(
    "Build failed",
    extra={
        "target": target,
        "config": config,
        "compiler": compiler,
        "error": str(error)
    }
)

# GOOD: Log exceptions with traceback
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")
```

#### Custom Formatters

```python
# GOOD: Custom formatter for colored output
class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support."""

    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)
```

### File Logging Requirements

#### C++ File Logging

```cpp
// GOOD: Rotating file sink
#include <spdlog/sinks/rotating_file_sink.h>

auto file_sink = std::make_shared<spdlog::sinks::rotating_file_sink_mt>(
    "logs/omnicpp_engine.log",
    1024 * 1024 * 10,  // 10 MB max file size
    5                   // Keep 5 files
);
```

#### Python File Logging

```python
# GOOD: Rotating file handler
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    "logs/omnicpp_python.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)
```

### Custom Formatting

#### C++ Custom Formatting

```cpp
// GOOD: Custom pattern with timestamp, logger name, level, and message
spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] [%t] %v");

// Pattern options:
// %Y - Year (4 digits)
// %m - Month (01-12)
// %d - Day (01-31)
// %H - Hour (00-23)
// %M - Minute (00-59)
// %S - Second (00-59)
// %e - Millisecond (000-999)
// %n - Logger name
// %l - Log level (DEBUG, INFO, etc.)
// %t - Thread ID
// %v - Message
```

#### Python Custom Formatting

```python
# GOOD: Custom format with timestamp, logger name, level, and message
format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(
    fmt=format_string,
    datefmt=date_format
)
```

---

## Cross-Platform Guidelines

### Platform Detection

#### C++ Platform Detection

```cpp
// GOOD: Use preprocessor macros for platform detection
#if defined(_WIN32) || defined(_WIN64)
    #define OMNICPP_PLATFORM_WINDOWS
#elif defined(__linux__)
    #define OMNICPP_PLATFORM_LINUX
#elif defined(__APPLE__)
    #define OMNICPP_PLATFORM_MACOS
#endif

// Usage
#ifdef OMNICPP_PLATFORM_WINDOWS
    // Windows-specific code
    #include <windows.h>
#elif defined(OMNICPP_PLATFORM_LINUX)
    // Linux-specific code
    #include <unistd.h>
#endif
```

#### Python Platform Detection

```python
# GOOD: Use sys.platform for platform detection
import sys

if sys.platform == "win32":
    # Windows-specific code
    import winreg
elif sys.platform.startswith("linux"):
    # Linux-specific code
    import os
elif sys.platform == "darwin":
    # macOS-specific code
    pass
```

### Path Handling

#### C++ Path Handling

```cpp
// GOOD: Use std::filesystem for cross-platform paths
#include <filesystem>

namespace fs = std::filesystem;

// Get project root
fs::path project_root = fs::current_path();

// Construct paths
fs::path config_path = project_root / "config" / "build.json";

// Check existence
if (fs::exists(config_path)) {
    // Load config
}

// Create directories
fs::path logs_dir = project_root / "logs";
fs::create_directories(logs_dir);
```

#### Python Path Handling

```python
# GOOD: Use pathlib for cross-platform paths
from pathlib import Path

# Get project root
project_root = Path.cwd()

# Construct paths
config_path = project_root / "config" / "build.json"

# Check existence
if config_path.exists():
    # Load config
    pass

# Create directories
logs_dir = project_root / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)
```

### Compiler-Specific Code

#### MSVC

```cpp
// GOOD: MSVC-specific code
#ifdef _MSC_VER
    #pragma warning(push, 0)
    #include <windows.h>
    #pragma warning(pop)

    // MSVC-specific attributes
    __declspec(dllexport) void exportFunction();
#endif
```

#### GCC/Clang

```cpp
// GOOD: GCC/Clang-specific code
#if defined(__GNUC__) || defined(__clang__)
    // GCC/Clang-specific attributes
    __attribute__((visibility("default"))) void exportFunction();

    // Suppress warnings
    #pragma GCC diagnostic push
    #pragma GCC diagnostic ignored "-Wunused-parameter"
    #include <some_header.h>
    #pragma GCC diagnostic pop
#endif
```

### Dynamic Library Loading

#### C++ Dynamic Library Loading

```cpp
// GOOD: Cross-platform dynamic library loading
#ifdef OMNICPP_PLATFORM_WINDOWS
    #include <windows.h>
    using LibraryHandle = HMODULE;
#else
    #include <dlfcn.h>
    using LibraryHandle = void*;
#endif

class DynamicLibrary {
public:
    explicit DynamicLibrary(const std::filesystem::path& path) {
#ifdef OMNICPP_PLATFORM_WINDOWS
        handle_ = LoadLibraryW(path.c_str());
#else
        handle_ = dlopen(path.c_str(), RTLD_LAZY);
#endif
        if (!handle_) {
            throw std::runtime_error("Failed to load library");
        }
    }

    ~DynamicLibrary() {
        if (handle_) {
#ifdef OMNICPP_PLATFORM_WINDOWS
            FreeLibrary(handle_);
#else
            dlclose(handle_);
#endif
        }
    }

    template<typename T>
    T getSymbol(const std::string& name) {
#ifdef OMNICPP_PLATFORM_WINDOWS
        return reinterpret_cast<T>(GetProcAddress(handle_, name.c_str()));
#else
        return reinterpret_cast<T>(dlsym(handle_, name.c_str()));
#endif
    }

private:
    LibraryHandle handle_;
};
```

#### Python Dynamic Library Loading

```python
# GOOD: Use ctypes for cross-platform dynamic library loading
import ctypes
import sys

if sys.platform == "win32":
    library = ctypes.CDLL("library.dll")
elif sys.platform.startswith("linux"):
    library = ctypes.CDLL("library.so")
elif sys.platform == "darwin":
    library = ctypes.CDLL("library.dylib")
```

### Thread Handling

#### C++ Thread Handling

```cpp
// GOOD: Use std::thread for cross-platform threading
#include <thread>
#include <mutex>
#include <condition_variable>

class ThreadPool {
public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers_.emplace_back([this] { workerThread(); });
        }
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            stop_ = true;
        }
        condition_.notify_all();
        for (auto& worker : workers_) {
            worker.join();
        }
    }

private:
    void workerThread() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(queue_mutex_);
                condition_.wait(lock, [this] {
                    return stop_ || !tasks_.empty();
                });

                if (stop_ && tasks_.empty()) {
                    return;
                }

                task = std::move(tasks_.front());
                tasks_.pop();
            }
            task();
        }
    }

    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex queue_mutex_;
    std::condition_variable condition_;
    bool stop_ = false;
};
```

#### Python Thread Handling

```python
# GOOD: Use concurrent.futures for cross-platform threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

def process_task(task_id: int) -> int:
    """Process a single task."""
    logger.info("Processing task %d", task_id)
    return task_id * 2

def main() -> None:
    """Main function."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_task, i) for i in range(10)]

        for future in as_completed(futures):
            try:
                result = future.result()
                logger.info("Task completed: %d", result)
            except Exception as e:
                logger.exception("Task failed: %s", e)
```

### WASM Support

#### CMake WASM Configuration

```cmake
# GOOD: WASM-specific configuration
if(EMSCRIPTEN)
    set(CMAKE_EXECUTABLE_SUFFIX ".html")

    target_compile_options(engine PUBLIC
        -s USE_SDL=2
        -s USE_VULKAN=1
        -s ALLOW_MEMORY_GROWTH=1
        -s MAX_WEBGL_VERSION=2
    )

    target_link_options(engine PUBLIC
        -s WASM=1
        -s EXPORTED_FUNCTIONS=["_main","_initialize"]
        -s EXPORTED_RUNTIME_METHODS=["ccall","cwrap"]
    )
endif()
```

#### Python WASM Detection

```python
# GOOD: Detect WASM environment
import sys

def is_wasm() -> bool:
    """Check if running in WASM environment."""
    return sys.platform == "emscripten"

if is_wasm():
    # WASM-specific code
    print("Running in WASM environment")
```

---

## Package Manager Integration

### CPM.cmake

#### Adding Dependencies

```cmake
# GOOD: Use CPM for header-only libraries
CPMAddPackage(
    NAME spdlog
    VERSION 1.12.0
    GITHUB_REPOSITORY gabime/spdlog
    OPTIONS
        SPDLOG_BUILD_SHARED OFF
        SPDLOG_BUILD_EXAMPLE OFF
        SPDLOG_BUILD_TESTS OFF
)

# GOOD: Use CPM for compiled libraries
CPMAddPackage(
    NAME glm
    VERSION 0.9.9.8
    GITHUB_REPOSITORY g-truc/glm
    URL https://github.com/g-truc/glm/archive/0.9.9.8.tar.gz
)

# Link to CPM packages
target_link_libraries(engine
    PUBLIC
        spdlog::spdlog
        glm::glm
)
```

#### CPM Best Practices

```cmake
# GOOD: Use CPMFindPackage for system packages
CPMFindPackage(
    NAME Vulkan
    VERSION 1.3.0
    FIND_PACKAGE_ARGUMENTS "Vulkan REQUIRED"
)

# GOOD: Use CPMAddPackage for Git dependencies
CPMAddPackage(
    NAME fmt
    VERSION 10.0.0
    GITHUB_REPOSITORY fmtlib/fmt
    GIT_TAG 10.0.0
    GIT_SHALLOW TRUE
)

# GOOD: Use CPM for local packages
CPMAddPackage(
    NAME local_package
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/external/local_package
)
```

### Conan

#### Conan Integration

```cmake
# GOOD: Conan integration
if(OMNICPP_USE_CONAN)
    include(cmake/ConanIntegration.cmake)

    # Install Conan dependencies
    conan_cmake_install(
        PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}
        BUILD missing
        SETTINGS build_type=${CMAKE_BUILD_TYPE}
        SETTINGS compiler=${CMAKE_CXX_COMPILER_ID}
        SETTINGS compiler.version=${CMAKE_CXX_COMPILER_VERSION}
        SETTINGS os=${CMAKE_SYSTEM_NAME}
        SETTINGS arch=${CMAKE_SYSTEM_PROCESSOR}
    )

    # Include Conan-generated files
    include(${CMAKE_BINARY_DIR}/conan/conan_toolchain.cmake)
endif()
```

#### Conan Profile

```ini
# conan/profiles/msvc
[settings]
os=Windows
arch=x86_64
compiler=Visual Studio
compiler.version=193
build_type=Release

[buildenv]
CC=cl
CXX=cl
```

#### Conanfile

```python
# conanfile.py
from conan import ConanFile

class OmniCppConan(ConanFile):
    name = "omnicpp"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    requires = "spdlog/1.12.0", "glm/0.9.9.8", "vulkan-headers/1.3.0"
    generators = "CMakeToolchain", "CMakeDeps"

    def configure(self):
        if self.settings.os == "Windows":
            self.options["spdlog"].shared = False
```

### vcpkg

#### vcpkg Integration

```cmake
# GOOD: vcpkg integration
if(OMNICPP_USE_VCPKG)
    # vcpkg toolchain file is set via CMAKE_TOOLCHAIN_FILE
    # Find vcpkg packages
    find_package(Vulkan REQUIRED)
    find_package(spdlog CONFIG REQUIRED)
    find_package(glm CONFIG REQUIRED)

    # Link to vcpkg packages
    target_link_libraries(engine
        PUBLIC
            Vulkan::Vulkan
            spdlog::spdlog
            glm::glm
    )
endif()
```

#### vcpkg.json

```json
{
  "name": "omnicpp",
  "version": "1.0.0",
  "dependencies": [
    "spdlog",
    "glm",
    "vulkan-headers",
    "stb"
  ],
  "builtin-baseline": "2024-01-01"
}
```

### Package Manager Selection

```cmake
# GOOD: Allow selection of package manager
option(OMNICPP_USE_CONAN "Use Conan package manager" OFF)
option(OMNICPP_USE_VCPKG "Use vcpkg package manager" OFF)
option(OMNICPP_USE_CPM "Use CPM.cmake package manager" ON)

# Ensure at least one package manager is selected
if(NOT OMNICPP_USE_CONAN AND NOT OMNICPP_USE_VCPKG AND NOT OMNICPP_USE_CPM)
    message(FATAL_ERROR "At least one package manager must be enabled")
endif()

# Priority: Conan > vcpkg > CPM
if(OMNICPP_USE_CONAN)
    include(cmake/ConanIntegration.cmake)
elseif(OMNICPP_USE_VCPKG)
    include(cmake/VcpkgIntegration.cmake)
else()
    include(cmake/CPM.cmake)
endif()
```

---

## Testing Standards

### C++ Testing

#### Google Test Framework

```cpp
// GOOD: Use Google Test for unit tests
#include <gtest/gtest.h>
#include "engine/core/engine.hpp"

class EngineTest : public ::testing::Test {
protected:
    void SetUp() override {
        engine = std::make_unique<Engine>();
    }

    void TearDown() override {
        engine.reset();
    }

    std::unique_ptr<Engine> engine;
};

TEST_F(EngineTest, Initialization) {
    ASSERT_TRUE(engine->initialize());
    EXPECT_EQ(engine->getState(), EngineState::Initialized);
}

TEST_F(EngineTest, Rendering) {
    engine->initialize();
    ASSERT_TRUE(engine->render());
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

#### Test Organization

```
tests/
├── engine/
│   ├── CMakeLists.txt
│   ├── test_engine.cpp
│   ├── test_renderer.cpp
│   └── test_physics.cpp
├── game/
│   ├── CMakeLists.txt
│   ├── test_game.cpp
│   └── test_scene.cpp
└── CMakeLists.txt
```

#### Test Coverage

```cmake
# GOOD: Enable code coverage
if(OMNICPP_ENABLE_COVERAGE)
    include(cmake/Coverage.cmake)

    target_compile_options(engine PRIVATE
        --coverage
    )

    target_link_options(engine PRIVATE
        --coverage
    )
endif()
```

### Python Testing

#### Pytest Framework

```python
# GOOD: Use pytest for unit tests
import pytest
from omni_scripts.build_system.cmake import CMakeManager

class TestCMakeManager:
    """Test cases for CMakeManager."""

    @pytest.fixture
    def cmake_manager(self):
        """Create a CMakeManager instance for testing."""
        return CMakeManager()

    def test_initialization(self, cmake_manager):
        """Test that CMakeManager initializes correctly."""
        assert cmake_manager is not None
        assert cmake_manager.cmake_path.exists()

    def test_configure(self, cmake_manager):
        """Test CMake configuration."""
        result = cmake_manager.configure(
            source_dir=Path("."),
            build_dir=Path("build/test"),
            preset="default"
        )
        assert result == 0

    @pytest.mark.parametrize("preset", ["debug", "release"])
    def test_configure_presets(self, cmake_manager, preset):
        """Test CMake configuration with different presets."""
        result = cmake_manager.configure(
            source_dir=Path("."),
            build_dir=Path(f"build/{preset}"),
            preset=preset
        )
        assert result == 0
```

#### Test Organization

```
tests/
├── unit/
│   ├── test_build_system.py
│   ├── test_compilers.py
│   └── test_controller.py
├── integration/
│   ├── test_full_build.py
│   └── test_cross_platform.py
└── conftest.py
```

#### Test Coverage

```python
# GOOD: Use pytest-cov for code coverage
# Run tests with coverage:
# pytest --cov=omni_scripts --cov-report=html --cov-report=term

def test_function_with_coverage():
    """Test function to measure coverage."""
    from omni_scripts.utils import calculate_sum

    result = calculate_sum([1, 2, 3, 4, 5])
    assert result == 15
```

### Integration Testing

#### C++ Integration Tests

```cpp
// GOOD: Integration tests for multiple components
#include <gtest/gtest.h>
#include "engine/core/engine.hpp"
#include "engine/graphics/renderer.hpp"
#include "engine/physics/physics_engine.hpp"

class IntegrationTest : public ::testing::Test {
protected:
    void SetUp() override {
        engine = std::make_unique<Engine>();
        renderer = std::make_unique<Renderer>();
        physics = std::make_unique<PhysicsEngine>();
    }

    std::unique_ptr<Engine> engine;
    std::unique_ptr<Renderer> renderer;
    std::unique_ptr<PhysicsEngine> physics;
};

TEST_F(IntegrationTest, EngineWithRenderer) {
    ASSERT_TRUE(engine->initialize());
    ASSERT_TRUE(renderer->initialize(engine->getWindow()));
    ASSERT_TRUE(engine->render());
}

TEST_F(IntegrationTest, EngineWithPhysics) {
    ASSERT_TRUE(engine->initialize());
    ASSERT_TRUE(physics->initialize());
    ASSERT_TRUE(engine->updatePhysics());
}
```

#### Python Integration Tests

```python
# GOOD: Integration tests for multiple components
import pytest
from pathlib import Path
from omni_scripts.controller.build_controller import BuildController
from omni_scripts.build_system.cmake import CMakeManager

class TestIntegration:
    """Integration tests for build system."""

    @pytest.fixture
    def build_controller(self):
        """Create a BuildController instance."""
        args = argparse.Namespace(
            command="build",
            target="engine",
            config="debug",
            compiler=None,
            verbose=True
        )
        return BuildController(args)

    def test_full_build(self, build_controller):
        """Test full build process."""
        result = build_controller.execute()
        assert result == 0

    def test_build_with_coverage(self, build_controller):
        """Test build with code coverage."""
        # Enable coverage
        build_controller.args.coverage = True
        result = build_controller.execute()
        assert result == 0
```

### Test Requirements

#### Unit Tests

- **Coverage:** Minimum 80% code coverage
- **Speed:** Each test should complete in < 1 second
- **Isolation:** Tests must be independent and order-independent
- **Naming:** Test names should describe what is being tested

#### Integration Tests

- **Scope:** Test interactions between multiple components
- **Environment:** Should run in a clean environment
- **Cleanup:** Must clean up after execution
- **Documentation:** Should document the integration scenario

#### Performance Tests

```cpp
// GOOD: Performance benchmarks
#include <benchmark/benchmark.h>

static void BM_Rendering(benchmark::State& state) {
    Engine engine;
    engine.initialize();

    for (auto _ : state) {
        engine.render();
    }

    state.SetItemsProcessed(state.iterations());
}

BENCHMARK(BM_Rendering);
```

```python
# GOOD: Performance benchmarks
import pytest
import time

def test_rendering_performance():
    """Test rendering performance."""
    engine = Engine()
    engine.initialize()

    start_time = time.time()
    for _ in range(100):
        engine.render()
    end_time = time.time()

    avg_time = (end_time - start_time) / 100
    assert avg_time < 0.016  # 60 FPS target
```

---

## Code Quality Enforcement

### Automated Tools

#### C++ Code Quality

```bash
# Format code with clang-format
clang-format -i --style=file src/**/*.cpp include/**/*.hpp

# Lint code with clang-tidy
clang-tidy src/**/*.cpp -- -std=c++23 -I include/

# Run static analysis
cppcheck --enable=all --std=c++23 --suppress=missingIncludeSystem src/
```

#### Python Code Quality

```bash
# Format code with black
black omni_scripts/

# Sort imports with isort
isort omni_scripts/

# Type check with mypy
mypy omni_scripts/ --strict

# Lint with pylint
pylint omni_scripts/

# Lint with flake8
flake8 omni_scripts/ --max-line-length=100
```

#### CMake Code Quality

```bash
# Format CMake files
cmake-format -i cmake/*.cmake

# Lint CMake files
cmake-lint cmake/*.cmake
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v17.0.6
    hooks:
      - id: clang-format
        files: \.(cpp|hpp|h)$
        args: ['-i', '--style=file']

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        files: \.py$

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        files: \.py$

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        files: \.py$
        args: ['--strict']

  - repo: https://github.com/cheshirekow/cmake-format-precommit
    rev: v0.6.13
    hooks:
      - id: cmake-format
        files: \.cmake$
```

### CI/CD Integration

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        compiler: [gcc, clang, msvc]
        config: [debug, release]

    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-docs.txt

      - name: Format check
        run: |
          black --check omni_scripts/
          clang-format --dry-run --Werror src/**/*.cpp include/**/*.hpp

      - name: Lint
        run: |
          mypy omni_scripts/ --strict
          clang-tidy src/**/*.cpp -- -std=c++23 -I include/

      - name: Build
        run: |
          cmake -B build -DCMAKE_BUILD_TYPE=${{ matrix.config }}
          cmake --build build --config ${{ matrix.config }}

      - name: Test
        run: |
          ctest --test-dir build --output-on-failure

      - name: Coverage
        if: matrix.config == 'debug'
        run: |
          ctest --test-dir build --coverage
          lcov --capture --directory build --output-file coverage.info
          bash <(curl -s https://codecov.io/bash) -f coverage.info
```

### Code Review Checklist

#### C++ Code Review

- [ ] Code follows C++23 standards
- [ ] No modules used (traditional header/source files)
- [ ] Proper RAII for resource management
- [ ] Smart pointers used correctly
- [ ] Const correctness maintained
- [ ] Exception safety ensured
- [ ] Thread safety considered
- [ ] Performance implications understood
- [ ] Documentation complete
- [ ] Tests written and passing

#### Python Code Review

- [ ] Code follows PEP 8 standards
- [ ] Type hints complete and correct
- [ ] Zero Pylance errors
- [ ] Proper error handling
- [ ] Logging implemented
- [ ] Tests written and passing
- [ ] Documentation complete
- [ ] No security vulnerabilities
- [ ] Performance considered
- [ ] Cross-platform compatible

#### CMake Code Review

- [ ] Modern CMake practices used
- [ ] Target-based approach
- [ ] Proper dependency management
- [ ] Cross-platform compatible
- [ ] Proper installation rules
- [ ] Testing configured
- [ ] Coverage enabled
- [ ] Formatting consistent
- [ ] Documentation complete
- [ ] No hardcoded paths

---

## Appendix

### References

- [C++23 Standard](https://en.cppreference.com/w/cpp/23)
- [PEP 8 - Style Guide for Python Code](https://peps.org/pep-0008/)
- [CMake Documentation](https://cmake.org/documentation/)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [CMake Best Practices](https://cliutils.gitlab.io/modern-cmake/chapters/introduction/)

### Tools

- **C++:** clang-format, clang-tidy, cppcheck, Google Test, Benchmark
- **Python:** Black, isort, mypy, pylint, flake8, pytest, pytest-cov
- **CMake:** cmake-format, cmake-lint, CTest
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-07 | Initial version |

---

**Document Status:** Active
**Next Review:** 2026-07-07
**Maintained By:** OmniCPP Development Team
