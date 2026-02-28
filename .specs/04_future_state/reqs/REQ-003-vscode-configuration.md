# REQ-003: VSCode Configuration

**Requirement ID:** REQ-003
**Title:** VSCode Configuration
**Status:** Draft
**Created:** 2026-01-27
**Last Updated:** 2026-01-27

---

## Description

The VSCode configuration files ([`tasks.json`](../../.vscode/tasks.json:1) and [`launch.json`](../../.vscode/launch.json:1)) shall be enhanced with Linux-specific build tasks, debug configurations, Nix shell integration, CachyOS validation, and platform-specific task selection.

### Overview

The system shall:
1. Add Linux build tasks for GCC and Clang
2. Add Linux debug configurations for GDB and LLDB
3. Add Nix shell task for environment setup
4. Add CachyOS validation task
5. Implement platform-specific task selection

---

## REQ-003-001: Add Linux Build Tasks

### Description

The [`tasks.json`](../../.vscode/tasks.json:1) shall include Linux-specific build tasks for GCC and Clang compilers with debug and release configurations.

### Functional Requirements

The system shall:
1. Add "Configure Build (Linux GCC - Debug)" task
2. Add "Configure Build (Linux GCC - Release)" task
3. Add "Configure Build (Linux Clang - Debug)" task
4. Add "Configure Build (Linux Clang - Release)" task
5. Add "Build Engine (Linux GCC - Debug)" task
6. Add "Build Engine (Linux GCC - Release)" task
7. Add "Build Engine (Linux Clang - Debug)" task
8. Add "Build Engine (Linux Clang - Release)" task
9. Add "Build Game (Linux GCC - Debug)" task
10. Add "Build Game (Linux GCC - Release)" task
11. Add "Build Game (Linux Clang - Debug)" task
12. Add "Build Game (Linux Clang - Release)" task
13. Add "Build Standalone (Linux GCC - Debug)" task
14. Add "Build Standalone (Linux GCC - Release)" task
15. Add "Build Standalone (Linux Clang - Debug)" task
16. Add "Build Standalone (Linux Clang - Release)" task
17. Add "--use-nix" flag to all Linux tasks
18. Set problemMatcher to "$gcc" for GCC tasks
19. Set problemMatcher to "$clang" for Clang tasks
20. Set group.kind to "build" for all build tasks

### Acceptance Criteria

- [ ] "Configure Build (Linux GCC - Debug)" task exists
- [ ] "Configure Build (Linux GCC - Release)" task exists
- [ ] "Configure Build (Linux Clang - Debug)" task exists
- [ ] "Configure Build (Linux Clang - Release)" task exists
- [ ] "Build Engine (Linux GCC - Debug)" task exists
- [ ] "Build Engine (Linux GCC - Release)" task exists
- [ ] "Build Engine (Linux Clang - Debug)" task exists
- [ ] "Build Engine (Linux Clang - Release)" task exists
- [ ] "Build Game (Linux GCC - Debug)" task exists
- [ ] "Build Game (Linux GCC - Release)" task exists
- [ ] "Build Game (Linux Clang - Debug)" task exists
- [ ] "Build Game (Linux Clang - Release)" task exists
- [ ] "Build Standalone (Linux GCC - Debug)" task exists
- [ ] "Build Standalone (Linux GCC - Release)" task exists
- [ ] "Build Standalone (Linux Clang - Debug)" task exists
- [ ] "Build Standalone (Linux Clang - Release)" task exists
- [ ] All tasks include "--use-nix" flag
- [ ] GCC tasks use "$gcc" problemMatcher
- [ ] Clang tasks use "$clang" problemMatcher
- [ ] All tasks are in "build" group

### Priority

**High** - Linux build tasks are essential for Linux development.

### Dependencies

- REQ-001-008: Generate Linux build commands

### Related ADRs

