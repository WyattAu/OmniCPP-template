#!/usr/bin/env bash
#
# Description: Setup script for Qt6 and Vulkan dependencies on Linux
# Usage: ./scripts/linux/setup_qt6_vulkan.sh [options]
#
# Options:
#   --dry-run    Show what would be done without making changes
#   --help        Show this help message
#   --version     Show script version
#
# References:
#   - ADR-035: Linux Setup Script Architecture
#   - REQ-005-005: Create setup_qt6_vulkan.sh
#   - TM-LX-005: Linux Script Security Risks
#

set -euo pipefail

# Script metadata
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly MIN_QT_MAJOR=6
readonly MIN_QT_MINOR=0
readonly MIN_VULKAN_MAJOR=1
readonly MIN_VULKAN_MINOR=3

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

Setup Qt6 and Vulkan dependencies on Linux.

Options:
  --dry-run    Show what would be done without making changes
  --help        Show this help message
  --version     Show script version
  --debug       Enable debug output

Environment Variables:
  QT_QPA_PLATFORM      Qt platform plugin (default: wayland)
  SKIP_INSTALL         Skip package installation (default: false)
  SKIP_QT6            Skip Qt6 setup (default: false)
  SKIP_VULKAN         Skip Vulkan setup (default: false)

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
        # Use grep to avoid sourcing potentially malicious content (TM-LX-005)
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

# Check if Qt6 is installed
check_qt6_installed() {
    command -v qmake6 >/dev/null 2>&1 || command -v qmake >/dev/null 2>&1
}

# Get Qt6 version
get_qt6_version() {
    local qmake_cmd=""
    if command -v qmake6 >/dev/null 2>&1; then
        qmake_cmd="qmake6"
    elif command -v qmake >/dev/null 2>&1; then
        qmake_cmd="qmake"
    fi

    if [[ -n "$qmake_cmd" ]]; then
        # Extract version from qmake output
        "$qmake_cmd" -v 2>&1 | grep -oP 'Qt version \K[0-9.]+' || echo "unknown"
    else
        echo "not found"
    fi
}

# Check if Vulkan is installed
check_vulkan_installed() {
    command -v vulkaninfo >/dev/null 2>&1
}

