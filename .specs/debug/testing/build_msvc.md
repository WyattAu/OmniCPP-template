# Test: build
# Compiler: msvc
# Command: python OmniCppController.py build engine Clean Build Pipeline default release --compiler msvc
# Timestamp: 2026-01-19T02:09:02.834037
# Exit Code: 1

## STDOUT
2026-01-19 02:08:23 - omni_scripts.platform.detector - [32m[1mINFO[0m - Detected platform: Windows x86_64 (64-bit)
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Initializing OmniCpp Controller on Windows x86_64
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Detecting available compiler...
2026-01-19 02:08:23 - omni_scripts.platform.windows - [32m[1mINFO[0m - Found MSVC 19.44 (BuildTools 2022) at C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Detected compiler: MSVC 19.44
2026-01-19 02:08:23 - omni_scripts.compilers.detector - [32m[1mINFO[0m - MSVC 19.44 supports C++23
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Compiler supports C++23: True
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Building target: engine
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Pipeline: Clean Build Pipeline
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Preset: default
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Config: release
2026-01-19 02:08:23 - __main__ - [32m[1mINFO[0m - Compiler: msvc
**********************************************************************
** Visual Studio 2022 Developer Command Prompt v17.14.20
** Copyright (c) 2025 Microsoft Corporation
**********************************************************************
[vcvarsall.bat] Environment initialized for: 'x64'
[INFO] 2026-01-19T02:08:23.658277 - Starting Clean Build Pipeline for engine
[INFO] 2026-01-19T02:08:23.658292 - Build context: product=engine, task=Clean Build Pipeline, arch=x64, build_type=release, compiler=msvc, lib_flag=True, st_flag=False
[INFO] 2026-01-19T02:08:23.658298 - Step 1: Cleaning build directories
[INFO] 2026-01-19T02:08:23.658302 - Cleaning build directories for engine
[INFO] 2026-01-19T02:08:23.658306 - lib_flag: True, st_flag: False
[INFO] 2026-01-19T02:08:23.658313 - Targets to clean: ['engine']
[INFO] 2026-01-19T02:08:23.658362 - Build directory for engine: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
[SUCCESS] 2026-01-19T02:08:23.658532 - Build directories cleaned successfully (0 directories)
[INFO] 2026-01-19T02:08:23.658543 - Step 2: Installing dependencies
[INFO] 2026-01-19T02:08:23.658714 - Using Visual Studio Developer Command Prompt: C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat
[INFO] 2026-01-19T02:08:23.658726 - Installing dependencies for engine
[INFO] 2026-01-19T02:08:23.658763 - Installing dependencies for engine in E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
[INFO] 2026-01-19T02:08:23.658770 - Installing Conan dependencies for release build
[INFO] 2026-01-19T02:08:23.659823 - Using conanfile: E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\conanfile.py
[INFO] 2026-01-19T02:08:23.659928 - Executing in vsdevcmd environment: conan install E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\conanfile.py --output-folder E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine --build=missing --profile:host E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\profiles\msvc-release --profile:build E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\profiles\msvc-release --settings build_type=Release
[INFO] 2026-01-19T02:08:23.659937 - Capture output: enabled
[INFO] 2026-01-19T02:08:23.660041 - Executing command in vsdevcmd environment
[INFO] 2026-01-19T02:08:23.660048 - Working directory: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
[INFO] 2026-01-19T02:08:23.660052 - Full command: call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && conan install E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\conanfile.py --output-folder E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine --build=missing --profile:host E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\profiles\msvc-release --profile:build E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\profiles\msvc-release --settings build_type=Release
[INFO] 2026-01-19T02:09:02.083352 - Command completed with return code: 1
[INFO] 2026-01-19T02:09:02.599736 - Validating Conan installation in: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
[INFO] 2026-01-19T02:09:02.600037 - Build directory exists: False
2026-01-19 02:09:02 - __main__ - [31m[1mERROR[0m - Build error: BuildError: Failed to install dependencies for engine Context: {'dependency': 'engine'}


## STDERR

======== Input profiles ========
Profile host:
[settings]
arch=x86_64
build_type=Release
compiler=msvc
compiler.cppstd=20
compiler.runtime=dynamic
compiler.runtime_type=Release
compiler.version=193
os=Windows
[conf]
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.microsoft.msbuild:vs_version=17
[buildenv]
CC=cl.exe
CXX=cl.exe

Profile build:
[settings]
arch=x86_64
build_type=Release
compiler=msvc
compiler.cppstd=20
compiler.runtime=dynamic
compiler.runtime_type=Release
compiler.version=193
os=Windows
[conf]
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.microsoft.msbuild:vs_version=17
[buildenv]
CC=cl.exe
CXX=cl.exe


======== Computing dependency graph ========
vulkan-loader/1.3.296.0: Not found in local cache, looking in remotes...
vulkan-loader/1.3.296.0: Checking remote: conancenter
Connecting to remote 'conancenter' anonymously
Graph root
    conanfile.py (omnicpp-template/0.0.3): E:\syncfold\Filen_private\dev\template\OmniCPP-template\conan\conanfile.py
Requirements
    catch2/3.7.1#d828f12a91e21037c58d9f08ddb63b5d - Cache
    cpptrace/0.5.4#0173ccf8a5410010c882d670237c648a - Cache
    fmt/10.2.1#658771bb858b77f380be2ebb22c338e9 - Cache
    glm/1.0.1#94392c53a527f7d830119b84fe80c754 - Cache
    gtest/1.15.0#9eba70e54373fb7325151ad3375934a1 - Cache
    libdwarf/0.9.1#2cc29f5c8ebecc1786278d3f647cf507 - Cache
    nlohmann_json/3.12.0#2d634ab0ec8d9f56353e5ccef6d6612c - Cache
    openssl/3.2.6#bd65eda90cfe5e42b0cd7df8fada8ecc - Cache
    spdlog/1.14.1#4fd40d9cbc1978247443a10d2ace58fd - Cache
    stb/cci.20240531#ede183dce303916dab0c1b835df3926a - Cache
    vulkan-headers/1.3.296.0#d3016741798609ba9dfa100c7a80ad5b - Cache
    zlib/1.3.1#cac0f6daea041b0ccf42934163defb20 - Cache
    zstd/1.5.7#b68ca8e3de04ba5957761751d1d661f4 - Cache
Build requirements
    nasm/2.16.01#31e26f2ee3c4346ecd347911bd126904 - Cache
    strawberryperl/5.32.1.1#8d114504d172cfea8ea1662d09b6333e - Cache
Resolved version ranges
    cpptrace/[~0.5]: cpptrace/0.5.4
    fmt/[~10.2]: fmt/10.2.1
    glm/[~1.0]: glm/1.0.1
    nlohmann_json/[~3.12]: nlohmann_json/3.12.0
    openssl/[~3.2]: openssl/3.2.6
    spdlog/[~1.14]: spdlog/1.14.1
    stb/[>=2023]: stb/cci.20240531
    zlib/[~1.3]: zlib/1.3.1
    zstd/[~1.5]: zstd/1.5.7
ERROR: Package 'vulkan-loader/1.3.296.0' not resolved: Unable to find 'vulkan-loader/1.3.296.0' in remotes.
[ERROR] 2026-01-19T02:09:02.601653 - Build directory does not exist: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\msvc\engine
