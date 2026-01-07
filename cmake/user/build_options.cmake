# Licensed under the Apache License, Version 2.0 (the "License");

# ==============================================================================
# ENTERPRISE-GRADE PROJECT OPTIONS AND BUILD CONFIGURATIONS
# ==============================================================================
# This file provides comprehensive build options, sanitizers, hardening,
# and production-ready configurations for enterprise C++ projects.
#
# Features:
# - Multiple sanitizers (address, undefined, thread, memory)
# - Security hardening with configurable levels
# - Link-time optimization (IPO/LTO)
# - Code coverage analysis
# - Static runtime linking
# - Debug information control
# - Build profiles (development, staging, production)
# - Cross-platform and cross-compiler support
# ==============================================================================

cmake_minimum_required(VERSION 3.14 FATAL_ERROR)
include(CheckCXXCompilerFlag)
include(CheckIPOSupported)
include(${CMAKE_CURRENT_LIST_DIR}/tmplt-architecture.cmake)

# ==============================================================================
# BUILD PROFILES
# ==============================================================================
# Build profiles automatically configure options for different environments
set(BUILD_PROFILE "development" CACHE STRING "Build profile: development, staging, production")
set_property(CACHE BUILD_PROFILE PROPERTY STRINGS development staging production)

# ==============================================================================
# CORE BUILD OPTIONS
# ==============================================================================

# Compiler cache
option(ENABLE_CCACHE "Use ccache compiler cache" ON)

# Build types and optimization
option(ENABLE_IPO "Enable link-time optimization (IPO/LTO)" OFF)
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
option(USE_STATIC_RUNTIME "Link against static runtime libraries" OFF)

# Development and testing
option(ENABLE_COVERAGE "Enable code coverage analysis with gcovr" OFF)
option(ENABLE_TESTS "Build and run unit tests with Catch2" ON)

# Security and hardening
option(ENABLE_HARDENING "Enable security hardening" OFF)
set(HARDENING_LEVEL "standard" CACHE STRING "Hardening level: minimal, standard, maximum")
set_property(CACHE HARDENING_LEVEL PROPERTY STRINGS minimal standard maximum)

# Sanitizers (mutually exclusive where noted)
option(SANITIZE_ADDRESS "Enable address sanitizer" OFF)
option(SANITIZE_UNDEFINED "Enable undefined behavior sanitizer" OFF)
option(SANITIZE_THREAD "Enable thread sanitizer (incompatible with address sanitizer)" OFF)
option(SANITIZE_MEMORY "Enable memory sanitizer (incompatible with address/thread sanitizers)" OFF)

# Additional security options
option(ENABLE_STACK_PROTECTOR "Enable stack protector" ON)
option(ENABLE_FORTIFY_SOURCE "Enable fortify source" ON)
option(ENABLE_PIE "Enable position independent executable" ON)

# Architecture-specific optimizations
option(ENABLE_ARCH_OPTIMIZATIONS "Enable architecture-specific optimizations" OFF)
option(ENABLE_AVX512 "Enable AVX-512 instructions (x86_64)" OFF)
option(ENABLE_SVE "Enable SVE instructions (ARM64)" OFF)
option(ENABLE_CRYPTO "Enable crypto extensions (ARM64)" OFF)
option(ENABLE_FAST_MATH "Enable fast math optimizations" OFF)

# ==============================================================================
# PROFILE-BASED DEFAULTS
# ==============================================================================
if(BUILD_PROFILE STREQUAL "development")
    # Development: Enable debugging, some sanitizers, coverage
    set(ENABLE_COVERAGE ON CACHE BOOL "Enable coverage for development" FORCE)
    set(SANITIZE_ADDRESS ON CACHE BOOL "Enable address sanitizer for development" FORCE)
    set(ENABLE_HARDENING OFF CACHE BOOL "Disable hardening for faster development builds" FORCE)

elseif(BUILD_PROFILE STREQUAL "staging")
    # Staging: Balanced security and performance
    set(ENABLE_HARDENING ON CACHE BOOL "Enable hardening for staging" FORCE)
    set(HARDENING_LEVEL "standard" CACHE STRING "Standard hardening for staging" FORCE)
    set(SANITIZE_UNDEFINED ON CACHE BOOL "Enable undefined sanitizer for staging" FORCE)

