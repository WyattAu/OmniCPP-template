# Installation

## Prerequisites

Before building OmniCppLib, ensure you have the following installed:

### Required Tools

- **CMake 4.0+**: Build system generator
- **C++ Compiler**: GCC 11+, Clang 14+, or MSVC 2022+ with C++20 support
- **Git**: For cloning the repository

### Optional Dependencies

- **Qt6**: For Qt/Vulkan components (optional)
- **Vulkan SDK**: For graphics features (optional)
- **Doxygen**: For API documentation generation
- **MkDocs**: For project documentation (requires Python)

## Installing Prerequisites

### Windows

```powershell
# Using Chocolatey
choco install cmake git

# Or download from official sites
# CMake: https://cmake.org/download/
# Git: https://git-scm.com/downloads
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install cmake git build-essential

# For Qt/Vulkan (optional)
sudo apt install qt6-base-dev vulkan-tools
```

### macOS

```bash
# Using Homebrew
brew install cmake git

# For Qt (optional)
brew install qt6
```

## Cloning the Repository

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

## Building the Project

```bash
# Configure
cmake -B build -S .

# Build
cmake --build build

# Install (optional)
cmake --install build
```

### Build Options

- `BUILD_LIBRARY`: Build the core library (default: ON)
- `BUILD_STANDALONE`: Build standalone executable (default: ON)
- `BUILD_QT_VULKAN`: Build Qt/Vulkan components (default: OFF)

Example with custom options:

```bash
cmake -B build -S . -DBUILD_QT_VULKAN=ON