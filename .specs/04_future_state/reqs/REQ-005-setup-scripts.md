# REQ-005: Setup Scripts

**Requirement ID:** REQ-005
**Title:** Setup Scripts
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

Setup scripts shall be created to configure compiler environments, Nix integration, Qt6/Vulkan dependencies, and validate the build environment on Linux.

### Overview

The system shall:
1. Create setup_gcc.sh script
2. Create setup_clang.sh script
3. Create setup_cachyos.sh script
4. Create setup_nix.sh script
5. Create setup_qt6_vulkan.sh script
6. Create validate_environment.sh script

---

## REQ-005-001: Create setup_gcc.sh

### Description

A shell script shall be created to set up GCC compiler environment on Linux.

### Functional Requirements

The system shall:
1. Create [`scripts/setup_gcc.sh`](../../scripts/setup_gcc.sh:1) file
2. Check if GCC is installed
3. Install GCC if not installed
4. Set CC=gcc environment variable
5. Set CXX=g++ environment variable
6. Verify GCC version meets minimum requirements
7. Log setup progress
8. Provide usage instructions
9. Make script executable
10. Support dry-run mode

### Acceptance Criteria

- [ ] [`scripts/setup_gcc.sh`](../../scripts/setup_gcc.sh:1) file exists
- [ ] Script checks if GCC is installed
- [ ] Script installs GCC if not installed
- [ ] Script sets CC=gcc
- [ ] Script sets CXX=g++
- [ ] Script verifies GCC version
- [ ] Script logs setup progress
- [ ] Script provides usage instructions
- [ ] Script is executable
- [ ] Script supports dry-run mode

### Priority

**High** - GCC setup script is required for GCC builds.

### Dependencies

- None

### Related ADRs

- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test GCC Setup Script**
   - **Description:** Verify GCC setup script works
   - **Steps:**
     1. Run `./scripts/setup_gcc.sh`
     2. Verify GCC is installed
     3. Verify environment variables are set
     4. Verify version check passes
   - **Expected Result:** GCC is set up correctly

---

## REQ-005-002: Create setup_clang.sh

### Description

A shell script shall be created to set up Clang compiler environment on Linux.

### Functional Requirements

The system shall:
1. Create [`scripts/setup_clang.sh`](../../scripts/setup_clang.sh:1) file
2. Check if Clang is installed
3. Install Clang if not installed
4. Set CC=clang environment variable
5. Set CXX=clang++ environment variable
6. Verify Clang version meets minimum requirements
7. Log setup progress
8. Provide usage instructions
9. Make script executable
10. Support dry-run mode

### Acceptance Criteria

- [ ] [`scripts/setup_clang.sh`](../../scripts/setup_clang.sh:1) file exists
- [ ] Script checks if Clang is installed
- [ ] Script installs Clang if not installed
- [ ] Script sets CC=clang
- [ ] Script sets CXX=clang++
- [ ] Script verifies Clang version
- [ ] Script logs setup progress
- [ ] Script provides usage instructions
- [ ] Script is executable
- [ ] Script supports dry-run mode

### Priority

**High** - Clang setup script is required for Clang builds.

### Dependencies

- None

### Related ADRs

- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Clang Setup Script**
   - **Description:** Verify Clang setup script works
   - **Steps:**
     1. Run `./scripts/setup_clang.sh`
     2. Verify Clang is installed
     3. Verify environment variables are set
     4. Verify version check passes
   - **Expected Result:** Clang is set up correctly

---

## REQ-005-003: Create setup_cachyos.sh

### Description

A shell script shall be created to set up CachyOS-specific compiler environment and optimizations.

### Functional Requirements

The system shall:
1. Create [`scripts/setup_cachyos.sh`](../../scripts/setup_cachyos.sh:1) file
2. Check if running on CachyOS
3. Install CachyOS-specific packages if needed
4. Apply CachyOS-specific compiler flags
5. Set CC=gcc environment variable
6. Set CXX=g++ environment variable
7. Verify GCC version meets minimum requirements
8. Log setup progress
9. Provide usage instructions
10. Make script executable
11. Support dry-run mode
12. Display CachyOS-specific optimizations

### Acceptance Criteria

- [ ] [`scripts/setup_cachyos.sh`](../../scripts/setup_cachyos.sh:1) file exists
- [ ] Script checks if running on CachyOS
- [ ] Script installs CachyOS-specific packages
- [ ] Script applies CachyOS-specific flags
- [ ] Script sets CC=gcc
- [ ] Script sets CXX=g++
- [ ] Script verifies GCC version
- [ ] Script logs setup progress
- [ ] Script provides usage instructions
- [ ] Script is executable
- [ ] Script supports dry-run mode
- [ ] Script displays CachyOS optimizations

### Priority

**High** - CachyOS setup script is required for CachyOS builds.

### Dependencies

