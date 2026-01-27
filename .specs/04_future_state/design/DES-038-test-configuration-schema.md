# DES-038: Test Configuration Schema

## Overview
Defines the test configuration schema for OmniCpp build system and C++ engine testing.

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Test Configuration Schema",
  "description": "Configuration schema for OmniCpp testing",
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "description": "Configuration version",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "test_suites": {
      "type": "array",
      "description": "Test suites configuration",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Test suite name"
          },
          "description": {
            "type": "string",
            "description": "Test suite description"
          },
          "category": {
            "type": "string",
            "enum": ["build_system", "compiler", "package_manager", "engine", "game", "logging", "utils"],
            "description": "Test suite category"
          },
          "scope": {
            "type": "string",
            "enum": ["unit", "integration", "system", "e2e"],
            "description": "Test suite scope"
          },
          "enabled": {
            "type": "boolean",
            "description": "Whether the test suite is enabled",
            "default": true
          },
          "tests": {
            "type": "array",
            "description": "Test names",
            "items": {
              "type": "string"
            }
          },
          "fixtures": {
            "type": "array",
            "description": "Fixture names",
            "items": {
              "type": "string"
            }
          },
          "setup_timeout": {
            "type": "number",
            "description": "Setup timeout in seconds",
            "minimum": 0,
            "default": 30.0
          },
          "teardown_timeout": {
            "type": "number",
            "description": "Teardown timeout in seconds",
            "minimum": 0,
            "default": 30.0
          },
          "test_timeout": {
            "type": "number",
            "description": "Test timeout in seconds",
            "minimum": 0,
            "default": 60.0
          },
          "parallel": {
            "type": "boolean",
            "description": "Whether tests can run in parallel",
            "default": false
          },
          "max_workers": {
            "type": "integer",
            "description": "Maximum number of parallel workers",
            "minimum": 1,
            "default": 1
          },
          "retry_on_failure": {
            "type": "boolean",
            "description": "Whether to retry failed tests",
            "default": false
          },
          "max_retries": {
            "type": "integer",
            "description": "Maximum number of retries",
            "minimum": 0,
            "default": 3
          },
          "continue_on_failure": {
            "type": "boolean",
            "description": "Whether to continue on test failure",
            "default": true
          }
        },
        "required": ["name", "category", "scope"]
      }
    },
    "fixtures": {
      "type": "array",
      "description": "Fixture configuration",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Fixture name"
          },
          "type": {
            "type": "string",
            "enum": ["base", "build_system", "compiler", "package_manager", "engine"],
            "description": "Fixture type"
          },
          "enabled": {
            "type": "boolean",
            "description": "Whether the fixture is enabled",
            "default": true
          },
          "dependencies": {
            "type": "array",
            "description": "Fixture dependencies",
            "items": {
              "type": "string"
            }
          },
          "setup_timeout": {
            "type": "number",
            "description": "Setup timeout in seconds",
            "minimum": 0,
            "default": 30.0
          },
          "teardown_timeout": {
            "type": "number",
            "description": "Teardown timeout in seconds",
            "minimum": 0,
            "default": 30.0
          },
          "cleanup_on_failure": {
            "type": "boolean",
            "description": "Whether to cleanup on failure",
            "default": true
          }
        },
        "required": ["name", "type"]
      }
    },
    "output": {
      "type": "object",
      "description": "Output configuration",
      "properties": {
        "format": {
          "type": "string",
          "enum": ["json", "xml", "html", "junit", "console"],
          "description": "Output format",
          "default": "console"
        },
        "directory": {
          "type": "string",
          "description": "Output directory",
          "default": "test_results"
        },
        "filename": {
          "type": "string",
          "description": "Output filename",
          "default": "test_results"
        },
        "verbose": {
          "type": "boolean",
          "description": "Verbose output",
          "default": false
        },
        "show_traceback": {
          "type": "boolean",
          "description": "Show traceback on failure",
          "default": true
        },
        "show_skipped": {
          "type": "boolean",
            "description": "Show skipped tests",
            "default": true
        },
        "color_output": {
          "type": "boolean",
          "description": "Color output",
          "default": true
        }
      }
    },
    "coverage": {
      "type": "object",
      "description": "Coverage configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether coverage is enabled",
          "default": false
        },
        "format": {
          "type": "string",
          "enum": ["json", "xml", "html", "lcov", "cobertura"],
          "description": "Coverage format",
          "default": "json"
        },
        "directory": {
          "type": "string",
          "description": "Coverage output directory",
          "default": "coverage"
        },
        "filename": {
          "type": "string",
          "description": "Coverage filename",
          "default": "coverage"
        },
        "minimum_coverage": {
          "type": "number",
          "description": "Minimum coverage percentage",
          "minimum": 0,
          "maximum": 100,
          "default": 80.0
        },
        "fail_on_low_coverage": {
          "type": "boolean",
          "description": "Whether to fail on low coverage",
          "default": false
        },
        "include": {
          "type": "array",
          "description": "Include patterns",
          "items": {
            "type": "string"
          }
        },
        "exclude": {
          "type": "array",
          "description": "Exclude patterns",
          "items": {
            "type": "string"
          }
        },
        "branch_coverage": {
          "type": "boolean",
          "description": "Whether to include branch coverage",
          "default": true
        },
        "line_coverage": {
          "type": "boolean",
          "description": "Whether to include line coverage",
          "default": true
        },
        "function_coverage": {
          "type": "boolean",
          "description": "Whether to include function coverage",
          "default": true
        }
      }
    },
    "reporting": {
      "type": "object",
      "description": "Reporting configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether reporting is enabled",
          "default": true
        },
        "format": {
          "type": "string",
          "enum": ["json", "xml", "html", "markdown"],
          "description": "Report format",
          "default": "json"
        },
        "directory": {
          "type": "string",
          "description": "Report output directory",
          "default": "reports"
        },
        "filename": {
          "type": "string",
          "description": "Report filename",
          "default": "test_report"
        },
        "include_statistics": {
          "type": "boolean",
          "description": "Include statistics in report",
          "default": true
        },
        "include_coverage": {
          "type": "boolean",
          "description": "Include coverage in report",
          "default": true
        },
        "include_history": {
          "type": "boolean",
          "description": "Include test history in report",
          "default": false
        },
        "include_trends": {
          "type": "boolean",
          "description": "Include test trends in report",
          "default": false
        }
      }
    },
    "environment": {
      "type": "object",
      "description": "Environment configuration",
      "properties": {
        "variables": {
          "type": "object",
          "description": "Environment variables",
          "additionalProperties": {
            "type": "string"
          }
        },
        "python_path": {
          "type": "string",
          "description": "Python path"
        },
        "cmake_path": {
          "type": "string",
          "description": "CMake path"
        },
        "compiler_path": {
          "type": "string",
          "description": "Compiler path"
        },
        "package_manager_path": {
          "type": "string",
          "description": "Package manager path"
        }
      }
    },
    "logging": {
      "type": "object",
      "description": "Logging configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether logging is enabled",
          "default": true
        },
        "level": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
          "description": "Log level",
          "default": "INFO"
        },
        "format": {
          "type": "string",
          "description": "Log format",
          "default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "file": {
          "type": "string",
          "description": "Log file path",
          "default": "test.log"
        },
        "console": {
          "type": "boolean",
          "description": "Whether to log to console",
          "default": true
        }
      }
    },
    "parallel": {
      "type": "object",
      "description": "Parallel execution configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether parallel execution is enabled",
          "default": false
        },
        "max_workers": {
          "type": "integer",
          "description": "Maximum number of workers",
          "minimum": 1,
          "default": 4
        },
        "worker_type": {
          "type": "string",
          "enum": ["process", "thread"],
          "description": "Worker type",
          "default": "process"
        }
      }
    },
    "timeout": {
      "type": "object",
      "description": "Timeout configuration",
      "properties": {
        "default": {
          "type": "number",
          "description": "Default timeout in seconds",
          "minimum": 0,
          "default": 60.0
        },
        "setup": {
          "type": "number",
          "description": "Setup timeout in seconds",
          "minimum": 0,
          "default": 30.0
        },
        "teardown": {
          "type": "number",
          "description": "Teardown timeout in seconds",
          "minimum": 0,
          "default": 30.0
        },
        "test": {
          "type": "number",
          "description": "Test timeout in seconds",
          "minimum": 0,
          "default": 60.0
        }
      }
    },
    "retry": {
      "type": "object",
      "description": "Retry configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether retry is enabled",
          "default": false
        },
        "max_retries": {
          "type": "integer",
          "description": "Maximum number of retries",
          "minimum": 0,
          "default": 3
        },
        "delay": {
          "type": "number",
          "description": "Delay between retries in seconds",
          "minimum": 0,
          "default": 1.0
        },
        "backoff": {
          "type": "boolean",
          "description": "Whether to use exponential backoff",
          "default": false
        }
      }
    },
    "filter": {
      "type": "object",
      "description": "Filter configuration",
      "properties": {
        "include": {
          "type": "array",
          "description": "Include patterns",
          "items": {
            "type": "string"
          }
        },
        "exclude": {
          "type": "array",
          "description": "Exclude patterns",
          "items": {
            "type": "string"
          }
        },
        "categories": {
          "type": "array",
          "description": "Include categories",
          "items": {
            "type": "string",
            "enum": ["build_system", "compiler", "package_manager", "engine", "game", "logging", "utils"]
          }
        },
        "scopes": {
          "type": "array",
          "description": "Include scopes",
          "items": {
            "type": "string",
            "enum": ["unit", "integration", "system", "e2e"]
          }
        },
        "tags": {
          "type": "array",
          "description": "Include tags",
          "items": {
            "type": "string"
          }
        }
      }
    }
  },
  "required": ["version"]
}
```

## Python Code

```python
"""
Test Configuration Schema for OmniCpp

This module defines the test configuration schema for testing the build system and C++ engine.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class TestScope(Enum):
    """Test scope"""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    E2E = "e2e"


class TestCategory(Enum):
    """Test category"""
    BUILD_SYSTEM = "build_system"
    COMPILER = "compiler"
    PACKAGE_MANAGER = "package_manager"
    ENGINE = "engine"
    GAME = "game"
    LOGGING = "logging"
    UTILS = "utils"


class OutputFormat(Enum):
    """Output format"""
    JSON = "json"
    XML = "xml"
    HTML = "html"
    JUNIT = "junit"
    CONSOLE = "console"


class CoverageFormat(Enum):
    """Coverage format"""
    JSON = "json"
    XML = "xml"
    HTML = "html"
    LCOV = "lcov"
    COBERTURA = "cobertura"


class ReportFormat(Enum):
    """Report format"""
    JSON = "json"
    XML = "xml"
    HTML = "html"
    MARKDOWN = "markdown"


class LogLevel(Enum):
    """Log level"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class WorkerType(Enum):
    """Worker type"""
    PROCESS = "process"
    THREAD = "thread"


