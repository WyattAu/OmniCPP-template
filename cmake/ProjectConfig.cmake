# ============================================================================
# OmniCpp Template - Project Configuration
# ============================================================================
# Defines project-wide variables and paths
# ============================================================================

# Project metadata
set(OMNICPP_PROJECT_NAME "OmniCppTemplate" CACHE STRING "Project name")
set(OMNICPP_PROJECT_VERSION "1.0.0" CACHE STRING "Project version")
set(OMNICPP_PROJECT_DESCRIPTION "OmniCpp Template Project" CACHE STRING "Project description")

# Source directories
set(OMNICPP_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}" CACHE PATH "Source directory")
set(OMNICPP_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include" CACHE PATH "Include directory")
set(OMNICPP_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src" CACHE PATH "Source code directory")
set(OMNICPP_TESTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/tests" CACHE PATH "Tests directory")
set(OMNICPP_EXAMPLES_DIR "${CMAKE_CURRENT_SOURCE_DIR}/examples" CACHE PATH "Examples directory")
set(OMNICPP_ASSETS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/assets" CACHE PATH "Assets directory")

# Build directories
set(OMNICPP_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}" CACHE PATH "Build directory")
set(OMNICPP_BIN_DIR "${CMAKE_CURRENT_BINARY_DIR}/bin" CACHE PATH "Binary output directory")
set(OMNICPP_LIB_DIR "${CMAKE_CURRENT_BINARY_DIR}/lib" CACHE PATH "Library output directory")
set(OMNICPP_OBJ_DIR "${CMAKE_CURRENT_BINARY_DIR}/obj" CACHE PATH "Object files directory")

# Installation directories
set(OMNICPP_INSTALL_BIN_DIR "bin" CACHE STRING "Binary installation directory")
set(OMNICPP_INSTALL_LIB_DIR "lib" CACHE STRING "Library installation directory")
set(OMNICPP_INSTALL_INCLUDE_DIR "include" CACHE STRING "Header installation directory")
set(OMNICPP_INSTALL_DATA_DIR "share/${OMNICPP_PROJECT_NAME}" CACHE STRING "Data installation directory")
set(OMNICPP_INSTALL_DOC_DIR "share/doc/${OMNICPP_PROJECT_NAME}" CACHE STRING "Documentation installation directory")
set(OMNICPP_INSTALL_CMAKE_DIR "lib/cmake/${OMNICPP_PROJECT_NAME}" CACHE STRING "CMake config installation directory")

# C++ standard
set(OMNICPP_CPP_STANDARD "23" CACHE STRING "C++ standard to use")
set_property(CACHE OMNICPP_CPP_STANDARD PROPERTY STRINGS "20" "23")

# Set C++ standard
set(CMAKE_CXX_STANDARD ${OMNICPP_CPP_STANDARD})
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export variables for use in subdirectories
set(OMNICPP_PROJECT_NAME ${OMNICPP_PROJECT_NAME} PARENT_SCOPE)
set(OMNICPP_PROJECT_VERSION ${OMNICPP_PROJECT_VERSION} PARENT_SCOPE)
set(OMNICPP_PROJECT_DESCRIPTION ${OMNICPP_PROJECT_DESCRIPTION} PARENT_SCOPE)
set(OMNICPP_SOURCE_DIR ${OMNICPP_SOURCE_DIR} PARENT_SCOPE)
set(OMNICPP_INCLUDE_DIR ${OMNICPP_INCLUDE_DIR} PARENT_SCOPE)
set(OMNICPP_SRC_DIR ${OMNICPP_SRC_DIR} PARENT_SCOPE)
set(OMNICPP_TESTS_DIR ${OMNICPP_TESTS_DIR} PARENT_SCOPE)
set(OMNICPP_EXAMPLES_DIR ${OMNICPP_EXAMPLES_DIR} PARENT_SCOPE)
set(OMNICPP_ASSETS_DIR ${OMNICPP_ASSETS_DIR} PARENT_SCOPE)
set(OMNICPP_BUILD_DIR ${OMNICPP_BUILD_DIR} PARENT_SCOPE)
set(OMNICPP_BIN_DIR ${OMNICPP_BIN_DIR} PARENT_SCOPE)
set(OMNICPP_LIB_DIR ${OMNICPP_LIB_DIR} PARENT_SCOPE)
set(OMNICPP_OBJ_DIR ${OMNICPP_OBJ_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_BIN_DIR ${OMNICPP_INSTALL_BIN_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_LIB_DIR ${OMNICPP_INSTALL_LIB_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_INCLUDE_DIR ${OMNICPP_INSTALL_INCLUDE_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_DATA_DIR ${OMNICPP_INSTALL_DATA_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_DOC_DIR ${OMNICPP_INSTALL_DOC_DIR} PARENT_SCOPE)
set(OMNICPP_INSTALL_CMAKE_DIR ${OMNICPP_INSTALL_CMAKE_DIR} PARENT_SCOPE)

# Validate configuration
if(NOT EXISTS "${OMNICPP_SOURCE_DIR}")
    message(FATAL_ERROR "Source directory does not exist: ${OMNICPP_SOURCE_DIR}")
endif()

if(NOT EXISTS "${OMNICPP_INCLUDE_DIR}")
    message(FATAL_ERROR "Include directory does not exist: ${OMNICPP_INCLUDE_DIR}")
endif()

message(STATUS "Project configuration loaded successfully")
