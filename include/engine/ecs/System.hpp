/**
 * @file System.hpp
 * @brief System base class for Entity Component System (ECS)
 * @version 1.0.0
 */

#pragma once

#include <vector>
#include <memory>

namespace omnicpp {
namespace ecs {

// Forward declarations
class Entity;
class Component;

/**
 * @brief Base class for all systems
 * 
 * Systems contain logic that operates on entities with specific components.
 * They process entities in the update loop.
 */
class System {
public:
    /**
     * @brief Construct a new System object
     */
    System() = default;
    
    /**
     * @brief Virtual destructor for proper cleanup
     */
    virtual ~System() = default;

    /**
     * @brief Initialize the system
     * @return true if initialization succeeded, false otherwise
     */
    virtual bool initialize() { return true; }

    /**
     * @brief Shutdown the system
     */
    virtual void shutdown() {}

    /**
     * @brief Update the system
     * @param delta_time Time since last frame in seconds
     */
    virtual void update(float delta_time) = 0;

    /**
     * @brief Called when an entity is added to the system
     * @param entity The entity that was added
     */
    virtual void on_entity_added(Entity* entity) {}

    /**
     * @brief Called when an entity is removed from the system
     * @param entity The entity that was removed
     */
    virtual void on_entity_removed(Entity* entity) {}

    /**
     * @brief Get the system's priority
     * @return int The priority (higher values update first)
     */
    int get_priority() const { return m_priority; }

    /**
     * @brief Set the system's priority
     * @param priority The new priority
     */
    void set_priority(int priority) { m_priority = priority; }

    /**
     * @brief Check if the system is enabled
     * @return true if enabled, false otherwise
     */
    bool is_enabled() const { return m_enabled; }

    /**
     * @brief Set the system's enabled state
     * @param enabled The new enabled state
     */
    void set_enabled(bool enabled) { m_enabled = enabled; }

protected:
    int m_priority = 0;
    bool m_enabled = true;
};

} // namespace ecs
} // namespace omnicpp
