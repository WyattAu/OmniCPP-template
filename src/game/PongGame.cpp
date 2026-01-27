/**
 * @file PongGame.cpp
 * @brief 3D Pong game implementation with complete gameplay loop
 * @version 1.0.0
 */

#include "game/PongGame.hpp"
#include "engine/ecs/Entity.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include "engine/ecs/Camera/CameraComponent.hpp"
#include "engine/scene/Scene.hpp"
#include "engine/scene/SceneManager.hpp"
#include "engine/input/InputManager.hpp"
#include "engine/Engine.hpp"
#include "engine/IRenderer.hpp"
#include "engine/IInputManager.hpp"
#include "engine/IResourceManager.hpp"
#include "engine/ILogger.hpp"
#include "engine/IPlatform.hpp"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <spdlog/spdlog.h>

namespace omnicpp {
namespace game {

PongGame::PongGame(Engine* engine)
    : m_engine(engine)
    , m_scene(nullptr)
    , m_initialized(false)
    , m_running(false)
    , m_player_score(0)
    , m_ai_score(0) {

    // Initialize random seed
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    spdlog::debug("PongGame: Constructor called");
}

PongGame::~PongGame() {
    shutdown();
}

bool PongGame::initialize() {
    spdlog::info("PongGame: Initializing 3D Pong game...");

    // Get engine subsystems
    auto renderer = m_engine->get_renderer();
    auto input_manager = m_engine->get_input_manager();
    auto resource_manager = m_engine->get_resource_manager();

    if (!renderer || !input_manager || !resource_manager) {
        spdlog::error("PongGame: Failed to get engine subsystems");
        return false;
    }

    // Create scene manager
    m_scene_manager = std::make_unique<SceneManager>();

    // Create main scene
    m_scene = new Scene("PongScene");
    m_scene_manager->add_scene(std::unique_ptr<scene::Scene>(m_scene));
    m_scene_manager->load_scene("PongScene");

    // Create scene with camera and entities
    create_scene();
    create_entities();

    // Register input callback
    input_manager->register_callback([this](const input::InputEvent& event) {
        this->handle_input(event);
    });

    // Initialize game state
    m_initialized = true;
    spdlog::info("PongGame: 3D Pong game initialized successfully");
    spdlog::info("PongGame: Controls:");
    spdlog::info("PongGame:   W - Move paddle up");
    spdlog::info("PongGame:   S - Move paddle down");
    spdlog::info("PongGame:   ESC - Exit game");
    spdlog::info("PongGame: First to {} points wins!", WINNING_SCORE);

    return true;
}

void PongGame::shutdown() {
    if (!m_initialized) {
        return;
    }

    spdlog::info("PongGame: Shutting down 3D Pong game...");

    m_scene_manager->unload_scene();
    m_scene_manager.reset();
    m_camera_entity.reset();
    m_player_paddle.reset();
    m_ai_paddle.reset();
    m_ball.reset();

    m_initialized = false;
    spdlog::info("PongGame: Shutdown complete");
}

void PongGame::create_scene() {
    // Create camera entity
    m_camera_entity = std::make_unique<ecs::Entity>(1, "MainCamera");
    auto camera_component = m_camera_entity->add_component<ecs::CameraComponent>(
        CameraType::PERSPECTIVE,
        60.0f,  // FOV
        0.1f,   // Near plane
        100.0f   // Far plane
    );
    auto camera_transform = m_camera_entity->add_component<ecs::TransformComponent>();
    camera_transform->set_position(Vec3{0.0f, 0.0f, 15.0f});
    camera_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});

    m_scene->add_entity(std::move(m_camera_entity));
    m_scene->set_active_camera(camera_component);

    // Set game boundaries
    m_bounds.left = -10.0f;
    m_bounds.right = 10.0f;
    m_bounds.top = 6.0f;
    m_bounds.bottom = -6.0f;
    m_bounds.front = -2.0f;
    m_bounds.back = 2.0f;
}

