/**
 * @file resource_manager.hpp
 * @brief Resource management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Resources {

  /**
   * @brief Resource type enumeration
   */
  enum class ResourceType : uint32_t { Unknown = 0, Texture, Mesh, Shader, Audio, Font, Data };

  /**
   * @brief Resource manager class
   */
  class ResourceManager {
  public:
    ResourceManager ();
    ~ResourceManager ();

    ResourceManager (const ResourceManager&) = delete;
    ResourceManager& operator= (const ResourceManager&) = delete;

    ResourceManager (ResourceManager&&) noexcept;
    ResourceManager& operator= (ResourceManager&&) noexcept;

    bool initialize ();
    void shutdown ();
    void update ();

    bool load_resource (const std::string& name, const std::string& path, ResourceType type);
    bool unload_resource (const std::string& name);
    bool has_resource (const std::string& name) const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Resources
