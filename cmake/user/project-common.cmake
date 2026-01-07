# Licensed under the Apache License, Version 2.0 (the "License");

# ==============================================================================
# Common project settings and options
# ==============================================================================

# CMake policies
cmake_policy(SET CMP0048 NEW)
cmake_policy(SET CMP0076 NEW)
cmake_policy(SET CMP0091 NEW)

# Compiler diagnostics
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    add_compile_options(-fdiagnostics-color=always)
endif()

# ==============================================================================
# Project naming configuration
# Must be compatible with renaming script
# ==============================================================================

# Library names and attributes
set(LIBRARY_NAME TestLib)
string(TOLOWER "${LIBRARY_NAME}" LIBRARY_NAME_LOWER)
set(LIBRARY_NAMESPACE omnicpp)

# Standalone names and attributes
set(STANDALONE_NAME TestApp)
string(TOLOWER "${STANDALONE_NAME}" STANDALONE_NAME_LOWER)
set(STANDALONE_NAMESPACE omnicpp)

# Qt/Vulkan library names and attributes
set(QT_VULKAN_LIBRARY_NAME OmniCppQtVulkanLib)
string(TOLOWER "${QT_VULKAN_LIBRARY_NAME}" QT_VULKAN_LIBRARY_NAME_LOWER)
set(QT_VULKAN_LIBRARY_NAMESPACE omnicpp_qt_vulkan)

# Qt/Vulkan standalone names and attributes
set(QT_VULKAN_STANDALONE_NAME OmniCppQtVulkanStandalone)
string(TOLOWER "${QT_VULKAN_STANDALONE_NAME}" QT_VULKAN_STANDALONE_NAME_LOWER)
set(QT_VULKAN_STANDALONE_NAMESPACE omnicpp_qt_vulkan)

# Test names and attributes
set(TEST_NAME ${LIBRARY_NAME}Tester)
string(TOLOWER "${TEST_NAME}" TEST_NAME_LOWER)
set(TEST_NAMESPACE omnicpp)

# ==============================================================================
# Common build options
# ==============================================================================

option(ENABLE_TESTS "Build and run unit tests with Catch2" OFF)
option(ENABLE_CCACHE "Use ccache compiler cache" ON)
option(BUILD_SHARED_LIBS "Build shared (.so) libraries" OFF)
option(USE_STATIC_RUNTIME "Link C++ runtime statically" OFF)
option(ENABLE_IPO "Enable link-time optimization" OFF)
option(ENABLE_HARDENING "Enable security hardening" OFF)
option(ENABLE_COVERAGE "Enable code coverage analysis" OFF)
option(ENABLE_STATIC_ANALYSIS "Enable Clang-Tidy and Cppcheck during build" OFF)
option(SANITIZE_ADDRESS "Enable address sanitizer" OFF)
option(SANITIZE_UNDEFINED "Enable undefined behavior sanitizer" OFF)
option(SANITIZE_THREAD "Enable thread sanitizer" OFF)
option(SANITIZE_MEMORY "Enable memory sanitizer" OFF)

# ==============================================================================
# ccache setup
# ==============================================================================
if(ENABLE_CCACHE)
    find_program(CCACHE_PROGRAM ccache)
    if(CCACHE_PROGRAM)
        set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
        set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
    endif()
endif()

# ==============================================================================
# Static analysis setup
# ==============================================================================
if(ENABLE_STATIC_ANALYSIS)
    # Find the tools
    find_program(CLANG_TIDY_PATH clang-tidy)
    find_program(CPPCHECK_PATH cppcheck)

    # Configure Clang-Tidy
    if(CLANG_TIDY_PATH)
        # set CXX_CLANG_TIDY property on all targets created after this line
        set(CMAKE_CXX_CLANG_TIDY "${CLANG_TIDY_PATH}")
        message(STATUS "Clang-Tidy enabled: ${CLANG_TIDY_PATH}")
    else()
        message(WARNING "clang-tidy not found")
    endif()

    # Configure Cppcheck
    if(CPPCHECK_PATH)
        # --enable=all: Enable all checks
        # --suppress=missingIncludeSystem: Don't fail if system headers are missing
        set(CMAKE_CXX_CPPCHECK
            "${CPPCHECK_PATH};--enable=all;--suppress=missingIncludeSystem;--error-exitcode=1")
        message(STATUS "Cppcheck enabled: ${CPPCHECK_PATH}")
    else()
        message(WARNING "cppcheck not found")
    endif()
