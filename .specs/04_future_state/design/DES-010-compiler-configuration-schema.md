# DES-010: Compiler Configuration Schema

## Overview

Defines the compiler configuration schema for specifying compiler settings, flags, and toolchain configurations.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Compiler Configuration",
  "description": "Compiler configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "compilers": {
      "type": "object",
      "description": "Compiler configurations",
      "properties": {
        "gcc": {
          "type": "object",
          "description": "GCC compiler configuration",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to GCC executable"
            },
            "version": {
              "type": "string",
              "pattern": "^\\d+\\.\\d+\\.\\d+$",
              "description": "Minimum GCC version required"
            },
            "c_standard": {
              "type": "string",
              "enum": ["c11", "c17", "c23"],
              "default": "c17",
              "description": "C language standard"
            },
            "cpp_standard": {
              "type": "string",
              "enum": ["c++11", "c++14", "c++17", "c++20", "c++23"],
              "default": "c++23",
              "description": "C++ language standard"
            },
            "optimization": {
              "type": "string",
              "enum": ["O0", "O1", "O2", "O3", "Os", "Oz"],
              "default": "O2",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["Wall", "Wextra", "Wpedantic"],
              "description": "Warning flags"
            },
            "warnings_as_errors": {
              "type": "boolean",
              "default": false,
              "description": "Treat warnings as errors"
            },
            "additional_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional compiler flags"
            },
            "linker_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional linker flags"
            },
            "defines": {
              "type": "object",
              "description": "Preprocessor definitions",
              "additionalProperties": {
                "type": "string"
              }
            },
            "include_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional include paths"
            },
            "library_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional library paths"
            },
            "libraries": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Libraries to link"
            }
          }
        },
        "clang": {
          "type": "object",
          "description": "Clang compiler configuration",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to Clang executable"
            },
            "version": {
              "type": "string",
              "pattern": "^\\d+\\.\\d+\\.\\d+$",
              "description": "Minimum Clang version required"
            },
            "c_standard": {
              "type": "string",
              "enum": ["c11", "c17", "c23"],
              "default": "c17",
              "description": "C language standard"
            },
            "cpp_standard": {
              "type": "string",
              "enum": ["c++11", "c++14", "c++17", "c++20", "c++23"],
              "default": "c++23",
              "description": "C++ language standard"
            },
            "optimization": {
              "type": "string",
              "enum": ["O0", "O1", "O2", "O3", "Os", "Oz"],
              "default": "O2",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["Wall", "Wextra", "Wpedantic"],
              "description": "Warning flags"
            },
            "warnings_as_errors": {
              "type": "boolean",
              "default": false,
              "description": "Treat warnings as errors"
            },
            "additional_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional compiler flags"
            },
            "linker_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional linker flags"
            },
            "defines": {
              "type": "object",
              "description": "Preprocessor definitions",
              "additionalProperties": {
                "type": "string"
              }
            },
            "include_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional include paths"
            },
            "library_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional library paths"
            },
            "libraries": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Libraries to link"
            }
          }
        },
        "msvc": {
          "type": "object",
          "description": "MSVC compiler configuration",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to cl.exe"
            },
            "version": {
              "type": "string",
              "pattern": "^\\d{3}$",
              "description": "MSVC version (e.g., 193 for VS2022)"
            },
            "architecture": {
              "type": "string",
              "enum": ["x64", "x86", "arm64"],
              "default": "x64",
              "description": "Target architecture"
            },
            "toolset": {
              "type": "string",
              "description": "MSVC toolset (e.g., v143, v142)"
            },
            "c_standard": {
              "type": "string",
              "enum": ["c11", "c17", "c23"],
              "default": "c17",
              "description": "C language standard"
            },
            "cpp_standard": {
              "type": "string",
              "enum": ["c++11", "c++14", "c++17", "c++20", "c++23"],
              "default": "c++23",
              "description": "C++ language standard"
            },
            "optimization": {
              "type": "string",
              "enum": ["O0", "O1", "O2", "Ox"],
              "default": "O2",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["W4"],
              "description": "Warning levels"
            },
            "warnings_as_errors": {
              "type": "boolean",
              "default": false,
              "description": "Treat warnings as errors"
            },
            "additional_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional compiler flags"
            },
            "linker_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional linker flags"
            },
            "defines": {
              "type": "object",
              "description": "Preprocessor definitions",
              "additionalProperties": {
                "type": "string"
              }
            },
            "include_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional include paths"
            },
            "library_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional library paths"
            },
            "libraries": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Libraries to link"
            },
            "runtime_library": {
              "type": "string",
              "enum": ["MT", "MTd", "MD", "MDd"],
              "description": "Runtime library linkage"
            },
            "exception_handling": {
              "type": "string",
              "enum": ["sc", "a", "s", "ac"],
              "default": "sc",
              "description": "Exception handling model"
            }
          }
        },
        "mingw": {
          "type": "object",
          "description": "MinGW compiler configuration",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to MinGW executable"
            },
            "version": {
              "type": "string",
              "pattern": "^\\d+\\.\\d+\\.\\d+$",
              "description": "Minimum MinGW version required"
            },
            "architecture": {
              "type": "string",
              "enum": ["x64", "x86", "arm64"],
              "default": "x64",
              "description": "Target architecture"
            },
            "c_standard": {
              "type": "string",
              "enum": ["c11", "c17", "c23"],
              "default": "c17",
              "description": "C language standard"
            },
            "cpp_standard": {
              "type": "string",
              "enum": ["c++11", "c++14", "c++17", "c++20", "c++23"],
              "default": "c++23",
              "description": "C++ language standard"
            },
            "optimization": {
              "type": "string",
              "enum": ["O0", "O1", "O2", "O3", "Os", "Oz"],
              "default": "O2",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["Wall", "Wextra", "Wpedantic"],
              "description": "Warning flags"
            },
            "warnings_as_errors": {
              "type": "boolean",
              "default": false,
              "description": "Treat warnings as errors"
            },
            "additional_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional compiler flags"
            },
            "linker_flags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional linker flags"
            },
            "defines": {
              "type": "object",
              "description": "Preprocessor definitions",
              "additionalProperties": {
                "type": "string"
              }
            },
            "include_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional include paths"
            },
            "library_paths": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Additional library paths"
            },
            "libraries": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Libraries to link"
            }
          }
        }
      }
    },
    "toolchain": {
      "type": "object",
      "description": "Toolchain configuration",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["gcc", "clang", "msvc", "mingw"],
          "description": "Toolchain type"
        },
        "prefix": {
          "type": "string",
          "description": "Toolchain prefix (for cross-compilation)"
        },
        "sysroot": {
          "type": "string",
          "description": "Sysroot path (for cross-compilation)"
        },
        "target": {
          "type": "string",
          "description": "Target triplet (for cross-compilation)"
        },
        "host": {
          "type": "string",
          "description": "Host triplet (for cross-compilation)"
        },
        "build": {
          "type": "string",
          "description": "Build triplet (for cross-compilation)"
        }
      }
    }
  }
}
```

### Python Data Classes

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class CStandard(Enum):
    """C language standards"""
    C11 = "c11"
    C17 = "c17"
    C23 = "c23"

class CppStandard(Enum):
    """C++ language standards"""
    CPP11 = "c++11"
    CPP14 = "c++14"
    CPP17 = "c++17"
    CPP20 = "c++20"
    CPP23 = "c++23"

class OptimizationLevel(Enum):
    """Optimization levels"""
    O0 = "O0"
    O1 = "O1"
    O2 = "O2"
    O3 = "O3"
    Os = "Os"
    Oz = "Oz"
    Ox = "Ox"

class MSVCArchitecture(Enum):
    """MSVC architectures"""
    X64 = "x64"
    X86 = "x86"
    ARM64 = "arm64"

class MSVCRuntimeLibrary(Enum):
    """MSVC runtime libraries"""
    MT = "MT"
    MTd = "MTd"
    MD = "MD"
    MDd = "MDd"

class MSVCExceptionHandling(Enum):
    """MSVC exception handling models"""
    SC = "sc"
    A = "a"
    S = "s"
    AC = "ac"

@dataclass
class BaseCompilerConfig:
    """Base compiler configuration"""
    executable: Optional[str] = None
    version: Optional[str] = None
    c_standard: CStandard = CStandard.C17
    cpp_standard: CppStandard = CppStandard.CPP23
    optimization: OptimizationLevel = OptimizationLevel.O2
    debug_symbols: bool = False
    warnings: List[str] = field(default_factory=lambda: ["Wall", "Wextra", "Wpedantic"])
    warnings_as_errors: bool = False
    additional_flags: List[str] = field(default_factory=list)
    linker_flags: List[str] = field(default_factory=list)
    defines: Dict[str, str] = field(default_factory=dict)
    include_paths: List[str] = field(default_factory=list)
    library_paths: List[str] = field(default_factory=list)
    libraries: List[str] = field(default_factory=list)

@dataclass
class GCCCompilerConfig(BaseCompilerConfig):
    """GCC compiler configuration"""
    pass

@dataclass
class ClangCompilerConfig(BaseCompilerConfig):
    """Clang compiler configuration"""
    pass

@dataclass
class MSVCCompilerConfig(BaseCompilerConfig):
    """MSVC compiler configuration"""
    architecture: MSVCArchitecture = MSVCArchitecture.X64
    toolset: Optional[str] = None
    runtime_library: Optional[MSVCRuntimeLibrary] = None
    exception_handling: MSVCExceptionHandling = MSVCExceptionHandling.SC
    warnings: List[str] = field(default_factory=lambda: ["W4"])

@dataclass
class MinGWCompilerConfig(BaseCompilerConfig):
    """MinGW compiler configuration"""
    architecture: MSVCArchitecture = MSVCArchitecture.X64

@dataclass
class ToolchainConfig:
    """Toolchain configuration"""
    type: Optional[str] = None
    prefix: Optional[str] = None
    sysroot: Optional[str] = None
    target: Optional[str] = None
    host: Optional[str] = None
    build: Optional[str] = None

@dataclass
class CompilerConfiguration:
    """Main compiler configuration"""
    gcc: Optional[GCCCompilerConfig] = None
    clang: Optional[ClangCompilerConfig] = None
    msvc: Optional[MSVCCompilerConfig] = None
    mingw: Optional[MinGWCompilerConfig] = None
    toolchain: Optional[ToolchainConfig] = None
```

