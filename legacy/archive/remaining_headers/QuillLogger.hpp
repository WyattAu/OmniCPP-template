/**
 * @file QuillLogger.hpp
 * @brief Quill-based logger implementation for OmniCpp engine
 * @version 1.0.0
 *
 * This file provides a modern C++23 logger implementation using Quill.
 */

#pragma once

#include "engine/ILogger.hpp"
#include <memory>
#include <string>
#include <quill/Frontend.h>
#include <quill/Backend.h>
#include <quill/Logger.h>
#include <quill/core/LogLevel.h>
#include <quill/sinks/FileSink.h>
#include <quill/sinks/ConsoleSink.h>

namespace omnicpp {

/**
 * @brief Quill-based logger implementation
 *
 * Provides high-performance logging with file rotation, console output,
 * and configurable log levels using Quill.
 */
class QuillLogger : public ILogger {
public:
    /**
     * @brief Construct a new QuillLogger object
     *
     * @param logger_name Name of the logger
     */
    explicit QuillLogger(std::string logger_name = "omnicpp");

    /**
     * @brief Destroy the QuillLogger object
     */
    ~QuillLogger() override;

    // Disable copying
    QuillLogger(const QuillLogger&) = delete;
    QuillLogger& operator=(const QuillLogger&) = delete;

    // Enable moving
    QuillLogger(QuillLogger&&) noexcept = default;
    QuillLogger& operator=(QuillLogger&&) noexcept = default;

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
     * @brief Get the underlying Quill logger
     *
     * @return Pointer to Quill logger
     */
    quill::Logger* get_quill_logger() const noexcept {
        return m_logger;
    }

private:
    /**
     * @brief Convert LogLevel to quill::LogLevel
     *
     * @param level LogLevel to convert
     * @return Corresponding Quill log level
     */
    static quill::LogLevel to_quill_level(LogLevel level) noexcept;

    /**
     * @brief Convert quill::LogLevel to LogLevel
     *
     * @param level Quill log level to convert
     * @return Corresponding LogLevel
     */
    static LogLevel from_quill_level(quill::LogLevel level) noexcept;

    quill::Logger* m_logger{nullptr};
    std::string m_logger_name;
    bool m_console_enabled{true};
    bool m_file_enabled{true};
    std::string m_file_path{"logs/omnicpp_engine.log"};
    bool m_initialized{false};
};

} // namespace omnicpp
