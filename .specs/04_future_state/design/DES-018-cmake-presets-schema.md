# DES-018: CMake Presets Schema

## Overview
Defines the CMake Presets schema for cross-platform build configurations.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CMake Presets",
  "description": "CMake Presets schema for OmniCppController",
  "type": "object",
  "properties": {
    "version": {
      "type": "integer",
      "minimum": 1,
      "default": 3,
      "description": "CMake presets schema version"
    },
    "include": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Files to include"
    },
    "vendor": {
      "type": "object",
      "description": "Vendor-specific presets",
      "additionalProperties": {
        "type": "object"
      }
    },
    "buildPresets": {
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
          "architecture": {
            "type": "string",
            "description": "Target architecture"
          },
          "inherits": {
            "type": "string",
            "description": "Inherit from preset"
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
    "configurePresets": {
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
          "architecture": {
            "type": "string",
            "description": "Target architecture"
          },
          "inherits": {
            "type": "string",
            "description": "Inherit from preset"
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
          }
        }
      }
    },
    "testPresets": {
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
          "inherits": {
            "type": "string",
            "description": "Inherit from preset"
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
          }
        }
      }
    },
    "packagePresets": {
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
          "inherits": {
            "type": "string",
            "description": "Inherit from preset"
          },
          "environment": {
            "type": "object",
            "description": "Environment",
            "additionalProperties": {
              "type": "string"
            }
          },
          "cmakeExecutable": {
            "type": "string",
            "description": "CMake executable path"
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
    "workflowPresets": {
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
```

## Dependencies

### Internal Dependencies
- `DES-017` - CMake configuration schema

### External Dependencies
- `json` - JSON parsing
- `typing` - Type hints
- `dataclasses` - Data structures

## Related Requirements
- REQ-022: CMake 4 Configuration
- REQ-023: Ninja Generator Default
- REQ-024: CMake Presets Cross-Platform

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Preset Structure
1. Use CMake Presets v3 format
2. Support preset inheritance
3. Include vendor presets
4. Support multiple preset types

### Cross-Platform Support
1. Define presets for each platform
2. Use architecture-specific settings
3. Use platform-specific generators
4. Handle platform-specific paths

### Preset Validation
1. Validate preset structure
2. Check for circular inheritance
3. Validate required fields
4. Check for invalid values

### Preset Generation
1. Generate presets from configuration
2. Support preset inheritance
3. Generate platform-specific presets
4. Generate vendor presets

## Usage Example

```python
from omni_scripts.cmake_presets import (
    CMakePresets,
    CMakeBuildPreset,
    CMakeGenerator
)

# Create presets
presets = CMakePresets(
    version=3,
    build_presets={
        "debug": CMakeBuildPreset(
            name="debug",
            display_name="Debug Build",
            description="Debug configuration",
            build_type="Debug",
            generator=CMakeGenerator.NINJA
        ),
        "release": CMakeBuildPreset(
            name="release",
            display_name="Release Build",
            description="Release configuration",
            build_type="Release",
            generator=CMakeGenerator.NINJA
        )
    }
)

# Save presets
presets.save("CMakePresets.json")
print("Presets saved successfully")
```
