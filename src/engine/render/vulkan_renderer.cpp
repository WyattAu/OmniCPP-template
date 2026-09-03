/**
 * @file vulkan_renderer.cpp
 * @brief Vulkan renderer implementation: command buffers, frame sync, draw loop.
 */

#include "engine/render/vulkan_renderer.hpp"
#include <cstring>

#ifdef OMNICPP_HAS_VULKAN
#include <vulkan/vulkan.h>
#endif

namespace omnicpp::render {

void FrameResources::cleanup(VkDevice device) noexcept {
#ifdef OMNICPP_HAS_VULKAN
  if (device) {
    if (in_flight_fence) vkDestroyFence(device, in_flight_fence, nullptr);
    if (image_available_semaphore) vkDestroySemaphore(device, image_available_semaphore, nullptr);
    if (render_finished_semaphore) vkDestroySemaphore(device, render_finished_semaphore, nullptr);
  }
  command_buffer = nullptr;
  in_flight_fence = nullptr;
  image_available_semaphore = nullptr;
  render_finished_semaphore = nullptr;
  frame_in_flight = false;
#else
  (void)device;
#endif
}

VulkanRenderer::~VulkanRenderer() { cleanup(nullptr); }

omnicpp::core::Result<void> VulkanRenderer::initialize(
    VulkanContext& context,
    const VulkanSwapchain& swapchain,
    const VulkanRenderPass& render_pass,
    const RendererConfig& config) {
#ifdef OMNICPP_HAS_VULKAN
  if (!context.is_initialized() || !context.device()) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }

  device_ = context.device();
  graphics_queue_ = context.graphics_queue();
  present_queue_ = context.present_queue();
  render_pass_ = render_pass.render_pass();
  swapchain_ = &swapchain;
  config_ = config;

  auto pool_result = create_command_pool(
      device_, static_cast<std::uint32_t>(context.queue_families().graphics_family));
  if (!pool_result.is_ok()) {
    return omnicpp::core::Result<void>::error(pool_result.error());
  }
  command_pool_ = pool_result.value();

  if (config.max_frames_in_flight == 0 || swapchain.image_count() == 0) {
    cleanup(device_);
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::invalid_config);
  }

  frames_.resize(config.max_frames_in_flight);
  images_in_flight_.assign(swapchain.image_count(), VK_NULL_HANDLE);
  render_finished_semaphores_.assign(swapchain.image_count(), VK_NULL_HANDLE);
  // Timeline pacing decision up front: it changes which resources are created.
  timeline_pacing_ = timeline_pacing_requested_ && context.has_timeline_semaphores();
  VkSemaphoreCreateInfo sem_info{};
  sem_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
  for (std::size_t i = 0; i < frames_.size(); ++i) {
    auto cb_result = allocate_command_buffer(device_, command_pool_);
    if (!cb_result.is_ok()) {
      cleanup(device_);
      return omnicpp::core::Result<void>::error(cb_result.error());
    }
    frames_[i].command_buffer = cb_result.value();

    if (!timeline_pacing_) {
      VkFenceCreateInfo fence_info{};
      fence_info.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
      fence_info.flags = VK_FENCE_CREATE_SIGNALED_BIT;
      if (vkCreateFence(device_, &fence_info, nullptr, &frames_[i].in_flight_fence) != VK_SUCCESS) {
        cleanup(device_);
        return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
      }
    }
    // In timeline mode the per-frame fence is omitted entirely: the timeline
    // semaphore paces CPU-GPU, and a never-reset fence would be submitted in
    // the SIGNALED state (VUID-vkQueueSubmit-fence-00063).

    if (vkCreateSemaphore(device_, &sem_info, nullptr, &frames_[i].image_available_semaphore) != VK_SUCCESS) {
      cleanup(device_);
      return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
    }
  }
  for (auto& semaphore : render_finished_semaphores_) {
    const VkResult result = vkCreateSemaphore(device_, &sem_info, nullptr, &semaphore);
    if (result != VK_SUCCESS) {
      cleanup(device_);
      return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
    }
  }

  // Timeline semaphore for frame pacing (decision made before resource creation).
  if (timeline_pacing_) {
    VkSemaphoreTypeCreateInfo type_info{};
    type_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_TYPE_CREATE_INFO;
    type_info.semaphoreType = VK_SEMAPHORE_TYPE_TIMELINE;
    type_info.initialValue = 0;
    VkSemaphoreCreateInfo timeline_info{};
    timeline_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
    timeline_info.pNext = &type_info;
    if (vkCreateSemaphore(device_, &timeline_info, nullptr, &timeline_semaphore_) != VK_SUCCESS) {
      cleanup(device_);
      return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
    }
    image_last_frame_.assign(swapchain.image_count(), 0);
  }

  initialized_ = true;
  return omnicpp::core::Result<void>::ok();
