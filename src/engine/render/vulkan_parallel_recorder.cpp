#include "engine/render/vulkan_parallel_recorder.hpp"

#include <algorithm>
#include <thread>

#ifdef OMNICPP_HAS_VULKAN
#include <vulkan/vulkan.h>
#endif

namespace omnicpp::render {

VulkanParallelRecorder::~VulkanParallelRecorder() { cleanup(); }

omnicpp::core::Result<void> VulkanParallelRecorder::initialize(
    VkDevice device, std::uint32_t queue_family_index, std::uint32_t band_count) {
#ifdef OMNICPP_HAS_VULKAN
  if (!device || band_count == 0) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::invalid_config);
  }
  if (device_) cleanup();
  device_ = device;
  queue_family_index_ = queue_family_index;
  band_count_ = band_count;
  bands_.resize(band_count);
  for (auto& band : bands_) {
    band.pool = VK_NULL_HANDLE;
    band.buffer = VK_NULL_HANDLE;
  }
  for (auto& band : bands_) {
    VkCommandPoolCreateInfo pool_info{};
    pool_info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
    pool_info.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
    pool_info.queueFamilyIndex = queue_family_index;
    if (vkCreateCommandPool(device_, &pool_info, nullptr, &band.pool) != VK_SUCCESS) {
      cleanup();
      return omnicpp::core::Result<void>::error(
          omnicpp::core::RuntimeError::vulkan_not_available);
    }
    VkCommandBufferAllocateInfo alloc_info{};
    alloc_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    alloc_info.commandPool = band.pool;
    alloc_info.level = VK_COMMAND_BUFFER_LEVEL_SECONDARY;
    alloc_info.commandBufferCount = 1;
    if (vkAllocateCommandBuffers(device_, &alloc_info, &band.buffer) != VK_SUCCESS) {
      cleanup();
      return omnicpp::core::Result<void>::error(
          omnicpp::core::RuntimeError::vulkan_not_available);
    }
  }
  return omnicpp::core::Result<void>::ok();
#else
  (void)device; (void)queue_family_index; (void)band_count;
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

void VulkanParallelRecorder::cleanup() noexcept {
#ifdef OMNICPP_HAS_VULKAN
  if (device_) {
    for (auto& band : bands_) {
      if (band.pool) vkDestroyCommandPool(device_, band.pool, nullptr);
    }
  }
#endif
  bands_.clear();
  band_count_ = 0;
  device_ = VK_NULL_HANDLE;
}

omnicpp::core::Result<std::vector<VkCommandBuffer>> VulkanParallelRecorder::record_parallel(
    std::uint32_t width, std::uint32_t height, const RecordBandFn& record_band,
    VkRenderPass compatible_pass, VkFramebuffer framebuffer) {
#ifdef OMNICPP_HAS_VULKAN
  if (!device_ || !record_band || width == 0 || height == 0 || !compatible_pass) {
    return omnicpp::core::Result<std::vector<VkCommandBuffer>>::error(
        omnicpp::core::RuntimeError::invalid_config);
  }
  if (height < band_count_) {
    return omnicpp::core::Result<std::vector<VkCommandBuffer>>::error(
        omnicpp::core::RuntimeError::invalid_config);
  }

  const std::uint32_t band_height = height / band_count_;

  auto record_band_buffer = [&](std::size_t index) {
    const VkCommandBuffer buffer = bands_[index].buffer;
    VkCommandBufferBeginInfo begin{};
    begin.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    begin.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT |
                  VK_COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT;
    VkCommandBufferInheritanceInfo inheritance{};
    inheritance.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_INFO;
    inheritance.renderPass = compatible_pass;
    inheritance.framebuffer = framebuffer;
    inheritance.subpass = 0;
    begin.pInheritanceInfo = &inheritance;
    vkBeginCommandBuffer(buffer, &begin);

    VkRect2D scissor{};
    scissor.offset = {0, static_cast<std::int32_t>(index * band_height)};
    scissor.extent = {width, (index + 1 == bands_.size()) ? height - index * band_height
                                                          : band_height};
    record_band(buffer, scissor);

    vkEndCommandBuffer(buffer);
  };

  std::vector<std::thread> workers;
  workers.reserve(bands_.size());
  for (std::size_t i = 1; i < bands_.size(); ++i) {
    workers.emplace_back(record_band_buffer, i);
  }
  record_band_buffer(0); // Band 0 on the calling thread.
  for (auto& worker : workers) {
    worker.join();
  }

  std::vector<VkCommandBuffer> buffers;
  buffers.reserve(bands_.size());
  for (const auto& band : bands_) {
    buffers.push_back(band.buffer);
  }
  return omnicpp::core::Result<std::vector<VkCommandBuffer>>::ok(buffers);
#else
  (void)width; (void)height; (void)record_band;
  (void)compatible_pass; (void)framebuffer;
  return omnicpp::core::Result<std::vector<VkCommandBuffer>>::error(
      omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

omnicpp::core::Result<void> VulkanParallelRecorder::reset() {
#ifdef OMNICPP_HAS_VULKAN
  if (!device_) {
    return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::invalid_config);
  }
  for (auto& band : bands_) {
    vkResetCommandBuffer(band.buffer, 0);
  }
  return omnicpp::core::Result<void>::ok();
#else
  return omnicpp::core::Result<void>::error(omnicpp::core::RuntimeError::vulkan_not_available);
#endif
}

} // namespace omnicpp::render
