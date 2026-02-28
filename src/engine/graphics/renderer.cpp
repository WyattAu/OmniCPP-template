/**
 * @file renderer.cpp
 * @brief Graphics renderer implementation with Vulkan 3D rendering
 */

#include "engine/graphics/renderer.hpp"
#include "engine/graphics/shaders.hpp"
#include "engine/graphics/spirv_shaders.hpp"
#include "engine/graphics/mesh.hpp"
#include "engine/window/window_manager.hpp"
#include <mutex>
#include "engine/logging/Log.hpp"
#include <cstring>
#include <vector>
#include <array>
#include <optional>
#include <set>
#include <cstdlib>

#ifdef OMNICPP_HAS_VULKAN
#include <xcb/xcb.h>
#include <vulkan/vulkan.h>
#include <vulkan/vulkan_xcb.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#endif

#ifdef OMNICPP_HAS_QT_VULKAN
#include <QVulkanInstance>
#include <QWindow>
#include <QGuiApplication>
#endif

namespace OmniCpp::Engine::Graphics {

#ifdef OMNICPP_HAS_VULKAN

// Vertex structure for 3D rendering
struct Vertex {
    glm::vec3 pos;
    glm::vec3 color;
    glm::vec2 tex_coord;

    static VkVertexInputBindingDescription get_binding_description() {
        VkVertexInputBindingDescription binding_description{};
        binding_description.binding = 0;
        binding_description.stride = sizeof(Vertex);
        binding_description.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
        return binding_description;
    }

    static std::array<VkVertexInputAttributeDescription, 3> get_attribute_descriptions() {
        std::array<VkVertexInputAttributeDescription, 3> attribute_descriptions{};

        // Position attribute
        attribute_descriptions[0].binding = 0;
        attribute_descriptions[0].location = 0;
        attribute_descriptions[0].format = VK_FORMAT_R32G32B32_SFLOAT;
        attribute_descriptions[0].offset = offsetof(Vertex, pos);

        // Color attribute
        attribute_descriptions[1].binding = 0;
        attribute_descriptions[1].location = 1;
        attribute_descriptions[1].format = VK_FORMAT_R32G32B32_SFLOAT;
        attribute_descriptions[1].offset = offsetof(Vertex, color);

        // Texture coordinate attribute
        attribute_descriptions[2].binding = 0;
        attribute_descriptions[2].location = 2;
        attribute_descriptions[2].format = VK_FORMAT_R32G32_SFLOAT;
        attribute_descriptions[2].offset = offsetof(Vertex, tex_coord);

        return attribute_descriptions;
    }
};

// Uniform buffer object for transformation matrices
struct UniformBufferObject {
    alignas(16) glm::mat4 model;
    alignas(16) glm::mat4 view;
    alignas(16) glm::mat4 proj;
};

// Helper function to convert VkResult to string
static const char* vk_result_to_string(VkResult result) {
    switch (result) {
        case VK_SUCCESS: return "VK_SUCCESS";
        case VK_NOT_READY: return "VK_NOT_READY";
        case VK_TIMEOUT: return "VK_TIMEOUT";
        case VK_EVENT_SET: return "VK_EVENT_SET";
        case VK_EVENT_RESET: return "VK_EVENT_RESET";
        case VK_INCOMPLETE: return "VK_INCOMPLETE";
        case VK_ERROR_OUT_OF_HOST_MEMORY: return "VK_ERROR_OUT_OF_HOST_MEMORY";
        case VK_ERROR_OUT_OF_DEVICE_MEMORY: return "VK_ERROR_OUT_OF_DEVICE_MEMORY";
        case VK_ERROR_INITIALIZATION_FAILED: return "VK_ERROR_INITIALIZATION_FAILED";
        case VK_ERROR_DEVICE_LOST: return "VK_ERROR_DEVICE_LOST";
        case VK_ERROR_MEMORY_MAP_FAILED: return "VK_ERROR_MEMORY_MAP_FAILED";
        case VK_ERROR_LAYER_NOT_PRESENT: return "VK_ERROR_LAYER_NOT_PRESENT";
        case VK_ERROR_EXTENSION_NOT_PRESENT: return "VK_ERROR_EXTENSION_NOT_PRESENT";
        case VK_ERROR_FEATURE_NOT_PRESENT: return "VK_ERROR_FEATURE_NOT_PRESENT";
        case VK_ERROR_INCOMPATIBLE_DRIVER: return "VK_ERROR_INCOMPATIBLE_DRIVER";
        case VK_ERROR_TOO_MANY_OBJECTS: return "VK_ERROR_TOO_MANY_OBJECTS";
        case VK_ERROR_FORMAT_NOT_SUPPORTED: return "VK_ERROR_FORMAT_NOT_SUPPORTED";
        case VK_ERROR_FRAGMENTED_POOL: return "VK_ERROR_FRAGMENTED_POOL";
        case VK_ERROR_UNKNOWN: return "VK_ERROR_UNKNOWN";
        case VK_ERROR_OUT_OF_POOL_MEMORY: return "VK_ERROR_OUT_OF_POOL_MEMORY";
        case VK_ERROR_INVALID_EXTERNAL_HANDLE: return "VK_ERROR_INVALID_EXTERNAL_HANDLE";
        case VK_ERROR_SURFACE_LOST_KHR: return "VK_ERROR_SURFACE_LOST_KHR";
        case VK_ERROR_NATIVE_WINDOW_IN_USE_KHR: return "VK_ERROR_NATIVE_WINDOW_IN_USE_KHR";
        case VK_SUBOPTIMAL_KHR: return "VK_SUBOPTIMAL_KHR";
        case VK_ERROR_OUT_OF_DATE_KHR: return "VK_ERROR_OUT_OF_DATE_KHR";
        case VK_ERROR_INCOMPATIBLE_DISPLAY_KHR: return "VK_ERROR_INCOMPATIBLE_DISPLAY_KHR";
        case VK_ERROR_VALIDATION_FAILED_EXT: return "VK_ERROR_VALIDATION_FAILED_EXT";
        case VK_ERROR_INVALID_SHADER_NV: return "VK_ERROR_INVALID_SHADER_NV";
        default: return "UNKNOWN_VK_RESULT";
    }
}

// Get highest supported Vulkan API version
static uint32_t get_highest_vulkan_api_version() {
    uint32_t api_version = 0;
    VkResult result = vkEnumerateInstanceVersion(&api_version);
    if (result != VK_SUCCESS) {
        omnicpp::log::warn("Failed to enumerate Vulkan instance version: {} ({}), using VK_API_VERSION_1_0",
                     vk_result_to_string(result), static_cast<int>(result));
        return VK_API_VERSION_1_0;
    }

    uint32_t major = VK_VERSION_MAJOR(api_version);
    uint32_t minor = VK_VERSION_MINOR(api_version);
    uint32_t patch = VK_VERSION_PATCH(api_version);

    omnicpp::log::info("Highest supported Vulkan API version: {}.{}.{}", major, minor, patch);

    // Use exact version reported by driver for maximum compatibility
    // Vulkan drivers are backward compatible, so requesting exact version
    // ensures we get all available features without compatibility issues
    return api_version;
}

// Debug callback for Vulkan validation layers
static VKAPI_ATTR VkBool32 VKAPI_CALL debug_callback(
    VkDebugUtilsMessageSeverityFlagBitsEXT message_severity,
    VkDebugUtilsMessageTypeFlagsEXT message_type,
    const VkDebugUtilsMessengerCallbackDataEXT* callback_data,
    void* user_data) {

    // Suppress false positives from validation layers
    if (strcmp(callback_data->pMessageIdName, "VUID-vkCmdDrawIndexed-None-02721") == 0) {
        return VK_FALSE;
    }

    omnicpp::log::debug("[Vulkan Validation] {}: {}",
        callback_data->pMessageIdName ? callback_data->pMessageIdName : "Unknown",
        callback_data->pMessage ? callback_data->pMessage : "No message");

    return VK_FALSE;
}

// Populate debug messenger create info
static VkResult create_debug_utils_messenger_ext(
    VkInstance instance,
    const VkDebugUtilsMessengerCreateInfoEXT* pCreateInfo,
    const VkAllocationCallbacks* pAllocator,
    VkDebugUtilsMessengerEXT* pDebugMessenger) {

    auto func = (PFN_vkCreateDebugUtilsMessengerEXT)vkGetInstanceProcAddr(
        instance, "vkCreateDebugUtilsMessengerEXT");
    if (func != nullptr) {
        return func(instance, pCreateInfo, pAllocator, pDebugMessenger);
    }
    return VK_ERROR_EXTENSION_NOT_PRESENT;
}

// Destroy debug messenger
static void destroy_debug_utils_messenger_ext(
    VkInstance instance,
    VkDebugUtilsMessengerEXT debugMessenger,
    const VkAllocationCallbacks* pAllocator) {

    auto func = (PFN_vkDestroyDebugUtilsMessengerEXT)vkGetInstanceProcAddr(
        instance, "vkDestroyDebugUtilsMessengerEXT");
    if (func != nullptr) {
        func(instance, debugMessenger, pAllocator);
    }
}

// Check if validation layers are available
static bool check_validation_layer_support() {
    uint32_t layer_count;
    VkResult result = vkEnumerateInstanceLayerProperties(&layer_count, nullptr);
    if (result != VK_SUCCESS) {
        omnicpp::log::error("Failed to enumerate Vulkan instance layers: {} ({})",
                      vk_result_to_string(result), static_cast<int>(result));
        return false;
    }

    omnicpp::log::info("Found {} Vulkan instance layers", layer_count);

    std::vector<VkLayerProperties> available_layers(layer_count);
    result = vkEnumerateInstanceLayerProperties(&layer_count, available_layers.data());
    if (result != VK_SUCCESS) {
        omnicpp::log::error("Failed to get Vulkan instance layer properties: {} ({})",
                      vk_result_to_string(result), static_cast<int>(result));
        return false;
    }

    // Log all available layers for debugging
    omnicpp::log::info("Available Vulkan instance layers:");
    for (const auto& layer_properties : available_layers) {
        omnicpp::log::info("  - {} (spec version: {}, impl version: {})",
                     layer_properties.layerName,
                     VK_VERSION_MAJOR(layer_properties.specVersion),
                     VK_VERSION_MINOR(layer_properties.specVersion));
    }

    const char* validation_layer = "VK_LAYER_KHRONOS_validation";
    for (const auto& layer_properties : available_layers) {
        if (strcmp(validation_layer, layer_properties.layerName) == 0) {
            omnicpp::log::info("Validation layer '{}' is available", validation_layer);
            return true;
        }
    }

    omnicpp::log::warn("Validation layer '{}' is NOT available", validation_layer);
    return false;
}

// Get required extensions
static std::vector<const char*> get_required_extensions(bool enable_validation_layers) {
    std::vector<const char*> extensions;

    // Add platform-specific extensions
#ifdef OMNICPP_HAS_QT_VULKAN
    // Query Qt6 for required Vulkan instance extensions
    extensions.push_back(VK_KHR_SURFACE_EXTENSION_NAME);
#ifdef VK_USE_PLATFORM_WAYLAND_KHR
    extensions.push_back(VK_KHR_WAYLAND_SURFACE_EXTENSION_NAME);
#endif
#ifdef VK_USE_PLATFORM_XCB_KHR
    extensions.push_back(VK_KHR_XCB_SURFACE_EXTENSION_NAME);
#endif
#endif

    // Add debug extension if validation layers are enabled
    if (enable_validation_layers) {
        extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    }

    return extensions;
}

// Rate physical device suitability
static uint32_t rate_device_suitability(VkPhysicalDevice device) {
    uint32_t score = 0;

    VkPhysicalDeviceProperties device_properties;
    vkGetPhysicalDeviceProperties(device, &device_properties);

    // Discrete GPUs have a significant performance advantage
    if (device_properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) {
        score += 1000;
    }

    // Maximum possible size of textures affects graphics quality
    score += device_properties.limits.maxImageDimension2D;

    return score;
}

// Check if device supports required extensions
static bool check_device_extension_support(VkPhysicalDevice device) {
    uint32_t extension_count;
    vkEnumerateDeviceExtensionProperties(device, nullptr, &extension_count, nullptr);

    std::vector<VkExtensionProperties> available_extensions(extension_count);
    vkEnumerateDeviceExtensionProperties(device, nullptr, &extension_count, available_extensions.data());

    std::set<std::string> required_extensions = {
        VK_KHR_SWAPCHAIN_EXTENSION_NAME
    };

    for (const auto& extension : available_extensions) {
        required_extensions.erase(extension.extensionName);
    }

    return required_extensions.empty();
}

// Find queue families
struct QueueFamilyIndices {
    std::optional<uint32_t> graphics_family;
    std::optional<uint32_t> present_family;

