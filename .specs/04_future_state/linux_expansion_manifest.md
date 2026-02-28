# OmniCPP Template - Linux Expansion Manifest

**Generated:** 2026-01-27
**Purpose:** Define comprehensive Linux support expansion for OmniCPP Template
**Scope:** Enhanced Linux/CachyOS support with Nix integration
**Target Platform:** CachyOS PC (Arch Linux derivative)

---

## Executive Summary

This document defines the enhanced Linux support for the OmniCPP Template, expanding from partial Linux support to comprehensive first-class Linux development environment. The expansion focuses on CachyOS as the primary target platform while maintaining compatibility with other Linux distributions.

**Key Enhancements:**

- **Enhanced OmniCppController.py** with Linux-specific detection and Nix integration
- **Comprehensive flake.nix** for reproducible CachyOS development environment
- **Complete Conan profiles** for GCC, Clang, and CachyOS
- **Linux-specific setup scripts** for compiler environment configuration
- **Enhanced VSCode configurations** with Linux task variants
- **Comprehensive documentation** for Linux builds and Nix workflow
- **Repository cleanup** to remove Windows-centric artifacts
- **Enhanced CMake integration** with Nix-aware presets

---

## 1. Enhanced OmniCppController.py Structure

### 1.1 New Functions/Methods for Linux Support

**Platform Detection Enhancements:**

```python
# omni_scripts/platform/linux.py - New methods
def detect_linux_distribution() -> LinuxDistribution:
    """Detect Linux distribution and version.
    
    Returns:
        LinuxDistribution: Distribution info with name, version, family
    """

def detect_package_manager() -> PackageManager:
    """Detect system package manager (pacman, apt, dnf, etc.).
    
    Returns:
        PackageManager: Package manager type and command
    """

def is_nix_environment() -> bool:
    """Check if running in Nix shell.
    
    Returns:
        bool: True if Nix environment detected
    """

def is_cachyos() -> bool:
    """Check if running on CachyOS.
    
    Returns:
        bool: True if CachyOS detected
    """

# omni_scripts/compilers/detector.py - Enhanced methods
def detect_linux_gcc() -> Optional[GCCCompiler]:
    """Detect GCC compiler on Linux with Nix awareness.
    
    Returns:
        Optional[GCCCompiler]: GCC compiler info or None
    """

def detect_linux_clang() -> Optional[ClangCompiler]:
    """Detect Clang compiler on Linux with Nix awareness.
    
    Returns:
        Optional[ClangCompiler]: Clang compiler info or None
    """

def get_linux_compiler_path(compiler: str) -> Path:
    """Get full path to compiler on Linux.
    
    Args:
        compiler: Compiler name (gcc, clang)
    
    Returns:
        Path: Full path to compiler executable
    """

# omni_scripts/utils/nix_utils.py - New module
def setup_nix_environment() -> None:
    """Setup environment variables for Nix shell.
    
    Configures:
    - NIX_PATH
    - NIX_PROFILES
    - Compiler paths from Nix store
    """

def get_nix_packages() -> list[str]:
    """Get list of packages available in Nix environment.
    
    Returns:
        list[str]: Available package names
    """

def validate_nix_environment() -> bool:
    """Validate Nix environment is properly configured.
    
    Returns:
        bool: True if Nix environment is valid
    """
```

**Nix Integration Points:**

```python
# OmniCppController.py - New methods
def _setup_nix_environment(self) -> None:
    """Configure build environment for Nix shell.
    
    Sets environment variables for:
    - Nix-provided compilers
    - Nix-provided CMake
    - Nix-provided Ninja
    - Nix-provided Qt6 and Vulkan
    """

def _validate_linux_environment(self) -> bool:
    """Validate Linux build environment is complete.
    
    Checks:
    - Compiler availability
    - CMake availability
    - Ninja availability
    - Qt6 availability (if needed)
    - Vulkan availability (if needed)
    - Conan availability
    
    Returns:
        bool: True if environment is valid
    """

def _get_linux_build_context(
    self,
    target: str,
    pipeline: str,
    preset: str,
    config: str,
    compiler: Optional[str] = None
) -> BuildContext:
    """Create BuildContext optimized for Linux builds.
    
    Args:
        target: Build target (engine, game, standalone, all)
        pipeline: Build pipeline name
        preset: CMake preset name
        config: Build configuration (debug, release)
        compiler: Optional compiler (gcc, clang, auto-detect)
    
    Returns:
        BuildContext: Configured build context for Linux
    """
```

**CachyOS-Specific Configurations:**

```python
# omni_scripts/platform/linux.py - New methods
def get_cachyos_compiler_flags(compiler: str, build_type: str) -> list[str]:
    """Get CachyOS-specific compiler flags.
    
    Args:
        compiler: Compiler name (gcc, clang)
        build_type: Build type (debug, release)
    
    Returns:
        list[str]: Compiler flags for CachyOS
    """

def get_cachyos_linker_flags() -> list[str]:
    """Get CachyOS-specific linker flags.
    
    Returns:
        list[str]: Linker flags for CachyOS
    """

def get_cachyos_library_paths() -> list[Path]:
    """Get CachyOS library search paths.
    
    Returns:
        list[Path]: Library directories for CachyOS
    """
```

### 1.2 Platform Detection Enhancements

**Linux Distribution Detection:**

```python
@dataclass
class LinuxDistribution:
    """Linux distribution information."""
    name: str  # e.g., "Arch Linux", "Ubuntu", "Fedora"
    version: str  # e.g., "2023.12.01", "22.04", "38"
    family: str  # e.g., "arch", "debian", "fedora"
    package_manager: str  # e.g., "pacman", "apt", "dnf"
    is_cachyos: bool  # True if CachyOS detected
```

**Detection Logic:**

1. Check `/etc/os-release` for distribution info
2. Detect CachyOS by checking for `ID=cachyos` or `ID_LIKE=arch`
3. Detect package manager by checking for `pacman`, `apt`, `dnf`, `yum`
4. Detect Nix environment by checking `$IN_NIX_SHELL` environment variable

### 1.3 Enhanced Build Methods

**Linux-Specific Build Flow:**

```python
def build(
    self,
    target: str,
    pipeline: str,
    preset: str,
    config: str,
    compiler: Optional[str] = None,
    clean: bool = False,
    use_nix: bool = False
) -> int:
    """Build the project with Linux-specific enhancements.
    
    Enhanced to:
    - Auto-detect Linux distribution
    - Use Nix environment if available
    - Apply CachyOS-specific flags
    - Validate Linux environment before build
    """
```

---

## 2. Enhanced flake.nix Structure

