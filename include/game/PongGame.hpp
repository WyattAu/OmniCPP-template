/**
 * @file PongGame.hpp
 * @brief 3D Pong game implementation with complete gameplay loop
 * @version 1.0.0
 */

#pragma once

#include <memory>
#include <cstdint>

namespace omnicpp {

// Forward declarations
class Engine;

namespace ecs {
class Entity;
class TransformComponent;
}

namespace scene {
class Scene;
class SceneManager;
}

namespace input {
class InputManager;
}

namespace game {

/**
 * @brief 3D Pong game with complete gameplay mechanics
 * 
 * Features:
 * - Two paddles (player and AI)
 * - Ball physics with collision detection
 * - Scoring system
 * - Keyboard controls (W/S for player paddle)
 * - Simple AI opponent
 */
class PongGame {
public:
    /**
     * @brief Construct a new Pong Game object
     * @param engine Pointer to the engine
     */
    explicit PongGame(Engine* engine);

    /**
     * @brief Destroy the Pong Game object
     */
    ~PongGame();

    // Disable copying
    PongGame(const PongGame&) = delete;
    PongGame& operator=(const PongGame&) = delete;

    // Enable moving
    PongGame(PongGame&&) noexcept = default;
    PongGame& operator=(PongGame&&) noexcept = default;

    /**
     * @brief Initialize the game
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown the game
     */
    void shutdown();

    /**
     * @brief Update game state
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Render the game
     */
    void render();

    /**
     * @brief Run the main game loop
     * @return Exit code (0 for success, non-zero for error)
     */
    int run();

private:
    /**
     * @brief Handle input events
     * @param event The input event
     */
    void handle_input(const input::InputEvent& event);

    /**
     * @brief Update player paddle based on input
     * @param delta_time Time since last frame in seconds
     */
    void update_player_paddle(float delta_time);

    /**
     * @brief Update AI paddle (simple tracking)
     * @param delta_time Time since last frame in seconds
     */
    void update_ai_paddle(float delta_time);

    /**
     * @brief Update ball physics and movement
     * @param delta_time Time since last frame in seconds
     */
    void update_ball(float delta_time);

    /**
     * @brief Check and handle collisions
     */
    void check_collisions();

    /**
     * @brief Reset ball to center with random direction
     */
    void reset_ball();

    /**
     * @brief Update score display
     */
    void update_score();

    /**
     * @brief Create game entities (paddles, ball, camera)
     */
    void create_entities();

    /**
     * @brief Create scene with proper lighting and camera
     */
    void create_scene();

private:
    Engine* m_engine;
    std::unique_ptr<scene::SceneManager> m_scene_manager;
    scene::Scene* m_scene;

    // Game entities
    std::unique_ptr<ecs::Entity> m_camera_entity;
    std::unique_ptr<ecs::Entity> m_player_paddle;
    std::unique_ptr<ecs::Entity> m_ai_paddle;
    std::unique_ptr<ecs::Entity> m_ball;

    // Game state
    bool m_initialized;
    bool m_running;

    // Ball physics
    struct BallState {
        float x, y, z;
        float velocity_x, velocity_y, velocity_z;
        float radius;
    } m_ball_state;

    // Paddle state
    struct PaddleState {
        float x, y, z;
        float width, height, depth;
        float speed;
    } m_player_paddle_state, m_ai_paddle_state;

    // Game boundaries
    struct GameBounds {
        float left, right;
        float top, bottom;
        float front, back;
    } m_bounds;

    // Scoring
    int m_player_score;
    int m_ai_score;

    // Constants
    static constexpr float PADDLE_SPEED = 8.0f;
    static constexpr float BALL_SPEED = 6.0f;
    static constexpr float BALL_SPEED_INCREMENT = 0.5f;
    static constexpr float AI_PADDLE_SPEED = 4.0f;
    static constexpr float AI_REACTION_DELAY = 0.1f;
    static constexpr float WINNING_SCORE = 10;
};

} // namespace game
} // namespace omnicpp
