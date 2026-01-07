/**
 * @file scene_manager.cpp
 * @brief Scene management implementation
 */

#include "engine/scene/scene_manager.hpp"
#include <mutex>

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
      return true;
    }

    m_impl->current_scene.clear ();
    m_impl->initialized = true;

    return true;
  }

  void SceneManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->current_scene.clear ();
    m_impl->initialized = false;
  }

  void SceneManager::update (float delta_time) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update scene here
  }

  bool SceneManager::load_scene (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return false;
    }

    m_impl->current_scene = name;
    return true;
  }

  bool SceneManager::unload_scene (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return false;
    }

    if (m_impl->current_scene == name) {
      m_impl->current_scene.clear ();
      return true;
    }
    return false;
  }

  const std::string& SceneManager::get_current_scene () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->current_scene;
  }

} // namespace OmniCpp::Engine::Scene
