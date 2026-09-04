/**
 * @file Entity.hpp
 * @brief Entity class for the Entity Component System (ECS)
 * @version 1.0.0
 */

#pragma once

#include <cstdint>
#include <string>
#include <memory>
#include <unordered_map>
#include <typeindex>

namespace omnicpp {
namespace ecs {

// Forward declarations
class Component;

/**
 * @brief Entity class representing a game object
 * 
 * Entities are lightweight identifiers that can have multiple components attached.
 * Components contain the actual data and behavior for the entity.
 */
class Entity {
public:
    /**
     * @brief Construct a new Entity object
     * @param id Unique identifier for the entity
     * @param name Optional name for the entity
     */
    explicit Entity(uint64_t id, const std::string& name = "Entity");
    
    /**
     * @brief Destroy the Entity object
     */
    ~Entity();

    // Disable copying
    Entity(const Entity&) = delete;
    Entity& operator=(const Entity&) = delete;

    // Enable moving
    Entity(Entity&&) noexcept = default;
    Entity& operator=(Entity&&) noexcept = default;

    /**
     * @brief Get the entity's unique ID
     * @return uint64_t The entity ID
     */
    uint64_t get_id() const { return m_id; }

    /**
     * @brief Get the entity's name
     * @return const std::string& The entity name
     */
    const std::string& get_name() const { return m_name; }

    /**
     * @brief Set the entity's name
     * @param name The new name
     */
    void set_name(const std::string& name) { m_name = name; }

    /**
     * @brief Check if the entity is active
     * @return true if active, false otherwise
     */
    bool is_active() const { return m_active; }

    /**
     * @brief Set the entity's active state
     * @param active The new active state
     */
    void set_active(bool active) { m_active = active; }

    /**
     * @brief Add a component to the entity
     * @tparam T The component type
     * @tparam Args Argument types for component construction
     * @param args Arguments to forward to component constructor
     * @return T* Pointer to the added component
     */
    template<typename T, typename... Args>
    T* add_component(Args&&... args);

    /**
     * @brief Remove a component from the entity
     * @tparam T The component type
     */
    template<typename T>
    void remove_component();

    /**
     * @brief Get a component from the entity
     * @tparam T The component type
     * @return T* Pointer to the component, or nullptr if not found
     */
    template<typename T>
    T* get_component();

    /**
     * @brief Get a component from the entity (const version)
     * @tparam T The component type
     * @return const T* Pointer to the component, or nullptr if not found
     */
    template<typename T>
    const T* get_component() const;

    /**
     * @brief Check if the entity has a specific component
     * @tparam T The component type
     * @return true if the component exists, false otherwise
     */
    template<typename T>
    bool has_component() const;

    /**
     * @brief Get all components attached to the entity
     * @return const std::unordered_map<std::type_index, std::unique_ptr<Component>>&
     */
    const std::unordered_map<std::type_index, std::unique_ptr<Component>>& get_components() const {
        return m_components;
    }

private:
    uint64_t m_id;
    std::string m_name;
    bool m_active;
    std::unordered_map<std::type_index, std::unique_ptr<Component>> m_components;
};

} // namespace ecs
} // namespace omnicpp
