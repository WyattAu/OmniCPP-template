# DES-017: CMake Configuration Schema

## Overview
Defines the CMake configuration schema for specifying CMake build settings, generators, and toolchain configurations.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CMake Configuration",
  "description": "CMake configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "cmake": {
      "type": "object",
      "description": "CMake configuration",
      "properties": {
        "minimum_version": {
          "type": "string",
          "default": "3.20",
          "description": "Minimum CMake version required"
        },
        "generator": {
          "type": "string",
          "description": "CMake generator (e.g., Ninja, Unix Makefiles, Visual Studio)"
        },
        "toolchain_file": {
          "type": "string",
          "description": "Path to CMake toolchain file"
        },
        "install_prefix": {
          "type": "string",
          "description": "Installation prefix"
        },
        "build_type": {
          "type": "string",
          "enum": ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"],
          "default": "Release",
          "description": "CMake build type"
        },
        "compile_definitions": {
          "type": "object",
          "description": "CMake compile definitions",
          "additionalProperties": {
            "type": "string"
          }
        },
        "compile_options": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "CMake compile options"
        },
        "link_options": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "CMake link options"
        },
        "cache_variables": {
          "type": "object",
          "description": "CMake cache variables",
          "additionalProperties": {
            "type": "string"
          }
        },
        "environment_variables": {
          "type": "object",
          "description": "Environment variables for CMake",
          "additionalProperties": {
            "type": "string"
          }
        }
      }
    },
    "presets": {
      "type": "object",
      "description": "CMake presets configuration",
      "properties": {
        "version": {
          "type": "integer",
          "default": 3,
          "description": "CMake presets version"
        },
        "include": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Files to include"
        },
        "build_presets": {
          "type": "object",
          "description": "Build presets",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "displayName": {
                "type": "string",
                "description": "Display name"
              },
              "description": {
                "type": "string",
                "description": "Description"
              },
              "binaryDir": {
                "type": "string",
                "description": "Binary directory"
              },
              "generator": {
                "type": "string",
                "description": "CMake generator"
              },
              "toolchainFile": {
                "type": "string",
                "description": "Toolchain file"
              },
              "toolchain": {
                "type": "string",
                "description": "Toolchain"
              },
              "cacheVariables": {
                "type": "object",
                "description": "Cache variables",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "environment": {
                "type": "object",
                "description": "Environment variables",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "cmakeExecutable": {
                "type": "string",
                "description": "CMake executable path"
              },
              "configurePreset": {
                "type": "string",
                "description": "Configure preset"
              },
              "inheritConfigurePreset": {
                "type": "string",
                "description": "Inherit configure preset"
              },
              "warnings": {
                "type": "object",
                "description": "Warnings",
                "properties": {
                  "dev": {
                    "type": "boolean",
                    "description": "Developer warnings"
                  },
                  "deprecated": {
                    "type": "boolean",
                    "description": "Deprecated warnings"
                  },
                  "uninitialized": {
                    "type": "boolean",
                    "description": "Uninitialized warnings"
                  },
                  "unusedCli": {
                    "type": "boolean",
                    "description": "Unused CLI warnings"
                  },
                  "systemVars": {
                    "type": "boolean",
                    "description": "System variables warnings"
                  }
                }
              },
              "errors": {
                "type": "object",
                "description": "Errors",
                "properties": {
                  "dev": {
                    "type": "boolean",
                    "description": "Developer errors"
                  },
                  "deprecated": {
                    "type": "boolean",
                    "description": "Deprecated errors"
                  }
                }
              },
              "debug": {
                "type": "object",
                "description": "Debug settings",
                "properties": {
                  "output": {
                    "type": "boolean",
                    "description": "Debug output"
                  },
                  "tryCompile": {
                    "type": "boolean",
                    "description": "Try compile"
                  },
                  "findPackage": {
                    "type": "boolean",
                    "description": "Find package"
                  }
                }
              }
            }
          }
        },
        "configure_presets": {
          "type": "object",
          "description": "Configure presets",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "displayName": {
                "type": "string",
                "description": "Display name"
              },
              "description": {
                "type": "string",
                "description": "Description"
              },
              "generator": {
                "type": "string",
                "description": "CMake generator"
              },
              "toolchainFile": {
                "type": "string",
                "description": "Toolchain file"
              },
              "toolchain": {
                "type": "string",
                "description": "Toolchain"
              },
              "cacheVariables": {
                "type": "object",
                "description": "Cache variables",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "environment": {
                "type": "object",
                "description": "Environment variables",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "cmakeExecutable": {
                "type": "string",
                "description": "CMake executable path"
              },
              "binaryDir": {
                "type": "string",
                "description": "Binary directory"
              },
              "inherits": {
                "type": "string",
                "description": "Inherit from preset"
              },
              "warnings": {
                "type": "object",
                "description": "Warnings",
                "properties": {
                  "dev": {
                    "type": "boolean",
                    "description": "Developer warnings"
                  },
                  "deprecated": {
                    "type": "boolean",
                    "description": "Deprecated warnings"
                  },
                  "uninitialized": {
                    "type": "boolean",
                    "description": "Uninitialized warnings"
                  },
                  "unusedCli": {
                    "type": "boolean",
                    "description": "Unused CLI warnings"
                  },
                  "systemVars": {
                    "type": "boolean",
                    "description": "System variables warnings"
                  }
                }
              },
              "errors": {
                "type": "object",
                "description": "Errors",
                "properties": {
                  "dev": {
                    "type": "boolean",
                    "description": "Developer errors"
                  },
                  "deprecated": {
                    "type": "boolean",
                    "description": "Deprecated errors"
                  }
                }
              },
              "debug": {
                "type": "object",
                "description": "Debug settings",
                "properties": {
                  "output": {
                    "type": "boolean",
                    "description": "Debug output"
                  },
                  "tryCompile": {
                    "type": "boolean",
                    "description": "Try compile"
                  },
                  "findPackage": {
                    "type": "boolean",
                    "description": "Find package"
                  }
                }
              }
            }
          }
        },
        "test_presets": {
          "type": "object",
          "description": "Test presets",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "displayName": {
                "type": "string",
                "description": "Display name"
              },
              "description": {
                "type": "string",
                "description": "Description"
              },
              "configuration": {
                "type": "string",
                "description": "Configuration"
              },
              "overwrite": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Overwrite options"
              },
              "output": {
                "type": "object",
                "description": "Output settings",
                "properties": {
                  "outputOnFailure": {
                    "type": "string",
                    "description": "Output on failure"
                  },
                  "outputPrefix": {
                    "type": "string",
                    "description": "Output prefix"
                  },
                  "shortProgress": {
                    "type": "boolean",
                    "description": "Short progress"
                  },
                  "verbosity": {
                    "type": "string",
                    "enum": ["default", "verbose", "extra"],
                    "description": "Verbosity level"
                  },
                  "debug": {
                    "type": "boolean",
                    "description": "Debug output"
                  }
                }
              },
              "filter": {
                "type": "string",
                "description": "Test filter"
              },
              "execution": {
                "type": "object",
                "description": "Execution settings",
                "properties": {
                  "stopOnFailure": {
                    "type": "boolean",
                    "description": "Stop on failure"
                  },
                  "enableFailover": {
                    "type": "boolean",
                    "description": "Enable failover"
                  },
                  "jobs": {
                    "type": "integer",
                    "description": "Number of jobs"
                  },
                  "resourceSpecFile": {
                    "type": "string",
                    "description": "Resource spec file"
                  },
                  "testLoad": {
                    "type": "integer",
                    "description": "Test load"
                  },
                  "showOnly": {
                    "type": "boolean",
                    "description": "Show only"
                  },
                  "repeat": {
                    "type": "integer",
                    "description": "Repeat count"
                  },
                  "shuffle": {
                    "type": "boolean",
                    "description": "Shuffle tests"
                  },
                  "rerunFailed": {
                    "type": "string",
                    "description": "Rerun failed tests"
                  }
                }
              }
            }
          }
        },
        "package_presets": {
          "type": "object",
          "description": "Package presets",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "displayName": {
                "type": "string",
                "description": "Display name"
              },
              "description": {
                "type": "string",
                "description": "Description"
              },
              "configurations": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Configurations"
              },
              "generators": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Generators"
              },
              "inheritEnvironments": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Inherit environments"
              },
              "variables": {
                "type": "object",
                "description": "Variables",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "environment": {
                "type": "object",
                "description": "Environment",
                "additionalProperties": {
                  "type": "string"
                }
              },
              "output": {
                "type": "object",
                "description": "Output settings",
                "properties": {
                  "outputDirectory": {
                    "type": "string",
                    "description": "Output directory"
                  },
                  "debugOutput": {
                    "type": "boolean",
                    "description": "Debug output"
                  }
                }
              }
            }
          }
        },
        "workflow_presets": {
          "type": "object",
          "description": "Workflow presets",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "displayName": {
                "type": "string",
                "description": "Display name"
              },
              "description": {
                "type": "string",
                "description": "Description"
              },
              "steps": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "enum": ["configure", "build", "test", "package"],
                      "description": "Step type"
                    },
                    "name": {
                      "type": "string",
                      "description": "Step name"
                    },
                    "preset": {
                      "type": "string",
                      "description": "Preset to use"
                    }
                  }
                },
                "description": "Workflow steps"
              }
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
import json