### 2.1 Required Nix Packages for CachyOS

**Core Development Tools:**

```nix
buildInputs = with pkgs; [
  # Compilers
  gcc
  clang
  gcc13  # Latest stable GCC
  llvmPackages_19.clang  # Latest stable Clang
  
  # Build System
  cmake
  ninja
  ccache  # Compiler cache
  
  # Package Managers
  conan
  python3
  python3Packages.pip
  
  # Documentation
  doxygen
  graphviz
  
  # Code Quality
  clang-tools  # clang-format, clang-tidy
  cppcheck
]
```

**Qt6 and Vulkan:**

```nix
buildInputs = with pkgs; [
  # Qt6
  qt6.qtbase
  qt6.qttools
  qt6.qtdeclarative
  qt6.qtwayland
  qt6.qtsvg
  qt6.qtimageformats
  
  # Vulkan
  vulkan-headers
  vulkan-loader
  vulkan-tools
  vulkan-validation-layers
  vulkan-extension-layer
  
  # Graphics
  mesa
  glslang
  spirv-tools
]
```

**Testing and Debugging:**

```nix
buildInputs = with pkgs; [
  # Testing
  gtest
  gmock
  pytest
  
  # Debugging
  gdb
  lldb
  valgrind
  
  # Performance
  perf-tools
  hotspot
]
```

### 2.2 Development Environment Shell

**Shell Configuration:**

```nix
devShells.${system}.default = pkgs.mkShell {
  name = "omnicpp-cachyos-dev";
  
  buildInputs = with pkgs; [
    # All packages listed above
  ];
  
  shellHook = ''
    echo ">> Loaded OmniCPP C++ Development Environment (CachyOS)"
    echo ">> Platform: Linux (CachyOS)"
    echo ">> Compilers: GCC 13, Clang 19"
    echo ">> Qt6: Latest stable"
    echo ">> Vulkan: Latest stable"
    
    # Qt6 environment
    export QT_QPA_PLATFORM=wayland
    export QT_PLUGIN_PATH=${pkgs.qt6.qtbase}/lib/qt-6/plugins
    
    # Vulkan environment
    export VK_LAYER_PATH=${pkgs.vulkan-validation-layers}/share/vulkan/explicit_layer.d
    export VK_ICD_FILENAMES=${pkgs.vulkan-loader}/share/vulkan/icd.d/intel_icd.x86_64.json
    
    # Compiler cache
    export CCACHE_DIR=$PWD/.ccache
    
    # Conan environment
    export CONAN_USER_HOME=$PWD/.conan2
    
    # CMake defaults
    export CMAKE_GENERATOR="Ninja"
    export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)
    
    echo ">> Environment ready!"
  '';
}
```

### 2.3 CMake Integration

**Nix-Aware CMake Configuration:**

```nix
# CMake configuration in shellHook
export CMAKE_PREFIX_PATH="${pkgs.qt6.qtbase}:${pkgs.vulkan-headers}:$CMAKE_PREFIX_PATH"
export CMAKE_LIBRARY_PATH="${pkgs.qt6.qtbase}/lib:${pkgs.vulkan-loader}/lib:$CMAKE_LIBRARY_PATH"
export CMAKE_INCLUDE_PATH="${pkgs.qt6.qtbase}/include:${pkgs.vulkan-headers}/include:$CMAKE_INCLUDE_PATH"
```

### 2.4 Compiler Toolchains

**GCC Toolchain:**

```nix
gccToolchain = pkgs.mkShell {
  name = "omnicpp-gcc-toolchain";
  
  buildInputs = with pkgs; [
    gcc13
    gnumake
    ninja
  ];
  
  shellHook = ''
    export CC=gcc
    export CXX=g++
    export CMAKE_C_COMPILER=gcc
    export CMAKE_CXX_COMPILER=g++
    echo ">> GCC toolchain configured"
  '';
}
```

**Clang Toolchain:**

```nix
clangToolchain = pkgs.mkShell {
  name = "omnicpp-clang-toolchain";
  
  buildInputs = with pkgs; [
    llvmPackages_19.clang
    llvmPackages_19.clang-tools
    ninja
  ];
  
  shellHook = ''
    export CC=clang
    export CXX=clang++
    export CMAKE_C_COMPILER=clang
    export CMAKE_CXX_COMPILER=clang++
    echo ">> Clang toolchain configured"
  '';
}
```

### 2.5 Conan/vcpkg Integration

**Conan Integration:**

```nix
# Conan environment setup in shellHook
export CONAN_USER_HOME=$PWD/.conan2
export CONAN_REVISIONS_ENABLED=1
export CONAN_V2_MODE=1
```

**vcpkg Integration (Optional):**

```nix
# vcpkg environment setup in shellHook
export VCPKG_ROOT=$PWD/vcpkg
export VCPKG_DEFAULT_TRIPLET=x64-linux
```

---

## 3. Enhanced VSCode Configuration

### 3.1 New Tasks in tasks.json for Linux

**Linux Configure Tasks:**

```json
{
  "label": "Configure Build (Linux GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": [
    "OmniCppController.py",
    "configure",
    "--compiler",
    "gcc",
    "--build-type",
    "Debug",
    "--use-nix"
  ],
  "options": {
    "cwd": "${workspaceFolder}"
  },
  "problemMatcher": [],
  "group": {
    "kind": "build",
    "isDefault": false
  },
  "detail": "Configure CMake project with GCC compiler for Debug build using Nix environment"
}
```

**Linux Build Tasks:**

```json
{
  "label": "Build Engine (Linux GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": [
    "OmniCppController.py",
    "build",
    "engine",
    "Clean Build Pipeline",
    "gcc-debug",
    "debug",
    "--compiler",
    "gcc",
    "--use-nix"
  ],
  "options": {
    "cwd": "${workspaceFolder}"
  },
  "problemMatcher": "$gcc",
  "group": {
    "kind": "build",
    "isDefault": false
  },
  "dependsOn": [
    "Configure Build (Linux GCC - Debug)"
  ],
  "detail": "Build Engine target with GCC compiler in Debug mode using Nix"
}
```

**Nix Shell Tasks:**

```json
{
  "label": "Enter Nix Dev Shell",
  "type": "shell",
  "command": "nix-shell",
  "args": [
    ".",
    "--run",
    "python",
    "OmniCppController.py",
    "help"
  ],
  "options": {
    "cwd": "${workspaceFolder}"
  },
  "problemMatcher": [],
  "group": {
    "kind": "build",
    "isDefault": false
  },
  "detail": "Enter Nix development shell and run OmniCppController"
}
```

