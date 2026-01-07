#include "Qt/QtVulkanIntegration.hpp"
#include <QVulkanInstance>
#include <QVulkanDeviceFunctions>
#include <QSurface>
#include <QLoggingCategory>
#include <vector>
#include <set>

Q_LOGGING_CATEGORY(logVulkan, "omnicpp.vulkan")

namespace OmniCpp {

QtVulkanIntegration::QtVulkanIntegration()
    : m_qtVulkanInstance(std::make_unique<QVulkanInstance>())
{
}

QtVulkanIntegration::~QtVulkanIntegration()
{
    shutdown();
}

bool QtVulkanIntegration::initialize()
{
    qCDebug(logVulkan) << "Initializing Qt/Vulkan integration...";

    if (!createVulkanInstance()) {
        qCCritical(logVulkan) << "Failed to create Vulkan instance";
        return false;
    }

    if (!selectPhysicalDevice()) {
        qCCritical(logVulkan) << "Failed to select physical device";
        return false;
    }

    if (!createLogicalDevice()) {
        qCCritical(logVulkan) << "Failed to create logical device";
        return false;
    }

    qCDebug(logVulkan) << "Qt/Vulkan integration initialized successfully";
    return true;
}

void QtVulkanIntegration::shutdown()
{
    qCDebug(logVulkan) << "Shutting down Qt/Vulkan integration...";

    if (m_device) {
        vkDestroyDevice(m_device, nullptr);
        m_device = VK_NULL_HANDLE;
    }

    if (m_qtVulkanInstance) {
        m_qtVulkanInstance.reset();
    }

    m_vkInstance = VK_NULL_HANDLE;
    m_physicalDevice = VK_NULL_HANDLE;
    m_deviceFunctions = nullptr;
}

bool QtVulkanIntegration::createVulkanInstance()
{
    qCDebug(logVulkan) << "Creating Vulkan instance...";

    // Get available extensions
    uint32_t extensionCount = 0;
    vkEnumerateInstanceExtensionProperties(nullptr, &extensionCount, nullptr);
    std::vector<VkExtensionProperties> extensions(extensionCount);
    vkEnumerateInstanceExtensionProperties(nullptr, &extensionCount, extensions.data());

    qCDebug(logVulkan) << "Available Vulkan extensions:" << extensionCount;

    // Get required extensions from Qt
    QByteArrayList requiredExtensions = QVulkanInstance::supportedExtensions();
    std::vector<const char*> enabledExtensions;
    for (const QByteArray& ext : requiredExtensions) {
        enabledExtensions.push_back(ext.constData());
        qCDebug(logVulkan) << "Enabling extension:" << ext;
    }

    // Create Vulkan instance
    VkApplicationInfo appInfo{};
    appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    appInfo.pApplicationName = "OmniCpp Engine";
    appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
    appInfo.pEngineName = "OmniCpp Engine";
    appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
    appInfo.apiVersion = VK_API_VERSION_1_0;

    VkInstanceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    createInfo.pApplicationInfo = &appInfo;
    createInfo.enabledExtensionCount = static_cast<uint32_t>(enabledExtensions.size());
    createInfo.ppEnabledExtensionNames = enabledExtensions.data();

    if (vkCreateInstance(&createInfo, nullptr, &m_vkInstance) != VK_SUCCESS) {
        qCCritical(logVulkan) << "Failed to create Vulkan instance";
        return false;
    }

    // Initialize Qt Vulkan instance
    m_qtVulkanInstance->setVkInstance(m_vkInstance);
    if (!m_qtVulkanInstance->create()) {
        qCCritical(logVulkan) << "Failed to create Qt Vulkan instance";
        return false;
    }

    qCDebug(logVulkan) << "Vulkan instance created successfully";
    return true;
}

bool QtVulkanIntegration::selectPhysicalDevice()
{
    qCDebug(logVulkan) << "Selecting physical device...";

    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(m_vkInstance, &deviceCount, nullptr);

    if (deviceCount == 0) {
        qCCritical(logVulkan) << "No physical devices found";
        return false;
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(m_vkInstance, &deviceCount, devices.data());

    // Select the first suitable device
    for (const VkPhysicalDevice& device : devices) {
        VkPhysicalDeviceProperties deviceProperties;
        vkGetPhysicalDeviceProperties(device, &deviceProperties);

        qCDebug(logVulkan) << "Found device:" << deviceProperties.deviceName;

        // Check for graphics queue family
        uint32_t queueFamilyCount = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);
        std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
        vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());

        for (uint32_t i = 0; i < queueFamilyCount; ++i) {
            if (queueFamilies[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
                m_physicalDevice = device;
                m_graphicsQueueFamily = i;
                qCDebug(logVulkan) << "Selected physical device:" << deviceProperties.deviceName;
                return true;
            }
        }
    }

    qCCritical(logVulkan) << "No suitable physical device found";
    return false;
}

bool QtVulkanIntegration::createLogicalDevice()
{
    qCDebug(logVulkan) << "Creating logical device...";

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
        qCCritical(logVulkan) << "Failed to create logical device";
        return false;
    }

    // Get device functions
    m_deviceFunctions = m_qtVulkanInstance->deviceFunctions(m_device);
    if (!m_deviceFunctions) {
        qCCritical(logVulkan) << "Failed to get device functions";
        return false;
    }

    // Get graphics queue
    vkGetDeviceQueue(m_device, m_graphicsQueueFamily, 0, &m_graphicsQueue);

    qCDebug(logVulkan) << "Logical device created successfully";
    return true;
}

} // namespace OmniCpp
