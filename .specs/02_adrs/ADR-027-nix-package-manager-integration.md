# ADR-027: Nix Package Manager Integration

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Linux Development Environment Setup

---

## Context

The OmniCPP Template project requires a reproducible development environment for Linux builds, particularly targeting CachyOS (an Arch Linux derivative). Traditional Linux package management approaches have several limitations:

1. **Environment Drift:** System package updates can break build environments
2. **Reproducibility Issues:** Different developers may have different toolchain versions
3. **Dependency Conflicts:** System packages may conflict with project dependencies
4. **Setup Complexity:** Developers must manually install and configure multiple tools
5. **Version Pinning Difficulty:** Hard to ensure exact versions across all dependencies

The project needs a solution that provides:
- Reproducible build environments across different machines
- Declarative specification of all dependencies
- Isolation from system packages
- Easy onboarding for new developers
- Support for both GCC and Clang toolchains
- Integration with Qt6 and Vulkan graphics libraries

## Decision

Adopt **Nix flakes** as the primary mechanism for reproducible Linux development environments.

### 1. Nix Flake Configuration

Create a comprehensive [`flake.nix`](../../flake.nix:1) file that declares all development dependencies:

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

          # Graphics
          qt6.qtbase
          qt6.qtwayland
          vulkan-headers
          vulkan-loader
          vulkan-validation-layers

          # Tools
          clang-tools
          doxygen
        ];

        shellHook = ''
          echo ">> Loaded OmniCPP C++ Development Environment"
          export QT_QPA_PLATFORM=wayland
          export CMAKE_GENERATOR="Ninja"
        '';
      };
    };
}
```

### 2. Direnv Integration

Use [`.envrc`](../../.envrc:1) with direnv for automatic environment loading:

```bash
use flake
```

This automatically loads the Nix environment when entering the project directory.

### 3. Multi-Toolchain Support

Create separate Nix shells for different toolchains:

```nix
devShells.${system}.gcc = pkgs.mkShell {
  buildInputs = with pkgs; [ gcc13 cmake ninja ];
  shellHook = ''
    export CC=gcc
    export CXX=g++
  '';
};

devShells.${system}.clang = pkgs.mkShell {
  buildInputs = with pkgs; [ llvmPackages_19.clang cmake ninja ];
  shellHook = ''
    export CC=clang
    export CXX=clang++
  '';
};
```

### 4. Environment Isolation

Nix provides complete isolation from system packages:
- All dependencies are installed in the Nix store
- No interference with system packages
- Exact version pinning via [`flake.lock`](../../flake.lock:1)
- Reproducible builds across different machines

### 5. Integration with OmniCppController.py

Extend [`OmniCppController.py`](../../OmniCppController.py:1) to detect Nix environment:

```python
def is_nix_environment() -> bool:
    """Check if running in Nix shell."""
    return os.environ.get('IN_NIX_SHELL') == '1'

def setup_nix_environment() -> None:
    """Configure build environment for Nix shell."""
    if is_nix_environment():
        # Use Nix-provided toolchain
        pass
    else:
        # Use system toolchain
        pass
```

## Consequences

### Positive

1. **Reproducibility:** Exact same environment across all developer machines
2. **Declarative:** All dependencies specified in single [`flake.nix`](../../flake.nix:1) file
3. **Isolation:** No conflicts with system packages
4. **Version Pinning:** [`flake.lock`](../../flake.lock:1) ensures exact dependency versions
5. **Easy Onboarding:** New developers run `nix develop` and have complete environment
6. **Rollback:** Can revert to previous environment versions
7. **Multiple Toolchains:** Easy to switch between GCC and Clang
8. **CI/CD Integration:** Same environment in CI as on developer machines
9. **No Root Required:** Users don't need sudo to install dependencies
10. **Binary Caching:** Can share pre-built packages across team

### Negative

1. **Learning Curve:** Developers must learn Nix concepts
2. **Disk Space:** Nix store can consume significant disk space
3. **Build Time:** First-time setup can be slow (mitigated by binary cache)
4. **Platform Support:** Nix primarily supports Linux and macOS
5. **Windows Support:** Windows support via WSL2, not native
6. **Complexity:** Nix expression language can be complex for advanced use cases
7. **Tooling:** IDE integration may require additional configuration
8. **Dependency Updates:** Updating dependencies requires careful testing

### Neutral

1. **Documentation:** Requires Nix-specific documentation
2. **CI/CD:** CI/CD pipelines must install Nix
3. **Debugging:** Debugging Nix issues can be challenging
4. **Community:** Smaller community compared to traditional package managers

## Alternatives Considered

### Alternative 1: Traditional System Package Manager

**Description:** Use pacman, apt, or dnf to install dependencies system-wide

**Pros:**
- Familiar to most Linux developers
- No additional tools required
- Fast installation (binary packages)

**Cons:**
- Environment drift over time
- No reproducibility across machines
- Requires root access
- Difficult to pin exact versions
- System updates can break builds
- Conflicts with system packages

**Rejected:** Insufficient reproducibility and isolation

### Alternative 2: Docker Containers

**Description:** Use Docker containers for isolated development environments

**Pros:**
- Complete isolation from host system
- Reproducible across platforms
- Easy to share environments
- Well-known technology

**Cons:**
- Requires Docker daemon
- Slower than native execution
- Filesystem overhead
- IDE integration complexity
- Not suitable for GUI applications (Qt6, Vulkan)
- Requires X11/Wayland forwarding for graphics

**Rejected:** Overhead and complexity for C++ development with graphics

### Alternative 3: Conda Environment

**Description:** Use Conda for Python and C++ package management

**Pros:**
- Familiar to Python developers
- Good Python ecosystem
- Environment isolation

**Cons:**
- Limited C++ package ecosystem
- Not designed for system-level packages
- Poor support for Qt6 and Vulkan
- Not reproducible across machines
- Requires conda-forge for many packages

**Rejected:** Insufficient C++ and graphics library support

### Alternative 4: Guix

**Description:** Use GNU Guix (similar to Nix but uses Guile Scheme)

**Pros:**
- Similar benefits to Nix
- GNU project
- Functional package management

**Cons:**
- Smaller ecosystem than Nix
- Less mature tooling
- Guile Scheme learning curve
- Less community support
- Fewer available packages

**Rejected:** Smaller ecosystem and community compared to Nix

### Alternative 5: vcpkg on Linux

**Description:** Use vcpkg as primary package manager on Linux

**Pros:**
- Already used in project
- Cross-platform support
- Binary packages available

**Cons:**
- Not reproducible across machines
- No environment isolation
- Requires manual installation of system dependencies
- Limited Linux package ecosystem
- No declarative configuration

**Rejected:** Insufficient reproducibility and isolation

## Related ADRs

- [ADR-001: Multi-package manager strategy](ADR-001-multi-package-manager-strategy.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-029: Direnv for Environment Management](ADR-029-direnv-environment-management.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-031: Linux-Specific Multi-Package Manager Strategy](ADR-031-linux-multi-package-manager-strategy.md)

## Threat Model References

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)
  - Nix expression injection
  - Flake dependency hijacking
  - Binary cache poisoning
  - Mitigation: Pin exact versions, verify flake inputs, use trusted binary caches

## References

- [Nix Manual](https://nixos.org/manual/nix/stable/)
- [Nix Flakes](https://nixos.wiki/wiki/Flakes)
- [Nix Pills](https://nixos.org/guides/nix-pills/)
- [Direnv](https://direnv.net/)
- [CachyOS Nix Guide](https://wiki.cachyos.org/nix)
- [Reproducible Builds with Nix](https://reproducible-builds.org/docs/nix/)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
