/**
 * @file CameraComponent.hpp
 * @brief Camera component for 3D rendering
 * @version 1.0.0
 */

#pragma once

#include "engine/ecs/Component.hpp"
#include "math.hpp"

namespace omnicpp {
namespace ecs {

/**
 * @brief Camera type enumeration
 */
enum class CameraType {
    PERSPECTIVE,
    ORTHOGRAPHIC
};

/**
 * @brief Camera component for 3D rendering
 * 
 * This component stores camera parameters for rendering.
 */
class CameraComponent : public Component {
public:
    /**
     * @brief Construct a new Camera Component object
     * @param entity_id The entity ID
     */
    explicit CameraComponent(uint64_t entity_id);

    /**
     * @brief Construct a new Camera Component object with parameters
     * @param entity_id The entity ID
     * @param type The camera type
     * @param fov Field of view in degrees (perspective only)
     * @param near_plane Near clipping plane
     * @param far_plane Far clipping plane
     */
    CameraComponent(uint64_t entity_id,
                 CameraType type,
                 float fov = 60.0f,
                 float near_plane = 0.1f,
                 float far_plane = 1000.0f);

    /**
     * @brief Get camera type
     * @return CameraType The camera type
     */
    CameraType get_type() const { return m_type; }

    /**
     * @brief Set camera type
     * @param type The new camera type
     */
    void set_type(CameraType type) { m_type = type; }

    /**
     * @brief Get field of view
     * @return float The field of view in degrees
     */
    float get_fov() const { return m_fov; }

    /**
     * @brief Set field of view
     * @param fov The new field of view in degrees
     */
    void set_fov(float fov) { m_fov = fov; }

    /**
     * @brief Get near clipping plane
     * @return float The near clipping plane
     */
    float get_near_plane() const { return m_near_plane; }

    /**
     * @brief Set near clipping plane
     * @param near_plane The new near clipping plane
     */
    void set_near_plane(float near_plane) { m_near_plane = near_plane; }

    /**
     * @brief Get far clipping plane
     * @return float The far clipping plane
     */
    float get_far_plane() const { return m_far_plane; }

    /**
     * @brief Set far clipping plane
     * @param far_plane The new far clipping plane
     */
    void set_far_plane(float far_plane) { m_far_plane = far_plane; }

    /**
     * @brief Get view matrix
     * @return Mat4 The view matrix
     */
    Mat4 get_view_matrix() const;

    /**
     * @brief Get projection matrix
     * @param aspect_ratio The aspect ratio (width/height)
     * @return Mat4 The projection matrix
     */
    Mat4 get_projection_matrix(float aspect_ratio) const;

private:
    CameraType m_type = CameraType::PERSPECTIVE;
    float m_fov = 60.0f;
    float m_near_plane = 0.1f;
    float m_far_plane = 1000.0f;
};

} // namespace ecs
} // namespace omnicpp
