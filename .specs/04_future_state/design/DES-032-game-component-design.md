# DES-032: Game Component Design

## Overview

Defines the game component design for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_GAME_COMPONENT_DESIGN_H
#define OMNICPP_GAME_COMPONENT_DESIGN_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <unordered_map>

namespace omnicpp {
namespace game {

// Forward declarations
class IGameComponent;
class IGameEntity;

// Component configuration
struct ComponentConfig {
    std::string type;
    std::string name;
    bool is_required;
    bool is_unique;

    ComponentConfig()
        : type("BaseComponent")
        , name("UntitledComponent")
        , is_required(false)
        , is_unique(false)
    {}
};

// Component state
enum class ComponentState {
    UNINITIALIZED,
    INITIALIZING,
    ACTIVE,
    INACTIVE,
    PAUSED,
    DESTROYING,
    DESTROYED
};

// Component statistics
struct ComponentStats {
    uint32_t entity_count;
    double update_time;
    double render_time;

    ComponentStats()
        : entity_count(0)
        , update_time(0.0)
        , render_time(0.0)
    {}
};

// Component interface
class IGameComponent {
public:
    virtual ~IGameComponent() = default;

    // Component lifecycle
    virtual void initialize() = 0;
    virtual void shutdown() = 0;
    virtual void destroy() = 0;

    // Component update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // Component state
    virtual ComponentState get_state() const = 0;
    virtual void set_state(ComponentState state) = 0;

    // Component configuration
    virtual const ComponentConfig& get_config() const = 0;
    virtual void set_config(const ComponentConfig& config) = 0;

    // Component type
    virtual const std::string& get_type() const = 0;
    virtual void set_type(const std::string& type) = 0;

    // Component name
    virtual const std::string& get_name() const = 0;
    virtual void set_name(const std::string& name) = 0;

    // Component entity
    virtual void set_entity(IGameEntity* entity) = 0;
    virtual IGameEntity* get_entity() const = 0;
    virtual bool has_entity() const = 0;

    // Component active
    virtual void set_active(bool active) = 0;
    virtual bool is_active() const = 0;

    // Component enabled
    virtual void set_enabled(bool enabled) = 0;
    virtual bool is_enabled() const = 0;

    // Component properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;

    // Component user data
    virtual void set_user_data(void* data) = 0;
    virtual void* get_user_data() const = 0;

    // Component statistics
    virtual const ComponentStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Component serialization
    virtual std::string serialize() const = 0;
    virtual bool deserialize(const std::string& data) = 0;
};

// Transform component
class TransformComponent : public IGameComponent {
private:
    float m_position_x;
    float m_position_y;
    float m_position_z;
    float m_rotation_x;
    float m_rotation_y;
    float m_rotation_z;
    float m_rotation_w;
    float m_scale_x;
    float m_scale_y;
    float m_scale_z;

public:
    TransformComponent()
        : m_position_x(0.0f)
        , m_position_y(0.0f)
        , m_position_z(0.0f)
        , m_rotation_x(0.0f)
        , m_rotation_y(0.0f)
        , m_rotation_z(0.0f)
        , m_rotation_w(1.0f)
        , m_scale_x(1.0f)
        , m_scale_y(1.0f)
        , m_scale_z(1.0f)
    {}

    void initialize() override {
        // Initialize transform component
    }

    void shutdown() override {
        // Shutdown transform component
    }

    void destroy() override {
        // Destroy transform component
    }

    void update(double delta_time) override {
        // Update transform component
    }

    void render() override {
        // Render transform component
    }

    void pause() override {
        // Pause transform component
    }

    void resume() override {
        // Resume transform component
    }

    ComponentState get_state() const override {
        return ComponentState::ACTIVE;
    }

    void set_state(ComponentState state) override {
        // Set component state
    }

    const ComponentConfig& get_config() const override {
        static ComponentConfig config;
        config.type = "TransformComponent";
        return config;
    }

    void set_config(const ComponentConfig& config) override {
        // Set component configuration
    }

    const std::string& get_type() const override {
        static std::string type = "TransformComponent";
        return type;
    }

    void set_type(const std::string& type) override {
        // Set component type
    }

    const std::string& get_name() const override {
        static std::string name = "Transform";
        return name;
    }

    void set_name(const std::string& name) override {
        // Set component name
    }

    void set_entity(IGameEntity* entity) override {
        // Set component entity
    }

    IGameEntity* get_entity() const override {
        return nullptr;
    }

    bool has_entity() const override {
        return false;
    }