class FixtureType(Enum):
    """Fixture type"""
    BASE = "base"
    BUILD_SYSTEM = "build_system"
    COMPILER = "compiler"
    PACKAGE_MANAGER = "package_manager"
    ENGINE = "engine"


@dataclass
class TestSuiteConfig:
    """Test suite configuration"""
    name: str
    category: TestCategory
    scope: TestScope
    description: str = ""
    enabled: bool = True
    tests: List[str] = field(default_factory=list)
    fixtures: List[str] = field(default_factory=list)
    setup_timeout: float = 30.0
    teardown_timeout: float = 30.0
    test_timeout: float = 60.0
    parallel: bool = False
    max_workers: int = 1
    retry_on_failure: bool = False
    max_retries: int = 3
    continue_on_failure: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert test suite config to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "scope": self.scope.value,
            "enabled": self.enabled,
            "tests": self.tests,
            "fixtures": self.fixtures,
            "setup_timeout": self.setup_timeout,
            "teardown_timeout": self.teardown_timeout,
            "test_timeout": self.test_timeout,
            "parallel": self.parallel,
            "max_workers": self.max_workers,
            "retry_on_failure": self.retry_on_failure,
            "max_retries": self.max_retries,
            "continue_on_failure": self.continue_on_failure
        }


@dataclass
class FixtureConfig:
    """Fixture configuration"""
    name: str
    type: FixtureType
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    setup_timeout: float = 30.0
    teardown_timeout: float = 30.0
    cleanup_on_failure: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert fixture config to dictionary"""
        return {
            "name": self.name,
            "type": self.type.value,
            "enabled": self.enabled,
            "dependencies": self.dependencies,
            "setup_timeout": self.setup_timeout,
            "teardown_timeout": self.teardown_timeout,
            "cleanup_on_failure": self.cleanup_on_failure
        }


@dataclass
class OutputConfig:
    """Output configuration"""
    format: OutputFormat = OutputFormat.CONSOLE
    directory: str = "test_results"
    filename: str = "test_results"
    verbose: bool = False
    show_traceback: bool = True
    show_skipped: bool = True
    color_output: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert output config to dictionary"""
        return {
            "format": self.format.value,
            "directory": self.directory,
            "filename": self.filename,
            "verbose": self.verbose,
            "show_traceback": self.show_traceback,
            "show_skipped": self.show_skipped,
            "color_output": self.color_output
        }


