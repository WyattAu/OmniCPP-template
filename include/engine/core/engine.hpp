/**
 * @file engine.hpp
 * @brief Core engine interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Core {

  /**
   * @brief Engine configuration structure
   */
  struct EngineConfig {
    uint32_t max_fps{ 60 };
    float fixed_timestep{ 0.01667f }; // ~60 FPS
    bool enable_profiling{ false };
  };

  /**
   * @brief Core engine class
   * 
   * Manages main game loop, initialization, and shutdown of all engine subsystems.
   * Follows C++23 best practices with RAII and move semantics.
   */
  class Engine {
  public:
    Engine ();
    ~Engine ();

    // Delete copy operations (C++23 best practice)
    Engine (const Engine&) = delete;
    Engine& operator= (const Engine&) = delete;

    // Enable move operations (C++23 best practice)
    Engine (Engine&&) noexcept;
    Engine& operator= (Engine&&) noexcept;

    /**
     * @brief Initialize engine with configuration
     * @param config Engine configuration
     * @return true if successful, false otherwise
     */
    bool initialize (const EngineConfig& config);

    /**
     * @brief Run engine main loop
     * 
     * This method blocks until engine is shut down.
     */
    void run ();

    /**
     * @brief Shutdown engine and all subsystems
     */
    void shutdown ();

    /**
     * @brief Update engine state
     * @param deltaTime Time since last update in seconds
     */
    void update (float deltaTime);

    /**
     * @brief Render current frame
     */
    void render ();

    /**
     * @brief Check if engine is running
     * @return true if running, false otherwise
     */
    [[nodiscard]] bool is_running () const noexcept;

    /**
     * @brief Get engine configuration
     * @return Current engine configuration
     */
    [[nodiscard]] const EngineConfig& get_config () const noexcept;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl; // Pimpl idiom for ABI stability
  };

} // namespace OmniCpp::Engine::Core