    void set_active(bool active) override {
        // Set component active
    }

    bool is_active() const override {
        return true;
    }

    void set_enabled(bool enabled) override {
        // Set component enabled
    }

    bool is_enabled() const override {
        return true;
    }

    void set_property(const std::string& name, const std::string& value) override {
        // Set component property
    }

    std::string get_property(const std::string& name) const override {
        return "";
    }

    bool has_property(const std::string& name) const override {
        return false;
    }

    void clear_properties() override {
        // Clear component properties
    }

    void set_user_data(void* data) override {
        // Set component user data
    }

    void* get_user_data() const override {
        return nullptr;
    }

    const ComponentStats& get_stats() const override {
        static ComponentStats stats;
        return stats;
    }

    void reset_stats() override {
        // Reset component statistics
    }

    std::string serialize() const override {
        // Serialize component data
        return "";
    }

    bool deserialize(const std::string& data) override {
        // Deserialize component data
        return true;
    }

    // Transform methods
    void set_position(float x, float y, float z) {
        m_position_x = x;
        m_position_y = y;
        m_position_z = z;
    }

    void get_position(float& x, float& y, float& z) const {
        x = m_position_x;
        y = m_position_y;
        z = m_position_z;
    }

    void set_rotation(float x, float y, float z, float w) {
        m_rotation_x = x;
        m_rotation_y = y;
        m_rotation_z = z;
        m_rotation_w = w;
    }

    void get_rotation(float& x, float& y, float& z, float& w) const {
        x = m_rotation_x;
        y = m_rotation_y;
        z = m_rotation_z;
        w = m_rotation_w;
    }

    void set_scale(float x, float y, float z) {
        m_scale_x = x;
        m_scale_y = y;
        m_scale_z = z;
    }

    void get_scale(float& x, float& y, float& z) const {
        x = m_scale_x;
        y = m_scale_y;
        z = m_scale_z;
    }
};

// Mesh component
class MeshComponent : public IGameComponent {
private:
    std::string m_mesh_path;
    std::string m_material_path;
    bool m_visible;
    bool m_cast_shadows;
    bool m_receive_shadows;

public:
    MeshComponent()
        : m_mesh_path("")
        , m_material_path("")
        , m_visible(true)
        , m_cast_shadows(true)
        , m_receive_shadows(true)
    {}

    void initialize() override {
        // Initialize mesh component
    }

    void shutdown() override {
        // Shutdown mesh component
    }

    void destroy() override {
        // Destroy mesh component
    }

    void update(double delta_time) override {
        // Update mesh component
    }

    void render() override {
        // Render mesh component
    }

    void pause() override {
        // Pause mesh component
    }

    void resume() override {
        // Resume mesh component
    }

    ComponentState get_state() const override {
        return ComponentState::ACTIVE;
    }

    void set_state(ComponentState state) override {
        // Set component state
    }

    const ComponentConfig& get_config() const override {
        static ComponentConfig config;
        config.type = "MeshComponent";
        return config;
    }

    void set_config(const ComponentConfig& config) override {
        // Set component configuration
    }

    const std::string& get_type() const override {
        static std::string type = "MeshComponent";
        return type;
    }

    void set_type(const std::string& type) override {
        // Set component type
    }

    const std::string& get_name() const override {
        static std::string name = "Mesh";
        return name;
    }

    void set_name(const std::string& name) override {
        // Set component name
    }

    void set_entity(IGameEntity* entity) override {
        // Set component entity
    }

    IGameEntity* get_entity() const override {
        return nullptr;
    }

    bool has_entity() const override {
        return false;
    }

    void set_active(bool active) override {
        // Set component active
    }

    bool is_active() const override {
        return true;
    }

    void set_enabled(bool enabled) override {
        // Set component enabled
    }

    bool is_enabled() const override {
        return true;
    }

    void set_property(const std::string& name, const std::string& value) override {
        // Set component property
    }

    std::string get_property(const std::string& name) const override {
        return "";
    }

    bool has_property(const std::string& name) const override {
        return false;
    }

    void clear_properties() override {
        // Clear component properties
    }

    void set_user_data(void* data) override {
        // Set component user data
    }

    void* get_user_data() const override {
        return nullptr;
    }

    const ComponentStats& get_stats() const override {
        static ComponentStats stats;
        return stats;
    }

    void reset_stats() override {
        // Reset component statistics
    }

    std::string serialize() const override {
        // Serialize component data
        return "";
    }

    bool deserialize(const std::string& data) override {
        // Deserialize component data
        return true;
    }

