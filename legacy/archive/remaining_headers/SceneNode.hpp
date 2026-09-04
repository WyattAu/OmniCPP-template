/**
 * @file SceneNode.hpp
 * @brief Scene node for hierarchical scene graph
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <vector>
#include <memory>
#include "engine/ecs/Entity.hpp"

namespace omnicpp {
namespace scene {

// Forward declarations
class SceneNode;

/**
 * @brief Scene node for hierarchical scene graph
 * 
 * Scene nodes form a tree structure representing the scene hierarchy.
 * Each node can have children and a parent.
 */
class SceneNode {
public:
    /**
     * @brief Construct a new Scene Node object
     * @param name The node name
     */
    explicit SceneNode(const std::string& name = "SceneNode");

    /**
     * @brief Destroy the Scene Node object
     */
    ~SceneNode();

    // Disable copying
    SceneNode(const SceneNode&) = delete;
    SceneNode& operator=(const SceneNode&) = delete;

    // Enable moving
    SceneNode(SceneNode&&) noexcept = default;
    SceneNode& operator=(SceneNode&&) noexcept = default;

    /**
     * @brief Get node name
     * @return const std::string& The node name
     */
    const std::string& get_name() const { return m_name; }

    /**
     * @brief Set node name
     * @param name The new name
     */
    void set_name(const std::string& name) { m_name = name; }

    /**
     * @brief Get parent node
     * @return SceneNode* Pointer to parent, or nullptr if root
     */
    SceneNode* get_parent() const { return m_parent; }

    /**
     * @brief Get children
     * @return const std::vector<std::unique_ptr<SceneNode>>& The children
     */
    const std::vector<std::unique_ptr<SceneNode>>& get_children() const { return m_children; }

    /**
     * @brief Get entity associated with this node
     * @return ecs::Entity* Pointer to entity, or nullptr if none
     */
    ecs::Entity* get_entity() const { return m_entity; }

    /**
     * @brief Set entity for this node
     * @param entity Pointer to entity
     */
    void set_entity(ecs::Entity* entity) { m_entity = entity; }

    /**
     * @brief Add a child node
     * @param child The child node to add (takes ownership)
     */
    void add_child(std::unique_ptr<SceneNode> child);

    /**
     * @brief Remove a child node
     * @param child The child node to remove
     * @return std::unique_ptr<SceneNode> The removed child
     */
    std::unique_ptr<SceneNode> remove_child(SceneNode* child);

    /**
     * @brief Get child by index
     * @param index The child index
     * @return SceneNode* Pointer to child, or nullptr if index is invalid
     */
    SceneNode* get_child(size_t index) const;

    /**
     * @brief Get child count
     * @return size_t The number of children
     */
    size_t get_child_count() const { return m_children.size(); }

    /**
     * @brief Update node and all children
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Check if node is active
     * @return true if active, false otherwise
     */
    bool is_active() const { return m_active; }

    /**
     * @brief Set node's active state
     * @param active The new active state
     */
    void set_active(bool active) { m_active = active; }

private:
    std::string m_name;
    SceneNode* m_parent = nullptr;
    std::vector<std::unique_ptr<SceneNode>> m_children;
    ecs::Entity* m_entity = nullptr;
    bool m_active = true;
};

} // namespace scene
} // namespace omnicpp
