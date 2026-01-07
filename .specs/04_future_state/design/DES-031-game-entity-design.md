# DES-031: Game Entity Design

## Overview
Defines the game entity design for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_GAME_ENTITY_DESIGN_H
#define OMNICPP_GAME_ENTITY_DESIGN_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <unordered_map>

namespace omnicpp {
namespace game {

// Forward declarations
class IGameEntity;
class IGameComponent;
class IGameSystem;

// Entity configuration
struct EntityConfig {
    std::string name;
    std::string description;
    bool is_persistent;
    bool is_static;
    int layer;

    EntityConfig()
        : name("UntitledEntity")
        , description("")
        , is_persistent(false)
        , is_static(false)
        , layer(0)
    {}
};

// Entity state
enum class EntityState {
    UNINITIALIZED,
    INITIALIZING,
    ACTIVE,
    INACTIVE,
    PAUSED,
    DESTROYING,
    DESTROYED
};

// Entity statistics
struct EntityStats {
    uint32_t component_count;
    uint32_t child_count;
    double update_time;
    double render_time;

    EntityStats()
        : component_count(0)
        , child_count(0)
        , update_time(0.0)
        , render_time(0.0)
    {}
};

// Entity interface
class IGameEntity {
public:
    virtual ~IGameEntity() = default;

    // Entity lifecycle
    virtual void initialize() = 0;
    virtual void shutdown() = 0;
    virtual void destroy() = 0;

    // Entity update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // Entity state
    virtual EntityState get_state() const = 0;
    virtual void set_state(EntityState state) = 0;

    // Entity configuration
    virtual const EntityConfig& get_config() const = 0;
    virtual void set_config(const EntityConfig& config) = 0;

    // Entity ID
    virtual uint32_t get_id() const = 0;
    virtual void set_id(uint32_t id) = 0;

    // Entity name
    virtual const std::string& get_name() const = 0;
    virtual void set_name(const std::string& name) = 0;

    // Entity transform
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void set_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;
    virtual void set_scale(float x, float y, float z) = 0;
    virtual void get_scale(float& x, float& y, float& z) const = 0;

    // Entity hierarchy
    virtual void set_parent(IGameEntity* parent) = 0;
    virtual IGameEntity* get_parent() const = 0;
    virtual void add_child(IGameEntity* child) = 0;
    virtual void remove_child(IGameEntity* child) = 0;
    virtual std::vector<IGameEntity*> get_children() const = 0;
    virtual bool has_children() const = 0;

    // Entity components
    virtual void add_component(IGameComponent* component) = 0;
    virtual void remove_component(IGameComponent* component) = 0;
    virtual IGameComponent* get_component(const std::string& type) const = 0;
    virtual std::vector<IGameComponent*> get_components() const = 0;
    virtual bool has_component(const std::string& type) const = 0;
    virtual void clear_components() = 0;

    // Entity tags
    virtual void add_tag(const std::string& tag) = 0;
    virtual void remove_tag(const std::string& tag) = 0;
    virtual bool has_tag(const std::string& tag) const = 0;
    virtual std::vector<std::string> get_tags() const = 0;
    virtual void clear_tags() = 0;

    // Entity layer
    virtual void set_layer(int layer) = 0;
    virtual int get_layer() const = 0;
    virtual bool is_in_layer(int layer) const = 0;

    // Entity active
    virtual void set_active(bool active) = 0;
    virtual bool is_active() const = 0;

    // Entity visible
    virtual void set_visible(bool visible) = 0;
    virtual bool is_visible() const = 0;

    // Entity properties
    virtual void set_property(const std::string& name, const std::string& value) = 0;
    virtual std::string get_property(const std::string& name) const = 0;
    virtual bool has_property(const std::string& name) const = 0;
    virtual void clear_properties() = 0;

    // Entity user data
    virtual void set_user_data(void* data) = 0;
    virtual void* get_user_data() const = 0;

    // Entity statistics
    virtual const EntityStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Entity serialization
    virtual std::string serialize() const = 0;
    virtual bool deserialize(const std::string& data) = 0;
};

// Entity manager interface
class IEntityManager {
public:
    virtual ~IEntityManager() = default;

