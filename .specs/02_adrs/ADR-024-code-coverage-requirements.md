# ADR-024: Code Coverage Requirements (80%)

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Testing

---

## Context

The OmniCPP Template project requires comprehensive code coverage to ensure code quality and maintainability. Code coverage is a critical metric for measuring test effectiveness. The coding standards (`.specs/01_standards/coding_standards.md`) specify the need for comprehensive testing.

### Current State

Code coverage is inconsistent:
- **No Requirements:** No code coverage requirements
- **No Tracking:** No code coverage tracking
- **No Reporting:** No code coverage reporting
- **No Enforcement:** No code coverage enforcement
- **No CI/CD:** No CI/CD integration for coverage

### Issues

1. **No Requirements:** No code coverage requirements
2. **No Tracking:** No code coverage tracking
3. **No Reporting:** No code coverage reporting
4. **No Enforcement:** No code coverage enforcement
5. **No CI/CD:** No CI/CD integration for coverage
6. **No Standards:** No coverage standards

## Decision

Implement **code coverage requirements (80%)** with:
1. **Coverage Threshold:** 80% code coverage threshold
2. **Coverage Tracking:** Track code coverage for all modules
3. **Coverage Reporting:** Generate coverage reports
4. **Coverage Enforcement:** Enforce coverage threshold in CI/CD
5. **Coverage Exclusions:** Define coverage exclusions
6. **Coverage Trends:** Track coverage trends over time
7. **Coverage Documentation:** Document coverage requirements

### 1. Coverage Configuration

```cmake
# cmake/Coverage.cmake
# Code coverage configuration

# Find coverage tools
find_program(LCOV_EXECUTABLE lcov)
find_program(GENHTML_EXECUTABLE genhtml)
find_program(GCOV_EXECUTABLE gcov)

# Enable coverage
option(ENABLE_COVERAGE "Enable code coverage" OFF)

if(ENABLE_COVERAGE)
    message(STATUS "Code coverage enabled")

    # Add coverage flags
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        add_compile_options(-fprofile-arcs -ftest-coverage)
        add_link_options(-fprofile-arcs)
    elseif(MSVC)
        add_compile_options(/profile)
    endif()

    # Add coverage target
    add_custom_target(coverage
        COMMAND ${LCOV_EXECUTABLE} --capture --directory . --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '/usr/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '*/tests/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '*/external/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --list coverage.info
        COMMAND ${GENHTML_EXECUTABLE} coverage.info --output-directory coverage_html
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Generating code coverage report"
    )

    # Add coverage check target
    add_custom_target(coverage_check
        COMMAND ${LCOV_EXECUTABLE} --capture --directory . --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '/usr/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '*/tests/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --remove coverage.info '*/external/*' --output-file coverage.info
        COMMAND ${LCOV_EXECUTABLE} --summary coverage.info
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Checking code coverage"
    )
endif()
```

### 2. Coverage Requirements

