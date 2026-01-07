# DES-001: OmniCppController.py Interface Design

## Overview
Defines the main entry point interface for the OmniCppController, providing a unified command-line interface for all build system operations.

## Interface Definition

### Python Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    """Logging levels for controller operations"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Command(Enum):
    """Available controller commands"""
    BUILD = "build"
    CLEAN = "clean"
    CONFIGURE = "configure"
    INSTALL = "install"
    TEST = "test"
    LINT = "lint"
    FORMAT = "format"
    PACKAGE = "package"
    CONFIG = "config"

@dataclass
class ControllerConfig:
    """Configuration for the controller"""
    project_root: str
    build_dir: str = "build"
    config_dir: str = "config"
    log_level: LogLevel = LogLevel.INFO
    verbose: bool = False
    dry_run: bool = False
    parallel_jobs: int = 1

@dataclass
class CommandResult:
    """Result of a command execution"""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    execution_time: float
    command: str

class IOmniCppController(ABC):
    """Interface for OmniCppController"""

    @abstractmethod
    def __init__(self, config: ControllerConfig) -> None:
        """Initialize the controller with configuration"""
        pass

    @abstractmethod
    def execute(self, command: Command, args: List[str]) -> CommandResult:
        """Execute a command with given arguments"""
        pass

    @abstractmethod
    def build(self, target: Optional[str] = None, config: Optional[str] = None) -> CommandResult:
        """Build the project"""
        pass

    @abstractmethod
    def clean(self, target: Optional[str] = None) -> CommandResult:
        """Clean build artifacts"""
        pass

    @abstractmethod
    def configure(self, generator: Optional[str] = None, toolchain: Optional[str] = None) -> CommandResult:
        """Configure the build system"""
        pass

    @abstractmethod
    def install(self, prefix: Optional[str] = None) -> CommandResult:
        """Install the project"""
        pass

    @abstractmethod
    def test(self, filter: Optional[str] = None) -> CommandResult:
        """Run tests"""
        pass

    @abstractmethod
    def lint(self, fix: bool = False) -> CommandResult:
        """Run linting"""
        pass

    @abstractmethod
    def format(self, check: bool = False) -> CommandResult:
        """Format code"""
        pass

    @abstractmethod
    def package(self, type: Optional[str] = None) -> CommandResult:
        """Create package"""
        pass

    @abstractmethod
    def config(self, action: str, key: Optional[str] = None, value: Optional[str] = None) -> CommandResult:
        """Manage configuration"""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get controller version"""
        pass

    @abstractmethod
    def get_help(self, command: Optional[Command] = None) -> str:
        """Get help information"""
        pass

class OmniCppController(IOmniCppController):
    """Main implementation of OmniCppController"""

    def __init__(self, config: ControllerConfig) -> None:
        """Initialize the controller"""
        self._config = config
        self._logger = None  # Will be initialized with logging system
        self._platform_detector = None
        self._compiler_detector = None
        self._package_manager = None
        self._build_system = None

    def execute(self, command: Command, args: List[str]) -> CommandResult:
        """Execute a command with given arguments"""
        # Implementation will delegate to specific command methods
        pass

    def build(self, target: Optional[str] = None, config: Optional[str] = None) -> CommandResult:
        """Build the project"""
        pass

    def clean(self, target: Optional[str] = None) -> CommandResult:
        """Clean build artifacts"""
        pass

    def configure(self, generator: Optional[str] = None, toolchain: Optional[str] = None) -> CommandResult:
        """Configure the build system"""
        pass

    def install(self, prefix: Optional[str] = None) -> CommandResult:
        """Install the project"""
        pass

    def test(self, filter: Optional[str] = None) -> CommandResult:
        """Run tests"""
        pass

    def lint(self, fix: bool = False) -> CommandResult:
        """Run linting"""
        pass

    def format(self, check: bool = False) -> CommandResult:
        """Format code"""
        pass

    def package(self, type: Optional[str] = None) -> CommandResult:
        """Create package"""
        pass

    def config(self, action: str, key: Optional[str] = None, value: Optional[str] = None) -> CommandResult:
        """Manage configuration"""
        pass

    def get_version(self) -> str:
        """Get controller version"""
        return "1.0.0"

    def get_help(self, command: Optional[Command] = None) -> str:
        """Get help information"""
        pass
```

## Dependencies

### Internal Dependencies
- `omni_scripts.logging.logger` - Logging functionality
- `omni_scripts.platform.detector` - Platform detection
- `omni_scripts.compilers.detector` - Compiler detection
- `omni_scripts.build_system.cmake` - CMake integration
- `omni_scripts.build_system.conan` - Conan integration
- `omni_scripts.build_system.vcpkg` - vcpkg integration

### External Dependencies
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations
- `argparse` - Command-line argument parsing

## Related Requirements
- REQ-001: OmniCpp Controller Entry Point
- REQ-002: Modular Controller Pattern
- REQ-003: Type Hints Enforcement
- REQ-004: Python Script Consolidation
- REQ-005: Logging Configuration
- REQ-006: Error Handling & Exception Management
- REQ-007: Configuration Management
- REQ-008: Command Line Interface

## Related ADRs
- ADR-001: Python Build System Architecture
- ADR-002: Modular Controller Pattern
- ADR-003: Type Hints Enforcement Strategy

## Implementation Notes

### Initialization Flow
1. Load configuration from config files
2. Initialize logging system
3. Detect platform and compiler
4. Initialize package manager
5. Initialize build system
6. Validate environment

### Command Execution Flow
1. Parse command and arguments
2. Validate preconditions
3. Execute command
4. Capture output
5. Handle errors
6. Return result

### Error Handling
- All methods should raise appropriate exceptions
- Use custom exception hierarchy (see DES-005)
- Log errors before raising
- Provide meaningful error messages

### Thread Safety
- Controller is not thread-safe by default
- Each command should be executed sequentially
- Parallel execution should be handled by individual controllers

## Usage Example

```python
from omni_scripts.controller import OmniCppController, ControllerConfig, Command

# Initialize controller
config = ControllerConfig(
    project_root="/path/to/project",
    log_level=LogLevel.INFO,
    verbose=True
)
controller = OmniCppController(config)

# Execute commands
result = controller.build(config="Release")
if result.success:
    print("Build successful!")
else:
    print(f"Build failed: {result.stderr}")
```

## Testing Considerations
- Mock all external dependencies
- Test all command paths
- Test error conditions
- Test with various configurations
- Test with different platforms and compilers
