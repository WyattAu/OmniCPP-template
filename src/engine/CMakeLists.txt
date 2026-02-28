cmake_minimum_required(VERSION 3.20)
project(OmniCppEngine VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
# Using C++23 as per ADR-016: C++23 Without Modules
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Vulkan is required for graphics rendering
message(STATUS "ENGINE: OMNICPP_BUILD_ENGINE = ${OMNICPP_BUILD_ENGINE}")
message(STATUS "ENGINE: OMNICPP_USE_VULKAN = ${OMNICPP_USE_VULKAN}")
message(STATUS "ENGINE: Vulkan_FOUND = ${Vulkan_FOUND}")
message(STATUS "ENGINE: Vulkan_INCLUDE_DIRS = ${Vulkan_INCLUDE_DIRS}")
message(STATUS "ENGINE: Vulkan_LIBRARIES = ${Vulkan_LIBRARIES}")
if(OMNICPP_USE_VULKAN AND Vulkan_FOUND)
    message(STATUS "Found Vulkan for engine: using pre-configured Vulkan")
    message(STATUS "  Include: ${Vulkan_INCLUDE_DIRS}")
    message(STATUS "  Library: ${Vulkan_LIBRARIES}")
else()
    message(WARNING "Vulkan not configured - graphics will be disabled")
    set(OMNICPP_USE_VULKAN OFF CACHE BOOL "Use Vulkan" FORCE)
endif()

# Find Qt6 (optional) and Vulkan (optional)
if(OMNICPP_USE_QT6)
    find_package(Qt6 COMPONENTS Core Gui Widgets)

    # Use TARGET check instead of Qt6_FOUND for more reliable detection
    # Qt6_FOUND variable may not be set properly in all CMake configurations
    if(NOT TARGET Qt6::Core)
        message(FATAL_ERROR "Qt6 requested (OMNICPP_USE_QT6=ON) but not found. "
            "Please install Qt6 or set OMNICPP_USE_QT6=OFF to build without Qt6.")
    endif()

    message(STATUS "Qt6 found - Qt6 integration enabled")

    # Qt6 Vulkan integration requires both Qt6 and Vulkan
    # Vulkan is configured above (before Qt6) so that Vulkan_FOUND is set
    # Use TARGET check instead of Qt6_FOUND for more reliable detection
    if(TARGET Qt6::Core AND Vulkan_FOUND)
        message(STATUS "Qt6 and Vulkan found - Qt6 Vulkan integration enabled")
        set(OMNICPP_USE_QT_VULKAN ON CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    else()
        message(WARNING "Qt6 Vulkan integration requires both Qt6 and Vulkan - Qt6 Vulkan integration disabled")
        message(STATUS "  Vulkan_FOUND: ${Vulkan_FOUND}")
        set(OMNICPP_USE_QT_VULKAN OFF CACHE BOOL "Use Qt6 with Vulkan" FORCE)
    endif()
endif()

# GLFW is optional based on OMNICPP_USE_GLFW option
if(OMNICPP_USE_GLFW)
    find_package(glfw3 QUIET)
    if(NOT glfw3_FOUND)
        message(FATAL_ERROR "GLFW requested (OMNICPP_USE_GLFW=ON) but not found. "
            "Please install GLFW or set OMNICPP_USE_GLFW=OFF to build without windowing support.")
    endif()
endif()

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
    window/window_manager.cpp
    window/vulkan_window.cpp
    graphics/renderer.cpp
)

# Link Vulkan libraries to engine
if(OMNICPP_USE_VULKAN)
    if(TARGET Vulkan::Vulkan)
        target_link_libraries(omnicpp_engine PUBLIC Vulkan::Vulkan)
    elseif(Vulkan_FOUND AND VULKAN_LIBRARIES)
        target_link_libraries(omnicpp_engine PUBLIC ${VULKAN_LIBRARIES})
    endif()
    target_include_directories(omnicpp_engine PUBLIC ${Vulkan_INCLUDE_DIRS})
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_VULKAN)
endif()

# Add QuillLogger.cpp conditionally if quill is enabled
# Temporarily disabled - using spdlog_shim instead
# if(OMNICPP_USE_QUILL)
#     target_sources(omnicpp_engine PRIVATE logging/QuillLogger.cpp)
# endif()

# Include directories
target_include_directories(omnicpp_engine
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/../../include
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../../include/engine
)

# Platform-specific exports
if(WIN32)
    target_compile_definitions(omnicpp_engine PRIVATE OMNICPP_BUILD_DLL)
