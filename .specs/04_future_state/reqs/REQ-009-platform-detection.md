# REQ-009: Platform Detection

**Requirement ID:** REQ-009
**Title:** Platform Detection
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall detect the current platform (Windows, Linux, macOS, WASM) and architecture (x86_64, ARM64) automatically. Platform detection shall be used to determine appropriate compilers, build tools, and configuration options.

## Acceptance Criteria

- [ ] Platform detection module exists in omni_scripts/platform/detector.py
- [ ] Platform enum defines all supported platforms (WINDOWS, LINUX, MACOS, WASM)
- [ ] Architecture enum defines all supported architectures (X86_64, ARM64)
- [ ] Platform is detected automatically using sys.platform
- [ ] Architecture is detected automatically using platform.machine()
- [ ] Detection is cached to avoid repeated system calls
- [ ] Platform detection is available to all components
- [ ] Detection handles edge cases (unknown platforms, architectures)
- [ ] Platform information is logged at startup

## Priority

**Critical** - Platform detection is foundational for cross-platform support.

## Dependencies

- **REQ-010:** Compiler detection (requires platform information)
- **REQ-011:** Terminal invocation (requires platform information)

## Related ADRs

- None directly, but supports all cross-platform ADRs

## Test Cases

### Unit Tests

1. **Test Platform Detection**
   - **Description:** Verify platform is detected correctly
   - **Steps:**
     1. Run platform detection on Windows
     2. Run platform detection on Linux
     3. Run platform detection on macOS
   - **Expected Result:** Correct platform detected for each OS

2. **Test Architecture Detection**
   - **Description:** Verify architecture is detected correctly
   - **Steps:**
     1. Run architecture detection on x86_64 system
     2. Run architecture detection on ARM64 system
   - **Expected Result:** Correct architecture detected

3. **Test Detection Caching**
   - **Description:** Verify detection results are cached
   - **Steps:**
     1. Call platform detection multiple times
     2. Verify cached value is returned
   - **Expected Result:** Cached value returned on subsequent calls

4. **Test Edge Cases**
   - **Description:** Verify edge cases are handled
   - **Steps:**
     1. Test with unknown platform
     2. Test with unknown architecture
   - **Expected Result:** Appropriate error raised or default used

### Integration Tests

1. **Test Cross-Platform Build**
   - **Description:** Verify builds work on all platforms
   - **Steps:**
     1. Build on Windows with MSVC
     2. Build on Linux with GCC
     3. Build on macOS with Clang
   - **Expected Result:** Builds succeed on all platforms

2. **Test Platform-Specific Configuration**
   - **Description:** Verify platform-specific configuration is applied
   - **Steps:**
     1. Build on Windows
     2. Verify Windows-specific settings are applied
     3. Build on Linux
     4. Verify Linux-specific settings are applied
   - **Expected Result:** Platform-specific configuration applied correctly

## Implementation Notes

- Use sys.platform for OS detection
- Use platform.machine() for architecture detection
- Implement caching to avoid repeated system calls
- Define Platform and Architecture enums
- Provide get_platform() and get_architecture() functions
- Log platform detection at startup
- Handle unknown platforms gracefully
- Support WASM as special platform case

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Cross-Platform Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
