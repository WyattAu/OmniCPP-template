# DES-020: Toolchain File Design

## Overview
Defines the toolchain file design for cross-platform CMake builds.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_TOOLCHAIN_FILE_H
#define OMNICPP_TOOLCHAIN_FILE_H

#include <string>
#include <map>
#include <optional>

namespace omnicpp {
namespace toolchain {

// Toolchain configuration
struct ToolchainConfig {
    std::string name;
    std::string version;
    std::string description;
    std::map<std::string, std::string> variables;

    bool validate() const {
        return !name.empty();
    }
};

// Platform configuration
struct PlatformConfig {
    std::string system_name;
    std::string system_version;
    std::string processor;
    std::string architecture;

    bool validate() const {
        return !system_name.empty() && !architecture.empty();
    }
};

// Compiler configuration
struct CompilerConfig {
    std::string id;
    std::string executable;
    std::string version;
    std::string language;
    std::string language_standard;
    std::string target;
    std::vector<std::string> flags;
    std::vector<std::string> include_dirs;
    std::vector<std::string> library_dirs;
    std::vector<std::string> libraries;

    bool validate() const {
        return !id.empty() && !executable.empty();
    }
};

// Linker configuration
struct LinkerConfig {
    std::string id;
    std::string executable;
    std::string version;
    std::string language;
    std::string target;
    std::vector<std::string> flags;
    std::vector<std::string> library_dirs;
    std::vector<std::string> libraries;

    bool validate() const {
        return !id.empty() && !executable.empty();
    }
};

// Archiver configuration
struct ArchiverConfig {
    std::string id;
    std::string executable;
    std::string version;
    std::string language;
    std::string target;
    std::vector<std::string> flags;

    bool validate() const {
        return !id.empty() && !executable.empty();
    }
};

// Build system configuration
struct BuildSystemConfig {
    std::string id;
    std::string executable;
    std::string version;
    std::string generator;
    std::string toolchain_file;

    bool validate() const {
        return !id.empty() && !executable.empty();
    }
};

// Toolchain file
class ToolchainFile {
public:
    ToolchainFile() = default;
    virtual ~ToolchainFile() = default;

    // Load toolchain file
    virtual bool load(const std::string& path) = 0;

    // Save toolchain file
    virtual bool save(const std::string& path) const = 0;

    // Get configuration
    virtual const ToolchainConfig& get_toolchain() const = 0;
    virtual const PlatformConfig& get_platform() const = 0;
    virtual const CompilerConfig& get_compiler() const = 0;
    virtual const LinkerConfig& get_linker() const = 0;
    virtual const ArchiverConfig& get_archiver() const = 0;
    virtual const BuildSystemConfig& get_build_system() const = 0;

    // Set configuration
    virtual void set_toolchain(const ToolchainConfig& config) = 0;
    virtual void set_platform(const PlatformConfig& config) = 0;
    virtual void set_compiler(const CompilerConfig& config) = 0;
    virtual void set_linker(const LinkerConfig& config) = 0;
    virtual void set_archiver(const ArchiverConfig& config) = 0;
    virtual void set_build_system(const BuildSystemConfig& config) = 0;

    // Validate configuration
    virtual bool validate() const = 0;

    // Generate CMake toolchain file
    virtual std::string generate_cmake_toolchain() const = 0;

    // Generate toolchain file for specific compiler
    virtual std::string generate_gcc_toolchain() const = 0;
    virtual std::string generate_clang_toolchain() const = 0;
    virtual std::string generate_msvc_toolchain() const = 0;
    virtual std::string generate_mingw_toolchain() const = 0;
};

// Default implementation
class DefaultToolchainFile : public ToolchainFile {
private:
    ToolchainConfig m_toolchain;
    PlatformConfig m_platform;
    CompilerConfig m_compiler;
    LinkerConfig m_linker;
    ArchiverConfig m_archiver;
    BuildSystemConfig m_build_system;

public:
    bool load(const std::string& path) override {
        // Parse toolchain file
        // Implementation would read and parse the file
        return true;
    }

    bool save(const std::string& path) const override {
        // Write toolchain file
        // Implementation would write the configuration
        return true;
    }

    const ToolchainConfig& get_toolchain() const override {
        return m_toolchain;
    }

    const PlatformConfig& get_platform() const override {
        return m_platform;
    }

    const CompilerConfig& get_compiler() const override {
        return m_compiler;
    }

    const LinkerConfig& get_linker() const override {
        return m_linker;
    }

    const ArchiverConfig& get_archiver() const override {
        return m_archiver;
    }

