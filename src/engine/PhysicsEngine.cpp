/**
 * @file PhysicsEngine.cpp
 * @brief Stub implementation of physics engine subsystem
 * @version 1.0.0
 */

#include "engine/IPhysicsEngine.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {

class PhysicsEngineStub : public IPhysicsEngine {
public:
    PhysicsEngineStub() = default;
    ~PhysicsEngineStub() override = default;

    bool initialize() override {
        omnicpp::log::info("PhysicsEngineStub: Initialized");
        return true;
    }

    void shutdown() override {
        omnicpp::log::info("PhysicsEngineStub: Shutdown");
    }

    void update(float delta_time) override {
        (void)delta_time;
    }

    uint32_t create_rigid_body(float mass, const float* position) override {
        omnicpp::log::debug("PhysicsEngineStub: Creating rigid body with mass {}", mass);
        (void)mass;
        (void)position;
        return 0;
    }

    uint32_t create_dynamic_body(float mass, const float* position) override {
        omnicpp::log::debug("PhysicsEngineStub: Creating dynamic body with mass {}", mass);
        (void)mass;
        (void)position;
        return 0;
    }

    void destroy_body(uint32_t body_id) override {
        omnicpp::log::debug("PhysicsEngineStub: Destroying body {}", body_id);
        (void)body_id;
    }

    void apply_force(uint32_t body_id, const float* force, float duration) override {
        omnicpp::log::debug("PhysicsEngineStub: Applying force to body {} for {} seconds", body_id, duration);
        (void)body_id;
        (void)force;
        (void)duration;
    }

    void set_gravity(const float* gravity) override {
        omnicpp::log::debug("PhysicsEngineStub: Setting gravity to ({}, {}, {})", gravity[0], gravity[1], gravity[2]);
        (void)gravity;
    }

    void get_gravity(float* out_gravity) const override {
        if (out_gravity) {
            out_gravity[0] = 0.0f;
            out_gravity[1] = -9.81f;
            out_gravity[2] = 0.0f;
        }
    }
};

} // namespace omnicpp
