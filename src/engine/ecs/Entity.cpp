/**
 * @file Entity.cpp
 * @brief Entity implementation for Entity Component System (ECS)
 * @version 1.0.0
 */

#include "engine/ecs/Entity.hpp"
#include "engine/ecs/Component.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include "engine/ecs/MeshComponent.hpp"
#include <stdexcept>
#include <spdlog/spdlog.h>

namespace omnicpp {
namespace ecs {

static uint64_t s_next_entity_id = 1;

Entity::Entity(uint64_t id, const std::string& name)
    : m_id(id == 0 ? s_next_entity_id++ : id)
    , m_name(name)
    , m_active(true) {
    spdlog::debug("Entity: Created entity {} with name '{}'", m_id, name);
}

Entity::~Entity() = default;

template<typename T, typename... Args>
T* Entity::add_component(Args&&... args) {
    auto component = std::make_unique<T>(m_id, std::forward<Args>(args)...);
    T* ptr = component.get();
    m_components[std::type_index(typeid(T))] = std::move(component);
    ptr->on_attach();
    return ptr;
}

template<typename T>
void Entity::remove_component() {
    auto it = m_components.find(std::type_index(typeid(T)));
    if (it != m_components.end()) {
        it->second->on_detach();
        m_components.erase(it);
    }
}

template<typename T>
T* Entity::get_component() {
    auto it = m_components.find(std::type_index(typeid(T)));
    if (it != m_components.end()) {
        return static_cast<T*>(it->second.get());
    }
    return nullptr;
}

template<typename T>
const T* Entity::get_component() const {
    auto it = m_components.find(std::type_index(typeid(T)));
    if (it != m_components.end()) {
        return static_cast<const T*>(it->second.get());
    }
    return nullptr;
}

template<typename T>
bool Entity::has_component() const {
    return m_components.find(std::type_index(typeid(T))) != m_components.end();
}

// Explicit template instantiations
template TransformComponent* Entity::add_component<TransformComponent>();
template void Entity::remove_component<TransformComponent>();
template TransformComponent* Entity::get_component<TransformComponent>();
template const TransformComponent* Entity::get_component<TransformComponent>() const;
template bool Entity::has_component<TransformComponent>() const;

template MeshComponent* Entity::add_component<MeshComponent>();
template void Entity::remove_component<MeshComponent>();
template MeshComponent* Entity::get_component<MeshComponent>();
template const MeshComponent* Entity::get_component<MeshComponent>() const;
template bool Entity::has_component<MeshComponent>() const;

} // namespace ecs
} // namespace omnicpp
