# Licensed under the Apache License, Version 2.0 (the "License");

# ==============================================================================
# Enterprise-grade CPM Dependency Management
# ==============================================================================
#
# This module provides enhanced dependency management functions that build upon
# CPM.cmake with enterprise-grade features including:
# - Comprehensive error handling and validation
# - Detailed logging and status reporting
# - Version compatibility checking
# - Fallback mechanisms for dependency resolution
# - Dependency health monitoring
# - Integration with package lock files
#
# Usage:
#   include(dependencies.cmake)
#
#   cpm_add_enterprise_dependency(
#       NAME MyLib
#       GITHUB_REPOSITORY myorg/mylib
#       VERSION 1.2.3
#       [OPTIONS "MYLIB_BUILD_TESTS OFF"]
#       [REQUIRED]  # Makes failure fatal
#       [QUIET]     # Suppresses verbose logging
#   )

include_guard(GLOBAL)

# ==============================================================================
# Configuration Options
# ==============================================================================

# Enable detailed dependency logging
option(CPM_DEPS_ENABLE_VERBOSE_LOGGING "Enable verbose dependency management logging" ON)

# Treat dependency failures as fatal by default
option(CPM_DEPS_FAIL_ON_MISSING "Fail CMake configuration if dependencies cannot be resolved" ON)

# Enable dependency health checks
option(CPM_DEPS_ENABLE_HEALTH_CHECKS "Enable dependency health validation" ON)

# ==============================================================================
# Internal Variables
# ==============================================================================

# Track dependency resolution statistics
set(CPM_DEPS_TOTAL_COUNT 0 CACHE INTERNAL "Total number of dependencies processed")
set(CPM_DEPS_SUCCESS_COUNT 0 CACHE INTERNAL "Number of successfully resolved dependencies")
set(CPM_DEPS_FAILED_COUNT 0 CACHE INTERNAL "Number of failed dependency resolutions")
set(CPM_DEPS_SKIPPED_COUNT 0 CACHE INTERNAL "Number of skipped dependencies")

# Track dependency metadata
set(CPM_DEPS_RESOLVED_PACKAGES "" CACHE INTERNAL "List of successfully resolved packages")
set(CPM_DEPS_FAILED_PACKAGES "" CACHE INTERNAL "List of failed packages")

# ==============================================================================
# Logging Functions
# ==============================================================================

function(cpm_deps_log LEVEL MESSAGE)
    if(CPM_DEPS_ENABLE_VERBOSE_LOGGING OR LEVEL STREQUAL "ERROR" OR LEVEL STREQUAL "WARNING")
        if(LEVEL STREQUAL "ERROR")
            message(STATUS "[CPM-DEPS ERROR] ${MESSAGE}")
        elseif(LEVEL STREQUAL "WARNING")
            message(STATUS "[CPM-DEPS WARN]  ${MESSAGE}")
        elseif(LEVEL STREQUAL "INFO")
            message(STATUS "[CPM-DEPS INFO]  ${MESSAGE}")
        elseif(LEVEL STREQUAL "DEBUG")
            if(CPM_DEPS_ENABLE_VERBOSE_LOGGING)
                message(STATUS "[CPM-DEPS DEBUG] ${MESSAGE}")
            endif()
        endif()
    endif()
endfunction()

# ==============================================================================
# Version Validation Functions
# ==============================================================================

function(cpm_deps_validate_version VERSION RESULT_VAR)
    # Basic version format validation (semver-like)
    if(VERSION MATCHES "^[0-9]+\\.[0-9]+\\.[0-9]+.*$")
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    elseif(VERSION MATCHES "^[0-9]+\\.[0-9]+.*$")
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    elseif(VERSION MATCHES "^v[0-9]+\\.[0-9]+.*$")
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    elseif(VERSION MATCHES "^[a-f0-9]{7,40}$")
        # Git commit hash
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    elseif(VERSION MATCHES "^#.*$")
        # Git branch/tag reference
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    else()
        set(${RESULT_VAR} FALSE PARENT_SCOPE)
    endif()
