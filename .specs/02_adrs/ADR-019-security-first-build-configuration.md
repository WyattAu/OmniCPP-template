# ADR-019: Security-First Build Configuration

**Status:** Accepted
**Date:** 2026-01-07
**Context:** Security

---

## Context

The OmniCPP Template project requires a security-first approach to build configuration to prevent vulnerabilities and ensure secure builds. The threat model (`.specs/03_threat_model/analysis.md`) identifies multiple security threats that need to be addressed through build configuration.

### Current State

Build configuration has inconsistent security settings:
- **Inconsistent Flags:** Different security flags across compilers
- **No Hardening:** No compiler hardening enabled
- **No Sanitizers:** No address sanitizers enabled
- **No Validation:** No build validation for security
- **No Integrity Checks:** No dependency integrity checks

### Issues

1. **Inconsistent Security:** Inconsistent security settings across compilers
2. **No Hardening:** No compiler hardening enabled
3. **No Sanitizers:** No address sanitizers enabled
4. **No Validation:** No build validation for security
5. **No Integrity Checks:** No dependency integrity checks
6. **Vulnerabilities:** Potential vulnerabilities in builds

## Decision

Implement **security-first build configuration** with:
1. **Compiler Hardening:** Enable compiler hardening flags
2. **Sanitizers:** Enable address sanitizers for debug builds
3. **Validation:** Validate build configuration for security
4. **Integrity Checks:** Verify dependency integrity
5. **Secure Defaults:** Secure defaults for all configurations
6. **Security Auditing:** Regular security audits of builds

### 1. Compiler Hardening Flags

```cmake
# cmake/CompilerFlags.cmake
# Compiler hardening flags

if(MSVC)
    # MSVC hardening flags
    add_compile_options(
        /GS                    # Buffer security check
        /DYNAMICBASE           # Address space layout randomization
        /NXCOMPAT              # Data execution prevention
        /HIGHENTROPYVA        # 64-bit entropy
        /sdl                   # Security Development Lifecycle
        /guard:cf              # Control Flow Guard
        /Qspectre              # Spectre mitigation
        /Zc:__cplusplus        # Enable correct __cplusplus macro
    )

    add_link_options(
        /DYNAMICBASE           # Address space layout randomization
        /NXCOMPAT              # Data execution prevention
        /GUARD:CF              # Control Flow Guard
    )

elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    # GCC hardening flags
    add_compile_options(
        -fstack-protector-strong  # Stack protection
        -D_FORTIFY_SOURCE=2      # Source fortification
        -fPIE                   # Position-independent executable
        -fPIC                    # Position-independent code
        -D_GLIBCXX_ASSERTIONS  # Enable assertions
        -fasynchronous-unwind-tables
        -fno-omit-frame-pointer
        -Wformat -Wformat-security
        -Werror=format-security
    )

    add_link_options(
        -pie                     # Position-independent executable
        -Wl,-z,relro           # Read-only relocations
        -Wl,-z,now              # No lazy binding
        -Wl,-z,noexecstack       # No executable stack
    )

elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    # Clang hardening flags
    add_compile_options(
        -fstack-protector-strong  # Stack protection
        -D_FORTIFY_SOURCE=2      # Source fortification
        -fPIE                   # Position-independent executable
        -fPIC                    # Position-independent code
        -D_GLIBCXX_ASSERTIONS  # Enable assertions
        -fasynchronous-unwind-tables
        -fno-omit-frame-pointer
        -Wformat -Wformat-security
        -Werror=format-security
    )

    add_link_options(
        -pie                     # Position-independent executable
        -Wl,-z,relro           # Read-only relocations
        -Wl,-z,now              # No lazy binding
        -Wl,-z,noexecstack       # No executable stack
    )
endif()
```

### 2. Sanitizer Configuration

```cmake
# cmake/Sanitizers.cmake
# Sanitizer configuration

option(ENABLE_SANITIZERS "Enable sanitizers" OFF)
option(ENABLE_ASAN "Enable Address Sanitizer" OFF)
option(ENABLE_UBSAN "Enable Undefined Behavior Sanitizer" OFF)
option(ENABLE_TSAN "Enable Thread Sanitizer" OFF)

if(ENABLE_SANITIZERS)
    # Enable Address Sanitizer
    if(ENABLE_ASAN)
        add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
        add_link_options(-fsanitize=address)
        message(STATUS "Address Sanitizer enabled")
    endif()

    # Enable Undefined Behavior Sanitizer
    if(ENABLE_UBSAN)
        add_compile_options(-fsanitize=undefined -fno-omit-frame-pointer)
        add_link_options(-fsanitize=undefined)
        message(STATUS "Undefined Behavior Sanitizer enabled")
    endif()

    # Enable Thread Sanitizer
    if(ENABLE_TSAN)
        add_compile_options(-fsanitize=thread -fno-omit-frame-pointer)
        add_link_options(-fsanitize=thread)
        message(STATUS "Thread Sanitizer enabled")
    endif()

    # Disable optimizations for sanitizers
    add_compile_options(-O0 -g)
endif()
```

