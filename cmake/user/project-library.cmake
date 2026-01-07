# Licensed under the Apache License, Version 2.0 (the "License");

# ==============================================================================
# LIBRARY-SPECIFIC CONFIGURATION
# ==============================================================================
include(${CMAKE_CURRENT_LIST_DIR}/../user/project-common.cmake)

project(
    ${LIBRARY_NAME}
    VERSION 0.0.1
    LANGUAGES C CXX
    DESCRIPTION "template"
    HOMEPAGE_URL "https://github.com/your-org/your-repo")

# ==============================================================================
# Build guards
# ==============================================================================
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
    message(
        WARNING
            "In-source builds. Please make a new directory (called a Build directory) and run CMake from there."
    )
endif()

# ==============================================================================
# Library installation attributes
# ==============================================================================
set(INSTALL_INCLUDE_DIR include/${LIBRARY_NAME})
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/${LIBRARY_NAME}/
        DESTINATION ${INSTALL_INCLUDE_DIR})

# ==============================================================================
# Library dependencies
# ==============================================================================
# Try to find dependencies via find_package (Conan/system), fallback to CPM
find_package(fmt QUIET)
if(NOT fmt_FOUND)
    CPMAddPackage("gh:fmtlib/fmt#11.2.0")
endif()


# CPM packages specific to library
CPMAddPackage("gh:TheLartians/PackageProject.cmake@1.12.0")
CPMAddPackage("gh:cpm-cmake/CPMLicenses.cmake@0.0.7")
cpm_licenses_create_disclaimer_target(
    write-licenses-${LIBRARY_NAME} "${CMAKE_CURRENT_BINARY_DIR}/${LIBRARY_NAME}_third_party.txt"
    "${CPM_PACKAGES}")

# ==============================================================================
# Library source files
# ==============================================================================
gather_sources(headers ${CMAKE_CURRENT_SOURCE_DIR}/include)
gather_sources(sources ${CMAKE_CURRENT_SOURCE_DIR}/src)

# Gather module interface files
file(GLOB_RECURSE module_interfaces "${CMAKE_CURRENT_SOURCE_DIR}/src/modules/*.cppm")

# ==============================================================================
# Create library target
# ==============================================================================
add_library(${LIBRARY_NAME})
target_sources(${LIBRARY_NAME}
    PRIVATE ${headers}
    PRIVATE ${sources}
)

# Add C++ modules if available and not disabled
if(module_interfaces AND NOT DISABLE_CPP_MODULES)
    target_sources(${LIBRARY_NAME}
        PRIVATE FILE_SET cxx_modules TYPE CXX_MODULES
        BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/src/modules
        FILES ${module_interfaces}
    )
endif()

# Apply common target settings
apply_common_target_settings(${LIBRARY_NAME})

# ==============================================================================
# Library-specific configuration
# ==============================================================================
# Emscripten handler
include(${CMAKE_CURRENT_LIST_DIR}/tmplt-emscripten.cmake)
emscripten(${LIBRARY_NAME} 0 1 "")

# Headers
target_include_directories(
    ${LIBRARY_NAME}
    PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
    PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src>
    PUBLIC $<INSTALL_INTERFACE:${INSTALL_INCLUDE_DIR}>)

# Compile options
target_compile_options(
    ${LIBRARY_NAME}
    PUBLIC "$<$<COMPILE_LANG_AND_ID:CXX,MSVC>:/permissive-;/W4;$<$<NOT:$<BOOL:${DISABLE_CPP_MODULES}>>:/experimental:module>>"
    PUBLIC
        "$<$<AND:$<NOT:$<COMPILE_LANG_AND_ID:CXX,MSVC>>,$<NOT:$<PLATFORM_ID:Darwin>>,$<NOT:$<CXX_COMPILER_ID:Clang>>>:-Wall;-Wextra;-Wpedantic;-MMD;-MP;-fmodules-ts>"
    PUBLIC
        "$<$<AND:$<NOT:$<COMPILE_LANG_AND_ID:CXX,MSVC>>,$<PLATFORM_ID:Darwin>>:-Wall;-Wextra;-Wpedantic;-fmodules-ts>"
    PUBLIC "$<$<CXX_COMPILER_ID:Clang>:-fmodules-ts>"
)

# C++ standard
target_compile_features(${LIBRARY_NAME} PUBLIC cxx_std_23)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# C++ Modules configuration (only for supported generators)
if(NOT CMAKE_GENERATOR MATCHES "Visual Studio" AND NOT DISABLE_CPP_MODULES)
    set(CMAKE_CXX_MODULE_STD ON)
    set(CMAKE_CXX_MODULE_EXT ON)
endif()

# Linking
target_link_libraries(
    ${LIBRARY_NAME}
    PUBLIC fmt::fmt
    PRIVATE nlohmann_json::nlohmann_json)

# ==============================================================================
# Installation rules
# ==============================================================================
install(TARGETS ${LIBRARY_NAME}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Install library target (handled by packageProject)

# Workaround: Ensure .dll files go to bin/ on Windows, not bin/LibraryName/
if(WIN32 AND BUILD_SHARED_LIBS)
    install(TARGETS ${LIBRARY_NAME} RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT Runtime)

    # Remove duplicate DLL created by packageProject
    install(
        CODE "
        file(REMOVE_RECURSE \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/${LIBRARY_NAME}\")
        message(STATUS \"Removed duplicate DLL directory: ${CMAKE_INSTALL_BINDIR}/${LIBRARY_NAME}\")
    ")
endif()
