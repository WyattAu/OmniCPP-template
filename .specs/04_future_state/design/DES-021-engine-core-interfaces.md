# DES-021: Engine Core Interfaces

## Overview
Defines the core engine interfaces for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_ENGINE_CORE_INTERFACES_H
#define OMNICPP_ENGINE_CORE_INTERFACES_H

#include <memory>
#include <string>
#include <vector>
#include <functional>
#include <chrono>

namespace omnicpp {
namespace engine {

// Forward declarations
class IPlatform;
class IRenderer;
class IAudioManager;
class IPhysicsEngine;
class IResourceManager;
class ISceneManager;
class IInputManager;
class ILogger;

// Engine configuration
struct EngineConfig {
    std::string window_title;
    int window_width;
    int window_height;
    bool fullscreen;
    bool vsync;
    int max_fps;
    std::string log_level;
    std::string log_file;

    EngineConfig()
        : window_title("OmniCpp Engine")
        , window_width(1280)
        , window_height(720)
        , fullscreen(false)
        , vsync(true)
        , max_fps(60)
        , log_level("info")
        , log_file("engine.log")
    {}
};

// Engine state
enum class EngineState {
    UNINITIALIZED,
    INITIALIZING,
    RUNNING,
    PAUSED,
    SHUTTING_DOWN,
    SHUTDOWN
};

// Engine statistics
struct EngineStats {
    double fps;
    double frame_time;
    double delta_time;
    uint64_t frame_count;
    uint64_t total_time;

    EngineStats()
        : fps(0.0)
        , frame_time(0.0)
        , delta_time(0.0)
        , frame_count(0)
        , total_time(0)
    {}
};

// Engine interface
class IEngine {
public:
    virtual ~IEngine() = default;

    // Initialization
    virtual bool initialize(const EngineConfig& config) = 0;
    virtual void shutdown() = 0;

    // Main loop
    virtual void run() = 0;
    virtual void stop() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // State management
    virtual EngineState get_state() const = 0;
    virtual void set_state(EngineState state) = 0;

    // Statistics
    virtual const EngineStats& get_stats() const = 0;
    virtual void update_stats(double delta_time) = 0;

    // Subsystems
    virtual IPlatform* get_platform() const = 0;
    virtual IRenderer* get_renderer() const = 0;
    virtual IAudioManager* get_audio_manager() const = 0;
    virtual IPhysicsEngine* get_physics_engine() const = 0;
    virtual IResourceManager* get_resource_manager() const = 0;
    virtual ISceneManager* get_scene_manager() const = 0;
    virtual IInputManager* get_input_manager() const = 0;
    virtual ILogger* get_logger() const = 0;

    // Frame callbacks
    virtual void on_frame_start() = 0;
    virtual void on_frame_end() = 0;
    virtual void on_update(double delta_time) = 0;
    virtual void on_render() = 0;

    // Event handling
    virtual void handle_events() = 0;
};

// Engine factory
class IEngineFactory {
public:
    virtual ~IEngineFactory() = default;

    virtual std::unique_ptr<IEngine> create_engine() = 0;
    virtual void destroy_engine(std::unique_ptr<IEngine> engine) = 0;
};

// Engine builder
class IEngineBuilder {
public:
    virtual ~IEngineBuilder() = default;

    virtual IEngineBuilder& set_config(const EngineConfig& config) = 0;
    virtual IEngineBuilder& set_platform(std::unique_ptr<IPlatform> platform) = 0;
    virtual IEngineBuilder& set_renderer(std::unique_ptr<IRenderer> renderer) = 0;
    virtual IEngineBuilder& set_audio_manager(std::unique_ptr<IAudioManager> audio_manager) = 0;
    virtual IEngineBuilder& set_physics_engine(std::unique_ptr<IPhysicsEngine> physics_engine) = 0;
    virtual IEngineBuilder& set_resource_manager(std::unique_ptr<IResourceManager> resource_manager) = 0;
    virtual IEngineBuilder& set_scene_manager(std::unique_ptr<ISceneManager> scene_manager) = 0;
    virtual IEngineBuilder& set_input_manager(std::unique_ptr<IInputManager> input_manager) = 0;
    virtual IEngineBuilder& set_logger(std::unique_ptr<ILogger> logger) = 0;

    virtual std::unique_ptr<IEngine> build() = 0;
};

// Engine event
struct EngineEvent {
    enum class Type {
        INITIALIZED,
        SHUTDOWN,
        PAUSED,
        RESUMED,
        ERROR
    };

    Type type;
    std::string message;
    std::chrono::system_clock::time_point timestamp;

    EngineEvent(Type t, const std::string& msg = "")
        : type(t)
        , message(msg)
        , timestamp(std::chrono::system_clock::now())
    {}
};

// Engine event listener
using EngineEventListener = std::function<void(const EngineEvent&)>;

// Engine event manager
class IEngineEventManager {
public:
    virtual ~IEngineEventManager() = default;

