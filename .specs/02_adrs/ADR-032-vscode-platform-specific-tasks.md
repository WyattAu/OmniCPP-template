# ADR-032: VSCode Platform-Specific Tasks

**Status:** Accepted
**Date:** 2026-01-27
**Context:** VSCode Integration Enhancement

---

## Context

The OmniCPP Template project uses VSCode as the primary IDE. The current VSCode configuration ([`.vscode/tasks.json`](../../.vscode/tasks.json:1) and [`.vscode/launch.json`](../../.vscode/launch.json:1)) is primarily Windows-centric, with tasks and launch configurations optimized for MSVC, MSVC-clang, MinGW-GCC, and MinGW-Clang.

### Current State

1. **Windows-First Design:** All tasks and launch configurations are Windows-specific
2. **MSVC Integration:** Tasks for MSVC Developer Command Prompt
3. **MinGW Integration:** Tasks for MinGW via MSYS2
4. **No Linux Tasks:** No Linux-specific tasks or launch configurations
5. **No Nix Integration:** No Nix-aware tasks
6. **No CachyOS Tasks:** No CachyOS-specific configurations
7. **Single Platform:** Assumes Windows environment

### Linux Expansion Requirements

The Linux expansion requires VSCode to support:

1. **Linux Build Tasks:** Tasks for building with GCC and Clang on Linux
2. **Linux Debug Configurations:** Launch configurations for debugging on Linux
3. **Nix Integration:** Tasks that work with Nix environment
4. **CachyOS Optimizations:** CachyOS-specific compiler flags
5. **Multiple Toolchains:** GCC and Clang variants
6. **Platform Detection:** Tasks that detect platform and adapt
7. **Consistent Interface:** Same task names across platforms

### VSCode Challenges

1. **Platform-Specific Tasks:** Different tasks for Windows and Linux
2. **Task Complexity:** More tasks increase complexity
3. **Maintenance Burden:** More tasks to maintain
4. **User Experience:** Too many tasks can be confusing
5. **Platform Detection:** VSCode tasks don't have built-in platform detection
6. **Environment Variables:** Need to handle different environment variables
7. **Path Separators:** Windows uses `\`, Linux uses `/`

## Decision

Add Linux-specific tasks and launch configurations to VSCode while maintaining Windows support.

### 1. Platform-Specific Task Organization

Organize tasks by platform:

```json
{
  "version": "2.0.0",
  "tasks": [
    // Windows Tasks
    {
      "label": "Configure Build (Windows MSVC - Debug)",
      "type": "shell",
      "command": "cmd",
      "args": ["/c", "python", "OmniCppController.py", "configure", "--compiler", "msvc", "--build-type", "Debug"],
      "group": "build",
      "presentation": {"reveal": "always"}
    },

    // Linux Tasks
    {
      "label": "Configure Build (Linux GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "configure", "--compiler", "gcc", "--build-type", "Debug"],
      "group": "build",
      "presentation": {"reveal": "always"}
    },

    // Nix Tasks
    {
      "label": "Configure Build (Nix GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "configure", "--compiler", "gcc", "--build-type", "Debug", "--use-nix"],
      "group": "build",
      "presentation": {"reveal": "always"}
    }
  ]
}
```

### 2. Linux Build Tasks

Create comprehensive Linux build tasks:

```json
// GCC Tasks
{
  "label": "Configure Build (Linux GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "configure", "--compiler", "gcc", "--build-type", "Debug"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": [],
  "group": {"kind": "build", "isDefault": false},
  "detail": "Configure CMake project with GCC compiler for Debug build"
},

{
  "label": "Build Engine (Linux GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "gcc-debug", "debug", "--compiler", "gcc"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": "$gcc",
  "group": {"kind": "build", "isDefault": true},
  "detail": "Build engine with GCC compiler in Debug configuration"
},

// Clang Tasks
{
  "label": "Configure Build (Linux Clang - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "configure", "--compiler", "clang", "--build-type", "Debug"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": [],
  "group": {"kind": "build", "isDefault": false},
  "detail": "Configure CMake project with Clang compiler for Debug build"
},