**CachyOS-Specific Tasks:**

```json
{
  "label": "Validate CachyOS Environment",
  "type": "shell",
  "command": "python",
  "args": [
    "OmniCppController.py",
    "validate",
    "--platform",
    "cachyos"
  ],
  "options": {
    "cwd": "${workspaceFolder}"
  },
  "problemMatcher": [],
  "group": {
    "kind": "test",
    "isDefault": false
  },
  "detail": "Validate CachyOS build environment is properly configured"
}
```

### 3.2 New Launch Configurations in launch.json

**Linux Debug Configurations:**

```json
{
  "name": "Debug Engine (Linux GCC - Debug)",
  "type": "cppdbg",
  "request": "launch",
  "program": "${workspaceFolder}/build/gcc/debug/bin/OmniCppEngine",
  "args": [],
  "stopAtEntry": false,
  "cwd": "${workspaceFolder}",
  "environment": [
    {
      "name": "LD_LIBRARY_PATH",
      "value": "${workspaceFolder}/build/gcc/debug/lib"
    }
  ],
  "externalConsole": false,
  "MIMode": "gdb",
  "miDebuggerPath": "/usr/bin/gdb",
  "miDebuggerArgs": "",
  "setupCommands": [
    {
      "description": "Enable pretty-printing for gdb",
      "text": "-enable-pretty-printing",
      "ignoreFailures": true
    },
    {
      "description": "Set Disassembly Flavor to Intel",
      "text": "-gdb-set disassembly-flavor intel",
      "ignoreFailures": true
    },
    {
      "description": "Set library search path",
      "text": "-gdb-set solib-search-path ${workspaceFolder}/build/gcc/debug/lib",
      "ignoreFailures": true
    }
  ],
  "preLaunchTask": "Build Engine (Linux GCC - Debug)"
}
```

**Linux Clang Debug Configurations:**

```json
{
  "name": "Debug Engine (Linux Clang - Debug)",
  "type": "cppdbg",
  "request": "launch",
  "program": "${workspaceFolder}/build/clang/debug/bin/OmniCppEngine",
  "args": [],
  "stopAtEntry": false,
  "cwd": "${workspaceFolder}",
  "environment": [
    {
      "name": "LD_LIBRARY_PATH",
      "value": "${workspaceFolder}/build/clang/debug/lib"
    }
  ],
  "externalConsole": false,
  "MIMode": "lldb",
  "miDebuggerPath": "/usr/bin/lldb",
  "miDebuggerArgs": "",
  "setupCommands": [
    {
      "description": "Enable pretty-printing for lldb",
      "text": "-enable-pretty-printing",
      "ignoreFailures": true
    }
  ],
  "preLaunchTask": "Build Engine (Linux Clang - Debug)"
}
```

### 3.3 Platform-Specific Task Variants

**Task Organization:**

- **Windows Tasks:** MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang
- **Linux Tasks:** GCC, Clang (with Nix variants)
- **WASM Tasks:** Emscripten
- **Cross-Compile Tasks:** ARM64, x86

**Task Naming Convention:**

```
Configure Build (<Platform> <Compiler> - <Config>)
Build <Target> (<Platform> <Compiler> - <Config>)
Debug <Target> (<Platform> <Compiler> - <Config>)
```

---

## 4. New Conan Profiles

### 4.1 Linux Profiles

**gcc-linux Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[buildenv]
CC=gcc
CXX=g++
CMAKE_C_COMPILER=gcc
CMAKE_CXX_COMPILER=g++

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
```

**gcc-linux-debug Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Debug

[buildenv]
CC=gcc
CXX=g++
CMAKE_C_COMPILER=gcc
CMAKE_CXX_COMPILER=g++
CFLAGS=-g -O0 -Wall -Wextra
CXXFLAGS=-g -O0 -Wall -Wextra

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
*:with_debug_info=True
```

**clang-linux Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Release

[buildenv]
CC=clang
CXX=clang++
CMAKE_C_COMPILER=clang
CMAKE_CXX_COMPILER=clang++

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
```

**clang-linux-debug Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Debug

[buildenv]
CC=clang
CXX=clang++
CMAKE_C_COMPILER=clang
CMAKE_CXX_COMPILER=clang++
CFLAGS=-g -O0 -Wall -Wextra
CXXFLAGS=-g -O0 -Wall -Wextra

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
*:with_debug_info=True
```

### 4.2 CachyOS-Specific Profiles

**cachyos Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Release

[buildenv]
CC=gcc
CXX=g++
CMAKE_C_COMPILER=gcc
CMAKE_CXX_COMPILER=g++
LDFLAGS=-Wl,--as-needed

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
*:enable_lto=True
```

**cachyos-debug Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Debug

[buildenv]
CC=gcc
CXX=g++
CMAKE_C_COMPILER=gcc
CMAKE_CXX_COMPILER=g++
CFLAGS=-g -O0 -Wall -Wextra -fno-omit-frame-pointer
CXXFLAGS=-g -O0 -Wall -Wextra -fno-omit-frame-pointer
LDFLAGS=-Wl,--as-needed

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
*:with_debug_info=True
*:enable_sanitizers=True
```

**cachyos-clang Profile:**

```ini
[settings]
os=Linux
arch=x86_64
compiler=clang
compiler.version=19
compiler.libcxx=libc++
build_type=Release

[buildenv]
CC=clang
CXX=clang++
CMAKE_C_COMPILER=clang
CMAKE_CXX_COMPILER=clang++
LDFLAGS=-Wl,--as-needed

[conf]
tools.build:jobs=auto

[options]
*:shared=True
*:fPIC=True
*:enable_lto=True
```

### 4.3 Debug/Release Variants

**Profile Naming Convention:**

```
gcc-linux           # Release
gcc-linux-debug     # Debug
clang-linux         # Release
clang-linux-debug   # Debug
cachyos            # Release
cachyos-debug      # Debug
cachyos-clang      # Release
cachyos-clang-debug # Debug
```

**Profile Inheritance:**

```
gcc-linux-debug inherits from gcc-linux
clang-linux-debug inherits from clang-linux
cachyos-debug inherits from gcc-linux-debug
cachyos-clang-debug inherits from clang-linux-debug
```

---

## 5. New Setup Scripts

### 5.1 Linux Setup Scripts (.sh)

**setup_gcc.sh:**

