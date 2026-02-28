# REQ-007: Repository Cleanup

**Requirement ID:** REQ-007
**Title:** Repository Cleanup
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

Repository cleanup shall be performed to archive Windows-specific scripts, reorganize test files, remove duplicate files, and update documentation.

### Overview

The system shall:
1. Archive Windows-specific scripts
2. Reorganize test files
3. Remove duplicate files
4. Update documentation

---

## REQ-007-001: Archive Windows-Specific Scripts

### Description

Windows-specific scripts shall be archived to an `archive/` directory to reduce repository clutter.

### Functional Requirements

The system shall:
1. Create `archive/` directory
2. Move Windows-specific setup scripts to `archive/windows/`
3. Move Windows-specific test scripts to `archive/windows/`
4. Create README in `archive/windows/` explaining archived scripts
5. Update [`README.md`](../../README.md:1) to reference archived scripts
6. Add `.gitignore` entry for `archive/` directory
7. Document why scripts were archived
8. Provide instructions for restoring scripts if needed

### Acceptance Criteria

- [ ] `archive/` directory exists
- [ ] Windows-specific setup scripts are archived
- [ ] Windows-specific test scripts are archived
- [ ] README exists in `archive/windows/`
- [ ] [`README.md`](../../README.md:1) references archived scripts
- [ ] `.gitignore` includes `archive/` entry
- [ ] Archival reason is documented
- [ ] Restoration instructions are provided

### Priority

**Low** - Archiving Windows scripts improves repository organization.

### Dependencies

- None

### Related ADRs

- [ADR-033: Repository Cleanup Strategy](../02_adrs/ADR-033-repository-cleanup-strategy.md)

### Related Threats

- None directly

### Test Cases

#### Review Tests

1. **Test Windows Scripts Archived**
   - **Description:** Verify Windows scripts are archived
   - **Steps:**
     1. Check `archive/windows/` directory
     2. Verify Windows scripts are present
     3. Verify README exists
     4. Verify [`README.md`](../../README.md:1) references archive
   - **Expected Result:** Windows scripts are archived

---

## REQ-007-002: Reorganize Test Files

### Description

Test files shall be reorganized into logical structure for better maintainability.

### Functional Requirements

The system shall:
1. Create `tests/` directory
2. Move C++ test files to `tests/cpp/`
3. Move Python test files to `tests/python/`
4. Move integration test files to `tests/integration/`
5. Create README in `tests/` explaining test structure
6. Update test documentation
7. Update CI/CD configuration for new test locations
8. Ensure all tests are still discoverable

### Acceptance Criteria

- [ ] `tests/` directory exists
- [ ] C++ test files are in `tests/cpp/`
- [ ] Python test files are in `tests/python/`
- [ ] Integration test files are in `tests/integration/`
- [ ] README exists in `tests/`
- [ ] Test documentation is updated
- [ ] CI/CD configuration is updated
- [ ] All tests are discoverable

### Priority

**Low** - Reorganizing test files improves maintainability.

### Dependencies

- None

### Related ADRs

- [ADR-033: Repository Cleanup Strategy](../02_adrs/ADR-033-repository-cleanup-strategy.md)

### Related Threats

- None directly

### Test Cases

#### Review Tests

1. **Test Files Reorganized**
   - **Description:** Verify test files are reorganized
   - **Steps:**
     1. Check `tests/` directory structure
     2. Verify C++ tests are in `tests/cpp/`
     3. Verify Python tests are in `tests/python/`
     4. Verify integration tests are in `tests/integration/`
     5. Verify README exists
   - **Expected Result:** Test files are reorganized

---

## REQ-007-003: Remove Duplicate Files

### Description

Duplicate files shall be identified and removed to reduce repository clutter.

### Functional Requirements

The system shall:
1. Identify duplicate files across repository
2. Compare file contents to confirm duplicates
3. Remove duplicate files
4. Keep the most recent or most complete version
5. Document which files were removed and why
6. Update any references to removed files
7. Verify no broken references remain

### Acceptance Criteria

- [ ] Duplicate files are identified
- [ ] File contents are compared
- [ ] Duplicate files are removed
- [ ] Most recent version is kept
- [ ] Removal is documented
- [ ] References are updated
- [ ] No broken references remain

### Priority

**Low** - Removing duplicate files reduces repository clutter.

### Dependencies

- None

### Related ADRs

- [ADR-033: Repository Cleanup Strategy](../02_adrs/ADR-033-repository-cleanup-strategy.md)

### Related Threats

- None directly

### Test Cases

#### Review Tests

1. **Test Duplicate Files Removed**
   - **Description:** Verify duplicate files are removed
   - **Steps:**
     1. Check repository for duplicate files
     2. Verify duplicates are removed
     3. Verify documentation exists
     4. Verify no broken references
   - **Expected Result:** Duplicate files are removed

---

## REQ-007-004: Update Documentation

### Description

Documentation shall be updated to reflect repository cleanup and new structure.

### Functional Requirements

The system shall:
1. Update [`README.md`](../../README.md:1) with new repository structure
2. Update [`docs/index.md`](../../docs/index.md:1) with new structure
3. Update getting started guides
4. Update developer guides
5. Update troubleshooting guides
6. Update all references to moved files
7. Add section about archived Windows scripts
8. Add section about new test structure
9. Verify all links are valid
10. Verify all examples work

### Acceptance Criteria