void PongGame::create_entities() {
    // Create player paddle (left side)
    m_player_paddle = std::make_unique<ecs::Entity>(2, "PlayerPaddle");
    auto player_transform = m_player_paddle->add_component<ecs::TransformComponent>();
    player_transform->set_position(Vec3{-9.0f, 0.0f, 0.0f});
    player_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});
    player_transform->set_scale(Vec3{0.5f, 2.0f, 0.5f});

    m_scene->add_entity(std::move(m_player_paddle));

    // Initialize player paddle state
    m_player_paddle_state.x = -9.0f;
    m_player_paddle_state.y = 0.0f;
    m_player_paddle_state.z = 0.0f;
    m_player_paddle_state.width = 0.5f;
    m_player_paddle_state.height = 2.0f;
    m_player_paddle_state.depth = 0.5f;
    m_player_paddle_state.speed = PADDLE_SPEED;

    // Create AI paddle (right side)
    m_ai_paddle = std::make_unique<ecs::Entity>(3, "AIPaddle");
    auto ai_transform = m_ai_paddle->add_component<ecs::TransformComponent>();
    ai_transform->set_position(Vec3{9.0f, 0.0f, 0.0f});
    ai_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});
    ai_transform->set_scale(Vec3{0.5f, 2.0f, 0.5f});

    m_scene->add_entity(std::move(m_ai_paddle));

    // Initialize AI paddle state
    m_ai_paddle_state.x = 9.0f;
    m_ai_paddle_state.y = 0.0f;
    m_ai_paddle_state.z = 0.0f;
    m_ai_paddle_state.width = 0.5f;
    m_ai_paddle_state.height = 2.0f;
    m_ai_paddle_state.depth = 0.5f;
    m_ai_paddle_state.speed = AI_PADDLE_SPEED;

    // Create ball
    m_ball = std::make_unique<ecs::Entity>(4, "Ball");
    auto ball_transform = m_ball->add_component<ecs::TransformComponent>();
    ball_transform->set_position(Vec3{0.0f, 0.0f, 0.0f});
    ball_transform->set_rotation(Vec3{0.0f, 0.0f, 0.0f});
    ball_transform->set_scale(Vec3{0.3f, 0.3f, 0.3f});

    m_scene->add_entity(std::move(m_ball));

    // Initialize ball state
    reset_ball();
}

void PongGame::reset_ball() {
    m_ball_state.x = 0.0f;
    m_ball_state.y = 0.0f;
    m_ball_state.z = 0.0f;
    m_ball_state.radius = 0.3f;

    // Random initial direction (left or right)
    float direction = (std::rand() % 2 == 0) ? 1.0f : -1.0f;

    // Random angle between -45 and 45 degrees
    float angle = ((std::rand() % 90) - 45.0f) * (3.14159265f / 180.0f);

    m_ball_state.velocity_x = direction * BALL_SPEED * std::cos(angle);
    m_ball_state.velocity_y = BALL_SPEED * std::sin(angle);
    m_ball_state.velocity_z = 0.0f;

    // Update ball entity position
    auto ball_transform = m_ball->get_component<ecs::TransformComponent>();
    if (ball_transform) {
        ball_transform->set_position(Vec3{m_ball_state.x, m_ball_state.y, m_ball_state.z});
    }
}

void PongGame::update(float delta_time) {
    if (!m_initialized) {
        return;
    }

    // Update scene
    m_scene_manager->update(delta_time);

    // Update game logic
    update_player_paddle(delta_time);
    update_ai_paddle(delta_time);
    update_ball(delta_time);
    check_collisions();
}

void PongGame::update_player_paddle(float delta_time) {
    auto input_manager = m_engine->get_input_manager();
    auto paddle_transform = m_player_paddle->get_component<ecs::TransformComponent>();

    if (!paddle_transform) {
        return;
    }

    // Move paddle based on input
    if (input_manager->is_key_pressed(input::KeyCode::W)) {
        m_player_paddle_state.y += m_player_paddle_state.speed * delta_time;
    }
    if (input_manager->is_key_pressed(input::KeyCode::S)) {
        m_player_paddle_state.y -= m_player_paddle_state.speed * delta_time;
    }

    // Clamp paddle position to bounds
    float half_height = m_player_paddle_state.height / 2.0f;
    m_player_paddle_state.y = std::max(m_bounds.bottom + half_height,
                                       std::min(m_bounds.top - half_height, m_player_paddle_state.y));

    // Update entity transform
    paddle_transform->set_position(Vec3{m_player_paddle_state.x, m_player_paddle_state.y, m_player_paddle_state.z});
}