endfunction()

function(cpm_deps_check_version_compatibility PACKAGE_NAME EXPECTED_VERSION ACTUAL_VERSION RESULT_VAR)
    # For now, just check if versions are different and warn
    # In a more advanced implementation, this could check semver compatibility
    if(NOT EXPECTED_VERSION STREQUAL ACTUAL_VERSION)
        cpm_deps_log(WARNING "${PACKAGE_NAME}: Version mismatch - expected ${EXPECTED_VERSION}, got ${ACTUAL_VERSION}")
        set(${RESULT_VAR} FALSE PARENT_SCOPE)
    else()
        set(${RESULT_VAR} TRUE PARENT_SCOPE)
    endif()
endfunction()

# ==============================================================================
# Dependency Health Check Functions
# ==============================================================================

function(cpm_deps_perform_health_check PACKAGE_NAME)
    if(NOT CPM_DEPS_ENABLE_HEALTH_CHECKS)
        return()
    endif()

    # Check if package was actually added
    if(NOT ${PACKAGE_NAME}_ADDED)
        cpm_deps_log(WARNING "${PACKAGE_NAME}: Health check failed - package not marked as added")
        return()
    endif()

    # Check if source directory exists
    if(DEFINED ${PACKAGE_NAME}_SOURCE_DIR AND EXISTS "${${PACKAGE_NAME}_SOURCE_DIR}")
        cpm_deps_log(DEBUG "${PACKAGE_NAME}: Source directory exists at ${${PACKAGE_NAME}_SOURCE_DIR}")
    else()
        cpm_deps_log(WARNING "${PACKAGE_NAME}: Health check warning - source directory not found")
    endif()

    # Additional health checks could be added here
    # - Check for expected CMake targets
    # - Validate library files exist
    # - Check include directories
endfunction()

# ==============================================================================
# Main Enterprise Dependency Function
# ==============================================================================

