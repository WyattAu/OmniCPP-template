#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <memory>

namespace OmniCpp {

class VulkanDevice;

/**
 * @brief Vulkan renderer
 * 
 * This class handles Vulkan rendering operations.
 */
class VulkanRenderer {
public:
    VulkanRenderer();
    ~VulkanRenderer();

    /**
     * @brief Initialize Vulkan renderer
     * @param device Vulkan device
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize(VkDevice device, VkPhysicalDevice physicalDevice);

    /**
     * @brief Shutdown Vulkan renderer
     */
    void shutdown();

    /**
     * @brief Begin frame
     */
    void beginFrame();

    /**
     * @brief End frame
     */
    void endFrame();

    /**
     * @brief Render frame
     */
    void render();

private:
    bool createRenderPass();
    bool createPipeline();
    bool createFramebuffers();
    bool createCommandBuffers();

    VkDevice m_device = VK_NULL_HANDLE;
    VkPhysicalDevice m_physicalDevice = VK_NULL_HANDLE;
    VkRenderPass m_renderPass = VK_NULL_HANDLE;
    VkPipeline m_pipeline = VK_NULL_HANDLE;
    VkPipelineLayout m_pipelineLayout = VK_NULL_HANDLE;
    std::vector<VkFramebuffer> m_framebuffers;
    std::vector<VkCommandBuffer> m_commandBuffers;
    uint32_t m_currentFrame = 0;
};

} // namespace OmniCpp
