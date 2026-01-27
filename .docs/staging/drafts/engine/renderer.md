# Renderer Reference

The renderer subsystem handles all graphics operations using the Vulkan API. This reference documents the [`IRenderer`](include/engine/IRenderer.hpp:19) interface and the [`VulkanRenderer`](include/engine/render/VulkanRenderer.hpp:26) implementation.

## IRenderer Interface

The [`IRenderer`](include/engine/IRenderer.hpp:19) interface defines the contract for all renderer implementations:

```cpp
namespace omnicpp {

class IRenderer {
public:
    virtual ~IRenderer() = default;

    virtual bool initialize() = 0;
    virtual void shutdown() = 0;
    virtual bool begin_frame() = 0;
    virtual void end_frame() = 0;
    virtual uint32_t get_frame_number() const = 0;
};

} // namespace omnicpp
```

### Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| [`initialize()`](include/engine/IRenderer.hpp:28) | `bool` | Initialize the renderer. Returns `true` on success. |
| [`shutdown()`](include/engine/IRenderer.hpp:33) | `void` | Shutdown the renderer and release resources. |
| [`begin_frame()`](include/engine/IRenderer.hpp:40) | `bool` | Begin a new frame. Returns `true` on success. |
| [`end_frame()`](include/engine/IRenderer.hpp:45) | `void` | End the current frame and present to screen. |
| [`get_frame_number()`](include/engine/IRenderer.hpp:52) | `uint32_t` | Get the current frame number. |

## VulkanRenderer Implementation

The [`VulkanRenderer`](include/engine/render/VulkanRenderer.hpp:26) class provides a Vulkan-based renderer implementation:

```cpp
namespace omnicpp {
namespace render {

class VulkanRenderer : public IRenderer {
public:
    VulkanRenderer();
    ~VulkanRenderer() override;

    bool initialize() override;
    void shutdown() override;
    bool begin_frame() override;
    void end_frame() override;
    uint32_t get_frame_number() const override;

    // Vulkan-specific accessors
    VkInstance get_instance() const;
    VkPhysicalDevice get_physical_device() const;
    VkDevice get_device() const;
    VkQueue get_graphics_queue() const;
    VkQueue get_present_queue() const;
    VkCommandPool get_command_pool() const;
    RenderPipeline* get_render_pipeline() const;
    ShaderManager* get_shader_manager() const;
    SwapChain* get_swap_chain() const;
    bool is_initialized() const;

private:
    bool create_instance();
    bool setup_debug_messenger();
    bool pick_physical_device();
    bool create_logical_device();
    bool create_swap_chain();
    bool create_command_pool();
    bool create_render_pipeline();
    bool create_shader_manager();

private:
    VkInstance m_instance = VK_NULL_HANDLE;
    VkDebugUtilsMessengerEXT m_debug_messenger = VK_NULL_HANDLE;
    VkPhysicalDevice m_physical_device = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    VkQueue m_graphics_queue = VK_NULL_HANDLE;
    VkQueue m_present_queue = VK_NULL_HANDLE;
    VkCommandPool m_command_pool = VK_NULL_HANDLE;

    std::unique_ptr<RenderPipeline> m_render_pipeline;
    std::unique_ptr<ShaderManager> m_shader_manager;
    std::unique_ptr<SwapChain> m_swap_chain;

    bool m_initialized = false;
    bool m_enable_validation_layers = true;
};

} // namespace render
} // namespace omnicpp
```

### Vulkan-Specific Accessors

| Method | Return Type | Description |
|--------|-------------|-------------|
| [`get_instance()`](include/engine/render/VulkanRenderer.hpp:71) | `VkInstance` | Get the Vulkan instance handle. |
| [`get_physical_device()`](include/engine/render/VulkanRenderer.hpp:77) | `VkPhysicalDevice` | Get the physical device handle. |
| [`get_device()`](include/engine/render/VulkanRenderer.hpp:83) | `VkDevice` | Get the logical device handle. |
| [`get_graphics_queue()`](include/engine/render/VulkanRenderer.hpp:89) | `VkQueue` | Get the graphics queue handle. |
| [`get_present_queue()`](include/engine/render/VulkanRenderer.hpp:95) | `VkQueue` | Get the present queue handle. |
| [`get_command_pool()`](include/engine/render/VulkanRenderer.hpp:101) | `VkCommandPool` | Get the command pool handle. |
| [`get_render_pipeline()`](include/engine/render/VulkanRenderer.hpp:107) | `RenderPipeline*` | Get the render pipeline object. |
| [`get_shader_manager()`](include/engine/render/VulkanRenderer.hpp:113) | `ShaderManager*` | Get the shader manager object. |
| [`get_swap_chain()`](include/engine/render/VulkanRenderer.hpp:119) | `SwapChain*` | Get the swap chain object. |
| [`is_initialized()`](include/engine/render/VulkanRenderer.hpp:125) | `bool` | Check if the renderer is initialized. |

