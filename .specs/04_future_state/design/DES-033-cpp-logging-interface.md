# DES-033: C++ Logging Interface (spdlog wrapper)

## Overview

Defines the C++ logging interface for the OmniCpp game engine, wrapping spdlog functionality.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_CPP_LOGGING_INTERFACE_H
#define OMNICPP_CPP_LOGGING_INTERFACE_H

#include <string>
#include <memory>
#include <functional>
#include <vector>
#include <unordered_map>

namespace omnicpp {
namespace logging {

// Log level
enum class LogLevel {
    TRACE,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    CRITICAL,
    OFF
};

// Log pattern
enum class LogPattern {
    DEFAULT,
    DETAILED,
    COMPACT,
    JSON,
    CUSTOM
};

// Log sink type
enum class LogSinkType {
    CONSOLE,
    FILE,
    ROTATING_FILE,
    DAILY_FILE,
    CUSTOM
};

// Log message
struct LogMessage {
    LogLevel level;
    std::string message;
    std::string logger_name;
    std::string file;
    int line;
    std::string function;
    std::chrono::system_clock::time_point timestamp;
    std::thread::id thread_id;

    LogMessage()
        : level(LogLevel::INFO)
        , logger_name("")
        , file("")
        , line(0)
        , function("")
        , timestamp(std::chrono::system_clock::now())
        , thread_id(std::this_thread::get_id())
    {}
};

// Log sink configuration
struct LogSinkConfig {
    LogSinkType type;
    std::string path;
    std::string pattern;
    bool async;
    int queue_size;
    bool flush_on_error;

    LogSinkConfig()
        : type(LogSinkType::CONSOLE)
        , path("")
        , pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%l] %v")
        , async(false)
        , queue_size(8192)
        , flush_on_error(true)
    {}
};

// Logger configuration
struct LoggerConfig {
    std::string name;
    LogLevel level;
    LogPattern pattern;
    std::vector<LogSinkConfig> sinks;
    bool flush_every;
    int flush_interval_ms;

    LoggerConfig()
        : name("OmniCppLogger")
        , level(LogLevel::INFO)
        , pattern(LogPattern::DEFAULT)
        , flush_every(false)
        , flush_interval_ms(1000)
    {}
};

// Logger interface
class ILogger {
public:
    virtual ~ILogger() = default;

    // Logging methods
    virtual void trace(const std::string& message) = 0;
    virtual void debug(const std::string& message) = 0;
    virtual void info(const std::string& message) = 0;
    virtual void warn(const std::string& message) = 0;
    virtual void error(const std::string& message) = 0;
    virtual void critical(const std::string& message) = 0;

    // Formatted logging
    virtual void trace(const char* format, ...) = 0;
    virtual void debug(const char* format, ...) = 0;
    virtual void info(const char* format, ...) = 0;
    virtual void warn(const char* format, ...) = 0;
    virtual void error(const char* format, ...) = 0;
    virtual void critical(const char* format, ...) = 0;

    // Log level
    virtual void set_level(LogLevel level) = 0;
    virtual LogLevel get_level() const = 0;

    // Logger name
    virtual const std::string& get_name() const = 0;
    virtual void set_name(const std::string& name) = 0;

    // Flush
    virtual void flush() = 0;

    // Sink management
    virtual void add_sink(const LogSinkConfig& config) = 0;
    virtual void remove_sink(const std::string& sink_name) = 0;
    virtual std::vector<std::string> get_sink_names() const = 0;

    // Pattern
    virtual void set_pattern(LogPattern pattern) = 0;
    virtual void set_custom_pattern(const std::string& pattern) = 0;
    virtual LogPattern get_pattern() const = 0;
    virtual const std::string& get_custom_pattern() const = 0;

    // Async logging
    virtual void set_async(bool async) = 0;
    virtual bool is_async() const = 0;

    // Flush interval
    virtual void set_flush_interval(int interval_ms) = 0;
    virtual int get_flush_interval() const = 0;
};

// Logger factory
class ILoggerFactory {
public:
    virtual ~ILoggerFactory() = default;

    virtual std::unique_ptr<ILogger> create_logger(const LoggerConfig& config) = 0;
    virtual void destroy_logger(std::unique_ptr<ILogger> logger) = 0;
};

// Logger manager
class ILoggerManager {
public:
    virtual ~ILoggerManager() = default;

