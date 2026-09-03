#pragma once

#include <vulkan/vulkan.h>
#include <QVulkanInstance>
#include <QVulkanDeviceFunctions>
#include <memory>

namespace OmniCpp {

/**
 * @brief Qt/Vulkan integration class
 * 
 * This class provides integration between Qt6 and Vulkan,
 * enabling Qt widgets to render Vulkan content.
 */
class QtVulkanIntegration {
public:
    QtVulkanIntegration();
    ~QtVulkanIntegration();

    /**
     * @brief Initialize the Qt/Vulkan integration
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown the Qt/Vulkan integration
     */
    void shutdown();

    /**
     * @brief Get the Qt Vulkan instance
     * @return Pointer to the Qt Vulkan instance
     */
    QVulkanInstance* getQtVulkanInstance() const { return m_qtVulkanInstance.get(); }

    /**
     * @brief Get the Vulkan instance
     * @return Vulkan instance handle
     */
    VkInstance getVulkanInstance() const { return m_vkInstance; }

    /**
     * @brief Get the Vulkan physical device
     * @return Vulkan physical device handle
     */
    VkPhysicalDevice getPhysicalDevice() const { return m_physicalDevice; }

    /**
     * @brief Get the Vulkan device
     * @return Vulkan device handle
     */
    VkDevice getDevice() const { return m_device; }

    /**
     * @brief Get the Vulkan device functions
     * @return Pointer to the Vulkan device functions
     */
    QVulkanDeviceFunctions* getDeviceFunctions() const { return m_deviceFunctions; }

    /**
     * @brief Get the graphics queue family index
     * @return Graphics queue family index
     */
    uint32_t getGraphicsQueueFamily() const { return m_graphicsQueueFamily; }

    /**
     * @brief Get the graphics queue
     * @return Graphics queue handle
     */
    VkQueue getGraphicsQueue() const { return m_graphicsQueue; }

private:
    std::unique_ptr<QVulkanInstance> m_qtVulkanInstance;
    VkInstance m_vkInstance = VK_NULL_HANDLE;
    VkPhysicalDevice m_physicalDevice = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    QVulkanDeviceFunctions* m_deviceFunctions = nullptr;
    uint32_t m_graphicsQueueFamily = 0;
    VkQueue m_graphicsQueue = VK_NULL_HANDLE;

    bool createVulkanInstance();
    bool selectPhysicalDevice();
    bool createLogicalDevice();
};

} // namespace OmniCpp
