/**
 * @file MeshComponent.hpp
 * @brief Mesh component for rendering 3D geometry
 * @version 1.0.0
 */

#pragma once

#include "engine/ecs/Component.hpp"
#include <cstdint>
#include <vector>

namespace omnicpp {
namespace ecs {

// Forward declarations
class Mesh;
class Material;

/**
 * @brief Mesh component for rendering 3D geometry
 * 
 * This component stores mesh and material data for rendering.
 */
class MeshComponent : public Component {
public:
    /**
     * @brief Construct a new Mesh Component object
     * @param entity_id The entity ID
     */
    explicit MeshComponent(uint64_t entity_id);

    /**
     * @brief Construct a new Mesh Component object with mesh and material
     * @param entity_id The entity ID
     * @param mesh Pointer to the mesh
     * @param material Pointer to the material
     */
    MeshComponent(uint64_t entity_id, Mesh* mesh, Material* material);

    /**
     * @brief Get the mesh
     * @return Mesh* Pointer to the mesh
     */
    Mesh* get_mesh() const { return m_mesh; }

    /**
     * @brief Set the mesh
     * @param mesh Pointer to the mesh
     */
    void set_mesh(Mesh* mesh) { m_mesh = mesh; }

    /**
     * @brief Get the material
     * @return Material* Pointer to the material
     */
    Material* get_material() const { return m_material; }

    /**
     * @brief Set the material
     * @param material Pointer to the material
     */
    void set_material(Material* material) { m_material = material; }

    /**
     * @brief Check if mesh is visible
     * @return true if visible, false otherwise
     */
    bool is_visible() const { return m_visible; }

    /**
     * @brief Set visibility
     * @param visible The new visibility state
     */
    void set_visible(bool visible) { m_visible = visible; }

    /**
     * @brief Check if mesh casts shadows
     * @return true if casts shadows, false otherwise
     */
    bool casts_shadows() const { return m_casts_shadows; }

    /**
     * @brief Set shadow casting
     * @param casts_shadows The new shadow casting state
     */
    void set_casts_shadows(bool casts_shadows) { m_casts_shadows = casts_shadows; }

private:
    Mesh* m_mesh = nullptr;
    Material* m_material = nullptr;
    bool m_visible = true;
    bool m_casts_shadows = true;
};

} // namespace ecs
} // namespace omnicpp
