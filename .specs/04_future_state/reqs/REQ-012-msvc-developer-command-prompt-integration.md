# REQ-012: MSVC Developer Command Prompt Integration

**Requirement ID:** REQ-012
**Title:** MSVC Developer Command Prompt Integration
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall integrate with MSVC Developer Command Prompt on Windows. Integration shall include automatic detection of Visual Studio installations, selection of appropriate architecture (x64, x86, ARM64), and environment setup.

## Acceptance Criteria

- [ ] MSVC Developer Command Prompt detection module exists
- [ ] Visual Studio installations are detected automatically
- [ ] Multiple Visual Studio versions are supported
- [ ] Architecture selection works (x64, x86, ARM64)
- [ ] Environment variables are set correctly
- [ ] vcvarsall.bat is invoked correctly
- [ ] MSVC compiler is accessible after setup
- [ ] MSVC-clang compiler is accessible after setup
- [ ] Detection handles missing installations gracefully
- [ ] Setup is logged for debugging

## Priority

**Critical** - MSVC integration is essential for Windows builds.

## Dependencies

- **REQ-009:** Platform detection (required for MSVC detection)
- **REQ-010:** Compiler detection (required for MSVC detection)
- **REQ-011:** Terminal invocation (required for MSVC setup)

## Related ADRs

- None directly, but supports all Windows build ADRs

## Test Cases

### Unit Tests

1. **Test Visual Studio Detection**
   - **Description:** Verify Visual Studio installations are detected
   - **Steps:**
     1. Run Visual Studio detection
     2. Verify installations are found
     3. Verify versions are detected
   - **Expected Result:** Visual Studio installations detected correctly

2. **Test Architecture Selection**
   - **Description:** Verify architecture selection works
   - **Steps:**
     1. Select x64 architecture
     2. Verify environment is set for x64
     3. Select x86 architecture
     4. Verify environment is set for x86
   - **Expected Result:** Architecture selected correctly

3. **Test vcvarsall.bat Invocation**
   - **Description:** Verify vcvarsall.bat is invoked correctly
   - **Steps:**
     1. Invoke vcvarsall.bat with architecture
     2. Verify environment is set
     3. Verify compiler is accessible
   - **Expected Result:** vcvarsall.bat invoked successfully

4. **Test Missing Installation Handling**
   - **Description:** Verify missing installations are handled gracefully
   - **Steps:**
     1. Run detection on system without Visual Studio
     2. Verify appropriate error is raised
   - **Expected Result:** Appropriate error raised

### Integration Tests

1. **Test MSVC Build**
   - **Description:** Verify MSVC build works after setup
   - **Steps:**
     1. Setup MSVC environment
     2. Configure CMake with MSVC
     3. Build project
   - **Expected Result:** Build succeeds

2. **Test MSVC-clang Build**
   - **Description:** Verify MSVC-clang build works after setup
   - **Steps:**
     1. Setup MSVC environment
     2. Configure CMake with MSVC-clang
     3. Build project
   - **Expected Result:** Build succeeds

## Implementation Notes

- Use vswhere.exe to detect Visual Studio installations
- Support Visual Studio 2019, 2022, and later
- Support x64, x86, and ARM64 architectures
- Invoke vcvarsall.bat with appropriate arguments
- Set environment variables correctly
- Provide setup_msvc_environment() function
- Provide get_msvc_installations() function
- Log setup process
- Handle missing installations gracefully
- Support custom installation paths

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Windows Build Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