class CMakeBuildType(Enum):
    """CMake build types"""
    DEBUG = "Debug"
    RELEASE = "Release"
    RELWITHDEBINFO = "RelWithDebInfo"
    MINSIZEREL = "MinSizeRel"

class CMakeGenerator(Enum):
    """CMake generators"""
    NINJA = "Ninja"
    UNIX_MAKEFILES = "Unix Makefiles"
    NMAKE = "NMake Makefiles"
    MSVC = "Visual Studio"
    XCODE = "Xcode"

@dataclass
class CMakeConfig:
    """CMake configuration"""
    minimum_version: str = "3.20"
    generator: Optional[str] = None
    toolchain_file: Optional[str] = None
    install_prefix: Optional[str] = None
    build_type: CMakeBuildType = CMakeBuildType.RELEASE
    compile_definitions: Dict[str, str] = field(default_factory=dict)
    compile_options: List[str] = field(default_factory=list)
    link_options: List[str] = field(default_factory=list)
    cache_variables: Dict[str, str] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)

@dataclass
class CMakeWarnings:
    """CMake warnings configuration"""
    dev: bool = False
    deprecated: bool = False
    uninitialized: bool = False
    unused_cli: bool = False
    system_vars: bool = False

@dataclass
class CMakeErrors:
    """CMake errors configuration"""
    dev: bool = False
    deprecated: bool = False

