/**
 * @file TransformComponent.hpp
 * @brief Transform component for position, rotation, and scale
 * @version 1.0.0
 */

#pragma once

#include "engine/ecs/Component.hpp"
#include "engine/math/Vec3.hpp"
#include "engine/math/Mat4.hpp"

namespace omnicpp {
namespace ecs {

using math::Vec3;
using math::Mat4;

/**
 * @brief Transform component for position, rotation, and scale
 * 
 * This component stores the spatial transformation of an entity.
 */
class TransformComponent : public Component {
public:
    /**
     * @brief Construct a new Transform Component object
     * @param entity_id The entity ID
     */
    explicit TransformComponent(uint64_t entity_id);

    /**
     * @brief Construct a new Transform Component object with initial values
     * @param entity_id The entity ID
     * @param position Initial position
     * @param rotation Initial rotation (Euler angles in degrees)
     * @param scale Initial scale
     */
    TransformComponent(uint64_t entity_id, 
                   const Vec3& position,
                   const Vec3& rotation,
                   const Vec3& scale);

    /**
     * @brief Get position
     * @return const Vec3& The position
     */
    const Vec3& get_position() const { return m_position; }

    /**
     * @brief Set position
     * @param position The new position
     */
    void set_position(const Vec3& position) { m_position = position; }

    /**
     * @brief Get rotation (Euler angles in degrees)
     * @return const Vec3& The rotation
     */
    const Vec3& get_rotation() const { return m_rotation; }

    /**
     * @brief Set rotation (Euler angles in degrees)
     * @param rotation The new rotation
     */
    void set_rotation(const Vec3& rotation) { m_rotation = rotation; }

    /**
     * @brief Get scale
     * @return const Vec3& The scale
     */
    const Vec3& get_scale() const { return m_scale; }

    /**
     * @brief Set scale
     * @param scale The new scale
     */
    void set_scale(const Vec3& scale) { m_scale = scale; }

    /**
     * @brief Translate by a vector
     * @param delta The translation vector
     */
    void translate(const Vec3& delta);

    /**
     * @brief Rotate by Euler angles
     * @param delta The rotation vector (in degrees)
     */
    void rotate(const Vec3& delta);

    /**
     * @brief Scale by a factor
     * @param factor The scale factor
     */
    void scale(const Vec3& factor);

    /**
     * @brief Get the transformation matrix
     * @return Mat4 The transformation matrix
     */
    Mat4 get_transform_matrix() const;

private:
    Vec3 m_position{0.0f, 0.0f, 0.0f};
    Vec3 m_rotation{0.0f, 0.0f, 0.0f};
    Vec3 m_scale{1.0f, 1.0f, 1.0f};
};

} // namespace ecs
} // namespace omnicpp
