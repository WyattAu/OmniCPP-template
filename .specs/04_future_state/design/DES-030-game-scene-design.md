# DES-030: Game Scene Design

## Overview
Defines the game scene design for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_GAME_SCENE_DESIGN_H
#define OMNICPP_GAME_SCENE_DESIGN_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace omnicpp {
namespace game {

// Forward declarations
class IGameScene;
class IGameObject;
class IGameCamera;
class IGameLight;

// Game scene configuration
struct GameSceneConfig {
    std::string name;
    std::string description;
    bool enable_physics;
    bool enable_audio;
    bool enable_ai;
    bool enable_networking;
    float gravity;

    GameSceneConfig()
        : name("UntitledScene")
        , description("")
        , enable_physics(true)
        , enable_audio(true)
        , enable_ai(true)
        , enable_networking(false)
        , gravity(-9.81f)
    {}
};

// Game scene state
enum class GameSceneState {
    UNLOADED,
    LOADING,
    LOADED,
    ACTIVE,
    PAUSED,
    UNLOADING
};

// Game scene type
enum class GameSceneType {
    MENU,
    GAMEPLAY,
    CUTSCENE,
    LOADING,
    PAUSE,
    SETTINGS,
    CREDITS
};

// Game scene statistics
struct GameSceneStats {
    uint32_t game_objects;
    uint32_t active_objects;
    uint32_t cameras;
    uint32_t lights;
    double load_time;
    double update_time;
    double render_time;

    GameSceneStats()
        : game_objects(0)
        , active_objects(0)
        , cameras(0)
        , lights(0)
        , load_time(0.0)
        , update_time(0.0)
        , render_time(0.0)
    {}
};

// Game scene interface
class IGameScene {
public:
    virtual ~IGameScene() = default;

    // Scene lifecycle
    virtual bool load() = 0;
    virtual void unload() = 0;
    virtual void initialize() = 0;
    virtual void shutdown() = 0;

    // Scene update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // Scene state
    virtual GameSceneState get_state() const = 0;
    virtual void set_state(GameSceneState state) = 0;

    // Scene type
    virtual GameSceneType get_type() const = 0;
    virtual void set_type(GameSceneType type) = 0;

    // Scene configuration
    virtual const GameSceneConfig& get_config() const = 0;
    virtual void set_config(const GameSceneConfig& config) = 0;

    // Game objects
    virtual uint32_t create_game_object(const std::string& name) = 0;
    virtual void destroy_game_object(uint32_t object_id) = 0;
    virtual IGameObject* get_game_object(uint32_t object_id) = 0;
    virtual const IGameObject* get_game_object(uint32_t object_id) const = 0;
    virtual IGameObject* get_game_object_by_name(const std::string& name) = 0;
    virtual const IGameObject* get_game_object_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_game_objects() const = 0;
    virtual std::vector<uint32_t> get_active_game_objects() const = 0;

    // Cameras
    virtual uint32_t create_camera(const std::string& name) = 0;
    virtual void destroy_camera(uint32_t camera_id) = 0;
    virtual IGameCamera* get_camera(uint32_t camera_id) = 0;
    virtual const IGameCamera* get_camera(uint32_t camera_id) const = 0;
    virtual IGameCamera* get_camera_by_name(const std::string& name) = 0;
    virtual const IGameCamera* get_camera_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_cameras() const = 0;
    virtual void set_active_camera(uint32_t camera_id) = 0;
    virtual uint32_t get_active_camera() const = 0;

    // Lights
    virtual uint32_t create_light(const std::string& name) = 0;
    virtual void destroy_light(uint32_t light_id) = 0;
    virtual IGameLight* get_light(uint32_t light_id) = 0;
    virtual const IGameLight* get_light(uint32_t light_id) const = 0;
    virtual IGameLight* get_light_by_name(const std::string& name) = 0;
    virtual const IGameLight* get_light_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_lights() const = 0;

    // Scene properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;

