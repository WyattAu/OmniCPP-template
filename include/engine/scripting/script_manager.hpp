/**
 * @file script_manager.hpp
 * @brief Script management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Scripting {

  /**
   * @brief Script manager class
   */
  class ScriptManager {
  public:
    ScriptManager ();
    ~ScriptManager ();

    ScriptManager (const ScriptManager&) = delete;
    ScriptManager& operator= (const ScriptManager&) = delete;

    ScriptManager (ScriptManager&&) noexcept;
    ScriptManager& operator= (ScriptManager&&) noexcept;

    bool initialize ();
    void shutdown ();
    void update (float delta_time);

    bool load_script (const std::string& name, const std::string& path);
    bool unload_script (const std::string& name);
    bool execute_script (const std::string& name);

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Scripting