{
  "label": "Build Engine (Linux Clang - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "clang-debug", "debug", "--compiler", "clang"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": "$gcc",
  "group": {"kind": "build", "isDefault": false},
  "detail": "Build engine with Clang compiler in Debug configuration"
}
```

### 3. Nix-Aware Tasks

Create Nix-specific tasks:

```json
{
  "label": "Configure Build (Nix GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "configure", "--compiler", "gcc", "--build-type", "Debug", "--use-nix"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": [],
  "group": {"kind": "build", "isDefault": false},
  "detail": "Configure CMake project with Nix GCC compiler for Debug build"
},

{
  "label": "Build Engine (Nix GCC - Debug)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "nix-gcc-debug", "debug", "--compiler", "gcc", "--use-nix"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": "$gcc",
  "group": {"kind": "build", "isDefault": false},
  "detail": "Build engine with Nix GCC compiler in Debug configuration"
}
```

### 4. CachyOS-Optimized Tasks

Create CachyOS-specific tasks:

```json
{
  "label": "Configure Build (CachyOS GCC - Release)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "configure", "--compiler", "gcc", "--build-type", "Release", "--cachyos"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": [],
  "group": {"kind": "build", "isDefault": false},
  "detail": "Configure CMake project with CachyOS GCC compiler for Release build with optimizations"
},