#else
  (void)context; (void)swapchain; (void)render_pass; (void)config;
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<std::uint32_t> VulkanRenderer::begin_frame() {
#ifdef OMNICPP_HAS_VULKAN
  if (!initialized_) return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);

  auto& frame = frames_[current_frame_];
  if (timeline_pacing_) {
    // Timeline pacing: this frame's slot is safe when the timeline has passed
    // the value this slot last signaled (one frame in flight per slot).
    // Throttle only when every slot has been used at least once; otherwise
    // the arithmetic would underflow and wait on an unreachable value.
    const std::uint64_t frame_slots = frames_.size();
    if (frame_counter_ >= frame_slots) {
      const std::uint64_t wait_value = frame_counter_ + 1U - frame_slots;
      VkSemaphoreWaitInfo wait_info{};
      wait_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_WAIT_INFO;
      wait_info.semaphoreCount = 1;
      wait_info.pSemaphores = &timeline_semaphore_;
      wait_info.pValues = &wait_value;
      if (vkWaitSemaphores(device_, &wait_info, UINT64_MAX) != VK_SUCCESS) {
        return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);
      }
    }
  } else {
    vkWaitForFences(device_, 1, &frame.in_flight_fence, VK_TRUE, UINT64_MAX);
  }
  frame.frame_in_flight = false;

  std::uint32_t image_index = 0;
  VkResult result = vkAcquireNextImageKHR(device_, swapchain_->swapchain(), UINT64_MAX,
      frame.image_available_semaphore, VK_NULL_HANDLE, &image_index);

  if (result == VK_ERROR_OUT_OF_DATE_KHR) {
    return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::invalid_config);
  }
  if (result != VK_SUCCESS && result != VK_SUBOPTIMAL_KHR) {
    return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }
  if (image_index >= images_in_flight_.size()) {
    return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }
  if (images_in_flight_[image_index] && images_in_flight_[image_index] != frame.in_flight_fence) {
    vkWaitForFences(device_, 1, &images_in_flight_[image_index], VK_TRUE, UINT64_MAX);
  }

  if (timeline_pacing_) {
    // Per-image reuse: wait until the exact frame that last rendered this
    // image has completed (timeline reached that frame's signal value).
    const std::uint64_t last_frame = image_last_frame_[image_index];
    if (last_frame > 0) {
      VkSemaphoreWaitInfo wait_info{};
      wait_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_WAIT_INFO;
      wait_info.semaphoreCount = 1;
      wait_info.pSemaphores = &timeline_semaphore_;
      wait_info.pValues = &last_frame;
      if (vkWaitSemaphores(device_, &wait_info, UINT64_MAX) != VK_SUCCESS) {
        return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);
      }
    }
  } else {
    if (images_in_flight_[image_index] && images_in_flight_[image_index] != frame.in_flight_fence) {
      vkWaitForFences(device_, 1, &images_in_flight_[image_index], VK_TRUE, UINT64_MAX);
    }
  }

  if (!timeline_pacing_) {
    vkResetFences(device_, 1, &frame.in_flight_fence);
  }
  vkResetCommandBuffer(frame.command_buffer, 0);
  if (!timeline_pacing_) {
    images_in_flight_[image_index] = frame.in_flight_fence;
  }
  acquired_image_index_ = image_index;
  frame_acquired_ = true;
  return omnicpp::core::Result<std::uint32_t>::ok(image_index);
