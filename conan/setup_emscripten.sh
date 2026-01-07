#!/bin/bash
# Setup script for Emscripten environment

# Check if emsdk is available
if [ -z "$EMSDK" ]; then
    # Try to find emsdk
    if [ -f "/opt/emsdk/emsdk_env.sh" ]; then
        source "/opt/emsdk/emsdk_env.sh"
    elif [ -f "$HOME/emsdk/emsdk_env.sh" ]; then
        source "$HOME/emsdk/emsdk_env.sh"
    else
        echo "Error: Emscripten SDK not found."
        echo "Please install from: https://emscripten.org/docs/getting_started/downloads.html"
        echo "Or set EMSDK environment variable to emsdk root directory."
        exit 1
    fi
fi

# Validate emcc is available
if ! command -v emcc > /dev/null 2>&1; then
    echo "Error: emcc not found in PATH after Emscripten setup."
    exit 1
fi

echo "Emscripten environment setup complete."
echo "EMSDK: $EMSDK"
echo "CC: emcc"
echo "CXX: em++"