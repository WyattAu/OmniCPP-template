# DES-019: Build Configuration Schema

## Overview
Defines the build configuration schema for specifying build settings, targets, and optimization options.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Build Configuration",
  "description": "Build configuration schema for OmniCppController",
  "type": "object",
  "properties": {
    "targets": {
      "type": "object",
      "description": "Build targets",
      "properties": {
        "all": {
          "type": "object",
          "description": "Build all targets",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable all target"
            },
            "dependencies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Dependencies for all target"
            },
            "options": {
              "type": "object",
              "description": "Build options",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        },
        "engine": {
          "type": "object",
          "description": "Build engine target",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable engine target"
            },
            "dependencies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Dependencies for engine target"
            },
            "options": {
              "type": "object",
              "description": "Build options",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        },
        "game": {
          "type": "object",
          "description": "Build game target",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable game target"
            },
            "dependencies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Dependencies for game target"
            },
            "options": {
              "type": "object",
              "description": "Build options",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        },
        "tests": {
          "type": "object",
          "description": "Build tests target",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable tests target"
            },
            "dependencies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Dependencies for tests target"
            },
            "options": {
              "type": "object",
              "description": "Build options",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        },
        "examples": {
          "type": "object",
          "description": "Build examples target",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": true,
              "description": "Enable examples target"
            },
            "dependencies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Dependencies for examples target"
            },
            "options": {
              "type": "object",
              "description": "Build options",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        }
      }
    },
    "configurations": {
      "type": "object",
      "description": "Build configurations",
      "properties": {
        "debug": {
          "type": "object",
          "description": "Debug configuration",
          "properties": {
            "type": {
              "type": "string",
              "default": "Debug",
              "description": "CMake build type"
            },
            "optimization": {
              "type": "string",
              "default": "O0",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": true,
              "description": "Generate debug symbols"
            },
            "defines": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Preprocessor definitions"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Warning flags"
            }
          }
        },
        "release": {
          "type": "object",
          "description": "Release configuration",
          "properties": {
            "type": {
              "type": "string",
              "default": "Release",
              "description": "CMake build type"
            },
            "optimization": {
              "type": "string",
              "default": "O3",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "defines": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Preprocessor definitions"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Warning flags"
            }
          }
        },
        "relwithdebinfo": {
          "type": "object",
          "description": "Release with debug info configuration",
          "properties": {
            "type": {
              "type": "string",
              "default": "RelWithDebInfo",
              "description": "CMake build type"
            },
            "optimization": {
              "type": "string",
              "default": "O2",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": true,
              "description": "Generate debug symbols"
            },
            "defines": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Preprocessor definitions"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Warning flags"
            }
          }
        },
        "minsizerel": {
          "type": "object",
          "description": "Minimum size release configuration",
          "properties": {
            "type": {
              "type": "string",
              "default": "MinSizeRel",
              "description": "CMake build type"
            },
            "optimization": {
              "type": "string",
              "default": "Os",
              "description": "Optimization level"
            },
            "debug_symbols": {
              "type": "boolean",
              "default": false,
              "description": "Generate debug symbols"
            },
            "defines": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Preprocessor definitions"
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Warning flags"
            }
          }
        }
      }
    },
    "optimizations": {
      "type": "object",
      "description": "Build optimizations",
      "properties": {
        "lto": {
          "type": "object",
          "description": "Link Time Optimization",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable LTO"
            },
            "type": {
              "type": "string",
              "enum": ["full", "thin", "off"],
              "default": "off",
              "description": "LTO type"
            },
            "jobs": {
              "type": "integer",
              "default": 1,
              "description": "Number of parallel LTO jobs"
            }
          }
        },
        "ipo": {
          "type": "object",
          "description": "Interprocedural Optimization",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable IPO"
            },
            "type": {
              "type": "string",
              "enum": ["full", "single", "off"],
              "default": "off",
              "description": "IPO type"
            }
          }
        },
        "pgo": {
          "type": "object",
          "description": "Profile Guided Optimization",
          "properties": {
            "enabled": {
              "type": "boolean",
              "default": false,
              "description": "Enable PGO"
            },
            "profile_data": {
              "type": "string",
              "description": "Path to profile data"
            },
            "use_profile": {
              "type": "boolean",
              "default": false,
              "description": "Use existing profile"
            }
          }
        }
      }
    },
    "parallel": {
      "type": "object",
      "description": "Parallel build configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable parallel builds"
        },
        "jobs": {
          "type": "integer",
          "default": 1,
          "description": "Number of parallel jobs"
        },
        "load_balance": {
          "type": "string",
          "enum": ["auto", "none", "target"],
          "default": "auto",
          "description": "Load balancing strategy"
        }
      }
    },
    "caching": {
      "type": "object",
      "description": "Build caching configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable build caching"
        },
        "type": {
          "type": "string",
          "enum": ["ccache", "sccache", "none"],
          "default": "ccache",
          "description": "Cache type"
        },
        "directory": {
          "type": "string",
          "description": "Cache directory"
        },
        "max_size": {
          "type": "integer",
          "default": 5368709120,
          "description": "Maximum cache size in bytes (5GB)"
        },
        "compression": {
          "type": "boolean",
          "default": true,
          "description": "Enable cache compression"
        }
      }
    },
    "incremental": {
      "type": "object",
      "description": "Incremental build configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": false,
          "description": "Enable incremental builds"
        },
        "type": {
          "type": "string",
          "enum": ["header", "target", "custom"],
          "default": "target",
          "description": "Incremental type"
        },
        "directory": {
          "type": "string",
          "description": "Incremental build directory"
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

class BuildTarget(Enum):
    """Build targets"""
    ALL = "all"
    ENGINE = "engine"
    GAME = "game"
    TESTS = "tests"
    EXAMPLES = "examples"

class BuildConfigType(Enum):
    """Build configuration types"""
    DEBUG = "debug"
    RELEASE = "release"
    RELWITHDEBINFO = "relwithdebinfo"
    MINSIZEREL = "minsizerel"

class OptimizationLevel(Enum):
    """Optimization levels"""
    O0 = "O0"
    O1 = "O1"
    O2 = "O2"
    O3 = "O3"
    Os = "Os"
    Oz = "Oz"

class LTOType(Enum):
    """LTO types"""
    FULL = "full"
    THIN = "thin"
    OFF = "off"

class IPOType(Enum):
    """IPO types"""
    FULL = "full"
    SINGLE = "single"
    OFF = "off"

class CacheType(Enum):
    """Cache types"""
    CCACHE = "ccache"
    SCCACHE = "sccache"
    NONE = "none"

class IncrementalType(Enum):
    """Incremental types"""
    HEADER = "header"
    TARGET = "target"
    CUSTOM = "custom"

@dataclass
class TargetConfig:
    """Target configuration"""
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    options: Dict[str, str] = field(default_factory=dict)

@dataclass
class BuildConfiguration:
    """Build configuration"""
    type: str
    optimization: OptimizationLevel = OptimizationLevel.O2
    debug_symbols: bool = False
    defines: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

@dataclass
class LTOConfig:
    """LTO configuration"""
    enabled: bool = False
    type: LTOType = LTOType.OFF
    jobs: int = 1

@dataclass
class IPOConfig:
    """IPO configuration"""
    enabled: bool = False
    type: IPOType = IPOType.OFF

@dataclass
class PGOConfig:
    """PGO configuration"""
    enabled: bool = False
    profile_data: Optional[str] = None
    use_profile: bool = False

@dataclass
class ParallelConfig:
    """Parallel build configuration"""
    enabled: bool = True
    jobs: int = 1
    load_balance: str = "auto"

@dataclass
class CacheConfig:
    """Cache configuration"""
    enabled: bool = True
    type: CacheType = CacheType.CCACHE
    directory: Optional[str] = None
    max_size: int = 5368709120  # 5GB
    compression: bool = True

@dataclass
class IncrementalConfig:
    """Incremental build configuration"""
    enabled: bool = False
    type: IncrementalType = IncrementalType.TARGET
    directory: Optional[str] = None

@dataclass
class BuildConfigurationSchema:
    """Main build configuration schema"""
    targets: Dict[str, TargetConfig] = field(default_factory=lambda: {
        "all": TargetConfig(),
        "engine": TargetConfig(),
        "game": TargetConfig(),
        "tests": TargetConfig(),
        "examples": TargetConfig()
    })
    configurations: Dict[str, BuildConfiguration] = field(default_factory=lambda: {
        "debug": BuildConfiguration(
            type="Debug",
            optimization=OptimizationLevel.O0,
            debug_symbols=True
        ),
        "release": BuildConfiguration(
            type="Release",
            optimization=OptimizationLevel.O3,
            debug_symbols=False
        ),
        "relwithdebinfo": BuildConfiguration(
            type="RelWithDebInfo",
            optimization=OptimizationLevel.O2,
            debug_symbols=True
        ),
        "minsizerel": BuildConfiguration(
            type="MinSizeRel",
            optimization=OptimizationLevel.Os,
            debug_symbols=False
        )
    })
    optimizations: Dict[str, Any] = field(default_factory=lambda: {
        "lto": LTOConfig(),
        "ipo": IPOConfig(),
        "pgo": PGOConfig()
    })
    parallel: ParallelConfig = field(default_factory=ParallelConfig)
    caching: CacheConfig = field(default_factory=CacheConfig)
    incremental: IncrementalConfig = field(default_factory=IncrementalConfig)
```

## Dependencies

### Internal Dependencies
- `DES-003` - Configuration schema
- `DES-017` - CMake configuration schema

### External Dependencies
- `dataclasses` - Data structures
- `typing` - Type hints
- `enum` - Enumerations
- `json` - JSON parsing

## Related Requirements
- REQ-026: Build Optimization & Caching
- REQ-027: Parallel Build Support

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Build Configuration
1. Load configuration from JSON file
2. Validate against schema
3. Apply defaults
4. Override with environment variables

### Target Management
1. Define build targets
2. Specify target dependencies
3. Configure target-specific options
4. Support target-specific builds

### Optimization Configuration
1. Configure LTO settings
2. Configure IPO settings
3. Configure PGO settings
4. Validate optimization compatibility

### Parallel Build
1. Detect CPU core count
2. Configure parallel jobs
3. Implement load balancing
4. Handle dependencies

### Caching Strategy
1. Configure cache type
2. Set cache directory
3. Configure cache size limits
4. Enable compression

## Usage Example

```python
from omni_scripts.build_config import (
    BuildConfigurationSchema,
    BuildConfiguration,
    OptimizationLevel,
    LTOConfig,
    ParallelConfig
)

# Create build configuration
config = BuildConfigurationSchema(
    configurations={
        "release": BuildConfiguration(
            type="Release",
            optimization=OptimizationLevel.O3,
            debug_symbols=False
        )
    },
    optimizations={
        "lto": LTOConfig(
            enabled=True,
            type=LTOType.FULL,
            jobs=4
        )
    },
    parallel=ParallelConfig(
        enabled=True,
        jobs=8
    )
)

# Get release configuration
release_config = config.configurations["release"]
print(f"Build type: {release_config.type}")
print(f"Optimization: {release_config.optimization}")
```
