# API Contracts and Interface Definitions

**Document ID:** contracts_01
**Status:** Draft
**Last Updated:** 2026-01-06

---

## Overview

This document defines the API signatures, data types, and event schemas for the OmniCPP build system. These contracts serve as the interface specifications between components.

---

## Python Controller API Contracts

### Command Handler Interface

```python
def handle_command(args: argparse.Namespace) -> int
```

**Return Values:**

- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Configuration error
- `4` - Toolchain error
- `5` - Build error
- `6` - Test failure
- `7` - Lint failure

### Command Dispatchers

#### Configure Command

```python
def configure(args: argparse.Namespace) -> int
```

**Required Arguments:** None

**Optional Arguments:**

- `build_type`: Debug | Release | RelWithDebInfo | MinSizeRel
- `generator`: str (CMake generator name)
- `toolchain`: Path (toolchain file path)
- `preset`: str (CMake preset name)

**Validation:** At least one of generator, toolchain, or preset must be specified

#### Build Command

```python
def build(args: argparse.Namespace) -> int
```

**Required Arguments:**

- `target`: engine | game | standalone | all
- `pipeline`: str (build pipeline name)
- `preset`: str (CMake preset name)
- `config`: debug | release

**Optional Arguments:**

- `compiler`: msvc | clang-msvc | mingw-clang | mingw-gcc | gcc | clang
- `clean`: bool (clean before building)

#### Clean Command

```python
def clean(args: argparse.Namespace) -> int
```

**Required Arguments:** None

**Optional Arguments:**

- `target`: engine | game | standalone | all

**Default:** Clean all targets if not specified

#### Install Command

```python
def install(args: argparse.Namespace) -> int
```

**Required Arguments:**

- `target`: engine | game | standalone | all
- `config`: debug | release

#### Test Command

```python
def test(args: argparse.Namespace) -> int
```

**Required Arguments:**

- `target`: engine | game | standalone | all
- `config`: debug | release

**Optional Arguments:**

- `filter`: str (TBD)

#### Package Command

```python
def package(args: argparse.Namespace) -> int
```

**Required Arguments:**

- `target`: engine | game | standalone | all
- `config`: debug | release

**Optional Arguments:**

- `format`: str (TBD)

#### Format Command

```python
def format(args: argparse.Namespace) -> int
```

**Required Arguments:** None

**Optional Arguments:**

- `files`: List[Path] (specific files to format)
- `directories`: List[Path] (directories to scan)
- `check`: bool (only check formatting without modifying)
- `dry_run`: bool (run in dry-run mode)
- `cpp_only`: bool (only format C++ files)
- `python_only`: bool (only format Python files)

**Default:** Scan current directory if no files or directories specified

#### Lint Command

```python
def lint(args: argparse.Namespace) -> int
```

**Required Arguments:** None

**Optional Arguments:**

- `files`: List[Path] (specific files to lint)
- `directories`: List[Path] (directories to scan)
- `fix`: bool (apply automatic fixes)
- `cpp_only`: bool (only lint C++ files)
- `python_only`: bool (only lint Python files)

**Default:** Scan current directory if no files or directories specified

### Exception Hierarchy

```python
class ControllerError(Exception):
    """Base exception for controller-related errors"""
    fields: ["command: str", "context: Dict[str, Any]"]

class InvalidTargetError(ControllerError):
    """Raised when an invalid target is specified"""
    fields: ["target: str", "valid_targets: List[str]"]

class InvalidPipelineError(ControllerError):
    """Raised when an invalid pipeline is specified"""
    fields: ["pipeline: str", "valid_pipelines: List[str]"]

class ConfigurationError(ControllerError):
    """Raised when configuration is invalid"""
    fields: ["config_file: Path", "validation_errors: List[str]"]

class ToolchainError(ControllerError):
    """Raised when toolchain is not available"""
    fields: ["compiler: str", "reason: str", "suggestions: List[str]"]
```

---

## Configuration Schema Contracts

### Logging Configuration Schema

**File:** `config/logging_python.json`

**Schema:**

```json
{
  "type": "object",
  "required": ["version", "handlers", "loggers"],
  "properties": {
    "version": { "type": "integer", "enum": [1] },
    "handlers": {
      "type": "object",
      "properties": {
        "console": {
          "type": "object",
          "properties": {
            "class": "string",
            "level": "string",
            "formatter": "string",
            "stream": "string"
          }
        },
        "file": {
          "type": "object",
          "properties": {
            "class": "string",
            "level": "string",
            "formatter": "string",
            "filename": "string",
            "maxBytes": "integer",
            "backupCount": "integer"
          }
        }
      }
    },
    "loggers": {
      "type": "object",
      "properties": {
        "": {
          "type": "object",
          "properties": {
            "level": "string",
            "handlers": "array"
          }
        }
      }
    }
  }
}
```

