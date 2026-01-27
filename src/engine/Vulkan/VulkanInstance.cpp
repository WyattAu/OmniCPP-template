#include "Vulkan/VulkanInstance.hpp"
#include <QLoggingCategory>
#include <set>
#include <algorithm>

Q_LOGGING_CATEGORY(logVulkanInstance, "omnicpp.vulkaninstance")

// MSVC-compatible attribute for unused parameters
#ifdef _MSC_VER
    #define MAYBE_UNUSED __declspec(unsued)
#else
    #define MAYBE_UNUSED [[maybe_unused]]
#endif

namespace OmniCpp {

VulkanInstance::VulkanInstance()
    : m_instance(VK_NULL_HANDLE)
    , m_debugMessenger(VK_NULL_HANDLE)
    , m_enableValidationLayers(false)
{
#ifdef _DEBUG
    m_enableValidationLayers = true;
#endif
}

VulkanInstance::~VulkanInstance()
{
    shutdown();
}

bool VulkanInstance::initialize(const std::string& appName, uint32_t appVersion)
{
    qCDebug(logVulkanInstance) << "Initializing Vulkan instance...";

    if (m_enableValidationLayers && !checkValidationLayerSupport()) {
        qCCritical(logVulkanInstance) << "Validation layers requested but not available";
        return false;
    }

    // Get required extensions
    m_enabledExtensions = getRequiredExtensions();

    // Create application info
    VkApplicationInfo appInfo{};
    appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    appInfo.pApplicationName = appName.c_str();
    appInfo.applicationVersion = appVersion;
    appInfo.pEngineName = "OmniCpp Engine";
    appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
    appInfo.apiVersion = VK_API_VERSION_1_0;

    // Create instance info
    VkInstanceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    createInfo.pApplicationInfo = &appInfo;

    // Enable validation layers
    if (m_enableValidationLayers) {
        const char* validationLayers[] = {"VK_LAYER_KHRONOS_validation"};
        createInfo.enabledLayerCount = 1;
        createInfo.ppEnabledLayerNames = validationLayers;
        createInfo.pNext = nullptr;
    }

    // Enable extensions
    createInfo.enabledExtensionCount = static_cast<uint32_t>(m_enabledExtensions.size());
    createInfo.ppEnabledExtensionNames = m_enabledExtensions.data();

    // Create instance
    if (vkCreateInstance(&createInfo, nullptr, &m_instance) != VK_SUCCESS) {
        qCCritical(logVulkanInstance) << "Failed to create Vulkan instance";
        return false;
    }

    // Setup debug messenger
    if (m_enableValidationLayers) {
        setupDebugMessenger();
    }

    qCDebug(logVulkanInstance) << "Vulkan instance initialized successfully";
    return true;
}

void VulkanInstance::shutdown()
{
    qCDebug(logVulkanInstance) << "Shutting down Vulkan instance...";

    if (m_debugMessenger != VK_NULL_HANDLE) {
        auto func = (PFN_vkDestroyDebugUtilsMessengerEXT)vkGetInstanceProcAddr(
            m_instance, "vkDestroyDebugUtilsMessengerEXT");
        if (func != nullptr) {
            func(m_instance, m_debugMessenger, nullptr);
        }
        m_debugMessenger = VK_NULL_HANDLE;
    }

    if (m_instance != VK_NULL_HANDLE) {
        vkDestroyInstance(m_instance, nullptr);
        m_instance = VK_NULL_HANDLE;
    }

    qCDebug(logVulkanInstance) << "Vulkan instance shut down";
}

bool VulkanInstance::checkValidationLayerSupport()
{
    uint32_t layerCount;
    vkEnumerateInstanceLayerProperties(&layerCount, nullptr);

    std::vector<VkLayerProperties> availableLayers(layerCount);
    vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());

    const char* validationLayers[] = {"VK_LAYER_KHRONOS_validation"};

    for (const char* layerName : validationLayers) {
        bool layerFound = false;
        for (const auto& layerProperties : availableLayers) {
            if (strcmp(layerName, layerProperties.layerName) == 0) {
                layerFound = true;
                break;
            }
        }

        if (!layerFound) {
            return false;
        }
    }

    return true;
}

std::vector<const char*> VulkanInstance::getRequiredExtensions()
{
    std::vector<const char*> extensions;

    // Get required extensions from Qt
    uint32_t glfwExtensionCount = 0;
    const char** glfwExtensions = nullptr;
    // glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

    for (uint32_t i = 0; i < glfwExtensionCount; i++) {
        extensions.push_back(glfwExtensions[i]);
    }

    // Add debug extension if validation layers are enabled
    if (m_enableValidationLayers) {
        extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    }

    return extensions;
}

void VulkanInstance::setupDebugMessenger()
{
    VkDebugUtilsMessengerCreateInfoEXT createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
    createInfo.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT |
                               VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
                               VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
    createInfo.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
                           VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
                           VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;
    createInfo.pfnUserCallback = [](VkDebugUtilsMessageSeverityFlagBitsEXT messageSeverity,
                                     [[maybe_unused]] VkDebugUtilsMessageTypeFlagsEXT messageType,
                                     const VkDebugUtilsMessengerCallbackDataEXT* pCallbackData,
                                     [[maybe_unused]] void* pUserData) -> VkBool32 {
        if (messageSeverity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT) {
            qWarning() << "Validation layer:" << pCallbackData->pMessage;
        }
        return VK_FALSE;
    };

    auto func = (PFN_vkCreateDebugUtilsMessengerEXT)vkGetInstanceProcAddr(
        m_instance, "vkCreateDebugUtilsMessengerEXT");

    if (func != nullptr) {
        func(m_instance, &createInfo, nullptr, &m_debugMessenger);
    }
}

} // namespace OmniCpp
