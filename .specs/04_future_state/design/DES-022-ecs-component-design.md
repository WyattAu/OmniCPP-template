# DES-022: ECS Component Design

## Overview
Defines the Entity-Component-System (ECS) component design for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_ECS_COMPONENT_H
#define OMNICPP_ECS_COMPONENT_H

#include <cstdint>
#include <string>
#include <typeindex>
#include <type_traits>
#include <memory>

namespace omnicpp {
namespace ecs {

// Component ID type
using ComponentID = uint32_t;

// Component type ID
using ComponentTypeID = std::type_index;

// Component base class
class IComponent {
public:
    virtual ~IComponent() = default;

    // Get component type ID
    virtual ComponentTypeID get_type_id() const = 0;

    // Get component name
    virtual const char* get_name() const = 0;

    // Clone component
    virtual std::unique_ptr<IComponent> clone() const = 0;

    // Serialize component
    virtual std::string serialize() const = 0;

    // Deserialize component
    virtual void deserialize(const std::string& data) = 0;
};

// Component traits
template<typename T>
struct ComponentTraits {
    static constexpr bool is_component = std::is_base_of<IComponent, T>::value;
    static constexpr ComponentTypeID type_id = typeid(T);
};

// Component manager
class IComponentManager {
public:
    virtual ~IComponentManager() = default;

    // Register component type
    virtual ComponentID register_component_type(ComponentTypeID type_id) = 0;

    // Get component ID
    virtual ComponentID get_component_id(ComponentTypeID type_id) const = 0;

    // Create component
    virtual std::unique_ptr<IComponent> create_component(ComponentID component_id) const = 0;

    // Destroy component
    virtual void destroy_component(std::unique_ptr<IComponent> component) = 0;

    // Get component type info
    virtual const char* get_component_name(ComponentID component_id) const = 0;
};

// Transform component
struct TransformComponent : public IComponent {
    float position_x;
    float position_y;
    float position_z;
    float rotation_x;
    float rotation_y;
    float rotation_z;
    float scale_x;
    float scale_y;
    float scale_z;

    TransformComponent()
        : position_x(0.0f)
        , position_y(0.0f)
        , position_z(0.0f)
        , rotation_x(0.0f)
        , rotation_y(0.0f)
        , rotation_z(0.0f)
        , scale_x(1.0f)
        , scale_y(1.0f)
        , scale_z(1.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<TransformComponent>::type_id;
    }

    const char* get_name() const override {
        return "TransformComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<TransformComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize transform data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize transform data
    }
};

// Mesh component
struct MeshComponent : public IComponent {
    std::string mesh_path;
    std::string material_path;
    bool visible;
    bool cast_shadows;
    bool receive_shadows;

    MeshComponent()
        : visible(true)
        , cast_shadows(true)
        , receive_shadows(true)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<MeshComponent>::type_id;
    }

    const char* get_name() const override {
        return "MeshComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<MeshComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize mesh data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize mesh data
    }
};

// Camera component
struct CameraComponent : public IComponent {
    float fov;
    float near_plane;
    float far_plane;
    bool is_active;
    bool is_orthographic;
    float ortho_size;

    CameraComponent()
        : fov(60.0f)
        , near_plane(0.1f)
        , far_plane(1000.0f)
        , is_active(true)
        , is_orthographic(false)
        , ortho_size(10.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<CameraComponent>::type_id;
    }

    const char* get_name() const override {
        return "CameraComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<CameraComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize camera data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize camera data
    }
};

// Light component
struct LightComponent : public IComponent {
    enum class Type {
        DIRECTIONAL,
        POINT,
        SPOT,
        AMBIENT
    };

    Type type;
    float intensity;
    float color_r;
    float color_g;
    float color_b;
    float range;
    float spot_angle;

    LightComponent()
        : type(Type::POINT)
        , intensity(1.0f)
        , color_r(1.0f)
        , color_g(1.0f)
        , color_b(1.0f)
        , range(10.0f)
        , spot_angle(45.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<LightComponent>::type_id;
    }

    const char* get_name() const override {
        return "LightComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<LightComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize light data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize light data
    }
};

// Rigid body component
struct RigidBodyComponent : public IComponent {
    float mass;
    bool is_static;
    bool is_kinematic;
    float linear_damping;
    float angular_damping;
    float friction;
    float restitution;

    RigidBodyComponent()
        : mass(1.0f)
        , is_static(false)
        , is_kinematic(false)
        , linear_damping(0.0f)
        , angular_damping(0.0f)
        , friction(0.5f)
        , restitution(0.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<RigidBodyComponent>::type_id;
    }

    const char* get_name() const override {
        return "RigidBodyComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<RigidBodyComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize rigid body data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize rigid body data
    }
};

// Collider component
struct ColliderComponent : public IComponent {
    enum class Type {
        BOX,
        SPHERE,
        CAPSULE,
        MESH
    };

