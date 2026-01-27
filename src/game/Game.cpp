/**
 * @file Game.cpp
 * @brief Game application implementation for OmniCpp
 * @version 1.0.0
 */

#include "game/Game.hpp"

// Platform-specific dynamic loading
#ifdef _WIN32
    #include <windows.h>
    #define LOAD_LIBRARY(path) LoadLibraryA(path)
    #define GET_SYMBOL(handle, name) GetProcAddress((HMODULE)handle, name)
    #define FREE_LIBRARY(handle) FreeLibrary((HMODULE)handle)
#else
    #include <dlfcn.h>
    #define LOAD_LIBRARY(path) dlopen(path, RTLD_LAZY)
    #define GET_SYMBOL(handle, name) dlsym(handle, name)
    #define FREE_LIBRARY(handle) dlclose(handle)
#endif

#include <iostream>
#include <stdexcept>

namespace omnicpp {

Game::Game() = default;
Game::~Game() {
    shutdown();
}

bool Game::load_engine() {
    // Determine library path based on platform
    const char* library_path = nullptr;
#ifdef _WIN32
    library_path = "omnicpp_engine.dll";
#else
    library_path = "./libomnicpp_engine.so";
#endif

    // Load the engine library
    m_engine_handle = LOAD_LIBRARY(library_path);
    if (!m_engine_handle) {
        std::cerr << "Failed to load engine library: " << library_path << std::endl;
#ifdef _WIN32
        std::cerr << "Error code: " << GetLastError() << std::endl;
#else
        std::cerr << "Error: " << dlerror() << std::endl;
#endif
        return false;
    }

    // Load engine functions
    m_create_engine = reinterpret_cast<CreateEngineFunc>(GET_SYMBOL(m_engine_handle, "create_engine"));
    m_destroy_engine = reinterpret_cast<DestroyEngineFunc>(GET_SYMBOL(m_engine_handle, "destroy_engine"));
    m_get_version = reinterpret_cast<GetVersionFunc>(GET_SYMBOL(m_engine_handle, "engine_get_version"));

    if (!m_create_engine || !m_destroy_engine || !m_get_version) {
        std::cerr << "Failed to load engine functions" << std::endl;
        unload_engine();
        return false;
    }

    // Print engine version
    std::cout << "Loaded engine version: " << m_get_version() << std::endl;

    return true;
}

void Game::unload_engine() {
    if (m_engine) {
        m_destroy_engine(m_engine);
        m_engine = nullptr;
    }

    if (m_engine_handle) {
        FREE_LIBRARY(m_engine_handle);
        m_engine_handle = nullptr;
    }

    m_create_engine = nullptr;
    m_destroy_engine = nullptr;
    m_get_version = nullptr;
}

bool Game::initialize() {
    std::cout << "Initializing game..." << std::endl;

    // Load engine library
    if (!load_engine()) {
        return false;
    }

    // Create engine with configuration
    EngineConfig config;
    // Note: Subsystems will be created by the game in a full implementation
    // For now, we pass nullptr for all subsystems
    config.renderer = nullptr;
    config.input_manager = nullptr;
    config.audio_manager = nullptr;
    config.physics_engine = nullptr;
    config.resource_manager = nullptr;
    config.logger = nullptr;
    config.platform = nullptr;

    m_engine = m_create_engine(config);
    if (!m_engine) {
        std::cerr << "Failed to create engine" << std::endl;
        unload_engine();
        return false;
    }

    m_initialized = true;
    std::cout << "Game initialized successfully" << std::endl;
    return true;
}

void Game::update(float delta_time) {
    if (m_engine) {
        m_engine->update(delta_time);
    }
}

void Game::render() {
    if (m_engine) {
        m_engine->render();
    }
}

void Game::handle_input() {
    // Handle input here
    // For now, this is a placeholder
}

int Game::run() {
    if (!m_initialized) {
        spdlog::error("Game: Game not initialized");
        return 1;
    }

    spdlog::info("Game: Starting game loop...");
    m_running = true;

    // Simple game loop
    while (m_running) {
        handle_input();
        update(0.016f); // 60 FPS
        render();
    }

    spdlog::info("Game: Game loop ended");
    return 0;
}

void Game::shutdown() {
    if (!m_initialized) {
        return;
    }

    spdlog::info("Game: Shutting down game...");
    m_running = false;
    unload_engine();
    m_initialized = false;
    spdlog::info("Game: Game shutdown complete");
}

} // namespace omnicpp

// Main entry point
int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;

    omnicpp::Game game;

    if (!game.initialize()) {
        spdlog::error("Game: Failed to initialize game");
        return 1;
    }

    int exit_code = game.run();
    game.shutdown();

    return exit_code;
}
