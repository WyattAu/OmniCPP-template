/**
 * @file physics_engine.hpp
 * @brief Physics engine interface
 */

#pragma once

#include <cstdint>
#include <memory>

namespace OmniCpp::Engine::Physics {

  /**
   * @brief Physics configuration structure
   */
  struct PhysicsConfig {
    float gravity{ 9.81f };
    uint32_t max_substeps{ 8 };
    float fixed_timestep{ 1.0f / 60.0f };
  };

  /**
   * @brief Physics engine class
   */
  class PhysicsEngine {
  public:
    PhysicsEngine ();
    ~PhysicsEngine ();

    PhysicsEngine (const PhysicsEngine&) = delete;
    PhysicsEngine& operator= (const PhysicsEngine&) = delete;

    PhysicsEngine (PhysicsEngine&&) noexcept;
    PhysicsEngine& operator= (PhysicsEngine&&) noexcept;

    bool initialize (const PhysicsConfig& config);
    void shutdown ();
    void update (float delta_time);

    void set_gravity (float gravity);
    [[nodiscard]] float get_gravity () const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Physics
