/**
 * @file ResourceManager.cpp
 * @brief Stub implementation of resource manager subsystem
 * @version 1.0.0
 */

#include "engine/IResourceManager.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {

class ResourceManagerStub : public IResourceManager {
public:
    ResourceManagerStub() = default;
    ~ResourceManagerStub() override = default;

    bool initialize() override {
        omnicpp::log::info("ResourceManagerStub: Initialized");
        return true;
    }

    void shutdown() override {
        omnicpp::log::info("ResourceManagerStub: Shutdown");
    }

    uint32_t load_resource(const char* file_path, ResourceType type) override {
        omnicpp::log::debug("ResourceManagerStub: Loading resource from {} (type: {})", file_path, static_cast<int>(type));
        (void)file_path;
        (void)type;
        return 0;
    }

    void unload_resource(uint32_t resource_id) override {
        omnicpp::log::debug("ResourceManagerStub: Unloading resource {}", resource_id);
        (void)resource_id;
    }

    void* get_resource(uint32_t resource_id) override {
        (void)resource_id;
        return nullptr;
    }

    bool reload_resource(uint32_t resource_id) override {
        omnicpp::log::debug("ResourceManagerStub: Reloading resource {}", resource_id);
        (void)resource_id;
        return true;
    }

    void set_search_path(const char* path) override {
        omnicpp::log::debug("ResourceManagerStub: Setting search path to {}", path);
        (void)path;
    }

    const char* get_search_path() const override {
        return "./";
    }

    ResourceType get_resource_type(uint32_t resource_id) const override {
        (void)resource_id;
        return ResourceType::UNKNOWN;
    }
};

} // namespace omnicpp
