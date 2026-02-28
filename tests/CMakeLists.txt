cmake_minimum_required(VERSION 3.28...4.0)
project(OmniCppTests VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
# Using C++23 as per ADR-016: C++23 Without Modules
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find dependencies
# Vulkan is configured in cmake/FindDependencies.cmake for Nix environment
find_package(Qt6 COMPONENTS Core Gui Widgets)
find_package(Threads REQUIRED)

# Find Google Test - use the one already found by parent CMakeLists.txt
# The parent CMakeLists.txt (FindDependencies.cmake) already handles GTest via CPM
# so we don't need to find it again here

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Unit test executable
add_executable(omnicpp_unit_tests
    unit/test_quill_logger.cpp
    unit/test_input_manager.cpp
    unit/test_resource_manager.cpp
    unit/test_physics_engine.cpp
    unit/test_audio_manager.cpp
    unit/test_ecs.cpp
    )

target_link_libraries(omnicpp_unit_tests
    PRIVATE
    omnicpp_engine
    Threads::Threads
    gtest
    gtest_main
)

if(Vulkan_FOUND)
    target_link_libraries(omnicpp_unit_tests PRIVATE Vulkan::Vulkan)
endif()

if(Qt6_FOUND)
    target_link_libraries(omnicpp_unit_tests PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
endif()

# Integration test executable
add_executable(omnicpp_integration_tests
    test_engine.cpp
    test_game.cpp
)

target_link_libraries(omnicpp_integration_tests
    PRIVATE
    omnicpp_engine
    Threads::Threads
)

if(Vulkan_FOUND)
    target_link_libraries(omnicpp_integration_tests PRIVATE Vulkan::Vulkan)
endif()

if(Qt6_FOUND)
    target_link_libraries(omnicpp_integration_tests PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
endif()

# Enable testing
enable_testing()

# Unit tests
add_test(NAME SpdLogLoggerTest COMMAND omnicpp_unit_tests)

# Integration tests
add_test(NAME EngineTest COMMAND omnicpp_integration_tests --test-engine)
add_test(NAME GameTest COMMAND omnicpp_integration_tests --test-game)