# Get Vulkan version
get_vulkan_version() {
    if command -v vulkaninfo >/dev/null 2>&1; then
        # Extract version from vulkaninfo output
        vulkaninfo --summary 2>/dev/null | grep -oP 'Vulkan Instance Version: \K[0-9.]+' || echo "unknown"
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

# Validate Qt6 version meets minimum requirements
validate_qt6_version() {
    local version="$1"
    local min_major="$2"
    local min_minor="$3"

    log_info "Validating Qt6 version: $version (minimum required: $min_major.$min_minor.0)"

    # Handle "unknown" or "not found" versions
    if [[ "$version" == "unknown" || "$version" == "not found" ]]; then
        log_warn "Unable to determine Qt6 version"
        return 0
    fi

    local current_major current_minor
    read -r current_major current_minor <<< "$(parse_version "$version")"

    # Check major version
    if ((current_major < min_major)); then
        log_error "Qt6 version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    # Check minor version if major version matches
    if ((current_major == min_major)) && ((current_minor < min_minor)); then
        log_error "Qt6 version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    log_info "Qt6 version $version meets minimum requirements"
    return 0
}

# Validate Vulkan version meets minimum requirements
validate_vulkan_version() {
    local version="$1"
    local min_major="$2"
    local min_minor="$3"

    log_info "Validating Vulkan version: $version (minimum required: $min_major.$min_minor.0)"

    # Handle "unknown" or "not found" versions
    if [[ "$version" == "unknown" || "$version" == "not found" ]]; then
        log_warn "Unable to determine Vulkan version"
        return 0
    fi

    local current_major current_minor
    read -r current_major current_minor <<< "$(parse_version "$version")"

    # Check major version
    if ((current_major < min_major)); then
        log_error "Vulkan version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    # Check minor version if major version matches
    if ((current_major == min_major)) && ((current_minor < min_minor)); then
        log_error "Vulkan version $version is older than minimum required $min_major.$min_minor.0"
        return 1
    fi

    log_info "Vulkan version $version meets minimum requirements"
    return 0
}

# Install Qt6 using appropriate package manager
install_qt6() {
    local distro="$1"
    local pkg_manager="$2"
    local dry_run="$3"

    log_info "Package manager: $pkg_manager"
    log_info "Distribution: $distro"

    # Check if installation should be skipped
    if [[ "${SKIP_INSTALL:-false}" == "true" ]]; then
        log_warn "SKIP_INSTALL is set, skipping package installation"
        return 0
    fi

    if [[ "${SKIP_QT6:-false}" == "true" ]]; then
        log_warn "SKIP_QT6 is set, skipping Qt6 installation"
        return 0
    fi

    case "$pkg_manager" in
        pacman)
            log_info "Installing Qt6 with pacman..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo pacman -S --needed --noconfirm qt6-base qt6-declarative qt6-tools qt6-wayland qt6-svg qt6-imageformats"
            else
                sudo pacman -S --needed --noconfirm qt6-base qt6-declarative qt6-tools qt6-wayland qt6-svg qt6-imageformats
            fi
            ;;
        apt)
            log_info "Installing Qt6 with apt..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo apt-get update"
                echo "Would run: sudo apt-get install -y qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-wayland-dev qt6-svg-dev libqt6imageformats6"
            else
                sudo apt-get update
                sudo apt-get install -y qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-wayland-dev qt6-svg-dev libqt6imageformats6
            fi
            ;;
        dnf|yum)
            log_info "Installing Qt6 with $pkg_manager..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo $pkg_manager install -y qt6-qtbase-devel qt6-qtdeclarative-devel qt6-qttools-devel qt6-qtwayland qt6-qtsvg-devel"
            else
                sudo "$pkg_manager" install -y qt6-qtbase-devel qt6-qtdeclarative-devel qt6-qttools-devel qt6-qtwayland qt6-qtsvg-devel
            fi
            ;;
        zypper)
            log_info "Installing Qt6 with zypper..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo zypper install -y qt6-base-devel qt6-declarative-devel qt6-tools-devel qt6-wayland qt6-svg-devel"
            else
                sudo zypper install -y qt6-base-devel qt6-declarative-devel qt6-tools-devel qt6-wayland qt6-svg-devel
            fi
            ;;
        *)
            log_error "Unsupported package manager: $pkg_manager"
            log_error "Please install Qt6 manually and run this script again"
            return 1
            ;;
    esac
}

# Install Vulkan using appropriate package manager
install_vulkan() {
    local distro="$1"
    local pkg_manager="$2"
    local dry_run="$3"

    log_info "Package manager: $pkg_manager"
    log_info "Distribution: $distro"

    # Check if installation should be skipped
    if [[ "${SKIP_INSTALL:-false}" == "true" ]]; then
        log_warn "SKIP_INSTALL is set, skipping package installation"
        return 0
    fi

    if [[ "${SKIP_VULKAN:-false}" == "true" ]]; then
        log_warn "SKIP_VULKAN is set, skipping Vulkan installation"
        return 0
    fi

    case "$pkg_manager" in
        pacman)
            log_info "Installing Vulkan with pacman..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo pacman -S --needed --noconfirm vulkan-headers vulkan-loader vulkan-tools vulkan-validation-layers vulkan-extension-layer glslang shaderc spirv-tools mesa"
            else
                sudo pacman -S --needed --noconfirm vulkan-headers vulkan-loader vulkan-tools vulkan-validation-layers vulkan-extension-layer glslang shaderc spirv-tools mesa
            fi
            ;;
        apt)
            log_info "Installing Vulkan with apt..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo apt-get update"
                echo "Would run: sudo apt-get install -y vulkan-headers libvulkan-dev vulkan-tools vulkan-validationlayers glslang-tools shaderc spirv-tools mesa-vulkan-drivers"
            else
                sudo apt-get update
                sudo apt-get install -y vulkan-headers libvulkan-dev vulkan-tools vulkan-validationlayers glslang-tools shaderc spirv-tools mesa-vulkan-drivers
            fi
            ;;
        dnf|yum)
            log_info "Installing Vulkan with $pkg_manager..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo $pkg_manager install -y vulkan-headers vulkan-loader vulkan-tools vulkan-validation-layers glslang shaderc spirv-tools mesa-vulkan-drivers"
            else
                sudo "$pkg_manager" install -y vulkan-headers vulkan-loader vulkan-tools vulkan-validation-layers glslang shaderc spirv-tools mesa-vulkan-drivers
            fi
            ;;
        zypper)
            log_info "Installing Vulkan with zypper..."
            if [[ "$dry_run" == "true" ]]; then
                echo "Would run: sudo zypper install -y vulkan-headers libvulkan1 vulkan-tools vulkan-validationlayers glslang-devel shaderc spirv-tools mesa-vulkan-drivers"
            else
                sudo zypper install -y vulkan-headers libvulkan1 vulkan-tools vulkan-validationlayers glslang-devel shaderc spirv-tools mesa-vulkan-drivers
            fi
            ;;
        *)
            log_error "Unsupported package manager: $pkg_manager"
            log_error "Please install Vulkan manually and run this script again"
            return 1
            ;;
    esac
}

