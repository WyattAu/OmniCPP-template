/**
 * @file ConsoleLogger.hpp
 * @brief Console logger implementation
 * @version 1.0.0
 */

#pragma once

#include "engine/ILogger.hpp"
#include <string>

namespace omnicpp {

/**
 * @brief Console logger implementation
 * 
 * Outputs log messages to console with timestamps.
 */
class ConsoleLogger : public ILogger {
public:
    /**
     * @brief Construct a new Console Logger object
     */
    ConsoleLogger() = default;

    /**
     * @brief Destroy the Console Logger object
     */
    ~ConsoleLogger() override = default;

    // Disable copying
    ConsoleLogger(const ConsoleLogger&) = delete;
    ConsoleLogger& operator=(const ConsoleLogger&) = delete;

    // Enable moving
    ConsoleLogger(ConsoleLogger&&) noexcept = default;
    ConsoleLogger& operator=(ConsoleLogger&&) noexcept = default;

    /**
     * @brief Initialize the logger
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize() override;

    /**
     * @brief Shutdown the logger
     */
    void shutdown() override;

    /**
     * @brief Log a message
     * @param level The log level
     * @param message The message to log
     * @param context The context (e.g., module name)
     */
    void log(LogLevel level, const std::string& message, const std::string& context) override;
};

} // namespace omnicpp
