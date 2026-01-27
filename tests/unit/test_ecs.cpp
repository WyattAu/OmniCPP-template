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

namespace omnicpp {
namespace test {

class ECSTest : public ::testing::Test {
protected:
    void SetUp() override {
        entity_manager_ = std::make_unique<EntityManager>();
    }

    void TearDown() override {
        if (entity_manager_) {
            entity_manager_->shutdown();
        }
    }

    std::unique_ptr<EntityManager> entity_manager_;
};

TEST_F(ECSTest, CreateEntity) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);
}

TEST_F(ECSTest, DestroyEntity) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);

    entity_manager_->destroy_entity(entity);
}

TEST_F(ECSTest, AddComponent) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);

    auto transform = std::make_shared<TransformComponent>();
    entity_manager_->add_component(entity, transform);
}

TEST_F(ECSTest, GetComponent) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);

    auto transform = std::make_shared<TransformComponent>();
    entity_manager_->add_component(entity, transform);

    auto retrieved = entity_manager_->get_component<TransformComponent>(entity);
    ASSERT_NE(retrieved, nullptr);
}

TEST_F(ECSTest, RemoveComponent) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);

    auto transform = std::make_shared<TransformComponent>();
    entity_manager_->add_component(entity, transform);

    entity_manager_->remove_component<TransformComponent>(entity);

    auto retrieved = entity_manager_->get_component<TransformComponent>(entity);
    ASSERT_EQ(retrieved, nullptr);
}

TEST_F(ECSTest, TransformComponentDefaultValues) {
    auto transform = std::make_shared<TransformComponent>();

    ASSERT_FLOAT_EQ(transform->position.x, 0.0f);
    ASSERT_FLOAT_EQ(transform->position.y, 0.0f);
    ASSERT_FLOAT_EQ(transform->position.z, 0.0f);

    ASSERT_FLOAT_EQ(transform->rotation.x, 0.0f);
    ASSERT_FLOAT_EQ(transform->rotation.y, 0.0f);
    ASSERT_FLOAT_EQ(transform->rotation.z, 0.0f);

    ASSERT_FLOAT_EQ(transform->scale.x, 1.0f);
    ASSERT_FLOAT_EQ(transform->scale.y, 1.0f);
    ASSERT_FLOAT_EQ(transform->scale.z, 1.0f);
}

TEST_F(ECSTest, TransformComponentSetValues) {
    auto transform = std::make_shared<TransformComponent>();

    transform->position = Vec3(1.0f, 2.0f, 3.0f);
    transform->rotation = Vec3(45.0f, 90.0f, 135.0f);
    transform->scale = Vec3(2.0f, 2.0f, 2.0f);

    ASSERT_FLOAT_EQ(transform->position.x, 1.0f);
    ASSERT_FLOAT_EQ(transform->position.y, 2.0f);
    ASSERT_FLOAT_EQ(transform->position.z, 3.0f);

    ASSERT_FLOAT_EQ(transform->rotation.x, 45.0f);
    ASSERT_FLOAT_EQ(transform->rotation.y, 90.0f);
    ASSERT_FLOAT_EQ(transform->rotation.z, 135.0f);

    ASSERT_FLOAT_EQ(transform->scale.x, 2.0f);
    ASSERT_FLOAT_EQ(transform->scale.y, 2.0f);
    ASSERT_FLOAT_EQ(transform->scale.z, 2.0f);
}

TEST_F(ECSTest, MeshComponentDefaultValues) {
    auto mesh = std::make_shared<MeshComponent>();

    ASSERT_EQ(mesh->mesh_id, 0);
    ASSERT_EQ(mesh->material_id, 0);
}

TEST_F(ECSTest, MeshComponentSetValues) {
    auto mesh = std::make_shared<MeshComponent>();

    mesh->mesh_id = 123;
    mesh->material_id = 456;

    ASSERT_EQ(mesh->mesh_id, 123);
    ASSERT_EQ(mesh->material_id, 456);
}

TEST_F(ECSTest, MultipleComponentsOnEntity) {
    auto entity = entity_manager_->create_entity();
    ASSERT_NE(entity, nullptr);

    auto transform = std::make_shared<TransformComponent>();
    auto mesh = std::make_shared<MeshComponent>();

    entity_manager_->add_component(entity, transform);
    entity_manager_->add_component(entity, mesh);

    auto retrieved_transform = entity_manager_->get_component<TransformComponent>(entity);
    auto retrieved_mesh = entity_manager_->get_component<MeshComponent>(entity);

    ASSERT_NE(retrieved_transform, nullptr);
    ASSERT_NE(retrieved_mesh, nullptr);
}

TEST_F(ECSTest, EntityCount) {
    auto count_before = entity_manager_->get_entity_count();

    auto entity1 = entity_manager_->create_entity();
    auto entity2 = entity_manager_->create_entity();
    auto entity3 = entity_manager_->create_entity();

    auto count_after = entity_manager_->get_entity_count();

    ASSERT_EQ(count_after, count_before + 3);
}

TEST_F(ECSTest, GetAllEntities) {
    auto entity1 = entity_manager_->create_entity();
    auto entity2 = entity_manager_->create_entity();

    auto entities = entity_manager_->get_all_entities();

    ASSERT_GE(entities.size(), 2);
}

} // namespace test
} // namespace omnicpp