    const BuildSystemConfig& get_build_system() const override {
        return m_build_system;
    }

    void set_toolchain(const ToolchainConfig& config) override {
        m_toolchain = config;
    }

    void set_platform(const PlatformConfig& config) override {
        m_platform = config;
    }

    void set_compiler(const CompilerConfig& config) override {
        m_compiler = config;
    }

    void set_linker(const LinkerConfig& config) override {
        m_linker = config;
    }

    void set_archiver(const ArchiverConfig& config) override {
        m_archiver = config;
    }

    void set_build_system(const BuildSystemConfig& config) override {
        m_build_system = config;
    }

    bool validate() const override {
        return m_toolchain.validate() &&
               m_platform.validate() &&
               m_compiler.validate() &&
               m_linker.validate() &&
               m_archiver.validate() &&
               m_build_system.validate();
    }

    std::string generate_cmake_toolchain() const override {
        std::string cmake_file;

        cmake_file += "# CMake Toolchain File\n";
        cmake_file += "# Generated by OmniCppController\n\n";

        // Toolchain information
        cmake_file += "set(CMAKE_SYSTEM_NAME \"" + m_platform.system_name + "\")\n";
        cmake_file += "set(CMAKE_SYSTEM_VERSION \"" + m_platform.system_version + "\")\n";
        cmake_file += "set(CMAKE_SYSTEM_PROCESSOR \"" + m_platform.processor + "\")\n";
        cmake_file += "set(CMAKE_MACHINE \"" + m_platform.architecture + "\")\n\n";

        // Compiler information
        cmake_file += "set(CMAKE_C_COMPILER \"" + m_compiler.executable + "\")\n";
        cmake_file += "set(CMAKE_C_COMPILER_VERSION \"" + m_compiler.version + "\")\n";
        cmake_file += "set(CMAKE_C_COMPILER_ID \"" + m_compiler.id + "\")\n";
        cmake_file += "set(CMAKE_C_COMPILER_TARGET \"" + m_compiler.target + "\")\n";
        cmake_file += "set(CMAKE_CXX_COMPILER \"" + m_compiler.executable + "\")\n";
        cmake_file += "set(CMAKE_CXX_COMPILER_VERSION \"" + m_compiler.version + "\")\n";
        cmake_file += "set(CMAKE_CXX_COMPILER_ID \"" + m_compiler.id + "\")\n";
        cmake_file += "set(CMAKE_CXX_COMPILER_TARGET \"" + m_compiler.target + "\")\n";

        // Compiler flags
        cmake_file += "set(CMAKE_C_FLAGS \"" + join_flags(m_compiler.flags) + "\")\n";
        cmake_file += "set(CMAKE_CXX_FLAGS \"" + join_flags(m_compiler.flags) + "\")\n";

        // Include directories
        cmake_file += "set(CMAKE_C_INCLUDE_PATH \"" + join_paths(m_compiler.include_dirs) + "\")\n";
        cmake_file += "set(CMAKE_CXX_INCLUDE_PATH \"" + join_paths(m_compiler.include_dirs) + "\")\n";

        // Library directories
        cmake_file += "set(CMAKE_LIBRARY_PATH \"" + join_paths(m_compiler.library_dirs) + "\")\n";
        cmake_file += "set(CMAKE_CXX_LIBRARY_PATH \"" + join_paths(m_compiler.library_dirs) + "\")\n";

        // Linker information
        cmake_file += "set(CMAKE_LINKER \"" + m_linker.executable + "\")\n";
        cmake_file += "set(CMAKE_LINKER_VERSION \"" + m_linker.version + "\")\n";
        cmake_file += "set(CMAKE_LINKER_ID \"" + m_linker.id + "\")\n";
        cmake_file += "set(CMAKE_LINKER_FLAGS \"" + join_flags(m_linker.flags) + "\")\n";

        // Libraries
        cmake_file += "set(CMAKE_C_STANDARD_LIBRARIES \"" + join_strings(m_compiler.libraries) + "\")\n";
        cmake_file += "set(CMAKE_CXX_STANDARD_LIBRARIES \"" + join_strings(m_compiler.libraries) + "\")\n";

        // Build system
        cmake_file += "set(CMAKE_BUILD_TOOL \"" + m_build_system.executable + "\")\n";
        cmake_file += "set(CMAKE_BUILD_TOOL_VERSION \"" + m_build_system.version + "\")\n";
        cmake_file += "set(CMAKE_GENERATOR \"" + m_build_system.generator + "\")\n";

        return cmake_file;
    }

