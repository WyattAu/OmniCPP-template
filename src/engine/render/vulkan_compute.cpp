/**
 * @file vulkan_compute.cpp
 * @brief Compute dispatch and event-based GPU synchronization.
 *
 * Uses core events (vkCmdSetEvent/vkCmdWaitEvents with explicit stage masks)
 * so the helpers work on any Vulkan 1.0+ device; the render graph's sync2
 * submission is orthogonal to event ordering.
 */

#include "engine/render/vulkan_compute.hpp"

#include <cassert>

#ifdef OMNICPP_HAS_VULKAN
#include <vulkan/vulkan.h>
#endif

namespace omnicpp::render {

void cmd_signal_event(VkCommandBuffer command_buffer, VkEvent event,
                      std::uint32_t src_stage) {
#ifdef OMNICPP_HAS_VULKAN
  assert(event != VK_NULL_HANDLE);
  vkCmdSetEvent(command_buffer, event, src_stage);
#endif
}

void cmd_acquire_shared_image(VkCommandBuffer command_buffer, VkEvent event,
                              const QueueImageState& state) {
#ifdef OMNICPP_HAS_VULKAN
  assert(event != VK_NULL_HANDLE && state.image != VK_NULL_HANDLE);

  // Concurrent-usage images: queue ownership transfers via RELEASE (producer
  // side) then ACQUIRE (this call). With single-queue testing the acquire
  // barrier still performs the layout transition + visibility; the event
  // provides producer->consumer ordering without CPU round-trips.
  VkImageMemoryBarrier acquire{};
  acquire.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
  acquire.srcAccessMask = 0;  // The wait provides producer visibility.
  acquire.dstAccessMask = state.consumer_access;
  acquire.oldLayout = state.current_layout;
  acquire.newLayout = state.consumer_layout;
  acquire.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
  acquire.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
  acquire.image = state.image;
  acquire.subresourceRange = {VK_IMAGE_ASPECT_COLOR_BIT, 0, 1, 0, 1};

  vkCmdWaitEvents(
      command_buffer, 1, &event,
      state.last_stage, state.consumer_stage,
      0, nullptr, 0, nullptr, 1, &acquire);
#else
  (void)command_buffer;
  (void)event;
  (void)state;
#endif
}

}  // namespace omnicpp::render
