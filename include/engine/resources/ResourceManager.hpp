/**
 * @file ResourceManager.hpp
 * @brief Resource manager for loading and caching assets
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <vector>
#include <cstdint>

namespace omnicpp {
namespace resources {

// Forward declarations
class Mesh;
class Material;
class Texture;
class Shader;

/**
 * @brief Resource type enumeration
 */
enum class ResourceType {
    MESH,
    MATERIAL,
    TEXTURE,
    SHADER,
    AUDIO,
    SCRIPT
};

/**
 * @brief Base resource class
 */
class Resource {
public:
    virtual ~Resource() = default;
    virtual ResourceType get_type() const = 0;
    virtual const std::string& get_path() const = 0;
    virtual uint32_t get_ref_count() const = 0;
    virtual void add_ref() = 0;
    virtual void release() = 0;
};

/**
 * @brief Resource manager for loading and caching assets
 * 
 * Manages loading, caching, and cleanup of game resources.
 */
class ResourceManager {
public:
    /**
     * @brief Construct a new Resource Manager object
     */
    ResourceManager() = default;

    /**
     * @brief Destroy the Resource Manager object
     */
    ~ResourceManager();

    // Disable copying
    ResourceManager(const ResourceManager&) = delete;
    ResourceManager& operator=(const ResourceManager&) = delete;

    // Enable moving
    ResourceManager(ResourceManager&&) noexcept = default;
    ResourceManager& operator=(ResourceManager&&) noexcept = default;

    /**
     * @brief Initialize resource manager
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown resource manager
     */
    void shutdown();

    /**
     * @brief Load a mesh from file
     * @param path Path to mesh file
     * @return Mesh* Pointer to loaded mesh, or nullptr if failed
     */
    Mesh* load_mesh(const std::string& path);

    /**
     * @brief Load a material from file
     * @param path Path to material file
     * @return Material* Pointer to loaded material, or nullptr if failed
     */
    Material* load_material(const std::string& path);

    /**
     * @brief Load a texture from file
     * @param path Path to texture file
     * @return Texture* Pointer to loaded texture, or nullptr if failed
     */
    Texture* load_texture(const std::string& path);

    /**
     * @brief Load a shader from file
     * @param path Path to shader file
     * @return Shader* Pointer to loaded shader, or nullptr if failed
     */
    Shader* load_shader(const std::string& path);

    /**
     * @brief Unload a resource
     * @param path Path to resource
     */
    void unload_resource(const std::string& path);

    /**
     * @brief Unload all resources
     */
    void unload_all();

    /**
     * @brief Get resource by path
     * @param path Path to resource
     * @return Resource* Pointer to resource, or nullptr if not found
     */
    Resource* get_resource(const std::string& path) const;

    /**
     * @brief Get loaded resource count
     * @return size_t The number of loaded resources
     */
    size_t get_resource_count() const { return m_resources.size(); }

    /**
     * @brief Get memory usage in bytes
     * @return size_t The memory usage
     */
    size_t get_memory_usage() const { return m_memory_usage; }

private:
    /**
     * @brief Add resource to cache
     * @param path Path to resource
     * @param resource Pointer to resource
     */
    void add_resource(const std::string& path, Resource* resource);

    /**
     * @brief Remove resource from cache
     * @param path Path to resource
     */
    void remove_resource(const std::string& path);

private:
    std::unordered_map<std::string, std::unique_ptr<Resource>> m_resources;
    size_t m_memory_usage = 0;
};

} // namespace resources
} // namespace omnicpp
