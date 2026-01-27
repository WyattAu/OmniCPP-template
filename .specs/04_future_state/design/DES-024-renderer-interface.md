# DES-024: Renderer Interface

## Overview
Defines the renderer interface for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_RENDERER_INTERFACE_H
#define OMNICPP_RENDERER_INTERFACE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace omnicpp {
namespace engine {

// Forward declarations
class IShader;
class ITexture;
class IMesh;
class IMaterial;
class ICamera;
class ILight;

// Renderer configuration
struct RendererConfig {
    int width;
    int height;
    bool vsync;
    bool fullscreen;
    int multisample_samples;
    bool enable_shadows;
    bool enable_post_processing;
    int max_lights;

    RendererConfig()
        : width(1280)
        , height(720)
        , vsync(true)
        , fullscreen(false)
        , multisample_samples(4)
        , enable_shadows(true)
        , enable_post_processing(true)
        , max_lights(8)
    {}
};

// Render target
struct RenderTarget {
    uint32_t id;
    int width;
    int height;
    uint32_t texture_id;
    uint32_t depth_buffer_id;

    RenderTarget()
        : id(0)
        , width(0)
        , height(0)
        , texture_id(0)
        , depth_buffer_id(0)
    {}
};

// Viewport
struct Viewport {
    int x;
    int y;
    int width;
    int height;
    float min_depth;
    float max_depth;

    Viewport()
        : x(0)
        , y(0)
        , width(1280)
        , height(720)
        , min_depth(0.0f)
        , max_depth(1.0f)
    {}
};

// Scissor rect
struct ScissorRect {
    int x;
    int y;
    int width;
    int height;

    ScissorRect()
        : x(0)
        , y(0)
        , width(1280)
        , height(720)
    {}
};

// Clear flags
enum class ClearFlag {
    COLOR = 1 << 0,
    DEPTH = 1 << 1,
    STENCIL = 1 << 2,
    ALL = COLOR | DEPTH | STENCIL
};

// Primitive type
enum class PrimitiveType {
    POINTS,
    LINES,
    LINE_STRIP,
    TRIANGLES,
    TRIANGLE_STRIP,
    TRIANGLE_FAN
};

// Blend mode
enum class BlendMode {
    NONE,
    ALPHA,
    ADDITIVE,
    MULTIPLICATIVE,
    SCREEN
};

// Cull mode
enum class CullMode {
    NONE,
    FRONT,
    BACK
};

// Compare function
enum class CompareFunction {
    NEVER,
    LESS,
    EQUAL,
    LEQUAL,
    GREATER,
    NOTEQUAL,
    GEQUAL,
    ALWAYS
};

// Stencil operation
enum class StencilOperation {
    KEEP,
    ZERO,
    REPLACE,
    INCREMENT,
    DECREMENT,
    INVERT
};

// Renderer statistics
struct RendererStats {
    uint32_t draw_calls;
    uint32_t triangles_rendered;
    uint32_t vertices_rendered;
    double frame_time;
    double fps;

    RendererStats()
        : draw_calls(0)
        , triangles_rendered(0)
        , vertices_rendered(0)
        , frame_time(0.0)
        , fps(0.0)
    {}
};

// Renderer interface
class IRenderer {
public:
    virtual ~IRenderer() = default;

    // Initialization
    virtual bool initialize(const RendererConfig& config) = 0;
    virtual void shutdown() = 0;

    // Frame management
    virtual void begin_frame() = 0;
    virtual void end_frame() = 0;
    virtual void present() = 0;

    // Clear
    virtual void clear(uint32_t flags) = 0;
    virtual void clear_color(float r, float g, float b, float a) = 0;
    virtual void clear_depth(float depth) = 0;
    virtual void clear_stencil(int stencil) = 0;

    // Viewport and scissor
    virtual void set_viewport(const Viewport& viewport) = 0;
    virtual void set_scissor(const ScissorRect& scissor) = 0;
    virtual void reset_viewport() = 0;
    virtual void reset_scissor() = 0;

    // Render targets
    virtual uint32_t create_render_target(int width, int height) = 0;
    virtual void destroy_render_target(uint32_t render_target_id) = 0;
    virtual void set_render_target(uint32_t render_target_id) = 0;
    virtual void reset_render_target() = 0;

