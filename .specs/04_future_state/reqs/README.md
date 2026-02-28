# Functional Requirements Index

This document provides an index of all functional requirements for the OmniCPP Template refactoring project.

## Requirements Overview

Total Requirements: 64

### Linux Expansion Requirements (REQ-001 to REQ-008)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-001](REQ-001-omnicppcontroller-linux-support.md) | OmniCppController.py Linux Support | Critical | Draft |
| [REQ-002](REQ-002-flake-nix-enhancement.md) | flake.nix Enhancement | Critical | Draft |
| [REQ-003](REQ-003-vscode-configuration.md) | VSCode Configuration | High | Draft |
| [REQ-004](REQ-004-conan-profiles.md) | Conan Profiles | High | Draft |
| [REQ-005](REQ-005-setup-scripts.md) | Setup Scripts | High | Draft |
| [REQ-006](REQ-006-documentation.md) | Documentation | Medium | Draft |
| [REQ-007](REQ-007-repository-cleanup.md) | Repository Cleanup | Low | Draft |
| [REQ-008](REQ-008-cmake-integration.md) | CMake Integration | High | Draft |

### Python Build System Requirements (REQ-009 to REQ-016)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-009](REQ-001-omnicpp-controller-entry-point.md) | OmniCppController.py as Single Entry Point | Critical | Draft |
| [REQ-010](REQ-002-modular-controller-pattern.md) | Modular Controller Pattern Implementation | Critical | Draft |
| [REQ-011](REQ-003-type-hints-enforcement.md) | Type Hints Enforcement (Zero Pylance Errors) | Critical | Draft |
| [REQ-012](REQ-004-python-script-consolidation.md) | Python Script Consolidation | High | Draft |
| [REQ-013](REQ-005-logging-configuration.md) | Logging Configuration and Custom Formatters | High | Draft |
| [REQ-014](REQ-006-error-handling-exception-management.md) | Error Handling and Exception Management | High | Draft |
| [REQ-015](REQ-007-configuration-management.md) | Configuration Management | High | Draft |
| [REQ-016](REQ-008-command-line-interface.md) | Command-Line Interface | High | Draft |

### Cross-Platform Compilation Requirements (REQ-017 to REQ-023)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-017](REQ-009-platform-detection.md) | Platform Detection | Critical | Draft |
| [REQ-018](REQ-010-compiler-detection.md) | Compiler Detection | Critical | Draft |
| [REQ-019](REQ-011-terminal-invocation-patterns.md) | Terminal Invocation Patterns | Critical | Draft |
| [REQ-020](REQ-012-msvc-developer-command-prompt-integration.md) | MSVC Developer Command Prompt Integration | Critical | Draft |
| [REQ-021](REQ-013-msys2-terminal-integration.md) | MSYS2 Terminal Integration | High | Draft |
| [REQ-022](REQ-014-cross-compilation-support.md) | Cross-Compilation Support | High | Draft |
| [REQ-023](REQ-015-compiler-selection-fallback.md) | Compiler Selection and Fallback Mechanisms | High | Draft |

### Package Manager Requirements (REQ-024 to REQ-029)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-024](REQ-016-conan-integration.md) | Conan Integration | High | Draft |
| [REQ-025](REQ-017-vcpkg-integration.md) | vcpkg Integration | High | Draft |
| [REQ-026](REQ-018-cpm-cmake-integration.md) | CPM.cmake Integration | High | Draft |
| [REQ-027](REQ-019-priority-based-package-manager-selection.md) | Priority-Based Package Manager Selection | Critical | Draft |
| [REQ-028](REQ-020-package-security-verification.md) | Package Security Verification | Critical | Draft |
| [REQ-029](REQ-021-dependency-resolution-caching.md) | Dependency Resolution and Caching | High | Draft |

### Build System Requirements (REQ-030 to REQ-035)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-030](REQ-022-cmake-4-configuration.md) | CMake 4 Configuration | Critical | Draft |
| [REQ-031](REQ-023-ninja-generator-default.md) | Ninja Generator as Default | Critical | Draft |
| [REQ-032](REQ-024-cmake-presets-cross-platform.md) | CMake Presets for Cross-Platform Builds | High | Draft |
| [REQ-033](REQ-025-toolchain-file-organization.md) | Toolchain File Organization | High | Draft |
| [REQ-034](REQ-026-build-optimization-caching.md) | Build Optimization and Caching | High | Draft |
| [REQ-035](REQ-027-parallel-build-support.md) | Parallel Build Support | High | Draft |