```bash
#!/bin/bash
# Setup GCC build environment for Linux

set -e

echo "Setting up GCC build environment..."

# Detect GCC installation
if command -v gcc &> /dev/null; then
    GCC_VERSION=$(gcc --version | head -n1)
    echo "Found GCC: $GCC_VERSION"
else
    echo "Error: GCC not found. Install with: sudo apt install build-essential"
    exit 1
fi

# Set environment variables
export CC=gcc
export CXX=g++
export CMAKE_C_COMPILER=gcc
export CMAKE_CXX_COMPILER=g++

# Validate CMake
if command -v cmake &> /dev/null; then
    CMAKE_VERSION=$(cmake --version | head -n1)
    echo "Found CMake: $CMAKE_VERSION"
else
    echo "Error: CMake not found. Install with: sudo apt install cmake"
    exit 1
fi

# Validate Ninja
if command -v ninja &> /dev/null; then
    echo "Found Ninja: $(ninja --version)"
else
    echo "Error: Ninja not found. Install with: sudo apt install ninja-build"
    exit 1
fi

echo "GCC build environment ready!"
```

**setup_clang.sh:**

```bash
#!/bin/bash
# Setup Clang build environment for Linux

set -e

echo "Setting up Clang build environment..."

# Detect Clang installation
if command -v clang &> /dev/null; then
    CLANG_VERSION=$(clang --version | head -n1)
    echo "Found Clang: $CLANG_VERSION"
else
    echo "Error: Clang not found. Install with: sudo apt install clang"
    exit 1
fi

# Set environment variables
export CC=clang
export CXX=clang++
export CMAKE_C_COMPILER=clang
export CMAKE_CXX_COMPILER=clang++

# Validate CMake
if command -v cmake &> /dev/null; then
    CMAKE_VERSION=$(cmake --version | head -n1)
    echo "Found CMake: $CMAKE_VERSION"
else
    echo "Error: CMake not found. Install with: sudo apt install cmake"
    exit 1
fi

# Validate Ninja
if command -v ninja &> /dev/null; then
    echo "Found Ninja: $(ninja --version)"
else
    echo "Error: Ninja not found. Install with: sudo apt install ninja-build"
    exit 1
fi

echo "Clang build environment ready!"
```

**setup_cachyos.sh:**

```bash
#!/bin/bash
# Setup CachyOS build environment

set -e

echo "Setting up CachyOS build environment..."

# Detect CachyOS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" = "cachyos" ] || [ "$ID_LIKE" = "arch" ]; then
        echo "Detected CachyOS/Arch Linux"
    else
        echo "Warning: Not running on CachyOS/Arch Linux"
    fi
else
    echo "Error: Cannot detect Linux distribution"
    exit 1
fi

# Validate pacman
if command -v pacman &> /dev/null; then
    echo "Found pacman: $(pacman --version | head -n1)"
else
    echo "Error: pacman not found"
    exit 1
fi

# Check for required packages
REQUIRED_PACKAGES="gcc clang cmake ninja python3"
for pkg in $REQUIRED_PACKAGES; do
    if ! command -v $pkg &> /dev/null; then
        echo "Error: $pkg not found. Install with: sudo pacman -S $pkg"
        exit 1
    fi
done

echo "CachyOS build environment ready!"
```

**setup_nix.sh:**

```bash
#!/bin/bash
# Setup Nix development environment

set -e

echo "Setting up Nix development environment..."

# Check for Nix
if [ -n "$IN_NIX_SHELL" ]; then
    echo "Running in Nix shell"
else
    echo "Error: Not in Nix shell. Run with: nix-shell ."
    exit 1
fi

# Validate Nix packages
REQUIRED_NIX_PKGS="gcc clang cmake ninja python3"
for pkg in $REQUIRED_NIX_PKGS; do
    if ! command -v $pkg &> /dev/null; then
        echo "Error: $pkg not found in Nix environment"
        echo "Add to flake.nix buildInputs"
        exit 1
    fi
done

# Set Nix-specific environment
export NIX_PATH=$NIX_PATH
export NIX_PROFILES=$NIX_PROFILES

echo "Nix development environment ready!"
```

**setup_qt6_vulkan.sh:**

```bash
#!/bin/bash
# Setup Qt6 and Vulkan environment for Linux

set -e

echo "Setting up Qt6 and Vulkan environment..."

# Check Qt6
if pkg-config --exists Qt6Core; then
    QT_VERSION=$(pkg-config --modversion Qt6Core)
    echo "Found Qt6: $QT_VERSION"
else
    echo "Error: Qt6 not found"
    echo "Install with: sudo apt install qt6-base-dev (Ubuntu/Debian)"
    echo "Install with: sudo pacman -S qt6-base (Arch/CachyOS)"
    exit 1
fi

# Set Qt6 environment
export QT_QPA_PLATFORM=wayland
export QT_PLUGIN_PATH=$(pkg-config --variable=plugins_dir Qt6Core)

# Check Vulkan
if command -v vulkaninfo &> /dev/null; then
    echo "Found Vulkan tools"
else
    echo "Error: Vulkan tools not found"
    echo "Install with: sudo apt install vulkan-tools (Ubuntu/Debian)"
    echo "Install with: sudo pacman -S vulkan-tools (Arch/CachyOS)"
    exit 1
fi

# Set Vulkan environment
export VK_LAYER_PATH=/usr/share/vulkan/explicit_layer.d
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/intel_icd.x86_64.json

echo "Qt6 and Vulkan environment ready!"
```

**validate_environment.sh:**

```bash
#!/bin/bash
# Validate Linux build environment

set -e

echo "Validating Linux build environment..."

# Check compilers
echo "Checking compilers..."
if command -v gcc &> /dev/null; then
    echo "✓ GCC: $(gcc --version | head -n1)"
else
    echo "✗ GCC not found"
    exit 1
fi

if command -v clang &> /dev/null; then
    echo "✓ Clang: $(clang --version | head -n1)"
else
    echo "✗ Clang not found"
fi

# Check build tools
echo "Checking build tools..."
if command -v cmake &> /dev/null; then
    echo "✓ CMake: $(cmake --version | head -n1)"
else
    echo "✗ CMake not found"
    exit 1
fi

if command -v ninja &> /dev/null; then
    echo "✓ Ninja: $(ninja --version)"
else
    echo "✗ Ninja not found"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python: $(python3 --version)"
else
    echo "✗ Python not found"
    exit 1
fi

# Check Conan
if command -v conan &> /dev/null; then
    echo "✓ Conan: $(conan --version)"
else
    echo "✗ Conan not found"
    exit 1
fi

# Check Qt6
if pkg-config --exists Qt6Core; then
    echo "✓ Qt6: $(pkg-config --modversion Qt6Core)"
else
    echo "✗ Qt6 not found"
fi

# Check Vulkan
if command -v vulkaninfo &> /dev/null; then
    echo "✓ Vulkan tools found"
else
    echo "✗ Vulkan tools not found"
fi

# Check Nix
if [ -n "$IN_NIX_SHELL" ]; then
    echo "✓ Nix shell active"
else
    echo "✗ Not in Nix shell"
fi

echo ""
echo "Environment validation complete!"
```

