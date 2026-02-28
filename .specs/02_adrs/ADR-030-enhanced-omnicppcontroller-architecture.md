# ADR-030: Enhanced OmniCppController.py Architecture

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Build Controller Architecture Enhancement

---

## Context

The [`OmniCppController.py`](../../OmniCppController.py:1) is the single entry point for all build operations in the OmniCPP Template project. Currently, the controller is primarily Windows-centric with the following characteristics:

### Current State

1. **Windows-First Design:** Optimized for MSVC, MSVC-clang, MinGW-GCC, MinGW-Clang
2. **Limited Linux Support:** Basic GCC and Clang support exists but is not comprehensive
3. **No Nix Integration:** Does not detect or integrate with Nix environments
4. **No Distribution Detection:** Does not detect Linux distributions (CachyOS, Ubuntu, etc.)
5. **No Package Manager Detection:** Does not detect system package managers (pacman, apt, dnf)
6. **No CachyOS Optimizations:** Does not apply CachyOS-specific compiler flags
7. **No Environment Validation:** Does not validate Nix or direnv environments

### Linux Expansion Requirements

The Linux expansion requires the controller to:

1. **Detect Linux Distributions:** Identify CachyOS, Arch, Ubuntu, Fedora, etc.
2. **Detect Nix Environment:** Check if running in Nix shell
3. **Detect Direnv:** Check if direnv environment is active
4. **Apply CachyOS Optimizations:** Use CachyOS-specific compiler flags
5. **Integrate with Nix:** Use Nix-provided toolchain when available
6. **Support Multiple Toolchains:** GCC, Clang, with Nix and system variants
7. **Validate Environment:** Ensure all required tools are available
8. **Provide Linux-Specific Help:** Show Linux-specific help and examples

### Architectural Challenges

1. **Complexity:** Adding Linux support increases complexity significantly
2. **Maintainability:** More code paths to maintain
3. **Testing:** More platforms to test
4. **Documentation:** More documentation required
5. **Code Organization:** Need to organize Linux-specific code

## Decision

Extend [`OmniCppController.py`](../../OmniCppController.py:1) with comprehensive Linux support while maintaining Windows functionality.

### 1. Linux Platform Detection Module

Create `omni_scripts/platform/linux.py`:

```python
@dataclass
class LinuxDistribution:
    """Linux distribution information."""
    name: str  # e.g., "CachyOS", "Arch Linux", "Ubuntu"
    version: str  # e.g., "2023.12.01", "22.04", "38"
    family: str  # e.g., "arch", "debian", "fedora"
    package_manager: str  # e.g., "pacman", "apt", "dnf"
    is_cachyos: bool  # True if CachyOS detected

def detect_linux_distribution() -> LinuxDistribution:
    """Detect Linux distribution and version."""
    # Check /etc/os-release
    if Path("/etc/os-release").exists():
        with open("/etc/os-release") as f:
            content = f.read()

        if "ID=cachyos" in content:
            return LinuxDistribution(
                name="CachyOS",
                version=_extract_version(content),
                family="arch",
                package_manager="pacman",
                is_cachyos=True
            )
        # ... other distributions

    return LinuxDistribution(
        name="Unknown",
        version="",
        family="unknown",
        package_manager="unknown",
        is_cachyos=False
    )

def is_cachyos() -> bool:
    """Check if running on CachyOS."""
    distro = detect_linux_distribution()
    return distro.is_cachyos

def detect_package_manager() -> PackageManager:
    """Detect system package manager."""
    if shutil.which("pacman"):
        return PackageManager("pacman", "pacman")
    elif shutil.which("apt"):
        return PackageManager("apt", "apt-get")
    elif shutil.which("dnf"):
        return PackageManager("dnf", "dnf")
    return PackageManager("unknown", "")
```

### 2. Nix Integration Module

Create `omni_scripts/utils/nix_utils.py`:

```python
def is_nix_environment() -> bool:
    """Check if running in Nix shell."""
    return os.environ.get('IN_NIX_SHELL') == '1'

def setup_nix_environment() -> None:
    """Setup environment variables for Nix shell."""
    if not is_nix_environment():
        return

    # Configure paths from Nix store
    nix_paths = os.environ.get('PATH', '').split(':')
    nix_paths = [p for p in nix_paths if '/nix/store' in p]

    # Set compiler paths
    if nix_paths:
        os.environ['PATH'] = ':'.join(nix_paths) + ':' + os.environ.get('PATH', '')

def get_nix_packages() -> list[str]:
    """Get list of packages available in Nix environment."""
    if not is_nix_environment():
        return []

    # Parse NIX_PATH to get available packages
    nix_path = os.environ.get('NIX_PATH', '')
    return nix_path.split(':')

def validate_nix_environment() -> bool:
    """Validate Nix environment is properly configured."""
    if not is_nix_environment():
        return False

    # Check for required tools
    required_tools = ['gcc', 'clang', 'cmake', 'ninja']
    for tool in required_tools:
        if not shutil.which(tool):
            log_warning(f"Required tool not found in Nix environment: {tool}")
            return False

    return True
```