elseif(BUILD_PROFILE STREQUAL "production")
    # Production: Maximum security and optimization
    set(ENABLE_IPO ON CACHE BOOL "Enable IPO for production performance" FORCE)
    set(ENABLE_HARDENING ON CACHE BOOL "Enable hardening for production security" FORCE)
    set(HARDENING_LEVEL "maximum" CACHE STRING "Maximum hardening for production" FORCE)
    set(USE_STATIC_RUNTIME ON CACHE BOOL "Static runtime for production deployment" FORCE)
    set(ENABLE_PIE ON CACHE BOOL "PIE for production security" FORCE)
endif()

# ==============================================================================
# CCACHE SETUP
# ==============================================================================
if(ENABLE_CCACHE)
    find_program(CCACHE_PROGRAM ccache)
    if(CCACHE_PROGRAM)
        set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
        set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM})
        message(STATUS "Using ccache: ${CCACHE_PROGRAM}")
    else()
        message(WARNING "ccache not found, compilation may be slower")
    endif()
endif()

# ==============================================================================
# COMPILER DIAGNOSTICS
# ==============================================================================
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    add_compile_options(-fdiagnostics-color=always)
endif()

# ==============================================================================
# SANITIZER FUNCTIONS
# ==============================================================================

function(apply_address_sanitizer TARGET_NAME)
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(WARNING "Address sanitizer not supported on ${CMAKE_CXX_COMPILER_ID}")
        return()
    endif()

    target_compile_options(${TARGET_NAME} PRIVATE -fsanitize=address -fno-omit-frame-pointer)
    if(NOT APPLE)
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=address -static-libasan)
    else()
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=address)
    endif()

    set(ENV{ASAN_OPTIONS} "detect_leaks=1:strict_string_checks=1:verbosity=1:log_threads=1")
    message(STATUS "Applied address sanitizer to ${TARGET_NAME}")
endfunction()

function(apply_undefined_sanitizer TARGET_NAME)
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(WARNING "Undefined behavior sanitizer not supported on ${CMAKE_CXX_COMPILER_ID}")
        return()
    endif()

    target_compile_options(${TARGET_NAME} PRIVATE -fsanitize=undefined)
    if(NOT APPLE)
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=undefined -static-libubsan)
    else()
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=undefined)
    endif()

    message(STATUS "Applied undefined behavior sanitizer to ${TARGET_NAME}")
endfunction()

function(apply_thread_sanitizer TARGET_NAME)
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(WARNING "Thread sanitizer not supported on ${CMAKE_CXX_COMPILER_ID}")
        return()
    endif()

    target_compile_options(${TARGET_NAME} PRIVATE -fsanitize=thread)
    if(NOT APPLE)
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=thread -static-libtsan)
    else()
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=thread)
    endif()

    message(STATUS "Applied thread sanitizer to ${TARGET_NAME}")
endfunction()

function(apply_memory_sanitizer TARGET_NAME)
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(WARNING "Memory sanitizer not supported on ${CMAKE_CXX_COMPILER_ID}")
        return()
    endif()

    target_compile_options(${TARGET_NAME} PRIVATE -fsanitize=memory)
    if(NOT APPLE)
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=memory -static-libmsan)
    else()
        target_link_options(${TARGET_NAME} PRIVATE -fsanitize=memory)
    endif()

    message(STATUS "Applied memory sanitizer to ${TARGET_NAME}")
endfunction()

function(apply_sanitizers TARGET_NAME)
    message(STATUS "Applying sanitizers to ${TARGET_NAME}")

    if(SANITIZE_ADDRESS)
        apply_address_sanitizer(${TARGET_NAME})
    endif()

    if(SANITIZE_UNDEFINED)
        apply_undefined_sanitizer(${TARGET_NAME})
    endif()

    if(SANITIZE_THREAD)
        if(SANITIZE_ADDRESS)
            message(FATAL_ERROR "Thread sanitizer is incompatible with address sanitizer")
        endif()
        apply_thread_sanitizer(${TARGET_NAME})
    endif()

    if(SANITIZE_MEMORY)
        if(SANITIZE_ADDRESS OR SANITIZE_THREAD)
            message(FATAL_ERROR "Memory sanitizer is incompatible with address or thread sanitizers")
        endif()
        apply_memory_sanitizer(${TARGET_NAME})
    endif()
