# ADR-026: VSCode tasks.json and launch.json Configuration

**Status:** Accepted
**Date:** 2026-01-07
**Context:** VSCode Integration

---

## Context

The OmniCPP Template project requires comprehensive VSCode integration for a seamless development experience. VSCode tasks and launch configurations are critical for building, debugging, and testing the project. The future state (`.specs/04_future_state/manifest.md`) specifies the need for VSCode integration.

### Current State

VSCode integration is incomplete:
- **No Tasks:** No VSCode tasks configuration
- **No Launch:** No VSCode launch configuration
- **No Debugging:** No debugging configuration
- **No Testing:** No testing integration
- **No Extensions:** No recommended extensions

### Issues

1. **No Tasks:** No VSCode tasks configuration
2. **No Launch:** No VSCode launch configuration
3. **No Debugging:** No debugging configuration
4. **No Testing:** No testing integration
5. **No Extensions:** No recommended extensions
6. **Poor DX:** Poor developer experience

## Decision

Implement **VSCode tasks.json and launch.json configuration** with:
1. **Tasks Configuration:** Comprehensive tasks for build, clean, test, etc.
2. **Launch Configuration:** Debugging configurations for C++ and Python
3. **Testing Integration:** Test integration with VSCode
4. **Recommended Extensions:** Recommended extensions for C++ and Python
5. **Settings:** VSCode settings for the project
6. **Problem Matchers:** Problem matchers for error detection
7. **Keybindings:** Custom keybindings for common tasks

### 1. tasks.json Configuration

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build (Default)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": [
        "$gcc",
        "$msCompile"
      ],
      "detail": "Build project with default preset"
    },
    {
      "label": "Build (Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build",
        "--preset",
        "debug"
      ],
      "group": "build",
      "problemMatcher": [
        "$gcc",
        "$msCompile"
      ],
      "detail": "Build project with debug preset"
    },
    {
      "label": "Build (Release)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build",
        "--preset",
        "release"
      ],
      "group": "build",
      "problemMatcher": [
        "$gcc",
        "$msCompile"
      ],
      "detail": "Build project with release preset"
    },
    {
      "label": "Build (Coverage)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "build",
        "--preset",
        "coverage"
      ],
      "group": "build",
      "problemMatcher": [
        "$gcc",
        "$msCompile"
      ],
      "detail": "Build project with coverage preset"
    },
    {
      "label": "Clean",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "clean"
      ],
      "problemMatcher": [],
      "detail": "Clean build artifacts"
    },
    {
      "label": "Clean All",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "clean",
        "--all"
      ],
      "problemMatcher": [],
      "detail": "Clean all artifacts including dependencies"
    },
    {
      "label": "Configure",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "configure"
      ],
      "problemMatcher": [],
      "detail": "Configure project"
    },
    {
      "label": "Configure (Debug)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "configure",
        "--preset",
        "debug"
      ],
      "problemMatcher": [],
      "detail": "Configure project with debug preset"
    },
    {
      "label": "Configure (Release)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "configure",
        "--preset",
        "release"
      ],
      "problemMatcher": [],
      "detail": "Configure project with release preset"
    },
    {
      "label": "Format",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "format",
        "--fix"
      ],
      "problemMatcher": [],
      "detail": "Format code"
    },
    {
      "label": "Format Check",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "format",
        "--check"
      ],
      "problemMatcher": [],
      "detail": "Check code formatting"
    },
    {
      "label": "Lint",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "lint"
      ],
      "problemMatcher": [
        "$eslint-stylish",
        "$pylint"
      ],
      "detail": "Lint code"
    },
    {
      "label": "Lint Fix",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "lint",
        "--fix"
      ],
      "problemMatcher": [
        "$eslint-stylish",
        "$pylint"
      ],
      "detail": "Lint and fix code"
    },
    {
      "label": "Install Dependencies",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "install"
      ],
      "problemMatcher": [],
      "detail": "Install dependencies"
    },
    {
      "label": "Update Dependencies",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "install",
        "--update"
      ],
      "problemMatcher": [],
      "detail": "Update dependencies"
    },
    {
      "label": "Package",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "package"
      ],
      "problemMatcher": [],
      "detail": "Package project"
    },
    {
      "label": "Test",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "test"
      ],
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "problemMatcher": [],
      "detail": "Run tests"
    },
    {
      "label": "Test (Coverage)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "test",
        "--coverage"
      ],
      "group": "test",
      "problemMatcher": [],
      "detail": "Run tests with coverage"
    },
    {
      "label": "Test (Verbose)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "test",
        "--verbose"
      ],
      "group": "test",
      "problemMatcher": [],
      "detail": "Run tests with verbose output"
    },
    {
      "label": "Validate",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "validate"
      ],
      "problemMatcher": [],
      "detail": "Validate configuration"
    },
    {
      "label": "Validate (Strict)",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/OmniCppController.py",
        "validate",
        "--strict"
      ],
      "problemMatcher": [],
      "detail": "Validate configuration with strict mode"
    }
  ]
}
```

### 2. launch.json Configuration

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "C++ Debug (Default)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/bin/OmniCppEngine",
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
        }
      ],
      "preLaunchTask": "Build (Debug)",
      "problemMatcher": [
        "$gcc"
      ]
    },
    {
      "name": "C++ Debug (Release)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/bin/OmniCppEngine",
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
        }
      ],
      "preLaunchTask": "Build (Release)",
      "problemMatcher": [
        "$gcc"
      ]
    },
    {
      "name": "C++ Debug (MSVC)",
      "type": "cppvsdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/bin/OmniCppEngine.exe",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "console": "externalTerminal",
      "preLaunchTask": "Build (Debug)",
      "problemMatcher": [
        "$msCompile"
      ]
    },
    {
      "name": "Python Debug (OmniCppController)",
      "type": "debugpy",
      "request": "launch",
      "module": "OmniCppController",
      "args": [
        "build"
      ],
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}",
      "problemMatcher": []
    },
    {
      "name": "Python Debug (Tests)",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "--no-cov"
      ],
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}",
      "problemMatcher": []
    },
    {
      "name": "Python Debug (Current File)",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}",
      "problemMatcher": []
    },
    {
      "name": "Attach to C++ Process",
      "type": "cppdbg",
      "request": "attach",
      "program": "${workspaceFolder}/build/bin/OmniCppEngine",
      "processId": "${command:pickProcess}",
      "MIMode": "gdb",
      "miDebuggerPath": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "problemMatcher": [
        "$gcc"
      ]
    },
    {
      "name": "Attach to Python Process",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      },
      "problemMatcher": []
    }
  ]
}
```

