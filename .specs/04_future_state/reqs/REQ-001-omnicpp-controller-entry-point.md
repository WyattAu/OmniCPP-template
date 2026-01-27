# REQ-001: OmniCppController.py as Single Entry Point

**Requirement ID:** REQ-001
**Title:** OmniCppController.py as Single Entry Point
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The OmniCppController.py script shall serve as the single, unified entry point for all build system operations, consolidating functionality from scripts/, omni_scripts/, and impl/ directories. This controller shall provide a command-line interface (CLI) that dispatches to appropriate sub-controllers for specific operations.

## Acceptance Criteria

- [ ] OmniCppController.py exists at project root
- [ ] OmniCppController.py provides CLI interface with commands: configure, build, clean, install, test, package, format, lint
- [ ] All commands are dispatched to appropriate controller classes in omni_scripts/controller/
- [ ] OmniCppController.py imports only from omni_scripts/ (no imports from scripts/ or impl/)
- [ ] Command-line arguments are parsed using argparse with proper help messages
- [ ] Invalid commands display usage information and exit with non-zero status
- [ ] All commands return appropriate exit codes (0 for success, non-zero for failure)
- [ ] OmniCppController.py can be invoked with `python OmniCppController.py <command> [options]`
- [ ] OmniCppController.py supports `--help` flag to display usage information

## Priority

**Critical** - This is the foundational requirement for the refactoring effort. Without a single entry point, the consolidation cannot be completed.

## Dependencies

- **REQ-002:** Modular controller pattern implementation
- **REQ-003:** Type hints enforcement
- **REQ-008:** Command-line interface

## Related ADRs

- **ADR-001:** Multi-package manager strategy (requires unified entry point)
- **ADR-002:** Priority-based package manager selection (requires unified controller)

## Test Cases

### Unit Tests

1. **Test Entry Point Exists**
   - **Description:** Verify OmniCppController.py exists at project root
   - **Steps:**
     1. Check if OmniCppController.py exists in project root
     2. Verify file is executable
   - **Expected Result:** File exists and is executable

2. **Test CLI Interface**
   - **Description:** Verify CLI interface provides all required commands
   - **Steps:**
     1. Run `python OmniCppController.py --help`
     2. Verify all commands are listed: configure, build, clean, install, test, package, format, lint
   - **Expected Result:** All commands are displayed in help output

3. **Test Command Dispatch**
   - **Description:** Verify commands are dispatched to correct controllers
   - **Steps:**
     1. Run `python OmniCppController.py build engine debug`
     2. Verify BuildController is invoked
     3. Run `python OmniCppController.py clean`
     4. Verify CleanController is invoked
   - **Expected Result:** Correct controllers are invoked for each command

4. **Test Invalid Command**
   - **Description:** Verify invalid commands display usage and exit with error
   - **Steps:**
     1. Run `python OmniCppController.py invalid_command`
     2. Check exit code is non-zero
     3. Verify usage information is displayed
   - **Expected Result:** Usage displayed, exit code non-zero

5. **Test No Imports from Legacy Directories**
   - **Description:** Verify OmniCppController.py does not import from scripts/ or impl/
   - **Steps:**
     1. Search OmniCppController.py for imports from scripts/
     2. Search OmniCppController.py for imports from impl/
   - **Expected Result:** No imports from scripts/ or impl/ found

### Integration Tests

1. **Test Full Build Workflow**
   - **Description:** Verify complete build workflow through entry point
   - **Steps:**
     1. Run `python OmniCppController.py configure`
     2. Run `python OmniCppController.py build engine debug`
     3. Verify build completes successfully
   - **Expected Result:** Build completes with exit code 0

2. **Test All Commands**
   - **Description:** Verify all commands execute successfully
   - **Steps:**
     1. Execute each command: configure, build, clean, install, test, package, format, lint
     2. Verify each command completes successfully
   - **Expected Result:** All commands execute without errors

## Implementation Notes

- Use argparse for CLI argument parsing
- Implement command dispatcher pattern in omni_scripts/controller/dispatcher.py
- Each command should have dedicated controller class in omni_scripts/controller/
- Use proper exit codes: 0 for success, 1 for general errors, 2 for invalid arguments
- Provide comprehensive help messages for each command
- Support verbose flag for debugging

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Python Standards section
- [`.specs/00_current_state/manifest.md`](../00_current_state/manifest.md) - Current Python script locations
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
