/**
 * @file IResourceManager.hpp
 * @brief Resource manager subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for resource loading and management.
 */

#ifndef OMNICPP_IRESOURCE_MANAGER_HPP
#define OMNICPP_IRESOURCE_MANAGER_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Resource types
 */
enum class ResourceType : uint32_t {
    TEXTURE = 0,
    MESH = 1,
    SHADER = 2,
    AUDIO = 3,
    MATERIAL = 4,
    UNKNOWN = 0xFFFFFFFF
};

/**
 * @brief Resource manager interface
 */
class IResourceManager {
public:
    virtual ~IResourceManager() = default;
    
    /**
     * @brief Initialize resource manager
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown resource manager
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Load a resource
     * 
     * @param file_path Path to resource file
     * @param type Type of resource
     * @return Resource ID, or 0 on failure
     */
    virtual uint32_t load_resource(const char* file_path, ResourceType type) = 0;
    
    /**
     * @brief Unload a resource
     * 
     * @param resource_id Resource ID to unload
     */
    virtual void unload_resource(uint32_t resource_id) = 0;
    
    /**
     * @brief Get resource by ID
     * 
     * @param resource_id Resource ID
     * @return Pointer to resource data, or nullptr if not found
     */
    virtual void* get_resource(uint32_t resource_id) = 0;
    
    /**
     * @brief Reload a resource
     * 
     * @param resource_id Resource ID to reload
     * @return True if successful, false otherwise
     */
    virtual bool reload_resource(uint32_t resource_id) = 0;
    
    /**
     * @brief Set resource search path
     * 
     * @param path Directory path to search for resources
     */
    virtual void set_search_path(const char* path) = 0;
    
    /**
     * @brief Get resource search path
     * 
     * @return Current search path
     */
    virtual const char* get_search_path() const = 0;
    
    /**
     * @brief Get resource type
     * 
     * @param resource_id Resource ID
     * @return Resource type
     */
    virtual ResourceType get_resource_type(uint32_t resource_id) const = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IRESOURCE_MANAGER_HPP
