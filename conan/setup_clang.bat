@echo off
REM Setup script for Clang compiler environment with Vulkan

REM Auto-detect VsDevCmd.bat location (more reliable than vcvarsall.bat)
set VS_DEV_CMD=
for %%e in (Community Professional Enterprise) do (
    if exist "C:\Program Files\Microsoft Visual Studio\2022\%%e\Common7\Tools\VsDevCmd.bat" (
        set VS_DEV_CMD=C:\Program Files\Microsoft Visual Studio\2022\%%e\Common7\Tools\VsDevCmd.bat
        goto :vs_found
    )
)
:vs_found

if not defined VS_DEV_CMD (
    echo Error: VsDevCmd.bat not found in C:\Program Files\Microsoft Visual Studio\2022\*
    echo Please ensure Visual Studio 2022 is installed with C++ tools.
    exit /b 1
)

REM Set VS install path for Developer PowerShell
set VS_INSTALL_PATH=%VS_DEV_CMD:\Common7\Tools\VsDevCmd.bat=%

REM Check if LLVM is installed (try common locations)
set LLVM_FOUND=0
echo Checking for LLVM...

REM Check for LLVM in Visual Studio installation
set LLVM_CHECKED=0
for %%e in (Community Professional Enterprise) do (
    if exist "C:\Program Files\Microsoft Visual Studio\2022\%%e\VC\Tools\Llvm\bin\clang-cl.exe" (
        echo Found LLVM in VS 2022 %%e
        set LLVM_DIR=C:\Program Files\Microsoft Visual Studio\2022\%%e\VC\Tools\Llvm
        set LLVM_FOUND=1
        set LLVM_CHECKED=1
    )
)
if %LLVM_CHECKED%==1 goto :llvm_found
:llvm_found
if %LLVM_FOUND%==0 (
    echo Checking if clang-cl is in PATH...
    where clang-cl >nul 2>nul
    if %errorlevel% equ 0 (
        echo clang-cl found in PATH
        set LLVM_FOUND=1
        REM LLVM is in PATH, don't set LLVM_DIR
    ) else (
        echo clang-cl not found
    )
)

if %LLVM_FOUND%==0 (
    echo Error: LLVM/Clang not found.
    echo Please install LLVM from https://llvm.org/ or ensure clang-cl.exe is in your PATH.
    echo Note: clang-cl is required for MSVC compatibility when using Clang with Visual Studio.
    echo.
    echo For Windows, download from: https://github.com/llvm/llvm-project/releases
    echo Make sure to add LLVM\bin to your PATH or install to default location.
    echo.
    echo Skipping LLVM setup - continuing with MSVC-only environment.
) else (
    REM Set up Clang environment
    if defined LLVM_DIR (
        set "PATH=%LLVM_DIR%\bin;%PATH%"
    )
)

REM Check if this is a Qt/Vulkan build by examining build context
if "%OMNICPP_BUILD_TARGET%"=="qt-vulkan" goto :setup_vulkan
echo Building non-Qt target - Vulkan SDK not required
goto :vulkan_done

:setup_vulkan
REM Auto-detect Vulkan SDK version
for /d %%i in ("C:\VulkanSDK\*") do (
    set VULKAN_SDK=%%i
    goto :vulkan_found
)
:vulkan_found

if not defined VULKAN_SDK (
    echo Vulkan SDK not found. Attempting automatic installation...
    python "%~dp0..\omni_scripts\setup_vulkan.py" --install
    if %errorlevel% neq 0 (
        echo Error: Failed to install Vulkan SDK automatically.
        echo Vulkan SDK is required for Qt/Vulkan builds.
        echo Please install Vulkan SDK manually from https://vulkan.lunarg.com/sdk/home
        echo Alternatively, build non-Qt targets which don't require Vulkan SDK.
        exit /b 1
    )
    REM Re-detect Vulkan SDK after installation
    for /d %%i in ("C:\VulkanSDK\*") do (
        set VULKAN_SDK=%%i
        goto :vulkan_found_after_install
    )
    :vulkan_found_after_install
    if not defined VULKAN_SDK (
        echo Error: Vulkan SDK installation completed but SDK not found.
        echo Please check the installation or install manually.
        exit /b 1
    )
)

REM Set Vulkan SDK environment variables
set PATH=%VULKAN_SDK%\Bin;%PATH%
set VK_SDK_PATH=%VULKAN_SDK%

REM Optional: Set additional Vulkan paths if needed
set VK_LAYER_PATH=%VULKAN_SDK%\Bin
set VK_DATA_DIR=%VULKAN_SDK%\share\vulkan\explicit_layer.d

echo Vulkan SDK environment setup complete for Qt/Vulkan build.

:vulkan_done

REM Set Clang-specific environment variables (using clang-cl for MSVC compatibility)
if %LLVM_FOUND%==1 (
    set CC=clang-cl.exe
    set CXX=clang-cl.exe
) else (
    set CC=cl.exe
    set CXX=cl.exe
)

echo Clang-MSVC environment setup complete.
if %LLVM_FOUND%==1 (
    echo LLVM_DIR: %LLVM_DIR%
) else (
    echo LLVM: Not found - using MSVC compiler
)
echo VULKAN_SDK: %VULKAN_SDK%
echo CC: %CC%
echo CXX: %CXX%
echo VS_INSTALL_PATH: %VS_INSTALL_PATH%

REM Call VsDevCmd.bat to set up VS environment
call "%VS_DEV_CMD%" -arch=x64 -host_arch=x64

REM Validate environment setup
if not defined VSINSTALLDIR (
    echo Error: VSINSTALLDIR not set after VsDevCmd.bat call.
    echo Visual Studio environment setup failed.
    echo This may indicate a problem with your Visual Studio installation.
    echo Try repairing Visual Studio or reinstalling the C++ workload.
    exit /b 1
)

if %LLVM_FOUND%==1 (
    set CLANG_CL=clang-cl.exe
    where clang-cl >nul 2>nul
    if %errorlevel% neq 0 (
        echo Error: clang-cl.exe not found in PATH after LLVM setup.
        echo LLVM installation may be incomplete or PATH not set correctly.
        echo Please ensure LLVM\bin is in your PATH.
        exit /b 1
    )
) else (
    echo Warning: LLVM not found. Using MSVC compiler only.
    echo For Clang-MSVC builds, install LLVM and ensure clang-cl.exe is available.
    REM Fallback: could set generator to Ninja if VS generator fails, but profile handles it
)