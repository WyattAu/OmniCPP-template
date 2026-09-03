/**
 * @file SceneManager.hpp
 * @brief Scene manager for managing multiple scenes
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <unordered_map>
#include "engine/scene/Scene.hpp"

namespace omnicpp {
namespace scene {

/**
 * @brief Scene manager for managing multiple scenes
 * 
 * Manages scene loading, unloading, and switching.
 */
class SceneManager {
public:
    /**
     * @brief Construct a new Scene Manager object
     */
    SceneManager() = default;

    /**
     * @brief Destroy the Scene Manager object
     */
    ~SceneManager() = default;

    // Disable copying
    SceneManager(const SceneManager&) = delete;
    SceneManager& operator=(const SceneManager&) = delete;

    // Enable moving
    SceneManager(SceneManager&&) noexcept = default;
    SceneManager& operator=(SceneManager&&) noexcept = default;

    /**
     * @brief Add a scene to the manager
     * @param scene Pointer to scene (takes ownership)
     */
    void add_scene(std::unique_ptr<Scene> scene);

    /**
     * @brief Remove a scene from the manager
     * @param name The scene name
     * @return std::unique_ptr<Scene> The removed scene
     */
    std::unique_ptr<Scene> remove_scene(const std::string& name);

    /**
     * @brief Get a scene by name
     * @param name The scene name
     * @return Scene* Pointer to scene, or nullptr if not found
     */
    Scene* get_scene(const std::string& name) const;

    /**
     * @brief Get all scenes
     * @return const std::vector<std::unique_ptr<Scene>>& The scenes
     */
    const std::vector<std::unique_ptr<Scene>>& get_scenes() const { return m_scenes; }

    /**
     * @brief Get active scene
     * @return Scene* Pointer to active scene, or nullptr if none
     */
    Scene* get_active_scene() const { return m_active_scene; }

    /**
     * @brief Load a scene
     * @param name The scene name
     * @return true if loaded successfully, false otherwise
     */
    bool load_scene(const std::string& name);

    /**
     * @brief Unload the active scene
     */
    void unload_scene();

    /**
     * @brief Switch to a different scene
     * @param name The scene name
     * @return true if switched successfully, false otherwise
     */
    bool switch_scene(const std::string& name);

    /**
     * @brief Update the active scene
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Render the active scene
     */
    void render();

private:
    std::vector<std::unique_ptr<Scene>> m_scenes;
    std::unordered_map<std::string, Scene*> m_scene_map;
    Scene* m_active_scene = nullptr;
};

} // namespace scene
} // namespace omnicpp