### 3. CachyOS-Specific Optimizations

Add CachyOS-specific compiler flags:

```python
def get_cachyos_compiler_flags(compiler: str, build_type: str) -> list[str]:
    """Get CachyOS-specific compiler flags."""
    flags = []

    if build_type == "release":
        # CachyOS performance optimizations
        flags.extend([
            "-march=native",  # Use native CPU features
            "-O3",            # Maximum optimization
            "-flto",          # Link-time optimization
            "-DNDEBUG"        # Disable debug assertions
        ])
    else:
        # Debug build flags
        flags.extend([
            "-g",
            "-O0",
            "-DDEBUG"
        ])

    # CachyOS-specific security flags
    if compiler == "gcc":
        flags.extend([
            "-fstack-protector-strong",
            "-D_FORTIFY_SOURCE=2"
        ])
    elif compiler == "clang":
        flags.extend([
            "-fstack-protector-strong",
            "-D_FORTIFY_SOURCE=2"
        ])

    return flags

def get_cachyos_linker_flags() -> list[str]:
    """Get CachyOS-specific linker flags."""
    return [
        "-Wl,--as-needed",
        "-Wl,--no-undefined"
    ]
```

### 4. Enhanced Platform Detection

Extend existing platform detection:

```python
def detect_platform() -> PlatformInfo:
    """Detect platform with Linux enhancements."""
    platform = get_system_platform()

    if platform.os == "Linux":
        distro = detect_linux_distribution()
        nix_env = is_nix_environment()

        return PlatformInfo(
            os=platform.os,
            arch=platform.arch,
            distro=distro,
            is_nix=nix_env,
            is_cachyos=distro.is_cachyos
        )

    return platform
```

### 5. Enhanced Compiler Detection

Extend compiler detection for Linux:

```python
def detect_linux_gcc() -> Optional[GCCCompiler]:
    """Detect GCC compiler on Linux with Nix awareness."""
    if is_nix_environment():
        # Use Nix-provided GCC
        gcc_path = shutil.which("gcc")
        if gcc_path and "/nix/store" in gcc_path:
            return GCCCompiler(
                path=gcc_path,
                version=get_gcc_version(gcc_path),
                is_nix=True
            )

    # Fallback to system GCC
    gcc_path = shutil.which("gcc")
    if gcc_path:
        return GCCCompiler(
            path=gcc_path,
            version=get_gcc_version(gcc_path),
            is_nix=False
        )

    return None

def detect_linux_clang() -> Optional[ClangCompiler]:
    """Detect Clang compiler on Linux with Nix awareness."""
    if is_nix_environment():
        # Use Nix-provided Clang
        clang_path = shutil.which("clang")
        if clang_path and "/nix/store" in clang_path:
            return ClangCompiler(
                path=clang_path,
                version=get_clang_version(clang_path),
                is_nix=True
            )

    # Fallback to system Clang
    clang_path = shutil.which("clang")
    if clang_path:
        return ClangCompiler(
            path=clang_path,
            version=get_clang_version(clang_path),
            is_nix=False
        )

    return None
```

### 6. Environment Validation

Add environment validation:

```python
def validate_linux_environment() -> bool:
    """Validate Linux build environment is complete."""
    platform = detect_platform()

    if platform.os != "Linux":
        return True  # Not Linux, skip validation

    # Check Nix environment
    if platform.is_nix:
        if not validate_nix_environment():
            log_error("Nix environment validation failed")
            return False

    # Check compiler availability
    if not shutil.which("gcc") and not shutil.which("clang"):
        log_error("No compiler found (gcc or clang required)")
        return False

    # Check CMake availability
    if not shutil.which("cmake"):
        log_error("CMake not found")
        return False

    # Check Ninja availability
    if not shutil.which("ninja"):
        log_error("Ninja not found")
        return False

    # Check Conan availability
    if not shutil.which("conan"):
        log_warning("Conan not found, package management may be limited")

    return True
```

### 7. Enhanced Build Context

Create Linux-specific build context:

```python
def get_linux_build_context(
    self,
    target: str,
    pipeline: str,
    preset: str,
    config: str,
    compiler: Optional[str] = None
) -> BuildContext:
    """Create BuildContext optimized for Linux builds."""
    platform = detect_platform()

    # Auto-detect compiler if not specified
    if compiler is None:
        if platform.is_cachyos:
            compiler = "gcc"  # CachyOS default to GCC
        else:
            compiler = "clang"  # Other distros default to Clang

    # Get compiler info
    compiler_info = detect_compiler(compiler)

    # Get compiler flags
    if platform.is_cachyos:
        flags = get_cachyos_compiler_flags(compiler, config)
    else:
        flags = get_generic_linux_flags(compiler, config)

    # Create build context
    return BuildContext(
        target=target,
        pipeline=pipeline,
        preset=preset,
        config=config,
        compiler=compiler_info,
        flags=flags,
        platform=platform
    )
```

