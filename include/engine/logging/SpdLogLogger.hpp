/**
 * @file SpdLogLogger.hpp
 * @brief spdlog-based logger implementation for OmniCpp engine
 * @version 1.0.0
 *
 * This file provides a modern C++23 logger implementation using spdlog.
 */

#pragma once

#include "engine/ILogger.hpp"
#include <memory>
#include <string>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/sinks/rotating_file_sink.h>

namespace omnicpp {

/**
 * @brief spdlog-based logger implementation
 *
 * Provides modern logging with file rotation, console output,
 * and configurable log levels using spdlog.
 */
class SpdLogLogger : public ILogger {
public:
    /**
     * @brief Construct a new SpdLogLogger object
     *
     * @param logger_name Name of the logger
     */
    explicit SpdLogLogger(std::string logger_name = "omnicpp");

    /**
     * @brief Destroy the SpdLogLogger object
     */
    ~SpdLogLogger() override = default;

    // Disable copying
    SpdLogLogger(const SpdLogLogger&) = delete;
    SpdLogLogger& operator=(const SpdLogLogger&) = delete;

    // Enable moving
    SpdLogLogger(SpdLogLogger&&) noexcept = default;
    SpdLogLogger& operator=(SpdLogLogger&&) noexcept = default;

    /**
     * @brief Initialize logger with default configuration
     *
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize() override;

    /**
     * @brief Initialize logger with custom configuration
     *
     * @param config_file Path to JSON configuration file
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize(const std::string& config_file);

    /**
     * @brief Shutdown logger and flush all buffers
     */
    void shutdown() override;

    /**
     * @brief Log a message
     *
     * @param level Log level
     * @param message Message to log
     * @param category Optional category (e.g., "RENDERER", "PHYSICS")
     */
    void log(LogLevel level, const char* message, const char* category = nullptr) override;

    /**
     * @brief Set minimum log level
     *
     * @param level Minimum level to log
     */
    void set_log_level(LogLevel level) override;

    /**
     * @brief Get current log level
     *
     * @return Current log level
     */
    LogLevel get_log_level() const override;

    /**
     * @brief Enable/disable console output
     *
     * @param enabled True to enable, false to disable
     */
    void set_console_output(bool enabled) override;

    /**
     * @brief Enable/disable file output
     *
     * @param enabled True to enable, false to disable
     * @param file_path Optional file path (if enabled)
     */
    void set_file_output(bool enabled, const char* file_path = nullptr) override;

    /**
     * @brief Flush log buffers
     */
    void flush() override;

    /**
     * @brief Get the underlying spdlog logger
     *
     * @return Shared pointer to spdlog logger
     */
    std::shared_ptr<spdlog::logger> get_spdlog_logger() const noexcept {
        return m_logger;
    }

private:
    /**
     * @brief Convert LogLevel to spdlog::level::level_enum
     *
     * @param level LogLevel to convert
     * @return Corresponding spdlog level
     */
    static spdlog::level::level_enum to_spdlog_level(LogLevel level) noexcept;

    /**
     * @brief Convert spdlog::level::level_enum to LogLevel
     *
     * @param level spdlog level to convert
     * @return Corresponding LogLevel
     */
    static LogLevel from_spdlog_level(spdlog::level::level_enum level) noexcept;

    /**
     * @brief Create console sink
     *
     * @return Shared pointer to console sink
     */
    std::shared_ptr<spdlog::sinks::stdout_color_sink_mt> create_console_sink() const;

    /**
     * @brief Create file sink with rotation
     *
     * @param file_path Path to log file
     * @param max_size Maximum file size in bytes
     * @param max_files Maximum number of files to keep
     * @return Shared pointer to file sink
     */
    std::shared_ptr<spdlog::sinks::rotating_file_sink_mt> create_file_sink(
        const std::string& file_path,
        size_t max_size = 10 * 1024 * 1024,
        size_t max_files = 5
    ) const;

    std::shared_ptr<spdlog::logger> m_logger;
    std::string m_logger_name;
    bool m_console_enabled = true;
    bool m_file_enabled = true;
    std::string m_file_path = "logs/omnicpp_engine.log";
    size_t m_max_file_size = 10 * 1024 * 1024;
    size_t m_max_files = 5;
};

} // namespace omnicpp
