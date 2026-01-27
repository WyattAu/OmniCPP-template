cmake_minimum_required(VERSION 3.20)
project(OmniCppEngine VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Qt6 (optional) and Vulkan (required)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)
    find_package(Qt6 OPTIONAL_COMPONENTS VulkanSupport)

    if(NOT Qt6_FOUND)
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()
endif()

find_package(Vulkan REQUIRED)

# Engine library as shared library
add_library(omnicpp_engine SHARED
    Engine.cpp
    Renderer.cpp
    InputManager.cpp
    AudioManager.cpp
    PhysicsEngine.cpp
    ResourceManager.cpp
    Logger.cpp
    Platform.cpp

    # Logging
    logging/SpdLogLogger.cpp

    # ECS
    ecs/Entity.cpp
    ecs/Component.cpp
    ecs/TransformComponent.cpp
    ecs/MeshComponent.cpp

    # Scene
    scene/SceneNode.cpp
    scene/Scene.cpp
    scene/SceneManager.cpp

    # Qt/Vulkan Integration (disabled - Qt6::VulkanSupport not available)
    # Qt/QtVulkanIntegration.cpp
    # Qt/MainWindow.cpp
    # Qt/RenderWidget.cpp
    # Qt/ControlPanel.cpp
    # Qt/FPSOverlay.cpp
    # Vulkan (disabled - requires Qt6::VulkanSupport)
    # Vulkan/VulkanInstance.cpp
    # Vulkan/VulkanDevice.cpp
    # Vulkan/VulkanRenderer.cpp
    # Vulkan/ShaderManager.cpp
    # Vulkan/PyramidGeometry.cpp
)

# Include directories
target_include_directories(omnicpp_engine
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../../include>
    $<INSTALL_INTERFACE:include>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Platform-specific exports
if(WIN32)
    target_compile_definitions(omnicpp_engine PRIVATE OMNICPP_BUILD_DLL)
elseif(UNIX)
    target_compile_definitions(omnicpp_engine PRIVATE OMNICPP_BUILD_SO)
endif()

# Qt6 integration (optional)
if(OMNICPP_USE_QT6 AND Qt6_FOUND)
    target_link_libraries(omnicpp_engine PUBLIC Qt6::Core Qt6::Gui Qt6::Widgets)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_QT)

    # Enable Qt MOC, RCC, UIC
    set_target_properties(omnicpp_engine PROPERTIES
        AUTOMOC ON
        AUTORCC ON
        AUTOUIC ON
    )
endif()

# Vulkan integration (required)
target_link_libraries(omnicpp_engine PUBLIC Vulkan::Vulkan)
target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_VULKAN)

# spdlog integration (required)
if(OMNICPP_USE_SPDLOG AND TARGET spdlog::spdlog)
    target_link_libraries(omnicpp_engine PUBLIC spdlog::spdlog)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_USE_SPDLOG)
endif()

# nlohmann/json for logging configuration
if(OMNICPP_USE_SPDLOG)
    CPMAddPackage(
        NAME nlohmann_json
        VERSION 3.11.3
        GITHUB_REPOSITORY nlohmann/json
        OPTIONS "CMAKE_POLICY_VERSION_MINIMUM=3.5"
    )
    target_link_libraries(omnicpp_engine PUBLIC nlohmann_json::nlohmann_json)
endif()

# Additional dependencies
find_package(Threads REQUIRED)
target_link_libraries(omnicpp_engine PUBLIC Threads::Threads)

# Compiler-specific flags
if(MSVC)
    target_compile_options(omnicpp_engine PRIVATE
        /W4
        /permissive-
        /Zc:__cplusplus
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(omnicpp_engine PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Werror
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(omnicpp_engine PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Werror
    )
endif()

# Installation
include(GNUInstallDirs)

install(TARGETS omnicpp_engine
    EXPORT OmniCppEngineTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../../include/engine
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )

# Create package config
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/OmniCppEngineConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake/OmniCppEngineConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/OmniCppEngineConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/OmniCppEngine
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/OmniCppEngineConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/OmniCppEngineConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/OmniCppEngine
)
