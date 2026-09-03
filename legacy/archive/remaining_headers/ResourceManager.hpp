#pragma once

#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

namespace omnicpp::resources {

enum class ResourceType { MESH, MATERIAL, TEXTURE, SHADER, AUDIO, SCRIPT, BINARY };

class Resource {
public:
    Resource(std::string path, ResourceType type, std::vector<std::byte> data)
        : m_path(std::move(path)), m_type(type), m_data(std::move(data)) {}
    virtual ~Resource() = default;
    [[nodiscard]] const std::string& get_path() const noexcept { return m_path; }
    [[nodiscard]] ResourceType get_type() const noexcept { return m_type; }
    [[nodiscard]] std::size_t size() const noexcept { return m_data.size(); }

private:
    std::string m_path;
    ResourceType m_type;
    std::vector<std::byte> m_data;
};

class ResourceManager {
public:
    ResourceManager() = default;
    ~ResourceManager() = default;
    ResourceManager(const ResourceManager&) = delete;
    ResourceManager& operator=(const ResourceManager&) = delete;
    ResourceManager(ResourceManager&&) noexcept = default;
    ResourceManager& operator=(ResourceManager&&) noexcept = default;

    bool initialize();
    void shutdown();
    void update();

    bool load_resource(const std::string& name, const std::string& path, ResourceType type);
    bool unload_resource(const std::string& name);
    bool has_resource(const std::string& name) const;
    Resource* get_resource(const std::string& name) const;
    void unload_all();
    [[nodiscard]] std::size_t get_resource_count() const noexcept { return m_resources.size(); }
    [[nodiscard]] std::size_t get_memory_usage() const noexcept { return m_memory_usage; }

private:
    std::unordered_map<std::string, std::unique_ptr<Resource>> m_resources;
    std::size_t m_memory_usage{0};
    bool m_initialized{false};
};

} // namespace omnicpp::resources
