/**
 * @file RenderPipeline.hpp
 * @brief Render pipeline for Vulkan
 * @version 1.0.0
 */

#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <memory>

namespace omnicpp {
namespace render {

// Forward declarations
class ShaderManager;

/**
 * @brief Render pipeline for Vulkan
 * 
 * Manages the graphics pipeline state and configuration.
 */
class RenderPipeline {
public:
    /**
     * @brief Construct a new Render Pipeline object
     * @param device Vulkan logical device
     * @param swap_chain_extent Swap chain extent
     * @param shader_manager Pointer to shader manager
     */
    RenderPipeline(VkDevice device, 
                 VkExtent2D swap_chain_extent,
                 ShaderManager* shader_manager);

    /**
     * @brief Destroy the Render Pipeline object
     */
    ~RenderPipeline();

    // Disable copying
    RenderPipeline(const RenderPipeline&) = delete;
    RenderPipeline& operator=(const RenderPipeline&) = delete;

    // Enable moving
    RenderPipeline(RenderPipeline&&) noexcept = default;
    RenderPipeline& operator=(RenderPipeline&&) noexcept = default;

    /**
     * @brief Get pipeline layout
     * @return VkPipelineLayout The pipeline layout
     */
    VkPipelineLayout get_pipeline_layout() const { return m_pipeline_layout; }

    /**
     * @brief Get graphics pipeline
     * @return VkPipeline The graphics pipeline
     */
    VkPipeline get_pipeline() const { return m_pipeline; }

    /**
     * @brief Get render pass
     * @return VkRenderPass The render pass
     */
    VkRenderPass get_render_pass() const { return m_render_pass; }

    /**
     * @brief Recreate pipeline (e.g., after window resize)
     * @param new_extent New swap chain extent
     */
    void recreate(VkExtent2D new_extent);

private:
    /**
     * @brief Create render pass
     * @return true if successful, false otherwise
     */
    bool create_render_pass();

    /**
     * @brief Create pipeline layout
     * @return true if successful, false otherwise
     */
    bool create_pipeline_layout();

    /**
     * @brief Create graphics pipeline
     * @return true if successful, false otherwise
     */
    bool create_graphics_pipeline();

    /**
     * @brief Cleanup pipeline resources
     */
    void cleanup();

private:
    VkDevice m_device = VK_NULL_HANDLE;
    VkExtent2D m_swap_chain_extent;
    ShaderManager* m_shader_manager = nullptr;

    VkPipelineLayout m_pipeline_layout = VK_NULL_HANDLE;
    VkPipeline m_pipeline = VK_NULL_HANDLE;
    VkRenderPass m_render_pass = VK_NULL_HANDLE;
};

} // namespace render
} // namespace omnicpp
