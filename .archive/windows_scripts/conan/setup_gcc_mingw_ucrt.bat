@echo off
REM Setup script for GCC with MSYS2 UCRT64 compiler environment

REM Detect if running in MSYS2 terminal vs cmd.exe
if defined MSYSTEM (
    REM Running in MSYS2 terminal - use MSYS2 path conventions
    set MSYS2_ROOT=/c/msys64
    set PATH_PREFIX=
) else (
    REM Running in cmd.exe - use Windows path conventions
    set MSYS2_ROOT=C:\msys64
    set PATH_PREFIX=%MSYS2_ROOT%\ucrt64\bin;
)

if not exist "%MSYS2_ROOT%\ucrt64\bin\gcc.exe" (
    echo Error: MSYS2 UCRT64 GCC not found at %MSYS2_ROOT%\ucrt64\bin\gcc.exe
    echo Please ensure MSYS2 is installed with ucrt64 toolchain.
    exit /b 1
)

REM Check for cmake and install if missing
if not exist "%MSYS2_ROOT%\ucrt64\bin\cmake.exe" (
    echo Installing cmake in MSYS2...
    if defined MSYSTEM (
        pacman -S --noconfirm cmake
    ) else (
        "%MSYS2_ROOT%\usr\bin\bash.exe" -c "pacman -S --noconfirm cmake"
    )
)

REM Set up MSYS2 UCRT64 environment
set PATH=%PATH_PREFIX%%MSYS2_ROOT%\ucrt64\bin;%PATH%

REM Validate cmake is available
cmake --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: cmake not found in PATH after setup.
    echo Please ensure cmake is installed and accessible.
    exit /b 1
)
echo cmake found:
cmake --version | findstr "cmake version"

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

REM Set GCC-specific environment variables
set CC=gcc.exe
set CXX=g++.exe

echo GCC-MSYS2-UCRT64 environment setup complete.
echo MSYS2_ROOT: %MSYS2_ROOT%
echo VULKAN_SDK: %VULKAN_SDK%
echo CC: %CC%
echo CXX: %CXX%