### C++ Engine and Game Requirements (REQ-036 to REQ-044)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-036](REQ-028-cpp23-standard-compliance.md) | C++23 Standard Compliance (No Modules) | Critical | Draft |
| [REQ-037](REQ-029-modern-cpp-features.md) | Modern C++ Features Adoption | High | Draft |
| [REQ-038](REQ-030-memory-management.md) | Memory Management (RAII, Smart Pointers) | Critical | Draft |
| [REQ-039](REQ-031-spdlog-integration.md) | spdlog Integration for C++ Logging | High | Draft |
| [REQ-040](REQ-032-file-rotation-log-retention.md) | File Rotation and Log Retention | Medium | Draft |
| [REQ-041](REQ-033-structured-logging-format.md) | Structured Logging Format | Medium | Draft |
| [REQ-042](REQ-034-qt6-vulkan-integration.md) | QT6 and Vulkan Integration | High | Draft |
| [REQ-043](REQ-035-engine-architecture.md) | Engine Architecture (ECS, Components, Systems) | High | Draft |
| [REQ-044](REQ-036-game-architecture.md) | Game Architecture (Scenes, Entities, Components) | High | Draft |

### Testing Requirements (REQ-045 to REQ-050)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-045](REQ-037-google-test-cpp-unit-tests.md) | Google Test for C++ Unit Tests | Critical | Draft |
| [REQ-046](REQ-038-pytest-python-tests.md) | pytest for Python Tests | Critical | Draft |
| [REQ-047](REQ-039-code-coverage.md) | Code Coverage (80% Minimum) | High | Draft |
| [REQ-048](REQ-040-integration-tests.md) | Integration Tests | High | Draft |
| [REQ-049](REQ-041-cross-platform-test-execution.md) | Cross-Platform Test Execution | High | Draft |
| [REQ-050](REQ-042-test-automation.md) | Test Automation | High | Draft |

### Security Requirements (REQ-051 to REQ-055)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-051](REQ-043-secure-terminal-invocation.md) | Secure Terminal Invocation | Critical | Draft |
| [REQ-052](REQ-044-dependency-integrity-verification.md) | Dependency Integrity Verification | Critical | Draft |
| [REQ-053](REQ-045-secure-logging.md) | Secure Logging (No Sensitive Data) | Critical | Draft |
| [REQ-054](REQ-046-build-system-security.md) | Build System Security | Critical | Draft |
| [REQ-055](REQ-047-package-manager-security.md) | Package Manager Security | Critical | Draft |

### VSCode Integration Requirements (REQ-056 to REQ-060)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-056](REQ-048-vscode-tasks-configuration.md) | VSCode tasks.json Configuration | High | Draft |
| [REQ-057](REQ-049-vscode-launch-configuration.md) | VSCode launch.json Configuration | High | Draft |
| [REQ-058](REQ-050-omnicpp-controller-integration.md) | OmniCppController.py Integration | High | Draft |
| [REQ-059](REQ-051-debugging-support.md) | Debugging Support | High | Draft |
| [REQ-060](REQ-052-task-automation.md) | Task Automation | High | Draft |

### Documentation Requirements (REQ-061 to REQ-064)

| ID | Title | Priority | Status |
|-----|--------|----------|--------|
| [REQ-061](REQ-053-api-documentation.md) | API Documentation | High | Draft |
| [REQ-062](REQ-054-user-documentation.md) | User Documentation | High | Draft |
| [REQ-063](REQ-055-developer-documentation.md) | Developer Documentation | High | Draft |
| [REQ-064](REQ-056-architecture-documentation.md) | Architecture Documentation | High | Draft |

## Priority Summary

- **Critical:** 26 requirements
- **High:** 34 requirements
- **Medium:** 4 requirements
- **Low:** 0 requirements

## Linux Expansion Requirements Breakdown

### REQ-001: OmniCppController.py Linux Support (8 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-001-001 | Detect Linux distribution | Critical | None |
| REQ-001-002 | Detect CachyOS specifically | Critical | REQ-001-001 |
| REQ-001-003 | Detect Nix environment | Critical | None |
| REQ-001-004 | Detect package manager | Critical | REQ-001-001 |
| REQ-001-005 | Apply CachyOS-specific compiler flags | High | REQ-001-002 |
| REQ-001-006 | Integrate with Nix shell | Critical | REQ-001-003 |
| REQ-001-007 | Validate Linux build environment | Critical | REQ-001-004, REQ-001-006 |
| REQ-001-008 | Generate Linux build commands | High | REQ-001-005, REQ-001-007 |

### REQ-002: flake.nix Enhancement (8 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-002-001 | Define CachyOS-specific packages | Critical | None |
| REQ-002-002 | Define GCC toolchain | Critical | None |
| REQ-002-003 | Define Clang toolchain | Critical | None |
| REQ-002-004 | Define Qt6 dependencies | Critical | None |
| REQ-002-005 | Define Vulkan dependencies | Critical | None |
| REQ-002-006 | Define development shell | Critical | REQ-002-001, REQ-002-002, REQ-002-003, REQ-002-004, REQ-002-005 |
| REQ-002-007 | Configure CMake integration | High | REQ-002-006 |
| REQ-002-008 | Configure Conan integration | High | REQ-002-006 |

### REQ-003: VSCode Configuration (5 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-003-001 | Add Linux build tasks | High | REQ-001-008 |
| REQ-003-002 | Add Linux debug configurations | High | REQ-001-008 |
| REQ-003-003 | Add Nix shell task | High | REQ-001-006 |
| REQ-003-004 | Add CachyOS validation task | Medium | REQ-001-007 |
| REQ-003-005 | Platform-specific task selection | Medium | REQ-003-001, REQ-003-002 |

