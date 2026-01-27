/**
 * @file logger.hpp
 * @brief Logging interface with spdlog integration
 */

#pragma once

#include <memory>
#include <spdlog/spdlog.h>
#include <string>

namespace OmniCpp::Engine::Logging {

  /**
   * @brief Log level enumeration
   */
  enum class LogLevel {
    Trace = SPDLOG_LEVEL_TRACE,
    Debug = SPDLOG_LEVEL_DEBUG,
    Info = SPDLOG_LEVEL_INFO,
    Warning = SPDLOG_LEVEL_WARN,
    Error = SPDLOG_LEVEL_ERROR,
    Critical = SPDLOG_LEVEL_CRITICAL,
    Off = SPDLOG_LEVEL_OFF
  };

  /**
   * @brief Logger class
   * 
   * Provides logging functionality using spdlog.
   * Follows C++23 best practices with RAII and move semantics.
   */
  class Logger {
  public:
    explicit Logger (const std::string& name);
    ~Logger ();

    // Delete copy operations (C++23 best practice)
    Logger (const Logger&) = delete;
    Logger& operator= (const Logger&) = delete;

    // Enable move operations (C++23 best practice)
    Logger (Logger&&) noexcept;
    Logger& operator= (Logger&&) noexcept;

    /**
     * @brief Log trace message
     * @param message Message to log
     */
    void trace (const std::string& message);

    /**
     * @brief Log debug message
     * @param message Message to log
     */
    void debug (const std::string& message);

    /**
     * @brief Log info message
     * @param message Message to log
     */
    void info (const std::string& message);

    /**
     * @brief Log warning message
     * @param message Message to log
     */
    void warning (const std::string& message);

    /**
     * @brief Log error message
     * @param message Message to log
     */
    void error (const std::string& message);

    /**
     * @brief Log critical message
     * @param message Message to log
     */
    void critical (const std::string& message);

    /**
     * @brief Set log level
     * @param level Log level to set
     */
    void set_level (LogLevel level);

    /**
     * @brief Get current log level
     * @return Current log level
     */
    [[nodiscard]] LogLevel get_level () const noexcept;

    /**
     * @brief Flush log buffers
     */
    void flush ();

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl; // Pimpl idiom for ABI stability
  };

} // namespace OmniCpp::Engine::Logging
