/**
 * @file ILogger.hpp
 * @brief Logger subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for logging functionality.
 */

#ifndef OMNICPP_ILOGGER_HPP
#define OMNICPP_ILOGGER_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Log levels
 */
enum class LogLevel : int32_t {
    TRACE = 0,
    DEBUG = 1,
    INFO = 2,
    WARNING = 3,
    ERROR = 4,
    FATAL = 5
};

/**
 * @brief Logger interface
 */
class ILogger {
public:
    virtual ~ILogger() = default;
    
    /**
     * @brief Initialize logger
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown logger
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Log a message
     * 
     * @param level Log level
     * @param message Message to log
     * @param category Optional category (e.g., "RENDERER", "PHYSICS")
     */
    virtual void log(LogLevel level, const char* message, const char* category = nullptr) = 0;
    
    /**
     * @brief Set minimum log level
     * 
     * @param level Minimum level to log
     */
    virtual void set_log_level(LogLevel level) = 0;
    
    /**
     * @brief Get current log level
     * 
     * @return Current log level
     */
    virtual LogLevel get_log_level() const = 0;
    
    /**
     * @brief Enable/disable console output
     * 
     * @param enabled True to enable, false to disable
     */
    virtual void set_console_output(bool enabled) = 0;
    
    /**
     * @brief Enable/disable file output
     * 
     * @param enabled True to enable, false to disable
     * @param file_path Optional file path (if enabled)
     */
    virtual void set_file_output(bool enabled, const char* file_path = nullptr) = 0;
    
    /**
     * @brief Flush log buffers
     */
    virtual void flush() = 0;
};

} // namespace omnicpp

#endif // OMNICPP_ILOGGER_HPP