@dataclass
class CoverageConfig:
    """Coverage configuration"""
    enabled: bool = False
    format: CoverageFormat = CoverageFormat.JSON
    directory: str = "coverage"
    filename: str = "coverage"
    minimum_coverage: float = 80.0
    fail_on_low_coverage: bool = False
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)
    branch_coverage: bool = True
    line_coverage: bool = True
    function_coverage: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert coverage config to dictionary"""
        return {
            "enabled": self.enabled,
            "format": self.format.value,
            "directory": self.directory,
            "filename": self.filename,
            "minimum_coverage": self.minimum_coverage,
            "fail_on_low_coverage": self.fail_on_low_coverage,
            "include": self.include,
            "exclude": self.exclude,
            "branch_coverage": self.branch_coverage,
            "line_coverage": self.line_coverage,
            "function_coverage": self.function_coverage
        }


@dataclass
class ReportingConfig:
    """Reporting configuration"""
    enabled: bool = True
    format: ReportFormat = ReportFormat.JSON
    directory: str = "reports"
    filename: str = "test_report"
    include_statistics: bool = True
    include_coverage: bool = True
    include_history: bool = False
    include_trends: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert reporting config to dictionary"""
        return {
            "enabled": self.enabled,
            "format": self.format.value,
            "directory": self.directory,
            "filename": self.filename,
            "include_statistics": self.include_statistics,
            "include_coverage": self.include_coverage,
            "include_history": self.include_history,
            "include_trends": self.include_trends
        }


