# REQ-004: Python Script Consolidation

**Requirement ID:** REQ-004
**Title:** Python Script Consolidation
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

All Python scripts from scripts/, omni_scripts/, and impl/ directories shall be consolidated into a single omni_scripts/ directory. This consolidation eliminates duplication, provides clear separation of concerns, and ensures all Python code follows consistent patterns.

## Acceptance Criteria

- [ ] All useful scripts from scripts/ are moved to omni_scripts/
- [ ] All useful scripts from impl/ are moved to omni_scripts/ or tests/
- [ ] Duplicate code is removed
- [ ] No imports from scripts/ or impl/ remain in omni_scripts/
- [ ] All scripts follow consistent naming conventions
- [ ] All scripts have complete type hints
- [ ] Directory structure matches future state manifest
- [ ] Legacy scripts/ directory is removed after consolidation
- [ ] Legacy impl/ directory is removed after consolidation
- [ ] All functionality is preserved during consolidation

## Priority

**Critical** - Consolidation is required to eliminate duplication and confusion.

## Dependencies

- **REQ-001:** OmniCppController.py as single entry point (requires consolidated scripts)
- **REQ-002:** Modular controller pattern (requires consolidated controllers)
- **REQ-003:** Type hints enforcement (requires typed consolidated code)

## Related ADRs

- **ADR-001:** Multi-package manager strategy (requires consolidated build scripts)
- **ADR-002:** Priority-based package manager selection (requires consolidated package managers)

## Test Cases

### Unit Tests

1. **Test No Legacy Imports**
   - **Description:** Verify no imports from scripts/ or impl/ in omni_scripts/
   - **Steps:**
     1. Search omni_scripts/ for imports from scripts/
     2. Search omni_scripts/ for imports from impl/
   - **Expected Result:** No imports from legacy directories found

2. **Test Directory Structure**
   - **Description:** Verify omni_scripts/ structure matches future state
   - **Steps:**
     1. List all directories in omni_scripts/
     2. Compare with future state manifest
   - **Expected Result:** Structure matches future state manifest

3. **Test Functionality Preservation**
   - **Description:** Verify all functionality is preserved
   - **Steps:**
     1. Identify all functions in legacy scripts/
     2. Verify equivalent functions exist in omni_scripts/
   - **Expected Result:** All functionality preserved

### Integration Tests

1. **Test Build Workflow**
   - **Description:** Verify build workflow works with consolidated scripts
   - **Steps:**
     1. Run build using consolidated scripts
     2. Verify build completes successfully
   - **Expected Result:** Build workflow works correctly

2. **Test All Commands**
   - **Description:** Verify all commands work with consolidated scripts
   - **Steps:**
     1. Execute each command: configure, build, clean, install, test, package, format, lint
     2. Verify each command completes successfully
   - **Expected Result:** All commands work correctly

## Implementation Notes

- Create mapping of legacy scripts to new locations
- Move scripts preserving functionality
- Update all import statements
- Remove duplicate code
- Delete legacy directories after validation
- Update documentation to reflect new structure
- Run all tests to ensure functionality is preserved

## References

- [`.specs/00_current_state/manifest.md`](../00_current_state/manifest.md) - Current script locations
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Python Standards section
