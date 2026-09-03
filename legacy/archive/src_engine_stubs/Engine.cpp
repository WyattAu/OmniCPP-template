/**
 * @file Engine.cpp
 * @brief Main engine implementation for OmniCpp
 * @version 1.0.0
 */

#include "engine/version.h"
#include "engine/Engine.hpp"
#include "engine/IEngine.hpp"
#include "engine/IRenderer.hpp"
#include "engine/IInputManager.hpp"
#include "engine/IAudioManager.hpp"
#include "engine/IPhysicsEngine.hpp"
#include "engine/IResourceManager.hpp"
#include "engine/ILogger.hpp"
#include "engine/IPlatform.hpp"
#include "engine/logging/Log.hpp"
#include "engine/window/window_manager.hpp"
#include "engine/graphics/renderer.hpp"

#include <iostream>
#include <memory>
#include <stdexcept>

namespace omnicpp {

/**
 * @brief Engine implementation
 */
class EngineImpl : public IEngine {
public:
    EngineImpl() = default;
    ~EngineImpl() override = default;

    bool initialize(const EngineConfig& config) override {
        // Initialize logging
        omnicpp::log::init();
        omnicpp::log::info("Engine initialization started");

        // Initialize platform
        if (config.platform) {
            m_platform.reset(config.platform);
            if (!m_platform->initialize()) {
                omnicpp::log::error("Failed to initialize platform");
                return false;
            }
            omnicpp::log::info("Platform initialized");
        }

        // Initialize window manager and renderer
        m_window_manager = std::make_unique<OmniCpp::Engine::Window::WindowManager>();
        if (!m_window_manager->initialize({"OmniCpp Engine", 1280, 720, false, true, true})) {
            omnicpp::log::error("Failed to initialize window manager");
            return false;
        }

        m_graphics_renderer = std::make_unique<OmniCpp::Engine::Graphics::Renderer>();
        OmniCpp::Engine::Graphics::RendererConfig renderer_config;
        renderer_config.vsync = true;
        renderer_config.msaa_samples = 4;
        renderer_config.enable_debug = false;
        if (!m_graphics_renderer->initialize(renderer_config)) {
            omnicpp::log::error("Failed to initialize graphics renderer");
            return false;
        }

        m_graphics_renderer->set_window_manager(m_window_manager.get());

        // Initialize renderer
        if (config.renderer) {
            m_renderer.reset(config.renderer);
            if (!m_renderer->initialize()) {
                omnicpp::log::error("Failed to initialize renderer");
                return false;
            }
            omnicpp::log::info("Renderer initialized");
        }

        // Initialize input manager
        if (config.input_manager) {
            m_input_manager.reset(config.input_manager);
            if (!m_input_manager->initialize()) {
                omnicpp::log::error("Failed to initialize input manager");
                return false;
            }
            omnicpp::log::info("Input manager initialized");
        }

        // Initialize audio manager
        if (config.audio_manager) {
            m_audio_manager.reset(config.audio_manager);
            if (!m_audio_manager->initialize()) {
                omnicpp::log::error("Failed to initialize audio manager");
                return false;
            }
            omnicpp::log::info("Audio manager initialized");
        }

        // Initialize physics engine
        if (config.physics_engine) {
            m_physics_engine.reset(config.physics_engine);
            if (!m_physics_engine->initialize()) {
                omnicpp::log::error("Failed to initialize physics engine");
                return false;
            }
            omnicpp::log::info("Physics engine initialized");
        }

        // Initialize resource manager
        if (config.resource_manager) {
            m_resource_manager.reset(config.resource_manager);
            if (!m_resource_manager->initialize()) {
                omnicpp::log::error("Failed to initialize resource manager");
                return false;
            }
            omnicpp::log::info("Resource manager initialized");
        }

        m_initialized = true;
        omnicpp::log::info("Engine initialization complete");
        return true;
    }