    // Scene serialization
    virtual std::string serialize() const = 0;
    virtual bool deserialize(const std::string& data) = 0;
    virtual bool save_to_file(const std::string& path) const = 0;
    virtual bool load_from_file(const std::string& path) = 0;

    // Statistics
    virtual const GameSceneStats& get_stats() const = 0;
    virtual void reset_stats() = 0;
};

// Game object interface
class IGameObject {
public:
    virtual ~IGameObject() = default;

    // Object lifecycle
    virtual void initialize() = 0;
    virtual void shutdown() = 0;

    // Object update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;

    // Object state
    virtual void set_active(bool active) = 0;
    virtual bool is_active() const = 0;
    virtual void set_visible(bool visible) = 0;
    virtual bool is_visible() const = 0;

    // Object transform
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void set_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;
    virtual void set_scale(float x, float y, float z) = 0;
    virtual void get_scale(float& x, float& y, float& z) const = 0;

    // Object hierarchy
    virtual void set_parent(IGameObject* parent) = 0;
    virtual IGameObject* get_parent() const = 0;
    virtual void add_child(IGameObject* child) = 0;
    virtual void remove_child(IGameObject* child) = 0;
    virtual std::vector<IGameObject*> get_children() const = 0;

    // Object properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;

    // Object tags
    virtual void add_tag(const std::string& tag) = 0;
    virtual void remove_tag(const std::string& tag) = 0;
    virtual bool has_tag(const std::string& tag) const = 0;
    virtual std::vector<std::string> get_tags() const = 0;
    virtual void clear_tags() = 0;

    // Object layers
    virtual void set_layer(int layer) = 0;
    virtual int get_layer() const = 0;
    virtual bool is_in_layer(int layer) const = 0;

    // User data
    virtual void set_user_data(void* data) = 0;
    virtual void* get_user_data() const = 0;
};

// Game camera interface
class IGameCamera {
public:
    virtual ~IGameCamera() = default;

    // Camera transform
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void set_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;

    // Camera properties
    virtual void set_fov(float fov) = 0;
    virtual float get_fov() const = 0;
    virtual void set_near_plane(float near_plane) = 0;
    virtual float get_near_plane() const = 0;
    virtual void set_far_plane(float far_plane) = 0;
    virtual float get_far_plane() const = 0;
    virtual void set_aspect_ratio(float aspect_ratio) = 0;
    virtual float get_aspect_ratio() const = 0;

    // Camera mode
    virtual void set_orthographic(bool orthographic) = 0;
    virtual bool is_orthographic() const = 0;
    virtual void set_ortho_size(float size) = 0;
    virtual float get_ortho_size() const = 0;

    // Camera target
    virtual void set_target(IGameObject* target) = 0;
    virtual IGameObject* get_target() const = 0;
    virtual void set_follow_speed(float speed) = 0;
    virtual float get_follow_speed() const = 0;

    // Camera shake
    virtual void set_shake_intensity(float intensity) = 0;
    virtual float get_shake_intensity() const = 0;
    virtual void set_shake_duration(float duration) = 0;
    virtual float get_shake_duration() const = 0;

    // Camera update
    virtual void update(double delta_time) = 0;
};

// Game light interface
class IGameLight {
public:
    virtual ~IGameLight() = default;

    // Light type
    enum class Type {
        DIRECTIONAL,
        POINT,
        SPOT,
        AMBIENT
    };

    virtual void set_type(Type type) = 0;
    virtual Type get_type() const = 0;

    // Light transform
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void set_direction(float x, float y, float z) = 0;
    virtual void get_direction(float& x, float& y, float& z) const = 0;

    // Light properties
    virtual void set_color(float r, float g, float b) = 0;
    virtual void get_color(float& r, float& g, float& b) const = 0;
    virtual void set_intensity(float intensity) = 0;
    virtual float get_intensity() const = 0;
    virtual void set_range(float range) = 0;
    virtual float get_range() const = 0;