### 5.2 Script Purposes

| Script | Purpose | Usage |
|---------|---------|--------|
| setup_gcc.sh | Configure GCC build environment | `./setup_gcc.sh` |
| setup_clang.sh | Configure Clang build environment | `./setup_clang.sh` |
| setup_cachyos.sh | Configure CachyOS-specific environment | `./setup_cachyos.sh` |
| setup_nix.sh | Configure Nix development environment | `./setup_nix.sh` |
| setup_qt6_vulkan.sh | Configure Qt6 and Vulkan environment | `./setup_qt6_vulkan.sh` |
| validate_environment.sh | Validate complete build environment | `./validate_environment.sh` |

---

## 6. Documentation Updates

### 6.1 Documentation Files to Create

**New Documentation:**

- `docs/nix-development.md` - Nix development workflow guide
- `docs/cachyos-builds.md` - CachyOS-specific build guide
- `docs/linux-troubleshooting.md` - Linux troubleshooting guide
- `docs/conan-linux-profiles.md` - Conan Linux profiles guide
- `docs/vscode-linux-setup.md` - VSCode Linux configuration guide

### 6.2 Documentation Files to Update

**Update Existing Documentation:**

- `docs/linux-builds.md` - Add Nix integration, CachyOS specifics
- `README.md` - Add Linux/CachyOS as primary development platform
- `docs/getting-started/installation.md` - Add Linux/CachyOS installation steps
- `docs/user-guide-build-system.md` - Add Linux build system details
- `docs/troubleshooting-guide.md` - Add Linux-specific troubleshooting

### 6.3 New Guides for Linux Builds

**Nix Development Guide:**

```markdown
# Nix Development Guide

## Overview
Nix provides reproducible development environments for OmniCPP Template.

## Getting Started
1. Install Nix: `sh <(curl -L https://nixos.org/nix/install)`
2. Enter dev shell: `nix-shell .`
3. Build project: `python OmniCppController.py build all "Clean Build Pipeline" default Release`

## Nix Shell Features
- GCC 13 and Clang 19 compilers
- Qt6 with Wayland support
- Vulkan SDK with validation layers
- CMake and Ninja build system
- Conan package manager

## Troubleshooting
- Package not found: Add to flake.nix buildInputs
- Environment issues: Run `nix-shell --pure .`
```

**CachyOS Build Guide:**

```markdown
# CachyOS Build Guide

## Overview
CachyOS is an Arch Linux derivative optimized for performance.

## Prerequisites
- CachyOS 2023.12.01 or later
- GCC 13+ or Clang 19+
- CMake 4.0+
- Ninja build system
- Conan 2.0+

## Installation
```bash
sudo pacman -S gcc clang cmake ninja python3 python-pip
pip install conan
```

## Building
```bash
python OmniCppController.py build all "Clean Build Pipeline" default Release
```

## CachyOS-Specific Features
- LTO (Link-Time Optimization) enabled by default
- Optimized compiler flags for CachyOS kernel
- Wayland support for Qt6
- Vulkan with Mesa drivers
```

---

## 7. Cleanup Actions

### 7.1 Duplicate Files to Remove

**Windows-Specific Test Files:**

- `test_mingw_clang.cpp` - MinGW-Clang test (Linux equivalent exists)
- `test_mingw_gcc.cpp` - MinGW-GCC test (Linux equivalent exists)
- `test_msvc.cpp` - MSVC test (no Linux equivalent needed)

**Rationale:**
- These files are Windows-specific compilation tests
- Linux builds use `test_gcc.cpp` and `test_clang.cpp` instead
- Removing reduces confusion and repository size

### 7.2 Obsolete Files to Archive

**Legacy Python Scripts:**

- `scripts/setup_environment.bat` - Windows batch script
- `scripts/setup_environment.ps1` - Windows PowerShell script
- `scripts/detect_msvc_version.ps1` - MSVC-specific script

**Archive Location:**
- Create `.archive/windows_scripts/` directory
- Move files with timestamp: `.archive/windows_scripts/2026-01-27/`

**Rationale:**
- These scripts are Windows-specific
- Linux uses shell scripts (.sh) instead
- Archive preserves history if needed

### 7.3 Reorganization of Test Files

**Current Test File Structure:**

```
test_mingw_clang.cpp
test_mingw_gcc.cpp
test_msvc.cpp
```

**Reorganized Test File Structure:**

```
tests/
├── cpp/
│   ├── test_gcc.cpp          # GCC test (Linux)
│   ├── test_clang.cpp        # Clang test (Linux)
│   ├── test_msvc.cpp         # MSVC test (Windows - archived)
│   ├── test_mingw_gcc.cpp    # MinGW-GCC test (Windows - archived)
│   └── test_mingw_clang.cpp  # MinGW-Clang test (Windows - archived)
└── platform/
    ├── test_linux_gcc.cpp     # Linux GCC platform test
    ├── test_linux_clang.cpp   # Linux Clang platform test
    ├── test_windows_msvc.cpp   # Windows MSVC platform test
    └── test_windows_mingw.cpp  # Windows MinGW platform test
```

**Rationale:**
- Clear separation of platform-specific tests
- Easier to find relevant tests for each platform
- Reduces root directory clutter

---

## 8. Enhanced CMake Integration

### 8.1 New CMake Presets for Linux

**Nix-Aware Presets:**

```json
{
  "name": "nix-gcc-debug",
  "displayName": "Nix GCC Debug",
  "description": "Debug build with GCC in Nix environment",
  "binaryDir": "${sourceDir}/build/nix/gcc/debug",
  "generator": "Ninja",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_COMPILER": "gcc",
    "CMAKE_CXX_COMPILER": "g++",
    "CMAKE_EXPORT_COMPILE_COMMANDS": "ON",
    "OMNICPP_BUILD_ENGINE": "ON",
    "OMNICPP_BUILD_GAME": "ON",
    "OMNICPP_BUILD_TESTS": "ON"
  },
  "environment": {
    "NIX_PATH": "$env{NIX_PATH}",
    "NIX_PROFILES": "$env{NIX_PROFILES}"
  }
}
```

**CachyOS Presets:**

```json
{
  "name": "cachyos-gcc-debug",
  "displayName": "CachyOS GCC Debug",
  "description": "Debug build with GCC on CachyOS",
  "binaryDir": "${sourceDir}/build/cachyos/gcc/debug",
  "generator": "Ninja",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "CMAKE_C_COMPILER": "gcc",
    "CMAKE_CXX_COMPILER": "g++",
    "CMAKE_C_FLAGS": "-g -O0 -Wall -Wextra -fno-omit-frame-pointer",
    "CMAKE_CXX_FLAGS": "-g -O0 -Wall -Wextra -fno-omit-frame-pointer",
    "CMAKE_EXE_LINKER_FLAGS": "-Wl,--as-needed",
    "OMNICPP_BUILD_ENGINE": "ON",
    "OMNICPP_BUILD_GAME": "ON",
    "OMNICPP_BUILD_TESTS": "ON"
  }
}
```

### 8.2 Platform Detection Improvements

**CMake Platform Detection:**

```cmake
# cmake/PlatformConfig.cmake - Enhanced

