/**
 * @file Component.cpp
 * @brief Component implementation for Entity Component System (ECS)
 * @version 1.0.0
 */

#include "engine/ecs/Component.hpp"
#include <spdlog/spdlog.h>

namespace omnicpp {
namespace ecs {

Component::Component(uint64_t entity_id)
    : m_entity_id(entity_id) {
    spdlog::debug("Component: Created component for entity {}", entity_id);
}

} // namespace ecs
} // namespace omnicpp
