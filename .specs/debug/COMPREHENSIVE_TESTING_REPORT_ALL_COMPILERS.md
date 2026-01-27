# Comprehensive Testing Report - All Compilers

**Generated:** 2026-01-19T02:10:41.105245

## Test Matrix

| Functionality | MSVC | MSVC-clang | mingw-gcc | mingw-clang |
|---------------|------|------------|-----------|--------------|
| help | PASS | N/A | N/A | N/A |
| configure | FAIL | FAIL | FAIL | FAIL | 
| build | FAIL | FAIL | FAIL | FAIL | 
| clean | PASS | N/A | N/A | N/A |
| install | FAIL | FAIL | FAIL | FAIL | 
| test | FAIL | FAIL | FAIL | FAIL | 
| package | FAIL | FAIL | FAIL | FAIL | 
| format | FAIL | N/A | N/A | N/A |
| lint | FAIL | N/A | N/A | N/A |

## Errors Encountered

### configure_msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc

```

**Full Output:** See `.specs\debug\testing\configure_msvc.md`

### configure_clang-msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc

```

**Full Output:** See `.specs\debug\testing\configure_clang-msvc.md`

### configure_mingw-gcc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc

```

**Full Output:** See `.specs\debug\testing\configure_mingw-gcc.md`

### configure_mingw-clang

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang

```

**Full Output:** See `.specs\debug\testing\configure_mingw-clang.md`

### format

**Exit Code:** 1

**Full Output:** See `.specs\debug\testing\format.md`

### lint

**Exit Code:** 1

**Full Output:** See `.specs\debug\testing\lint.md`

### build_msvc

**Exit Code:** 1

**Error Output:**
```

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

```

**Full Output:** See `.specs\debug\testing\build_msvc.md`

### build_clang-msvc

**Exit Code:** 1

**Error Output:**
```

======== Input profiles ========
Profile host:
[settings]
arch=x86_64
build_type=Release
compiler=clang
compiler.cppstd=20
compiler.libcxx=libc++
compiler.runtime=dynamic
compiler.runtime_type=Release
compiler.runtime_version=v143
compiler.version=19
os=Windows
[options]
vulkan/*:shared=True
[conf]
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.microsoft.msbuild:vs_version=17
[buildenv]
CC=clang-cl.exe
CXX=clang-cl.exe

Profile build:
[settings]
arch=x86_64
build_type=Release
compiler=clang
compiler.cppstd=20
compiler.libcxx=libc++
compiler.runtime=dynamic
compiler.runtime_type=Release
compiler.runtime_version=v143
compiler.version=19
os=Windows
[options]
vulkan/*:shared=True
[conf]
tools.cmake.cmaketoolchain:generator=Ninja Multi-Config
tools.microsoft.msbuild:vs_version=17
[buildenv]
CC=clang-cl.exe
CXX=clang-cl.exe


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
    msys2/cci.latest#1996656c3c98e5765b25b60ff5cf77b4 - Cache
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
[ERROR] 2026-01-19T02:10:19.213046 - Build directory does not exist: E:\syncfold\Filen_private\dev\template\OmniCPP-template\build\release\clang-msvc\engine

```

**Full Output:** See `.specs\debug\testing\build_clang-msvc.md`

### build_mingw-gcc

**Exit Code:** 1

**Error Output:**
```
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


```

**Full Output:** See `.specs\debug\testing\build_mingw-gcc.md`

### build_mingw-clang

**Exit Code:** 1

**Error Output:**
```
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


```

**Full Output:** See `.specs\debug\testing\build_mingw-clang.md`

### install_msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc

```

**Full Output:** See `.specs\debug\testing\install_msvc.md`

### install_clang-msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc

```

**Full Output:** See `.specs\debug\testing\install_clang-msvc.md`

### install_mingw-gcc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc

```

**Full Output:** See `.specs\debug\testing\install_mingw-gcc.md`

### install_mingw-clang

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang

```

**Full Output:** See `.specs\debug\testing\install_mingw-clang.md`

### test_msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc

```

**Full Output:** See `.specs\debug\testing\test_msvc.md`

### test_clang-msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc

```

**Full Output:** See `.specs\debug\testing\test_clang-msvc.md`

### test_mingw-gcc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc

```

**Full Output:** See `.specs\debug\testing\test_mingw-gcc.md`

### test_mingw-clang

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang

```

**Full Output:** See `.specs\debug\testing\test_mingw-clang.md`

### package_msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler msvc

```

**Full Output:** See `.specs\debug\testing\package_msvc.md`

### package_clang-msvc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler clang-msvc

```

**Full Output:** See `.specs\debug\testing\package_clang-msvc.md`

### package_mingw-gcc

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-gcc

```

**Full Output:** See `.specs\debug\testing\package_mingw-gcc.md`

### package_mingw-clang

**Exit Code:** 2

**Error Output:**
```
usage: OmniCppController.py [-h] [--version]
                            {configure,build,clean,install,test,package,format,lint} ...
OmniCppController.py: error: unrecognized arguments: --compiler mingw-clang

```

**Full Output:** See `.specs\debug\testing\package_mingw-clang.md`

## Working Functionalities

- help
- clean

## Broken Functionalities

- configure_msvc (exit code: 2)
- configure_clang-msvc (exit code: 2)
- configure_mingw-gcc (exit code: 2)
- configure_mingw-clang (exit code: 2)
- format (exit code: 1)
- lint (exit code: 1)
- build_msvc (exit code: 1)
- build_clang-msvc (exit code: 1)
- build_mingw-gcc (exit code: 1)
- build_mingw-clang (exit code: 1)
- install_msvc (exit code: 2)
- install_clang-msvc (exit code: 2)
- install_mingw-gcc (exit code: 2)
- install_mingw-clang (exit code: 2)
- test_msvc (exit code: 2)
- test_clang-msvc (exit code: 2)
- test_mingw-gcc (exit code: 2)
- test_mingw-clang (exit code: 2)
- package_msvc (exit code: 2)
- package_clang-msvc (exit code: 2)
- package_mingw-gcc (exit code: 2)
- package_mingw-clang (exit code: 2)

## Recommendations

The following issues were found:

1. **configure_msvc**: Review the error output in the corresponding test file.
1. **configure_clang-msvc**: Review the error output in the corresponding test file.
1. **configure_mingw-gcc**: Review the error output in the corresponding test file.
1. **configure_mingw-clang**: Review the error output in the corresponding test file.
1. **format**: Review the error output in the corresponding test file.
1. **lint**: Review the error output in the corresponding test file.
1. **build_msvc**: Review the error output in the corresponding test file.
1. **build_clang-msvc**: Review the error output in the corresponding test file.
1. **build_mingw-gcc**: Review the error output in the corresponding test file.
1. **build_mingw-clang**: Review the error output in the corresponding test file.
1. **install_msvc**: Review the error output in the corresponding test file.
1. **install_clang-msvc**: Review the error output in the corresponding test file.
1. **install_mingw-gcc**: Review the error output in the corresponding test file.
1. **install_mingw-clang**: Review the error output in the corresponding test file.
1. **test_msvc**: Review the error output in the corresponding test file.
1. **test_clang-msvc**: Review the error output in the corresponding test file.
1. **test_mingw-gcc**: Review the error output in the corresponding test file.
1. **test_mingw-clang**: Review the error output in the corresponding test file.
1. **package_msvc**: Review the error output in the corresponding test file.
1. **package_clang-msvc**: Review the error output in the corresponding test file.
1. **package_mingw-gcc**: Review the error output in the corresponding test file.
1. **package_mingw-clang**: Review the error output in the corresponding test file.