    // Spot light properties
    virtual void set_spot_angle(float angle) = 0;
    virtual float get_spot_angle() const = 0;
    virtual void set_spot_falloff(float falloff) = 0;
    virtual float get_spot_falloff() const = 0;

    // Light shadows
    virtual void set_cast_shadows(bool cast_shadows) = 0;
    virtual bool casts_shadows() const = 0;
    virtual void set_shadow_bias(float bias) = 0;
    virtual float get_shadow_bias() const = 0;

    // Light update
    virtual void update(double delta_time) = 0;
};

// Game scene factory
class IGameSceneFactory {
public:
    virtual ~IGameSceneFactory() = default;

    virtual std::unique_ptr<IGameScene> create_scene() = 0;
    virtual void destroy_scene(std::unique_ptr<IGameScene> scene) = 0;
};

} // namespace game
} // namespace omnicpp

#endif // OMNICPP_GAME_SCENE_DESIGN_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces
- `DES-028` - Scene Manager Interface
- `DES-029` - Game Core Interfaces

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects

## Related Requirements
- REQ-047: Game Scene Management
- REQ-048: Game Object Management

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Game Scene Design
1. Abstract game scene interface
2. Support multiple scene types
3. Game object management
4. Camera and light management

### Game Objects
1. Object lifecycle
2. Transform hierarchy
3. Tags and layers
4. User data

### Game Cameras
1. Camera transform
2. Camera properties
3. Camera modes
4. Camera effects

### Game Lights
1. Light types
2. Light properties
3. Shadow casting
4. Light updates

## Usage Example

```cpp
#include "game_scene_design.hpp"

using namespace omnicpp::game;

int main() {
    // Create game scene configuration
    GameSceneConfig config;
    config.name = "MainMenu";
    config.description = "Main menu scene";
    config.enable_physics = false;
    config.enable_audio = true;
    config.enable_ai = false;

    // Create game scene
    auto scene = std::make_unique<GameScene>();
    scene->set_config(config);

    // Initialize scene
    scene->initialize();

    // Load scene
    if (!scene->load()) {
        std::cerr << "Failed to load scene" << std::endl;
        return 1;
    }

    // Create game object
    uint32_t object_id = scene->create_game_object("Player");
    IGameObject* player = scene->get_game_object(object_id);

    // Set object position
    player->set_position(0.0f, 0.0f, 0.0f);

    // Add tag
    player->add_tag("Player");
    player->add_tag("Controllable");

    // Set layer
    player->set_layer(1);

    // Create camera
    uint32_t camera_id = scene->create_camera("MainCamera");
    IGameCamera* camera = scene->get_camera(camera_id);

    // Set camera position
    camera->set_position(0.0f, 5.0f, 10.0f);
    camera->set_fov(60.0f);
    camera->set_near_plane(0.1f);
    camera->set_far_plane(1000.0f);

    // Set active camera
    scene->set_active_camera(camera_id);

    // Create light
    uint32_t light_id = scene->create_light("SunLight");
    IGameLight* light = scene->get_light(light_id);

    // Set light properties
    light->set_type(IGameLight::Type::DIRECTIONAL);
    light->set_direction(0.0f, -1.0f, 0.0f);
    light->set_color(1.0f, 1.0f, 1.0f);
    light->set_intensity(1.0f);
    light->set_cast_shadows(true);

    // Update scene
    double delta_time = 0.016; // 60 FPS
    scene->update(delta_time);
    scene->render();

    // Get statistics
    const GameSceneStats& stats = scene->get_stats();
    std::cout << "Game objects: " << stats.game_objects << std::endl;
    std::cout << "Active objects: " << stats.active_objects << std::endl;
    std::cout << "Cameras: " << stats.cameras << std::endl;
    std::cout << "Lights: " << stats.lights << std::endl;

    // Cleanup
    scene->destroy_game_object(object_id);
    scene->destroy_camera(camera_id);
    scene->destroy_light(light_id);
    scene->unload();
    scene->shutdown();

    return 0;
}
```