endif()

# ==============================================================================
# Common includes
# ==============================================================================
include(GNUInstallDirs)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-runtime.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-sanitizer.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-hardening.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-ipo.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-debug.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../user/tmplt-coverage.cmake)

# ==============================================================================
# Build system configuration
# ==============================================================================
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_PDB_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# ==============================================================================
# Cross-compilation indicator (global)
# ==============================================================================
set(omnicpp_CROSSCOMPILING OFF)
if(CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
    set(omnicpp_CROSSCOMPILING ON)
elseif(CMAKE_CROSSCOMPILING)
    set(omnicpp_CROSSCOMPILING ON)
elseif(NOT CMAKE_HOST_SYSTEM_NAME STREQUAL CMAKE_SYSTEM_NAME)
    set(omnicpp_CROSSCOMPILING ON)
endif()
set(omnicpp_CROSSCOMPILING
    "${omnicpp_CROSSCOMPILING}"
    CACHE BOOL "Building with cross-compilation")

# Provide preprocessor define
if(omnicpp_CROSSCOMPILING)
    add_compile_definitions(omnicpp_CROSSCOMPILING=1)
else()
    add_compile_definitions(omnicpp_CROSSCOMPILING=0)
endif()

# ==============================================================================
# Common dependency management
# ==============================================================================
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../generated")
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

# Set compiler environment variables for CPM
set(ENV{CC} "${CMAKE_C_COMPILER}")
set(ENV{CXX} "${CMAKE_CXX_COMPILER}")

# CPM.cmake setup
include(${CMAKE_CURRENT_LIST_DIR}/../generated/CPM.cmake)

# Common dependencies - prioritize vcpkg, fallback to CPM
find_package(fmt QUIET)
if(NOT fmt_FOUND)
    CPMAddPackage(
        NAME fmt
        GITHUB_REPOSITORY fmtlib/fmt
        GIT_TAG 9.1.0
    )
endif()

find_package(nlohmann_json QUIET)
if(NOT nlohmann_json_FOUND)
    CPMAddPackage("gh:nlohmann/json@3.12.0")
endif()

# find_package(ZLIB QUIET)
# if(NOT ZLIB_FOUND)
#     CPMAddPackage(
#         NAME zlib
#         GITHUB_REPOSITORY madler/zlib
#         GIT_TAG v1.3
#     )
# endif()

find_package(spdlog QUIET)
if(NOT spdlog_FOUND)
    CPMAddPackage("gh:gabime/spdlog@1.14.1")
endif()

find_package(Catch2 QUIET)
if(NOT Catch2_FOUND)
    CPMAddPackage("gh:catchorg/Catch2@3.7.1")
endif()

find_package(GTest QUIET)
if(NOT GTest_FOUND)
    CPMAddPackage("gh:google/googletest@1.15.0")
endif()

# find_package(PostgreSQL QUIET)
# if(NOT PostgreSQL_FOUND)
#     CPMAddPackage("gh:postgresql/postgresql@15.4")
# endif()

# ==============================================================================
# Helper function for applying common target settings
# ==============================================================================
function(apply_common_target_settings TARGET_NAME)
    apply_ipo(${TARGET_NAME})
    apply_hardening(${TARGET_NAME})
    apply_sanitizers(${TARGET_NAME})
    apply_static_runtime(${TARGET_NAME})
    apply_debug_info_control(${TARGET_NAME})
    apply_coverage_settings(${TARGET_NAME})
endfunction()

# ==============================================================================
# Helper function for creating source file lists
# ==============================================================================
function(gather_sources OUTPUT_VAR SOURCE_DIR)
    file(
        GLOB_RECURSE
        sources
        CONFIGURE_DEPENDS
        ${SOURCE_DIR}/*.h
        ${SOURCE_DIR}/*.hpp
        ${SOURCE_DIR}/*.hh
        ${SOURCE_DIR}/*.hxx
        ${SOURCE_DIR}/*.c
        ${SOURCE_DIR}/*.cpp
        ${SOURCE_DIR}/*.cc
        ${SOURCE_DIR}/*.cxx)
    set(${OUTPUT_VAR}
        ${sources}
        PARENT_SCOPE)
endfunction()

# ==============================================================================
# Documentation setup (only define targets once at root level)
# ==============================================================================

# Find Doxygen
find_package(Doxygen)

# Find Python for MkDocs
find_package(Python3 COMPONENTS Interpreter)
