#pragma once

/**
 * @file vulkan_parallel_recorder.hpp
 * @brief Multithreaded secondary-command-buffer recording.
 *
 * Splits a viewport into horizontal bands and records one secondary command
 * buffer per band on worker threads (command pools are thread-local, one per
 * thread, per Vulkan's external synchronization requirements). The primary
 * buffer then executes the secondaries inside the render pass.
 */

#include "engine/core/deterministic_runtime.hpp"
#include "engine/render/vulkan_types.hpp"
#include <functional>
#include <vector>

namespace omnicpp::render {

//! Per-band record job: receives the secondary buffer and the band's scissor.
using RecordBandFn = std::function<void(VkCommandBuffer, VkRect2D)>;

class VulkanParallelRecorder final {
public:
  VulkanParallelRecorder() = default;
  ~VulkanParallelRecorder();
  VulkanParallelRecorder(const VulkanParallelRecorder&) = delete;
  VulkanParallelRecorder& operator=(const VulkanParallelRecorder&) = delete;
  VulkanParallelRecorder(VulkanParallelRecorder&&) = delete;
  VulkanParallelRecorder& operator=(VulkanParallelRecorder&&) = delete;

  [[nodiscard]] omnicpp::core::Result<void> initialize(
      VkDevice device, std::uint32_t queue_family_index,
      std::uint32_t band_count);
  void cleanup() noexcept;

  [[nodiscard]] bool is_initialized() const noexcept { return device_ != VK_NULL_HANDLE; }
  [[nodiscard]] std::uint32_t band_count() const noexcept { return band_count_; }

  /**
   * @brief Records `band_count` secondary buffers in parallel.
   *
   * @param width, height      Full-frame extents (bands split height evenly).
   * @param record_band        Called once per band on a worker thread. It must
   *                           only record into the given secondary buffer.
   * @param compatible_pass    Render pass the secondaries will execute in
   *                           (required for RENDER_PASS_CONTINUE inheritance).
   * @param framebuffer        Framebuffer being rendered to (0 allowed).
   * @return Secondary buffers in band order, ready for
   *         vkCmdExecuteCommands inside an active render pass.
   */
  [[nodiscard]] omnicpp::core::Result<std::vector<VkCommandBuffer>> record_parallel(
      std::uint32_t width, std::uint32_t height, const RecordBandFn& record_band,
      VkRenderPass compatible_pass, VkFramebuffer framebuffer = VK_NULL_HANDLE);

  //! Reset all secondary buffers for the next frame (call outside render pass).
  [[nodiscard]] omnicpp::core::Result<void> reset();

private:
  struct Band {
    VkCommandPool pool{VK_NULL_HANDLE};
    VkCommandBuffer buffer{VK_NULL_HANDLE};
  };

  VkDevice device_{VK_NULL_HANDLE};
  std::uint32_t queue_family_index_{0};
  std::vector<Band> bands_;
  std::uint32_t band_count_{0};
};

} // namespace omnicpp::render