- [ADR-026: VSCode Tasks and Launch Configuration](../02_adrs/ADR-026-vscode-tasks-launch-configuration.md)
- [ADR-032: VSCode Platform-Specific Tasks](../02_adrs/ADR-032-vscode-platform-specific-tasks.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Linux GCC Build Task**
   - **Description:** Verify Linux GCC build task works
   - **Steps:**
     1. Open VSCode on Linux
     2. Run "Build Engine (Linux GCC - Debug)" task
     3. Verify build succeeds
     4. Verify output is captured
   - **Expected Result:** Build task works correctly

2. **Test Linux Clang Build Task**
   - **Description:** Verify Linux Clang build task works
   - **Steps:**
     1. Open VSCode on Linux
     2. Run "Build Engine (Linux Clang - Debug)" task
     3. Verify build succeeds
     4. Verify output is captured
   - **Expected Result:** Build task works correctly

---

## REQ-003-002: Add Linux Debug Configurations

### Description

The [`launch.json`](../../.vscode/launch.json:1) shall include Linux-specific debug configurations for GDB and LLDB debuggers.

### Functional Requirements

The system shall:
1. Add "Debug Engine (Linux GDB)" configuration
2. Add "Debug Engine (Linux LLDB)" configuration
3. Add "Debug Game (Linux GDB)" configuration
4. Add "Debug Game (Linux LLDB)" configuration
5. Add "Debug Standalone (Linux GDB)" configuration
6. Add "Debug Standalone (Linux LLDB)" configuration
7. Set "type" to "cppdbg" for all configurations
8. Set "request" to "launch" for all configurations
9. Set "MIMode" to "gdb" for GDB configurations
10. Set "MIMode" to "lldb" for LLDB configurations
11. Set "miDebuggerPath" to "gdb" for GDB configurations
12. Set "miDebuggerPath" to "lldb" for LLDB configurations
13. Set "setupCommands" for GDB pretty-printers
14. Set "setupCommands" for LLDB pretty-printers
15. Set "preLaunchTask" to appropriate build task
16. Set "cwd" to "${workspaceFolder}"
17. Set "externalConsole" to false
18. Set "stopAtEntry" to false

### Acceptance Criteria

- [ ] "Debug Engine (Linux GDB)" configuration exists
- [ ] "Debug Engine (Linux LLDB)" configuration exists
- [ ] "Debug Game (Linux GDB)" configuration exists
- [ ] "Debug Game (Linux LLDB)" configuration exists
- [ ] "Debug Standalone (Linux GDB)" configuration exists
- [ ] "Debug Standalone (Linux LLDB)" configuration exists
- [ ] All configurations have "type": "cppdbg"
- [ ] All configurations have "request": "launch"
- [ ] GDB configurations have "MIMode": "gdb"
- [ ] LLDB configurations have "MIMode": "lldb"
- [ ] GDB configurations have "miDebuggerPath": "gdb"
- [ ] LLDB configurations have "miDebuggerPath": "lldb"
- [ ] All configurations have "setupCommands"
- [ ] All configurations have "preLaunchTask"
- [ ] All configurations have "cwd": "${workspaceFolder}"

### Priority

**High** - Linux debug configurations are essential for debugging.

### Dependencies

- REQ-001-008: Generate Linux build commands

### Related ADRs

- [ADR-026: VSCode Tasks and Launch Configuration](../02_adrs/ADR-026-vscode-tasks-launch-configuration.md)
- [ADR-032: VSCode Platform-Specific Tasks](../02_adrs/ADR-032-vscode-platform-specific-tasks.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Linux GDB Debug Configuration**
   - **Description:** Verify Linux GDB debug configuration works
   - **Steps:**
     1. Open VSCode on Linux
     2. Set breakpoint in code
     3. Run "Debug Engine (Linux GDB)" configuration
     4. Verify debugger starts
     5. Verify breakpoint is hit
   - **Expected Result:** Debug configuration works correctly

2. **Test Linux LLDB Debug Configuration**
   - **Description:** Verify Linux LLDB debug configuration works
   - **Steps:**
     1. Open VSCode on Linux
     2. Set breakpoint in code
     3. Run "Debug Engine (Linux LLDB)" configuration
     4. Verify debugger starts
     5. Verify breakpoint is hit
   - **Expected Result:** Debug configuration works correctly

---

## REQ-003-003: Add Nix Shell Task

### Description

The [`tasks.json`](../../.vscode/tasks.json:1) shall include a task to load the Nix development shell.

### Functional Requirements

The system shall:
1. Add "Load Nix Shell" task
2. Set "type" to "shell"
3. Set "command" to "nix"
4. Set "args" to ["develop"]
5. Set "options.cwd" to "${workspaceFolder}"
6. Set "problemMatcher" to []
7. Set "group.kind" to "build"
8. Set "isDefault" to false
9. Set "detail" to "Load Nix development environment"
10. Set "presentation" to show in terminal

### Acceptance Criteria

- [ ] "Load Nix Shell" task exists
- [ ] Task has "type": "shell"
- [ ] Task has "command": "nix"
- [ ] Task has "args": ["develop"]
- [ ] Task has "options.cwd": "${workspaceFolder}"
- [ ] Task has "problemMatcher": []
- [ ] Task is in "build" group
- [ ] Task has "detail" description
- [ ] Task has "presentation" configuration

### Priority

**High** - Nix shell task is essential for Nix integration.

### Dependencies

- REQ-001-006: Integrate with Nix shell

### Related ADRs

- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-029: Direnv for Environment Management](../02_adrs/ADR-029-direnv-environment-management.md)

### Related Threats

- **TM-LX-001: Nix Package Manager Security Risks** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md:498)

