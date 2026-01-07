/**
 * @file DemoMain.cpp
 * @brief Main entry point for demo game
 * @version 1.0.0
 */

#include "game/DemoGame.hpp"
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

namespace omnicpp {

// Function pointer types
using CreateEngineFunc = IEngine* (*)(const EngineConfig&);
using DestroyEngineFunc = void (*)(IEngine*);
using GetVersionFunc = const char* (*)();

int main(int argc, char* argv[]) {
    std::cout << "=== OmniCpp Demo Game ===" << std::endl;
    std::cout << "Version 1.0.0" << std::endl;
    std::cout << std::endl;

    // Determine library path based on platform
    const char* library_path = nullptr;
#ifdef _WIN32
    library_path = "omnicpp_engine.dll";
#else
    library_path = "./libomnicpp_engine.so";
#endif

    // Load engine library
    auto engine_handle = LOAD_LIBRARY(library_path);
    if (!engine_handle) {
        std::cerr << "Failed to load engine library: " << library_path << std::endl;
#ifdef _WIN32
        std::cerr << "Error code: " << GetLastError() << std::endl;
#else
        std::cerr << "Error: " << dlerror() << std::endl;
#endif
        return 1;
    }

    // Load engine functions
    auto create_engine = reinterpret_cast<CreateEngineFunc>(
        GET_SYMBOL(engine_handle, "create_engine"));
    auto destroy_engine = reinterpret_cast<DestroyEngineFunc>(
        GET_SYMBOL(engine_handle, "destroy_engine"));
    auto get_version = reinterpret_cast<GetVersionFunc>(
        GET_SYMBOL(engine_handle, "engine_get_version"));

    if (!create_engine || !destroy_engine || !get_version) {
        std::cerr << "Failed to load engine functions" << std::endl;
        FREE_LIBRARY(engine_handle);
        return 1;
    }

    // Print engine version
    std::cout << "Loaded engine version: " << get_version() << std::endl;

    // Create subsystems (simplified for demo)
    // In a full implementation, these would be created by the game
    auto logger = std::make_unique<ConsoleLogger>();
    auto platform = std::make_unique<Platform>();
    
    // Create engine configuration
    EngineConfig config;
    config.logger = logger.get();
    config.platform = platform.get();
    config.renderer = nullptr;  // Will use default renderer
    config.input_manager = nullptr;  // Will use default input
    config.audio_manager = nullptr;  // Will use default audio
    config.physics_engine = nullptr;  // Will use default physics
    config.resource_manager = nullptr;  // Will use default resources

    // Create engine
    auto engine = create_engine(config);
    if (!engine) {
        std::cerr << "Failed to create engine" << std::endl;
        FREE_LIBRARY(engine_handle);
        return 1;
    }

    // Create and initialize demo game
    auto demo_game = std::make_unique<game::DemoGame>(engine);

    if (!demo_game->initialize()) {
        std::cerr << "Failed to initialize demo game" << std::endl;
        destroy_engine(engine);
        FREE_LIBRARY(engine_handle);
        return 1;
    }

    // Run demo game
    int exit_code = demo_game->run();

    // Cleanup
    demo_game->shutdown();
    destroy_engine(engine);
    FREE_LIBRARY(engine_handle);

    std::cout << "Demo game exited with code: " << exit_code << std::endl;
    return exit_code;
}

} // namespace omnicpp
