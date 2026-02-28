# ADR-035: Linux Setup Script Architecture

**Status:** Accepted
**Date:** 2026-01-27
**Context:** Linux Build Automation

---

## Context

The OmniCPP Template project has Windows-specific setup scripts ([`conan/setup_*.bat`](../../conan/setup_clang_mingw_ucrt.bat:1)) for configuring the build environment. The Linux expansion requires equivalent Linux setup scripts.

### Current State

**Windows Setup Scripts:**
- [`conan/setup_clang_mingw_ucrt.bat`](../../conan/setup_clang_mingw_ucrt.bat:1) - Clang MinGW UCRT setup
- [`conan/setup_clang_mingw.bat`](../../conan/setup_clang_mingw.bat:1) - Clang MinGW setup
- [`conan/setup_clang.bat`](../../conan/setup_clang.bat:1) - Clang setup
- [`conan/setup_emscripten.bat`](../../conan/setup_emscripten.bat:1) - Emscripten setup
- [`conan/setup_gcc_mingw_ucrt.bat`](../../conan/setup_gcc_mingw_ucrt.bat:1) - GCC MinGW UCRT setup
- [`conan/setup_gcc_mingw.bat`](../../conan/setup_gcc_mingw.bat:1) - GCC MinGW setup
- [`conan/setup_msvc.bat`](../../conan/setup_msvc.bat:1) - MSVC setup

**Linux Setup Scripts:**
- [`conan/setup_emscripten.sh`](../../conan/setup_emscripten.sh:1) - Emscripten setup (already exists)

### Linux Expansion Requirements

The Linux expansion requires setup scripts for:

1. **GCC Setup:** Configure GCC compiler environment
2. **Clang Setup:** Configure Clang compiler environment
3. **CachyOS Setup:** Configure CachyOS-specific environment
4. **Nix Setup:** Configure Nix environment
5. **Conan Setup:** Configure Conan package manager
6. **System Dependencies:** Install system dependencies
7. **Environment Variables:** Set environment variables
8. **Validation:** Validate setup is complete

### Script Requirements

1. **Idempotent:** Can be run multiple times safely
2. **Error Handling:** Handle errors gracefully
3. **User Feedback:** Provide clear feedback to user
4. **Validation:** Validate setup is complete
5. **Rollback:** Ability to rollback changes
6. **Logging:** Log all actions
7. **Documentation:** Well-documented scripts
8. **Cross-Distribution:** Work on multiple Linux distributions

## Decision

Create comprehensive Linux setup scripts with clear architecture and error handling.

### 1. Script Organization

Organize scripts by purpose:

```bash
scripts/linux/
├── setup.sh                    # Main setup script
├── setup_gcc.sh                # GCC setup
├── setup_clang.sh              # Clang setup
├── setup_cachyos.sh            # CachyOS setup
├── setup_nix.sh                # Nix setup
├── setup_conan.sh              # Conan setup
├── setup_dependencies.sh        # System dependencies
├── validate.sh                  # Validate setup
└── rollback.sh                 # Rollback changes
```

### 2. Main Setup Script

Create main setup script that orchestrates all setup:

```bash
#!/bin/bash
# scripts/linux/setup.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log function
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warn "Running as root. This is not recommended."
        read -p "Continue? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

# Main setup function
main() {
    log_info "Starting OmniCPP Linux setup..."

    # Check root
    check_root

    # Detect distribution
    DISTRO=$(detect_distro)
    log_info "Detected distribution: $DISTRO"

    # Install system dependencies
    log_info "Installing system dependencies..."
    ./scripts/linux/setup_dependencies.sh

    # Setup Conan
    log_info "Setting up Conan..."
    ./scripts/linux/setup_conan.sh

    # Setup Nix (optional)
    if command -v nix &> /dev/null; then
        log_info "Setting up Nix..."
        ./scripts/linux/setup_nix.sh
    else
        log_warn "Nix not found. Skipping Nix setup."
    fi

    # Setup compiler
    log_info "Setting up compiler..."
    if command -v gcc &> /dev/null; then
        ./scripts/linux/setup_gcc.sh
    fi
    if command -v clang &> /dev/null; then
        ./scripts/linux/setup_clang.sh
    fi

    # CachyOS-specific setup
    if [[ "$DISTRO" == "cachyos" ]]; then
        log_info "Setting up CachyOS-specific configuration..."
        ./scripts/linux/setup_cachyos.sh
    fi

    # Validate setup
    log_info "Validating setup..."
    ./scripts/linux/validate.sh

    log_info "Setup complete!"
    log_info "Run 'nix develop' to enter development environment."
}

# Run main function
main "$@"
```

