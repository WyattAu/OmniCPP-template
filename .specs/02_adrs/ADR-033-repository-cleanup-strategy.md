# ADR-033: Repository Cleanup Strategy

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Repository Organization and Maintenance

---

## Context

The OmniCPP Template repository has accumulated various files and directories over time. The Linux expansion provides an opportunity to clean up and reorganize the repository to better support multi-platform development.

### Current State Issues

1. **Windows-Centric Artifacts:** Many files are Windows-specific and not relevant to Linux
2. **Duplicate Files:** Multiple test files with similar purposes
3. **Obsolete Scripts:** Old setup scripts that are no longer used
4. **Inconsistent Organization:** Files not organized logically
5. **Documentation Scattered:** Documentation spread across multiple locations
6. **Test Files in Root:** Test files ([`test_msvc.cpp`](../../test_msvc.cpp:1), [`test_mingw_gcc.cpp`](../../test_mingw_gcc.cpp:1), etc.) in project root
7. **Debug Artifacts:** Debug directory with temporary files
8. **Migration Artifacts:** Old migration files no longer needed

### Specific Files to Address

**Test Files in Root:**
- [`test_msvc.cpp`](../../test_msvc.cpp:1)
- [`test_mingw_clang.cpp`](../../test_mingw_clang.cpp:1)
- [`test_mingw_gcc.cpp`](../../test_mingw_gcc.cpp:1)

**Windows-Specific Setup Scripts:**
- [`conan/setup_clang_mingw_ucrt.bat`](../../conan/setup_clang_mingw_ucrt.bat:1)
- [`conan/setup_clang_mingw.bat`](../../conan/setup_clang_mingw.bat:1)
- [`conan/setup_clang.bat`](../../conan/setup_clang.bat:1)
- [`conan/setup_msvc.bat`](../../conan/setup_msvc.bat:1)
- [`conan/setup_gcc_mingw_ucrt.bat`](../../conan/setup_gcc_mingw_ucrt.bat:1)
- [`conan/setup_gcc_mingw.bat`](../../conan/setup_gcc_mingw.bat:1)

### Linux Expansion Requirements

The Linux expansion requires:

1. **Clean Repository:** Remove obsolete and duplicate files
2. **Logical Organization:** Organize files by purpose
3. **Platform-Specific Areas:** Separate Windows and Linux files
4. **Archive Old Files:** Keep historical files but move to archive
5. **Consistent Structure:** Follow consistent directory structure
6. **Clear Documentation:** Centralized documentation
7. **Test Organization:** Move test files to appropriate locations

## Decision

Implement a comprehensive repository cleanup strategy to organize files, remove duplicates, and archive obsolete files.

### 1. Archive Windows-Specific Scripts

Move Windows-specific setup scripts to archive:

```bash
# Create archive directory
mkdir -p .archive/windows-scripts

# Move Windows-specific setup scripts
mv conan/setup_clang_mingw_ucrt.bat .archive/windows-scripts/
mv conan/setup_clang_mingw.bat .archive/windows-scripts/
mv conan/setup_clang.bat .archive/windows-scripts/
mv conan/setup_msvc.bat .archive/windows-scripts/
mv conan/setup_gcc_mingw_ucrt.bat .archive/windows-scripts/
mv conan/setup_gcc_mingw.bat .archive/windows-scripts/
```

### 2. Move Test Files to Tests Directory

Move test files from root to tests directory:

```bash
# Create tests directory
mkdir -p tests/compiler-detection

# Move test files
mv test_msvc.cpp tests/compiler-detection/
mv test_mingw_clang.cpp tests/compiler-detection/
mv test_mingw_gcc.cpp tests/compiler-detection/

# Add Linux test files
touch tests/compiler-detection/test_linux_gcc.cpp
touch tests/compiler-detection/test_linux_clang.cpp
```

### 3. Create Linux-Specific Areas

Create Linux-specific directories:

```bash
# Create Linux-specific directories
mkdir -p scripts/linux
mkdir -p scripts/windows
```

### 4. Update .gitignore

Update [`.gitignore`](../../.gitignore:1):

```gitignore
# Archive directories
.archive/

# Build artifacts
build/
.ccache/
.conan2/
```

### 5. Create Migration Guide

Create migration guide for users explaining the changes and how to update workflows.

## Consequences

### Positive

1. **Cleaner Repository:** Remove obsolete and duplicate files
2. **Better Organization:** Logical file organization
3. **Clearer Structure:** Easier to navigate
4. **Platform Separation:** Clear separation of Windows and Linux files
5. **Historical Preservation:** Archived files kept for reference
6. **Consistent Structure:** Follow consistent directory structure
7. **Improved Onboarding:** Easier for new developers
8. **Reduced Confusion:** Less clutter in repository
9. **Better Maintenance:** Easier to maintain
10. **Professional Appearance:** More professional repository

### Negative

1. **Breaking Changes:** Users may need to update workflows
2. **Migration Effort:** Users need to migrate to new structure
3. **Documentation Updates:** Need to update all documentation
4. **Script Updates:** Need to update build scripts
5. **CI/CD Updates:** Need to update CI/CD pipelines
6. **Potential Issues:** May break existing workflows
7. **User Confusion:** Users may be confused by changes
8. **Rollback Complexity:** Harder to rollback if issues arise

### Neutral

1. **Git History:** Changes will be in git history
2. **Archive Size:** Archive directory will grow over time
3. **Migration Guide:** Need to create migration guide
4. **Communication:** Need to communicate changes to users

## Alternatives Considered

### Alternative 1: No Cleanup

**Description:** Keep repository as-is, don't clean up

**Pros:**
- No breaking changes
- No migration effort
- No user confusion

**Cons:**
- Repository remains messy
- Harder to navigate
- Duplicate files remain
- Confusing for new developers
- Unprofessional appearance

**Rejected:** Repository remains messy, poor developer experience

### Alternative 2: Delete Obsolete Files

**Description:** Delete obsolete files instead of archiving

**Pros:**
- Cleaner repository
- Smaller repository size
- No archive directory

**Cons:**
- Lose historical reference
- Can't rollback easily
- May break existing workflows
- Users may complain

**Rejected:** Lose historical reference, can't rollback

### Alternative 3: Gradual Cleanup

**Description:** Clean up gradually over time

**Pros:**
- Less breaking changes at once
- Easier to manage
- Can test changes

**Cons:**
- Takes longer
- Repository remains messy longer
- More git commits
- Harder to track progress

**Rejected:** Takes too long, repository remains messy

## Related ADRs

- [ADR-007: Consolidation of Python scripts into omni_scripts/](ADR-007-python-scripts-consolidation.md)
- [ADR-035: Linux Setup Script Architecture](ADR-035-linux-setup-script-architecture.md)

## Threat Model References

- **TM-LX-006: Repository Security** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - Sensitive data in archived files
  - Credentials in old scripts
  - Secrets in debug artifacts
  - Mitigation: Review archived files for sensitive data, use git-secrets, scan for credentials

## References

- [Git Best Practices](https://sethrobertson.github.io/git-best-practices/)
- [Repository Structure Guidelines](https://github.com/goldbergyoni/nodebestpractices)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
