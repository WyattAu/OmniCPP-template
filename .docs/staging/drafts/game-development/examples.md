# Examples Reference

This reference documents all available game examples in the OmniCPP-template project. Each example demonstrates different aspects of game development and serves as a learning resource.

## Overview

| Example | Location | Complexity | Demonstrates |
|----------|-----------|-------------|--------------|
| **simple_game** | [`examples/simple_game/`](examples/simple_game/) | Beginner | Basic engine usage and game loop |
| **DemoGame** | [`src/game/DemoGame.cpp`](src/game/DemoGame.cpp) | Intermediate | 3D scene, camera control, entity management |
| **PongGame** | [`src/game/PongGame.cpp`](src/game/PongGame.cpp) | Advanced | Complete game with physics, AI, scoring |

## simple_game Example

### Location

- **Source**: [`examples/simple_game/main.cpp`](examples/simple_game/main.cpp)
- **CMake**: [`examples/simple_game/CMakeLists.txt`](examples/simple_game/CMakeLists.txt)

### Description

The simplest example demonstrating how to use the OmniCPP engine. It creates an engine instance and runs a basic game loop for 100 frames.

### What It Demonstrates

- Engine configuration with [`EngineConfig`](include/engine/IEngine.hpp:26)
- Engine creation using [`create_engine()`](include/engine/Engine.hpp:48)
- Basic game loop with update and render calls
- Engine shutdown and cleanup

### Code Structure

```cpp
// From examples/simple_game/main.cpp
int main(int argc, char* argv[]) {
    // Create engine configuration
    omnicpp::EngineConfig config;
    config.renderer = nullptr;
    config.input_manager = nullptr;
    config.audio_manager = nullptr;
    config.physics_engine = nullptr;
    config.resource_manager = nullptr;
    config.logger = nullptr;
    config.platform = nullptr;
    
    // Create engine
    omnicpp::IEngine* engine = omnicpp::create_engine(config);
    if (!engine) {
        std::cerr << "Failed to create engine!" << std::endl;
        return 1;
    }
    
    // Simple game loop
    const float delta_time = 0.016f;  // 60 FPS
    for (int i = 0; i < 100; ++i) {
        engine->update(delta_time);
        engine->render();
    }
    
    // Cleanup
    engine->shutdown();
    omnicpp::destroy_engine(engine);
    
    return 0;
}
```

### How to Run

```bash
# Build the example
python OmniCppController.py build --target simple_game

# Run the example
python OmniCppController.py run --target simple_game
```

### Key Takeaways

- Engine configuration uses `nullptr` for default subsystems
- Always check if engine creation succeeded
- Call `shutdown()` before `destroy_engine()`
- Use delta time for frame-rate independence

### Known Limitations

- No visual output (just runs the loop)
- No input handling
- No entities or scenes
- Fixed frame count (100 frames)

## DemoGame Example

### Location

- **Header**: [`include/game/DemoGame.hpp`](include/game/DemoGame.hpp)
- **Source**: [`src/game/DemoGame.cpp`](src/game/DemoGame.cpp)
- **Main**: [`src/game/DemoMain.cpp`](src/game/DemoMain.cpp)

### Description

A complete 3D scene example with a rotating cube and camera controls. Demonstrates entity-component system, scene management, and input handling.

### What It Demonstrates

- Scene manager and scene creation
- Entity creation with components
- Camera setup and control
- Input callback registration
- Entity transformation (rotation)
- Game loop with proper phases

### Code Structure

```cpp
// From include/game/DemoGame.hpp
class DemoGame {
public:
    explicit DemoGame(IEngine* engine);
    ~DemoGame();
    
    bool initialize();
    void shutdown();
    void update(float delta_time);
    void render();
    int run();
    
private:
    void handle_input(const input::InputEvent& event);
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
```

### Key Features

#### Camera Control

- **W/S**: Move forward/backward
- **A/D**: Move left/right
- **Space/Shift**: Move up/down
- **Mouse**: Look around
- **ESC**: Exit game

#### Entity Management

```cpp
// Create camera entity
m_camera_entity = std::make_unique<Entity>(1, "MainCamera");
auto camera_component = m_camera_entity->add_component<CameraComponent>(
    CameraType::PERSPECTIVE, 60.0f, 0.1f, 100.0f
);
auto camera_transform = m_camera_entity->add_component<TransformComponent>();
camera_transform->set_position(Vec3{0.0f, 2.0f, 5.0f});

m_scene->add_entity(std::move(m_camera_entity));
m_scene->set_active_camera(camera_component);
```

#### Input Handling

```cpp
input_manager->register_callback([this](const input::InputEvent& event) {
    this->handle_input(event);
});
```

### How to Run

```bash
# Build the example
python OmniCppController.py build --target demo_game

# Run the example
python OmniCppController.py run --target demo_game
```

### Key Takeaways

- Use scene manager for entity organization
- Components provide modular functionality
- Input callbacks enable event-driven design
- Camera requires both component and scene setup
- Smart pointers manage memory automatically

### Known Limitations

- Cube has no mesh (just transform)
- No physics simulation
- No audio
- Single scene only

## PongGame Example

### Location

- **Header**: [`include/game/PongGame.hpp`](include/game/PongGame.hpp)
- **Source**: [`src/game/PongGame.cpp`](src/game/PongGame.cpp)
- **Main**: [`src/game/PongMain.cpp`](src/game/PongMain.cpp)

### Description

A complete 3D Pong game with player vs AI gameplay. Demonstrates physics simulation, collision detection, scoring system, and game state management.

### What It Demonstrates

- Complete game loop with all phases
- Physics simulation (ball movement, collision)
- AI opponent logic
- Scoring system
- Game state management
- Multiple entities with different behaviors
- Boundary checking and collision response

