# DES-028: Scene Manager Interface

## Overview
Defines scene manager interface for OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_SCENE_MANAGER_INTERFACE_H
#define OMNICPP_SCENE_MANAGER_INTERFACE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <stack>

namespace omnicpp {
namespace engine {

// Forward declarations
class IScene;
class ISceneNode;
class IEntity;

// Scene configuration
struct SceneConfig {
    int max_scenes;
    int max_nodes_per_scene;
    int max_entities_per_scene;
    bool enable_scene_caching;
    bool enable_async_loading;

    SceneConfig()
        : max_scenes(10)
        , max_nodes_per_scene(10000)
        , max_entities_per_scene(10000)
        , enable_scene_caching(true)
        , enable_async_loading(false)
    {}
};

// Scene state
enum class SceneState {
    UNLOADED,
    LOADING,
    LOADED,
    UNLOADING,
    ACTIVE,
    PAUSED
};

// Scene transition type
enum class SceneTransitionType {
    NONE,
    FADE,
    SLIDE,
    ZOOM,
    CUSTOM
};

// Scene statistics
struct SceneStats {
    uint32_t active_scenes;
    uint32_t loaded_scenes;
    uint32_t total_nodes;
    uint32_t total_entities;
    double load_time;
    double update_time;
    double render_time;

    SceneStats()
        : active_scenes(0)
        , loaded_scenes(0)
        , total_nodes(0)
        , total_entities(0)
        , load_time(0.0)
        , update_time(0.0)
        , render_time(0.0)
    {}
};

// Scene manager interface
class ISceneManager {
public:
    virtual ~ISceneManager() = default;

    // Initialization
    virtual bool initialize(const SceneConfig& config) = 0;
    virtual void shutdown() = 0;

    // Update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;

    // Scene management
    virtual uint32_t create_scene(const std::string& name) = 0;
    virtual void destroy_scene(uint32_t scene_id) = 0;
    virtual IScene* get_scene(uint32_t scene_id) = 0;
    virtual const IScene* get_scene(uint32_t scene_id) const = 0;
    virtual IScene* get_scene_by_name(const std::string& name) = 0;
    virtual const IScene* get_scene_by_name(const std::string& name) const = 0;

    // Scene loading
    virtual bool load_scene(uint32_t scene_id) = 0;
    virtual bool unload_scene(uint32_t scene_id) = 0;
    virtual bool reload_scene(uint32_t scene_id) = 0;

    // Scene activation
    virtual void set_active_scene(uint32_t scene_id) = 0;
    virtual uint32_t get_active_scene() const = 0;
    virtual void push_scene(uint32_t scene_id) = 0;
    virtual void pop_scene() = 0;
    virtual void clear_scene_stack() = 0;
    virtual std::stack<uint32_t> get_scene_stack() const = 0;

    // Scene transitions
    virtual void set_scene_transition(SceneTransitionType type, float duration) = 0;
    virtual SceneTransitionType get_scene_transition_type() const = 0;
    virtual float get_scene_transition_duration() const = 0;
    virtual bool is_transitioning() const = 0;

    // Scene queries
    virtual bool has_scene(uint32_t scene_id) const = 0;
    virtual bool has_scene_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_scenes() const = 0;
    virtual std::vector<uint32_t> get_loaded_scenes() const = 0;

    // Scene callbacks
    using SceneCallback = std::function<void(uint32_t scene_id, SceneState state)>;
    virtual void set_scene_callback(SceneCallback callback) = 0;
    virtual void clear_scene_callback() = 0;

    // Statistics
    virtual const SceneStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Configuration
    virtual const SceneConfig& get_config() const = 0;
    virtual void set_config(const SceneConfig& config) = 0;
};

// Scene interface
class IScene {
public:
    virtual ~IScene() = default;

    virtual uint32_t get_id() const = 0;
    virtual const std::string& get_name() const = 0;
    virtual SceneState get_state() const = 0;

    virtual void set_name(const std::string& name) = 0;
    virtual void set_state(SceneState state) = 0;

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

    // Scene nodes
    virtual uint32_t create_node(const std::string& name) = 0;
    virtual void destroy_node(uint32_t node_id) = 0;
    virtual ISceneNode* get_node(uint32_t node_id) = 0;
    virtual const ISceneNode* get_node(uint32_t node_id) const = 0;
    virtual ISceneNode* get_node_by_name(const std::string& name) = 0;
    virtual const ISceneNode* get_node_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_nodes() const = 0;

    // Scene entities
    virtual uint32_t create_entity(const std::string& name) = 0;
    virtual void destroy_entity(uint32_t entity_id) = 0;
    virtual IEntity* get_entity(uint32_t entity_id) = 0;
    virtual const IEntity* get_entity(uint32_t entity_id) const = 0;
    virtual IEntity* get_entity_by_name(const std::string& name) = 0;
    virtual const IEntity* get_entity_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_all_entities() const = 0;

    // Root node
    virtual ISceneNode* get_root_node() = 0;
    virtual const ISceneNode* get_root_node() const = 0;

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
};

// Scene node interface
class ISceneNode {
public:
    virtual ~ISceneNode() = default;

    virtual uint32_t get_id() const = 0;
    virtual const std::string& get_name() const = 0;

    virtual void set_name(const std::string& name) = 0;

    // Transform
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void set_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;
    virtual void set_scale(float x, float y, float z) = 0;
    virtual void get_scale(float& x, float& y, float& z) const = 0;

    // Parent/child
    virtual void set_parent(ISceneNode* parent) = 0;
    virtual ISceneNode* get_parent() const = 0;
    virtual void add_child(ISceneNode* child) = 0;
    virtual void remove_child(ISceneNode* child) = 0;
    virtual std::vector<ISceneNode*> get_children() const = 0;
    virtual bool has_children() const = 0;