#else
  return omnicpp::core::Result<std::uint32_t>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<void> VulkanRenderer::record_commands(
    std::uint32_t image_index, VkFramebuffer framebuffer,
    std::uint32_t width, std::uint32_t height) {
#ifdef OMNICPP_HAS_VULKAN
  if (!initialized_ || image_index >= swapchain_->image_count()) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }

  auto& frame = frames_[current_frame_];
  VkCommandBuffer cb = frame.command_buffer;

  VkCommandBufferBeginInfo begin_info{};
  begin_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
  begin_info.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;
  vkBeginCommandBuffer(cb, &begin_info);

  VkRenderPassBeginInfo rp_info{};
  rp_info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
  rp_info.renderPass = render_pass_;
  rp_info.framebuffer = framebuffer;
  rp_info.renderArea.offset = {0, 0};
  rp_info.renderArea.extent = {width, height};

  VkClearValue clear_values[2];
  clear_values[0].color = {{config_.clear_color_r, config_.clear_color_g, config_.clear_color_b, config_.clear_color_a}};
  clear_values[1].depthStencil = {config_.clear_depth, config_.clear_depth_stencil};
  rp_info.clearValueCount = 2;
  rp_info.pClearValues = clear_values;

  vkCmdBeginRenderPass(cb, &rp_info, VK_SUBPASS_CONTENTS_INLINE);

  VkViewport viewport{};
  viewport.x = 0.0f; viewport.y = 0.0f;
  viewport.width = static_cast<float>(width);
  viewport.height = static_cast<float>(height);
  viewport.minDepth = 0.0f; viewport.maxDepth = 1.0f;
  vkCmdSetViewport(cb, 0, 1, &viewport);

  VkRect2D scissor{};
  scissor.offset = {0, 0};
  scissor.extent = {width, height};
  vkCmdSetScissor(cb, 0, 1, &scissor);

  if (pipeline_) {
    vkCmdBindPipeline(cb, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline_);
    vkCmdDraw(cb, 3, 1, 0, 0);
  }

  vkCmdEndRenderPass(cb);
  vkEndCommandBuffer(cb);

  return omnicpp::core::Result<void>::ok();
#else
  (void)image_index; (void)framebuffer; (void)width; (void)height;
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<void> VulkanRenderer::submit_frame() {
#ifdef OMNICPP_HAS_VULKAN
  if (!initialized_ || !frame_acquired_ ||
      acquired_image_index_ >= render_finished_semaphores_.size()) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }

  auto& frame = frames_[current_frame_];
  VkSubmitInfo submit_info{};
  submit_info.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
  VkSemaphore wait_semaphores[] = {frame.image_available_semaphore};
  VkPipelineStageFlags wait_stages[] = {VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT};
  submit_info.waitSemaphoreCount = 1;
  submit_info.pWaitSemaphores = wait_semaphores;
  submit_info.pWaitDstStageMask = wait_stages;
  submit_info.commandBufferCount = 1;
  submit_info.pCommandBuffers = &frame.command_buffer;
  const VkSemaphore render_finished_semaphore =
      render_finished_semaphores_[acquired_image_index_];
  submit_info.signalSemaphoreCount = 1;
  submit_info.pSignalSemaphores = &render_finished_semaphore;

  // Timeline pacing: signal the monotonic frame counter on submit.
  const std::uint64_t signal_frame = frame_counter_ + 1;

  if (synchronization2_) {
    auto submit2 = reinterpret_cast<PFN_vkQueueSubmit2>(vkGetDeviceProcAddr(
        device_, "vkQueueSubmit2"));
    if (submit2) {
      VkCommandBufferSubmitInfo command_info{};
      command_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_SUBMIT_INFO;
      command_info.commandBuffer = frame.command_buffer;
      VkSemaphoreSubmitInfo wait_info{};
      wait_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO;
      wait_info.semaphore = frame.image_available_semaphore;
      wait_info.stageMask = VK_PIPELINE_STAGE_2_COLOR_ATTACHMENT_OUTPUT_BIT;
      VkSemaphoreSubmitInfo signal_info{};
      signal_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO;
      signal_info.semaphore = render_finished_semaphores_[acquired_image_index_];
      signal_info.stageMask = VK_PIPELINE_STAGE_2_COLOR_ATTACHMENT_OUTPUT_BIT;
      VkSubmitInfo2 submit2_info{};
      submit2_info.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO_2;
      submit2_info.commandBufferInfoCount = 1;
      submit2_info.pCommandBufferInfos = &command_info;
      submit2_info.waitSemaphoreInfoCount = 1;
      submit2_info.pWaitSemaphoreInfos = &wait_info;
      submit2_info.signalSemaphoreInfoCount = 1;
      submit2_info.pSignalSemaphoreInfos = &signal_info;
      if (timeline_pacing_) {
        VkSemaphoreSubmitInfo timeline_signal_info{};
        timeline_signal_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO;
        timeline_signal_info.semaphore = timeline_semaphore_;
        timeline_signal_info.value = signal_frame;
        timeline_signal_info.stageMask = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
        // Contiguous value array; decays to the required pointer type.
        VkSemaphoreSubmitInfo signal_infos[2] = {signal_info, timeline_signal_info};
        submit2_info.pSignalSemaphoreInfos = signal_infos;
        submit2_info.signalSemaphoreInfoCount = 2;
      }
      const VkResult result = submit2(graphics_queue_, 1, &submit2_info,
          timeline_pacing_ ? VK_NULL_HANDLE : frame.in_flight_fence);
      if (result != VK_SUCCESS) {
        return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
      }
      frame.frame_in_flight = true;
      frame_counter_ = signal_frame;
      image_last_frame_[acquired_image_index_] = signal_frame;
      return omnicpp::core::Result<void>::ok();
    }
  }

  // Timeline pacing on the legacy path: attach signal values via pNext chain.
  VkSemaphore legacy_signal_semaphores[2] = {render_finished_semaphore, timeline_semaphore_};
  std::uint64_t legacy_signal_values[2] = {0, signal_frame};
  VkTimelineSemaphoreSubmitInfo timeline_submit_info{};
  if (timeline_pacing_) {
    timeline_submit_info.sType = VK_STRUCTURE_TYPE_TIMELINE_SEMAPHORE_SUBMIT_INFO;
    timeline_submit_info.signalSemaphoreValueCount = 2;
    timeline_submit_info.pSignalSemaphoreValues = legacy_signal_values;
    submit_info.pNext = &timeline_submit_info;
    submit_info.signalSemaphoreCount = 2;
    submit_info.pSignalSemaphores = legacy_signal_semaphores;
  }

  const VkResult result = vkQueueSubmit(graphics_queue_, 1, &submit_info,
      timeline_pacing_ ? VK_NULL_HANDLE : frame.in_flight_fence);
  if (result != VK_SUCCESS) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }
  frame.frame_in_flight = true;
  if (timeline_pacing_) {
    frame_counter_ = signal_frame;
    image_last_frame_[acquired_image_index_] = signal_frame;
  }
  return omnicpp::core::Result<void>::ok();
