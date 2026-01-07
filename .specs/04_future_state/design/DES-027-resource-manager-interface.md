# DES-027: Resource Manager Interface

## Overview
Defines resource manager interface for OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_RESOURCE_MANAGER_INTERFACE_H
#define OMNICPP_RESOURCE_MANAGER_INTERFACE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <unordered_map>

namespace omnicpp {
namespace engine {

// Forward declarations
class IResource;
class IResourceLoader;
class IResourceCache;

// Resource type
enum class ResourceType {
    TEXTURE,
    MESH,
    SHADER,
    MATERIAL,
    AUDIO,
    FONT,
    SCRIPT,
    DATA,
    CUSTOM
};

// Resource state
enum class ResourceState {
    UNLOADED,
    LOADING,
    LOADED,
    UNLOADING,
    ERROR
};

// Resource loading mode
enum class LoadingMode {
    SYNCHRONOUS,
    ASYNCHRONOUS,
    LAZY
};

// Resource configuration
struct ResourceConfig {
    size_t cache_size;
    int max_resources;
    bool enable_async_loading;
    int async_threads;
    bool enable_compression;
    bool enable_streaming;
    size_t streaming_chunk_size;

    ResourceConfig()
        : cache_size(256 * 1024 * 1024) // 256 MB
        , max_resources(1000)
        , enable_async_loading(true)
        , async_threads(4)
        , enable_compression(false)
        , enable_streaming(false)
        , streaming_chunk_size(1024 * 1024) // 1 MB
    {}
};

// Resource statistics
struct ResourceStats {
    uint32_t total_resources;
    uint32_t loaded_resources;
    uint32_t loading_resources;
    uint32_t error_resources;
    size_t memory_usage;
    size_t cache_usage;
    double load_time;
    uint32_t cache_hits;
    uint32_t cache_misses;

    ResourceStats()
        : total_resources(0)
        , loaded_resources(0)
        , loading_resources(0)
        , error_resources(0)
        , memory_usage(0)
        , cache_usage(0)
        , load_time(0.0)
        , cache_hits(0)
        , cache_misses(0)
    {}
};

// Resource metadata
struct ResourceMetadata {
    std::string name;
    std::string path;
    ResourceType type;
    size_t size;
    uint64_t last_modified;
    std::unordered_map<std::string, std::string> custom_data;

    ResourceMetadata()
        : type(ResourceType::CUSTOM)
        , size(0)
        , last_modified(0)
    {}
};

// Resource manager interface
class IResourceManager {
public:
    virtual ~IResourceManager() = default;

    // Initialization
    virtual bool initialize(const ResourceConfig& config) = 0;
    virtual void shutdown() = 0;

    // Update
    virtual void update(double delta_time) = 0;

    // Resource loading
    virtual uint32_t load_resource(const std::string& path, ResourceType type, LoadingMode mode = LoadingMode::SYNCHRONOUS) = 0;
    virtual void unload_resource(uint32_t resource_id) = 0;
    virtual void reload_resource(uint32_t resource_id) = 0;

    // Resource access
    virtual IResource* get_resource(uint32_t resource_id) = 0;
    virtual const IResource* get_resource(uint32_t resource_id) const = 0;
    virtual IResource* get_resource_by_name(const std::string& name) = 0;
    virtual const IResource* get_resource_by_name(const std::string& name) const = 0;

    // Resource queries
    virtual bool has_resource(uint32_t resource_id) const = 0;
    virtual bool has_resource_by_name(const std::string& name) const = 0;
    virtual std::vector<uint32_t> get_resources_by_type(ResourceType type) const = 0;
    virtual std::vector<uint32_t> get_all_resources() const = 0;

    // Resource paths
    virtual void add_resource_path(const std::string& path) = 0;
    virtual void remove_resource_path(const std::string& path) = 0;
    virtual std::vector<std::string> get_resource_paths() const = 0;

    // Resource loaders
    virtual void register_loader(ResourceType type, std::unique_ptr<IResourceLoader> loader) = 0;
    virtual void unregister_loader(ResourceType type) = 0;
    virtual IResourceLoader* get_loader(ResourceType type) const = 0;

    // Resource cache
    virtual void clear_cache() = 0;
    virtual void clear_cache_by_type(ResourceType type) = 0;
    virtual size_t get_cache_size() const = 0;
    virtual size_t get_cache_usage() const = 0;

