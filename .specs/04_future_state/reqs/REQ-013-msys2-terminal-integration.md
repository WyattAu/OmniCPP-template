# REQ-013: MSYS2 Terminal Integration

**Requirement ID:** REQ-013
**Title:** MSYS2 Terminal Integration
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall integrate with MSYS2 terminal on Windows for MinGW compiler support. Integration shall include automatic detection of MSYS2 installations, selection of appropriate MinGW environment (UCRT, MSVCRT), and environment setup.

## Acceptance Criteria

- [ ] MSYS2 terminal detection module exists
- [ ] MSYS2 installations are detected automatically
- [ ] MinGW environments are detected (UCRT, MSVCRT)
- [ ] MSYS2 terminal is invoked correctly
- [ ] Environment variables are set correctly
- [ ] MinGW-GCC compiler is accessible after setup
- [ ] MinGW-clang compiler is accessible after setup
- [ ] Detection handles missing installations gracefully
- [ ] Setup is logged for debugging
- [ ] Multiple MSYS2 installations are supported

## Priority

**High** - MSYS2 integration is important for MinGW builds on Windows.

## Dependencies

- **REQ-009:** Platform detection (required for MSYS2 detection)
- **REQ-010:** Compiler detection (required for MinGW detection)
- **REQ-011:** Terminal invocation (required for MSYS2 setup)

## Related ADRs

- None directly, but supports all MinGW build ADRs

## Test Cases

### Unit Tests

1. **Test MSYS2 Detection**
   - **Description:** Verify MSYS2 installations are detected
   - **Steps:**
     1. Run MSYS2 detection
     2. Verify installations are found
     3. Verify paths are correct
   - **Expected Result:** MSYS2 installations detected correctly

2. **Test MinGW Environment Detection**
   - **Description:** Verify MinGW environments are detected
   - **Steps:**
     1. Detect UCRT environment
     2. Detect MSVCRT environment
     3. Verify compilers are found
   - **Expected Result:** MinGW environments detected correctly

3. **Test MSYS2 Terminal Invocation**
   - **Description:** Verify MSYS2 terminal is invoked correctly
   - **Steps:**
     1. Invoke MSYS2 terminal
     2. Verify environment is set
     3. Verify compiler is accessible
   - **Expected Result:** MSYS2 terminal invoked successfully

4. **Test Missing Installation Handling**
   - **Description:** Verify missing installations are handled gracefully
   - **Steps:**
     1. Run detection on system without MSYS2
     2. Verify appropriate error is raised
   - **Expected Result:** Appropriate error raised

### Integration Tests

1. **Test MinGW-GCC Build**
   - **Description:** Verify MinGW-GCC build works after setup
   - **Steps:**
     1. Setup MSYS2 environment
     2. Configure CMake with MinGW-GCC
     3. Build project
   - **Expected Result:** Build succeeds

2. **Test MinGW-clang Build**
   - **Description:** Verify MinGW-clang build works after setup
   - **Steps:**
     1. Setup MSYS2 environment
     2. Configure CMake with MinGW-clang
     3. Build project
   - **Expected Result:** Build succeeds

## Implementation Notes

- Detect MSYS2 installation from registry or common paths
- Support UCRT and MSVCRT environments
- Invoke MSYS2 shell with appropriate environment
- Set environment variables correctly
- Provide setup_msys2_environment() function
- Provide get_msys2_installations() function
- Log setup process
- Handle missing installations gracefully
- Support custom installation paths
- Support both 32-bit and 64-bit environments

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - MinGW Build Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
