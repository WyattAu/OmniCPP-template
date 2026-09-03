#pragma once

#include <cstddef>
#include <memory>
#include <string>
#include <vector>

namespace omnicpp::scripting {

class Script {
public:
    Script(std::string path, std::string source)
        : m_path(std::move(path)), m_source(std::move(source)) {}

    [[nodiscard]] const std::string& path() const noexcept { return m_path; }
    [[nodiscard]] const std::string& source() const noexcept { return m_source; }

private:
    std::string m_path;
    std::string m_source;
};

class ScriptManager {
public:
    ScriptManager();
    ~ScriptManager();

    ScriptManager(const ScriptManager&) = delete;
    ScriptManager& operator=(const ScriptManager&) = delete;
    ScriptManager(ScriptManager&&) noexcept;
    ScriptManager& operator=(ScriptManager&&) noexcept;

    bool initialize();
    void shutdown();
    void update(float delta_time);

    Script* load_script(const std::string& path);
    void unload_script(const std::string& path);
    bool execute_script(Script* script);
    bool call_function(const std::string& function_name,
                       const std::vector<std::string>& args = {});
    void register_function(const std::string& name, void* function);

    [[nodiscard]] const std::vector<Script*>& get_scripts() const noexcept {
        return m_script_list;
    }
    [[nodiscard]] bool is_initialized() const noexcept { return m_initialized; }

private:
    std::vector<std::unique_ptr<Script>> m_scripts;
    std::vector<Script*> m_script_list;
    bool m_initialized{false};
};

} // namespace omnicpp::scripting
