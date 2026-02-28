/**
 * @file test_physics_engine.cpp
 * @brief Unit tests for PhysicsEngine
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/physics/PhysicsEngine.hpp"

namespace omnicpp {
namespace test {

using physics::PhysicsEngine;

class PhysicsEngineTest : public ::testing::Test {
protected:
    void SetUp() override {
        physics_engine = std::make_unique<PhysicsEngine>();
    }

    void TearDown() override {
        if (physics_engine) {
            physics_engine->shutdown();
        }
    }

    std::unique_ptr<PhysicsEngine> physics_engine;
};

TEST_F(PhysicsEngineTest, DefaultInitialization) {
    ASSERT_TRUE(physics_engine->initialize());
}

TEST_F(PhysicsEngineTest, MultipleInitialization) {
    ASSERT_TRUE(physics_engine->initialize());
    physics_engine->shutdown();
    
    // Re-initialize should work
    ASSERT_TRUE(physics_engine->initialize());
    physics_engine->shutdown();
}

TEST_F(PhysicsEngineTest, ShutdownWithoutInitialize) {
    // Should not crash
    physics_engine->shutdown();
}

TEST_F(PhysicsEngineTest, UpdateWithoutInitialize) {
    // Should not crash
    physics_engine->update(0.016f);
}

TEST_F(PhysicsEngineTest, SetGravity) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash
    physics_engine->set_gravity(0.0f, -9.81f, 0.0f);
}

TEST_F(PhysicsEngineTest, GetGravity) {
    ASSERT_TRUE(physics_engine->initialize());
    
    float x, y, z;
    physics_engine->get_gravity(x, y, z);
    // Default gravity should be -9.81 on Y axis
    EXPECT_FLOAT_EQ(x, 0.0f);
    EXPECT_FLOAT_EQ(y, -9.81f);
    EXPECT_FLOAT_EQ(z, 0.0f);
}

TEST_F(PhysicsEngineTest, AddRigidBody) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash with null pointer (defensive handling)
    physics_engine->add_rigid_body(nullptr);
}

TEST_F(PhysicsEngineTest, RemoveRigidBody) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash with null pointer (defensive handling)
    physics_engine->remove_rigid_body(nullptr);
}

TEST_F(PhysicsEngineTest, GetRigidBodies) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash
    const auto& bodies = physics_engine->get_rigid_bodies();
    // Initially empty
    EXPECT_TRUE(bodies.empty());
}

TEST_F(PhysicsEngineTest, GetCollisionDetection) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash
    auto* collision = physics_engine->get_collision_detection();
    // May be null if not implemented
    (void)collision;
}

TEST_F(PhysicsEngineTest, SetStepSize) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash
    physics_engine->set_step_size(1.0f / 120.0f);
}

TEST_F(PhysicsEngineTest, GetStepSize) {
    ASSERT_TRUE(physics_engine->initialize());
    
    auto step_size = physics_engine->get_step_size();
    ASSERT_GT(step_size, 0.0f);
    // Default is 1/60
    EXPECT_FLOAT_EQ(step_size, 1.0f / 60.0f);
}

TEST_F(PhysicsEngineTest, UpdateAfterInitialize) {
    ASSERT_TRUE(physics_engine->initialize());
    
    // Should not crash
    physics_engine->update(0.016f);
    physics_engine->update(0.016f);
    physics_engine->update(0.016f);
}

} // namespace test
} // namespace omnicpp
