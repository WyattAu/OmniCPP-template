cmake_minimum_required(VERSION 3.20)
project(SimpleGame VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find OmniCpp engine
find_package(OmniCppEngine REQUIRED)

# Example executable
add_executable(simple_game
    main.cpp
)

target_link_libraries(simple_game
    PRIVATE
        OmniCpp::OmniCppEngine
)

# Installation
include(GNUInstallDirs)
install(TARGETS simple_game
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