### 3. Security Validation

```python
# omni_scripts/validators/security_validator.py
"""Security validator for build configuration."""

from typing import Dict, List, Optional
from pathlib import Path
import logging

from exceptions import ValidationError

class SecurityValidator:
    """Security validator for build configuration."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize security validator.

        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

    def validate_compiler_flags(self, flags: List[str]) -> List[str]:
        """Validate compiler flags for security.

        Args:
            flags: Compiler flags

        Returns:
            List of validation errors
        """
        errors = []

        # Check for security flags
        security_flags = {
            "MSVC": ["/GS", "/DYNAMICBASE", "/NXCOMPAT", "/guard:cf"],
            "GCC": ["-fstack-protector-strong", "-D_FORTIFY_SOURCE=2", "-fPIE"],
            "Clang": ["-fstack-protector-strong", "-D_FORTIFY_SOURCE=2", "-fPIE"],
        }

        # Check if security flags are present
        for compiler, required_flags in security_flags.items():
            for flag in required_flags:
                if flag not in flags:
                    errors.append(f"Missing security flag: {flag} for {compiler}")

        return errors

    def validate_sanitizers(self, flags: List[str]) -> List[str]:
        """Validate sanitizer flags.

        Args:
            flags: Compiler flags

        Returns:
            List of validation errors
        """
        errors = []

        # Check for sanitizer flags
        sanitizer_flags = ["-fsanitize=address", "-fsanitize=undefined", "-fsanitize=thread"]

        # Check if at least one sanitizer is enabled
        has_sanitizer = any(flag in flags for flag in sanitizer_flags)

        if not has_sanitizer:
            errors.append("No sanitizer enabled")

        return errors

    def validate_warnings(self, flags: List[str]) -> List[str]:
        """Validate warning flags.

        Args:
            flags: Compiler flags

        Returns:
            List of validation errors
        """
        errors = []

        # Check for warning flags
        warning_flags = ["-Wall", "-Wextra", "-Wpedantic", "-Werror"]

        # Check if warning flags are present
        for flag in warning_flags:
            if flag not in flags:
                errors.append(f"Missing warning flag: {flag}")

        return errors

    def validate_build(self, config: Dict[str, any]) -> List[str]:
        """Validate build configuration for security.

        Args:
            config: Build configuration

        Returns:
            List of validation errors
        """
        errors = []

        # Validate compiler flags
        compiler_flags = config.get("compiler_flags", [])
        errors.extend(self.validate_compiler_flags(compiler_flags))

        # Validate sanitizers
        errors.extend(self.validate_sanitizers(compiler_flags))

        # Validate warnings
        errors.extend(self.validate_warnings(compiler_flags))

        return errors
```

### 4. CMake Presets with Security

```json
// CMakePresets.json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "debug-secure",
      "displayName": "Debug with Security",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "ENABLE_SANITIZERS": "ON",
        "ENABLE_ASAN": "ON",
        "ENABLE_UBSAN": "ON"
      }
    },
    {
      "name": "release-secure",
      "displayName": "Release with Security",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "ENABLE_SANITIZERS": "OFF"
      }
    }
  ]
}
```

### 5. Security Audit Script