### REQ-004: Conan Profiles (8 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-004-001 | Create gcc-linux profile | High | None |
| REQ-004-002 | Create gcc-linux-debug profile | High | REQ-004-001 |
| REQ-004-003 | Create clang-linux profile | High | None |
| REQ-004-004 | Create clang-linux-debug profile | High | REQ-004-003 |
| REQ-004-005 | Create cachyos profile | High | REQ-004-001 |
| REQ-004-006 | Create cachyos-debug profile | High | REQ-004-005 |
| REQ-004-007 | Create cachyos-clang profile | High | REQ-004-003 |
| REQ-004-008 | Create cachyos-clang-debug profile | High | REQ-004-007 |

### REQ-005: Setup Scripts (6 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-005-001 | Create setup_gcc.sh | High | None |
| REQ-005-002 | Create setup_clang.sh | High | None |
| REQ-005-003 | Create setup_cachyos.sh | High | REQ-005-001 |
| REQ-005-004 | Create setup_nix.sh | High | None |
| REQ-005-005 | Create setup_qt6_vulkan.sh | High | REQ-002-004, REQ-002-005 |
| REQ-005-006 | Create validate_environment.sh | High | REQ-001-007 |

### REQ-006: Documentation (5 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-006-001 | Create nix-development.md | Medium | REQ-002-006 |
| REQ-006-002 | Create cachyos-builds.md | Medium | REQ-001-002 |
| REQ-006-003 | Create linux-troubleshooting.md | Medium | REQ-001-007 |
| REQ-006-004 | Create conan-linux-profiles.md | Medium | REQ-004-001 |
| REQ-006-005 | Create vscode-linux-setup.md | Medium | REQ-003-001 |

### REQ-007: Repository Cleanup (4 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-007-001 | Archive Windows-specific scripts | Low | None |
| REQ-007-002 | Reorganize test files | Low | None |
| REQ-007-003 | Remove duplicate files | Low | None |
| REQ-007-004 | Update documentation | Low | REQ-007-001, REQ-007-002, REQ-007-003 |

### REQ-008: CMake Integration (4 sub-requirements)

| ID | Title | Priority | Dependencies |
|-----|--------|----------|---------------|
| REQ-008-001 | Add Nix-aware CMake presets | High | REQ-002-007 |
| REQ-008-002 | Add CachyOS build configurations | High | REQ-001-005 |
| REQ-008-003 | Enhance platform detection | Critical | REQ-001-001 |
| REQ-008-004 | Add Linux compiler flags | High | REQ-001-005 |

## Implementation Order

### Phase 1: Foundation (Critical Path)
1. REQ-001-001, REQ-001-003, REQ-001-004 (Platform detection)
2. REQ-002-001, REQ-002-002, REQ-002-003, REQ-002-004, REQ-002-005 (Nix packages)
3. REQ-002-006, REQ-002-007, REQ-002-008 (Nix shell integration)
4. REQ-001-006, REQ-001-007 (Nix integration, validation)
5. REQ-001-005, REQ-001-008 (CachyOS flags, build commands)
6. REQ-008-003, REQ-008-004 (CMake platform detection, flags)

### Phase 2: Tooling (High Priority)
1. REQ-004-001, REQ-004-002, REQ-004-003, REQ-004-004 (Base Conan profiles)
2. REQ-004-005, REQ-004-006, REQ-004-007, REQ-004-008 (CachyOS Conan profiles)
3. REQ-005-001, REQ-005-002, REQ-005-003, REQ-005-004 (Setup scripts)
4. REQ-005-005, REQ-005-006 (Qt6/Vulkan setup, validation)
5. REQ-008-001, REQ-008-002 (CMake presets, CachyOS configs)

### Phase 3: Integration (High Priority)
1. REQ-003-001, REQ-003-002, REQ-003-003, REQ-003-004, REQ-003-005 (VSCode tasks)

### Phase 4: Documentation (Medium Priority)
1. REQ-006-001, REQ-006-002, REQ-006-003, REQ-006-004, REQ-006-005 (Documentation)

### Phase 5: Cleanup (Low Priority)
1. REQ-007-001, REQ-007-002, REQ-007-003, REQ-007-004 (Repository cleanup)

## Related Documents

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Coding Standards
- [`.specs/00_current_state/manifest.md`](../00_current_state/manifest.md) - Current State
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future State
- [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md) - Threat Model Analysis
- [`.specs/02_adrs/`](../02_adrs/) - Architecture Decision Records
- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest

## Notes

- All requirements are currently in Draft status
- Each requirement includes detailed acceptance criteria, test cases, and implementation notes
- Requirements are organized by domain for easy navigation
- Priority levels are assigned based on criticality to the system
- Linux expansion requirements (REQ-001 to REQ-008) are new additions for Phase 5
- Implementation order follows dependency graph and criticality
