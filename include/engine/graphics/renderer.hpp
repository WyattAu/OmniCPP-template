/**
 * @file renderer.hpp
 * @brief Graphics renderer interface with Vulkan 3D rendering support
 */

#pragma once

#include <cstdint>
#include <memory>

namespace OmniCpp::Engine {
  namespace Window {
    class WindowManager;
  }
}

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
   * @brief Renderer class for Vulkan 3D graphics rendering
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

    void set_window_manager (Window::WindowManager* window_manager);
    void set_ball_position(float x, float y);
    void set_paddle_position(bool is_left, float y);
    [[nodiscard]] uint32_t get_frame_count () const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Graphics