    virtual void add_listener(EngineEventListener listener) = 0;
    virtual void remove_listener(EngineEventListener listener) = 0;
    virtual void emit_event(const EngineEvent& event) = 0;
    virtual void clear_listeners() = 0;
};

// Engine context
class IEngineContext {
public:
    virtual ~IEngineContext() = default;

    virtual IEngine* get_engine() const = 0;
    virtual IPlatform* get_platform() const = 0;
    virtual IRenderer* get_renderer() const = 0;
    virtual IAudioManager* get_audio_manager() const = 0;
    virtual IPhysicsEngine* get_physics_engine() const = 0;
    virtual IResourceManager* get_resource_manager() const = 0;
    virtual ISceneManager* get_scene_manager() const = 0;
    virtual IInputManager* get_input_manager() const = 0;
    virtual ILogger* get_logger() const = 0;

    virtual const EngineConfig& get_config() const = 0;
    virtual const EngineStats& get_stats() const = 0;
    virtual EngineState get_state() const = 0;
};

// Engine module
class IEngineModule {
public:
    virtual ~IEngineModule() = default;

    virtual bool initialize(IEngineContext* context) = 0;
    virtual void shutdown() = 0;
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;

    virtual std::string get_name() const = 0;
    virtual std::string get_version() const = 0;
};

// Engine module manager
class IEngineModuleManager {
public:
    virtual ~IEngineModuleManager() = default;

    virtual bool register_module(std::unique_ptr<IEngineModule> module) = 0;
    virtual bool unregister_module(const std::string& name) = 0;
    virtual IEngineModule* get_module(const std::string& name) const = 0;
    virtual std::vector<IEngineModule*> get_all_modules() const = 0;

    virtual void update_modules(double delta_time) = 0;
    virtual void render_modules() = 0;
    virtual void shutdown_modules() = 0;
};

// Engine profiler
class IEngineProfiler {
public:
    virtual ~IEngineProfiler() = default;

    virtual void begin_frame() = 0;
    virtual void end_frame() = 0;
    virtual void begin_sample(const std::string& name) = 0;
    virtual void end_sample(const std::string& name) = 0;

    virtual double get_sample_time(const std::string& name) const = 0;
    virtual std::vector<std::string> get_sample_names() const = 0;
    virtual void clear_samples() = 0;
};

// Engine memory manager
class IEngineMemoryManager {
public:
    virtual ~IEngineMemoryManager() = default;

    virtual void* allocate(size_t size, size_t alignment = 16) = 0;
    virtual void deallocate(void* ptr) = 0;

    virtual size_t get_allocated_size() const = 0;
    virtual size_t get_total_allocations() const = 0;
    virtual void reset_stats() = 0;
};

// Engine task scheduler
class IEngineTaskScheduler {
public:
    virtual ~IEngineTaskScheduler() = default;

    virtual void schedule_task(std::function<void()> task) = 0;
    virtual void schedule_delayed_task(std::function<void()> task, double delay) = 0;
    virtual void schedule_recurring_task(std::function<void()> task, double interval) = 0;

    virtual void update(double delta_time) = 0;
    virtual void clear_tasks() = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_ENGINE_CORE_INTERFACES_H
```

## Dependencies

### Internal Dependencies
- `DES-022` - ECS Component Design
- `DES-023` - ECS System Design
- `DES-024` - Renderer Interface
- `DES-025` - Audio Manager Interface
- `DES-026` - Physics Engine Interface
- `DES-027` - Resource Manager Interface
- `DES-028` - Scene Manager Interface

### External Dependencies
- `memory` - Smart pointers
- `string` - String handling
- `vector` - Dynamic arrays
- `functional` - Function objects
- `chrono` - Time handling

## Related Requirements
- REQ-030: Engine Core Architecture
- REQ-031: Engine Subsystem Integration

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Engine Initialization
1. Initialize subsystems in order
2. Validate configuration
3. Set up event listeners
4. Start main loop

### Main Loop
1. Handle events
2. Update delta time
3. Update subsystems
4. Render frame
5. Update statistics

### State Management
1. Track engine state
2. Handle state transitions
3. Pause/resume functionality
4. Clean shutdown

### Subsystem Integration
1. Provide access to all subsystems
2. Coordinate subsystem updates
3. Handle subsystem errors
4. Manage subsystem lifecycle

## Usage Example

```cpp
#include "engine_core_interfaces.hpp"

using namespace omnicpp::engine;

int main() {
    // Create engine configuration
    EngineConfig config;
    config.window_title = "My Game";
    config.window_width = 1920;
    config.window_height = 1080;
    config.fullscreen = false;
    config.vsync = true;
    config.max_fps = 60;

    // Create engine
    auto engine = std::make_unique<Engine>();

    // Initialize engine
    if (!engine->initialize(config)) {
        std::cerr << "Failed to initialize engine" << std::endl;
        return 1;
    }

    // Run engine
    engine->run();

    // Shutdown engine
    engine->shutdown();

    return 0;
}
```
