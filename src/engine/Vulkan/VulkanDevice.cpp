#include "Vulkan/VulkanDevice.hpp"
#include <QLoggingCategory>
#include <set>
#include <algorithm>

Q_LOGGING_CATEGORY(logVulkanDevice, "omnicpp.vulkandevice")

namespace OmniCpp {

VulkanDevice::VulkanDevice()
    : m_physicalDevice(VK_NULL_HANDLE)
    , m_device(VK_NULL_HANDLE)
    , m_graphicsQueue(VK_NULL_HANDLE)
    , m_graphicsQueueFamily(0)
{
}

VulkanDevice::~VulkanDevice()
{
    shutdown();
}

bool VulkanDevice::initialize(VkInstance instance)
{
    qCDebug(logVulkanDevice) << "Initializing Vulkan device...";

    if (!pickPhysicalDevice(instance)) {
        qCCritical(logVulkanDevice) << "Failed to pick physical device";
        return false;
    }

    if (!createLogicalDevice()) {
        qCCritical(logVulkanDevice) << "Failed to create logical device";
        return false;
    }

    qCDebug(logVulkanDevice) << "Vulkan device initialized successfully";
    return true;
}

void VulkanDevice::shutdown()
{
    qCDebug(logVulkanDevice) << "Shutting down Vulkan device...";

    if (m_device != VK_NULL_HANDLE) {
        vkDestroyDevice(m_device, nullptr);
        m_device = VK_NULL_HANDLE;
    }

    m_physicalDevice = VK_NULL_HANDLE;
    m_graphicsQueue = VK_NULL_HANDLE;

    qCDebug(logVulkanDevice) << "Vulkan device shut down";
}

bool VulkanDevice::pickPhysicalDevice(VkInstance instance)
{
    qCDebug(logVulkanDevice) << "Picking physical device...";

    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

    if (deviceCount == 0) {
        qCCritical(logVulkanDevice) << "No physical devices found";
        return false;
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());

    // Use an ordered map to automatically sort candidates by increasing score
    std::multimap<int, VkPhysicalDevice> candidates;

    for (const auto& device : devices) {
        int score = 0;
        VkPhysicalDeviceProperties deviceProperties;
        vkGetPhysicalDeviceProperties(device, &deviceProperties);

        // Discrete GPUs have a significant performance advantage
        if (deviceProperties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) {
            score += 1000;
        }

        // Maximum possible size of textures affects graphics quality
        score += deviceProperties.limits.maxImageDimension2D;

        // Check if device is suitable
        if (isDeviceSuitable(device)) {
            candidates.insert(std::make_pair(score, device));
        }
    }

    // Check if the best candidate is suitable at all
    if (candidates.rbegin()->second == VK_NULL_HANDLE) {
        qCCritical(logVulkanDevice) << "No suitable physical device found";
        return false;
    }

    m_physicalDevice = candidates.rbegin()->second;

    VkPhysicalDeviceProperties deviceProperties;
    vkGetPhysicalDeviceProperties(m_physicalDevice, &deviceProperties);
    qCDebug(logVulkanDevice) << "Selected physical device:" << deviceProperties.deviceName;

    return true;
}

bool VulkanDevice::isDeviceSuitable(VkPhysicalDevice device)
{
    // Get queue family properties
    uint32_t queueFamilyCount = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);
    std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());

    // Check for graphics queue family
    for (uint32_t i = 0; i < queueFamilyCount; ++i) {
        if (queueFamilies[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
            m_graphicsQueueFamily = i;
            return true;
        }
    }

    return false;
}

bool VulkanDevice::createLogicalDevice()
{
    qCDebug(logVulkanDevice) << "Creating logical device...";

    // Get queue family properties
    uint32_t queueFamilyCount = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(m_physicalDevice, &queueFamilyCount, nullptr);
    std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
    vkGetPhysicalDeviceQueueFamilyProperties(m_physicalDevice, &queueFamilyCount, queueFamilies.data());

    // Create queue info
    VkDeviceQueueCreateInfo queueCreateInfo{};
    queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    queueCreateInfo.queueFamilyIndex = m_graphicsQueueFamily;
    queueCreateInfo.queueCount = 1;
    float queuePriority = 1.0f;
    queueCreateInfo.pQueuePriorities = &queuePriority;

    // Get device extensions
    uint32_t extensionCount = 0;
    vkEnumerateDeviceExtensionProperties(m_physicalDevice, nullptr, &extensionCount, nullptr);
    std::vector<VkExtensionProperties> availableExtensions(extensionCount);
    vkEnumerateDeviceExtensionProperties(m_physicalDevice, nullptr, &extensionCount, availableExtensions.data());

    // Enable swapchain extension
    std::vector<const char*> enabledExtensions;
    enabledExtensions.push_back(VK_KHR_SWAPCHAIN_EXTENSION_NAME);

    // Create logical device
    VkDeviceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
    createInfo.queueCreateInfoCount = 1;
    createInfo.pQueueCreateInfos = &queueCreateInfo;
    createInfo.enabledExtensionCount = static_cast<uint32_t>(enabledExtensions.size());
    createInfo.ppEnabledExtensionNames = enabledExtensions.data();

    if (vkCreateDevice(m_physicalDevice, &createInfo, nullptr, &m_device) != VK_SUCCESS) {
        qCCritical(logVulkanDevice) << "Failed to create logical device";
        return false;
    }

    // Get graphics queue
    vkGetDeviceQueue(m_device, m_graphicsQueueFamily, 0, &m_graphicsQueue);

    qCDebug(logVulkanDevice) << "Logical device created successfully";
    return true;
}

} // namespace OmniCpp
