# Vulkan Rendering Stack

Modern Vulkan 1.3-first rendering layer, Qt-free, verified on hardware (RTX 2060) under the
Khronos validation layer with zero diagnostics, and exercised in CI on Mesa lavapipe
(software GPU).

## Layers

| Layer | Header | Purpose |
|-------|--------|---------|
| Context & feature negotiation | `engine/render/vulkan_context.hpp` | Instance, device, queues, Vulkan 1.2/1.3 feature chain |
| Swapchain | `engine/render/vulkan_swapchain.hpp` | Format/present-mode selection, recreation |
| Render pass | `engine/render/vulkan_render_pass.hpp` | Color+depth pass, framebuffers, depth resources |
| Pipeline | `engine/render/vulkan_pipeline.hpp` | SPIR-V loading, graphics pipeline, explicit layouts |
| Renderer | `engine/render/vulkan_renderer.hpp` | Frame loop, sync2 submission, timeline pacing, GPU telemetry |
| Memory allocator | `engine/render/vulkan_memory_allocator.hpp` | Block sub-allocation + staging upload ring |
| Descriptors | `engine/render/vulkan_descriptors.hpp` | SPIR-V reflection, layouts, pools, set writes |
| Render graph | `engine/render/vulkan_render_graph.hpp` | Automatic image barriers between passes |
| Parallel recorder | `engine/render/vulkan_parallel_recorder.hpp` | Multithreaded secondary command buffers |
| Offscreen target | `engine/render/vulkan_offscreen.hpp` | Headless color+depth targets with GPU readback |

## Feature Negotiation

`VulkanContext` queries `VkPhysicalDeviceVulkan13Features` and
`VkPhysicalDeviceVulkan12Features` in one chained `vkGetPhysicalDeviceFeatures2` call and
enables, only when the device advertises them:

- **Synchronization 2** (1.3) — unlocks `vkQueueSubmit2` and stage/access-scoped submit infos
- **Timeline semaphores** (1.2) — unlocks fence-free CPU/GPU frame pacing

Introspection: `has_synchronization2()`, `has_timeline_semaphores()`, and
`timestamp_period_ns` (device limits, for GPU timestamp conversion).

Extensions such as `VK_KHR_synchronization2` are added to the device only when the
corresponding feature is actually enabled.

## Frame Submission

`VulkanRenderer::submit_frame()` has two paths selected by negotiated features:

- **Sync2 path**: `vkQueueSubmit2` with `VkCommandBufferSubmitInfo` /
  `VkSemaphoreSubmitInfo`, resolving the function pointer through the device.
- **Legacy path**: `vkQueueSubmit` with a `VkTimelineSemaphoreSubmitInfo` pNext chain when
  timeline values are signaled.

Both paths preserve per-image render-finished semaphore ownership.

### Timeline Frame Pacing

When `set_timeline_pacing(true)` is requested and timeline semaphores are negotiated:

- One global timeline semaphore signals a monotonic frame counter on every submit
  (`frame_counter()`).
- `begin_frame()` throttles CPU/GPU in-flight frames by waiting on timeline value
  `frame_counter − slots + 1` (no binary fences involved).
- Per-image reuse waits on the exact timeline value that last rendered that image.
- The per-frame fence is omitted entirely in this mode; the legacy fence path remains the
  fallback for devices without timeline semaphores.

### GPU Timestamp Telemetry

Timestamp query pools bracket the offscreen render pass; durations convert to nanoseconds
via `timestampPeriod`. On the RTX 2060 the 640×480 triangle pass measures ~6 µs.

## Memory: Allocator + Upload Ring

`VulkanMemoryAllocator` replaces one-`vkAllocateMemory`-per-resource with:

- **Block sub-allocation**: 64 MiB device-local / 16 MiB host-visible blocks carved by
  first-fit with alignment-aware free ranges, leading-pad reuse, and neighbor coalescing.
