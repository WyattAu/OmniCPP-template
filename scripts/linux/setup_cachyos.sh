#!/usr/bin/env bash
#
# Description: Setup script for CachyOS-specific compiler environment and optimizations
# Usage: ./scripts/linux/setup_cachyos.sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#   --version     Show script version
#
# References:
#   - ADR-035: Linux Setup Script Architecture
#   - REQ-005-003: Create setup_cachyos.sh
#   - ADR-028: CachyOS as Primary Linux Target
#   - TM-LX-002: Distribution-Specific Vulnerabilities
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

# CachyOS-specific compiler flags
readonly CACHYOS_CFLAGS="-march=native -O3 -flto -DNDEBUG"
readonly CACHYOS_CXXFLAGS="-march=native -O3 -flto -DNDEBUG"
readonly CACHYOS_LDFLAGS="-Wl,--as-needed -Wl,--no-undefined -flto"

# Colors for output (use tput for compatibility)
if command -v tput >/dev/null 2>&1 && tput colors >/dev/null 2>&1; then
    RED="$(tput setaf 1)"
    GREEN="$(tput setaf 2)"
    YELLOW="$(tput setaf 3)"
    BLUE="$(tput setaf 4)"
    CYAN="$(tput setaf 6)"
    NC="$(tput sgr0)"
else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    CYAN=""
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

log_cachyos() {
    echo -e "${CYAN}[CACHYOS]${NC} $1"
}

# Display usage information
show_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [options]

Setup CachyOS-specific compiler environment and optimizations.

This script configures the build environment for CachyOS, an Arch Linux derivative
optimized for performance. It applies CachyOS-specific compiler flags including
Link Time Optimization (LTO) and native architecture optimizations.

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
  FORCE_CACHYOS Force CachyOS setup even if not on CachyOS (default: false)

CachyOS Optimizations:
  -march=native  Generate code optimized for the host CPU
  -O3            Maximum optimization level
  -flto          Link Time Optimization for better performance
  --as-needed     Remove unused library dependencies
  --no-undefined  Fail on undefined symbols at link time

Examples:
  $SCRIPT_NAME                    # Run setup on CachyOS
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
        # Using grep to avoid sourcing potentially malicious content
        local distro_id
        distro_id=$(grep -E '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"')
        echo "$distro_id"
    else
        echo "unknown"
    fi
}