#else
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<void> VulkanRenderer::present_frame() {
#ifdef OMNICPP_HAS_VULKAN
  if (!initialized_ || !frame_acquired_) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }

  const VkSemaphore render_finished_semaphore =
      render_finished_semaphores_[acquired_image_index_];
  VkPresentInfoKHR present_info{};
  present_info.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
  present_info.waitSemaphoreCount = 1;
  present_info.pWaitSemaphores = &render_finished_semaphore;
  VkSwapchainKHR swapchains[] = {swapchain_->swapchain()};
  const std::uint32_t image_index = acquired_image_index_;
  present_info.swapchainCount = 1;
  present_info.pSwapchains = swapchains;
  present_info.pImageIndices = &image_index;

  const VkResult result = vkQueuePresentKHR(present_queue_, &present_info);
  if (result != VK_SUCCESS && result != VK_SUBOPTIMAL_KHR && result != VK_ERROR_OUT_OF_DATE_KHR) {
    frame_acquired_ = false;
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  }

  frame_acquired_ = false;
  current_frame_ = (current_frame_ + 1) % static_cast<std::uint32_t>(frames_.size());
  ++frame_count_;
  return omnicpp::core::Result<void>::ok();
#else
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<void> VulkanRenderer::end_frame() {
  auto submit_result = submit_frame();
  if (!submit_result.is_ok()) return submit_result;
  return present_frame();
}

