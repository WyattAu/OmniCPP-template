# DES-039: Coverage Report Schema

## Overview
Defines the coverage report schema for OmniCpp build system and C++ engine testing.

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Coverage Report Schema",
  "description": "Coverage report schema for OmniCpp testing",
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "description": "Coverage report version",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "timestamp": {
      "type": "string",
      "description": "Report timestamp in ISO 8601 format",
      "format": "date-time"
    },
    "summary": {
      "type": "object",
      "description": "Coverage summary",
      "properties": {
        "line_coverage": {
          "type": "number",
          "description": "Line coverage percentage",
          "minimum": 0,
          "maximum": 100
        },
        "branch_coverage": {
          "type": "number",
          "description": "Branch coverage percentage",
          "minimum": 0,
          "maximum": 100
        },
        "function_coverage": {
          "type": "number",
          "description": "Function coverage percentage",
          "minimum": 0,
          "maximum": 100
        },
        "total_lines": {
          "type": "integer",
          "description": "Total number of lines",
          "minimum": 0
        },
        "covered_lines": {
          "type": "integer",
          "description": "Number of covered lines",
          "minimum": 0
        },
        "total_branches": {
          "type": "integer",
          "description": "Total number of branches",
          "minimum": 0
        },
        "covered_branches": {
          "type": "integer",
          "description": "Number of covered branches",
          "minimum": 0
        },
        "total_functions": {
          "type": "integer",
          "description": "Total number of functions",
          "minimum": 0
        },
        "covered_functions": {
          "type": "integer",
          "description": "Number of covered functions",
          "minimum": 0
        },
        "threshold_met": {
          "type": "boolean",
          "description": "Whether coverage threshold is met"
        }
      },
      "required": ["line_coverage", "branch_coverage", "function_coverage"]
    },
    "files": {
      "type": "array",
      "description": "File coverage data",
      "items": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "File path"
          },
          "language": {
            "type": "string",
            "description": "Programming language"
          },
          "line_coverage": {
            "type": "number",
            "description": "Line coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "branch_coverage": {
            "type": "number",
            "description": "Branch coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "function_coverage": {
            "type": "number",
            "description": "Function coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "total_lines": {
            "type": "integer",
            "description": "Total number of lines",
            "minimum": 0
          },
          "covered_lines": {
            "type": "integer",
            "description": "Number of covered lines",
            "minimum": 0
          },
          "total_branches": {
            "type": "integer",
            "description": "Total number of branches",
            "minimum": 0
          },
          "covered_branches": {
            "type": "integer",
            "description": "Number of covered branches",
            "minimum": 0
          },
          "total_functions": {
            "type": "integer",
            "description": "Total number of functions",
            "minimum": 0
          },
          "covered_functions": {
            "type": "integer",
            "description": "Number of covered functions",
            "minimum": 0
          },
          "lines": {
            "type": "array",
            "description": "Line coverage data",
            "items": {
              "type": "object",
              "properties": {
                "line_number": {
                  "type": "integer",
                  "description": "Line number",
                  "minimum": 1
                },
                "execution_count": {
                  "type": "integer",
                  "description": "Execution count",
                  "minimum": 0
                },
                "covered": {
                  "type": "boolean",
                  "description": "Whether the line is covered"
                },
                "code": {
                  "type": "string",
                  "description": "Source code line"
                }
              },
              "required": ["line_number", "covered"]
            }
          },
          "branches": {
            "type": "array",
            "description": "Branch coverage data",
            "items": {
              "type": "object",
              "properties": {
                "line_number": {
                  "type": "integer",
                  "description": "Line number",
                  "minimum": 1
                },
                "branch_number": {
                  "type": "integer",
                  "description": "Branch number",
                  "minimum": 0
                },
                "covered": {
                  "type": "boolean",
                  "description": "Whether the branch is covered"
                },
                "execution_count": {
                  "type": "integer",
                  "description": "Execution count",
                  "minimum": 0
                }
              },
              "required": ["line_number", "branch_number", "covered"]
            }
          },
          "functions": {
            "type": "array",
            "description": "Function coverage data",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Function name"
                },
                "start_line": {
                  "type": "integer",
                  "description": "Start line number",
                  "minimum": 1
                },
                "end_line": {
                  "type": "integer",
                  "description": "End line number",
                  "minimum": 1
                },
                "covered": {
                  "type": "boolean",
                  "description": "Whether the function is covered"
                },
                "execution_count": {
                  "type": "integer",
                  "description": "Execution count",
                  "minimum": 0
                }
              },
              "required": ["name", "start_line", "end_line", "covered"]
            }
          }
        },
        "required": ["path", "line_coverage"]
      }
    },
    "directories": {
      "type": "array",
      "description": "Directory coverage data",
      "items": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "Directory path"
          },
          "line_coverage": {
            "type": "number",
            "description": "Line coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "branch_coverage": {
            "type": "number",
            "description": "Branch coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "function_coverage": {
            "type": "number",
            "description": "Function coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "total_lines": {
            "type": "integer",
            "description": "Total number of lines",
            "minimum": 0
          },
          "covered_lines": {
            "type": "integer",
            "description": "Number of covered lines",
            "minimum": 0
          },
          "total_branches": {
            "type": "integer",
            "description": "Total number of branches",
            "minimum": 0
          },
          "covered_branches": {
            "type": "integer",
            "description": "Number of covered branches",
            "minimum": 0
          },
          "total_functions": {
            "type": "integer",
            "description": "Total number of functions",
            "minimum": 0
          },
          "covered_functions": {
            "type": "integer",
            "description": "Number of covered functions",
            "minimum": 0
          },
          "files": {
            "type": "array",
            "description": "File paths in directory",
            "items": {
              "type": "string"
            }
          }
        },
        "required": ["path", "line_coverage"]
      }
    },
    "modules": {
      "type": "array",
      "description": "Module coverage data",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Module name"
          },
          "path": {
            "type": "string",
            "description": "Module path"
          },
          "line_coverage": {
            "type": "number",
            "description": "Line coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "branch_coverage": {
            "type": "number",
            "description": "Branch coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "function_coverage": {
            "type": "number",
            "description": "Function coverage percentage",
            "minimum": 0,
            "maximum": 100
          },
          "total_lines": {
            "type": "integer",
            "description": "Total number of lines",
            "minimum": 0
          },
          "covered_lines": {
            "type": "integer",
            "description": "Number of covered lines",
            "minimum": 0
          },
          "total_branches": {
            "type": "integer",
            "description": "Total number of branches",
            "minimum": 0
          },
          "covered_branches": {
            "type": "integer",
            "description": "Number of covered branches",
            "minimum": 0
          },
          "total_functions": {
            "type": "integer",
            "description": "Total number of functions",
            "minimum": 0
          },
          "covered_functions": {
            "type": "integer",
            "description": "Number of covered functions",
            "minimum": 0
          },
          "files": {
            "type": "array",
            "description": "File paths in module",
            "items": {
              "type": "string"
            }
          }
        },
        "required": ["name", "line_coverage"]
      }
    },
    "uncovered_lines": {
      "type": "array",
      "description": "Uncovered lines",
      "items": {
        "type": "object",
        "properties": {
          "file": {
            "type": "string",
            "description": "File path"
          },
          "line_number": {
            "type": "integer",
            "description": "Line number",
            "minimum": 1
          },
          "code": {
            "type": "string",
            "description": "Source code line"
          }
        },
        "required": ["file", "line_number"]
      }
    },
    "uncovered_branches": {
      "type": "array",
      "description": "Uncovered branches",
      "items": {
        "type": "object",
        "properties": {
          "file": {
            "type": "string",
            "description": "File path"
          },
          "line_number": {
            "type": "integer",
            "description": "Line number",
            "minimum": 1
          },
          "branch_number": {
            "type": "integer",
            "description": "Branch number",
            "minimum": 0
          }
        },
        "required": ["file", "line_number", "branch_number"]
      }
    },
    "uncovered_functions": {
      "type": "array",
      "description": "Uncovered functions",
      "items": {
        "type": "object",
        "properties": {
          "file": {
            "type": "string",
            "description": "File path"
          },
          "function_name": {
            "type": "string",
            "description": "Function name"
          },
          "start_line": {
            "type": "integer",
            "description": "Start line number",
            "minimum": 1
          },
          "end_line": {
            "type": "integer",
            "description": "End line number",
            "minimum": 1
          }
        },
        "required": ["file", "function_name", "start_line", "end_line"]
      }
    },
    "thresholds": {
      "type": "object",
      "description": "Coverage thresholds",
      "properties": {
        "line_threshold": {
          "type": "number",
          "description": "Line coverage threshold",
          "minimum": 0,
          "maximum": 100
        },
        "branch_threshold": {
          "type": "number",
          "description": "Branch coverage threshold",
          "minimum": 0,
          "maximum": 100
        },
        "function_threshold": {
          "type": "number",
          "description": "Function coverage threshold",
          "minimum": 0,
          "maximum": 100
        },
        "fail_on_low_coverage": {
          "type": "boolean",
          "description": "Whether to fail on low coverage"
        }
      },
      "required": ["line_threshold", "branch_threshold", "function_threshold"]
    },
    "metadata": {
      "type": "object",
      "description": "Coverage report metadata",
      "properties": {
        "generator": {
          "type": "string",
          "description": "Coverage report generator"
        },
        "generator_version": {
          "type": "string",
          "description": "Generator version"
        },
        "test_suite": {
          "type": "string",
          "description": "Test suite name"
        },
        "test_run_id": {
          "type": "string",
          "description": "Test run ID"
        },
        "build_type": {
          "type": "string",
          "description": "Build type"
        },
        "compiler": {
          "type": "string",
          "description": "Compiler used"
        },
        "platform": {
          "type": "string",
          "description": "Platform"
        },
        "architecture": {
          "type": "string",
          "description": "Architecture"
        }
      }
    }
  },
  "required": ["version", "timestamp", "summary"]
}
```

## Python Code

```python
"""
Coverage Report Schema for OmniCpp

This module defines the coverage report schema for testing the build system and C++ engine.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CoverageFormat(Enum):
    """Coverage format"""
    JSON = "json"
    XML = "xml"
    HTML = "html"
    LCOV = "lcov"
    COBERTURA = "cobertura"


@dataclass
class LineCoverage:
    """Line coverage data"""
    line_number: int
    covered: bool
    execution_count: int = 0
    code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert line coverage to dictionary"""
        return {
            "line_number": self.line_number,
            "execution_count": self.execution_count,
            "covered": self.covered,
            "code": self.code
        }