    // Entity management
    virtual uint32_t create_entity(const EntityConfig& config) = 0;
    virtual void destroy_entity(uint32_t entity_id) = 0;
    virtual IGameEntity* get_entity(uint32_t entity_id) = 0;
    virtual const IGameEntity* get_entity(uint32_t entity_id) const = 0;
    virtual IGameEntity* get_entity_by_name(const std::string& name) = 0;
    virtual const IGameEntity* get_entity_by_name(const std::string& name) const = 0;

    // Entity queries
    virtual std::vector<IGameEntity*> get_all_entities() const = 0;
    virtual std::vector<IGameEntity*> get_entities_by_tag(const std::string& tag) const = 0;
    virtual std::vector<IGameEntity*> get_entities_by_layer(int layer) const = 0;
    virtual std::vector<IGameEntity*> get_entities_by_component(const std::string& component_type) const = 0;
    virtual std::vector<IGameEntity*> get_active_entities() const = 0;
    virtual std::vector<IGameEntity*> get_visible_entities() const = 0;

    // Entity state
    virtual void set_entity_state(uint32_t entity_id, EntityState state) = 0;
    virtual EntityState get_entity_state(uint32_t entity_id) const = 0;

    // Entity update
    virtual void update_entities(double delta_time) = 0;
    virtual void render_entities() = 0;

    // Entity statistics
    virtual uint32_t get_entity_count() const = 0;
    virtual uint32_t get_active_entity_count() const = 0;
    virtual uint32_t get_component_count() const = 0;

    // Entity cleanup
    virtual void destroy_all_entities() = 0;
    virtual void destroy_entities_by_tag(const std::string& tag) = 0;
    virtual void destroy_entities_by_layer(int layer) = 0;
};

// Entity factory
class IEntityFactory {
public:
    virtual ~IEntityFactory() = default;

    virtual std::unique_ptr<IGameEntity> create_entity(const EntityConfig& config) = 0;
    virtual void destroy_entity(std::unique_ptr<IGameEntity> entity) = 0;
};

// Entity pool
class IEntityPool {
public:
    virtual ~IEntityPool() = default;

    virtual void acquire(IGameEntity* entity) = 0;
    virtual void release(IGameEntity* entity) = 0;
    virtual bool is_available(IGameEntity* entity) const = 0;
    virtual std::vector<IGameEntity*> get_available_entities() const = 0;
    virtual std::vector<IGameEntity*> get_acquired_entities() const = 0;
    virtual void clear() = 0;
};

// Entity query
struct EntityQuery {
    std::vector<std::string> required_tags;
    std::vector<std::string> excluded_tags;
    std::vector<int> layers;
    std::vector<std::string> required_components;
    std::vector<std::string> excluded_components;
    bool active_only;
    bool visible_only;

    EntityQuery()
        : active_only(false)
        , visible_only(false)
    {}

    EntityQuery& require_tag(const std::string& tag) {
        required_tags.push_back(tag);
        return *this;
    }

    EntityQuery& exclude_tag(const std::string& tag) {
        excluded_tags.push_back(tag);
        return *this;
    }

    EntityQuery& in_layer(int layer) {
        layers.push_back(layer);
        return *this;
    }

    EntityQuery& require_component(const std::string& component_type) {
        required_components.push_back(component_type);
        return *this;
    }

    EntityQuery& exclude_component(const std::string& component_type) {
        excluded_components.push_back(component_type);
        return *this;
    }

    EntityQuery& set_active_only(bool active) {
        active_only = active;
        return *this;
    }

    EntityQuery& set_visible_only(bool visible) {
        visible_only = visible;
        return *this;
    }
};

// Entity query executor
class IEntityQueryExecutor {
public:
    virtual ~IEntityQueryExecutor() = default;

