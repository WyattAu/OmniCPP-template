#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>

namespace OmniCpp {

/**
 * @brief Vulkan instance wrapper
 * 
 * This class wraps the Vulkan instance and provides
 * methods for managing Vulkan instance lifecycle.
 */
class VulkanInstance {
public:
    VulkanInstance();
    ~VulkanInstance();

    /**
     * @brief Initialize Vulkan instance
     * @param appName Application name
     * @param appVersion Application version
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize(const std::string& appName, uint32_t appVersion);

    /**
     * @brief Shutdown Vulkan instance
     */
    void shutdown();

    /**
     * @brief Get Vulkan instance handle
     * @return Vulkan instance handle
     */
    VkInstance getInstance() const { return m_instance; }

    /**
     * @brief Get enabled extensions
     * @return List of enabled extensions
     */
    const std::vector<const char*>& getEnabledExtensions() const { return m_enabledExtensions; }

private:
    bool checkValidationLayerSupport();
    std::vector<const char*> getRequiredExtensions();
    void setupDebugMessenger();

    VkInstance m_instance = VK_NULL_HANDLE;
    VkDebugUtilsMessengerEXT m_debugMessenger = VK_NULL_HANDLE;
    std::vector<const char*> m_enabledExtensions;
    bool m_enableValidationLayers = false;
};

} // namespace OmniCpp
