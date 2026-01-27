# ADR-009: Type Hints Enforcement for Zero Pylance Errors

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Python Architecture

---

## Context

The OmniCPP Template project uses Python 3.11+ for build scripts and utilities. Type hints are essential for code quality, IDE support, and catching errors early. The project aims for zero Pylance errors to ensure type safety and improve developer experience.

### Current State

Python scripts have inconsistent type hints:
- Some scripts have complete type hints
- Some scripts have partial type hints
- Some scripts have no type hints
- Pylance reports numerous type errors

### Issues

1. **Type Errors:** Pylance reports numerous type errors
2. **Poor IDE Support:** Incomplete type hints reduce IDE autocomplete
3. **Runtime Errors:** Type errors that could be caught at compile time
4. **Code Quality:** Inconsistent type hints reduce code quality
5. **Maintenance:** Harder to maintain code without type hints
6. **Refactoring:** Risky refactoring without type safety

## Decision

Enforce **complete type hints** for all Python code with **zero Pylance errors** as the goal.

### 1. Type Hint Requirements

```python
# All functions must have type hints
def build_project(
    preset: str,
    target: Optional[str] = None,
    clean: bool = False
) -> BuildResult:
    """Build the project.

    Args:
        preset: CMake preset to use
        target: Target to build (None for all)
        clean: Clean before build

    Returns:
        Build result with success status and error message
    """
    pass

# All classes must have type hints
class BuildController(BaseController):
    """Controller for build operations."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize build controller.

        Args:
            logger: Logger instance
            config: Configuration dictionary
        """
        super().__init__(logger, config)

    def run(self, args: Any) -> int:
        """Run build operation.

        Args:
            args: Command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass

# All variables must have type hints
result: BuildResult = self.cmake_manager.configure(preset)
config: Dict[str, Any] = load_config()
logger: Logger = Logger(config)
```

### 2. Type Hint Standards

```python
# Use typing module for standard types
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    Callable,
    Iterator,
    Iterable,
    Sequence,
    Mapping,
    MutableMapping,
    Set,
    FrozenSet,
    TypeVar,
    Generic,
    Protocol,
    runtime_checkable,
)

# Use collections.abc for abstract base classes
from collections.abc import (
    Mapping as MappingABC,
    MutableMapping as MutableMappingABC,
    Sequence as SequenceABC,
    Iterable as IterableABC,
    Iterator as IteratorABC,
)

# Use typing_extensions for newer types
from typing_extensions import (
    Self,
    ParamSpec,
    Concatenate,
    TypeGuard,
    Never,
    Literal,
    TypedDict,
    Final,
    override,
)

# Use pathlib.Path for file paths
from pathlib import Path

# Use enum for enumerations
from enum import Enum, auto
```

### 3. Type Hint Best Practices

```python
# Use Optional for nullable types
def get_config(key: str) -> Optional[str]:
    """Get configuration value.

    Args:
        key: Configuration key

    Returns:
        Configuration value or None if not found
    """
    pass

# Use Union for multiple types
def process_value(value: Union[str, int, float]) -> str:
    """Process value.

    Args:
        value: Value to process

    Returns:
        Processed value as string
    """
    pass

# Use Literal for specific values
def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    """Set log level.

    Args:
        level: Log level
    """
    pass

# Use TypedDict for structured dictionaries
class BuildConfig(TypedDict):
    """Build configuration."""
    preset: str
    target: Optional[str]
    clean: bool
    parallel_jobs: int

def build(config: BuildConfig) -> BuildResult:
    """Build project.

    Args:
        config: Build configuration

    Returns:
        Build result
    """
    pass

# Use Protocol for duck typing
@runtime_checkable
class Logger(Protocol):
    """Logger protocol."""

    def debug(self, message: str) -> None:
        """Log debug message."""
        pass

    def info(self, message: str) -> None:
        """Log info message."""
        pass

    def warning(self, message: str) -> None:
        """Log warning message."""
        pass

    def error(self, message: str) -> None:
        """Log error message."""
        pass

def log_message(logger: Logger, level: str, message: str) -> None:
    """Log message.

    Args:
        logger: Logger instance
        level: Log level
        message: Message to log
    """
    pass

# Use TypeVar for generic types
T = TypeVar('T')

def first(items: List[T]) -> Optional[T]:
    """Get first item from list.

    Args:
        items: List of items

    Returns:
        First item or None if list is empty
    """
    return items[0] if items else None

# Use Self for return type
class Builder:
    """Builder class."""

    def add_item(self, item: str) -> Self:
        """Add item to builder.

        Args:
            item: Item to add

        Returns:
            Self for method chaining
        """
        return self
```

