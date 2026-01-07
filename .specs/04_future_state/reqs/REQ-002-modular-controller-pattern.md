# REQ-002: Modular Controller Pattern Implementation

**Requirement ID:** REQ-002
**Title:** Modular Controller Pattern Implementation
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall implement a modular controller pattern where each major operation (configure, build, clean, install, test, package, format, lint) has a dedicated controller class. Controllers shall inherit from a base controller class that provides common functionality such as logging, error handling, and configuration management.

## Acceptance Criteria

- [ ] Base controller class exists in omni_scripts/controller/base.py
- [ ] All controllers inherit from base controller class
- [ ] Each controller implements execute() method with consistent signature
- [ ] Controllers are organized in omni_scripts/controller/ directory
- [ ] Base controller provides common functionality:
  - [ ] Logging initialization
  - [ ] Error handling
  - [ ] Configuration loading
  - [ ] Path resolution
- [ ] Controllers are discoverable and importable from omni_scripts/controller/
- [ ] Each controller has clear single responsibility
- [ ] Controllers do not have circular dependencies

## Priority

**Critical** - Modular architecture is essential for maintainability and testability.

## Dependencies

- **REQ-001:** OmniCppController.py as single entry point (requires controllers to dispatch to)
- **REQ-003:** Type hints enforcement (requires typed controller interfaces)

## Related ADRs

- **ADR-001:** Multi-package manager strategy (requires modular controllers)
- **ADR-002:** Priority-based package manager selection (requires modular controllers)

## Test Cases

### Unit Tests

1. **Test Base Controller Exists**
   - **Description:** Verify base controller class exists and provides required methods
   - **Steps:**
     1. Import BaseController from omni_scripts/controller/base.py
     2. Verify base controller has execute() method
     3. Verify base controller has logging setup
   - **Expected Result:** Base controller exists with required methods

2. **Test Controller Inheritance**
   - **Description:** Verify all controllers inherit from base controller
   - **Steps:**
     1. Import all controllers from omni_scripts/controller/
     2. Verify each controller is subclass of BaseController
     3. Verify each controller implements execute() method
   - **Expected Result:** All controllers inherit from BaseController

3. **Test Controller Single Responsibility**
   - **Description:** Verify each controller has single, well-defined responsibility
   - **Steps:**
     1. Review BuildController - should only handle build operations
     2. Review CleanController - should only handle clean operations
     3. Review TestController - should only handle test operations
   - **Expected Result:** Each controller has single responsibility

4. **Test Controller Discoverability**
   - **Description:** Verify controllers can be discovered and imported
   - **Steps:**
     1. Attempt to import all controllers from omni_scripts/controller/
     2. Verify imports succeed without errors
   - **Expected Result:** All controllers import successfully

### Integration Tests

1. **Test Controller Dispatch**
   - **Description:** Verify dispatcher can route to correct controller
   - **Steps:**
     1. Invoke OmniCppController.py with build command
     2. Verify BuildController.execute() is called
     3. Invoke OmniCppController.py with test command
     4. Verify TestController.execute() is called
   - **Expected Result:** Dispatcher routes to correct controllers

2. **Test Controller Error Handling**
   - **Description:** Verify controllers handle errors consistently
   - **Steps:**
     1. Invoke controller with invalid arguments
     2. Verify error is caught and logged
     3. Verify appropriate exit code is returned
   - **Expected Result:** Errors handled consistently

## Implementation Notes

- Base controller should be abstract class with execute() method
- Use dependency injection for logging and configuration
- Implement common error handling in base controller
- Each controller should be in separate file
- Use factory pattern for controller instantiation
- Controllers should not directly instantiate other controllers (use dispatcher)

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Python Standards section
- [`.specs/00_current_state/manifest.md`](../00_current_state/manifest.md) - Current controller structure
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future controller structure