- REQ-005-001: Create setup_gcc.sh

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- **TM-LX-002: Distribution-Specific Vulnerabilities** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:352)

### Test Cases

#### Integration Tests

1. **Test CachyOS Setup Script**
   - **Description:** Verify CachyOS setup script works
   - **Steps:**
     1. Run `./scripts/setup_cachyos.sh`
     2. Verify CachyOS is detected
     3. Verify packages are installed
     4. Verify flags are applied
   - **Expected Result:** CachyOS is set up correctly

---

## REQ-005-004: Create setup_nix.sh

### Description

A shell script shall be created to set up Nix environment and load Nix shell.

### Functional Requirements

The system shall:
1. Create [`scripts/setup_nix.sh`](../../scripts/setup_nix.sh:1) file
2. Check if Nix is installed
3. Install Nix if not installed
4. Initialize Nix if not initialized
5. Load Nix shell
6. Verify Nix environment is loaded
7. Log setup progress
8. Provide usage instructions
9. Make script executable
10. Support dry-run mode
11. Display Nix environment information

### Acceptance Criteria

- [ ] [`scripts/setup_nix.sh`](../../scripts/setup_nix.sh:1) file exists
- [ ] Script checks if Nix is installed
- [ ] Script installs Nix if not installed
- [ ] Script initializes Nix if not initialized
- [ ] Script loads Nix shell
- [ ] Script verifies Nix environment
- [ ] Script logs setup progress
- [ ] Script provides usage instructions
- [ ] Script is executable
- [ ] Script supports dry-run mode
- [ ] Script displays Nix environment information

### Priority

**High** - Nix setup script is required for Nix integration.

### Dependencies

- None

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)
- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Integration Tests

1. **Test Nix Setup Script**
   - **Description:** Verify Nix setup script works
   - **Steps:**
     1. Run `./scripts/setup_nix.sh`
     2. Verify Nix is installed
     3. Verify Nix shell is loaded
     4. Verify environment variables are set
   - **Expected Result:** Nix is set up correctly

---

## REQ-005-005: Create setup_qt6_vulkan.sh

### Description

A shell script shall be created to set up Qt6 and Vulkan dependencies on Linux.

### Functional Requirements

The system shall:
1. Create [`scripts/setup_qt6_vulkan.sh`](../../scripts/setup_qt6_vulkan.sh:1) file
2. Check if Qt6 is installed
3. Install Qt6 if not installed
4. Check if Vulkan is installed
5. Install Vulkan if not installed
6. Set QT_QPA_PLATFORM=wayland environment variable
7. Set VK_LAYER_PATH environment variable
8. Set VK_ICD_FILENAMES environment variable
9. Verify Qt6 version meets minimum requirements
10. Verify Vulkan version meets minimum requirements
11. Log setup progress
12. Provide usage instructions
13. Make script executable
14. Support dry-run mode

### Acceptance Criteria

- [ ] [`scripts/setup_qt6_vulkan.sh`](../../scripts/setup_qt6_vulkan.sh:1) file exists
- [ ] Script checks if Qt6 is installed
- [ ] Script installs Qt6 if not installed
- [ ] Script checks if Vulkan is installed
- [ ] Script installs Vulkan if not installed
- [ ] Script sets QT_QPA_PLATFORM=wayland
- [ ] Script sets VK_LAYER_PATH
- [ ] Script sets VK_ICD_FILENAMES
- [ ] Script verifies Qt6 version
- [ ] Script verifies Vulkan version
- [ ] Script logs setup progress
- [ ] Script provides usage instructions
- [ ] Script is executable
- [ ] Script supports dry-run mode

### Priority

**High** - Qt6/Vulkan setup script is required for graphics development.

### Dependencies

- REQ-002-004: Define Qt6 dependencies
- REQ-002-005: Define Vulkan dependencies

### Related ADRs

- [ADR-034: Qt6 and Vulkan Integration](../04_future_state/reqs/REQ-034-qt6-vulkan-integration.md)
- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Qt6/Vulkan Setup Script**
   - **Description:** Verify Qt6/Vulkan setup script works
   - **Steps:**
     1. Run `./scripts/setup_qt6_vulkan.sh`
     2. Verify Qt6 is installed
     3. Verify Vulkan is installed
     4. Verify environment variables are set
   - **Expected Result:** Qt6/Vulkan is set up correctly

---

## REQ-005-006: Create validate_environment.sh

### Description

A shell script shall be created to validate the Linux build environment.

### Functional Requirements

The system shall:
1. Create [`scripts/validate_environment.sh`](../../scripts/validate_environment.sh:1) file
2. Check compiler availability (GCC or Clang)
3. Check CMake availability
4. Check Ninja availability
5. Check Qt6 availability (if required)
6. Check Vulkan availability (if required)
7. Check Conan availability
8. Validate compiler version meets minimum requirements
9. Validate CMake version meets minimum requirements
10. Display validation results
11. Return exit code 0 if valid, 1 if invalid
12. Log validation results
13. Provide usage instructions
14. Make script executable

