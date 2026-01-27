# Test Plan - TDD Strategy

**Document Version:** 1.0.0
**Created:** 2026-01-07
**Last Updated:** 2026-01-07
**Status:** Draft

---

## Table of Contents

1. [Overview](#overview)
2. [Test Philosophy](#test-philosophy)
3. [Test Organization Structure](#test-organization-structure)
4. [Test Scenarios by Domain](#test-scenarios-by-domain)
5. [Test Coverage Requirements](#test-coverage-requirements)
6. [Test Automation Strategy](#test-automation-strategy)
7. [Test Data Management](#test-data-management)
8. [Test Execution Workflow](#test-execution-workflow)
9. [Test Reporting Strategy](#test-reporting-strategy)
10. [TDD Implementation Guidelines](#tdd-implementation-guidelines)
11. [Test Maintenance](#test-maintenance)
12. [References](#references)

---

## Overview

This test plan defines a comprehensive testing strategy for the OmniCpp build system refactoring, implementing Test-Driven Development (TDD) principles across all domains. The plan ensures high code quality, maintainability, and reliability through systematic testing at unit, integration, system, and end-to-end levels.

### Objectives

- **Quality Assurance:** Ensure 80% minimum code coverage across all components
- **Early Detection:** Identify defects early in the development cycle through TDD
- **Regression Prevention:** Prevent regressions through comprehensive test suites
- **Documentation:** Use tests as living documentation of system behavior
- **Cross-Platform Validation:** Validate behavior across Windows, Linux, macOS, and Emscripten
- **Performance Validation:** Ensure performance requirements are met
- **Security Verification:** Validate security controls and prevent vulnerabilities

### Scope

This test plan covers:

- Python build system (OmniCppController.py and omni_scripts/)
- Cross-platform compilation infrastructure
- Package manager integrations (Conan, vcpkg, CPM)
- CMake build system configuration
- C++ engine components
- C++ game components
- Logging infrastructure (Python and C++)
- Security controls
- VSCode integration

---

## Test Philosophy

### Test-Driven Development (TDD) Principles

#### Red-Green-Refactor Cycle

1. **Red:** Write a failing test that defines a desired behavior
2. **Green:** Write the minimum code to make the test pass
3. **Refactor:** Improve the code while keeping tests green

#### Test First Approach

- **Before Implementation:** Write tests before implementing features
- **Incremental Development:** Build features incrementally with tests
- **Continuous Validation:** Run tests continuously during development
- **Refactoring Safety:** Refactor with confidence using test coverage

### Testing Pyramid

```
        /\
       /E2E\      - 5%  (End-to-End Tests)
      /------\
     /System \     - 10% (System Tests)
    /--------\
   /Integration\  - 25% (Integration Tests)
  /----------\
 /   Unit     \ - 60% (Unit Tests)
/______________\
```

### Test Categories

1. **Unit Tests:** Test individual functions, classes, and methods in isolation
2. **Integration Tests:** Test interactions between components
3. **System Tests:** Test complete subsystems
4. **End-to-End Tests:** Test complete workflows from user perspective
5. **Performance Tests:** Validate performance characteristics
6. **Security Tests:** Validate security controls
7. **Cross-Platform Tests:** Validate behavior across platforms

---

## Test Organization Structure

### Directory Structure

```
tests/
├── python/
│   ├── unit/
│   │   ├── controller/
│   │   │   ├── test_base_controller.py
│   │   │   ├── test_build_controller.py
│   │   │   ├── test_clean_controller.py
│   │   │   ├── test_configure_controller.py
│   │   │   ├── test_format_controller.py
│   │   │   ├── test_install_controller.py
│   │   │   ├── test_lint_controller.py
│   │   │   ├── test_package_controller.py
│   │   │   └── test_test_controller.py
│   │   ├── platform/
│   │   │   ├── test_detector.py
│   │   │   ├── test_windows.py
│   │   │   ├── test_linux.py
│   │   │   └── test_macos.py
│   │   ├── compilers/
│   │   │   ├── test_detector.py
│   │   │   ├── test_msvc.py
│   │   │   ├── test_gcc.py
│   │   │   ├── test_clang.py
│   │   │   └── test_mingw.py
│   │   ├── package_managers/
│   │   │   ├── test_conan.py
│   │   │   ├── test_vcpkg.py
│   │   │   └── test_cpm.py
│   │   ├── build_system/
│   │   │   ├── test_cmake.py
│   │   │   ├── test_presets.py
│   │   │   └── test_toolchain.py
│   │   ├── logging/
│   │   │   ├── test_logger.py
│   │   │   ├── test_formatters.py
│   │   │   └── test_handlers.py
│   │   ├── config/
│   │   │   ├── test_config_manager.py
│   │   │   └── test_config_loader.py
│   │   └── utils/
│   │       ├── test_file_utils.py
│   │       ├── test_path_utils.py
│   │       └── test_terminal_utils.py
│   ├── integration/
│   │   ├── test_controller_integration.py
│   │   ├── test_platform_compiler_integration.py
│   │   ├── test_package_manager_integration.py
│   │   ├── test_build_system_integration.py
│   │   └── test_logging_integration.py
│   ├── system/
│   │   ├── test_full_build_workflow.py
│   │   ├── test_cross_platform_build.py
│   │   └── test_package_manager_workflow.py
│   ├── e2e/
│   │   ├── test_complete_workflow.py
│   │   └── test_user_scenarios.py
│   ├── performance/
│   │   ├── test_build_performance.py
│   │   ├── test_parallel_build.py
│   │   └── test_cache_performance.py
│   ├── security/
│   │   ├── test_terminal_security.py
│   │   ├── test_dependency_integrity.py
│   │   └── test_logging_security.py
│   └── fixtures/
│       ├── build_system_fixture.py
│       ├── compiler_fixture.py
│       ├── package_manager_fixture.py
│       └── engine_fixture.py
├── cpp/
│   ├── unit/
│   │   ├── engine/
│   │   │   ├── core/
│   │   │   │   ├── test_engine.cpp
│   │   │   │   └── test_engine_core.cpp
│   │   │   ├── ecs/
│   │   │   │   ├── test_entity.cpp
│   │   │   │   ├── test_component.cpp
│   │   │   │   └── test_system.cpp
│   │   │   ├── graphics/
│   │   │   │   ├── test_renderer.cpp
│   │   │   │   └── test_shader_manager.cpp
│   │   │   ├── audio/
│   │   │   │   └── test_audio_manager.cpp
│   │   │   ├── physics/
│   │   │   │   └── test_physics_engine.cpp
│   │   │   ├── resources/
│   │   │   │   └── test_resource_manager.cpp
│   │   │   └── scene/
│   │   │       └── test_scene_manager.cpp
│   │   ├── game/
│   │   │   ├── core/
│   │   │   │   └── test_game.cpp
│   │   │   ├── scene/
│   │   │   │   └── test_game_scene.cpp
│   │   │   └── entity/
│   │   │       └── test_game_entity.cpp
│   │   └── logging/
│   │       └── test_logger.cpp
│   ├── integration/
│   │   ├── test_engine_integration.cpp
│   │   ├── test_ecs_integration.cpp
│   │   └── test_game_integration.cpp
│   └── performance/
│       ├── test_rendering_performance.cpp
│       ├── test_physics_performance.cpp
│       └── test_resource_loading_performance.cpp
├── cross_platform/
│   ├── windows/
│   │   ├── test_msvc_build.py
│   │   └── test_mingw_build.py
│   ├── linux/
│   │   ├── test_gcc_build.py
│   │   └── test_clang_build.py
│   ├── macos/
│   │   └── test_clang_build.py
│   └── emscripten/
│       └── test_wasm_build.py
├── data/
│   ├── fixtures/
│   │   ├── config/
│   │   │   ├── test_config.json
│   │   │   └── test_logging.json
│   │   ├── source/
│   │   │   ├── test_main.cpp
│   │   │   └── test_engine.cpp
│   │   └── packages/
│   │       └── test_package/
│   │           └── CMakeLists.txt
│   ├── mocks/
│   │   ├── mock_compiler.py
│   │   ├── mock_package_manager.py
│   │   └── mock_terminal.py
│   └── expected/
│       ├── build_output/
│       └── test_results/
├── config/
│   ├── pytest.ini
│   ├── conftest.py
│   └── test_config.json
└── README.md
```

### Test Naming Conventions

#### Python Tests

- **Unit Tests:** `test_<module>_<function>.py`
- **Integration Tests:** `test_<component>_integration.py`
- **System Tests:** `test_<workflow>.py`
- **E2E Tests:** `test_<scenario>.py`

#### C++ Tests

- **Unit Tests:** `test_<class>.cpp`
- **Integration Tests:** `test_<component>_integration.cpp`
- **Performance Tests:** `test_<component>_performance.cpp`

### Test File Organization

Each test file should:

1. **Import Dependencies:** Import necessary modules and fixtures
2. **Define Fixtures:** Define pytest fixtures for setup/teardown
3. **Group Tests:** Group related tests using pytest markers
4. **Document Tests:** Include docstrings explaining test purpose
5. **Use Descriptive Names:** Use descriptive test names following `test_<scenario>_<expected_result>` pattern

---

## Test Scenarios by Domain

### Python Build System Tests

#### OmniCppController.py Entry Point Tests

**Unit Tests**

1. **Test Entry Point Exists**
   - **Description:** Verify OmniCppController.py exists at project root
   - **TDD Approach:**
     - Write test that checks file existence
     - Create OmniCppController.py file
     - Verify test passes
   - **Test Code:**
     ```python
     def test_entry_point_exists():
         """Verify OmniCppController.py exists at project root"""
         from pathlib import Path
         entry_point = Path("OmniCppController.py")
         assert entry_point.exists()
         assert entry_point.is_file()
     ```

2. **Test CLI Interface Commands**
   - **Description:** Verify CLI interface provides all required commands
   - **TDD Approach:**
     - Write test that checks all commands are available
     - Implement CLI with argparse
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cli_commands_available():
         """Verify all required commands are available"""
         from omni_scripts.controller.cli import parse_args
         commands = ["configure", "build", "clean", "install", "test", "package", "format", "lint"]
         for command in commands:
             args = parse_args([command, "--help"])
             assert args.command == command
     ```

3. **Test Command Dispatch**
   - **Description:** Verify commands are dispatched to correct controllers
   - **TDD Approach:**
     - Write test that mocks controller execution
     - Implement dispatcher
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.parametrize("command,controller_class", [
         ("build", BuildController),
         ("clean", CleanController),
         ("test", TestController),
     ])
     def test_command_dispatch(command, controller_class, mocker):
         """Verify commands dispatch to correct controllers"""
         from omni_scripts.controller.dispatcher import dispatch_command
         mock_controller = mocker.patch(f"omni_scripts.controller.{controller_class.__name__}")
         dispatch_command(command, [])
         mock_controller.assert_called_once()
     ```

4. **Test Invalid Command Handling**
   - **Description:** Verify invalid commands display usage and exit with error
   - **TDD Approach:**
     - Write test that expects SystemExit
     - Implement error handling
     - Verify test passes
   - **Test Code:**
     ```python
     def test_invalid_command():
         """Verify invalid commands display usage and exit with error"""
         from omni_scripts.controller.cli import parse_args
         with pytest.raises(SystemExit):
             parse_args(["invalid_command"])
     ```

5. **Test Help Flag**
   - **Description:** Verify --help flag displays usage information
   - **TDD Approach:**
     - Write test that checks help output
     - Implement help flag
     - Verify test passes
   - **Test Code:**
     ```python
     def test_help_flag(capsys):
         """Verify --help flag displays usage information"""
         from omni_scripts.controller.cli import parse_args
         with pytest.raises(SystemExit):
             parse_args(["--help"])
         captured = capsys.readouterr()
         assert "usage:" in captured.out.lower()
     ```

**Integration Tests**

1. **Test Full Build Workflow**
   - **Description:** Verify complete build workflow through entry point
   - **TDD Approach:**
     - Write test that executes full workflow
     - Implement workflow
     - Verify test passes
   - **Test Code:**
     ```python
     def test_full_build_workflow(build_system_fixture):
         """Verify complete build workflow through entry point"""
         from omni_scripts.controller.dispatcher import dispatch_command
         dispatch_command("configure", [])
         result = dispatch_command("build", ["engine", "debug"])
         assert result == 0
     ```

2. **Test All Commands Execute**
   - **Description:** Verify all commands execute successfully
   - **TDD Approach:**
     - Write test that executes all commands
     - Implement all commands
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.parametrize("command", ["configure", "build", "clean", "test"])
     def test_all_commands_execute(command, build_system_fixture):
         """Verify all commands execute successfully"""
         from omni_scripts.controller.dispatcher import dispatch_command
         result = dispatch_command(command, [])
         assert result == 0
     ```

#### Controller Pattern Tests

**Unit Tests**

1. **Test Base Controller Exists**
   - **Description:** Verify base controller class exists and provides required methods
   - **TDD Approach:**
     - Write test that imports BaseController
     - Create BaseController class
     - Verify test passes
   - **Test Code:**
     ```python
     def test_base_controller_exists():
         """Verify base controller class exists"""
         from omni_scripts.controller.base import BaseController
         assert hasattr(BaseController, 'execute')
         assert hasattr(BaseController, 'setup_logging')
         assert hasattr(BaseController, 'load_config')
     ```

2. **Test Controller Inheritance**
   - **Description:** Verify all controllers inherit from base controller
   - **TDD Approach:**
     - Write test that checks inheritance
     - Implement controllers inheriting from BaseController
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.parametrize("controller_class", [
         BuildController,
         CleanController,
         TestController,
     ])
     def test_controller_inheritance(controller_class):
         """Verify all controllers inherit from BaseController"""
         from omni_scripts.controller.base import BaseController
         assert issubclass(controller_class, BaseController)
     ```

3. **Test Controller Execute Method**
   - **Description:** Verify each controller implements execute() method
   - **TDD Approach:**
     - Write test that checks execute method
     - Implement execute methods
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.parametrize("controller_class", [
         BuildController,
         CleanController,
         TestController,
     ])
     def test_controller_execute_method(controller_class):
         """Verify each controller implements execute() method"""
         controller = controller_class()
         assert callable(controller.execute)
     ```

4. **Test Controller Single Responsibility**
   - **Description:** Verify each controller has single, well-defined responsibility
   - **TDD Approach:**
     - Write test that checks controller methods
     - Implement controllers with single responsibility
     - Verify test passes
   - **Test Code:**
     ```python
     def test_build_controller_responsibility():
         """Verify BuildController only handles build operations"""
         controller = BuildController()
         assert hasattr(controller, 'build')
         assert not hasattr(controller, 'clean')
     ```

**Integration Tests**

1. **Test Controller Dispatch**
   - **Description:** Verify dispatcher can route to correct controller
   - **TDD Approach:**
     - Write test that mocks dispatcher
     - Implement dispatcher
     - Verify test passes
   - **Test Code:**
     ```python
     def test_controller_dispatch(mocker):
         """Verify dispatcher routes to correct controllers"""
         from omni_scripts.controller.dispatcher import dispatch_command
         mock_build = mocker.patch.object(BuildController, 'execute')
         dispatch_command("build", [])
         mock_build.assert_called_once()
     ```

2. **Test Controller Error Handling**
   - **Description:** Verify controllers handle errors consistently
   - **TDD Approach:**
     - Write test that triggers errors
     - Implement error handling
     - Verify test passes
   - **Test Code:**
     ```python
     def test_controller_error_handling():
         """Verify controllers handle errors consistently"""
         controller = BuildController()
         with pytest.raises(BuildError):
             controller.execute(["invalid_target"])
     ```

#### Configuration Management Tests

**Unit Tests**

1. **Test Configuration Loading**
   - **Description:** Verify configuration can be loaded from JSON file
   - **TDD Approach:**
     - Write test that loads configuration
     - Implement configuration loader
     - Verify test passes
   - **Test Code:**
     ```python
     def test_configuration_loading(config_file):
         """Verify configuration can be loaded from JSON file"""
         from omni_scripts.config.config_manager import ConfigManager
         manager = ConfigManager()
         config = manager.load(config_file)
         assert config is not None
         assert "version" in config
     ```

2. **Test Configuration Validation**
   - **Description:** Verify configuration is validated against schema
   - **TDD Approach:**
     - Write test that validates configuration
     - Implement validation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_configuration_validation():
         """Verify configuration is validated against schema"""
         from omni_scripts.config.config_manager import ConfigManager
         manager = ConfigManager()
         valid_config = {"version": "1.0.0"}
         assert manager.validate(valid_config) is True
     ```

3. **Test Configuration Merging**
   - **Description:** Verify multiple configuration files can be merged
   - **TDD Approach:**
     - Write test that merges configurations
     - Implement merging logic
     - Verify test passes
   - **Test Code:**
     ```python
     def test_configuration_merging():
         """Verify multiple configuration files can be merged"""
         from omni_scripts.config.config_manager import ConfigManager
         manager = ConfigManager()
         config1 = {"key1": "value1"}
         config2 = {"key2": "value2"}
         merged = manager.merge_configs([config1, config2])
         assert merged["key1"] == "value1"
         assert merged["key2"] == "value2"
     ```

4. **Test Configuration Defaults**
   - **Description:** Verify default values are applied for missing configuration
   - **TDD Approach:**
     - Write test that checks defaults
     - Implement default values
     - Verify test passes
   - **Test Code:**
     ```python
     def test_configuration_defaults():
         """Verify default values are applied"""
         from omni_scripts.config.config_manager import ConfigManager
         manager = ConfigManager()
         config = manager.apply_defaults({})
         assert "version" in config
         assert config["version"] == "1.0.0"
     ```

#### Logging Tests

**Unit Tests**

1. **Test Logger Initialization**
   - **Description:** Verify logger can be initialized from configuration
   - **TDD Approach:**
     - Write test that initializes logger
     - Implement logger initialization
     - Verify test passes
   - **Test Code:**
     ```python
     def test_logger_initialization(logging_config):
         """Verify logger can be initialized from configuration"""
         from omni_scripts.logging.logger import Logger
         logger = Logger.from_config(logging_config)
         assert logger is not None
         assert logger.level == logging.INFO
     ```

2. **Test Colored Formatter**
   - **Description:** Verify colored console formatter works correctly
   - **TDD Approach:**
     - Write test that checks colored output
     - Implement colored formatter
     - Verify test passes
   - **Test Code:**
     ```python
     def test_colored_formatter():
         """Verify colored console formatter works"""
         from omni_scripts.logging.formatters import ColoredFormatter
         formatter = ColoredFormatter()
         record = logging.LogRecord(
             name="test", level=logging.INFO, pathname="", lineno=0,
             msg="Test message", args=(), exc_info=None
         )
         formatted = formatter.format(record)
         assert "\033[" in formatted  # ANSI color codes
     ```

3. **Test Structured Logging**
   - **Description:** Verify structured logging with context works
   - **TDD Approach:**
     - Write test that logs with context
     - Implement structured logging
     - Verify test passes
   - **Test Code:**
     ```python
     def test_structured_logging(caplog):
         """Verify structured logging with context"""
         from omni_scripts.logging.logger import Logger
         logger = Logger("test")
         with caplog.at_level(logging.INFO):
             logger.info("Test message", extra={"context": "test_context"})
         assert "context" in caplog.text
     ```

4. **Test File Rotation**
   - **Description:** Verify log file rotation works correctly
   - **TDD Approach:**
     - Write test that triggers rotation
     - Implement file rotation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_file_rotation(tmp_path):
         """Verify log file rotation works"""
         from omni_scripts.logging.handlers import RotatingFileHandler
         log_file = tmp_path / "test.log"
         handler = RotatingFileHandler(str(log_file), maxBytes=1024, backupCount=3)
         # Write enough data to trigger rotation
         for i in range(1000):
             handler.emit(logging.LogRecord(
                 name="test", level=logging.INFO, pathname="", lineno=0,
                 msg=f"Test message {i}", args=(), exc_info=None
             ))
         assert log_file.exists()
         assert len(list(tmp_path.glob("test.log.*"))) > 0
     ```

5. **Test Sensitive Data Redaction**
   - **Description:** Verify sensitive data is redacted from logs
   - **TDD Approach:**
     - Write test that logs sensitive data
     - Implement redaction
     - Verify test passes
   - **Test Code:**
     ```python
     def test_sensitive_data_redaction(caplog):
         """Verify sensitive data is redacted from logs"""
         from omni_scripts.logging.formatters import RedactingFormatter
         formatter = RedactingFormatter()
         record = logging.LogRecord(
             name="test", level=logging.INFO, pathname="", lineno=0,
             msg="Password: secret123", args=(), exc_info=None
         )
         formatted = formatter.format(record)
         assert "secret123" not in formatted
         assert "***" in formatted
     ```

#### Error Handling Tests

**Unit Tests**

1. **Test Custom Exceptions**
   - **Description:** Verify custom exception classes exist and work correctly
   - **TDD Approach:**
     - Write test that raises custom exception
     - Create custom exception classes
     - Verify test passes
   - **Test Code:**
     ```python
     def test_custom_exceptions():
         """Verify custom exception classes exist"""
         from omni_scripts.exceptions import BuildError, ConfigError, CompilerError
         with pytest.raises(BuildError):
             raise BuildError("Build failed")
         with pytest.raises(ConfigError):
             raise ConfigError("Invalid config")
         with pytest.raises(CompilerError):
             raise CompilerError("Compiler error")
     ```

2. **Test Exception Context**
   - **Description:** Verify exceptions include context information
   - **TDD Approach:**
     - Write test that checks exception context
     - Implement exception context
     - Verify test passes
   - **Test Code:**
     ```python
     def test_exception_context():
         """Verify exceptions include context information"""
         from omni_scripts.exceptions import BuildError
         error = BuildError("Build failed", command="build", file="test.cpp")
         assert error.command == "build"
         assert error.file == "test.cpp"
     ```

3. **Test Exception Logging**
   - **Description:** Verify exceptions are logged with appropriate level
   - **TDD Approach:**
     - Write test that logs exception
     - Implement exception logging
     - Verify test passes
   - **Test Code:**
     ```python
     def test_exception_logging(caplog):
         """Verify exceptions are logged with appropriate level"""
         from omni_scripts.exceptions import BuildError
         from omni_scripts.logging.logger import Logger
         logger = Logger("test")
         with caplog.at_level(logging.ERROR):
             try:
                 raise BuildError("Build failed")
             except BuildError as e:
                 logger.error(str(e))
         assert "Build failed" in caplog.text
     ```

4. **Test Exit Code Consistency**
   - **Description:** Verify exit codes are consistent across commands
   - **TDD Approach:**
     - Write test that checks exit codes
     - Implement exit codes
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.parametrize("exception_class,expected_exit_code", [
         (BuildError, 1),
         (ConfigError, 2),
         (CompilerError, 3),
     ])
     def test_exit_code_consistency(exception_class, expected_exit_code):
         """Verify exit codes are consistent"""
         from omni_scripts.exceptions import BuildError, ConfigError, CompilerError
         error = exception_class("Test error")
         assert error.exit_code == expected_exit_code
     ```

#### CLI Argument Parsing Tests

**Unit Tests**

1. **Test Required Arguments**
   - **Description:** Verify required arguments are validated
   - **TDD Approach:**
     - Write test that checks required arguments
     - Implement argument validation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_required_arguments():
         """Verify required arguments are validated"""
         from omni_scripts.controller.cli import parse_args
         with pytest.raises(SystemExit):
             parse_args([])  # No command provided
     ```

2. **Test Optional Arguments**
   - **Description:** Verify optional arguments work correctly
   - **TDD Approach:**
     - Write test that uses optional arguments
     - Implement optional arguments
     - Verify test passes
   - **Test Code:**
     ```python
     def test_optional_arguments():
         """Verify optional arguments work correctly"""
         from omni_scripts.controller.cli import parse_args
         args = parse_args(["build", "engine", "debug", "--verbose"])
         assert args.verbose is True
     ```

3. **Test Argument Types**
   - **Description:** Verify argument types are validated
   - **TDD Approach:**
     - Write test that validates types
     - Implement type validation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_argument_types():
         """Verify argument types are validated"""
         from omni_scripts.controller.cli import parse_args
         args = parse_args(["build", "engine", "debug", "--jobs", "4"])
         assert isinstance(args.jobs, int)
         assert args.jobs == 4
     ```

4. **Test Help Messages**
   - **Description:** Verify help messages are displayed correctly
   - **TDD Approach:**
     - Write test that checks help output
     - Implement help messages
     - Verify test passes
   - **Test Code:**
     ```python
     def test_help_messages(capsys):
         """Verify help messages are displayed correctly"""
         from omni_scripts.controller.cli import parse_args
         with pytest.raises(SystemExit):
             parse_args(["--help"])
         captured = capsys.readouterr()
         assert "OmniCpp" in captured.out
     ```

---

### Cross-Platform Compilation Tests

#### Platform Detection Tests

**Unit Tests**

1. **Test Windows Detection**
   - **Description:** Verify Windows platform is detected correctly
   - **TDD Approach:**
     - Write test that detects Windows
     - Implement Windows detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
     def test_windows_detection():
         """Verify Windows platform is detected correctly"""
         from omni_scripts.platform.detector import PlatformDetector
         detector = PlatformDetector()
         assert detector.get_platform() == "windows"
     ```

2. **Test Linux Detection**
   - **Description:** Verify Linux platform is detected correctly
   - **TDD Approach:**
     - Write test that detects Linux
     - Implement Linux detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
     def test_linux_detection():
         """Verify Linux platform is detected correctly"""
         from omni_scripts.platform.detector import PlatformDetector
         detector = PlatformDetector()
         assert detector.get_platform() == "linux"
     ```

3. **Test macOS Detection**
   - **Description:** Verify macOS platform is detected correctly
   - **TDD Approach:**
     - Write test that detects macOS
     - Implement macOS detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")
     def test_macos_detection():
         """Verify macOS platform is detected correctly"""
         from omni_scripts.platform.detector import PlatformDetector
         detector = PlatformDetector()
         assert detector.get_platform() == "macos"
     ```

4. **Test Architecture Detection**
   - **Description:** Verify system architecture is detected correctly
   - **TDD Approach:**
     - Write test that detects architecture
     - Implement architecture detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_architecture_detection():
         """Verify system architecture is detected correctly"""
         from omni_scripts.platform.detector import PlatformDetector
         detector = PlatformDetector()
         arch = detector.get_architecture()
         assert arch in ["x86_64", "arm64", "x86"]
     ```

#### Compiler Detection Tests

**Unit Tests**

1. **Test MSVC Detection**
   - **Description:** Verify MSVC compiler is detected correctly on Windows
   - **TDD Approach:**
     - Write test that detects MSVC
     - Implement MSVC detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
     def test_msvc_detection():
         """Verify MSVC compiler is detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         compiler = detector.detect_compiler()
         if compiler:
             assert compiler.name == "msvc"
     ```

2. **Test GCC Detection**
   - **Description:** Verify GCC compiler is detected correctly on Linux
   - **TDD Approach:**
     - Write test that detects GCC
     - Implement GCC detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
     def test_gcc_detection():
         """Verify GCC compiler is detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         compiler = detector.detect_compiler()
         if compiler:
             assert compiler.name == "gcc"
     ```

3. **Test Clang Detection**
   - **Description:** Verify Clang compiler is detected correctly
   - **TDD Approach:**
     - Write test that detects Clang
     - Implement Clang detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_clang_detection():
         """Verify Clang compiler is detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         compiler = detector.detect_compiler()
         if compiler:
             assert compiler.name == "clang"
     ```

4. **Test MinGW Detection**
   - **Description:** Verify MinGW compiler is detected correctly on Windows
   - **TDD Approach:**
     - Write test that detects MinGW
     - Implement MinGW detection
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
     def test_mingw_detection():
         """Verify MinGW compiler is detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         compiler = detector.detect_compiler()
         if compiler:
             assert compiler.name in ["mingw-gcc", "mingw-clang"]
     ```

5. **Test Compiler Version Detection**
   - **Description:** Verify compiler version is detected correctly
   - **TDD Approach:**
     - Write test that detects version
     - Implement version detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_compiler_version_detection():
         """Verify compiler version is detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         compiler = detector.detect_compiler()
         if compiler:
             assert compiler.version is not None
             assert len(compiler.version.split(".")) >= 2
     ```

#### Terminal Invocation Tests

**Unit Tests**

1. **Test MSVC Developer Command Prompt**
   - **Description:** Verify MSVC developer command prompt is invoked correctly
   - **TDD Approach:**
     - Write test that invokes MSVC prompt
     - Implement MSVC prompt invocation
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
     def test_msvc_dev_prompt_invocation(mocker):
         """Verify MSVC developer command prompt is invoked correctly"""
         from omni_scripts.utils.terminal_utils import TerminalInvoker
         invoker = TerminalInvoker()
         mock_subprocess = mocker.patch('subprocess.run')
         invoker.invoke_msvc_dev_prompt()
         mock_subprocess.assert_called_once()
     ```

2. **Test MSYS2 Terminal Invocation**
   - **Description:** Verify MSYS2 terminal is invoked correctly
   - **TDD Approach:**
     - Write test that invokes MSYS2
     - Implement MSYS2 invocation
     - Verify test passes
   - **Test Code:**
     ```python
     @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
     def test_msys2_terminal_invocation(mocker):
         """Verify MSYS2 terminal is invoked correctly"""
         from omni_scripts.utils.terminal_utils import TerminalInvoker
         invoker = TerminalInvoker()
         mock_subprocess = mocker.patch('subprocess.run')
         invoker.invoke_msys2()
         mock_subprocess.assert_called_once()
     ```

3. **Test Command Execution**
   - **Description:** Verify commands are executed correctly
   - **TDD Approach:**
     - Write test that executes command
     - Implement command execution
     - Verify test passes
   - **Test Code:**
     ```python
     def test_command_execution(mocker):
         """Verify commands are executed correctly"""
         from omni_scripts.utils.terminal_utils import TerminalInvoker
         invoker = TerminalInvoker()
         mock_subprocess = mocker.patch('subprocess.run')
         invoker.execute_command(["echo", "test"])
         mock_subprocess.assert_called_once_with(["echo", "test"], check=True)
     ```

4. **Test Command Output Capture**
   - **Description:** Verify command output is captured correctly
   - **TDD Approach:**
     - Write test that captures output
     - Implement output capture
     - Verify test passes
   - **Test Code:**
     ```python
     def test_command_output_capture():
         """Verify command output is captured correctly"""
         from omni_scripts.utils.terminal_utils import TerminalInvoker
         invoker = TerminalInvoker()
         result = invoker.execute_command(["echo", "test"], capture_output=True)
         assert "test" in result.stdout
     ```

#### Cross-Compilation Tests

**Unit Tests**

1. **Test ARM64 Cross-Compilation**
   - **Description:** Verify ARM64 cross-compilation works correctly
   - **TDD Approach:**
     - Write test that cross-compiles to ARM64
     - Implement ARM64 cross-compilation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_arm64_cross_compilation(build_system_fixture):
         """Verify ARM64 cross-compilation works correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result = builder.build(
             target="arm64-linux-gnu",
             toolchain="cmake/toolchains/arm64-linux-gnu.cmake"
         )
         assert result == 0
     ```

2. **Test Emscripten Cross-Compilation**
   - **Description:** Verify Emscripten cross-compilation to WebAssembly works
   - **TDD Approach:**
     - Write test that cross-compiles to WASM
     - Implement Emscripten cross-compilation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_emscripten_cross_compilation(build_system_fixture):
         """Verify Emscripten cross-compilation works correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result = builder.build(
             target="wasm32-unknown-emscripten",
             toolchain="cmake/toolchains/emscripten.cmake"
         )
         assert result == 0
     ```

3. **Test Cross-Compiler Detection**
   - **Description:** Verify cross-compilers are detected correctly
   - **TDD Approach:**
     - Write test that detects cross-compiler
     - Implement cross-compiler detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cross_compiler_detection():
         """Verify cross-compilers are detected correctly"""
         from omni_scripts.compilers.detector import CompilerDetector
         detector = CompilerDetector()
         cross_compiler = detector.detect_cross_compiler("arm64-linux-gnu")
         if cross_compiler:
             assert cross_compiler.architecture == "arm64"
     ```

---

### Package Manager Tests

#### Conan Integration Tests

**Unit Tests**

1. **Test Conan Installation**
   - **Description:** Verify Conan can be installed and detected
   - **TDD Approach:**
     - Write test that detects Conan
     - Implement Conan detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_conan_detection():
         """Verify Conan can be detected"""
         from omni_scripts.package_managers.conan import ConanManager
         manager = ConanManager()
         assert manager.is_available() is True
     ```

2. **Test Conan Profile Creation**
   - **Description:** Verify Conan profiles can be created
   - **TDD Approach:**
     - Write test that creates profile
     - Implement profile creation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_conan_profile_creation(tmp_path):
         """Verify Conan profiles can be created"""
         from omni_scripts.package_managers.conan import ConanManager
         manager = ConanManager()
         profile_path = tmp_path / "test_profile"
         manager.create_profile(str(profile_path), {"compiler": "gcc", "compiler.version": "13"})
         assert profile_path.exists()
     ```

3. **Test Conan Package Installation**
   - **Description:** Verify Conan packages can be installed
   - **TDD Approach:**
     - Write test that installs package
     - Implement package installation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_conan_package_installation():
         """Verify Conan packages can be installed"""
         from omni_scripts.package_managers.conan import ConanManager
         manager = ConanManager()
         result = manager.install("fmt/10.0.0")
         assert result == 0
     ```

4. **Test Conan Dependency Resolution**
   - **Description:** Verify Conan resolves dependencies correctly
   - **TDD Approach:**
     - Write test that resolves dependencies
     - Implement dependency resolution
     - Verify test passes
   - **Test Code:**
     ```python
     def test_conan_dependency_resolution():
         """Verify Conan resolves dependencies correctly"""
         from omni_scripts.package_managers.conan import ConanManager
         manager = ConanManager()
         dependencies = manager.resolve_dependencies(["fmt/10.0.0", "spdlog/1.12.0"])
         assert len(dependencies) >= 2
     ```

#### vcpkg Integration Tests

**Unit Tests**

1. **Test vcpkg Installation**
   - **Description:** Verify vcpkg can be installed and detected
   - **TDD Approach:**
     - Write test that detects vcpkg
     - Implement vcpkg detection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vcpkg_detection():
         """Verify vcpkg can be detected"""
         from omni_scripts.package_managers.vcpkg import VcpkgManager
         manager = VcpkgManager()
         assert manager.is_available() is True
     ```

2. **Test vcpkg Package Installation**
   - **Description:** Verify vcpkg packages can be installed
   - **TDD Approach:**
     - Write test that installs package
     - Implement package installation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vcpkg_package_installation():
         """Verify vcpkg packages can be installed"""
         from omni_scripts.package_managers.vcpkg import VcpkgManager
         manager = VcpkgManager()
         result = manager.install("fmt")
         assert result == 0
     ```

3. **Test vcpkg Triplet Selection**
   - **Description:** Verify vcpkg triplets are selected correctly
   - **TDD Approach:**
     - Write test that selects triplet
     - Implement triplet selection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vcpkg_triplet_selection():
         """Verify vcpkg triplets are selected correctly"""
         from omni_scripts.package_managers.vcpkg import VcpkgManager
         manager = VcpkgManager()
         triplet = manager.get_triplet(platform="windows", arch="x64")
         assert triplet == "x64-windows"
     ```

#### CPM Integration Tests

**Unit Tests**

1. **Test CPM Integration**
   - **Description:** Verify CPM is integrated with CMake
   - **TDD Approach:**
     - Write test that checks CPM integration
     - Implement CPM integration
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cpm_integration():
         """Verify CPM is integrated with CMake"""
         from omni_scripts.package_managers.cpm import CPMManager
         manager = CPMManager()
         assert manager.is_available() is True
     ```

2. **Test CPM Package Addition**
   - **Description:** Verify CPM packages can be added to CMake
   - **TDD Approach:**
     - Write test that adds package
     - Implement package addition
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cpm_package_addition():
         """Verify CPM packages can be added to CMake"""
         from omni_scripts.package_managers.cpm import CPMManager
         manager = CPMManager()
         manager.add_package("fmt", "10.0.0", "https://github.com/fmtlib/fmt")
         assert "fmt" in manager.get_packages()
     ```

#### Package Security Verification Tests

**Unit Tests**

1. **Test Package Integrity Check**
   - **Description:** Verify package integrity is checked
   - **TDD Approach:**
     - Write test that checks integrity
     - Implement integrity check
     - Verify test passes
   - **Test Code:**
     ```python
     def test_package_integrity_check():
         """Verify package integrity is checked"""
         from omni_scripts.package_managers.security import SecurityValidator
         validator = SecurityValidator()
         result = validator.check_integrity("fmt/10.0.0", expected_hash="abc123")
         assert result is True
     ```

2. **Test Package Signature Verification**
   - **Description:** Verify package signatures are verified
   - **TDD Approach:**
     - Write test that verifies signature
     - Implement signature verification
     - Verify test passes
   - **Test Code:**
     ```python
     def test_package_signature_verification():
         """Verify package signatures are verified"""
         from omni_scripts.package_managers.security import SecurityValidator
         validator = SecurityValidator()
         result = validator.verify_signature("fmt/10.0.0", signature="sig123")
         assert result is True
     ```

3. **Test Vulnerability Scan**
   - **Description:** Verify packages are scanned for vulnerabilities
   - **TDD Approach:**
     - Write test that scans for vulnerabilities
     - Implement vulnerability scan
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vulnerability_scan():
         """Verify packages are scanned for vulnerabilities"""
         from omni_scripts.package_managers.security import SecurityValidator
         validator = SecurityValidator()
         vulnerabilities = validator.scan_vulnerabilities("fmt/10.0.0")
         assert isinstance(vulnerabilities, list)
     ```

#### Priority-Based Package Manager Selection Tests

**Unit Tests**

1. **Test Priority Selection**
   - **Description:** Verify package manager is selected based on priority
   - **TDD Approach:**
     - Write test that selects by priority
     - Implement priority selection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_priority_selection():
         """Verify package manager is selected based on priority"""
         from omni_scripts.package_managers.selector import PackageManagerSelector
         selector = PackageManagerSelector()
         selector.set_priority(["conan", "vcpkg", "cpm"])
         manager = selector.select_manager("fmt")
         assert manager.name == "conan"
     ```

2. **Test Fallback Selection**
   - **Description:** Verify fallback to next priority manager
   - **TDD Approach:**
     - Write test that tests fallback
     - Implement fallback logic
     - Verify test passes
   - **Test Code:**
     ```python
     def test_fallback_selection(mocker):
         """Verify fallback to next priority manager"""
         from omni_scripts.package_managers.selector import PackageManagerSelector
         selector = PackageManagerSelector()
         selector.set_priority(["conan", "vcpkg", "cpm"])
         mocker.patch.object(selector.managers[0], 'is_available', return_value=False)
         manager = selector.select_manager("fmt")
         assert manager.name == "vcpkg"
     ```

---

### Build System Tests

#### CMake Configuration Tests

**Unit Tests**

1. **Test CMake Configuration**
   - **Description:** Verify CMake can be configured correctly
   - **TDD Approach:**
     - Write test that configures CMake
     - Implement CMake configuration
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cmake_configuration(build_system_fixture):
         """Verify CMake can be configured correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result = builder.configure(
             source_dir=".",
             build_dir="build",
             generator="Ninja"
         )
         assert result == 0
     ```

2. **Test CMake Preset Application**
   - **Description:** Verify CMake presets are applied correctly
   - **TDD Approach:**
     - Write test that applies preset
     - Implement preset application
     - Verify test passes
   - **Test Code:**
     ```python
     def test_cmake_preset_application():
         """Verify CMake presets are applied correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result = builder.apply_preset("debug")
         assert result == 0
     ```

3. **Test Toolchain File Selection**
   - **Description:** Verify toolchain files are selected correctly
   - **TDD Approach:**
     - Write test that selects toolchain
     - Implement toolchain selection
     - Verify test passes
   - **Test Code:**
     ```python
     def test_toolchain_file_selection():
         """Verify toolchain files are selected correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         toolchain = builder.select_toolchain(platform="windows", compiler="msvc")
         assert toolchain.endswith(".cmake")
     ```

#### Build Optimization Tests

**Unit Tests**

1. **Test Parallel Build**
   - **Description:** Verify parallel builds work correctly
   - **TDD Approach:**
     - Write test that builds in parallel
     - Implement parallel build
     - Verify test passes
   - **Test Code:**
     ```python
     def test_parallel_build(build_system_fixture):
         """Verify parallel builds work correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result = builder.build(jobs=4)
         assert result == 0
     ```

2. **Test Build Caching**
   - **Description:** Verify build caching works correctly
   - **TDD Approach:**
     - Write test that uses cache
     - Implement build caching
     - Verify test passes
   - **Test Code:**
     ```python
     def test_build_caching(build_system_fixture):
         """Verify build caching works correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result1 = builder.build(use_cache=True)
         result2 = builder.build(use_cache=True)
         assert result1 == 0
         assert result2 == 0
     ```

3. **Test Incremental Build**
   - **Description:** Verify incremental builds work correctly
   - **TDD Approach:**
     - Write test that builds incrementally
     - Implement incremental build
     - Verify test passes
   - **Test Code:**
     ```python
     def test_incremental_build(build_system_fixture):
         """Verify incremental builds work correctly"""
         from omni_scripts.build_system.cmake import CMakeBuilder
         builder = CMakeBuilder()
         result1 = builder.build()
         # Modify a source file
         result2 = builder.build(incremental=True)
         assert result1 == 0
         assert result2 == 0
     ```

---

### C++ Engine Tests

#### Engine Core Tests

**Unit Tests**

1. **Test Engine Initialization**
   - **Description:** Verify engine initializes correctly
   - **TDD Approach:**
     - Write test that initializes engine
     - Implement engine initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(EngineTest, Initialize) {
         omnicpp::engine::Engine engine;
         EXPECT_TRUE(engine.initialize());
         EXPECT_TRUE(engine.is_initialized());
     }
     ```

2. **Test Engine Shutdown**
   - **Description:** Verify engine shuts down correctly
   - **TDD Approach:**
     - Write test that shuts down engine
     - Implement engine shutdown
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(EngineTest, Shutdown) {
         omnicpp::engine::Engine engine;
         engine.initialize();
         EXPECT_TRUE(engine.shutdown());
         EXPECT_FALSE(engine.is_initialized());
     }
     ```

3. **Test Engine Update Loop**
   - **Description:** Verify engine update loop works correctly
   - **TDD Approach:**
     - Write test that updates engine
     - Implement update loop
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(EngineTest, UpdateLoop) {
         omnicpp::engine::Engine engine;
         engine.initialize();
         EXPECT_TRUE(engine.update(0.016f));  // 60 FPS
         engine.shutdown();
     }
     ```

#### ECS Component Tests

**Unit Tests**

1. **Test Entity Creation**
   - **Description:** Verify entities can be created
   - **TDD Approach:**
     - Write test that creates entity
     - Implement entity creation
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ECSTest, CreateEntity) {
         omnicpp::engine::ecs::EntityManager manager;
         auto entity = manager.create_entity();
         EXPECT_TRUE(entity.is_valid());
     }
     ```

2. **Test Component Addition**
   - **Description:** Verify components can be added to entities
   - **TDD Approach:**
     - Write test that adds component
     - Implement component addition
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ECSTest, AddComponent) {
         omnicpp::engine::ecs::EntityManager manager;
         auto entity = manager.create_entity();
         auto& transform = manager.add_component<TransformComponent>(entity);
         EXPECT_TRUE(manager.has_component<TransformComponent>(entity));
     }
     ```

3. **Test Component Removal**
   - **Description:** Verify components can be removed from entities
   - **TDD Approach:**
     - Write test that removes component
     - Implement component removal
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ECSTest, RemoveComponent) {
         omnicpp::engine::ecs::EntityManager manager;
         auto entity = manager.create_entity();
         manager.add_component<TransformComponent>(entity);
         manager.remove_component<TransformComponent>(entity);
         EXPECT_FALSE(manager.has_component<TransformComponent>(entity));
     }
     ```

#### ECS System Tests

**Unit Tests**

1. **Test System Registration**
   - **Description:** Verify systems can be registered
   - **TDD Approach:**
     - Write test that registers system
     - Implement system registration
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ECSTest, RegisterSystem) {
         omnicpp::engine::ecs::SystemManager manager;
         auto system = std::make_shared<MovementSystem>();
         manager.register_system(system);
         EXPECT_TRUE(manager.has_system<MovementSystem>());
     }
     ```

2. **Test System Update**
   - **Description:** Verify systems can be updated
   - **TDD Approach:**
     - Write test that updates system
     - Implement system update
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ECSTest, UpdateSystem) {
         omnicpp::engine::ecs::SystemManager manager;
         auto system = std::make_shared<MovementSystem>();
         manager.register_system(system);
         EXPECT_TRUE(manager.update(0.016f));
     }
     ```

#### Renderer Tests

**Unit Tests**

1. **Test Renderer Initialization**
   - **Description:** Verify renderer initializes correctly
   - **TDD Approach:**
     - Write test that initializes renderer
     - Implement renderer initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(RendererTest, Initialize) {
         omnicpp::engine::graphics::Renderer renderer;
         EXPECT_TRUE(renderer.initialize());
         EXPECT_TRUE(renderer.is_initialized());
     }
     ```

2. **Test Rendering**
   - **Description:** Verify rendering works correctly
   - **TDD Approach:**
     - Write test that renders
     - Implement rendering
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(RendererTest, Render) {
         omnicpp::engine::graphics::Renderer renderer;
         renderer.initialize();
         EXPECT_TRUE(renderer.render());
         renderer.shutdown();
     }
     ```

#### Audio Manager Tests

**Unit Tests**

1. **Test Audio Manager Initialization**
   - **Description:** Verify audio manager initializes correctly
   - **TDD Approach:**
     - Write test that initializes audio manager
     - Implement audio manager initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(AudioTest, Initialize) {
         omnicpp::engine::audio::AudioManager manager;
         EXPECT_TRUE(manager.initialize());
         EXPECT_TRUE(manager.is_initialized());
     }
     ```

2. **Test Sound Playback**
   - **Description:** Verify sounds can be played
   - **TDD Approach:**
     - Write test that plays sound
     - Implement sound playback
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(AudioTest, PlaySound) {
         omnicpp::engine::audio::AudioManager manager;
         manager.initialize();
         EXPECT_TRUE(manager.play_sound("test.wav"));
         manager.shutdown();
     }
     ```

#### Physics Engine Tests

**Unit Tests**

1. **Test Physics Engine Initialization**
   - **Description:** Verify physics engine initializes correctly
   - **TDD Approach:**
     - Write test that initializes physics engine
     - Implement physics engine initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(PhysicsTest, Initialize) {
         omnicpp::engine::physics::PhysicsEngine engine;
         EXPECT_TRUE(engine.initialize());
         EXPECT_TRUE(engine.is_initialized());
     }
     ```

2. **Test Physics Simulation**
   - **Description:** Verify physics simulation works correctly
   - **TDD Approach:**
     - Write test that simulates physics
     - Implement physics simulation
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(PhysicsTest, Simulate) {
         omnicpp::engine::physics::PhysicsEngine engine;
         engine.initialize();
         EXPECT_TRUE(engine.simulate(0.016f));
         engine.shutdown();
     }
     ```

#### Resource Manager Tests

**Unit Tests**

1. **Test Resource Loading**
   - **Description:** Verify resources can be loaded
   - **TDD Approach:**
     - Write test that loads resource
     - Implement resource loading
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ResourceTest, LoadResource) {
         omnicpp::engine::resources::ResourceManager manager;
         auto resource = manager.load<Texture>("test.png");
         EXPECT_NE(resource, nullptr);
     }
     ```

2. **Test Resource Caching**
   - **Description:** Verify resources are cached
   - **TDD Approach:**
     - Write test that caches resource
     - Implement resource caching
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(ResourceTest, CacheResource) {
         omnicpp::engine::resources::ResourceManager manager;
         auto resource1 = manager.load<Texture>("test.png");
         auto resource2 = manager.load<Texture>("test.png");
         EXPECT_EQ(resource1, resource2);  // Same cached resource
     }
     ```

#### Scene Manager Tests

**Unit Tests**

1. **Test Scene Creation**
   - **Description:** Verify scenes can be created
   - **TDD Approach:**
     - Write test that creates scene
     - Implement scene creation
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(SceneTest, CreateScene) {
         omnicpp::engine::scene::SceneManager manager;
         auto scene = manager.create_scene("TestScene");
         EXPECT_NE(scene, nullptr);
     }
     ```

2. **Test Scene Loading**
   - **Description:** Verify scenes can be loaded
   - **TDD Approach:**
     - Write test that loads scene
     - Implement scene loading
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(SceneTest, LoadScene) {
         omnicpp::engine::scene::SceneManager manager;
         EXPECT_TRUE(manager.load_scene("test_scene.json"));
     }
     ```

---

### C++ Game Tests

#### Game Core Tests

**Unit Tests**

1. **Test Game Initialization**
   - **Description:** Verify game initializes correctly
   - **TDD Approach:**
     - Write test that initializes game
     - Implement game initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(GameTest, Initialize) {
         omnicpp::game::Game game;
         EXPECT_TRUE(game.initialize());
         EXPECT_TRUE(game.is_initialized());
     }
     ```

2. **Test Game Loop**
   - **Description:** Verify game loop works correctly
   - **TDD Approach:**
     - Write test that runs game loop
     - Implement game loop
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(GameTest, GameLoop) {
         omnicpp::game::Game game;
         game.initialize();
         EXPECT_TRUE(game.run_frame());
         game.shutdown();
     }
     ```

#### Game Scene Tests

**Unit Tests**

1. **Test Game Scene Creation**
   - **Description:** Verify game scenes can be created
   - **TDD Approach:**
     - Write test that creates game scene
     - Implement game scene creation
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(GameSceneTest, CreateScene) {
         omnicpp::game::scene::GameScene scene;
         EXPECT_TRUE(scene.initialize());
     }
     ```

#### Game Entity Tests

**Unit Tests**

1. **Test Game Entity Creation**
   - **Description:** Verify game entities can be created
   - **TDD Approach:**
     - Write test that creates game entity
     - Implement game entity creation
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(GameEntityTest, CreateEntity) {
         omnicpp::game::entity::GameEntity entity;
         EXPECT_TRUE(entity.initialize());
     }
     ```

---

### Logging Tests

#### C++ spdlog Integration Tests

**Unit Tests**

1. **Test Logger Initialization**
   - **Description:** Verify spdlog logger initializes correctly
   - **TDD Approach:**
     - Write test that initializes logger
     - Implement logger initialization
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(LoggingTest, Initialize) {
         auto logger = omnicpp::logging::Logger::get("test");
         EXPECT_NE(logger, nullptr);
     }
     ```

2. **Test Log Levels**
   - **Description:** Verify log levels work correctly
   - **TDD Approach:**
     - Write test that logs at different levels
     - Implement log levels
     - Verify test passes
   - **Test Code:**
     ```cpp
     TEST(LoggingTest, LogLevels) {
         auto logger = omnicpp::logging::Logger::get("test");
         logger->debug("Debug message");
         logger->info("Info message");
         logger->warn("Warning message");
         logger->error("Error message");
         SUCCEED();
     }
     ```

#### Python Logging Tests

**Unit Tests**

1. **Test Logger Initialization**
   - **Description:** Verify Python logger initializes correctly
   - **TDD Approach:**
     - Write test that initializes logger
     - Implement logger initialization
     - Verify test passes
   - **Test Code:**
     ```python
     def test_logger_initialization():
         """Verify Python logger initializes correctly"""
         from omni_scripts.logging.logger import Logger
         logger = Logger("test")
         assert logger is not None
     ```

2. **Test Log Levels**
   - **Description:** Verify log levels work correctly
   - **TDD Approach:**
     - Write test that logs at different levels
     - Implement log levels
     - Verify test passes
   - **Test Code:**
     ```python
     def test_log_levels(caplog):
         """Verify log levels work correctly"""
         from omni_scripts.logging.logger import Logger
         logger = Logger("test")
         with caplog.at_level(logging.DEBUG):
             logger.debug("Debug message")
             logger.info("Info message")
             logger.warning("Warning message")
             logger.error("Error message")
         assert "Debug message" in caplog.text
         assert "Info message" in caplog.text
     ```

#### File Rotation Tests

**Unit Tests**

1. **Test Log File Rotation**
   - **Description:** Verify log files rotate correctly
   - **TDD Approach:**
     - Write test that triggers rotation
     - Implement file rotation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_log_file_rotation(tmp_path):
         """Verify log files rotate correctly"""
         from omni_scripts.logging.handlers import RotatingFileHandler
         log_file = tmp_path / "test.log"
         handler = RotatingFileHandler(str(log_file), maxBytes=1024, backupCount=3)
         # Write enough data to trigger rotation
         for i in range(1000):
             handler.emit(logging.LogRecord(
                 name="test", level=logging.INFO, pathname="", lineno=0,
                 msg=f"Test message {i}", args=(), exc_info=None
             ))
         assert log_file.exists()
         assert len(list(tmp_path.glob("test.log.*"))) > 0
     ```

#### Log Format Tests

**Unit Tests**

1. **Test Log Format**
   - **Description:** Verify log format is consistent
   - **TDD Approach:**
     - Write test that checks format
     - Implement log formatting
     - Verify test passes
   - **Test Code:**
     ```python
     def test_log_format(caplog):
         """Verify log format is consistent"""
         from omni_scripts.logging.logger import Logger
         logger = Logger("test")
         with caplog.at_level(logging.INFO):
             logger.info("Test message")
         assert "test" in caplog.text
         assert "INFO" in caplog.text
         assert "Test message" in caplog.text
     ```

---

### Security Tests

#### Terminal Invocation Security Tests

**Unit Tests**

1. **Test Command Injection Prevention**
   - **Description:** Verify command injection is prevented
   - **TDD Approach:**
     - Write test that attempts injection
     - Implement injection prevention
     - Verify test passes
   - **Test Code:**
     ```python
     def test_command_injection_prevention():
         """Verify command injection is prevented"""
         from omni_scripts.utils.terminal_utils import TerminalInvoker
         invoker = TerminalInvoker()
         with pytest.raises(SecurityError):
             invoker.execute_command(["echo", "test; rm -rf /"])
     ```

2. **Test Path Traversal Prevention**
   - **Description:** Verify path traversal is prevented
   - **TDD Approach:**
     - Write test that attempts traversal
     - Implement traversal prevention
     - Verify test passes
   - **Test Code:**
     ```python
     def test_path_traversal_prevention():
         """Verify path traversal is prevented"""
         from omni_scripts.utils.file_utils import FileUtils
         utils = FileUtils()
         with pytest.raises(SecurityError):
             utils.validate_path("../../../etc/passwd")
     ```

#### Dependency Integrity Tests

**Unit Tests**

1. **Test Dependency Hash Verification**
   - **Description:** Verify dependency hashes are checked
   - **TDD Approach:**
     - Write test that verifies hash
     - Implement hash verification
     - Verify test passes
   - **Test Code:**
     ```python
     def test_dependency_hash_verification():
         """Verify dependency hashes are checked"""
         from omni_scripts.package_managers.security import SecurityValidator
         validator = SecurityValidator()
         result = validator.verify_hash("fmt/10.0.0", expected_hash="abc123")
         assert result is True
     ```

2. **Test Dependency Signature Verification**
   - **Description:** Verify dependency signatures are checked
   - **TDD Approach:**
     - Write test that verifies signature
     - Implement signature verification
     - Verify test passes
   - **Test Code:**
     ```python
     def test_dependency_signature_verification():
         """Verify dependency signatures are checked"""
         from omni_scripts.package_managers.security import SecurityValidator
         validator = SecurityValidator()
         result = validator.verify_signature("fmt/10.0.0", signature="sig123")
         assert result is True
     ```

#### Logging Security Tests

**Unit Tests**

1. **Test Sensitive Data Redaction**
   - **Description:** Verify sensitive data is redacted from logs
   - **TDD Approach:**
     - Write test that logs sensitive data
     - Implement data redaction
     - Verify test passes
   - **Test Code:**
     ```python
     def test_sensitive_data_redaction(caplog):
         """Verify sensitive data is redacted from logs"""
         from omni_scripts.logging.formatters import RedactingFormatter
         formatter = RedactingFormatter()
         record = logging.LogRecord(
             name="test", level=logging.INFO, pathname="", lineno=0,
             msg="Password: secret123", args=(), exc_info=None
         )
         formatted = formatter.format(record)
         assert "secret123" not in formatted
         assert "***" in formatted
     ```

2. **Test Log File Permissions**
   - **Description:** Verify log files have correct permissions
   - **TDD Approach:**
     - Write test that checks permissions
     - Implement permission setting
     - Verify test passes
   - **Test Code:**
     ```python
     def test_log_file_permissions(tmp_path):
         """Verify log files have correct permissions"""
         from omni_scripts.logging.handlers import SecureFileHandler
         log_file = tmp_path / "test.log"
         handler = SecureFileHandler(str(log_file))
         handler.setMode(0o600)  # Read/write for owner only
         assert oct(log_file.stat().st_mode) == "0o100600"
     ```

#### Build System Security Tests

**Unit Tests**

1. **Test Build Artifact Verification**
   - **Description:** Verify build artifacts are verified
   - **TDD Approach:**
     - Write test that verifies artifacts
     - Implement artifact verification
     - Verify test passes
   - **Test Code:**
     ```python
     def test_build_artifact_verification():
         """Verify build artifacts are verified"""
         from omni_scripts.build_system.security import BuildValidator
         validator = BuildValidator()
         result = validator.verify_artifact("build/engine.exe", expected_hash="abc123")
         assert result is True
     ```

2. **Test Build Environment Isolation**
   - **Description:** Verify build environment is isolated
   - **TDD Approach:**
     - Write test that checks isolation
     - Implement environment isolation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_build_environment_isolation():
         """Verify build environment is isolated"""
         from omni_scripts.build_system.security import BuildEnvironment
         env = BuildEnvironment()
         env.set_isolated(True)
         assert env.is_isolated() is True
     ```

---

### VSCode Integration Tests

#### tasks.json Tests

**Unit Tests**

1. **Test tasks.json Generation**
   - **Description:** Verify tasks.json is generated correctly
   - **TDD Approach:**
     - Write test that generates tasks.json
     - Implement tasks.json generation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_tasks_json_generation(tmp_path):
         """Verify tasks.json is generated correctly"""
         from omni_scripts.vscode.tasks import TasksGenerator
         generator = TasksGenerator()
         tasks_file = tmp_path / ".vscode" / "tasks.json"
         generator.generate(str(tasks_file))
         assert tasks_file.exists()
     ```

2. **Test Task Execution**
   - **Description:** Verify VSCode tasks execute correctly
   - **TDD Approach:**
     - Write test that executes task
     - Implement task execution
     - Verify test passes
   - **Test Code:**
     ```python
     def test_task_execution():
         """Verify VSCode tasks execute correctly"""
         from omni_scripts.vscode.tasks import TaskExecutor
         executor = TaskExecutor()
         result = executor.execute("build")
         assert result == 0
     ```

#### launch.json Tests

**Unit Tests**

1. **Test launch.json Generation**
   - **Description:** Verify launch.json is generated correctly
   - **TDD Approach:**
     - Write test that generates launch.json
     - Implement launch.json generation
     - Verify test passes
   - **Test Code:**
     ```python
     def test_launch_json_generation(tmp_path):
         """Verify launch.json is generated correctly"""
         from omni_scripts.vscode.launch import LaunchGenerator
         generator = LaunchGenerator()
         launch_file = tmp_path / ".vscode" / "launch.json"
         generator.generate(str(launch_file))
         assert launch_file.exists()
     ```

2. **Test Debug Configuration**
   - **Description:** Verify debug configurations work correctly
   - **TDD Approach:**
     - Write test that tests debug config
     - Implement debug configuration
     - Verify test passes
   - **Test Code:**
     ```python
     def test_debug_configuration():
         """Verify debug configurations work correctly"""
         from omni_scripts.vscode.launch import LaunchGenerator
         generator = LaunchGenerator()
         configs = generator.get_debug_configs()
         assert len(configs) > 0
     ```

#### OmniCppController.py Integration Tests

**Unit Tests**

1. **Test VSCode Task Integration**
   - **Description:** Verify OmniCppController.py integrates with VSCode tasks
   - **TDD Approach:**
     - Write test that tests integration
     - Implement VSCode integration
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vscode_task_integration():
         """Verify OmniCppController.py integrates with VSCode tasks"""
         from omni_scripts.vscode.integration import VSCodeIntegration
         integration = VSCodeIntegration()
         result = integration.execute_task("build")
         assert result == 0
     ```

2. **Test VSCode Debug Integration**
   - **Description:** Verify OmniCppController.py integrates with VSCode debugger
   - **TDD Approach:**
     - Write test that tests debug integration
     - Implement debug integration
     - Verify test passes
   - **Test Code:**
     ```python
     def test_vscode_debug_integration():
         """Verify OmniCppController.py integrates with VSCode debugger"""
         from omni_scripts.vscode.integration import VSCodeIntegration
         integration = VSCodeIntegration()
         result = integration.start_debugging("engine")
         assert result == 0
     ```

---

## Test Coverage Requirements

### Minimum Coverage Targets

| Component | Line Coverage | Branch Coverage | Function Coverage |
|-----------|--------------|----------------|------------------|
| Python Build System | 85% | 80% | 90% |
| C++ Engine | 80% | 75% | 85% |
| C++ Game | 80% | 75% | 85% |
| Cross-Platform | 85% | 80% | 90% |
| Package Managers | 85% | 80% | 90% |
| Build System | 85% | 80% | 90% |
| Logging | 90% | 85% | 95% |
| Security | 95% | 90% | 100% |
| VSCode Integration | 80% | 75% | 85% |

### Critical Path Coverage

All critical paths must have 100% coverage:

- **Entry Point:** OmniCppController.py command dispatch
- **Controller Execution:** All controller execute() methods
- **Error Handling:** All exception paths
- **Security:** All security validations
- **Platform Detection:** All platform-specific code paths
- **Compiler Detection:** All compiler detection paths
- **Package Manager Selection:** All selection and fallback paths

### Edge Case Coverage

Edge cases must be tested:

- **Empty Inputs:** Test with empty strings, empty lists, None values
- **Boundary Conditions:** Test with minimum and maximum values
- **Invalid Inputs:** Test with invalid types, malformed data
- **Concurrent Access:** Test thread safety where applicable
- **Resource Exhaustion:** Test with limited resources
- **Network Failures:** Test with network errors
- **File System Errors:** Test with missing files, permission errors

### Error Path Coverage

All error paths must be tested:

- **Exception Handling:** All try-except blocks
- **Error Recovery:** All error recovery mechanisms
- **Graceful Degradation:** All fallback mechanisms
- **User-Friendly Messages:** All error messages
- **Exit Codes:** All exit code paths

---

## Test Automation Strategy

### CI/CD Integration

#### GitHub Actions Workflow

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  python-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.11']
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      - name: Run Python tests
        run: |
          pytest tests/python/ -v --cov=omni_scripts --cov-report=xml --cov-report=html
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  cpp-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        compiler: [gcc, clang, msvc]
    steps:
      - uses: actions/checkout@v3
      - name: Configure CMake
        run: |
          cmake -B build -DCMAKE_BUILD_TYPE=Debug -DBUILD_TESTING=ON
      - name: Build
        run: cmake --build build --config Debug
      - name: Run C++ tests
        run: |
          ctest --test-dir build --output-on-failure --verbose
      - name: Generate coverage
        run: |
          gcov -r build/**/*.gcda
          lcov --capture --directory build --output-file coverage.info
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.info

  cross-platform-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Emscripten
        uses: mymindstorm/setup-emsdk@v12
        with:
          version: latest
          actions-cache-folder: 'emsdk-cache'
      - name: Build for WASM
        run: |
          emcmake cmake -B build-wasm
          emmake cmake --build build-wasm
      - name: Run WASM tests
        run: |
          node build-wasm/tests/test_runner.js
```

### Pre-commit Hooks

#### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=100"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/python/unit/ -v
        language: system
        pass_filenames: false
```

### Automated Test Execution

#### Test Execution Schedule

| Test Type | Frequency | Trigger |
|-----------|-----------|---------|
| Unit Tests | Every commit | Pre-commit hook |
| Integration Tests | Every push | CI/CD pipeline |
| System Tests | Every pull request | CI/CD pipeline |
| E2E Tests | Nightly | Scheduled job |
| Performance Tests | Weekly | Scheduled job |
| Security Tests | Every push | CI/CD pipeline |
| Cross-Platform Tests | Every push | CI/CD pipeline |

#### Parallel Test Execution

```python
# pytest.ini
[pytest]
addopts = -n auto --dist loadscope
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Coverage Reporting

#### Coverage Thresholds

```python
# .coveragerc
[run]
source = omni_scripts
omit =
    */tests/*
    */__pycache__/*
    */site-packages/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

#### Coverage Badges

Generate coverage badges for README:

```yaml
- name: Generate coverage badge
  run: |
    coverage-badge -o coverage.svg -f
```

---

## Test Data Management

### Test Fixtures

#### Fixture Organization

```python
# tests/python/fixtures/build_system_fixture.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def build_system_fixture():
    """Fixture for build system tests"""
    temp_dir = Path(tempfile.mkdtemp(prefix="build_system_"))

    # Create directory structure
    (temp_dir / "config").mkdir(parents=True, exist_ok=True)
    (temp_dir / "build").mkdir(parents=True, exist_ok=True)
    (temp_dir / "source").mkdir(parents=True, exist_ok=True)

    # Copy configuration files
    config_source = Path("config")
    if config_source.exists():
        for file in config_source.glob("*.json"):
            shutil.copy2(file, temp_dir / "config" / file.name)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
```

#### Fixture Dependencies

```python
@pytest.fixture
def compiler_fixture(build_system_fixture):
    """Fixture that depends on build_system_fixture"""
    from omni_scripts.compilers.detector import CompilerDetector
    detector = CompilerDetector()
    compiler = detector.detect_compiler()
    return {
        "build_dir": build_system_fixture / "build",
        "compiler": compiler
    }
```

### Mock Objects

#### Mock Compiler

```python
# tests/python/data/mocks/mock_compiler.py
from unittest.mock import Mock

class MockCompiler:
    """Mock compiler for testing"""

    def __init__(self):
        self.name = "mock-compiler"
        self.version = "1.0.0"
        self.path = "/usr/bin/mock-compiler"

    def compile(self, source, output):
        """Mock compile method"""
        return True

    def get_version(self):
        """Mock get_version method"""
        return self.version
```

#### Mock Package Manager

```python
# tests/python/data/mocks/mock_package_manager.py
from unittest.mock import Mock

class MockPackageManager:
    """Mock package manager for testing"""

    def __init__(self):
        self.name = "mock-pm"
        self.installed_packages = []

    def install(self, package):
        """Mock install method"""
        self.installed_packages.append(package)
        return True

    def is_available(self):
        """Mock is_available method"""
        return True
```

### Test Data Files

#### Configuration Files

```json
// tests/python/data/fixtures/config/test_config.json
{
  "version": "1.0.0",
  "build": {
    "type": "debug",
    "jobs": 4
  },
  "compiler": {
    "name": "gcc",
    "version": "13.2"
  }
}
```

#### Source Files

```cpp
// tests/cpp/data/fixtures/source/test_main.cpp
#include <iostream>

int main() {
    std::cout << "Test" << std::endl;
    return 0;
}
```

### Test Configuration

#### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=omni_scripts
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    system: System tests
    e2e: End-to-end tests
    slow: Slow running tests
    windows: Windows only tests
    linux: Linux only tests
    macos: macOS only tests
```

#### conftest.py

```python
# tests/python/config/conftest.py
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def test_config():
    """Load test configuration"""
    import json
    config_file = project_root / "tests" / "python" / "data" / "fixtures" / "config" / "test_config.json"
    with open(config_file) as f:
        return json.load(f)

@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    import logging
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    return logger
```

---

## Test Execution Workflow

### Local Development Workflow

#### 1. Write Test First (TDD)

```bash
# Create test file
touch tests/python/unit/controller/test_build_controller.py

# Write failing test
# (Implement test that fails)
```

#### 2. Run Test

```bash
# Run specific test
pytest tests/python/unit/controller/test_build_controller.py::test_build_command -v

# Run with coverage
pytest tests/python/unit/controller/test_build_controller.py --cov=omni_scripts/controller --cov-report=html
```

#### 3. Implement Code

```bash
# Implement minimum code to make test pass
# (Write implementation)
```

#### 4. Verify Test Passes

```bash
# Run test again
pytest tests/python/unit/controller/test_build_controller.py::test_build_command -v

# Verify coverage
pytest tests/python/unit/controller/test_build_controller.py --cov=omni_scripts/controller --cov-report=term-missing
```

#### 5. Refactor

```bash
# Refactor code while keeping tests green
# (Improve code quality)
```

#### 6. Run All Tests

```bash
# Run all unit tests
pytest tests/python/unit/ -v

# Run all tests
pytest tests/ -v
```

### CI/CD Workflow

#### 1. Trigger Pipeline

```yaml
# Triggered by:
# - Push to main/develop
# - Pull request to main/develop
# - Scheduled nightly runs
```

#### 2. Run Tests

```bash
# Python tests
pytest tests/python/ -v --cov=omni_scripts --cov-report=xml

# C++ tests
ctest --test-dir build --output-on-failure
```

#### 3. Generate Reports

```bash
# Coverage reports
coverage html
coverage xml

# Test reports
pytest --junitxml=test-results.xml
```

#### 4. Upload Artifacts

```yaml
- name: Upload coverage reports
  uses: actions/upload-artifact@v3
  with:
    name: coverage-reports
    path: |
      htmlcov/
      coverage.xml
```

#### 5. Notify Results

```yaml
- name: Notify test results
  if: failure()
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: 'Tests failed. Please check the logs.'
      })
```

### Test Execution Commands

#### Run All Tests

```bash
# Python tests
pytest tests/python/ -v

# C++ tests
ctest --test-dir build --output-on-failure

# All tests
pytest tests/ && ctest --test-dir build
```

#### Run Specific Test Suite

```bash
# Unit tests only
pytest tests/python/unit/ -v

# Integration tests only
pytest tests/python/integration/ -v

# System tests only
pytest tests/python/system/ -v

# E2E tests only
pytest tests/python/e2e/ -v
```

#### Run Tests by Marker

```bash
# Run unit tests
pytest -m unit -v

# Run integration tests
pytest -m integration -v

# Run slow tests
pytest -m slow -v

# Run Windows tests
pytest -m windows -v
```

#### Run Tests in Parallel

```bash
# Run with pytest-xdist
pytest tests/ -n auto -v

# Run with specific number of workers
pytest tests/ -n 4 -v
```

#### Run Tests with Coverage

```bash
# Generate HTML coverage report
pytest tests/ --cov=omni_scripts --cov-report=html

# Generate XML coverage report
pytest tests/ --cov=omni_scripts --cov-report=xml

# Generate terminal coverage report
pytest tests/ --cov=omni_scripts --cov-report=term-missing

# Generate all coverage reports
pytest tests/ --cov=omni_scripts --cov-report=html --cov-report=xml --cov-report=term-missing
```

---

## Test Reporting Strategy

### Test Result Formats

#### JUnit XML

```xml
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="BuildControllerTests" tests="5" failures="0" errors="0" skipped="0" time="1.234">
    <testcase name="test_build_command" classname="BuildControllerTests" time="0.123"/>
    <testcase name="test_clean_command" classname="BuildControllerTests" time="0.234"/>
  </testsuite>
</testsuites>
```

#### JSON Format

```json
{
  "version": "1.0.0",
  "timestamp": "2026-01-07T09:52:52.962Z",
  "summary": {
    "total": 100,
    "passed": 95,
    "failed": 3,
    "skipped": 2,
    "duration": 45.678
  },
  "test_suites": [
    {
      "name": "BuildControllerTests",
      "tests": 5,
      "passed": 5,
      "failed": 0,
      "skipped": 0,
      "duration": 1.234
    }
  ]
}
```

#### HTML Report

Generate HTML reports with pytest-html:

```bash
pytest tests/ --html=test-report.html --self-contained-html
```

### Coverage Reports

#### HTML Coverage Report

```bash
pytest tests/ --cov=omni_scripts --cov-report=html
# Open htmlcov/index.html in browser
```

#### XML Coverage Report

```bash
pytest tests/ --cov=omni_scripts --cov-report=xml
# Upload to Codecov, Coveralls, etc.
```

#### Terminal Coverage Report

```bash
pytest tests/ --cov=omni_scripts --cov-report=term-missing
```

### Test Metrics

#### Key Metrics to Track

1. **Test Count:** Total number of tests
2. **Pass Rate:** Percentage of passing tests
3. **Failure Rate:** Percentage of failing tests
4. **Skip Rate:** Percentage of skipped tests
5. **Test Duration:** Total time to run tests
6. **Coverage:** Line, branch, and function coverage
7. **Flaky Tests:** Tests that fail intermittently
8. **Slow Tests:** Tests that take longer than threshold

#### Metrics Dashboard

Create a metrics dashboard using:

- **GitHub Actions:** Built-in test results
- **Codecov:** Coverage reports and trends
- **Allure:** Test reports and analytics
- **Grafana:** Custom metrics dashboard

### Test Trends

#### Track Trends Over Time

1. **Coverage Trends:** Track coverage changes over time
2. **Test Count Trends:** Track test count growth
3. **Failure Rate Trends:** Track failure rate changes
4. **Performance Trends:** Track test execution time

#### Trend Visualization

```python
# Generate trend reports
import matplotlib.pyplot as plt

def plot_coverage_trend(coverage_data):
    """Plot coverage trend over time"""
    dates = [data['date'] for data in coverage_data]
    coverage = [data['coverage'] for data in coverage_data]

    plt.plot(dates, coverage)
    plt.xlabel('Date')
    plt.ylabel('Coverage (%)')
    plt.title('Coverage Trend')
    plt.savefig('coverage_trend.png')
```

### Test Notifications

#### Email Notifications

```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 'Tests failed'
    to: team@example.com
    from: ci@example.com
    body: 'Tests failed. Please check the logs.'
```

#### Slack Notifications

```yaml
- name: Slack notification
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Tests failed'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## TDD Implementation Guidelines

### Red-Green-Refactor Cycle

#### 1. Red: Write Failing Test

```python
# Write test that describes desired behavior
def test_build_command():
    """Verify build command executes successfully"""
    from omni_scripts.controller.build_controller import BuildController
    controller = BuildController()
    result = controller.execute(["engine", "debug"])
    assert result == 0  # This will fail initially
```

#### 2. Green: Write Minimum Code

```python
# Write minimum code to make test pass
class BuildController(BaseController):
    def execute(self, args):
        # Minimum implementation
        return 0
```

#### 3. Refactor: Improve Code

```python
# Refactor while keeping tests green
class BuildController(BaseController):
    def execute(self, args):
        """Execute build command"""
        target = args[0] if args else "all"
        config = args[1] if len(args) > 1 else "release"

        self.logger.info(f"Building {target} with {config} configuration")

        # Actual build logic
        result = self._build(target, config)

        return result

    def _build(self, target, config):
        """Internal build method"""
        # Build implementation
        return 0
```

### Test First Checklist

Before writing implementation code:

- [ ] Write test that describes desired behavior
- [ ] Run test and verify it fails (Red)
- [ ] Write minimum code to make test pass (Green)
- [ ] Run test and verify it passes
- [ ] Refactor code while keeping tests green
- [ ] Run all tests to ensure no regressions
- [ ] Check coverage meets requirements

### Test Design Principles

#### AAA Pattern (Arrange-Act-Assert)

```python
def test_build_command():
    """Verify build command executes successfully"""
    # Arrange
    controller = BuildController()
    args = ["engine", "debug"]

    # Act
    result = controller.execute(args)

    # Assert
    assert result == 0
```

#### Given-When-Then Pattern

```python
def test_build_command():
    """Verify build command executes successfully"""
    # Given
    controller = BuildController()
    args = ["engine", "debug"]

    # When
    result = controller.execute(args)

    # Then
    assert result == 0
```

#### One Assertion Per Test

```python
# Good: One assertion
def test_build_command_returns_zero():
    """Verify build command returns zero on success"""
    controller = BuildController()
    result = controller.execute(["engine", "debug"])
    assert result == 0

# Bad: Multiple assertions
def test_build_command():
    """Verify build command"""
    controller = BuildController()
    result = controller.execute(["engine", "debug"])
    assert result == 0
    assert controller.logger is not None  # Separate test
```

### Test Naming Conventions

#### Descriptive Test Names

```python
# Good: Descriptive
def test_build_command_returns_zero_on_success():
    """Verify build command returns zero on success"""
    pass

# Bad: Vague
def test_build():
    """Test build"""
    pass
```

#### Test Name Format

```
test_<component>_<action>_<expected_result>
```

Examples:
- `test_build_controller_returns_zero_on_success`
- `test_compiler_detection_finds_gcc_on_linux`
- `test_package_manager_installs_package_correctly`

### Test Organization

#### Group Related Tests

```python
class TestBuildController:
    """Tests for BuildController"""

    def test_build_command(self):
        """Test build command"""
        pass

    def test_clean_command(self):
        """Test clean command"""
        pass

class TestCompilerDetection:
    """Tests for CompilerDetection"""

    def test_gcc_detection(self):
        """Test GCC detection"""
        pass

    def test_clang_detection(self):
        """Test Clang detection"""
        pass
```

#### Use Test Markers

```python
import pytest

@pytest.mark.unit
def test_build_command():
    """Unit test for build command"""
    pass

@pytest.mark.integration
def test_full_build_workflow():
    """Integration test for full build workflow"""
    pass

@pytest.mark.slow
def test_large_build():
    """Slow test for large build"""
    pass

@pytest.mark.windows
def test_msvc_detection():
    """Windows-only test for MSVC detection"""
    pass
```

---

## Test Maintenance

### Test Review Process

#### Regular Test Reviews

1. **Weekly:** Review flaky tests
2. **Monthly:** Review slow tests
3. **Quarterly:** Review test coverage
4. **Annually:** Review test strategy

#### Test Review Checklist

- [ ] Are tests still relevant?
- [ ] Are tests passing consistently?
- [ ] Is test coverage adequate?
- [ ] Are tests well-documented?
- [ ] Are tests maintainable?
- [ ] Are tests fast enough?

### Test Refactoring

#### When to Refactor Tests

- Tests are slow
- Tests are flaky
- Tests are hard to understand
- Tests are duplicated
- Tests are brittle

#### Refactoring Guidelines

1. **Extract Common Setup:** Use fixtures for common setup
2. **Remove Duplication:** Create helper functions for repeated code
3. **Improve Readability:** Use descriptive names and comments
4. **Reduce Dependencies:** Mock external dependencies
5. **Optimize Performance:** Parallelize slow tests

### Test Documentation

#### Document Test Purpose

```python
def test_build_command_returns_zero_on_success():
    """
    Verify that the build command returns zero on success.

    This test ensures that when the build command is executed
    with valid arguments, it returns a zero exit code indicating
    success.

    Related Requirements:
    - REQ-001: OmniCppController.py as Single Entry Point
    - REQ-002: Modular Controller Pattern Implementation
    """
    controller = BuildController()
    result = controller.execute(["engine", "debug"])
    assert result == 0
```

#### Document Test Scenarios

```python
@pytest.mark.parametrize("target,config,expected_result", [
    ("engine", "debug", 0),
    ("engine", "release", 0),
    ("game", "debug", 0),
])
def test_build_various_targets(target, config, expected_result):
    """
    Test building various targets with different configurations.

    Scenarios:
    1. Build engine with debug configuration
    2. Build engine with release configuration
    3. Build game with debug configuration

    Expected Result:
    All builds should succeed (return 0)
    """
    controller = BuildController()
    result = controller.execute([target, config])
    assert result == expected_result
```

### Test Deletion

#### When to Delete Tests

- Feature is removed
- Test is redundant
- Test is obsolete
- Test cannot be maintained

#### Test Deletion Process

1. **Identify Obsolete Tests:** Review test relevance
2. **Verify No Coverage Loss:** Check coverage impact
3. **Delete Test:** Remove test file
4. **Run All Tests:** Ensure no regressions
5. **Update Documentation:** Update test documentation

---

## References

### Related Documents

- [`.specs/04_future_state/reqs/`](./reqs/) - Requirements
- [`.specs/04_future_state/design/`](./design/) - Design Documents
- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Coding Standards
- [`.specs/02_current_state/`](../02_current_state/) - Current State
- [`.specs/03_threat_model/`](../03_threat_model/) - Threat Model
- [`.specs/05_adrs/`](../05_adrs/) - Architecture Decision Records

### External References

- [pytest Documentation](https://docs.pytest.org/)
- [Google Test Documentation](https://google.github.io/googletest/)
- [CMake Testing](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [Code Coverage](https://codecov.io/)
- [TDD Best Practices](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

### Tools and Frameworks

#### Python Testing

- **pytest:** Test framework
- **pytest-cov:** Coverage plugin
- **pytest-xdist:** Parallel test execution
- **pytest-mock:** Mocking support
- **pytest-html:** HTML reports

#### C++ Testing

- **Google Test:** Test framework
- **Google Mock:** Mocking framework
- **gcov/lcov:** Coverage tools

#### CI/CD

- **GitHub Actions:** CI/CD platform
- **Codecov:** Coverage reporting
- **Allure:** Test reporting

---

## Appendix

### Test Metrics Dashboard Template

```markdown
# Test Metrics Dashboard

## Summary
- Total Tests: 100
- Passed: 95
- Failed: 3
- Skipped: 2
- Pass Rate: 95%

## Coverage
- Line Coverage: 85%
- Branch Coverage: 80%
- Function Coverage: 90%

## Test Duration
- Total Time: 45.678s
- Average Time: 0.457s
- Slowest Test: 5.123s

## Flaky Tests
- test_build_command (failed 2 times)
- test_package_install (failed 1 time)

## Slow Tests
- test_full_build (5.123s)
- test_cross_compilation (3.456s)
```

### Test Report Template

```markdown
# Test Report

## Test Run Information
- Date: 2026-01-07
- Time: 09:52:52 UTC
- Platform: Windows 11
- Python Version: 3.11.0
- C++ Compiler: MSVC 19.35

## Test Results
- Total Tests: 100
- Passed: 95
- Failed: 3
- Skipped: 2
- Pass Rate: 95%

## Coverage
- Line Coverage: 85%
- Branch Coverage: 80%
- Function Coverage: 90%

## Failed Tests
1. test_build_command (BuildControllerTests)
   - Error: Assertion failed
   - Location: tests/python/unit/controller/test_build_controller.py:42

2. test_package_install (PackageManagerTests)
   - Error: Package not found
   - Location: tests/python/unit/package_managers/test_conan.py:78

3. test_cross_compilation (CrossPlatformTests)
   - Error: Toolchain not found
   - Location: tests/python/cross_platform/test_arm64.py:56

## Recommendations
1. Fix failing build command test
2. Update package installation test
3. Configure cross-compilation toolchain
```

### Test Checklist Template

```markdown
# Test Checklist

## Pre-Test
- [ ] Test environment is set up
- [ ] Dependencies are installed
- [ ] Configuration files are in place
- [ ] Test data is prepared

## During Test
- [ ] Tests are running
- [ ] No unexpected errors
- [ ] Tests are completing in reasonable time

## Post-Test
- [ ] All tests passed
- [ ] Coverage meets requirements
- [ ] Test reports are generated
- [ ] Results are documented
```

---

**Document Status:** Draft
**Next Review Date:** 2026-01-14
**Approved By:** [Pending Approval]
**Version History:**
- v1.0.0 (2026-01-07): Initial draft