## RenderPipeline

The [`RenderPipeline`](include/engine/render/RenderPipeline.hpp:24) class manages the graphics pipeline state:

```cpp
namespace omnicpp {
namespace render {

class RenderPipeline {
public:
    RenderPipeline(VkDevice device,
                 VkExtent2D swap_chain_extent,
                 ShaderManager* shader_manager);
    ~RenderPipeline();

    VkPipelineLayout get_pipeline_layout() const;
    VkPipeline get_pipeline() const;
    VkRenderPass get_render_pass() const;
    void recreate(VkExtent2D new_extent);

private:
    bool create_render_pass();
    bool create_pipeline_layout();
    bool create_graphics_pipeline();
    void cleanup();

private:
    VkDevice m_device = VK_NULL_HANDLE;
    VkExtent2D m_swap_chain_extent;
    ShaderManager* m_shader_manager = nullptr;

    VkPipelineLayout m_pipeline_layout = VK_NULL_HANDLE;
    VkPipeline m_pipeline = VK_NULL_HANDLE;
    VkRenderPass m_render_pass = VK_NULL_HANDLE;
};

} // namespace render
} // namespace omnicpp
```

### RenderPipeline Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| [`get_pipeline_layout()`](include/engine/render/RenderPipeline.hpp:53) | `VkPipelineLayout` | Get the pipeline layout handle. |
| [`get_pipeline()`](include/engine/render/RenderPipeline.hpp:59) | `VkPipeline` | Get the graphics pipeline handle. |
| [`get_render_pass()`](include/engine/render/RenderPipeline.hpp:65) | `VkRenderPass` | Get the render pass handle. |
| [`recreate()`](include/engine/render/RenderPipeline.hpp:71) | `void` | Recreate the pipeline (e.g., after window resize). |

## ShaderManager

The [`ShaderManager`](include/engine/render/ShaderManager.hpp:30) class handles shader loading and management:

```cpp
namespace omnicpp {
namespace render {

struct ShaderModule {
    VkShaderModule module = VK_NULL_HANDLE;
    std::string entry_point = "main";
};

class ShaderManager {
public:
    explicit ShaderManager(VkDevice device);
    ~ShaderManager();

    ShaderModule load_shader(const std::string& filename,
                        const std::string& entry_point = "main");
    VkPipelineShaderStageCreateInfo create_shader_stage_info(
        const ShaderModule& module,
        VkShaderStageFlagBits stage);
    VkDevice get_device() const;

private:
    std::vector<char> read_shader_file(const std::string& filename);
    VkShaderModule create_shader_module(const std::vector<char>& code);

private:
    VkDevice m_device = VK_NULL_HANDLE;
    std::unordered_map<std::string, ShaderModule> m_shaders;
};

} // namespace render
} // namespace omnicpp
```

### ShaderManager Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| [`load_shader()`](include/engine/render/ShaderManager.hpp:57) | `ShaderModule` | Load a shader from a SPIR-V file. |
| [`create_shader_stage_info()`](include/engine/render/ShaderManager.hpp:66) | `VkPipelineShaderStageCreateInfo` | Create shader stage create info for pipeline. |
| [`get_device()`](include/engine/render/ShaderManager.hpp:74) | `VkDevice` | Get the Vulkan device handle. |

## Rendering Pipeline

The rendering pipeline follows this sequence:

```mermaid
sequenceDiagram
    participant Game
    participant Renderer
    participant Pipeline
    participant SwapChain
    participant GPU

    Game->>Renderer: begin_frame()
    Renderer->>SwapChain: Acquire next image
    SwapChain-->>Renderer: Image index
    Renderer->>Pipeline: Begin render pass
    Pipeline->>GPU: Record commands
    GPU-->>Pipeline: Commands recorded
    Pipeline->>Renderer: End render pass
    Renderer->>SwapChain: Present image
    SwapChain->>GPU: Present to screen
    GPU-->>Renderer: Present complete
    Renderer-->>Game: Frame complete
```

## Code Examples

### Basic Rendering Setup

