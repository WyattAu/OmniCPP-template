# Test: build
# Compiler: mingw-gcc
# Command: python OmniCppController.py build engine Clean Build Pipeline default release --compiler mingw-gcc
# Timestamp: 2026-01-19T02:10:22.977689
# Exit Code: 1

## STDOUT
2026-01-19 02:10:19 - omni_scripts.platform.detector - [32m[1mINFO[0m - Detected platform: Windows x86_64 (64-bit)
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Initializing OmniCpp Controller on Windows x86_64
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Detecting available compiler...
2026-01-19 02:10:19 - omni_scripts.platform.windows - [32m[1mINFO[0m - Found MSVC 19.44 (BuildTools 2022) at C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Detected compiler: MSVC 19.44
2026-01-19 02:10:19 - omni_scripts.compilers.detector - [32m[1mINFO[0m - MSVC 19.44 supports C++23
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Compiler supports C++23: True
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Building target: engine
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Pipeline: Clean Build Pipeline
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Preset: default
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Config: release
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Compiler: mingw-gcc
2026-01-19 02:10:19 - __main__ - [32m[1mINFO[0m - Setting up terminal environment for mingw-gcc
[INFO] 2026-01-19T02:10:19.998062 - Added user local bin to MSYS2 PATH: /c/Users/mushroomyy/.local/bin
[INFO] 2026-01-19T02:10:19.998142 - Using MSYS2 UCRT64: C:\msys64
[INFO] 2026-01-19T02:10:19.998223 - Setting MSYS2 PATH: /c/Users/mushroomyy/.local/bin:/ucrt64/bin:/usr/bin:/usr/local/bin
[INFO] 2026-01-19T02:10:19.998233 - Executing in msys2 environment: "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-gcc\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:19.998240 - Capture output: enabled
[INFO] 2026-01-19T02:10:19.998396 - MSYS2 bash.exe: C:\msys64\usr\bin\bash.exe
[INFO] 2026-01-19T02:10:19.998405 - Command to execute: "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-gcc\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:19.998413 - Command type: <class 'str'>
[INFO] 2026-01-19T02:10:19.998417 - Command length: 404
[INFO] 2026-01-19T02:10:20.039786 - Full command to execute: cd "/e/syncfold/Filen_private/dev/template/OmniCPP-template" && "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-gcc\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:20.039811 - Full command length: 468
[INFO] 2026-01-19T02:10:22.663414 - Starting Clean Build Pipeline for engine
[INFO] 2026-01-19T02:10:22.663414 - Build context: product=engine, task=Clean Build Pipeline, arch=x64, build_type=release, compiler=mingw-gcc, lib_flag=True, st_flag=False
[INFO] 2026-01-19T02:10:22.663414 - Step 1: Cleaning build directories
[INFO] 2026-01-19T02:10:22.663414 - Cleaning build directories for engine
[INFO] 2026-01-19T02:10:22.663414 - lib_flag: True, st_flag: False
[INFO] 2026-01-19T02:10:22.663414 - Targets to clean: ['engine']
[INFO] 2026-01-19T02:10:22.663414 - Build directory for engine: E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-gcc/engine
[SUCCESS] 2026-01-19T02:10:22.664411 - Build directories cleaned successfully (0 directories)
[INFO] 2026-01-19T02:10:22.664411 - Step 2: Installing dependencies
[INFO] 2026-01-19T02:10:22.830457 - Added user local bin to MSYS2 PATH: /c/Users/mushroomyy/.local/bin
[INFO] 2026-01-19T02:10:22.830457 - Using MSYS2 UCRT64: C:/msys64
[INFO] 2026-01-19T02:10:22.830457 - Installing dependencies for engine
[INFO] 2026-01-19T02:10:22.830457 - Installing dependencies for engine in E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-gcc/engine
[INFO] 2026-01-19T02:10:22.830457 - Installing Conan dependencies for release build

[INFO] 2026-01-19T02:10:22.939197 - MSYS2 execution completed with return code: 1


## STDERR
[ERROR] 2026-01-19T02:10:22.831466 - Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release
Traceback (most recent call last):
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 311, in install_dependencies
    self.conan_manager.install(
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/conan.py", line 166, in install
    raise ConanProfileError(
omni_scripts.conan.ConanProfileError: Conan profile not found: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-gcc-release

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 545, in run_clean_build_pipeline
    self.install_dependencies(context, terminal_env)
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 330, in install_dependencies
    raise DependencyError(
omni_scripts.build.DependencyError: BuildError: Failed to install dependencies for engine Context: {'dependency': 'engine'}