    // Resource callbacks
    using ResourceCallback = std::function<void(uint32_t resource_id, ResourceState state)>;
    virtual void set_resource_callback(ResourceCallback callback) = 0;
    virtual void clear_resource_callback() = 0;

    // Statistics
    virtual const ResourceStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Configuration
    virtual const ResourceConfig& get_config() const = 0;
    virtual void set_config(const ResourceConfig& config) = 0;
};

// Resource interface
class IResource {
public:
    virtual ~IResource() = default;

    virtual uint32_t get_id() const = 0;
    virtual const std::string& get_name() const = 0;
    virtual const std::string& get_path() const = 0;
    virtual ResourceType get_type() const = 0;
    virtual ResourceState get_state() const = 0;
    virtual const ResourceMetadata& get_metadata() const = 0;

    virtual void set_name(const std::string& name) = 0;
    virtual void set_path(const std::string& path) = 0;
    virtual void set_state(ResourceState state) = 0;
    virtual void set_metadata(const ResourceMetadata& metadata) = 0;

    virtual size_t get_size() const = 0;
    virtual void* get_data() = 0;
    virtual const void* get_data() const = 0;

    virtual bool is_loaded() const = 0;
    virtual bool is_loading() const = 0;
    virtual bool is_error() const = 0;

    virtual int get_reference_count() const = 0;
    virtual void add_reference() = 0;
    virtual void remove_reference() = 0;
};

// Resource loader interface
class IResourceLoader {
public:
    virtual ~IResourceLoader() = default;

    virtual ResourceType get_type() const = 0;
    virtual std::vector<std::string> get_supported_extensions() const = 0;

    virtual bool can_load(const std::string& path) const = 0;
    virtual std::unique_ptr<IResource> load(const std::string& path) = 0;
    virtual bool save(const std::string& path, const IResource* resource) const = 0;

    virtual ResourceMetadata get_metadata(const std::string& path) const = 0;
};

// Resource cache interface
class IResourceCache {
public:
    virtual ~IResourceCache() = default;

    virtual void add_resource(uint32_t resource_id, std::unique_ptr<IResource> resource) = 0;
    virtual void remove_resource(uint32_t resource_id) = 0;
    virtual IResource* get_resource(uint32_t resource_id) = 0;
    virtual const IResource* get_resource(uint32_t resource_id) const = 0;

    virtual bool has_resource(uint32_t resource_id) const = 0;
    virtual void clear() = 0;
    virtual size_t get_size() const = 0;
    virtual size_t get_usage() const = 0;

    virtual void set_max_size(size_t max_size) = 0;
    virtual size_t get_max_size() const = 0;

    virtual void evict_lru() = 0;
    virtual void evict_by_type(ResourceType type) = 0;
};

// Resource manager factory
class IResourceManagerFactory {
public:
    virtual ~IResourceManagerFactory() = default;

    virtual std::unique_ptr<IResourceManager> create_resource_manager() = 0;
    virtual void destroy_resource_manager(std::unique_ptr<IResourceManager> resource_manager) = 0;
};

// Texture resource
class TextureResource : public IResource {
public:
    virtual int get_width() const = 0;
    virtual int get_height() const = 0;
    virtual int get_channels() const = 0;
    virtual int get_bits_per_pixel() const = 0;

    virtual void set_data(const void* data, size_t size) = 0;
    virtual void get_data(void* data, size_t size) const = 0;
};

// Mesh resource
class MeshResource : public IResource {
public:
    virtual size_t get_vertex_count() const = 0;
    virtual size_t get_index_count() const = 0;
    virtual size_t get_vertex_size() const = 0;
    virtual size_t get_index_size() const = 0;

    virtual void set_vertex_data(const void* data, size_t size) = 0;
    virtual void set_index_data(const void* data, size_t size) = 0;
    virtual void get_vertex_data(void* data, size_t size) const = 0;
    virtual void get_index_data(void* data, size_t size) const = 0;
};

// Shader resource
class ShaderResource : public IResource {
public:
    virtual const std::string& get_vertex_source() const = 0;
    virtual const std::string& get_fragment_source() const = 0;
    virtual const std::string& get_geometry_source() const = 0;
    virtual const std::string& get_compute_source() const = 0;

