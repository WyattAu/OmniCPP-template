/**
 * @file IEngine.hpp
 * @brief Engine interface for OmniCpp
 * @version 1.0.0
 */

#ifndef OMNICPP_IENGINE_HPP
#define OMNICPP_IENGINE_HPP

#include <cstdint>

namespace omnicpp {

// Forward declarations
class IRenderer;
class IInputManager;
class IAudioManager;
class IPhysicsEngine;
class IResourceManager;
class ILogger;
class IPlatform;

/**
 * @brief Engine configuration structure
 */
struct EngineConfig {
    IRenderer* renderer;
    IInputManager* input_manager;
    IAudioManager* audio_manager;
    IPhysicsEngine* physics_engine;
    IResourceManager* resource_manager;
    ILogger* logger;
    IPlatform* platform;
};

/**
 * @brief Engine interface
 */
class IEngine {
public:
    virtual ~IEngine() = default;
    
    /**
     * @brief Initialize engine
     * @param config Engine configuration
     * @return True if successful, false otherwise
     */
    virtual bool initialize(const EngineConfig& config) = 0;
    
    /**
     * @brief Shutdown engine
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Update engine state
     * @param delta_time Time since last frame in seconds
     */
    virtual void update(float delta_time) = 0;
    
    /**
     * @brief Render frame
     */
    virtual void render() = 0;
    
    /**
     * @brief Get renderer subsystem
     * @return Pointer to renderer interface, or nullptr
     */
    virtual IRenderer* get_renderer() const = 0;
    
    /**
     * @brief Get input manager subsystem
     * @return Pointer to input manager interface, or nullptr
     */
    virtual IInputManager* get_input_manager() const = 0;
    
    /**
     * @brief Get audio manager subsystem
     * @return Pointer to audio manager interface, or nullptr
     */
    virtual IAudioManager* get_audio_manager() const = 0;
    
    /**
     * @brief Get physics engine subsystem
     * @return Pointer to physics engine interface, or nullptr
     */
    virtual IPhysicsEngine* get_physics_engine() const = 0;
    
    /**
     * @brief Get resource manager subsystem
     * @return Pointer to resource manager interface, or nullptr
     */
    virtual IResourceManager* get_resource_manager() const = 0;
    
    /**
     * @brief Get logger subsystem
     * @return Pointer to logger interface, or nullptr
     */
    virtual ILogger* get_logger() const = 0;
    
    /**
     * @brief Get platform subsystem
     * @return Pointer to platform interface, or nullptr
     */
    virtual IPlatform* get_platform() const = 0;
    
    /**
     * @brief Check if engine is initialized
     * @return True if initialized, false otherwise
     */
    virtual bool is_initialized() const = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IENGINE_HPP