```python
# omni_scripts/validators/coverage_validator.py
"""Coverage validator for code coverage requirements."""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from exceptions import CoverageError

@dataclass
class CoverageReport:
    """Coverage report."""

    line_coverage: float
    function_coverage: float
    branch_coverage: float
    total_lines: int
    covered_lines: int
    total_functions: int
    covered_functions: int
    total_branches: int
    covered_branches: int

    @property
    def meets_threshold(self, threshold: float = 80.0) -> bool:
        """Check if coverage meets threshold.

        Args:
            threshold: Coverage threshold

        Returns:
            True if meets threshold, False otherwise
        """
        return self.line_coverage >= threshold


class CoverageValidator:
    """Coverage validator for code coverage requirements."""

    # Coverage threshold
    COVERAGE_THRESHOLD = 80.0

    # Coverage exclusions
    COVERAGE_EXCLUSIONS = [
        "*/tests/*",
        "*/test_*",
        "*/external/*",
        "*/vendor/*",
        "*/build/*",
        "*/cmake/*",
        "*/CPM_modules/*",
    ]

    def __init__(self, logger: logging.Logger, threshold: float = COVERAGE_THRESHOLD):
        """Initialize coverage validator.

        Args:
            logger: Logger instance
            threshold: Coverage threshold
        """
        self.logger = logger
        self.threshold = threshold

    def validate_coverage(self, coverage_file: Path) -> bool:
        """Validate code coverage.

        Args:
            coverage_file: Path to coverage file

        Returns:
            True if coverage meets threshold, False otherwise

        Raises:
            CoverageError: If coverage does not meet threshold
        """
        self.logger.info(f"Validating coverage from {coverage_file}")

        # Parse coverage file
        coverage_report = self._parse_coverage_file(coverage_file)

        # Check if coverage meets threshold
        if not coverage_report.meets_threshold(self.threshold):
            raise CoverageError(
                f"Coverage {coverage_report.line_coverage:.2f}% does not meet threshold {self.threshold:.2f}%"
            )

        self.logger.info(f"Coverage {coverage_report.line_coverage:.2f}% meets threshold {self.threshold:.2f}%")

        return True

    def _parse_coverage_file(self, coverage_file: Path) -> CoverageReport:
        """Parse coverage file.

        Args:
            coverage_file: Path to coverage file

        Returns:
            Coverage report
        """
        # Read coverage file
        with open(coverage_file, 'r') as f:
            content = f.read()

        # Parse coverage summary
        line_coverage = self._extract_coverage(content, "lines")
        function_coverage = self._extract_coverage(content, "functions")
        branch_coverage = self._extract_coverage(content, "branches")

        # Parse coverage details
        total_lines = self._extract_total(content, "lines")
        covered_lines = self._extract_covered(content, "lines")
        total_functions = self._extract_total(content, "functions")
        covered_functions = self._extract_covered(content, "functions")
        total_branches = self._extract_total(content, "branches")
        covered_branches = self._extract_covered(content, "branches")

        return CoverageReport(
            line_coverage=line_coverage,
            function_coverage=function_coverage,
            branch_coverage=branch_coverage,
            total_lines=total_lines,
            covered_lines=covered_lines,
            total_functions=total_functions,
            covered_functions=covered_functions,
            total_branches=total_branches,
            covered_branches=covered_branches
        )

    def _extract_coverage(self, content: str, metric: str) -> float:
        """Extract coverage metric.

        Args:
            content: Coverage file content
            metric: Coverage metric

        Returns:
            Coverage percentage
        """
        # Extract coverage percentage
        pattern = rf"{metric}.*?(\d+\.\d+)%"
        match = re.search(pattern, content)

        if match:
            return float(match.group(1))

        return 0.0

    def _extract_total(self, content: str, metric: str) -> int:
        """Extract total count.

        Args:
            content: Coverage file content
            metric: Coverage metric

        Returns:
            Total count
        """
        # Extract total count
        pattern = rf"{metric}.*?(\d+)"
        match = re.search(pattern, content)

        if match:
            return int(match.group(1))

        return 0

    def _extract_covered(self, content: str, metric: str) -> int:
        """Extract covered count.

        Args:
            content: Coverage file content
            metric: Coverage metric

        Returns:
            Covered count
        """
        # Extract covered count
        pattern = rf"{metric}.*?(\d+).*?(\d+)"
        match = re.search(pattern, content)

        if match:
            return int(match.group(2))

        return 0

    def generate_coverage_report(self, coverage_file: Path, output_file: Path) -> None:
        """Generate coverage report.

        Args:
            coverage_file: Path to coverage file
            output_file: Path to output file
        """
        self.logger.info(f"Generating coverage report to {output_file}")

        # Parse coverage file
        coverage_report = self._parse_coverage_file(coverage_file)

        # Generate report
        report = f"""
# Code Coverage Report

## Summary

- **Line Coverage:** {coverage_report.line_coverage:.2f}%
- **Function Coverage:** {coverage_report.function_coverage:.2f}%
- **Branch Coverage:** {coverage_report.branch_coverage:.2f}%

## Details

- **Total Lines:** {coverage_report.total_lines}
- **Covered Lines:** {coverage_report.covered_lines}
- **Total Functions:** {coverage_report.total_functions}
- **Covered Functions:** {coverage_report.covered_functions}
- **Total Branches:** {coverage_report.total_branches}
- **Covered Branches:** {coverage_report.covered_branches}

## Threshold

- **Required:** {self.threshold:.2f}%
- **Status:** {'PASS' if coverage_report.meets_threshold(self.threshold) else 'FAIL'}
"""

        # Write report
        with open(output_file, 'w') as f:
            f.write(report)
```

