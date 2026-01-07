/**
 * @file Game.hpp
 * @brief Game application header for OmniCpp
 * @version 1.0.0
 */

#ifndef OMNICPP_GAME_HPP
#define OMNICPP_GAME_HPP

#include "engine/Engine.hpp"
#include <memory>

namespace omnicpp {

/**
 * @brief Game application class
 */
class Game {
public:
    Game();
    ~Game();

    /**
     * @brief Initialize the game
     * 
     * @return True if successful, false otherwise
     */
    bool initialize();

    /**
     * @brief Run the game main loop
     * 
     * @return Exit code
     */
    int run();

    /**
     * @brief Shutdown the game
     */
    void shutdown();

private:
    /**
     * @brief Load engine library dynamically
     * 
     * @return True if successful, false otherwise
     */
    bool load_engine();

    /**
     * @brief Unload engine library
     */
    void unload_engine();

    /**
     * @brief Update game logic
     * 
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Render game
     */
    void render();

    /**
     * @brief Handle input
     */
    void handle_input();

private:
    // Engine library handle
    void* m_engine_handle = nullptr;

    // Engine interface
    IEngine* m_engine = nullptr;

    // Engine function pointers
    using CreateEngineFunc = IEngine*(*)(const EngineConfig&);
    using DestroyEngineFunc = void(*)(IEngine*);
    using GetVersionFunc = const char* (*)();

    CreateEngineFunc m_create_engine = nullptr;
    DestroyEngineFunc m_destroy_engine = nullptr;
    GetVersionFunc m_get_version = nullptr;

    // Game state
    bool m_running = false;
    bool m_initialized = false;
};

} // namespace omnicpp

#endif // OMNICPP_GAME_HPP