### 4. Type Hint Enforcement Configuration

```json
// .vscode/settings.json
{
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "error",
    "reportMissingModuleSource": "error",
    "reportUndefinedVariable": "error",
    "reportInvalidTypeVarUse": "error",
    "reportInvalidStringEscapeSequence": "error",
    "reportInvalidTypeArguments": "error",
    "reportInvalidStubStatement": "error",
    "reportInvalidTypeForm": "error",
    "reportIncompatibleMethodOverride": "error",
    "reportIncompatibleVariableOverride": "error",
    "reportIncompatibleReturnStatement": "error",
    "reportIncompatibleArgumentType": "error",
    "reportIncompatibleAssignment": "error",
    "reportPossiblyUnboundVariable": "error",
    "reportOptionalCall": "error",
    "reportOptionalMemberAccess": "error",
    "reportOptionalIterable": "error",
    "reportOptionalContextManager": "error",
    "reportOptionalOperand": "error",
    "reportOptionalSubscript": "error",
    "reportOptionalAttributeAccess": "error",
    "reportOptionalIterable": "error",
    "reportOptionalContextManager": "error",
    "reportOptionalOperand": "error",
    "reportOptionalSubscript": "error",
    "reportOptionalAttributeAccess": "error",
    "reportGeneralTypeIssues": "error",
    "reportFunctionMemberAccess": "error",
    "reportUnusedImport": "warning",
    "reportUnusedClass": "warning",
    "reportUnusedVariable": "warning",
    "reportUnusedFunction": "warning",
    "reportUnusedCoroutine": "warning",
    "reportUnusedExpression": "warning",
    "reportUnusedParameter": "warning",
    "reportUnusedCallResult": "warning",
    "reportUnusedIgnoreComment": "warning",
    "reportUnusedClass": "warning",
    "reportUnusedVariable": "warning",
    "reportUnusedFunction": "warning",
    "reportUnusedCoroutine": "warning",
    "reportUnusedExpression": "warning",
    "reportUnusedParameter": "warning",
    "reportUnusedCallResult": "warning",
    "reportUnusedIgnoreComment": "warning"
  },
  "python.analysis.stubPath": "./stubs",
  "python.analysis.extraPaths": [
    "./omni_scripts"
  ]
}
```

### 5. Type Hint Validation Script

