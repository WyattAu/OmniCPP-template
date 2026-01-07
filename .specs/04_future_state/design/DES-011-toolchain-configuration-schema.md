# DES-011: Toolchain Configuration Schema

## Overview
Defines the toolchain configuration schema for specifying build toolchains, including compilers, linkers, and build tools.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Toolchain Configuration",
  "description": "Toolchain configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "toolchains": {
      "type": "object",
      "description": "Toolchain configurations",
      "properties": {
        "default": {
          "type": "string",
          "description": "Default toolchain name"
        },
        "available": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Toolchain name"
              },
              "description": {
                "type": "string",
                "description": "Toolchain description"
              },
              "compiler": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["gcc", "clang", "msvc", "mingw"],
                    "description": "Compiler type"
                  },
                  "executable": {
                    "type": "string",
                    "description": "Compiler executable path"
                  },
                  "version": {
                    "type": "string",
                    "description": "Compiler version"
                  }
                }
              },
              "linker": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["ld", "lld", "gold", "mold", "link"],
                    "description": "Linker type"
                  },
                  "executable": {
                    "type": "string",
                    "description": "Linker executable path"
                  }
                }
              },
              "archiver": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["ar", "llvm-ar", "lib"],
                    "description": "Archiver type"
                  },
                  "executable": {
                    "type": "string",
                    "description": "Archiver executable path"
                  }
                }
              },
              "build_system": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["cmake", "meson", "ninja", "make"],
                    "description": "Build system type"
                  },
                  "generator": {
                    "type": "string",
                    "description": "Build system generator"
                  }
                }
              },
              "debugger": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["gdb", "lldb", "cdb"],
                    "description": "Debugger type"
                  },
                  "executable": {
                    "type": "string",
                    "description": "Debugger executable path"
                  }
                }
              },
              "profiler": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["gprof", "perf", "vtune", "sample"],
                    "description": "Profiler type"
                  },
                  "executable": {
                    "type": "string",
                    "description": "Profiler executable path"
                  }
                }
              },
              "target": {
                "type": "object",
                "properties": {
                  "triplet": {
                    "type": "string",
                    "description": "Target triplet (e.g., x86_64-linux-gnu)"
                  },
                  "architecture": {
                    "type": "string",
                    "enum": ["x86", "x86_64", "arm", "arm64", "aarch64", "mips", "mips64", "powerpc", "powerpc64", "riscv", "riscv64"],
                    "description": "Target architecture"
                  },
                  "os": {
                    "type": "string",
                    "enum": ["linux", "windows", "macos", "freebsd", "android", "ios"],
                    "description": "Target operating system"
                  },
                  "abi": {
                    "type": "string",
                    "enum": ["gnu", "msvc", "mingw", "musl", "eabi", "eabihf"],
                    "description": "Target ABI"
                  }
                }
              },
              "sysroot": {
                "type": "string",
                "description": "Sysroot path for cross-compilation"
              },
              "prefix": {
                "type": "string",
                "description": "Toolchain prefix for cross-compilation"
              },
              "flags": {
                "type": "object",
                "properties": {
                  "cflags": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "C compiler flags"
                  },
                  "cxxflags": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "C++ compiler flags"
                  },
                  "ldflags": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "Linker flags"
                  },
                  "arflags": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "Archiver flags"
                  }
                }
              },
              "environment": {
                "type": "object",
                "description": "Environment variables for toolchain",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    },
    "cross_compilation": {
      "type": "object",
      "description": "Cross-compilation configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": false,
          "description": "Enable cross-compilation"
        },
        "toolchain": {
          "type": "string",
          "description": "Cross-compilation toolchain name"
        },
        "target": {
          "type": "string",
          "description": "Target triplet"
        },
        "host": {
          "type": "string",
          "description": "Host triplet"
        },
        "build": {
          "type": "string",
          "description": "Build triplet"
        },
        "sysroot": {
          "type": "string",
          "description": "Sysroot path"
        },
        "qemu": {
          "type": "object",
          "description": "QEMU configuration for testing",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable QEMU for testing"
            },
            "executable": {
              "type": "string",
              "description": "QEMU executable path"
            },
            "architecture": {
              "type": "string",
              "description": "QEMU architecture"
            }
          }
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

class CompilerType(Enum):
    """Compiler types"""
    GCC = "gcc"
    CLANG = "clang"
    MSVC = "msvc"
    MINGW = "mingw"

class LinkerType(Enum):
    """Linker types"""
    LD = "ld"
    LLD = "lld"
    GOLD = "gold"
    MOLD = "mold"
    LINK = "link"

class ArchiverType(Enum):
    """Archiver types"""
    AR = "ar"
    LLVM_AR = "llvm-ar"
    LIB = "lib"

class BuildSystemType(Enum):
    """Build system types"""
    CMAKE = "cmake"
    MESON = "meson"
    NINJA = "ninja"
    MAKE = "make"

class DebuggerType(Enum):
    """Debugger types"""
    GDB = "gdb"
    LLDB = "lldb"
    CDB = "cdb"

class ProfilerType(Enum):
    """Profiler types"""
    GPROF = "gprof"
    PERF = "perf"
    VTUNE = "vtune"
    SAMPLE = "sample"

class Architecture(Enum):
    """CPU architectures"""
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    AARCH64 = "aarch64"
    MIPS = "mips"
    MIPS64 = "mips64"
    POWERPC = "powerpc"
    POWERPC64 = "powerpc64"
    RISCV = "riscv"
    RISCV64 = "riscv64"