    std::string generate_gcc_toolchain() const override {
        std::string toolchain;

        toolchain += "# GCC Toolchain\n";
        toolchain += "set(CMAKE_C_COMPILER gcc)\n";
        toolchain += "set(CMAKE_CXX_COMPILER g++)\n";
        toolchain += "set(CMAKE_C_COMPILER_ID GNU)\n";
        toolchain += "set(CMAKE_CXX_COMPILER_ID GNU)\n";

        return toolchain;
    }

    std::string generate_clang_toolchain() const override {
        std::string toolchain;

        toolchain += "# Clang Toolchain\n";
        toolchain += "set(CMAKE_C_COMPILER clang)\n";
        toolchain += "set(CMAKE_CXX_COMPILER clang++)\n";
        toolchain += "set(CMAKE_C_COMPILER_ID Clang)\n";
        toolchain += "set(CMAKE_CXX_COMPILER_ID Clang)\n";

        return toolchain;
    }

    std::string generate_msvc_toolchain() const override {
        std::string toolchain;

        toolchain += "# MSVC Toolchain\n";
        toolchain += "set(CMAKE_C_COMPILER cl)\n";
        toolchain += "set(CMAKE_CXX_COMPILER cl)\n";
        toolchain += "set(CMAKE_C_COMPILER_ID MSVC)\n";
        toolchain += "set(CMAKE_CXX_COMPILER_ID MSVC)\n";

        return toolchain;
    }

    std::string generate_mingw_toolchain() const override {
        std::string toolchain;

        toolchain += "# MinGW Toolchain\n";
        toolchain += "set(CMAKE_C_COMPILER gcc)\n";
        toolchain += "set(CMAKE_CXX_COMPILER g++)\n";
        toolchain += "set(CMAKE_C_COMPILER_ID GNU)\n";
        toolchain += "set(CMAKE_CXX_COMPILER_ID GNU)\n";

        return toolchain;
    }

private:
    static std::string join_flags(const std::vector<std::string>& flags) {
        std::string result;
        for (const auto& flag : flags) {
            if (!result.empty()) {
                result += " ";
            }
            result += flag;
        }
        return result;
    }

    static std::string join_paths(const std::vector<std::string>& paths) {
        std::string result;
        for (const auto& path : paths) {
            if (!result.empty()) {
                result += ";";
            }
            result += path;
        }
        return result;
    }

    static std::string join_strings(const std::vector<std::string>& strings) {
        std::string result;
        for (const auto& str : strings) {
            if (!result.empty()) {
                result += ";";
            }
            result += str;
        }
        return result;
    }
};

} // namespace toolchain
} // namespace omnicpp

#endif // OMNICPP_TOOLCHAIN_FILE_H
```

## Dependencies

### Internal Dependencies
- `DES-011` - Toolchain configuration schema

### External Dependencies
- `string` - String handling
- `map` - Map container
- `vector` - Dynamic array
- `optional` - Optional values

## Related Requirements
- REQ-025: Toolchain File Organization

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Toolchain File Format
1. Use CMake set() commands
2. Set system information
3. Set compiler information
4. Set linker information
5. Set build system information
6. Support cross-compilation

### Cross-Compilation Support
1. Set target triplet
2. Set sysroot
3. Set toolchain prefix
4. Configure include and library paths

### Toolchain Detection
1. Detect compiler executable
2. Detect compiler version
3. Detect compiler target
4. Detect compiler capabilities

### Error Handling
- Validate configuration before use
- Provide clear error messages
- Handle missing tools gracefully

## Usage Example

```cpp
#include "toolchain_file.hpp"

using namespace omnicpp::toolchain;

int main() {
    // Create toolchain file
    DefaultToolchainFile toolchain;

    // Configure toolchain
    PlatformConfig platform;
    platform.system_name = "Linux";
    platform.system_version = "5.15.0";
    platform.processor = "x86_64";
    platform.architecture = "x86_64";

    CompilerConfig compiler;
    compiler.id = "GNU";
    compiler.executable = "/usr/bin/gcc";
    compiler.version = "11.0.0";
    compiler.language = "C";
    compiler.language_standard = "17";
    compiler.target = "x86_64-linux-gnu";
    compiler.flags = {"-Wall", "-Wextra", "-O3"};
    compiler.include_dirs = {"/usr/include"};
    compiler.library_dirs = {"/usr/lib"};
    compiler.libraries = {"m", "pthread"};

    toolchain.set_platform(platform);
    toolchain.set_compiler(compiler);

    // Generate CMake toolchain file
    std::string cmake_toolchain = toolchain.generate_cmake_toolchain();

    // Save toolchain file
    toolchain.save("toolchain.cmake");

    return 0;
}
```
