# ADR-007: Consolidation of Python Scripts into omni_scripts/

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Python Architecture

---

## Context

The OmniCPP Template project currently has Python scripts scattered across multiple directories, leading to code duplication, maintenance issues, and confusion about which scripts to use. The project needs a unified, organized structure for all Python build and utility scripts.

### Current State

Python scripts are distributed across three directories:

1. **Root Directory:**
   - `OmniCppController.py` - Main controller script
   - `scaffold_directories.py` - Directory scaffolding

2. **`scripts/` Directory:**
   - `build.py` - Build script
   - `clean.py` - Clean script
   - `format.py` - Format script
   - `install.py` - Install script
   - `lint.py` - Lint script
   - `package.py` - Package script
   - `test.py` - Test script
   - `validate_environment.py` - Environment validation
   - `setup_environment.bat` - Windows environment setup
   - `setup_environment.ps1` - PowerShell environment setup
   - `detect_msvc_version.ps1` - MSVC version detection
   - `scripts/python/` - Python utility modules

3. **`omni_scripts/` Directory:**
   - `build.py` - Build script
   - `cmake.py` - CMake utilities
   - `conan.py` - Conan utilities
   - `config.py` - Configuration utilities
   - `error_handler.py` - Error handling
   - `exceptions.py` - Custom exceptions
   - `job_optimizer.py` - Job optimization
   - `resilience_manager.py` - Resilience management
   - `setup_vulkan.py` - Vulkan setup
   - `omni_scripts/build_system/` - Build system modules
   - `omni_scripts/compilers/` - Compiler detection
   - `omni_scripts/controller/` - Controller modules
   - `omni_scripts/logging/` - Logging modules
   - `omni_scripts/platform/` - Platform detection
   - `omni_scripts/utils/` - Utility modules
   - `omni_scripts/validators/` - Validation modules

### Issues

1. **Code Duplication:** Multiple versions of similar scripts (e.g., `build.py` in both `scripts/` and `omni_scripts/`)
2. **Confusion:** Developers unsure which scripts to use
3. **Maintenance Burden:** Changes must be made in multiple places
4. **Inconsistent Quality:** Different scripts have different quality levels
5. **No Clear Entry Point:** Multiple entry points for build operations
6. **Deprecated Scripts:** Some scripts are outdated but still present

## Decision

**Consolidate all Python scripts into the `omni_scripts/` directory** and establish a clear, modular structure.

### 1. Target Directory Structure

```
omni_scripts/
├── __init__.py
├── OmniCppController.py          # Main entry point (moved from root)
├── build.py                      # Build operations (consolidated)
├── clean.py                      # Clean operations (consolidated)
├── format.py                     # Format operations (consolidated)
├── install.py                    # Install operations (consolidated)
├── lint.py                       # Lint operations (consolidated)
├── package.py                    # Package operations (consolidated)
├── test.py                       # Test operations (consolidated)
├── validate_environment.py       # Environment validation (consolidated)
├── scaffold_directories.py       # Directory scaffolding (moved from root)
├── setup_vulkan.py               # Vulkan setup (existing)
├── build_system/                 # Build system modules (existing)
│   ├── __init__.py
│   ├── cmake.py
│   ├── conan.py
│   ├── optimizer.py
│   └── vcpkg.py
├── compilers/                    # Compiler detection (existing)
│   ├── __init__.py
│   ├── base.py
│   ├── clang.py
│   ├── detector.py
│   ├── gcc.py
│   └── msvc.py
├── controller/                   # Controller modules (existing)
│   ├── __init__.py
│   ├── base.py
│   ├── build_controller.py
│   ├── clean_controller.py
│   ├── cli.py
│   ├── config_controller.py
│   ├── configure_controller.py
│   ├── dispatcher.py
│   ├── format_controller.py
│   ├── install_controller.py
│   ├── lint_controller.py
│   ├── package_controller.py
│   └── test_controller.py
├── logging/                      # Logging modules (existing)
│   ├── __init__.py
│   ├── config.py
│   ├── formatters.py
│   ├── handlers.py
│   └── logger.py
├── platform/                     # Platform detection (existing)
│   ├── __init__.py
│   ├── detector.py
│   ├── linux.py
│   ├── macos.py
│   └── windows.py
├── utils/                        # Utility modules (existing)
│   ├── __init__.py
│   ├── command_utils.py
│   ├── exceptions.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   ├── path_utils.py
│   ├── platform_utils.py
│   ├── system_utils.py
│   └── terminal_utils.py
└── validators/                    # Validation modules (existing)
    ├── __init__.py
    ├── build_validator.py
    ├── config_validator.py
    └── dependency_validator.py
```