    Type type;
    bool is_trigger;
    float center_x;
    float center_y;
    float center_z;
    float size_x;
    float size_y;
    float size_z;
    float radius;
    float height;

    ColliderComponent()
        : type(Type::BOX)
        , is_trigger(false)
        , center_x(0.0f)
        , center_y(0.0f)
        , center_z(0.0f)
        , size_x(1.0f)
        , size_y(1.0f)
        , size_z(1.0f)
        , radius(0.5f)
        , height(1.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<ColliderComponent>::type_id;
    }

    const char* get_name() const override {
        return "ColliderComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<ColliderComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize collider data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize collider data
    }
};

// Audio source component
struct AudioSourceComponent : public IComponent {
    std::string audio_path;
    bool loop;
    bool play_on_start;
    float volume;
    float pitch;
    bool is_3d;
    float min_distance;
    float max_distance;

    AudioSourceComponent()
        : loop(false)
        , play_on_start(false)
        , volume(1.0f)
        , pitch(1.0f)
        , is_3d(false)
        , min_distance(1.0f)
        , max_distance(100.0f)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<AudioSourceComponent>::type_id;
    }

    const char* get_name() const override {
        return "AudioSourceComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<AudioSourceComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize audio source data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize audio source data
    }
};

// Script component
struct ScriptComponent : public IComponent {
    std::string script_path;
    std::string script_class;
    bool enabled;

    ScriptComponent()
        : enabled(true)
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<ScriptComponent>::type_id;
    }

    const char* get_name() const override {
        return "ScriptComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<ScriptComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize script data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize script data
    }
};

// Tag component
struct TagComponent : public IComponent {
    std::string tag;

    TagComponent()
        : tag("Untagged")
    {}

    ComponentTypeID get_type_id() const override {
        return ComponentTraits<TagComponent>::type_id;
    }

    const char* get_name() const override {
        return "TagComponent";
    }

    std::unique_ptr<IComponent> clone() const override {
        return std::make_unique<TagComponent>(*this);
    }

    std::string serialize() const override {
        // Serialize tag data
        return "";
    }

    void deserialize(const std::string& data) override {
        // Deserialize tag data
    }
};

// Component pool
class IComponentPool {
public:
    virtual ~IComponentPool() = default;

    // Get component
    virtual IComponent* get(uint32_t entity_id) = 0;
    virtual const IComponent* get(uint32_t entity_id) const = 0;

    // Add component
    virtual void add(uint32_t entity_id, std::unique_ptr<IComponent> component) = 0;

    // Remove component
    virtual void remove(uint32_t entity_id) = 0;

    // Check if component exists
    virtual bool has(uint32_t entity_id) const = 0;

    // Get all entities with this component
    virtual std::vector<uint32_t> get_entities() const = 0;

    // Clear pool
    virtual void clear() = 0;
};

// Component pool factory
class IComponentPoolFactory {
public:
    virtual ~IComponentPoolFactory() = default;

    virtual std::unique_ptr<IComponentPool> create_pool(ComponentID component_id) = 0;
};

} // namespace ecs
} // namespace omnicpp

#endif // OMNICPP_ECS_COMPONENT_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces
- `DES-023` - ECS System Design

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `typeindex` - Type information
- `type_traits` - Type traits
- `memory` - Smart pointers
- `vector` - Dynamic arrays

## Related Requirements
- REQ-032: ECS Architecture
- REQ-033: Component System

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Component Design
1. All components inherit from IComponent
2. Components are data-only structures
3. Components support serialization
4. Components support cloning

### Component Management
1. Register component types
2. Create component pools
3. Manage component lifecycle
4. Handle component dependencies

### Component Pooling
1. Pool components by type
2. Efficient memory allocation
3. Fast component lookup
4. Support for iteration

### Serialization
1. Serialize component data
2. Deserialize component data
3. Support for versioning
4. Handle missing fields

## Usage Example

```cpp
#include "ecs_component.hpp"

using namespace omnicpp::ecs;

int main() {
    // Create transform component
    auto transform = std::make_unique<TransformComponent>();
    transform->position_x = 10.0f;
    transform->position_y = 5.0f;
    transform->position_z = 0.0f;

    // Create mesh component
    auto mesh = std::make_unique<MeshComponent>();
    mesh->mesh_path = "models/player.obj";
    mesh->material_path = "materials/player.mat";

    // Create rigid body component
    auto rigid_body = std::make_unique<RigidBodyComponent>();
    rigid_body->mass = 10.0f;
    rigid_body->is_static = false;

    // Get component type IDs
    auto transform_id = ComponentTraits<TransformComponent>::type_id;
    auto mesh_id = ComponentTraits<MeshComponent>::type_id;
    auto rigid_body_id = ComponentTraits<RigidBodyComponent>::type_id;

    return 0;
}
```
