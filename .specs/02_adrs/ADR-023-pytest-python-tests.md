# ADR-023: pytest for Python Tests

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Testing

---

## Context

The OmniCPP Template project requires a robust testing framework for Python code. Unit testing is critical for code quality and maintainability. The coding standards (`.specs/01_standards/coding_standards.md`) specify the need for comprehensive testing.

### Current State

Python testing is inconsistent:
- **No Framework:** No consistent testing framework
- **No Coverage:** No code coverage tracking
- **No Integration:** No integration with build system
- **No CI/CD:** No CI/CD integration
- **No Reporting:** No test reporting

### Issues

1. **No Framework:** No consistent testing framework
2. **No Coverage:** No code coverage tracking
3. **No Integration:** No integration with build system
4. **No CI/CD:** No CI/CD integration
5. **No Reporting:** No test reporting
6. **No Standards:** No testing standards

## Decision

Implement **pytest** for Python tests with:
1. **pytest Framework:** Use pytest for unit testing
2. **pytest-cov:** Use pytest-cov for code coverage
3. **pytest-mock:** Use pytest-mock for mocking
4. **pytest-asyncio:** Use pytest-asyncio for async testing
5. **Test Organization:** Organize tests by module
6. **Test Naming:** Follow consistent test naming conventions
7. **Test Documentation:** Document all tests

### 1. pytest Configuration

```python
# pyproject.toml
# pytest configuration

[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Test options
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=omni_scripts",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80",
]

# Markers
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
    "skip_ci: Skip tests in CI",
]

# Coverage options
[tool.coverage.run]
source = ["omni_scripts"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/site-packages/*",
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
```

### 2. Test Organization

```python
# tests/unit/build_system/test_cmake.py
# CMake build system tests

import pytest
from pathlib import Path
from typing import Dict, Any

from omni_scripts.build_system.cmake import CMake
from omni_scripts.exceptions import BuildError


class TestCMake:
    """Test CMake build system."""

    @pytest.fixture
    def cmake(self) -> CMake:
        """Create CMake instance.

        Returns:
            CMake instance
        """
        return CMake()

    @pytest.fixture
    def project_dir(self, tmp_path: Path) -> Path:
        """Create temporary project directory.

        Args:
            tmp_path: Temporary path

        Returns:
            Project directory
        """
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        # Create CMakeLists.txt
        cmake_file = project_dir / "CMakeLists.txt"
        cmake_file.write_text("""
cmake_minimum_required(VERSION 3.20)
project(TestProject)
""")

        return project_dir

    def test_configure(self, cmake: CMake, project_dir: Path) -> None:
        """Test CMake configuration.

        Args:
            cmake: CMake instance
            project_dir: Project directory
        """
        # Configure project
        cmake.configure(
            source_dir=project_dir,
            build_dir=project_dir / "build"
        )

        # Check if build directory exists
        assert (project_dir / "build").exists()

    def test_build(self, cmake: CMake, project_dir: Path) -> None:
        """Test CMake build.

        Args:
            cmake: CMake instance
            project_dir: Project directory
        """
        # Configure project
        cmake.configure(
            source_dir=project_dir,
            build_dir=project_dir / "build"
        )

        # Build project
        cmake.build(
            build_dir=project_dir / "build"
        )

    def test_clean(self, cmake: CMake, project_dir: Path) -> None:
        """Test CMake clean.

        Args:
            cmake: CMake instance
            project_dir: Project directory
        """
        # Configure and build project
        cmake.configure(
            source_dir=project_dir,
            build_dir=project_dir / "build"
        )
        cmake.build(
            build_dir=project_dir / "build"
        )

        # Clean project
        cmake.clean(
            build_dir=project_dir / "build"
        )

        # Check if build directory is empty
        assert not list((project_dir / "build").glob("*"))

    def test_invalid_source_dir(self, cmake: CMake) -> None:
        """Test invalid source directory.

        Args:
            cmake: CMake instance
        """
        with pytest.raises(BuildError):
            cmake.configure(
                source_dir=Path("/nonexistent"),
                build_dir=Path("/nonexistent/build")
            )

    @pytest.mark.parametrize("generator", ["Ninja", "Unix Makefiles"])
    def test_different_generators(
        self,
        cmake: CMake,
        project_dir: Path,
        generator: str
    ) -> None:
        """Test different CMake generators.

        Args:
            cmake: CMake instance
            project_dir: Project directory
            generator: CMake generator
        """
        # Configure project with generator
        cmake.configure(
            source_dir=project_dir,
            build_dir=project_dir / "build",
            generator=generator
        )

        # Check if build directory exists
        assert (project_dir / "build").exists()
```

### 3. Test Naming Conventions

