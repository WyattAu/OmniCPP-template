# ARM64 Linux Cross-Compilation Toolchain
# Licensed under the Apache License, Version 2.0 (the "License");

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# Specify the cross compiler
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

# Specify the sysroot if needed
# set(CMAKE_SYSROOT /path/to/arm64/sysroot)

# Specify the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Compiler flags for ARM64
set(CMAKE_C_FLAGS_INIT "-march=armv8-a -mtune=cortex-a72")
set(CMAKE_CXX_FLAGS_INIT "-march=armv8-a -mtune=cortex-a72")

# Linker flags
set(CMAKE_EXE_LINKER_FLAGS_INIT "-Wl,--as-needed")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "-Wl,--as-needed")

# Enable NEON by default for ARM64
add_compile_definitions(__ARM_NEON__)

message(STATUS "ARM64 Linux cross-compilation toolchain loaded")