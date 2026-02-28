/**
 * @file window_manager.hpp
 * @brief Window management interface
 */

#pragma once

#include <cstdint>
#include <functional>
#include <memory>
#include <string>

#ifdef OMNICPP_HAS_GLFW
#include <GLFW/glfw3.h>
#endif

#ifdef OMNICPP_HAS_VULKAN
#include <vulkan/vulkan.h>
#endif

#ifdef OMNICPP_HAS_QT_VULKAN
#include <QWindow>
#include <QVulkanInstance>
#include <QGuiApplication>
#endif

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

#ifdef OMNICPP_HAS_GLFW
    [[nodiscard]] GLFWwindow* get_glfw_window () const;
#endif

#ifdef OMNICPP_HAS_VULKAN
    [[nodiscard]] VkSurfaceKHR get_vulkan_surface (VkInstance instance) const;
#endif

#ifdef OMNICPP_HAS_QT_VULKAN
    /**
     * @brief Set Qt6 application instance (must be called before initialize)
     * @param app The QGuiApplication instance (must exist for the lifetime of window manager)
     */
    void set_qt_application (QGuiApplication* app);

    /**
     * @brief Set window close callback (must be called before initialize)
     * @param callback The callback function to invoke when window is closed
     */
    void set_close_callback (std::function<void()> callback);

    /**
     * @brief Request window to be shown and brought to front
     * @note On Wayland, this requests the compositor to show the window
     * @note On X11, this restores the window from minimized state
     */
    void request_window_visibility ();

    [[nodiscard]] QVulkanInstance* get_qt_vulkan_instance () const;
    [[nodiscard]] QWindow* get_qt_window () const;
#endif

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Window
