#include "engine/render/vulkan_render_graph.hpp"

#include <cstring>
#include <unordered_map>

#ifdef OMNICPP_HAS_VULKAN
#include <vulkan/vulkan.h>
#endif

namespace omnicpp::render {

// Attachment builder helpers. Values mirror the Vulkan constants so the
// Vulkan-off shim build resolves them; real Vulkan builds see the same bits.

RenderPassAttachment color_attachment(
    VkImage image, VkImageView view, VkFormat format,
    VkImageLayout final_layout) {
  RenderPassAttachment a;
  a.image = image;
  a.view = view;
  a.format = format;
  a.used_layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
  a.final_layout = final_layout;
#ifdef OMNICPP_HAS_VULKAN
  a.access = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
  a.stage = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
#else
  constexpr std::uint32_t kColorWriteAccess = 0x40;
  constexpr std::uint32_t kColorOutStage = 0x200;
  a.access = kColorWriteAccess;
  a.stage = kColorOutStage;
#endif
  a.is_depth = false;
  return a;
}

RenderPassAttachment depth_attachment(
    VkImage image, VkImageView view, VkFormat format,
    VkImageLayout final_layout) {
  RenderPassAttachment a;
  a.image = image;
  a.view = view;
  a.format = format;
  a.used_layout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
  a.final_layout = final_layout;
#ifdef OMNICPP_HAS_VULKAN
  a.access = VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT;
  a.stage = VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT |
            VK_PIPELINE_STAGE_LATE_FRAGMENT_TESTS_BIT;
#else
  constexpr std::uint32_t kDepthWriteAccess = 0x200;
  constexpr std::uint32_t kEarlyFrag = 0x1000;
  constexpr std::uint32_t kLateFrag = 0x2000;
  a.access = kDepthWriteAccess;
  a.stage = kEarlyFrag | kLateFrag;
#endif
  a.is_depth = true;
  return a;
}

// =============================================================================
// Compiler
// =============================================================================

namespace {

struct ImageState {
  VkImageLayout layout{VK_IMAGE_LAYOUT_UNDEFINED};
  std::uint32_t access{0};
  std::uint32_t stage{0};
  bool valid{false};   // False until the image's first declaration.
};

//! Previous-pass access vs. this pass's access: barrier needed when the
//! ordering matters (write-after-read, read-after-write, write-after-write).
bool access_ordering_matters(std::uint32_t prev_access, std::uint32_t prev_stage,
                             std::uint32_t next_access, std::uint32_t next_stage) {
  const bool prev_writes =
      (prev_access & (0x40U /*COLOR_WRITE*/ | 0x200U /*DEPTH_WRITE*/ |
                      0x8U /*TRANSFER_WRITE*/ | 0x1U /*SHADER_WRITE*/)) != 0U;
  const bool next_writes =
      (next_access & (0x40U | 0x200U | 0x8U | 0x1U)) != 0U;
  (void)prev_stage; (void)next_stage;
  return prev_writes || next_writes; // conservative: sync on any write edge
}

} // namespace

CompiledRenderGraph compile_render_graph(const std::vector<GraphPass>& passes) {
  CompiledRenderGraph out;
  out.barriers_per_pass.resize(passes.size());

  std::unordered_map<VkImage, ImageState> states;

  for (std::size_t p = 0; p < passes.size(); ++p) {
    const GraphPass& pass = passes[p];
    std::vector<GraphBarrier>& barriers = out.barriers_per_pass[p];

    for (const RenderPassAttachment& att : pass.attachments) {
      if (!att.image) continue;
      ImageState& state = states[att.image];

      const bool needs_barrier =
          !state.valid ||
          state.layout != att.used_layout ||
          access_ordering_matters(state.access, state.stage,
                                  att.access, att.stage);

      if (needs_barrier) {
        GraphBarrier barrier;
        barrier.image = att.image;
        barrier.old_layout = state.valid ? state.layout : VK_IMAGE_LAYOUT_UNDEFINED;
        barrier.new_layout = att.used_layout;
        barrier.src_access = state.access;
        barrier.dst_access = att.access;
        barrier.src_stage = state.valid ? state.stage : 0U;
        barrier.dst_stage = att.stage;
        barriers.push_back(barrier);
      }
      state.layout = att.final_layout;
      state.access = att.access;
      state.stage = att.stage;
      state.valid = true;
    }
  }

  return out;
}

// =============================================================================
// Executor
// =============================================================================

void execute_render_graph(
    VkCommandBuffer command_buffer,
    const std::vector<GraphPass>& passes,
    const CompiledRenderGraph& compiled,
    void (*record_pass)(VkCommandBuffer, const GraphPass&, void*)) {
  if (!command_buffer) return;

#ifdef OMNICPP_HAS_VULKAN
  for (std::size_t p = 0; p < passes.size() && p < compiled.barriers_per_pass.size(); ++p) {
    const auto& barriers = compiled.barriers_per_pass[p];
    if (!barriers.empty()) {
      std::vector<VkImageMemoryBarrier> vk_barriers;
      vk_barriers.reserve(barriers.size());
      VkPipelineStageFlags src_stage_mask = 0;
      VkPipelineStageFlags dst_stage_mask = 0;
      for (const auto& barrier : barriers) {
        VkImageMemoryBarrier b{};
        b.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
        b.oldLayout = barrier.old_layout;
        b.newLayout = barrier.new_layout;
        b.srcAccessMask = barrier.src_access;
        b.dstAccessMask = barrier.dst_access;
        b.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
        b.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
        b.image = barrier.image;
        b.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        b.subresourceRange.levelCount = 1;
        b.subresourceRange.layerCount = 1;
        vk_barriers.push_back(b);
        src_stage_mask |= barrier.src_stage;
        dst_stage_mask |= barrier.dst_stage;
      }
      // UNDEFINED -> X transitions need no src access; ensure non-zero masks.
      if (src_stage_mask == 0) src_stage_mask = VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT;
      if (dst_stage_mask == 0) dst_stage_mask = VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT;
      vkCmdPipelineBarrier(command_buffer, src_stage_mask, dst_stage_mask,
                           0, 0, nullptr, 0, nullptr,
                           static_cast<std::uint32_t>(vk_barriers.size()),
                           vk_barriers.data());
    }

    const GraphPass& pass = passes[p];

    VkRenderPassBeginInfo begin_info{};
    begin_info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
    begin_info.renderPass = pass.render_pass;
    begin_info.framebuffer = pass.framebuffer;
    begin_info.renderArea.extent = {pass.width, pass.height};
    begin_info.clearValueCount = pass.clear_value_count;
    begin_info.pClearValues = pass.clear_values;
    vkCmdBeginRenderPass(command_buffer, &begin_info, VK_SUBPASS_CONTENTS_INLINE);

    if (record_pass) {
      record_pass(command_buffer, pass, pass.user_data);
    }

    vkCmdEndRenderPass(command_buffer);
  }
#else
  (void)passes; (void)compiled; (void)record_pass;
#endif
}

} // namespace omnicpp::render