### 3. settings.json Configuration

```json
{
  "files.associations": {
    "*.cmake": "cmake",
    "CMakeLists.txt": "cmake",
    "*.h": "cpp",
    "*.hpp": "cpp",
    "*.cpp": "cpp",
    "*.cc": "cpp",
    "*.cxx": "cpp"
  },
  "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",
  "C_Cpp.default.intelliSenseMode": "linux-gcc-x64",
  "C_Cpp.default.compilerPath": "/usr/bin/gcc",
  "C_Cpp.default.includePath": [
    "${workspaceFolder}/include",
    "${workspaceFolder}/build/include"
  ],
  "C_Cpp.default.defines": [],
  "C_Cpp.errorSquiggles": "enabled",
  "C_Cpp.autocomplete": "default",
  "C_Cpp.formatting": "clangFormat",
  "C_Cpp.clang_format_style": "file",
  "C_Cpp.clang_format_fallbackStyle": "llvm",
  "C_Cpp.clang_format_sortIncludes": true,
  "C_Cpp.inlayHints.autoDeclarationTypes.enabled": true,
  "C_Cpp.inlayHints.parameterNames.enabled": true,
  "C_Cpp.inlayHints.referenceOperator.enabled": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.autoSearchPaths": true,
  "python.analysis.extraPaths": [
    "${workspaceFolder}/omni_scripts"
  ],
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": [
    "--line-length=100"
  ],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.pylintArgs": [
    "--rcfile=${workspaceFolder}/.pylintrc"
  ],
  "python.linting.mypyEnabled": true,
  "python.linting.mypyArgs": [
    "--strict",
    "--ignore-missing-imports"
  ],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests/"
  ],
  "python.testing.unittestEnabled": false,
  "cmake.configureOnOpen": true,
  "cmake.buildDirectory": "${workspaceFolder}/build",
  "cmake.sourceDirectory": "${workspaceFolder}",
  "cmake.generator": "Ninja",
  "cmake.defaultVariants": {
    "buildType": [
      {
        "short": "Debug",
        "long": "Debug",
        "buildType": "Debug"
      },
      {
        "short": "Release",
        "long": "Release",
        "buildType": "Release"
      }
    ]
  },
  "cmake.configureArgs": [
    "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
  ],
  "cmake.buildArgs": [
    "-j$(nproc)"
  ],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "editor.rulers": [
    100
  ],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.trimAutoWhitespace": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/.hg": true,
    "**/CVS": true,
    "**/.DS_Store": true,
    "**/Thumbs.db": true,
    "**/build": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true,
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/coverage_html": true,
    "**/.coverage": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/bower_components": true,
    "**/build": true,
    "**/dist": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true,
    "**/__pycache__": true,
    "**/coverage_html": true
  },
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/build/**": true,
    "**/node_modules/**": true,
    "**/.pytest_cache/**": true,
    "**/.mypy_cache/**": true,
    "**/__pycache__/**": true
  }
}
```

