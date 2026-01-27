# DES-026: Physics Engine Interface

## Overview
Defines physics engine interface for OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_PHYSICS_ENGINE_INTERFACE_H
#define OMNICPP_PHYSICS_ENGINE_INTERFACE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace omnicpp {
namespace engine {

// Forward declarations
class IRigidBody;
class ICollider;
class IPhysicsMaterial;
class IJoint;

// Physics configuration
struct PhysicsConfig {
    float gravity_x;
    float gravity_y;
    float gravity_z;
    int solver_iterations;
    int solver_velocity_iterations;
    bool enable_sleeping;
    float sleep_threshold;
    bool enable_continuous_collision;
    float fixed_time_step;
    int max_sub_steps;

    PhysicsConfig()
        : gravity_x(0.0f)
        , gravity_y(-9.81f)
        , gravity_z(0.0f)
        , solver_iterations(10)
        , solver_velocity_iterations(1)
        , enable_sleeping(true)
        , sleep_threshold(0.1f)
        , enable_continuous_collision(false)
        , fixed_time_step(1.0f / 60.0f)
        , max_sub_steps(4)
    {}
};

// Physics body type
enum class BodyType {
    STATIC,
    KINEMATIC,
    DYNAMIC
};

// Collision shape type
enum class CollisionShapeType {
    BOX,
    SPHERE,
    CAPSULE,
    CYLINDER,
    CONE,
    MESH,
    HEIGHTFIELD,
    COMPOUND
};

// Joint type
enum class JointType {
    FIXED,
    HINGE,
    SLIDER,
    BALL,
    CONE_TWIST,
    GENERIC_6DOF
};

// Collision filter
struct CollisionFilter {
    uint32_t category_bits;
    uint32_t mask_bits;
    int group_index;

    CollisionFilter()
        : category_bits(1)
        , mask_bits(0xFFFFFFFF)
        , group_index(0)
    {}
};

// Physics statistics
struct PhysicsStats {
    uint32_t active_bodies;
    uint32_t sleeping_bodies;
    uint32_t total_bodies;
    uint32_t collisions;
    uint32_t contacts;
    double simulation_time;
    double broadphase_time;
    double narrowphase_time;

    PhysicsStats()
        : active_bodies(0)
        , sleeping_bodies(0)
        , total_bodies(0)
        , collisions(0)
        , contacts(0)
        , simulation_time(0.0)
        , broadphase_time(0.0)
        , narrowphase_time(0.0)
    {}
};

// Collision contact
struct CollisionContact {
    float position_x;
    float position_y;
    float position_z;
    float normal_x;
    float normal_y;
    float normal_z;
    float penetration_depth;
    float impulse;

    CollisionContact()
        : position_x(0.0f)
        , position_y(0.0f)
        , position_z(0.0f)
        , normal_x(0.0f)
        , normal_y(0.0f)
        , normal_z(0.0f)
        , penetration_depth(0.0f)
        , impulse(0.0f)
    {}
};

// Collision event
struct CollisionEvent {
    uint32_t body_a_id;
    uint32_t body_b_id;
    std::vector<CollisionContact> contacts;
    bool is_starting;

    CollisionEvent()
        : body_a_id(0)
        , body_b_id(0)
        , is_starting(true)
    {}
};

// Physics engine interface
class IPhysicsEngine {
public:
    virtual ~IPhysicsEngine() = default;

    // Initialization
    virtual bool initialize(const PhysicsConfig& config) = 0;
    virtual void shutdown() = 0;

    // Simulation
    virtual void update(double delta_time) = 0;
    virtual void step_simulation(float time_step, int max_sub_steps) = 0;

    // Rigid bodies
    virtual uint32_t create_rigid_body(BodyType type) = 0;
    virtual void destroy_rigid_body(uint32_t body_id) = 0;
    virtual IRigidBody* get_rigid_body(uint32_t body_id) = 0;
    virtual const IRigidBody* get_rigid_body(uint32_t body_id) const = 0;

    // Colliders
    virtual uint32_t create_collider(CollisionShapeType shape_type) = 0;
    virtual void destroy_collider(uint32_t collider_id) = 0;
    virtual ICollider* get_collider(uint32_t collider_id) = 0;
    virtual const ICollider* get_collider(uint32_t collider_id) const = 0;

