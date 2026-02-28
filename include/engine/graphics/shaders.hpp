/**
 * @file shaders.hpp
 * @brief Shader sources for 3D rendering
 * @version 1.0.0
 */

#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace OmniCpp::Engine::Graphics {

/**
 * @brief Get vertex shader source code (GLSL)
 */
inline const char* get_vertex_shader_glsl() {
    return R"(
#version 450

// Vertex input
layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 inTexCoord;

// Uniform buffer for transformation matrices
layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;

// Outputs to fragment shader
layout(location = 0) out vec3 fragColor;
layout(location = 1) out vec2 fragTexCoord;

void main() {
    gl_Position = ubo.proj * ubo.view * ubo.model * vec4(inPosition, 1.0);
    fragColor = inColor;
    fragTexCoord = inTexCoord;
}
)";
}

/**
 * @brief Get fragment shader source code (GLSL)
 */
inline const char* get_fragment_shader_glsl() {
    return R"(
#version 450

// Inputs from vertex shader
layout(location = 0) in vec3 fragColor;
layout(location = 1) in vec2 fragTexCoord;

// Output color
layout(location = 0) out vec4 outColor;

void main() {
    outColor = vec4(fragColor, 1.0);
}
)";
}

/**
 * @brief Get vertex shader code as vector of chars
 */
inline std::vector<char> get_vertex_shader_code() {
    std::string shader = get_vertex_shader_glsl();
    return std::vector<char>(shader.begin(), shader.end());
}

/**
 * @brief Get fragment shader code as vector of chars
 */
inline std::vector<char> get_fragment_shader_code() {
    std::string shader = get_fragment_shader_glsl();
    return std::vector<char>(shader.begin(), shader.end());
}

} // namespace OmniCpp::Engine::Graphics
