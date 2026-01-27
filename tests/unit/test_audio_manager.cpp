/**
 * @file test_audio_manager.cpp
 * @brief Unit tests for AudioManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/audio/AudioManager.hpp"

namespace omnicpp {
namespace test {

class AudioManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        audio_manager_ = std::make_unique<AudioManager>();
    }

    void TearDown() override {
        if (audio_manager_) {
            audio_manager_->shutdown();
        }
    }

    std::unique_ptr<AudioManager> audio_manager_;
};

TEST_F(AudioManagerTest, DefaultInitialization) {
    ASSERT_TRUE(audio_manager_->initialize());
}

TEST_F(AudioManagerTest, MultipleInitialization) {
    ASSERT_TRUE(audio_manager_->initialize());
    audio_manager_->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(audio_manager_->initialize());
    audio_manager_->shutdown();
}

TEST_F(AudioManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    audio_manager_->shutdown();
}

TEST_F(AudioManagerTest, UpdateWithoutInitialize) {
    // Should not crash
    audio_manager_->update();
}

TEST_F(AudioManagerTest, LoadSound) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Test sound loading (will fail if file doesn't exist, but shouldn't crash)
    auto sound = audio_manager_->load_sound("nonexistent.wav");
    // We don't assert the result as it depends on the file system
}

TEST_F(AudioManagerTest, LoadMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Test music loading (will fail if file doesn't exist, but shouldn't crash)
    auto music = audio_manager_->load_music("nonexistent.mp3");
    // We don't assert the result as it depends on the file system
}

TEST_F(AudioManagerTest, PlaySound) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->play_sound(nullptr);
}

TEST_F(AudioManagerTest, StopSound) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->stop_sound(nullptr);
}

TEST_F(AudioManagerTest, PlayMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->play_music(nullptr);
}

TEST_F(AudioManagerTest, StopMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->stop_music();
}

TEST_F(AudioManagerTest, PauseMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->pause_music();
}

TEST_F(AudioManagerTest, ResumeMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->resume_music();
}

TEST_F(AudioManagerTest, SetMusicVolume) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->set_music_volume(0.5f);
}

TEST_F(AudioManagerTest, SetSoundVolume) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->set_sound_volume(0.5f);
}

TEST_F(AudioManagerTest, GetMusicVolume) {
    ASSERT_TRUE(audio_manager_->initialize());

    auto volume = audio_manager_->get_music_volume();
    ASSERT_GE(volume, 0.0f);
    ASSERT_LE(volume, 1.0f);
}

TEST_F(AudioManagerTest, GetSoundVolume) {
    ASSERT_TRUE(audio_manager_->initialize());

    auto volume = audio_manager_->get_sound_volume();
    ASSERT_GE(volume, 0.0f);
    ASSERT_LE(volume, 1.0f);
}

TEST_F(AudioManagerTest, UnloadSound) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->unload_sound("nonexistent");
}

TEST_F(AudioManagerTest, UnloadMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->unload_music("nonexistent");
}

TEST_F(AudioManagerTest, UnloadAllSounds) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->unload_all_sounds();
}

TEST_F(AudioManagerTest, UnloadAllMusic) {
    ASSERT_TRUE(audio_manager_->initialize());

    // Should not crash
    audio_manager_->unload_all_music();
}

} // namespace test
} // namespace omnicpp
