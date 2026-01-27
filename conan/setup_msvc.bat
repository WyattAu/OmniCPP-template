@echo off
REM Setup script for MSVC compiler environment

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
    echo Please ensure Visual Studio 2022 is installed.
    exit /b 1
)

REM Set VS install path for Developer PowerShell
set VS_INSTALL_PATH=%VS_DEV_CMD:\Common7\Tools\VsDevCmd.bat=%

REM Detect the VS toolset version (will be set in Developer PowerShell)
REM VS 2022 typically uses v143, but we should detect it dynamically
REM For now, assume v143 as default, will be overridden in PowerShell
set VS_TOOLSET=v143



REM Set MSVC-specific environment variables
set CC=cl.exe
set CXX=cl.exe

REM Force Conan to use x86_64 architecture instead of auto-detecting amd64
REM Note: This is kept for compatibility, but Conan should auto-detect properly now
set CONAN_ARCH=x86_64

REM Set CMake generator toolset to match detected VS version
set CMAKE_GENERATOR_TOOLSET=%VS_TOOLSET%

echo MSVC environment setup complete.
echo CC: %CC%
echo CXX: %CXX%
echo CONAN_ARCH: %CONAN_ARCH%
echo CMAKE_GENERATOR_TOOLSET: %CMAKE_GENERATOR_TOOLSET%
echo VS_INSTALL_PATH: %VS_INSTALL_PATH%

REM Call VsDevCmd.bat to set up VS environment
call "%VS_DEV_CMD%" -arch=x64 -host_arch=x64