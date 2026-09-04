#include "engine/resources/ResourceManager.hpp"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iterator>
#include <utility>

namespace omnicpp::resources {

bool ResourceManager::initialize() {
    if (m_initialized) {
        return true;
    }
    m_resources.clear();
    m_memory_usage = 0;
    m_initialized = true;
    return true;
}

void ResourceManager::shutdown() {
    unload_all();
    m_initialized = false;
}

void ResourceManager::update() {}

bool ResourceManager::load_resource(const std::string& name, const std::string& path,
                                    ResourceType type) {
    if (!m_initialized || name.empty() || path.empty() ||
        !std::filesystem::is_regular_file(path)) {
        return false;
    }

    std::ifstream input(path, std::ios::binary);
    if (!input) {
        return false;
    }
    std::vector<std::byte> data;
    input.seekg(0, std::ios::end);
    const auto size = input.tellg();
    if (size < 0) {
        return false;
    }
    data.resize(static_cast<std::size_t>(size));
    input.seekg(0, std::ios::beg);
    if (!data.empty()) {
        input.read(reinterpret_cast<char*>(data.data()), static_cast<std::streamsize>(data.size()));
        if (!input) {
            return false;
        }
    }

    unload_resource(name);
    m_memory_usage += data.size();
    m_resources.emplace(name, std::make_unique<Resource>(path, type, std::move(data)));
    return true;
}

bool ResourceManager::unload_resource(const std::string& name) {
    const auto it = m_resources.find(name);
    if (it == m_resources.end()) {
        return false;
    }
    m_memory_usage -= it->second->size();
    m_resources.erase(it);
    return true;
}

bool ResourceManager::has_resource(const std::string& name) const {
    return m_resources.find(name) != m_resources.end();
}

Resource* ResourceManager::get_resource(const std::string& name) const {
    const auto it = m_resources.find(name);
    return it == m_resources.end() ? nullptr : it->second.get();
}

void ResourceManager::unload_all() {
    m_resources.clear();
    m_memory_usage = 0;
}

} // namespace omnicpp::resources