    // Shaders
    virtual uint32_t create_shader(const std::string& vertex_source, const std::string& fragment_source) = 0;
    virtual void destroy_shader(uint32_t shader_id) = 0;
    virtual void bind_shader(uint32_t shader_id) = 0;
    virtual void unbind_shader() = 0;

    // Textures
    virtual uint32_t create_texture(int width, int height, const void* data) = 0;
    virtual void destroy_texture(uint32_t texture_id) = 0;
    virtual void bind_texture(uint32_t texture_id, int slot) = 0;
    virtual void unbind_texture(int slot) = 0;

    // Meshes
    virtual uint32_t create_mesh(const void* vertices, size_t vertex_count, const void* indices, size_t index_count) = 0;
    virtual void destroy_mesh(uint32_t mesh_id) = 0;
    virtual void draw_mesh(uint32_t mesh_id, PrimitiveType primitive_type) = 0;

    // Materials
    virtual uint32_t create_material(uint32_t shader_id) = 0;
    virtual void destroy_material(uint32_t material_id) = 0;
    virtual void bind_material(uint32_t material_id) = 0;
    virtual void set_material_texture(uint32_t material_id, const std::string& name, uint32_t texture_id) = 0;
    virtual void set_material_float(uint32_t material_id, const std::string& name, float value) = 0;
    virtual void set_material_vec3(uint32_t material_id, const std::string& name, float x, float y, float z) = 0;
    virtual void set_material_vec4(uint32_t material_id, const std::string& name, float x, float y, float z, float w) = 0;
    virtual void set_material_matrix4(uint32_t material_id, const std::string& name, const float* matrix) = 0;

    // Camera
    virtual void set_camera(ICamera* camera) = 0;
    virtual ICamera* get_camera() const = 0;

    // Lights
    virtual void add_light(ILight* light) = 0;
    virtual void remove_light(ILight* light) = 0;
    virtual void clear_lights() = 0;
    virtual std::vector<ILight*> get_lights() const = 0;

    // Render state
    virtual void set_blend_mode(BlendMode mode) = 0;
    virtual void set_cull_mode(CullMode mode) = 0;
    virtual void set_depth_test(bool enabled) = 0;
    virtual void set_depth_write(bool enabled) = 0;
    virtual void set_depth_function(CompareFunction func) = 0;
    virtual void set_stencil_test(bool enabled) = 0;
    virtual void set_stencil_function(CompareFunction func, int ref, uint32_t mask) = 0;
    virtual void set_stencil_operation(StencilOperation fail, StencilOperation depth_fail, StencilOperation pass) = 0;

    // Statistics
    virtual const RendererStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Configuration
    virtual const RendererConfig& get_config() const = 0;
    virtual void set_config(const RendererConfig& config) = 0;

    // Resize
    virtual void resize(int width, int height) = 0;

    // VSync
    virtual void set_vsync(bool enabled) = 0;
    virtual bool get_vsync() const = 0;
};

// Shader interface
class IShader {
public:
    virtual ~IShader() = default;

    virtual uint32_t get_id() const = 0;
    virtual const std::string& get_vertex_source() const = 0;
    virtual const std::string& get_fragment_source() const = 0;

    virtual void bind() const = 0;
    virtual void unbind() const = 0;

    virtual void set_uniform(const std::string& name, int value) = 0;
    virtual void set_uniform(const std::string& name, float value) = 0;
    virtual void set_uniform(const std::string& name, float x, float y) = 0;
    virtual void set_uniform(const std::string& name, float x, float y, float z) = 0;
    virtual void set_uniform(const std::string& name, float x, float y, float z, float w) = 0;
    virtual void set_uniform(const std::string& name, const float* matrix) = 0;
};

// Texture interface
class ITexture {
public:
    virtual ~ITexture() = default;

    virtual uint32_t get_id() const = 0;
    virtual int get_width() const = 0;
    virtual int get_height() const = 0;

    virtual void bind(int slot) const = 0;
    virtual void unbind(int slot) const = 0;

    virtual void set_data(const void* data) = 0;
    virtual void get_data(void* data) const = 0;
};

// Mesh interface
class IMesh {
public:
    virtual ~IMesh() = default;

    virtual uint32_t get_id() const = 0;
    virtual size_t get_vertex_count() const = 0;
    virtual size_t get_index_count() const = 0;

    virtual void draw(PrimitiveType primitive_type) const = 0;

    virtual void set_vertex_data(const void* data, size_t count) = 0;
    virtual void set_index_data(const void* data, size_t count) = 0;
};

// Material interface
class IMaterial {
public:
    virtual ~IMaterial() = default;

