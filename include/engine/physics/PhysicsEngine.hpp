/**
 * @file PhysicsEngine.hpp
 * @brief Physics engine for simulation
 * @version 1.0.0
 */

#pragma once

#include <vector>
#include <memory>

namespace omnicpp {
namespace physics {

// Forward declarations
class CollisionDetection;
class RigidBody;

/**
 * @brief Physics engine for simulation
 * 
 * Handles physics simulation and collision detection.
 */
class PhysicsEngine {
public:
    /**
     * @brief Construct a new Physics Engine object
     */
    PhysicsEngine() = default;

    /**
     * @brief Destroy the Physics Engine object
     */
    ~PhysicsEngine() = default;

    // Disable copying
    PhysicsEngine(const PhysicsEngine&) = delete;
    PhysicsEngine& operator=(const PhysicsEngine&) = delete;

    // Enable moving
    PhysicsEngine(PhysicsEngine&&) noexcept = default;
    PhysicsEngine& operator=(PhysicsEngine&&) noexcept = default;

    /**
     * @brief Initialize physics engine
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown physics engine
     */
    void shutdown();

    /**
     * @brief Update physics simulation
     * @param delta_time Time since last frame in seconds
     */
    void update(float delta_time);

    /**
     * @brief Add a rigid body to simulation
     * @param body Pointer to rigid body
     */
    void add_rigid_body(RigidBody* body);

    /**
     * @brief Remove a rigid body from simulation
     * @param body Pointer to rigid body
     */
    void remove_rigid_body(RigidBody* body);

    /**
     * @brief Get all rigid bodies
     * @return const std::vector<RigidBody*>& The rigid bodies
     */
    const std::vector<RigidBody*>& get_rigid_bodies() const { return m_rigid_bodies; }

    /**
     * @brief Get collision detection system
     * @return CollisionDetection* Pointer to collision detection
     */
    CollisionDetection* get_collision_detection() const { return m_collision_detection.get(); }

    /**
     * @brief Set gravity
     * @param x X component of gravity
     * @param y Y component of gravity
     * @param z Z component of gravity
     */
    void set_gravity(float x, float y, float z);

    /**
     * @brief Get gravity
     * @param x Output X component
     * @param y Output Y component
     * @param z Output Z component
     */
    void get_gravity(float& x, float& y, float& z) const;

    /**
     * @brief Set simulation step size
     * @param step_size The step size in seconds
     */
    void set_step_size(float step_size) { m_step_size = step_size; }

    /**
     * @brief Get simulation step size
     * @return float The step size in seconds
     */
    float get_step_size() const { return m_step_size; }

private:
    std::vector<RigidBody*> m_rigid_bodies;
    std::unique_ptr<CollisionDetection> m_collision_detection;
    float m_gravity_x = 0.0f;
    float m_gravity_y = -9.81f;
    float m_gravity_z = 0.0f;
    float m_step_size = 1.0f / 60.0f;
};

} // namespace physics
} // namespace omnicpp