    // Mesh methods
    void set_mesh_path(const std::string& path) {
        m_mesh_path = path;
    }

    const std::string& get_mesh_path() const {
        return m_mesh_path;
    }

    void set_material_path(const std::string& path) {
        m_material_path = path;
    }

    const std::string& get_material_path() const {
        return m_material_path;
    }

    void set_visible(bool visible) {
        m_visible = visible;
    }

    bool is_visible() const {
        return m_visible;
    }

    void set_cast_shadows(bool cast_shadows) {
        m_cast_shadows = cast_shadows;
    }

    bool casts_shadows() const {
        return m_cast_shadows;
    }

    void set_receive_shadows(bool receive_shadows) {
        m_receive_shadows = receive_shadows;
    }

    bool receives_shadows() const {
        return m_receive_shadows;
    }
};

// Audio component
class AudioComponent : public IGameComponent {
private:
    std::string m_audio_path;
    bool m_loop;
    bool m_play_on_start;
    float m_volume;
    float m_pitch;
    bool m_is_3d;
    float m_min_distance;
    float m_max_distance;

public:
    AudioComponent()
        : m_audio_path("")
        , m_loop(false)
        , m_play_on_start(false)
        , m_volume(1.0f)
        , m_pitch(1.0f)
        , m_is_3d(false)
        , m_min_distance(1.0f)
        , m_max_distance(100.0f)
    {}

    void initialize() override {
        // Initialize audio component
    }

    void shutdown() override {
        // Shutdown audio component
    }

    void destroy() override {
        // Destroy audio component
    }

    void update(double delta_time) override {
        // Update audio component
    }

    void render() override {
        // Render audio component
    }

    void pause() override {
        // Pause audio component
    }

    void resume() override {
        // Resume audio component
    }

    ComponentState get_state() const override {
        return ComponentState::ACTIVE;
    }

    void set_state(ComponentState state) override {
        // Set component state
    }

    const ComponentConfig& get_config() const override {
        static ComponentConfig config;
        config.type = "AudioComponent";
        return config;
    }

    void set_config(const ComponentConfig& config) override {
        // Set component configuration
    }

    const std::string& get_type() const override {
        static std::string type = "AudioComponent";
        return type;
    }

    void set_type(const std::string& type) override {
        // Set component type
    }

    const std::string& get_name() const override {
        static std::string name = "Audio";
        return name;
    }

    void set_name(const std::string& name) override {
        // Set component name
    }

    void set_entity(IGameEntity* entity) override {
        // Set component entity
    }

    IGameEntity* get_entity() const override {
        return nullptr;
    }

    bool has_entity() const override {
        return false;
    }

    void set_active(bool active) override {
        // Set component active
    }

    bool is_active() const override {
        return true;
    }

    void set_enabled(bool enabled) override {
        // Set component enabled
    }

    bool is_enabled() const override {
        return true;
    }

    void set_property(const std::string& name, const std::string& value) override {
        // Set component property
    }

    std::string get_property(const std::string& name) const override {
        return "";
    }

    bool has_property(const std::string& name) const override {
        return false;
    }

    void clear_properties() override {
        // Clear component properties
    }

    void set_user_data(void* data) override {
        // Set component user data
    }

    void* get_user_data() const override {
        return nullptr;
    }

    const ComponentStats& get_stats() const override {
        static ComponentStats stats;
        return stats;
    }

    void reset_stats() override {
        // Reset component statistics
    }

    std::string serialize() const override {
        // Serialize component data
        return "";
    }

    bool deserialize(const std::string& data) override {
        // Deserialize component data
        return true;
    }

    // Audio methods
    void set_audio_path(const std::string& path) {
        m_audio_path = path;
    }

    const std::string& get_audio_path() const {
        return m_audio_path;
    }

    void set_loop(bool loop) {
        m_loop = loop;
    }

    bool is_looping() const {
        return m_loop;
    }

    void set_play_on_start(bool play_on_start) {
        m_play_on_start = play_on_start;
    }

    bool should_play_on_start() const {
        return m_play_on_start;
    }

    void set_volume(float volume) {
        m_volume = volume;
    }

    float get_volume() const {
        return m_volume;
    }

    void set_pitch(float pitch) {
        m_pitch = pitch;
    }

    float get_pitch() const {
        return m_pitch;
    }

    void set_3d(bool is_3d) {
        m_is_3d = is_3d;
    }

    bool is_3d() const {
        return m_is_3d;
    }