function(cpm_add_enterprise_dependency)
    # Parse arguments
    set(options REQUIRED QUIET FORCE)
    set(oneValueArgs NAME VERSION GITHUB_REPOSITORY GIT_TAG URL)
    set(multiValueArgs OPTIONS DEPENDS FIND_PACKAGE_ARGUMENTS)
    cmake_parse_arguments(CPM_DEP "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    # Validate required arguments
    if(NOT CPM_DEP_NAME)
        cpm_deps_log(ERROR "NAME is required for dependency declaration")
        if(CPM_DEPS_FAIL_ON_MISSING)
            message(FATAL_ERROR "Missing required NAME parameter in cpm_add_enterprise_dependency")
        endif()
        return()
    endif()

    # Increment total count
    math(EXPR CPM_DEPS_TOTAL_COUNT "${CPM_DEPS_TOTAL_COUNT} + 1")
    set(CPM_DEPS_TOTAL_COUNT ${CPM_DEPS_TOTAL_COUNT} CACHE INTERNAL "Total number of dependencies processed")

    # Check if already processed
    if(${CPM_DEP_NAME} IN_LIST CPM_DEPS_RESOLVED_PACKAGES)
        cpm_deps_log(DEBUG "${CPM_DEP_NAME}: Already resolved, skipping")
        math(EXPR CPM_DEPS_SKIPPED_COUNT "${CPM_DEPS_SKIPPED_COUNT} + 1")
        set(CPM_DEPS_SKIPPED_COUNT ${CPM_DEPS_SKIPPED_COUNT} CACHE INTERNAL "Number of skipped dependencies")
        return()
    endif()

    if(${CPM_DEP_NAME} IN_LIST CPM_DEPS_FAILED_PACKAGES)
        cpm_deps_log(DEBUG "${CPM_DEP_NAME}: Previously failed, skipping")
        math(EXPR CPM_DEPS_SKIPPED_COUNT "${CPM_DEPS_SKIPPED_COUNT} + 1")
        set(CPM_DEPS_SKIPPED_COUNT ${CPM_DEPS_SKIPPED_COUNT} CACHE INTERNAL "Number of skipped dependencies")
        return()
    endif()

    # Validate version if provided
    if(CPM_DEP_VERSION)
        cpm_deps_validate_version(${CPM_DEP_VERSION} VERSION_VALID)
        if(NOT VERSION_VALID)
            cpm_deps_log(WARNING "${CPM_DEP_NAME}: Invalid version format '${CPM_DEP_VERSION}'")
        endif()
    endif()

    # Prepare CPMAddPackage arguments
    set(CPM_ARGS "NAME;${CPM_DEP_NAME}")

    if(CPM_DEP_GITHUB_REPOSITORY)
        list(APPEND CPM_ARGS "GITHUB_REPOSITORY;${CPM_DEP_GITHUB_REPOSITORY}")
    endif()

    if(CPM_DEP_VERSION)
        list(APPEND CPM_ARGS "VERSION;${CPM_DEP_VERSION}")
    elseif(CPM_DEP_GIT_TAG)
        list(APPEND CPM_ARGS "GIT_TAG;${CPM_DEP_GIT_TAG}")
    endif()

    if(CPM_DEP_URL)
        list(APPEND CPM_ARGS "URL;${CPM_DEP_URL}")
    endif()

    if(CPM_DEP_OPTIONS)
        list(APPEND CPM_ARGS "OPTIONS;${CPM_DEP_OPTIONS}")
    endif()

    if(CPM_DEP_DEPENDS)
        list(APPEND CPM_ARGS "DEPENDS;${CPM_DEP_DEPENDS}")
    endif()

    # Log dependency resolution attempt
    if(NOT CPM_DEP_QUIET)
        if(CPM_DEP_VERSION)
            cpm_deps_log(INFO "Resolving ${CPM_DEP_NAME}@${CPM_DEP_VERSION}")
        elseif(CPM_DEP_GIT_TAG)
            cpm_deps_log(INFO "Resolving ${CPM_DEP_NAME}@${CPM_DEP_GIT_TAG}")
        else()
            cpm_deps_log(INFO "Resolving ${CPM_DEP_NAME}")
        endif()
    endif()

    # Try to find package locally first (if applicable)
    if(CPM_DEP_FIND_PACKAGE_ARGUMENTS)
        find_package(${CPM_DEP_NAME} ${CPM_DEP_FIND_PACKAGE_ARGUMENTS} QUIET)
        if(${CPM_DEP_NAME}_FOUND)
            cpm_deps_log(DEBUG "${CPM_DEP_NAME}: Found via find_package")
            CPMRegisterPackage("${CPM_DEP_NAME}" "${${CPM_DEP_NAME}_VERSION}")
            set(${CPM_DEP_NAME}_ADDED YES)
            set(CPM_PACKAGE_FOUND YES)
        endif()
    endif()

    # Attempt to add via CPM if not found locally
    if(NOT ${CPM_DEP_NAME}_FOUND)
        if(CPM_DEP_FORCE)
            list(APPEND CPM_ARGS "FORCE")
        endif()

        # Call CPMAddPackage
        CPMAddPackage(${CPM_ARGS})
    endif()

    # Check result and perform validation
    if(${CPM_DEP_NAME}_ADDED)
        # Success
        math(EXPR CPM_DEPS_SUCCESS_COUNT "${CPM_DEPS_SUCCESS_COUNT} + 1")
        set(CPM_DEPS_SUCCESS_COUNT ${CPM_DEPS_SUCCESS_COUNT} CACHE INTERNAL "Number of successfully resolved dependencies")

        set(CPM_DEPS_RESOLVED_PACKAGES "${CPM_DEPS_RESOLVED_PACKAGES};${CPM_DEP_NAME}" CACHE INTERNAL "List of successfully resolved packages")

        if(NOT CPM_DEP_QUIET)
            cpm_deps_log(INFO "${CPM_DEP_NAME}: Successfully resolved")
        endif()

        # Perform health check
        cpm_deps_perform_health_check(${CPM_DEP_NAME})

        # Version compatibility check
        if(CPM_DEP_VERSION AND DEFINED ${CPM_DEP_NAME}_VERSION)
            cpm_deps_check_version_compatibility(${CPM_DEP_NAME} ${CPM_DEP_VERSION} ${${CPM_DEP_NAME}_VERSION} VERSION_COMPATIBLE)
        endif()

    else()
        # Failure
        math(EXPR CPM_DEPS_FAILED_COUNT "${CPM_DEPS_FAILED_COUNT} + 1")
        set(CPM_DEPS_FAILED_COUNT ${CPM_DEPS_FAILED_COUNT} CACHE INTERNAL "Number of failed dependency resolutions")

        set(CPM_DEPS_FAILED_PACKAGES "${CPM_DEPS_FAILED_PACKAGES};${CPM_DEP_NAME}" CACHE INTERNAL "List of failed packages")

        cpm_deps_log(ERROR "${CPM_DEP_NAME}: Failed to resolve dependency")

        if(CPM_DEP_REQUIRED OR CPM_DEPS_FAIL_ON_MISSING)
            message(FATAL_ERROR "Required dependency ${CPM_DEP_NAME} could not be resolved. Please check network connectivity, GitHub access, and ensure all build dependencies are installed.")
        else()
            cpm_deps_log(WARNING "${CPM_DEP_NAME}: Dependency resolution failed, but marked as optional")
        endif()
    endif()
endfunction()

# ==============================================================================
# Utility Functions
# ==============================================================================

function(cpm_deps_print_summary)
    message(STATUS "CPM Dependencies Summary:")
    message(STATUS "  Total: ${CPM_DEPS_TOTAL_COUNT}")
    message(STATUS "  Resolved: ${CPM_DEPS_SUCCESS_COUNT}")
    message(STATUS "  Failed: ${CPM_DEPS_FAILED_COUNT}")
    message(STATUS "  Skipped: ${CPM_DEPS_SKIPPED_COUNT}")

    if(CPM_DEPS_FAILED_PACKAGES)
        message(STATUS "Failed packages: ${CPM_DEPS_FAILED_PACKAGES}")
    endif()
endfunction()

function(cpm_deps_require_all_resolved)
    if(CPM_DEPS_FAILED_COUNT GREATER 0)
        cpm_deps_print_summary()
        message(FATAL_ERROR "Some dependencies failed to resolve. See summary above.")
    endif()
endfunction()

# ==============================================================================
# Convenience Macros for Common Patterns
# ==============================================================================

macro(cpm_add_required_dependency)
    cpm_add_enterprise_dependency(${ARGN} REQUIRED)
endmacro()

macro(cpm_add_optional_dependency)
    cpm_add_enterprise_dependency(${ARGN})
endmacro()

# ==============================================================================
# Integration with CPM Package Lock
# ==============================================================================

function(cpm_deps_enable_package_lock FILE_PATH)
    CPMUsePackageLock(${FILE_PATH})
    cpm_deps_log(INFO "Package lock enabled: ${FILE_PATH}")
endfunction()



# ==============================================================================
# Cleanup and Finalization
# ==============================================================================

# Register cleanup function to be called at the end of configuration
function(cpm_deps_finalize)
    cpm_deps_print_summary()

    # Additional cleanup could be performed here
    # - Validate all required dependencies are present
    # - Generate dependency reports
    # - Update package lock files
endfunction()

# Ensure finalization happens at the end of the main CMakeLists.txt
cmake_language(DEFER CALL cpm_deps_finalize)