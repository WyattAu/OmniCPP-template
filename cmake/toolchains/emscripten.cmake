# Emscripten WebAssembly Toolchain
# Licensed under the Apache License, Version 2.0 (the "License");

# Set the system name
set(CMAKE_SYSTEM_NAME Emscripten)
set(CMAKE_SYSTEM_PROCESSOR wasm32)

# Specify Emscripten compilers (these should be in PATH)
set(CMAKE_C_COMPILER emcc)
set(CMAKE_CXX_COMPILER em++)
set(CMAKE_AR emar)
set(CMAKE_RANLIB emranlib)

# Find Emscripten root
if(NOT DEFINED ENV{EMSDK})
    message(FATAL_ERROR "EMSDK environment variable not set. Please source emsdk_env.sh")
endif()

# Set Emscripten-specific flags
set(CMAKE_C_FLAGS_INIT "-s USE_PTHREADS=1 -s WASM=1")
set(CMAKE_CXX_FLAGS_INIT "-s USE_PTHREADS=1 -s WASM=1")

# Default optimization flags for Emscripten
set(CMAKE_C_FLAGS_RELEASE_INIT "-O3 -s WASM=1")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "-O3 -s WASM=1")

# Linker flags for WebAssembly
set(CMAKE_EXE_LINKER_FLAGS_INIT "-s WASM=1 -s ALLOW_MEMORY_GROWTH=1 -s MODULARIZE=1 -s EXPORT_ES6=1")

# Disable certain CMake features that don't work with Emscripten
set(CMAKE_CROSSCOMPILING_EMULATOR "")

# Set the target environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Emscripten-specific definitions
add_compile_definitions(__EMSCRIPTEN__)

message(STATUS "Emscripten WebAssembly toolchain loaded")