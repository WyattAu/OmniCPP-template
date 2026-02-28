/**
 * @file QuillLogger.cpp
 * @brief Quill-based logger implementation for OmniCpp engine
 * @version 1.0.0
 */

#include "engine/logging/QuillLogger.hpp"
#include <quill/Backend.h>
#include <quill/Frontend.h>
#include <quill/sinks/FileSink.h>
#include <quill/sinks/ConsoleSink.h>
#include <filesystem>
#include <iostream>

namespace omnicpp {

QuillLogger::QuillLogger(std::string logger_name)
    : m_logger_name(std::move(logger_name)) {
}

QuillLogger::~QuillLogger() {
    if (m_initialized) {
        shutdown();
    }
}

bool QuillLogger::initialize() {
    if (m_initialized) {
        return true;
    }

    try {
        // Start the Quill backend (only once per application)
        quill::BackendOptions backend_options;
        backend_options.backend_thread_sleep_duration = std::chrono::nanoseconds{500};
        quill::Backend::start(backend_options);

        // Create console sink
        auto console_sink = quill::Backend::create_sink<quill::ConsoleSink>("console_sink");

        // Create file sink if enabled
        std::shared_ptr<quill::Sink> file_sink;
        if (m_file_enabled && !m_file_path.empty()) {
            // Create logs directory if it doesn't exist
            std::filesystem::path log_path(m_file_path);
            if (log_path.has_parent_path()) {
                std::filesystem::create_directories(log_path.parent_path());
            }
            file_sink = quill::Backend::create_sink<quill::FileSink>(
                "file_sink",
                quill::FileSinkConfig{m_file_path}
            );
        }

        // Create logger with sinks
        std::vector<std::shared_ptr<quill::Sink>> sinks;
        if (m_console_enabled) {
            sinks.push_back(console_sink);
        }
        if (file_sink) {
            sinks.push_back(file_sink);
        }

        m_logger = quill::Frontend::create_or_get_logger(
            m_logger_name,
            sinks.begin(),
            sinks.end()
        );

        // Set default log level
        m_logger->set_log_level(quill::LogLevel::Info);
        m_initialized = true;

        return true;
    } catch (const std::exception& e) {
        std::cerr << "Failed to initialize Quill logger: " << e.what() << std::endl;
        return false;
    }
}

bool QuillLogger::initialize(const std::string& config_file) {
    // For now, ignore config file and use default initialization
    // TODO: Parse JSON config file
    (void)config_file;
    return initialize();
}

void QuillLogger::shutdown() {
    if (!m_initialized) {
        return;
    }

    try {
        // Flush all pending log messages
        m_logger->flush_log();
        
        // Stop the backend
        quill::Backend::stop();
        
        m_initialized = false;
    } catch (const std::exception& e) {
        std::cerr << "Error during Quill shutdown: " << e.what() << std::endl;
    }
}

void QuillLogger::log(LogLevel level, const char* message, const char* category) {
    if (!m_initialized || !m_logger) {
        std::cerr << "[" << static_cast<int>(level) << "] " 
                  << (category ? category : "") << ": " << message << std::endl;
        return;
    }

    const quill::LogLevel quill_level = to_quill_level(level);
    
    if (category) {
        // Format with category prefix
        std::string formatted_message = "[";
        formatted_message += category;
        formatted_message += "] ";
        formatted_message += message;
        
        m_logger->log(quill_level, "{}", formatted_message);
    } else {
        m_logger->log(quill_level, "{}", message);
    }
}

void QuillLogger::set_log_level(LogLevel level) {
    if (m_logger) {
        m_logger->set_log_level(to_quill_level(level));
    }
}

LogLevel QuillLogger::get_log_level() const {
    if (m_logger) {
        return from_quill_level(m_logger->get_log_level());
    }
    return LogLevel::INFO;
}

void QuillLogger::set_console_output(bool enabled) {
    m_console_enabled = enabled;
    // Note: Changing sinks at runtime requires re-creating the logger
}

void QuillLogger::set_file_output(bool enabled, const char* file_path) {
    m_file_enabled = enabled;
    if (file_path) {
        m_file_path = file_path;
    }
    // Note: Changing sinks at runtime requires re-creating the logger
}

void QuillLogger::flush() {
    if (m_logger) {
        m_logger->flush_log();
    }
}

quill::LogLevel QuillLogger::to_quill_level(LogLevel level) noexcept {
    switch (level) {
        case LogLevel::TRACE:
            return quill::LogLevel::TraceL3;
        case LogLevel::DEBUG:
            return quill::LogLevel::Debug;
        case LogLevel::INFO:
            return quill::LogLevel::Info;
        case LogLevel::WARNING:
            return quill::LogLevel::Warning;
        case LogLevel::ERROR:
            return quill::LogLevel::Error;
        case LogLevel::FATAL:
            return quill::LogLevel::Critical;
        default:
            return quill::LogLevel::Info;
    }
}

LogLevel QuillLogger::from_quill_level(quill::LogLevel level) noexcept {
    switch (level) {
        case quill::LogLevel::TraceL3:
        case quill::LogLevel::TraceL2:
        case quill::LogLevel::TraceL1:
            return LogLevel::TRACE;
        case quill::LogLevel::Debug:
            return LogLevel::DEBUG;
        case quill::LogLevel::Info:
            return LogLevel::INFO;
        case quill::LogLevel::Warning:
            return LogLevel::WARNING;
        case quill::LogLevel::Error:
            return LogLevel::ERROR;
        case quill::LogLevel::Critical:
            return LogLevel::FATAL;
        default:
            return LogLevel::INFO;
    }
}

} // namespace omnicpp
