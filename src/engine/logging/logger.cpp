/**
 * @file logger.cpp
 * @brief Logging implementation with spdlog integration
 */

#include "engine/logging/logger.hpp"
#include <memory>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>

namespace OmniCpp::Engine::Logging {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct Logger::Impl {
    std::shared_ptr<spdlog::logger> logger;
    std::string name;
    LogLevel current_level{ LogLevel::Info };
    bool initialized{ false };
  };

  Logger::Logger (const std::string& name) : m_impl (std::make_unique<Impl> ()) {
    m_impl->name = name;

    // Create console sink with color support
    auto console_sink
        = std::make_shared<spdlog::sinks::stdout_color_sink_mt> (spdlog::color_mode::automatic);

    // Create file sink
    try {
      auto file_sink
          = std::make_shared<spdlog::sinks::basic_file_sink_mt> ("logs/" + name + ".log", true);

      // Create multi-sink logger
      m_impl->logger = std::make_shared<spdlog::logger> (name, console_sink, file_sink);

      // Set default pattern
      spdlog::set_pattern ("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] %v");

      // Set default level
      m_impl->logger->set_level (spdlog::level::info);

      m_impl->initialized = true;
    } catch (const spdlog::spdlog_ex& ex) {
      // Fallback to console only if file sink fails
      m_impl->logger = std::make_shared<spdlog::logger> (name, console_sink);
      m_impl->initialized = true;
    }
  }

  Logger::~Logger () {
    if (m_impl->initialized && m_impl->logger) {
      m_impl->logger->flush ();
    }
  }

  Logger::Logger (Logger&& other) noexcept : m_impl (std::move (other.m_impl)) {
    // Move constructor
  }

  Logger& Logger::operator= (Logger&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  void Logger::trace (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->trace (message);
  }

  void Logger::debug (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->debug (message);
  }

  void Logger::info (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->info (message);
  }

  void Logger::warning (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->warn (message);
  }

  void Logger::error (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->error (message);
  }

  void Logger::critical (const std::string& message) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }
    m_impl->logger->critical (message);
  }

  void Logger::set_level (LogLevel level) {
    if (!m_impl->initialized || !m_impl->logger) {
      return;
    }

    m_impl->current_level = level;

    // Map our LogLevel to spdlog level
    spdlog::level::level_enum spdlog_level;
    switch (level) {
    case LogLevel::Trace:
      spdlog_level = spdlog::level::trace;
      break;
    case LogLevel::Debug:
      spdlog_level = spdlog::level::debug;
      break;
    case LogLevel::Info:
      spdlog_level = spdlog::level::info;
      break;
    case LogLevel::Warning:
      spdlog_level = spdlog::level::warn;
      break;
    case LogLevel::Error:
      spdlog_level = spdlog::level::err;
      break;
    case LogLevel::Critical:
      spdlog_level = spdlog::level::critical;
      break;
    case LogLevel::Off:
      spdlog_level = spdlog::level::off;
      break;
    default:
      spdlog_level = spdlog::level::info;
      break;
    }

    m_impl->logger->set_level (spdlog_level);
  }

  LogLevel Logger::get_level () const noexcept {
    return m_impl->current_level;
  }

  void Logger::flush () {
    if (m_impl->initialized && m_impl->logger) {
      m_impl->logger->flush ();
    }
  }

} // namespace OmniCpp::Engine::Logging