### 3. GCC Setup Script

Create GCC setup script:

```bash
#!/bin/bash
# scripts/linux/setup_gcc.sh

set -euo pipefail

log_info "Setting up GCC compiler..."

# Check GCC is installed
if ! command -v gcc &> /dev/null; then
    log_error "GCC not found. Please install GCC first."
    exit 1
fi

# Get GCC version
GCC_VERSION=$(gcc --version | head -n1 | awk '{print $NF}')
log_info "GCC version: $GCC_VERSION"

# Validate GCC version
GCC_MAJOR=$(echo $GCC_VERSION | cut -d. -f1)
if [[ $GCC_MAJOR -lt 13 ]]; then
    log_warn "GCC version $GCC_VERSION is older than recommended (13.x)"
fi

# Set environment variables
export CC=gcc
export CXX=g++

# Configure CMake for GCC
log_info "Configuring CMake for GCC..."
cat > /tmp/gcc_toolchain.cmake << 'EOF'
cmake_minimum_required(3.20)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_FLAGS "-march=native -O3")
set(CMAKE_CXX_FLAGS "-march=native -O3")
EOF

log_info "GCC setup complete!"
```

### 4. Clang Setup Script

Create Clang setup script:

```bash
#!/bin/bash
# scripts/linux/setup_clang.sh

set -euo pipefail

log_info "Setting up Clang compiler..."

# Check Clang is installed
if ! command -v clang &> /dev/null; then
    log_error "Clang not found. Please install Clang first."
    exit 1
fi

# Get Clang version
CLANG_VERSION=$(clang --version | head -n1 | awk '{print $NF}')
log_info "Clang version: $CLANG_VERSION"

# Validate Clang version
CLANG_MAJOR=$(echo $CLANG_VERSION | cut -d. -f1)
if [[ $CLANG_MAJOR -lt 19 ]]; then
    log_warn "Clang version $CLANG_VERSION is older than recommended (19.x)"
fi

# Set environment variables
export CC=clang
export CXX=clang++

# Configure CMake for Clang
log_info "Configuring CMake for Clang..."
cat > /tmp/clang_toolchain.cmake << 'EOF'
cmake_minimum_required(3.20)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_C_FLAGS "-march=native -O3")
set(CMAKE_CXX_FLAGS "-march=native -O3")
EOF

log_info "Clang setup complete!"
```

### 5. CachyOS Setup Script

Create CachyOS-specific setup script:

```bash
#!/bin/bash
# scripts/linux/setup_cachyos.sh

set -euo pipefail

log_info "Setting up CachyOS-specific configuration..."

# Check if running on CachyOS
if [[ ! -f /etc/os-release ]] || ! grep -q "ID=cachyos" /etc/os-release; then
    log_warn "Not running on CachyOS. Skipping CachyOS setup."
    exit 0
fi

# Enable CachyOS performance optimizations
log_info "Enabling CachyOS performance optimizations..."

# Set CachyOS-specific compiler flags
export CACHYOS_FLAGS="-march=native -O3 -flto -DNDEBUG"

# Configure CMake for CachyOS
log_info "Configuring CMake for CachyOS..."
cat > /tmp/cachyos_toolchain.cmake << 'EOF'
cmake_minimum_required(3.20)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_FLAGS "-march=native -O3 -flto -DNDEBUG")
set(CMAKE_CXX_FLAGS "-march=native -O3 -flto -DNDEBUG")
set(CMAKE_EXE_LINKER_FLAGS "-Wl,--as-needed -Wl,--no-undefined -flto")
set(CMAKE_SHARED_LINKER_FLAGS "-Wl,--as-needed -Wl,--no-undefined -flto")
EOF

# Enable Wayland by default
export QT_QPA_PLATFORM=wayland

log_info "CachyOS setup complete!"
```

### 6. Nix Setup Script

Create Nix setup script:

