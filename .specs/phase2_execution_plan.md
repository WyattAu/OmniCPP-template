# Phase 2: Python Script Consolidation - Execution Plan

**Generated:** 2026-01-07
**Status:** In Progress

---

## Executive Summary

The `omni_scripts/` directory structure exists but `scripts/python/` contains significantly more advanced functionality that must be migrated. This execution plan details the systematic migration of all advanced functionality.

---

## Migration Priority Matrix

### High Priority (Critical Path)

| Module | Source | Target | Complexity | Effort |
|---------|--------|--------|------------|---------|
| Compiler Detection System | scripts/python/compilers/compiler_detection_system.py | omni_scripts/compilers/detector.py | High | 8h |
| Configuration Manager | scripts/python/core/config_manager.py | omni_scripts/config.py | Medium | 4h |
| Cross-Compilation Support | scripts/python/compilers/*_cross_compiler.py | omni_scripts/compilers/ | High | 6h |
| Terminal Detection | scripts/python/compilers/*_detector.py | omni_scripts/utils/terminal_utils.py | Medium | 4h |
| Package Managers | scripts/python/package_managers/ | omni_scripts/build_system/ | Medium | 4h |
| Test Migration | impl/tests/ | omni_scripts/tests/ | Medium | 6h |

### Medium Priority

| Module | Source | Target | Complexity | Effort |
|---------|--------|--------|------------|---------|
| CMake Modules | scripts/python/cmake/ | omni_scripts/build_system/cmake.py | Medium | 4h |
| Commands | scripts/python/commands/ | omni_scripts/controller/ | Low | 2h |
| Targets | scripts/python/targets/ | omni_scripts/platform/ | Low | 2h |

---

## Detailed Migration Steps

### Step 1: Enhance Compiler Detection System (P2-004.1)

**Source:** `scripts/python/compilers/compiler_detection_system.py`
**Target:** `omni_scripts/compilers/detector.py`

**Actions:**
1. Add `CompilerDetectionSystem` class with unified detection
2. Add terminal detection and mapping
3. Add cross-compiler support (Linux, WASM, Android)
4. Add toolchain detection
5. Add CMake generator selection
6. Add comprehensive validation
7. Update type hints throughout

**Acceptance Criteria:**
- [ ] CompilerDetectionSystem class implemented
- [ ] Terminal detection working
- [ ] Cross-compiler support working
- [ ] Toolchain detection working
- [ ] CMake generator selection working
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 2: Enhance Configuration Manager (P2-004.2)

**Source:** `scripts/python/core/config_manager.py`
**Target:** `omni_scripts/config.py`

**Actions:**
1. Add ConfigManager class with full functionality
2. Add configuration validation
3. Add configuration caching
4. Add dot notation support for nested keys
5. Add save/reload functionality
6. Update type hints throughout

**Acceptance Criteria:**
- [ ] ConfigManager class implemented
- [ ] Configuration validation working
- [ ] Configuration caching working
- [ ] Dot notation support working
- [ ] Save/reload functionality working
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 3: Migrate Cross-Compilation Support (P2-004.3)

**Source:** `scripts/python/compilers/*_cross_compiler.py`
**Target:** `omni_scripts/compilers/`

**Actions:**
1. Create `cross_compilers.py` module
2. Add LinuxCrossCompiler class
3. Add WASMCrossCompiler class
4. Add AndroidCrossCompiler class
5. Add cross-compiler factory
6. Update type hints throughout

**Acceptance Criteria:**
- [ ] Cross-compilers module created
- [ ] LinuxCrossCompiler implemented
- [ ] WASMCrossCompiler implemented
- [ ] AndroidCrossCompiler implemented
- [ ] Cross-compiler factory working
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 4: Enhance Terminal Detection (P2-004.4)

**Source:** `scripts/python/compilers/*_detector.py`
**Target:** `omni_scripts/utils/terminal_utils.py`

**Actions:**
1. Add terminal detection classes
2. Add terminal invoker
3. Add compiler-terminal mapper
4. Add environment setup for different terminals
5. Update type hints throughout

**Acceptance Criteria:**
- [ ] Terminal detection classes implemented
- [ ] Terminal invoker working
- [ ] Compiler-terminal mapper working
- [ ] Environment setup working
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 5: Migrate Package Managers (P2-004.5)

**Source:** `scripts/python/package_managers/`
**Target:** `omni_scripts/build_system/`

**Actions:**
1. Enhance existing package manager modules
2. Add package manager factory
3. Add priority-based selection
4. Add security verification
5. Update type hints throughout

**Acceptance Criteria:**
- [ ] Package managers enhanced
- [ ] Package manager factory working
- [ ] Priority-based selection working
- [ ] Security verification working
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 6: Migrate Test Files (P2-005)

**Source:** `impl/tests/`
**Target:** `omni_scripts/tests/`

**Actions:**
1. Create `omni_scripts/tests/` directory structure
2. Create `unit/` subdirectory
3. Create `integration/` subdirectory
4. Create `fixtures/` subdirectory
5. Migrate all test files
6. Update test imports
7. Update type hints throughout

**Acceptance Criteria:**
- [ ] Tests directory structure created
- [ ] All test files migrated
- [ ] Test imports updated
- [ ] All type hints added
- [ ] Zero Pylance errors

### Step 7: Update Imports (P2-006)

**Actions:**
1. Scan all files for import statements
2. Update imports from `scripts.python.*` to `omni_scripts.*`
3. Update imports from `impl.tests.*` to `omni_scripts.tests.*`
4. Resolve circular dependencies
5. Validate dependency graph

**Acceptance Criteria:**
- [ ] All imports updated
- [ ] Circular dependencies resolved
- [ ] Dependency graph validated
- [ ] No import errors

### Step 8: Remove Duplicate Files (P2-007)

**Actions:**
1. Identify duplicate files
2. Catalog obsolete files
3. Delete safe-to-remove files
4. Ensure no functionality lost
5. Update documentation

**Acceptance Criteria:**
- [ ] Duplicate files identified
- [ ] Obsolete files cataloged
- [ ] Safe-to-remove files deleted
- [ ] No functionality lost
- [ ] Documentation updated

### Step 9: Add Type Hints (P2-008)

**Actions:**
1. Add type hints to all functions
2. Add type hints to all classes
3. Add type hints to variables where appropriate
4. Use TypeAlias for complex types
5. Achieve zero Pylance errors

**Acceptance Criteria:**
- [ ] All functions have type hints
- [ ] All classes have type hints
- [ ] All variables have type hints where appropriate
- [ ] TypeAlias used for complex types
- [ ] Zero Pylance errors

### Step 10: Fix Pylance Errors (P2-009)

**Actions:**
1. Run Pylance on all Python files
2. Resolve all errors
3. Address or suppress warnings with justification
4. Improve code quality

**Acceptance Criteria:**
- [ ] Zero Pylance errors
- [ ] Zero critical warnings
- [ ] All warnings addressed or suppressed
- [ ] Code quality improved

### Step 11: Update OmniCppController.py (P2-010)

**Actions:**
1. Review current OmniCppController.py
2. Update imports to use new structure
3. Implement modular controller pattern
4. Maintain backward compatibility
5. Ensure all tests pass

**Acceptance Criteria:**
- [ ] OmniCppController.py updated
- [ ] Imports from omni_scripts/
- [ ] Modular controller pattern implemented
- [ ] Backward compatibility maintained
- [ ] All tests pass

### Step 12: Test Python Scripts (P2-011)

**Actions:**
1. Create unit tests for all modules
2. Create integration tests
3. Ensure all tests pass
4. Achieve code coverage > 80%
5. Establish performance benchmarks

**Acceptance Criteria:**
- [ ] Unit tests created for all modules
- [ ] Integration tests created
- [ ] All tests pass
- [ ] Code coverage > 80%
- [ ] Performance benchmarks established

---

## Risk Mitigation

### Risk 1: Breaking Existing Functionality

**Mitigation:**
- Keep original files until migration is verified
- Run comprehensive tests after each migration step
- Maintain backward compatibility

### Risk 2: Import Errors

**Mitigation:**
- Update imports incrementally
- Test imports after each update
- Use explicit imports to avoid circular dependencies

### Risk 3: Type Hint Errors

**Mitigation:**
- Add type hints incrementally
- Run Pylance after each addition
- Use Optional and Union for complex types

### Risk 4: Test Failures

**Mitigation:**
- Run tests after each migration step
- Fix issues immediately
- Maintain test coverage

---

## Timeline

| Week | Tasks | Effort |
|-------|--------|---------|
| Week 2 | Steps 1-6 (P2-004, P2-005) | 32h |
| Week 3 | Steps 7-12 (P2-006 through P2-011) | 32h |

**Total Effort:** 64 hours (8 days)

---

## Success Criteria

- [ ] All 11 Phase 2 tasks completed
- [ ] All Python scripts consolidated into omni_scripts/
- [ ] Type hints added to all code
- [ ] Zero Pylance errors achieved
- [ ] OmniCppController.py refactored
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] Performance benchmarks established

---

**Document Version:** 1.0
**Last Updated:** 2026-01-07
