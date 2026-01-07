/**
 * @file AudioManager.cpp
 * @brief Stub implementation of audio manager subsystem
 * @version 1.0.0
 */

#include "engine/IAudioManager.hpp"

namespace omnicpp {

class AudioManagerStub : public IAudioManager {
public:
    AudioManagerStub() = default;
    ~AudioManagerStub() override = default;

    bool initialize() override {
        return true;
    }

    void shutdown() override {
    }

    uint32_t load_sound(const char* file_path) override {
        (void)file_path;
        return 0;
    }

    bool play_sound(uint32_t sound_id) override {
        (void)sound_id;
        return true;
    }

    bool stop_sound(uint32_t sound_id) override {
        (void)sound_id;
        return true;
    }

    void set_master_volume(float volume) override {
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
