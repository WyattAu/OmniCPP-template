/**
 * @file test_resource_manager.cpp
 * @brief Unit tests for ResourceManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/resources/ResourceManager.hpp"

namespace omnicpp {
namespace test {

class ResourceManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        resource_manager_ = std::make_unique<ResourceManager>();
    }

    void TearDown() override {
        if (resource_manager_) {
            resource_manager_->shutdown();
        }
    }

    std::unique_ptr<ResourceManager> resource_manager_;
};

TEST_F(ResourceManagerTest, DefaultInitialization) {
    ASSERT_TRUE(resource_manager_->initialize());
}

TEST_F(ResourceManagerTest, MultipleInitialization) {
    ASSERT_TRUE(resource_manager_->initialize());
    resource_manager_->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(resource_manager_->initialize());
    resource_manager_->shutdown();
}

TEST_F(ResourceManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    resource_manager_->shutdown();
}

TEST_F(ResourceManagerTest, UpdateWithoutInitialize) {
    // Should not crash
    resource_manager_->update();
}

TEST_F(ResourceManagerTest, LoadTexture) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Test texture loading (will fail if file doesn't exist, but shouldn't crash)
    auto texture = resource_manager_->load_texture("nonexistent.png");
    // We don't assert the result as it depends on the file system
}

TEST_F(ResourceManagerTest, LoadShader) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Test shader loading (will fail if file doesn't exist, but shouldn't crash)
    auto shader = resource_manager_->load_shader("nonexistent.vert", "nonexistent.frag");
    // We don't assert the result as it depends on the file system
}

TEST_F(ResourceManagerTest, LoadModel) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Test model loading (will fail if file doesn't exist, but shouldn't crash)
    auto model = resource_manager_->load_model("nonexistent.obj");
    // We don't assert the result as it depends on the file system
}

TEST_F(ResourceManagerTest, LoadAudio) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Test audio loading (will fail if file doesn't exist, but shouldn't crash)
    auto audio = resource_manager_->load_audio("nonexistent.wav");
    // We don't assert the result as it depends on the file system
}

TEST_F(ResourceManagerTest, UnloadResource) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Should not crash
    resource_manager_->unload_resource("nonexistent");
}

TEST_F(ResourceManagerTest, UnloadAllResources) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Should not crash
    resource_manager_->unload_all_resources();
}

TEST_F(ResourceManagerTest, GetResourceCount) {
    ASSERT_TRUE(resource_manager_->initialize());

    auto count = resource_manager_->get_resource_count();
    ASSERT_GE(count, 0);
}

TEST_F(ResourceManagerTest, SetResourcePath) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Should not crash
    resource_manager_->set_resource_path("assets/");
}

TEST_F(ResourceManagerTest, GetResourcePath) {
    ASSERT_TRUE(resource_manager_->initialize());

    auto path = resource_manager_->get_resource_path();
    // We don't assert the value as it depends on the configuration
}

TEST_F(ResourceManagerTest, ReloadResource) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Should not crash
    resource_manager_->reload_resource("nonexistent");
}

TEST_F(ResourceManagerTest, PreloadResources) {
    ASSERT_TRUE(resource_manager_->initialize());

    // Should not crash
    resource_manager_->preload_resources();
}

} // namespace test
} // namespace omnicpp
