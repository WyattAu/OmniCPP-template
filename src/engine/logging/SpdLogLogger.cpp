/**
 * @file SpdLogLogger.cpp
 * @brief spdlog-based logger implementation for OmniCpp engine
 * @version 1.0.0
 */

#include "engine/logging/SpdLogLogger.hpp"
#include <filesystem>
#include <fstream>
#include <nlohmann/json.hpp>

namespace omnicpp {

namespace fs = std::filesystem;

SpdLogLogger::SpdLogLogger(std::string logger_name)
    : m_logger_name(std::move(logger_name)) {
}

bool SpdLogLogger::initialize() {
    try {
        // Create logs directory if it doesn't exist
        fs::path logs_dir = fs::path(m_file_path).parent_path();
        if (!logs_dir.empty() && !fs::exists(logs_dir)) {
            fs::create_directories(logs_dir);
        }

        // Create sinks
        std::vector<spdlog::sink_ptr> sinks;

        if (m_console_enabled) {
            sinks.push_back(create_console_sink());
        }

        if (m_file_enabled) {
            sinks.push_back(create_file_sink(m_file_path, m_max_file_size, m_max_files));
        }

        // Create logger with multiple sinks
        m_logger = std::make_shared<spdlog::logger>(m_logger_name, sinks.begin(), sinks.end());

        // Set default pattern
        m_logger->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] [%t] %v");

        // Set default log level
        m_logger->set_level(spdlog::level::info);

        // Register as default logger
        spdlog::set_default_logger(m_logger);

        // Flush on error or higher
        m_logger->flush_on(spdlog::level::err);

        return true;
    } catch (const std::exception& e) {
        std::cerr << "Failed to initialize logger: " << e.what() << std::endl;
        return false;
    }
}

bool SpdLogLogger::initialize(const std::string& config_file) {
    try {
        // Load configuration from JSON file
        std::ifstream config_stream(config_file);
        if (!config_stream.is_open()) {
            std::cerr << "Failed to open config file: " << config_file << std::endl;
            return initialize(); // Fall back to default initialization
        }

        nlohmann::json config;
        config_stream >> config;

        // Parse configuration
        if (config.contains("level")) {
            std::string level_str = config["level"];
            spdlog::level::level_enum level = spdlog::level::from_str(level_str);
            m_logger->set_level(level);
        }

        if (config.contains("pattern")) {
            m_logger->set_pattern(config["pattern"]);
        }

        if (config.contains("console_sink_enabled")) {
            m_console_enabled = config["console_sink_enabled"];
        }

        if (config.contains("file_sink_enabled")) {
            m_file_enabled = config["file_sink_enabled"];
        }

        if (config.contains("file_path")) {
            m_file_path = config["file_path"];
        }

        if (config.contains("max_file_size")) {
            m_max_file_size = config["max_file_size"];
        }

        if (config.contains("max_files")) {
            m_max_files = config["max_files"];
        }

        if (config.contains("flush_level")) {
            std::string flush_level_str = config["flush_level"];
            spdlog::level::level_enum flush_level = spdlog::level::from_str(flush_level_str);
            m_logger->flush_on(flush_level);
        }

        // Initialize with parsed configuration
        return initialize();
    } catch (const std::exception& e) {
        std::cerr << "Failed to load logger configuration: " << e.what() << std::endl;
        return initialize(); // Fall back to default initialization
    }
}

void SpdLogLogger::shutdown() {
    if (m_logger) {
        m_logger->flush();
        m_logger.reset();
    }
}

void SpdLogLogger::log(LogLevel level, const char* message, const char* category) {
    if (!m_logger) {
        return;
    }

    spdlog::level::level_enum spdlog_level = to_spdlog_level(level);

    if (category) {
        m_logger->log(spdlog_level, "[{}] {}", category, message);
    } else {
        m_logger->log(spdlog_level, "{}", message);
    }
}

void SpdLogLogger::set_log_level(LogLevel level) {
    if (m_logger) {
        m_logger->set_level(to_spdlog_level(level));
    }
}

LogLevel SpdLogLogger::get_log_level() const {
    if (!m_logger) {
        return LogLevel::INFO;
    }

    return from_spdlog_level(m_logger->level());
}

void SpdLogLogger::set_console_output(bool enabled) {
    m_console_enabled = enabled;
    // Reinitialize to apply changes
    shutdown();
    initialize();
}

void SpdLogLogger::set_file_output(bool enabled, const char* file_path) {
    m_file_enabled = enabled;
    if (file_path) {
        m_file_path = file_path;
    }
    // Reinitialize to apply changes
    shutdown();
    initialize();
}

void SpdLogLogger::flush() {
    if (m_logger) {
        m_logger->flush();
    }
}

spdlog::level::level_enum SpdLogLogger::to_spdlog_level(LogLevel level) noexcept {
    switch (level) {
        case LogLevel::TRACE:
            return spdlog::level::trace;
        case LogLevel::DEBUG:
            return spdlog::level::debug;
        case LogLevel::INFO:
            return spdlog::level::info;
        case LogLevel::WARNING:
            return spdlog::level::warn;
        case LogLevel::ERROR:
            return spdlog::level::err;
        case LogLevel::FATAL:
            return spdlog::level::critical;
        default:
            return spdlog::level::info;
    }
}

LogLevel SpdLogLogger::from_spdlog_level(spdlog::level::level_enum level) noexcept {
    switch (level) {
        case spdlog::level::trace:
            return LogLevel::TRACE;
        case spdlog::level::debug:
            return LogLevel::DEBUG;
        case spdlog::level::info:
            return LogLevel::INFO;
        case spdlog::level::warn:
            return LogLevel::WARNING;
        case spdlog::level::err:
            return LogLevel::ERROR;
        case spdlog::level::critical:
            return LogLevel::FATAL;
        default:
            return LogLevel::INFO;
    }
}

std::shared_ptr<spdlog::sinks::stdout_color_sink_mt> SpdLogLogger::create_console_sink() const {
    auto sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    sink->set_level(spdlog::level::trace);
    sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%^%l%$] %v");
    return sink;
}

std::shared_ptr<spdlog::sinks::rotating_file_sink_mt> SpdLogLogger::create_file_sink(
    const std::string& file_path,
    size_t max_size,
    size_t max_files
) const {
    auto sink = std::make_shared<spdlog::sinks::rotating_file_sink_mt>(
        file_path, max_size, max_files
    );
    sink->set_level(spdlog::level::trace);
    sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] [%t] %v");
    return sink;
}

} // namespace omnicpp
