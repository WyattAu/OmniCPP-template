# OmniCppController Automated Testing Framework

This directory contains a comprehensive automated testing framework for validating cross-platform consistency and functionality of the OmniCppController build pipeline.

## Overview

The testing framework consists of multiple specialized validation scripts that ensure:

- **Cross-platform consistency** across Windows and Linux
- **Toolchain compatibility** with MSVC, Clang, GCC, and MinGW
- **Build reliability** and artifact consistency
- **Performance monitoring** and optimization insights
- **Platform-specific validation** for Windows/Linux environments
- **Comprehensive test coverage** including edge cases and error conditions

## Test Scripts

### 1. Cross-Platform Validation (`cross_platform_validation.py`)

Validates cross-platform consistency across different toolchains and platforms.

**Usage:**
```bash
# Auto-detect platform and test all supported toolchains
python cross_platform_validation.py

# Specify platform and toolchains
python cross_platform_validation.py --platform windows --toolchains msvc,clang-msvc

# Custom output directory
python cross_platform_validation.py --output custom_reports
```

**What it tests:**
- Toolchain detection and configuration
- Build artifact consistency
- CMake configuration equivalence
- Dependency resolution
- Cross-platform compatibility

### 2. Toolchain Validation (`toolchain_validation.py`)

Validates toolchain-specific configurations and dependencies.

**Usage:**
```bash
# Test all supported toolchains
python toolchain_validation.py

# Test specific toolchains
python toolchain_validation.py --toolchains msvc,gcc

# Custom output directory
python toolchain_validation.py --output toolchain_reports
```

**What it tests:**
- Toolchain executable detection
- Path configuration validation
- Compiler flag validation
- Dependency availability
- Toolchain-specific environment setup

### 3. Build Consistency (`build_consistency.py`)

Compares build outputs across different toolchains to ensure consistency.

**Usage:**
```bash
# Test all toolchains with debug/release builds
python build_consistency.py

# Test specific toolchains and build types
python build_consistency.py --toolchains msvc,clang-msvc --build-types debug

# Custom output directory
python build_consistency.py --output consistency_reports
```

**What it tests:**
- Build artifact comparison
- Build time consistency
- Output file validation
- Packaging consistency
- Installation validation

### 4. Platform Checks (`platform_checks.py`)

Performs platform-specific validation checks.

**Usage:**
```bash
# Auto-detect and test current platform
python platform_checks.py

# Test specific platform
python platform_checks.py --platform linux

# Custom output directory
python platform_checks.py --output platform_reports
```

**What it tests:**
- Windows: VS DevCmd, MSYS2, MinGW, Windows SDK
- Linux: bash, package managers, development packages
- Path handling validation
- Environment variable validation
- Platform-specific dependencies

### 5. Performance Monitoring (`performance_monitoring.py`)

Monitors build performance and resource usage.

**Usage:**
```bash
# Run performance tests with 3 iterations per test
python performance_monitoring.py --iterations 3

# Test specific toolchains
python performance_monitoring.py --toolchains msvc,gcc --iterations 5

# Custom output directory
python performance_monitoring.py --output performance_reports
```

**What it tests:**
- Build time tracking
- CPU and memory usage monitoring
- Success/failure rate analysis
- Performance trend analysis
- Resource efficiency comparison

### 6. Comprehensive Test Suite (`test_suite.py`)

Runs a complete test suite covering all functionality.

**Usage:**
```bash
# Run quick smoke tests (default)
python test_suite.py --quick

# Run full comprehensive test suite
python test_suite.py --full

# Custom output directory
python test_suite.py --output test_reports
```

**What it tests:**
- Basic controller functionality
- Configuration validation
- Build pipeline testing
- Edge cases and error conditions
- Cross-platform compatibility
- Vulkan/Qt integration
- Toolchain compatibility

## Quick Start

### Running All Tests

1. **Quick validation** (recommended for regular checks):
   ```bash
   cd impl/tests
   python test_suite.py --quick
   ```

2. **Full validation** (comprehensive testing):
   ```bash
   cd impl/tests
   python test_suite.py --full
   ```

3. **Individual component testing**:
   ```bash
   # Cross-platform validation
   python cross_platform_validation.py

   # Toolchain validation
   python toolchain_validation.py

   # Build consistency
   python build_consistency.py

   # Platform checks
   python platform_checks.py

   # Performance monitoring
   python performance_monitoring.py
   ```