```bash
#!/bin/bash
# scripts/linux/setup_nix.sh

set -euo pipefail

log_info "Setting up Nix environment..."

# Check Nix is installed
if ! command -v nix &> /dev/null; then
    log_error "Nix not found. Please install Nix first."
    log_info "Visit https://nixos.org/download.html for installation instructions."
    exit 1
fi

# Check Nix flakes are enabled
if ! nix flake show &> /dev/null 2>&1; then
    log_warn "Nix flakes may not be enabled."
    log_info "Add 'experimental-features = nix-command flakes' to ~/.config/nix/nix.conf"
fi

# Enter Nix environment
log_info "Entering Nix development environment..."
nix develop

log_info "Nix setup complete!"
```

### 7. Conan Setup Script

Create Conan setup script:

```bash
#!/bin/bash
# scripts/linux/setup_conan.sh

set -euo pipefail

log_info "Setting up Conan package manager..."

# Check Conan is installed
if ! command -v conan &> /dev/null; then
    log_error "Conan not found. Please install Conan first."
    log_info "Install with: pip install conan"
    exit 1
fi

# Get Conan version
CONAN_VERSION=$(conan --version)
log_info "Conan version: $CONAN_VERSION"

# Configure Conan
log_info "Configuring Conan..."

# Set Conan home directory
export CONAN_USER_HOME=$PWD/.conan2
log_info "Conan home directory: $CONAN_USER_HOME"

# Create Conan home directory
mkdir -p "$CONAN_USER_HOME"

# Configure Conan profiles
log_info "Configuring Conan profiles..."
CONAN_PROFILES_DIR=$PWD/conan/profiles
if [[ -d "$CONAN_PROFILES_DIR" ]]; then
    log_info "Conan profiles directory: $CONAN_PROFILES_DIR"
else
    log_warn "Conan profiles directory not found: $CONAN_PROFILES_DIR"
fi

# Validate Conan installation
log_info "Validating Conan installation..."
conan --version
conan profile show default || log_warn "Default Conan profile not found"

log_info "Conan setup complete!"
```

### 8. Dependencies Setup Script

Create system dependencies setup script:

```bash
#!/bin/bash
# scripts/linux/setup_dependencies.sh

set -euo pipefail

log_info "Installing system dependencies..."

# Detect package manager
if command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
elif command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
else
    log_error "No supported package manager found."
    exit 1
fi

log_info "Package manager: $PKG_MANAGER"

# Install dependencies based on package manager
case $PKG_MANAGER in
    pacman)
        log_info "Installing dependencies with pacman..."
        sudo pacman -S --needed --noconfirm \
            gcc \
            clang \
            cmake \
            ninja \
            python \
            python-pip \
            git
        ;;
    apt)
        log_info "Installing dependencies with apt..."
        sudo apt update
        sudo apt install -y \
            gcc \
            clang \
            cmake \
            ninja-build \
            python3 \
            python3-pip \
            git
        ;;
    dnf)
        log_info "Installing dependencies with dnf..."
        sudo dnf install -y \
            gcc \
            clang \
            cmake \
            ninja-build \
            python3 \
            python3-pip \
            git
        ;;
esac

# Install Python packages
log_info "Installing Python packages..."
pip install --user conan

log_info "System dependencies installed!"
```

### 9. Validation Script

Create validation script:

```bash
#!/bin/bash
# scripts/linux/validate.sh

set -euo pipefail

log_info "Validating setup..."

ERRORS=0

# Check GCC
if command -v gcc &> /dev/null; then
    log_info "✓ GCC found: $(gcc --version | head -n1)"
else
    log_error "✗ GCC not found"
    ((ERRORS++))
fi

# Check Clang
if command -v clang &> /dev/null; then
    log_info "✓ Clang found: $(clang --version | head -n1)"
else
    log_warn "✗ Clang not found (optional)"
fi

# Check CMake
if command -v cmake &> /dev/null; then
    log_info "✓ CMake found: $(cmake --version | head -n1)"
else
    log_error "✗ CMake not found"
    ((ERRORS++))
fi

# Check Ninja
if command -v ninja &> /dev/null; then
    log_info "✓ Ninja found: $(ninja --version)"
else
    log_error "✗ Ninja not found"
    ((ERRORS++))
fi

# Check Conan
if command -v conan &> /dev/null; then
    log_info "✓ Conan found: $(conan --version)"
else
    log_error "✗ Conan not found"
    ((ERRORS++))
fi

# Check Python
if command -v python &> /dev/null; then
    log_info "✓ Python found: $(python --version)"
else
    log_error "✗ Python not found"
    ((ERRORS++))
fi

# Check Nix
if command -v nix &> /dev/null; then
    log_info "✓ Nix found: $(nix --version)"
else
    log_warn "✗ Nix not found (optional)"
fi

# Summary
if [[ $ERRORS -eq 0 ]]; then
    log_info "✓ All required dependencies found!"
    exit 0
else
    log_error "✗ $ERRORS required dependencies missing!"
    exit 1
fi
```