@dataclass
class CMakeDebug:
    """CMake debug configuration"""
    output: bool = False
    try_compile: bool = False
    find_package: bool = False

@dataclass
class CMakeConfigurePreset:
    """CMake configure preset"""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    generator: Optional[str] = None
    toolchain_file: Optional[str] = None
    toolchain: Optional[str] = None
    cache_variables: Dict[str, str] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    cmake_executable: Optional[str] = None
    binary_dir: Optional[str] = None
    inherits: Optional[str] = None
    warnings: CMakeWarnings = field(default_factory=CMakeWarnings)
    errors: CMakeErrors = field(default_factory=CMakeErrors)
    debug: CMakeDebug = field(default_factory=CMakeDebug)

@dataclass
class CMakeBuildPreset:
    """CMake build preset"""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    binary_dir: Optional[str] = None
    generator: Optional[str] = None
    toolchain_file: Optional[str] = None
    toolchain: Optional[str] = None
    cache_variables: Dict[str, str] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    cmake_executable: Optional[str] = None
    configure_preset: Optional[str] = None
    inherit_configure_preset: Optional[str] = None
    warnings: CMakeWarnings = field(default_factory=CMakeWarnings)
    errors: CMakeErrors = field(default_factory=CMakeErrors)
    debug: CMakeDebug = field(default_factory=CMakeDebug)

@dataclass
class CMakeTestOutput:
    """CMake test output configuration"""
    output_on_failure: Optional[str] = None
    output_prefix: Optional[str] = None
    short_progress: bool = False
    verbosity: str = "default"
    debug: bool = False

@dataclass
class CMakeTestExecution:
    """CMake test execution configuration"""
    stop_on_failure: bool = False
    enable_failover: bool = False
    jobs: Optional[int] = None
    resource_spec_file: Optional[str] = None
    test_load: Optional[int] = None
    show_only: bool = False
    repeat: Optional[int] = None
    shuffle: bool = False
    rerun_failed: Optional[str] = None

@dataclass
class CMakeTestPreset:
    """CMake test preset"""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[str] = None
    overwrite: List[str] = field(default_factory=list)
    output: CMakeTestOutput = field(default_factory=CMakeTestOutput)
    filter: Optional[str] = None
    execution: CMakeTestExecution = field(default_factory=CMakeTestExecution)

@dataclass
class CMakePackageOutput:
    """CMake package output configuration"""
    output_directory: Optional[str] = None
    debug_output: bool = False

@dataclass
class CMakePackagePreset:
    """CMake package preset"""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    configurations: List[str] = field(default_factory=list)
    generators: List[str] = field(default_factory=list)
    inherit_environments: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    output: CMakePackageOutput = field(default_factory=CMakePackageOutput)

