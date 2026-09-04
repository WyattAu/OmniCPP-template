#pragma once

#include <memory>
#include <string>

namespace OmniCpp::Engine::Logging {

enum class LogLevel {
  Trace = 0,
  Debug = 1,
  Info = 2,
  Warning = 3,
  Error = 4,
  Critical = 5
};

class Logger {
public:
  explicit Logger(const std::string& name);
  ~Logger();
  Logger(const Logger&) = delete;
  Logger& operator=(const Logger&) = delete;
  Logger(Logger&&) noexcept;
  Logger& operator=(Logger&&) noexcept;

  void trace(const std::string& message);
  void debug(const std::string& message);
  void info(const std::string& message);
  void warning(const std::string& message);
  void error(const std::string& message);
  void critical(const std::string& message);
  void set_level(LogLevel level);
  [[nodiscard]] LogLevel get_level() const noexcept;
  void flush();

private:
  struct Impl;
  std::unique_ptr<Impl> m_impl;
};

} // namespace OmniCpp::Engine::Logging
