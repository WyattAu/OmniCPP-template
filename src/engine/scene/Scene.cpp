/**
 * @file Scene.cpp
 * @brief Scene implementation
 * @version 1.0.0
 */

#include "engine/scene/Scene.hpp"
#include "engine/scene/SceneNode.hpp"
#include "engine/ecs/Entity.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include "engine/ecs/MeshComponent.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {
namespace scene {

Scene::Scene(const std::string& name)
    : m_name(name)
    , m_root_node(std::make_unique<SceneNode>("Root")) {
    omnicpp::log::debug("Scene: Created scene '{}'", name);
}

Scene::~Scene() = default;

void Scene::add_entity(std::unique_ptr<ecs::Entity> entity) {
    if (entity) {
        uint64_t id = entity->get_id();
        m_entities.push_back(std::move(entity));
        m_entity_map[id] = m_entities.back().get();

        // Attach entity to root node
        m_root_node->set_entity(m_entities.back().get());
    }
}

std::unique_ptr<ecs::Entity> Scene::remove_entity(uint64_t entity_id) {
    auto it = m_entity_map.find(entity_id);
    if (it != m_entity_map.end()) {
        ecs::Entity* entity = it->second;

        // Detach from scene node
        m_root_node->set_entity(nullptr);

        // Remove from entities vector
        for (auto eit = m_entities.begin(); eit != m_entities.end(); ++eit) {
            if (eit->get() == entity) {
                auto removed = std::move(*eit);
                m_entities.erase(eit);
                m_entity_map.erase(it);
                return removed;
            }
        }
    }
    return nullptr;
}

ecs::Entity* Scene::get_entity(uint64_t entity_id) const {
    auto it = m_entity_map.find(entity_id);
    if (it != m_entity_map.end()) {
        return it->second;
    }
    return nullptr;
}

void Scene::update(float delta_time) {
    if (!m_active) {
        return;
    }

    // Update root node (which updates all children)
    m_root_node->update(delta_time);

    // Update all entities
    for (auto& entity : m_entities) {
        if (entity && entity->is_active()) {
            // Update all components
            auto transform = entity->get_component<ecs::TransformComponent>();
            if (transform) {
                transform->on_update(delta_time);
            }

            auto mesh = entity->get_component<ecs::MeshComponent>();
            if (mesh) {
                mesh->on_update(delta_time);
            }
        }
    }
}

void Scene::render() {
    if (!m_active) {
        return;
    }

    // Render scene through active camera
    // This is a placeholder - actual rendering would be done by the renderer
    // which would traverse the scene graph and render visible entities
}

} // namespace scene
} // namespace omnicpp
