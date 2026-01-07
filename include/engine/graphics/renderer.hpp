/**
 * @file renderer.hpp
 * @brief Graphics renderer interface
 */

#pragma once

#include <cstdint>
#include <memory>

namespace OmniCpp::Engine::Graphics {

  /**
   * @brief Renderer configuration structure
   */
  struct RendererConfig {
    bool vsync{ true };
    uint32_t msaa_samples{ 4 };
    bool enable_debug{ false };
  };

  /**
   * @brief Renderer class
   */
  class Renderer {
  public:
    Renderer ();
    ~Renderer ();

    Renderer (const Renderer&) = delete;
    Renderer& operator= (const Renderer&) = delete;

    Renderer (Renderer&&) noexcept;
    Renderer& operator= (Renderer&&) noexcept;

    bool initialize (const RendererConfig& config);
    void shutdown ();
    void update ();
    void render ();

    void clear ();
    void present ();

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Graphics