# Detect CachyOS specifically
detect_cachyos() {
    local distro
    distro=$(detect_distro)
    
    # Check for CachyOS ID or ID_LIKE
    if [[ "$distro" == "cachyos" ]]; then
        echo "true"
        return 0
    fi
    
    # Check for CachyOS in ID_LIKE
    if [[ -f /etc/os-release ]]; then
        local id_like
        id_like=$(grep -E '^ID_LIKE=' /etc/os-release | cut -d= -f2 | tr -d '"')
        if [[ "$id_like" == *"cachyos"* ]]; then
            echo "true"
            return 0
        fi
    fi
    
    # Check for CachyOS-specific files
    if [[ -f /etc/cachyos-release ]] || [[ -f /usr/lib/cachyos-release ]]; then
        echo "true"
        return 0
    fi
    
    echo "false"
    return 0
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

# Configure GCC environment variables with CachyOS optimizations
configure_gcc_environment() {
    local dry_run="$1"

    log_info "Configuring GCC environment variables..."

    # Set compiler environment variables
    export CC="${CC:-gcc}"
    export CXX="${CXX:-g++}"

    # Set CachyOS-specific compiler flags
    export CFLAGS="${CFLAGS:-$CACHYOS_CFLAGS}"
    export CXXFLAGS="${CXXFLAGS:-$CACHYOS_CXXFLAGS}"
    export LDFLAGS="${LDFLAGS:-$CACHYOS_LDFLAGS}"

    log_info "CC=$CC"
    log_info "CXX=$CXX"
    log_info "CFLAGS=$CFLAGS"
    log_info "CXXFLAGS=$CXXFLAGS"
    log_info "LDFLAGS=$LDFLAGS"

    # Create environment file for persistence
    local env_file="$PROJECT_ROOT/.cachyos.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create environment file: $env_file"
        echo "Content:"
        cat << EOF
# CachyOS environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export CC=$CC
export CXX=$CXX
export CFLAGS="$CFLAGS"
export CXXFLAGS="$CXXFLAGS"
export LDFLAGS="$LDFLAGS"
EOF
    else
        cat > "$env_file" << EOF
# CachyOS environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export CC=$CC
export CXX=$CXX
export CFLAGS="$CFLAGS"
export CXXFLAGS="$CXXFLAGS"
export LDFLAGS="$LDFLAGS"
EOF
        log_info "Created environment file: $env_file"
    fi
}

# Display CachyOS-specific optimizations
display_cachyos_optimizations() {
    log_cachyos "CachyOS-Specific Optimizations:"
    echo ""
    echo "  Compiler Flags:"
    echo "    CFLAGS:  $CACHYOS_CFLAGS"
    echo "    CXXFLAGS: $CACHYOS_CXXFLAGS"
    echo ""
    echo "  Linker Flags:"
    echo "    LDFLAGS:  $CACHYOS_LDFLAGS"
    echo ""
    echo "  Optimization Details:"
    echo "    -march=native    Optimize for host CPU architecture"
    echo "    -O3              Maximum optimization level"
    echo "    -flto            Link Time Optimization for better performance"
    echo "    -DNDEBUG          Disable debugging assertions"
    echo "    --as-needed       Remove unused library dependencies"
    echo "    --no-undefined   Fail on undefined symbols at link time"
    echo ""
}

# Configure CMake for CachyOS
configure_cmake_cachyos() {
    local dry_run="$1"
    local gcc_version="$2"

    log_info "Configuring CMake for CachyOS..."

    local cmake_toolchain_dir="$PROJECT_ROOT/cmake/toolchains"
    local cachyos_toolchain_file="$cmake_toolchain_dir/cachyos.cmake"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create CMake toolchain file: $cachyos_toolchain_file"
    else
        # Create toolchains directory if it doesn't exist
        mkdir -p "$cmake_toolchain_dir"

        # Write CachyOS toolchain file
        cat > "$cachyos_toolchain_file" << EOF
# CMake toolchain file for CachyOS
# Generated by setup_cachyos.sh
# CachyOS is an Arch Linux derivative optimized for performance

cmake_minimum_required(3.20)

# Set compilers
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

# CachyOS-specific compiler flags
# These flags are optimized for performance on CachyOS
set(CMAKE_C_FLAGS_INIT "-march=native")
set(CMAKE_CXX_FLAGS_INIT "-march=native")

# Enable position independent code
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# CachyOS-specific optimizations for Release builds
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Maximum optimization with LTO
    set(CMAKE_C_FLAGS "\${CMAKE_C_FLAGS} -O3 -flto -DNDEBUG")
    set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -O3 -flto -DNDEBUG")
    
    # Linker optimizations
    set(CMAKE_EXE_LINKER_FLAGS "\${CMAKE_EXE_LINKER_FLAGS} -Wl,--as-needed -Wl,--no-undefined -flto")
    set(CMAKE_SHARED_LINKER_FLAGS "\${CMAKE_SHARED_LINKER_FLAGS} -Wl,--as-needed -Wl,--no-undefined -flto")
    set(CMAKE_MODULE_LINKER_FLAGS "\${CMAKE_MODULE_LINKER_FLAGS} -Wl,--as-needed -Wl,--no-undefined -flto")
elseif(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # Debug builds with symbols
    set(CMAKE_C_FLAGS "\${CMAKE_C_FLAGS} -g -O0")
    set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -g -O0")
elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
    # Optimized with debug symbols
    set(CMAKE_C_FLAGS "\${CMAKE_C_FLAGS} -O2 -g -flto -DNDEBUG")
    set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -O2 -g -flto -DNDEBUG")
    set(CMAKE_EXE_LINKER_FLAGS "\${CMAKE_EXE_LINKER_FLAGS} -Wl,--as-needed -flto")
    set(CMAKE_SHARED_LINKER_FLAGS "\${CMAKE_SHARED_LINKER_FLAGS} -Wl,--as-needed -flto")
elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
    # Optimized for size
    set(CMAKE_C_FLAGS "\${CMAKE_C_FLAGS} -Os -flto -DNDEBUG")
    set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -Os -flto -DNDEBUG")
    set(CMAKE_EXE_LINKER_FLAGS "\${CMAKE_EXE_LINKER_FLAGS} -Wl,--as-needed -flto")
    set(CMAKE_SHARED_LINKER_FLAGS "\${CMAKE_SHARED_LINKER_FLAGS} -Wl,--as-needed -flto")
endif()

# Enable warnings
set(CMAKE_C_FLAGS "\${CMAKE_C_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

# CachyOS-specific C++ warnings
set(CMAKE_CXX_FLAGS "\${CMAKE_CXX_FLAGS} -Wnon-virtual-dtor")

# Interprocedural optimization (LTO) settings
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)

# Enable unity builds for faster compilation
set(CMAKE_UNITY_BUILD ON)

# CachyOS-specific: Use lto-wrapper for LTO
set(CMAKE_AR gcc-ar)
set(CMAKE_RANLIB gcc-ranlib)
set(CMAKE_NM gcc-nm)
EOF
        log_info "Created CMake toolchain file: $cachyos_toolchain_file"
    fi
}

# Configure Conan for CachyOS
configure_conan_cachyos() {
    local dry_run="$1"
    local gcc_version="$2"

    log_info "Configuring Conan for CachyOS..."

    local conan_profiles_dir="$PROJECT_ROOT/conan/profiles"
    local cachyos_profile="$conan_profiles_dir/cachyos"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Conan profile: $cachyos_profile"
    else
        # Create profiles directory if it doesn't exist
        mkdir -p "$conan_profiles_dir"

        # Write Conan profile for CachyOS
        cat > "$cachyos_profile" << EOF
# Conan profile for CachyOS
# Generated by setup_cachyos.sh
# CachyOS is an Arch Linux derivative optimized for performance

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=$gcc_version
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}
tools.cmake.cmaketoolchain:user_toolchain=["\${PROJECT_ROOT}/cmake/toolchains/cachyos.cmake"]
tools.build:skip_test=false

[buildenv]
CC=gcc
CXX=g++
CFLAGS="$CACHYOS_CFLAGS"
CXXFLAGS="$CACHYOS_CXXFLAGS"
LDFLAGS="$CACHYOS_LDFLAGS"

[tool_requires]
# Add CachyOS-specific tool requirements if needed
EOF
        log_info "Created Conan profile: $cachyos_profile"
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

    # Check CachyOS-specific flags
    if [[ -n "${CFLAGS:-}" ]]; then
        log_info "✓ CFLAGS environment variable set"
    else
        log_warn "✗ CFLAGS environment variable not set"
    fi

    if [[ -n "${CXXFLAGS:-}" ]]; then
        log_info "✓ CXXFLAGS environment variable set"
    else
        log_warn "✗ CXXFLAGS environment variable not set"
    fi

    # Test compilation
    if command -v gcc >/dev/null 2>&1; then
        local test_file="/tmp/cachyos_gcc_test_$$.c"
        local test_output="/tmp/cachyos_gcc_test_$$.out"

        echo '#include <stdio.h>' > "$test_file"
        echo 'int main() { printf("Hello from CachyOS GCC\\n"); return 0; }' >> "$test_file"

        if gcc "$test_file" -o "$test_output" 2>/dev/null; then
            log_info "✓ GCC can compile C programs"
            rm -f "$test_file" "$test_output"
        else
            log_error "✗ GCC compilation test failed"
            ((errors++))
            rm -f "$test_file" "$test_output"
        fi
    fi

    # Test C++ compilation with CachyOS flags
    if command -v g++ >/dev/null 2>&1; then
        local test_file="/tmp/cachyos_gxx_test_$$.cpp"
        local test_output="/tmp/cachyos_gxx_test_$$.out"

        echo '#include <iostream>' > "$test_file"
        echo 'int main() { std::cout << "Hello from CachyOS G++" << std::endl; return 0; }' >> "$test_file"

        if g++ "$test_file" -o "$test_output" 2>/dev/null; then
            log_info "✓ G++ can compile C++ programs"
            rm -f "$test_file" "$test_output"
        else
            log_error "✗ G++ compilation test failed"
            ((errors++))
            rm -f "$test_file" "$test_output"
        fi
    fi

    return "$errors"
}

# Validate CachyOS configuration
validate_cachyos_configuration() {
    log_info "Validating CachyOS configuration..."

    local errors=0

    # Check CMake toolchain file
    local cmake_toolchain_file="$PROJECT_ROOT/cmake/toolchains/cachyos.cmake"
    if [[ -f "$cmake_toolchain_file" ]]; then
        log_info "✓ CMake toolchain file exists: $cmake_toolchain_file"
    else
        log_warn "✗ CMake toolchain file not found: $cmake_toolchain_file"
    fi

    # Check Conan profile
    local conan_profile="$PROJECT_ROOT/conan/profiles/cachyos"
    if [[ -f "$conan_profile" ]]; then
        log_info "✓ Conan profile exists: $conan_profile"
    else
        log_warn "✗ Conan profile not found: $conan_profile"
    fi

    # Check environment file
    local env_file="$PROJECT_ROOT/.cachyos.env"
    if [[ -f "$env_file" ]]; then
        log_info "✓ Environment file exists: $env_file"
    else
        log_warn "✗ Environment file not found: $env_file"
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
    log_info "CachyOS Setup Script v$SCRIPT_VERSION"
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

    # Detect CachyOS
    local is_cachyos
    is_cachyos=$(detect_cachyos)

    if [[ "$is_cachyos" == "true" ]]; then
        log_cachyos "Running on CachyOS - applying CachyOS-specific optimizations"
    else
        log_warn "Not running on CachyOS (detected: $distro)"
        
        # Check if forced
        if [[ "${FORCE_CACHYOS:-false}" != "true" ]]; then
            log_warn "CachyOS-specific optimizations may not work correctly"
            log_warn "Set FORCE_CACHYOS=true to force CachyOS setup"
            log_warn "Exiting..."
            exit 0
        else
            log_warn "FORCE_CACHYOS is set - proceeding with CachyOS setup"
        fi
    fi

    # Display CachyOS optimizations
    display_cachyos_optimizations

    # Check if GCC is already installed
    if check_gcc_installed; then
        local gcc_version
        gcc_version=$(get_gcc_version)
        log_info "GCC is already installed: $gcc_version"

        # Validate version
        if ! validate_gcc_version "$gcc_version" "$MIN_GCC_MAJOR" "$MIN_GCC_MINOR"; then
            log_warn "GCC version is below minimum requirements"
            log_warn "Consider upgrading GCC"
        fi
    else
        log_info "GCC is not installed"
        log_info "Installing GCC..."

        # Install GCC
        if ! install_gcc "$distro" "$pkg_manager" "$dry_run"; then
            log_error "Failed to install GCC"
            exit 1
        fi

        # Verify installation
        if ! check_gcc_installed; then
            log_error "GCC installation verification failed"
            exit 1
        fi

        local gcc_version
        gcc_version=$(get_gcc_version)
        log_info "GCC installed successfully: $gcc_version"
    fi

    # Configure GCC environment with CachyOS optimizations
    configure_gcc_environment "$dry_run"

    # Configure CMake for CachyOS
    configure_cmake_cachyos "$dry_run" "$gcc_version"

    # Configure Conan for CachyOS
    configure_conan_cachyos "$dry_run" "$gcc_version"

    # Validate installation
    log_info "=========================================="
    log_info "Validation"
    log_info "=========================================="

    local validation_errors
    validation_errors=$(validate_gcc_installation)
    if [[ $validation_errors -gt 0 ]]; then
        log_error "GCC installation validation failed with $validation_errors error(s)"
        exit 1
    fi

    # Validate CachyOS configuration
    validate_cachyos_configuration

    # Summary
    log_info "=========================================="
    log_info "Setup Complete"
    log_info "=========================================="
    log_info "CachyOS-specific optimizations have been configured"
    log_info ""
    log_info "Next steps:"
    log_info "  1. Source the environment file: source .cachyos.env"
    log_info "  2. Build with CMake: cmake -DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/cachyos.cmake"
    log_info "  3. Or use Conan: conan install . --profile:cachyos"
    log_info ""
    log_info "For more information, see:"
    log_info "  - ADR-035: Linux Setup Script Architecture"
    log_info "  - REQ-005-003: Create setup_cachyos.sh"
    log_info "  - ADR-028: CachyOS as Primary Linux Target"

    if [[ "$dry_run" == "true" ]]; then
        log_info ""
        log_info "DRY-RUN complete - no changes were made"
    fi

    exit 0
}

# Run main function
main "$@"