void PongGame::update_ai_paddle(float delta_time) {
    auto paddle_transform = m_ai_paddle->get_component<ecs::TransformComponent>();

    if (!paddle_transform) {
        return;
    }

    // Simple AI: move towards ball Y position
    float target_y = m_ball_state.y;
    float dy = target_y - m_ai_paddle_state.y;

    // Move towards ball with reaction delay
    if (std::abs(dy) > 0.1f) {
        float move_amount = m_ai_paddle_state.speed * delta_time;
        if (dy > 0) {
            m_ai_paddle_state.y += std::min(move_amount, dy);
        } else {
            m_ai_paddle_state.y += std::max(-move_amount, dy);
        }
    }

    // Clamp paddle position to bounds
    float half_height = m_ai_paddle_state.height / 2.0f;
    m_ai_paddle_state.y = std::max(m_bounds.bottom + half_height,
                                   std::min(m_bounds.top - half_height, m_ai_paddle_state.y));

    // Update entity transform
    paddle_transform->set_position(Vec3{m_ai_paddle_state.x, m_ai_paddle_state.y, m_ai_paddle_state.z});
}

void PongGame::update_ball(float delta_time) {
    auto ball_transform = m_ball->get_component<ecs::TransformComponent>();

    if (!ball_transform) {
        return;
    }

    // Update ball position
    m_ball_state.x += m_ball_state.velocity_x * delta_time;
    m_ball_state.y += m_ball_state.velocity_y * delta_time;
    m_ball_state.z += m_ball_state.velocity_z * delta_time;

    // Update entity transform
    ball_transform->set_position(Vec3{m_ball_state.x, m_ball_state.y, m_ball_state.z});
}

