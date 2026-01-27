/**
 * @file script_manager.cpp
 * @brief Script management implementation
 */

#include "engine/scripting/script_manager.hpp"
#include <mutex>
#include <unordered_map>
#include <spdlog/spdlog.h>

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
      spdlog::warn("ScriptManager: Already initialized");
      return true;
    }

    m_impl->scripts.clear ();
    m_impl->initialized = true;

    spdlog::info("ScriptManager: Initialized");
    return true;
  }

  void ScriptManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->scripts.clear ();
    m_impl->initialized = false;

    spdlog::info("ScriptManager: Shutdown");
  }

  void ScriptManager::update (float delta_time) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update scripts here
  }

  bool ScriptManager::load_script (const std::string& name, const std::string& path) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("ScriptManager: Not initialized, cannot load script: {}", name);
      return false;
    }

    Impl::ScriptInfo info{ path };
    m_impl->scripts[name] = info;
    spdlog::debug("ScriptManager: Loaded script '{}' from '{}'", name, path);
    return true;
  }

  bool ScriptManager::unload_script (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("ScriptManager: Not initialized, cannot unload script: {}", name);
      return false;
    }

    auto it = m_impl->scripts.find (name);
    if (it != m_impl->scripts.end ()) {
      m_impl->scripts.erase (it);
      spdlog::debug("ScriptManager: Unloaded script '{}'", name);
      return true;
    }
    spdlog::warn("ScriptManager: Script '{}' not found", name);
    return false;
  }

  bool ScriptManager::execute_script (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("ScriptManager: Not initialized, cannot execute script: {}", name);
      return false;
    }

    auto it = m_impl->scripts.find (name);
    if (it != m_impl->scripts.end ()) {
      spdlog::debug("ScriptManager: Executing script '{}'", name);
      return true;
    }
    spdlog::warn("ScriptManager: Script '{}' not found", name);
    return false;
  }

} // namespace OmniCpp::Engine::Scripting
