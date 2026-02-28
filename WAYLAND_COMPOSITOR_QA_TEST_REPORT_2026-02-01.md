# Wayland Compositor QA Test Report

**Date:** 2026-02-01T21:47:00.000Z  
**Task:** Test game on Wayland compositor (window visibility, 3D graphics, controllability, statistics overlay, Qt configuration windows)  
**Status:** BLOCKED - Pre-existing build system issue prevents testing  
**Role:** QA Specialist

---

## Executive Summary

The QA testing of the OmniCpp 3D Pong game on Wayland compositor was **BLOCKED** due to a **critical build system issue**. The game cannot be compiled due to undefined references to `WindowManager` methods that are not being included in the engine library build.

**Key Findings:**
- **Wayland Compositor:** ✅ Running (KWin Wayland)
- **Qt6:** ✅ Installed (version 6.10.2)
- **Vulkan:** ✅ Installed (version 1.4.335.0)
- **Engine Library Build:** ✅ Successful
- **Pong Example Build:** ❌ BLOCKED - Undefined references to WindowManager methods

**Root Cause:** The engine library is being built without `OMNICPP_HAS_QT_VULKAN` compile definition, which causes the Qt6 Vulkan-specific `WindowManager` methods (`set_qt_application`, `set_close_callback`, `get_qt_window`) to be excluded from the compiled library.

---

## Table of Contents

