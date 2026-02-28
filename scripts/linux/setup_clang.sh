#!/usr/bin/env bash
#
# Description: Setup script for Clang compiler environment on Linux
# Usage: ./scripts/linux/setup_clang.sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#   --version     Show script version
#
# References:
#   - ADR-035: Linux Setup Script Architecture
#   - REQ-005-002: Create setup_clang.sh
#   - TM-LX-005: Linux Script Security Risks
#

set -euo pipefail

# Script metadata
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly MIN_CLANG_MAJOR=19
readonly MIN_CLANG_MINOR=0

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

Setup Clang compiler environment on Linux.

Options:
  --dry-run    Show what would be done without making changes
  --help        Show this help message
  --version     Show script version
  --debug       Enable debug output

Environment Variables:
  CC            Override C compiler (default: clang)
  CXX           Override C++ compiler (default: clang++)
  CLANG_VERSION Specific Clang version to install (optional)
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

# Check if Clang is installed
check_clang_installed() {
    command -v clang >/dev/null 2>&1
}

# Get Clang version
get_clang_version() {
    if command -v clang >/dev/null 2>&1; then
        clang --version | head -n1 | sed -n 's/.*version \([0-9.]*\).*/\1/p'
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

# Validate Clang version meets minimum requirements
validate_clang_version() {
    local version="$1"
    local min_major="$2"
    local min_minor="$3"

    log_info "Validating Clang version: $version (minimum required: $min_major.$min_minor.0)"

    local current_major current_minor
    read -r current_major current_minor <<< "$(parse_version "$version")"

    # Check major version
    if ((current_major < min_major)); then
        log_error "Clang version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    # Check minor version if major version matches
    if ((current_major == min_major)) && ((current_minor < min_minor)); then
        log_error "Clang version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    log_info "Clang version $version meets minimum requirements"
    return 0
}

# Install Clang using appropriate package manager
install_clang() {
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
            log_info "Installing Clang with pacman..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo pacman -S --needed --noconfirm clang"
            else
                sudo pacman -S --needed --noconfirm clang
            fi
            ;;
        apt)
            log_info "Installing Clang with apt..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo apt-get update"
                echo "Would run: sudo apt-get install -y clang clang++ lld"
            else
                sudo apt-get update
                sudo apt-get install -y clang clang++ lld
            fi
            ;;
        dnf|yum)
            log_info "Installing Clang with $pkg_manager..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo $pkg_manager install -y clang clang-tools-extra lld"
            else
                sudo "$pkg_manager" install -y clang clang-tools-extra lld
            fi
            ;;
        zypper)
            log_info "Installing Clang with zypper..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo zypper install -y clang clang-tools lld"
            else
                sudo zypper install -y clang clang-tools lld
            fi
            ;;
        *)
            log_error "Unsupported package manager: $pkg_manager"
            log_error "Please install Clang manually and run this script again"
            return 1
            ;;
    esac
}

# Configure Clang environment variables
configure_clang_environment() {
    local dry_run="$1"

    log_info "Configuring Clang environment variables..."

    # Set compiler environment variables
    export CC="${CC:-clang}"
    export CXX="${CXX:-clang++}"

    log_info "CC=$CC"
    log_info "CXX=$CXX"

    # Create environment file for persistence
    local env_file="$PROJECT_ROOT/.clang.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create environment file: $env_file"
        echo "Content:"
        cat << EOF
export CC=$CC
export CXX=$CXX
EOF
    else
        cat > "$env_file" << EOF
# Clang environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export CC=$CC
export CXX=$CXX
EOF
        log_info "Created environment file: $env_file"
    fi
}

# Configure CMake for Clang
configure_cmake_clang() {
    local dry_run="$1"

    log_info "Configuring CMake for Clang..."

    local cmake_toolchain_dir="$PROJECT_ROOT/cmake/toolchains"
    local clang_toolchain_file="$cmake_toolchain_dir/clang-linux.cmake"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create CMake toolchain file: $clang_toolchain_file"
    else
        # Create toolchains directory if it doesn't exist
        mkdir -p "$cmake_toolchain_dir"

        # Write Clang toolchain file
        cat > "$clang_toolchain_file" << 'EOF'
# CMake toolchain file for Clang on Linux
# Generated by setup_clang.sh

cmake_minimum_required(3.20)

# Set compilers
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

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

# Clang-specific warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wnon-virtual-dtor -Wold-style-cast")

# Use LLD linker if available
find_program(LLD_LINKER lld)
if(LLD_LINKER)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fuse-ld=lld")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fuse-ld=lld")
endif()
EOF
        log_info "Created CMake toolchain file: $clang_toolchain_file"
    fi
}

