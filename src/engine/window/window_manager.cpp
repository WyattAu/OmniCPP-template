/**
 * @file window_manager.cpp
 * @brief Window management implementation with Qt6 and Vulkan support
 */

#include "engine/window/window_manager.hpp"
#include "engine/window/vulkan_window.hpp"
#include <QGuiApplication>
#include <QVulkanInstance>
#include <QWindow>
#include <mutex>
#include "engine/logging/Log.hpp"
#include <cstring>

namespace OmniCpp::Engine::Window {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct WindowManager::Impl {
    WindowConfig config;
    QGuiApplication* qt_application{ nullptr };
    VulkanWindow* qt_window{ nullptr };
    QVulkanInstance* qt_vulkan_instance{ nullptr };
    std::function<void()> close_callback;
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

#ifdef OMNICPP_HAS_QT_VULKAN
  void WindowManager::set_qt_application (QGuiApplication* app) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    m_impl->qt_application = app;
  }

  void WindowManager::set_close_callback (std::function<void()> callback) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    m_impl->close_callback = std::move(callback);
  }

  void WindowManager::request_window_visibility () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    if (m_impl->qt_window) {
      m_impl->qt_window->show();
      m_impl->qt_window->raise();
      m_impl->qt_window->requestActivate();
    }
  }

  QVulkanInstance* WindowManager::get_qt_vulkan_instance () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->qt_vulkan_instance;
  }

  QWindow* WindowManager::get_qt_window () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->qt_window;
  }
#endif

  bool WindowManager::initialize (const WindowConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      omnicpp::log::warn("WindowManager: Already initialized");
      return true;
    }

    m_impl->config = config;
    m_impl->should_close = false;

#ifdef OMNICPP_HAS_QT_VULKAN
    // Detect platform
    const char* qt_platform = std::getenv("QT_QPA_PLATFORM");
    bool is_wayland = (qt_platform && (std::strcmp(qt_platform, "wayland") == 0));
    
    if (is_wayland) {
      omnicpp::log::info("WindowManager: Wayland platform detected");
    } else {
      omnicpp::log::info("WindowManager: Qt Platform: {}", qt_platform ? qt_platform : "default");
    }

    // Validate Qt application is set
    if (!m_impl->qt_application) {
      omnicpp::log::error("WindowManager: Qt application not set. Call set_qt_application() before initialize()");
      return false;
    }

    // Create Qt Vulkan instance
    m_impl->qt_vulkan_instance = new QVulkanInstance();
    
    // Use Vulkan 1.2 for broad compatibility
    m_impl->qt_vulkan_instance->setApiVersion(QVersionNumber(1, 2));
    
    // Configure extensions for surface support
    // Request common surface extensions that Qt needs
    QByteArrayList extensions;
    extensions << "VK_KHR_surface";
    extensions << "VK_KHR_xcb_surface";
    extensions << "VK_KHR_xlib_surface";
    m_impl->qt_vulkan_instance->setExtensions(extensions);
    
    // Create the Vulkan instance
    if (!m_impl->qt_vulkan_instance->create()) {
      omnicpp::log::error("WindowManager: Failed to create Qt Vulkan instance");
      omnicpp::log::error("  This usually means Vulkan drivers are not installed or accessible");
      omnicpp::log::error("  Try: vulkaninfo | head -20");
      delete m_impl->qt_vulkan_instance;
      m_impl->qt_vulkan_instance = nullptr;
      return false;
    }
    omnicpp::log::info("WindowManager: Qt Vulkan instance created successfully");
    omnicpp::log::info("WindowManager: Supported API version: {}.{}.{}", 
                 m_impl->qt_vulkan_instance->supportedApiVersion().majorVersion(),
                 m_impl->qt_vulkan_instance->supportedApiVersion().minorVersion(),
                 m_impl->qt_vulkan_instance->supportedApiVersion().microVersion());

    // Create Vulkan window
    m_impl->qt_window = new VulkanWindow();
    
    // IMPORTANT: Associate the window with the Vulkan instance
    m_impl->qt_window->setVulkanInstance(m_impl->qt_vulkan_instance);
    
    // Set close callback
    if (m_impl->close_callback) {
      m_impl->qt_window->set_close_callback([this]() {
        std::lock_guard<std::mutex> lock(m_impl->mutex);
        m_impl->should_close = true;
        omnicpp::log::info("WindowManager: Window closed by user");
        if (m_impl->close_callback) {
          m_impl->close_callback();
        }
      });
    }

    // Configure window
    m_impl->qt_window->setTitle(QString::fromStdString(config.title));
    m_impl->qt_window->resize(static_cast<int>(config.width), static_cast<int>(config.height));

    // Show window - must be visible for Vulkan surface creation
    if (config.fullscreen) {
      m_impl->qt_window->showFullScreen();
    } else {
      m_impl->qt_window->show();
    }
    
    // Process events to ensure window is realized
    for (int i = 0; i < 3; i++) {
      m_impl->qt_application->processEvents();
    }

    // Handle platform-specific window state
    if (!is_wayland) {
      m_impl->qt_window->setWindowState(Qt::WindowNoState);
      omnicpp::log::info("WindowManager: Window state set to normal (not minimized)");
    } else {
      omnicpp::log::info("WindowManager: Wayland detected - skipping setWindowState()");
    }

    // Ensure window is visible
    m_impl->qt_window->raise();
    m_impl->qt_window->requestActivate();

    omnicpp::log::info("WindowManager: Qt Vulkan window created and shown ({}x{})", config.width, config.height);

    if (is_wayland) {
      omnicpp::log::info("WindowManager: Window is visible on Wayland compositor");
    }
#endif

    m_impl->initialized = true;
    omnicpp::log::info("WindowManager: Initialized with title '{}', size {}x{}", config.title, config.width, config.height);
    return true;
  }

  void WindowManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

#ifdef OMNICPP_HAS_QT_VULKAN
    // Clean up Vulkan window
    if (m_impl->qt_window) {
      omnicpp::log::info("WindowManager: Destroying Qt Vulkan window");
      delete m_impl->qt_window;
      m_impl->qt_window = nullptr;
    }

    // Clean up Vulkan instance
    if (m_impl->qt_vulkan_instance) {
      omnicpp::log::info("WindowManager: Destroying Qt Vulkan instance");
      delete m_impl->qt_vulkan_instance;
      m_impl->qt_vulkan_instance = nullptr;
    }
#endif

    m_impl->initialized = false;
    omnicpp::log::info("WindowManager: Shutdown");
  }

  void WindowManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

#ifdef OMNICPP_HAS_QT_VULKAN
    // Process Qt events
    if (m_impl->qt_application) {
      m_impl->qt_application->processEvents();
    }
#endif
  }

  bool WindowManager::should_close () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->should_close;
  }

  void WindowManager::swap_buffers () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Swap buffers here - handled by Vulkan renderer
  }

  void WindowManager::poll_events () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Poll events here - handled by Qt processEvents in update()
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