### Test Cases

#### Integration Tests

1. **Test Nix Shell Task**
   - **Description:** Verify Nix shell task works
   - **Steps:**
     1. Open VSCode on Linux
     2. Run "Load Nix Shell" task
     3. Verify Nix shell loads
     4. Verify welcome message is displayed
   - **Expected Result:** Nix shell loads correctly

---

## REQ-003-004: Add CachyOS Validation Task

### Description

The [`tasks.json`](../../.vscode/tasks.json:1) shall include a task to validate the CachyOS build environment.

### Functional Requirements

The system shall:
1. Add "Validate CachyOS Environment" task
2. Set "type" to "shell"
3. Set "command" to "python"
4. Set "args" to ["OmniCppController.py", "validate", "--platform", "linux"]
5. Set "options.cwd" to "${workspaceFolder}"
6. Set "problemMatcher" to []
7. Set "group.kind" to "test"
8. Set "isDefault" to false
9. Set "detail" to "Validate CachyOS build environment"
10. Set "presentation" to show in terminal

### Acceptance Criteria

- [ ] "Validate CachyOS Environment" task exists
- [ ] Task has "type": "shell"
- [ ] Task has "command": "python"
- [ ] Task has "args": ["OmniCppController.py", "validate", "--platform", "linux"]
- [ ] Task has "options.cwd": "${workspaceFolder}"
- [ ] Task has "problemMatcher": []
- [ ] Task is in "test" group
- [ ] Task has "detail" description
- [ ] Task has "presentation" configuration

### Priority

**Medium** - CachyOS validation task is useful for environment verification.

### Dependencies

- REQ-001-007: Validate Linux build environment

### Related ADRs

- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test CachyOS Validation Task**
   - **Description:** Verify CachyOS validation task works
   - **Steps:**
     1. Open VSCode on CachyOS
     2. Run "Validate CachyOS Environment" task
     3. Verify validation runs
     4. Verify results are displayed
   - **Expected Result:** Validation task works correctly

---

## REQ-003-005: Platform-Specific Task Selection

### Description

The VSCode configuration shall provide platform-specific task selection to show only relevant tasks for the current platform.

### Functional Requirements

The system shall:
1. Add "when" clause to Linux-specific tasks
2. Set "when" clause to check for Linux platform
3. Hide Linux tasks on Windows
4. Hide Linux tasks on macOS
5. Hide Windows tasks on Linux
6. Hide macOS tasks on Linux
7. Show all tasks when platform cannot be determined
8. Document platform-specific task behavior in comments

### Acceptance Criteria

- [ ] Linux tasks have "when" clause
- [ ] Linux tasks are hidden on Windows
- [ ] Linux tasks are hidden on macOS
- [ ] Windows tasks are hidden on Linux
- [ ] macOS tasks are hidden on Linux
- [ ] All tasks are shown when platform is unknown
- [ ] Platform-specific behavior is documented

### Priority

**Medium** - Platform-specific task selection improves user experience.

### Dependencies

- REQ-003-001: Add Linux build tasks
- REQ-003-002: Add Linux debug configurations

### Related ADRs

- [ADR-032: VSCode Platform-Specific Tasks](../02_adrs/ADR-032-vscode-platform-specific-tasks.md)

### Related Threats

- None directly

### Test Cases

#### Integration Tests

1. **Test Linux Tasks on Linux**
   - **Description:** Verify Linux tasks are shown on Linux
   - **Steps:**
     1. Open VSCode on Linux
     2. Open Command Palette
     3. Run "Tasks: Run Task"
     4. Verify Linux tasks are shown
     5. Verify Windows tasks are hidden
   - **Expected Result:** Linux tasks are shown on Linux

2. **Test Linux Tasks on Windows**
   - **Description:** Verify Linux tasks are hidden on Windows
   - **Steps:**
     1. Open VSCode on Windows
     2. Open Command Palette
     3. Run "Tasks: Run Task"
     4. Verify Linux tasks are hidden
     5. Verify Windows tasks are shown
   - **Expected Result:** Linux tasks are hidden on Windows

---

## Implementation Notes

### tasks.json Structure

