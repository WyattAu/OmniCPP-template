# ARM64 Windows MSVC Cross-Compilation Toolchain
# Licensed under the Apache License, Version 2.0 (the "License");

set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR ARM64)

# Specify the cross compiler (assuming Visual Studio Build Tools with ARM64 support)
set(CMAKE_C_COMPILER cl)
set(CMAKE_CXX_COMPILER cl)

# Set the target architecture
set(CMAKE_C_FLAGS_INIT "/arch:arm64")
set(CMAKE_CXX_FLAGS_INIT "/arch:arm64")

# Specify the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Windows-specific definitions
add_compile_definitions(_WIN32 WIN32 _WINDOWS)

# ARM64-specific definitions
add_compile_definitions(__ARM64__ _ARM64_)

message(STATUS "ARM64 Windows MSVC cross-compilation toolchain loaded")