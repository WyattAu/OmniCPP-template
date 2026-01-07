cmake_minimum_required(VERSION 3.20)
project(OmniCppGame VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Qt6 (optional) and Vulkan (required)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)

    if(NOT Qt6_FOUND)
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()
endif()

find_package(Vulkan REQUIRED)

# 3D Pong game executable with Qt6 and Vulkan
if(OMNICPP_USE_QT6 AND Qt6_FOUND)
    # Enable Qt MOC, RCC, UIC
    set(CMAKE_AUTOMOC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOUIC ON)

    add_executable(omnicpp_pong
        Pong3D.cpp
        Qt/PongMainWindow.cpp
        Qt/PongRenderWidget.cpp
        Qt/PongControlPanel.cpp
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
        Pong3D.cpp
    )
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

if(TARGET Vulkan::Vulkan)
    target_link_libraries(omnicpp_pong PRIVATE Vulkan::Vulkan)
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

target_compile_definitions(omnicpp_pong PRIVATE OMNICPP_HAS_VULKAN=1)

# Compiler-specific flags
if(MSVC)
    target_compile_options(omnicpp_pong PRIVATE
        /W4
        /WX
        /permissive-
        /Zc:__cplusplus
        /std:c++23
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(omnicpp_pong PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Werror
        -std=c++23
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(omnicpp_pong PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Werror
        -std=c++23
    )
endif()

# Installation
include(GNUInstallDirs)

install(TARGETS omnicpp_pong
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
