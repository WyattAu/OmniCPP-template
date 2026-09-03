/**
 * @file SceneManager.cpp
 * @brief Scene manager implementation
 * @version 1.0.0
 */

#include "engine/scene/SceneManager.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {
namespace scene {

void SceneManager::add_scene(std::unique_ptr<Scene> scene) {
    if (scene) {
        const std::string& name = scene->get_name();
        m_scenes.push_back(std::move(scene));
        m_scene_map[name] = m_scenes.back().get();
        omnicpp::log::debug("SceneManager: Added scene '{}'", name);
    }
}

std::unique_ptr<Scene> SceneManager::remove_scene(const std::string& name) {
    auto it = m_scene_map.find(name);
    if (it != m_scene_map.end()) {
        Scene* scene = it->second;

        // Remove from map
        m_scene_map.erase(it);

        // Remove from vector
        for (auto sit = m_scenes.begin(); sit != m_scenes.end(); ++sit) {
            if (sit->get() == scene) {
                auto removed = std::move(*sit);
                m_scenes.erase(sit);

                // If this was the active scene, clear it
                if (m_active_scene == scene) {
                    m_active_scene = nullptr;
                }

                omnicpp::log::debug("SceneManager: Removed scene '{}'", name);
                return removed;
            }
        }
    }
    omnicpp::log::warn("SceneManager: Scene '{}' not found", name);
    return nullptr;
}

Scene* SceneManager::get_scene(const std::string& name) const {
    auto it = m_scene_map.find(name);
    if (it != m_scene_map.end()) {
        return it->second;
    }
    return nullptr;
}

bool SceneManager::load_scene(const std::string& name) {
    Scene* scene = get_scene(name);
    if (!scene) {
        return false;
    }

    // Unload current scene if any
    if (m_active_scene) {
        m_active_scene->set_active(false);
    }

    // Set new scene as active
    m_active_scene = scene;
    m_active_scene->set_active(true);

    return true;
}

void SceneManager::unload_scene() {
    if (m_active_scene) {
        m_active_scene->set_active(false);
        m_active_scene = nullptr;
    }
}

bool SceneManager::switch_scene(const std::string& name) {
    return load_scene(name);
}

void SceneManager::update(float delta_time) {
    if (m_active_scene) {
        m_active_scene->update(delta_time);
    }
}

void SceneManager::render() {
    if (m_active_scene) {
        m_active_scene->render();
    }
}

} // namespace scene
} // namespace omnicpp
