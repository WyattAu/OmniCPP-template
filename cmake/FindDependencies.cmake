# ============================================================================
# OmniCpp Template - Find Dependencies
# ============================================================================
# Resolves all project dependencies using available package managers
# ============================================================================

# ============================================================================
# Core Dependencies
# ============================================================================

# Threads (always required)
find_package(Threads REQUIRED)

# ============================================================================
# Optional Dependencies
# ============================================================================

# spdlog - Logging library
if(OMNICPP_USE_SPDLOG)
    if(OMNICPP_USE_CPM)
        CPMAddPackage(
            NAME spdlog
            VERSION 1.12.0
            GITHUB_REPOSITORY gabime/spdlog
            OPTIONS "SPDLOG_BUILD_SHARED OFF" "SPDLOG_BUILD_EXAMPLE OFF" "SPDLOG_BUILD_TESTS OFF"
        )
    else()
        find_package(spdlog QUIET)

        if(NOT spdlog_FOUND)
            message(WARNING "spdlog not found, logging will be disabled")
            set(OMNICPP_USE_SPDLOG OFF)
        endif()
    endif()
endif()

# GLM - Math library
if(OMNICPP_USE_GLM)
    if(OMNICPP_USE_CPM)
        CPMAddPackage(
            NAME glm
            VERSION 0.9.9.8
            GITHUB_REPOSITORY g-truc/glm
        )
    else()
        find_package(glm QUIET)

        if(NOT glm_FOUND)
            message(WARNING "GLM not found, math library will be disabled")
            set(OMNICPP_USE_GLM OFF)
        endif()
    endif()
endif()

# STB - Image library
if(OMNICPP_USE_STB)
    if(OMNICPP_USE_CPM)
        CPMAddPackage(
            NAME stb
            VERSION 0.0.0
            GITHUB_REPOSITORY nothings/stb
        )
    else()
        # STB is header-only, just check if headers exist
        find_path(STB_INCLUDE_DIR stb_image.h
            PATHS ${CMAKE_SOURCE_DIR}/external/stb
            ${CMAKE_INSTALL_PREFIX}/include
        )

        if(NOT STB_INCLUDE_DIR)
            message(WARNING "STB not found, image loading will be disabled")
            set(OMNICPP_USE_STB OFF)
        endif()
    endif()
endif()

# ============================================================================
# Graphics Dependencies
# ============================================================================

# Vulkan
if(OMNICPP_USE_VULKAN)
    find_package(Vulkan QUIET)

    if(NOT Vulkan_FOUND)
        message(WARNING "Vulkan not found, Vulkan support disabled")
        set(OMNICPP_USE_VULKAN OFF)
    endif()
endif()

# OpenGL
if(OMNICPP_USE_OPENGL)
    find_package(OpenGL QUIET)

    if(NOT OpenGL_FOUND)
        message(WARNING "OpenGL not found, OpenGL support disabled")
        set(OMNICPP_USE_OPENGL OFF)
    endif()
endif()

# ============================================================================
# Qt6 Framework
# ============================================================================
if(OMNICPP_USE_QT6)
    find_package(Qt6 QUIET COMPONENTS Core Gui Widgets)

    if(NOT Qt6_FOUND)
        message(WARNING "Qt6 not found, Qt6 support disabled")
        set(OMNICPP_USE_QT6 OFF)
    else()
        # Enable Qt MOC, RCC, UIC
        set(CMAKE_AUTOMOC ON)
        set(CMAKE_AUTORCC ON)
        set(CMAKE_AUTOUIC ON)
    endif()
endif()

# ============================================================================
# Testing Dependencies
# ============================================================================
if(OMNICPP_BUILD_TESTS)
    # Google Test
    if(OMNICPP_USE_CPM)
        CPMAddPackage(
            NAME googletest
            VERSION 1.14.0
            GITHUB_REPOSITORY google/googletest
            OPTIONS "BUILD_GMOCK OFF" "INSTALL_GTEST OFF"
        )
    else()
        find_package(GTest QUIET)

        if(NOT GTest_FOUND)
            message(WARNING "Google Test not found, tests will be disabled")
            set(OMNICPP_BUILD_TESTS OFF)
        endif()
    endif()
endif()

# ============================================================================
# Coverage Dependencies
# ============================================================================
if(OMNICPP_ENABLE_COVERAGE)
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        # Coverage flags
        add_compile_options(--coverage)
        add_link_options(--coverage)

        # Exclude certain directories from coverage
        set(COVERAGE_EXCLUDE_PATTERNS
            "*/tests/*"
            "*/examples/*"
            "*/build/*"
            "*/external/*"
            "*/CPM_modules/*"
        )
    else()
        message(WARNING "Coverage only supported with GCC and Clang")
        set(OMNICPP_ENABLE_COVERAGE OFF)
    endif()
endif()

# ============================================================================
# Dependency Summary
# ============================================================================
message(STATUS "")
message(STATUS "=== Dependency Summary ===")
message(STATUS "Core:")
message(STATUS "  Threads: ${Threads_FOUND}")
message(STATUS "")
message(STATUS "Optional:")
message(STATUS "  spdlog: ${OMNICPP_USE_SPDLOG} (${spdlog_FOUND})")
message(STATUS "  GLM: ${OMNICPP_USE_GLM} (${glm_FOUND})")
message(STATUS "  STB: ${OMNICPP_USE_STB} (${STB_INCLUDE_DIR})")
message(STATUS "")
message(STATUS "Graphics:")
message(STATUS "  Vulkan: ${OMNICPP_USE_VULKAN} (${Vulkan_FOUND})")
message(STATUS "  OpenGL: ${OMNICPP_USE_OPENGL} (${OpenGL_FOUND})")
message(STATUS "  Qt6: ${OMNICPP_USE_QT6} (${Qt6_FOUND})")
message(STATUS "")
message(STATUS "Testing:")
message(STATUS "  Google Test: ${OMNICPP_BUILD_TESTS} (${GTest_FOUND})")
message(STATUS "  Coverage: ${OMNICPP_ENABLE_COVERAGE}")
message(STATUS "==========================")
message(STATUS "")

# ============================================================================
# Export dependency variables
# ============================================================================
set(OMNICPP_DEPENDENCIES_FOUND TRUE)
