# REQ-002: flake.nix Enhancement

**Requirement ID:** REQ-002
**Title:** flake.nix Enhancement
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

The [`flake.nix`](../../flake.nix:1) file shall be enhanced to provide a comprehensive, reproducible C++ development environment for CachyOS, including GCC and Clang toolchains, Qt6 and Vulkan dependencies, development shell configuration, CMake integration, and Conan integration.

### Overview

The system shall:
1. Define CachyOS-specific packages and versions
2. Define complete GCC toolchain with multiple versions
3. Define complete Clang toolchain with multiple versions
4. Define comprehensive Qt6 dependencies
5. Define comprehensive Vulkan dependencies
6. Define development shell with proper environment setup
7. Configure CMake integration for Nix environment
8. Configure Conan integration for Nix environment

---

## REQ-002-001: Define CachyOS-Specific Packages

### Description

The [`flake.nix`](../../flake.nix:1) shall define CachyOS-specific packages and versions to ensure reproducible builds on CachyOS platform.

### Functional Requirements

The system shall:
1. Specify Nixpkgs input as `nixos-unstable` branch
2. Pin specific Nixpkgs commit via [`flake.lock`](../../flake.lock:1)
3. Define system as `x86_64-linux`
4. Include CachyOS-specific kernel headers if available
5. Include CachyOS-specific performance tools if available
6. Document CachyOS-specific packages in comments
7. Provide separate shell for CachyOS if needed
8. Log CachyOS-specific package loading

### Acceptance Criteria

- [ ] Nixpkgs input is `nixos-unstable`
- [ ] System is defined as `x86_64-linux`
- [ ] [`flake.lock`](../../flake.lock:1) pins specific Nixpkgs commit
- [ ] CachyOS-specific packages are documented in comments
- [ ] Shell loads successfully on CachyOS
- [ ] All packages are available in Nix store

### Priority

**Critical** - CachyOS-specific packages ensure platform compatibility.

### Dependencies

- None

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Integration Tests

1. **Test Flake Loads on CachyOS**
   - **Description:** Verify flake loads successfully on CachyOS
   - **Steps:**
     1. Run `nix flake show` on CachyOS
     2. Verify no errors
     3. Verify all packages are listed
   - **Expected Result:** Flake loads successfully

2. **Test Flake Lock Validity**
   - **Description:** Verify [`flake.lock`](../../flake.lock:1) is valid
   - **Steps:**
     1. Run `nix flake lock --update-input nixpkgs`
     2. Verify lock file updates
     3. Verify commit hash is valid
   - **Expected Result:** Lock file is valid

---

## REQ-002-002: Define GCC Toolchain

### Description

The [`flake.nix`](../../flake.nix:1) shall define a complete GCC toolchain with multiple versions for C++23 development.

### Functional Requirements

The system shall:
1. Include `gcc` package (default GCC)
2. Include `gcc13` package (latest stable GCC)
3. Include `g++` package (GNU C++ compiler)
4. Include `gcc13Stdenv` for complete GCC environment
5. Include `gnumake` for make-based builds
6. Include `binutils` for binary utilities
7. Provide separate GCC toolchain shell
8. Set `CC=gcc` and `CXX=g++` in GCC shell
9. Set `CMAKE_C_COMPILER=gcc` and `CMAKE_CXX_COMPILER=g++` in GCC shell

### Acceptance Criteria

- [ ] `gcc` package is included in buildInputs
- [ ] `gcc13` package is included in buildInputs
- [ ] `g++` package is available
- [ ] `gnumake` package is included in buildInputs
- [ ] `binutils` package is included in buildInputs
- [ ] Separate GCC toolchain shell exists
- [ ] GCC shell sets `CC=gcc` and `CXX=g++`
- [ ] GCC shell sets CMake compiler variables

### Priority

**Critical** - GCC toolchain is required for C++23 development.

### Dependencies