# Detect Linux distribution
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    # Read /etc/os-release
    if(EXISTS "/etc/os-release")
        file(READ "/etc/os-release" OS_RELEASE)
        
        # Detect CachyOS
        if(OS_RELEASE MATCHES "ID=cachyos")
            set(OMNICPP_IS_CACHYOS TRUE)
            message(STATUS "Detected CachyOS")
        elseif(OS_RELEASE MATCHES "ID_LIKE=arch")
            set(OMNICPP_IS_ARCH TRUE)
            message(STATUS "Detected Arch Linux")
        elseif(OS_RELEASE MATCHES "ID=ubuntu")
            set(OMNICPP_IS_UBUNTU TRUE)
            message(STATUS "Detected Ubuntu")
        endif()
    endif()
    
    # Detect Nix environment
    if(DEFINED ENV{IN_NIX_SHELL})
        set(OMNICPP_IS_NIX TRUE)
        message(STATUS "Detected Nix environment")
    endif()
endif()
```

### 8.3 Nix-Aware Build Configurations

**Nix Build Configuration:**

```cmake
# cmake/user/tmplt-nix.cmake - New module

if(OMNICPP_IS_NIX)
    # Use Nix-provided paths
    set(CMAKE_PREFIX_PATH "${NIX_PATH}" CACHE PATH "Nix prefix path")
    set(CMAKE_LIBRARY_PATH "${NIX_PROFILES}/lib" CACHE PATH "Nix library path")
    set(CMAKE_INCLUDE_PATH "${NIX_PROFILES}/include" CACHE PATH "Nix include path")
    
    # Enable compiler cache
    set(OMNICPP_ENABLE_CCACHE ON CACHE BOOL "Enable ccache in Nix")
    
    message(STATUS "Configuring for Nix environment")
endif()
```

**CachyOS Build Configuration:**

```cmake
# cmake/user/tmplt-cachyos.cmake - New module

if(OMNICPP_IS_CACHYOS)
    # Enable LTO for CachyOS
    set(OMNICPP_ENABLE_LTO ON CACHE BOOL "Enable Link-Time Optimization")
    
    # CachyOS-specific flags
    set(OMNICPP_CACHYOS_FLAGS "-march=x86-64-v3 -mtune=generic")
    
    # Use Wayland by default
    set(OMNICPP_QT_PLATFORM "wayland" CACHE STRING "Qt platform")
    
    message(STATUS "Configuring for CachyOS")
endif()
```

---

## 9. Directory Structure Changes

### 9.1 New Directories to Create

```
OmniCPP-template/
├── .specs/
│   └── 04_future_state/
│       └── linux_expansion_manifest.md  # This document
├── .archive/                          # New: Archive directory
│   └── windows_scripts/               # New: Archived Windows scripts
├── scripts/
│   └── linux/                        # New: Linux setup scripts
│       ├── setup_gcc.sh
│       ├── setup_clang.sh
│       ├── setup_cachyos.sh
│       ├── setup_nix.sh
│       ├── setup_qt6_vulkan.sh
│       └── validate_environment.sh
├── tests/
│   └── platform/                     # New: Platform-specific tests
│       ├── test_linux_gcc.cpp
│       ├── test_linux_clang.cpp
│       ├── test_windows_msvc.cpp
│       └── test_windows_mingw.cpp
└── docs/
    ├── nix-development.md              # New: Nix guide
    ├── cachyos-builds.md              # New: CachyOS guide
    ├── linux-troubleshooting.md         # New: Linux troubleshooting
    ├── conan-linux-profiles.md        # New: Conan Linux profiles
    └── vscode-linux-setup.md          # New: VSCode Linux guide
```

### 9.2 Directories to Reorganize

**Reorganize Root Test Files:**

```
# Move from root:
test_mingw_clang.cpp  -> tests/platform/test_windows_mingw.cpp
test_mingw_gcc.cpp   -> tests/platform/test_windows_mingw.cpp
test_msvc.cpp        -> tests/platform/test_windows_msvc.cpp

# Create new tests:
tests/platform/test_linux_gcc.cpp
tests/platform/test_linux_clang.cpp
```

**Reorganize Setup Scripts:**

```
# Move from scripts/setup_*.bat and *.ps1:
scripts/setup_environment.bat      -> .archive/windows_scripts/2026-01-27/
scripts/setup_environment.ps1     -> .archive/windows_scripts/2026-01-27/
scripts/detect_msvc_version.ps1 -> .archive/windows_scripts/2026-01-27/

