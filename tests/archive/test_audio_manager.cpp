/**
 * @file test_audio_manager.cpp
 * @brief Unit tests for AudioManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/audio/AudioManager.hpp"

namespace omnicpp {
namespace test {

using audio::AudioManager;
using audio::Sound;

class AudioManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        audio_manager = std::make_unique<AudioManager>();
    }

    void TearDown() override {
        if (audio_manager) {
            audio_manager->shutdown();
        }
    }

    std::unique_ptr<AudioManager> audio_manager;
};

TEST_F(AudioManagerTest, DefaultInitialization) {
    ASSERT_TRUE(audio_manager->initialize());
}

TEST_F(AudioManagerTest, MultipleInitialization) {
    ASSERT_TRUE(audio_manager->initialize());
    audio_manager->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(audio_manager->initialize());
    audio_manager->shutdown();
}

TEST_F(AudioManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    audio_manager->shutdown();
}

TEST_F(AudioManagerTest, UpdateWithoutInitialize) {
    // Should not crash
    audio_manager->update(0.016f);
}

TEST_F(AudioManagerTest, UpdateAfterInitialize) {
    ASSERT_TRUE(audio_manager->initialize());
    
    // Should not crash
    audio_manager->update(0.016f);
}

TEST_F(AudioManagerTest, LoadSound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Test sound loading (will fail if file doesn't exist, but shouldn't crash)
    auto* sound = audio_manager->load_sound("nonexistent.wav");
    // nullptr is expected since file doesn't exist
    EXPECT_EQ(sound, nullptr);
}

TEST_F(AudioManagerTest, UnloadSound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash
    audio_manager->unload_sound("nonexistent");
}

TEST_F(AudioManagerTest, PlaySound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash with nullptr
    audio_manager->play_sound(nullptr);
}

TEST_F(AudioManagerTest, PlaySoundWithLoopAndVolume) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash with nullptr
    audio_manager->play_sound(nullptr, true, 0.5f);
}

TEST_F(AudioManagerTest, StopSound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash with nullptr
    audio_manager->stop_sound(nullptr);
}

TEST_F(AudioManagerTest, PauseSound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash with nullptr
    audio_manager->pause_sound(nullptr);
}

TEST_F(AudioManagerTest, ResumeSound) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash with nullptr
    audio_manager->resume_sound(nullptr);
}

TEST_F(AudioManagerTest, SetMasterVolume) {
    ASSERT_TRUE(audio_manager->initialize());

    // Should not crash
    audio_manager->set_master_volume(0.5f);
}

TEST_F(AudioManagerTest, GetMasterVolume) {
    ASSERT_TRUE(audio_manager->initialize());

    auto volume = audio_manager->get_master_volume();
    ASSERT_GE(volume, 0.0f);
    ASSERT_LE(volume, 1.0f);
}

TEST_F(AudioManagerTest, SetAndGetMasterVolume) {
    ASSERT_TRUE(audio_manager->initialize());

    audio_manager->set_master_volume(0.75f);
    auto volume = audio_manager->get_master_volume();
    EXPECT_FLOAT_EQ(volume, 0.75f);
}

TEST_F(AudioManagerTest, GetSoundEngine) {
    ASSERT_TRUE(audio_manager->initialize());

    // May return nullptr if not implemented
    auto* engine = audio_manager->get_sound_engine();
    (void)engine;
}

} // namespace test
} // namespace omnicpp
