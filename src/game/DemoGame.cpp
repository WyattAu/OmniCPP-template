/**
 * @file DemoGame.cpp
 * @brief Demo game implementation with basic 3D scene
 * @version 1.0.0
 */

#include "game/DemoGame.hpp"
#include "engine/ecs/Entity.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include "engine/ecs/MeshComponent.hpp"
#include "engine/ecs/Camera/CameraComponent.hpp"
#include "engine/scene/Scene.hpp"
#include "engine/scene/SceneManager.hpp"
#include "engine/input/InputManager.hpp"
#include "engine/IRenderer.hpp"
#include "engine/IEngine.hpp"
#include <iostream>
#include <cmath>

namespace omnicpp {
namespace game {

DemoGame::DemoGame(IEngine* engine)
    : m_engine(engine) {
}

DemoGame::~DemoGame() {
    shutdown();
}

bool DemoGame::initialize() {
    std::cout << "Initializing demo game..." << std::endl;

    // Get engine subsystems
    auto renderer = m_engine->get_renderer();
    auto input_manager = m_engine->get_input_manager();
    auto resource_manager = m_engine->get_resource_manager();

    if (!renderer || !input_manager || !resource_manager) {
        std::cerr << "Failed to get engine subsystems" << std::endl;
        return false;
    }

    // Create scene manager
    m_scene_manager = std::make_unique<SceneManager>();

    // Create main scene
    m_scene = std::make_unique<Scene>("MainScene");
    m_scene_manager->add_scene(std::move(m_scene));
    m_scene_manager->load_scene("MainScene");

    // Create camera entity
    m_camera_entity = std::make_unique<Entity>(1, "MainCamera");
    auto camera_component = m_camera_entity->add_component<CameraComponent>(
        CameraType::PERSPECTIVE,
        60.0f,  // FOV
        0.1f,   // Near plane
        100.0f   // Far plane
    );
    auto camera_transform = m_camera_entity->add_component<TransformComponent>();
    camera_transform->set_position(Vec3{0.0f, 2.0f, 5.0f});
    camera_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});

    m_scene->add_entity(std::move(m_camera_entity));
    m_scene->set_active_camera(camera_component);

    // Create cube entity
    m_cube_entity = std::make_unique<Entity>(2, "Cube");
    auto cube_transform = m_cube_entity->add_component<TransformComponent>();
    cube_transform->set_position(Vec3{0.0f, 0.0f, 0.0f});
    cube_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});
    cube_transform->set_scale(Vec3{1.0f, 1.0f, 1.0f});

    // Note: Mesh component would be added when mesh loading is implemented
    // For now, we just have the transform

    m_scene->add_entity(std::move(m_cube_entity));

    // Register input callback
    input_manager->register_callback([this](const input::InputEvent& event) {
        this->handle_input(event);
    });

    m_initialized = true;
    std::cout << "Demo game initialized successfully" << std::endl;
    return true;
}

void DemoGame::shutdown() {
    if (!m_initialized) {
        return;
    }

    std::cout << "Shutting down demo game..." << std::endl;

    m_scene_manager->unload_scene();
    m_scene_manager.reset();
    m_camera_entity.reset();
    m_cube_entity.reset();

    m_initialized = false;
}

void DemoGame::update(float delta_time) {
    if (!m_initialized) {
        return;
    }

    // Update scene
    m_scene_manager->update(delta_time);

    // Update camera based on input
    update_camera(delta_time);

    // Rotate cube
    auto cube_transform = m_cube_entity->get_component<TransformComponent>();
    if (cube_transform) {
        Vec3 rotation = cube_transform->get_rotation();
        rotation.y += 30.0f * delta_time;  // Rotate 30 degrees per second
        cube_transform->set_rotation(rotation);
    }
}

void DemoGame::render() {
    if (!m_initialized) {
        return;
    }

    // Render scene
    m_scene_manager->render();
}

void DemoGame::handle_input(const input::InputEvent& event) {
    if (event.type == input::EventType::KEY_PRESS) {
        if (event.key_code == input::KeyCode::ESCAPE) {
            spdlog::info("DemoGame: ESCAPE pressed, stopping game");
            m_running = false;
        }
    }
}

void DemoGame::update_camera(float delta_time) {
    auto camera_transform = m_camera_entity->get_component<TransformComponent>();
    if (!camera_transform) {
        return;
    }

    Vec3 position = camera_transform->get_position();
    Vec3 rotation = camera_transform->get_rotation();

    // Camera movement speed
    const float move_speed = 5.0f;
    const float rotate_speed = 90.0f;

    // Get input manager
    auto input_manager = m_engine->get_input_manager();

    // Forward/Backward (W/S)
    if (input_manager->is_key_pressed(input::KeyCode::W)) {
        position.z -= move_speed * delta_time;
    }
    if (input_manager->is_key_pressed(input::KeyCode::S)) {
        position.z += move_speed * delta_time;
    }

    // Left/Right (A/D)
    if (input_manager->is_key_pressed(input::KeyCode::A)) {
        position.x -= move_speed * delta_time;
    }
    if (input_manager->is_key_pressed(input::KeyCode::D)) {
        position.x += move_speed * delta_time;
    }

    // Up/Down (Space/Shift)
    if (input_manager->is_key_pressed(input::KeyCode::SPACE)) {
        position.y += move_speed * delta_time;
    }
    if (input_manager->is_key_pressed(input::KeyCode::LEFT_SHIFT)) {
        position.y -= move_speed * delta_time;
    }

    // Mouse rotation
    float mouse_delta_x, mouse_delta_y;
    input_manager->get_mouse_delta(mouse_delta_x, mouse_delta_y);

    rotation.y += mouse_delta_x * rotate_speed * delta_time;
    rotation.x += mouse_delta_y * rotate_speed * delta_time;

    // Clamp rotation
    rotation.x = std::max(-89.0f, std::min(89.0f, rotation.x));

    camera_transform->set_position(position);
    camera_transform->set_rotation(rotation);
}

int DemoGame::run() {
    if (!m_initialized) {
        spdlog::error("DemoGame: Game not initialized");
        return 1;
    }

    spdlog::info("DemoGame: Starting demo game loop...");
    spdlog::info("DemoGame: Controls:");
    spdlog::info("DemoGame:   W/S - Move Forward/Backward");
    spdlog::info("DemoGame:   A/D - Move Left/Right");
    spdlog::info("DemoGame:   Space/Shift - Move Up/Down");
    spdlog::info("DemoGame:   Mouse - Look around");
    spdlog::info("DemoGame:   ESC - Exit");

    m_running = true;

    // Simple game loop
    while (m_running) {
        float delta_time = 0.016f;  // 60 FPS

        // Process input
        auto input_manager = m_engine->get_input_manager();
        input_manager->process_events();

        // Update game
        update(delta_time);

        // Render
        render();

        // Update engine
        m_engine->update(delta_time);
    }

    spdlog::info("DemoGame: Demo game loop ended");
    return 0;
}

} // namespace game
} // namespace omnicpp
