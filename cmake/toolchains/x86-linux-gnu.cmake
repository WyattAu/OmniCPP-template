# x86 Linux Cross-Compilation Toolchain
# Licensed under the Apache License, Version 2.0 (the "License");

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR i686)

# Specify the cross compiler
set(CMAKE_C_COMPILER i686-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER i686-linux-gnu-g++)

# Specify the sysroot if needed
# set(CMAKE_SYSROOT /path/to/x86/sysroot)

# Specify the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Compiler flags for x86
set(CMAKE_C_FLAGS_INIT "-march=i686 -mtune=generic -m32")
set(CMAKE_CXX_FLAGS_INIT "-march=i686 -mtune=generic -m32")

# Linker flags
set(CMAKE_EXE_LINKER_FLAGS_INIT "-Wl,--as-needed -m32")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "-Wl,--as-needed -m32")

# Enable SSE2 by default for x86
add_compile_definitions(__SSE2__)

message(STATUS "x86 Linux cross-compilation toolchain loaded")