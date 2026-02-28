/**
 * @file logger.hpp
 * @brief Logging interface with Quill integration
 */

#pragma once

#include <memory>
#include <string>
#include <quill/Quill.h>

namespace OmniCpp::Engine::Logging {

  /**
   * @brief Log level enumeration
   */
  enum class LogLevel {
    Trace = 0,
    Debug = 1,
    Info = 2,
    Warning = 3,
    Error = 4,
    Critical = 5
  };

  /**
   * @brief Logger class for the engine
   *
   * Provides logging functionality using Quill.
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
