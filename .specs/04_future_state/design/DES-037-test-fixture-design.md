# DES-037: Test Fixture Design

## Overview

Defines the test fixture design for OmniCpp build system and C++ engine testing.

## Interface Definition

### Python Code

```python
"""
Test Fixture Design for OmniCpp

This module defines the test fixture design for testing the build system and C++ engine.
"""

import os
import sys
import tempfile
import shutil
from typing import Optional, Callable, Dict, List, Any, Type
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod
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


class TestStatus(Enum):
    """Test status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    RUNNING = "running"


@dataclass
class TestResult:
    """Test result"""
    test_name: str
    status: TestStatus
    duration: float = 0.0
    message: str = ""
    error: Optional[str] = None
    traceback: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert test result to dictionary"""
        return {
            "test_name": self.test_name,
            "status": self.status.value,
            "duration": self.duration,
            "message": self.message,
            "error": self.error,
            "traceback": self.traceback,
            "metadata": self.metadata
        }

    def __str__(self) -> str:
        """String representation of test result"""
        return f"{self.test_name}: {self.status.value} ({self.duration:.2f}s)"


@dataclass
class TestSuite:
    """Test suite"""
    name: str
    description: str = ""
    category: TestCategory = TestCategory.UTILS
    scope: TestScope = TestScope.UNIT
    tests: List[str] = field(default_factory=list)
    fixtures: List[str] = field(default_factory=list)
    setup_timeout: float = 30.0
    teardown_timeout: float = 30.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert test suite to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "scope": self.scope.value,
            "tests": self.tests,
            "fixtures": self.fixtures,
            "setup_timeout": self.setup_timeout,
            "teardown_timeout": self.teardown_timeout
        }


class ITestFixture(ABC):
    """Test fixture interface"""

    @abstractmethod
    def setup(self) -> None:
        """Set up the test fixture"""
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Tear down the test fixture"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the fixture name"""
        pass

    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Get fixture dependencies"""
        pass

    def setup_with_timeout(self, timeout: float) -> bool:
        """Set up the test fixture with timeout"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Fixture setup timed out after {timeout} seconds")

        # Set timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        try:
            self.setup()
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            return True
        except TimeoutError:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            return False

    def teardown_with_timeout(self, timeout: float) -> bool:
        """Tear down the test fixture with timeout"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Fixture teardown timed out after {timeout} seconds")

        # Set timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        try:
            self.teardown()
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            return True
        except TimeoutError:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            return False


class BaseTestFixture(ITestFixture):
    """Base test fixture implementation"""

    def __init__(self, name: str):
        self._name = name
        self._temp_dir: Optional[Path] = None
        self._setup_complete = False

    def setup(self) -> None:
        """Set up the test fixture"""
        self._temp_dir = Path(tempfile.mkdtemp(prefix=f"fixture_{self._name}_"))
        self._setup_complete = True

    def teardown(self) -> None:
        """Tear down the test fixture"""
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir)
        self._temp_dir = None
        self._setup_complete = False

    def get_name(self) -> str:
        """Get the fixture name"""
        return self._name

    def get_dependencies(self) -> List[str]:
        """Get fixture dependencies"""
        return []

    def get_temp_dir(self) -> Path:
        """Get the temporary directory"""
        if not self._temp_dir:
            self._temp_dir = Path(tempfile.mkdtemp(prefix=f"fixture_{self._name}_"))
        return self._temp_dir

    def is_setup_complete(self) -> bool:
        """Check if setup is complete"""
        return self._setup_complete


class BuildSystemFixture(BaseTestFixture):
    """Build system test fixture"""

    def __init__(self, name: str = "BuildSystem"):
        super().__init__(name)
        self._config_dir: Optional[Path] = None
        self._build_dir: Optional[Path] = None

    def setup(self) -> None:
        """Set up the build system fixture"""
        super().setup()

        # Create config directory
        self._config_dir = self.get_temp_dir() / "config"
        self._config_dir.mkdir(parents=True, exist_ok=True)

        # Create build directory
        self._build_dir = self.get_temp_dir() / "build"
        self._build_dir.mkdir(parents=True, exist_ok=True)

        # Copy configuration files
        config_source = Path("config")
        if config_source.exists():
            for file in config_source.glob("*.json"):
                shutil.copy2(file, self._config_dir / file.name)

    def teardown(self) -> None:
        """Tear down the build system fixture"""
        super().teardown()
        self._config_dir = None
        self._build_dir = None

    def get_config_dir(self) -> Path:
        """Get the config directory"""
        return self._config_dir

    def get_build_dir(self) -> Path:
        """Get the build directory"""
        return self._build_dir


class CompilerFixture(BaseTestFixture):
    """Compiler test fixture"""

    def __init__(self, name: str = "Compiler"):
        super().__init__(name)
        self._test_source_dir: Optional[Path] = None
        self._test_output_dir: Optional[Path] = None

    def setup(self) -> None:
        """Set up the compiler fixture"""
        super().setup()

        # Create test source directory
        self._test_source_dir = self.get_temp_dir() / "source"
        self._test_source_dir.mkdir(parents=True, exist_ok=True)

        # Create test output directory
        self._test_output_dir = self.get_temp_dir() / "output"
        self._test_output_dir.mkdir(parents=True, exist_ok=True)

        # Create test source files
        test_source = self._test_source_dir / "test.cpp"
        test_source.write_text("""
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
""")

    def teardown(self) -> None:
        """Tear down the compiler fixture"""
        super().teardown()
        self._test_source_dir = None
        self._test_output_dir = None

    def get_test_source_dir(self) -> Path:
        """Get the test source directory"""
        return self._test_source_dir

    def get_test_output_dir(self) -> Path:
        """Get the test output directory"""
        return self._test_output_dir


class PackageManagerFixture(BaseTestFixture):
    """Package manager test fixture"""

    def __init__(self, name: str = "PackageManager"):
        super().__init__(name)
        self._package_cache_dir: Optional[Path] = None
        self._test_package_dir: Optional[Path] = None

    def setup(self) -> None:
        """Set up the package manager fixture"""
        super().setup()

        # Create package cache directory
        self._package_cache_dir = self.get_temp_dir() / "cache"
        self._package_cache_dir.mkdir(parents=True, exist_ok=True)

        # Create test package directory
        self._test_package_dir = self.get_temp_dir() / "packages"
        self._test_package_dir.mkdir(parents=True, exist_ok=True)

        # Create test package
        test_package = self._test_package_dir / "test_package"
        test_package.mkdir(parents=True, exist_ok=True)
        test_package.joinpath("CMakeLists.txt").write_text("""
cmake_minimum_required(VERSION 3.10)
project(TestPackage)

add_executable(test_app main.cpp)
""")

    def teardown(self) -> None:
        """Tear down the package manager fixture"""
        super().teardown()
        self._package_cache_dir = None
        self._test_package_dir = None

    def get_package_cache_dir(self) -> Path:
        """Get the package cache directory"""
        return self._package_cache_dir

    def get_test_package_dir(self) -> Path:
        """Get the test package directory"""
        return self._test_package_dir


class EngineFixture(BaseTestFixture):
    """Engine test fixture"""

    def __init__(self, name: str = "Engine"):
        super().__init__(name)
        self._engine_lib_dir: Optional[Path] = None
        self._test_scene_dir: Optional[Path] = None

    def setup(self) -> None:
        """Set up the engine fixture"""
        super().setup()

        # Create engine library directory
        self._engine_lib_dir = self.get_temp_dir() / "lib"
        self._engine_lib_dir.mkdir(parents=True, exist_ok=True)

        # Create test scene directory
        self._test_scene_dir = self.get_temp_dir() / "scenes"
        self._test_scene_dir.mkdir(parents=True, exist_ok=True)

        # Create test scene
        test_scene = self._test_scene_dir / "test_scene.json"
        test_scene.write_text("""
{
    "name": "TestScene",
    "entities": []
}
""")

    def teardown(self) -> None:
        """Tear down the engine fixture"""
        super().teardown()
        self._engine_lib_dir = None
        self._test_scene_dir = None

    def get_engine_lib_dir(self) -> Path:
        """Get the engine library directory"""
        return self._engine_lib_dir

    def get_test_scene_dir(self) -> Path:
        """Get the test scene directory"""
        return self._test_scene_dir


class TestFixtureManager:
    """Test fixture manager"""

    def __init__(self):
        self._fixtures: Dict[str, ITestFixture] = {}
        self._fixture_dependencies: Dict[str, List[str]] = {}

    def register_fixture(self, fixture: ITestFixture) -> None:
        """Register a test fixture"""
        self._fixtures[fixture.get_name()] = fixture
        self._fixture_dependencies[fixture.get_name()] = fixture.get_dependencies()

    def unregister_fixture(self, name: str) -> None:
        """Unregister a test fixture"""
        if name in self._fixtures:
            del self._fixtures[name]
            if name in self._fixture_dependencies:
                del self._fixture_dependencies[name]

    def get_fixture(self, name: str) -> Optional[ITestFixture]:
        """Get a test fixture by name"""
        return self._fixtures.get(name)

    def get_all_fixtures(self) -> List[ITestFixture]:
        """Get all test fixtures"""
        return list(self._fixtures.values())

    def setup_fixtures(self, fixture_names: List[str]) -> bool:
        """Set up multiple fixtures"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Fixture setup timed out")

        # Set timeout for each fixture
        for name in fixture_names:
            fixture = self.get_fixture(name)
            if fixture:
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(fixture.setup_timeout)

                try:
                    fixture.setup()
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                except TimeoutError:
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                    return False

        return True

    def teardown_fixtures(self, fixture_names: List[str]) -> bool:
        """Tear down multiple fixtures"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Fixture teardown timed out")

        # Set timeout for each fixture
        for name in fixture_names:
            fixture = self.get_fixture(name)
            if fixture:
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(fixture.teardown_timeout)

                try:
                    fixture.teardown()
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                except TimeoutError:
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                    return False

        return True

    def cleanup_all_fixtures(self) -> None:
        """Clean up all fixtures"""
        for fixture in self.get_all_fixtures():
            fixture.teardown()
```

