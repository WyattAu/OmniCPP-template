/**
 * @file test_resource_manager.cpp
 * @brief Unit tests for ResourceManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/resources/ResourceManager.hpp"

namespace omnicpp {
namespace test {

using resources::ResourceManager;
using resources::Resource;
using resources::ResourceType;

class ResourceManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        resource_manager = std::make_unique<ResourceManager>();
    }

    void TearDown() override {
        if (resource_manager) {
            resource_manager->shutdown();
        }
    }

    std::unique_ptr<ResourceManager> resource_manager;
};

TEST_F(ResourceManagerTest, DefaultInitialization) {
    ASSERT_TRUE(resource_manager->initialize());
}

TEST_F(ResourceManagerTest, MultipleInitialization) {
    ASSERT_TRUE(resource_manager->initialize());
    resource_manager->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(resource_manager->initialize());
    resource_manager->shutdown();
}

TEST_F(ResourceManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    resource_manager->shutdown();
}

TEST_F(ResourceManagerTest, LoadTexture) {
    ASSERT_TRUE(resource_manager->initialize());

    // Test texture loading (will fail if file doesn't exist, but shouldn't crash)
    auto* texture = resource_manager->load_texture("nonexistent.png");
    // nullptr is expected since file doesn't exist
    EXPECT_EQ(texture, nullptr);
}

TEST_F(ResourceManagerTest, LoadShader) {
    ASSERT_TRUE(resource_manager->initialize());

    // Test shader loading (will fail if file doesn't exist, but shouldn't crash)
    auto* shader = resource_manager->load_shader("nonexistent.vert");
    // nullptr is expected since file doesn't exist
    EXPECT_EQ(shader, nullptr);
}

TEST_F(ResourceManagerTest, LoadMesh) {
    ASSERT_TRUE(resource_manager->initialize());

    // Test mesh loading (will fail if file doesn't exist, but shouldn't crash)
    auto* mesh = resource_manager->load_mesh("nonexistent.obj");
    // nullptr is expected since file doesn't exist
    EXPECT_EQ(mesh, nullptr);
}

TEST_F(ResourceManagerTest, LoadMaterial) {
    ASSERT_TRUE(resource_manager->initialize());

    // Test material loading (will fail if file doesn't exist, but shouldn't crash)
    auto* material = resource_manager->load_material("nonexistent.mat");
    // nullptr is expected since file doesn't exist
    EXPECT_EQ(material, nullptr);
}

TEST_F(ResourceManagerTest, UnloadResource) {
    ASSERT_TRUE(resource_manager->initialize());

    // Should not crash
    resource_manager->unload_resource("nonexistent");
}

TEST_F(ResourceManagerTest, UnloadAllResources) {
    ASSERT_TRUE(resource_manager->initialize());

    // Should not crash
    resource_manager->unload_all();
}

TEST_F(ResourceManagerTest, GetResourceCount) {
    ASSERT_TRUE(resource_manager->initialize());

    auto count = resource_manager->get_resource_count();
    ASSERT_EQ(count, 0);
}

TEST_F(ResourceManagerTest, GetMemoryUsage) {
    ASSERT_TRUE(resource_manager->initialize());

    auto usage = resource_manager->get_memory_usage();
    ASSERT_EQ(usage, 0);
}

TEST_F(ResourceManagerTest, GetResource) {
    ASSERT_TRUE(resource_manager->initialize());

    // Should return nullptr for non-existent resource
    auto* resource = resource_manager->get_resource("nonexistent");
    EXPECT_EQ(resource, nullptr);
}

} // namespace test
} // namespace omnicpp