    bool is_complete() const {
        return graphics_family.has_value() && present_family.has_value();
    }
};

static QueueFamilyIndices find_queue_families(VkPhysicalDevice device, VkSurfaceKHR surface) {
    QueueFamilyIndices indices;

    uint32_t queue_family_count = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queue_family_count, nullptr);

    std::vector<VkQueueFamilyProperties> queue_families(queue_family_count);
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queue_family_count, queue_families.data());

    omnicpp::log::info("Checking {} queue families for surface support...", queue_family_count);

    // First check surface capabilities to verify surface is valid
    omnicpp::log::info("Checking surface capabilities...");
    VkSurfaceCapabilitiesKHR surface_caps;
    VkResult caps_result = vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, surface, &surface_caps);
    
    if (caps_result != VK_SUCCESS) {
        omnicpp::log::error("Failed to get surface capabilities: {}", 
                        vk_result_to_string(caps_result));
        return indices;
    }
    
    omnicpp::log::info("Surface capabilities: minImageCount={}, maxImageCount={}, currentExtent={}x{}",
                 surface_caps.minImageCount, surface_caps.maxImageCount,
                 surface_caps.currentExtent.width, surface_caps.currentExtent.height);

    int i = 0;
    for (const auto& queue_family : queue_families) {
        // Check for graphics support
        if (queue_family.queueFlags & VK_QUEUE_GRAPHICS_BIT) {
            indices.graphics_family = i;
            omnicpp::log::info("  Queue family {}: has graphics support", i);
        }

        // Check for present support
        VkBool32 present_support = false;
        VkResult result = vkGetPhysicalDeviceSurfaceSupportKHR(device, i, surface, &present_support);
        omnicpp::log::info("  Queue family {}: present support check result = {}, present = {}", 
                     i, vk_result_to_string(result), present_support);

        if (result == VK_SUCCESS && present_support) {
            indices.present_family = i;
            omnicpp::log::info("  Queue family {}: has present support!", i);
        }

        if (indices.is_complete()) {
            break;
        }

        i++;
    }

    if (!indices.is_complete()) {
        omnicpp::log::error("Queue family check incomplete: graphics={}, present={}",
                      indices.graphics_family.has_value() ? std::to_string(indices.graphics_family.value()) : "none",
                      indices.present_family.has_value() ? std::to_string(indices.present_family.value()) : "none");
    }

    return indices;
}

// Swap chain support details
struct SwapChainSupportDetails {
    VkSurfaceCapabilitiesKHR capabilities;
    std::vector<VkSurfaceFormatKHR> formats;
    std::vector<VkPresentModeKHR> present_modes;
};

static SwapChainSupportDetails query_swap_chain_support(VkPhysicalDevice device, VkSurfaceKHR surface) {
    SwapChainSupportDetails details;

    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, surface, &details.capabilities);

    uint32_t format_count;
    vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &format_count, nullptr);

    if (format_count != 0) {
        details.formats.resize(format_count);
        vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &format_count, details.formats.data());
    }

    uint32_t present_mode_count;
    vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &present_mode_count, nullptr);

    if (present_mode_count != 0) {
        details.present_modes.resize(present_mode_count);
        vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &present_mode_count, details.present_modes.data());
    }

    return details;
}

// Choose swap surface format
static VkSurfaceFormatKHR choose_swap_surface_format(const std::vector<VkSurfaceFormatKHR>& available_formats) {
    for (const auto& available_format : available_formats) {
        if (available_format.format == VK_FORMAT_B8G8R8A8_SRGB &&
            available_format.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) {
            return available_format;
        }
    }
    return available_formats[0];
}

// Choose swap present mode
static VkPresentModeKHR choose_swap_present_mode(const std::vector<VkPresentModeKHR>& available_present_modes) {
    for (const auto& available_present_mode : available_present_modes) {
        if (available_present_mode == VK_PRESENT_MODE_MAILBOX_KHR) {
            return available_present_mode;
        }
    }
    return VK_PRESENT_MODE_FIFO_KHR;
}

// Choose swap extent
static VkExtent2D choose_swap_extent(const VkSurfaceCapabilitiesKHR& capabilities, uint32_t width, uint32_t height) {
    if (capabilities.currentExtent.width != UINT32_MAX) {
        return capabilities.currentExtent;
    }

    VkExtent2D actual_extent = {
        std::clamp(width, capabilities.minImageExtent.width, capabilities.maxImageExtent.width),
        std::clamp(height, capabilities.minImageExtent.height, capabilities.maxImageExtent.height)
    };

    return actual_extent;
}

// Read shader file
static std::vector<char> read_shader_file(const std::string& filename) {
    // For embedded shaders, return compiled SPIR-V
    // This is a placeholder - actual shader loading would read from files
    omnicpp::log::warn("Shader file loading not implemented: {}", filename);
    return {};
}

// Create shader module
static VkShaderModule create_shader_module(VkDevice device, const std::vector<char>& code) {
    VkShaderModuleCreateInfo create_info{};
    create_info.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    create_info.codeSize = code.size();
    create_info.pCode = reinterpret_cast<const uint32_t*>(code.data());

    VkShaderModule shader_module;
    if (vkCreateShaderModule(device, &create_info, nullptr, &shader_module) != VK_SUCCESS) {
        omnicpp::log::error("Failed to create shader module");
        return VK_NULL_HANDLE;
    }

    return shader_module;
}

#endif // OMNICPP_HAS_VULKAN

/**
 * @brief Private implementation structure (Pimpl idiom)
 */
struct Renderer::Impl {
    RendererConfig config;
    Window::WindowManager* window_manager{ nullptr };
    uint32_t frame_count{ 0 };
    std::mutex mutex;
    bool initialized{ false };
    static constexpr uint32_t MAX_FRAMES_IN_FLIGHT = 2;

#ifdef OMNICPP_HAS_VULKAN
    // Vulkan instance
    VkInstance instance{ VK_NULL_HANDLE };
    VkDebugUtilsMessengerEXT debug_messenger{ VK_NULL_HANDLE };

    // Vulkan surface
    VkSurfaceKHR surface{ VK_NULL_HANDLE };

    // Physical device and logical device
    VkPhysicalDevice physical_device{ VK_NULL_HANDLE };
    VkDevice device{ VK_NULL_HANDLE };

    // Queue handles
    VkQueue graphics_queue{ VK_NULL_HANDLE };
    VkQueue present_queue{ VK_NULL_HANDLE };

