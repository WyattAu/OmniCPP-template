/**
 * @file ScriptManager.hpp
 * @brief Script manager for Lua scripting
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <memory>
#include <unordered_map>
#include <vector>

namespace omnicpp {
namespace scripting {

// Forward declarations
class LuaVM;
class Script;

/**
 * @brief Script manager for Lua scripting
 * 
 * Manages loading, execution, and lifecycle of Lua scripts.
 */
class ScriptManager {
public:
    /**
     * @brief Construct a new Script Manager object
     */
    ScriptManager() = default;

    /**
     * @brief Destroy the Script Manager object
     */
    ~ScriptManager();

    // Disable copying
    ScriptManager(const ScriptManager&) = delete;
    ScriptManager& operator=(const ScriptManager&) = delete;

    // Enable moving
    ScriptManager(ScriptManager&&) noexcept = default;
    ScriptManager& operator=(ScriptManager&&) noexcept = default;

    /**
     * @brief Initialize script manager
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown script manager
     */
    void shutdown();

    /**
     * @brief Load a script from file
     * @param path Path to script file
     * @return Script* Pointer to loaded script, or nullptr if failed
     */
    Script* load_script(const std::string& path);

    /**
     * @brief Unload a script
     * @param path Path to script file
     */
    void unload_script(const std::string& path);

    /**
     * @brief Execute a script
     * @param script Pointer to script
     * @return true if execution succeeded, false otherwise
     */
    bool execute_script(Script* script);

    /**
     * @brief Call a Lua function
     * @param function_name The function name
     * @param args Arguments to pass to function
     * @return true if call succeeded, false otherwise
     */
    bool call_function(const std::string& function_name, 
                   const std::vector<std::string>& args = {});

    /**
     * @brief Register a C++ function to Lua
     * @param name The function name in Lua
     * @param function The C++ function pointer
     */
    void register_function(const std::string& name, void* function);

    /**
     * @brief Get Lua VM
     * @return LuaVM* Pointer to Lua VM
     */
    LuaVM* get_lua_vm() const { return m_lua_vm.get(); }

    /**
     * @brief Get all loaded scripts
     * @return const std::vector<Script*>& The scripts
     */
    const std::vector<Script*>& get_scripts() const { return m_scripts; }

private:
    std::unique_ptr<LuaVM> m_lua_vm;
    std::unordered_map<std::string, std::unique_ptr<Script>> m_scripts;
    std::vector<Script*> m_script_list;
};

} // namespace scripting
} // namespace omnicpp