# Configure Qt6 environment variables
configure_qt6_environment() {
    local dry_run="$1"

    log_info "Configuring Qt6 environment variables..."

    # Set Qt6 platform plugin
    export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-wayland}"

    log_info "QT_QPA_PLATFORM=$QT_QPA_PLATFORM"

    # Find Qt6 installation paths
    local qt6_base_path=""
    local qmake_cmd=""

    if command -v qmake6 >/dev/null 2>&1; then
        qmake_cmd="qmake6"
    elif command -v qmake >/dev/null 2>&1; then
        qmake_cmd="qmake"
    fi

    if [[ -n "$qmake_cmd" ]]; then
        qt6_base_path=$("$qmake_cmd" -query QT_INSTALL_PREFIX 2>/dev/null || echo "")
        log_debug "Qt6 base path: $qt6_base_path"
    fi

    # Create environment file for persistence
    local env_file="$PROJECT_ROOT/.qt6_vulkan.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would create environment file: $env_file"
        echo "Content:"
        cat << EOF
# Qt6 and Vulkan environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export QT_QPA_PLATFORM=$QT_QPA_PLATFORM
EOF
        if [[ -n "$qt6_base_path" ]]; then
            echo "export QT_PLUGIN_PATH=\$QT_PLUGIN_PATH:$qt6_base_path/lib/qt-6/plugins"
            echo "export CMAKE_PREFIX_PATH=\$CMAKE_PREFIX_PATH:$qt6_base_path"
        fi
    else
        cat > "$env_file" << EOF
# Qt6 and Vulkan environment configuration
# Generated by $SCRIPT_NAME on $(date -u +"%Y-%m-%d %H:%M:%S UTC")
export QT_QPA_PLATFORM=$QT_QPA_PLATFORM
EOF
        if [[ -n "$qt6_base_path" ]]; then
            echo "export QT_PLUGIN_PATH=\$QT_PLUGIN_PATH:$qt6_base_path/lib/qt-6/plugins" >> "$env_file"
            echo "export CMAKE_PREFIX_PATH=\$CMAKE_PREFIX_PATH:$qt6_base_path" >> "$env_file"
        fi
        log_info "Created environment file: $env_file"
    fi
}