### Compiler Configuration Schema

**File:** `config/compilers.json`

**Schema:**

```json
{
  "type": "object",
  "required": ["platforms"],
  "properties": {
    "platforms": {
      "type": "object",
      "properties": {
        "windows": {
          "type": "object",
          "properties": {
            "msvc": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string",
                "vcvars_path": "string"
              }
            },
            "clang_msvc": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string"
              }
            },
            "mingw_gcc": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string",
                "environment": "UCRT64|MSYS2"
              }
            },
            "mingw_clang": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string",
                "environment": "UCRT64|MSYS2"
              }
            }
          }
        },
        "linux": {
          "type": "object",
          "properties": {
            "gcc": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string"
              }
            },
            "clang": {
              "type": "object",
              "properties": {
                "path": "string",
                "version": "string"
              }
            }
          }
        }
      }
    }
  }
}
```

### Build Configuration Schema

**File:** `config/build.json`

**Schema:**

```json
{
  "type": "object",
  "required": ["targets", "pipelines"],
  "properties": {
    "targets": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["engine", "game", "standalone"]
      }
    },
    "pipelines": {
      "type": "object",
      "properties": {
        "default": {
          "type": "object",
          "properties": {
            "cmake_args": "array",
            "conan_args": "array"
          }
        }
      }
    }
  }
}
```

---

## Cross-Platform Compilation Interfaces

### Platform Detection Interface

```python
def detect_host() -> PlatformInfo
```

**Return Type:** `PlatformInfo`

**Fields:**

- `os`: Windows | Linux | macOS
- `architecture`: x86_64 | ARM64 | other
- `is_64bit`: bool

```python
def detect_target(args: argparse.Namespace) -> TargetInfo
```

**Return Type:** `TargetInfo`

**Fields:**

- `platform`: Windows | Linux | WASM | other
- `architecture`: x86_64 | ARM64 | other
- `toolchain`: Path

### Compiler Detection Interface

```python
def detect_msvc() -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: MSVC
- `version`: str
- `path`: Path
- `vcvars_path`: Path
- `supports_cpp23`: bool

```python
def detect_msvc_clang() -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: MSVC-Clang
- `version`: str
- `path`: Path
- `supports_cpp23`: bool

```python
def detect_mingw_gcc(environment: str) -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: MinGW-GCC
- `version`: str
- `path`: Path
- `environment`: UCRT64 | MSYS2
- `supports_cpp23`: bool

```python
def detect_mingw_clang(environment: str) -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: MinGW-Clang
- `version`: str
- `path`: Path
- `environment`: UCRT64 | MSYS2
- `supports_cpp23`: bool

```python
def detect_gcc() -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: GCC
- `version`: str
- `path`: Path
- `supports_cpp23`: bool

```python
def detect_clang() -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: Clang
- `version`: str
- `path`: Path
- `supports_cpp23`: bool

```python
def detect_emscripten() -> CompilerInfo | None
```

**Return Type:** `CompilerInfo | None`

**Fields:**

- `name`: Emscripten
- `version`: str
- `path`: Path
- `supports_cpp23`: bool

```python
def validate_cpp23_support(compiler: CompilerInfo) -> ValidationResult
```

**Return Type:** `ValidationResult`

**Fields:**

- `supported`: bool
- `version`: str
- `warnings`: List[str]
- `fallback`: C++20 | None

### Terminal Setup Interface

```python
def setup_vs_dev_prompt(arch: str = 'x64') -> bool
```

**Return Type:** bool

**Parameters:**

- `arch`: x64 | ARM64

**Environment Variables:**

- INCLUDE
- LIB
- LIBPATH
- PATH

```python
def setup_msys2_environment(environment: str = 'UCRT64') -> bool
```

**Return Type:** bool

**Parameters:**

- `environment`: UCRT64 | MSYS2

**Environment Variables:**

- MSYSTEM
- MSYSTEM_PREFIX
- PATH

```python
def setup_linux_environment(compiler: str) -> bool
```

**Return Type:** bool

**Parameters:**

- `compiler`: gcc | clang

**Environment Variables:**

- PATH
- CC
- CXX

```python
def validate_environment(compiler: str) -> ValidationResult
```

**Return Type:** `ValidationResult`

**Fields:**

- `valid`: bool
- `missing_vars`: List[str]
- `compiler_accessible`: bool
- `errors`: List[str]

