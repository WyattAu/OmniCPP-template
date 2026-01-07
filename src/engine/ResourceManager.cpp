/**
 * @file ResourceManager.cpp
 * @brief Stub implementation of resource manager subsystem
 * @version 1.0.0
 */

#include "engine/IResourceManager.hpp"

namespace omnicpp {

class ResourceManagerStub : public IResourceManager {
public:
    ResourceManagerStub() = default;
    ~ResourceManagerStub() override = default;

    bool initialize() override {
        return true;
    }

    void shutdown() override {
    }

    uint32_t load_resource(const char* file_path, ResourceType type) override {
        (void)file_path;
        (void)type;
        return 0;
    }

    void unload_resource(uint32_t resource_id) override {
        (void)resource_id;
    }

    void* get_resource(uint32_t resource_id) override {
        (void)resource_id;
        return nullptr;
    }

    bool reload_resource(uint32_t resource_id) override {
        (void)resource_id;
        return true;
    }

    void set_search_path(const char* path) override {
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
