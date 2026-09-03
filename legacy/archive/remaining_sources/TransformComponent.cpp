/**
 * @file TransformComponent.cpp
 * @brief Transform component implementation
 * @version 1.0.0
 */

#include "engine/ecs/TransformComponent.hpp"
#include "math.hpp"
#include <cmath>
#include "engine/logging/Log.hpp"

namespace omnicpp {
namespace ecs {

TransformComponent::TransformComponent(uint64_t entity_id)
    : Component(entity_id) {
    omnicpp::log::debug("TransformComponent: Created transform component for entity {}", entity_id);
}

TransformComponent::TransformComponent(uint64_t entity_id,
                               const Vec3& position,
                               const Vec3& rotation,
                               const Vec3& scale)
    : Component(entity_id)
    , m_position(position)
    , m_rotation(rotation)
    , m_scale(scale) {
    omnicpp::log::debug("TransformComponent: Created transform component for entity {} with position ({}, {}, {})", entity_id, position.x, position.y, position.z);
}

void TransformComponent::translate(const Vec3& delta) {
    m_position.x += delta.x;
    m_position.y += delta.y;
    m_position.z += delta.z;
}

void TransformComponent::rotate(const Vec3& delta) {
    m_rotation.x += delta.x;
    m_rotation.y += delta.y;
    m_rotation.z += delta.z;
}

void TransformComponent::scale(const Vec3& factor) {
    m_scale.x *= factor.x;
    m_scale.y *= factor.y;
    m_scale.z *= factor.z;
}

Mat4 TransformComponent::get_transform_matrix() const {
    // Create transformation matrix from position, rotation, and scale
    // This is a simplified implementation
    Mat4 transform = Mat4::create_identity();

    // Apply translation
    transform = transform * Mat4::translation(m_position);

    // Apply rotation (simplified - just using rotation around Y axis)
    float angle_rad = m_rotation.y * 3.14159265f / 180.0f;
    float cos_a = std::cos(angle_rad);
    float sin_a = std::sin(angle_rad);

    Mat4 rotation_matrix = Mat4::create_identity();
    rotation_matrix.m[0][0] = cos_a;
    rotation_matrix.m[0][2] = sin_a;
    rotation_matrix.m[2][0] = -sin_a;
    rotation_matrix.m[2][2] = cos_a;

    transform = transform * rotation_matrix;

    // Apply scale
    transform = transform * Mat4::scale(m_scale);

    return transform;
}

} // namespace ecs
} // namespace omnicpp