# Create new scripts/linux/:
scripts/linux/setup_gcc.sh
scripts/linux/setup_clang.sh
scripts/linux/setup_cachyos.sh
scripts/linux/setup_nix.sh
scripts/linux/setup_qt6_vulkan.sh
scripts/linux/validate_environment.sh
```

### 9.3 Naming Conventions for Consistency

**File Naming Conventions:**

- **Setup Scripts:** `setup_<compiler>_<platform>.sh` or `setup_<feature>_<platform>.sh`
- **Test Files:** `test_<platform>_<compiler>.cpp`
- **Conan Profiles:** `<compiler>-<platform>-<config>`
- **CMake Presets:** `<platform>-<compiler>-<config>`
- **Documentation:** `<topic>-<platform>.md`

**Directory Naming Conventions:**

- **Platform-Specific:** `scripts/<platform>/`, `tests/platform/`
- **Archived:** `.archive/<platform>/`
- **Documentation:** `docs/<topic>/`

---

## 10. File Artifact Summary

### 10.1 New File Artifacts

**Python Modules:**

- `omni_scripts/platform/linux.py` - Enhanced with CachyOS detection
- `omni_scripts/compilers/detector.py` - Enhanced with Linux compiler detection
- `omni_scripts/utils/nix_utils.py` - New Nix utilities module

**Configuration Files:**

- `flake.nix` - Enhanced with comprehensive CachyOS packages
- `.vscode/tasks.json` - Enhanced with Linux tasks
- `.vscode/launch.json` - Enhanced with Linux launch configs
- `CMakePresets.json` - Enhanced with Nix and CachyOS presets

**Conan Profiles:**

- `conan/profiles/gcc-linux` - New GCC Linux profile
- `conan/profiles/gcc-linux-debug` - New GCC Linux debug profile
- `conan/profiles/clang-linux` - New Clang Linux profile
- `conan/profiles/clang-linux-debug` - New Clang Linux debug profile
- `conan/profiles/cachyos` - New CachyOS profile
- `conan/profiles/cachyos-debug` - New CachyOS debug profile
- `conan/profiles/cachyos-clang` - New CachyOS Clang profile
- `conan/profiles/cachyos-clang-debug` - New CachyOS Clang debug profile

**Setup Scripts:**

- `scripts/linux/setup_gcc.sh` - New GCC setup script
- `scripts/linux/setup_clang.sh` - New Clang setup script
- `scripts/linux/setup_cachyos.sh` - New CachyOS setup script
- `scripts/linux/setup_nix.sh` - New Nix setup script
- `scripts/linux/setup_qt6_vulkan.sh` - New Qt6/Vulkan setup script
- `scripts/linux/validate_environment.sh` - New environment validation script

**CMake Modules:**

- `cmake/user/tmplt-nix.cmake` - New Nix template
- `cmake/user/tmplt-cachyos.cmake` - New CachyOS template

**Documentation:**

- `docs/nix-development.md` - New Nix development guide
- `docs/cachyos-builds.md` - New CachyOS build guide
- `docs/linux-troubleshooting.md` - New Linux troubleshooting guide
- `docs/conan-linux-profiles.md` - New Conan Linux profiles guide
- `docs/vscode-linux-setup.md` - New VSCode Linux setup guide

**Test Files:**

- `tests/platform/test_linux_gcc.cpp` - New Linux GCC test
- `tests/platform/test_linux_clang.cpp` - New Linux Clang test

### 10.2 Modified File Artifacts

**Enhanced Files:**

- `OmniCppController.py` - Enhanced with Linux/Nix/CachyOS support
- `flake.nix` - Enhanced with comprehensive packages
- `.vscode/tasks.json` - Enhanced with Linux tasks
- `.vscode/launch.json` - Enhanced with Linux launch configs
- `CMakePresets.json` - Enhanced with Nix/CachyOS presets
- `cmake/PlatformConfig.cmake` - Enhanced with Linux detection
- `docs/linux-builds.md` - Updated with Nix/CachyOS info
- `README.md` - Updated with Linux/CachyOS as primary platform

### 10.3 Archived File Artifacts

**Archived Files:**

- `.archive/windows_scripts/2026-01-27/setup_environment.bat`
- `.archive/windows_scripts/2026-01-27/setup_environment.ps1`
- `.archive/windows_scripts/2026-01-27/detect_msvc_version.ps1`

### 10.4 Removed File Artifacts

**Removed Files:**

- `test_mingw_clang.cpp` - Moved to `tests/platform/test_windows_mingw.cpp`
- `test_mingw_gcc.cpp` - Moved to `tests/platform/test_windows_mingw.cpp`
- `test_msvc.cpp` - Moved to `tests/platform/test_windows_msvc.cpp`

### 10.5 Estimated File Counts

**New Files:** 28
- Python modules: 3
- Configuration files: 5
- Conan profiles: 7
- Setup scripts: 6
- CMake modules: 2
- Documentation: 5

**Modified Files:** 8
- Python controller: 1
- Configuration files: 4
- CMake modules: 1
- Documentation: 2

**Archived Files:** 3
- Windows scripts: 3

**Removed Files:** 3
- Test files: 3

**Total Changes:** 42 files

---

## 11. Linux and Windows Coexistence

### 11.1 Platform Detection Logic

**Unified Platform Detection:**

```python
# omni_scripts/platform/detector.py

def detect_platform() -> PlatformInfo:
    """Detect platform with Linux and Windows support.
    
    Returns:
        PlatformInfo: Platform information with OS, distribution, compiler
    """
    
    if sys.platform == "win32":
        return detect_windows_platform()
    elif sys.platform == "linux":
        return detect_linux_platform()
    elif sys.platform == "darwin":
        return detect_macos_platform()
    else:
        raise UnsupportedPlatformError(f"Unsupported platform: {sys.platform}")
```

### 11.2 Compiler Selection Strategy

**Automatic Compiler Selection:**

```python
# omni_scripts/compilers/detector.py

def detect_compiler(platform_info: PlatformInfo) -> Optional[CompilerInfo]:
    """Detect best available compiler for platform.
    
    Selection Logic:
    - Windows: MSVC (primary), MSVC-Clang (fallback)
    - Linux: GCC (primary), Clang (fallback)
    - Nix: Use Nix-provided compilers
    - CachyOS: GCC with LTO (primary), Clang (fallback)
    
    Returns:
        Optional[CompilerInfo]: Compiler information or None
    """
```

### 11.3 Build Configuration Harmonization

**Unified Build Context:**

```python
# omni_scripts/build.py

class BuildContext:
    """Unified build context for all platforms.
    
    Attributes:
        product: Build target (engine, game, standalone)
        task: Build pipeline name
        arch: Architecture (x64, arm64)
        build_type: Build configuration (debug, release)
        compiler: Compiler name (msvc, gcc, clang, auto-detect)
        platform: Platform info (Windows, Linux, CachyOS, Nix)
        is_cross_compilation: Cross-compilation flag
        lib_flag: Library build flag
        st_flag: Standalone build flag
        use_nix: Nix environment flag
    """