    // Swap chain
    VkSwapchainKHR swap_chain{ VK_NULL_HANDLE };
    std::vector<VkImage> swap_chain_images;
    VkFormat swap_chain_image_format;
    VkExtent2D swap_chain_extent;
    std::vector<VkImageView> swap_chain_image_views;

    // Render pass
    VkRenderPass render_pass{ VK_NULL_HANDLE };

    // Pipeline layout
    VkPipelineLayout pipeline_layout{ VK_NULL_HANDLE };

    // Graphics pipeline
    VkPipeline graphics_pipeline{ VK_NULL_HANDLE };

    // Framebuffers
    std::vector<VkFramebuffer> swap_chain_framebuffers;

    // Command pool
    VkCommandPool command_pool{ VK_NULL_HANDLE };

    // Command buffers
    std::vector<VkCommandBuffer> command_buffers;

    // Synchronization primitives
    std::vector<VkSemaphore> image_available_semaphores;
    std::vector<VkSemaphore> render_finished_semaphores;
    std::vector<VkFence> in_flight_fences;
    std::vector<VkFence> images_in_flight;

    uint32_t current_frame{ 0 };

    // Vertex buffer
    VkBuffer vertex_buffer{ VK_NULL_HANDLE };
    VkDeviceMemory vertex_buffer_memory{ VK_NULL_HANDLE };

    // Index buffer
    VkBuffer index_buffer{ VK_NULL_HANDLE };
    VkDeviceMemory index_buffer_memory{ VK_NULL_HANDLE };

    // Uniform buffers
    std::vector<VkBuffer> uniform_buffers;
    std::vector<VkDeviceMemory> uniform_buffers_memory;
    std::vector<void*> uniform_buffers_mapped;

    // Descriptor pool
    VkDescriptorPool descriptor_pool{ VK_NULL_HANDLE };

    // Descriptor sets
    std::vector<VkDescriptorSet> descriptor_sets;
    VkDescriptorSetLayout descriptor_set_layout{ VK_NULL_HANDLE };
    
    // Game object rendering info
    uint32_t field_first_index{0};
    uint32_t field_index_count{0};
    uint32_t left_paddle_first_index{0};
    uint32_t left_paddle_index_count{0};
    uint32_t right_paddle_first_index{0};
    uint32_t right_paddle_index_count{0};
    uint32_t ball_first_index{0};
    uint32_t ball_index_count{0};
    
    // Game state for rendering
    float ball_x{10.0f}, ball_y{5.0f};
    float left_paddle_y{5.0f}, right_paddle_y{5.0f};
#endif
};

Renderer::Renderer () : m_impl (std::make_unique<Impl> ()) {
}

Renderer::~Renderer () {
  shutdown ();
}

Renderer::Renderer (Renderer&& other) noexcept : m_impl (std::move (other.m_impl)) {
}

Renderer& Renderer::operator= (Renderer&& other) noexcept {
  if (this != &other) {
    m_impl = std::move (other.m_impl);
  }
  return *this;
}

