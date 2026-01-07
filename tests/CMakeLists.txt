cmake_minimum_required(VERSION 3.20)
project(OmniCppTests VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find dependencies
find_package(Vulkan)
find_package(Qt6 COMPONENTS Core Gui Widgets)
find_package(Threads REQUIRED)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/../include)

# Test executable
add_executable(omnicpp_tests
    test_engine.cpp
    test_game.cpp
)

target_link_libraries(omnicpp_tests
    PRIVATE
        omnicpp_engine
        Threads::Threads
)

if(Vulkan_FOUND)
    target_link_libraries(omnicpp_tests PRIVATE Vulkan::Vulkan)
endif()

if(Qt6_FOUND)
    target_link_libraries(omnicpp_tests PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
endif()

# Enable testing
enable_testing()
add_test(NAME EngineTest COMMAND omnicpp_tests --test-engine)
add_test(NAME GameTest COMMAND omnicpp_tests --test-game)