```

### 11.4 VSCode Configuration Organization

**Platform-Specific Task Groups:**

```json
{
  "version": "2.0.0",
  "tasks": [
    // Windows Tasks
    { "label": "Configure Build (Windows MSVC - Debug)", "group": { "kind": "build", "isDefault": false } },
    { "label": "Configure Build (Windows MSVC - Release)", "group": { "kind": "build", "isDefault": false } },
    
    // Linux Tasks
    { "label": "Configure Build (Linux GCC - Debug)", "group": { "kind": "build", "isDefault": false } },
    { "label": "Configure Build (Linux Clang - Debug)", "group": { "kind": "build", "isDefault": false } },
    
    // Nix Tasks
    { "label": "Enter Nix Dev Shell", "group": { "kind": "build", "isDefault": false } },
    
    // CachyOS Tasks
    { "label": "Validate CachyOS Environment", "group": { "kind": "test", "isDefault": false } }
  ]
}
```

---

## 12. Implementation Boundaries

### 12.1 Component Boundaries

**OmniCppController.py:**
- **Scope:** Platform detection, compiler selection, build orchestration
- **Not Scope:** CMake generation, Conan execution (delegated to managers)
- **Interface:** Public methods for configure, build, clean, install, test, package

**flake.nix:**
- **Scope:** Nix package definitions, shell environment
- **Not Scope:** Project configuration, build logic
- **Interface:** `nix-shell .` command

**VSCode Configuration:**
- **Scope:** Task definitions, launch configurations
- **Not Scope:** Build execution, debugging logic
- **Interface:** VSCode task runner, debugger

**Conan Profiles:**
- **Scope:** Compiler settings, build options
- **Not Scope:** Package definitions, dependency resolution
- **Interface:** `conan install . --profile=<profile>`

**Setup Scripts:**
- **Scope:** Environment validation, tool verification
- **Not Scope:** Build execution, dependency installation
- **Interface:** Direct script execution

### 12.2 Platform Boundaries

**Windows Support:**
- **Maintain:** All existing Windows functionality
- **Enhance:** None (Windows is already comprehensive)
- **Boundary:** Windows-specific files remain in place

**Linux Support:**
- **Maintain:** Existing Linux functionality
- **Enhance:** Nix integration, CachyOS support, comprehensive profiles
- **Boundary:** Linux-specific files added, Windows files archived

**Cross-Platform Support:**
- **Maintain:** Shared CMake modules, Python utilities
- **Enhance:** Platform detection, compiler selection
- **Boundary:** Platform-specific code isolated to platform modules

### 12.3 Integration Boundaries

**Nix Integration:**
- **Scope:** Environment setup, package availability
- **Not Scope:** Nix package management, NixOS configuration
- **Boundary:** Nix shell hook only

**CachyOS Integration:**
- **Scope:** CachyOS detection, compiler flags
- **Not Scope:** Pacman package management, Arch Linux configuration
- **Boundary:** Detection and configuration only

**Qt6/Vulkan Integration:**
- **Scope:** Environment setup, path configuration
- **Not Scope:** Qt6 installation, Vulkan SDK installation
- **Boundary:** Assumes Qt6/Vulkan are installed

---

## 13. Success Criteria

### 13.1 Functional Requirements

**Platform Detection:**
- [ ] Detect Linux distribution (Ubuntu, Arch, Fedora, CachyOS)
- [ ] Detect package manager (apt, pacman, dnf)
- [ ] Detect Nix environment
- [ ] Detect CachyOS specifically

**Compiler Detection:**
- [ ] Detect GCC on Linux
- [ ] Detect Clang on Linux
- [ ] Detect Nix-provided compilers
- [ ] Select appropriate compiler for CachyOS

**Build System:**
- [ ] Build with GCC on Linux
- [ ] Build with Clang on Linux
- [ ] Build in Nix environment
- [ ] Build with CachyOS-specific flags

**Package Management:**
- [ ] Use Conan with Linux profiles
- [ ] Use Nix packages in dev shell
- [ ] Use system packages for dependencies

**Development Environment:**
- [ ] Enter Nix dev shell
- [ ] Validate Linux environment
- [ ] Setup Qt6/Vulkan environment
- [ ] Configure VSCode for Linux

### 13.2 Non-Functional Requirements

**Code Quality:**
- [ ] Zero pylance errors in Python modules
- [ ] Comprehensive type hints in all functions
- [ ] Clear separation of platform-specific code
- [ ] Consistent naming conventions

**Documentation:**
- [ ] Comprehensive Linux build documentation
- [ ] Nix development guide
- [ ] CachyOS build guide
- [ ] Troubleshooting guides

**Maintainability:**
- [ ] Clear component boundaries
- [ ] Modular architecture
- [ ] Easy to add new platforms
- [ ] Easy to add new compilers

### 13.3 Performance Requirements

**Build Performance:**
- [ ] Parallel builds with Ninja
- [ ] Compiler cache support (ccache)
- [ ] Incremental builds
- [ ] Fast dependency resolution

**Runtime Performance:**
- [ ] Optimized compiler flags for CachyOS
- [ ] LTO enabled by default
- [ ] Native compilation for target platform

---

## 14. Migration Plan

### 14.1 Implementation Phases

**Phase 1: Foundation (Platform Detection)**
- Enhance `omni_scripts/platform/linux.py`
- Add `omni_scripts/utils/nix_utils.py`
- Update `omni_scripts/compilers/detector.py`

**Phase 2: Configuration (Nix and Conan)**
- Enhance `flake.nix`
- Create Conan Linux profiles
- Update CMake presets

**Phase 3: Integration (VSCode and Setup)**
- Update VSCode configurations
- Create setup scripts
- Update documentation

**Phase 4: Cleanup (Repository Organization)**
- Archive Windows scripts
- Reorganize test files
- Remove duplicate files

**Phase 5: Validation (Testing)**
- Test Linux builds with GCC
- Test Linux builds with Clang
- Test Nix environment
- Test CachyOS builds

### 14.2 Rollback Plan

**If Issues Arise:**
- Revert to previous commit
- Archive new files to `.archive/failed/`
- Document issues in `.specs/04_future_state/linux_rollback_report.md`

**Rollback Triggers:**
- Build failures on Linux
- Nix environment issues
- Conan profile problems
- VSCode configuration errors

---

## 15. Conclusion

This Linux expansion manifest defines a comprehensive enhancement to the OmniCPP Template, transforming it from a Windows-centric template to a truly cross-platform development environment with first-class Linux support. The expansion focuses on CachyOS as the primary target platform while maintaining compatibility with other Linux distributions and Windows.

**Key Outcomes:**

- **Enhanced OmniCppController.py** with Linux/Nix/CachyOS detection and integration
- **Comprehensive flake.nix** for reproducible CachyOS development
- **Complete Conan profiles** for GCC, Clang, and CachyOS
- **Linux-specific setup scripts** for environment configuration
- **Enhanced VSCode configurations** with Linux task variants
- **Comprehensive documentation** for Linux builds and Nix workflow
- **Repository cleanup** to remove Windows-centric artifacts
- **Enhanced CMake integration** with Nix-aware presets

**Total Changes:** 42 files (28 new, 8 modified, 3 archived, 3 removed)

This manifest serves as the blueprint for implementing comprehensive Linux support in the OmniCPP Template.