### 2. Migration Strategy

```python
# scripts/migrate_to_omni_scripts.py
#!/usr/bin/env python3
"""Migrate scripts from root and scripts/ to omni_scripts/."""

import os
import shutil
from pathlib import Path

def migrate_scripts():
    """Migrate scripts to omni_scripts/."""
    root_dir = Path(__file__).parent.parent
    omni_scripts_dir = root_dir / "omni_scripts"
    scripts_dir = root_dir / "scripts"

    # Scripts to move from root
    root_scripts = [
        "OmniCppController.py",
        "scaffold_directories.py"
    ]

    # Scripts to move from scripts/
    scripts_to_move = [
        "build.py",
        "clean.py",
        "format.py",
        "install.py",
        "lint.py",
        "package.py",
        "test.py",
        "validate_environment.py"
    ]

    # Move scripts from root
    for script in root_scripts:
        src = root_dir / script
        dst = omni_scripts_dir / script
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved {script} from root to omni_scripts/")

    # Move scripts from scripts/
    for script in scripts_to_move:
        src = scripts_dir / script
        dst = omni_scripts_dir / script
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved {script} from scripts/ to omni_scripts/")

    # Move scripts/python/ to omni_scripts/python/
    python_dir = scripts_dir / "python"
    if python_dir.exists():
        dst_dir = omni_scripts_dir / "python"
        if dst_dir.exists():
            shutil.rmtree(str(dst_dir))
        shutil.move(str(python_dir), str(dst_dir))
        print(f"Moved scripts/python/ to omni_scripts/python/")

    print("\nMigration complete!")
    print(f"All scripts are now in {omni_scripts_dir}")

if __name__ == "__main__":
    migrate_scripts()
```

### 3. Entry Point

```python
# omni_scripts/OmniCppController.py
#!/usr/bin/env python3
"""
OmniCppController - Main entry point for all build operations.

This script provides a unified interface for all build operations:
- Build: Configure and build the project
- Clean: Clean build artifacts
- Format: Format code
- Install: Install dependencies
- Lint: Lint code
- Package: Package the project
- Test: Run tests
- Validate: Validate environment
"""

import sys
from pathlib import Path

# Add omni_scripts to path
omni_scripts_dir = Path(__file__).parent
sys.path.insert(0, str(omni_scripts_dir))

from controller.cli import main

if __name__ == "__main__":
    sys.exit(main())
```

### 4. CLI Interface

