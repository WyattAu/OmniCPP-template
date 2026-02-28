/**
 * @file test_engine_core.cpp
 * @brief Unit tests for Engine Core
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/core/engine.hpp"

namespace omnicpp {
namespace test {

class EngineCoreTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create engine for each test
        engine_ = std::make_unique<Engine>();
    }

    void TearDown() override {
        if (engine_) {
            engine_->shutdown();
        }
    }

    std::unique_ptr<Engine> engine_;
};

TEST_F(EngineCoreTest, DefaultInitialization) {
    ASSERT_TRUE(engine_->initialize());
}

TEST_F(EngineCoreTest, InitializationWithConfig) {
    EngineConfig config;
    config.window_width = 1280;
    config.window_height = 720;
    config.window_title = "Test Engine";

    ASSERT_TRUE(engine_->initialize(config));
}

TEST_F(EngineCoreTest, MultipleInitialization) {
    ASSERT_TRUE(engine_->initialize());
    engine_->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(engine_->initialize());
    engine_->shutdown();
}

TEST_F(EngineCoreTest, RunWithoutInitialize) {
    // Should not crash
    engine_->run();
}

TEST_F(EngineCoreTest, ShutdownWithoutInitialize) {
    // Should not crash
    engine_->shutdown();
}

TEST_F(EngineCoreTest, GetVersion) {
    auto version = engine_->get_version();
    ASSERT_GT(version.major, 0);
}

TEST_F(EngineCoreTest, GetSubsystems) {
    ASSERT_TRUE(engine_->initialize());

    auto renderer = engine_->get_renderer();
    ASSERT_NE(renderer, nullptr);

    auto input_manager = engine_->get_input_manager();
    ASSERT_NE(input_manager, nullptr);

    auto audio_manager = engine_->get_audio_manager();
    ASSERT_NE(audio_manager, nullptr);

    auto physics_engine = engine_->get_physics_engine();
    ASSERT_NE(physics_engine, nullptr);

    auto resource_manager = engine_->get_resource_manager();
    ASSERT_NE(resource_manager, nullptr);
}

TEST_F(EngineCoreTest, SetLogger) {
    auto logger = std::make_shared<SpdLogLogger>("test_logger");
    ASSERT_TRUE(logger->initialize());

    engine_->set_logger(logger);

    ASSERT_TRUE(engine_->initialize());
}

TEST_F(EngineCoreTest, RunWithInitialize) {
    ASSERT_TRUE(engine_->initialize());

    // Run for a short time (should not block indefinitely)
    // In a real test, you'd use a timeout or mock the run loop
    engine_->run();
}

} // namespace test
} // namespace omnicpp
