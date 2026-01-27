# REQ-017: vcpkg Integration

**Requirement ID:** REQ-017
**Title:** vcpkg Integration
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall integrate with vcpkg package manager for C++ dependency management. Integration shall include automatic detection, triplet management, dependency installation, and CMake integration.

## Acceptance Criteria

- [ ] vcpkg integration module exists in omni_scripts/build_system/vcpkg.py
- [ ] vcpkg installation is detected automatically
- [ ] vcpkg triplets are managed
- [ ] Dependencies are installed automatically
- [ ] vcpkg toolchain is generated
- [ ] CMake integration works via vcpkg toolchain file
- [ ] Multiple triplets are supported (x64-windows, x64-linux, etc.)
- [ ] vcpkg cache is managed efficiently
- [ ] Integration handles missing vcpkg gracefully
- [ ] vcpkg operations are logged

## Priority

**High** - vcpkg integration is important for dependency management.

## Dependencies

- **REQ-019:** Priority-based package manager selection (vcpkg is one option)
- **REQ-022:** CMake 4 configuration (required for vcpkg integration)

## Related ADRs

- [`.specs/02_adrs/ADR-001-multi-package-manager-strategy.md`](../02_adrs/ADR-001-multi-package-manager-strategy.md) - Multi-package manager strategy
- [`.specs/02_adrs/ADR-002-priority-based-package-manager-selection.md`](../02_adrs/ADR-002-priority-based-package-manager-selection.md) - Priority-based selection
- [`.specs/02_adrs/ADR-003-package-security-verification-approach.md`](../02_adrs/ADR-003-package-security-verification-approach.md) - Security verification

## Test Cases

### Unit Tests

1. **Test vcpkg Detection**
   - **Description:** Verify vcpkg is detected correctly
   - **Steps:**
     1. Run vcpkg detection
     2. Verify vcpkg is found
     3. Verify version is detected
   - **Expected Result:** vcpkg detected with correct version

2. **Test Triplet Management**
   - **Description:** Verify vcpkg triplets are managed correctly
   - **Steps:**
     1. Select vcpkg triplet
     2. Verify triplet is used
     3. Verify triplet is valid
   - **Expected Result:** Triplet managed correctly

3. **Test Dependency Installation**
   - **Description:** Verify dependencies are installed correctly
   - **Steps:**
     1. Install dependency via vcpkg
     2. Verify dependency is installed
     3. Verify dependency is available
   - **Expected Result:** Dependency installed successfully

4. **Test Toolchain Generation**
   - **Description:** Verify vcpkg toolchain is generated
   - **Steps:**
     1. Generate vcpkg toolchain
     2. Verify toolchain file is created
     3. Verify toolchain is valid
   - **Expected Result:** Toolchain generated successfully

5. **Test Missing vcpkg Handling**
   - **Description:** Verify missing vcpkg is handled gracefully
   - **Steps:**
     1. Run vcpkg integration without vcpkg installed
     2. Verify appropriate error is raised
   - **Expected Result:** Appropriate error raised

### Integration Tests

1. **Test Complete vcpkg Workflow**
   - **Description:** Verify complete vcpkg workflow works
   - **Steps:**
     1. Detect vcpkg
     2. Install dependencies
     3. Generate toolchain
     4. Configure CMake with toolchain
     5. Build project
   - **Expected Result:** Complete workflow succeeds

2. **Test Multi-Triplet Build**
   - **Description:** Verify multi-triplet builds work
   - **Steps:**
     1. Build with x64-windows triplet
     2. Build with x64-linux triplet
     3. Verify both builds succeed
   - **Expected Result:** Both builds succeed

## Implementation Notes

- Detect vcpkg installation via vcpkg version
- Manage vcpkg triplets
- Use vcpkg install to install dependencies
- Generate vcpkg toolchain file for CMake integration
- Support multiple triplets (x64-windows, x64-linux, etc.)
- Manage vcpkg cache efficiently
- Provide install_vcpkg_dependencies() function
- Provide generate_vcpkg_toolchain() function
- Log vcpkg operations
- Handle missing vcpkg gracefully
- Support custom vcpkg configurations

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Package Manager Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