    void set_min_distance(float distance) {
        m_min_distance = distance;
    }

    float get_min_distance() const {
        return m_min_distance;
    }

    void set_max_distance(float distance) {
        m_max_distance = distance;
    }

    float get_max_distance() const {
        return m_max_distance;
    }
};

// Script component
class ScriptComponent : public IGameComponent {
private:
    std::string m_script_path;
    std::string m_script_class;
    bool m_enabled;

public:
    ScriptComponent()
        : m_script_path("")
        , m_script_class("")
        , m_enabled(true)
    {}

    void initialize() override {
        // Initialize script component
    }

    void shutdown() override {
        // Shutdown script component
    }

    void destroy() override {
        // Destroy script component
    }

    void update(double delta_time) override {
        // Update script component
    }

    void render() override {
        // Render script component
    }

    void pause() override {
        // Pause script component
    }

    void resume() override {
        // Resume script component
    }

    ComponentState get_state() const override {
        return ComponentState::ACTIVE;
    }

    void set_state(ComponentState state) override {
        // Set component state
    }

    const ComponentConfig& get_config() const override {
        static ComponentConfig config;
        config.type = "ScriptComponent";
        return config;
    }

    void set_config(const ComponentConfig& config) override {
        // Set component configuration
    }

    const std::string& get_type() const override {
        static std::string type = "ScriptComponent";
        return type;
    }

    void set_type(const std::string& type) override {
        // Set component type
    }

    const std::string& get_name() const override {
        static std::string name = "Script";
        return name;
    }

    void set_name(const std::string& name) override {
        // Set component name
    }

    void set_entity(IGameEntity* entity) override {
        // Set component entity
    }

    IGameEntity* get_entity() const override {
        return nullptr;
    }

    bool has_entity() const override {
        return false;
    }

    void set_active(bool active) override {
        // Set component active
    }

    bool is_active() const override {
        return true;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_property(const std::string& name, const std::string& value) override {
        // Set component property
    }

    std::string get_property(const std::string& name) const override {
        return "";
    }

    bool has_property(const std::string& name) const override {
        return false;
    }

    void clear_properties() override {
        // Clear component properties
    }

    void set_user_data(void* data) override {
        // Set component user data
    }

    void* get_user_data() const override {
        return nullptr;
    }

    const ComponentStats& get_stats() const override {
        static ComponentStats stats;
        return stats;
    }

    void reset_stats() override {
        // Reset component statistics
    }

    std::string serialize() const override {
        // Serialize component data
        return "";
    }

    bool deserialize(const std::string& data) override {
        // Deserialize component data
        return true;
    }

    // Script methods
    void set_script_path(const std::string& path) {
        m_script_path = path;
    }

    const std::string& get_script_path() const {
        return m_script_path;
    }

    void set_script_class(const std::string& script_class) {
        m_script_class = script_class;
    }

    const std::string& get_script_class() const {
        return m_script_class;
    }
};

// Component manager interface
class IComponentManager {
public:
    virtual ~IComponentManager() = default;

    // Component management
    virtual uint32_t create_component(const ComponentConfig& config) = 0;
    virtual void destroy_component(uint32_t component_id) = 0;
    virtual IGameComponent* get_component(uint32_t component_id) = 0;
    virtual const IGameComponent* get_component(uint32_t component_id) const = 0;
    virtual IGameComponent* get_component_by_name(const std::string& name) = 0;
    virtual const IGameComponent* get_component_by_name(const std::string& name) const = 0;

    // Component queries
    virtual std::vector<IGameComponent*> get_all_components() const = 0;
    virtual std::vector<IGameComponent*> get_components_by_type(const std::string& type) const = 0;
    virtual std::vector<IGameComponent*> get_components_by_entity(uint32_t entity_id) const = 0;
    virtual std::vector<IGameComponent*> get_active_components() const = 0;

    // Component state
    virtual void set_component_state(uint32_t component_id, ComponentState state) = 0;
    virtual ComponentState get_component_state(uint32_t component_id) const = 0;

    // Component update
    virtual void update_components(double delta_time) = 0;
    virtual void render_components() = 0;

    // Component statistics
    virtual uint32_t get_component_count() const = 0;
    virtual uint32_t get_active_component_count() const = 0;

    // Component cleanup
    virtual void destroy_all_components() = 0;
    virtual void destroy_components_by_type(const std::string& type) = 0;
    virtual void destroy_components_by_entity(uint32_t entity_id) = 0;
};

// Component factory
class IComponentFactory {
public:
    virtual ~IComponentFactory() = default;

