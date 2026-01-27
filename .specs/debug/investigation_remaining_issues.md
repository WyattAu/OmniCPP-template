# Investigation Report: Why --compiler Flag Fixes Didn't Work

**Date:** 2026-01-19  
**Role:** Scout Agent  
**Task:** Investigate Why --compiler Flag Fixes Didn't Work

## Executive Summary

The `--compiler` flag was added to the CLI parser for all commands (configure, build, install, test, package), but only the `build` command works correctly. The root cause is that the individual command controllers (configure, install, test, package) are NOT extracting and using the `compiler` argument from the parsed args, even though the CLI parser defines it.

## Root Cause Analysis

### The Problem

The CLI parser in [`omni_scripts/controller/cli.py`](omni_scripts/controller/cli.py) correctly defines the `--compiler` flag for all commands:

| Command | CLI Parser Definition | Line Numbers |
|---------|----------------------|--------------|
| configure | ✅ Defined | 171-174 |
| build | ✅ Defined | 238-241 |
| install | ✅ Defined | 331-334 |
| test | ✅ Defined | 382-385 |
| package | ✅ Defined | 433-436 |

However, the command controllers are NOT extracting this argument from `args`:

| Command | Extracts `compiler`? | Line Numbers |
|---------|----------------------|--------------|
| configure | ❌ NO | 34-46 |
| build | ✅ YES | 41 |
| install | ❌ NO | 30-40 |
| test | ❌ NO | 27-38 |
| package | ❌ NO | 30-40 |

### Why This Causes the Issue

When argparse parses the command-line arguments, it creates a `Namespace` object containing all the parsed values. If a controller doesn't extract a specific argument from this namespace using `getattr(args, "compiler", None)`, the argument is effectively ignored, even though it was successfully parsed by the CLI parser.

The verification tests show that the `--compiler` flag appears to be "not supported" because the controllers don't acknowledge its existence - they simply don't use it.

## Detailed Comparison: Working vs Non-Working Commands

### BuildController (WORKING) - [`omni_scripts/controller/build_controller.py`](omni_scripts/controller/build_controller.py)

```python
def __init__(self, args: argparse.Namespace) -> None:
    """Initialize build controller.

    Args:
        args: Parsed command-line arguments.
    """
    super().__init__(args)
    self.target = getattr(args, "target", "all")
    self.pipeline = getattr(args, "pipeline", "default")
    self.preset = getattr(args, "preset", "default")
    self.config = getattr(args, "config", "release")
    self.compiler = getattr(args, "compiler", None)  # ← EXTRACTS COMPILER
    self.clean = getattr(args, "clean", False)
    self.parallel = getattr(args, "parallel", None)
```

And validates it:

```python
def validate_arguments(self) -> None:
    """Validate build command arguments.

    Raises:
        InvalidTargetError: If target is invalid.
        ControllerError: If other arguments are invalid.
    """
    # Validate target
    self.validate_target(self.target)

    # Validate config
    self.validate_config(self.config)

    # Validate compiler if specified
    self.validate_compiler(self.compiler)  # ← VALIDATES COMPILER

    # Validate preset exists
    cmake_wrapper = CMakeWrapper(source_dir=self.get_project_root())
    preset = cmake_wrapper.get_preset(self.preset)
    if preset is None:
        self.logger.warning(f"CMake preset not found: {self.preset}")
        self.logger.info("Using default preset")
```

### ConfigureController (NOT WORKING) - [`omni_scripts/controller/configure_controller.py`](omni_scripts/controller/configure_controller.py)

```python
def __init__(self, args: argparse.Namespace) -> None:
    """Initialize the configure controller.

    Args:
        args: Parsed command-line arguments.
    """
    super().__init__(args)
    self.build_type = getattr(args, "build_type", "Release")
    self.generator = getattr(args, "generator", None)
    self.toolchain = getattr(args, "toolchain", None)
    self.preset = getattr(args, "preset", None)
    self.configure_conan = getattr(args, "configure_conan", False)
    self.configure_vcpkg = getattr(args, "configure_vcpkg", False)
    # ❌ MISSING: self.compiler = getattr(args, "compiler", None)
```

### InstallController (NOT WORKING) - [`omni_scripts/controller/install_controller.py`](omni_scripts/controller/install_controller.py)

```python
def __init__(self, args: argparse.Namespace) -> None:
    """Initialize install controller.

    Args:
        args: Parsed command-line arguments.
    """
    super().__init__(args)
    self.target = getattr(args, "target", "all")
    self.config = getattr(args, "config", "release")
    self.install_dependencies = getattr(args, "install_dependencies", False)
    self.install_prefix = getattr(args, "prefix", None)
    # ❌ MISSING: self.compiler = getattr(args, "compiler", None)
```

### TestController (NOT WORKING) - [`omni_scripts/controller/test_controller.py`](omni_scripts/controller/test_controller.py)

```python
def __init__(self, args: argparse.Namespace) -> None:
    """Initialize test controller.

    Args:
        args: Parsed command-line arguments.
    """
    super().__init__(args)
    self.logger = logging.getLogger(self.__class__.__name__)
    self.cmake_wrapper = CMakeWrapper(
        source_dir=Path.cwd(),
        build_dir=Path("build")
    )
    # ❌ MISSING: self.compiler = getattr(args, "compiler", None)
```

