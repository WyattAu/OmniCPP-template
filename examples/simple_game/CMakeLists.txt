cmake_minimum_required(VERSION 3.20)
project(SimpleGame VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Example executable
add_executable(simple_game
    main.cpp
)

# Link to the engine directly (same project)
target_link_libraries(simple_game
    PRIVATE
        omnicpp_engine
)

# Installation
include(GNUInstallDirs)
install(TARGETS simple_game
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
