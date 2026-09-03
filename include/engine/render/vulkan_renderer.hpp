#pragma once

/**
 * @file vulkan_renderer.hpp
 * @brief Vulkan renderer: command buffers, frame synchronization, draw loop.
 */

#include "engine/core/deterministic_runtime.hpp"
#include "engine/render/vulkan_context.hpp"
#include "engine/render/vulkan_swapchain.hpp"
#include "engine/render/vulkan_render_pass.hpp"
#include "engine/render/vulkan_pipeline.hpp"
#include <cstdint>
#include <vector>

namespace omnicpp::render {

//! Per-frame GPU timing telemetry in nanoseconds.
struct GpuTiming {
  std::uint64_t render_pass_ns{0};
};

struct FrameResources {
  VkCommandBuffer command_buffer{VK_NULL_HANDLE};
  VkFence in_flight_fence{VK_NULL_HANDLE};
  VkSemaphore image_available_semaphore{VK_NULL_HANDLE};
  VkSemaphore render_finished_semaphore{VK_NULL_HANDLE};
  bool frame_in_flight{false};
  void cleanup(VkDevice device) noexcept;
};

struct RendererConfig {
  std::uint32_t max_frames_in_flight{2};
  float clear_color_r{0.0f};
  float clear_color_g{0.0f};
  float clear_color_b{0.0f};
  float clear_color_a{1.0f};
  float clear_depth{1.0f};
  std::uint32_t clear_depth_stencil{0};
};

class VulkanRenderer final {
public:
  VulkanRenderer() = default;
  ~VulkanRenderer();

  VulkanRenderer(const VulkanRenderer&) = delete;
  VulkanRenderer& operator=(const VulkanRenderer&) = delete;
  VulkanRenderer(VulkanRenderer&&) = delete;
  VulkanRenderer& operator=(VulkanRenderer&&) = delete;

  [[nodiscard]] omnicpp::core::Result<void> initialize(
      VulkanContext& context,
      const VulkanSwapchain& swapchain,
      const VulkanRenderPass& render_pass,
      const RendererConfig& config = {});

  [[nodiscard]] omnicpp::core::Result<std::uint32_t> begin_frame();
  [[nodiscard]] omnicpp::core::Result<void> record_commands(
      std::uint32_t image_index,
      VkFramebuffer framebuffer,
      std::uint32_t width, std::uint32_t height);
  //! Submit the acquired frame without presenting it. Keeps the image acquired.
  [[nodiscard]] omnicpp::core::Result<void> submit_frame();
  //! Present the frame previously submitted by submit_frame().
  [[nodiscard]] omnicpp::core::Result<void> present_frame();
  //! Submit and present the acquired frame.
  [[nodiscard]] omnicpp::core::Result<void> end_frame();
  //! Rebind to a recreated swapchain and rebuilt pass/framebuffer resources.
  [[nodiscard]] omnicpp::core::Result<void> resync_for_swapchain(
      const VulkanSwapchain& swapchain, VkRenderPass render_pass);

  void wait_idle() noexcept;
  void cleanup(VkDevice device) noexcept;

  [[nodiscard]] bool is_initialized() const noexcept { return initialized_; }
  [[nodiscard]] std::uint32_t current_frame() const noexcept { return current_frame_; }
  [[nodiscard]] std::uint64_t frame_count() const noexcept { return frame_count_; }
  [[nodiscard]] const RendererConfig& config() const noexcept { return config_; }

  //! Bind the graphics pipeline used by record_commands().
  void set_pipeline(VkPipeline pipeline) noexcept { pipeline_ = pipeline; }

  //! Enable Synchronization 2 submission path (requires negotiated device).
  void set_synchronization2(bool enabled) noexcept { synchronization2_ = enabled; }
  [[nodiscard]] bool uses_synchronization2() const noexcept { return synchronization2_; }
  //! Enable timeline-semaphore frame pacing (requires negotiated Vulkan 1.2 feature).
  //! Replaces binary fence waits with a monotonic frame-counter timeline:
  //! CPU throttling and per-image reuse waits use exact signaled frame values.
  void set_timeline_pacing(bool enabled) noexcept { timeline_pacing_requested_ = enabled; }
  [[nodiscard]] bool uses_timeline_pacing() const noexcept { return timeline_pacing_; }
  //! Monotonic count of successfully submitted frames (timeline signal value).
  [[nodiscard]] std::uint64_t frame_counter() const noexcept { return frame_counter_; }
  //! Query function pointers from the device each initialize(); nullptr on 1.2 devices.
  [[nodiscard]] const GpuTiming& gpu_timing() const noexcept { return gpu_timing_; }

  [[nodiscard]] static omnicpp::core::Result<VkCommandPool> create_command_pool(
      VkDevice device, std::uint32_t queue_family_index);
  [[nodiscard]] static omnicpp::core::Result<VkCommandBuffer> allocate_command_buffer(
      VkDevice device, VkCommandPool pool);

private:
  VkDevice device_{VK_NULL_HANDLE};
  VkQueue graphics_queue_{VK_NULL_HANDLE};
  VkQueue present_queue_{VK_NULL_HANDLE};
  VkCommandPool command_pool_{VK_NULL_HANDLE};
  VkRenderPass render_pass_{VK_NULL_HANDLE};
  VkPipelineLayout pipeline_layout_{VK_NULL_HANDLE};
  VkPipeline pipeline_{VK_NULL_HANDLE};
  const VulkanSwapchain* swapchain_{nullptr};
  std::vector<FrameResources> frames_;
  // A present operation may retain its signal semaphore after the frame slot
  // advances, so render-finished semaphores are owned by swapchain image.
  std::vector<VkSemaphore> render_finished_semaphores_;
  std::uint32_t current_frame_{0};
  std::uint64_t frame_count_{0};
  bool initialized_{false};
  RendererConfig config_;
  std::uint32_t acquired_image_index_{0};
  bool frame_acquired_{false};
  std::vector<VkFence> images_in_flight_;
  bool synchronization2_{false};
  bool timeline_pacing_requested_{false};
  bool timeline_pacing_{false};
  VkSemaphore timeline_semaphore_{VK_NULL_HANDLE};
  std::uint64_t frame_counter_{0};
  // Timeline mode: frame value whose submit last rendered each swapchain image.
  std::vector<std::uint64_t> image_last_frame_;
  GpuTiming gpu_timing_{};
};

} // namespace omnicpp::render
