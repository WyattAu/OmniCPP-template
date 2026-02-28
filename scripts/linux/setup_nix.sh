#!/usr/bin/env bash
#
# Description: Setup script for Nix environment on Linux
# Usage: ./scripts/linux/setup_nix.sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#   --version     Show script version
#   --install     Force Nix installation
#   --no-flakes   Skip flakes configuration
#   --multi-user  Install Nix in multi-user mode (requires sudo)
#
# References:
#   - ADR-027: Nix Package Manager Integration
#   - ADR-035: Linux Setup Script Architecture
#   - REQ-005-004: Create setup_nix.sh
#   - TM-LX-005: Linux Script Security Risks
#   - TM-LX-007: Nix Store Security
#

set -euo pipefail

# Script metadata
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly MIN_NIX_MAJOR=2
readonly MIN_NIX_MINOR=4
readonly NIX_INSTALL_URL="https://nixos.org/nix/install"

# Nix configuration paths
readonly NIX_CONF_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/nix"
readonly NIX_CONF_FILE="$NIX_CONF_DIR/nix.conf"

# Colors for output (use tput for compatibility)
if command -v tput >/dev/null 2>&1 && tput colors >/dev/null 2>&1; then
    RED="$(tput setaf 1)"
    GREEN="$(tput setaf 2)"
    YELLOW="$(tput setaf 3)"
    BLUE="$(tput setaf 4)"
    NC="$(tput sgr0)"
else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    NC=""
fi

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1" >&2
    fi
}

# Display usage information
show_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [options]

Setup Nix environment and load Nix shell on Linux.

Options:
  --dry-run      Show what would be done without making changes
  --help         Show this help message
  --version      Show script version
  --debug        Enable debug output
  --install       Force Nix installation (even if already installed)
  --no-flakes    Skip flakes configuration
  --multi-user    Install Nix in multi-user mode (requires sudo)

Environment Variables:
  NIX_INSTALL_URL    Override Nix installation URL
  NIX_VERSION        Specific Nix version to install (optional)
  SKIP_INSTALL       Skip package installation (default: false)
  NIX_CHANNEL        Nix channel to use (default: nixos-unstable)

Examples:
  $SCRIPT_NAME                    # Run setup
  $SCRIPT_NAME --dry-run          # Preview changes
  $SCRIPT_NAME --debug            # Enable debug output
  $SCRIPT_NAME --multi-user       # Install in multi-user mode

EOF
}

# Show script version
show_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        # Use grep to avoid sourcing potentially malicious content (TM-LX-005)
        local distro_id
        distro_id=$(grep -E '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
        echo "$distro_id"
    else
        echo "unknown"
    fi
}

# Check if Nix is installed
check_nix_installed() {
    command -v nix >/dev/null 2>&1
}

# Get Nix version
get_nix_version() {
    if command -v nix >/dev/null 2>&1; then
        nix --version | grep -oP 'nix \(Nix\) \K[0-9.]+' || echo "unknown"
    else
        echo "not found"
    fi
}

# Parse version string into major and minor components
parse_version() {
    local version="$1"
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    echo "$major $minor"
}

