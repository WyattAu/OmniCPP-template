# DES-003: Configuration Schema

## Overview

Defines the JSON configuration schema for the OmniCppController system, including project settings, build configurations, and toolchain settings.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OmniCppController Configuration",
  "description": "Configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "project": {
      "type": "object",
      "description": "Project-level configuration",
      "properties": {
        "name": {
          "type": "string",
          "description": "Project name"
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9]+)?$",
          "description": "Project version (semantic versioning)"
        },
        "description": {
          "type": "string",
          "description": "Project description"
        },
        "root_dir": {
          "type": "string",
          "description": "Project root directory (absolute or relative)"
        },
        "build_dir": {
          "type": "string",
          "default": "build",
          "description": "Build output directory"
        },
        "config_dir": {
          "type": "string",
          "default": "config",
          "description": "Configuration directory"
        },
        "source_dir": {
          "type": "string",
          "default": "src",
          "description": "Source code directory"
        },
        "include_dir": {
          "type": "string",
          "default": "include",
          "description": "Header files directory"
        },
        "test_dir": {
          "type": "string",
          "default": "tests",
          "description": "Test files directory"
        }
      },
      "required": ["name", "version"]
    },
    "build": {
      "type": "object",
      "description": "Build configuration",
      "properties": {
        "default_config": {
          "type": "string",
          "enum": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
          "default": "Release",
          "description": "Default build configuration"
        },
        "parallel_jobs": {
          "type": "integer",
          "minimum": 1,
          "default": 1,
          "description": "Number of parallel build jobs"
        },
        "generator": {
          "type": "string",
          "description": "CMake generator (e.g., Ninja, Unix Makefiles, Visual Studio)"
        },
        "toolchain_file": {
          "type": "string",
          "description": "Path to CMake toolchain file"
        },
        "cmake_args": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Additional CMake arguments"
        },
        "compiler_args": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Additional compiler arguments"
        },
        "linker_args": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Additional linker arguments"
        },
        "optimizations": {
          "type": "object",
          "description": "Build optimization settings",
          "properties": {
            "lto": {
              "type": "boolean",
              "default": false,
              "description": "Enable Link Time Optimization"
            },
            "ipo": {
              "type": "boolean",
              "default": false,
              "description": "Enable Interprocedural Optimization"
            },
            "pgo": {
              "type": "boolean",
              "default": false,
              "description": "Enable Profile Guided Optimization"
            }
          }
        }
      }
    },
    "compilers": {
      "type": "object",
      "description": "Compiler configuration",
      "properties": {
        "preferred": {
          "type": "string",
          "enum": ["auto", "gcc", "clang", "msvc", "mingw"],
          "default": "auto",
          "description": "Preferred compiler"
        },
        "fallback_order": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["gcc", "clang", "msvc", "mingw"]
          },
          "description": "Fallback compiler order"
        },
        "gcc": {
          "type": "object",
          "description": "GCC-specific settings",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to GCC executable"
            },
            "version": {
              "type": "string",
              "description": "Minimum GCC version required"
            },
            "args": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "GCC-specific arguments"
            }
          }
        },
        "clang": {
          "type": "object",
          "description": "Clang-specific settings",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to Clang executable"
            },
            "version": {
              "type": "string",
              "description": "Minimum Clang version required"
            },
            "args": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Clang-specific arguments"
            }
          }
        },
        "msvc": {
          "type": "object",
          "description": "MSVC-specific settings",
          "properties": {
            "version": {
              "type": "string",
              "description": "MSVC version (e.g., 193, 194)"
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
            "args": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "MSVC-specific arguments"
            }
          }
        },
        "mingw": {
          "type": "object",
          "description": "MinGW-specific settings",
          "properties": {
            "executable": {
              "type": "string",
              "description": "Path to MinGW executable"
            },
            "version": {
              "type": "string",
              "description": "Minimum MinGW version required"
            },
            "args": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "MinGW-specific arguments"
            }
          }
        }
      }
    },
    "package_managers": {
      "type": "object",
      "description": "Package manager configuration",
      "properties": {
        "priority": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["conan", "vcpkg", "cpm"]
          },
          "default": ["conan", "vcpkg", "cpm"],
          "description": "Package manager priority order"
        },
        "conan": {
          "type": "object",
          "description": "Conan configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable Conan"
            },
            "executable": {
              "type": "string",
              "description": "Path to Conan executable"
            },
            "profile": {
              "type": "string",
              "description": "Conan profile to use"
            },
            "config_dir": {
              "type": "string",
              "description": "Conan configuration directory"
            },
            "cache_dir": {
              "type": "string",
              "description": "Conan cache directory"
            },
            "remote": {
              "type": "string",
              "description": "Conan remote repository"
            }
          }
        },
        "vcpkg": {
          "type": "object",
          "description": "vcpkg configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable vcpkg"
            },
            "executable": {
              "type": "string",
              "description": "Path to vcpkg executable"
            },
            "root": {
              "type": "string",
              "description": "vcpkg root directory"
            },
            "triplet": {
              "type": "string",
              "description": "vcpkg triplet"
            },
            "overlay_triplets": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Overlay triplet directories"
            }
          }
        },
        "cpm": {
          "type": "object",
          "description": "CPM configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable CPM"
            },
            "cache_dir": {
              "type": "string",
              "description": "CPM cache directory"
            },
            "source_dir": {
              "type": "string",
              "description": "CPM source directory"
            }
          }
        }
      }
    },
    "logging": {
      "type": "object",
      "description": "Logging configuration",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
          "default": "INFO",
          "description": "Logging level"
        },
        "format": {
          "type": "string",
          "default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
          "description": "Log message format"
        },
        "file": {
          "type": "object",
          "description": "File logging configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable file logging"
            },
            "path": {
              "type": "string",
              "default": "logs/omnicpp.log",
              "description": "Log file path"
            },
            "max_size": {
              "type": "integer",
              "default": 10485760,
              "description": "Maximum log file size in bytes"
            },
            "backup_count": {
              "type": "integer",
              "default": 5,
              "description": "Number of backup files to keep"
            },
            "rotation": {
              "type": "string",
              "enum": ["size", "time"],
              "default": "size",
              "description": "Log rotation strategy"
            }
          }
        },
        "console": {
          "type": "object",
          "description": "Console logging configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable console logging"
            },
            "color": {
              "type": "boolean",
              "default": true,
              "description": "Enable colored output"
            }
          }
        }
      }
    },
    "testing": {
      "type": "object",
      "description": "Testing configuration",
      "properties": {
        "framework": {
          "type": "string",
          "enum": ["gtest", "catch2", "boost"],
          "default": "gtest",
          "description": "Testing framework"
        },
        "coverage": {
          "type": "object",
          "description": "Code coverage configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable code coverage"
            },
            "format": {
              "type": "string",
              "enum": ["lcov", "xml", "html"],
              "default": "lcov",
              "description": "Coverage report format"
            },
            "output_dir": {
              "type": "string",
              "default": "coverage",
              "description": "Coverage output directory"
            },
            "threshold": {
              "type": "object",
              "description": "Coverage thresholds",
              "properties": {
                "line": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100,
                  "default": 80,
                  "description": "Line coverage threshold"
                },
                "function": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100,
                  "default": 80,
                  "description": "Function coverage threshold"
                },
                "branch": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100,
                  "default": 70,
                  "description": "Branch coverage threshold"
                }
              }
            }
          }
        },
        "parallel": {
          "type": "boolean",
          "default": true,
          "description": "Enable parallel test execution"
        },
        "timeout": {
          "type": "integer",
          "default": 300,
          "description": "Test timeout in seconds"
        }
      }
    },
    "formatting": {
      "type": "object",
      "description": "Code formatting configuration",
      "properties": {
        "clang_format": {
          "type": "object",
          "description": "Clang-format configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable clang-format"
            },
            "executable": {
              "type": "string",
              "description": "Path to clang-format executable"
            },
            "style": {
              "type": "string",
              "default": "file",
              "description": "Clang-format style (file, LLVM, Google, Chromium, Mozilla, WebKit)"
            },
            "config_file": {
              "type": "string",
              "default": ".clang-format",
              "description": "Path to clang-format configuration file"
            }
          }
        },
        "cmake_format": {
          "type": "object",
          "description": "CMake-format configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable cmake-format"
            },
            "executable": {
              "type": "string",
              "description": "Path to cmake-format executable"
            },
            "config_file": {
              "type": "string",
              "default": ".cmake-format",
              "description": "Path to cmake-format configuration file"
            }
          }
        }
      }
    },
    "linting": {
      "type": "object",
      "description": "Code linting configuration",
      "properties": {
        "clang_tidy": {
          "type": "object",
          "description": "Clang-tidy configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable clang-tidy"
            },
            "executable": {
              "type": "string",
              "description": "Path to clang-tidy executable"
            },
            "config_file": {
              "type": "string",
              "default": ".clang-tidy",
              "description": "Path to clang-tidy configuration file"
            },
            "checks": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Clang-tidy checks to enable"
            },
            "warnings_as_errors": {
              "type": "boolean",
              "default": false,
              "description": "Treat warnings as errors"
            }
          }
        },
        "cppcheck": {
          "type": "object",
          "description": "Cppcheck configuration",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable cppcheck"
            },
            "executable": {
              "type": "string",
              "description": "Path to cppcheck executable"
            },
            "suppressions_file": {
              "type": "string",
              "description": "Path to cppcheck suppressions file"
            }
          }
        }
      }
    },
    "security": {
      "type": "object",
      "description": "Security configuration",
      "properties": {
        "sanitizers": {
          "type": "object",
          "description": "Sanitizer configuration",
          "properties": {
            "address": {
              "type": "boolean",
              "default": false,
              "description": "Enable AddressSanitizer"
            },
            "memory": {
              "type": "boolean",
              "default": false,
              "description": "Enable MemorySanitizer"
            },
            "thread": {
              "type": "boolean",
              "default": false,
              "description": "Enable ThreadSanitizer"
            },
            "undefined": {
              "type": "boolean",
              "default": false,
              "description": "Enable UndefinedBehaviorSanitizer"
            }
          }
        },
        "hardening": {
          "type": "object",
          "description": "Hardening options",
          "properties": {
            "stack_protector": {
              "type": "boolean",
              "default": true,
              "description": "Enable stack protector"
            },
            "fortify_source": {
              "type": "boolean",
              "default": true,
              "description": "Enable _FORTIFY_SOURCE"
            },
            "relro": {
              "type": "boolean",
              "default": true,
              "description": "Enable RELRO"
            },
            "pie": {
              "type": "boolean",
              "default": true,
              "description": "Enable PIE"
            }
          }
        }
      }
    },
    "platform": {
      "type": "object",
      "description": "Platform-specific configuration",
      "properties": {
        "windows": {
          "type": "object",
          "description": "Windows-specific settings",
          "properties": {
            "msvc_dev_cmd": {
              "type": "string",
              "description": "Path to MSVC Developer Command Prompt"
            },
            "msys2_root": {
              "type": "string",
              "description": "Path to MSYS2 installation"
            }
          }
        },
        "linux": {
          "type": "object",
          "description": "Linux-specific settings",
          "properties": {
            "pkg_config_path": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "PKG_CONFIG_PATH directories"
            }
          }
        },
        "macos": {
          "type": "object",
          "description": "macOS-specific settings",
          "properties": {
            "xcode_path": {
              "type": "string",
              "description": "Path to Xcode installation"
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
from typing import Dict, List, Optional, Any
from enum import Enum

class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class BuildConfig(Enum):
    """Build configurations"""
    DEBUG = "Debug"
    RELEASE = "Release"
    RELWITHDEBINFO = "RelWithDebInfo"
    MINSIZEREL = "MinSizeRel"

class CompilerType(Enum):
    """Compiler types"""
    AUTO = "auto"
    GCC = "gcc"
    CLANG = "clang"
    MSVC = "msvc"
    MINGW = "mingw"

class PackageManagerType(Enum):
    """Package manager types"""
    CONAN = "conan"
    VCPKG = "vcpkg"
    CPM = "cpm"

@dataclass
class ProjectConfig:
    """Project configuration"""
    name: str
    version: str
    description: Optional[str] = None
    root_dir: Optional[str] = None
    build_dir: str = "build"
    config_dir: str = "config"
    source_dir: str = "src"
    include_dir: str = "include"
    test_dir: str = "tests"

@dataclass
class CompilerSettings:
    """Compiler-specific settings"""
    executable: Optional[str] = None
    version: Optional[str] = None
    args: List[str] = field(default_factory=list)

@dataclass
class MSVCSettings(CompilerSettings):
    """MSVC-specific settings"""
    architecture: str = "x64"
    toolset: Optional[str] = None

@dataclass
class CompilersConfig:
    """Compilers configuration"""
    preferred: CompilerType = CompilerType.AUTO
    fallback_order: List[CompilerType] = field(default_factory=lambda: [CompilerType.GCC, CompilerType.CLANG, CompilerType.MSVC, CompilerType.MINGW])
    gcc: CompilerSettings = field(default_factory=CompilerSettings)
    clang: CompilerSettings = field(default_factory=CompilerSettings)
    msvc: MSVCSettings = field(default_factory=MSVCSettings)
    mingw: CompilerSettings = field(default_factory=CompilerSettings)

@dataclass
class ConanConfig:
    """Conan configuration"""
    enabled: bool = True
    executable: Optional[str] = None
    profile: Optional[str] = None
    config_dir: Optional[str] = None
    cache_dir: Optional[str] = None
    remote: Optional[str] = None

@dataclass
class VcpkgConfig:
    """vcpkg configuration"""
    enabled: bool = True
    executable: Optional[str] = None
    root: Optional[str] = None
    triplet: Optional[str] = None
    overlay_triplets: List[str] = field(default_factory=list)

@dataclass
class CPMConfig:
    """CPM configuration"""
    enabled: bool = True
    cache_dir: Optional[str] = None
    source_dir: Optional[str] = None

@dataclass
class PackageManagersConfig:
    """Package managers configuration"""
    priority: List[PackageManagerType] = field(default_factory=lambda: [PackageManagerType.CONAN, PackageManagerType.VCPKG, PackageManagerType.CPM])
    conan: ConanConfig = field(default_factory=ConanConfig)
    vcpkg: VcpkgConfig = field(default_factory=VcpkgConfig)
    cpm: CPMConfig = field(default_factory=CPMConfig)

@dataclass
class FileLoggingConfig:
    """File logging configuration"""
    enabled: bool = True
    path: str = "logs/omnicpp.log"
    max_size: int = 10485760  # 10MB
    backup_count: int = 5
    rotation: str = "size"

@dataclass
class ConsoleLoggingConfig:
    """Console logging configuration"""
    enabled: bool = True
    color: bool = True

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: FileLoggingConfig = field(default_factory=FileLoggingConfig)
    console: ConsoleLoggingConfig = field(default_factory=ConsoleLoggingConfig)

@dataclass
class CoverageThresholds:
    """Coverage thresholds"""
    line: float = 80.0
    function: float = 80.0
    branch: float = 70.0

@dataclass
class CoverageConfig:
    """Code coverage configuration"""
    enabled: bool = False
    format: str = "lcov"
    output_dir: str = "coverage"
    threshold: CoverageThresholds = field(default_factory=CoverageThresholds)

@dataclass
class TestingConfig:
    """Testing configuration"""
    framework: str = "gtest"
    coverage: CoverageConfig = field(default_factory=CoverageConfig)
    parallel: bool = True
    timeout: int = 300

@dataclass
class ClangFormatConfig:
    """Clang-format configuration"""
    enabled: bool = True
    executable: Optional[str] = None
    style: str = "file"
    config_file: str = ".clang-format"

@dataclass
class CMakeFormatConfig:
    """CMake-format configuration"""
    enabled: bool = True
    executable: Optional[str] = None
    config_file: str = ".cmake-format"

@dataclass
class FormattingConfig:
    """Formatting configuration"""
    clang_format: ClangFormatConfig = field(default_factory=ClangFormatConfig)
    cmake_format: CMakeFormatConfig = field(default_factory=CMakeFormatConfig)

@dataclass
class ClangTidyConfig:
    """Clang-tidy configuration"""
    enabled: bool = True
    executable: Optional[str] = None
    config_file: str = ".clang-tidy"
    checks: List[str] = field(default_factory=list)
    warnings_as_errors: bool = False

@dataclass
class CppcheckConfig:
    """Cppcheck configuration"""
    enabled: bool = False
    executable: Optional[str] = None
    suppressions_file: Optional[str] = None

@dataclass
class LintingConfig:
    """Linting configuration"""
    clang_tidy: ClangTidyConfig = field(default_factory=ClangTidyConfig)
    cppcheck: CppcheckConfig = field(default_factory=CppcheckConfig)

@dataclass
class SanitizersConfig:
    """Sanitizer configuration"""
    address: bool = False
    memory: bool = False
    thread: bool = False
    undefined: bool = False

@dataclass
class HardeningConfig:
    """Hardening configuration"""
    stack_protector: bool = True
    fortify_source: bool = True
    relro: bool = True
    pie: bool = True

@dataclass
class SecurityConfig:
    """Security configuration"""
    sanitizers: SanitizersConfig = field(default_factory=SanitizersConfig)
    hardening: HardeningConfig = field(default_factory=HardeningConfig)

@dataclass
class WindowsPlatformConfig:
    """Windows platform configuration"""
    msvc_dev_cmd: Optional[str] = None
    msys2_root: Optional[str] = None

@dataclass
class LinuxPlatformConfig:
    """Linux platform configuration"""
    pkg_config_path: List[str] = field(default_factory=list)

@dataclass
class MacOSPlatformConfig:
    """macOS platform configuration"""
    xcode_path: Optional[str] = None

@dataclass
class PlatformConfig:
    """Platform configuration"""
    windows: WindowsPlatformConfig = field(default_factory=WindowsPlatformConfig)
    linux: LinuxPlatformConfig = field(default_factory=LinuxPlatformConfig)
    macos: MacOSPlatformConfig = field(default_factory=MacOSPlatformConfig)

@dataclass
class OptimizationsConfig:
    """Build optimization configuration"""
    lto: bool = False
    ipo: bool = False
    pgo: bool = False

@dataclass
class BuildConfigSettings:
    """Build configuration"""
    default_config: BuildConfig = BuildConfig.RELEASE
    parallel_jobs: int = 1
    generator: Optional[str] = None
    toolchain_file: Optional[str] = None
    cmake_args: List[str] = field(default_factory=list)
    compiler_args: List[str] = field(default_factory=list)
    linker_args: List[str] = field(default_factory=list)
    optimizations: OptimizationsConfig = field(default_factory=OptimizationsConfig)

@dataclass
class OmniCppConfig:
    """Main configuration class"""
    project: ProjectConfig
    build: BuildConfigSettings = field(default_factory=BuildConfigSettings)
    compilers: CompilersConfig = field(default_factory=CompilersConfig)
    package_managers: PackageManagersConfig = field(default_factory=PackageManagersConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    testing: TestingConfig = field(default_factory=TestingConfig)
    formatting: FormattingConfig = field(default_factory=FormattingConfig)
    linting: LintingConfig = field(default_factory=LintingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    platform: PlatformConfig = field(default_factory=PlatformConfig)
```

## Dependencies

### Internal Dependencies

- `DES-001` - ControllerConfig
- `DES-004` - Logging configuration schema

### External Dependencies

- `dataclasses` - Data structures
- `typing` - Type hints
- `enum` - Enumerations
- `json` - JSON parsing
- `jsonschema` - JSON schema validation

## Related Requirements

- REQ-005: Logging Configuration
- REQ-006: Error Handling & Exception Management
- REQ-007: Configuration Management
- REQ-008: Command Line Interface

## Related ADRs

- ADR-001: Python Build System Architecture

## Implementation Notes

### Configuration Loading

1. Load from JSON file
2. Validate against schema
3. Apply defaults
4. Override with environment variables
5. Override with command-line arguments

### Configuration Validation

- Use jsonschema for validation
- Provide clear error messages
- Validate paths exist
- Validate compiler versions

### Configuration Merging

- Deep merge configuration files
- User config overrides default config
- Command-line args override config files

### Configuration Caching

- Cache parsed configuration
- Watch for file changes
- Reload on change

## Usage Example

```python
from omni_scripts.config import OmniCppConfig, ProjectConfig
import json

# Load configuration from file
with open("config/project.json", "r") as f:
    config_data = json.load(f)

# Create configuration object
config = OmniCppConfig(**config_data)

# Access configuration
print(f"Project: {config.project.name} v{config.project.version}")
print(f"Build config: {config.build.default_config}")
print(f"Parallel jobs: {config.build.parallel_jobs}")
```
