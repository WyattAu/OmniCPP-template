# DES-023: ECS System Design

## Overview
Defines the Entity-Component-System (ECS) system design for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_ECS_SYSTEM_H
#define OMNICPP_ECS_SYSTEM_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <typeindex>

namespace omnicpp {
namespace ecs {

// Forward declarations
class IEntityManager;
class IComponentManager;
class IComponentPool;

// Entity ID type
using EntityID = uint32_t;

// System ID type
using SystemID = uint32_t;

// System type ID
using SystemTypeID = std::type_index;

// System base class
class ISystem {
public:
    virtual ~ISystem() = default;

    // Get system type ID
    virtual SystemTypeID get_type_id() const = 0;

    // Get system name
    virtual const char* get_name() const = 0;

    // Initialize system
    virtual bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) = 0;

    // Shutdown system
    virtual void shutdown() = 0;

    // Update system
    virtual void update(double delta_time) = 0;

    // Render system
    virtual void render() = 0;

    // Get system priority
    virtual int get_priority() const = 0;

    // Is system enabled
    virtual bool is_enabled() const = 0;

    // Enable/disable system
    virtual void set_enabled(bool enabled) = 0;
};

// System traits
template<typename T>
struct SystemTraits {
    static constexpr bool is_system = std::is_base_of<ISystem, T>::value;
    static constexpr SystemTypeID type_id = typeid(T);
};

// System manager
class ISystemManager {
public:
    virtual ~ISystemManager() = default;

    // Register system type
    virtual SystemID register_system_type(SystemTypeID type_id) = 0;

    // Get system ID
    virtual SystemID get_system_id(SystemTypeID type_id) const = 0;

    // Create system
    virtual std::unique_ptr<ISystem> create_system(SystemID system_id) const = 0;

    // Add system
    virtual bool add_system(std::unique_ptr<ISystem> system) = 0;

    // Remove system
    virtual bool remove_system(SystemID system_id) = 0;

    // Get system
    virtual ISystem* get_system(SystemID system_id) const = 0;

    // Get all systems
    virtual std::vector<ISystem*> get_all_systems() const = 0;

    // Update all systems
    virtual void update_systems(double delta_time) = 0;

    // Render all systems
    virtual void render_systems() = 0;

    // Shutdown all systems
    virtual void shutdown_systems() = 0;

    // Sort systems by priority
    virtual void sort_systems() = 0;
};

// Transform system
class TransformSystem : public ISystem {
private:
    IEntityManager* m_entity_manager;
    IComponentManager* m_component_manager;
    bool m_enabled;

public:
    TransformSystem()
        : m_entity_manager(nullptr)
        , m_component_manager(nullptr)
        , m_enabled(true)
    {}

    SystemTypeID get_type_id() const override {
        return SystemTraits<TransformSystem>::type_id;
    }

    const char* get_name() const override {
        return "TransformSystem";
    }

    bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) override {
        m_entity_manager = entity_manager;
        m_component_manager = component_manager;
        return true;
    }

    void shutdown() override {
        m_entity_manager = nullptr;
        m_component_manager = nullptr;
    }

    void update(double delta_time) override {
        // Update transform components
    }

    void render() override {
        // Transform system doesn't render
    }

    int get_priority() const override {
        return 100;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }
};

// Render system
class RenderSystem : public ISystem {
private:
    IEntityManager* m_entity_manager;
    IComponentManager* m_component_manager;
    bool m_enabled;

public:
    RenderSystem()
        : m_entity_manager(nullptr)
        , m_component_manager(nullptr)
        , m_enabled(true)
    {}

    SystemTypeID get_type_id() const override {
        return SystemTraits<RenderSystem>::type_id;
    }

    const char* get_name() const override {
        return "RenderSystem";
    }

    bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) override {
        m_entity_manager = entity_manager;
        m_component_manager = component_manager;
        return true;
    }

    void shutdown() override {
        m_entity_manager = nullptr;
        m_component_manager = nullptr;
    }

    void update(double delta_time) override {
        // Update render components
    }

    void render() override {
        // Render entities with mesh components
    }

    int get_priority() const override {
        return 1000;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }
};

// Physics system
class PhysicsSystem : public ISystem {
private:
    IEntityManager* m_entity_manager;
    IComponentManager* m_component_manager;
    bool m_enabled;

public:
    PhysicsSystem()
        : m_entity_manager(nullptr)
        , m_component_manager(nullptr)
        , m_enabled(true)
    {}

    SystemTypeID get_type_id() const override {
        return SystemTraits<PhysicsSystem>::type_id;
    }

    const char* get_name() const override {
        return "PhysicsSystem";
    }

    bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) override {
        m_entity_manager = entity_manager;
        m_component_manager = component_manager;
        return true;
    }

    void shutdown() override {
        m_entity_manager = nullptr;
        m_component_manager = nullptr;
    }

    void update(double delta_time) override {
        // Update physics simulation
    }

    void render() override {
        // Physics system doesn't render
    }

    int get_priority() const override {
        return 200;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }
};

// Audio system
class AudioSystem : public ISystem {
private:
    IEntityManager* m_entity_manager;
    IComponentManager* m_component_manager;
    bool m_enabled;

public:
    AudioSystem()
        : m_entity_manager(nullptr)
        , m_component_manager(nullptr)
        , m_enabled(true)
    {}

    SystemTypeID get_type_id() const override {
        return SystemTraits<AudioSystem>::type_id;
    }

    const char* get_name() const override {
        return "AudioSystem";
    }

    bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) override {
        m_entity_manager = entity_manager;
        m_component_manager = component_manager;
        return true;
    }

    void shutdown() override {
        m_entity_manager = nullptr;
        m_component_manager = nullptr;
    }

    void update(double delta_time) override {
        // Update audio components
    }

    void render() override {
        // Audio system doesn't render
    }

    int get_priority() const override {
        return 300;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }
};

// Script system
class ScriptSystem : public ISystem {
private:
    IEntityManager* m_entity_manager;
    IComponentManager* m_component_manager;
    bool m_enabled;

public:
    ScriptSystem()
        : m_entity_manager(nullptr)
        , m_component_manager(nullptr)
        , m_enabled(true)
    {}

    SystemTypeID get_type_id() const override {
        return SystemTraits<ScriptSystem>::type_id;
    }

    const char* get_name() const override {
        return "ScriptSystem";
    }

    bool initialize(IEntityManager* entity_manager, IComponentManager* component_manager) override {
        m_entity_manager = entity_manager;
        m_component_manager = component_manager;
        return true;
    }

    void shutdown() override {
        m_entity_manager = nullptr;
        m_component_manager = nullptr;
    }

    void update(double delta_time) override {
        // Update script components
    }

    void render() override {
        // Script system doesn't render
    }

    int get_priority() const override {
        return 400;
    }

    bool is_enabled() const override {
        return m_enabled;
    }

    void set_enabled(bool enabled) override {
        m_enabled = enabled;
    }
};

// System query
struct SystemQuery {
    std::vector<ComponentID> required_components;
    std::vector<ComponentID> optional_components;
    std::vector<ComponentID> excluded_components;

    SystemQuery() = default;

    SystemQuery& require(ComponentID component_id) {
        required_components.push_back(component_id);
        return *this;
    }

    SystemQuery& optional(ComponentID component_id) {
        optional_components.push_back(component_id);
        return *this;
    }

    SystemQuery& exclude(ComponentID component_id) {
        excluded_components.push_back(component_id);
        return *this;
    }
};

// System executor
class ISystemExecutor {
public:
    virtual ~ISystemExecutor() = default;

    // Execute system
    virtual void execute(ISystem* system, double delta_time) = 0;

    // Execute system with query
    virtual void execute_with_query(ISystem* system, const SystemQuery& query, double delta_time) = 0;

    // Execute system for entity
    virtual void execute_for_entity(ISystem* system, EntityID entity_id, double delta_time) = 0;
};

// System scheduler
class ISystemScheduler {
public:
    virtual ~ISystemScheduler() = default;

    // Schedule system
    virtual void schedule_system(ISystem* system) = 0;

    // Schedule system with priority
    virtual void schedule_system_with_priority(ISystem* system, int priority) = 0;

    // Schedule system with dependencies
    virtual void schedule_system_with_dependencies(ISystem* system, const std::vector<SystemID>& dependencies) = 0;

    // Execute scheduled systems
    virtual void execute_scheduled_systems(double delta_time) = 0;

    // Clear schedule
    virtual void clear_schedule() = 0;
};

// System profiler
class ISystemProfiler {
public:
    virtual ~ISystemProfiler() = default;

    // Begin system profiling
    virtual void begin_system(ISystem* system) = 0;

    // End system profiling
    virtual void end_system(ISystem* system) = 0;

    // Get system execution time
    virtual double get_system_time(SystemID system_id) const = 0;

    // Get all system times
    virtual std::vector<std::pair<SystemID, double>> get_all_system_times() const = 0;

    // Clear profiling data
    virtual void clear() = 0;
};

} // namespace ecs
} // namespace omnicpp

#endif // OMNICPP_ECS_SYSTEM_H
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
- `typeindex` - Type information
- `utility` - Pair

## Related Requirements
- REQ-032: ECS Architecture
- REQ-034: System Architecture

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### System Design
1. All systems inherit from ISystem
2. Systems operate on components
3. Systems have update and render phases
4. Systems can be enabled/disabled

### System Management
1. Register system types
2. Create system instances
3. Manage system lifecycle
4. Handle system dependencies

### System Execution
1. Execute systems in priority order
2. Support system queries
3. Profile system execution
4. Schedule systems efficiently

### System Queries
1. Query entities by components
2. Support required components
3. Support optional components
4. Support excluded components

## Usage Example

```cpp
#include "ecs_system.hpp"

using namespace omnicpp::ecs;

int main() {
    // Create systems
    auto transform_system = std::make_unique<TransformSystem>();
    auto render_system = std::make_unique<RenderSystem>();
    auto physics_system = std::make_unique<PhysicsSystem>();
    auto audio_system = std::make_unique<AudioSystem>();
    auto script_system = std::make_unique<ScriptSystem>();

    // Get system type IDs
    auto transform_id = SystemTraits<TransformSystem>::type_id;
    auto render_id = SystemTraits<RenderSystem>::type_id;
    auto physics_id = SystemTraits<PhysicsSystem>::type_id;
    auto audio_id = SystemTraits<AudioSystem>::type_id;
    auto script_id = SystemTraits<ScriptSystem>::type_id;

    // Create system query
    SystemQuery query;
    query.require(1)  // Transform component
          .require(2)  // Mesh component
          .optional(3); // Camera component

    // Update systems
    double delta_time = 0.016; // 60 FPS
    transform_system->update(delta_time);
    physics_system->update(delta_time);
    audio_system->update(delta_time);
    script_system->update(delta_time);

    // Render systems
    render_system->render();

    return 0;
}
```
