/**
 * @file DemoGame.hpp
 * @brief Demo game class with basic 3D scene
 * @version 1.0.0
 */

#pragma once

#include "engine/IEngine.hpp"
#include "engine/scene/Scene.hpp"
#include "engine/scene/SceneManager.hpp"
#include "engine/ecs/Entity.hpp"
#include "engine/ecs/Camera/CameraComponent.hpp"
#include <memory>

namespace omnicpp {
namespace game {

// Forward declarations
class IEngine;
namespace ecs {
    class Entity;
    class TransformComponent;
    class MeshComponent;
}
namespace scene {
    class Scene;
    class SceneManager;
}
namespace input {
    class InputEvent;
}

/**
 * @brief Demo game class with basic 3D scene
 * 
 * Implements a simple demo with a camera and a rotating cube.
 */
class DemoGame {
public:
    /**
     * @brief Construct a new Demo Game object
     * @param engine Pointer to the engine
     */
    explicit DemoGame(IEngine* engine);

    /**
     * @brief Destroy the Demo Game object
     */
    ~DemoGame();

    // Disable copying
    DemoGame(const DemoGame&) = delete;
    DemoGame& operator=(const DemoGame&) = delete;

    // Enable moving
    DemoGame(DemoGame&&) noexcept = default;
    DemoGame& operator=(DemoGame&&) noexcept = default;

    /**
     * @brief Initialize the demo game
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown the demo game
     */
    void shutdown();

    /**
     * @brief Update the demo game
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Render the demo game
     */
    void render();

    /**
     * @brief Run the demo game loop
     * @return Exit code (0 for success)
     */
    int run();

private:
    /**
     * @brief Handle input events
     * @param event The input event
     */
    void handle_input(const input::InputEvent& event);

    /**
     * @brief Update camera based on input
     * @param delta_time Time since last frame in seconds
     */
    void update_camera(float delta_time);

private:
    IEngine* m_engine = nullptr;
    std::unique_ptr<scene::SceneManager> m_scene_manager;
    scene::Scene* m_scene = nullptr;
    std::unique_ptr<ecs::Entity> m_camera_entity;
    std::unique_ptr<ecs::Entity> m_cube_entity;
    bool m_initialized = false;
    bool m_running = false;
};

} // namespace game
} // namespace omnicpp