bool Renderer::initialize (const RendererConfig& config) {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (m_impl->initialized) {
    omnicpp::log::warn("Renderer: Already initialized");
    return true;
  }

  m_impl->config = config;

#ifdef OMNICPP_HAS_VULKAN
  omnicpp::log::info("Initializing Vulkan renderer...");

  // Check for validation layer support with environment variable override
  bool enable_validation_layers = config.enable_debug;

  // Check for environment variable to force-disable validation layers
  const char* disable_validation_env = std::getenv("OMNICPP_DISABLE_VULKAN_VALIDATION");
  if (disable_validation_env && (std::strcmp(disable_validation_env, "1") == 0 ||
                                 std::strcmp(disable_validation_env, "true") == 0 ||
                                 std::strcmp(disable_validation_env, "TRUE") == 0)) {
    omnicpp::log::info("Validation layers disabled via OMNICPP_DISABLE_VULKAN_VALIDATION environment variable");
    enable_validation_layers = false;
  }

  // Check for validation layer availability
  if (enable_validation_layers) {
    bool layers_available = check_validation_layer_support();
    if (!layers_available) {
      omnicpp::log::warn("Validation layers requested, but not available!");
      omnicpp::log::warn("Disabling validation layers and continuing without them");
      omnicpp::log::warn("To install validation layers, install the Vulkan SDK from https://vulkan.lunarg.com/");
      omnicpp::log::info("Alternatively, set OMNICPP_DISABLE_VULKAN_VALIDATION=1 to suppress this warning");
      enable_validation_layers = false;
    } else {
      omnicpp::log::info("Validation layers enabled");
    }
  } else {
    omnicpp::log::info("Validation layers disabled");
  }

  // Get required extensions
  VkResult result = VK_SUCCESS;
  
  // Check if we have Qt Vulkan window from window manager
  bool use_qt_vulkan = false;
#ifdef OMNICPP_HAS_QT_VULKAN
  if (m_impl->window_manager) {
    QVulkanInstance* qt_vulkan = m_impl->window_manager->get_qt_vulkan_instance();
    QWindow* qt_window = m_impl->window_manager->get_qt_window();
    
    if (qt_vulkan && qt_window) {
      // Use Qt's Vulkan instance
      m_impl->instance = qt_vulkan->vkInstance();
      omnicpp::log::info("Using Qt Vulkan instance");
      
      // Try Qt's surfaceForWindow first
      m_impl->surface = qt_vulkan->surfaceForWindow(qt_window);
      
      if (m_impl->surface != VK_NULL_HANDLE) {
        omnicpp::log::info("Vulkan surface created from Qt window");
        use_qt_vulkan = true;
      } else {
        // Qt's surfaceForWindow failed - window may not be fully exposed yet
        // Try a few times with event processing
        omnicpp::log::warn("Qt surfaceForWindow failed, retrying with event processing...");
        
        for (int retry = 0; retry < 10; ++retry) {
          // Process events to allow window to be exposed
          QCoreApplication::processEvents();
          
          m_impl->surface = qt_vulkan->surfaceForWindow(qt_window);
          if (m_impl->surface != VK_NULL_HANDLE) {
            omnicpp::log::info("Vulkan surface created from Qt window after {} retries", retry + 1);
            use_qt_vulkan = true;
            break;
          }
          
          // Small delay
          std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
        
        if (m_impl->surface == VK_NULL_HANDLE) {
          omnicpp::log::error("Failed to create Vulkan surface after retries");
          return false;
        }
      }
    }
  }
#endif

  // If not using Qt Vulkan, create our own instance
  if (!use_qt_vulkan) {
    std::vector<const char*> extensions = get_required_extensions(enable_validation_layers);

    // Log extensions
    omnicpp::log::info("Required Vulkan extensions:");
    for (const auto& ext : extensions) {
      omnicpp::log::info("  - {}", ext);
    }

    // Create Vulkan instance
    VkApplicationInfo app_info{};
    app_info.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app_info.pApplicationName = "OmniCpp Pong";
    app_info.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
    app_info.pEngineName = "OmniCpp Engine";
    app_info.engineVersion = VK_MAKE_VERSION(1, 0, 0);
    app_info.apiVersion = get_highest_vulkan_api_version();

    VkInstanceCreateInfo create_info{};
    create_info.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    create_info.pApplicationInfo = &app_info;
    create_info.enabledExtensionCount = static_cast<uint32_t>(extensions.size());
    create_info.ppEnabledExtensionNames = extensions.data();

    // Validation layers
    VkDebugUtilsMessengerCreateInfoEXT debug_create_info{};
    if (enable_validation_layers) {
      const char* validation_layers[] = { "VK_LAYER_KHRONOS_validation" };
      create_info.enabledLayerCount = 1;
      create_info.ppEnabledLayerNames = validation_layers;

      // Setup debug messenger
      debug_create_info.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
      debug_create_info.messageSeverity =
          VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT |
          VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
          VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
      debug_create_info.messageType =
          VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
          VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
          VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;
      debug_create_info.pfnUserCallback = debug_callback;
      create_info.pNext = (VkDebugUtilsMessengerCreateInfoEXT*)&debug_create_info;
    }

    VkResult result = vkCreateInstance(&create_info, nullptr, &m_impl->instance);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create Vulkan instance: {} ({})",
                    vk_result_to_string(result), static_cast<int>(result));
      
      // Provide helpful error messages for common issues
      if (result == VK_ERROR_INCOMPATIBLE_DRIVER) {
        omnicpp::log::error("No compatible Vulkan driver found!");
        omnicpp::log::error("This may be because:");
        omnicpp::log::error("  1. No GPU is available in the system");
        omnicpp::log::error("  2. GPU drivers are not installed");
        omnicpp::log::error("  3. Running in a container without GPU access");
        omnicpp::log::error("  4. Vulkan ICD configuration is missing");
        omnicpp::log::error("The game will continue in headless mode without graphics.");
      }
      return false;
    }

    // Create Vulkan surface from window
    if (m_impl->window_manager) {
#ifdef OMNICPP_HAS_QT_VULKAN
      QWindow* qt_window = m_impl->window_manager->get_qt_window();
      if (qt_window) {
        m_impl->surface = QVulkanInstance::surfaceForWindow(qt_window);
        if (m_impl->surface == VK_NULL_HANDLE) {
          omnicpp::log::error("Failed to create Vulkan surface from Qt window");
          return false;
        }
        omnicpp::log::info("Vulkan surface created from Qt window");
      } else {
        omnicpp::log::error("Qt window is null, cannot create Vulkan surface");
        return false;
      }
#else
      omnicpp::log::error("Qt6 not available, cannot create Vulkan surface");
      return false;
#endif
    } else {
      omnicpp::log::warn("Window manager not set, skipping surface creation");
    }
  }

  // Pick physical device
  uint32_t device_count = 0;
  vkEnumeratePhysicalDevices(m_impl->instance, &device_count, nullptr);

  if (device_count == 0) {
    omnicpp::log::error("Failed to find GPUs with Vulkan support");
    return false;
  }

  std::vector<VkPhysicalDevice> devices(device_count);
  vkEnumeratePhysicalDevices(m_impl->instance, &device_count, devices.data());

  // Use the first available device
  m_impl->physical_device = devices[0];
  for (const auto& device : devices) {
    uint32_t score = rate_device_suitability(device);
    if (score > rate_device_suitability(m_impl->physical_device)) {
      m_impl->physical_device = device;
    }
  }

  VkPhysicalDeviceProperties device_properties;
  vkGetPhysicalDeviceProperties(m_impl->physical_device, &device_properties);
  omnicpp::log::info("Selected physical device: {}", device_properties.deviceName);

  // Find queue families
  QueueFamilyIndices indices = find_queue_families(m_impl->physical_device, m_impl->surface);
  if (!indices.is_complete()) {
    omnicpp::log::error("Failed to find suitable queue families");
    return false;
  }

  // Create logical device
  std::vector<VkDeviceQueueCreateInfo> queue_create_infos;
  std::set<uint32_t> unique_queue_families = {
    indices.graphics_family.value(),
    indices.present_family.value()
  };

  float queue_priority = 1.0f;
  for (uint32_t queue_family : unique_queue_families) {
    VkDeviceQueueCreateInfo queue_create_info{};
    queue_create_info.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    queue_create_info.queueFamilyIndex = queue_family;
    queue_create_info.queueCount = 1;
    queue_create_info.pQueuePriorities = &queue_priority;
    queue_create_infos.push_back(queue_create_info);
  }

  VkPhysicalDeviceFeatures device_features{};
  device_features.samplerAnisotropy = VK_TRUE;

  const char* device_extensions[] = {
    VK_KHR_SWAPCHAIN_EXTENSION_NAME
  };

  VkDeviceCreateInfo device_create_info{};
  device_create_info.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
  device_create_info.queueCreateInfoCount = static_cast<uint32_t>(queue_create_infos.size());
  device_create_info.pQueueCreateInfos = queue_create_infos.data();
  device_create_info.pEnabledFeatures = &device_features;
  device_create_info.enabledExtensionCount = 1;
  device_create_info.ppEnabledExtensionNames = device_extensions;

  result = vkCreateDevice(m_impl->physical_device, &device_create_info, nullptr, &m_impl->device);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create logical device: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Logical device created successfully");

  // Get queue handles
  vkGetDeviceQueue(m_impl->device, indices.graphics_family.value(), 0, &m_impl->graphics_queue);
  vkGetDeviceQueue(m_impl->device, indices.present_family.value(), 0, &m_impl->present_queue);

  omnicpp::log::info("Graphics and present queues obtained");

  // Create swap chain
  SwapChainSupportDetails swap_chain_support = query_swap_chain_support(m_impl->physical_device, m_impl->surface);

  VkSurfaceFormatKHR surface_format = choose_swap_surface_format(swap_chain_support.formats);
  VkPresentModeKHR present_mode = choose_swap_present_mode(swap_chain_support.present_modes);
  VkExtent2D extent = choose_swap_extent(swap_chain_support.capabilities,
                                        m_impl->window_manager ? m_impl->window_manager->get_width() : 800,
                                        m_impl->window_manager ? m_impl->window_manager->get_height() : 600);

  uint32_t image_count = swap_chain_support.capabilities.minImageCount + 1;
  if (swap_chain_support.capabilities.maxImageCount > 0 && image_count > swap_chain_support.capabilities.maxImageCount) {
    image_count = swap_chain_support.capabilities.maxImageCount;
  }

  VkSwapchainCreateInfoKHR swap_chain_create_info{};
  swap_chain_create_info.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
  swap_chain_create_info.surface = m_impl->surface;
  swap_chain_create_info.minImageCount = image_count;
  swap_chain_create_info.imageFormat = surface_format.format;
  swap_chain_create_info.imageColorSpace = surface_format.colorSpace;
  swap_chain_create_info.imageExtent = extent;
  swap_chain_create_info.imageArrayLayers = 1;
  swap_chain_create_info.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
  swap_chain_create_info.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
  swap_chain_create_info.preTransform = swap_chain_support.capabilities.currentTransform;
  swap_chain_create_info.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
  swap_chain_create_info.presentMode = present_mode;
  swap_chain_create_info.clipped = VK_TRUE;
  swap_chain_create_info.oldSwapchain = VK_NULL_HANDLE;

  result = vkCreateSwapchainKHR(m_impl->device, &swap_chain_create_info, nullptr, &m_impl->swap_chain);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create swap chain: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Swap chain created successfully");

  m_impl->swap_chain_image_format = surface_format.format;
  m_impl->swap_chain_extent = extent;

  // Get swap chain images
  vkGetSwapchainImagesKHR(m_impl->device, m_impl->swap_chain, &image_count, nullptr);
  m_impl->swap_chain_images.resize(image_count);
  vkGetSwapchainImagesKHR(m_impl->device, m_impl->swap_chain, &image_count, m_impl->swap_chain_images.data());

  omnicpp::log::info("Swap chain has {} images", image_count);

  // Create image views
  m_impl->swap_chain_image_views.resize(image_count);
  for (size_t i = 0; i < image_count; i++) {
    VkImageViewCreateInfo create_info{};
    create_info.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
    create_info.image = m_impl->swap_chain_images[i];
    create_info.viewType = VK_IMAGE_VIEW_TYPE_2D;
    create_info.format = m_impl->swap_chain_image_format;
    create_info.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
    create_info.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
    create_info.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
    create_info.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;
    create_info.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    create_info.subresourceRange.baseMipLevel = 0;
    create_info.subresourceRange.levelCount = 1;
    create_info.subresourceRange.baseArrayLayer = 0;
    create_info.subresourceRange.layerCount = 1;

    result = vkCreateImageView(m_impl->device, &create_info, nullptr, &m_impl->swap_chain_image_views[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create image view {} ({})", i, static_cast<int>(result));
      return false;
    }
  }

  omnicpp::log::info("Image views created successfully");

  // Create render pass
  VkAttachmentDescription color_attachment{};
  color_attachment.format = m_impl->swap_chain_image_format;
  color_attachment.samples = VK_SAMPLE_COUNT_1_BIT;
  color_attachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
  color_attachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
  color_attachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
  color_attachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
  color_attachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
  color_attachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;

  VkAttachmentReference color_attachment_ref{};
  color_attachment_ref.attachment = 0;
  color_attachment_ref.layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;

  VkSubpassDescription subpass{};
  subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
  subpass.colorAttachmentCount = 1;
  subpass.pColorAttachments = &color_attachment_ref;

  VkSubpassDependency dependency{};
  dependency.srcSubpass = VK_SUBPASS_EXTERNAL;
  dependency.dstSubpass = 0;
  dependency.srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
  dependency.srcAccessMask = 0;
  dependency.dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
  dependency.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;

  VkRenderPassCreateInfo render_pass_info{};
  render_pass_info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
  render_pass_info.attachmentCount = 1;
  render_pass_info.pAttachments = &color_attachment;
  render_pass_info.subpassCount = 1;
  render_pass_info.pSubpasses = &subpass;
  render_pass_info.dependencyCount = 1;
  render_pass_info.pDependencies = &dependency;

  result = vkCreateRenderPass(m_impl->device, &render_pass_info, nullptr, &m_impl->render_pass);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create render pass: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Render pass created successfully");

  // Create descriptor set layout
  VkDescriptorSetLayoutBinding ubo_layout_binding{};
  ubo_layout_binding.binding = 0;
  ubo_layout_binding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
  ubo_layout_binding.descriptorCount = 1;
  ubo_layout_binding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
  ubo_layout_binding.pImmutableSamplers = nullptr;

  VkDescriptorSetLayoutCreateInfo layout_info{};
  layout_info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
  layout_info.bindingCount = 1;
  layout_info.pBindings = &ubo_layout_binding;

  result = vkCreateDescriptorSetLayout(m_impl->device, &layout_info, nullptr, &m_impl->descriptor_set_layout);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create descriptor set layout: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Descriptor set layout created successfully");

  // Create pipeline layout
  VkPipelineLayoutCreateInfo pipeline_layout_info{};
  pipeline_layout_info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
  pipeline_layout_info.setLayoutCount = 1;
  pipeline_layout_info.pSetLayouts = &m_impl->descriptor_set_layout;

  result = vkCreatePipelineLayout(m_impl->device, &pipeline_layout_info, nullptr, &m_impl->pipeline_layout);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create pipeline layout: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Pipeline layout created successfully");

  // === Create Graphics Pipeline with Shaders ===
  omnicpp::log::info("Creating graphics pipeline with SPIR-V shaders...");
  
  // Load shader modules from embedded SPIR-V
  auto vertex_shader_code = get_vertex_shader_spirv();
  auto fragment_shader_code = get_fragment_shader_spirv();
  
  VkShaderModule vertex_shader_module = create_shader_module(m_impl->device, vertex_shader_code);
  if (vertex_shader_module == VK_NULL_HANDLE) {
    omnicpp::log::error("Failed to create vertex shader module");
    return false;
  }
  
  VkShaderModule fragment_shader_module = create_shader_module(m_impl->device, fragment_shader_code);
  if (fragment_shader_module == VK_NULL_HANDLE) {
    omnicpp::log::error("Failed to create fragment shader module");
    vkDestroyShaderModule(m_impl->device, vertex_shader_module, nullptr);
    return false;
  }
  
  omnicpp::log::info("Shader modules created successfully");
  
  // Shader stage create info
  VkPipelineShaderStageCreateInfo vert_shader_stage_info{};
  vert_shader_stage_info.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
  vert_shader_stage_info.stage = VK_SHADER_STAGE_VERTEX_BIT;
  vert_shader_stage_info.module = vertex_shader_module;
  vert_shader_stage_info.pName = "main";
  
  VkPipelineShaderStageCreateInfo frag_shader_stage_info{};
  frag_shader_stage_info.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
  frag_shader_stage_info.stage = VK_SHADER_STAGE_FRAGMENT_BIT;
  frag_shader_stage_info.module = fragment_shader_module;
  frag_shader_stage_info.pName = "main";
  
  VkPipelineShaderStageCreateInfo shader_stages[] = {vert_shader_stage_info, frag_shader_stage_info};
  
  // Vertex input state
  auto binding_description = Vertex::get_binding_description();
  auto attribute_descriptions = Vertex::get_attribute_descriptions();
  
  VkPipelineVertexInputStateCreateInfo vertex_input_info{};
  vertex_input_info.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;
  vertex_input_info.vertexBindingDescriptionCount = 1;
  vertex_input_info.pVertexBindingDescriptions = &binding_description;
  vertex_input_info.vertexAttributeDescriptionCount = static_cast<uint32_t>(attribute_descriptions.size());
  vertex_input_info.pVertexAttributeDescriptions = attribute_descriptions.data();
  
  // Input assembly state
  VkPipelineInputAssemblyStateCreateInfo input_assembly{};
  input_assembly.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
  input_assembly.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
  input_assembly.primitiveRestartEnable = VK_FALSE;
  
  // Viewport state
  VkPipelineViewportStateCreateInfo viewport_state{};
  viewport_state.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
  viewport_state.viewportCount = 1;
  viewport_state.scissorCount = 1;
  
  // Rasterizer
  VkPipelineRasterizationStateCreateInfo rasterizer{};
  rasterizer.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
  rasterizer.depthClampEnable = VK_FALSE;
  rasterizer.rasterizerDiscardEnable = VK_FALSE;
  rasterizer.polygonMode = VK_POLYGON_MODE_FILL;
  rasterizer.lineWidth = 1.0f;
  rasterizer.cullMode = VK_CULL_MODE_BACK_BIT;
  rasterizer.frontFace = VK_FRONT_FACE_CLOCKWISE;
  rasterizer.depthBiasEnable = VK_FALSE;
  
  // Multisampling
  VkPipelineMultisampleStateCreateInfo multisampling{};
  multisampling.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
  multisampling.sampleShadingEnable = VK_FALSE;
  multisampling.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
  
  // Color blending
  VkPipelineColorBlendAttachmentState color_blend_attachment{};
  color_blend_attachment.colorWriteMask = VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT | 
                                          VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
  color_blend_attachment.blendEnable = VK_FALSE;
  
  VkPipelineColorBlendStateCreateInfo color_blending{};
  color_blending.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
  color_blending.logicOpEnable = VK_FALSE;
  color_blending.attachmentCount = 1;
  color_blending.pAttachments = &color_blend_attachment;
  
  // Dynamic state
  VkDynamicState dynamic_states[] = {VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR};
  VkPipelineDynamicStateCreateInfo dynamic_state{};
  dynamic_state.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
  dynamic_state.dynamicStateCount = 2;
  dynamic_state.pDynamicStates = dynamic_states;
  
  // Create graphics pipeline
  VkGraphicsPipelineCreateInfo pipeline_info{};
  pipeline_info.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
  pipeline_info.stageCount = 2;
  pipeline_info.pStages = shader_stages;
  pipeline_info.pVertexInputState = &vertex_input_info;
  pipeline_info.pInputAssemblyState = &input_assembly;
  pipeline_info.pViewportState = &viewport_state;
  pipeline_info.pRasterizationState = &rasterizer;
  pipeline_info.pMultisampleState = &multisampling;
  pipeline_info.pColorBlendState = &color_blending;
  pipeline_info.pDynamicState = &dynamic_state;
  pipeline_info.layout = m_impl->pipeline_layout;
  pipeline_info.renderPass = m_impl->render_pass;
  pipeline_info.subpass = 0;
  
  result = vkCreateGraphicsPipelines(m_impl->device, VK_NULL_HANDLE, 1, &pipeline_info, nullptr, &m_impl->graphics_pipeline);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create graphics pipeline: {} ({})", vk_result_to_string(result), static_cast<int>(result));
    vkDestroyShaderModule(m_impl->device, vertex_shader_module, nullptr);
    vkDestroyShaderModule(m_impl->device, fragment_shader_module, nullptr);
    return false;
  }
  
  omnicpp::log::info("Graphics pipeline created successfully");
  
  // Clean up shader modules (no longer needed after pipeline creation)
  vkDestroyShaderModule(m_impl->device, vertex_shader_module, nullptr);
  vkDestroyShaderModule(m_impl->device, fragment_shader_module, nullptr);
  
  // === Create Vertex and Index Buffers for Game Objects ===
  omnicpp::log::info("Creating vertex and index buffers for 3D objects...");
  
  // Define vertices for game objects directly using explicit construction
  std::vector<Vertex> all_vertices;
  
  // Playing field (quad at y=0) - 4 vertices
  all_vertices.push_back({glm::vec3(-10.0f, 0.0f, -5.0f), glm::vec3(0.1f, 0.1f, 0.15f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 10.0f, 0.0f, -5.0f), glm::vec3(0.1f, 0.1f, 0.15f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 10.0f, 0.0f,  5.0f), glm::vec3(0.1f, 0.1f, 0.15f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-10.0f, 0.0f,  5.0f), glm::vec3(0.1f, 0.1f, 0.15f), glm::vec2(0.0f, 1.0f)});
  
  // Left paddle (blue cube) - 24 vertices (4 per face * 6 faces)
  // Front face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  // Back face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  // Top face
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  // Bottom face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  // Right face
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  // Left face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.2f, 0.6f, 0.9f), glm::vec2(0.0f, 1.0f)});
  
  // Right paddle (red cube) - 24 vertices
  // Front face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  // Back face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  // Top face
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  // Bottom face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  // Right face
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  // Left face
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f, -1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f,  0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.25f,  1.0f, -0.25f), glm::vec3(0.9f, 0.3f, 0.3f), glm::vec2(0.0f, 1.0f)});
  
  // Ball (white cube) - 24 vertices
  // Front face
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  // Back face
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  // Top face
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  // Bottom face
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  // Right face
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3( 0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  // Left face
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.3f, -0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 0.0f)});
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f,  0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(1.0f, 1.0f)});
  all_vertices.push_back({glm::vec3(-0.3f,  0.3f, -0.3f), glm::vec3(1.0f, 1.0f, 1.0f), glm::vec2(0.0f, 1.0f)});
  
  // Indices for the meshes
  std::vector<uint32_t> all_indices = {
    // Field (2 triangles)
    0, 1, 2, 0, 2, 3,
  };
  
  // Store index info for field
  m_impl->field_first_index = 0;
  m_impl->field_index_count = 6;
  
  // Add paddle indices (left paddle - 6 faces, 12 triangles)
  m_impl->left_paddle_first_index = static_cast<uint32_t>(all_indices.size());
  m_impl->left_paddle_index_count = 36;  // 6 faces * 2 triangles * 3 indices
  uint32_t base = 4;  // Start after field vertices
  // Front face
  all_indices.insert(all_indices.end(), {base+0, base+1, base+2, base+0, base+2, base+3});
  // Back face  
  all_indices.insert(all_indices.end(), {base+4, base+5, base+6, base+4, base+6, base+7});
  // Bottom face
  all_indices.insert(all_indices.end(), {base+8, base+9, base+10, base+8, base+10, base+11});
  // Top face
  all_indices.insert(all_indices.end(), {base+12, base+13, base+14, base+12, base+14, base+15});
  // Left face
  all_indices.insert(all_indices.end(), {base+16, base+17, base+18, base+16, base+18, base+19});
  // Right face
  all_indices.insert(all_indices.end(), {base+20, base+21, base+22, base+20, base+22, base+23});
  
  // Add right paddle indices
  m_impl->right_paddle_first_index = static_cast<uint32_t>(all_indices.size());
  m_impl->right_paddle_index_count = 36;
  base = 4 + 24;  // After field + left paddle
  // Front face
  all_indices.insert(all_indices.end(), {base+0, base+1, base+2, base+0, base+2, base+3});
  // Back face  
  all_indices.insert(all_indices.end(), {base+4, base+5, base+6, base+4, base+6, base+7});
  // Bottom face
  all_indices.insert(all_indices.end(), {base+8, base+9, base+10, base+8, base+10, base+11});
  // Top face
  all_indices.insert(all_indices.end(), {base+12, base+13, base+14, base+12, base+14, base+15});
  // Left face
  all_indices.insert(all_indices.end(), {base+16, base+17, base+18, base+16, base+18, base+19});
  // Right face
  all_indices.insert(all_indices.end(), {base+20, base+21, base+22, base+20, base+22, base+23});
  
  // Add ball indices
  m_impl->ball_first_index = static_cast<uint32_t>(all_indices.size());
  m_impl->ball_index_count = 36;
  base = 4 + 24 + 24;  // After field + paddles
  // Front face
  all_indices.insert(all_indices.end(), {base+0, base+1, base+2, base+0, base+2, base+3});
  // Back face  
  all_indices.insert(all_indices.end(), {base+4, base+5, base+6, base+4, base+6, base+7});
  // Bottom face
  all_indices.insert(all_indices.end(), {base+8, base+9, base+10, base+8, base+10, base+11});
  // Top face
  all_indices.insert(all_indices.end(), {base+12, base+13, base+14, base+12, base+14, base+15});
  // Left face
  all_indices.insert(all_indices.end(), {base+16, base+17, base+18, base+16, base+18, base+19});
  // Right face
  all_indices.insert(all_indices.end(), {base+20, base+21, base+22, base+20, base+22, base+23});
  
  omnicpp::log::info("Total vertices: {}, indices: {}", all_vertices.size(), all_indices.size());
  
  // Create vertex buffer
  VkDeviceSize buffer_size = sizeof(Vertex) * all_vertices.size();
  
  VkBufferCreateInfo vertex_buffer_info{};
  vertex_buffer_info.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
  vertex_buffer_info.size = buffer_size;
  vertex_buffer_info.usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
  vertex_buffer_info.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
  
  result = vkCreateBuffer(m_impl->device, &vertex_buffer_info, nullptr, &m_impl->vertex_buffer);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create vertex buffer: {}", vk_result_to_string(result));
    return false;
  }
  
  // Allocate vertex buffer memory
  VkMemoryRequirements mem_requirements;
  vkGetBufferMemoryRequirements(m_impl->device, m_impl->vertex_buffer, &mem_requirements);
  
  VkMemoryAllocateInfo alloc_info{};
  alloc_info.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
  alloc_info.allocationSize = mem_requirements.size;
  // Find memory type that is host visible
  VkPhysicalDeviceMemoryProperties mem_properties;
  vkGetPhysicalDeviceMemoryProperties(m_impl->physical_device, &mem_properties);
  uint32_t memory_type_index = UINT32_MAX;
  for (uint32_t i = 0; i < mem_properties.memoryTypeCount; i++) {
    if ((mem_requirements.memoryTypeBits & (1 << i))
&& 
        ((mem_properties.memoryTypes[i].propertyFlags & (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)) == (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT))) {
      memory_type_index = i;
      omnicpp::log::info("Found suitable memory type {} for vertex buffer", i);
      break;
    }
  }
  
  if (memory_type_index == 0 && mem_properties.memoryTypeCount > 0) {
    omnicpp::log::warn("Could not find ideal memory type, using first available");
    memory_type_index = 0;
  }
  
  if (memory_type_index == UINT32_MAX) {
    omnicpp::log::error("Failed to find suitable memory type for vertex buffer");
    return false;
  }
  
  alloc_info.memoryTypeIndex = memory_type_index;
  
  result = vkAllocateMemory(m_impl->device, &alloc_info, nullptr, &m_impl->vertex_buffer_memory);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to allocate vertex buffer memory: {}", vk_result_to_string(result));
    return false;
  }
  
  vkBindBufferMemory(m_impl->device, m_impl->vertex_buffer, m_impl->vertex_buffer_memory, 0);
  
  // Map and copy vertex data
  void* data = nullptr;
  result = vkMapMemory(m_impl->device, m_impl->vertex_buffer_memory, 0, buffer_size, 0, &data);
  if (result != VK_SUCCESS || data == nullptr) {
    omnicpp::log::error("Failed to map vertex buffer memory: {}", vk_result_to_string(result));
    return false;
  }
  memcpy(data, all_vertices.data(), buffer_size);
  vkUnmapMemory(m_impl->device, m_impl->vertex_buffer_memory);
  
  // Create index buffer
  VkDeviceSize index_buffer_size = sizeof(uint32_t) * all_indices.size();
  
  VkBufferCreateInfo index_buffer_info{};
  index_buffer_info.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
  index_buffer_info.size = index_buffer_size;
  index_buffer_info.usage = VK_BUFFER_USAGE_INDEX_BUFFER_BIT;
  index_buffer_info.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
  
  result = vkCreateBuffer(m_impl->device, &index_buffer_info, nullptr, &m_impl->index_buffer);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create index buffer: {}", vk_result_to_string(result));
    return false;
  }
  
  // Allocate index buffer memory
  vkGetBufferMemoryRequirements(m_impl->device, m_impl->index_buffer, &mem_requirements);
  alloc_info.allocationSize = mem_requirements.size;
  alloc_info.memoryTypeIndex = memory_type_index;
  
  result = vkAllocateMemory(m_impl->device, &alloc_info, nullptr, &m_impl->index_buffer_memory);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to allocate index buffer memory: {}", vk_result_to_string(result));
    return false;
  }
  
  vkBindBufferMemory(m_impl->device, m_impl->index_buffer, m_impl->index_buffer_memory, 0);
  
  // Map and copy index data
  vkMapMemory(m_impl->device, m_impl->index_buffer_memory, 0, index_buffer_size, 0, &data);
  memcpy(data, all_indices.data(), index_buffer_size);
  vkUnmapMemory(m_impl->device, m_impl->index_buffer_memory);
  
  omnicpp::log::info("Vertex and index buffers created successfully");
  
  // === Create Uniform Buffers ===
  omnicpp::log::info("Creating uniform buffers...");
  
  VkDeviceSize uniform_buffer_size = sizeof(UniformBufferObject);
  m_impl->uniform_buffers.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  m_impl->uniform_buffers_memory.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  m_impl->uniform_buffers_mapped.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  
  for (size_t i = 0; i < m_impl->MAX_FRAMES_IN_FLIGHT; i++) {
    VkBufferCreateInfo uniform_buffer_info{};
    uniform_buffer_info.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
    uniform_buffer_info.size = uniform_buffer_size;
    uniform_buffer_info.usage = VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT;
    uniform_buffer_info.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    
    result = vkCreateBuffer(m_impl->device, &uniform_buffer_info, nullptr, &m_impl->uniform_buffers[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create uniform buffer {}: {}", i, vk_result_to_string(result));
      return false;
    }
    
    vkGetBufferMemoryRequirements(m_impl->device, m_impl->uniform_buffers[i], &mem_requirements);
    alloc_info.allocationSize = mem_requirements.size;
    alloc_info.memoryTypeIndex = memory_type_index;
    
    result = vkAllocateMemory(m_impl->device, &alloc_info, nullptr, &m_impl->uniform_buffers_memory[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to allocate uniform buffer memory {}: {}", i, vk_result_to_string(result));
      return false;
    }
    
    vkBindBufferMemory(m_impl->device, m_impl->uniform_buffers[i], m_impl->uniform_buffers_memory[i], 0);
    vkMapMemory(m_impl->device, m_impl->uniform_buffers_memory[i], 0, uniform_buffer_size, 0, &m_impl->uniform_buffers_mapped[i]);
  }
  
  omnicpp::log::info("Uniform buffers created successfully");
  
  // === Create Descriptor Pool and Sets ===
  omnicpp::log::info("Creating descriptor pool and sets...");
  
  VkDescriptorPoolSize pool_size{};
  pool_size.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
  pool_size.descriptorCount = static_cast<uint32_t>(m_impl->MAX_FRAMES_IN_FLIGHT);
  
  VkDescriptorPoolCreateInfo pool_info{};
  pool_info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
  pool_info.poolSizeCount = 1;
  pool_info.pPoolSizes = &pool_size;
  pool_info.maxSets = static_cast<uint32_t>(m_impl->MAX_FRAMES_IN_FLIGHT);
  
  result = vkCreateDescriptorPool(m_impl->device, &pool_info, nullptr, &m_impl->descriptor_pool);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create descriptor pool: {}", vk_result_to_string(result));
    return false;
  }
  
  // Allocate descriptor sets
  std::vector<VkDescriptorSetLayout> layouts(m_impl->MAX_FRAMES_IN_FLIGHT, m_impl->descriptor_set_layout);
  VkDescriptorSetAllocateInfo descriptor_alloc_info{};
  descriptor_alloc_info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
  descriptor_alloc_info.descriptorPool = m_impl->descriptor_pool;
  descriptor_alloc_info.descriptorSetCount = static_cast<uint32_t>(m_impl->MAX_FRAMES_IN_FLIGHT);
  descriptor_alloc_info.pSetLayouts = layouts.data();
  
  m_impl->descriptor_sets.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  result = vkAllocateDescriptorSets(m_impl->device, &descriptor_alloc_info, m_impl->descriptor_sets.data());
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to allocate descriptor sets: {}", vk_result_to_string(result));
    return false;
  }
  
  // Update descriptor sets
  for (size_t i = 0; i < m_impl->MAX_FRAMES_IN_FLIGHT; i++) {
    VkDescriptorBufferInfo buffer_info{};
    buffer_info.buffer = m_impl->uniform_buffers[i];
    buffer_info.offset = 0;
    buffer_info.range = sizeof(UniformBufferObject);
    
    VkWriteDescriptorSet descriptor_write{};
    descriptor_write.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
    descriptor_write.dstSet = m_impl->descriptor_sets[i];
    descriptor_write.dstBinding = 0;
    descriptor_write.dstArrayElement = 0;
    descriptor_write.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    descriptor_write.descriptorCount = 1;
    descriptor_write.pBufferInfo = &buffer_info;
    
    vkUpdateDescriptorSets(m_impl->device, 1, &descriptor_write, 0, nullptr);
  }
  
  omnicpp::log::info("3D rendering pipeline initialized successfully");

  // Create framebuffers
  m_impl->swap_chain_framebuffers.resize(m_impl->swap_chain_image_views.size());
  for (size_t i = 0; i < m_impl->swap_chain_image_views.size(); i++) {
    VkImageView attachments[] = {
      m_impl->swap_chain_image_views[i]
    };

    VkFramebufferCreateInfo framebuffer_info{};
    framebuffer_info.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
    framebuffer_info.renderPass = m_impl->render_pass;
    framebuffer_info.attachmentCount = 1;
    framebuffer_info.pAttachments = attachments;
    framebuffer_info.width = m_impl->swap_chain_extent.width;
    framebuffer_info.height = m_impl->swap_chain_extent.height;
    framebuffer_info.layers = 1;

    result = vkCreateFramebuffer(m_impl->device, &framebuffer_info, nullptr, &m_impl->swap_chain_framebuffers[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create framebuffer {} ({})", i, static_cast<int>(result));
      return false;
    }
  }

  omnicpp::log::info("Framebuffers created successfully");

  // Create command pool
  QueueFamilyIndices queue_family_indices = find_queue_families(m_impl->physical_device, m_impl->surface);

  VkCommandPoolCreateInfo cmd_pool_info{};
  cmd_pool_info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
  cmd_pool_info.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
  cmd_pool_info.queueFamilyIndex = queue_family_indices.graphics_family.value();

  result = vkCreateCommandPool(m_impl->device, &cmd_pool_info, nullptr, &m_impl->command_pool);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to create command pool: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Command pool created successfully");

  // Create command buffers
  m_impl->command_buffers.resize(m_impl->swap_chain_framebuffers.size());

  VkCommandBufferAllocateInfo cmd_alloc_info{};
  cmd_alloc_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
  cmd_alloc_info.commandPool = m_impl->command_pool;
  cmd_alloc_info.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
  cmd_alloc_info.commandBufferCount = static_cast<uint32_t>(m_impl->command_buffers.size());

  result = vkAllocateCommandBuffers(m_impl->device, &cmd_alloc_info, m_impl->command_buffers.data());
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to allocate command buffers: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return false;
  }

  omnicpp::log::info("Command buffers allocated successfully");

  // Create semaphores
  m_impl->image_available_semaphores.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  m_impl->render_finished_semaphores.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  m_impl->in_flight_fences.resize(m_impl->MAX_FRAMES_IN_FLIGHT);
  m_impl->images_in_flight.resize(m_impl->swap_chain_images.size(), VK_NULL_HANDLE);

  VkSemaphoreCreateInfo semaphore_info{};
  semaphore_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;

  VkFenceCreateInfo fence_info{};
  fence_info.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
  fence_info.flags = VK_FENCE_CREATE_SIGNALED_BIT;

  for (size_t i = 0; i < m_impl->MAX_FRAMES_IN_FLIGHT; i++) {
    result = vkCreateSemaphore(m_impl->device, &semaphore_info, nullptr, &m_impl->image_available_semaphores[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create semaphore: {} ({})",
                    vk_result_to_string(result), static_cast<int>(result));
      return false;
    }

    result = vkCreateSemaphore(m_impl->device, &semaphore_info, nullptr, &m_impl->render_finished_semaphores[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create semaphore: {} ({})",
                    vk_result_to_string(result), static_cast<int>(result));
      return false;
    }

    result = vkCreateFence(m_impl->device, &fence_info, nullptr, &m_impl->in_flight_fences[i]);
    if (result != VK_SUCCESS) {
      omnicpp::log::error("Failed to create fence: {} ({})",
                    vk_result_to_string(result), static_cast<int>(result));
      return false;
    }
  }

  omnicpp::log::info("Semaphores and fences created successfully");

  m_impl->initialized = true;

  omnicpp::log::info("Renderer: Initialized with Vulkan");
  return true;