## Output and Reports

All test scripts generate JSON reports in the `validation_reports/` directory (or custom directory if specified). Reports include:

- **Test results** with pass/fail status
- **Performance metrics** and timing data
- **Error details** and failure analysis
- **Recommendations** for improvements
- **Consistency scores** and validation metrics

### Report Structure

```
validation_reports/
├── cross_platform_validation_[timestamp].json
├── toolchain_validation_[timestamp].json
├── build_consistency_[timestamp].json
├── platform_checks_[platform]_[timestamp].json
├── performance_monitoring_[timestamp].json
└── test_suite_[type]_[timestamp].json
```

## Prerequisites

### System Requirements

- **Python 3.8+** with standard library
- **CMake 3.20+**
- **Ninja build system** (recommended)
- **Git** for dependency management

### Platform-Specific Requirements

#### Windows
- Visual Studio 2019/2022 with MSVC compiler
- Windows SDK
- MSYS2/MinGW (for GCC/Clang-MinGW toolchains)
- Vulkan SDK (optional, for Vulkan-Qt integration)

#### Linux
- GCC 9+ or Clang 10+
- Development packages: `build-essential`, `cmake`, `ninja-build`
- Vulkan development packages (optional)
- Qt development packages (optional)

### Dependencies

The test scripts use only Python standard library modules, with optional dependencies:

- `psutil` for performance monitoring (recommended)
- `statistics` (Python 3.8+ built-in)

## Test Categories

### Functional Tests
- Command-line interface validation
- Configuration file parsing
- Build pipeline execution
- Error handling and recovery

### Compatibility Tests
- Cross-platform path handling
- Toolchain detection and setup
- Dependency resolution
- Environment variable handling

### Performance Tests
- Build time analysis
- Resource usage monitoring
- Memory and CPU profiling
- Scalability testing

### Integration Tests
- Vulkan SDK integration
- Qt framework integration
- External dependency management
- Packaging and distribution

## Troubleshooting

### Common Issues

1. **Toolchain not detected**
   - Ensure toolchain executables are in PATH
   - Check Visual Studio/MSYS2 installation
   - Verify environment variables

2. **Build failures**
   - Check CMake version compatibility
   - Verify dependency installations
   - Review build logs for specific errors

3. **Performance monitoring errors**
   - Install `psutil`: `pip install psutil`
   - Check system permissions for resource monitoring

4. **Path handling issues**
   - Ensure consistent path separators
   - Check for mixed absolute/relative paths
   - Verify workspace directory structure

### Debug Mode

Run tests with verbose output:
```bash
python test_script.py --verbose
```

Enable debug logging in the controller:
```bash
python OmniCppController.py --debug command args...
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Cross-Platform Validation
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest]

    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Run Tests
      run: |
        cd impl/tests
        python test_suite.py --quick
```

### Local CI Setup

Create a local test script:

```bash
#!/bin/bash
# run_tests.sh

cd impl/tests

echo "Running quick test suite..."
python test_suite.py --quick

echo "Running cross-platform validation..."
python cross_platform_validation.py

echo "Running toolchain validation..."
python toolchain_validation.py

echo "Tests completed. Check validation_reports/ for results."
```

## Contributing

When adding new tests:

1. Follow the existing script structure
2. Include comprehensive error handling
3. Generate detailed JSON reports
4. Update this README with new test information
5. Test on both Windows and Linux platforms

## Support

For issues or questions:

1. Check the generated test reports for detailed error information
2. Review the controller debug logs
3. Verify system requirements and dependencies
4. Check platform-specific documentation

## Version History

- **v1.0** - Initial comprehensive testing framework
  - Cross-platform validation
  - Toolchain compatibility checks
  - Build consistency verification
  - Performance monitoring
  - Platform-specific validation
  - Comprehensive test suite</content>
</xai:function_call"> 

<xai:function_call name="update_todo_list">
<parameter name="todos">[x] Create cross-platform validation script\n[x] Create toolchain validation checks\n[x] Create build consistency checks\n[x] Create platform-specific checks\n[x] Create performance monitoring\n[x] Create comprehensive test suite\n[x] Create documentation for running tests\n[-] Provide summary of all created files