# Configure Vulkan environment variables
configure_vulkan_environment() {
    local dry_run="$1"
    local distro="$2"

    log_info "Configuring Vulkan environment variables..."

    # Detect Vulkan paths based on distribution
    local vk_layer_path=""
    local vk_icd_filenames=""

    case "$distro" in
        arch|cachyos|manjaro)
            # Arch Linux paths
            vk_layer_path="/usr/share/vulkan/explicit_layer.d"
            vk_icd_filenames="/usr/share/vulkan/icd.d/intel_icd.x86_64.json:/usr/share/vulkan/icd.d/radeon_icd.x86_64.json:/usr/share/vulkan/icd.d/nvidia_icd.json"
            ;;
        ubuntu|debian|linuxmint|pop)
            # Debian/Ubuntu paths
            vk_layer_path="/usr/share/vulkan/explicit_layer.d"
            vk_icd_filenames="/usr/share/vulkan/icd.d/intel_icd.x86_64.json:/usr/share/vulkan/icd.d/radeon_icd.x86_64.json:/usr/share/vulkan/icd.d/nvidia_icd.json"
            ;;
        fedora|rhel|centos)
            # Fedora/RHEL paths
            vk_layer_path="/usr/share/vulkan/explicit_layer.d"
            vk_icd_filenames="/usr/share/vulkan/icd.d/intel_icd.x86_64.json:/usr/share/vulkan/icd.d/radeon_icd.x86_64.json:/usr/share/vulkan/icd.d/nvidia_icd.json"
            ;;
        opensuse*)
            # openSUSE paths
            vk_layer_path="/usr/share/vulkan/explicit_layer.d"
            vk_icd_filenames="/usr/share/vulkan/icd.d/intel_icd.x86_64.json:/usr/share/vulkan/icd.d/radeon_icd.x86_64.json:/usr/share/vulkan/icd.d/nvidia_icd.json"
            ;;
        *)
            # Default paths (may need adjustment)
            vk_layer_path="/usr/share/vulkan/explicit_layer.d"
            vk_icd_filenames="/usr/share/vulkan/icd.d/*.json"
            log_warn "Using default Vulkan paths for unknown distribution: $distro"
            ;;
    esac

    # Verify paths exist
    if [[ ! -d "$vk_layer_path" ]]; then
        log_warn "Vulkan layer path not found: $vk_layer_path"
        vk_layer_path=""
    fi

    # Set environment variables
    if [[ -n "$vk_layer_path" ]]; then
        export VK_LAYER_PATH="$vk_layer_path"
        log_info "VK_LAYER_PATH=$VK_LAYER_PATH"
    fi

    if [[ -n "$vk_icd_filenames" ]]; then
        export VK_ICD_FILENAMES="$vk_icd_filenames"
        log_info "VK_ICD_FILENAMES=$VK_ICD_FILENAMES"
    fi

    # Append to environment file
    local env_file="$PROJECT_ROOT/.qt6_vulkan.env"
    if [[ "$dry_run" == "true" ]]; then
        echo "Would append to environment file: $env_file"
        echo "Content:"
        if [[ -n "$vk_layer_path" ]]; then
            echo "export VK_LAYER_PATH=$vk_layer_path"
        fi
        if [[ -n "$vk_icd_filenames" ]]; then
            echo "export VK_ICD_FILENAMES=$vk_icd_filenames"
        fi
    else
        if [[ -n "$vk_layer_path" ]]; then
            echo "export VK_LAYER_PATH=$vk_layer_path" >> "$env_file"
        fi
        if [[ -n "$vk_icd_filenames" ]]; then
            echo "export VK_ICD_FILENAMES=$vk_icd_filenames" >> "$env_file"
        fi
        log_info "Updated environment file: $env_file"
    fi
}

# Configure CMake for Qt6 and Vulkan
configure_cmake_qt6_vulkan() {
    local dry_run="$1"

    log_info "Configuring CMake for Qt6 and Vulkan..."

    local cmake_toolchain_dir="$PROJECT_ROOT/cmake/toolchains"
    local qt6_vulkan_toolchain_file="$cmake_toolchain_dir/qt6_vulkan-linux.cmake"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create CMake toolchain file: $qt6_vulkan_toolchain_file"
    else
        # Create toolchains directory if it doesn't exist
        mkdir -p "$cmake_toolchain_dir"

        # Write Qt6/Vulkan toolchain file
        cat > "$qt6_vulkan_toolchain_file" << 'EOF'
# CMake toolchain file for Qt6 and Vulkan on Linux
# Generated by setup_qt6_vulkan.sh

cmake_minimum_required(3.20)

# Find Qt6 package
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt6 components
find_package(Qt6 COMPONENTS Core Gui Widgets Quick QUIET)

# Find Vulkan
find_package(Vulkan QUIET)

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

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

# Qt6-specific settings
if(Qt6_FOUND)
    message(STATUS "Qt6 found: ${Qt6_VERSION}")
    message(STATUS "Qt6 installation prefix: ${Qt6_DIR}")
else()
    message(WARNING "Qt6 not found")
endif()

# Vulkan-specific settings
if(Vulkan_FOUND)
    message(STATUS "Vulkan found: ${Vulkan_VERSION}")
else()
    message(WARNING "Vulkan not found")
endif()
EOF
        log_info "Created CMake toolchain file: $qt6_vulkan_toolchain_file"
    fi
}