### 4. extensions.json Configuration

```json
{
  "recommendations": [
    "ms-vscode.cpptools",
    "ms-vscode.cmake-tools",
    "twxs.cmake",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-python.pylint",
    "ms-python.mypy",
    "ms-python.isort",
    "ms-vscode.test-adapter-converter",
    "hbenl.vscode-test-explorer",
    "streetsidesoftware.code-spell-checker",
    "eamodio.gitlens",
    "vscodevim.vim",
    "formulahendry.code-runner",
    "usernamehw.errorlens",
    "wakatime.vscode-wakatime",
    "ms-vscode-remote.remote-containers",
    "ms-vscode-remote.remote-ssh",
    "ms-vscode-remote.remote-wsl"
  ]
}
```

### 5. keybindings.json Configuration

```json
[
  {
    "key": "ctrl+shift+b",
    "command": "workbench.action.tasks.build"
  },
  {
    "key": "ctrl+shift+t",
    "command": "workbench.action.tasks.test"
  },
  {
    "key": "ctrl+shift+f",
    "command": "workbench.action.tasks.runTask",
    "args": "Format"
  },
  {
    "key": "ctrl+shift+l",
    "command": "workbench.action.tasks.runTask",
    "args": "Lint"
  },
  {
    "key": "ctrl+shift+c",
    "command": "workbench.action.tasks.runTask",
    "args": "Clean"
  },
  {
    "key": "f5",
    "command": "workbench.action.debug.start",
    "when": "!inDebugMode"
  },
  {
    "key": "f5",
    "command": "workbench.action.debug.continue",
    "when": "inDebugMode"
  },
  {
    "key": "f9",
    "command": "editor.debug.action.toggleBreakpoint",
    "when": "editorTextFocus"
  },
  {
    "key": "f10",
    "command": "workbench.action.debug.stepOver",
    "when": "inDebugMode"
  },
  {
    "key": "f11",
    "command": "workbench.action.debug.stepInto",
    "when": "inDebugMode"
  },
  {
    "key": "shift+f11",
    "command": "workbench.action.debug.stepOut",
    "when": "inDebugMode"
  },
  {
    "key": "shift+f5",
    "command": "workbench.action.debug.stop",
    "when": "inDebugMode"
  }
]
```

### 6. Usage Examples

```bash
# Build project
# Press Ctrl+Shift+B or run "Build (Default)" task

# Run tests
# Press Ctrl+Shift+T or run "Test" task

# Format code
# Press Ctrl+Shift+F or run "Format" task

# Lint code
# Press Ctrl+Shift+L or run "Lint" task

# Clean build artifacts
# Press Ctrl+Shift+C or run "Clean" task

# Debug C++ code
# Press F5 or select "C++ Debug (Default)" configuration

# Debug Python code
# Select "Python Debug (OmniCppController)" configuration
```

## Consequences

### Positive

1. **Integration:** Comprehensive VSCode integration
2. **Tasks:** Comprehensive tasks for all operations
3. **Debugging:** Debugging configurations for C++ and Python
4. **Testing:** Testing integration with VSCode
5. **Extensions:** Recommended extensions
6. **Settings:** VSCode settings for the project
7. **DX:** Improved developer experience

### Negative

1. **Complexity:** More complex than no configuration
2. **Maintenance:** Configuration needs to be maintained
3. **Platform:** Platform-specific configurations
4. **Learning:** Learning curve for VSCode features

### Neutral

1. **Documentation:** Requires documentation for VSCode integration
2. **Training:** Need to train developers on VSCode features

## Alternatives Considered

### Alternative 1: No VSCode Integration

**Description:** No VSCode integration

**Pros:**
- Simpler implementation
- No maintenance

**Cons:**
- Poor developer experience
- No debugging
- No testing integration

**Rejected:** Poor developer experience and no debugging

### Alternative 2: Minimal VSCode Integration

**Description:** Minimal VSCode integration

**Pros:**
- Simpler implementation
- Less maintenance

**Cons:**
- Limited functionality
- Poor developer experience
- No debugging

**Rejected:** Limited functionality and poor developer experience

### Alternative 3: External Tools

**Description:** Use external tools for VSCode integration

**Pros:**
- No custom configuration
- Proven solutions

**Cons:**
- External dependencies
- Less control
- Platform-specific

**Rejected:** External dependencies and less control

## Related ADRs

- [ADR-025: OmniCppController.py as single entry point](ADR-025-omnicppcontroller-single-entry-point.md)

## References

- [VSCode Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [VSCode Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [VSCode Settings](https://code.visualstudio.com/docs/getstarted/settings)
- [VSCode Extensions](https://code.visualstudio.com/docs/editor/extension-marketplace)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|---------|---------|
| 1.0 | 2026-01-07 | System Architect | Initial version |
