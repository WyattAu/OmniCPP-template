/**
 * @file ShaderManager.hpp
 * @brief Shader manager for Vulkan
 * @version 1.0.0
 */

#pragma once

#include <vulkan/vulkan.h>
#include <string>
#include <unordered_map>
#include <vector>

namespace omnicpp {
namespace render {

/**
 * @brief Shader module wrapper
 */
struct ShaderModule {
    VkShaderModule module = VK_NULL_HANDLE;
    std::string entry_point = "main";
};

/**
 * @brief Shader manager for Vulkan
 * 
 * Manages loading, compilation, and lifecycle of shaders.
 */
class ShaderManager {
public:
    /**
     * @brief Construct a new Shader Manager object
     * @param device Vulkan logical device
     */
    explicit ShaderManager(VkDevice device);

    /**
     * @brief Destroy the Shader Manager object
     */
    ~ShaderManager();

    // Disable copying
    ShaderManager(const ShaderManager&) = delete;
    ShaderManager& operator=(const ShaderManager&) = delete;

    // Enable moving
    ShaderManager(ShaderManager&&) noexcept = default;
    ShaderManager& operator=(ShaderManager&&) noexcept = default;

    /**
     * @brief Load a shader from SPIR-V file
     * @param filename Path to shader file
     * @param entry_point Entry point name (default: "main")
     * @return ShaderModule The loaded shader module
     */
    ShaderModule load_shader(const std::string& filename, 
                        const std::string& entry_point = "main");

    /**
     * @brief Create a shader stage create info
     * @param module The shader module
     * @param stage The shader stage (vertex, fragment, etc.)
     * @return VkPipelineShaderStageCreateInfo The shader stage create info
     */
    VkPipelineShaderStageCreateInfo create_shader_stage_info(
        const ShaderModule& module, 
        VkShaderStageFlagBits stage);

    /**
     * @brief Get Vulkan device
     * @return VkDevice The logical device
     */
    VkDevice get_device() const { return m_device; }

private:
    /**
     * @brief Read SPIR-V shader file
     * @param filename Path to shader file
     * @return std::vector<char> The shader bytecode
     */
    std::vector<char> read_shader_file(const std::string& filename);

    /**
     * @brief Create shader module from bytecode
     * @param code The shader bytecode
     * @return VkShaderModule The created shader module
     */
    VkShaderModule create_shader_module(const std::vector<char>& code);

private:
    VkDevice m_device = VK_NULL_HANDLE;
    std::unordered_map<std::string, ShaderModule> m_shaders;
};

} // namespace render
} // namespace omnicpp