- [ ] [`README.md`](../../README.md:1) is updated
- [ ] [`docs/index.md`](../../docs/index.md:1) is updated
- [ ] Getting started guides are updated
- [ ] Developer guides are updated
- [ ] Troubleshooting guides are updated
- [ ] References to moved files are updated
- [ ] Archived scripts section exists
- [ ] New test structure section exists
- [ ] All links are valid
- [ ] All examples work

### Priority

**Low** - Updating documentation ensures consistency.

### Dependencies

- REQ-007-001: Archive Windows-specific scripts
- REQ-007-002: Reorganize test files
- REQ-007-003: Remove duplicate files

### Related ADRs

- [ADR-033: Repository Cleanup Strategy](../02_adrs/ADR-033-repository-cleanup-strategy.md)

### Related Threats

- None directly

### Test Cases

#### Review Tests

1. **Test Documentation Updated**
   - **Description:** Verify documentation is updated
   - **Steps:**
     1. Read [`README.md`](../../README.md:1)
     2. Read [`docs/index.md`](../../docs/index.md:1)
     3. Verify all sections are updated
     4. Verify all links are valid
     5. Verify examples work
   - **Expected Result:** Documentation is updated

---

## Implementation Notes

### Repository Structure After Cleanup

```
OmniCPP-template/
├── archive/                    # Archived files
│   └── windows/               # Windows-specific scripts
│       ├── setup_msvc.bat
│       ├── setup_mingw.bat
│       └── README.md
├── tests/                       # Test files
│   ├── cpp/                   # C++ tests
│   │   ├── test_engine.cpp
│   │   └── test_game.cpp
│   ├── python/                 # Python tests
│   │   ├── test_controller.py
│   │   └── test_build.py
│   └── integration/             # Integration tests
│       ├── test_full_build.py
│       └── test_cross_platform.py
├── scripts/                     # Setup scripts
│   ├── setup_gcc.sh
│   ├── setup_clang.sh
│   ├── setup_cachyos.sh
│   ├── setup_nix.sh
│   ├── setup_qt6_vulkan.sh
│   └── validate_environment.sh
├── conan/                       # Conan configuration
│   └── profiles/              # Conan profiles
│       ├── gcc-linux
│       ├── gcc-linux-debug
│       ├── clang-linux
│       ├── clang-linux-debug
│       ├── cachyos
│       ├── cachyos-debug
│       ├── cachyos-clang
│       └── cachyos-clang-debug
├── docs/                        # Documentation
│   ├── nix-development.md
│   ├── cachyos-builds.md
│   ├── linux-troubleshooting.md
│   ├── conan-linux-profiles.md
│   └── vscode-linux-setup.md
└── ... (rest of repository)
```

### Archive README Template

```markdown
# Archived Windows Scripts

This directory contains Windows-specific scripts that have been archived as part of the Linux expansion effort.

## Why Archived?

These scripts were archived to:
1. Reduce repository clutter
2. Focus on Linux as primary development platform
3. Simplify repository structure
4. Improve maintainability

## Restoring Scripts

To restore these scripts:
1. Copy scripts from `archive/windows/` back to root directory
2. Update [`README.md`](../../README.md:1) to reference restored scripts
3. Update CI/CD configuration if needed

## Scripts

### Setup Scripts

- `setup_msvc.bat` - MSVC compiler setup
- `setup_mingw.bat` - MinGW compiler setup

### Test Scripts

- `test_msvc.cpp` - MSVC compilation test
- `test_mingw_gcc.cpp` - MinGW GCC compilation test
- `test_mingw_clang.cpp` - MinGW Clang compilation test

## Notes

- These scripts are still functional
- They can be restored if needed
- Documentation for these scripts is in the original repository
```

### Tests README Template

```markdown
# Test Files

This directory contains all test files for the OmniCPP Template project.

## Structure

### C++ Tests (`tests/cpp/`)

C++ unit tests and integration tests.

- `test_engine.cpp` - Engine unit tests
- `test_game.cpp` - Game unit tests

### Python Tests (`tests/python/`)

Python unit tests for build system and utilities.

- `test_controller.py` - OmniCppController tests
- `test_build.py` - Build system tests

### Integration Tests (`tests/integration/`)

Integration tests for full build pipeline.

- `test_full_build.py` - Full build pipeline test
- `test_cross_platform.py` - Cross-platform build test

## Running Tests

### C++ Tests

```bash
cd build
ctest --output-on-failure
```

### Python Tests

```bash
pytest tests/python/
```

### Integration Tests

```bash
pytest tests/integration/
```

## Notes

- All tests are discoverable by CI/CD
- Test documentation is in respective test files
- Add new tests to appropriate subdirectory
```

### Documentation Updates

Update [`README.md`](../../README.md:1) with:

```markdown
## Repository Structure

```
OmniCPP-template/
├── archive/                    # Archived Windows scripts
├── tests/                       # Test files
│   ├── cpp/                   # C++ tests
│   ├── python/                 # Python tests
│   └── integration/             # Integration tests
├── scripts/                     # Setup scripts
├── conan/                       # Conan configuration
├── docs/                        # Documentation
└── ... (rest of repository)
```

## Archived Files

Windows-specific scripts have been archived to `archive/windows/`. See [archive/windows/README.md](archive/windows/README.md) for details.

## Test Structure

Test files have been reorganized into `tests/` directory. See [tests/README.md](tests/README.md) for details.
```

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-033: Repository Cleanup Strategy](../02_adrs/ADR-033-repository-cleanup-strategy.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
