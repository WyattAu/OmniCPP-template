/**
 * @file IPhysicsEngine.hpp
 * @brief Physics engine subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for physics simulation.
 */

#ifndef OMNICPP_IPHYSICS_ENGINE_HPP
#define OMNICPP_IPHYSICS_ENGINE_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Physics engine interface
 */
class IPhysicsEngine {
public:
    virtual ~IPhysicsEngine() = default;
    
    /**
     * @brief Initialize physics engine
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown physics engine
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Update physics simulation
     * 
     * @param delta_time Time since last frame in seconds
     */
    virtual void update(float delta_time) = 0;
    
    /**
     * @brief Create a rigid body
     * 
     * @param mass Mass of the body
     * @param position Initial position
     * @return Body ID, or 0 on failure
     */
    virtual uint32_t create_rigid_body(float mass, const float* position) = 0;
    
    /**
     * @brief Create a dynamic body
     * 
     * @param mass Mass of the body
     * @param position Initial position
     * @return Body ID, or 0 on failure
     */
    virtual uint32_t create_dynamic_body(float mass, const float* position) = 0;
    
    /**
     * @brief Destroy a body
     * 
     * @param body_id Body ID to destroy
     */
    virtual void destroy_body(uint32_t body_id) = 0;
    
    /**
     * @brief Apply force to a body
     * 
     * @param body_id Body ID
     * @param force Force vector
     * @param duration Duration in seconds
     */
    virtual void apply_force(uint32_t body_id, const float* force, float duration) = 0;
    
    /**
     * @brief Set gravity
     * 
     * @param gravity Gravity vector (x, y, z)
     */
    virtual void set_gravity(const float* gravity) = 0;
    
    /**
     * @brief Get gravity
     * 
     * @return Current gravity vector
     */
    virtual void get_gravity(float* out_gravity) const = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IPHYSICS_ENGINE_HPP