void PongGame::check_collisions() {
    // Check top and bottom wall collisions
    if (m_ball_state.y + m_ball_state.radius > m_bounds.top) {
        m_ball_state.y = m_bounds.top - m_ball_state.radius;
        m_ball_state.velocity_y = -m_ball_state.velocity_y;
    } else if (m_ball_state.y - m_ball_state.radius < m_bounds.bottom) {
        m_ball_state.y = m_bounds.bottom + m_ball_state.radius;
        m_ball_state.velocity_y = -m_ball_state.velocity_y;
    }

    // Check front and back wall collisions
    if (m_ball_state.z + m_ball_state.radius > m_bounds.back) {
        m_ball_state.z = m_bounds.back - m_ball_state.radius;
        m_ball_state.velocity_z = -m_ball_state.velocity_z;
    } else if (m_ball_state.z - m_ball_state.radius < m_bounds.front) {
        m_ball_state.z = m_bounds.front + m_ball_state.radius;
        m_ball_state.velocity_z = -m_ball_state.velocity_z;
    }

    // Check player paddle collision (left side)
    float player_half_width = m_player_paddle_state.width / 2.0f;
    float player_half_height = m_player_paddle_state.height / 2.0f;
    float player_half_depth = m_player_paddle_state.depth / 2.0f;

    if (m_ball_state.x - m_ball_state.radius < m_player_paddle_state.x + player_half_width &&
        m_ball_state.x + m_ball_state.radius > m_player_paddle_state.x - player_half_width &&
        m_ball_state.y - m_ball_state.radius < m_player_paddle_state.y + player_half_height &&
        m_ball_state.y + m_ball_state.radius > m_player_paddle_state.y - player_half_height &&
        m_ball_state.z - m_ball_state.radius < m_player_paddle_state.z + player_half_depth &&
        m_ball_state.z + m_ball_state.radius > m_player_paddle_state.z - player_half_depth) {

        // Ball hit player paddle
        m_ball_state.x = m_player_paddle_state.x + player_half_width + m_ball_state.radius;
        m_ball_state.velocity_x = std::abs(m_ball_state.velocity_x) + BALL_SPEED_INCREMENT;

        // Add some angle based on where ball hit paddle
        float hit_offset = (m_ball_state.y - m_player_paddle_state.y) / player_half_height;
        m_ball_state.velocity_y += hit_offset * 2.0f;

        // Normalize velocity
        float speed = std::sqrt(m_ball_state.velocity_x * m_ball_state.velocity_x +
                               m_ball_state.velocity_y * m_ball_state.velocity_y);
        m_ball_state.velocity_x = (m_ball_state.velocity_x / speed) * std::abs(m_ball_state.velocity_x);
        m_ball_state.velocity_y = (m_ball_state.velocity_y / speed) * std::abs(m_ball_state.velocity_x);
    }

    // Check AI paddle collision (right side)
    float ai_half_width = m_ai_paddle_state.width / 2.0f;
    float ai_half_height = m_ai_paddle_state.height / 2.0f;
    float ai_half_depth = m_ai_paddle_state.depth / 2.0f;

    if (m_ball_state.x + m_ball_state.radius > m_ai_paddle_state.x - ai_half_width &&
        m_ball_state.x - m_ball_state.radius < m_ai_paddle_state.x + ai_half_width &&
        m_ball_state.y - m_ball_state.radius < m_ai_paddle_state.y + ai_half_height &&
        m_ball_state.y + m_ball_state.radius > m_ai_paddle_state.y - ai_half_height &&
        m_ball_state.z - m_ball_state.radius < m_ai_paddle_state.z + ai_half_depth &&
        m_ball_state.z + m_ball_state.radius > m_ai_paddle_state.z - ai_half_depth) {

        // Ball hit AI paddle
        m_ball_state.x = m_ai_paddle_state.x - ai_half_width - m_ball_state.radius;
        m_ball_state.velocity_x = -std::abs(m_ball_state.velocity_x) - BALL_SPEED_INCREMENT;

        // Add some angle based on where ball hit paddle
        float hit_offset = (m_ball_state.y - m_ai_paddle_state.y) / ai_half_height;
        m_ball_state.velocity_y += hit_offset * 2.0f;

        // Normalize velocity
        float speed = std::sqrt(m_ball_state.velocity_x * m_ball_state.velocity_x +
                               m_ball_state.velocity_y * m_ball_state.velocity_y);
        m_ball_state.velocity_x = (m_ball_state.velocity_x / speed) * std::abs(m_ball_state.velocity_x);
        m_ball_state.velocity_y = (m_ball_state.velocity_y / speed) * std::abs(m_ball_state.velocity_x);
    }

    // Check scoring (ball went past paddles)
    if (m_ball_state.x < m_bounds.left) {
        // AI scores
        m_ai_score++;
        spdlog::info("PongGame: AI scores! Score: Player {} - AI {}", m_player_score, m_ai_score);
        reset_ball();
        update_score();
    } else if (m_ball_state.x > m_bounds.right) {
        // Player scores
        m_player_score++;
        spdlog::info("PongGame: Player scores! Score: Player {} - AI {}", m_player_score, m_ai_score);
        reset_ball();
        update_score();
    }
}

void PongGame::update_score() {
    // Check for win condition
    if (m_player_score >= WINNING_SCORE) {
        spdlog::info("PongGame: PLAYER WINS!");
        spdlog::info("PongGame: Final Score: Player {} - AI {}", m_player_score, m_ai_score);
        m_running = false;
    } else if (m_ai_score >= WINNING_SCORE) {
        spdlog::info("PongGame: AI WINS!");
        spdlog::info("PongGame: Final Score: Player {} - AI {}", m_player_score, m_ai_score);
        m_running = false;
    }
}

void PongGame::render() {
    if (!m_initialized) {
        return;
    }

    // Render scene
    m_scene_manager->render();
}

void PongGame::handle_input(const input::InputEvent& event) {
    if (event.type == input::EventType::KEY_PRESS) {
        if (event.key_code == input::KeyCode::ESCAPE) {
            spdlog::info("PongGame: ESCAPE pressed, stopping game");
            m_running = false;
        }
    }
}

int PongGame::run() {
    if (!m_initialized) {
        spdlog::error("PongGame: Game not initialized");
        return 1;
    }

    spdlog::info("PongGame: Starting 3D Pong game loop...");
    m_running = true;

    // Game loop
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

    spdlog::info("PongGame: 3D Pong game loop ended");
    return 0;
}

} // namespace game
} // namespace omnicpp