@dataclass
class EnvironmentConfig:
    """Environment configuration"""
    variables: Dict[str, str] = field(default_factory=dict)
    python_path: Optional[str] = None
    cmake_path: Optional[str] = None
    compiler_path: Optional[str] = None
    package_manager_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert environment config to dictionary"""
        return {
            "variables": self.variables,
            "python_path": self.python_path,
            "cmake_path": self.cmake_path,
            "compiler_path": self.compiler_path,
            "package_manager_path": self.package_manager_path
        }


@dataclass
class LoggingConfig:
    """Logging configuration"""
    enabled: bool = True
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "test.log"
    console: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert logging config to dictionary"""
        return {
            "enabled": self.enabled,
            "level": self.level.value,
            "format": self.format,
            "file": self.file,
            "console": self.console
        }


@dataclass
class ParallelConfig:
    """Parallel execution configuration"""
    enabled: bool = False
    max_workers: int = 4
    worker_type: WorkerType = WorkerType.PROCESS

    def to_dict(self) -> Dict[str, Any]:
        """Convert parallel config to dictionary"""
        return {
            "enabled": self.enabled,
            "max_workers": self.max_workers,
            "worker_type": self.worker_type.value
        }


@dataclass
class TimeoutConfig:
    """Timeout configuration"""
    default: float = 60.0
    setup: float = 30.0
    teardown: float = 30.0
    test: float = 60.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert timeout config to dictionary"""
        return {
            "default": self.default,
            "setup": self.setup,
            "teardown": self.teardown,
            "test": self.test
        }


@dataclass
class RetryConfig:
    """Retry configuration"""
    enabled: bool = False
    max_retries: int = 3
    delay: float = 1.0
    backoff: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert retry config to dictionary"""
        return {
            "enabled": self.enabled,
            "max_retries": self.max_retries,
            "delay": self.delay,
            "backoff": self.backoff
        }