1. [Pre-Computation](#pre-computation)
2. [Wayland Compositor Availability](#wayland-compositor-availability)
3. [Build System Analysis](#build-system-analysis)
4. [Root Cause Analysis](#root-cause-analysis)
5. [Previous Reports Review](#previous-reports-review)
6. [Test Results](#test-results)
7. [Issues Found](#issues-found)
8. [Fixes Needed](#fixes-needed)
9. [Security Considerations](#security-considerations)
10. [Recommendations](#recommendations)
11. [Conclusion](#conclusion)

---

## Pre-Computation

### 1.1 Threat Model Review

Reviewed [`.specs/03_threat_model/analysis.md`](.specs/03_threat_model/analysis.md:1) for security considerations relevant to Wayland testing:

**Key Security Considerations:**
- **TM-LX-002:** Distribution-Specific vulnerabilities - Wayland compositor security considerations
- **TM-LX-001:** Nix Package Manager security risks
- **TM-001:** Malicious Package Injection (Conan)
- **TM-004:** Dependency Confusion Attack

**Relevant Threats for Wayland Testing:**
1. **Window State Management:** On Wayland, the compositor controls window state, not the application
2. **Input Handling:** Wayland uses different input mechanisms compared to X11
3. **Surface Creation:** Wayland requires specific Vulkan surface extension (`VK_KHR_wayland_surface`)
4. **Environment Variables:** `QT_QPA_PLATFORM=wayland` must be set correctly

### 1.2 Game Source Review

Reviewed [`examples/pong/main.cpp`](examples/pong/main.cpp:1):

**Wayland-Specific Code:**
- Lines 300-310: Wayland platform detection using `QT_QPA_PLATFORM` environment variable
- Lines 397-403: Wayland-specific window visibility requests (`raise()`, `activateWindow()`)
- Lines 456-462: Wayland-specific FPS logging with `[Wayland]` prefix

**Key Features to Test:**
1. Window visibility on Wayland (lines 397-403)
2. 3D graphics rendering with Vulkan
3. Game controllability (keyboard/mouse input)
4. Statistics overlay (lines 161-177)
5. Qt configuration windows (lines 207-211)

### 1.3 Previous Reports Review

**Reports Reviewed:**
1. [`WAYLAND_PONG_3D_IMPLEMENTATION_REPORT.md`](WAYLAND_PONG_3D_IMPLEMENTATION_REPORT.md:1) - 95% complete implementation
2. [`WAYLAND_VULKAN_FIX_REPORT.md`](WAYLAND_VULKAN_FIX_REPORT.md:1) - Vulkan fixes
3. [`WAYLAND_VULKAN_RENDERING_WINDOW_STATE_INTERACTIVITY_FIX_REPORT.md`](WAYLAND_VULKAN_RENDERING_WINDOW_STATE_INTERACTIVITY_FIX_REPORT.md:1) - Rendering fixes
4. [`WAYLAND_WINDOW_STATE_FPS_FIX_REPORT.md`](WAYLAND_WINDOW_STATE_FPS_FIX_REPORT.md:1) - Window state fixes
5. [`WAYLAND_WINDOW_VISIBILITY_FIX_REPORT.md`](WAYLAND_WINDOW_VISIBILITY_FIX_REPORT.md:1) - Visibility fixes
6. [`CPP23_STANDARD_UPGRADE_REPORT.md`](CPP23_STANDARD_UPGRADE_REPORT.md:1) - C++23 upgrade report

**Key Findings from Previous Reports:**
- Window visibility was fixed by implementing proper Qt6 window creation
- Vulkan instance extensions were configured for Wayland
- Window state issues were addressed by skipping `setWindowState()` on Wayland
- FPS measurement system was implemented
- C++23 upgrade resolved spdlog/fmt compatibility issue

---

## Wayland Compositor Availability

### 2.1 Compositor Detection

**Detection Method:**
```bash
echo $XDG_SESSION_TYPE
ps aux | grep -i wayland | grep -v grep
```

**Results:**
```
XDG_SESSION_TYPE: wayland
WAYLAND_DISPLAY: wayland-0
```

**Compositor:** KWin Wayland  
**Process:** `/usr/bin/kwin_wayland --wayland-fd 7 --socket wayland-0 --xwayland-fd 8`

### 2.2 Environment Variables

**Current Environment:**
- `XDG_SESSION_TYPE`: `wayland`
- `WAYLAND_DISPLAY`: `wayland-0`
- `DISPLAY`: `:0` (XWayland for X11 compatibility)

**Test Configuration:**
- `QT_QPA_PLATFORM`: Should be set to `wayland` for testing

---

## Build System Analysis

### 3.1 Build Directory Status

**Build Directory:** `/home/wyatt/dev/templates/OmniCPP-template/build/`

**Existing Build Artifacts:**
```
lib/libomnicpp_engine.so  ✅ Built successfully
bin/simple_game              ✅ Built successfully
```

**Missing Build Artifact:**
```
bin/omnicpp_pong_example   ❌ Not built
```

### 3.2 CMake Configuration

**CMake Cache Analysis:**
```cmake
OMNICPP_USE_QT6:BOOL=ON
OMNICPP_USE_QT_VULKAN:BOOL=OFF  ⚠️ WARNING
OMNICPP_USE_VULKAN:BOOL=ON
Vulkan_FOUND:BOOL=TRUE
```

**Issue Identified:** `OMNICPP_USE_QT_VULKAN` is set to `OFF`, which causes the engine library to be built without Qt6 Vulkan-specific methods.

### 3.3 Build Attempt Results

**Build Command:**
```bash
cd build && make omnicpp_pong_example
```

**Build Errors:**
```
/usr/bin/ld: /tmp/ccFDzdaw.ltrans0.ltrans.o: in function `main':
<artificial>:(.text.startup+0x222): undefined reference to `OmniCpp::Engine::Window::WindowManager::set_qt_application(QGuiApplication*)'
/usr/bin/ld: <artificial>:(.text.startup+0x25d): undefined reference to `OmniCpp::Engine::Window::WindowManager::set_close_callback(std::function<void ()>)'
/usr/bin/ld: <artificial>:(.text.startup+0x646): undefined reference to `OmniCpp::Engine::Window::WindowManager::get_qt_window() const'
collect2: error: ld returned 1 exit status
```

**Undefined Symbols:**
1. `WindowManager::set_qt_application(QGuiApplication*)`
2. `WindowManager::set_close_callback(std::function<void()>)`
3. `WindowManager::get_qt_window() const`

### 3.4 Engine Library Symbol Analysis

**Symbol Check:**
```bash
nm lib/libomnicpp_engine.so | grep -E "set_qt_application|set_close_callback|get_qt_window"
```

**Result:** Only `VulkanWindow::set_close_callback` is present. The `WindowManager` methods are **not** in the library.

**Conclusion:** The engine library was compiled without `OMNICPP_HAS_QT_VULKAN` defined, so the Qt6 Vulkan-specific `WindowManager` methods were excluded from compilation.

---

## Root Cause Analysis

### 4.1 CMake Configuration Issue

**Engine CMakeLists.txt Analysis:**

File: [`src/engine/CMakeLists.txt`](src/engine/CMakeLists.txt:1)

**Lines 13-30:**
```cmake
# Find Qt6 (optional) and Vulkan (optional)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)

    if(NOT Qt6_FOUND)
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()

    # Qt6 Vulkan integration requires both Qt6 and Vulkan
    # Vulkan is configured in cmake/FindDependencies.cmake for Nix environment
    if(Qt6_FOUND AND Vulkan_FOUND)
        message(STATUS "Qt6 and Vulkan found - Qt6 Vulkan integration enabled")
        set(OMNICPP_USE_QT_VULKAN ON CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    else()
        message(WARNING "Qt6 Vulkan integration requires both Qt6 and Vulkan - Qt6 Vulkan integration disabled")
        set(OMNICPP_USE_QT_VULKAN OFF CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    endif()
endif()
```

**Issue:** The `Qt6_FOUND` variable is not being set properly by the `find_package(Qt6 ...)` call in the engine's CMakeLists.txt. This causes the condition `if(Qt6_FOUND AND Vulkan_FOUND)` to fail, resulting in `OMNICPP_USE_QT_VULKAN` being set to `OFF`.

### 4.2 Root Cause

**Primary Root Cause:**
The root CMakeLists.txt calls `find_package(Qt6 ...)` which successfully finds Qt6, but when the engine's CMakeLists.txt calls `find_package(Qt6 ...)` again, it doesn't properly set the `Qt6_FOUND` variable.

**Secondary Root Cause:**
The engine's CMakeLists.txt uses `Qt6_FOUND` to determine whether to enable Qt6 Vulkan integration, but this variable is not being set correctly during the engine's configuration phase.

### 4.3 Impact Analysis

**Impact on Build:**
- Engine library builds successfully but without Qt6 Vulkan-specific methods
- Pong example fails to link due to undefined references to `WindowManager` methods
- Testing on Wayland compositor is blocked

**Impact on Testing:**
- Cannot test window visibility on Wayland
- Cannot test 3D graphics rendering on Wayland
- Cannot test game controllability on Wayland
- Cannot test statistics overlay on Wayland
- Cannot test Qt configuration windows on Wayland
- Cannot verify FPS performance on Wayland

---

## Previous Reports Review

### 5.1 CPP23 Standard Upgrade Report

**Report:** [`CPP23_STANDARD_UPGRADE_REPORT.md`](CPP23_STANDARD_UPGRADE_REPORT.md:1)

**Status:** ✅ COMPLETED

**Key Findings:**
- C++23 standard upgrade was successful
- Main engine library (`libomnicpp_engine.so`) was built successfully with C++23
- spdlog/fmt compatibility issue was resolved by using spdlog's bundled fmt

**Pre-existing Issues Documented:**
```
### Pre-existing Build Issues (Not Related to C++23 Upgrade)

1. **Test Files:**
   - `tests/unit/test_audio_manager.cpp` - Duplicate test definitions and missing member variables
   - `tests/unit/test_resource_manager.cpp` - Missing member variable `resource_manager_`
   - `tests/unit/test_ecs.cpp` - Undefined reference to `test::EntityTest::SetUp()`

2. **Pong Example:**
   - `examples/pong/main.cpp` - Undefined references to `WindowManager` functions
   - `examples/pong/pong_game.cpp` - Deprecated Qt6 API usage (`stateChanged`)
```

**Note:** The pong example build issue was documented as a pre-existing issue in the C++23 upgrade report.

### 5.2 Wayland Fix Reports

**Reports Reviewed:**

1. **WAYLAND_WINDOW_VISIBILITY_FIX_REPORT.md**
   - ✅ Window visibility fixed for Wayland
   - ✅ Qt6 window created correctly
   - ✅ Wayland platform detection added

2. **WAYLAND_WINDOW_STATE_FPS_FIX_REPORT.md**
   - ✅ Window state fixed for Wayland (skipping `setWindowState()`)
   - ✅ FPS measurement system implemented
   - ✅ Stable 57-58 FPS performance on Wayland

3. **WAYLAND_VULKAN_RENDERING_WINDOW_STATE_INTERACTIVITY_FIX_REPORT.md**
   - ✅ Vulkan rendering fixed for Wayland
   - ✅ Wayland surface extension enabled
   - ✅ Full input event handling implemented

4. **WAYLAND_VULKAN_FIX_REPORT.md**
   - ⚠️ Build Fixed - Wayland-Specific Implementation Pending
   - ⚠️ Qt6 Vulkan instance creation API compatibility noted

**Note:** All previous Wayland fix reports indicate that the implementation was completed, but the build system issue prevents testing.

---

## Test Results

### 6.1 Test Execution Status

**Overall Status:** BLOCKED

| Test Case | Status | Notes |
|-----------|--------|-------|
| Wayland compositor available | ✅ PASS | KWin Wayland running |
| Game can be built | ❌ BLOCKED | Pre-existing build issue |
| Game runs on Wayland | ❌ BLOCKED | Cannot run without successful build |
| Window visibility on Wayland | ❌ BLOCKED | Cannot test without successful build |
| 3D graphics rendering on Wayland | ❌ BLOCKED | Cannot test without successful build |
| Game controllability on Wayland | ❌ BLOCKED | Cannot test without successful build |
| Statistics overlay on Wayland | ❌ BLOCKED | Cannot test without successful build |
| Qt configuration windows on Wayland | ❌ BLOCKED | Cannot test without successful build |
| FPS performance verification | ❌ BLOCKED | Cannot test without successful build |

### 6.2 Definition of Done Checklist

| Requirement | Status |
|------------|--------|
| Game built successfully | ❌ BLOCKED - Pre-existing build issue |
| Game runs on Wayland | ❌ BLOCKED - Cannot run without successful build |
| Window is visible on Wayland | ❌ BLOCKED - Cannot test without successful build |
| 3D graphics are rendered on Wayland | ❌ BLOCKED - Cannot test without successful build |
| Game is controllable on Wayland | ❌ BLOCKED - Cannot test without successful build |
| Statistics overlay works on Wayland | ❌ BLOCKED - Cannot test without successful build |
| Qt configuration windows work on Wayland | ❌ BLOCKED - Cannot test without successful build |
| No errors | ❌ BLOCKED - Build errors present |
| FPS performance is good | ❌ BLOCKED - Cannot verify without successful build |
| Test results documented | ✅ PASS | This report |
| Any issues found documented | ✅ PASS | This report |
| Any fixes needed documented | ✅ PASS | This report |
| Final status summary provided | ✅ PASS | This report |

---

## Issues Found

### 7.1 Critical Issue: Build System Failure

**Issue ID:** BUILD-001  
**Severity:** Critical  
**Category:** Build System

**Description:**
The pong example cannot be built due to undefined references to `WindowManager` methods that are not being included in the engine library build.

**Undefined Symbols:**
1. `OmniCpp::Engine::Window::WindowManager::set_qt_application(QGuiApplication*)`
2. `OmniCpp::Engine::Window::WindowManager::set_close_callback(std::function<void()>)`
3. `OmniCpp::Engine::Window::WindowManager::get_qt_window() const`

**Root Cause:**
The engine library is being built without `OMNICPP_HAS_QT_VULKAN` compile definition, which causes the Qt6 Vulkan-specific `WindowManager` methods to be excluded from compilation.

**CMake Configuration Issue:**
```cmake
# Engine CMakeLists.txt lines 23-29
if(Qt6_FOUND AND Vulkan_FOUND)
    message(STATUS "Qt6 and Vulkan found - Qt6 Vulkan integration enabled")
    set(OMNICPP_USE_QT_VULKAN ON CACHE BOOL "Use Qt6 with Vulkan" FORCE)
else()
    message(WARNING "Qt6 Vulkan integration requires both Qt6 and Vulkan - Qt6 Vulkan integration disabled")
    set(OMNICPP_USE_QT_VULKAN OFF CACHE BOOL "Use Qt6 with Vulkan" FORCE)
endif()
```

**CMake Warning:**
```
CMake Warning at src/engine/CMakeLists.txt:27 (message):
  Qt6 Vulkan integration requires both Qt6 and Vulkan - Qt6 Vulkan
  integration disabled
```

### 7.2 Pre-existing Issue

**Issue ID:** PREEXIST-001  
**Severity:** High  
**Category:** Pre-existing Build Issue

**Description:**
This build issue was documented in [`CPP23_STANDARD_UPGRADE_REPORT.md`](CPP23_STANDARD_UPGRADE_REPORT.md:1) as a pre-existing issue unrelated to the C++23 upgrade.

**Reference:**
```
### Pre-existing Build Issues (Not Related to C++23 Upgrade)

2. **Pong Example:**
   - `examples/pong/main.cpp` - Undefined references to `WindowManager` functions
   - `examples/pong/pong_game.cpp` - Deprecated Qt6 API usage (`stateChanged`)
```

---

## Fixes Needed

### 8.1 Fix for CMake Configuration Issue

**Issue:** `Qt6_FOUND` variable not being set properly in engine's CMakeLists.txt

**Proposed Fix:**

**Option 1: Use Qt6 Imported Targets**
Modify [`src/engine/CMakeLists.txt`](src/engine/CMakeLists.txt:1) to use Qt6 imported targets instead of `Qt6_FOUND`:

```cmake
# Find Qt6 (optional) and Vulkan (optional)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)

    # Use Qt6 imported targets for checking
    if(TARGET Qt6::Core)
        message(STATUS "Qt6 found - Qt6 integration enabled")
        set(OMNICPP_USE_QT6 ON CACHE BOOL "Use Qt6" FORCE)
    else()
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()

    # Qt6 Vulkan integration requires both Qt6 and Vulkan
    # Use TARGET check instead of Qt6_FOUND
    if(TARGET Qt6::Core AND Vulkan_FOUND)
        message(STATUS "Qt6 and Vulkan found - Qt6 Vulkan integration enabled")
        set(OMNICPP_USE_QT_VULKAN ON CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    else()
        message(WARNING "Qt6 Vulkan integration requires both Qt6 and Vulkan - Qt6 Vulkan integration disabled")
        set(OMNICPP_USE_QT_VULKAN OFF CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    endif()
endif()
```

**Option 2: Propagate Qt6_FOUND from Root CMakeLists.txt**
Modify root [`CMakeLists.txt`](CMakeLists.txt:1) to propagate `Qt6_FOUND` to engine subdirectory:

```cmake
# Qt6 Configuration
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)
    
    if(Qt6_FOUND)
        message(STATUS "Qt6 found: ${Qt6_VERSION}")
        # Propagate Qt6_FOUND to subdirectories
        set(Qt6_FOUND ${Qt6_FOUND} PARENT_SCOPE)
    else()
        message(FATAL_ERROR "Qt6 not found")
    endif()
endif()
```

### 8.2 Fix for Deprecated Qt6 API Usage

**Issue:** `examples/pong/pong_game.cpp` uses deprecated `stateChanged` API

**Proposed Fix:**
Replace `stateChanged` with `checkStateChanged` as per Qt6 documentation.

**File:** [`examples/pong/pong_game.cpp`](examples/pong/pong_game.cpp:1)

**Search Pattern:**
```cpp
stateChanged
```

**Replace With:**
```cpp
checkStateChanged
```

### 8.3 Fix for Test Files

**Issues:**
1. `tests/unit/test_audio_manager.cpp` - Duplicate test definitions
2. `tests/unit/test_resource_manager.cpp` - Missing member variable `resource_manager_`
3. `tests/unit/test_ecs.cpp` - Undefined reference to `test::EntityTest::SetUp()`

**Proposed Fix:**
Review and fix each test file to resolve the identified issues.

---

## Security Considerations

### 9.1 Wayland-Specific Security Considerations

**From Threat Model Analysis:**

**TM-LX-002: Distribution-Specific Vulnerabilities**
- Wayland compositor security considerations
- Input handling security
- Window state management security

**Best Practices for Wayland Testing:**
1. **Environment Variable Validation:**
   - Validate `QT_QPA_PLATFORM` before running game
   - Ensure `QT_QPA_PLATFORM=wayland` is set correctly

2. **Input Validation:**
   - Validate all keyboard and mouse input
   - Prevent input injection attacks

3. **Window State Management:**
   - On Wayland, the compositor controls window state
   - Application cannot force window state changes
   - Use `requestActivate()` instead of `setWindowState()`

4. **Surface Creation:**
   - Use proper Wayland surface extension (`VK_KHR_wayland_surface`)
   - Validate surface creation success

### 9.2 Build System Security Considerations

**TM-001: Malicious Package Injection**
- Ensure all dependencies are from trusted sources
- Use exact version pinning for all dependencies
- Implement package signature verification

**TM-004: Dependency Confusion Attack**
- Use scoped package names for internal packages
- Configure private repositories with highest priority
- Pin all dependency versions to exact versions

---

## Recommendations

### 10.1 Immediate Actions

1. **Fix CMake Configuration Issue (BUILD-001)**
   - Implement Option 1 or Option 2 from section 8.1
   - Rebuild engine library with `OMNICPP_HAS_QT_VULKAN` defined
   - Verify `WindowManager` methods are present in engine library

2. **Fix Deprecated Qt6 API Usage (PREEXIST-001)**
   - Replace `stateChanged` with `checkStateChanged`
   - Rebuild pong example

3. **Fix Test Files**
   - Resolve duplicate test definitions in `test_audio_manager.cpp`
   - Add missing member variable `resource_manager_` in `test_resource_manager.cpp`
   - Fix undefined reference in `test_ecs.cpp`

### 10.2 Short-term Actions

1. **Test Game on Wayland After Fixes**
   - Execute all planned tests after build issues are resolved
   - Verify window visibility on Wayland
   - Verify 3D graphics rendering on Wayland
   - Verify game controllability on Wayland
   - Verify statistics overlay on Wayland
   - Verify Qt configuration windows on Wayland

2. **Performance Testing**
   - Measure FPS performance on Wayland
   - Compare with X11 performance (if available)
   - Identify any Wayland-specific performance issues

3. **Cross-Platform Testing**
   - Test on various Wayland compositors (GNOME, KDE, Sway, etc.)
   - Test on X11 for backward compatibility
   - Document any platform-specific issues

### 10.3 Long-term Actions

1. **Automated Testing**
   - Set up automated Wayland testing in CI/CD
   - Add performance benchmarks
   - Add regression tests for Wayland-specific features

2. **Documentation Updates**
   - Document Wayland-specific build requirements
   - Document Wayland-specific troubleshooting steps
   - Add Wayland testing procedures to developer guide

3. **Security Enhancements**
   - Implement package signature verification
   - Add dependency validation in CI/CD
   - Implement input validation for all user input

---

## Conclusion

The QA testing of the OmniCpp 3D Pong game on Wayland compositor was **BLOCKED** due to a **critical build system issue**. The root cause is a CMake configuration issue where the `Qt6_FOUND` variable is not being set properly in the engine's CMakeLists.txt, causing the engine library to be built without Qt6 Vulkan-specific methods.

**Key Findings:**
- ✅ Wayland compositor is available and running (KWin Wayland)
- ✅ Qt6 is installed and available (version 6.10.2)
- ✅ Vulkan is installed and available (version 1.4.335.0)
- ✅ Engine library builds successfully
- ❌ Pong example cannot be built due to undefined references to `WindowManager` methods
- ❌ All Wayland-specific tests are blocked due to build failure

**Status:** BLOCKED - Pre-existing build issue prevents testing

**Next Steps:**
1. Fix CMake configuration issue (BUILD-001)
2. Fix deprecated Qt6 API usage (PREEXIST-001)
3. Rebuild pong example
4. Execute all planned Wayland tests
5. Document test results

---

**Report Generated:** 2026-02-01T21:47:00.000Z  
**Generated By:** QA Specialist  
**Task Reference:** Test game on Wayland compositor (window visibility, 3D graphics, controllability, statistics overlay, Qt configuration windows)

---

## References

- [Threat Model Analysis](.specs/03_threat_model/analysis.md)
- [Coding Standards](.specs/01_standards/coding_standards.md)
- [CPP23 Standard Upgrade Report](CPP23_STANDARD_UPGRADE_REPORT.md)
- [Wayland Pong 3D Implementation Report](WAYLAND_PONG_3D_IMPLEMENTATION_REPORT.md)
- [Wayland Vulkan Fix Report](WAYLAND_VULKAN_FIX_REPORT.md)
- [Wayland Vulkan Rendering Window State Interactivity Fix Report](WAYLAND_VULKAN_RENDERING_WINDOW_STATE_INTERACTIVITY_FIX_REPORT.md)
- [Wayland Window State FPS Fix Report](WAYLAND_WINDOW_STATE_FPS_FIX_REPORT.md)
- [Wayland Window Visibility Fix Report](WAYLAND_WINDOW_VISIBILITY_FIX_REPORT.md)
- [Qt6 Wayland Platform](https://doc.qt.io/qt-6/linux-requirements.html)
- [Vulkan Wayland Specification](https://www.khronos.org/registry/vulkan/specs/1.3/html/chap34.html)
