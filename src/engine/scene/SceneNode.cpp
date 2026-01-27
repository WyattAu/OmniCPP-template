/**
 * @file SceneNode.cpp
 * @brief Scene node implementation
 * @version 1.0.0
 */

#include "engine/scene/SceneNode.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include <spdlog/spdlog.h>

namespace omnicpp {
namespace scene {

SceneNode::SceneNode(const std::string& name)
    : m_name(name) {
    spdlog::debug("SceneNode: Created node '{}'", name);
}

SceneNode::~SceneNode() = default;

void SceneNode::add_child(std::unique_ptr<SceneNode> child) {
    if (child) {
        spdlog::debug("SceneNode: Adding child '{}' to node '{}'", child->get_name(), m_name);
        child->m_parent = this;
        m_children.push_back(std::move(child));
    }
}

std::unique_ptr<SceneNode> SceneNode::remove_child(SceneNode* child) {
    for (auto it = m_children.begin(); it != m_children.end(); ++it) {
        if (it->get() == child) {
            spdlog::debug("SceneNode: Removing child '{}' from node '{}'", child->get_name(), m_name);
            auto removed = std::move(*it);
            m_children.erase(it);
            child->m_parent = nullptr;
            return removed;
        }
    }
    return nullptr;
}

SceneNode* SceneNode::get_child(size_t index) const {
    if (index < m_children.size()) {
        return m_children[index].get();
    }
    return nullptr;
}

void SceneNode::update(float delta_time) {
    if (!m_active) {
        return;
    }

    // Update entity if attached
    if (m_entity && m_entity->is_active()) {
        // Update entity components
        auto transform = m_entity->get_component<ecs::TransformComponent>();
        if (transform) {
            transform->on_update(delta_time);
        }
    }

    // Update all children
    for (auto& child : m_children) {
        child->update(delta_time);
    }
}

} // namespace scene
} // namespace omnicpp