# Configure Conan for Qt6 and Vulkan
configure_conan_qt6_vulkan() {
    local dry_run="$1"

    log_info "Configuring Conan for Qt6 and Vulkan..."

    local conan_profiles_dir="$PROJECT_ROOT/conan/profiles"
    local qt6_vulkan_profile="$conan_profiles_dir/qt6_vulkan-linux"

    if [[ "$dry_run" == "true" ]]; then
        echo "Would create Conan profile: $qt6_vulkan_profile"
    else
        # Create profiles directory if it doesn't exist
        mkdir -p "$conan_profiles_dir"

        # Write Conan profile for Qt6/Vulkan
        cat > "$qt6_vulkan_profile" << 'EOF'
# Conan profile for Qt6 and Vulkan on Linux
# Generated by setup_qt6_vulkan.sh

[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[conf]
tools.build:compiler_executables={"c": "gcc", "cpp": "g++"}

[buildenv]
QT_QPA_PLATFORM=wayland

[options]
qt*:shared=True
vulkan*:shared=True
EOF
        log_info "Created Conan profile: $qt6_vulkan_profile"
    fi
}

# Validate Qt6 installation
validate_qt6_installation() {
    log_info "Validating Qt6 installation..."

    local errors=0

    # Check qmake command
    if command -v qmake6 >/dev/null 2>&1; then
        local qt6_version
        qt6_version=$(get_qt6_version)
        log_info "✓ Qt6 qmake6 found: $qt6_version"
    elif command -v qmake >/dev/null 2>&1; then
        local qt6_version
        qt6_version=$(get_qt6_version)
        log_info "✓ Qt6 qmake found: $qt6_version"
    else
        log_error "✗ Qt6 qmake not found"
        ((errors++))
    fi

    # Check Qt6 libraries
    local qt6_lib_paths=(
        "/usr/lib/qt6"
        "/usr/lib/x86_64-linux-gnu/qt6"
        "/usr/lib64/qt6"
    )

    for lib_path in "${qt6_lib_paths[@]}"; do
        if [[ -d "$lib_path" ]]; then
            log_info "✓ Qt6 libraries found at: $lib_path"
            break
        fi
    done

    # Check QT_QPA_PLATFORM environment variable
    if [[ -n "${QT_QPA_PLATFORM:-}" ]]; then
        log_info "✓ QT_QPA_PLATFORM environment variable: $QT_QPA_PLATFORM"
    else
        log_warn "✗ QT_QPA_PLATFORM environment variable not set"
    fi

    return "$errors"
}

# Validate Vulkan installation
validate_vulkan_installation() {
    log_info "Validating Vulkan installation..."

    local errors=0

    # Check vulkaninfo command
    if command -v vulkaninfo >/dev/null 2>&1; then
        local vulkan_version
        vulkan_version=$(get_vulkan_version)
        log_info "✓ Vulkan found: $vulkan_version"
    else
        log_error "✗ Vulkan not found"
        ((errors++))
    fi

    # Check Vulkan headers
    local vulkan_header_paths=(
        "/usr/include/vulkan"
        "/usr/local/include/vulkan"
    )

    for header_path in "${vulkan_header_paths[@]}"; do
        if [[ -f "$header_path/vulkan.h" ]]; then
            log_info "✓ Vulkan headers found at: $header_path"
            break
        fi
    done

    # Check VK_LAYER_PATH environment variable
    if [[ -n "${VK_LAYER_PATH:-}" ]]; then
        log_info "✓ VK_LAYER_PATH environment variable: $VK_LAYER_PATH"
    else
        log_warn "✗ VK_LAYER_PATH environment variable not set"
    fi

    # Check VK_ICD_FILENAMES environment variable
    if [[ -n "${VK_ICD_FILENAMES:-}" ]]; then
        log_info "✓ VK_ICD_FILENAMES environment variable set"
    else
        log_warn "✗ VK_ICD_FILENAMES environment variable not set"
    fi

    # Test Vulkan if available
    if command -v vulkaninfo >/dev/null 2>&1; then
        if vulkaninfo --summary >/dev/null 2>&1; then
            log_info "✓ Vulkan can query system information"
        else
            log_warn "✗ Vulkan query test failed (may be normal without GPU)"
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
    log_info "Qt6/Vulkan Setup Script v$SCRIPT_VERSION"
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

    # Setup Qt6
    log_info "=========================================="
    log_info "Qt6 Setup"
    log_info "=========================================="

    if check_qt6_installed; then
        local qt6_version
        qt6_version=$(get_qt6_version)
        log_info "Qt6 is already installed: $qt6_version"

        # Validate version
        if ! validate_qt6_version "$qt6_version" "$MIN_QT_MAJOR" "$MIN_QT_MINOR"; then
            log_warn "Qt6 version is below minimum requirements"
        fi
    else
        log_info "Qt6 is not installed"
        install_qt6 "$distro" "$pkg_manager" "$dry_run"

        # Verify installation
        if [[ "$dry_run" == "false" ]] && check_qt6_installed; then
            local qt6_version
            qt6_version=$(get_qt6_version)
            log_info "Qt6 installed successfully: $qt6_version"
        elif [[ "$dry_run" == "false" ]]; then
            log_error "Qt6 installation failed"
            exit 1
        fi
    fi

    # Setup Vulkan
    log_info "=========================================="
    log_info "Vulkan Setup"
    log_info "=========================================="

    if check_vulkan_installed; then
        local vulkan_version
        vulkan_version=$(get_vulkan_version)
        log_info "Vulkan is already installed: $vulkan_version"

        # Validate version
        if ! validate_vulkan_version "$vulkan_version" "$MIN_VULKAN_MAJOR" "$MIN_VULKAN_MINOR"; then
            log_warn "Vulkan version is below minimum requirements"
        fi
    else
        log_info "Vulkan is not installed"
        install_vulkan "$distro" "$pkg_manager" "$dry_run"

        # Verify installation
        if [[ "$dry_run" == "false" ]] && check_vulkan_installed; then
            local vulkan_version
            vulkan_version=$(get_vulkan_version)
            log_info "Vulkan installed successfully: $vulkan_version"
        elif [[ "$dry_run" == "false" ]]; then
            log_error "Vulkan installation failed"
            exit 1
        fi
    fi

    # Configure environment
    log_info "=========================================="
    log_info "Environment Configuration"
    log_info "=========================================="

    configure_qt6_environment "$dry_run"
    configure_vulkan_environment "$dry_run" "$distro"
    configure_cmake_qt6_vulkan "$dry_run"
    configure_conan_qt6_vulkan "$dry_run"

    # Validate installation
    log_info "=========================================="
    log_info "Validation"
    log_info "=========================================="

    local total_errors=0

    validate_qt6_installation || ((total_errors+=$?))
    validate_vulkan_installation || ((total_errors+=$?))

    log_info "=========================================="
    log_info "Setup Complete"
    log_info "=========================================="

    if [[ "$total_errors" -eq 0 ]]; then
        log_info "Qt6 and Vulkan setup completed successfully!"
        log_info ""
        log_info "To use the Qt6 and Vulkan environment, source the environment file:"
        log_info "  source $PROJECT_ROOT/.qt6_vulkan.env"
        log_info ""
        log_info "Or add the following to your shell profile (~/.bashrc or ~/.zshrc):"
        log_info "  source $PROJECT_ROOT/.qt6_vulkan.env"
        log_info ""
        log_info "To build with CMake using the Qt6/Vulkan toolchain:"
        log_info "  cmake -DCMAKE_TOOLCHAIN_FILE=$PROJECT_ROOT/cmake/toolchains/qt6_vulkan-linux.cmake .."
    else
        log_error "Setup completed with $total_errors error(s)"
        exit 1
    fi
}

# Run main function
main "$@"
