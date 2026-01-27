# REQ-010: Compiler Detection

**Requirement ID:** REQ-010
**Title:** Compiler Detection
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall detect available compilers (MSVC, MSVC-clang, MinGW-GCC, MinGW-clang, GCC, Clang) automatically. Compiler detection shall include version detection, capability detection, and availability verification.

## Acceptance Criteria

- [ ] Compiler detection module exists in omni_scripts/compilers/detector.py
- [ ] Compiler enum defines all supported compilers
- [ ] MSVC detection works on Windows
- [ ] MSVC-clang detection works on Windows
- [ ] MinGW-GCC detection works on Windows
- [ ] MinGW-clang detection works on Windows
- [ ] GCC detection works on Linux
- [ ] Clang detection works on Linux and macOS
- [ ] Version detection works for all compilers
- [ ] Capability detection works for all compilers
- [ ] Detection is cached to avoid repeated system calls
- [ ] Detection results are logged

## Priority

**Critical** - Compiler detection is essential for build system operation.

## Dependencies

- **REQ-009:** Platform detection (required for compiler detection)
- **REQ-011:** Terminal invocation (required for compiler detection)

## Related ADRs

- None directly, but supports all compiler-related ADRs

## Test Cases

### Unit Tests

1. **Test MSVC Detection**
   - **Description:** Verify MSVC is detected correctly
   - **Steps:**
     1. Run compiler detection on Windows with MSVC installed
     2. Verify MSVC is detected
     3. Verify version is detected
   - **Expected Result:** MSVC detected with correct version

2. **Test GCC Detection**
   - **Description:** Verify GCC is detected correctly
   - **Steps:**
     1. Run compiler detection on Linux with GCC installed
     2. Verify GCC is detected
     3. Verify version is detected
   - **Expected Result:** GCC detected with correct version

3. **Test Clang Detection**
   - **Description:** Verify Clang is detected correctly
   - **Steps:**
     1. Run compiler detection on Linux with Clang installed
     2. Verify Clang is detected
     3. Verify version is detected
   - **Expected Result:** Clang detected with correct version

4. **Test MinGW Detection**
   - **Description:** Verify MinGW compilers are detected correctly
   - **Steps:**
     1. Run compiler detection on Windows with MinGW installed
     2. Verify MinGW-GCC is detected
     3. Verify MinGW-clang is detected
   - **Expected Result:** MinGW compilers detected correctly

5. **Test Detection Caching**
   - **Description:** Verify detection results are cached
   - **Steps:**
     1. Call compiler detection multiple times
     2. Verify cached value is returned
   - **Expected Result:** Cached value returned on subsequent calls

### Integration Tests

1. **Test Multi-Compiler Environment**
   - **Description:** Verify detection works with multiple compilers
   - **Steps:**
     1. Install multiple compilers on system
     2. Run compiler detection
     3. Verify all compilers are detected
   - **Expected Result:** All compilers detected correctly

2. **Test Compiler Selection**
   - **Description:** Verify compiler can be selected from detected list
   - **Steps:**
     1. Detect available compilers
     2. Select specific compiler
     3. Verify selection works
   - **Expected Result:** Compiler selected successfully

## Implementation Notes

- Use subprocess to invoke compilers for detection
- Parse compiler version output
- Test compiler capabilities with simple compilation
- Implement caching to avoid repeated detection
- Define Compiler enum with all supported compilers
- Provide get_available_compilers() function
- Provide get_compiler_version() function
- Log detection results
- Handle missing compilers gracefully
- Support compiler aliases (e.g., clang++ for Clang)

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Compiler Support section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
