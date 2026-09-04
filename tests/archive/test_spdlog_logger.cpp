/**
 * @file test_spdlog_logger.cpp
 * @brief Unit tests for SpdLogLogger
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/logging/SpdLogLogger.hpp"

namespace omnicpp {
namespace test {

class SpdLogLoggerTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create logger for each test
        logger_ = std::make_unique<SpdLogLogger>("test_logger");
    }

    void TearDown() override {
        if (logger_) {
            logger_->shutdown();
        }
    }

    std::unique_ptr<SpdLogLogger> logger_;
};

TEST_F(SpdLogLoggerTest, DefaultInitialization) {
    ASSERT_TRUE(logger_->initialize());
    ASSERT_EQ(logger_->get_log_level(), LogLevel::INFO);
}

TEST_F(SpdLogLoggerTest, InitializationWithConfig) {
    // Test with non-existent config file (should use defaults)
    ASSERT_TRUE(logger_->initialize("nonexistent_config.json"));
}

TEST_F(SpdLogLoggerTest, LogLevelSetting) {
    ASSERT_TRUE(logger_->initialize());

    logger_->set_log_level(LogLevel::DEBUG);
    ASSERT_EQ(logger_->get_log_level(), LogLevel::DEBUG);

    logger_->set_log_level(LogLevel::WARNING);
    ASSERT_EQ(logger_->get_log_level(), LogLevel::WARNING);

    logger_->set_log_level(LogLevel::ERROR);
    ASSERT_EQ(logger_->get_log_level(), LogLevel::ERROR);

    logger_->set_log_level(LogLevel::TRACE);
    ASSERT_EQ(logger_->get_log_level(), LogLevel::TRACE);

    logger_->set_log_level(LogLevel::FATAL);
    ASSERT_EQ(logger_->get_log_level(), LogLevel::FATAL);
}

TEST_F(SpdLogLoggerTest, ConsoleOutputToggle) {
    ASSERT_TRUE(logger_->initialize());

    // Should not crash
    logger_->set_console_output(true);
    logger_->set_console_output(false);
    logger_->set_console_output(true);
}

TEST_F(SpdLogLoggerTest, FileOutputToggle) {
    ASSERT_TRUE(logger_->initialize());

    // Should not crash
    logger_->set_file_output(true, "test.log");
    logger_->set_file_output(false, nullptr);
    logger_->set_file_output(true, "test2.log");
}

TEST_F(SpdLogLoggerTest, LogMessageWithCategory) {
    ASSERT_TRUE(logger_->initialize());

    // Should not crash
    logger_->log(LogLevel::INFO, "Test message", "TestCategory");
    logger_->log(LogLevel::WARNING, "Warning message", "WarningCategory");
    logger_->log(LogLevel::ERROR, "Error message", "ErrorCategory");
    logger_->log(LogLevel::DEBUG, "Debug message", "DebugCategory");
    logger_->log(LogLevel::TRACE, "Trace message", "TraceCategory");
    logger_->log(LogLevel::FATAL, "Fatal message", "FatalCategory");
}

TEST_F(SpdLogLoggerTest, LogMessageWithoutCategory) {
    ASSERT_TRUE(logger_->initialize());

    // Should not crash
    logger_->log(LogLevel::INFO, "Test message", nullptr);
    logger_->log(LogLevel::WARNING, "Warning message", nullptr);
    logger_->log(LogLevel::ERROR, "Error message", nullptr);
}

TEST_F(SpdLogLoggerTest, Flush) {
    ASSERT_TRUE(logger_->initialize());

    logger_->log(LogLevel::INFO, "Message before flush", nullptr);
    logger_->flush();

    // Should not crash
    logger_->flush();
}

TEST_F(SpdLogLoggerTest, MultipleInitialization) {
    ASSERT_TRUE(logger_->initialize());
    logger_->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(logger_->initialize());
    logger_->shutdown();
}

TEST_F(SpdLogLoggerTest, GetSpdLogLogger) {
    ASSERT_TRUE(logger_->initialize());

    auto spdlog_logger = logger_->get_spdlog_logger();
    ASSERT_NE(spdlog_logger, nullptr);
}

TEST_F(SpdLogLoggerTest, LogAtDifferentLevels) {
    ASSERT_TRUE(logger_->initialize());

    // Set to TRACE to allow all levels
    logger_->set_log_level(LogLevel::TRACE);

    logger_->log(LogLevel::TRACE, "Trace message", nullptr);
    logger_->log(LogLevel::DEBUG, "Debug message", nullptr);
    logger_->log(LogLevel::INFO, "Info message", nullptr);
    logger_->log(LogLevel::WARNING, "Warning message", nullptr);
    logger_->log(LogLevel::ERROR, "Error message", nullptr);
    logger_->log(LogLevel::FATAL, "Fatal message", nullptr);
}

TEST_F(SpdLogLoggerTest, LogFiltering) {
    ASSERT_TRUE(logger_->initialize());

    // Set to ERROR level
    logger_->set_log_level(LogLevel::ERROR);

    // These should be filtered out
    logger_->log(LogLevel::TRACE, "Trace message", nullptr);
    logger_->log(LogLevel::DEBUG, "Debug message", nullptr);
    logger_->log(LogLevel::INFO, "Info message", nullptr);
    logger_->log(LogLevel::WARNING, "Warning message", nullptr);

    // These should be logged
    logger_->log(LogLevel::ERROR, "Error message", nullptr);
    logger_->log(LogLevel::FATAL, "Fatal message", nullptr);
}

TEST_F(SpdLogLoggerTest, EmptyMessage) {
    ASSERT_TRUE(logger_->initialize());

    // Should not crash with empty message
    logger_->log(LogLevel::INFO, "", nullptr);
}

TEST_F(SpdLogLoggerTest, LongMessage) {
    ASSERT_TRUE(logger_->initialize());

    // Create a long message
    std::string long_message(10000, 'A');
    logger_->log(LogLevel::INFO, long_message.c_str(), nullptr);
}

TEST_F(SpdLogLoggerTest, MultipleLoggers) {
    auto logger1 = std::make_unique<SpdLogLogger>("logger1");
    auto logger2 = std::make_unique<SpdLogLogger>("logger2");

    ASSERT_TRUE(logger1->initialize());
    ASSERT_TRUE(logger2->initialize());

    logger1->log(LogLevel::INFO, "Message from logger1", nullptr);
    logger2->log(LogLevel::INFO, "Message from logger2", nullptr);

    logger1->shutdown();
    logger2->shutdown();
}

TEST_F(SpdLogLoggerTest, ShutdownWithoutInitialize) {
    // Should not crash
    logger_->shutdown();
}

TEST_F(SpdLogLoggerTest, LogAfterShutdown) {
    ASSERT_TRUE(logger_->initialize());
    logger_->shutdown();

    // Should not crash (though may not log)
    logger_->log(LogLevel::INFO, "Message after shutdown", nullptr);
}

} // namespace test
} // namespace omnicpp
