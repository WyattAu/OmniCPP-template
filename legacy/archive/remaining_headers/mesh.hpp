/**
 * @file mesh.hpp
 * @brief 3D mesh generation utilities for game objects
 * @version 1.0.0
 */

#pragma once

#include <vector>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

namespace OmniCpp::Engine::Graphics {

/**
 * @brief Vertex structure for 3D rendering
 */
struct MeshVertex {
    glm::vec3 position;
    glm::vec3 color;
    glm::vec2 texCoord;
};

/**
 * @brief Mesh data structure containing vertices and indices
 */
struct Mesh {
    std::vector<MeshVertex> vertices;
    std::vector<uint32_t> indices;
};

/**
 * @brief Generate a cube mesh
 * @param size Size of the cube (width, height, depth)
 * @param color Color of the cube faces
 * @return Mesh data
 */
inline Mesh generate_cube(glm::vec3 size, glm::vec3 color) {
    Mesh mesh;
    
    float w = size.x / 2.0f;
    float h = size.y / 2.0f;
    float d = size.z / 2.0f;
    
    // Front face
    mesh.vertices.push_back({{-w, -h,  d}, color, {0.0f, 0.0f}});
    mesh.vertices.push_back({{ w, -h,  d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{ w,  h,  d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{-w,  h,  d}, color, {0.0f, 1.0f}});
    
    // Back face
    mesh.vertices.push_back({{-w, -h, -d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{-w,  h, -d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{ w,  h, -d}, color, {0.0f, 1.0f}});
    mesh.vertices.push_back({{ w, -h, -d}, color, {0.0f, 0.0f}});
    
    // Top face
    mesh.vertices.push_back({{-w,  h, -d}, color, {0.0f, 0.0f}});
    mesh.vertices.push_back({{-w,  h,  d}, color, {0.0f, 1.0f}});
    mesh.vertices.push_back({{ w,  h,  d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{ w,  h, -d}, color, {1.0f, 0.0f}});
    
    // Bottom face
    mesh.vertices.push_back({{-w, -h, -d}, color, {0.0f, 1.0f}});
    mesh.vertices.push_back({{ w, -h, -d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{ w, -h,  d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{-w, -h,  d}, color, {0.0f, 0.0f}});
    
    // Right face
    mesh.vertices.push_back({{ w, -h, -d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{ w,  h, -d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{ w,  h,  d}, color, {0.0f, 1.0f}});
    mesh.vertices.push_back({{ w, -h,  d}, color, {0.0f, 0.0f}});
    
    // Left face
    mesh.vertices.push_back({{-w, -h, -d}, color, {0.0f, 0.0f}});
    mesh.vertices.push_back({{-w, -h,  d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{-w,  h,  d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{-w,  h, -d}, color, {0.0f, 1.0f}});
    
    // Generate indices for each face (2 triangles per face)
    for (int face = 0; face < 6; face++) {
        uint32_t base = face * 4;
        mesh.indices.push_back(base + 0);
        mesh.indices.push_back(base + 1);
        mesh.indices.push_back(base + 2);
        mesh.indices.push_back(base + 0);
        mesh.indices.push_back(base + 2);
        mesh.indices.push_back(base + 3);
    }
    
    return mesh;
}

/**
 * @brief Generate a sphere mesh
 * @param radius Radius of the sphere
 * @param segments Number of horizontal segments
 * @param rings Number of vertical rings
 * @param color Color of the sphere
 * @return Mesh data
 */
inline Mesh generate_sphere(float radius, int segments, int rings, glm::vec3 color) {
    Mesh mesh;
    
    for (int ring = 0; ring <= rings; ring++) {
        float phi = static_cast<float>(ring) * glm::pi<float>() / static_cast<float>(rings);
        float y = std::cos(phi) * radius;
        float ringRadius = std::sin(phi) * radius;
        
        for (int seg = 0; seg <= segments; seg++) {
            float theta = static_cast<float>(seg) * 2.0f * glm::pi<float>() / static_cast<float>(segments);
            float x = std::cos(theta) * ringRadius;
            float z = std::sin(theta) * ringRadius;
            
            mesh.vertices.push_back({
                {x, y, z},
                color,
                {static_cast<float>(seg) / static_cast<float>(segments),
                 static_cast<float>(ring) / static_cast<float>(rings)}
            });
        }
    }
    
    // Generate indices
    for (int ring = 0; ring < rings; ring++) {
        for (int seg = 0; seg < segments; seg++) {
            uint32_t current = ring * (segments + 1) + seg;
            uint32_t next = current + segments + 1;
            
            mesh.indices.push_back(current);
            mesh.indices.push_back(next);
            mesh.indices.push_back(current + 1);
            
            mesh.indices.push_back(current + 1);
            mesh.indices.push_back(next);
            mesh.indices.push_back(next + 1);
        }
    }
    
    return mesh;
}

/**
 * @brief Generate a flat plane mesh (for the game field)
 * @param width Width of the plane
 * @param depth Depth of the plane
 * @param color Color of the plane
 * @return Mesh data
 */
inline Mesh generate_plane(float width, float depth, glm::vec3 color) {
    Mesh mesh;
    
    float w = width / 2.0f;
    float d = depth / 2.0f;
    
    // Two triangles forming a quad
    mesh.vertices.push_back({{-w, 0.0f, -d}, color, {0.0f, 0.0f}});
    mesh.vertices.push_back({{ w, 0.0f, -d}, color, {1.0f, 0.0f}});
    mesh.vertices.push_back({{ w, 0.0f,  d}, color, {1.0f, 1.0f}});
    mesh.vertices.push_back({{-w, 0.0f,  d}, color, {0.0f, 1.0f}});
    
    mesh.indices.push_back(0);
    mesh.indices.push_back(1);
    mesh.indices.push_back(2);
    mesh.indices.push_back(0);
    mesh.indices.push_back(2);
    mesh.indices.push_back(3);
    
    return mesh;
}

/**
 * @brief Generate a line (for the center line on the field)
 * @param start Start point
 * @param end End point
 * @param color Color of the line
 * @return Mesh data
 */
inline Mesh generate_line(glm::vec3 start, glm::vec3 end, glm::vec3 color) {
    Mesh mesh;
    
    mesh.vertices.push_back({start, color, {0.0f, 0.0f}});
    mesh.vertices.push_back({end, color, {1.0f, 1.0f}});
    
    mesh.indices.push_back(0);
    mesh.indices.push_back(1);
    
    return mesh;
}

} // namespace OmniCpp::Engine::Graphics