    virtual std::unique_ptr<IGameComponent> create_component(const ComponentConfig& config) = 0;
    virtual void destroy_component(std::unique_ptr<IGameComponent> component) = 0;
};

} // namespace game
} // namespace omnicpp

#endif // OMNICPP_GAME_COMPONENT_DESIGN_H
```

## Dependencies

### Internal Dependencies

- `DES-021` - Engine Core Interfaces
- `DES-022` - ECS Component Design
- `DES-031` - Game Entity Design

### External Dependencies

- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects
- `unordered_map` - Hash map

## Related Requirements

- REQ-051: Component Management
- REQ-052: Component Architecture

## Related ADRs

- ADR-002: C++ Engine Architecture

## Implementation Notes

### Component Design

1. Abstract component interface
2. Component-based architecture
3. Component lifecycle
4. Component serialization

### Component Types

1. Transform component
2. Mesh component
3. Audio component
4. Script component
5. Custom components

### Component Management

1. Create and destroy components
2. Query components
3. Update components
4. Render components

### Component Events

1. Component creation/destruction
2. Component state changes
3. Component property changes
4. Component entity changes

## Usage Example

```cpp
#include "game_component_design.hpp"

using namespace omnicpp::game;

int main() {
    // Create component manager
    auto component_manager = std::make_unique<ComponentManager>();

    // Create transform component
    ComponentConfig transform_config;
    transform_config.type = "TransformComponent";
    transform_config.name = "PlayerTransform";
    transform_config.is_required = true;
    transform_config.is_unique = true;

    uint32_t transform_id = component_manager->create_component(transform_config);
    IGameComponent* transform = component_manager->get_component(transform_id);

    // Cast to TransformComponent
    TransformComponent* player_transform = static_cast<TransformComponent*>(transform);
    player_transform->set_position(0.0f, 0.0f, 0.0f);
    player_transform->set_rotation(0.0f, 0.0f, 0.0f, 1.0f);
    player_transform->set_scale(1.0f, 1.0f, 1.0f);

    // Create mesh component
    ComponentConfig mesh_config;
    mesh_config.type = "MeshComponent";
    mesh_config.name = "PlayerMesh";
    mesh_config.is_required = true;
    mesh_config.is_unique = true;

    uint32_t mesh_id = component_manager->create_component(mesh_config);
    IGameComponent* mesh = component_manager->get_component(mesh_id);

    // Cast to MeshComponent
    MeshComponent* player_mesh = static_cast<MeshComponent*>(mesh);
    player_mesh->set_mesh_path("models/player.obj");
    player_mesh->set_material_path("materials/player.mat");
    player_mesh->set_visible(true);
    player_mesh->set_cast_shadows(true);

    // Create audio component
    ComponentConfig audio_config;
    audio_config.type = "AudioComponent";
    audio_config.name = "PlayerAudio";
    audio_config.is_required = false;
    audio_config.is_unique = false;

    uint32_t audio_id = component_manager->create_component(audio_config);
    IGameComponent* audio = component_manager->get_component(audio_id);

    // Cast to AudioComponent
    AudioComponent* player_audio = static_cast<AudioComponent*>(audio);
    player_audio->set_audio_path("sounds/player_footstep.wav");
    player_audio->set_loop(false);
    player_audio->set_volume(0.8f);
    player_audio->set_3d(true);

    // Create script component
    ComponentConfig script_config;
    script_config.type = "ScriptComponent";
    script_config.name = "PlayerScript";
    script_config.is_required = false;
    script_config.is_unique = true;

    uint32_t script_id = component_manager->create_component(script_config);
    IGameComponent* script = component_manager->get_component(script_id);

    // Cast to ScriptComponent
    ScriptComponent* player_script = static_cast<ScriptComponent*>(script);
    player_script->set_script_path("scripts/player.py");
    player_script->set_script_class("PlayerController");
    player_script->set_enabled(true);

    // Update components
    double delta_time = 0.016; // 60 FPS
    component_manager->update_components(delta_time);
    component_manager->render_components();

    // Get statistics
    std::cout << "Component count: " << component_manager->get_component_count() << std::endl;
    std::cout << "Active components: " << component_manager->get_active_component_count() << std::endl;

    // Cleanup
    component_manager->destroy_component(transform_id);
    component_manager->destroy_component(mesh_id);
    component_manager->destroy_component(audio_id);
    component_manager->destroy_component(script_id);
    component_manager->destroy_all_components();

    return 0;
}
```
