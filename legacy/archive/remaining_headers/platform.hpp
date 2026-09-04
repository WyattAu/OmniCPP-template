/**
 * @file platform.hpp
 * @brief Platform abstraction interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Platform {

  /**
   * @brief Platform type enumeration
   */
  enum class PlatformType : uint32_t { Unknown = 0, Windows, Linux, MacOS, Android, iOS };

  /**
   * @brief Platform class
   */
  class Platform {
  public:
    Platform ();
    ~Platform ();

    Platform (const Platform&) = delete;
    Platform& operator= (const Platform&) = delete;

    Platform (Platform&&) noexcept;
    Platform& operator= (Platform&&) noexcept;

    bool initialize ();
    void shutdown ();

    [[nodiscard]] PlatformType get_platform_type () const;
    [[nodiscard]] std::string get_platform_name () const;
    [[nodiscard]] uint64_t get_system_time_ms () const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Platform
