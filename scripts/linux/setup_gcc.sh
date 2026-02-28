#!/usr/bin/env bash
#
# Description: Setup script for GCC compiler environment on Linux
# Usage: ./scripts/linux/setup_gcc.sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#   --version     Show script version
#
# References:
#   - ADR-035: Linux Setup Script Architecture
#   - REQ-005-001: Create setup_gcc.sh
#   - TM-LX-005: Linux Script Security Risks
#

set -euo pipefail

# Script metadata
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly MIN_GCC_MAJOR=13
readonly MIN_GCC_MINOR=0

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

Setup GCC compiler environment on Linux.

Options:
  --dry-run    Show what would be done without making changes
  --help        Show this help message
  --version     Show script version
  --debug       Enable debug output

Environment Variables:
  CC            Override C compiler (default: gcc)
  CXX           Override C++ compiler (default: g++)
  GCC_VERSION   Specific GCC version to install (optional)
  SKIP_INSTALL  Skip package installation (default: false)

Examples:
  $SCRIPT_NAME                    # Run setup
  $SCRIPT_NAME --dry-run          # Preview changes
  $SCRIPT_NAME --debug            # Enable debug output

EOF
}

# Show script version
show_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        # Source os-release to get distribution info
        # Using grep to avoid sourcing potentially malicious content
        local distro_id
        distro_id=$(grep -E '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
        echo "$distro_id"
    else
        echo "unknown"
    fi
}

# Detect package manager
detect_package_manager() {
    if command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    elif command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    elif command -v zypper >/dev/null 2>&1; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

# Check if GCC is installed
check_gcc_installed() {
    command -v gcc >/dev/null 2>&1
}

# Get GCC version
get_gcc_version() {
    if command -v gcc >/dev/null 2>&1; then
        gcc --version | head -n1 | awk '{print $NF}'
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

# Validate GCC version meets minimum requirements
validate_gcc_version() {
    local version="$1"
    local min_major="$2"
    local min_minor="$3"

    log_info "Validating GCC version: $version (minimum required: $min_major.$min_minor.0)"

    local current_major current_minor
    read -r current_major current_minor <<< "$(parse_version "$version")"

    # Check major version
    if ((current_major < min_major)); then
        log_error "GCC version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    # Check minor version if major version matches
    if ((current_major == min_major)) && ((current_minor < min_minor)); then
        log_error "GCC version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    log_info "GCC version $version meets minimum requirements"
    return 0
}

# Install GCC using appropriate package manager
install_gcc() {
    local distro="$1"
    local pkg_manager="$2"
    local dry_run="$3"
    local version="${4:-}"

    log_info "Package manager: $pkg_manager"
    log_info "Distribution: $distro"

    # Check if installation should be skipped
    if [[ "${SKIP_INSTALL:-false}" == "true" ]]; then
        log_warn "SKIP_INSTALL is set, skipping package installation"
        return 0
    fi

    case "$pkg_manager" in
        pacman)
            log_info "Installing GCC with pacman..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo pacman -S --needed --noconfirm gcc"
            else
                sudo pacman -S --needed --noconfirm gcc
            fi
            ;;
        apt)
            log_info "Installing GCC with apt..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo apt-get update"
                echo "Would run: sudo apt-get install -y gcc g++ build-essential"
            else
                sudo apt-get update
                sudo apt-get install -y gcc g++ build-essential
            fi
            ;;
        dnf|yum)
            log_info "Installing GCC with $pkg_manager..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo $pkg_manager install -y gcc gcc-c++ make"
            else
                sudo "$pkg_manager" install -y gcc gcc-c++ make
            fi
            ;;
        zypper)
            log_info "Installing GCC with zypper..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo zypper install -y gcc gcc-c++ make"
            else
                sudo zypper install -y gcc gcc-c++ make
            fi
            ;;
        *)
            log_error "Unsupported package manager: $pkg_manager"
            log_error "Please install GCC manually and run this script again"
            return 1
            ;;
    esac
}

# Configure GCC environment variables
configure_gcc_environment() {
    local dry_run="$1"

    log_info "Configuring GCC environment variables..."

    # Set compiler environment variables
    export CC="${CC:-gcc}"
    export CXX="${CXX:-g++}"

    log_info "CC=$CC"
    log_info "CXX=$CXX"

    # Create environment file for persistence
    local env_file="$PROJECT_ROOT/.gcc.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create environment file: $env_file"
        echo "Content:"
        cat << EOF
export CC=$CC
export CXX=$CXX
EOF
    else
        cat > "$env_file" << EOF
# GCC environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export CC=$CC
export CXX=$CXX
EOF
        log_info "Created environment file: $env_file"
    fi
}

# Configure CMake for GCC
configure_cmake_gcc() {
    local dry_run="$1"

    log_info "Configuring CMake for GCC..."

    local cmake_toolchain_dir="$PROJECT_ROOT/cmake/toolchains"
    local gcc_toolchain_file="$cmake_toolchain_dir/gcc-linux.cmake"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create CMake toolchain file: $gcc_toolchain_file"
    else
        # Create toolchains directory if it doesn't exist
        mkdir -p "$cmake_toolchain_dir"

        # Write GCC toolchain file
        cat > "$gcc_toolchain_file" << 'EOF'
# CMake toolchain file for GCC on Linux
# Generated by setup_gcc.sh

cmake_minimum_required(3.20)

# Set compilers
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

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
EOF
        log_info "Created CMake toolchain file: $gcc_toolchain_file"
    fi
}

