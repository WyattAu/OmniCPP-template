/**
 * @file test_quill_logger.cpp
 * @brief Unit tests for QuillLogger
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/logging/QuillLogger.hpp"

namespace omnicpp {
namespace test {

class QuillLoggerTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create logger for each test
        logger_ = std::make_unique<QuillLogger>("test_logger");
    }

    void TearDown() override {
        if (logger_) {
            logger_->shutdown();
        }
    }

    std::unique_ptr<QuillLogger> logger_;
};

TEST_F(QuillLoggerTest, DefaultInitialization) {
    ASSERT_TRUE(logger_->initialize());
    ASSERT_EQ(logger_->get_log_level(), LogLevel::INFO);
}

TEST_F(QuillLoggerTest, InitializationWithConfig) {
    // Test with non-existent config file (should use defaults)
    ASSERT_TRUE(logger_->initialize("nonexistent_config.json"));
}

TEST_F(QuillLoggerTest, LogLevelSetting) {
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

TEST_F(QuillLoggerTest, LogMessages) {
    ASSERT_TRUE(logger_->initialize());

    // Log messages at different levels
    logger_->log(LogLevel::TRACE, "Trace message");
    logger_->log(LogLevel::DEBUG, "Debug message");
    logger_->log(LogLevel::INFO, "Info message");
    logger_->log(LogLevel::WARNING, "Warning message");
    logger_->log(LogLevel::ERROR, "Error message");
    logger_->log(LogLevel::FATAL, "Fatal message");

    // Test with category
    logger_->log(LogLevel::INFO, "Message with category", "TEST");

    // No assertion needed - just verify no crashes
    SUCCEED();
}

TEST_F(QuillLoggerTest, ConsoleOutputToggle) {
    ASSERT_TRUE(logger_->initialize());

    // Toggle console output
    logger_->set_console_output(false);
    logger_->set_console_output(true);

    SUCCEED();
}

TEST_F(QuillLoggerTest, FileOutputToggle) {
    ASSERT_TRUE(logger_->initialize());

    // Toggle file output
    logger_->set_file_output(false);
    logger_->set_file_output(true, "test.log");

    SUCCEED();
}

TEST_F(QuillLoggerTest, Flush) {
    ASSERT_TRUE(logger_->initialize());

    // Log some messages
    logger_->log(LogLevel::INFO, "Message before flush");

    // Flush
    logger_->flush();

    // Log after flush
    logger_->log(LogLevel::INFO, "Message after flush");

    SUCCEED();
}

TEST_F(QuillLoggerTest, MultipleLogLevels) {
    ASSERT_TRUE(logger_->initialize());

    // Set to trace and log
    logger_->set_log_level(LogLevel::TRACE);
    logger_->log(LogLevel::TRACE, "Trace should appear");

    // Set to error and verify trace doesn't crash
    logger_->set_log_level(LogLevel::ERROR);
    logger_->log(LogLevel::TRACE, "Trace should not appear");

    SUCCEED();
}

} // namespace test
} // namespace omnicpp