## Dependencies

### Internal Dependencies

- `DES-003` - Configuration schema
- `DES-008` - Compiler detection

### External Dependencies

- `dataclasses` - Data structures
- `typing` - Type hints
- `enum` - Enumerations
- `json` - JSON parsing

## Related Requirements

- REQ-010: Compiler Detection
- REQ-015: Compiler Selection Fallback

## Related ADRs

- ADR-001: Python Build System Architecture

## Implementation Notes

### Configuration Loading

1. Load from JSON file
2. Validate against schema
3. Apply defaults
4. Override with environment variables

### Configuration Merging

- Deep merge configuration files
- User config overrides default config
- Command-line args override config files

### Flag Generation

- Generate compiler flags from configuration
- Handle compiler-specific flag syntax
- Apply optimization and warning settings

### Cross-Compilation Support

- Use toolchain prefix for cross-compilation
- Set sysroot for target system
- Configure target triplet

## Usage Example

```python
from omni_scripts.compiler_config import (
    CompilerConfiguration,
    GCCCompilerConfig,
    CppStandard,
    OptimizationLevel
)

# Create compiler configuration
config = CompilerConfiguration(
    gcc=GCCCompilerConfig(
        executable="gcc",
        version="11.0.0",
        cpp_standard=CppStandard.CPP23,
        optimization=OptimizationLevel.O2,
        debug_symbols=True,
        warnings_as_errors=True
    )
)

# Generate compiler flags
flags = config.gcc.additional_flags + [
    f"-std={config.gcc.cpp_standard.value}",
    f"-{config.gcc.optimization.value}",
    "-g" if config.gcc.debug_symbols else ""
]

print(f"Compiler flags: {' '.join(flags)}")
```
