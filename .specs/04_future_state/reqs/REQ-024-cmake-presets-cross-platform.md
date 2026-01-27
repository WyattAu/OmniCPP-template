# REQ-024: CMake Presets for Cross-Platform Builds

**Requirement ID:** REQ-024
**Title:** CMake Presets for Cross-Platform Builds
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall use CMake Presets for cross-platform build configuration. CMake Presets shall provide pre-configured build settings for different platforms, compilers, and configurations.

## Acceptance Criteria

- [ ] CMakePresets.json exists
- [ ] CMakeUserPresets.json exists
- [ ] Presets are defined for all platforms (Windows, Linux, macOS)
- [ ] Presets are defined for all compilers (MSVC, GCC, Clang)
- [ ] Presets are defined for all configurations (Debug, Release)
- [ ] Presets are defined for cross-compilation targets
- [ ] Presets are well-documented
- [ ] Presets are tested
- [ ] Presets can be selected via CLI
- [ ] Presets are extensible

## Priority

**High** - CMake Presets are important for cross-platform build configuration.

## Dependencies

- **REQ-022:** CMake 4 configuration (requires CMake Presets)
- **REQ-023:** Ninja generator as default (Ninja is used in presets)

## Related ADRs

- [`.specs/02_adrs/ADR-004-cmake-4-ninja-default-generator.md`](../02_adrs/ADR-004-cmake-4-ninja-default-generator.md) - CMake 4 and Ninja generator

## Test Cases

### Unit Tests

1. **Test Preset Definition**
   - **Description:** Verify presets are defined correctly
   - **Steps:**
     1. Review CMakePresets.json
     2. Verify all platforms are defined
     3. Verify all compilers are defined
   - **Expected Result:** All presets defined correctly

2. **Test Preset Selection**
   - **Description:** Verify presets can be selected
   - **Steps:**
     1. Select preset via CLI
     2. Verify preset is used
     3. Verify configuration is correct
   - **Expected Result:** Preset selected successfully

3. **Test Preset Validation**
   - **Description:** Verify presets are valid
   - **Steps:**
     1. Validate CMakePresets.json
     2. Verify no errors
     3. Verify all presets are valid
   - **Expected Result:** All presets valid

4. **Test Preset Extensibility**
   - **Description:** Verify presets are extensible
   - **Steps:**
     1. Add custom preset
     2. Verify preset works
     3. Verify preset is used
   - **Expected Result:** Preset extended successfully

### Integration Tests

1. **Test Complete Preset Workflow**
   - **Description:** Verify complete preset workflow works
   - **Steps:**
     1. Select preset
     2. Configure CMake
     3. Build project
     4. Verify build succeeds
   - **Expected Result:** Complete workflow succeeds

2. **Test Cross-Platform Presets**
   - **Description:** Verify presets work on all platforms
   - **Steps:**
     1. Use Windows preset on Windows
     2. Use Linux preset on Linux
     3. Use macOS preset on macOS
   - **Expected Result:** All presets work correctly

## Implementation Notes

- Define CMakePresets.json with all presets
- Define CMakeUserPresets.json for user-specific presets
- Include presets for all platforms (Windows, Linux, macOS)
- Include presets for all compilers (MSVC, GCC, Clang)
- Include presets for all configurations (Debug, Release)
- Include presets for cross-compilation targets
- Document all presets
- Test all presets
- Support preset selection via CLI
- Make presets extensible

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - CMake Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
