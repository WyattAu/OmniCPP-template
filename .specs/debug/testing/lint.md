# Test: lint
# Command: python OmniCppController.py lint
# Timestamp: 2026-01-19T02:08:22.387812
# Exit Code: 1

## STDOUT
2026-01-19 02:08:18 - omni_scripts.platform.detector - [32m[1mINFO[0m - Detected platform: Windows x86_64 (64-bit)
2026-01-19 02:08:18 - __main__ - [32m[1mINFO[0m - Initializing OmniCpp Controller on Windows x86_64
2026-01-19 02:08:18 - __main__ - [32m[1mINFO[0m - Detecting available compiler...
2026-01-19 02:08:18 - omni_scripts.platform.windows - [32m[1mINFO[0m - Found MSVC 19.44 (BuildTools 2022) at C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
2026-01-19 02:08:18 - __main__ - [32m[1mINFO[0m - Detected compiler: MSVC 19.44
2026-01-19 02:08:18 - omni_scripts.compilers.detector - [32m[1mINFO[0m - MSVC 19.44 supports C++23
2026-01-19 02:08:18 - __main__ - [32m[1mINFO[0m - Compiler supports C++23: True
2026-01-19 02:08:18 - __main__ - [32m[1mINFO[0m - Starting static analysis...
2026-01-19 02:08:21 - __main__ - [32m[1mINFO[0m - Linting 3898 C++ file(s)...
2026-01-19 02:08:22 - __main__ - [33m[1mWARNING[0m - clang-tidy not found, skipping C++ linting
2026-01-19 02:08:22 - __main__ - [32m[1mINFO[0m - Linting 2442 Python file(s)...
2026-01-19 02:08:22 - omni_scripts.logging.logger - [31m[1mERROR[0m - Lint error: pylint executable not found


## STDERR
