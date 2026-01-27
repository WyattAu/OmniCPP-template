#pragma once

#include <vulkan/vulkan.h>
#include <string>
#include <vector>

namespace OmniCpp {

/**
 * @brief Shader manager
 * 
 * This class manages Vulkan shaders.
 */
class ShaderManager {
public:
    ShaderManager();
    ~ShaderManager();

    /**
     * @brief Initialize shader manager
     * @param device Vulkan device
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize(VkDevice device);

    /**
     * @brief Shutdown shader manager
     */
    void shutdown();

    /**
     * @brief Load shader from file
     * @param filename Shader filename
     * @return Shader module handle
     */
    VkShaderModule loadShader(const std::string& filename);

private:
    std::vector<char> readFile(const std::string& filename);

    VkDevice m_device = VK_NULL_HANDLE;
};

} // namespace OmniCpp
