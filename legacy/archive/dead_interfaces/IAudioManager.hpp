/**
 * @file IAudioManager.hpp
 * @brief Audio manager subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for audio playback and mixing.
 */

#ifndef OMNICPP_IAUDIO_MANAGER_HPP
#define OMNICPP_IAUDIO_MANAGER_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Audio manager interface
 */
class IAudioManager {
public:
    virtual ~IAudioManager() = default;
    
    /**
     * @brief Initialize audio manager
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown audio manager
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Load a sound file
     * 
     * @param file_path Path to sound file
     * @return Sound ID, or 0 on failure
     */
    virtual uint32_t load_sound(const char* file_path) = 0;
    
    /**
     * @brief Play a sound
     * 
     * @param sound_id Sound ID from load_sound
     * @return True if successful, false otherwise
     */
    virtual bool play_sound(uint32_t sound_id) = 0;
    
    /**
     * @brief Stop a sound
     * 
     * @param sound_id Sound ID to stop
     * @return True if successful, false otherwise
     */
    virtual bool stop_sound(uint32_t sound_id) = 0;
    
    /**
     * @brief Set master volume
     * 
     * @param volume Volume level (0.0 to 1.0)
     */
    virtual void set_master_volume(float volume) = 0;
    
    /**
     * @brief Get master volume
     * 
     * @return Current volume level
     */
    virtual float get_master_volume() const = 0;
    
    /**
     * @brief Update audio system
     * 
     * @param delta_time Time since last frame in seconds
     */
    virtual void update(float delta_time) = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IAUDIO_MANAGER_HPP