elseif(UNIX)
    target_compile_definitions(omnicpp_engine PRIVATE OMNICPP_BUILD_SO)
endif()

# Qt6 integration (optional)
if(OMNICPP_USE_QT6 AND TARGET Qt6::Core)
    target_link_libraries(omnicpp_engine PUBLIC Qt6::Core Qt6::Gui Qt6::Widgets)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_QT6)

    # Enable Qt MOC, RCC, UIC
    set_target_properties(omnicpp_engine PROPERTIES
        AUTOMOC ON
        AUTORCC ON
        AUTOUIC ON
    )

    # Qt6 Vulkan integration
    if(OMNICPP_USE_QT_VULKAN)
        target_link_libraries(omnicpp_engine PUBLIC Qt6::Core Qt6::Gui)
        target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_QT_VULKAN)
        message(STATUS "Qt6 Vulkan integration enabled")
    endif()
endif()

# Vulkan integration (required for graphics rendering)
if(OMNICPP_USE_VULKAN AND Vulkan_FOUND)
    # Find X11 first (this provides X11_xcb variables)
    find_package(X11 QUIET COMPONENTS Xcb)
    
    # Also find XCB directly
    find_package(PkgConfig QUIET)
    if(PkgConfig_FOUND)
        pkg_check_modules(XCB QUIET xcb)
    endif()
    
    # If not found via pkg-config, try system paths directly
    if(NOT XCB_FOUND)
        find_library(XCB_LIBRARY NAMES xcb PATHS /usr/lib /usr/lib64 NO_DEFAULT_PATH)
        if(XCB_LIBRARY)
            set(XCB_FOUND TRUE)
            set(XCB_LIBRARIES "${XCB_LIBRARY}")
        endif()
    endif()
    
    # Link XCB
    if(XCB_FOUND)
        target_link_libraries(omnicpp_engine PUBLIC ${XCB_LIBRARIES})
        message(STATUS "Engine: XCB linked for native Vulkan surface")
    endif()
    
    # Link X11 and X11-xcb from FindX11
    if(X11_FOUND)
        target_link_libraries(omnicpp_engine PUBLIC X11::X11)
        message(STATUS "Engine: X11 linked for native Vulkan surface")
    endif()
    
    # X11-xcb provides XGetXCBConnection
    if(X11_xcb_FOUND)
        target_link_libraries(omnicpp_engine PUBLIC X11::xcb)
        message(STATUS "Engine: X11::xcb linked for native Vulkan surface")
    elseif(TARGET X11::X11_xcb)
        target_link_libraries(omnicpp_engine PUBLIC X11::X11_xcb)
        message(STATUS "Engine: X11::X11_xcb linked for native Vulkan surface")
    else()
        # Try to find X11-xcb manually
        find_library(X11_XCB_LIBRARY NAMES X11-xcb PATHS /usr/lib /usr/lib64 NO_DEFAULT_PATH)
        if(X11_XCB_LIBRARY)
            target_link_libraries(omnicpp_engine PUBLIC ${X11_XCB_LIBRARY})
            message(STATUS "Engine: X11-xcb linked for native Vulkan surface (manual)")
        endif()
    endif()
    
    if(TARGET Vulkan::Vulkan)
        target_link_libraries(omnicpp_engine PUBLIC Vulkan::Vulkan)
    elseif(VULKAN_LIBRARIES)
        target_link_libraries(omnicpp_engine PUBLIC ${VULKAN_LIBRARIES})
    endif()
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_VULKAN)
endif()

# GLFW integration (required for windowing and Vulkan surface)
if(OMNICPP_USE_GLFW AND glfw3_FOUND)
    target_link_libraries(omnicpp_engine PUBLIC glfw)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_HAS_GLFW)
endif()

# Quill integration (required for logging)
if(OMNICPP_USE_QUILL AND TARGET quill::quill)
    target_link_libraries(omnicpp_engine PUBLIC quill::quill)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_USE_QUILL)
endif()

# GLM integration (required for math)
if(OMNICPP_USE_GLM)
    target_link_libraries(omnicpp_engine PUBLIC glm::glm)
    target_compile_definitions(omnicpp_engine PUBLIC OMNICPP_USE_GLM)
endif()

# nlohmann/json integration (required for JSON)
if(OMNICPP_USE_NLOHMANN_JSON)
    target_link_libraries(omnicpp_engine PRIVATE nlohmann_json::nlohmann_json)
endif()
