/**
 * @file Component.cpp
 * @brief Component implementation for Entity Component System (ECS)
 * @version 1.0.0
 */

#include "engine/ecs/Component.hpp"

namespace omnicpp {
namespace ecs {

Component::Component(uint64_t entity_id)
    : m_entity_id(entity_id) {
}

} // namespace ecs
} // namespace omnicpp