    // Logger management
    virtual void register_logger(const std::string& name, std::unique_ptr<ILogger> logger) = 0;
    virtual void unregister_logger(const std::string& name) = 0;
    virtual ILogger* get_logger(const std::string& name) = 0;
    virtual const ILogger* get_logger(const std::string& name) const = 0;
    virtual std::vector<std::string> get_logger_names() const = 0;

    // Default logger
    virtual void set_default_logger(const std::string& name) = 0;
    virtual ILogger* get_default_logger() = 0;
    virtual const ILogger* get_default_logger() const = 0;

    // Global log level
    virtual void set_global_level(LogLevel level) = 0;
    virtual LogLevel get_global_level() const = 0;

    // Flush all loggers
    virtual void flush_all() = 0;

    // Shutdown
    virtual void shutdown() = 0;
};

// Log listener
using LogListener = std::function<void(const LogMessage&)>;

// Log listener manager
class ILogListenerManager {
public:
    virtual ~ILogListenerManager() = default;

    virtual void add_listener(LogListener listener) = 0;
    virtual void remove_listener(LogListener listener) = 0;
    virtual void clear_listeners() = 0;
    virtual void notify_listeners(const LogMessage& message) = 0;
};

// Log statistics
struct LogStatistics {
    uint64_t total_messages;
    uint64_t trace_messages;
    uint64_t debug_messages;
    uint64_t info_messages;
    uint64_t warn_messages;
    uint64_t error_messages;
    uint64_t critical_messages;
    uint64_t dropped_messages;
    double average_message_size;

    LogStatistics()
        : total_messages(0)
        , trace_messages(0)
        , debug_messages(0)
        , info_messages(0)
        , warn_messages(0)
        , error_messages(0)
        , critical_messages(0)
        , dropped_messages(0)
        , average_message_size(0.0)
    {}
};

// Log statistics collector
class ILogStatisticsCollector {
public:
    virtual ~ILogStatisticsCollector() = default;

    virtual void record_message(const LogMessage& message) = 0;
    virtual const LogStatistics& get_statistics() const = 0;
    virtual void reset_statistics() = 0;
};

// Default logger implementation
class DefaultLogger : public ILogger {
private:
    std::string m_name;
    LogLevel m_level;
    LogPattern m_pattern;
    std::string m_custom_pattern;
    std::vector<std::unique_ptr<ILogger>> m_sinks;
    bool m_async;
    int m_flush_interval_ms;
    std::unique_ptr<ILogListenerManager> m_listener_manager;
    std::unique_ptr<ILogStatisticsCollector> m_statistics_collector;

public:
    DefaultLogger(const LoggerConfig& config);
    virtual ~DefaultLogger();

    void trace(const std::string& message) override;
    void debug(const std::string& message) override;
    void info(const std::string& message) override;
    void warn(const std::string& message) override;
    void error(const std::string& message) override;
    void critical(const std::string& message) override;

    void trace(const char* format, ...) override;
    void debug(const char* format, ...) override;
    void info(const char* format, ...) override;
    void warn(const char* format, ...) override;
    void error(const char* format, ...) override;
    void critical(const char* format, ...) override;

    void set_level(LogLevel level) override;
    LogLevel get_level() const override;

    const std::string& get_name() const override;
    void set_name(const std::string& name) override;

    void flush() override;

    void add_sink(const LogSinkConfig& config) override;
    void remove_sink(const std::string& sink_name) override;
    std::vector<std::string> get_sink_names() const override;

    void set_pattern(LogPattern pattern) override;
    void set_custom_pattern(const std::string& pattern) override;
    LogPattern get_pattern() const override;
    const std::string& get_custom_pattern() const override;

    void set_async(bool async) override;
    bool is_async() const override;

    void set_flush_interval(int interval_ms) override;
    int get_flush_interval() const override;

private:
    void log_message(LogLevel level, const std::string& message);
    std::string format_message(const LogMessage& message) const;
    std::string level_to_string(LogLevel level) const;
};

// Default logger manager implementation
class DefaultLoggerManager : public ILoggerManager {
private:
    std::unordered_map<std::string, std::unique_ptr<ILogger>> m_loggers;
    std::string m_default_logger_name;
    LogLevel m_global_level;

public:
    DefaultLoggerManager();
    virtual ~DefaultLoggerManager();

    void register_logger(const std::string& name, std::unique_ptr<ILogger> logger) override;
    void unregister_logger(const std::string& name) override;
    ILogger* get_logger(const std::string& name) override;
    const ILogger* get_logger(const std::string& name) const override;
    std::vector<std::string> get_logger_names() const override;

    void set_default_logger(const std::string& name) override;
    ILogger* get_default_logger() override;
    const ILogger* get_default_logger() const override;