    // Physics materials
    virtual uint32_t create_physics_material(float static_friction, float dynamic_friction, float restitution) = 0;
    virtual void destroy_physics_material(uint32_t material_id) = 0;
    virtual IPhysicsMaterial* get_physics_material(uint32_t material_id) = 0;
    virtual const IPhysicsMaterial* get_physics_material(uint32_t material_id) const = 0;

    // Joints
    virtual uint32_t create_joint(JointType joint_type) = 0;
    virtual void destroy_joint(uint32_t joint_id) = 0;
    virtual IJoint* get_joint(uint32_t joint_id) = 0;
    virtual const IJoint* get_joint(uint32_t joint_id) const = 0;

    // Collision detection
    virtual bool raycast(float origin_x, float origin_y, float origin_z,
                        float direction_x, float direction_y, float direction_z,
                        float max_distance, CollisionContact& contact) const = 0;
    virtual bool sweep_test(uint32_t body_id, float direction_x, float direction_y, float direction_z,
                          float max_distance, CollisionContact& contact) const = 0;
    virtual bool overlap_test(uint32_t body_a_id, uint32_t body_b_id) const = 0;

    // Gravity
    virtual void set_gravity(float x, float y, float z) = 0;
    virtual void get_gravity(float& x, float& y, float& z) const = 0;

    // Collision events
    using CollisionCallback = std::function<void(const CollisionEvent&)>;
    virtual void set_collision_callback(CollisionCallback callback) = 0;
    virtual void clear_collision_callback() = 0;

    // Statistics
    virtual const PhysicsStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Configuration
    virtual const PhysicsConfig& get_config() const = 0;
    virtual void set_config(const PhysicsConfig& config) = 0;
};

// Rigid body interface
class IRigidBody {
public:
    virtual ~IRigidBody() = default;

    virtual uint32_t get_id() const = 0;

    // Type
    virtual void set_type(BodyType type) = 0;
    virtual BodyType get_type() const = 0;

    // Position
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;

    // Rotation
    virtual void set_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;

    // Velocity
    virtual void set_linear_velocity(float x, float y, float z) = 0;
    virtual void get_linear_velocity(float& x, float& y, float& z) const = 0;
    virtual void set_angular_velocity(float x, float y, float z) = 0;
    virtual void get_angular_velocity(float& x, float& y, float& z) const = 0;

    // Mass
    virtual void set_mass(float mass) = 0;
    virtual float get_mass() const = 0;
    virtual void set_inverse_mass(float inverse_mass) = 0;
    virtual float get_inverse_mass() const = 0;

    // Inertia
    virtual void set_inertia(float x, float y, float z) = 0;
    virtual void get_inertia(float& x, float& y, float& z) const = 0;
    virtual void set_inverse_inertia(float x, float y, float z) = 0;
    virtual void get_inverse_inertia(float& x, float& y, float& z) const = 0;

    // Damping
    virtual void set_linear_damping(float damping) = 0;
    virtual float get_linear_damping() const = 0;
    virtual void set_angular_damping(float damping) = 0;
    virtual float get_angular_damping() const = 0;

    // Sleeping
    virtual void set_sleeping_allowed(bool allowed) = 0;
    virtual bool is_sleeping_allowed() const = 0;
    virtual void set_sleep_threshold(float threshold) = 0;
    virtual float get_sleep_threshold() const = 0;
    virtual void wake_up() = 0;
    virtual void put_to_sleep() = 0;
    virtual bool is_sleeping() const = 0;

    // Collision filter
    virtual void set_collision_filter(const CollisionFilter& filter) = 0;
    virtual const CollisionFilter& get_collision_filter() const = 0;

    // Colliders
    virtual void add_collider(uint32_t collider_id) = 0;
    virtual void remove_collider(uint32_t collider_id) = 0;
    virtual std::vector<uint32_t> get_colliders() const = 0;