### Toolchain Selection Interface

```python
def select_toolchain(target: TargetInfo) -> Path
```

**Return Type:** Path

**Parameters:**

- `target`: TargetInfo

**Toolchain Files:**

- Windows to Linux: `cmake/toolchains/x86-linux-gnu.cmake`
- Windows to WASM: `cmake/toolchains/emscripten.cmake`
- ARM64 Linux: `cmake/toolchains/arm64-linux-gnu.cmake`
- ARM64 Windows: `cmake/toolchains/arm64-windows-msvc.cmake`

```python
def validate_toolchain(toolchain_path: Path) -> ValidationResult
```

**Return Type:** `ValidationResult`

**Fields:**

- `valid`: bool
- `exists`: bool
- `syntax_valid`: bool
- `errors`: List[str]

---

## Logging Interfaces

### Logger Setup Interface

```python
def setup_logger(config_path: Path) -> logging.Logger
```

**Return Type:** `logging.Logger`

**Parameters:**

- `config_path`: Path to logging_python.json

**Log Levels:**

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

```python
def get_logger(name: str) -> logging.Logger
```

**Return Type:** `logging.Logger`

**Parameters:**

- `name`: Module name

### Formatter Interface

```python
class CustomFormatter(logging.Formatter):
    """Custom log formatter with timestamp, level, module, function, message"""
    format_string: "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
    fields:
        - timestamp: datetime
        - level: str
        - module: str
        - function: str
        - message: str
```

```python
class ColoredFormatter(CustomFormatter):
    """Colored console output formatter"""
    color_map:
        DEBUG: blue
        INFO: green
        WARNING: yellow
        ERROR: red
        CRITICAL: magenta
```

```python
class JsonFormatter(logging.Formatter):
    """JSON structured logging formatter"""
    output_format: JSON
    fields:
        - timestamp: ISO 8601
        - level: str
        - module: str
        - function: str
        - message: str
        - extra: Dict[str, Any]
```

### Sink Interface

```python
class ConsoleSink(logging.Handler):
    """Console output handler"""
    output: stdout/stderr
    supports_colors: bool
```

```python
class FileSink(logging.Handler):
    """File output handler with rotation"""
    output: file
    rotation:
        - max_bytes: int
        - backup_count: int
    log_directory: logs/
```

---

## Build System Interfaces

### CMake Integration Interface

```python
def cmake_configure(args: argparse.Namespace) -> int
```

**Return Type:** int

**Parameters:**

- `build_type`: str
- `generator`: str
- `toolchain`: Path
- `preset`: str

**Return Values:**

- 0: Success
- 1: Failure

```python
def cmake_build(target: str, config: str) -> int
```

**Return Type:** int

**Parameters:**

- `target`: str
- `config`: str

**Return Values:**

- 0: Success
- 1: Failure

```python
def cmake_clean(target: str) -> int
```

**Return Type:** int

**Parameters:**

- `target`: str

**Return Values:**

- 0: Success
- 1: Failure

### Conan Integration Interface

```python
def conan_install(profile: str, build_type: str) -> int
```

**Return Type:** int

**Parameters:**

- `profile`: str
- `build_type`: str

**Return Values:**

- 0: Success
- 1: Failure

```python
def conan_create_profile(compiler: str, arch: str) -> Path
```

**Return Type:** Path

**Parameters:**

- `compiler`: str
- `arch`: str

### vcpkg Integration Interface

```python
def vcpkg_install(packages: List[str], triplet: str) -> int
```

**Return Type:** int

**Parameters:**

- `packages`: List[str]
- `triplet`: str

**Return Values:**

- 0: Success
- 1: Failure

```python
def vcpkg_integrate() -> int
```

**Return Type:** int

**Return Values:**

- 0: Success
- 1: Failure

---

## Type Definitions

### PlatformInfo

```python
class PlatformInfo:
    os: str
    architecture: str
    is_64bit: bool
```

### TargetInfo

```python
class TargetInfo:
    platform: str
    architecture: str
    toolchain: Path
```

### CompilerInfo

```python
class CompilerInfo:
    name: str
    version: str
    path: Path
    supports_cpp23: bool
```

### ValidationResult

```python
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]
```

---

## Appendix: Exit Codes Reference

| Code | Meaning             |
| ---- | ------------------- |
| 0    | Success             |
| 1    | General error       |
| 2    | Invalid arguments   |
| 3    | Configuration error |
| 4    | Toolchain error     |
| 5    | Build error         |
| 6    | Test failure        |
| 7    | Lint failure        |

