#pragma once

/**
 * @file vulkan_offscreen.hpp
 * @brief Offscreen Vulkan color target for deterministic rendering tests.
 */

#include "engine/core/deterministic_runtime.hpp"
#include "engine/render/vulkan_memory_allocator.hpp"
#include "engine/render/vulkan_types.hpp"
#include <cstdint>

namespace omnicpp::render {

class VulkanOffscreenTarget final {
public:
  VulkanOffscreenTarget() = default;
  ~VulkanOffscreenTarget();

  VulkanOffscreenTarget(const VulkanOffscreenTarget&) = delete;
  VulkanOffscreenTarget& operator=(const VulkanOffscreenTarget&) = delete;
  VulkanOffscreenTarget(VulkanOffscreenTarget&&) = delete;
  VulkanOffscreenTarget& operator=(VulkanOffscreenTarget&&) = delete;

  [[nodiscard]] omnicpp::core::Result<void> create(
      VkDevice device, VkPhysicalDevice physical_device,
      VkFormat format, std::uint32_t width, std::uint32_t height,
      VulkanMemoryAllocator* allocator = nullptr);
  [[nodiscard]] omnicpp::core::Result<void> create_render_pass(VkDevice device);
  [[nodiscard]] omnicpp::core::Result<void> create_framebuffer(VkDevice device);
  void cleanup(VkDevice device) noexcept;

  [[nodiscard]] VkImage image() const noexcept { return image_; }
  [[nodiscard]] VkImageView image_view() const noexcept { return image_view_; }
  [[nodiscard]] VkRenderPass render_pass() const noexcept { return render_pass_; }
  [[nodiscard]] VkFramebuffer framebuffer() const noexcept { return framebuffer_; }
  [[nodiscard]] VkFormat format() const noexcept { return format_; }
  [[nodiscard]] std::uint32_t width() const noexcept { return width_; }
  [[nodiscard]] std::uint32_t height() const noexcept { return height_; }
  [[nodiscard]] bool is_valid() const noexcept {
    return image_ != VK_NULL_HANDLE && image_view_ != VK_NULL_HANDLE &&
           render_pass_ != VK_NULL_HANDLE && framebuffer_ != VK_NULL_HANDLE;
  }

private:
  VkImage image_{VK_NULL_HANDLE};
  VkDeviceMemory memory_{VK_NULL_HANDLE};
  // Owns the image binding when created through a VulkanMemoryAllocator.
  VulkanMemoryAllocator* allocator_{nullptr};
  Allocation allocator_allocation_{};
  bool uses_allocator_{false};
  VkImageView image_view_{VK_NULL_HANDLE};
  VkRenderPass render_pass_{VK_NULL_HANDLE};
  VkFramebuffer framebuffer_{VK_NULL_HANDLE};
  VkFormat format_{VK_FORMAT_UNDEFINED};
  std::uint32_t width_{0};
  std::uint32_t height_{0};
};

} // namespace omnicpp::render
