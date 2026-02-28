/**
 * @file AudioManager.cpp
 * @brief Stub implementation of audio manager subsystem
 * @version 1.0.0
 */

#include "engine/IAudioManager.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {

class AudioManagerStub : public IAudioManager {
public:
    AudioManagerStub() = default;
    ~AudioManagerStub() override = default;

    bool initialize() override {
        omnicpp::log::info("AudioManagerStub: Initialized");
        return true;
    }

    void shutdown() override {
        omnicpp::log::info("AudioManagerStub: Shutdown");
    }

    uint32_t load_sound(const char* file_path) override {
        omnicpp::log::debug("AudioManagerStub: Loading sound from {}", file_path);
        (void)file_path;
        return 0;
    }

    bool play_sound(uint32_t sound_id) override {
        omnicpp::log::debug("AudioManagerStub: Playing sound {}", sound_id);
        (void)sound_id;
        return true;
    }

    bool stop_sound(uint32_t sound_id) override {
        omnicpp::log::debug("AudioManagerStub: Stopping sound {}", sound_id);
        (void)sound_id;
        return true;
    }

    void set_master_volume(float volume) override {
        omnicpp::log::debug("AudioManagerStub: Setting master volume to {}", volume);
        (void)volume;
    }

    float get_master_volume() const override {
        return 1.0f;
    }

    void update(float delta_time) override {
        (void)delta_time;
    }
};

} // namespace omnicpp