    // Forces
    virtual void apply_force(float force_x, float force_y, float force_z) = 0;
    virtual void apply_force_at_point(float force_x, float force_y, float force_z,
                                   float point_x, float point_y, float point_z) = 0;
    virtual void apply_impulse(float impulse_x, float impulse_y, float impulse_z) = 0;
    virtual void apply_impulse_at_point(float impulse_x, float impulse_y, float impulse_z,
                                      float point_x, float point_y, float point_z) = 0;
    virtual void apply_torque(float torque_x, float torque_y, float torque_z) = 0;
    virtual void apply_torque_impulse(float torque_x, float torque_y, float torque_z) = 0;

    // Clear forces
    virtual void clear_forces() = 0;
    virtual void clear_torques() = 0;
    virtual void clear_forces_and_torques() = 0;
};

// Collider interface
class ICollider {
public:
    virtual ~ICollider() = default;

    virtual uint32_t get_id() const = 0;

    // Shape type
    virtual void set_shape_type(CollisionShapeType type) = 0;
    virtual CollisionShapeType get_shape_type() const = 0;

    // Shape parameters
    virtual void set_box_shape(float half_extents_x, float half_extents_y, float half_extents_z) = 0;
    virtual void set_sphere_shape(float radius) = 0;
    virtual void set_capsule_shape(float radius, float height) = 0;
    virtual void set_cylinder_shape(float radius, float height) = 0;
    virtual void set_cone_shape(float radius, float height) = 0;
    virtual void set_mesh_shape(const void* vertices, size_t vertex_count, const void* indices, size_t index_count) = 0;

    // Transform
    virtual void set_local_position(float x, float y, float z) = 0;
    virtual void get_local_position(float& x, float& y, float& z) const = 0;
    virtual void set_local_rotation(float quaternion_x, float quaternion_y, float quaternion_z, float quaternion_w) = 0;
    virtual void get_local_rotation(float& quaternion_x, float& quaternion_y, float& quaternion_z, float& quaternion_w) const = 0;

    // Material
    virtual void set_material(uint32_t material_id) = 0;
    virtual uint32_t get_material() const = 0;

    // Trigger
    virtual void set_is_trigger(bool is_trigger) = 0;
    virtual bool is_trigger() const = 0;

    // Collision filter
    virtual void set_collision_filter(const CollisionFilter& filter) = 0;
    virtual const CollisionFilter& get_collision_filter() const = 0;
};

// Physics material interface
class IPhysicsMaterial {
public:
    virtual ~IPhysicsMaterial() = default;

    virtual uint32_t get_id() const = 0;

    // Friction
    virtual void set_static_friction(float friction) = 0;
    virtual float get_static_friction() const = 0;
    virtual void set_dynamic_friction(float friction) = 0;
    virtual float get_dynamic_friction() const = 0;

    // Restitution
    virtual void set_restitution(float restitution) = 0;
    virtual float get_restitution() const = 0;

    // Friction combine mode
    enum class FrictionCombineMode {
        AVERAGE,
        MIN,
        MAX,
        MULTIPLY
    };
    virtual void set_friction_combine_mode(FrictionCombineMode mode) = 0;
    virtual FrictionCombineMode get_friction_combine_mode() const = 0;

    // Restitution combine mode
    enum class RestitutionCombineMode {
        AVERAGE,
        MIN,
        MAX,
        MULTIPLY
    };
    virtual void set_restitution_combine_mode(RestitutionCombineMode mode) = 0;
    virtual RestitutionCombineMode get_restitution_combine_mode() const = 0;
};

// Joint interface
class IJoint {
public:
    virtual ~IJoint() = default;

    virtual uint32_t get_id() const = 0;

    // Type
    virtual void set_type(JointType type) = 0;
    virtual JointType get_type() const = 0;

    // Bodies
    virtual void set_body_a(uint32_t body_id) = 0;
    virtual uint32_t get_body_a() const = 0;
    virtual void set_body_b(uint32_t body_id) = 0;
    virtual uint32_t get_body_b() const = 0;

    // Anchor points
    virtual void set_anchor_a(float x, float y, float z) = 0;
    virtual void get_anchor_a(float& x, float& y, float& z) const = 0;
    virtual void set_anchor_b(float x, float y, float z) = 0;
    virtual void get_anchor_b(float& x, float& y, float& z) const = 0;

