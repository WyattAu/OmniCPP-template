/**
 * @file VulkanRenderer.hpp
 * @brief Vulkan renderer implementation
 * @version 1.0.0
 */

#pragma once

#include "engine/IRenderer.hpp"
#include <vulkan/vulkan.h>
#include <memory>

namespace omnicpp {
namespace render {

// Forward declarations
class RenderPipeline;
class ShaderManager;
class SwapChain;

/**
 * @brief Vulkan renderer implementation
 * 
 * Handles Vulkan initialization, rendering, and resource management.
 */
class VulkanRenderer : public IRenderer {
public:
    /**
     * @brief Construct a new Vulkan Renderer object
     */
    VulkanRenderer();

    /**
     * @brief Destroy the Vulkan Renderer object
     */
    ~VulkanRenderer() override;

    // Disable copying
    VulkanRenderer(const VulkanRenderer&) = delete;
    VulkanRenderer& operator=(const VulkanRenderer&) = delete;

    // Enable moving
    VulkanRenderer(VulkanRenderer&&) noexcept = default;
    VulkanRenderer& operator=(VulkanRenderer&&) noexcept = default;

    /**
     * @brief Initialize the renderer
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize() override;

    /**
     * @brief Shutdown the renderer
     */
    void shutdown() override;

    /**
     * @brief Begin a new frame
     */
    void begin_frame() override;

    /**
     * @brief End the current frame
     */
    void end_frame() override;

    /**
     * @brief Get the Vulkan instance
     * @return VkInstance The Vulkan instance
     */
    VkInstance get_instance() const { return m_instance; }

    /**
     * @brief Get the physical device
     * @return VkPhysicalDevice The physical device
     */
    VkPhysicalDevice get_physical_device() const { return m_physical_device; }

    /**
     * @brief Get the logical device
     * @return VkDevice The logical device
     */
    VkDevice get_device() const { return m_device; }

    /**
     * @brief Get the graphics queue
     * @return VkQueue The graphics queue
     */
    VkQueue get_graphics_queue() const { return m_graphics_queue; }

    /**
     * @brief Get the present queue
     * @return VkQueue The present queue
     */
    VkQueue get_present_queue() const { return m_present_queue; }

    /**
     * @brief Get the command pool
     * @return VkCommandPool The command pool
     */
    VkCommandPool get_command_pool() const { return m_command_pool; }

    /**
     * @brief Get the render pipeline
     * @return RenderPipeline* Pointer to render pipeline
     */
    RenderPipeline* get_render_pipeline() const { return m_render_pipeline.get(); }

    /**
     * @brief Get the shader manager
     * @return ShaderManager* Pointer to shader manager
     */
    ShaderManager* get_shader_manager() const { return m_shader_manager.get(); }

    /**
     * @brief Get the swap chain
     * @return SwapChain* Pointer to swap chain
     */
    SwapChain* get_swap_chain() const { return m_swap_chain.get(); }

    /**
     * @brief Check if renderer is initialized
     * @return true if initialized, false otherwise
     */
    bool is_initialized() const { return m_initialized; }

private:
    /**
     * @brief Create Vulkan instance
     * @return true if successful, false otherwise
     */
    bool create_instance();

    /**
     * @brief Setup debug messenger
     * @return true if successful, false otherwise
     */
    bool setup_debug_messenger();

    /**
     * @brief Pick physical device
     * @return true if successful, false otherwise
     */
    bool pick_physical_device();

    /**
     * @brief Create logical device
     * @return true if successful, false otherwise
     */
    bool create_logical_device();

    /**
     * @brief Create swap chain
     * @return true if successful, false otherwise
     */
    bool create_swap_chain();

    /**
     * @brief Create command pool
     * @return true if successful, false otherwise
     */
    bool create_command_pool();

    /**
     * @brief Create render pipeline
     * @return true if successful, false otherwise
     */
    bool create_render_pipeline();

    /**
     * @brief Create shader manager
     * @return true if successful, false otherwise
     */
    bool create_shader_manager();

private:
    VkInstance m_instance = VK_NULL_HANDLE;
    VkDebugUtilsMessengerEXT m_debug_messenger = VK_NULL_HANDLE;
    VkPhysicalDevice m_physical_device = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    VkQueue m_graphics_queue = VK_NULL_HANDLE;
    VkQueue m_present_queue = VK_NULL_HANDLE;
    VkCommandPool m_command_pool = VK_NULL_HANDLE;

    std::unique_ptr<RenderPipeline> m_render_pipeline;
    std::unique_ptr<ShaderManager> m_shader_manager;
    std::unique_ptr<SwapChain> m_swap_chain;

    bool m_initialized = false;
    bool m_enable_validation_layers = true;
};

} // namespace render
} // namespace omnicpp
