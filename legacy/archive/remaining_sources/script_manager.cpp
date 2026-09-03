#include "engine/scripting/ScriptManager.hpp"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iterator>
#include <utility>

namespace omnicpp::scripting {

ScriptManager::ScriptManager() = default;
ScriptManager::~ScriptManager() { shutdown(); }
ScriptManager::ScriptManager(ScriptManager&&) noexcept = default;
ScriptManager& ScriptManager::operator=(ScriptManager&&) noexcept = default;

bool ScriptManager::initialize() {
    if (m_initialized) {
        return true;
    }
    m_scripts.clear();
    m_script_list.clear();
    m_initialized = true;
    return true;
}

void ScriptManager::shutdown() {
    m_script_list.clear();
    m_scripts.clear();
    m_initialized = false;
}

void ScriptManager::update(float) {
    // Script execution is explicit; update intentionally has no implicit side effects.
}

Script* ScriptManager::load_script(const std::string& path) {
    if (!m_initialized || path.empty() || !std::filesystem::is_regular_file(path)) {
        return nullptr;
    }

    std::ifstream input(path, std::ios::binary);
    if (!input) {
        return nullptr;
    }
    std::string source((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());

    unload_script(path);
    auto script = std::make_unique<Script>(path, std::move(source));
    Script* result = script.get();
    m_scripts.push_back(std::move(script));
    m_script_list.push_back(result);
    return result;
}

void ScriptManager::unload_script(const std::string& path) {
    auto it = std::find_if(m_scripts.begin(), m_scripts.end(),
        [&](const auto& script) { return script->path() == path; });
    if (it == m_scripts.end()) {
        return;
    }
    Script* removed = it->get();
    m_script_list.erase(std::remove(m_script_list.begin(), m_script_list.end(), removed),
                        m_script_list.end());
    m_scripts.erase(it);
}

bool ScriptManager::execute_script(Script* script) {
    if (!m_initialized || script == nullptr) {
        return false;
    }
    return std::any_of(m_script_list.begin(), m_script_list.end(),
                       [&](const auto* loaded) { return loaded == script; });
}

bool ScriptManager::call_function(const std::string& function_name,
                                  const std::vector<std::string>&) {
    if (!m_initialized || function_name.empty()) {
        return false;
    }
    return false; // No embedded VM is linked by the core build.
}

void ScriptManager::register_function(const std::string&, void*) {
    // Registration requires an embedded VM; the dependency-free core has none.
}

} // namespace omnicpp::scripting
