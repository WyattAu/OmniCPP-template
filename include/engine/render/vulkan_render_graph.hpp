#pragma once

/**
 * @file vulkan_render_graph.hpp
 * @brief Declarative pass graph with automatic image barriers.
 *
 * Passes declare color/depth attachments with explicit usage timelines.
 * `compile()` computes, for every image, the layout/access/stage transition
 * between consecutive passes and emits `VkImageMemoryBarrier`s. `execute()`
 * inserts the barriers and records each pass via a caller callback, all
 * inside one command buffer.
 */

#include "engine/core/deterministic_runtime.hpp"
#include "engine/render/vulkan_types.hpp"
#include <cstdint>
#include <vector>

namespace omnicpp::render {

//! Declares how one pass uses one image attachment.
struct RenderPassAttachment {
  VkImage image{VK_NULL_HANDLE};
  VkImageView view{VK_NULL_HANDLE};
  VkFormat format{VK_FORMAT_UNDEFINED};
  //! Layout the image must be in when the pass starts (after barriers).
  VkImageLayout used_layout{VK_IMAGE_LAYOUT_UNDEFINED};   // set per role below
  //! Layout the pass leaves the image in when it ends.
  VkImageLayout final_layout{VK_IMAGE_LAYOUT_UNDEFINED};
  //! Access mask the pass performs on the image.
  std::uint32_t access{0};   // VkAccessFlags value (0 when Vulkan-off)
  //! Pipeline stage where the access happens.
  std::uint32_t stage{0};    // VkPipelineStageFlags value (0 when Vulkan-off)
  bool is_depth{false};
};

//! Builder helpers so callers do not touch raw masks/levels by hand.
[[nodiscard]] RenderPassAttachment color_attachment(
    VkImage image, VkImageView view, VkFormat format,
    VkImageLayout final_layout);
[[nodiscard]] RenderPassAttachment depth_attachment(
    VkImage image, VkImageView view, VkFormat format,
    VkImageLayout final_layout);

//! One render pass: a name, its attachments, and a record callback handle.
struct GraphPass {
  const char* name{nullptr};
  VkRenderPass render_pass{VK_NULL_HANDLE};
  VkFramebuffer framebuffer{VK_NULL_HANDLE};
  std::vector<RenderPassAttachment> attachments;
  //! Clear values handed to the record callback (ownership stays with caller).
  const VkClearValue* clear_values{nullptr};
  std::uint32_t clear_value_count{0};
  std::uint32_t width{0};
  std::uint32_t height{0};
  //! Opaque handle returned to the record callback (e.g. the pass index).
  void* user_data{nullptr};
};

//! A computed transition inserted before a pass.
struct GraphBarrier {
  VkImage image{VK_NULL_HANDLE};
  VkImageLayout old_layout{VK_IMAGE_LAYOUT_UNDEFINED};
  VkImageLayout new_layout{VK_IMAGE_LAYOUT_UNDEFINED};
  std::uint32_t src_access{0};
  std::uint32_t dst_access{0};
  std::uint32_t src_stage{0};
  std::uint32_t dst_stage{0};
};

//! Compiled barrier plan: barriers_[pass_index] run before that pass.
struct CompiledRenderGraph {
  std::vector<std::vector<GraphBarrier>> barriers_per_pass;
};

/**
 * @brief Computes the minimal barrier set between declared passes.
 *
 * The compiler tracks each image's current layout/access/stage across the
 * declared sequence. When a pass needs a different layout or when writes
 * follow reads, it emits exactly the transitions required — no manual
 * barrier authoring, no hidden state.
 */
[[nodiscard]] CompiledRenderGraph compile_render_graph(
    const std::vector<GraphPass>& passes);

/**
 * @brief Executes a compiled graph inside one command buffer.
 *
 * @param command_buffer  Buffer in the recording state (caller began it).
 * @param passes          Same pass list given to compile_render_graph.
 * @param compiled        Output of compile_render_graph.
 * @param record_pass     Callback recording the pass's commands; receives
 *                        the command buffer and pass->user_data. It runs
 *                        inside an active render pass and must not end it.
 */
void execute_render_graph(
    VkCommandBuffer command_buffer,
    const std::vector<GraphPass>& passes,
    const CompiledRenderGraph& compiled,
    void (*record_pass)(VkCommandBuffer, const GraphPass&, void*));

} // namespace omnicpp::render
