# REQ-023: Ninja Generator as Default

**Requirement ID:** REQ-023
**Title:** Ninja Generator as Default
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall use Ninja as the default CMake generator. Ninja shall be used for all builds unless explicitly overridden. Ninja provides fast parallel builds and is cross-platform.

## Acceptance Criteria

- [ ] Ninja is the default CMake generator
- [ ] Ninja is detected automatically
- [ ] Ninja is installed automatically if missing
- [ ] Ninja is used for all builds by default
- [ ] Ninja can be overridden via CLI
- [ ] Ninja parallel builds work correctly
- [ ] Ninja build performance is optimized
- [ ] Ninja is supported on all platforms
- [ ] Ninja integration is tested
- [ ] Ninja usage is logged

## Priority

**Critical** - Ninja generator is essential for build performance.

## Dependencies

- **REQ-022:** CMake 4 configuration (requires Ninja generator)

## Related ADRs

- [`.specs/02_adrs/ADR-004-cmake-4-ninja-default-generator.md`](../02_adrs/ADR-004-cmake-4-ninja-default-generator.md) - CMake 4 and Ninja generator

## Test Cases

### Unit Tests

1. **Test Ninja Detection**

   - **Description:** Verify Ninja is detected correctly
   - **Steps:**
     1. Run Ninja detection
     2. Verify Ninja is found
     3. Verify version is detected
   - **Expected Result:** Ninja detected with correct version

2. **Test Ninja Default Generator**

   - **Description:** Verify Ninja is used as default generator
   - **Steps:**
     1. Configure CMake without specifying generator
     2. Verify Ninja is used
     3. Verify build succeeds
   - **Expected Result:** Ninja used as default generator

3. **Test Ninja Override**

   - **Description:** Verify Ninja can be overridden
   - **Steps:**
     1. Configure CMake with different generator
     2. Verify specified generator is used
     3. Verify build succeeds
   - **Expected Result:** Generator overridden successfully

4. **Test Ninja Parallel Builds**
   - **Description:** Verify Ninja parallel builds work
   - **Steps:**
     1. Build with Ninja
     2. Verify parallel execution
     3. Verify build performance
   - **Expected Result:** Parallel builds work correctly

### Integration Tests

1. **Test Complete Ninja Workflow**

   - **Description:** Verify complete Ninja workflow works
   - **Steps:**
     1. Configure CMake with Ninja
     2. Build project
     3. Verify build succeeds
   - **Expected Result:** Complete workflow succeeds

2. **Test Cross-Platform Ninja Builds**
   - **Description:** Verify Ninja works on all platforms
   - **Steps:**
     1. Build on Windows with Ninja
     2. Build on Linux with Ninja
     3. Build on macOS with Ninja
   - **Expected Result:** Builds succeed on all platforms

## Implementation Notes

- Use Ninja as default CMake generator
- Detect Ninja installation automatically
- Install Ninja automatically if missing
- Support Ninja override via CLI argument
- Optimize Ninja parallel builds
- Ensure Ninja is supported on all platforms
- Provide configure_with_ninja() function
- Log Ninja usage
- Test Ninja integration
- Document Ninja configuration

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Build System Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
