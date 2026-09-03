# Quick Start Guide

OmniCpp is an experimental C++23 engine/build-system template. The supported baseline is Linux with CMake and a C++23 compiler; Qt/Vulkan features require their platform dependencies.

## Prerequisites

- C++23-capable compiler
- CMake 3.28 or later
- Python 3.11 or later
- Ninja (recommended)

## Configure and build the portable baseline

The following disables optional GUI/graphics backends and is useful for validating the core build. The headless runtime supports fixed-step execution and configurable catch-up behavior; use the default policy for deterministic replay, or configure a tick cap when bounded recovery from stalls is required:

```bash
cmake -S . -B build -G Ninja \
  -DOMNICPP_USE_QT6=OFF \
  -DOMNICPP_USE_VULKAN=OFF \
  -DOMNICPP_USE_GLFW=OFF \
  -DOMNICPP_USE_QUILL=OFF \
  -DOMNICPP_USE_GLM=OFF \
  -DOMNICPP_USE_STB=OFF \
  -DOMNICPP_USE_NLOHMANN_JSON=OFF \
  -DOMNICPP_BUILD_EXAMPLES=OFF
cmake --build build
```

Enable only dependencies installed on your system. Do not rely on hard-coded SDK paths.

## Run tests

```bash
cmake -S . -B build-tests -G Ninja \
  -DOMNICPP_BUILD_TESTS=ON \
  -DOMNICPP_USE_QT6=OFF \
  -DOMNICPP_USE_VULKAN=OFF \
  -DOMNICPP_USE_GLFW=OFF \
  -DOMNICPP_USE_QUILL=OFF
cmake --build build-tests
ctest --test-dir build-tests --output-on-failure
```

Python tests can be run after package installation or with the repository root on `PYTHONPATH`:

```bash
PYTHONPATH=. python -m pytest -q
```

## Deterministic runtime policy

The canonical headless runtime defaults to `run_all`, which preserves all elapsed simulation time. Applications with real-time deadlines should configure either `cap_and_drop_time` or `cap_and_report_overrun` and monitor the overrun counters rather than allowing an unbounded catch-up loop.

## Status

Graphics, networking, scripting, and several game subsystems remain under development. Treat this repository as a template/prototype until the CI baseline is green and runtime benchmarks are available.

## Next steps

- Read the [API Documentation](../api/overview.md)
- Review the [Developer Guide](../developer-guide.md)
- Inspect the [build documentation](../user-guide-build-system.md)
