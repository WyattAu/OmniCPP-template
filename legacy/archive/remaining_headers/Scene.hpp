/**
 * @file Scene.hpp
 * @brief Scene class for managing game scenes
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <unordered_map>
#include "engine/scene/SceneNode.hpp"
#include "engine/ecs/Entity.hpp"

namespace omnicpp {
namespace scene {

// Forward declarations
class Camera;

/**
 * @brief Scene class for managing game scenes
 * 
 * Scenes contain a root scene node and manage entities.
 */
class Scene {
public:
    /**
     * @brief Construct a new Scene object
     * @param name The scene name
     */
    explicit Scene(const std::string& name = "Scene");

    /**
     * @brief Destroy the Scene object
     */
    ~Scene();

    // Disable copying
    Scene(const Scene&) = delete;
    Scene& operator=(const Scene&) = delete;

    // Enable moving
    Scene(Scene&&) noexcept = default;
    Scene& operator=(Scene&&) noexcept = default;

    /**
     * @brief Get scene name
     * @return const std::string& The scene name
     */
    const std::string& get_name() const { return m_name; }

    /**
     * @brief Set scene name
     * @param name The new name
     */
    void set_name(const std::string& name) { m_name = name; }

    /**
     * @brief Get root scene node
     * @return SceneNode* Pointer to root node
     */
    SceneNode* get_root_node() const { return m_root_node.get(); }

    /**
     * @brief Get active camera
     * @return Camera* Pointer to active camera
     */
    Camera* get_active_camera() const { return m_active_camera; }

    /**
     * @brief Set active camera
     * @param camera Pointer to camera
     */
    void set_active_camera(Camera* camera) { m_active_camera = camera; }

    /**
     * @brief Add an entity to the scene
     * @param entity Pointer to entity (takes ownership)
     */
    void add_entity(std::unique_ptr<ecs::Entity> entity);

    /**
     * @brief Remove an entity from the scene
     * @param entity_id The entity ID
     * @return std::unique_ptr<ecs::Entity> The removed entity
     */
    std::unique_ptr<ecs::Entity> remove_entity(uint64_t entity_id);

    /**
     * @brief Get an entity by ID
     * @param entity_id The entity ID
     * @return ecs::Entity* Pointer to entity, or nullptr if not found
     */
    ecs::Entity* get_entity(uint64_t entity_id) const;

    /**
     * @brief Get all entities in the scene
     * @return const std::vector<std::unique_ptr<ecs::Entity>>& The entities
     */
    const std::vector<std::unique_ptr<ecs::Entity>>& get_entities() const { return m_entities; }

    /**
     * @brief Update scene
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Render scene
     */
    void render();

    /**
     * @brief Check if scene is active
     * @return true if active, false otherwise
     */
    bool is_active() const { return m_active; }

    /**
     * @brief Set scene's active state
     * @param active The new active state
     */
    void set_active(bool active) { m_active = active; }

private:
    std::string m_name;
    std::unique_ptr<SceneNode> m_root_node;
    std::vector<std::unique_ptr<ecs::Entity>> m_entities;
    std::unordered_map<uint64_t, ecs::Entity*> m_entity_map;
    Camera* m_active_camera = nullptr;
    bool m_active = true;
};

} // namespace scene
} // namespace omnicpp