### Code Structure

```cpp
// From include/game/PongGame.hpp
class PongGame {
public:
    explicit PongGame(Engine* engine);
    ~PongGame();
    
    bool initialize();
    void shutdown();
    void update(float delta_time);
    void render();
    int run();
    
private:
    void handle_input(const input::InputEvent& event);
    void update_player_paddle(float delta_time);
    void update_ai_paddle(float delta_time);
    void update_ball(float delta_time);
    void check_collisions();
    void reset_ball();
    void update_score();
    void create_entities();
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
};
```

### Key Features

#### Controls

- **W**: Move player paddle up
- **S**: Move player paddle down
- **ESC**: Exit game

#### Game Mechanics

- **Ball Physics**: Velocity-based movement with collision response
- **Paddle Collision**: Ball bounces with angle variation based on hit position
- **Wall Collision**: Ball bounces off top/bottom walls
- **Scoring**: Ball passing paddles increments score
- **Win Condition**: First to 10 points wins

#### AI Logic

```cpp
void PongGame::update_ai_paddle(float delta_time) {
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
}
```

#### Collision Detection

```cpp
void PongGame::check_collisions() {
    // Check player paddle collision
    if (m_ball_state.x - m_ball_state.radius < m_player_paddle_state.x + player_half_width &&
        m_ball_state.x + m_ball_state.radius > m_player_paddle_state.x - player_half_width &&
        m_ball_state.y - m_ball_state.radius < m_player_paddle_state.y + player_half_height &&
        m_ball_state.y + m_ball_state.radius > m_player_paddle_state.y - player_half_height) {
        
        // Ball hit player paddle
        m_ball_state.x = m_player_paddle_state.x + player_half_width + m_ball_state.radius;
        m_ball_state.velocity_x = std::abs(m_ball_state.velocity_x) + BALL_SPEED_INCREMENT;
        
        // Add angle based on hit position
        float hit_offset = (m_ball_state.y - m_player_paddle_state.y) / player_half_height;
        m_ball_state.velocity_y += hit_offset * 2.0f;
    }
}
```

### How to Run

```bash
# Build the example
python OmniCppController.py build --target pong_game

# Run the example
python OmniCppController.py run --target pong_game
```

### Key Takeaways

- Use structs for game state organization
- Implement physics with velocity and collision
- AI can be simple (tracking) or complex (prediction)
- Separate update methods for different game objects
- Use constants for game balance (speed, bounds, scoring)

### Known Limitations

- No mesh rendering (entities exist but not visible)
- No sound effects
- AI is very basic (no prediction)
- No multiplayer support
- Fixed game bounds

## Comparison of Examples

| Feature | simple_game | DemoGame | PongGame |
|---------|-------------|------------|------------|
| Engine Creation | ✅ | ✅ | ✅ |
| Game Loop | ✅ | ✅ | ✅ |
| Input Handling | ❌ | ✅ | ✅ |
| Scene Management | ❌ | ✅ | ✅ |
| Entity System | ❌ | ✅ | ✅ |
| Camera Control | ❌ | ✅ | ✅ |
| Physics | ❌ | ❌ | ✅ |
| Collision Detection | ❌ | ❌ | ✅ |
| AI | ❌ | ❌ | ✅ |
| Scoring System | ❌ | ❌ | ✅ |
| Game States | ❌ | ❌ | ✅ |

## Building Examples

All examples use the same build system:

```bash
# Build all examples
python OmniCppController.py build

# Build specific example
python OmniCppController.py build --target <example_name>
```

### Available Targets

- `simple_game` - Basic engine usage
- `demo_game` - 3D scene with camera
- `pong_game` - Complete Pong game

## Running Examples

```bash
# Run specific example
python OmniCppController.py run --target <example_name>
```

## Common Issues

### Example Won't Build

**Problem**: CMake configuration fails for example

**Solution**: Ensure engine is built first:

```bash
python OmniCppController.py build
```

### Example Crashes on Startup

**Problem**: Application crashes immediately

**Solution**: Check:
1. Vulkan SDK is installed
2. All dependencies are linked
3. Engine library is in expected location

### No Output Visible

**Problem**: Window opens but nothing renders

**Solution**: Check:
1. Camera is set as active
2. Entities are added to scene
3. Scene is loaded
4. Renderer is initialized

### Input Not Responding

**Problem**: Keyboard/mouse input doesn't work

**Solution**: Ensure:
1. Input manager is initialized
2. Callbacks are registered
3. `process_events()` is called each frame

## Extending Examples

To extend an example:

1. **Copy the example** to a new directory
2. **Rename the class** to your game name
3. **Add new features** following the existing patterns
4. **Update CMakeLists.txt** with new source files
5. **Build and test** your changes

### Adding New Entities

```cpp
// Create new entity
auto entity = std::make_unique<Entity>(id, "EntityName");
auto transform = entity->add_component<TransformComponent>();
transform->set_position(Vec3{x, y, z});

// Add to scene
m_scene->add_entity(std::move(entity));
```

### Adding New Scenes

```cpp
// Create new scene
auto new_scene = std::make_unique<Scene>("NewScene");
m_scene_manager->add_scene(std::move(new_scene));

// Switch to new scene
m_scene_manager->load_scene("NewScene");
```

## Related Documentation

- [Creating Games Tutorial](creating-games.md) - Step-by-step game creation
- [Game Lifecycle Guide](game-lifecycle.md) - Understanding game phases
- [Game Development Overview](index.md) - Architecture and integration
- [Engine Overview](../engine/index.md) - Engine subsystems
- [ECS Architecture](../engine/ecs.md) - Entity Component System
- [Scene Management](../engine/scene-management.md) - Scene graph details
