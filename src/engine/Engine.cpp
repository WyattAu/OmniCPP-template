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
        // Initialize logger first
        if (config.logger) {
            m_logger.reset(config.logger);
            if (!m_logger->initialize()) {
                return false;
            }
            m_logger->log(LogLevel::INFO, "Engine initialization started", "ENGINE");
        }

        // Initialize platform
        if (config.platform) {
            m_platform.reset(config.platform);
            if (!m_platform->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize platform", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Platform initialized", "ENGINE");
            }
        }

        // Initialize renderer
        if (config.renderer) {
            m_renderer.reset(config.renderer);
            if (!m_renderer->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize renderer", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Renderer initialized", "ENGINE");
            }
        }

        // Initialize input manager
        if (config.input_manager) {
            m_input_manager.reset(config.input_manager);
            if (!m_input_manager->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize input manager", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Input manager initialized", "ENGINE");
            }
        }

        // Initialize audio manager
        if (config.audio_manager) {
            m_audio_manager.reset(config.audio_manager);
            if (!m_audio_manager->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize audio manager", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Audio manager initialized", "ENGINE");
            }
        }

        // Initialize physics engine
        if (config.physics_engine) {
            m_physics_engine.reset(config.physics_engine);
            if (!m_physics_engine->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize physics engine", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Physics engine initialized", "ENGINE");
            }
        }

        // Initialize resource manager
        if (config.resource_manager) {
            m_resource_manager.reset(config.resource_manager);
            if (!m_resource_manager->initialize()) {
                if (m_logger) {
                    m_logger->log(LogLevel::ERROR, "Failed to initialize resource manager", "ENGINE");
                }
                return false;
            }
            if (m_logger) {
                m_logger->log(LogLevel::INFO, "Resource manager initialized", "ENGINE");
            }
        }

        m_initialized = true;
        if (m_logger) {
            m_logger->log(LogLevel::INFO, "Engine initialization complete", "ENGINE");
        }
        return true;
    }

    void shutdown() override {
        if (!m_initialized) {
            return;
        }

        if (m_logger) {
            m_logger->log(LogLevel::INFO, "Engine shutdown started", "ENGINE");
        }

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
        if (m_platform) {
            m_platform->shutdown();
        }
        if (m_logger) {
            m_logger->log(LogLevel::INFO, "Engine shutdown complete", "ENGINE");
            m_logger->shutdown();
        }

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
    }

    void render() override {
        if (!m_initialized || !m_renderer) {
            return;
        }

        m_renderer->begin_frame();
        // Render scene here
        m_renderer->end_frame();
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
        return m_logger.get();
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
    std::unique_ptr<ILogger> m_logger;
    std::unique_ptr<IPlatform> m_platform;
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