    virtual uint32_t get_id() const = 0;
    virtual IShader* get_shader() const = 0;

    virtual void bind() const = 0;
    virtual void unbind() const = 0;

    virtual void set_texture(const std::string& name, ITexture* texture) = 0;
    virtual void set_float(const std::string& name, float value) = 0;
    virtual void set_vec3(const std::string& name, float x, float y, float z) = 0;
    virtual void set_vec4(const std::string& name, float x, float y, float z, float w) = 0;
    virtual void set_matrix4(const std::string& name, const float* matrix) = 0;
};

// Camera interface
class ICamera {
public:
    virtual ~ICamera() = default;

    virtual void set_position(float x, float y, float z) = 0;
    virtual void set_rotation(float pitch, float yaw, float roll) = 0;
    virtual void set_fov(float fov) = 0;
    virtual void set_near_plane(float near_plane) = 0;
    virtual void set_far_plane(float far_plane) = 0;
    virtual void set_aspect_ratio(float aspect_ratio) = 0;

    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void get_rotation(float& pitch, float& yaw, float& roll) const = 0;
    virtual float get_fov() const = 0;
    virtual float get_near_plane() const = 0;
    virtual float get_far_plane() const = 0;
    virtual float get_aspect_ratio() const = 0;

    virtual const float* get_view_matrix() const = 0;
    virtual const float* get_projection_matrix() const = 0;
    virtual const float* get_view_projection_matrix() const = 0;

    virtual void update() = 0;
};

// Light interface
class ILight {
public:
    virtual ~ILight() = default;

    virtual void set_position(float x, float y, float z) = 0;
    virtual void set_direction(float x, float y, float z) = 0;
    virtual void set_color(float r, float g, float b) = 0;
    virtual void set_intensity(float intensity) = 0;
    virtual void set_range(float range) = 0;
    virtual void set_spot_angle(float angle) = 0;

    virtual void get_position(float& x, float& y, float& z) const = 0;
    virtual void get_direction(float& x, float& y, float& z) const = 0;
    virtual void get_color(float& r, float& g, float& b) const = 0;
    virtual float get_intensity() const = 0;
    virtual float get_range() const = 0;
    virtual float get_spot_angle() const = 0;
};

// Renderer factory
class IRendererFactory {
public:
    virtual ~IRendererFactory() = default;

    virtual std::unique_ptr<IRenderer> create_renderer() = 0;
    virtual void destroy_renderer(std::unique_ptr<IRenderer> renderer) = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_RENDERER_INTERFACE_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects

## Related Requirements
- REQ-035: Renderer Architecture
- REQ-036: Rendering Pipeline

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Renderer Design
1. Abstract rendering API
2. Support multiple backends (OpenGL, Vulkan, DirectX)
3. Efficient resource management
4. Batch rendering support

### Resource Management
1. Create and destroy resources
2. Bind and unbind resources
3. Track resource usage
4. Handle resource errors

### Render State
1. Manage render state
2. Optimize state changes
3. Support multiple render targets
4. Handle viewport and scissor

### Performance
1. Track rendering statistics
2. Optimize draw calls
3. Support instancing
4. Batch similar draws

## Usage Example

```cpp
#include "renderer_interface.hpp"

using namespace omnicpp::engine;

int main() {
    // Create renderer configuration
    RendererConfig config;
    config.width = 1920;
    config.height = 1080;
    config.vsync = true;
    config.fullscreen = false;
    config.multisample_samples = 4;
    config.enable_shadows = true;
    config.enable_post_processing = true;
    config.max_lights = 8;

    // Create renderer
    auto renderer = std::make_unique<Renderer>();

    // Initialize renderer
    if (!renderer->initialize(config)) {
        std::cerr << "Failed to initialize renderer" << std::endl;
        return 1;
    }

    // Begin frame
    renderer->begin_frame();

    // Clear screen
    renderer->clear(static_cast<uint32_t>(ClearFlag::ALL));

    // Set viewport
    Viewport viewport;
    viewport.x = 0;
    viewport.y = 0;
    viewport.width = 1920;
    viewport.height = 1080;
    renderer->set_viewport(viewport);

    // Render scene
    // ...

    // End frame
    renderer->end_frame();

    // Present
    renderer->present();

    // Shutdown renderer
    renderer->shutdown();

    return 0;
}
```