    // Entity
    virtual void set_entity(IEntity* entity) = 0;
    virtual IEntity* get_entity() const = 0;
    virtual bool has_entity() const = 0;

    // Visibility
    virtual void set_visible(bool visible) = 0;
    virtual bool is_visible() const = 0;

    // Active
    virtual void set_active(bool active) = 0;
    virtual bool is_active() const = 0;

    // User data
    virtual void set_user_data(void* data) = 0;
    virtual void* get_user_data() const = 0;

    // Node properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;
};

// Entity interface
class IEntity {
public:
    virtual ~IEntity() = default;

    virtual uint32_t get_id() const = 0;
    virtual const std::string& get_name() const = 0;

    virtual void set_name(const std::string& name) = 0;

    // Components
    virtual void add_component(uint32_t component_id) = 0;
    virtual void remove_component(uint32_t component_id) = 0;
    virtual bool has_component(uint32_t component_id) const = 0;
    virtual std::vector<uint32_t> get_components() const = 0;

    // Scene node
    virtual void set_scene_node(ISceneNode* node) = 0;
    virtual ISceneNode* get_scene_node() const = 0;

    // Active
    virtual void set_active(bool active) = 0;
    virtual bool is_active() const = 0;

    // User data
    virtual void set_user_data(void* data) = 0;
    virtual void* get_user_data() const = 0;

    // Entity properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;
};

// Scene manager factory
class ISceneManagerFactory {
public:
    virtual ~ISceneManagerFactory() = default;

    virtual std::unique_ptr<ISceneManager> create_scene_manager() = 0;
    virtual void destroy_scene_manager(std::unique_ptr<ISceneManager> scene_manager) = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_SCENE_MANAGER_INTERFACE_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces
- `DES-022` - ECS Component Design

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects
- `stack` - Stack container

## Related Requirements
- REQ-043: Scene Management
- REQ-044: Scene Transitions

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Scene Manager Design
1. Abstract scene management
2. Support multiple scenes
3. Scene stack for navigation
4. Scene transitions

### Scene Lifecycle
1. Load and unload scenes
2. Initialize and shutdown scenes
3. Update and render scenes
4. Pause and resume scenes

### Scene Graph
1. Hierarchical node structure
2. Parent-child relationships
3. Transform propagation
4. Entity attachment

### Scene Transitions
1. Fade transitions
2. Slide transitions
3. Zoom transitions
4. Custom transitions

## Usage Example

```cpp
#include "scene_manager_interface.hpp"

using namespace omnicpp::engine;

int main() {
    // Create scene configuration
    SceneConfig config;
    config.max_scenes = 10;
    config.max_nodes_per_scene = 10000;
    config.max_entities_per_scene = 10000;
    config.enable_scene_caching = true;

    // Create scene manager
    auto scene_manager = std::make_unique<SceneManager>();

    // Initialize scene manager
    if (!scene_manager->initialize(config)) {
        std::cerr << "Failed to initialize scene manager" << std::endl;
        return 1;
    }

    // Create scenes
    uint32_t menu_scene_id = scene_manager->create_scene("MenuScene");
    uint32_t game_scene_id = scene_manager->create_scene("GameScene");
    uint32_t settings_scene_id = scene_manager->create_scene("SettingsScene");

    // Load scenes
    scene_manager->load_scene(menu_scene_id);
    scene_manager->load_scene(game_scene_id);
    scene_manager->load_scene(settings_scene_id);

    // Set active scene
    scene_manager->set_active_scene(menu_scene_id);

    // Set scene callback
    scene_manager->set_scene_callback([](uint32_t scene_id, SceneState state) {
        if (state == SceneState::LOADED) {
            std::cout << "Scene " << scene_id << " loaded" << std::endl;
        } else if (state == SceneState::UNLOADED) {
            std::cout << "Scene " << scene_id << " unloaded" << std::endl;
        }
    });

    // Get active scene
    IScene* active_scene = scene_manager->get_scene(scene_manager->get_active_scene());

    // Create scene node
    uint32_t node_id = active_scene->create_node("PlayerNode");
    ISceneNode* node = active_scene->get_node(node_id);

    // Set node position
    node->set_position(0.0f, 0.0f, 0.0f);

    // Create entity
    uint32_t entity_id = active_scene->create_entity("PlayerEntity");
    IEntity* entity = active_scene->get_entity(entity_id);

    // Attach entity to node
    node->set_entity(entity);
    entity->set_scene_node(node);

    // Set scene transition
    scene_manager->set_scene_transition(SceneTransitionType::FADE, 1.0f);

    // Push scene to stack
    scene_manager->push_scene(game_scene_id);

    // Update scene manager
    double delta_time = 0.016; // 60 FPS
    scene_manager->update(delta_time);
    scene_manager->render();

    // Pop scene
    scene_manager->pop_scene();

    // Get statistics
    const SceneStats& stats = scene_manager->get_stats();
    std::cout << "Active scenes: " << stats.active_scenes << std::endl;
    std::cout << "Total nodes: " << stats.total_nodes << std::endl;
    std::cout << "Total entities: " << stats.total_entities << std::endl;

    // Cleanup
    scene_manager->unload_scene(menu_scene_id);
    scene_manager->unload_scene(game_scene_id);
    scene_manager->unload_scene(settings_scene_id);
    scene_manager->destroy_scene(menu_scene_id);
    scene_manager->destroy_scene(game_scene_id);
    scene_manager->destroy_scene(settings_scene_id);
    scene_manager->shutdown();

    return 0;
}
```
