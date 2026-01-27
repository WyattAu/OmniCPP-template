# REQ-028: C++23 Standard Compliance (No Modules)

**Requirement ID:** REQ-028
**Title:** C++23 Standard Compliance (No Modules)
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall use C++23 standard without modules. C++23 features shall be used where appropriate, but C++ modules shall not be used due to compiler support limitations.

## Acceptance Criteria

- [ ] C++23 is the required standard
- [ ] C++23 features are used where appropriate
- [ ] C++ modules are not used
- [ ] C++23 compliance is enforced
- [ ] C++23 features are documented
- [ ] C++23 features are tested
- [ ] C++23 compatibility is verified
- [ ] C++23 migration is planned
- [ ] C++23 best practices are followed
- [ ] C++23 limitations are documented

## Priority

**Critical** - C++23 standard compliance is essential for code quality.

## Dependencies

- **REQ-010:** Compiler detection (requires C++23 support)
- **REQ-022:** CMake 4 configuration (requires C++23 support)

## Related ADRs

- None directly, but supports all C++ coding standards

## Test Cases

### Unit Tests

1. **Test C++23 Standard Enforcement**
   - **Description:** Verify C++23 standard is enforced
   - **Steps:**
     1. Check CMake configuration
     2. Verify C++23 is set as standard
     3. Verify compiler supports C++23
   - **Expected Result:** C++23 standard enforced

2. **Test C++23 Feature Usage**
   - **Description:** Verify C++23 features are used
   - **Steps:**
     1. Review code for C++23 features
     2. Verify features are used appropriately
     3. Verify features are documented
   - **Expected Result:** C++23 features used appropriately

3. **Test No C++ Modules**
   - **Description:** Verify C++ modules are not used
   - **Steps:**
     1. Search for module imports
     2. Verify no modules are found
     3. Verify headers are used instead
   - **Expected Result:** No C++ modules used

4. **Test C++23 Compatibility**
   - **Description:** Verify C++23 compatibility
   - **Steps:**
     1. Compile code with C++23
     2. Verify compilation succeeds
     3. Verify no C++23 errors
   - **Expected Result:** C++23 compatible

### Integration Tests

1. **Test Complete C++23 Workflow**
   - **Description:** Verify complete C++23 workflow works
   - **Steps:**
     1. Configure CMake with C++23
     2. Build project
     3. Verify build succeeds
   - **Expected Result:** Complete workflow succeeds

2. **Test Cross-Compiler C++23 Support**
   - **Description:** Verify C++23 works with all compilers
   - **Steps:**
     1. Build with MSVC and C++23
     2. Build with GCC and C++23
     3. Build with Clang and C++23
   - **Expected Result:** All compilers support C++23

## Implementation Notes

- Set C++23 as required standard in CMake
- Use C++23 features where appropriate
- Avoid C++ modules due to compiler support limitations
- Enforce C++23 compliance via compiler flags
- Document C++23 features used
- Test C++23 features
- Verify C++23 compatibility
- Plan C++23 migration
- Follow C++23 best practices
- Document C++23 limitations

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - C++ Standards section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
