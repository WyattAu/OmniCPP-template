/**
 * @file main.cpp
 * @brief Simple game example using OmniCpp engine
 * @version 1.0.0
 */

#include "engine/Engine.hpp"
#include <iostream>

int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;
    
    std::cout << "=== Simple Game Example ===" << std::endl;
    std::cout << "This example demonstrates how to use the OmniCpp engine." << std::endl;
    std::cout << std::endl;
    
    // Create engine configuration
    omnicpp::EngineConfig config;
    config.renderer = nullptr;  // Use default renderer
    config.input_manager = nullptr;  // Use default input manager
    config.audio_manager = nullptr;  // Use default audio manager
    config.physics_engine = nullptr;  // Use default physics engine
    config.resource_manager = nullptr;  // Use default resource manager
    config.logger = nullptr;  // Use default logger
    config.platform = nullptr;  // Use default platform
    
    // Create engine
    omnicpp::IEngine* engine = omnicpp::create_engine(config);
    if (!engine) {
        std::cerr << "Failed to create engine!" << std::endl;
        return 1;
    }
    
    std::cout << "Engine created successfully!" << std::endl;
    std::cout << "Engine version: " << omnicpp::engine_get_version() << std::endl;
    std::cout << std::endl;
    
    // Simple game loop
    std::cout << "Starting game loop..." << std::endl;
    std::cout << "Press Ctrl+C to exit." << std::endl;
    std::cout << std::endl;
    
    const float delta_time = 0.016f;  // 60 FPS
    int frame_count = 0;
    
    for (int i = 0; i < 100; ++i) {
        // Update engine
        engine->update(delta_time);
        
        // Render frame
        engine->render();
        
        frame_count++;
        
        if (frame_count % 60 == 0) {
            std::cout << "Frame: " << frame_count << std::endl;
        }
    }
    
    std::cout << std::endl;
    std::cout << "Game loop finished." << std::endl;
    std::cout << "Total frames rendered: " << frame_count << std::endl;
    
    // Cleanup
    engine->shutdown();
    omnicpp::destroy_engine(engine);
    
    std::cout << std::endl;
    std::cout << "=== Example Complete ===" << std::endl;
    
    return 0;
}
