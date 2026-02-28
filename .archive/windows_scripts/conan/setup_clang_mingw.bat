@echo off
setlocal enabledelayedexpansion
REM Setup script for Clang-MinGW compiler environment with Vulkan

REM Check if MSYS2 UCRT64 clang is installed
set LLVM_FOUND=0
if exist "C:\msys64\ucrt64\bin\clang.exe" goto llvm_msys
if exist "C:\Program Files\LLVM\bin\clang.exe" goto llvm_program_files
if exist "C:\Program Files (x86)\LLVM\bin\clang.exe" goto llvm_program_files_x86
where clang.exe >nul 2>nul
if %errorlevel% equ 0 goto llvm_path
goto llvm_not_found

:llvm_msys
echo Found LLVM in MSYS2 UCRT64
set LLVM_DIR=C:\msys64\ucrt64
set LLVM_FOUND=1
goto llvm_end

:llvm_program_files
echo Found LLVM in Program Files
set LLVM_DIR=C:\Program Files\LLVM
set LLVM_FOUND=1
goto llvm_end

:llvm_program_files_x86
echo Found LLVM in Program Files x86
set LLVM_DIR=C:\Program Files (x86)\LLVM
set LLVM_FOUND=1
goto llvm_end

:llvm_path
echo Found LLVM in PATH
set LLVM_FOUND=1
goto llvm_end

:llvm_not_found
echo Error: LLVM/Clang not found.
echo Please install LLVM from https://llvm.org/ or ensure clang.exe is in your PATH.
echo Note: clang.exe is required for MinGW-w64 compatibility.
echo.
echo For Windows, download from: https://github.com/llvm/llvm-project/releases
echo Make sure to add LLVM\bin to your PATH or install to default location.
exit /b 1

:llvm_end


REM Set up Clang environment
if defined LLVM_DIR (
    echo Setting PATH to %LLVM_DIR%\bin;!PATH!
    set PATH=%LLVM_DIR%\bin;!PATH!
)

REM Check if MSYS2 UCRT64 gcc is installed
set MINGW_FOUND=0
if exist "C:\msys64\ucrt64\bin\gcc.exe" goto mingw_msys
if exist "C:\mingw64\bin\gcc.exe" goto mingw_mingw64
where gcc.exe >nul 2>nul
if %errorlevel% equ 0 goto mingw_path
goto mingw_not_found

:mingw_msys
echo Found MinGW in MSYS2 UCRT64
set MINGW_DIR=C:\msys64\ucrt64
set MINGW_FOUND=1
goto mingw_end

:mingw_mingw64
echo Found MinGW in mingw64
set MINGW_DIR=C:\mingw64
set MINGW_FOUND=1
goto mingw_end

:mingw_path
echo Found MinGW in PATH
set MINGW_FOUND=1
goto mingw_end

:mingw_not_found
echo Error: MinGW-w64 UCRT not found.
echo Please install MinGW-w64 UCRT from https://www.mingw-w64.org/ or MSYS2.
echo Make sure to add MinGW\bin to your PATH or install to default location.
exit /b 1

:mingw_end

REM Check for cmake and install if missing (for MSYS2)
if "%MINGW_DIR%"=="C:\msys64\ucrt64" (
    if not exist "%MINGW_DIR%\bin\cmake.exe" (
        echo Installing cmake in MSYS2...
        "%MINGW_DIR%\..\usr\bin\bash.exe" -c "pacman -S --noconfirm cmake"
    )
)

REM Set up MinGW environment
if defined MINGW_DIR (
    set PATH=%MINGW_DIR%\bin;!PATH!
)

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
set VK_LAYER_PATH=%VULKAN_SDK%\Bin
set VK_DATA_DIR=%VULKAN_SDK%\share\vulkan\explicit_layer.d

echo Vulkan SDK environment setup complete for Qt/Vulkan build.

:vulkan_done

REM Set Clang-MinGW-specific environment variables
set CC=clang.exe
set CXX=clang++.exe

echo Clang-MinGW environment setup complete.
if defined LLVM_DIR (
    echo LLVM_DIR: %LLVM_DIR%
)
if defined MINGW_DIR (
    echo MINGW_DIR: %MINGW_DIR%
)
echo VULKAN_SDK: %VULKAN_SDK%
echo CC: %CC%
echo CXX: %CXX%