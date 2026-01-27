#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <memory>

namespace OmniCpp {

class VulkanInstance;

/**
 * @brief Vulkan device wrapper
 * 
 * This class wraps Vulkan physical and logical devices
 * and provides methods for managing device lifecycle.
 */
class VulkanDevice {
public:
    VulkanDevice();
    ~VulkanDevice();

    /**
     * @brief Initialize Vulkan device
     * @param instance Vulkan instance
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize(VkInstance instance);

    /**
     * @brief Shutdown Vulkan device
     */
    void shutdown();

    /**
     * @brief Get physical device
     * @return Physical device handle
     */
    VkPhysicalDevice getPhysicalDevice() const { return m_physicalDevice; }

    /**
     * @brief Get logical device
     * @return Logical device handle
     */
    VkDevice getDevice() const { return m_device; }

    /**
     * @brief Get graphics queue
     * @return Graphics queue handle
     */
    VkQueue getGraphicsQueue() const { return m_graphicsQueue; }

    /**
     * @brief Get graphics queue family index
     * @return Graphics queue family index
     */
    uint32_t getGraphicsQueueFamily() const { return m_graphicsQueueFamily; }

private:
    bool pickPhysicalDevice(VkInstance instance);
    bool isDeviceSuitable(VkPhysicalDevice device);
    bool createLogicalDevice();

    VkPhysicalDevice m_physicalDevice = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    VkQueue m_graphicsQueue = VK_NULL_HANDLE;
    uint32_t m_graphicsQueueFamily = 0;
};

} // namespace OmniCpp
