/**
 * @file logger.cpp
 * @brief Logging implementation using Quill backend
 */

#include "engine/logging/logger.hpp"
#include "engine/logging/Log.hpp"
#include <memory>

namespace OmniCpp::Engine::Logging {

  struct Logger::Impl {
    std::string name;
    LogLevel current_level{ LogLevel::Info };
    bool initialized{ false };
  };

  Logger::Logger (const std::string& name) : m_impl (std::make_unique<Impl> ()) {
    m_impl->name = name;
    m_impl->initialized = true;
    omnicpp::log::info("Logger '{}' initialized", name);
  }

  Logger::~Logger () {
    if (m_impl->initialized) {
      omnicpp::log::info("Logger '{}' shutting down", m_impl->name);
    }
  }

  Logger::Logger (Logger&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  Logger& Logger::operator= (Logger&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  void Logger::trace (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::trace("{}", message);
  }

  void Logger::debug (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::debug("{}", message);
  }

  void Logger::info (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::info("{}", message);
  }

  void Logger::warning (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::warn("{}", message);
  }

  void Logger::error (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::error("{}", message);
  }

  void Logger::critical (const std::string& message) {
    if (!m_impl->initialized) return;
    omnicpp::log::critical("{}", message);
  }

  void Logger::set_level (LogLevel level) {
    if (!m_impl->initialized) return;

    m_impl->current_level = level;

    // Map our LogLevel to Quill log level
    quill::LogLevel quill_level;
    switch (level) {
    case LogLevel::Trace:
      quill_level = quill::LogLevel::TraceL3;
      break;
    case LogLevel::Debug:
      quill_level = quill::LogLevel::Debug;
      break;
    case LogLevel::Info:
      quill_level = quill::LogLevel::Info;
      break;
    case LogLevel::Warning:
      quill_level = quill::LogLevel::Warning;
      break;
    case LogLevel::Error:
      quill_level = quill::LogLevel::Error;
      break;
    case LogLevel::Critical:
      quill_level = quill::LogLevel::Critical;
      break;
    case LogLevel::Off:
      quill_level = quill::LogLevel::None;
      break;
    default:
      quill_level = quill::LogLevel::Info;
      break;
    }

    omnicpp::log::set_level(quill_level);
  }

  LogLevel Logger::get_level () const noexcept {
    return m_impl->current_level;
  }

  void Logger::flush () {
    // Quill handles flushing automatically
  }

} // namespace OmniCpp::Engine::Logging