- None

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-016: C++23 Without Modules](../02_adrs/ADR-016-cpp23-without-modules.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test GCC Availability**
   - **Description:** Verify GCC is available in Nix shell
   - **Steps:**
     1. Run `nix develop`
     2. Run `gcc --version`
     3. Verify GCC version is displayed
   - **Expected Result:** GCC is available

2. **Test GCC Toolchain Shell**
   - **Description:** Verify GCC toolchain shell works
   - **Steps:**
     1. Run `nix develop .#gcc`
     2. Run `echo $CC`
     3. Verify `CC=gcc`
     4. Run `echo $CXX`
     5. Verify `CXX=g++`
   - **Expected Result:** GCC toolchain shell configured

---

## REQ-002-003: Define Clang Toolchain

### Description

The [`flake.nix`](../../flake.nix:1) shall define a complete Clang toolchain with multiple versions for C++23 development.

### Functional Requirements

The system shall:
1. Include `clang` package (default Clang)
2. Include `llvmPackages_19.clang` package (latest stable Clang)
3. Include `llvmPackages_19.llvm` package (LLVM infrastructure)
4. Include `llvmPackages_19.bintools` package (LLVM binary tools)
5. Include `clang-tools` package (clang-format, clang-tidy)
6. Provide separate Clang toolchain shell
7. Set `CC=clang` and `CXX=clang++` in Clang shell
8. Set `CMAKE_C_COMPILER=clang` and `CMAKE_CXX_COMPILER=clang++` in Clang shell

### Acceptance Criteria

- [ ] `clang` package is included in buildInputs
- [ ] `llvmPackages_19.clang` package is included in buildInputs
- [ ] `llvmPackages_19.llvm` package is included in buildInputs
- [ ] `llvmPackages_19.bintools` package is included in buildInputs
- [ ] `clang-tools` package is included in buildInputs
- [ ] Separate Clang toolchain shell exists
- [ ] Clang shell sets `CC=clang` and `CXX=clang++`
- [ ] Clang shell sets CMake compiler variables

### Priority

**Critical** - Clang toolchain is required for C++23 development.

### Dependencies

- None

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-016: C++23 Without Modules](../02_adrs/ADR-016-cpp23-without-modules.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Clang Availability**
   - **Description:** Verify Clang is available in Nix shell
   - **Steps:**
     1. Run `nix develop`
     2. Run `clang --version`
     3. Verify Clang version is displayed
   - **Expected Result:** Clang is available

2. **Test Clang Toolchain Shell**
   - **Description:** Verify Clang toolchain shell works
   - **Steps:**
     1. Run `nix develop .#clang`
     2. Run `echo $CC`
     3. Verify `CC=clang`
     4. Run `echo $CXX`
     5. Verify `CXX=clang++`
   - **Expected Result:** Clang toolchain shell configured

---

## REQ-002-004: Define Qt6 Dependencies

### Description

The [`flake.nix`](../../flake.nix:1) shall define comprehensive Qt6 dependencies for GUI and graphics development.

### Functional Requirements

The system shall:
1. Include `qt6.qtbase` package (Qt6 base libraries)
2. Include `qt6.qttools` package (Qt6 tools)
3. Include `qt6.qtdeclarative` package (Qt Quick/QML)
4. Include `qt6.qtwayland` package (Wayland support)
5. Include `qt6.qtsvg` package (SVG support)
6. Include `qt6.qtimageformats` package (image format support)
7. Set `QT_QPA_PLATFORM=wayland` environment variable
8. Set `QT_PLUGIN_PATH` to Nix Qt plugins directory
9. Set `QMAKE` to Nix qmake path
10. Set `CMAKE_PREFIX_PATH` to include Qt6

### Acceptance Criteria

- [ ] `qt6.qtbase` package is included in buildInputs
- [ ] `qt6.qttools` package is included in buildInputs
- [ ] `qt6.qtdeclarative` package is included in buildInputs
- [ ] `qt6.qtwayland` package is included in buildInputs
- [ ] `qt6.qtsvg` package is included in buildInputs
- [ ] `qt6.qtimageformats` package is included in buildInputs
- [ ] `QT_QPA_PLATFORM=wayland` is set in shellHook
- [ ] `QT_PLUGIN_PATH` is set to Nix Qt plugins
- [ ] `QMAKE` is set to Nix qmake path
- [ ] `CMAKE_PREFIX_PATH` includes Qt6

### Priority

**Critical** - Qt6 is required for GUI development.

### Dependencies

- None

### Related ADRs

- [ADR-034: Qt6 and Vulkan Integration](../04_future_state/reqs/REQ-034-qt6-vulkan-integration.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Qt6 Availability**
   - **Description:** Verify Qt6 is available in Nix shell
   - **Steps:**
     1. Run `nix develop`
     2. Run `qmake --version`
     3. Verify Qt6 version is displayed
   - **Expected Result:** Qt6 is available

2. **Test Qt6 Environment Variables**
   - **Description:** Verify Qt6 environment variables are set
   - **Steps:**
     1. Run `nix develop`
     2. Run `echo $QT_QPA_PLATFORM`
     3. Verify `QT_QPA_PLATFORM=wayland`
     4. Run `echo $QT_PLUGIN_PATH`
     5. Verify path points to Nix store
   - **Expected Result:** Qt6 environment variables are set

---

## REQ-002-005: Define Vulkan Dependencies

### Description

The [`flake.nix`](../../flake.nix:1) shall define comprehensive Vulkan dependencies for graphics development.

### Functional Requirements

The system shall:
1. Include `vulkan-headers` package (Vulkan header files)
2. Include `vulkan-loader` package (Vulkan loader library)
3. Include `vulkan-tools` package (Vulkan command-line tools)
4. Include `vulkan-validation-layers` package (Vulkan validation layers)
5. Include `vulkan-extension-layer` package (Vulkan extension layer)
6. Include `mesa` package (Mesa graphics drivers)
7. Include `glslang` package (GLSL to SPIR-V compiler)
8. Include `spirv-tools` package (SPIR-V tools)
9. Set `VK_LAYER_PATH` to Nix validation layers directory
10. Set `VK_ICD_FILENAMES` to Nix ICD files

### Acceptance Criteria

- [ ] `vulkan-headers` package is included in buildInputs
- [ ] `vulkan-loader` package is included in buildInputs
- [ ] `vulkan-tools` package is included in buildInputs
- [ ] `vulkan-validation-layers` package is included in buildInputs
- [ ] `vulkan-extension-layer` package is included in buildInputs
- [ ] `mesa` package is included in buildInputs
- [ ] `glslang` package is included in buildInputs
- [ ] `spirv-tools` package is included in buildInputs
- [ ] `VK_LAYER_PATH` is set in shellHook
- [ ] `VK_ICD_FILENAMES` is set in shellHook

### Priority

**Critical** - Vulkan is required for graphics development.

### Dependencies

- None

### Related ADRs

- [ADR-034: Qt6 and Vulkan Integration](../04_future_state/reqs/REQ-034-qt6-vulkan-integration.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Vulkan Availability**
   - **Description:** Verify Vulkan is available in Nix shell
   - **Steps:**
     1. Run `nix develop`
     2. Run `vulkaninfo`
     3. Verify Vulkan information is displayed
   - **Expected Result:** Vulkan is available

2. **Test Vulkan Environment Variables**
   - **Description:** Verify Vulkan environment variables are set
   - **Steps:**
     1. Run `nix develop`
     2. Run `echo $VK_LAYER_PATH`
     3. Verify path points to Nix store
     4. Run `echo $VK_ICD_FILENAMES`
     5. Verify path points to Nix store
   - **Expected Result:** Vulkan environment variables are set

---

## REQ-002-006: Define Development Shell

### Description

The [`flake.nix`](../../flake.nix:1) shall define a comprehensive development shell that includes all required packages and sets up the environment correctly.

### Functional Requirements

The system shall:
1. Define `devShells.${system}.default` as default shell
2. Include all compiler packages (GCC, Clang)
3. Include all build system packages (CMake, Ninja, ccache)
4. Include all package manager packages (Conan, Python, pip)
5. Include all Qt6 packages
6. Include all Vulkan packages
7. Include documentation tools (Doxygen, graphviz)
8. Include code quality tools (clang-tools, cppcheck)
9. Include testing tools (gtest, gmock, pytest)
10. Include debugging tools (gdb, lldb, valgrind)
11. Include performance tools (perf-tools, hotspot)
12. Set shell name to "omnicpp-cachyos-dev"
13. Display welcome message with platform information
14. Set all required environment variables in shellHook
15. Log shell loading at INFO level

### Acceptance Criteria

- [ ] `devShells.${system}.default` is defined
- [ ] All compiler packages are included
- [ ] All build system packages are included
- [ ] All package manager packages are included
- [ ] All Qt6 packages are included
- [ ] All Vulkan packages are included
- [ ] Documentation tools are included
- [ ] Code quality tools are included
- [ ] Testing tools are included
- [ ] Debugging tools are included
- [ ] Performance tools are included
- [ ] Shell name is "omnicpp-cachyos-dev"
- [ ] Welcome message is displayed
- [ ] All environment variables are set
- [ ] Shell loads without errors

### Priority

**Critical** - Development shell is essential for reproducible builds.

### Dependencies

- REQ-002-001: Define CachyOS-specific packages
- REQ-002-002: Define GCC toolchain
- REQ-002-003: Define Clang toolchain
- REQ-002-004: Define Qt6 dependencies
- REQ-002-005: Define Vulkan dependencies

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Integration Tests

1. **Test Development Shell Loads**
   - **Description:** Verify development shell loads successfully
   - **Steps:**
     1. Run `nix develop`
     2. Verify welcome message is displayed
     3. Verify no errors occur
   - **Expected Result:** Shell loads successfully

2. **Test All Tools Available**
   - **Description:** Verify all tools are available in shell
   - **Steps:**
     1. Run `nix develop`
     2. Run `gcc --version`
     3. Run `clang --version`
     4. Run `cmake --version`
     5. Run `ninja --version`
     6. Run `conan --version`
     7. Verify all commands succeed
   - **Expected Result:** All tools are available

---

## REQ-002-007: Configure CMake Integration

### Description

The [`flake.nix`](../../flake.nix:1) shall configure CMake to work correctly with Nix-provided packages and toolchains.

### Functional Requirements

The system shall:
1. Set `CMAKE_GENERATOR="Ninja"` environment variable
2. Set `CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)` environment variable
3. Set `CMAKE_PREFIX_PATH` to include Qt6 and Vulkan
4. Set `CMAKE_LIBRARY_PATH` to include Nix library paths
5. Set `CMAKE_INCLUDE_PATH` to include Nix include paths
6. Set `CMAKE_C_COMPILER` based on selected toolchain
7. Set `CMAKE_CXX_COMPILER` based on selected toolchain
8. Set `CMAKE_EXPORT_COMPILE_COMMANDS=ON` for IDE support
9. Set `CCACHE_DIR=$PWD/.ccache` for compiler cache
10. Log CMake configuration at DEBUG level

### Acceptance Criteria

- [ ] `CMAKE_GENERATOR="Ninja"` is set in shellHook
- [ ] `CMAKE_BUILD_PARALLEL_LEVEL` is set in shellHook
- [ ] `CMAKE_PREFIX_PATH` includes Qt6 and Vulkan
- [ ] `CMAKE_LIBRARY_PATH` includes Nix library paths
- [ ] `CMAKE_INCLUDE_PATH` includes Nix include paths
- [ ] `CMAKE_C_COMPILER` is set based on toolchain
- [ ] `CMAKE_CXX_COMPILER` is set based on toolchain
- [ ] `CMAKE_EXPORT_COMPILE_COMMANDS=ON` is set
- [ ] `CCACHE_DIR` is set in shellHook
- [ ] CMake configuration is logged

### Priority

**High** - CMake integration ensures correct build configuration.

### Dependencies

- REQ-002-006: Define development shell

### Related ADRs

- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-036: CMake Preset Expansion](../02_adrs/ADR-036-cmake-preset-expansion.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test CMake Configuration**
   - **Description:** Verify CMake is configured correctly
   - **Steps:**
     1. Run `nix develop`
     2. Run `echo $CMAKE_GENERATOR`
     3. Verify `CMAKE_GENERATOR=Ninja`
     4. Run `echo $CMAKE_BUILD_PARALLEL_LEVEL`
     5. Verify parallel level is set
   - **Expected Result:** CMake is configured correctly

2. **Test CMake Find Qt6**
   - **Description:** Verify CMake can find Qt6
   - **Steps:**
     1. Run `nix develop`
     2. Create test CMakeLists.txt with `find_package(Qt6)`
     3. Run `cmake .`
     4. Verify Qt6 is found
   - **Expected Result:** CMake finds Qt6

---

## REQ-002-008: Configure Conan Integration

### Description

The [`flake.nix`](../../flake.nix:1) shall configure Conan to work correctly with Nix-provided packages and toolchains.

### Functional Requirements

The system shall:
1. Set `CONAN_USER_HOME=$PWD/.conan2` environment variable
2. Set `CONAN_REVISIONS_ENABLED=1` environment variable
3. Set `CONAN_V2_MODE=1` environment variable
4. Set `CONAN_CPU_COUNT=$(nproc)` environment variable
5. Configure Conan to use Nix toolchain
6. Configure Conan to use Nix libraries
7. Configure Conan cache directory
8. Log Conan configuration at DEBUG level
9. Provide Conan profile for Nix environment

### Acceptance Criteria

- [ ] `CONAN_USER_HOME` is set in shellHook
- [ ] `CONAN_REVISIONS_ENABLED=1` is set in shellHook
- [ ] `CONAN_V2_MODE=1` is set in shellHook
- [ ] `CONAN_CPU_COUNT` is set in shellHook
- [ ] Conan is configured to use Nix toolchain
- [ ] Conan is configured to use Nix libraries
- [ ] Conan cache directory is configured
- [ ] Conan configuration is logged
- [ ] Conan profile for Nix exists

### Priority

**High** - Conan integration ensures package management works correctly.

### Dependencies

- REQ-002-006: Define development shell

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)

### Related Threats

- **TM-001: Malicious Package Injection (Conan)** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:156)

### Test Cases

#### Integration Tests

1. **Test Conan Configuration**
   - **Description:** Verify Conan is configured correctly
   - **Steps:**
     1. Run `nix develop`
     2. Run `echo $CONAN_USER_HOME`
     3. Verify path points to project directory
     4. Run `echo $CONAN_V2_MODE`
     5. Verify `CONAN_V2_MODE=1`
   - **Expected Result:** Conan is configured correctly

2. **Test Conan Install**
   - **Description:** Verify Conan can install packages
   - **Steps:**
     1. Run `nix develop`
     2. Run `conan install .`
     3. Verify packages are installed
     4. Verify no errors occur
   - **Expected Result:** Conan installs packages successfully

---

## Implementation Notes

### Complete flake.nix Structure

```nix
{
  description = "C++ Dev Environment with Qt6, Vulkan, GCC, and Clang";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        name = "omnicpp-cachyos-dev";

        buildInputs = with pkgs; [
          # Compilers
          gcc
          clang
          gcc13
          llvmPackages_19.clang

          # Build System
          cmake
          ninja
          ccache

          # Package Managers
          conan
          python3
          python3Packages.pip

          # Documentation
          doxygen
          graphviz

          # Code Quality
          clang-tools
          cppcheck

          # Qt6
          qt6.qtbase
          qt6.qttools
          qt6.qtdeclarative
          qt6.qtwayland
          qt6.qtsvg
          qt6.qtimageformats

          # Vulkan
          vulkan-headers
          vulkan-loader
          vulkan-tools
          vulkan-validation-layers
          vulkan-extension-layer

          # Graphics
          mesa
          glslang
          spirv-tools

          # Testing
          gtest
          gmock
          pytest

          # Debugging
          gdb
          lldb
          valgrind

          # Performance
          perf-tools
          hotspot
        ];

        shellHook = ''
          echo ">> Loaded OmniCPP C++ Development Environment (CachyOS)"
          echo ">> Platform: Linux (CachyOS)"
          echo ">> Compilers: GCC 13, Clang 19"
          echo ">> Qt6: Latest stable"
          echo ">> Vulkan: Latest stable"

          # Qt6 environment
          export QT_QPA_PLATFORM=wayland
          export QT_PLUGIN_PATH=${pkgs.qt6.qtbase}/lib/qt-6/plugins

          # Vulkan environment
          export VK_LAYER_PATH=${pkgs.vulkan-validation-layers}/share/vulkan/explicit_layer.d
          export VK_ICD_FILENAMES=${pkgs.vulkan-loader}/share/vulkan/icd.d/intel_icd.x86_64.json

          # CMake defaults
          export CMAKE_GENERATOR="Ninja"
          export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)
          export CMAKE_PREFIX_PATH="${pkgs.qt6.qtbase}:${pkgs.vulkan-headers}:$CMAKE_PREFIX_PATH"
          export CMAKE_LIBRARY_PATH="${pkgs.qt6.qtbase}/lib:${pkgs.vulkan-loader}/lib:$CMAKE_LIBRARY_PATH"
          export CMAKE_INCLUDE_PATH="${pkgs.qt6.qtbase}/include:${pkgs.vulkan-headers}/include:$CMAKE_INCLUDE_PATH"
          export CMAKE_EXPORT_COMPILE_COMMANDS=ON

          # Compiler cache
          export CCACHE_DIR=$PWD/.ccache

          # Conan environment
          export CONAN_USER_HOME=$PWD/.conan2
          export CONAN_REVISIONS_ENABLED=1
          export CONAN_V2_MODE=1
          export CONAN_CPU_COUNT=$(nproc)

          echo ">> Environment ready!"
        '';
      };

      # GCC toolchain shell
      devShells.${system}.gcc = pkgs.mkShell {
        name = "omnicpp-gcc-toolchain";

        buildInputs = with pkgs; [
          gcc13
          gnumake
          ninja
        ];

        shellHook = ''
          export CC=gcc
          export CXX=g++
          export CMAKE_C_COMPILER=gcc
          export CMAKE_CXX_COMPILER=g++
          echo ">> GCC toolchain configured"
        '';
      };

      # Clang toolchain shell
      devShells.${system}.clang = pkgs.mkShell {
        name = "omnicpp-clang-toolchain";

        buildInputs = with pkgs; [
          llvmPackages_19.clang
          llvmPackages_19.clang-tools
          ninja
        ];

        shellHook = ''
          export CC=clang
          export CXX=clang++
          export CMAKE_C_COMPILER=clang
          export CMAKE_CXX_COMPILER=clang++
          echo ">> Clang toolchain configured"
        '';
      };
    };
}
```

### Direnv Integration

Create or update [`.envrc`](../../.envrc:1) file:

```bash
use flake
```

This automatically loads the Nix environment when entering the project directory.

### Environment Variables Summary

| Variable | Purpose | Value |
|----------|---------|-------|
| `QT_QPA_PLATFORM` | Qt platform backend | `wayland` |
| `QT_PLUGIN_PATH` | Qt plugins directory | Nix Qt plugins path |
| `VK_LAYER_PATH` | Vulkan validation layers | Nix validation layers path |
| `VK_ICD_FILENAMES` | Vulkan ICD files | Nix ICD files path |
| `CMAKE_GENERATOR` | CMake generator | `Ninja` |
| `CMAKE_BUILD_PARALLEL_LEVEL` | CMake parallel jobs | `$(nproc)` |
| `CMAKE_PREFIX_PATH` | CMake prefix paths | Qt6, Vulkan paths |
| `CMAKE_LIBRARY_PATH` | CMake library paths | Nix library paths |
| `CMAKE_INCLUDE_PATH` | CMake include paths | Nix include paths |
| `CMAKE_EXPORT_COMPILE_COMMANDS` | Export compile commands | `ON` |
| `CCACHE_DIR` | Compiler cache directory | `$PWD/.ccache` |
| `CONAN_USER_HOME` | Conan home directory | `$PWD/.conan2` |
| `CONAN_REVISIONS_ENABLED` | Conan revisions | `1` |
| `CONAN_V2_MODE` | Conan v2 mode | `1` |
| `CONAN_CPU_COUNT` | Conan CPU count | `$(nproc)` |

### Shell Commands

- **Load default shell:** `nix develop`
- **Load GCC shell:** `nix develop .#gcc`
- **Load Clang shell:** `nix develop .#clang`
- **Update flake lock:** `nix flake lock --update-input nixpkgs`
- **Show flake info:** `nix flake show`

### Logging

All shell operations shall be logged:
- Shell loading: INFO level (welcome message)
- Environment variable setting: DEBUG level
- Toolchain configuration: INFO level
- CMake configuration: DEBUG level
- Conan configuration: DEBUG level

### Error Handling

The system shall handle the following error conditions:
- Missing packages in Nixpkgs
- Version conflicts between packages
- Nix store corruption
- Environment variable conflicts
- Shell hook failures

All errors shall be logged with appropriate severity and provide actionable error messages.

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)
- [ADR-034: Conan Profile Expansion](../02_adrs/ADR-034-conan-profile-expansion.md)
- [ADR-036: CMake Preset Expansion](../02_adrs/ADR-036-cmake-preset-expansion.md)
- [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md) - Threat Model Analysis

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