### 10. Rollback Script

Create rollback script:

```bash
#!/bin/bash
# scripts/linux/rollback.sh

set -euo pipefail

log_info "Rolling back changes..."

# Remove Conan cache
if [[ -d .conan2 ]]; then
    log_info "Removing Conan cache..."
    rm -rf .conan2
fi

# Remove build directory
if [[ -d build ]]; then
    log_info "Removing build directory..."
    rm -rf build
fi

# Remove CMake cache
if [[ -f CMakeCache.txt ]]; then
    log_info "Removing CMake cache..."
    rm -f CMakeCache.txt
fi

log_info "Rollback complete!"
```

## Consequences

### Positive

1. **Complete Linux Setup:** Comprehensive setup scripts for Linux
2. **Idempotent:** Can be run multiple times safely
3. **Error Handling:** Graceful error handling
4. **User Feedback:** Clear feedback to user
5. **Validation:** Validates setup is complete
6. **Rollback:** Ability to rollback changes
7. **Logging:** Logs all actions
8. **Documentation:** Well-documented scripts
9. **Cross-Distribution:** Works on multiple distributions
10. **Modular:** Modular script architecture

### Negative

1. **Script Complexity:** More complex than Windows scripts
2. **Maintenance Burden:** More scripts to maintain
3. **Distribution Differences:** Different distributions may need different scripts
4. **Testing Burden:** Need to test on multiple distributions
5. **Documentation Burden:** Need to document all scripts
6. **Error Scenarios:** Many error scenarios to handle
7. **Permission Issues:** May need sudo for some operations
8. **User Confusion:** Users may not know which script to run

### Neutral

1. **Script Organization:** Need to organize scripts logically
2. **Script Naming:** Need consistent naming convention
3. **Script Documentation:** Need to document script usage
4. **Script Testing:** Need to test all scripts

## Alternatives Considered

### Alternative 1: Single Setup Script

**Description:** Use single setup script for all operations

**Pros:**
- Fewer scripts
- Simpler maintenance
- Easier to run

**Cons:**
- Less modular
- Harder to debug
- Less flexible
- Monolithic script

**Rejected:** Less modular, harder to debug

### Alternative 2: Use OmniCppController.py Only

**Description:** Use OmniCppController.py for all setup, no separate scripts

**Pros:**
- Single entry point
- Consistent interface
- Less scripts

**Cons:**
- Python dependency
- Less flexible
- Harder to debug
- Not standard practice

**Rejected:** Less flexible, not standard practice

### Alternative 3: Ansible Playbooks

**Description:** Use Ansible for setup automation

**Pros:**
- Declarative
- Idempotent
- Well-tested
- Powerful

**Cons:**
- Additional dependency
- Learning curve
- Overkill for this use case
- Complex to debug

**Rejected:** Overkill, additional dependency

### Alternative 4: Docker Containers

**Description:** Use Docker containers for environment setup

**Pros:**
- Consistent environment
- Isolated
- Reproducible

**Cons:**
- Not suitable for graphics development
- Container overhead
- Complex to set up
- Not aligned with Nix approach

**Rejected:** Not suitable for graphics, not aligned with Nix

## Related ADRs

- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-033: Repository Cleanup Strategy](ADR-033-repository-cleanup-strategy.md)

## Threat Model References

- **TM-LX-007: Setup Script Security** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - Command injection in setup scripts
  - Path traversal in script execution
  - Privilege escalation
  - Mitigation: Validate all inputs, use secure defaults, avoid running as root, sanitize paths

## References

- [Bash Best Practices](https://google.github.io/styleguide/shellguide.html)
- [Linux Setup Guide](../../docs/linux-builds.md)
- [Conan Installation](https://docs.conan.io/en/latest/installation.html)
- [Nix Installation](https://nixos.org/download.html)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