@dataclass
class CMakeWorkflowStep:
    """CMake workflow step"""
    type: str
    name: str
    preset: Optional[str] = None

@dataclass
class CMakeWorkflowPreset:
    """CMake workflow preset"""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    steps: List[CMakeWorkflowStep] = field(default_factory=list)

@dataclass
class CMakePresets:
    """CMake presets configuration"""
    version: int = 3
    include: List[str] = field(default_factory=list)
    build_presets: Dict[str, CMakeBuildPreset] = field(default_factory=dict)
    configure_presets: Dict[str, CMakeConfigurePreset] = field(default_factory=dict)
    test_presets: Dict[str, CMakeTestPreset] = field(default_factory=dict)
    package_presets: Dict[str, CMakePackagePreset] = field(default_factory=dict)
    workflow_presets: Dict[str, CMakeWorkflowPreset] = field(default_factory=dict)

class CMakeConfigManager:
    """CMake configuration manager"""

    def __init__(self, config: CMakeConfig) -> None:
        """Initialize CMake configuration manager"""
        self._config = config
        self._presets: Optional[CMakePresets] = None

    def load_presets(self, presets_file: str = "CMakePresets.json") -> CMakePresets:
        """Load CMake presets from file"""
        try:
            with open(presets_file, 'r') as f:
                data = json.load(f)

            return CMakePresets(**data)
        except (IOError, json.JSONDecodeError):
            return CMakePresets()

    def save_presets(self, presets: CMakePresets,
                   presets_file: str = "CMakePresets.json") -> bool:
        """Save CMake presets to file"""
        try:
            with open(presets_file, 'w') as f:
                json.dump(presets.__dict__, f, indent=2)
            return True
        except IOError:
            return False

    def generate_cmake_args(self, preset_name: str) -> List[str]:
        """Generate CMake arguments from preset"""
        if not self._presets:
            self._presets = self.load_presets()

        if preset_name not in self._presets.build_presets:
            return []

        preset = self._presets.build_presets[preset_name]
        args = []

        if preset.generator:
            args.extend(["-G", preset.generator])

        if preset.toolchain_file:
            args.extend(["-DCMAKE_TOOLCHAIN_FILE=" + preset.toolchain_file])

        if preset.toolchain:
            args.extend(["-DCMAKE_TOOLCHAIN=" + preset.toolchain])

        if preset.cache_variables:
            for key, value in preset.cache_variables.items():
                args.extend(["-D", f"{key}={value}"])

        if preset.environment:
            for key, value in preset.environment.items():
                args.extend(["-D", f"{key}={value}"])

        return args

    def generate_build_command(self, preset_name: str,
                          target: Optional[str] = None) -> List[str]:
        """Generate CMake build command"""
        args = ["--build", preset_name]

        if target:
            args.extend(["--target", target])

        return args
```

## Dependencies

### Internal Dependencies
- `DES-003` - Configuration schema
- `DES-011` - Toolchain configuration

### External Dependencies
- `json` - JSON parsing
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-022: CMake 4 Configuration
- REQ-023: Ninja Generator Default
- REQ-024: CMake Presets Cross-Platform

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### CMake Configuration
1. Load configuration from JSON file
2. Validate against schema
3. Apply defaults
4. Override with environment variables

### Presets Management
1. Load presets from CMakePresets.json
2. Generate CMake arguments from presets
3. Support preset inheritance
4. Validate preset configuration

### Build Configuration
1. Generate CMake configure command
2. Generate CMake build command
3. Generate CMake test command
4. Generate CMake package command

### Error Handling
- Handle missing presets
- Handle invalid preset configuration
- Provide clear error messages
- Log configuration errors

## Usage Example

```python
from omni_scripts.cmake_config import (
    CMakeConfig,
    CMakeConfigManager,
    CMakeBuildType,
    CMakeGenerator
)

# Create CMake configuration
config = CMakeConfig(
    minimum_version="3.20",
    generator="Ninja",
    build_type=CMakeBuildType.RELEASE,
    compile_definitions={
        "CMAKE_CXX_STANDARD": "23"
    }
)

# Create configuration manager
manager = CMakeConfigManager(config)

# Load presets
presets = manager.load_presets()
print(f"Loaded {len(presets.build_presets)} build presets")

# Generate CMake arguments
args = manager.generate_cmake_args("default")
print(f"CMake args: {' '.join(args)}")
```
