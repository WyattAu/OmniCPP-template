# ADR-029: Direnv for Environment Management

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Development Environment Automation

---

## Context

The OmniCPP Template project uses Nix flakes to provide reproducible development environments (see [ADR-027](ADR-027-nix-package-manager-integration.md)). However, developers must manually activate the Nix environment for each terminal session:

```bash
# Manual activation required
nix develop

# Or for specific toolchain
nix develop .#gcc
nix develop .#clang
```

This manual activation has several issues:

1. **Forgetfulness:** Developers forget to activate the environment
2. **Inconsistent State:** Some terminals have environment, others don't
3. **Extra Step:** Always need to remember to run `nix develop`
4. **IDE Integration:** IDEs may not have environment loaded
5. **Context Switching:** Hard to switch between different toolchains
6. **Automation:** Scripts may not have correct environment
7. **Onboarding:** New developers may not know about environment activation

The project needs a solution that:
- Automatically loads the Nix environment when entering the project directory
- Unloads the environment when leaving the project directory
- Works seamlessly with terminals, IDEs, and scripts
- Provides visual feedback when environment is loaded
- Supports multiple toolchains
- Is secure and doesn't leak environment variables

## Decision

Adopt **direnv** with [`.envrc`](../../.envrc:1) for automatic environment management.

### 1. Direnv Configuration

Create a simple [`.envrc`](../../.envrc:1) file in the project root:

```bash
# .envrc
use flake
```

This single line automatically loads the Nix flake environment.

### 2. Direnv Installation

Document direnv installation for different shells:

```bash
# Install direnv
sudo pacman -S direnv  # Arch/CachyOS
sudo apt install direnv  # Ubuntu/Debian
sudo dnf install direnv  # Fedora

# Hook direnv into shell
# For bash
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# For zsh
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# For fish
echo 'direnv hook fish | source' >> ~/.config/fish/config.fish
```

### 3. Multi-Toolchain Support

Create environment-specific `.envrc` files:

```bash
# .envrc.gcc
use flake .#gcc

# .envrc.clang
use flake .#clang

# .envrc (default)
use flake
```

Developers can symlink to desired toolchain:

```bash
ln -sf .envrc.gcc .envrc  # Use GCC
ln -sf .envrc.clang .envrc  # Use Clang
```

### 4. Environment Variables

Add project-specific environment variables in `.envrc`:

```bash
use flake

# Project-specific variables
export OMNICPP_ROOT=$PWD
export OMNICPP_BUILD_DIR=$PWD/build
export OMNICPP_LOG_DIR=$PWD/logs

# CMake defaults
export CMAKE_GENERATOR="Ninja"
export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)

# Qt6 environment
export QT_QPA_PLATFORM=wayland

# Compiler cache
export CCACHE_DIR=$PWD/.ccache

# Conan environment
export CONAN_USER_HOME=$PWD/.conan2
```

### 5. Direnv Security

Direnv provides security through:

```bash
# First time entering directory
direnv: error .envrc is blocked. Run `direnv allow` to approve its content.

# Approve .envrc
direnv allow

# See what .envrc does
direnv status
```

This prevents malicious `.envrc` files from executing automatically.

### 6. IDE Integration

Configure IDEs to use direnv:

**VSCode:**
```json
{
  "terminal.integrated.env.linux": {
    "PATH": "${workspaceFolder}/direnv:${env:PATH}"
  }
}
```

**CLion/IntelliJ:**
- Install direnv plugin
- Configure to use direnv environment

**Vim/Neovim:**
```vim
" .vimrc
let g:direnv_auto = 1
```

### 7. Visual Feedback

Direnv provides visual feedback in terminal:

```bash
# When entering directory
direnv: loading .envrc
direnv: export +PATH +QT_QPA_PLATFORM +CMAKE_GENERATOR

# When leaving directory
direnv: unloading .envrc
direnv: export -PATH -QT_QPA_PLATFORM -CMAKE_GENERATOR
```

### 8. Integration with OmniCppController.py

Extend [`OmniCppController.py`](../../OmniCppController.py:1) to detect direnv:

```python
def is_direnv_active() -> bool:
    """Check if direnv environment is active."""
    return os.environ.get('DIRENV_DIR') is not None

def validate_environment() -> bool:
    """Validate development environment is correctly loaded."""
    if not is_direnv_active():
        log_warning("direnv environment not loaded. Run 'direnv allow' first.")
        return False

    if not is_nix_environment():
        log_warning("Nix environment not loaded. Run 'nix develop' first.")
        return False

    return True
```

## Consequences

### Positive

1. **Automatic Loading:** Environment loads automatically when entering directory
2. **Automatic Unloading:** Environment unloads when leaving directory
3. **Zero Friction:** No manual activation required
4. **Visual Feedback:** Clear indication when environment is loaded
5. **Security:** Requires explicit approval of `.envrc` files
6. **IDE Support:** Works seamlessly with IDEs
7. **Toolchain Switching:** Easy to switch between GCC and Clang
8. **Consistency:** All terminals have same environment
9. **Onboarding:** Simplified for new developers
10. **Automation:** Scripts automatically have correct environment

### Negative

1. **Additional Dependency:** Requires direnv installation
2. **Shell Hook:** Must configure shell hook for each user
3. **Performance:** Small overhead when changing directories
4. **Learning Curve:** Developers must understand direnv
5. **Debugging:** Harder to debug environment issues
6. **Cache Issues:** May need to run `direnv reload` after changes
7. **Remote Development:** May not work well with remote shells
8. **Container Environments:** May conflict with container environments
9. **Permission Issues:** May need to run `direnv allow` multiple times
10. **Cross-Platform:** Primarily Linux and macOS support

### Neutral

1. **Documentation:** Need to document direnv usage
2. **CI/CD:** CI/CD may need to manually load environment
3. **Version Control:** `.envrc` is committed to repository
4. **Team Adoption:** All team members must use direnv

## Alternatives Considered

### Alternative 1: Manual Nix Activation

**Description:** Continue using manual `nix develop` command

**Pros:**
- No additional dependencies
- Explicit control over environment
- No directory change overhead
- Works everywhere Nix works

**Cons:**
- Manual activation required
- Easy to forget
- Inconsistent across terminals
- Poor developer experience
- IDE integration difficult

**Rejected:** Poor developer experience, high friction

### Alternative 2: Shell Aliases

**Description:** Create shell aliases to activate environment

**Pros:**
- Simple to implement
- No additional dependencies
- Familiar to developers

**Cons:**
- Still manual activation
- Must remember to run alias
- Doesn't work with IDEs
- Doesn't unload when leaving directory
- No security mechanism

**Rejected:** Still manual, no automatic loading

### Alternative 3: Shell Functions

**Description:** Create shell functions that automatically activate environment

**Pros:**
- Can be automatic
- No additional dependencies
- Customizable behavior

**Cons:**
- Complex to implement
- Shell-specific
- Hard to maintain
- No security mechanism
- Doesn't work with IDEs

**Rejected:** Complex, shell-specific, no security

### Alternative 4: Python Virtual Environment

**Description:** Use Python virtualenv for environment management

**Pros:**
- Familiar to Python developers
- Well-documented
- Works across platforms

**Cons:**
- Only manages Python packages
- Doesn't manage system packages
- Doesn't work with Nix
- No automatic loading
- Not designed for C++ development

**Rejected:** Doesn't manage C++ toolchain, doesn't work with Nix

### Alternative 5: Environment Modules

**Description:** Use Environment Modules (module) system

**Pros:**
- Designed for HPC environments
- Well-established
- Can manage multiple environments

**Cons:**
- Primarily for HPC
- Complex setup
- Not designed for development
- Doesn't work with Nix
- Requires system administrator access

**Rejected:** Not designed for development, doesn't work with Nix

## Related ADRs

- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)

## Threat Model References

- **TM-LX-003: Direnv Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - Malicious `.envrc` files
  - Environment variable injection
  - Path manipulation attacks
  - Mitigation: Use direnv's security model, review `.envrc` before allowing, use `.envrc` allow list

## References

- [Direnv Documentation](https://direnv.net/)
- [Direnv Manual](https://direnv.net/man/direnv.1.html)
- [Nix and Direnv](https://nixos.wiki/wiki/Development_environment_with_nix-shell)
- [Direnv Security](https://github.com/direnv/direnv/blob/master/docs/security.md)
- [Direnv in IDEs](https://direnv.net/docs/hooking.html)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
