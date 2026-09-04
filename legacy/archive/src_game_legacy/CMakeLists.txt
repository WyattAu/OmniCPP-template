cmake_minimum_required(VERSION 3.20)
project(OmniCppGame VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
# Using C++23 as per ADR-016: C++23 Without Modules
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Qt6 (optional) and Vulkan (optional)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)

    if(NOT Qt6_FOUND)
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()
endif()

# Vulkan is optional based on OMNICPP_USE_VULKAN option
# Vulkan is configured in cmake/FindDependencies.cmake for Nix environment
# Vulkan_FOUND is set to TRUE in cmake/FindDependencies.cmake
# No need to check Vulkan_FOUND here

# Pong game executable with Qt6 and Vulkan
if(OMNICPP_USE_QT6 AND Qt6_FOUND)
    # Enable Qt MOC, RCC, UIC
    set(CMAKE_AUTOMOC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOUIC ON)

    add_executable(omnicpp_pong
        ${CMAKE_SOURCE_DIR}/examples/pong/main.cpp
        ${CMAKE_SOURCE_DIR}/examples/pong/pong_game.cpp
    )

    # Enable Qt MOC, RCC, UIC for game
    set_target_properties(omnicpp_pong PROPERTIES
        AUTOMOC ON
        AUTORCC ON
        AUTOUIC ON
    )
else()
    # Build without Qt6 - minimal game executable
    add_executable(omnicpp_pong
        ${CMAKE_SOURCE_DIR}/examples/pong/main.cpp
        ${CMAKE_SOURCE_DIR}/examples/pong/pong_game.cpp
    )

    # Ensure console application (not GUI)
    if(WIN32)
        set_target_properties(omnicpp_pong PROPERTIES
            WIN32_EXECUTABLE FALSE
            LINK_FLAGS "/SUBSYSTEM:CONSOLE /ENTRY:mainCRTStartup"
        )
    endif()
endif()

# Link against engine library
target_link_libraries(omnicpp_pong
    PRIVATE
    omnicpp_engine
)

# Link with Qt6 (optional) and Vulkan (required)
if(OMNICPP_USE_QT6 AND Qt6_FOUND)
    target_link_libraries(omnicpp_pong
        PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
    )

    if(TARGET Qt6::VulkanSupport)
        target_link_libraries(omnicpp_pong PRIVATE Qt6::VulkanSupport)
    endif()
endif()

# Link with Vulkan (optional)
if(OMNICPP_USE_VULKAN AND TARGET Vulkan::Vulkan)
    target_link_libraries(omnicpp_pong PRIVATE Vulkan::Vulkan)
endif()

# Link with libxcb for native XCB Vulkan surface (optional)
# This enables creating Vulkan surfaces from Qt XCB windows
# Try both Nix and system XCB
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(XCB QUIET xcb)
endif()

# If not found via pkg-config, try system paths directly
if(NOT XCB_FOUND)
    # Try to find system XCB directly
    find_path(XCB_INCLUDE_DIR NAMES xcb/xcb.h PATHS /usr/include NO_DEFAULT_PATH)
    find_library(XCB_LIBRARY NAMES xcb PATHS /usr/lib /usr/lib64 NO_DEFAULT_PATH)
    if(XCB_INCLUDE_DIR AND XCB_LIBRARY)
        set(XCB_FOUND TRUE)
        set(XCB_INCLUDE_DIRS "${XCB_INCLUDE_DIR}")
        set(XCB_LIBRARIES "${XCB_LIBRARY}")
        message(STATUS "Found system XCB: ${XCB_LIBRARY}")
    endif()
endif()

if(XCB_FOUND)
    target_link_libraries(omnicpp_pong PRIVATE ${XCB_LIBRARIES})
    target_include_directories(omnicpp_pong PRIVATE ${XCB_INCLUDE_DIRS})
    target_compile_definitions(omnicpp_pong PRIVATE OMNICPP_HAS_XCB=1)
    message(STATUS "XCB linking enabled for native Vulkan surface")
else()
    message(STATUS "XCB not found - using Qt's Vulkan surface approach")
endif()

# Include directories
target_include_directories(omnicpp_pong
    PRIVATE
    $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Define compile-time flags for Qt6 and Vulkan
if(OMNICPP_USE_QT6 AND Qt6_FOUND)
    target_compile_definitions(omnicpp_pong PRIVATE OMNICPP_HAS_QT=1)
endif()

# Define compile-time flag for Vulkan (optional)
if(OMNICPP_USE_VULKAN AND TARGET Vulkan::Vulkan)
    target_compile_definitions(omnicpp_pong PRIVATE OMNICPP_HAS_VULKAN=1)
endif()

# Compiler-specific flags
if(MSVC)
    target_compile_options(omnicpp_pong PRIVATE
        /W4
        /permissive-
        /Zc:__cplusplus
        /std:c++23
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(omnicpp_pong PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -std=c++23
    )
endif()

# Installation
include(GNUInstallDirs)

install(TARGETS omnicpp_pong
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
