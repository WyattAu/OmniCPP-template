/**
 * @file platform.cpp
 * @brief Platform abstraction implementation
 */

#include "engine/platform/platform.hpp"
#include <chrono>
#include <mutex>
#include <spdlog/spdlog.h>

#ifdef _WIN32
  #include <windows.h>
#else
  #include <unistd.h>
#endif

namespace OmniCpp::Engine::Platform {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct Platform::Impl {
    PlatformType platform_type;
    std::mutex mutex;
    bool initialized{ false };
  };

  Platform::Platform () : m_impl (std::make_unique<Impl> ()) {
  }

  Platform::~Platform () {
    shutdown ();
  }

  Platform::Platform (Platform&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  Platform& Platform::operator= (Platform&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool Platform::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      spdlog::warn("Platform: Already initialized");
      return true;
    }

#ifdef _WIN32
    m_impl->platform_type = PlatformType::Windows;
#elif defined(__linux__)
    m_impl->platform_type = PlatformType::Linux;
#elif defined(__APPLE__)
    #include <TargetConditionals.h>
  #if TARGET_OS_MAC
    m_impl->platform_type = PlatformType::MacOS;
  #elif TARGET_OS_IPHONE
    m_impl->platform_type = PlatformType::iOS;
  #endif
#elif defined(__ANDROID__)
    m_impl->platform_type = PlatformType::Android;
#else
    m_impl->platform_type = PlatformType::Unknown;
#endif

    m_impl->initialized = true;

    spdlog::info("Platform: Initialized as {}", get_platform_name());
    return true;
  }

  void Platform::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->initialized = false;

    spdlog::info("Platform: Shutdown");
  }

  PlatformType Platform::get_platform_type () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->platform_type;
  }

  std::string Platform::get_platform_name () const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    switch (m_impl->platform_type) {
    case PlatformType::Windows:
      return "Windows";
    case PlatformType::Linux:
      return "Linux";
    case PlatformType::MacOS:
      return "MacOS";
    case PlatformType::Android:
      return "Android";
    case PlatformType::iOS:
      return "iOS";
    default:
      return "Unknown";
    }
  }

  uint64_t Platform::get_system_time_ms () const {
    auto now = std::chrono::steady_clock::now ();
    auto duration = now.time_since_epoch ();
    return std::chrono::duration_cast<std::chrono::milliseconds> (duration).count ();
  }

} // namespace OmniCpp::Engine::Platform
