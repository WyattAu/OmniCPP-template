# Windows Scripts Archive

**Archive Date:** 2026-01-28  
**Purpose:** Archive Windows-specific build scripts and profiles  
**Reference:** ADR-028 - Linux Platform Support  
**Requirement:** REQ-009-001 - Repository Cleanup

---

## Overview

This directory contains Windows-specific build scripts, profiles, and toolchains that have been archived as part of the Linux platform support expansion. These files are preserved for historical reference and potential future Windows support restoration, but are not actively maintained.

---

## Archived Files

### Conan Setup Scripts (`conan/`)

| File | Purpose | Original Location |
|------|---------|-------------------|
| `setup_clang_mingw_ucrt.bat` | Clang with MinGW UCRT environment setup | `conan/` |
| `setup_clang_mingw.bat` | Clang with MinGW environment setup | `conan/` |
| `setup_clang.bat` | Clang compiler environment setup | `conan/` |
| `setup_emscripten.bat` | Emscripten (WASM) Windows environment setup | `conan/` |
| `setup_gcc_mingw_ucrt.bat` | GCC with MinGW UCRT environment setup | `conan/` |
| `setup_gcc_mingw.bat` | GCC with MinGW environment setup | `conan/` |
| `setup_msvc.bat` | Microsoft Visual C++ environment setup | `conan/` |

### Conan Profiles (`conan/profiles/`)

| Profile | Purpose | Compiler/Toolchain |
|---------|---------|-------------------|
| `clang-msvc` | Clang with MSVC runtime | Clang + MSVC |
| `clang-msvc-debug` | Debug build with Clang/MSVC | Clang + MSVC (Debug) |
| `clang-msvc-release` | Release build with Clang/MSVC | Clang + MSVC (Release) |
| `gcc-mingw-ucrt` | GCC with MinGW UCRT runtime | GCC + MinGW UCRT |
| `mingw-clang-debug` | Debug build with MinGW/Clang | Clang + MinGW (Debug) |
| `mingw-clang-release` | Release build with MinGW/Clang | Clang + MinGW (Release) |
| `mingw-gcc-release` | Release build with MinGW/GCC | GCC + MinGW (Release) |
| `msvc` | MSVC default profile | MSVC |
| `msvc-debug` | MSVC debug profile | MSVC (Debug) |
| `msvc-release` | MSVC release profile | MSVC (Release) |

### CMake Toolchains (`cmake/toolchains/`)

| File | Purpose | Target Platform |
|------|---------|------------------|
| `arm64-windows-msvc.cmake` | ARM64 Windows toolchain for MSVC | Windows ARM64 |

### Test Files (`root/`)

| File | Purpose | Compiler |
|------|---------|----------|
| `test_mingw_clang.cpp` | Compiler detection test for MinGW/Clang | Clang + MinGW |
| `test_mingw_gcc.cpp` | Compiler detection test for MinGW/GCC | GCC + MinGW |
| `test_msvc.cpp` | Compiler detection test for MSVC | MSVC |

---

## Archival Reason

Per **ADR-028: Linux Platform Support**, the project is transitioning to Linux-first development with CachyOS as the primary target platform. The Windows-specific files have been archived to:

1. **Reduce repository complexity** by removing platform-specific artifacts
2. **Focus development efforts** on Linux toolchains and workflows
3. **Improve build system clarity** by eliminating Windows-specific branching logic
4. **Preserve historical artifacts** for potential future Windows support restoration

---

## Restoration Instructions

If Windows support needs to be restored in the future:

1. **Restore files** from this archive to their original locations
2. **Update documentation** to include Windows build instructions
3. **Update CI/CD pipelines** to include Windows build targets
4. **Update VSCode configurations** to include Windows task variants
5. **Update CMake presets** to include Windows configurations
6. **Revert ADR-028** or create a new ADR for multi-platform support

---

## Retained Linux Scripts

The following scripts remain active in the main repository:

- `conan/setup_emscripten.sh` - Emscripten Linux environment setup
- `conan/profiles/cachyos` - CachyOS Linux profile
- `conan/profiles/cachyos-clang` - CachyOS with Clang
- `conan/profiles/cachyos-clang-debug` - CachyOS Clang debug
- `conan/profiles/cachyos-debug` - CachyOS debug
- `conan/profiles/clang-linux` - Linux Clang profile
- `conan/profiles/clang-linux-debug` - Linux Clang debug
- `conan/profiles/emscripten` - Emscripten (WASM) profile
- `conan/profiles/gcc-linux` - Linux GCC profile
- `conan/profiles/gcc-linux-debug` - Linux GCC debug
- `cmake/toolchains/arm64-linux-gnu.cmake` - ARM64 Linux toolchain
- `cmake/toolchains/clang-linux.cmake` - Clang Linux toolchain
- `cmake/toolchains/emscripten.cmake` - Emscripten toolchain
- `cmake/toolchains/x86-linux-gnu.cmake` - x86 Linux toolchain

---

## Related Documentation

- **ADR-028:** Linux Platform Support (`.specs/02_adrs/ADR-028-linux-platform-support.md`)
- **REQ-009-001:** Repository Cleanup (`.specs/04_future_state/reqs/REQ-009-cleanup.md`)
- **Linux Expansion Manifest:** (`.specs/04_future_state/linux_expansion_manifest.md`)
- **Coding Standards:** (`.specs/01_standards/coding_standards.md`)

---

## Contact

For questions about this archive or Windows support restoration, refer to the project documentation or contact the development team.
