/**
 * @file AudioManager.hpp
 * @brief Audio manager for sound playback
 * @version 1.0.0
 */

#pragma once

#include <string>
#include <memory>
#include <unordered_map>
#include <vector>

namespace omnicpp {
namespace audio {

// Forward declarations
class SoundEngine;
class Sound;

/**
 * @brief Audio manager for sound playback
 * 
 * Manages loading, playback, and lifecycle of audio resources.
 */
class AudioManager {
public:
    /**
     * @brief Construct a new Audio Manager object
     */
    AudioManager() = default;

    /**
     * @brief Destroy the Audio Manager object
     */
    ~AudioManager();

    // Disable copying
    AudioManager(const AudioManager&) = delete;
    AudioManager& operator=(const AudioManager&) = delete;

    // Enable moving
    AudioManager(AudioManager&&) noexcept = default;
    AudioManager& operator=(AudioManager&&) noexcept = default;

    /**
     * @brief Initialize audio manager
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown audio manager
     */
    void shutdown();

    /**
     * @brief Update audio manager
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Load a sound from file
     * @param path Path to sound file
     * @return Sound* Pointer to loaded sound, or nullptr if failed
     */
    Sound* load_sound(const std::string& path);

    /**
     * @brief Unload a sound
     * @param path Path to sound file
     */
    void unload_sound(const std::string& path);

    /**
     * @brief Play a sound
     * @param sound Pointer to sound
     * @param loop Whether to loop the sound
     * @param volume Volume (0.0 to 1.0)
     */
    void play_sound(Sound* sound, bool loop = false, float volume = 1.0f);

    /**
     * @brief Stop a sound
     * @param sound Pointer to sound
     */
    void stop_sound(Sound* sound);

    /**
     * @brief Pause a sound
     * @param sound Pointer to sound
     */
    void pause_sound(Sound* sound);

    /**
     * @brief Resume a sound
     * @param sound Pointer to sound
     */
    void resume_sound(Sound* sound);

    /**
     * @brief Set master volume
     * @param volume Volume (0.0 to 1.0)
     */
    void set_master_volume(float volume);

    /**
     * @brief Get master volume
     * @return float The master volume
     */
    float get_master_volume() const { return m_master_volume; }

    /**
     * @brief Get sound engine
     * @return SoundEngine* Pointer to sound engine
     */
    SoundEngine* get_sound_engine() const { return m_sound_engine.get(); }

private:
    std::unique_ptr<SoundEngine> m_sound_engine;
    std::unordered_map<std::string, std::unique_ptr<Sound>> m_sounds;
    float m_master_volume = 1.0f;
};

} // namespace audio
} // namespace omnicpp
