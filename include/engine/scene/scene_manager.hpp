/**
 * @file scene_manager.hpp
 * @brief Scene management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Scene {

  /**
   * @brief Scene manager class
   */
  class SceneManager {
  public:
    SceneManager ();
    ~SceneManager ();

    SceneManager (const SceneManager&) = delete;
    SceneManager& operator= (const SceneManager&) = delete;

    SceneManager (SceneManager&&) noexcept;
    SceneManager& operator= (SceneManager&&) noexcept;

    bool initialize ();
    void shutdown ();
    void update (float delta_time);

    bool load_scene (const std::string& name);
    bool unload_scene (const std::string& name);
    [[nodiscard]] const std::string& get_current_scene () const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Scene
