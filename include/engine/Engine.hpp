/**
 * @file Engine.hpp
 * @brief OmniCpp Engine API - Public interface for dynamic engine library
 * @version 1.0.0
 * 
 * This header defines the public API for the OmniCpp game engine library.
 * The library is designed to be dynamically loaded at runtime by game applications.
 * 
 * @copyright Copyright 2025 OmniCpp Project
 * @license Apache-2.0
 */

#ifndef OMNICPP_ENGINE_HPP
#define OMNICPP_ENGINE_HPP

#include <memory>
#include <string>
#include <cstdint>

// Platform detection
#ifdef _WIN32
    #define OMNICPP_WINDOWS
    #define OMNICPP_EXPORT __declspec(dllexport)
    #define OMNICPP_IMPORT __declspec(dllimport)
#else
    #define OMNICPP_LINUX
    #define OMNICPP_EXPORT __attribute__((visibility("default")))
    #define OMNICPP_IMPORT
#endif

// API versioning
#define OMNICPP_ENGINE_VERSION_MAJOR 1
#define OMNICPP_ENGINE_VERSION_MINOR 0
#define OMNICPP_ENGINE_VERSION_PATCH 0

// Forward declarations
namespace omnicpp {

// Engine configuration
struct EngineConfig {
    bool enable_vulkan;
    bool enable_audio;
    bool enable_physics;
    uint32_t max_frames_per_second;
    bool enable_validation_layers;
    bool enable_debug_renderer;
};

// Forward declare engine interface
class IRenderer;
class IInputManager;
class IAudioManager;
class IPhysicsEngine;
class IResourceManager;
class ILogger;

/**
 * @brief Create engine instance with specified configuration
 *
 * @param config Engine configuration
 * @return Pointer to engine instance, or nullptr on failure
 */
extern "C" OMNICPP_EXPORT IEngine* create_engine(const EngineConfig& config);

/**
 * @brief Destroy engine instance
 *
 * @param engine Pointer to engine instance
 */
extern "C" OMNICPP_EXPORT void destroy_engine(IEngine* engine);

/**
 * @brief Get renderer subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to renderer interface, or nullptr
 */
extern "C" OMNICPP_EXPORT IRenderer* get_renderer(IEngine* engine);

/**
 * @brief Get input manager subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to input manager interface, or nullptr
 */
extern "C" OMNICPP_EXPORT IInputManager* get_input_manager(IEngine* engine);

/**
 * @brief Get audio manager subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to audio manager interface, or nullptr
 */
extern "C" OMNICPP_EXPORT IAudioManager* get_audio_manager(IEngine* engine);

/**
 * @brief Get physics engine subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to physics engine interface, or nullptr
 */
extern "C" OMNICPP_EXPORT IPhysicsEngine* get_physics_engine(IEngine* engine);

/**
 * @brief Get resource manager subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to resource manager interface, or nullptr
 */
extern "C" OMNICPP_EXPORT IResourceManager* get_resource_manager(IEngine* engine);

/**
 * @brief Get logger subsystem
 *
 * @param engine Pointer to engine instance
 * @return Pointer to logger interface, or nullptr
 */
extern "C" OMNICPP_EXPORT ILogger* get_logger(IEngine* engine);

/**
 * @brief Update engine state
 *
 * @param engine Pointer to engine instance
 * @param delta_time Time since last frame in seconds
 */
extern "C" OMNICPP_EXPORT void engine_update(IEngine* engine, float delta_time);

/**
 * @brief Render frame
 *
 * @param engine Pointer to engine instance
 */
extern "C" OMNICPP_EXPORT void engine_render(IEngine* engine);

/**
 * @brief Get engine version string
 * 
 * @return Version string in format "MAJOR.MINOR.PATCH"
 */
extern "C" OMNICPP_EXPORT const char* engine_get_version();

} // namespace omnicpp

#endif // OMNICPP_ENGINE_HPP