    void set_global_level(LogLevel level) override;
    LogLevel get_global_level() const override;

    void flush_all() override;
    void shutdown() override;
};

// Default log listener manager implementation
class DefaultLogListenerManager : public ILogListenerManager {
private:
    std::vector<LogListener> m_listeners;

public:
    DefaultLogListenerManager();
    virtual ~DefaultLogListenerManager();

    void add_listener(LogListener listener) override;
    void remove_listener(LogListener listener) override;
    void clear_listeners() override;
    void notify_listeners(const LogMessage& message) override;
};

// Default log statistics collector implementation
class DefaultLogStatisticsCollector : public ILogStatisticsCollector {
private:
    LogStatistics m_statistics;
    std::vector<size_t> m_message_sizes;

public:
    DefaultLogStatisticsCollector();
    virtual ~DefaultLogStatisticsCollector();

    void record_message(const LogMessage& message) override;
    const LogStatistics& get_statistics() const override;
    void reset_statistics() override;
};

// Global logger accessor
class GlobalLogger {
private:
    static std::unique_ptr<ILoggerManager> s_logger_manager;

public:
    static void initialize(const LoggerConfig& config);
    static void shutdown();

    static ILogger* get_logger(const std::string& name = "");
    static ILogger* get_default_logger();

    static void set_global_level(LogLevel level);
    static LogLevel get_global_level();

    static void flush_all();

    static void trace(const std::string& message);
    static void debug(const std::string& message);
    static void info(const std::string& message);
    static void warn(const std::string& message);
    static void error(const std::string& message);
    static void critical(const std::string& message);
};

} // namespace logging
} // namespace omnicpp

#endif // OMNICPP_CPP_LOGGING_INTERFACE_H
```

## Dependencies

### Internal Dependencies

- `DES-021` - Engine Core Interfaces

### External Dependencies

- `string` - String handling
- `memory` - Smart pointers
- `functional` - Function objects
- `vector` - Dynamic arrays
- `unordered_map` - Hash map
- `chrono` - Time handling
- `thread` - Thread handling
- `cstdarg` - Variable arguments

## Related Requirements

- REQ-053: C++ Logging System
- REQ-054: Log Configuration

## Related ADRs

- ADR-003: Logging Architecture

## Implementation Notes

### Logger Design

1. Abstract logger interface
2. Multiple log levels
3. Multiple sink types
4. Async logging support

### Log Levels

1. TRACE - Most verbose
2. DEBUG - Debug information
3. INFO - General information
4. WARN - Warning messages
5. ERROR - Error messages
6. CRITICAL - Critical errors
7. OFF - Logging disabled

### Log Sinks

1. Console sink
2. File sink
3. Rotating file sink
4. Daily file sink
5. Custom sink

### Log Patterns

1. Default pattern
2. Detailed pattern
3. Compact pattern
4. JSON pattern
5. Custom pattern

## Usage Example

```cpp
#include "cpp_logging_interface.hpp"

using namespace omnicpp::logging;

int main() {
    // Create logger configuration
    LoggerConfig config;
    config.name = "MyLogger";
    config.level = LogLevel::DEBUG;
    config.pattern = LogPattern::DETAILED;

    // Add console sink
    LogSinkConfig console_sink;
    console_sink.type = LogSinkType::CONSOLE;
    console_sink.async = true;
    console_sink.queue_size = 8192;
    config.sinks.push_back(console_sink);

    // Add file sink
    LogSinkConfig file_sink;
    file_sink.type = LogSinkType::FILE;
    file_sink.path = "logs/myapp.log";
    file_sink.async = true;
    config.sinks.push_back(file_sink);

    // Create logger
    auto logger = std::make_unique<DefaultLogger>(config);

    // Log messages
    logger->trace("This is a trace message");
    logger->debug("This is a debug message");
    logger->info("This is an info message");
    logger->warn("This is a warning message");
    logger->error("This is an error message");
    logger->critical("This is a critical message");

    // Formatted logging
    logger->info("User %s logged in at %s", "john", "10:00");
    logger->error("Failed to load file: %s (line %d)", "config.json", 42);

    // Set log level
    logger->set_level(LogLevel::WARN);

    // Flush logger
    logger->flush();

    // Use global logger
    GlobalLogger::initialize(config);
    GlobalLogger::info("Global logger initialized");
    GlobalLogger::error("An error occurred");
    GlobalLogger::flush_all();
    GlobalLogger::shutdown();

    return 0;
}
```