    virtual std::vector<IGameEntity*> execute_query(const EntityQuery& query) const = 0;
    virtual uint32_t count_query(const EntityQuery& query) const = 0;
    virtual IGameEntity* find_first(const EntityQuery& query) const = 0;
};

// Entity event
struct EntityEvent {
    enum class Type {
        ENTITY_CREATED,
        ENTITY_DESTROYED,
        ENTITY_ACTIVATED,
        ENTITY_DEACTIVATED,
        COMPONENT_ADDED,
        COMPONENT_REMOVED,
        TAG_ADDED,
        TAG_REMOVED,
        PARENT_CHANGED,
        CHILD_ADDED,
        CHILD_REMOVED
    };

    Type type;
    uint32_t entity_id;
    std::string message;
    std::unordered_map<std::string, std::string> data;

    EntityEvent(Type t, uint32_t id, const std::string& msg = "")
        : type(t)
        , entity_id(id)
        , message(msg)
    {}
};

// Entity event listener
using EntityEventListener = std::function<void(const EntityEvent&)>;

// Entity event manager
class IEntityEventManager {
public:
    virtual ~IEntityEventManager() = default;

    virtual void add_listener(EntityEventListener listener) = 0;
    virtual void remove_listener(EntityEventListener listener) = 0;
    virtual void emit_event(const EntityEvent& event) = 0;
    virtual void clear_listeners() = 0;
};

} // namespace game
} // namespace omnicpp

#endif // OMNICPP_GAME_ENTITY_DESIGN_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces
- `DES-022` - ECS Component Design
- `DES-029` - Game Core Interfaces

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects
- `unordered_map` - Hash map

## Related Requirements
- REQ-049: Entity Management
- REQ-050: Entity Queries

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Entity Design
1. Abstract entity interface
2. Component-based architecture
3. Entity hierarchy
4. Entity pooling

### Entity Lifecycle
1. Initialize entities
2. Update entities
3. Render entities
4. Destroy entities

### Entity Queries
1. Query by tags
2. Query by layers
3. Query by components
4. Query by state

### Entity Events
1. Entity creation/destruction
2. Component changes
3. Tag changes
4. Hierarchy changes

## Usage Example

```cpp
#include "game_entity_design.hpp"

using namespace omnicpp::game;

int main() {
    // Create entity manager
    auto entity_manager = std::make_unique<EntityManager>();

    // Create entity configuration
    EntityConfig config;
    config.name = "Player";
    config.description = "Player entity";
    config.is_persistent = true;
    config.is_static = false;
    config.layer = 1;

    // Create entity
    uint32_t entity_id = entity_manager->create_entity(config);
    IGameEntity* player = entity_manager->get_entity(entity_id);

    // Set entity position
    player->set_position(0.0f, 0.0f, 0.0f);

    // Add tags
    player->add_tag("Player");
    player->add_tag("Controllable");

    // Set layer
    player->set_layer(1);

    // Set active
    player->set_active(true);
    player->set_visible(true);

    // Create entity query
    EntityQuery query;
    query.require_tag("Player")
          .require_tag("Controllable")
          .in_layer(1)
          .set_active_only(true)
          .set_visible_only(true);

    // Execute query
    std::vector<IGameEntity*> results = entity_manager->get_entities_by_tag("Player");

    // Set entity event listener
    IEntityEventManager* event_manager = entity_manager->get_event_manager();
    event_manager->add_listener([](const EntityEvent& event) {
        if (event.type == EntityEvent::Type::ENTITY_CREATED) {
            std::cout << "Entity " << event.entity_id << " created" << std::endl;
        } else if (event.type == EntityEvent::Type::ENTITY_DESTROYED) {
            std::cout << "Entity " << event.entity_id << " destroyed" << std::endl;
        }
    });

    // Update entities
    double delta_time = 0.016; // 60 FPS
    entity_manager->update_entities(delta_time);
    entity_manager->render_entities();

    // Get statistics
    std::cout << "Entity count: " << entity_manager->get_entity_count() << std::endl;
    std::cout << "Active entities: " << entity_manager->get_active_entity_count() << std::endl;
    std::cout << "Component count: " << entity_manager->get_component_count() << std::endl;

    // Cleanup
    entity_manager->destroy_entity(entity_id);
    entity_manager->destroy_all_entities();

    return 0;
}
```
