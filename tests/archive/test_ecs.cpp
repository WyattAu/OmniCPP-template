/**
 * @file test_ecs.cpp
 * @brief Unit tests for ECS (Entity Component System)
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/ecs/Entity.hpp"
#include "engine/ecs/Component.hpp"
#include "engine/ecs/TransformComponent.hpp"
#include "engine/ecs/MeshComponent.hpp"

using omnicpp::ecs::Entity;
using omnicpp::ecs::Component;
using omnicpp::ecs::TransformComponent;
using omnicpp::ecs::MeshComponent;

namespace omnicpp {
namespace test {

class ECSTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create entities directly - no EntityManager needed
        next_entity_id = 0;
    }

    void TearDown() override {
        // Entities clean up themselves via destructors
    }

    uint64_t next_entity_id = 0;
};

TEST_F(ECSTest, CreateEntity) {
    Entity entity(next_entity_id++, "TestEntity");
    ASSERT_EQ(entity.get_id(), 0);
    ASSERT_EQ(entity.get_name(), "TestEntity");
    ASSERT_TRUE(entity.is_active());
}

TEST_F(ECSTest, EntityName) {
    Entity entity(next_entity_id++, "NamedEntity");
    ASSERT_EQ(entity.get_name(), "NamedEntity");
    
    entity.set_name("RenamedEntity");
    ASSERT_EQ(entity.get_name(), "RenamedEntity");
}

TEST_F(ECSTest, EntityActiveState) {
    Entity entity(next_entity_id++);
    ASSERT_TRUE(entity.is_active());
    
    entity.set_active(false);
    ASSERT_FALSE(entity.is_active());
    
    entity.set_active(true);
    ASSERT_TRUE(entity.is_active());
}

TEST_F(ECSTest, AddComponent) {
    Entity entity(next_entity_id++);
    auto* transform = entity.add_component<TransformComponent>(entity.get_id());
    ASSERT_NE(transform, nullptr);
}

TEST_F(ECSTest, GetComponent) {
    Entity entity(next_entity_id++);
    entity.add_component<TransformComponent>(entity.get_id());
    
    auto* retrieved = entity.get_component<TransformComponent>();
    ASSERT_NE(retrieved, nullptr);
}

TEST_F(ECSTest, RemoveComponent) {
    Entity entity(next_entity_id++);
    entity.add_component<TransformComponent>(entity.get_id());
    
    entity.remove_component<TransformComponent>();
    
    auto* retrieved = entity.get_component<TransformComponent>();
    ASSERT_EQ(retrieved, nullptr);
}

TEST_F(ECSTest, HasComponent) {
    Entity entity(next_entity_id++);
    ASSERT_FALSE(entity.has_component<TransformComponent>());
    
    entity.add_component<TransformComponent>(entity.get_id());
    ASSERT_TRUE(entity.has_component<TransformComponent>());
    
    entity.remove_component<TransformComponent>();
    ASSERT_FALSE(entity.has_component<TransformComponent>());
}

TEST_F(ECSTest, TransformComponentDefaultValues) {
    Entity entity(next_entity_id++);
    auto* transform = entity.add_component<TransformComponent>(entity.get_id());
    
    auto pos = transform->get_position();
    ASSERT_FLOAT_EQ(pos.x, 0.0f);
    ASSERT_FLOAT_EQ(pos.y, 0.0f);
    ASSERT_FLOAT_EQ(pos.z, 0.0f);

    auto rot = transform->get_rotation();
    ASSERT_FLOAT_EQ(rot.x, 0.0f);
    ASSERT_FLOAT_EQ(rot.y, 0.0f);
    ASSERT_FLOAT_EQ(rot.z, 0.0f);

    auto scl = transform->get_scale();
    ASSERT_FLOAT_EQ(scl.x, 1.0f);
    ASSERT_FLOAT_EQ(scl.y, 1.0f);
    ASSERT_FLOAT_EQ(scl.z, 1.0f);
}

TEST_F(ECSTest, TransformComponentSetValues) {
    Entity entity(next_entity_id++);
    auto* transform = entity.add_component<TransformComponent>(entity.get_id());

    using omnicpp::math::Vec3;
    transform->set_position(Vec3(1.0f, 2.0f, 3.0f));
    transform->set_rotation(Vec3(45.0f, 90.0f, 135.0f));
    transform->set_scale(Vec3(2.0f, 2.0f, 2.0f));

    auto pos = transform->get_position();
    ASSERT_FLOAT_EQ(pos.x, 1.0f);
    ASSERT_FLOAT_EQ(pos.y, 2.0f);
    ASSERT_FLOAT_EQ(pos.z, 3.0f);

    auto rot = transform->get_rotation();
    ASSERT_FLOAT_EQ(rot.x, 45.0f);
    ASSERT_FLOAT_EQ(rot.y, 90.0f);
    ASSERT_FLOAT_EQ(rot.z, 135.0f);

    auto scl = transform->get_scale();
    ASSERT_FLOAT_EQ(scl.x, 2.0f);
    ASSERT_FLOAT_EQ(scl.y, 2.0f);
    ASSERT_FLOAT_EQ(scl.z, 2.0f);
}

TEST_F(ECSTest, MeshComponentDefaultValues) {
    Entity entity(next_entity_id++);
    auto* mesh = entity.add_component<MeshComponent>(entity.get_id());
    
    ASSERT_EQ(mesh->get_mesh(), nullptr);
    ASSERT_EQ(mesh->get_material(), nullptr);
    ASSERT_TRUE(mesh->is_visible());
    ASSERT_TRUE(mesh->casts_shadows());
}

TEST_F(ECSTest, MeshComponentSetValues) {
    Entity entity(next_entity_id++);
    auto* mesh = entity.add_component<MeshComponent>(entity.get_id());

    mesh->set_visible(false);
    mesh->set_casts_shadows(false);

    ASSERT_FALSE(mesh->is_visible());
    ASSERT_FALSE(mesh->casts_shadows());
}

TEST_F(ECSTest, MultipleComponentsOnEntity) {
    Entity entity(next_entity_id++);
    
    auto* transform = entity.add_component<TransformComponent>(entity.get_id());
    auto* mesh = entity.add_component<MeshComponent>(entity.get_id());

    ASSERT_NE(transform, nullptr);
    ASSERT_NE(mesh, nullptr);
    ASSERT_TRUE(entity.has_component<TransformComponent>());
    ASSERT_TRUE(entity.has_component<MeshComponent>());
}

TEST_F(ECSTest, GetComponentCount) {
    Entity entity(next_entity_id++);
    
    ASSERT_EQ(entity.get_components().size(), 0);
    
    entity.add_component<TransformComponent>(entity.get_id());
    ASSERT_EQ(entity.get_components().size(), 1);
    
    entity.add_component<MeshComponent>(entity.get_id());
    ASSERT_EQ(entity.get_components().size(), 2);
}

TEST_F(ECSTest, MultipleEntities) {
    Entity entity1(next_entity_id++);
    Entity entity2(next_entity_id++);
    Entity entity3(next_entity_id++);
    
    entity1.add_component<TransformComponent>(entity1.get_id());
    entity2.add_component<TransformComponent>(entity2.get_id());
    entity3.add_component<TransformComponent>(entity3.get_id());
    
    ASSERT_TRUE(entity1.has_component<TransformComponent>());
    ASSERT_TRUE(entity2.has_component<TransformComponent>());
    ASSERT_TRUE(entity3.has_component<TransformComponent>());
}

} // namespace test
} // namespace omnicpp