omnicpp::core::Result<void> VulkanRenderer::resync_for_swapchain(
    const VulkanSwapchain& swapchain, VkRenderPass render_pass) {
#ifdef OMNICPP_HAS_VULKAN
  if (!initialized_ || !device_ || !swapchain.is_valid() || swapchain.image_count() == 0 ||
      !render_pass) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::invalid_config);
  }
  if (frame_acquired_) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::invalid_config);
  }

  vkDeviceWaitIdle(device_);
  swapchain_ = &swapchain;
  render_pass_ = render_pass;

  // Retire and rebuild per-image resources for the new image set.
  for (auto semaphore : render_finished_semaphores_) {
    if (semaphore) vkDestroySemaphore(device_, semaphore, nullptr);
  }
  render_finished_semaphores_.assign(swapchain.image_count(), VK_NULL_HANDLE);
  images_in_flight_.assign(swapchain.image_count(), VK_NULL_HANDLE);
  VkSemaphoreCreateInfo sem_info{};
  sem_info.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
  for (auto& semaphore : render_finished_semaphores_) {
    if (vkCreateSemaphore(device_, &sem_info, nullptr, &semaphore) != VK_SUCCESS) {
      cleanup(device_);
      return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
    }
  }
  if (timeline_pacing_) {
    // Device is idle: no timeline work is pending, so per-image history resets.
    image_last_frame_.assign(swapchain.image_count(), 0);
  }
  current_frame_ = 0;
  acquired_image_index_ = 0;
  return omnicpp::core::Result<void>::ok();
#else
  (void)swapchain;
  (void)render_pass;
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

void VulkanRenderer::wait_idle() noexcept {
#ifdef OMNICPP_HAS_VULKAN
  if (device_) vkDeviceWaitIdle(device_);
#endif
}

void VulkanRenderer::cleanup(VkDevice device) noexcept {
#ifdef OMNICPP_HAS_VULKAN
  VkDevice dev = device ? device : device_;
  if (dev) {
    vkDeviceWaitIdle(dev);
    for (auto& frame : frames_) frame.cleanup(dev);
    for (auto semaphore : render_finished_semaphores_) {
      if (semaphore) vkDestroySemaphore(dev, semaphore, nullptr);
    }
    if (timeline_semaphore_) vkDestroySemaphore(dev, timeline_semaphore_, nullptr);
    if (command_pool_) vkDestroyCommandPool(dev, command_pool_, nullptr);
  }
  frames_.clear();
  render_finished_semaphores_.clear();
  timeline_semaphore_ = nullptr;
  timeline_pacing_ = false;
  frame_counter_ = 0;
  image_last_frame_.clear();
  command_pool_ = nullptr;
  device_ = nullptr;
  graphics_queue_ = nullptr;
  present_queue_ = nullptr;
  render_pass_ = nullptr;
  pipeline_ = nullptr;
  pipeline_layout_ = nullptr;
  swapchain_ = nullptr;
  current_frame_ = 0;
  frame_count_ = 0;
  images_in_flight_.clear();
  initialized_ = false;
  acquired_image_index_ = 0;
  frame_acquired_ = false;
#else
  (void)device;
#endif
}

omnicpp::core::Result<VkCommandPool> VulkanRenderer::create_command_pool(
    VkDevice device, std::uint32_t queue_family_index) {
#ifdef OMNICPP_HAS_VULKAN
  if (!device) return omnicpp::core::Result<VkCommandPool>::error(omnicpp::core::RuntimeError::vulkan_not_available);

  VkCommandPoolCreateInfo pool_info{};
  pool_info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
  pool_info.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
  pool_info.queueFamilyIndex = queue_family_index;

  VkCommandPool pool = nullptr;
  VkResult result = vkCreateCommandPool(device, &pool_info, nullptr, &pool);
  if (result != VK_SUCCESS || !pool) return omnicpp::core::Result<VkCommandPool>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  return omnicpp::core::Result<VkCommandPool>::ok(pool);
#else
  (void)device; (void)queue_family_index;
  return omnicpp::core::Result<VkCommandPool>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<VkCommandBuffer> VulkanRenderer::allocate_command_buffer(
    VkDevice device, VkCommandPool pool) {
#ifdef OMNICPP_HAS_VULKAN
  if (!device || !pool) return omnicpp::core::Result<VkCommandBuffer>::error(omnicpp::core::RuntimeError::vulkan_not_available);

  VkCommandBufferAllocateInfo alloc_info{};
  alloc_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
  alloc_info.commandPool = pool;
  alloc_info.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
  alloc_info.commandBufferCount = 1;

  VkCommandBuffer cb = nullptr;
  VkResult result = vkAllocateCommandBuffers(device, &alloc_info, &cb);
  if (result != VK_SUCCESS || !cb) return omnicpp::core::Result<VkCommandBuffer>::error(omnicpp::core::RuntimeError::vulkan_not_available);
  return omnicpp::core::Result<VkCommandBuffer>::ok(cb);
#else
  (void)device; (void)pool;
  return omnicpp::core::Result<VkCommandBuffer>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

} // namespace omnicpp::render
