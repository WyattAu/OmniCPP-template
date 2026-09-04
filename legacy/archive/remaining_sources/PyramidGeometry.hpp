#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <array>

namespace OmniCpp {

/**
 * @brief Pyramid geometry
 * 
 * This class provides pyramid geometry for rendering.
 */
class PyramidGeometry {
public:
    PyramidGeometry();
    ~PyramidGeometry() = default;

    /**
     * @brief Get vertices
     * @return Vector of vertices
     */
    const std::vector<float>& getVertices() const { return m_vertices; }

    /**
     * @brief Get indices
     * @return Vector of indices
     */
    const std::vector<uint16_t>& getIndices() const { return m_indices; }

    /**
     * @brief Get vertex count
     * @return Number of vertices
     */
    size_t getVertexCount() const { return m_vertices.size() / 3; }

    /**
     * @brief Get index count
     * @return Number of indices
     */
    size_t getIndexCount() const { return m_indices.size(); }

private:
    void createPyramid();

    std::vector<float> m_vertices;
    std::vector<uint16_t> m_indices;
};

} // namespace OmniCpp
