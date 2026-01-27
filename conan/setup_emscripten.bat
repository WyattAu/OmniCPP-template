@echo off
REM Setup script for Emscripten environment

REM Check if emsdk is available
if not defined EMSDK (
    REM Try to find emsdk
    if exist "C:\emsdk\emsdk_env.bat" (
        call "C:\emsdk\emsdk_env.bat"
    ) else if exist "%USERPROFILE%\emsdk\emsdk_env.bat" (
        call "%USERPROFILE%\emsdk\emsdk_env.bat"
    ) else (
        echo Error: Emscripten SDK not found.
        echo Please install from: https://emscripten.org/docs/getting_started/downloads.html
        echo Or set EMSDK environment variable to emsdk root directory.
        exit /b 1
    )
)

REM Validate emcc is available
where emcc >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: emcc not found in PATH after Emscripten setup.
    exit /b 1
)

echo Emscripten environment setup complete.
echo EMSDK: %EMSDK%
echo CC: emcc
echo CXX: em++