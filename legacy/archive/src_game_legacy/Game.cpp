/**
 * @file Game.cpp
 * @brief Game application implementation for dynamic engine loading
 * @version 1.0.0
 */

#include "game/Game.hpp"
#include "engine/Engine.hpp"
#include "engine/IEngine.hpp"
#include "engine/IRenderer.hpp"
#include "engine/IInputManager.hpp"
#include "engine/IAudioManager.hpp"
#include "engine/IPhysicsEngine.hpp"
#include "engine/IResourceManager.hpp"
#include "engine/ILogger.hpp"
#include "engine/IPlatform.hpp"
#include <iostream>
#include <memory>
#include <chrono>
#include "engine/logging/Log.hpp"

#ifdef _WIN32
    #include <windows.h>
    #define RTLD_NOW 0
    static void* dlopen(const char* filename, int) {
        return LoadLibraryA(filename);
    }
    static void* dlsym(void* handle, const char* symbol) {
        return (void*)GetProcAddress((HMODULE)handle, symbol);
    }
    static void dlclose(void* handle) {
        FreeLibrary((HMODULE)handle);
    }
#else
    #include <dlfcn.h>
#endif

namespace omnicpp {

// Static engine functions for fallback when dynamic loading fails
extern IEngine* create_engine(const EngineConfig& config);
extern void destroy_engine(IEngine* engine);

Game::Game() 
    : m_engine_handle(nullptr)
    , m_engine(nullptr)
    , m_create_engine(nullptr)
    , m_destroy_engine(nullptr)
    , m_get_version(nullptr)
    , m_running(false)
    , m_initialized(false) {
    omnicpp::log::debug("Game: Constructor");
}

Game::~Game() {
    if (m_initialized) {
        shutdown();
    }
    omnicpp::log::debug("Game: Destructor");
}

bool Game::load_engine() {
    omnicpp::log::info("Game: Loading engine...");
    
    // Try dynamic loading first
    const char* engine_lib = 
#ifdef _WIN32
        "omnicpp_engine.dll";
#elif defined(__APPLE__)
        "libomnicpp_engine.dylib";
#else
        "libomnicpp_engine.so";
#endif
    
    m_engine_handle = dlopen(engine_lib, RTLD_NOW);
    
    if (m_engine_handle) {
        // Load function pointers
        m_create_engine = reinterpret_cast<CreateEngineFunc>(dlsym(m_engine_handle, "create_engine"));
        m_destroy_engine = reinterpret_cast<DestroyEngineFunc>(dlsym(m_engine_handle, "destroy_engine"));
        m_get_version = reinterpret_cast<GetVersionFunc>(dlsym(m_engine_handle, "engine_get_version"));
        
        if (!m_create_engine || !m_destroy_engine) {
            omnicpp::log::warn("Game: Failed to load engine functions from {}", engine_lib);
            dlclose(m_engine_handle);
            m_engine_handle = nullptr;
        } else {
            omnicpp::log::info("Game: Engine loaded dynamically from {}", engine_lib);
            if (m_get_version) {
                omnicpp::log::info("Game: Engine version: {}", m_get_version());
            }
        }
    }
    
    // Fallback to static linking
    if (!m_engine_handle) {
        omnicpp::log::info("Game: Using statically linked engine");
        m_create_engine = &omnicpp::create_engine;
        m_destroy_engine = &omnicpp::destroy_engine;
        m_get_version = nullptr; // Static version available via engine_get_version()
    }
    
    return m_create_engine != nullptr && m_destroy_engine != nullptr;
}

void Game::unload_engine() {
    if (m_engine) {
        m_destroy_engine(m_engine);
        m_engine = nullptr;
    }
    
    if (m_engine_handle) {
        dlclose(m_engine_handle);
        m_engine_handle = nullptr;
    }
    
    m_create_engine = nullptr;
    m_destroy_engine = nullptr;
    m_get_version = nullptr;
}

bool Game::initialize() {
    omnicpp::log::info("Game: Initializing...");
    
    if (m_initialized) {
        omnicpp::log::warn("Game: Already initialized");
        return true;
    }
    
    // Load engine
    if (!load_engine()) {
        omnicpp::log::error("Game: Failed to load engine");
        return false;
    }
    
    // Create engine configuration
    EngineConfig config;
    config.platform = nullptr;
    config.renderer = nullptr;
    config.input_manager = nullptr;
    config.audio_manager = nullptr;
    config.physics_engine = nullptr;
    config.resource_manager = nullptr;
    config.logger = nullptr;
    
    // Create engine
    m_engine = m_create_engine(config);
    if (!m_engine) {
        omnicpp::log::error("Game: Failed to create engine");
        unload_engine();
        return false;
    }
    
    m_initialized = true;
    omnicpp::log::info("Game: Initialized successfully");
    return true;
}

void Game::shutdown() {
    if (!m_initialized) {
        return;
    }
    
    omnicpp::log::info("Game: Shutting down...");
    
    m_running = false;
    unload_engine();
    m_initialized = false;
    
    omnicpp::log::info("Game: Shutdown complete");
}

int Game::run() {
    if (!m_initialized || !m_engine) {
        omnicpp::log::error("Game: Cannot run - not initialized");
        return 1;
    }
    
    omnicpp::log::info("Game: Starting game loop");
    m_running = true;
    
    auto last_time = std::chrono::high_resolution_clock::now();
    
    // Main game loop
    while (m_running) {
        auto current_time = std::chrono::high_resolution_clock::now();
        float delta_time = std::chrono::duration<float>(current_time - last_time).count();
        last_time = current_time;
        
        // Handle input
        handle_input();
        
        // Update game logic
        update(delta_time);
        
        // Render
        render();
    }
    
    omnicpp::log::info("Game: Game loop ended");
    return 0;
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
    // Input handling - in a full implementation, this would poll input events
    // and update game state accordingly
}

} // namespace omnicpp
