/**
 * @file script_manager.cpp
 * @brief Script management implementation
 */

#include "engine/scripting/script_manager.hpp"
#include <mutex>
#include <unordered_map>

namespace OmniCpp::Engine::Scripting {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct ScriptManager::Impl {
    struct ScriptInfo {
      std::string path;
    };
    std::unordered_map<std::string, ScriptInfo> scripts;
    std::mutex mutex;
    bool initialized{ false };
  };

  ScriptManager::ScriptManager () : m_impl (std::make_unique<Impl> ()) {
  }

  ScriptManager::~ScriptManager () {
    shutdown ();
  }

  ScriptManager::ScriptManager (ScriptManager&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
  }

  ScriptManager& ScriptManager::operator= (ScriptManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool ScriptManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->scripts.clear ();
    m_impl->initialized = true;

    return true;
  }

  void ScriptManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->scripts.clear ();
    m_impl->initialized = false;
  }

  void ScriptManager::update (float delta_time) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update scripts here
  }

  bool ScriptManager::load_script (const std::string& name, const std::string& path) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return false;
    }

    Impl::ScriptInfo info{ path };
    m_impl->scripts[name] = info;
    return true;
  }

  bool ScriptManager::unload_script (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return false;
    }

    auto it = m_impl->scripts.find (name);
    if (it != m_impl->scripts.end ()) {
      m_impl->scripts.erase (it);
      return true;
    }
    return false;
  }

  bool ScriptManager::execute_script (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return false;
    }

    auto it = m_impl->scripts.find (name);
    return it != m_impl->scripts.end ();
  }

} // namespace OmniCpp::Engine::Scripting
