# REQ-005: Logging Configuration and Custom Formatters

**Requirement ID:** REQ-005
**Title:** Logging Configuration and Custom Formatters
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall provide comprehensive logging configuration with custom formatters for both Python and C++ components. Logging shall support multiple log levels, file rotation, colored console output, and structured logging with context.

## Acceptance Criteria

- [ ] Logging configuration exists in config/logging_python.json
- [ ] Logging configuration exists in config/logging_cpp.json
- [ ] Custom formatters are implemented in omni_scripts/logging/formatters.py
- [ ] Colored console formatter is implemented
- [ ] Structured logging formatter is implemented
- [ ] Rotating file handler is implemented
- [ ] Log levels are configurable (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- [ ] Log rotation is configurable (max file size, backup count)
- [ ] Logging can be initialized from configuration file
- [ ] Logger instances can be retrieved by name
- [ ] Sensitive data redaction is implemented
- [ ] Log format is consistent across Python and C++

## Priority

**High** - Logging is critical for debugging and monitoring.

## Dependencies

- **REQ-003:** Type hints enforcement (requires typed logging interfaces)
- **REQ-004:** Python script consolidation (requires unified logging system)

## Related ADRs

- None directly, but supports all ADRs by providing logging infrastructure

## Test Cases

### Unit Tests

1. **Test Logging Initialization**

   - **Description:** Verify logging can be initialized from configuration
   - **Steps:**
     1. Load logging configuration from config/logging_python.json
     2. Initialize logging system
     3. Verify loggers are created
   - **Expected Result:** Logging system initialized successfully

2. **Test Colored Formatter**

   - **Description:** Verify colored console formatter works correctly
   - **Steps:**
     1. Create logger with colored formatter
     2. Log messages at different levels
     3. Verify colors are applied correctly
   - **Expected Result:** Log levels have distinct colors

3. **Test Structured Formatter**

   - **Description:** Verify structured logging with context works
   - **Steps:**
     1. Log message with extra context
     2. Verify context is included in output
     3. Verify format is consistent
   - **Expected Result:** Context is included in log output

4. **Test Rotating File Handler**

   - **Description:** Verify log file rotation works correctly
   - **Steps:**
     1. Create logger with rotating file handler
     2. Write enough data to trigger rotation
     3. Verify backup files are created
     4. Verify old files are deleted
   - **Expected Result:** Log files rotate correctly

5. **Test Sensitive Data Redaction**
   - **Description:** Verify sensitive data is redacted from logs
   - **Steps:**
     1. Log message containing password
     2. Log message containing API key
     3. Verify sensitive data is redacted
   - **Expected Result:** Sensitive data replaced with \*\*\*

### Integration Tests

1. **Test Python and C++ Logging Consistency**

   - **Description:** Verify Python and C++ logging formats are consistent
   - **Steps:**
     1. Configure Python logging
     2. Configure C++ logging
     3. Log messages from both
     4. Compare formats
   - **Expected Result:** Formats are consistent

2. **Test Logging Performance**
   - **Description:** Verify logging does not significantly impact performance
   - **Steps:**
     1. Log large number of messages
     2. Measure time taken
     3. Verify performance is acceptable
   - **Expected Result:** Logging performance is acceptable

## Implementation Notes

- Use Python's logging.config.dictConfig for initialization
- Implement custom formatters in omni_scripts/logging/formatters.py
- Use RotatingFileHandler for log rotation
- Implement sensitive data redaction in formatters
- Support both colored and plain text output
- Use structured logging with extra context
- Configure C++ logging with spdlog from config/logging_cpp.json
- Ensure log format is consistent between Python and C++

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Logging Standards section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future logging architecture
