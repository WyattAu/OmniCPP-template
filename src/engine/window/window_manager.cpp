/**
 * @file window_manager.cpp
 * @brief Window management implementation
 */

#include "engine/window/window_manager.hpp"
#include <mutex>

namespace OmniCpp::Engine::Window {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct WindowManager::Impl {
    WindowConfig config;
    bool should_close{ false };
    std::mutex mutex;
    bool initialized{ false };
  };

  WindowManager::WindowManager () : m_impl (std::make_unique<Impl> ()) {
  }

  WindowManager::~WindowManager () {
    shutdown ();
  }

  WindowManager::WindowManager (WindowManager&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
  }

  WindowManager& WindowManager::operator= (WindowManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool WindowManager::initialize (const WindowConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->config = config;
    m_impl->should_close = false;
    m_impl->initialized = true;

    return true;
  }

  void WindowManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->initialized = false;
  }

  void WindowManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update window state here
  }

  bool WindowManager::should_close () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->should_close;
  }

  void WindowManager::swap_buffers () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Swap buffers here
  }

  void WindowManager::poll_events () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Poll events here
  }

  uint32_t WindowManager::get_width () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->config.width;
  }

  uint32_t WindowManager::get_height () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->config.height;
  }

  const std::string& WindowManager::get_title () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->config.title;
  }

} // namespace OmniCpp::Engine::Window
