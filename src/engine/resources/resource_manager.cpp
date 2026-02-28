/**
 * @file resource_manager.cpp
 * @brief Resource management implementation
 */

#include "engine/resources/ResourceManager.hpp"
#include <mutex>
#include <unordered_map>
#include "engine/logging/Log.hpp"

namespace omnicpp {
namespace resources {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct ResourceManager::Impl {
    struct ResourceInfo {
      std::string path;
      ResourceType type;
    };
    std::unordered_map<std::string, ResourceInfo> resources;
    std::mutex mutex;
    bool initialized{ false };
  };

  ResourceManager::ResourceManager () : m_impl (std::make_unique<Impl> ()) {
  }

  ResourceManager::~ResourceManager () {
    shutdown ();
  }

  ResourceManager::ResourceManager (ResourceManager&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
  }

  ResourceManager& ResourceManager::operator= (ResourceManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool ResourceManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      omnicpp::log::warn("ResourceManager: Already initialized");
      return true;
    }

    m_impl->resources.clear ();
    m_impl->initialized = true;

    omnicpp::log::info("ResourceManager: Initialized");
    return true;
  }

  void ResourceManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->resources.clear ();
    m_impl->initialized = false;

    omnicpp::log::info("ResourceManager: Shutdown");
  }

  void ResourceManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update resource state here
  }

  bool ResourceManager::load_resource (const std::string& name, const std::string& path,
       ResourceType type) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      omnicpp::log::error("ResourceManager: Not initialized, cannot load resource: {}", name);
      return false;
    }

    Impl::ResourceInfo info{ path, type };
    m_impl->resources[name] = info;
    omnicpp::log::debug("ResourceManager: Loaded resource '{}' from '{}' (type: {})", name, path, static_cast<int>(type));
    return true;
  }

  bool ResourceManager::unload_resource (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      omnicpp::log::error("ResourceManager: Not initialized, cannot unload resource: {}", name);
      return false;
    }

    auto it = m_impl->resources.find (name);
    if (it != m_impl->resources.end ()) {
      m_impl->resources.erase (it);
      omnicpp::log::debug("ResourceManager: Unloaded resource '{}'", name);
      return true;
    }
    omnicpp::log::warn("ResourceManager: Resource '{}' not found", name);
    return false;
  }

  bool ResourceManager::has_resource (const std::string& name) const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->resources.find (name) != m_impl->resources.end ();
  }

} // namespace resources
} // namespace omnicpp