endfunction()

# ==============================================================================
# HARDENING FUNCTIONS
# ==============================================================================

function(apply_hardening TARGET_NAME)
    if(NOT ENABLE_HARDENING)
        return()
    endif()

    message(STATUS "Applying ${HARDENING_LEVEL} hardening to ${TARGET_NAME}")

    if(MSVC)
        # MSVC hardening flags
        set(MSVC_HARDENING_FLAGS /GS /DYNAMICBASE /NXCOMPAT /CETCOMPAT)

        if(HARDENING_LEVEL STREQUAL "standard" OR HARDENING_LEVEL STREQUAL "maximum")
            list(APPEND MSVC_HARDENING_FLAGS /HIGHENTROPYVA /DYNAMICBASE /NXCOMPAT /GUARD:CF)
        endif()

        if(HARDENING_LEVEL STREQUAL "maximum")
            list(APPEND MSVC_HARDENING_FLAGS /SDL)
        endif()

        target_compile_options(${TARGET_NAME} PRIVATE ${MSVC_HARDENING_FLAGS})
        target_link_options(${TARGET_NAME} PRIVATE /HIGHENTROPYVA /DYNAMICBASE /NXCOMPAT /GUARD:CF)

    else()
        # GCC/Clang hardening flags
        set(HARDENING_COMPILE_FLAGS)

        # Basic hardening
        if(ENABLE_STACK_PROTECTOR)
            list(APPEND HARDENING_COMPILE_FLAGS -fstack-protector-strong)
        endif()

        if(ENABLE_FORTIFY_SOURCE)
            list(APPEND HARDENING_COMPILE_FLAGS -D_FORTIFY_SOURCE=2)
        endif()

        if(ENABLE_PIE)
            list(APPEND HARDENING_COMPILE_FLAGS -fPIE)
        endif()

        # Platform-specific flags
        if(NOT APPLE)
            list(APPEND HARDENING_COMPILE_FLAGS -fstack-clash-protection -fcf-protection -fno-common)
        endif()

        # Level-specific flags
        if(HARDENING_LEVEL STREQUAL "standard" OR HARDENING_LEVEL STREQUAL "maximum")
            if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT APPLE)
                list(APPEND HARDENING_COMPILE_FLAGS -fsanitize=safe-stack -fsanitize=cfi)
            endif()
        endif()

        if(HARDENING_LEVEL STREQUAL "maximum")
            if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT APPLE)
                list(APPEND HARDENING_COMPILE_FLAGS -fsanitize=cfi -fvisibility=hidden)
            endif()
        endif()

        target_compile_options(${TARGET_NAME} PRIVATE ${HARDENING_COMPILE_FLAGS})

        # Linker flags
        if(NOT APPLE AND NOT CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
            target_link_options(${TARGET_NAME} PRIVATE
                -Wl,-z,relro
                -Wl,-z,now
                -Wl,-z,noexecstack
                -Wl,-z,separate-code
            )
        endif()
    endif()
endfunction()

# ==============================================================================
# IPO/LTO FUNCTION
# ==============================================================================

function(apply_ipo TARGET_NAME)
    if(NOT ENABLE_IPO)
        return()
    endif()

    check_ipo_supported(RESULT ipo_supported OUTPUT error_message)

    if(ipo_supported)
        message(STATUS "Enabling IPO/LTO for ${TARGET_NAME}")
        set_property(TARGET ${TARGET_NAME} PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    else()
        message(WARNING "IPO/LTO not supported: ${error_message}")
    endif()
endfunction()

# ==============================================================================
# STATIC RUNTIME FUNCTION
# ==============================================================================

function(apply_static_runtime TARGET_NAME)
    if(NOT USE_STATIC_RUNTIME)
        return()
    endif()

    message(STATUS "Applying static runtime to ${TARGET_NAME}")

    if(MSVC)
        set_property(TARGET ${TARGET_NAME} PROPERTY MSVC_RUNTIME_LIBRARY
            "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    else()
        if(WIN32)
            target_link_options(${TARGET_NAME} PRIVATE -static)
        elseif(APPLE)
            target_link_options(${TARGET_NAME} PRIVATE -static-libstdc++ -Wl,-dead_strip)
        else()
            if(CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
                message(STATUS "Emscripten detected - skipping static runtime flags")
            else()
                target_link_options(${TARGET_NAME} PRIVATE -static-libgcc -static-libstdc++ -Wl,--as-needed)
            endif()
        endif()
    endif()

    # Prefer static libraries for executables
    get_target_property(TARGET_TYPE ${TARGET_NAME} TYPE)
    if(TARGET_TYPE STREQUAL "EXECUTABLE")
        set_target_properties(${TARGET_NAME} PROPERTIES
            LINK_SEARCH_START_STATIC ON
            LINK_SEARCH_END_STATIC ON)
    endif()
endfunction()

# ==============================================================================
# DEBUG INFO CONTROL FUNCTION
# ==============================================================================

function(apply_debug_info_control TARGET_NAME)
    # Keep debug info for Debug and RelWithDebInfo
    if(CMAKE_BUILD_TYPE STREQUAL "Debug" OR CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
        message(STATUS "${CMAKE_BUILD_TYPE} build - keeping debug info for ${TARGET_NAME}")
        if(CMAKE_BUILD_TYPE STREQUAL "Debug")
            target_compile_definitions(${TARGET_NAME} PRIVATE DEBUG)
        endif()
        return()
    endif()

    # Strip debug info for Release and MinSizeRel
    if(CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
        message(STATUS "${CMAKE_BUILD_TYPE} build - stripping debug info for ${TARGET_NAME}")
    else()
        return()
    endif()

    get_target_property(TARGET_TYPE ${TARGET_NAME} TYPE)

    if(MSVC)
        target_compile_options(${TARGET_NAME} PRIVATE /DNDEBUG)
        target_link_options(${TARGET_NAME} PRIVATE /DEBUG:NONE)
    else()
        target_compile_options(${TARGET_NAME} PRIVATE -DNDEBUG -g0)

        if(TARGET_TYPE STREQUAL "EXECUTABLE" AND NOT CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
            if(CMAKE_STRIP)
                set(STRIP_PROGRAM ${CMAKE_STRIP})
            elseif(DEFINED ENV{STRIP})
                set(STRIP_PROGRAM $ENV{STRIP})
            else()
                find_program(STRIP_PROGRAM NAMES strip)
            endif()

            if(STRIP_PROGRAM)
                if(APPLE)
                    add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
                        COMMAND ${STRIP_PROGRAM} -x $<TARGET_FILE:${TARGET_NAME}>
                        COMMENT "Stripping debug symbols from ${TARGET_NAME}")
                else()
                    add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
                        COMMAND ${STRIP_PROGRAM} --strip-all $<TARGET_FILE:${TARGET_NAME}>
                        COMMENT "Stripping debug symbols from ${TARGET_NAME}")
                endif()
            endif()
        endif()

        if(TARGET_TYPE STREQUAL "STATIC_LIBRARY")
            if(CMAKE_RANLIB)
                add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
                    COMMAND ${CMAKE_RANLIB} $<TARGET_FILE:${TARGET_NAME}>
                    COMMENT "Creating symbol index for ${TARGET_NAME}")
            endif()
        endif()
    endif()

    target_compile_definitions(${TARGET_NAME} PRIVATE NDEBUG)
endfunction()

# ==============================================================================
# COVERAGE FUNCTION
# ==============================================================================

function(apply_coverage_settings TARGET_NAME)
    if(NOT ENABLE_COVERAGE)
        return()
    endif()

    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(WARNING "Code coverage requires GCC or Clang")
        return()
    endif()

    set(COVERAGE_FLAGS --coverage -O0 -g -fprofile-arcs -ftest-coverage)

    target_compile_options(${TARGET_NAME} PRIVATE ${COVERAGE_FLAGS})
    target_link_options(${TARGET_NAME} PRIVATE --coverage)

    message(STATUS "Applied coverage settings to ${TARGET_NAME}")
endfunction()

# Setup coverage targets if enabled
if(ENABLE_COVERAGE)
    find_program(GCOVR_PATH gcovr)
    if(GCOVR_PATH)
        message(STATUS "Found gcovr: ${GCOVR_PATH}")

        # Coverage targets
        if(NOT TARGET coverage-html)
            add_custom_target(coverage-html
                COMMAND ${GCOVR_PATH} -r ${CMAKE_SOURCE_DIR}
                    --html --html-details -o ${CMAKE_BINARY_DIR}/coverage.html
                    --exclude '${CMAKE_BINARY_DIR}/.*'
                    --exclude '.*/tests/.*' --exclude '.*/test/.*'
                    --exclude '.*/external/.*' --exclude '.*/third_party/.*'
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                COMMENT "Generating HTML coverage report"
                VERBATIM)
        endif()

        if(NOT TARGET coverage-xml)
            add_custom_target(coverage-xml
                COMMAND ${GCOVR_PATH} -r ${CMAKE_SOURCE_DIR}
                    --xml -o ${CMAKE_BINARY_DIR}/coverage.xml
                    --exclude '${CMAKE_BINARY_DIR}/.*'
                    --exclude '.*/tests/.*' --exclude '.*/test/.*'
                    --exclude '.*/external/.*' --exclude '.*/third_party/.*'
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                COMMENT "Generating XML coverage report"
                VERBATIM)
        endif()

        if(NOT TARGET coverage)
            add_custom_target(coverage DEPENDS coverage-html coverage-xml)
        endif()

        if(NOT TARGET coverage-summary)
            add_custom_target(coverage-summary
                COMMAND ${GCOVR_PATH} -r ${CMAKE_SOURCE_DIR}
                    --exclude '${CMAKE_BINARY_DIR}/.*'
                    --exclude '.*/tests/.*' --exclude '.*/test/.*'
                    --exclude '.*/external/.*' --exclude '.*/third_party/.*'
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                COMMENT "Displaying coverage summary"
                VERBATIM)
        endif()

    else()
        message(WARNING "gcovr not found - install with: pip install gcovr")
    endif()
endif()

# ==============================================================================
# MASTER APPLY FUNCTION
# ==============================================================================

function(apply_common_target_settings TARGET_NAME)
    message(STATUS "Applying common settings to ${TARGET_NAME}")

    apply_ipo(${TARGET_NAME})
    apply_hardening(${TARGET_NAME})
    apply_sanitizers(${TARGET_NAME})
    apply_static_runtime(${TARGET_NAME})
    apply_debug_info_control(${TARGET_NAME})
    apply_coverage_settings(${TARGET_NAME})
    apply_architecture_optimizations(${TARGET_NAME})
endfunction()

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

function(gather_sources OUTPUT_VAR SOURCE_DIR)
    file(GLOB_RECURSE sources
        CONFIGURE_DEPENDS
        ${SOURCE_DIR}/*.h ${SOURCE_DIR}/*.hpp ${SOURCE_DIR}/*.hh ${SOURCE_DIR}/*.hxx
        ${SOURCE_DIR}/*.c ${SOURCE_DIR}/*.cpp ${SOURCE_DIR}/*.cc ${SOURCE_DIR}/*.cxx)
    set(${OUTPUT_VAR} ${sources} PARENT_SCOPE)
endfunction()

# ==============================================================================
# VALIDATION
# ==============================================================================

# Validate sanitizer combinations
if(SANITIZE_THREAD AND SANITIZE_ADDRESS)
    message(FATAL_ERROR "Thread and address sanitizers are mutually exclusive")
endif()

if(SANITIZE_MEMORY AND (SANITIZE_ADDRESS OR SANITIZE_THREAD))
    message(FATAL_ERROR "Memory sanitizer is incompatible with address or thread sanitizers")
endif()

# Warn about hardening with sanitizers
if(ENABLE_HARDENING AND (SANITIZE_ADDRESS OR SANITIZE_UNDEFINED OR SANITIZE_THREAD OR SANITIZE_MEMORY))
    message(WARNING "Hardening and sanitizers may conflict - test thoroughly")
endif()

message(STATUS "Build profile: ${BUILD_PROFILE}")
message(STATUS "Hardening level: ${HARDENING_LEVEL}")