## Dependencies

### Internal Dependencies

- `DES-001` - OmniCpp Controller Interface
- `DES-002` - Controller Base Class

### External Dependencies

- `os` - Operating system interface
- `sys` - System-specific parameters
- `tempfile` - Temporary file handling
- `shutil` - File operations
- `typing` - Type hints
- `dataclasses` - Data structures
- `pathlib` - Path handling
- `abc` - Abstract base classes
- `enum` - Enumerations
- `signal` - Signal handling

## Related Requirements

- REQ-060: Test Framework
- REQ-061: Test Fixtures

## Related ADRs

- ADR-004: Testing Architecture

## Implementation Notes

### Fixture Design

1. Abstract fixture interface
2. Base fixture implementation
3. Domain-specific fixtures
4. Fixture dependencies

### Fixture Lifecycle

1. Setup with timeout
2. Teardown with timeout
3. Temporary directory management
4. Cleanup on failure

### Fixture Types

1. Build system fixture
2. Compiler fixture
3. Package manager fixture
4. Engine fixture

### Fixture Manager

1. Register/unregister fixtures
2. Setup/teardown multiple fixtures
3. Fixture dependency management
4. Cleanup all fixtures

## Usage Example

```python
from omni_scripts.testing import (
    TestFixtureManager,
    BuildSystemFixture,
    CompilerFixture,
    PackageManagerFixture,
    EngineFixture,
    TestResult,
    TestStatus
)

# Create fixture manager
manager = TestFixtureManager()

# Register fixtures
manager.register_fixture(BuildSystemFixture())
manager.register_fixture(CompilerFixture())
manager.register_fixture(PackageManagerFixture())
manager.register_fixture(EngineFixture())

# Setup fixtures
fixture_names = ["BuildSystem", "Compiler", "PackageManager", "Engine"]
success = manager.setup_fixtures(fixture_names)

if success:
    # Run tests
    build_fixture = manager.get_fixture("BuildSystem")
    config_dir = build_fixture.get_config_dir()
    print(f"Config directory: {config_dir}")

    # Create test result
    result = TestResult(
        test_name="TestBuildSystem",
        status=TestStatus.PASSED,
        duration=1.5,
        message="Build system test passed"
    )
    print(result)

    # Teardown fixtures
    manager.teardown_fixtures(fixture_names)
else:
    print("Fixture setup failed")
```