    virtual void set_vertex_source(const std::string& source) = 0;
    virtual void set_fragment_source(const std::string& source) = 0;
    virtual void set_geometry_source(const std::string& source) = 0;
    virtual void set_compute_source(const std::string& source) = 0;
};

// Audio resource
class AudioResource : public IResource {
public:
    virtual int get_sample_rate() const = 0;
    virtual int get_channels() const = 0;
    virtual int get_bits_per_sample() const = 0;
    virtual size_t get_duration() const = 0;

    virtual void set_data(const void* data, size_t size) = 0;
    virtual void get_data(void* data, size_t size) const = 0;
};

// Font resource
class FontResource : public IResource {
public:
    virtual int get_size() const = 0;
    virtual int get_glyph_count() const = 0;

    virtual void set_data(const void* data, size_t size) = 0;
    virtual void get_data(void* data, size_t size) const = 0;
};

// Script resource
class ScriptResource : public IResource {
public:
    virtual const std::string& get_source() const = 0;
    virtual void set_source(const std::string& source) = 0;
};

// Data resource
class DataResource : public IResource {
public:
    virtual void set_data(const void* data, size_t size) = 0;
    virtual void get_data(void* data, size_t size) const = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_RESOURCE_MANAGER_INTERFACE_H
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
- `unordered_map` - Hash map

## Related Requirements
- REQ-041: Resource Management
- REQ-042: Resource Loading

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Resource Manager Design
1. Abstract resource loading
2. Support multiple resource types
3. Efficient caching
4. Async loading support

### Resource Loading
1. Load resources from files
2. Support synchronous and async loading
3. Lazy loading support
4. Resource streaming

### Resource Caching
1. LRU cache eviction
2. Memory management
3. Cache statistics
4. Cache clearing

### Resource References
1. Reference counting
2. Automatic unloading
3. Resource sharing
4. Memory optimization

## Usage Example

```cpp
#include "resource_manager_interface.hpp"

using namespace omnicpp::engine;

int main() {
    // Create resource configuration
    ResourceConfig config;
    config.cache_size = 256 * 1024 * 1024; // 256 MB
    config.max_resources = 1000;
    config.enable_async_loading = true;
    config.async_threads = 4;

    // Create resource manager
    auto resource_manager = std::make_unique<ResourceManager>();

    // Initialize resource manager
    if (!resource_manager->initialize(config)) {
        std::cerr << "Failed to initialize resource manager" << std::endl;
        return 1;
    }

    // Add resource paths
    resource_manager->add_resource_path("textures/");
    resource_manager->add_resource_path("models/");
    resource_manager->add_resource_path("sounds/");

    // Load texture
    uint32_t texture_id = resource_manager->load_resource("textures/player.png", ResourceType::TEXTURE, LoadingMode::ASYNCHRONOUS);

    // Load mesh
    uint32_t mesh_id = resource_manager->load_resource("models/player.obj", ResourceType::MESH, LoadingMode::ASYNCHRONOUS);

    // Load audio
    uint32_t audio_id = resource_manager->load_resource("sounds/explosion.wav", ResourceType::AUDIO, LoadingMode::ASYNCHRONOUS);

    // Set resource callback
    resource_manager->set_resource_callback([](uint32_t resource_id, ResourceState state) {
        if (state == ResourceState::LOADED) {
            std::cout << "Resource " << resource_id << " loaded" << std::endl;
        } else if (state == ResourceState::ERROR) {
            std::cerr << "Resource " << resource_id << " failed to load" << std::endl;
        }
    });

    // Update resource manager
    double delta_time = 0.016; // 60 FPS
    resource_manager->update(delta_time);

    // Get resource
    IResource* texture = resource_manager->get_resource(texture_id);
    if (texture && texture->is_loaded()) {
        TextureResource* tex = static_cast<TextureResource*>(texture);
        std::cout << "Texture size: " << tex->get_width() << "x" << tex->get_height() << std::endl;
    }

    // Get statistics
    const ResourceStats& stats = resource_manager->get_stats();
    std::cout << "Loaded resources: " << stats.loaded_resources << std::endl;
    std::cout << "Cache usage: " << stats.cache_usage << " bytes" << std::endl;

    // Cleanup
    resource_manager->unload_resource(texture_id);
    resource_manager->unload_resource(mesh_id);
    resource_manager->unload_resource(audio_id);
    resource_manager->shutdown();

    return 0;
}
```