```python
# scripts/validate_type_hints.py
#!/usr/bin/env python3
"""Validate type hints in Python files."""

import ast
import sys
from pathlib import Path
from typing import List, Tuple

def check_function_type_hints(node: ast.FunctionDef) -> List[str]:
    """Check if function has type hints.

    Args:
        node: Function definition node

    Returns:
        List of errors
    """
    errors = []

    # Check return type hint
    if node.returns is None:
        errors.append(f"Function '{node.name}' missing return type hint")

    # Check parameter type hints
    for arg in node.args.args:
        if arg.arg != 'self' and arg.annotation is None:
            errors.append(f"Function '{node.name}' parameter '{arg.arg}' missing type hint")

    return errors

def check_class_type_hints(node: ast.ClassDef) -> List[str]:
    """Check if class methods have type hints.

    Args:
        node: Class definition node

    Returns:
        List of errors
    """
    errors = []

    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            errors.extend(check_function_type_hints(item))

    return errors

def check_file_type_hints(file_path: Path) -> List[str]:
    """Check if file has type hints.

    Args:
        file_path: Path to Python file

    Returns:
        List of errors
    """
    errors = []

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                errors.extend(check_function_type_hints(node))
            elif isinstance(node, ast.ClassDef):
                errors.extend(check_class_type_hints(node))

    except Exception as e:
        errors.append(f"Error parsing {file_path}: {e}")

    return errors

def main():
    """Main validation function."""
    omni_scripts_dir = Path("omni_scripts")

    if not omni_scripts_dir.exists():
        print(f"ERROR: omni_scripts directory not found")
        return 1

    # Find all Python files
    python_files = list(omni_scripts_dir.rglob("*.py"))

    if not python_files:
        print(f"ERROR: No Python files found in {omni_scripts_dir}")
        return 1

    print(f"Found {len(python_files)} Python files")
    print()

    # Check each file
    all_errors = []
    for python_file in python_files:
        errors = check_file_type_hints(python_file)
        if errors:
            all_errors.extend([(python_file, error) for error in errors])

    # Print errors
    if all_errors:
        print("Type hint errors:")
        for file_path, error in all_errors:
            print(f"  {file_path}: {error}")
        print()
        print(f"Total errors: {len(all_errors)}")
        return 1
    else:
        print("All files have complete type hints!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 6. Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-PyYAML
        args:
          - --strict
          - --ignore-missing-imports
        files: ^omni_scripts/
```

## Consequences

### Positive

1. **Type Safety:** Catches type errors at compile time
2. **IDE Support:** Better autocomplete and navigation
3. **Code Quality:** Enforces consistent type hints
4. **Documentation:** Type hints serve as documentation
5. **Refactoring:** Safer refactoring with type safety
6. **Maintenance:** Easier to maintain code with type hints
7. **Zero Errors:** Goal of zero Pylance errors

### Negative

1. **Development Time:** Initial effort to add type hints
2. **Learning Curve:** Developers need to learn type hints
3. **Complexity:** Some type hints can be complex
4. **False Positives:** Pylance may report false positives

### Neutral

1. **Documentation:** Requires documentation for type hint standards
2. **Testing:** Need to test type hint validation

## Alternatives Considered

### Alternative 1: No Type Hints

**Description:** Continue without type hints

**Pros:**
- No initial effort
- Simpler code

**Cons:**
- No type safety
- Poor IDE support
- Runtime errors

**Rejected:** Too many runtime errors and poor IDE support

### Alternative 2: Partial Type Hints

**Description:** Add type hints only to critical functions

**Pros:**
- Less initial effort
- Type safety for critical code

**Cons:**
- Inconsistent type hints
- Partial type safety
- Still have type errors

**Rejected:** Inconsistent and partial type safety

### Alternative 3: Runtime Type Checking

**Description:** Use runtime type checking libraries

**Pros:**
- Catches type errors at runtime
- No compile-time overhead

**Cons:**
- Runtime overhead
- Doesn't catch errors early
- Performance impact

**Rejected:** Runtime overhead and doesn't catch errors early

## Related ADRs

- [ADR-007: Consolidation of Python scripts into omni_scripts/](ADR-007-python-scripts-consolidation.md)
- [ADR-008: Modular controller pattern for build operations](ADR-008-modular-controller-pattern.md)

## References

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 526 - Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 585 - Type Hinting Generics](https://peps.python.org/pep-0585/)
- [PEP 604 - Allow writing union types as X | Y](https://peps.python.org/pep-0604/)
- [PEP 613 - Explicit Type Aliases](https://peps.python.org/pep-0613/)
- [PEP 646 - Variadic Generics](https://peps.python.org/pep-0646/)
- [PEP 673 - Self Type](https://peps.python.org/pep-0673/)
- [Pylance Documentation](https://github.com/microsoft/pylance-release)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