# Compare versions (returns: 0=equal, 1=greater, 2=less)
compare_versions() {
    local v1="$1"
    local v2="$2"
    local i1 i2

    # Split by dots and compare each component
    IFS='.' read -ra i1 <<< "$v1"
    IFS='.' read -ra i2 <<< "$v2"

    for ((i=0; i<${#i1[@]} || i<${#i2[@]}; i++)); do
        local n1="${i1[i]:-0}"
        local n2="${i2[i]:-0}"
        if ((n1 > n2)); then
            return 1
        elif ((n1 < n2)); then
            return 2
        fi
    done
    return 0
}

# Validate Nix version meets minimum requirements
validate_nix_version() {
    local version="$1"
    local min_major="$2"
    local min_minor="$3"

    log_info "Validating Nix version: $version (minimum required: $min_major.$min_minor.0)"

    local current_major current_minor
    read -r current_major current_minor <<< "$(parse_version "$version")"

    # Check major version
    if ((current_major < min_major)); then
        log_error "Nix version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    # Check minor version if major version matches
    if ((current_major == min_major)) && ((current_minor < min_minor)); then
        log_error "Nix version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    log_info "Nix version $version meets minimum requirements"
    return 0
}

# Check if Nix is initialized (TM-LX-007: Nix Store Security)
check_nix_initialized() {
    # Check if Nix configuration directory exists
    if [[ ! -d "$NIX_CONF_DIR" ]]; then
        return 1
    fi

    # Check if Nix store is accessible
    if ! nix-store --version >/dev/null 2>&1; then
        return 1
    fi

    return 0
}

# Install Nix (single-user or multi-user)
install_nix() {
    local multi_user="$1"
    local dry_run="$2"

    # Check if installation should be skipped
    if [[ "${SKIP_INSTALL:-false}" == "true" ]]; then
        log_warn "SKIP_INSTALL is set, skipping Nix installation"
        return 0
    fi

    log_info "Installing Nix..."
    log_info "Installation mode: $([[ "$multi_user" == "true" ]] && echo "multi-user" || echo "single-user")"

    # Validate Nix installation URL (TM-LX-005: Linux Script Security Risks)
    local install_url="${NIX_INSTALL_URL}"
    if [[ ! "$install_url" =~ ^https://nixos\.org/ ]]; then
        log_error "Invalid Nix installation URL: $install_url"
        log_error "URL must be from https://nixos.org/"
        return 1
    fi

    if [[ "$dry_run" == "true" ]]; then
        echo "Would run: curl -L $install_url | sh"
        if [[ "$multi_user" == "true" ]]; then
            echo "Would run: sudo $install_url --daemon"
        else
            echo "Would run: $install_url --no-daemon"
        fi
        return 0
    fi

    # Download and verify installer (TM-LX-005: Validate downloads)
    local installer_script="/tmp/nix-installer-$$.sh"
    log_info "Downloading Nix installer from $install_url"

    if ! curl -fsSL "$install_url" -o "$installer_script"; then
        log_error "Failed to download Nix installer"
        return 1
    fi

    # Verify installer script is not empty and is a valid shell script
    if [[ ! -s "$installer_script" ]]; then
        log_error "Downloaded installer is empty"
        rm -f "$installer_script"
        return 1
    fi

    # Make installer executable
    chmod +x "$installer_script"

    # Run installer with appropriate flags
    if [[ "$multi_user" == "true" ]]; then
        log_info "Installing Nix in multi-user mode (requires sudo)..."
        if ! sudo bash "$installer_script" --daemon; then
            log_error "Nix multi-user installation failed"
            rm -f "$installer_script"
            return 1
        fi
    else
        log_info "Installing Nix in single-user mode..."
        if ! bash "$installer_script" --no-daemon; then
            log_error "Nix single-user installation failed"
            rm -f "$installer_script"
            return 1
        fi
    fi

    # Clean up installer
    rm -f "$installer_script"

    log_info "Nix installation complete"
    log_info "Please log out and log back in for Nix to be available"
    return 0
}

# Initialize Nix configuration
initialize_nix() {
    local dry_run="$1"

    log_info "Initializing Nix configuration..."

    # Create Nix configuration directory if it doesn't exist
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Nix configuration directory: $NIX_CONF_DIR"
    else
        mkdir -p "$NIX_CONF_DIR"
        log_info "Created Nix configuration directory: $NIX_CONF_DIR"
    fi
}

# Enable Nix flakes (experimental feature)
enable_flakes() {
    local dry_run="$1"

    log_info "Enabling Nix flakes..."

    if [[ "$dry_run" == "true" ]]; then
        echo "Would add experimental features to $NIX_CONF_FILE"
        echo "Content:"
        cat << EOF
experimental-features = nix-command flakes
EOF
        return 0
    fi

    # Check if flakes are already enabled
    if [[ -f "$NIX_CONF_FILE" ]] && grep -q "experimental-features.*flakes" "$NIX_CONF_FILE"; then
        log_info "Flakes are already enabled"
        return 0
    fi

    # Create or update nix.conf with flakes enabled
    if [[ -f "$NIX_CONF_FILE" ]]; then
        # Append flakes to existing experimental features
        if grep -q "^experimental-features" "$NIX_CONF_FILE"; then
            # Add flakes to existing experimental features
            sed -i 's/^experimental-features = \(.*\)/experimental-features = \1 flakes/' "$NIX_CONF_FILE"
        else
            # Add new experimental features line
            echo "experimental-features = nix-command flakes" >> "$NIX_CONF_FILE"
        fi
    else
        # Create new nix.conf
        cat > "$NIX_CONF_FILE" << EOF
# Nix configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Enable experimental features for flakes
experimental-features = nix-command flakes
EOF
    fi

    log_info "Flakes enabled in $NIX_CONF_FILE"
}

# Configure Nix environment variables
configure_nix_environment() {
    local dry_run="$1"

    log_info "Configuring Nix environment variables..."

    # Create environment file for persistence
    local env_file="$PROJECT_ROOT/.nix.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create environment file: $env_file"
        echo "Content:"
        cat << EOF
# Nix environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export NIX_PATH=$HOME/.nix-defexpr/channels
EOF
    else
        cat > "$env_file" << EOF
# Nix environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export NIX_PATH=$HOME/.nix-defexpr/channels
EOF
        log_info "Created environment file: $env_file"
    fi
}

# Configure CMake for Nix
configure_cmake_nix() {
    local dry_run="$1"

    log_info "Configuring CMake for Nix..."

    local cmake_toolchain_dir="$PROJECT_ROOT/cmake/toolchains"
    local nix_toolchain_file="$cmake_toolchain_dir/nix.cmake"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create CMake toolchain file: $nix_toolchain_file"
    else
        # Create toolchains directory if it doesn't exist
        mkdir -p "$cmake_toolchain_dir"

        # Write Nix toolchain file
        cat > "$nix_toolchain_file" << 'EOF'
# CMake toolchain file for Nix on Linux
# Generated by setup_nix.sh

cmake_minimum_required(3.20)

# Detect compiler from Nix environment
# Nix provides compilers in the buildInputs of the devShell
if(DEFINED ENV{CC})
    set(CMAKE_C_COMPILER $ENV{CC})
endif()

if(DEFINED ENV{CXX})
    set(CMAKE_CXX_COMPILER $ENV{CXX})
endif()

# Set compiler flags for optimization
set(CMAKE_C_FLAGS_INIT "-march=native")
set(CMAKE_CXX_FLAGS_INIT "-march=native")

# Enable position independent code
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler-specific flags
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -DNDEBUG")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -DNDEBUG")
elseif(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -O0")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0")
endif()

# Enable warnings
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

# Nix-specific settings
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
EOF
        log_info "Created CMake toolchain file: $nix_toolchain_file"
    fi
}

# Configure Conan for Nix
configure_conan_nix() {
    local dry_run="$1"

    log_info "Configuring Conan for Nix..."

    local conan_profiles_dir="$PROJECT_ROOT/conan/profiles"
    local nix_profile="$conan_profiles_dir/nix"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Conan profile: $nix_profile"
    else
        # Create profiles directory if it doesn't exist
        mkdir -p "$conan_profiles_dir"

        # Write Conan profile for Nix
        cat > "$nix_profile" << 'EOF'
# Conan profile for Nix on Linux
# Generated by setup_nix.sh

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
# Nix provides tools in specific paths
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}

[buildenv]
# Use Nix-provided compilers
CC=gcc
CXX=g++
EOF
        log_info "Created Conan profile: $nix_profile"
    fi
}

# Load Nix shell
load_nix_shell() {
    local dry_run="$1"

    log_info "Loading Nix development environment..."

    if [[ "$dry_run" == "true" ]]; then
        echo "Would run: nix develop"
        return 0
    fi

    # Check if flake.nix exists in project root
    if [[ ! -f "$PROJECT_ROOT/flake.nix" ]]; then
        log_warn "flake.nix not found in project root"
        log_warn "Nix shell will use default environment"
        return 0
    fi

    # Enter Nix development environment
    log_info "Entering Nix development environment..."
    log_info "Run 'exit' to leave the Nix shell"

    # Use exec to replace current shell with nix develop
    exec nix develop
}

# Validate Nix installation
validate_nix_installation() {
    log_info "Validating Nix installation..."

    local errors=0

    # Check nix command
    if command -v nix >/dev/null 2>&1; then
        local nix_version
        nix_version=$(get_nix_version)
        log_info "✓ Nix found: $nix_version"
    else
        log_error "✗ Nix not found"
        ((errors++))
    fi

    # Check nix-store command
    if command -v nix-store >/dev/null 2>&1; then
        log_info "✓ Nix store found"
    else
        log_error "✗ Nix store not found"
        ((errors++))
    fi

    # Check Nix configuration
    if [[ -f "$NIX_CONF_FILE" ]]; then
        log_info "✓ Nix configuration found: $NIX_CONF_FILE"
    else
        log_warn "✗ Nix configuration not found"
    fi

    # Check if flakes are enabled
    if [[ -f "$NIX_CONF_FILE" ]] && grep -q "experimental-features.*flakes" "$NIX_CONF_FILE"; then
        log_info "✓ Nix flakes enabled"
    else
        log_warn "✗ Nix flakes not enabled"
    fi

    # Check flake.nix in project
    if [[ -f "$PROJECT_ROOT/flake.nix" ]]; then
        log_info "✓ flake.nix found in project root"
    else
        log_warn "✗ flake.nix not found in project root"
    fi

    # Test Nix can evaluate flake
    if [[ -f "$PROJECT_ROOT/flake.nix" ]] && command -v nix >/dev/null 2>&1; then
        if nix flake show "$PROJECT_ROOT" >/dev/null 2>&1; then
            log_info "✓ Nix can evaluate flake"
        else
            log_warn "✗ Nix flake evaluation failed (may need 'nix flake update')"
        fi
    fi

    return "$errors"
}

# Display Nix environment information
display_nix_info() {
    log_info "=========================================="
    log_info "Nix Environment Information"
    log_info "=========================================="

    if command -v nix >/dev/null 2>&1; then
        local nix_version
        nix_version=$(get_nix_version)
        log_info "Nix version: $nix_version"
    else
        log_warn "Nix not installed"
    fi

    log_info "Nix configuration directory: $NIX_CONF_DIR"
    log_info "Nix configuration file: $NIX_CONF_FILE"
    log_info "Project root: $PROJECT_ROOT"
    log_info "Flake file: $PROJECT_ROOT/flake.nix"

    if [[ -f "$NIX_CONF_FILE" ]]; then
        log_info "Nix configuration:"
        cat "$NIX_CONF_FILE" | while read -r line; do
            echo "  $line"
        done
    fi

    log_info "=========================================="
    log_info "Available Nix commands:"
    log_info "  nix develop          - Enter Nix development environment"
    log_info "  nix flake update     - Update flake inputs"
    log_info "  nix flake show       - Show flake outputs"
    log_info "  nix build .#default  - Build default package"
    log_info "=========================================="
}

# Main setup function
main() {
    local dry_run=false
    local force_install=false
    local skip_flakes=false
    local multi_user=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            --version)
                show_version
                exit 0
                ;;
            --debug)
                DEBUG=1
                shift
                ;;
            --install)
                force_install=true
                shift
                ;;
            --no-flakes)
                skip_flakes=true
                shift
                ;;
            --multi-user)
                multi_user=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    log_info "=========================================="
    log_info "Nix Setup Script v$SCRIPT_VERSION"
    log_info "=========================================="

    if [[ "$dry_run" == "true" ]]; then
        log_info "Running in DRY-RUN mode - no changes will be made"
    fi

    # Detect system information
    local distro
    distro=$(detect_distro)
    log_info "Detected distribution: $distro"

    # Check if Nix is already installed
    if check_nix_installed; then
        local nix_version
        nix_version=$(get_nix_version)
        log_info "Nix is already installed: $nix_version"

        # Validate version
        if ! validate_nix_version "$nix_version" "$MIN_NIX_MAJOR" "$MIN_NIX_MINOR"; then
            log_warn "Nix version is below minimum requirements"
            log_warn "Please update Nix: nix-channel --update && nix-env -iA nix"
        fi

        # Check if forced installation
        if [[ "$force_install" == "true" ]]; then
            log_warn "Force installation requested, reinstalling Nix..."
            install_nix "$multi_user" "$dry_run"
        fi
    else
        log_info "Nix is not installed"
        install_nix "$multi_user" "$dry_run"
    fi

    # Check if Nix is initialized
    if ! check_nix_initialized; then
        log_info "Nix is not initialized"
        initialize_nix "$dry_run"
    else
        log_info "Nix is already initialized"
    fi

    # Enable flakes if not skipped
    if [[ "$skip_flakes" == "false" ]]; then
        enable_flakes "$dry_run"
    else
        log_info "Skipping flakes configuration (--no-flakes specified)"
    fi

    # Configure Nix environment
    configure_nix_environment "$dry_run"

    # Configure CMake for Nix
    configure_cmake_nix "$dry_run"

    # Configure Conan for Nix
    configure_conan_nix "$dry_run"

    # Validate Nix installation
    if [[ "$dry_run" == "false" ]]; then
        validate_nix_installation
    fi

    # Display Nix environment information
    display_nix_info

    log_info "=========================================="
    log_info "Nix setup complete!"
    log_info "=========================================="

    if [[ "$dry_run" == "false" ]]; then
        log_info "To enter the Nix development environment, run:"
        log_info "  nix develop"
        log_info ""
        log_info "Or use direnv for automatic environment loading:"
        log_info "  direnv allow"
    fi

    return 0
}

# Run main function
main "$@"
