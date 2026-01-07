# REQ-003: Type Hints Enforcement

**Requirement ID:** REQ-003
**Title:** Type Hints Enforcement (Zero Pylance Errors)
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

All Python code in the omni_scripts/ directory shall have complete type hints and pass strict type checking with zero Pylance errors. This includes all functions, classes, methods, and variables having proper type annotations.

## Acceptance Criteria

- [ ] All functions have complete type hints for parameters and return values
- [ ] All classes have type hints for all attributes
- [ ] All methods have complete type hints
- [ ] No use of `Any` type unless absolutely necessary
- [ ] All imports are properly typed
- [ ] No circular dependencies between modules
- [ ] All code passes mypy strict mode with zero errors
- [ ] All code passes Pylance type checking with zero errors
- [ ] Type hints use modern Python 3.11+ syntax (e.g., `list[str]` instead of `List[str]`)
- [ ] Optional types are used correctly for nullable values
- [ ] Union types are used correctly for multiple possible types
- [ ] Type aliases are defined for complex types

## Priority

**Critical** - Zero Pylance errors is a core requirement from coding standards.

## Dependencies

- **REQ-002:** Modular controller pattern (requires typed interfaces)
- **REQ-001:** OmniCppController.py as single entry point (requires typed entry point)

## Related ADRs

- None directly, but supports all ADRs by ensuring type safety

## Test Cases

### Unit Tests

1. **Test Type Hints Coverage**

   - **Description:** Verify all functions have type hints
   - **Steps:**
     1. Run mypy strict mode on omni_scripts/
     2. Check for missing type hints
     3. Verify no errors reported
   - **Expected Result:** Zero mypy errors

2. **Test No Any Types**

   - **Description:** Verify no unnecessary use of Any type
   - **Steps:**
     1. Search omni_scripts/ for `: Any` type hints
     2. Review each occurrence
     3. Verify Any is only used when absolutely necessary
   - **Expected Result:** Minimal or no Any types found

3. **Test Modern Type Syntax**

   - **Description:** Verify modern Python 3.11+ type syntax is used
   - **Steps:**
     1. Search for `List[`, `Dict[`, `Tuple[` type hints
     2. Verify they can be replaced with `list[`, `dict[`, `tuple[`
     3. Update to modern syntax where appropriate
   - **Expected Result:** Modern type syntax used throughout

4. **Test Optional Types**
   - **Description:** Verify Optional types are used correctly
   - **Steps:**
     1. Search for nullable parameters
     2. Verify they use `Optional[T]` type hint
     3. Verify proper None checking
   - **Expected Result:** Optional types used correctly

### Integration Tests

1. **Test Pylance Validation**

   - **Description:** Verify Pylance reports zero type errors
   - **Steps:**
     1. Open project in VSCode
     2. Wait for Pylance to analyze all files
     3. Check Problems panel for type errors
   - **Expected Result:** Zero Pylance type errors

2. **Test Import Type Safety**
   - **Description:** Verify all imports are properly typed
   - **Steps:**
     1. Import all omni_scripts modules
     2. Verify no import errors
     3. Verify type hints are available for imported modules
   - **Expected Result:** All imports work correctly with type hints

## Implementation Notes

- Use `from __future__ import annotations` at top of all files
- Define type aliases for complex types in module-level
- Use `Optional[T]` for nullable values
- Use `Union[T1, T2]` for multiple possible types
- Avoid `Any` unless absolutely necessary (e.g., for dynamic data)
- Use `TypeAlias` for complex type definitions
- Ensure all public APIs have complete type hints
- Use strict mypy mode in CI/CD pipeline
- Configure Pylance to use strict type checking

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Python Standards section, Zero Pylance Errors requirement
- [`.specs/00_current_state/manifest.md`](../00_current_state/manifest.md) - Current Python type hint status