@dataclass
class BranchCoverage:
    """Branch coverage data"""
    line_number: int
    branch_number: int
    covered: bool
    execution_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert branch coverage to dictionary"""
        return {
            "line_number": self.line_number,
            "branch_number": self.branch_number,
            "covered": self.covered,
            "execution_count": self.execution_count
        }


@dataclass
class FunctionCoverage:
    """Function coverage data"""
    name: str
    start_line: int
    end_line: int
    covered: bool
    execution_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert function coverage to dictionary"""
        return {
            "name": self.name,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "covered": self.covered,
            "execution_count": self.execution_count
        }


@dataclass
class FileCoverage:
    """File coverage data"""
    path: str
    line_coverage: float
    language: str = ""
    branch_coverage: float = 0.0
    function_coverage: float = 0.0
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    lines: List[LineCoverage] = field(default_factory=list)
    branches: List[BranchCoverage] = field(default_factory=list)
    functions: List[FunctionCoverage] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert file coverage to dictionary"""
        return {
            "path": self.path,
            "language": self.language,
            "line_coverage": self.line_coverage,
            "branch_coverage": self.branch_coverage,
            "function_coverage": self.function_coverage,
            "total_lines": self.total_lines,
            "covered_lines": self.covered_lines,
            "total_branches": self.total_branches,
            "covered_branches": self.covered_branches,
            "total_functions": self.total_functions,
            "covered_functions": self.covered_functions,
            "lines": [line.to_dict() for line in self.lines],
            "branches": [branch.to_dict() for branch in self.branches],
            "functions": [func.to_dict() for func in self.functions]
        }


@dataclass
class DirectoryCoverage:
    """Directory coverage data"""
    path: str
    line_coverage: float
    branch_coverage: float = 0.0
    function_coverage: float = 0.0
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    files: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert directory coverage to dictionary"""
        return {
            "path": self.path,
            "line_coverage": self.line_coverage,
            "branch_coverage": self.branch_coverage,
            "function_coverage": self.function_coverage,
            "total_lines": self.total_lines,
            "covered_lines": self.covered_lines,
            "total_branches": self.total_branches,
            "covered_branches": self.covered_branches,
            "total_functions": self.total_functions,
            "covered_functions": self.covered_functions,
            "files": self.files
        }