    void shutdown() override {
        if (!m_initialized) {
            return;
        }

        omnicpp::log::info("Engine shutdown started");

        // Shutdown in reverse order
        if (m_resource_manager) {
            m_resource_manager->shutdown();
        }
        if (m_physics_engine) {
            m_physics_engine->shutdown();
        }
        if (m_audio_manager) {
            m_audio_manager->shutdown();
        }
        if (m_input_manager) {
            m_input_manager->shutdown();
        }
        if (m_renderer) {
            m_renderer->shutdown();
        }
        if (m_graphics_renderer) {
            m_graphics_renderer->shutdown();
        }
        if (m_window_manager) {
            m_window_manager->shutdown();
        }
        if (m_platform) {
            m_platform->shutdown();
        }

        omnicpp::log::info("Engine shutdown complete");
        omnicpp::log::shutdown();

        m_initialized = false;
    }

    void update(float delta_time) override {
        if (!m_initialized) {
            return;
        }

        // Update input
        if (m_input_manager) {
            m_input_manager->process_events(delta_time);
        }

        // Update physics
        if (m_physics_engine) {
            m_physics_engine->update(delta_time);
        }

        // Update audio
        if (m_audio_manager) {
            m_audio_manager->update(delta_time);
        }

        // Update window and graphics
        if (m_window_manager) {
            m_window_manager->update();
        }
        if (m_graphics_renderer) {
            m_graphics_renderer->update();
        }

        // Check if window should close
        if (m_window_manager && m_window_manager->should_close()) {
            m_initialized = false;
        }
    }

    void render() override {
        if (!m_initialized) {
            return;
        }

        // Check if window should close
        if (m_window_manager && m_window_manager->should_close()) {
            m_initialized = false;
        }

        // Update window and graphics
        if (m_window_manager) {
            m_window_manager->update();
        }
        if (m_graphics_renderer) {
            m_graphics_renderer->render();
        }

        // Present frame
        if (m_graphics_renderer) {
            m_graphics_renderer->present();
        }

        // Render scene here
        if (m_renderer) {
            m_renderer->begin_frame();
            m_renderer->end_frame();
        }
    }

    IRenderer* get_renderer() const override {
        return m_renderer.get();
    }

    IInputManager* get_input_manager() const override {
        return m_input_manager.get();
    }

    IAudioManager* get_audio_manager() const override {
        return m_audio_manager.get();
    }

    IPhysicsEngine* get_physics_engine() const override {
        return m_physics_engine.get();
    }

    IResourceManager* get_resource_manager() const override {
        return m_resource_manager.get();
    }

    ILogger* get_logger() const override {
        return nullptr;  // Using spdlog shim directly
    }

    IPlatform* get_platform() const override {
        return m_platform.get();
    }

    bool is_initialized() const override {
        return m_initialized;
    }

private:
    std::unique_ptr<IRenderer> m_renderer;
    std::unique_ptr<IInputManager> m_input_manager;
    std::unique_ptr<IAudioManager> m_audio_manager;
    std::unique_ptr<IPhysicsEngine> m_physics_engine;
    std::unique_ptr<IResourceManager> m_resource_manager;
    std::unique_ptr<IPlatform> m_platform;
    std::unique_ptr<OmniCpp::Engine::Window::WindowManager> m_window_manager;
    std::unique_ptr<OmniCpp::Engine::Graphics::Renderer> m_graphics_renderer;
    bool m_initialized = false;
};

// Factory functions
extern "C" {

OMNICPP_EXPORT IEngine* create_engine(const EngineConfig& config) {
    try {
        auto* engine = new (std::nothrow) EngineImpl();
        if (!engine->initialize(config)) {
            delete engine;
            return nullptr;
        }
        return engine;
    } catch (const std::exception& e) {
        return nullptr;
    }
}

OMNICPP_EXPORT void destroy_engine(IEngine* engine) {
    if (engine) {
        engine->shutdown();
        delete engine;
    }
}

OMNICPP_EXPORT const char* engine_get_version() {
    return OMNICPP_ENGINE_VERSION_STRING;
}

OMNICPP_EXPORT int engine_get_version_major() {
    return OMNICPP_ENGINE_VERSION_MAJOR;
}

OMNICPP_EXPORT int engine_get_version_minor() {
    return OMNICPP_ENGINE_VERSION_MINOR;
}

OMNICPP_EXPORT int engine_get_version_patch() {
    return OMNICPP_ENGINE_VERSION_PATCH;
}

} // extern "C"

} // namespace omnicpp