# Configure Conan for Clang
configure_conan_clang() {
    local dry_run="$1"
    local clang_version="$2"

    log_info "Configuring Conan for Clang..."

    local conan_profiles_dir="$PROJECT_ROOT/conan/profiles"
    local clang_profile="$conan_profiles_dir/clang-linux"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Conan profile: $clang_profile"
    else
        # Create profiles directory if it doesn't exist
        mkdir -p "$conan_profiles_dir"

        # Write Conan profile for Clang
        cat > "$clang_profile" << EOF
# Conan profile for Clang on Linux
# Generated by setup_clang.sh

[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=$clang_version
compiler.libcxx=libc++
build_type=Release

[conf]
tools.build:compiler_executables={"c": "clang", "cpp": "clang++"}
tools.cmake.cmaketoolchain:user_toolchain=["\${PROJECT_ROOT}/cmake/toolchains/clang-linux.cmake"]

[buildenv]
CC=clang
CXX=clang++
EOF
        log_info "Created Conan profile: $clang_profile"
    fi
}

# Validate Clang installation
validate_clang_installation() {
    log_info "Validating Clang installation..."

    local errors=0

    # Check clang command
    if command -v clang >/dev/null 2>&1; then
        local clang_version
        clang_version=$(get_clang_version)
        log_info "✓ Clang found: $clang_version"
    else
        log_error "✗ Clang not found"
        ((errors++))
    fi

    # Check clang++ command
    if command -v clang++ >/dev/null 2>&1; then
        local clangxx_version
        clangxx_version=$(clang++ --version | head -n1 | sed -n 's/.*version \([0-9.]*\).*/\1/p')
        log_info "✓ Clang++ found: $clangxx_version"
    else
        log_error "✗ Clang++ not found"
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
    if command -v clang >/dev/null 2>&1; then
        local test_file="/tmp/clang_test_$$.c"
        local test_output="/tmp/clang_test_$$.out"

        echo '#include <stdio.h>' > "$test_file"
        echo 'int main() { printf("Hello from Clang\\n"); return 0; }' >> "$test_file"

        if clang "$test_file" -o "$test_output" 2>/dev/null; then
            log_info "✓ Clang can compile C programs"
            rm -f "$test_file" "$test_output"
        else
            log_error "✗ Clang compilation test failed"
            ((errors++))
            rm -f "$test_file" "$test_output"
        fi
    fi

    # Test C++ compilation
    if command -v clang++ >/dev/null 2>&1; then
        local test_file="/tmp/clangxx_test_$$.cpp"
        local test_output="/tmp/clangxx_test_$$.out"

        echo '#include <iostream>' > "$test_file"
        echo 'int main() { std::cout << "Hello from Clang++" << std::endl; return 0; }' >> "$test_file"

        if clang++ "$test_file" -o "$test_output" 2>/dev/null; then
            log_info "✓ Clang++ can compile C++ programs"
            rm -f "$test_file" "$test_output"
        else
            log_error "✗ Clang++ compilation test failed"
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
    log_info "Clang Setup Script v$SCRIPT_VERSION"
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

    # Check if Clang is already installed
    if check_clang_installed; then
        local clang_version
        clang_version=$(get_clang_version)
        log_info "Clang is already installed: $clang_version"

        # Validate version
        if ! validate_clang_version "$clang_version" "$MIN_CLANG_MAJOR" "$MIN_CLANG_MINOR"; then
            log_warn "Clang version is below minimum requirements"
            log_warn "Consider upgrading Clang to version $MIN_CLANG_MAJOR.$MIN_CLANG_MINOR or later"
        fi
    else
        log_info "Clang is not installed"
        log_info "Installing Clang..."

        # Install Clang
        if ! install_clang "$distro" "$pkg_manager" "$dry_run" "${CLANG_VERSION:-}"; then
            log_error "Failed to install Clang"
            exit 1
        fi

        # Verify installation
        if [[ "$dry_run" != "true" ]]; then
            if ! check_clang_installed; then
                log_error "Clang installation verification failed"
                exit 1
            fi
            log_info "Clang installation successful"
        fi
    fi

    # Get Clang version for configuration
    local clang_version
    clang_version=$(get_clang_version)
    log_info "Using Clang version: $clang_version"

    # Configure Clang environment
    configure_clang_environment "$dry_run"

    # Configure CMake for Clang
    configure_cmake_clang "$dry_run"

    # Configure Conan for Clang
    configure_conan_clang "$dry_run" "$clang_version"

    # Validate Clang installation
    if [[ "$dry_run" != "true" ]]; then
        log_info "=========================================="
        log_info "Validating Clang installation..."
        log_info "=========================================="

        if ! validate_clang_installation; then
            log_error "Clang installation validation failed"
            exit 1
        fi

        log_info "=========================================="
        log_info "Clang setup complete!"
        log_info "=========================================="
        log_info ""
        log_info "Environment variables have been configured:"
        log_info "  CC=$CC"
        log_info "  CXX=$CXX"
        log_info ""
        log_info "To use Clang for your next build, run:"
        log_info "  source $PROJECT_ROOT/.clang.env"
        log_info ""
        log_info "Or add the following to your shell profile (~/.bashrc or ~/.zshrc):"
        log_info "  source $PROJECT_ROOT/.clang.env"
        log_info ""
        log_info "CMake toolchain file created at:"
        log_info "  $PROJECT_ROOT/cmake/toolchains/clang-linux.cmake"
        log_info ""
        log_info "Conan profile created at:"
        log_info "  $PROJECT_ROOT/conan/profiles/clang-linux"
    else
        log_info "=========================================="
        log_info "Dry-run complete. No changes were made."
        log_info "=========================================="
    fi

    return 0
}

# Run main function
main "$@"
