# REQ-049: VSCode launch.json Configuration

**Requirement ID:** REQ-049
**Title:** VSCode launch.json Configuration
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall provide VSCode launch.json configuration for debugging. VSCode launch configurations shall provide convenient debugging for both Python and C++ code.

## Acceptance Criteria

- [ ] VSCode launch.json exists
- [ ] Python debug configuration is provided
- [ ] C++ debug configuration is provided
- [ ] Debug configurations are well-documented
- [ ] Debug configurations are tested
- [ ] Debug configurations support breakpoints
- [ ] Debug configurations support stepping
- [ ] Debug configurations support variable inspection
- [ ] Debug configurations are cross-platform
- [ ] Debug configurations are extensible

## Priority

**High** - VSCode launch.json configuration is important for developer experience.

## Dependencies

- **REQ-001:** OmniCppController.py as single entry point (requires debug config)
- **REQ-008:** Command-line interface (requires debug config)

## Related ADRs

- None directly, but supports all VSCode integration requirements

## Test Cases

### Unit Tests

1. **Test Python Debug Configuration**
   - **Description:** Verify Python debug configuration works
   - **Steps:**
     1. Launch Python debug from VSCode
     2. Verify debugger attaches
     3. Verify breakpoints work
   - **Expected Result:** Python debug works correctly

2. **Test C++ Debug Configuration**
   - **Description:** Verify C++ debug configuration works
   - **Steps:**
     1. Launch C++ debug from VSCode
     2. Verify debugger attaches
     3. Verify breakpoints work
   - **Expected Result:** C++ debug works correctly

3. **Test Breakpoint Support**
   - **Description:** Verify breakpoints work
   - **Steps:**
     1. Set breakpoint
     2. Launch debug
     3. Verify breakpoint hits
   - **Expected Result:** Breakpoints work correctly

4. **Test Stepping Support**
   - **Description:** Verify stepping works
   - **Steps:**
     1. Launch debug
     2. Step through code
     3. Verify stepping works
   - **Expected Result:** Stepping works correctly

5. **Test Variable Inspection**
   - **Description:** Verify variable inspection works
   - **Steps:**
     1. Launch debug
     2. Inspect variables
     3. Verify variables are displayed
   - **Expected Result:** Variable inspection works correctly

### Integration Tests

1. **Test Complete VSCode Debug Workflow**
   - **Description:** Verify complete VSCode debug workflow works
   - **Steps:**
     1. Set breakpoint
     2. Launch debug
     3. Step through code
     4. Inspect variables
   - **Expected Result:** Complete workflow succeeds

2. **Test VSCode Debug with Multiple Languages**
   - **Description:** Verify VSCode debug works with both languages
   - **Steps:**
     1. Debug Python code
     2. Debug C++ code
     3. Verify both work
   - **Expected Result:** Both languages work correctly

## Implementation Notes

- Create VSCode launch.json
- Configure Python debug
- Configure C++ debug
- Support breakpoints
- Support stepping
- Support variable inspection
- Document all configurations
- Test all configurations
- Ensure cross-platform compatibility
- Make configurations extensible

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - VSCode Integration Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