# Configure Conan for GCC
configure_conan_gcc() {
    local dry_run="$1"
    local gcc_version="$2"

    log_info "Configuring Conan for GCC..."

    local conan_profiles_dir="$PROJECT_ROOT/conan/profiles"
    local gcc_profile="$conan_profiles_dir/gcc-linux"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Conan profile: $gcc_profile"
    else
        # Create profiles directory if it doesn't exist
        mkdir -p "$conan_profiles_dir"

        # Write Conan profile for GCC
        cat > "$gcc_profile" << EOF
# Conan profile for GCC on Linux
# Generated by setup_gcc.sh

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=$gcc_version
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}

[buildenv]
CC=gcc
CXX=g++
EOF
        log_info "Created Conan profile: $gcc_profile"
    fi
}

# Validate GCC installation
validate_gcc_installation() {
    log_info "Validating GCC installation..."

    local errors=0

    # Check gcc command
    if command -v gcc >/dev/null 2>&1; then
        local gcc_version
        gcc_version=$(get_gcc_version)
        log_info "✓ GCC found: $gcc_version"
    else
        log_error "✗ GCC not found"
        ((errors++))
    fi

    # Check g++ command
    if command -v g++ >/dev/null 2>&1; then
        local gxx_version
        gxx_version=$(g++ --version | head -n1 | awk '{print $NF}')
        log_info "✓ G++ found: $gxx_version"
    else
        log_error "✗ G++ not found"
        ((errors++))
    fi

    # Check CC environment variable
    if [[ -n "${CC:-}" ]]; then
        log_info "✓ CC environment variable: $CC"
    else
        log_warn "✗ CC environment variable not set"
    fi

    # Check CXX environment variable
    if [[ -n "${CXX:-}" ]]; then
        log_info "✓ CXX environment variable: $CXX"
    else
        log_warn "✗ CXX environment variable not set"
    fi

    # Test compilation
    if command -v gcc >/dev/null 2>&1; then
        local test_file="/tmp/gcc_test_$$.c"
        local test_output="/tmp/gcc_test_$$.out"

        echo '#include <stdio.h>' > "$test_file"
        echo 'int main() { printf("Hello from GCC\\n"); return 0; }' >> "$test_file"

        if gcc "$test_file" -o "$test_output" 2>/dev/null; then
            log_info "✓ GCC can compile C programs"
            rm -f "$test_file" "$test_output"
        else
            log_error "✗ GCC compilation test failed"
            ((errors++))
            rm -f "$test_file" "$test_output"
        fi
    fi

    return "$errors"
}

# Main setup function
main() {
    local dry_run=false

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
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    log_info "=========================================="
    log_info "GCC Setup Script v$SCRIPT_VERSION"
    log_info "=========================================="

    if [[ "$dry_run" == "true" ]]; then
        log_info "Running in DRY-RUN mode - no changes will be made"
    fi

    # Detect system information
    local distro pkg_manager
    distro=$(detect_distro)
    pkg_manager=$(detect_package_manager)

    log_info "Detected distribution: $distro"
    log_info "Detected package manager: $pkg_manager"

    # Check if GCC is already installed
    if check_gcc_installed; then
        local gcc_version
        gcc_version=$(get_gcc_version)
        log_info "GCC is already installed: $gcc_version"

        # Validate version
        if ! validate_gcc_version "$gcc_version" "$MIN_GCC_MAJOR" "$MIN_GCC_MINOR"; then
            log_warn "GCC version is below minimum requirements"
            log_warn "Consider upgrading GCC to version $MIN_GCC_MAJOR.$MIN_GCC_MINOR.0 or later"
        fi
    else
        log_warn "GCC is not installed"
        log_info "Installing GCC..."

        if ! install_gcc "$distro" "$pkg_manager" "$dry_run" "${GCC_VERSION:-}"; then
            log_error "Failed to install GCC"
            exit 1
        fi

        if [[ "$dry_run" == "false" ]]; then
            # Verify installation
            if ! check_gcc_installed; then
                log_error "GCC installation verification failed"
                exit 1
            fi

            gcc_version=$(get_gcc_version)
            log_info "GCC installed successfully: $gcc_version"
        fi
    fi

    # Configure environment
    configure_gcc_environment "$dry_run"

    # Configure CMake
    configure_cmake_gcc "$dry_run"

    # Configure Conan
    configure_conan_gcc "$dry_run" "${gcc_version:-unknown}"

    # Validate installation
    if [[ "$dry_run" == "false" ]]; then
        log_info "Validating GCC installation..."
        if ! validate_gcc_installation; then
            log_error "GCC installation validation failed"
            exit 1
        fi
    fi

    log_info "=========================================="
    log_info "GCC setup complete!"
    log_info "=========================================="
    log_info ""
    log_info "To use GCC in your current shell, source the environment file:"
    log_info "  source $PROJECT_ROOT/.gcc.env"
    log_info ""
    log_info "To use GCC with CMake, use the toolchain file:"
    log_info "  cmake -DCMAKE_TOOLCHAIN_FILE=$PROJECT_ROOT/cmake/toolchains/gcc-linux.cmake .."
    log_info ""
    log_info "To use GCC with Conan, use the profile:"
    log_info "  conan install . --profile gcc-linux"
    log_info ""
}

# Run main function
main "$@"