### 3. Coverage Configuration Files

```python
# pyproject.toml
# pytest coverage configuration

[tool.pytest.ini_options]
addopts = [
    "--cov=omni_scripts",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80",
]

[tool.coverage.run]
source = ["omni_scripts"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/site-packages/*",
    "*/build/*",
    "*/cmake/*",
    "*/CPM_modules/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.coverage.html]
directory = "coverage_html"
```

### 4. Coverage Enforcement

```yaml
# .github/workflows/coverage.yml
# GitHub Actions workflow for coverage enforcement

name: Coverage

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install pytest pytest-cov

    - name: Run tests with coverage
      run: |
        pytest --cov=omni_scripts --cov-report=xml --cov-report=term-missing --cov-fail-under=80

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true
```

### 5. Coverage Trends

```python
# omni_scripts/validators/coverage_trends.py
"""Coverage trends tracker."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class CoverageSnapshot:
    """Coverage snapshot."""

    date: str
    line_coverage: float
    function_coverage: float
    branch_coverage: float

    def to_dict(self) -> Dict:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return asdict(self)


class CoverageTrends:
    """Coverage trends tracker."""

    def __init__(self, logger: logging.Logger, trends_file: Path):
        """Initialize coverage trends tracker.

        Args:
            logger: Logger instance
            trends_file: Path to trends file
        """
        self.logger = logger
        self.trends_file = trends_file
        self.trends: List[CoverageSnapshot] = []

        # Load trends
        if trends_file.exists():
            self.load_trends(trends_file)

    def load_trends(self, trends_file: Path) -> None:
        """Load trends from file.

        Args:
            trends_file: Path to trends file
        """
        self.logger.info(f"Loading trends from {trends_file}")

        with open(trends_file, 'r') as f:
            trends_data = json.load(f)

        self.trends = [
            CoverageSnapshot(**snapshot)
            for snapshot in trends_data
        ]

    def save_trends(self, trends_file: Path) -> None:
        """Save trends to file.

        Args:
            trends_file: Path to trends file
        """
        self.logger.info(f"Saving trends to {trends_file}")

        trends_data = [
            snapshot.to_dict()
            for snapshot in self.trends
        ]

        with open(trends_file, 'w') as f:
            json.dump(trends_data, f, indent=2)

    def add_snapshot(
        self,
        line_coverage: float,
        function_coverage: float,
        branch_coverage: float
    ) -> None:
        """Add coverage snapshot.

        Args:
            line_coverage: Line coverage
            function_coverage: Function coverage
            branch_coverage: Branch coverage
        """
        snapshot = CoverageSnapshot(
            date=datetime.utcnow().isoformat(),
            line_coverage=line_coverage,
            function_coverage=function_coverage,
            branch_coverage=branch_coverage
        )

        self.trends.append(snapshot)
        self.logger.info(f"Added coverage snapshot: {line_coverage:.2f}%")

    def get_trends(self) -> List[CoverageSnapshot]:
        """Get coverage trends.

        Returns:
            List of coverage snapshots
        """
        return self.trends.copy()

    def get_latest(self) -> Optional[CoverageSnapshot]:
        """Get latest coverage snapshot.

        Returns:
            Latest coverage snapshot or None
        """
        if not self.trends:
            return None

        return self.trends[-1]

    def get_average(self) -> Optional[float]:
        """Get average coverage.

        Returns:
            Average coverage or None
        """
        if not self.trends:
            return None

        total = sum(snapshot.line_coverage for snapshot in self.trends)
        return total / len(self.trends)
```