### Acceptance Criteria

- [ ] [`scripts/validate_environment.sh`](../../scripts/validate_environment.sh:1) file exists
- [ ] Script checks compiler availability
- [ ] Script checks CMake availability
- [ ] Script checks Ninja availability
- [ ] Script checks Qt6 availability
- [ ] Script checks Vulkan availability
- [ ] Script checks Conan availability
- [ ] Script validates compiler version
- [ ] Script validates CMake version
- [ ] Script displays validation results
- [ ] Script returns appropriate exit code
- [ ] Script logs validation results
- [ ] Script provides usage instructions
- [ ] Script is executable

### Priority

**High** - Environment validation script is required for build verification.

### Dependencies

- REQ-001-007: Validate Linux build environment

### Related ADRs

- [ADR-030: Enhanced OmniCppController.py Architecture](../02_adrs/ADR-030-enhanced-omnicppcontroller-architecture.md)
- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Environment Validation Script**
   - **Description:** Verify environment validation script works
   - **Steps:**
     1. Run `./scripts/validate_environment.sh`
     2. Verify all tools are checked
     3. Verify versions are validated
     4. Verify results are displayed
   - **Expected Result:** Environment is validated correctly

---

## Implementation Notes

### Script Structure

All setup scripts shall follow this structure:

```bash
#!/usr/bin/env bash
#
# Description: Setup script for [COMPONENT]
# Usage: ./scripts/setup_[COMPONENT].sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main setup logic
setup_component() {
    log_info "Setting up [COMPONENT]..."
    # Implementation here
    log_info "[COMPONENT] setup complete"
}

# Main script
main() {
    local dry_run=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --dry-run    Show what would be done without making changes"
                echo "  --help        Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Run setup
    setup_component
}

main "$@"
```

### setup_gcc.sh Example

```bash
#!/usr/bin/env bash
#
# Description: Setup script for GCC compiler on Linux
# Usage: ./scripts/setup_gcc.sh [options]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

setup_gcc() {
    log_info "Setting up GCC compiler..."

    # Check if GCC is installed
    if ! command -v gcc &> /dev/null; then
        log_warn "GCC not found, installing..."
        if [ "$dry_run" = false ]; then
            sudo pacman -S --noconfirm gcc
        else
            log_info "[DRY RUN] Would install GCC"
        fi
    else
        local gcc_version=$(gcc --version | head -n1 | awk '{print $3}')
        log_info "GCC version: $gcc_version"
    fi

    # Set environment variables
    export CC=gcc
    export CXX=g++
    log_info "CC=$CC"
    log_info "CXX=$CXX"

    log_info "GCC setup complete"
}

main() {
    local dry_run=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --dry-run    Show what would be done without making changes"
                echo "  --help        Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    setup_gcc
}

main "$@"
```

### validate_environment.sh Example

```bash
#!/usr/bin/env bash
#
# Description: Validate Linux build environment
# Usage: ./scripts/validate_environment.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

validate_compiler() {
    if command -v gcc &> /dev/null; then
        local gcc_version=$(gcc --version | head -n1 | awk '{print $3}')
        log_info "GCC version: $gcc_version"
        return 0
    elif command -v clang &> /dev/null; then
        local clang_version=$(clang --version | head -n1 | awk '{print $4}')
        log_info "Clang version: $clang_version"
        return 0
    else
        log_error "No compiler found (GCC or Clang)"
        return 1
    fi
}

validate_cmake() {
    if command -v cmake &> /dev/null; then
        local cmake_version=$(cmake --version | head -n1 | awk '{print $3}')
        log_info "CMake version: $cmake_version"
        return 0
    else
        log_error "CMake not found"
        return 1
    fi
}

validate_ninja() {
    if command -v ninja &> /dev/null; then
        local ninja_version=$(ninja --version | awk '{print $2}')
        log_info "Ninja version: $ninja_version"
        return 0
    else
        log_error "Ninja not found"
        return 1
    fi
}

main() {
    log_info "Validating build environment..."
    local valid=true

    validate_compiler || valid=false
    validate_cmake || valid=false
    validate_ninja || valid=false

    if [ "$valid" = true ]; then
        log_info "Build environment is valid"
        exit 0
    else
        log_error "Build environment is invalid"
        exit 1
    fi
}

main
```

### Script Documentation

All scripts shall include:
- Description header
- Usage information
- Options documentation
- Exit codes documentation
- Example usage

### Error Handling

All scripts shall:
- Use `set -euo pipefail` for error handling
- Log errors at ERROR level
- Return appropriate exit codes
- Provide actionable error messages

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-035: Linux Setup Script Architecture](../02_adrs/ADR-035-linux-setup-script-architecture.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
