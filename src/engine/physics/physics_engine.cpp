/**
 * @file physics_engine.cpp
 * @brief Physics engine implementation
 */

#include "engine/physics/physics_engine.hpp"
#include <mutex>

namespace OmniCpp::Engine::Physics {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct PhysicsEngine::Impl {
    PhysicsConfig config;
    std::mutex mutex;
    bool initialized{ false };
  };

  PhysicsEngine::PhysicsEngine () : m_impl (std::make_unique<Impl> ()) {
  }

  PhysicsEngine::~PhysicsEngine () {
    shutdown ();
  }

  PhysicsEngine::PhysicsEngine (PhysicsEngine&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
  }

  PhysicsEngine& PhysicsEngine::operator= (PhysicsEngine&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool PhysicsEngine::initialize (const PhysicsConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->config = config;
    m_impl->initialized = true;

    return true;
  }

  void PhysicsEngine::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->initialized = false;
  }

  void PhysicsEngine::update (float delta_time) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update physics simulation here
  }

  void PhysicsEngine::set_gravity (float gravity) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    m_impl->config.gravity = gravity;
  }

  float PhysicsEngine::get_gravity () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->config.gravity;
  }

} // namespace OmniCpp::Engine::Physics