Add the following Linux-specific tasks to [`.vscode/tasks.json`](../../.vscode/tasks.json:1):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Configure Build (Linux GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "OmniCppController.py",
        "configure",
        "--compiler",
        "gcc",
        "--build-type",
        "Debug",
        "--use-nix"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": false
      },
      "detail": "Configure CMake project with GCC compiler for Debug build using Nix environment",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Configure Build (Linux GCC - Release)",
      "type": "shell",
      "command": "python",
      "args": [
        "OmniCppController.py",
        "configure",
        "--compiler",
        "gcc",
        "--build-type",
        "Release",
        "--use-nix"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": false
      },
      "detail": "Configure CMake project with GCC compiler for Release build using Nix environment"
    },
    {
      "label": "Build Engine (Linux GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "OmniCppController.py",
        "build",
        "engine",
        "Clean Build Pipeline",
        "gcc-debug",
        "debug",
        "--compiler",
        "gcc",
        "--use-nix"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": "$gcc",
      "group": {
        "kind": "build",
        "isDefault": false
      },
      "detail": "Build Engine with GCC compiler for Debug build using Nix environment"
    },
    {
      "label": "Build Engine (Linux Clang - Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "OmniCppController.py",
        "build",
        "engine",
        "Clean Build Pipeline",
        "clang-debug",
        "debug",
        "--compiler",
        "clang",
        "--use-nix"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": "$clang",
      "group": {
        "kind": "build",
        "isDefault": false
      },
      "detail": "Build Engine with Clang compiler for Debug build using Nix environment"
    },
    {
      "label": "Load Nix Shell",
      "type": "shell",
      "command": "nix",
      "args": ["develop"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": false
      },
      "detail": "Load Nix development environment",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Validate CachyOS Environment",
      "type": "shell",
      "command": "python",
      "args": [
        "OmniCppController.py",
        "validate",
        "--platform",
        "linux"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "group": {
        "kind": "test",
        "isDefault": false
      },
      "detail": "Validate CachyOS build environment",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

### launch.json Structure

Add the following Linux-specific debug configurations to [`.vscode/launch.json`](../../.vscode/launch.json:1):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Engine (Linux GDB)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/engine-debug/engine",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "miDebuggerPath": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        },
        {
          "description": "Set Disassembly Flavor to Intel",
          "text": "-gdb-set disassembly-flavor intel",
          "ignoreFailures": true
        }
      ],
      "preLaunchTask": "Build Engine (Linux GCC - Debug)"
    },
    {
      "name": "Debug Engine (Linux LLDB)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/engine-clang-debug/engine",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "lldb",
      "miDebuggerPath": "lldb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for lldb",
          "text": "settings set target.inline-breakpoint-strategy always",
          "ignoreFailures": true
        }
      ],
      "preLaunchTask": "Build Engine (Linux Clang - Debug)"
    }
  ]
}
```

### Platform Detection

Use VSCode's built-in platform detection:

```json
{
  "label": "Build Engine (Linux GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": [
    "OmniCppController.py",
    "build",
    "engine",
    "Clean Build Pipeline",
    "gcc-debug",
    "debug",
    "--compiler",
    "gcc",
    "--use-nix"
  ],
  "options": {
    "cwd": "${workspaceFolder}"
  },
  "problemMatcher": "$gcc",
  "group": {
    "kind": "build",
    "isDefault": false
  },
  "detail": "Build Engine with GCC compiler for Debug build using Nix environment",
  "presentation": {
    "reveal": "always",
    "panel": "new"
  },
  "when": {
    "os": ["linux"]
  }
}
```

### Task Organization

Organize tasks into logical groups:
- **Configure:** Configuration tasks
- **Build:** Build tasks (engine, game, standalone)
- **Test:** Test and validation tasks
- **Format:** Code formatting tasks
- **Lint:** Static analysis tasks

### Debug Configuration Organization

Organize debug configurations by:
- **Target:** Engine, Game, Standalone
- **Compiler:** GCC, Clang
- **Debugger:** GDB, LLDB

### Documentation

Add comments to [`tasks.json`](../../.vscode/tasks.json:1) and [`launch.json`](../../.vscode/launch.json:1) explaining:
- Platform-specific tasks
- Nix integration
- CachyOS-specific configurations
- Debug configuration setup

---

## References

- [`.specs/04_future_state/linux_expansion_manifest.md`](../04_future_state/linux_expansion_manifest.md) - Linux Expansion Manifest
- [ADR-026: VSCode Tasks and Launch Configuration](../02_adrs/ADR-026-vscode-tasks-launch-configuration.md)
- [ADR-027: Nix Package Manager Integration](../02_adrs/ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](../02_adrs/ADR-028-cachyos-primary-linux-target.md)
- [ADR-032: VSCode Platform-Specific Tasks](../02_adrs/ADR-032-vscode-platform-specific-tasks.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
