# ============================================================================
# OmniCpp Template - Examples CMakeLists.txt
# ============================================================================
# Builds example applications
# ============================================================================

cmake_minimum_required(VERSION 3.20)
project(Examples VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Simple Game Example
add_subdirectory(simple_game)

# Pong Game Example (Vulkan rendering)
add_subdirectory(pong)
