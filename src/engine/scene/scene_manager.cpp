/**
 * @file scene_manager.cpp
 * @brief Scene management implementation
 */

#include "engine/scene/scene_manager.hpp"
#include <mutex>
#include <spdlog/spdlog.h>

namespace OmniCpp::Engine::Scene {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct SceneManager::Impl {
    std::string current_scene;
    std::mutex mutex;
    bool initialized{ false };
  };

  SceneManager::SceneManager () : m_impl (std::make_unique<Impl> ()) {
  }

  SceneManager::~SceneManager () {
    shutdown ();
  }

  SceneManager::SceneManager (SceneManager&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  SceneManager& SceneManager::operator= (SceneManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool SceneManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      spdlog::warn("SceneManager: Already initialized");
      return true;
    }

    m_impl->current_scene.clear ();
    m_impl->initialized = true;

    spdlog::info("SceneManager: Initialized");
    return true;
  }

  void SceneManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->current_scene.clear ();
    m_impl->initialized = false;

    spdlog::info("SceneManager: Shutdown");
  }

  void SceneManager::update (float delta_time) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update scene here
  }

  bool SceneManager::load_scene (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("SceneManager: Not initialized, cannot load scene: {}", name);
      return false;
    }

    m_impl->current_scene = name;
    spdlog::info("SceneManager: Loaded scene '{}'", name);
    return true;
  }

  bool SceneManager::unload_scene (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("SceneManager: Not initialized, cannot unload scene: {}", name);
      return false;
    }

    if (m_impl->current_scene == name) {
      m_impl->current_scene.clear ();
      spdlog::info("SceneManager: Unloaded scene '{}'", name);
      return true;
    }
    spdlog::warn("SceneManager: Scene '{}' is not the current scene", name);
    return false;
  }

  const std::string& SceneManager::get_current_scene () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->current_scene;
  }

} // namespace OmniCpp::Engine::Scene