@dataclass
class ModuleCoverage:
    """Module coverage data"""
    name: str
    path: str
    line_coverage: float
    branch_coverage: float = 0.0
    function_coverage: float = 0.0
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    files: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert module coverage to dictionary"""
        return {
            "name": self.name,
            "path": self.path,
            "line_coverage": self.line_coverage,
            "branch_coverage": self.branch_coverage,
            "function_coverage": self.function_coverage,
            "total_lines": self.total_lines,
            "covered_lines": self.covered_lines,
            "total_branches": self.total_branches,
            "covered_branches": self.covered_branches,
            "total_functions": self.total_functions,
            "covered_functions": self.covered_functions,
            "files": self.files
        }


@dataclass
class UncoveredLine:
    """Uncovered line data"""
    file: str
    line_number: int
    code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert uncovered line to dictionary"""
        return {
            "file": self.file,
            "line_number": self.line_number,
            "code": self.code
        }


@dataclass
class UncoveredBranch:
    """Uncovered branch data"""
    file: str
    line_number: int
    branch_number: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert uncovered branch to dictionary"""
        return {
            "file": self.file,
            "line_number": self.line_number,
            "branch_number": self.branch_number
        }


@dataclass
class UncoveredFunction:
    """Uncovered function data"""
    file: str
    function_name: str
    start_line: int
    end_line: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert uncovered function to dictionary"""
        return {
            "file": self.file,
            "function_name": self.function_name,
            "start_line": self.start_line,
            "end_line": self.end_line
        }


