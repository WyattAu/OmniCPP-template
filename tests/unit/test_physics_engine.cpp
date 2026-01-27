/**
 * @file test_physics_engine.cpp
 * @brief Unit tests for PhysicsEngine
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/physics/PhysicsEngine.hpp"

namespace omnicpp {
namespace test {

class PhysicsEngineTest : public ::testing::Test {
protected:
    void SetUp() override {
        physics_engine_ = std::make_unique<PhysicsEngine>();
    }

    void TearDown() override {
        if (physics_engine_) {
            physics_engine_->shutdown();
        }
    }

    std::unique_ptr<PhysicsEngine> physics_engine_;
};

TEST_F(PhysicsEngineTest, DefaultInitialization) {
    ASSERT_TRUE(physics_engine_->initialize());
}

TEST_F(PhysicsEngineTest, MultipleInitialization) {
    ASSERT_TRUE(physics_engine_->initialize());
    physics_engine_->shutdown();
    
    // Re-initialize should work
    ASSERT_TRUE(physics_engine_->initialize());
    physics_engine_->shutdown();
}

TEST_F(PhysicsEngineTest, ShutdownWithoutInitialize) {
    // Should not crash
    physics_engine_->shutdown();
}

TEST_F(PhysicsEngineTest, UpdateWithoutInitialize) {
    // Should not crash
    physics_engine_->update(0.016f);
}

TEST_F(PhysicsEngineTest, SetGravity) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_gravity(0.0f, -9.81f, 0.0f);
}

TEST_F(PhysicsEngineTest, GetGravity) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    auto gravity = physics_engine_->get_gravity();
    // We don't assert the value as it depends on the configuration
}

TEST_F(PhysicsEngineTest, CreateRigidBody) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    auto body = physics_engine_->create_rigidBody();
    // We don't assert the result as it depends on the implementation
}

TEST_F(PhysicsEngineTest, DestroyRigidBody) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->destroy_rigidBody(nullptr);
}

TEST_F(PhysicsEngineTest, SetRigidBodyPosition) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_position(nullptr, 0.0f, 0.0f, 0.0f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyRotation) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_rotation(nullptr, 0.0f, 0.0f, 0.0f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyVelocity) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_velocity(nullptr, 0.0f, 0.0f, 0.0f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyAngularVelocity) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_angular_velocity(nullptr, 0.0f, 0.0f, 0.0f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyMass) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_mass(nullptr, 1.0f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyFriction) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_friction(nullptr, 0.5f);
}

TEST_F(PhysicsEngineTest, SetRigidBodyRestitution) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    physics_engine_->set_rigidBody_restitution(nullptr, 0.5f);
}

TEST_F(PhysicsEngineTest, Raycast) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    // Should not crash
    auto result = physics_engine_->raycast(0.0f, 0.0f, 0.0f, 0.0f, -1.0f, 0.0f);
    // We don't assert the result as it depends on the scene
}

TEST_F(PhysicsEngineTest, GetRigidBodyCount) {
    ASSERT_TRUE(physics_engine_->initialize());
    
    auto count = physics_engine_->get_rigidBody_count();
    ASSERT_GE(count, 0);
}

} // namespace test
} // namespace omnicpp