@dataclass
class FilterConfig:
    """Filter configuration"""
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)
    categories: List[TestCategory] = field(default_factory=list)
    scopes: List[TestScope] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert filter config to dictionary"""
        return {
            "include": self.include,
            "exclude": self.exclude,
            "categories": [c.value for c in self.categories],
            "scopes": [s.value for s in self.scopes],
            "tags": self.tags
        }


@dataclass
class TestConfiguration:
    """Test configuration"""
    version: str
    test_suites: List[TestSuiteConfig] = field(default_factory=list)
    fixtures: List[FixtureConfig] = field(default_factory=list)
    output: OutputConfig = field(default_factory=OutputConfig)
    coverage: CoverageConfig = field(default_factory=CoverageConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    parallel: ParallelConfig = field(default_factory=ParallelConfig)
    timeout: TimeoutConfig = field(default_factory=TimeoutConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    filter: FilterConfig = field(default_factory=FilterConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Convert test configuration to dictionary"""
        return {
            "version": self.version,
            "test_suites": [ts.to_dict() for ts in self.test_suites],
            "fixtures": [f.to_dict() for f in self.fixtures],
            "output": self.output.to_dict(),
            "coverage": self.coverage.to_dict(),
            "reporting": self.reporting.to_dict(),
            "environment": self.environment.to_dict(),
            "logging": self.logging.to_dict(),
            "parallel": self.parallel.to_dict(),
            "timeout": self.timeout.to_dict(),
            "retry": self.retry.to_dict(),
            "filter": self.filter.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestConfiguration":
        """Create test configuration from dictionary"""
        return cls(
            version=data["version"],
            test_suites=[
                TestSuiteConfig(
                    name=ts["name"],
                    description=ts.get("description", ""),
                    category=TestCategory(ts["category"]),
                    scope=TestScope(ts["scope"]),
                    enabled=ts.get("enabled", True),
                    tests=ts.get("tests", []),
                    fixtures=ts.get("fixtures", []),
                    setup_timeout=ts.get("setup_timeout", 30.0),
                    teardown_timeout=ts.get("teardown_timeout", 30.0),
                    test_timeout=ts.get("test_timeout", 60.0),
                    parallel=ts.get("parallel", False),
                    max_workers=ts.get("max_workers", 1),
                    retry_on_failure=ts.get("retry_on_failure", False),
                    max_retries=ts.get("max_retries", 3),
                    continue_on_failure=ts.get("continue_on_failure", True)
                )
                for ts in data.get("test_suites", [])
            ],
            fixtures=[
                FixtureConfig(
                    name=f["name"],
                    type=FixtureType(f["type"]),
                    enabled=f.get("enabled", True),
                    dependencies=f.get("dependencies", []),
                    setup_timeout=f.get("setup_timeout", 30.0),
                    teardown_timeout=f.get("teardown_timeout", 30.0),
                    cleanup_on_failure=f.get("cleanup_on_failure", True)
                )
                for f in data.get("fixtures", [])
            ],
            output=OutputConfig(**data.get("output", {})),
            coverage=CoverageConfig(**data.get("coverage", {})),
            reporting=ReportingConfig(**data.get("reporting", {})),
            environment=EnvironmentConfig(**data.get("environment", {})),
            logging=LoggingConfig(**data.get("logging", {})),
            parallel=ParallelConfig(**data.get("parallel", {})),
            timeout=TimeoutConfig(**data.get("timeout", {})),
            retry=RetryConfig(**data.get("retry", {})),
            filter=FilterConfig(**data.get("filter", {}))
        )
```

## Dependencies

### Internal Dependencies
- `DES-037` - Test Fixture Design

### External Dependencies
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-060: Test Framework
- REQ-061: Test Fixtures
- REQ-062: Test Configuration

## Related ADRs
- ADR-004: Testing Architecture

## Implementation Notes

### Configuration Structure
1. Version control
2. Test suites configuration
3. Fixtures configuration
4. Output configuration
5. Coverage configuration
6. Reporting configuration
7. Environment configuration
8. Logging configuration
9. Parallel execution configuration
10. Timeout configuration
11. Retry configuration
12. Filter configuration

### Configuration Validation
1. JSON schema validation
2. Type validation
3. Range validation
4. Enum validation

### Configuration Loading
1. JSON file loading
2. Dictionary conversion
3. Default values
4. Error handling

## Usage Example

```python
from omni_scripts.testing import (
    TestConfiguration,
    TestSuiteConfig,
    FixtureConfig,
    TestCategory,
    TestScope,
    FixtureType
)

# Create test configuration
config = TestConfiguration(
    version="1.0.0",
    test_suites=[
        TestSuiteConfig(
            name="BuildSystemTests",
            category=TestCategory.BUILD_SYSTEM,
            scope=TestScope.INTEGRATION,
            tests=["test_build", "test_clean", "test_configure"],
            fixtures=["BuildSystem", "Compiler"],
            parallel=True,
            max_workers=4
        )
    ],
    fixtures=[
        FixtureConfig(
            name="BuildSystem",
            type=FixtureType.BUILD_SYSTEM,
            dependencies=["Compiler"]
        )
    ]
)

# Convert to dictionary
config_dict = config.to_dict()

# Save to JSON file
import json
with open("test_config.json", "w") as f:
    json.dump(config_dict, f, indent=2)

# Load from JSON file
with open("test_config.json", "r") as f:
    loaded_config = TestConfiguration.from_dict(json.load(f))
```