#else
  omnicpp::log::warn("Vulkan not available, renderer initialized in stub mode");
  m_impl->initialized = true;
  return true;
#endif
}

void Renderer::shutdown () {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (!m_impl->initialized) {
    return;
  }

#ifdef OMNICPP_HAS_VULKAN
  omnicpp::log::info("Shutting down Vulkan renderer...");

  vkDeviceWaitIdle(m_impl->device);

  // Cleanup semaphores and fences
  for (size_t i = 0; i < m_impl->MAX_FRAMES_IN_FLIGHT; i++) {
    if (m_impl->image_available_semaphores[i] != VK_NULL_HANDLE) {
      vkDestroySemaphore(m_impl->device, m_impl->image_available_semaphores[i], nullptr);
    }
    if (m_impl->render_finished_semaphores[i] != VK_NULL_HANDLE) {
      vkDestroySemaphore(m_impl->device, m_impl->render_finished_semaphores[i], nullptr);
    }
    if (m_impl->in_flight_fences[i] != VK_NULL_HANDLE) {
      vkDestroyFence(m_impl->device, m_impl->in_flight_fences[i], nullptr);
    }
  }

  // Cleanup command buffers and pool
  if (m_impl->command_pool != VK_NULL_HANDLE) {
    vkDestroyCommandPool(m_impl->device, m_impl->command_pool, nullptr);
  }

  // Cleanup framebuffers
  for (auto framebuffer : m_impl->swap_chain_framebuffers) {
    if (framebuffer != VK_NULL_HANDLE) {
      vkDestroyFramebuffer(m_impl->device, framebuffer, nullptr);
    }
  }

  // Cleanup pipeline
  if (m_impl->graphics_pipeline != VK_NULL_HANDLE) {
    vkDestroyPipeline(m_impl->device, m_impl->graphics_pipeline, nullptr);
  }

  // Cleanup pipeline layout
  if (m_impl->pipeline_layout != VK_NULL_HANDLE) {
    vkDestroyPipelineLayout(m_impl->device, m_impl->pipeline_layout, nullptr);
  }

  // Cleanup render pass
  if (m_impl->render_pass != VK_NULL_HANDLE) {
    vkDestroyRenderPass(m_impl->device, m_impl->render_pass, nullptr);
  }

  // Cleanup image views
  for (auto image_view : m_impl->swap_chain_image_views) {
    if (image_view != VK_NULL_HANDLE) {
      vkDestroyImageView(m_impl->device, image_view, nullptr);
    }
  }

  // Cleanup swap chain
  if (m_impl->swap_chain != VK_NULL_HANDLE) {
    vkDestroySwapchainKHR(m_impl->device, m_impl->swap_chain, nullptr);
  }

  // Cleanup descriptor set layout
  if (m_impl->descriptor_set_layout != VK_NULL_HANDLE) {
    vkDestroyDescriptorSetLayout(m_impl->device, m_impl->descriptor_set_layout, nullptr);
  }

  // Cleanup descriptor pool
  if (m_impl->descriptor_pool != VK_NULL_HANDLE) {
    vkDestroyDescriptorPool(m_impl->device, m_impl->descriptor_pool, nullptr);
  }

  // Cleanup uniform buffers
  for (size_t i = 0; i < m_impl->uniform_buffers.size(); i++) {
    if (m_impl->uniform_buffers[i] != VK_NULL_HANDLE) {
      vkDestroyBuffer(m_impl->device, m_impl->uniform_buffers[i], nullptr);
    }
    if (m_impl->uniform_buffers_memory[i] != VK_NULL_HANDLE) {
      vkFreeMemory(m_impl->device, m_impl->uniform_buffers_memory[i], nullptr);
    }
  }

  // Cleanup vertex buffer
  if (m_impl->vertex_buffer != VK_NULL_HANDLE) {
    vkDestroyBuffer(m_impl->device, m_impl->vertex_buffer, nullptr);
  }
  if (m_impl->vertex_buffer_memory != VK_NULL_HANDLE) {
    vkFreeMemory(m_impl->device, m_impl->vertex_buffer_memory, nullptr);
  }

  // Cleanup index buffer
  if (m_impl->index_buffer != VK_NULL_HANDLE) {
    vkDestroyBuffer(m_impl->device, m_impl->index_buffer, nullptr);
  }
  if (m_impl->index_buffer_memory != VK_NULL_HANDLE) {
    vkFreeMemory(m_impl->device, m_impl->index_buffer_memory, nullptr);
  }

  // Cleanup logical device
  if (m_impl->device != VK_NULL_HANDLE) {
    vkDestroyDevice(m_impl->device, nullptr);
  }

  // Cleanup surface
  if (m_impl->surface != VK_NULL_HANDLE) {
    vkDestroySurfaceKHR(m_impl->instance, m_impl->surface, nullptr);
  }

  // Cleanup debug messenger
  if (m_impl->debug_messenger != VK_NULL_HANDLE) {
    destroy_debug_utils_messenger_ext(m_impl->instance, m_impl->debug_messenger, nullptr);
  }

  // Cleanup instance
  if (m_impl->instance != VK_NULL_HANDLE) {
    vkDestroyInstance(m_impl->instance, nullptr);
  }

  omnicpp::log::info("Vulkan renderer shutdown complete");
#endif

  m_impl->initialized = false;

  omnicpp::log::info("Renderer: Shutdown");
}