    // Limits
    virtual void set_lower_limit(float limit) = 0;
    virtual float get_lower_limit() const = 0;
    virtual void set_upper_limit(float limit) = 0;
    virtual float get_upper_limit() const = 0;

    // Motor
    virtual void enable_motor(bool enabled) = 0;
    virtual bool is_motor_enabled() const = 0;
    virtual void set_motor_speed(float speed) = 0;
    virtual float get_motor_speed() const = 0;
    virtual void set_max_motor_force(float force) = 0;
    virtual float get_max_motor_force() const = 0;

    // Spring
    virtual void enable_spring(bool enabled) = 0;
    virtual bool is_spring_enabled() const = 0;
    virtual void set_stiffness(float stiffness) = 0;
    virtual float get_stiffness() const = 0;
    virtual void set_damping(float damping) = 0;
    virtual float get_damping() const = 0;

    // Breakable
    virtual void set_breakable(bool breakable) = 0;
    virtual bool is_breakable() const = 0;
    virtual void set_break_force(float force) = 0;
    virtual float get_break_force() const = 0;
    virtual void set_break_torque(float torque) = 0;
    virtual float get_break_torque() const = 0;
};

// Physics engine factory
class IPhysicsEngineFactory {
public:
    virtual ~IPhysicsEngineFactory() = default;

    virtual std::unique_ptr<IPhysicsEngine> create_physics_engine() = 0;
    virtual void destroy_physics_engine(std::unique_ptr<IPhysicsEngine> physics_engine) = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_PHYSICS_ENGINE_INTERFACE_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects

## Related Requirements
- REQ-039: Physics System Architecture
- REQ-040: Collision Detection

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Physics Engine Design
1. Abstract physics API
2. Support multiple backends (Bullet, PhysX, Box2D)
3. Efficient collision detection
4. Rigid body dynamics

### Rigid Bodies
1. Create and destroy bodies
2. Set body type (static, kinematic, dynamic)
3. Control position and rotation
4. Apply forces and impulses

### Colliders
1. Create collision shapes
2. Support multiple shape types
3. Local transform
4. Trigger colliders

### Joints
1. Create constraints
2. Support multiple joint types
3. Limits and motors
4. Breakable joints

### Collision Detection
1. Raycasting
2. Sweep tests
3. Overlap tests
4. Collision events

## Usage Example

```cpp
#include "physics_engine_interface.hpp"

using namespace omnicpp::engine;

int main() {
    // Create physics configuration
    PhysicsConfig config;
    config.gravity_x = 0.0f;
    config.gravity_y = -9.81f;
    config.gravity_z = 0.0f;
    config.solver_iterations = 10;
    config.enable_sleeping = true;
    config.fixed_time_step = 1.0f / 60.0f;

    // Create physics engine
    auto physics_engine = std::make_unique<PhysicsEngine>();

    // Initialize physics engine
    if (!physics_engine->initialize(config)) {
        std::cerr << "Failed to initialize physics engine" << std::endl;
        return 1;
    }

    // Create physics material
    uint32_t material_id = physics_engine->create_physics_material(0.5f, 0.5f, 0.0f);

    // Create rigid body
    uint32_t body_id = physics_engine->create_rigid_body(BodyType::DYNAMIC);
    IRigidBody* body = physics_engine->get_rigid_body(body_id);

    // Set position
    body->set_position(0.0f, 10.0f, 0.0f);

    // Set mass
    body->set_mass(1.0f);

    // Create collider
    uint32_t collider_id = physics_engine->create_collider(CollisionShapeType::BOX);
    ICollider* collider = physics_engine->get_collider(collider_id);

    // Set box shape
    collider->set_box_shape(0.5f, 0.5f, 0.5f);

    // Set material
    collider->set_material(material_id);

    // Add collider to body
    body->add_collider(collider_id);

    // Set collision callback
    physics_engine->set_collision_callback([](const CollisionEvent& event) {
        // Handle collision
    });

    // Update physics
    double delta_time = 0.016; // 60 FPS
    physics_engine->update(delta_time);

    // Cleanup
    physics_engine->destroy_rigid_body(body_id);
    physics_engine->destroy_collider(collider_id);
    physics_engine->destroy_physics_material(material_id);
    physics_engine->shutdown();

    return 0;
}
```
