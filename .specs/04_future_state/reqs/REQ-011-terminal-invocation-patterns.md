# REQ-011: Terminal Invocation Patterns

**Requirement ID:** REQ-011
**Title:** Terminal Invocation Patterns
**Status:** Draft
**Created:** 2026-01-07
**Last Updated:** 2026-01-07

---

## Description

The build system shall support different terminal invocation patterns for different platforms and compilers. Terminal invocation shall handle environment setup, command execution, and output capture correctly.

## Acceptance Criteria

- [ ] Terminal invocation module exists in omni_scripts/utils/terminal_utils.py
- [ ] Standard shell invocation works (bash, zsh, PowerShell)
- [ ] MSVC Developer Command Prompt invocation works
- [ ] MSYS2 terminal invocation works
- [ ] Environment variables are set correctly
- [ ] Command output is captured and logged
- [ ] Exit codes are returned correctly
- [ ] Timeout handling is implemented
- [ ] Error handling is implemented
- [ ] Cross-platform compatibility is maintained

## Priority

**Critical** - Terminal invocation is essential for compiler and build tool execution.

## Dependencies

- **REQ-009:** Platform detection (required for terminal selection)
- **REQ-010:** Compiler detection (required for terminal selection)

## Related ADRs

- None directly, but supports all compiler-related ADRs

## Test Cases

### Unit Tests

1. **Test Standard Shell Invocation**
   - **Description:** Verify standard shell invocation works
   - **Steps:**
     1. Invoke command in bash
     2. Verify command executes
     3. Verify output is captured
   - **Expected Result:** Command executes successfully

2. **Test PowerShell Invocation**
   - **Description:** Verify PowerShell invocation works
   - **Steps:**
     1. Invoke command in PowerShell
     2. Verify command executes
     3. Verify output is captured
   - **Expected Result:** Command executes successfully

3. **Test Environment Variable Setting**
   - **Description:** Verify environment variables are set correctly
   - **Steps:**
     1. Set environment variable
     2. Invoke command
     3. Verify variable is available
   - **Expected Result:** Environment variable set correctly

4. **Test Output Capture**
   - **Description:** Verify output is captured correctly
   - **Steps:**
     1. Invoke command with output
     2. Verify stdout is captured
     3. Verify stderr is captured
   - **Expected Result:** Output captured correctly

5. **Test Exit Code Handling**
   - **Description:** Verify exit codes are returned correctly
   - **Steps:**
     1. Invoke command that fails
     2. Verify exit code is non-zero
     3. Invoke command that succeeds
     4. Verify exit code is zero
   - **Expected Result:** Exit codes returned correctly

### Integration Tests

1. **Test MSVC Terminal Invocation**
   - **Description:** Verify MSVC terminal invocation works
   - **Steps:**
     1. Invoke MSVC Developer Command Prompt
     2. Execute MSVC compiler
     3. Verify compilation succeeds
   - **Expected Result:** MSVC compiler executes successfully

2. **Test MSYS2 Terminal Invocation**
   - **Description:** Verify MSYS2 terminal invocation works
   - **Steps:**
     1. Invoke MSYS2 terminal
     2. Execute MinGW compiler
     3. Verify compilation succeeds
   - **Expected Result:** MinGW compiler executes successfully

## Implementation Notes

- Use subprocess for command invocation
- Support different shell types (bash, zsh, PowerShell, cmd)
- Handle environment variable setting
- Capture stdout and stderr separately
- Implement timeout handling
- Implement error handling
- Provide invoke_command() function
- Provide invoke_in_terminal() function
- Log command execution
- Handle cross-platform differences
- Support command chaining

## References

- [`.specs/01_standards/coding_standards.md`](../01_standards/coding_standards.md) - Cross-Platform Guidelines section
- [`.specs/04_future_state/manifest.md`](../04_future_state/manifest.md) - Future state structure
