/**
 * @file vulkan_window.hpp
 * @brief Qt6 Vulkan window class with input handling
 * @version 1.0.0
 */

#pragma once

#include <QWindow>
#include <QResizeEvent>
#include <QCloseEvent>
#include <QKeyEvent>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QFocusEvent>
#include <functional>

namespace OmniCpp::Engine::Window {

  /**
   * @brief Callback types for input handling
   */
  using CloseCallback = std::function<void()>;
  using KeyCallback = std::function<void(int)>;
  using MouseCallback = std::function<void(float, float)>;
  using ResizeCallback = std::function<void(int, int)>;

  /**
   * @brief Custom QWindow for Vulkan rendering
   * This window is used with QVulkanInstance for surface creation
   */
  class VulkanWindow : public QWindow {
  public:
    explicit VulkanWindow(QWindow* parent = nullptr);
    ~VulkanWindow() override = default;

    bool event(QEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;
    void keyPressEvent(QKeyEvent* event) override;
    void keyReleaseEvent(QKeyEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void wheelEvent(QWheelEvent* event) override;
    void focusInEvent(QFocusEvent* event) override;
    void focusOutEvent(QFocusEvent* event) override;

    // Set callback to be invoked when window is closed
    void set_close_callback(CloseCallback callback);

    // Input callbacks for game integration
    void set_key_press_callback(KeyCallback callback);
    void set_key_release_callback(KeyCallback callback);
    void set_mouse_move_callback(MouseCallback callback);
    void set_mouse_press_callback(MouseCallback callback);
    void set_mouse_release_callback(MouseCallback callback);
    void set_resize_callback(ResizeCallback callback);

  private:
    CloseCallback m_close_callback;
    KeyCallback m_key_press_callback;
    KeyCallback m_key_release_callback;
    MouseCallback m_mouse_move_callback;
    MouseCallback m_mouse_press_callback;
    MouseCallback m_mouse_release_callback;
    ResizeCallback m_resize_callback;
  };

} // namespace OmniCpp::Engine::Window