```python
# omni_scripts/controller/cli.py
#!/usr/bin/env python3
"""Command-line interface for OmniCppController."""

import argparse
import sys
from pathlib import Path

# Add omni_scripts to path
omni_scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(omni_scripts_dir))

from controller.build_controller import BuildController
from controller.clean_controller import CleanController
from controller.format_controller import FormatController
from controller.install_controller import InstallController
from controller.lint_controller import LintController
from controller.package_controller import PackageController
from controller.test_controller import TestController
from controller.config_controller import ConfigController

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OmniCppController - Build system controller"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build the project")
    build_parser.add_argument("--preset", help="CMake preset to use")
    build_parser.add_argument("--target", help="Target to build")
    build_parser.add_argument("--clean", action="store_true", help="Clean before build")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean build artifacts")
    clean_parser.add_argument("--all", action="store_true", help="Clean all artifacts")

    # Format command
    format_parser = subparsers.add_parser("format", help="Format code")
    format_parser.add_argument("--check", action="store_true", help="Check formatting only")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install dependencies")
    install_parser.add_argument("--manager", help="Package manager to use")

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Lint code")
    lint_parser.add_argument("--fix", action="store_true", help="Fix linting issues")

    # Package command
    package_parser = subparsers.add_parser("package", help="Package the project")
    package_parser.add_argument("--type", help="Package type")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--suite", help="Test suite to run")
    test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate environment")
    validate_parser.add_argument("--full", action="store_true", help="Full validation")

    args = parser.parse_args()

    if args.command == "build":
        controller = BuildController()
        return controller.run(args)
    elif args.command == "clean":
        controller = CleanController()
        return controller.run(args)
    elif args.command == "format":
        controller = FormatController()
        return controller.run(args)
    elif args.command == "install":
        controller = InstallController()
        return controller.run(args)
    elif args.command == "lint":
        controller = LintController()
        return controller.run(args)
    elif args.command == "package":
        controller = PackageController()
        return controller.run(args)
    elif args.command == "test":
        controller = TestController()
        return controller.run(args)
    elif args.command == "validate":
        controller = ConfigController()
        return controller.validate(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 5. Usage Examples

```bash
# Build the project
python omni_scripts/OmniCppController.py build --preset windows-msvc-debug

# Clean build artifacts
python omni_scripts/OmniCppController.py clean --all

# Format code
python omni_scripts/OmniCppController.py format

# Install dependencies
python omni_scripts/OmniCppController.py install --manager conan

# Run tests
python omni_scripts/OmniCppController.py test --coverage

# Validate environment
python omni_scripts/OmniCppController.py validate --full
```

## Consequences

### Positive

1. **Single Source of Truth:** All Python scripts in one location
2. **Reduced Duplication:** Eliminates duplicate scripts
3. **Clear Entry Point:** Single entry point for all operations
4. **Better Organization:** Logical grouping of related functionality
5. **Easier Maintenance:** Changes only need to be made in one place
6. **Improved Discoverability:** Easier to find and understand scripts
7. **Consistent Quality:** All scripts follow same standards

### Negative

1. **Migration Effort:** Requires moving and updating scripts
2. **Breaking Changes:** Existing workflows may need updates
3. **Learning Curve:** Developers need to learn new structure
4. **Documentation:** Requires updating all documentation

### Neutral

1. **Path Changes:** Import paths may need updates
2. **CI/CD Updates:** CI/CD pipelines may need updates

## Alternatives Considered

### Alternative 1: Keep Scripts in Multiple Directories

**Description:** Maintain current structure with scripts in multiple directories

**Pros:**
- No migration effort
- No breaking changes

**Cons:**
- Continued duplication
- Confusion about which scripts to use
- Maintenance burden

**Rejected:** Too much duplication and confusion

### Alternative 2: Consolidate into scripts/ Directory

**Description:** Move all scripts to scripts/ directory

**Pros:**
- Single directory
- Familiar structure

**Cons:**
- omni_scripts/ already has good structure
- Would require restructuring omni_scripts/

**Rejected:** omni_scripts/ already has good structure

### Alternative 3: Create New Directory

**Description:** Create new directory for consolidated scripts

**Pros:**
- Clean slate
- Can design optimal structure

**Cons:**
- More migration effort
- omni_scripts/ already exists and is well-structured

**Rejected:** Unnecessary when omni_scripts/ already exists

## Related ADRs

- [ADR-008: Modular controller pattern for build operations](ADR-008-modular-controller-pattern.md)
- [ADR-009: Type hints enforcement for zero pylance errors](ADR-009-type-hints-enforcement.md)
- [ADR-025: OmniCppController.py as single entry point](ADR-025-omnicppcontroller-single-entry-point.md)

## References

- [Python Packaging Best Practices](https://packaging.python.org/en/latest/guides/)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)
- [Python Module Documentation](https://docs.python.org/3/tutorial/modules.html)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