@dataclass
class CoverageSummary:
    """Coverage summary"""
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    threshold_met: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert coverage summary to dictionary"""
        return {
            "line_coverage": self.line_coverage,
            "branch_coverage": self.branch_coverage,
            "function_coverage": self.function_coverage,
            "total_lines": self.total_lines,
            "covered_lines": self.covered_lines,
            "total_branches": self.total_branches,
            "covered_branches": self.covered_branches,
            "total_functions": self.total_functions,
            "covered_functions": self.covered_functions,
            "threshold_met": self.threshold_met
        }


@dataclass
class CoverageThresholds:
    """Coverage thresholds"""
    line_threshold: float
    branch_threshold: float
    function_threshold: float
    fail_on_low_coverage: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert coverage thresholds to dictionary"""
        return {
            "line_threshold": self.line_threshold,
            "branch_threshold": self.branch_threshold,
            "function_threshold": self.function_threshold,
            "fail_on_low_coverage": self.fail_on_low_coverage
        }


@dataclass
class CoverageMetadata:
    """Coverage report metadata"""
    generator: str = ""
    generator_version: str = ""
    test_suite: str = ""
    test_run_id: str = ""
    build_type: str = ""
    compiler: str = ""
    platform: str = ""
    architecture: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert coverage metadata to dictionary"""
        return {
            "generator": self.generator,
            "generator_version": self.generator_version,
            "test_suite": self.test_suite,
            "test_run_id": self.test_run_id,
            "build_type": self.build_type,
            "compiler": self.compiler,
            "platform": self.platform,
            "architecture": self.architecture
        }


@dataclass
class CoverageReport:
    """Coverage report"""
    version: str
    timestamp: datetime
    summary: CoverageSummary
    files: List[FileCoverage] = field(default_factory=list)
    directories: List[DirectoryCoverage] = field(default_factory=list)
    modules: List[ModuleCoverage] = field(default_factory=list)
    uncovered_lines: List[UncoveredLine] = field(default_factory=list)
    uncovered_branches: List[UncoveredBranch] = field(default_factory=list)
    uncovered_functions: List[UncoveredFunction] = field(default_factory=list)
    thresholds: Optional[CoverageThresholds] = None
    metadata: CoverageMetadata = field(default_factory=CoverageMetadata)

    def to_dict(self) -> Dict[str, Any]:
        """Convert coverage report to dictionary"""
        return {
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "summary": self.summary.to_dict(),
            "files": [file.to_dict() for file in self.files],
            "directories": [dir.to_dict() for dir in self.directories],
            "modules": [mod.to_dict() for mod in self.modules],
            "uncovered_lines": [line.to_dict() for line in self.uncovered_lines],
            "uncovered_branches": [branch.to_dict() for branch in self.uncovered_branches],
            "uncovered_functions": [func.to_dict() for func in self.uncovered_functions],
            "thresholds": self.thresholds.to_dict() if self.thresholds else None,
            "metadata": self.metadata.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoverageReport":
        """Create coverage report from dictionary"""
        return cls(
            version=data["version"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            summary=CoverageSummary(**data["summary"]),
            files=[
                FileCoverage(
                    path=f["path"],
                    language=f.get("language", ""),
                    line_coverage=f["line_coverage"],
                    branch_coverage=f.get("branch_coverage", 0.0),
                    function_coverage=f.get("function_coverage", 0.0),
                    total_lines=f.get("total_lines", 0),
                    covered_lines=f.get("covered_lines", 0),
                    total_branches=f.get("total_branches", 0),
                    covered_branches=f.get("covered_branches", 0),
                    total_functions=f.get("total_functions", 0),
                    covered_functions=f.get("covered_functions", 0),
                    lines=[LineCoverage(**line) for line in f.get("lines", [])],
                    branches=[BranchCoverage(**branch) for branch in f.get("branches", [])],
                    functions=[FunctionCoverage(**func) for func in f.get("functions", [])]
                )
                for f in data.get("files", [])
            ],
            directories=[
                DirectoryCoverage(
                    path=d["path"],
                    line_coverage=d["line_coverage"],
                    branch_coverage=d.get("branch_coverage", 0.0),
                    function_coverage=d.get("function_coverage", 0.0),
                    total_lines=d.get("total_lines", 0),
                    covered_lines=d.get("covered_lines", 0),
                    total_branches=d.get("total_branches", 0),
                    covered_branches=d.get("covered_branches", 0),
                    total_functions=d.get("total_functions", 0),
                    covered_functions=d.get("covered_functions", 0),
                    files=d.get("files", [])
                )
                for d in data.get("directories", [])
            ],
            modules=[
                ModuleCoverage(
                    name=m["name"],
                    path=m["path"],
                    line_coverage=m["line_coverage"],
                    branch_coverage=m.get("branch_coverage", 0.0),
                    function_coverage=m.get("function_coverage", 0.0),
                    total_lines=m.get("total_lines", 0),
                    covered_lines=m.get("covered_lines", 0),
                    total_branches=m.get("total_branches", 0),
                    covered_branches=m.get("covered_branches", 0),
                    total_functions=m.get("total_functions", 0),
                    covered_functions=m.get("covered_functions", 0),
                    files=m.get("files", [])
                )
                for m in data.get("modules", [])
            ],
            uncovered_lines=[
                UncoveredLine(**line) for line in data.get("uncovered_lines", [])
            ],
            uncovered_branches=[
                UncoveredBranch(**branch) for branch in data.get("uncovered_branches", [])
            ],
            uncovered_functions=[
                UncoveredFunction(**func) for func in data.get("uncovered_functions", [])
            ],
            thresholds=CoverageThresholds(**data["thresholds"]) if data.get("thresholds") else None,
            metadata=CoverageMetadata(**data.get("metadata", {}))
        )

    def check_thresholds(self) -> bool:
        """Check if coverage meets thresholds"""
        if not self.thresholds:
            return True

        if self.summary.line_coverage < self.thresholds.line_threshold:
            return False

        if self.summary.branch_coverage < self.thresholds.branch_threshold:
            return False

        if self.summary.function_coverage < self.thresholds.function_threshold:
            return False

        return True

    def get_low_coverage_files(self, threshold: float = 50.0) -> List[FileCoverage]:
        """Get files with low coverage"""
        return [file for file in self.files if file.line_coverage < threshold]

    def get_uncovered_files(self) -> List[FileCoverage]:
        """Get files with zero coverage"""
        return [file for file in self.files if file.line_coverage == 0.0]

    def get_high_coverage_files(self, threshold: float = 90.0) -> List[FileCoverage]:
        """Get files with high coverage"""
        return [file for file in self.files if file.line_coverage >= threshold]
```

## C++ Code

```cpp
/**
 * @file coverage_report.hpp
 * @brief Coverage report schema for OmniCpp
 */

#ifndef OMNICPP_COVERAGE_REPORT_HPP
#define OMNICPP_COVERAGE_REPORT_HPP

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <chrono>
#include <nlohmann/json.hpp>

namespace omnicpp {
namespace testing {

/**
 * @brief Line coverage data
 */
struct LineCoverage {
    int line_number;
    bool covered;
    int execution_count = 0;
    std::string code;

    nlohmann::json to_json() const {
        return {
            {"line_number", line_number},
            {"execution_count", execution_count},
            {"covered", covered},
            {"code", code}
        };
    }

    static LineCoverage from_json(const nlohmann::json& j) {
        LineCoverage lc;
        lc.line_number = j["line_number"];
        lc.execution_count = j.value("execution_count", 0);
        lc.covered = j["covered"];
        lc.code = j.value("code", "");
        return lc;
    }
};

/**
 * @brief Branch coverage data
 */
struct BranchCoverage {
    int line_number;
    int branch_number;
    bool covered;
    int execution_count = 0;

    nlohmann::json to_json() const {
        return {
            {"line_number", line_number},
            {"branch_number", branch_number},
            {"covered", covered},
            {"execution_count", execution_count}
        };
    }

    static BranchCoverage from_json(const nlohmann::json& j) {
        BranchCoverage bc;
        bc.line_number = j["line_number"];
        bc.branch_number = j["branch_number"];
        bc.covered = j["covered"];
        bc.execution_count = j.value("execution_count", 0);
        return bc;
    }
};

/**
 * @brief Function coverage data
 */
struct FunctionCoverage {
    std::string name;
    int start_line;
    int end_line;
    bool covered;
    int execution_count = 0;

    nlohmann::json to_json() const {
        return {
            {"name", name},
            {"start_line", start_line},
            {"end_line", end_line},
            {"covered", covered},
            {"execution_count", execution_count}
        };
    }

    static FunctionCoverage from_json(const nlohmann::json& j) {
        FunctionCoverage fc;
        fc.name = j["name"];
        fc.start_line = j["start_line"];
        fc.end_line = j["end_line"];
        fc.covered = j["covered"];
        fc.execution_count = j.value("execution_count", 0);
        return fc;
    }
};

/**
 * @brief File coverage data
 */
struct FileCoverage {
    std::string path;
    std::string language;
    double line_coverage;
    double branch_coverage = 0.0;
    double function_coverage = 0.0;
    int total_lines = 0;
    int covered_lines = 0;
    int total_branches = 0;
    int covered_branches = 0;
    int total_functions = 0;
    int covered_functions = 0;
    std::vector<LineCoverage> lines;
    std::vector<BranchCoverage> branches;
    std::vector<FunctionCoverage> functions;

    nlohmann::json to_json() const {
        nlohmann::json j;
        j["path"] = path;
        j["language"] = language;
        j["line_coverage"] = line_coverage;
        j["branch_coverage"] = branch_coverage;
        j["function_coverage"] = function_coverage;
        j["total_lines"] = total_lines;
        j["covered_lines"] = covered_lines;
        j["total_branches"] = total_branches;
        j["covered_branches"] = covered_branches;
        j["total_functions"] = total_functions;
        j["covered_functions"] = covered_functions;

        nlohmann::json lines_json = nlohmann::json::array();
        for (const auto& line : lines) {
            lines_json.push_back(line.to_json());
        }
        j["lines"] = lines_json;

        nlohmann::json branches_json = nlohmann::json::array();
        for (const auto& branch : branches) {
            branches_json.push_back(branch.to_json());
        }
        j["branches"] = branches_json;

        nlohmann::json functions_json = nlohmann::json::array();
        for (const auto& func : functions) {
            functions_json.push_back(func.to_json());
        }
        j["functions"] = functions_json;

        return j;
    }

    static FileCoverage from_json(const nlohmann::json& j) {
        FileCoverage fc;
        fc.path = j["path"];
        fc.language = j.value("language", "");
        fc.line_coverage = j["line_coverage"];
        fc.branch_coverage = j.value("branch_coverage", 0.0);
        fc.function_coverage = j.value("function_coverage", 0.0);
        fc.total_lines = j.value("total_lines", 0);
        fc.covered_lines = j.value("covered_lines", 0);
        fc.total_branches = j.value("total_branches", 0);
        fc.covered_branches = j.value("covered_branches", 0);
        fc.total_functions = j.value("total_functions", 0);
        fc.covered_functions = j.value("covered_functions", 0);

        if (j.contains("lines")) {
            for (const auto& line_json : j["lines"]) {
                fc.lines.push_back(LineCoverage::from_json(line_json));
            }
        }

        if (j.contains("branches")) {
            for (const auto& branch_json : j["branches"]) {
                fc.branches.push_back(BranchCoverage::from_json(branch_json));
            }
        }

        if (j.contains("functions")) {
            for (const auto& func_json : j["functions"]) {
                fc.functions.push_back(FunctionCoverage::from_json(func_json));
            }
        }

        return fc;
    }
};

/**
 * @brief Coverage summary
 */
struct CoverageSummary {
    double line_coverage;
    double branch_coverage;
    double function_coverage;
    int total_lines = 0;
    int covered_lines = 0;
    int total_branches = 0;
    int covered_branches = 0;
    int total_functions = 0;
    int covered_functions = 0;
    bool threshold_met = true;

    nlohmann::json to_json() const {
        return {
            {"line_coverage", line_coverage},
            {"branch_coverage", branch_coverage},
            {"function_coverage", function_coverage},
            {"total_lines", total_lines},
            {"covered_lines", covered_lines},
            {"total_branches", total_branches},
            {"covered_branches", covered_branches},
            {"total_functions", total_functions},
            {"covered_functions", covered_functions},
            {"threshold_met", threshold_met}
        };
    }

    static CoverageSummary from_json(const nlohmann::json& j) {
        CoverageSummary cs;
        cs.line_coverage = j["line_coverage"];
        cs.branch_coverage = j["branch_coverage"];
        cs.function_coverage = j["function_coverage"];
        cs.total_lines = j.value("total_lines", 0);
        cs.covered_lines = j.value("covered_lines", 0);
        cs.total_branches = j.value("total_branches", 0);
        cs.covered_branches = j.value("covered_branches", 0);
        cs.total_functions = j.value("total_functions", 0);
        cs.covered_functions = j.value("covered_functions", 0);
        cs.threshold_met = j.value("threshold_met", true);
        return cs;
    }
};

/**
 * @brief Coverage thresholds
 */
struct CoverageThresholds {
    double line_threshold;
    double branch_threshold;
    double function_threshold;
    bool fail_on_low_coverage = false;

    nlohmann::json to_json() const {
        return {
            {"line_threshold", line_threshold},
            {"branch_threshold", branch_threshold},
            {"function_threshold", function_threshold},
            {"fail_on_low_coverage", fail_on_low_coverage}
        };
    }

    static CoverageThresholds from_json(const nlohmann::json& j) {
        CoverageThresholds ct;
        ct.line_threshold = j["line_threshold"];
        ct.branch_threshold = j["branch_threshold"];
        ct.function_threshold = j["function_threshold"];
        ct.fail_on_low_coverage = j.value("fail_on_low_coverage", false);
        return ct;
    }
};

/**
 * @brief Coverage report metadata
 */
struct CoverageMetadata {
    std::string generator;
    std::string generator_version;
    std::string test_suite;
    std::string test_run_id;
    std::string build_type;
    std::string compiler;
    std::string platform;
    std::string architecture;

    nlohmann::json to_json() const {
        return {
            {"generator", generator},
            {"generator_version", generator_version},
            {"test_suite", test_suite},
            {"test_run_id", test_run_id},
            {"build_type", build_type},
            {"compiler", compiler},
            {"platform", platform},
            {"architecture", architecture}
        };
    }

    static CoverageMetadata from_json(const nlohmann::json& j) {
        CoverageMetadata cm;
        cm.generator = j.value("generator", "");
        cm.generator_version = j.value("generator_version", "");
        cm.test_suite = j.value("test_suite", "");
        cm.test_run_id = j.value("test_run_id", "");
        cm.build_type = j.value("build_type", "");
        cm.compiler = j.value("compiler", "");
        cm.platform = j.value("platform", "");
        cm.architecture = j.value("architecture", "");
        return cm;
    }
};

/**
 * @brief Coverage report
 */
class CoverageReport {
public:
    CoverageReport() = default;

    std::string version;
    std::chrono::system_clock::time_point timestamp;
    CoverageSummary summary;
    std::vector<FileCoverage> files;
    std::map<std::string, double> directories;
    std::map<std::string, double> modules;
    std::vector<std::pair<std::string, int>> uncovered_lines;
    std::vector<std::tuple<std::string, int, int>> uncovered_branches;
    std::vector<std::tuple<std::string, std::string, int, int>> uncovered_functions;
    std::shared_ptr<CoverageThresholds> thresholds;
    CoverageMetadata metadata;

    nlohmann::json to_json() const {
        nlohmann::json j;
        j["version"] = version;

        auto timestamp_t = std::chrono::system_clock::to_time_t(timestamp);
        j["timestamp"] = std::string(std::ctime(&timestamp_t));

        j["summary"] = summary.to_json();

        nlohmann::json files_json = nlohmann::json::array();
        for (const auto& file : files) {
            files_json.push_back(file.to_json());
        }
        j["files"] = files_json;

        nlohmann::json directories_json = nlohmann::json::object();
        for (const auto& [path, coverage] : directories) {
            directories_json[path] = coverage;
        }
        j["directories"] = directories_json;

        nlohmann::json modules_json = nlohmann::json::object();
        for (const auto& [name, coverage] : modules) {
            modules_json[name] = coverage;
        }
        j["modules"] = modules_json;

        nlohmann::json uncovered_lines_json = nlohmann::json::array();
        for (const auto& [file, line] : uncovered_lines) {
            uncovered_lines_json.push_back({
                {"file", file},
                {"line_number", line}
            });
        }
        j["uncovered_lines"] = uncovered_lines_json;

        nlohmann::json uncovered_branches_json = nlohmann::json::array();
        for (const auto& [file, line, branch] : uncovered_branches) {
            uncovered_branches_json.push_back({
                {"file", file},
                {"line_number", line},
                {"branch_number", branch}
            });
        }
        j["uncovered_branches"] = uncovered_branches_json;

        nlohmann::json uncovered_functions_json = nlohmann::json::array();
        for (const auto& [file, name, start, end] : uncovered_functions) {
            uncovered_functions_json.push_back({
                {"file", file},
                {"function_name", name},
                {"start_line", start},
                {"end_line", end}
            });
        }
        j["uncovered_functions"] = uncovered_functions_json;

        if (thresholds) {
            j["thresholds"] = thresholds->to_json();
        }

        j["metadata"] = metadata.to_json();

        return j;
    }

    static CoverageReport from_json(const nlohmann::json& j) {
        CoverageReport report;
        report.version = j["version"];

        std::string timestamp_str = j["timestamp"];
        std::tm tm = {};
        std::istringstream ss(timestamp_str);
        ss >> std::get_time(&tm, "%a %b %d %H:%M:%S %Y");
        report.timestamp = std::chrono::system_clock::from_time_t(std::mktime(&tm));

        report.summary = CoverageSummary::from_json(j["summary"]);

        if (j.contains("files")) {
            for (const auto& file_json : j["files"]) {
                report.files.push_back(FileCoverage::from_json(file_json));
            }
        }

        if (j.contains("directories")) {
            for (const auto& [path, coverage] : j["directories"].items()) {
                report.directories[path] = coverage.get<double>();
            }
        }

        if (j.contains("modules")) {
            for (const auto& [name, coverage] : j["modules"].items()) {
                report.modules[name] = coverage.get<double>();
            }
        }

        if (j.contains("uncovered_lines")) {
            for (const auto& line_json : j["uncovered_lines"]) {
                report.uncovered_lines.push_back({
                    line_json["file"],
                    line_json["line_number"]
                });
            }
        }

        if (j.contains("uncovered_branches")) {
            for (const auto& branch_json : j["uncovered_branches"]) {
                report.uncovered_branches.push_back({
                    branch_json["file"],
                    branch_json["line_number"],
                    branch_json["branch_number"]
                });
            }
        }

        if (j.contains("uncovered_functions")) {
            for (const auto& func_json : j["uncovered_functions"]) {
                report.uncovered_functions.push_back({
                    func_json["file"],
                    func_json["function_name"],
                    func_json["start_line"],
                    func_json["end_line"]
                });
            }
        }

        if (j.contains("thresholds")) {
            report.thresholds = std::make_shared<CoverageThresholds>(
                CoverageThresholds::from_json(j["thresholds"])
            );
        }

        if (j.contains("metadata")) {
            report.metadata = CoverageMetadata::from_json(j["metadata"]);
        }

        return report;
    }

    bool check_thresholds() const {
        if (!thresholds) {
            return true;
        }

        if (summary.line_coverage < thresholds->line_threshold) {
            return false;
        }

        if (summary.branch_coverage < thresholds->branch_threshold) {
            return false;
        }

        if (summary.function_coverage < thresholds->function_threshold) {
            return false;
        }

        return true;
    }

    std::vector<FileCoverage> get_low_coverage_files(double threshold = 50.0) const {
        std::vector<FileCoverage> low_coverage_files;
        for (const auto& file : files) {
            if (file.line_coverage < threshold) {
                low_coverage_files.push_back(file);
            }
        }
        return low_coverage_files;
    }

    std::vector<FileCoverage> get_uncovered_files() const {
        std::vector<FileCoverage> uncovered_files;
        for (const auto& file : files) {
            if (file.line_coverage == 0.0) {
                uncovered_files.push_back(file);
            }
        }
        return uncovered_files;
    }

    std::vector<FileCoverage> get_high_coverage_files(double threshold = 90.0) const {
        std::vector<FileCoverage> high_coverage_files;
        for (const auto& file : files) {
            if (file.line_coverage >= threshold) {
                high_coverage_files.push_back(file);
            }
        }
        return high_coverage_files;
    }
};

} // namespace testing
} // namespace omnicpp

#endif // OMNICPP_COVERAGE_REPORT_HPP
```

## Dependencies

### Internal Dependencies
- `DES-037` - Test Fixture Design
- `DES-038` - Test Configuration Schema

### External Dependencies
- `typing` - Type hints
- `dataclasses` - Data structures
- `datetime` - Date and time handling
- `enum` - Enumerations
- `nlohmann/json` - JSON library (C++)

## Related Requirements
- REQ-060: Test Framework
- REQ-061: Test Fixtures
- REQ-062: Test Configuration
- REQ-063: Coverage Reporting

## Related ADRs
- ADR-004: Testing Architecture

## Implementation Notes

### Coverage Report Structure
1. Version control
2. Timestamp
3. Coverage summary
4. File coverage data
5. Directory coverage data
6. Module coverage data
7. Uncovered lines
8. Uncovered branches
9. Uncovered functions
10. Coverage thresholds
11. Metadata

### Coverage Metrics
1. Line coverage
2. Branch coverage
3. Function coverage
4. Total/covered counts
5. Threshold checking

### Coverage Analysis
1. Low coverage files
2. Uncovered files
3. High coverage files
4. Threshold validation

### Serialization
1. JSON serialization
2. JSON deserialization
3. Type conversion
4. Error handling

## Usage Example

```python
from omni_scripts.testing import (
    CoverageReport,
    CoverageSummary,
    FileCoverage,
    LineCoverage,
    CoverageThresholds,
    CoverageMetadata
)
from datetime import datetime

# Create coverage report
report = CoverageReport(
    version="1.0.0",
    timestamp=datetime.now(),
    summary=CoverageSummary(
        line_coverage=85.5,
        branch_coverage=78.2,
        function_coverage=92.1,
        total_lines=1000,
        covered_lines=855,
        total_branches=200,
        covered_branches=156,
        total_functions=50,
        covered_functions=46
    ),
    files=[
        FileCoverage(
            path="src/engine.cpp",
            language="C++",
            line_coverage=90.0,
            total_lines=100,
            covered_lines=90,
            lines=[
                LineCoverage(line_number=1, covered=True, execution_count=5),
                LineCoverage(line_number=2, covered=False, execution_count=0)
            ]
        )
    ],
    thresholds=CoverageThresholds(
        line_threshold=80.0,
        branch_threshold=75.0,
        function_threshold=85.0
    ),
    metadata=CoverageMetadata(
        generator="OmniCpp",
        generator_version="1.0.0",
        test_suite="EngineTests",
        compiler="GCC 13.2",
        platform="Linux",
        architecture="x86_64"
    )
)

# Check thresholds
thresholds_met = report.check_thresholds()
print(f"Thresholds met: {thresholds_met}")

# Get low coverage files
low_coverage_files = report.get_low_coverage_files(threshold=50.0)
print(f"Low coverage files: {len(low_coverage_files)}")

# Convert to dictionary
report_dict = report.to_dict()

# Save to JSON file
import json
with open("coverage_report.json", "w") as f:
    json.dump(report_dict, f, indent=2)
```