```python
# scripts/security_audit.py
#!/usr/bin/env python3
"""Security audit script for builds."""

import subprocess
import sys
from pathlib import Path
import json
import logging

def check_compiler_flags(compiler: str, flags: list) -> dict:
    """Check compiler flags for security.

    Args:
        compiler: Compiler name
        flags: Compiler flags

    Returns:
        Dictionary of security checks
    """
    checks = {
        "stack_protection": False,
        "fortify_source": False,
        "pie": False,
        "relro": False,
        "noexecstack": False,
    }

    # Check for stack protection
    if "-fstack-protector-strong" in flags or "/GS" in flags:
        checks["stack_protection"] = True

    # Check for fortify source
    if "-D_FORTIFY_SOURCE=2" in flags:
        checks["fortify_source"] = True

    # Check for PIE
    if "-fPIE" in flags or "-pie" in flags:
        checks["pie"] = True

    # Check for RELRO
    if "-Wl,-z,relro" in flags:
        checks["relro"] = True

    # Check for noexecstack
    if "-Wl,-z,noexecstack" in flags:
        checks["noexecstack"] = True

    return checks

def audit_build(build_dir: Path) -> dict:
    """Audit build for security.

    Args:
        build_dir: Build directory

    Returns:
        Dictionary of audit results
    """
    results = {}

    # Read compile_commands.json
    compile_commands = build_dir / "compile_commands.json"
    if not compile_commands.exists():
        return {"error": "compile_commands.json not found"}

    with open(compile_commands, 'r') as f:
        commands = json.load(f)

    # Check each command
    for command in commands:
        compiler = command.get("command", [])[0]
        flags = command.get("command", [])[1:]

        # Check compiler flags
        if "gcc" in compiler or "g++" in compiler:
            checks = check_compiler_flags("GCC", flags)
        elif "clang" in compiler or "clang++" in compiler:
            checks = check_compiler_flags("Clang", flags)
        elif "cl.exe" in compiler:
            checks = check_compiler_flags("MSVC", flags)
        else:
            continue

        # Store results
        file = command.get("file")
        results[file] = checks

    return results

def main():
    """Main audit function."""
    build_dir = Path("build")

    if not build_dir.exists():
        print(f"Build directory not found: {build_dir}")
        return 1

    # Audit build
    results = audit_build(build_dir)

    # Print results
    print("Security Audit Results:")
    print("=" * 50)

    for file, checks in results.items():
        print(f"\nFile: {file}")
        print(f"  Stack Protection: {'✓' if checks.get('stack_protection') else '✗'}")
        print(f"  Fortify Source: {'✓' if checks.get('fortify_source') else '✗'}")
        print(f"  PIE: {'✓' if checks.get('pie') else '✗'}")
        print(f"  RELRO: {'✓' if checks.get('relro') else '✗'}")
        print(f"  No Exec Stack: {'✓' if checks.get('noexecstack') else '✗'}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Consequences

### Positive

1. **Security:** Improved security through hardening
2. **Vulnerability Prevention:** Prevents common vulnerabilities
3. **Sanitizers:** Catches memory errors and undefined behavior
4. **Validation:** Validates build configuration for security
5. **Integrity:** Verifies dependency integrity
6. **Auditing:** Regular security audits of builds
7. **Compliance:** Meets security best practices

### Negative

1. **Performance:** Some security features impact performance
2. **Build Time:** Hardening flags increase build time
3. **Complexity:** More complex build configuration
4. **Compatibility:** Some features may not work on all platforms

### Neutral

1. **Documentation:** Requires documentation for security features
2. **Testing:** Need to test security features

## Alternatives Considered

### Alternative 1: No Security Hardening

**Description:** No security hardening

**Pros:**
- Faster builds
- Simpler configuration
- No performance impact

**Cons:**
- Vulnerable builds
- Security vulnerabilities
- Non-compliant

**Rejected:** Vulnerable builds and security issues

### Alternative 2: External Security Tools

**Description:** Use external security tools

**Pros:**
- No build configuration changes
- Comprehensive security checks

**Cons:**
- External dependency
- Build time overhead
- Platform-specific

**Rejected:** External dependency and build time overhead

### Alternative 3: Runtime Security

**Description:** Runtime security only

**Pros:**
- No build time overhead
- Flexible security

**Cons:**
- Runtime overhead
- No compile-time checks
- Performance impact

**Rejected:** Runtime overhead and no compile-time checks

## Related ADRs

- [ADR-003: Package security verification approach](ADR-003-package-security-verification-approach.md)
- [ADR-020: Dependency integrity verification](ADR-020-dependency-integrity-verification.md)
- [ADR-021: Secure terminal invocation](ADR-021-secure-terminal-invocation.md)

## References

- [Compiler Hardening](https://wiki.debian.org/Hardening)
- [GCC Security Flags](https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html)
- [Clang Security Flags](https://clang.llvm.org/docs/CommandGuide/clang.html)
- [MSVC Security Flags](https://docs.microsoft.com/en-us/cpp/build/reference/compiler-options-listed-alphabetically/compiler-options)
- [Address Sanitizer](https://github.com/google/sanitizers)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