{
  "label": "Build Engine (CachyOS GCC - Release)",
  "type": "shell",
  "command": "python",
  "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "cachyos-gcc-release", "release", "--compiler", "gcc", "--cachyos"],
  "options": {"cwd": "${workspaceFolder}"},
  "problemMatcher": "$gcc",
  "group": {"kind": "build", "isDefault": false},
  "detail": "Build engine with CachyOS GCC compiler in Release configuration with performance optimizations"
}
```

### 5. Linux Debug Configurations

Create Linux-specific launch configurations:

```json
{
  "version": "0.2.0",
  "configurations": [
    // GDB Debug Configuration
    {
      "name": "Debug Engine (GDB)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/gcc-debug/engine/omnicpp_engine",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "preLaunchTask": "Build Engine (Linux GCC - Debug)"
    },

    // LLDB Debug Configuration
    {
      "name": "Debug Engine (LLDB)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/clang-debug/engine/omnicpp_engine",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "lldb",
      "preLaunchTask": "Build Engine (Linux Clang - Debug)"
    }
  ]
}
```

### 6. Task Groups

Organize tasks into logical groups:

```json
{
  "tasks": [
    // Configure Tasks
    {
      "label": "Configure Build (Linux GCC - Debug)",
      "group": {"kind": "configure", "isDefault": false}
    },

    // Build Tasks
    {
      "label": "Build Engine (Linux GCC - Debug)",
      "group": {"kind": "build", "isDefault": true}
    },

    // Test Tasks
    {
      "label": "Run Tests (Linux GCC)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "test"],
      "group": {"kind": "test", "isDefault": true}
    },

    // Clean Tasks
    {
      "label": "Clean Build (Linux)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "clean"],
      "group": {"kind": "none", "isDefault": false}
    }
  ]
}
```

### 7. Platform Detection

Use VSCode's platform detection:

```json
{
  "tasks": [
    {
      "label": "Configure Build (Default)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "configure"],
      "windows": {
        "args": ["OmniCppController.py", "configure", "--compiler", "msvc"]
      },
      "linux": {
        "args": ["OmniCppController.py", "configure", "--compiler", "gcc"]
      },
      "group": {"kind": "configure", "isDefault": true}
    }
  ]
}
```

### 8. Environment Variables

Set platform-specific environment variables:

```json
{
  "tasks": [
    {
      "label": "Build Engine (Linux GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "gcc-debug", "debug"],
      "options": {
        "cwd": "${workspaceFolder}",
        "env": {
          "CMAKE_GENERATOR": "Ninja",
          "CMAKE_BUILD_PARALLEL_LEVEL": "${command:extension.advanced.example.value}"
        }
      }
    }
  ]
}
```

### 9. Task Documentation

Add task documentation:

```json
{
  "tasks": [
    {
      "label": "Build Engine (Linux GCC - Debug)",
      "type": "shell",
      "command": "python",
      "args": ["OmniCppController.py", "build", "engine", "Clean Build Pipeline", "gcc-debug", "debug"],
      "detail": "Build engine with GCC compiler in Debug configuration",
      "presentation": {
        "reveal": "always",
        "panel": "new",
        "showReuseMessage": true,
        "clear": false
      }
    }
  ]
}
```

## Consequences

### Positive

1. **Complete Linux Support:** Full VSCode support for Linux development
2. **Nix Integration:** Tasks work with Nix environment
3. **CachyOS Optimizations:** CachyOS-specific tasks
4. **Multiple Toolchains:** Support for GCC and Clang
5. **Consistent Interface:** Same task names across platforms
6. **Better Debugging:** Linux-specific debug configurations
7. **Improved Productivity:** Quick access to common tasks
8. **Platform Detection:** Automatic platform adaptation
9. **Documentation:** Clear task descriptions
10. **User Experience:** Seamless development experience

### Negative

1. **Increased Complexity:** More tasks and configurations
2. **Maintenance Burden:** More tasks to maintain
3. **User Confusion:** Too many tasks can be overwhelming
4. **Configuration Size:** Larger VSCode configuration files
5. **Testing Burden:** Need to test all tasks
6. **Documentation Burden:** Need to document all tasks
7. **Task Duplication:** Similar tasks for different platforms
8. **IDE Limitations:** VSCode task limitations

### Neutral

1. **Task Organization:** Need to organize tasks logically
2. **Task Naming:** Need consistent naming convention
3. **Task Groups:** Need to group tasks appropriately
4. **Task Documentation:** Need to document task usage

## Alternatives Considered

### Alternative 1: Single Platform Tasks

**Description:** Use same tasks for all platforms, rely on OmniCppController.py to detect platform

**Pros:**
- Fewer tasks
- Simpler configuration
- Less maintenance

**Cons:**
- No platform-specific optimizations
- Confusing task names
- Harder to debug platform-specific issues
- Less clear what platform is being used

**Rejected:** No platform-specific optimizations, confusing

### Alternative 2: Separate VSCode Configurations

**Description:** Create separate `.vscode-windows/` and `.vscode-linux/` directories

**Pros:**
- Clear separation
- Platform-specific configurations
- No conflicts

**Cons:**
- Need to switch configurations manually
- Confusing for users
- Not standard VSCode practice
- Harder to maintain
- Git conflicts

**Rejected:** Not standard practice, confusing for users

### Alternative 3: Dynamic Task Generation

**Description:** Use VSCode extension to generate tasks dynamically

**Pros:**
- Fewer tasks in configuration
- Dynamic task generation
- Can adapt to environment

**Cons:**
- Requires custom extension
- Complex to implement
- Less transparent
- Harder to debug
- Not standard VSCode practice

**Rejected:** Too complex, not standard practice

### Alternative 4: Minimal Linux Support

**Description:** Add only basic Linux tasks, keep Windows as primary

**Pros:**
- Fewer tasks
- Less complexity
- Faster implementation

**Cons:**
- Poor Linux experience
- No Nix integration
- No CachyOS optimizations
- Linux users frustrated

**Rejected:** Poor Linux experience, not aligned with goals

## Related ADRs

- [ADR-026: VSCode tasks and launch configuration](ADR-026-vscode-tasks-launch-configuration.md)
- [ADR-027: Nix Package Manager Integration](ADR-027-nix-package-manager-integration.md)
- [ADR-028: CachyOS as Primary Linux Target](ADR-028-cachyos-primary-linux-target.md)
- [ADR-030: Enhanced OmniCppController.py Architecture](ADR-030-enhanced-omnicppcontroller-architecture.md)

## Threat Model References

- **TM-LX-005: VSCode Configuration Security** - See [`.specs/03_threat_model/analysis.md`](../03_threat_model/analysis.md)
  - Task injection attacks
  - Environment variable leakage
  - Path traversal in tasks
  - Mitigation: Validate task configurations, use secure defaults, avoid exposing sensitive data

## References

- [VSCode Tasks Documentation](https://code.visualstudio.com/docs/editor/tasks)
- [VSCode Debugging Documentation](https://code.visualstudio.com/docs/cpp/cpp-debug)
- [VSCode Multi-Root Workspaces](https://code.visualstudio.com/docs/editor/multi-root-workspaces)
- [Linux Expansion Manifest](../04_future_state/linux_expansion_manifest.md)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-27 | System Architect | Initial version |