### 8. Enhanced Help Command

Add Linux-specific help:

```python
def show_linux_help(self) -> None:
    """Show Linux-specific help information."""
    platform = detect_platform()

    log_info("Linux Build System Help")
    log_info("=" * 50)

    if platform.is_cachyos:
        log_info("Platform: CachyOS (Arch Linux derivative)")
        log_info("Package Manager: pacman")
        log_info("Default Compiler: GCC 13")
    else:
        distro = detect_linux_distribution()
        log_info(f"Platform: {distro.name}")
        log_info(f"Package Manager: {distro.package_manager}")

    if platform.is_nix:
        log_info("Nix Environment: Active")
    else:
        log_info("Nix Environment: Inactive")

    log_info("")
    log_info("Available Commands:")
    log_info("  configure  Configure CMake build system")
    log_info("  build      Build project")
    log_info("  test       Run tests")
    log_info("  clean      Clean build artifacts")
    log_info("")
    log_info("Examples:")
    log_info("  python OmniCppController.py configure --compiler gcc")
    log_info("  python OmniCppController.py build engine gcc-debug debug")
    log_info("  python OmniCppController.py test")
```

## Consequences

### Positive

1. **Comprehensive Linux Support:** Full Linux support with distribution detection
2. **Nix Integration:** Seamless integration with Nix environments
3. **CachyOS Optimizations:** Performance optimizations for CachyOS
4. **Environment Validation:** Validates environment before builds
5. **Auto-Detection:** Automatic detection of platform and compiler
6. **Better Error Messages:** Clear error messages for missing dependencies
7. **Improved Help:** Linux-specific help and examples
8. **Consistent Interface:** Same interface across Windows and Linux
9. **Extensible:** Easy to add support for more distributions
10. **Better Testing:** Easier to test on Linux

### Negative

1. **Increased Complexity:** More code paths and logic
2. **Maintainability:** More code to maintain
3. **Testing Burden:** More platforms to test
4. **Documentation:** More documentation required
5. **Code Size:** Larger codebase
6. **Debugging:** More complex to debug issues
7. **Performance:** Slight performance overhead from detection
8. **Dependencies:** More dependencies (Linux-specific modules)

### Neutral

1. **Code Organization:** Need to organize Linux-specific code
2. **Testing Strategy:** Need comprehensive Linux testing
3. **CI/CD:** May need Linux CI/CD pipelines
4. **Support:** May receive Linux-specific bug reports

## Alternatives Considered

### Alternative 1: Separate Linux Controller

**Description:** Create separate OmniCppControllerLinux.py for Linux

**Pros:**
- Separation of concerns
- Less complex single file
- Easier to maintain platform-specific code

**Cons:**
- Code duplication
- Inconsistent interface
- Harder to share common code
- Confusing for users
- More files to maintain

**Rejected:** Code duplication and inconsistent interface

### Alternative 2: Plugin Architecture

**Description:** Use plugin architecture for platform-specific code

**Pros:**
- Extensible
- Clean separation
- Easy to add new platforms

**Cons:**
- Complex to implement
- Overkill for current needs
- More indirection
- Harder to debug
- Additional complexity

**Rejected:** Overkill for current needs

### Alternative 3: Configuration-Based Approach

**Description:** Use configuration files for platform-specific behavior

**Pros:**
- No code changes needed
- Easy to modify
- Declarative

**Cons:**
- Limited flexibility
- Hard to implement complex logic
- Still need code to read config
- Not as powerful as code

**Rejected:** Limited flexibility

### Alternative 4: Minimal Linux Support

**Description:** Add minimal Linux support, keep Windows as primary

**Pros:**
- Less complexity
- Faster implementation
- Less testing

**Cons:**
- Poor Linux experience
- Not aligned with project goals
- Linux users frustrated
- Limited adoption

**Rejected:** Poor Linux experience, not aligned with goals

## Related ADRs

- [ADR-008: Modular controller pattern](ADR-008-modular-controller-pattern.md)
- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-029: Direnv for Environment Management](ADR-029-direnv-environment-management.md)
- [ADR-031: Linux-Specific Multi-Package Manager Strategy](ADR-031-linux-multi-package-manager-strategy.md)

## Threat Model References

- **TM-LX-004: Controller Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - Command injection in terminal invocation
  - Path traversal in compiler detection
  - Environment variable manipulation
  - Mitigation: Validate all inputs, sanitize paths, use secure defaults

## References

- [OmniCppController.py](../../OmniCppController.py:1)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)
- [Platform Detection Design](../04_future_state/design/DES-007-platform-detection-interface.md)
- [Compiler Detection Design](../04_future_state/design/DES-008-compiler-detection-interface.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
