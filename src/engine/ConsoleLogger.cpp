/**
 * @file ConsoleLogger.cpp
 * @brief Console logger implementation (deprecated - use SpdLogLogger instead)
 * @version 1.0.0
 * @deprecated This logger is deprecated. Use SpdLogLogger for modern logging.
 */

#include "engine/ILogger.hpp"
#include <iostream>
#include <ctime>
#include <iomanip>
#include <sstream>

namespace omnicpp {

ConsoleLogger::ConsoleLogger() = default;

ConsoleLogger::~ConsoleLogger() = default;

bool ConsoleLogger::initialize() {
    std::cout << "Logger initialized (deprecated - use SpdLogLogger)" << std::endl;
    return true;
}

void ConsoleLogger::shutdown() {
    std::cout << "Logger shutdown" << std::endl;
}

void ConsoleLogger::log(LogLevel level, const std::string& message, const std::string& context) {
    // Get current time
    time_t now = time(nullptr);
    struct tm timeinfo;
#ifdef _WIN32
    localtime_s(&timeinfo, &now);
#else
    localtime_r(&now, &timeinfo);
#endif

    std::ostringstream oss;
    oss << std::put_time(&timeinfo);
    oss << " [" << context << "] ";

    // Add log level prefix
    switch (level) {
        case LogLevel::DEBUG:
            oss << "[DEBUG] ";
            break;
        case LogLevel::INFO:
            oss << "[INFO] ";
            break;
        case LogLevel::WARNING:
            oss << "[WARNING] ";
            break;
        case LogLevel::ERROR:
            oss << "[ERROR] ";
            break;
        case LogLevel::FATAL:
            oss << "[FATAL] ";
            break;
    }

    oss << message;

    // Output to appropriate stream
    if (level >= LogLevel::ERROR) {
        std::cerr << oss.str() << std::endl;
    } else {
        std::cout << oss.str() << std::endl;
    }
}

} // namespace omnicpp
