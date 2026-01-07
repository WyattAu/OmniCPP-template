/**
 * @file window_manager.hpp
 * @brief Window management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Window {

  /**
   * @brief Window configuration structure
   */
  struct WindowConfig {
    std::string title{ "OmniCpp Engine" };
    uint32_t width{ 1280 };
    uint32_t height{ 720 };
    bool fullscreen{ false };
    bool vsync{ true };
    bool resizable{ true };
  };

  /**
   * @brief Window manager class
   */
  class WindowManager {
  public:
    WindowManager ();
    ~WindowManager ();

    WindowManager (const WindowManager&) = delete;
    WindowManager& operator= (const WindowManager&) = delete;

    WindowManager (WindowManager&&) noexcept;
    WindowManager& operator= (WindowManager&&) noexcept;

    bool initialize (const WindowConfig& config);
    void shutdown ();
    void update ();

    [[nodiscard]] bool should_close () const;
    void swap_buffers ();
    void poll_events ();

    [[nodiscard]] uint32_t get_width () const;
    [[nodiscard]] uint32_t get_height () const;
    [[nodiscard]] const std::string& get_title () const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Window
