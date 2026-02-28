# ============================================================================
# OmniCpp Template - Common Project Configuration
# ============================================================================
# Common configuration shared across all project targets

# ============================================================================
# Dependencies
# ============================================================================

# zlib (Compression Library)
find_package(ZLIB QUIET)
# if(NOT ZLIB_FOUND)
    CPMAddPackage(
        NAME zlib
        GITHUB_REPOSITORY madler/zlib
        GIT_TAG v1.3
    )
endif()

# fmt (Format String Library)
find_package(fmt QUIET)
# if(NOT fmt_FOUND)
    CPMAddPackage(
        NAME fmt
        GITHUB_REPOSITORY fmtlib/fmt
        GIT_TAG 9.1.0
    )
endif()

# Quill (Logging Library)
find_package(quill QUIET)
# if(NOT quill_FOUND)
    CPMAddPackage("gh:odygrd/quill@8.2.0")
endif()

# Catch2 (Testing Framework)
find_package(Catch2 QUIET)
# if(NOT Catch2_FOUND)
    CPMAddPackage(
        NAME Catch2
        GITHUB_REPOSITORY catchorg/Catch2
        GIT_TAG 3.7.1
    )
endif()

# GTest (Testing Framework)
find_package(GTest QUIET)
# if(NOT GTest_FOUND)
    CPMAddPackage(
        NAME GTest
        GITHUB_REPOSITORY google/googletest
        GIT_TAG 1.15.0
    )
endif()

# nlohmann_json (JSON Library)
find_package(nlohmann_json QUIET)
# if(NOT nlohmann_json_FOUND)
    CPMAddPackage(
        NAME nlohmann_json
        URL https://github.com/nlohmann/json/archive/refs/tags/v3.13.0.tar.gz
        VERSION 3.13.0
        FORCE
        EXCLUDE_FROM_ALL
    )
endif()

# PostgreSQL (Database)
find_package(PostgreSQL QUIET)
# if(NOT PostgreSQL_FOUND)
    CPMAddPackage(
        NAME PostgreSQL
        GITHUB_REPOSITORY postgresql/postgresql
        GIT_TAG 15.4
    )
endif()

# ============================================================================
# Helper function for applying common target settings
# ============================================================================

function(apply_common_target_settings TARGET_NAME)
    apply_ipo(${TARGET_NAME})
    apply_hardening(${TARGET_NAME})
    apply_sanitizers(${TARGET_NAME})
    apply_static_runtime(${TARGET_NAME})
    apply_debug_info_control(${TARGET_NAME})
    apply_coverage_settings(${TARGET_NAME})
endfunction()

# ============================================================================
# Helper function for creating source file lists
# ============================================================================

function(gather_sources OUTPUT_VAR SOURCE_DIR)
    file(
        GLOB_RECURSE
        sources
        CONFIGURE_DEPENDS
        ${SOURCE_DIR}/*.h
    )
endfunction()