### 6. Usage Examples

```python
# Example usage
from validators.coverage_validator import CoverageValidator, CoverageReport
from validators.coverage_trends import CoverageTrends
from logging.logger import Logger

# Initialize logger
logger = Logger()

# Initialize coverage validator
validator = CoverageValidator(logger, threshold=80.0)

# Validate coverage
try:
    validator.validate_coverage(Path("coverage.info"))
    logger.info("Coverage meets threshold")
except CoverageError as e:
    logger.error(f"Coverage does not meet threshold: {e}")

# Generate coverage report
validator.generate_coverage_report(
    coverage_file=Path("coverage.info"),
    output_file=Path("coverage_report.md")
)

# Initialize coverage trends
trends = CoverageTrends(logger, Path("coverage_trends.json"))

# Add coverage snapshot
trends.add_snapshot(
    line_coverage=85.5,
    function_coverage=82.3,
    branch_coverage=78.9
)

# Save trends
trends.save_trends(Path("coverage_trends.json"))

# Get trends
snapshots = trends.get_trends()
for snapshot in snapshots:
    print(f"{snapshot.date}: {snapshot.line_coverage:.2f}%")

# Get latest snapshot
latest = trends.get_latest()
if latest:
    print(f"Latest coverage: {latest.line_coverage:.2f}%")

# Get average coverage
average = trends.get_average()
if average:
    print(f"Average coverage: {average:.2f}%")
```

## Consequences

### Positive

1. **Quality:** Ensures code quality
2. **Maintainability:** Improves code maintainability
3. **Confidence:** Increases confidence in code changes
4. **Documentation:** Documents code coverage
5. **Trends:** Tracks coverage trends over time
6. **Enforcement:** Enforces coverage requirements
7. **Reporting:** Generates coverage reports

### Negative

1. **Complexity:** More complex than no coverage
2. **Build Time:** Coverage adds build time
3. **Maintenance:** Coverage needs to be maintained
4. **False Sense:** Coverage does not guarantee quality

### Neutral

1. **Documentation:** Requires documentation for coverage
2. **Training:** Need to train developers on coverage

## Alternatives Considered

### Alternative 1: No Coverage Requirements

**Description:** No code coverage requirements

**Pros:**
- Simpler implementation
- No build time overhead

**Cons:**
- No quality assurance
- No maintainability improvement
- No confidence in code changes

**Rejected:** No quality assurance and no maintainability improvement

### Alternative 2: Lower Coverage Threshold (50%)

**Description:** Lower coverage threshold to 50%

**Pros:**
- Easier to achieve
- Less build time

**Cons:**
- Lower quality assurance
- Less maintainability improvement
- Less confidence in code changes

**Rejected:** Lower quality assurance and less maintainability improvement

### Alternative 3: Higher Coverage Threshold (95%)

**Description:** Higher coverage threshold to 95%

**Pros:**
- Higher quality assurance
- Better maintainability improvement
- More confidence in code changes

**Cons:**
- Harder to achieve
- More build time
- May be impractical

**Rejected:** Harder to achieve and may be impractical

## Related ADRs

- [ADR-022: Google Test for C++ unit tests](ADR-022-google-test-cpp-unit-tests.md)
- [ADR-023: pytest for Python tests](ADR-023-pytest-python-tests.md)

## References

- [Code Coverage](https://en.wikipedia.org/wiki/Code_coverage)
- [gcov Documentation](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html)
- [lcov Documentation](http://ltp.sourceforge.net/coverage/lcov.php)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