### PackageController (NOT WORKING) - [`omni_scripts/controller/package_controller.py`](omni_scripts/controller/package_controller.py)

```python
def __init__(self, args: argparse.Namespace) -> None:
    """Initialize package controller.

    Args:
        args: Parsed command-line arguments.
    """
    super().__init__(args)
    self.target = getattr(args, "target", "all")
    self.config = getattr(args, "config", "release")
    self.format = getattr(args, "format", None)
    self.output_dir = getattr(args, "output_dir", None)
    # ❌ MISSING: self.compiler = getattr(args, "compiler", None)
```

## Available Infrastructure

The [`BaseController`](omni_scripts/controller/base.py) class already provides the necessary infrastructure:

1. **`VALID_COMPILERS` constant** (lines 44-51):
   ```python
   VALID_COMPILERS = [
       "msvc",
       "clang-msvc",
       "mingw-clang",
       "mingw-gcc",
       "gcc",
       "clang",
   ]
   ```

2. **`validate_compiler` method** (lines 104-119):
   ```python
   def validate_compiler(self, compiler: Optional[str]) -> None:
       """Validate that a compiler is valid.

       Args:
           compiler: The compiler to validate. If None, validation is skipped.

       Raises:
           ControllerError: If the compiler is not valid.
       """
       if compiler is not None and compiler not in self.VALID_COMPILERS:
           raise ControllerError(
               message=f"Invalid compiler '{compiler}'. Valid compilers are: {', '.join(self.VALID_COMPILERS)}",
               command=getattr(self.args, "command", "unknown"),
               context={"compiler": compiler, "valid_compilers": self.VALID_COMPILERS},
               exit_code=2,
           )
   ```

## Recommended Fix Approach

For each non-working command controller, the following changes are needed:

### 1. ConfigureController

**File:** [`omni_scripts/controller/configure_controller.py`](omni_scripts/controller/configure_controller.py)

**Changes:**
1. Add `self.compiler = getattr(args, "compiler", None)` to `__init__` method (after line 46)
2. Add `self.validate_compiler(self.compiler)` to `validate_arguments` method (after line 55)

### 2. InstallController

**File:** [`omni_scripts/controller/install_controller.py`](omni_scripts/controller/install_controller.py)

**Changes:**
1. Add `self.compiler = getattr(args, "compiler", None)` to `__init__` method (after line 40)
2. Add `self.validate_compiler(self.compiler)` to `validate_arguments` method (after line 53)

### 3. TestController

**File:** [`omni_scripts/controller/test_controller.py`](omni_scripts/controller/test_controller.py)

**Changes:**
1. Add `self.compiler = getattr(args, "compiler", None)` to `__init__` method (after line 38)
2. Add `self.validate_compiler(self.compiler)` to `validate_arguments` method (create this method if it doesn't exist)

### 4. PackageController

**File:** [`omni_scripts/controller/package_controller.py`](omni_scripts/controller/package_controller.py)

**Changes:**
1. Add `self.compiler = getattr(args, "compiler", None)` to `__init__` method (after line 40)
2. Add `self.validate_compiler(self.compiler)` to `validate_arguments` method (after line 53)

## Summary of Required Changes

| Controller | File | Add to `__init__` | Add to `validate_arguments` |
|------------|------|-------------------|----------------------------|
| ConfigureController | [`configure_controller.py`](omni_scripts/controller/configure_controller.py) | `self.compiler = getattr(args, "compiler", None)` | `self.validate_compiler(self.compiler)` |
| InstallController | [`install_controller.py`](omni_scripts/controller/install_controller.py) | `self.compiler = getattr(args, "compiler", None)` | `self.validate_compiler(self.compiler)` |
| TestController | [`test_controller.py`](omni_scripts/controller/test_controller.py) | `self.compiler = getattr(args, "compiler", None)` | `self.validate_compiler(self.compiler)` |
| PackageController | [`package_controller.py`](omni_scripts/controller/package_controller.py) | `self.compiler = getattr(args, "compiler", None)` | `self.validate_compiler(self.compiler)` |

## Conclusion

The `--compiler` flag fixes didn't work because the CLI parser changes were incomplete. While the flag was added to the argument parser for all commands, the individual command controllers were not updated to extract and use this argument. The fix is straightforward: each non-working controller needs to:

1. Extract the `compiler` argument from `args` in its `__init__` method
2. Validate the compiler argument in its `validate_arguments` method

The infrastructure for compiler validation already exists in the [`BaseController`](omni_scripts/controller/base.py) class, so the implementation can follow the same pattern used by the working [`BuildController`](omni_scripts/controller/build_controller.py).

## Related Bugs

This investigation addresses the following bugs:
- **BUG-012:** Configure --compiler flag
- **BUG-014:** Install --compiler flag
- **BUG-015:** Test --compiler flag
- **BUG-016:** Package --compiler flag

All four bugs have the same root cause and can be fixed with the same approach.
