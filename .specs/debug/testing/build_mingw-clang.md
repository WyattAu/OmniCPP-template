# Test: build
# Compiler: mingw-clang
# Command: python OmniCppController.py build engine Clean Build Pipeline default release --compiler mingw-clang
# Timestamp: 2026-01-19T02:10:31.090601
# Exit Code: 1

## STDOUT
2026-01-19 02:10:23 - omni_scripts.platform.detector - [32m[1mINFO[0m - Detected platform: Windows x86_64 (64-bit)
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Initializing OmniCpp Controller on Windows x86_64
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Detecting available compiler...
2026-01-19 02:10:23 - omni_scripts.platform.windows - [32m[1mINFO[0m - Found MSVC 19.44 (BuildTools 2022) at C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Detected compiler: MSVC 19.44
2026-01-19 02:10:23 - omni_scripts.compilers.detector - [32m[1mINFO[0m - MSVC 19.44 supports C++23
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Compiler supports C++23: True
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Building target: engine
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Pipeline: Clean Build Pipeline
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Preset: default
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Config: release
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Compiler: mingw-clang
2026-01-19 02:10:23 - __main__ - [32m[1mINFO[0m - Setting up terminal environment for mingw-clang
[INFO] 2026-01-19T02:10:24.117982 - Added user local bin to MSYS2 PATH: /c/Users/mushroomyy/.local/bin
[INFO] 2026-01-19T02:10:24.118061 - Using MSYS2 UCRT64: C:\msys64
[INFO] 2026-01-19T02:10:24.118144 - Setting MSYS2 PATH: /c/Users/mushroomyy/.local/bin:/ucrt64/bin:/usr/bin:/usr/local/bin
[INFO] 2026-01-19T02:10:24.118154 - Executing in msys2 environment: "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-clang\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:24.118161 - Capture output: enabled
[INFO] 2026-01-19T02:10:24.118315 - MSYS2 bash.exe: C:\msys64\usr\bin\bash.exe
[INFO] 2026-01-19T02:10:24.118322 - Command to execute: "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-clang\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:24.118330 - Command type: <class 'str'>
[INFO] 2026-01-19T02:10:24.118335 - Command length: 406
[INFO] 2026-01-19T02:10:24.230266 - Full command to execute: cd "/e/syncfold/Filen_private/dev/template/OmniCPP-template" && "python" -c "from omni_scripts.build import BuildManager, BuildContext; from pathlib import Path; bm = BuildManager(Path.cwd()); ctx = BuildContext(product=\"engine\", task=\"Clean Build Pipeline\", arch=\"x64\", build_type=\"release\", compiler=\"mingw-clang\", is_cross_compilation=False, lib_flag=True, st_flag=False, qt_vulkan_lib_flag=False, qt_vulkan_st_flag=False); bm.run_clean_build_pipeline(ctx)"
[INFO] 2026-01-19T02:10:24.230293 - Full command length: 470
[INFO] 2026-01-19T02:10:28.785603 - Starting Clean Build Pipeline for engine
[INFO] 2026-01-19T02:10:28.785603 - Build context: product=engine, task=Clean Build Pipeline, arch=x64, build_type=release, compiler=mingw-clang, lib_flag=True, st_flag=False
[INFO] 2026-01-19T02:10:28.785603 - Step 1: Cleaning build directories
[INFO] 2026-01-19T02:10:28.785603 - Cleaning build directories for engine
[INFO] 2026-01-19T02:10:28.785603 - lib_flag: True, st_flag: False
[INFO] 2026-01-19T02:10:28.785603 - Targets to clean: ['engine']
[INFO] 2026-01-19T02:10:28.785603 - Build directory for engine: E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine
[SUCCESS] 2026-01-19T02:10:28.785603 - Build directories cleaned successfully (0 directories)
[INFO] 2026-01-19T02:10:28.785603 - Step 2: Installing dependencies
[INFO] 2026-01-19T02:10:29.235254 - Added user local bin to MSYS2 PATH: /c/Users/mushroomyy/.local/bin
[INFO] 2026-01-19T02:10:29.235254 - Using MSYS2 UCRT64: C:/msys64
[INFO] 2026-01-19T02:10:29.235254 - Installing dependencies for engine
[INFO] 2026-01-19T02:10:29.235254 - Installing dependencies for engine in E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine
[INFO] 2026-01-19T02:10:29.235254 - Installing Conan dependencies for release build
[INFO] 2026-01-19T02:10:29.244766 - Using conanfile: E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/conanfile.py
[INFO] 2026-01-19T02:10:29.244766 - Setting MSYS2 PATH: /c/Users/mushroomyy/.local/bin:/ucrt64/bin:/usr/bin:/usr/local/bin
[INFO] 2026-01-19T02:10:29.244766 - Executing in msys2 environment: conan install E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/conanfile.py --output-folder E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine --build=missing --profile:host E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --profile:build E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --settings build_type=Release
[INFO] 2026-01-19T02:10:29.244766 - Capture output: enabled
[INFO] 2026-01-19T02:10:29.244766 - MSYS2 bash.exe: C:/msys64/usr/bin/bash.exe
[INFO] 2026-01-19T02:10:29.244766 - Command to execute: conan install E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/conanfile.py --output-folder E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine --build=missing --profile:host E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --profile:build E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --settings build_type=Release
[INFO] 2026-01-19T02:10:29.244766 - Command type: <class 'str'>
[INFO] 2026-01-19T02:10:29.244766 - Command length: 452
[INFO] 2026-01-19T02:10:29.317662 - Full command to execute: cd "/e/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine" && conan install E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/conanfile.py --output-folder E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine --build=missing --profile:host E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --profile:build E:/syncfold/Filen_private/dev/template/OmniCPP-template/conan/profiles/mingw-clang-release --settings build_type=Release
[INFO] 2026-01-19T02:10:29.317662 - Full command length: 549
[INFO] 2026-01-19T02:10:30.243587 - MSYS2 execution completed with return code: 1
[INFO] 2026-01-19T02:10:30.754619 - Validating Conan installation in: E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine
[INFO] 2026-01-19T02:10:30.754619 - Build directory exists: False

[INFO] 2026-01-19T02:10:30.900178 - MSYS2 execution completed with return code: 1


## STDERR
/usr/bin/bash: line 1: cd: /e/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine: No such file or directory

[ERROR] 2026-01-19T02:10:30.754619 - Build directory does not exist: E:/syncfold/Filen_private/dev/template/OmniCPP-template/build/release/mingw-clang/engine
Traceback (most recent call last):
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 311, in install_dependencies
    self.conan_manager.install(
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/conan.py", line 247, in install
    raise ConanInstallError(
omni_scripts.conan.ConanInstallError: Failed to install Conan dependencies: validation failed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 545, in run_clean_build_pipeline
    self.install_dependencies(context, terminal_env)
  File "E:/syncfold/Filen_private/dev/template/OmniCPP-template/omni_scripts/build.py", line 330, in install_dependencies
    raise DependencyError(
omni_scripts.build.DependencyError: BuildError: Failed to install dependencies for engine Context: {'dependency': 'engine'}

