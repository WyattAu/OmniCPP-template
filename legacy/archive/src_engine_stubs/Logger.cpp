/**
 * @file Logger.cpp
 * @brief Stub implementation of logger subsystem
 * @version 1.0.0
 */

#include "engine/ILogger.hpp"
#include <iostream>

namespace omnicpp {

class LoggerStub : public ILogger {
public:
    LoggerStub() = default;
    ~LoggerStub() override = default;

    bool initialize() override {
        return true;
    }

    void shutdown() override {
    }

    void log(LogLevel level, const char* message, const char* category) override {
        (void)category;
        
        const char* level_str = "INFO";
        switch (level) {
            case LogLevel::TRACE:   level_str = "TRACE"; break;
            case LogLevel::DEBUG:   level_str = "DEBUG"; break;
            case LogLevel::INFO:    level_str = "INFO"; break;
            case LogLevel::WARNING: level_str = "WARNING"; break;
            case LogLevel::ERROR:   level_str = "ERROR"; break;
            case LogLevel::FATAL:   level_str = "FATAL"; break;
        }
        
        if (category) {
            std::cout << "[" << level_str << "] [" << category << "] " << message << std::endl;
        } else {
            std::cout << "[" << level_str << "] " << message << std::endl;
        }
    }

    void set_log_level(LogLevel level) override {
        m_log_level = level;
    }

    LogLevel get_log_level() const override {
        return m_log_level;
    }

    void set_console_output(bool enabled) override {
        m_console_output = enabled;
    }

    void set_file_output(bool enabled, const char* file_path) override {
        (void)enabled;
        (void)file_path;
    }

    void flush() override {
        std::cout.flush();
    }

private:
    LogLevel m_log_level = LogLevel::INFO;
    bool m_console_output = true;
};

} // namespace omnicpp