void Renderer::update () {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (!m_impl->initialized) {
    return;
  }

#ifdef OMNICPP_HAS_VULKAN
  // Update renderer state here
  // For example: update uniform buffers, update scene state, etc.
#endif
}

void Renderer::render () {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (!m_impl->initialized) {
    omnicpp::log::error("Cannot render: Renderer not initialized");
    return;
  }

#ifdef OMNICPP_HAS_VULKAN
  // Wait for previous frame
  vkWaitForFences(m_impl->device, 1, &m_impl->in_flight_fences[m_impl->current_frame], VK_TRUE, UINT64_MAX);

  // Acquire image from swap chain
  uint32_t image_index;
  VkResult result = vkAcquireNextImageKHR(
      m_impl->device,
      m_impl->swap_chain,
      UINT64_MAX,
      m_impl->image_available_semaphores[m_impl->current_frame],
      VK_NULL_HANDLE,
      &image_index
  );

  if (result == VK_ERROR_OUT_OF_DATE_KHR) {
    // Swap chain is out of date (window resized/minimized)
    // Just skip this frame - the next frame will try again
    // This is a common occurrence during window operations
    omnicpp::log::debug("Swap chain out of date, skipping frame");
    return;
  } else if (result != VK_SUCCESS && result != VK_SUBOPTIMAL_KHR) {
    omnicpp::log::error("Failed to acquire swap chain image: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return;
  }

  // Reset fence for current frame
  vkResetFences(m_impl->device, 1, &m_impl->in_flight_fences[m_impl->current_frame]);

  // Reset command buffer
  vkResetCommandBuffer(m_impl->command_buffers[m_impl->current_frame], 0);

  // Record command buffer
  VkCommandBufferBeginInfo begin_info{};
  begin_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
  begin_info.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;

  result = vkBeginCommandBuffer(m_impl->command_buffers[m_impl->current_frame], &begin_info);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to begin recording command buffer: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return;
  }

  // Begin render pass
  VkRenderPassBeginInfo render_pass_info{};
  render_pass_info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
  render_pass_info.renderPass = m_impl->render_pass;
  render_pass_info.framebuffer = m_impl->swap_chain_framebuffers[image_index];
  render_pass_info.renderArea.offset = {0, 0};
  render_pass_info.renderArea.extent = m_impl->swap_chain_extent;

  VkClearValue clear_color = {{{0.0f, 0.0f, 0.0f, 1.0f}}};
  render_pass_info.clearValueCount = 1;
  render_pass_info.pClearValues = &clear_color;

  vkCmdBeginRenderPass(m_impl->command_buffers[m_impl->current_frame], &render_pass_info, VK_SUBPASS_CONTENTS_INLINE);

  // === Draw 3D Scene ===
  
  // Bind graphics pipeline
  vkCmdBindPipeline(m_impl->command_buffers[m_impl->current_frame], 
                    VK_PIPELINE_BIND_POINT_GRAPHICS, 
                    m_impl->graphics_pipeline);
  
  // Set viewport
  VkViewport viewport{};
  viewport.x = 0.0f;
  viewport.y = 0.0f;
  viewport.width = static_cast<float>(m_impl->swap_chain_extent.width);
  viewport.height = static_cast<float>(m_impl->swap_chain_extent.height);
  viewport.minDepth = 0.0f;
  viewport.maxDepth = 1.0f;
  vkCmdSetViewport(m_impl->command_buffers[m_impl->current_frame], 0, 1, &viewport);
  
  // Set scissor
  VkRect2D scissor{};
  scissor.offset = {0, 0};
  scissor.extent = m_impl->swap_chain_extent;
  vkCmdSetScissor(m_impl->command_buffers[m_impl->current_frame], 0, 1, &scissor);
  
  // Bind vertex buffer
  VkBuffer vertex_buffers[] = {m_impl->vertex_buffer};
  VkDeviceSize offsets[] = {0};
  vkCmdBindVertexBuffers(m_impl->command_buffers[m_impl->current_frame], 0, 1, vertex_buffers, offsets);
  
  // Bind index buffer
  vkCmdBindIndexBuffer(m_impl->command_buffers[m_impl->current_frame], m_impl->index_buffer, 0, VK_INDEX_TYPE_UINT32);
  
  // Bind descriptor sets (uniforms)
  vkCmdBindDescriptorSets(m_impl->command_buffers[m_impl->current_frame], 
                          VK_PIPELINE_BIND_POINT_GRAPHICS, 
                          m_impl->pipeline_layout, 
                          0, 1, &m_impl->descriptor_sets[m_impl->current_frame], 0, nullptr);
  
  // Update uniform buffer with camera matrices
  UniformBufferObject ubo{};
  
  // Camera view - positioned above and behind the field
  ubo.view = glm::lookAt(
      glm::vec3(10.0f, 15.0f, 20.0f),  // Camera position
      glm::vec3(10.0f, 5.0f, 0.0f),    // Look at center of field
      glm::vec3(0.0f, 1.0f, 0.0f)      // Up vector
  );
  
  // Projection matrix
  float aspect = static_cast<float>(m_impl->swap_chain_extent.width) / 
                 static_cast<float>(m_impl->swap_chain_extent.height);
  ubo.proj = glm::perspective(glm::radians(45.0f), aspect, 0.1f, 100.0f);
  
  // Draw playing field (floor)
  ubo.model = glm::mat4(1.0f);
  ubo.model = glm::translate(ubo.model, glm::vec3(10.0f, 0.0f, 0.0f));
  ubo.model = glm::rotate(ubo.model, glm::radians(-90.0f), glm::vec3(1.0f, 0.0f, 0.0f));
  memcpy(m_impl->uniform_buffers_mapped[m_impl->current_frame], &ubo, sizeof(ubo));
  vkCmdDrawIndexed(m_impl->command_buffers[m_impl->current_frame], 
                   m_impl->field_index_count, 1, m_impl->field_first_index, 0, 0);
  
  // Draw left paddle
  ubo.model = glm::mat4(1.0f);
  ubo.model = glm::translate(ubo.model, glm::vec3(1.0f, m_impl->left_paddle_y, 0.0f));
  memcpy(m_impl->uniform_buffers_mapped[m_impl->current_frame], &ubo, sizeof(ubo));
  vkCmdDrawIndexed(m_impl->command_buffers[m_impl->current_frame], 
                   m_impl->left_paddle_index_count, 1, m_impl->left_paddle_first_index, 0, 0);
  
  // Draw right paddle
  ubo.model = glm::mat4(1.0f);
  ubo.model = glm::translate(ubo.model, glm::vec3(19.0f, m_impl->right_paddle_y, 0.0f));
  memcpy(m_impl->uniform_buffers_mapped[m_impl->current_frame], &ubo, sizeof(ubo));
  vkCmdDrawIndexed(m_impl->command_buffers[m_impl->current_frame], 
                   m_impl->right_paddle_index_count, 1, m_impl->right_paddle_first_index, 0, 0);
  
  // Draw ball
  ubo.model = glm::mat4(1.0f);
  ubo.model = glm::translate(ubo.model, glm::vec3(m_impl->ball_x, m_impl->ball_y, 0.0f));
  memcpy(m_impl->uniform_buffers_mapped[m_impl->current_frame], &ubo, sizeof(ubo));
  vkCmdDrawIndexed(m_impl->command_buffers[m_impl->current_frame], 
                   m_impl->ball_index_count, 1, m_impl->ball_first_index, 0, 0);
  
  vkCmdEndRenderPass(m_impl->command_buffers[m_impl->current_frame]);

  result = vkEndCommandBuffer(m_impl->command_buffers[m_impl->current_frame]);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to record command buffer: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return;
  }

  // Submit command buffer
  VkSubmitInfo submit_info{};
  submit_info.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;

  VkSemaphore wait_semaphores[] = {
    m_impl->image_available_semaphores[m_impl->current_frame]
  };
  VkPipelineStageFlags wait_stages[] = {
    VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT
  };
  submit_info.waitSemaphoreCount = 1;
  submit_info.pWaitSemaphores = wait_semaphores;
  submit_info.pWaitDstStageMask = wait_stages;

  VkSemaphore signal_semaphores[] = {
    m_impl->render_finished_semaphores[m_impl->current_frame]
  };
  submit_info.signalSemaphoreCount = 1;
  submit_info.pSignalSemaphores = signal_semaphores;

  submit_info.commandBufferCount = 1;
  submit_info.pCommandBuffers = &m_impl->command_buffers[m_impl->current_frame];

  result = vkQueueSubmit(m_impl->graphics_queue, 1, &submit_info, m_impl->in_flight_fences[m_impl->current_frame]);
  if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to submit draw command buffer: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
    return;
  }

  // Present image
  VkPresentInfoKHR present_info{};
  present_info.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
  present_info.waitSemaphoreCount = 1;
  present_info.pWaitSemaphores = signal_semaphores;

  VkSwapchainKHR swap_chains[] = {
    m_impl->swap_chain
  };
  present_info.swapchainCount = 1;
  present_info.pSwapchains = swap_chains;
  present_info.pImageIndices = &image_index;

  result = vkQueuePresentKHR(m_impl->present_queue, &present_info);

  if (result == VK_ERROR_OUT_OF_DATE_KHR) {
    // Swap chain is out of date (window resized/minimized)
    // Will be handled on next frame
    omnicpp::log::debug("Swap chain out of date on present");
  } else if (result != VK_SUCCESS) {
    omnicpp::log::error("Failed to present swap chain image: {} ({})",
                  vk_result_to_string(result), static_cast<int>(result));
  }

  // Advance to next frame
  m_impl->current_frame = (m_impl->current_frame + 1) % m_impl->MAX_FRAMES_IN_FLIGHT;

  m_impl->frame_count++;
#endif
}

void Renderer::clear () {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (!m_impl->initialized) {
    return;
  }

#ifdef OMNICPP_HAS_VULKAN
  // Clear buffers here
#endif
}

void Renderer::present () {
  std::lock_guard<std::mutex> lock (m_impl->mutex);

  if (!m_impl->initialized) {
    return;
  }

#ifdef OMNICPP_HAS_VULKAN
  // Present is handled in render() method
#endif
}

void Renderer::set_window_manager (Window::WindowManager* window_manager) {
  std::lock_guard<std::mutex> lock (m_impl->mutex);
  m_impl->window_manager = window_manager;
}

void Renderer::set_ball_position(float x, float y) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    m_impl->ball_x = x;
    m_impl->ball_y = y;
}

void Renderer::set_paddle_position(bool is_left, float y) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    if (is_left) {
        m_impl->left_paddle_y = y;
    } else {
        m_impl->right_paddle_y = y;
    }
}

uint32_t Renderer::get_frame_count () const {
  std::lock_guard<std::mutex> lock (m_impl->mutex);
  return m_impl->frame_count;
}

} // namespace OmniCpp::Engine::Graphics
