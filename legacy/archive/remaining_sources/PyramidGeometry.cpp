#include "Vulkan/PyramidGeometry.hpp"
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logPyramidGeometry, "omnicpp.pyramidgeometry")

namespace OmniCpp {

PyramidGeometry::PyramidGeometry()
{
    qCDebug(logPyramidGeometry) << "Creating pyramid geometry...";
    createPyramid();
    qCDebug(logPyramidGeometry) << "Pyramid geometry created";
}

void PyramidGeometry::createPyramid()
{
    // Create pyramid vertices
    // A pyramid has 5 vertices (4 base + 1 top)
    // Each vertex has position (x, y, z) and color (r, g, b)
    
    // Base vertices (bottom square)
    // Front-left
    m_vertices.push_back(-1.0f); // x
    m_vertices.push_back(-1.0f); // y
    m_vertices.push_back(1.0f);  // z
    m_vertices.push_back(1.0f);  // r
    m_vertices.push_back(0.0f);  // g
    m_vertices.push_back(0.0f);  // b
    
    // Front-right
    m_vertices.push_back(1.0f);  // x
    m_vertices.push_back(-1.0f); // y
    m_vertices.push_back(1.0f);  // z
    m_vertices.push_back(0.0f);  // r
    m_vertices.push_back(1.0f);  // g
    m_vertices.push_back(0.0f);  // b
    
    // Back-right
    m_vertices.push_back(1.0f);  // x
    m_vertices.push_back(-1.0f); // y
    m_vertices.push_back(-1.0f); // z
    m_vertices.push_back(0.0f);  // r
    m_vertices.push_back(0.0f);  // g
    m_vertices.push_back(1.0f);  // b
    
    // Back-left
    m_vertices.push_back(-1.0f); // x
    m_vertices.push_back(-1.0f); // y
    m_vertices.push_back(-1.0f); // z
    m_vertices.push_back(0.0f);  // r
    m_vertices.push_back(1.0f);  // g
    m_vertices.push_back(1.0f);  // b
    
    // Top vertex
    m_vertices.push_back(0.0f);  // x
    m_vertices.push_back(1.0f);  // y
    m_vertices.push_back(0.0f);  // z
    m_vertices.push_back(1.0f);  // r
    m_vertices.push_back(1.0f);  // g
    m_vertices.push_back(0.0f);  // b
    
    // Create pyramid indices
    // Front face
    m_indices.push_back(0); // Front-left
    m_indices.push_back(1); // Front-right
    m_indices.push_back(4); // Top
    
    // Right face
    m_indices.push_back(1); // Front-right
    m_indices.push_back(2); // Back-right
    m_indices.push_back(4); // Top
    
    // Back face
    m_indices.push_back(2); // Back-right
    m_indices.push_back(3); // Back-left
    m_indices.push_back(4); // Top
    
    // Left face
    m_indices.push_back(3); // Back-left
    m_indices.push_back(0); // Front-left
    m_indices.push_back(4); // Top
    
    // Bottom face (two triangles)
    m_indices.push_back(0); // Front-left
    m_indices.push_back(1); // Front-right
    m_indices.push_back(2); // Back-right
    
    m_indices.push_back(0); // Front-left
    m_indices.push_back(2); // Back-right
    m_indices.push_back(3); // Back-left
    
    qCDebug(logPyramidGeometry) << "Pyramid vertices:" << getVertexCount();
    qCDebug(logPyramidGeometry) << "Pyramid indices:" << getIndexCount();
}

} // namespace OmniCpp
