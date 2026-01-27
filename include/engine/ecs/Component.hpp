/**
 * @file Component.hpp
 * @brief Component base class for Entity Component System (ECS)
 * @version 1.0.0
 */

#pragma once

#include <cstdint>

namespace omnicpp {
namespace ecs {

/**
 * @brief Base class for all components
 * 
 * Components are data containers that hold state for entities.
 * They should be lightweight and contain no logic.
 */
class Component {
public:
    /**
     * @brief Construct a new Component object
     * @param entity_id The ID of the entity this component belongs to
     */
    explicit Component(uint64_t entity_id);
    
    /**
     * @brief Virtual destructor for proper cleanup
     */
    virtual ~Component() = default;

    /**
     * @brief Get the entity ID this component belongs to
     * @return uint64_t The entity ID
     */
    uint64_t get_entity_id() const { return m_entity_id; }

    /**
     * @brief Called when component is attached to an entity
     */
    virtual void on_attach() {}

    /**
     * @brief Called when component is detached from an entity
     */
    virtual void on_detach() {}

    /**
     * @brief Called each frame to update component state
     * @param delta_time Time since last frame in seconds
     */
    virtual void on_update(float delta_time) {}

protected:
    uint64_t m_entity_id;
};

} // namespace ecs
} // namespace omnicpp