- **Memory-type selection**: best-match against `VkPhysicalDeviceMemoryProperties`, with
  block selection filtered by each resource's required `memoryTypeBits` (multi-heap GPUs).
- **Persistent mapping**: host-visible blocks return a stable `mapped` pointer — no
  per-object `vkMapMemory`.
- **API**: `create_buffer()`, `bind_image()`, `destroy_allocation()`, `stats()`.

`VulkanUploadRing` is a single persistently-mapped `TRANSFER_SRC` staging buffer used as a
ring: `acquire()` → CPU write → `record_copy()` → `submit()`. Each submit's fence guards
exactly the ranges handed out since the previous submit; wrap-around retires in-flight
fences for the tail region before reusing bytes.

## Descriptors + SPIR-V Reflection

`reflect_spirv_resources()` is a dependency-free SPIR-V parser that extracts set/binding/
type/count for UBOs, SSBOs, samplers, combined image samplers, storage images, and input
attachments. Stage flags derive from `OpEntryPoint` execution models and merge across
modules.

`VulkanDescriptorManager` builds layouts from reflected bindings, sizes its pool
automatically, allocates sets, and applies buffer/image writes.

## Render Graph

`compile_render_graph()` / `execute_render_graph()`:

- Passes declare color/depth attachments with explicit usage timelines.
- The compiler tracks per-image layout/access/stage state and emits exactly the required
  `VkImageMemoryBarrier`s between consecutive passes.
- The executor inserts barriers and records each pass via a callback in one command buffer.

## Multithreaded Command Recording

`VulkanParallelRecorder` splits the frame into horizontal bands and records one secondary
command buffer per band on worker threads, using per-thread command pools (Vulkan
external-sync rules) and correct `RENDER_PASS_CONTINUE` inheritance info. Secondaries
execute via `vkCmdExecuteCommands` inside one primary render pass.

## Swapchain Recreation

`VulkanSwapchain::recreate()` rebuilds image views safely;
`VulkanRenderer::resync_for_swapchain()` rebinds the swapchain and render pass, rebuilds
per-image semaphores, and resets timeline history while the device is idle. Mid-frame
resync is rejected.

## Validation Gate

Hardware tests run under the Khronos validation layer, forced via
`VK_LOADER_LAYERS_ENABLE=VK_LAYER_KHRONOS_validation` when
`OMNICPP_VULKAN_VALIDATION_TESTS=ON`. Any diagnostic fails the suite.

Key hardware tests (`tests/unit/test_rendering.cpp`):

- `VulkanHardware.SwapchainRecreationStress`
- `VulkanHardware.OffscreenTriangleReadback`
- `VulkanHardware.HeadlessSwapchainAndRenderSubmission`
- `VulkanHardware.DescriptorReflectionAndUboRender`
- `VulkanHardware.RenderGraphTwoPassBarriersAndRender`
- `VulkanHardware.ParallelRecorderMultithreadedBands`
- Allocator/upload-ring sub-allocation and byte-verification tests

Tests skip gracefully when no Vulkan loader, display, or compiled shaders are present, so
the same binary runs on GPU-less CI machines and full-GPU workstations.

## Building

```sh
# Configure (requires Vulkan SDK or distro packages: libvulkan-dev, glslc or glslangValidator)
cmake --preset vulkan-validation
cmake --build build/vulkan-validation
ctest --test-dir build/vulkan-validation --output-on-failure
```

Shader compilation prefers `glslc` (shaderc) and falls back to
`glslangValidator -V` where glslc is not packaged.

CI runs this exact preset on Mesa lavapipe (software GPU) with the validation layer
enabled — see `.github/workflows/test.yml`.

## Remaining Roadmap

1. **Cross-vendor hardware runs** (AMD/Intel/mobile) — requires physical hardware or a
   GPU CI service; the lavapipe CI job covers driver-independent correctness.
2. Bindless descriptor indexing (EXT_descriptor_indexing) on top of the reflection layer.
3. Async-compute queue support in the render graph (compute passes + transfer passes).