```python
# Test naming conventions

# 1. Test class name: Test<ClassName>
class TestCMake:
    """Test CMake build system."""
    pass

# 2. Test function name: test_<feature>_<behavior>
def test_configure():
    """Test CMake configuration."""
    pass

def test_build():
    """Test CMake build."""
    pass

def test_clean():
    """Test CMake clean."""
    pass

# 3. Parameterized test: test_<feature>_<behavior>_<parameter>
@pytest.mark.parametrize("generator", ["Ninja", "Unix Makefiles"])
def test_configure_with_generator(generator):
    """Test CMake configuration with different generators."""
    pass

# 4. Async test: test_<feature>_<behavior>_async
@pytest.mark.asyncio
async def test_async_operation():
    """Test async operation."""
    pass

# 5. Fixture name: <feature>_fixture
@pytest.fixture
def cmake_fixture():
    """Create CMake fixture."""
    return CMake()
```

### 4. Test Documentation

```python
# tests/unit/build_system/test_cmake.py
# CMake build system tests
#
# This file contains unit tests for the CMake build system.
#
# Test Coverage:
# - Configuration (configure)
# - Building (build)
# - Cleaning (clean)
# - Error handling (invalid source directory)
# - Different generators (Ninja, Unix Makefiles)
#
# Test Organization:
# - Test class: TestCMake
# - Test naming: test_<feature>_<behavior>
# - Test documentation: Each test has a docstring
#
# Dependencies:
# - pytest framework
# - pytest-cov for coverage
# - pytest-mock for mocking
# - CMake class
#
# Author: OmniCpp Team
# Date: 2026-01-07
```

### 5. pytest.ini

```ini
# pytest.ini
# pytest configuration file

[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Test options
addopts =
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=omni_scripts
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    skip_ci: Skip tests in CI
```

### 6. conftest.py

```python
# tests/conftest.py
# pytest configuration and fixtures

import pytest
from pathlib import Path
from typing import Generator
import tempfile
import shutil


@pytest.fixture
def tmp_path() -> Generator[Path, None, None]:
    """Create temporary directory.

    Yields:
        Temporary directory path
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create temporary project directory.

    Args:
        tmp_path: Temporary path

    Yields:
        Project directory path
    """
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    # Create CMakeLists.txt
    cmake_file = project_dir / "CMakeLists.txt"
    cmake_file.write_text("""
cmake_minimum_required(VERSION 3.20)
project(TestProject)
""")

    yield project_dir

    # Cleanup
    if project_dir.exists():
        shutil.rmtree(project_dir)


@pytest.fixture
def build_dir(project_dir: Path) -> Generator[Path, None, None]:
    """Create temporary build directory.

    Args:
        project_dir: Project directory

    Yields:
        Build directory path
    """
    build_dir = project_dir / "build"
    build_dir.mkdir()

    yield build_dir

    # Cleanup
    if build_dir.exists():
        shutil.rmtree(build_dir)


@pytest.fixture
def mock_logger():
    """Create mock logger.

    Returns:
        Mock logger
    """
    from unittest.mock import MagicMock
    logger = MagicMock()
    logger.info = MagicMock()
    logger.debug = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    return logger
```

### 7. Usage Examples

```python
# Example: Run all tests
# pytest

# Example: Run specific test file
# pytest tests/unit/build_system/test_cmake.py

# Example: Run specific test
# pytest tests/unit/build_system/test_cmake.py::TestCMake::test_configure

# Example: Run tests with coverage
# pytest --cov=omni_scripts --cov-report=html

# Example: Run tests with markers
# pytest -m unit
# pytest -m integration
# pytest -m "not slow"

# Example: Run tests with verbose output
# pytest -v

# Example: Run tests with short traceback
# pytest --tb=short

# Example: Run tests with coverage threshold
# pytest --cov=omni_scripts --cov-fail-under=80
```

## Consequences

### Positive

1. **Framework:** Consistent testing framework
2. **Coverage:** Code coverage tracking
3. **Integration:** Integration with build system
4. **CI/CD:** CI/CD integration
5. **Reporting:** Test reporting
6. **Standards:** Testing standards
7. **Documentation:** Test documentation
8. **Mocking:** pytest-mock for mocking
9. **Async:** pytest-asyncio for async testing

### Negative

1. **Complexity:** More complex than no testing
2. **Build Time:** Tests add build time
3. **Maintenance:** Tests need to be maintained
4. **Learning Curve:** Learning curve for pytest

### Neutral

1. **Documentation:** Requires documentation for testing
2. **Training:** Need to train developers on pytest

## Alternatives Considered

### Alternative 1: No Testing Framework

**Description:** No testing framework

**Pros:**
- Simpler implementation
- No build time overhead

**Cons:**
- No consistent testing
- No code coverage
- No CI/CD integration

**Rejected:** No consistent testing and no code coverage

### Alternative 2: unittest

**Description:** Use unittest for testing

**Pros:**
- Built-in to Python
- No dependencies

**Cons:**
- Less flexible than pytest
- More verbose
- Less features

**Rejected:** Less flexible and more verbose

### Alternative 3: nose2

**Description:** Use nose2 for testing

**Pros:**
- Extends unittest
- More features

**Cons:**
- Less popular than pytest
- Less active development
- Less community support

**Rejected:** Less popular and less active development

## Related ADRs

- [ADR-022: Google Test for C++ unit tests](ADR-022-google-test-cpp-unit-tests.md)
- [ADR-024: Code coverage requirements (80%)](ADR-024-code-coverage-requirements.md)

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