class OperatingSystem(Enum):
    """Operating systems"""
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"
    FREEBSD = "freebsd"
    ANDROID = "android"
    IOS = "ios"

class ABI(Enum):
    """Application Binary Interfaces"""
    GNU = "gnu"
    MSVC = "msvc"
    MINGW = "mingw"
    MUSL = "musl"
    EABI = "eabi"
    EABIHF = "eabihf"

@dataclass
class CompilerConfig:
    """Compiler configuration"""
    type: CompilerType
    executable: Optional[str] = None
    version: Optional[str] = None

@dataclass
class LinkerConfig:
    """Linker configuration"""
    type: LinkerType
    executable: Optional[str] = None

@dataclass
class ArchiverConfig:
    """Archiver configuration"""
    type: ArchiverType
    executable: Optional[str] = None

@dataclass
class BuildSystemConfig:
    """Build system configuration"""
    type: BuildSystemType
    generator: Optional[str] = None

@dataclass
class DebuggerConfig:
    """Debugger configuration"""
    type: DebuggerType
    executable: Optional[str] = None

@dataclass
class ProfilerConfig:
    """Profiler configuration"""
    type: ProfilerType
    executable: Optional[str] = None

@dataclass
class TargetConfig:
    """Target configuration"""
    triplet: Optional[str] = None
    architecture: Optional[Architecture] = None
    os: Optional[OperatingSystem] = None
    abi: Optional[ABI] = None

@dataclass
class ToolchainFlags:
    """Toolchain flags"""
    cflags: List[str] = field(default_factory=list)
    cxxflags: List[str] = field(default_factory=list)
    ldflags: List[str] = field(default_factory=list)
    arflags: List[str] = field(default_factory=list)

@dataclass
class ToolchainConfig:
    """Toolchain configuration"""
    name: str
    description: Optional[str] = None
    compiler: Optional[CompilerConfig] = None
    linker: Optional[LinkerConfig] = None
    archiver: Optional[ArchiverConfig] = None
    build_system: Optional[BuildSystemConfig] = None
    debugger: Optional[DebuggerConfig] = None
    profiler: Optional[ProfilerConfig] = None
    target: Optional[TargetConfig] = None
    sysroot: Optional[str] = None
    prefix: Optional[str] = None
    flags: ToolchainFlags = field(default_factory=ToolchainFlags)
    environment: Dict[str, str] = field(default_factory=dict)

@dataclass
class QEMUConfig:
    """QEMU configuration for cross-compilation testing"""
    enabled: bool = False
    executable: Optional[str] = None
    architecture: Optional[str] = None

@dataclass
class CrossCompilationConfig:
    """Cross-compilation configuration"""
    enabled: bool = False
    toolchain: Optional[str] = None
    target: Optional[str] = None
    host: Optional[str] = None
    build: Optional[str] = None
    sysroot: Optional[str] = None
    qemu: QEMUConfig = field(default_factory=QEMUConfig)

@dataclass
class ToolchainConfiguration:
    """Main toolchain configuration"""
    default: Optional[str] = None
    available: List[ToolchainConfig] = field(default_factory=list)
    cross_compilation: CrossCompilationConfig = field(default_factory=CrossCompilationConfig)
```

## Dependencies

### Internal Dependencies
- `DES-003` - Configuration schema
- `DES-008` - Compiler detection
- `DES-010` - Compiler configuration

### External Dependencies
- `dataclasses` - Data structures
- `typing` - Type hints
- `enum` - Enumerations
- `json` - JSON parsing

## Related Requirements
- REQ-010: Compiler Detection
- REQ-014: Cross-Compilation Support
- REQ-015: Compiler Selection Fallback

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Toolchain Detection
1. Detect available compilers
2. Detect available linkers
3. Detect available build systems
4. Match tools to toolchains
5. Validate toolchain completeness

### Cross-Compilation Setup
1. Set target triplet
2. Configure sysroot
3. Set toolchain prefix
4. Configure environment variables
5. Validate cross-compilation setup

### Toolchain Validation
- Check all required tools exist
- Validate tool versions
- Check tool compatibility
- Verify target configuration

### QEMU Integration
- Detect QEMU availability
- Configure QEMU for target architecture
- Set up testing environment
- Handle QEMU execution

## Usage Example

```python
from omni_scripts.toolchain import (
    ToolchainConfiguration,
    ToolchainConfig,
    CompilerConfig,
    LinkerConfig,
    TargetConfig,
    Architecture,
    OperatingSystem,
    ABI
)

# Create toolchain configuration
config = ToolchainConfiguration(
    default="gcc-x86_64-linux-gnu",
    available=[
        ToolchainConfig(
            name="gcc-x86_64-linux-gnu",
            description="GCC toolchain for x86_64 Linux",
            compiler=CompilerConfig(
                type=CompilerType.GCC,
                executable="gcc",
                version="11.0.0"
            ),
            linker=LinkerConfig(
                type=LinkerType.LLD,
                executable="ld.lld"
            ),
            target=TargetConfig(
                triplet="x86_64-linux-gnu",
                architecture=Architecture.X86_64,
                os=OperatingSystem.LINUX,
                abi=ABI.GNU
            )
        )
    ]
)

# Get default toolchain
default_toolchain = next(
    (tc for tc in config.available if tc.name == config.default),
    None
)

if default_toolchain:
    print(f"Toolchain: {default_toolchain.name}")
    print(f"Compiler: {default_toolchain.compiler.executable}")
    print(f"Target: {default_toolchain.target.triplet}")
```