```cpp
#include "engine/Engine.hpp"
#include "engine/render/VulkanRenderer.hpp"

int main() {
    // Create renderer
    auto renderer = std::make_unique<omnicpp::render::VulkanRenderer>();

    // Configure engine
    omnicpp::EngineConfig config{};
    config.renderer = renderer.get();

    // Create engine
    omnicpp::IEngine* engine = omnicpp::create_engine(config);
    if (!engine) {
        return -1;
    }

    // Game loop
    while (running) {
        float delta_time = calculate_delta_time();

        // Update game logic
        engine->update(delta_time);

        // Render frame
        engine->render();
    }

    // Cleanup
    omnicpp::destroy_engine(engine);
    return 0;
}
```

### Loading a Custom Shader

```cpp
#include "engine/render/VulkanRenderer.hpp"
#include "engine/render/ShaderManager.hpp"

void load_custom_shader(omnicpp::render::VulkanRenderer* renderer) {
    auto* shader_manager = renderer->get_shader_manager();

    // Load vertex shader
    auto vertex_shader = shader_manager->load_shader(
        "shaders/vert.spv",
        "main"
    );

    // Load fragment shader
    auto fragment_shader = shader_manager->load_shader(
        "shaders/frag.spv",
        "main"
    );

    // Create shader stage info
    auto vertex_stage = shader_manager->create_shader_stage_info(
        vertex_shader,
        VK_SHADER_STAGE_VERTEX_BIT
    );

    auto fragment_stage = shader_manager->create_shader_stage_info(
        fragment_shader,
        VK_SHADER_STAGE_FRAGMENT_BIT
    );

    // Use stages in pipeline creation...
}
```

### Handling Window Resize

```cpp
#include "engine/render/VulkanRenderer.hpp"

void on_window_resize(omnicpp::render::VulkanRenderer* renderer,
                 int width, int height) {
    auto* pipeline = renderer->get_render_pipeline();

    // Recreate pipeline with new extent
    VkExtent2D new_extent{static_cast<uint32_t>(width),
                           static_cast<uint32_t>(height)};
    pipeline->recreate(new_extent);
}
```

## Vulkan Requirements

### Minimum Requirements

- **Vulkan SDK**: Version 1.3 or higher
- **GPU**: Vulkan-compatible graphics card
- **Validation Layers**: VK_LAYER_KHRONOS_validation (optional but recommended)
- **Extensions**: VK_KHR_swapchain, VK_KHR_surface

### Platform-Specific Requirements

| Platform | Additional Requirements |
|----------|----------------------|
| **Windows** | Vulkan SDK for Windows |
| **Linux** | Vulkan SDK for Linux, X11 or Wayland |
| **WASM** | WebGPU backend (experimental) |

### Build Configuration

Enable Vulkan support in CMake:

```cmake
# From CMakeLists.txt
option(OMNICPP_USE_VULKAN "Use Vulkan graphics API" ON)

if(OMNICPP_USE_VULKAN)
    find_package(Vulkan)

    if(NOT Vulkan_FOUND)
        message(WARNING "Vulkan not found, Vulkan support disabled")
        set(OMNICPP_USE_VULKAN OFF)
    endif()
endif()
```

## Troubleshooting

### Vulkan Instance Creation Fails

**Symptom**: [`create_instance()`](include/engine/render/VulkanRenderer.hpp:132) returns `false`

**Possible causes**:
- Vulkan SDK not installed
- Vulkan loader not found
- Missing required extensions

**Solution**: Install Vulkan SDK and verify `VK_LAYER_PATH` environment variable.

### Physical Device Selection Fails

**Symptom**: [`pick_physical_device()`](include/engine/render/VulkanRenderer.hpp:144) returns `false`

**Possible causes**:
- No Vulkan-compatible GPU
- GPU doesn't support required features
- GPU doesn't support required extensions

**Solution**: Check GPU compatibility and ensure drivers are up to date.

### Swap Chain Creation Fails

**Symptom**: [`create_swap_chain()`](include/engine/render/VulkanRenderer.hpp:156) returns `false`

**Possible causes**:
- Invalid surface format
- Insufficient memory
- Window not properly created

**Solution**: Check window creation and surface format support.

### Shader Loading Fails

**Symptom**: [`load_shader()`](include/engine/render/ShaderManager.hpp:57) returns invalid module

**Possible causes**:
- Shader file not found
- Invalid SPIR-V bytecode
- Wrong entry point name

**Solution**: Verify shader compilation and file paths.

## Related Documentation

- [Engine Overview](index.md) - High-level engine architecture
- [Subsystems Guide](subsystems.md) - Subsystem interaction
- [Input Manager Reference](input-manager.md) - Input handling API
- [Resource Manager Reference](resource-manager.md) - Asset loading API
