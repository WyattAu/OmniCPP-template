/**
 * @file vulkan_window.cpp
 * @brief Qt6 Vulkan window class implementation with input handling
 * @version 1.0.0
 */

#include "engine/window/vulkan_window.hpp"
#include "engine/logging/Log.hpp"
#include <QMouseEvent>
#include <QWheelEvent>
#include <QFocusEvent>
#include <functional>

namespace OmniCpp::Engine::Window {

  VulkanWindow::VulkanWindow (QWindow* parent) : QWindow (parent) {
    // Configure surface type for Vulkan rendering
    setSurfaceType (QSurface::VulkanSurface);

    // Set window flags for proper Wayland support
    setFlags(Qt::Window | Qt::WindowCloseButtonHint);

    omnicpp::log::info ("VulkanWindow: Created Qt6 Vulkan window with input tracking");
  }

  void VulkanWindow::set_close_callback (CloseCallback callback) {
    m_close_callback = std::move(callback);
  }

  bool VulkanWindow::event (QEvent* event) {
    // Handle Qt events
    switch (event->type ()) {
      case QEvent::Close:
        omnicpp::log::info ("VulkanWindow: Close event received");
        // Invoke close callback if registered
        if (m_close_callback) {
          m_close_callback();
        }
        return QWindow::event (event);

      default:
        return QWindow::event (event);
    }
  }

  void VulkanWindow::resizeEvent (QResizeEvent* event) {
    // Handle window resize events
    QWindow::resizeEvent (event);

    omnicpp::log::info ("VulkanWindow: Resized to {}x{}", width (), height ());

    // Notify resize callback if registered
    if (m_resize_callback) {
      m_resize_callback(width(), height());
    }
  }

  void VulkanWindow::keyPressEvent (QKeyEvent* event) {
    // Handle key press events for interactivity
    QWindow::keyPressEvent (event);

    // Log key press for debugging
    omnicpp::log::debug ("VulkanWindow: Key pressed: {}", event->key ());

    // Handle key press events for game input
    if (m_key_press_callback) {
      m_key_press_callback(event->key());
    }

    // Handle ESC key to close window
    if (event->key () == Qt::Key_Escape) {
      omnicpp::log::info ("VulkanWindow: ESC key pressed, closing window");
      close();
      // Invoke close callback if registered
      if (m_close_callback) {
        m_close_callback();
      }
    }
  }

  void VulkanWindow::keyReleaseEvent (QKeyEvent* event) {
    // Handle key release events for interactivity
    QWindow::keyReleaseEvent (event);

    // Log key release for debugging
    omnicpp::log::debug ("VulkanWindow: Key released: {}", event->key ());

    // Handle key release events for game input
    if (m_key_release_callback) {
      m_key_release_callback(event->key());
    }
  }

  void VulkanWindow::mousePressEvent (QMouseEvent* event) {
    // Handle mouse press events for interactivity
    QWindow::mousePressEvent (event);

    // Log mouse press for debugging
    omnicpp::log::debug ("VulkanWindow: Mouse press at ({}, {})", event->position ().x (), event->position ().y ());

    // Handle mouse button press events for game input
    if (m_mouse_press_callback) {
      m_mouse_press_callback(event->position().x(), event->position().y());
    }
  }

  void VulkanWindow::mouseReleaseEvent (QMouseEvent* event) {
    // Handle mouse release events for interactivity
    QWindow::mouseReleaseEvent (event);

    // Log mouse release for debugging
    omnicpp::log::debug ("VulkanWindow: Mouse release at ({}, {})", event->position ().x (), event->position ().y ());

    // Handle mouse button release events for game input
    if (m_mouse_release_callback) {
      m_mouse_release_callback(event->position().x(), event->position().y());
    }
  }

  void VulkanWindow::mouseMoveEvent (QMouseEvent* event) {
    // Handle mouse move events for interactivity
    QWindow::mouseMoveEvent (event);

    // Handle mouse move events for game input
    if (m_mouse_move_callback) {
      m_mouse_move_callback(event->position().x(), event->position().y());
    }

    // Log mouse move for debugging (only log occasionally to avoid spam)
    static int move_count = 0;
    if (++move_count % 100 == 0) {
      omnicpp::log::debug ("VulkanWindow: Mouse move at ({}, {})", event->position ().x (), event->position ().y ());
    }
  }

  void VulkanWindow::wheelEvent (QWheelEvent* event) {
    // Handle mouse wheel events for interactivity
    QWindow::wheelEvent (event);

    // Log mouse wheel for debugging
    omnicpp::log::debug ("VulkanWindow: Mouse wheel delta: ({}, {})", event->angleDelta ().x (), event->angleDelta ().y ());
  }

  void VulkanWindow::focusInEvent (QFocusEvent* event) {
    // Handle focus in events for interactivity
    QWindow::focusInEvent (event);

    // Log focus in for debugging
    omnicpp::log::info ("VulkanWindow: Window gained focus");
  }

  void VulkanWindow::focusOutEvent (QFocusEvent* event) {
    // Handle focus out events for interactivity
    QWindow::focusOutEvent (event);

    // Log focus out for debugging
    omnicpp::log::info ("VulkanWindow: Window lost focus");
  }

  void VulkanWindow::set_key_press_callback (KeyCallback callback) {
    m_key_press_callback = std::move(callback);
  }

  void VulkanWindow::set_key_release_callback (KeyCallback callback) {
    m_key_release_callback = std::move(callback);
  }

  void VulkanWindow::set_mouse_move_callback (MouseCallback callback) {
    m_mouse_move_callback = std::move(callback);
  }

  void VulkanWindow::set_mouse_press_callback (MouseCallback callback) {
    m_mouse_press_callback = std::move(callback);
  }

  void VulkanWindow::set_mouse_release_callback (MouseCallback callback) {
    m_mouse_release_callback = std::move(callback);
  }

  void VulkanWindow::set_resize_callback (ResizeCallback callback) {
    m_resize_callback = std::move(callback);
  }

} // namespace OmniCpp::Engine::Window
