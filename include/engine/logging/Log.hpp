/**
 * @file Log.hpp
 * @brief Quill-based logging for OmniCpp engine
 * @version 1.0.0
 * 
 * This provides a clean logging API using Quill as the backend.
 * Usage:
 *   omnicpp::log::init();  // Call once at startup
 *   omnicpp::log::info("Message with {}", arg);
 *   omnicpp::log::shutdown();  // Call at shutdown
 */

#pragma once

#include <quill/Backend.h>
#include <quill/Frontend.h>
#include <quill/Logger.h>
#include <quill/LogMacros.h>
#include <quill/core/LogLevel.h>
#include <quill/sinks/ConsoleSink.h>

#include <string>
#include <mutex>
#include <source_location>

namespace omnicpp::log {

// ============================================================================
// Initialization and shutdown
// ============================================================================

namespace detail {
    inline std::mutex& init_mutex() {
        static std::mutex mtx;
        return mtx;
    }
    
    inline bool& is_initialized() {
        static bool initialized = false;
        return initialized;
    }
    
    inline quill::Logger*& global_logger() {
        static quill::Logger* logger = nullptr;
        return logger;
    }
}

/**
 * @brief Initialize the logging system
 * @param min_level Minimum log level to display (default: Info)
 */
inline void init(quill::LogLevel min_level = quill::LogLevel::Info) {
    std::lock_guard<std::mutex> lock(detail::init_mutex());
    
    if (detail::is_initialized()) {
        return;
    }
    
    // Start Quill backend
    quill::BackendOptions backend_options;
    backend_options.sleep_duration = std::chrono::nanoseconds{500};
    quill::Backend::start(backend_options);
    
    // Create console sink
    auto console_sink = quill::Frontend::create_or_get_sink<quill::ConsoleSink>(
        "omnicpp_console"
    );
    
    // Create logger
    detail::global_logger() = quill::Frontend::create_or_get_logger(
        "omnicpp",
        console_sink
    );
    
    detail::global_logger()->set_log_level(min_level);
    detail::is_initialized() = true;
}

/**
 * @brief Shutdown the logging system
 */
inline void shutdown() {
    std::lock_guard<std::mutex> lock(detail::init_mutex());
    
    if (!detail::is_initialized()) {
        return;
    }
    
    quill::Backend::stop();
    detail::is_initialized() = false;
    detail::global_logger() = nullptr;
}

/**
 * @brief Get the global logger
 */
inline quill::Logger* logger() {
    if (!detail::is_initialized()) {
        init();
    }
    return detail::global_logger();
}

/**
 * @brief Set the minimum log level
 */
inline void set_level(quill::LogLevel level) {
    if (auto* log = logger()) {
        log->set_log_level(level);
    }
}

// ============================================================================
// Logging macros - Use these for logging
// ============================================================================

#define LOG_TRACE(...) QUILL_LOG_TRACE_L3(omnicpp::log::logger(), __VA_ARGS__)
#define LOG_DEBUG(...) QUILL_LOG_DEBUG(omnicpp::log::logger(), __VA_ARGS__)
#define LOG_INFO(...)  QUILL_LOG_INFO(omnicpp::log::logger(), __VA_ARGS__)
#define LOG_WARN(...)  QUILL_LOG_WARNING(omnicpp::log::logger(), __VA_ARGS__)
#define LOG_ERROR(...) QUILL_LOG_ERROR(omnicpp::log::logger(), __VA_ARGS__)
#define LOG_CRITICAL(...) QUILL_LOG_CRITICAL(omnicpp::log::logger(), __VA_ARGS__)

// ============================================================================
// Convenience functions (for when macros aren't suitable)
// ============================================================================

template<typename... Args>
void trace(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_TRACE_L3(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

template<typename... Args>
void debug(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_DEBUG(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

template<typename... Args>
void info(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_INFO(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

template<typename... Args>
void warn(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_WARNING(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

template<typename... Args>
void error(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_ERROR(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

template<typename... Args>
void critical(std::format_string<Args...> fmt, Args&&... args) {
    if (auto* log = logger()) {
        QUILL_LOG_CRITICAL(log, "{}", std::format(fmt, std::forward<Args>(args)...));
    }
}

} // namespace omnicpp::log
