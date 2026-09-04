#pragma once

/**
 * @file vulkan_compute.hpp
 * @brief Compute dispatch and event-based GPU synchronization.
 *
 * Complements the render graph: graphics passes stay in the render graph
 * (render-pass-structured), while async compute/dispatch work uses this
 * module. Cross-queue ordering uses events + wait/dst-stage masks so a
 * graphics submission can consume compute results with a GPU-side wait —
 * no CPU round-trip, no blocking the graphics queue on the compute queue.
 */

#include "engine/core/deterministic_runtime.hpp"
#include "engine/render/vulkan_types.hpp"
#include <cstdint>

namespace omnicpp::render {

//! State of one image across a queue handoff (release/acquire pair).
struct QueueImageState {
  VkImage image{VK_NULL_HANDLE};
  //! Layout the image is in before the release (== after the producing work).
  VkImageLayout current_layout{VK_IMAGE_LAYOUT_UNDEFINED};
  //! Access mask of the producing work's last touch.
  std::uint32_t last_access{0};
  //! Pipeline stage of the producing work's last touch.
  std::uint32_t last_stage{0};
  //! Layout the consumer needs.
  VkImageLayout consumer_layout{VK_IMAGE_LAYOUT_UNDEFINED};
  //! Access mask the consumer performs.
  std::uint32_t consumer_access{0};
  //! Stage where the consumer touches the image.
  std::uint32_t consumer_stage{0};
};

//! Signal `event` after the producing work completes (record at the end of
//! the producer's command buffer, after its last write to the image).
void cmd_signal_event(VkCommandBuffer command_buffer, VkEvent event,
                      std::uint32_t src_stage);

//! Record the queue-handoff acquire: wait on `event` (raised by the producer
//! on another queue) and insert the release/acquire queue-ownership transfer
//! barrier for the image. Record at the start of the consumer's command
//! buffer, before any use of the image.
void cmd_acquire_shared_image(VkCommandBuffer command_buffer, VkEvent event,
                              const QueueImageState& state);

}  // namespace omnicpp::render
