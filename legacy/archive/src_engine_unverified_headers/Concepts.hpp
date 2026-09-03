/**
 * @file Concepts.hpp
 * @brief C++20 concepts for compile-time interface constraints
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 3 - Compiler Rigor & Type Modeling
 * - SFINAE and unconstrained templates are prohibited
 * - All template parameters must be constrained using C++20 concepts
 * - Provides instantaneous, readable compiler errors
 */

#pragma once

#include <concepts>
#include <type_traits>
#include <memory>
#include <string>
#include <functional>

namespace omnicpp {
namespace core {

// ============================================================================
// Fundamental Concepts
// ============================================================================

/**
 * @brief Concept for types that can be hashed
 */
template<typename T>
concept Hashable = requires(T a) {
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

/**
 * @brief Concept for types that can be compared for equality
 */
template<typename T>
concept EqualityComparable = requires(T a, T b) {
    { a == b } -> std::convertible_to<bool>;
    { a != b } -> std::convertible_to<bool>;
};

/**
 * @brief Concept for types that can be ordered
 */
template<typename T>
concept Ordered = EqualityComparable<T> && requires(T a, T b) {
    { a < b } -> std::convertible_to<bool>;
    { a > b } -> std::convertible_to<bool>;
    { a <= b } -> std::convertible_to<bool>;
    { a >= b } -> std::convertible_to<bool>;
};

/**
 * @brief Concept for types that can be serialized to string
 */
template<typename T>
concept StringConvertible = requires(T a) {
    { std::to_string(a) } -> std::convertible_to<std::string>;
};

/**
 * @brief Concept for types that can be formatted (fmtlib)
 */
template<typename T>
concept Formattable = requires(T a) {
    { fmt::format("{}", a) } -> std::convertible_to<std::string>;
};

// ============================================================================
// ECS Concepts
// ============================================================================

/**
 * @brief Base concept for all components
 * 
 * Components are data-only types that can be attached to entities.
 */
template<typename T>
concept Component = std::is_trivially_copyable_v<T> &&
                    std::is_default_constructible_v<T> &&
                    !std::is_pointer_v<T>;

/**
 * @brief Concept for components that can be serialized
 */
template<typename T>
concept SerializableComponent = Component<T> && requires(T a) {
    { a.serialize() } -> std::convertible_to<std::string>;
    { T::deserialize(std::declval<std::string>()) } -> std::same_as<T>;
};

/**
 * @brief Base concept for all systems
 * 
 * Systems are classes that process entities with specific components.
 */
template<typename T>
concept System = requires(T system) {
    { system.update(std::declval<float>()) } -> std::same_as<void>;
    typename T::ComponentTypes;
    requires std::tuple<typename T::ComponentTypes>;
};

/**
 * @brief Concept for systems that can be configured
 */
template<typename T>
concept ConfigurableSystem = System<T> && requires(T system) {
    { system.configure(std::declval<typename T::Config>()) } -> std::same_as<void>;
};

/**
 * @brief Concept for entity types
 */
template<typename T>
concept Entity = requires(T entity) {
    { entity.get_id() } -> std::integral;
    { entity.is_active() } -> std::convertible_to<bool>;
    { entity.template has_component<int>() } -> std::convertible_to<bool>;
};

/**
 * @brief Concept for entity manager types
 */
template<typename T>
concept EntityManager = requires(T manager) {
    typename T::EntityType;
    requires Entity<typename T::EntityType>;
    { manager.create_entity() } -> std::same_as<typename T::EntityType*>;
    { manager.destroy_entity(std::declval<typename T::EntityType*>()) } -> std::same_as<void>;
};

// ============================================================================
// Resource Concepts
// ============================================================================

/**
 * @brief Concept for resource types
 * 
 * Resources are singleton-like data containers managed by the engine.
 */
template<typename T>
concept Resource = std::is_default_constructible_v<T> &&
                   std::is_move_constructible_v<T> &&
                   !std::is_pointer_v<T>;

/**
 * @brief Concept for loadable resources
 */
template<typename T>
concept LoadableResource = Resource<T> && requires(T resource) {
    { resource.load(std::declval<std::string>()) } -> std::same_as<bool>;
    { resource.is_loaded() } -> std::convertible_to<bool>;
    { resource.unload() } -> std::same_as<void>;
};

/**
 * @brief Concept for async loadable resources
 */
template<typename T>
concept AsyncLoadableResource = LoadableResource<T> && requires(T resource) {
    { resource.load_async(std::declval<std::string>()) } -> std::same_as<std::future<bool>>;
};

/**
 * @brief Concept for resource manager types
 */
template<typename T>
concept ResourceManager = requires(T manager) {
    { manager.initialize() } -> std::same_as<bool>;
    { manager.shutdown() } -> std::same_as<void>;
};

// ============================================================================
// Engine Subsystem Concepts
// ============================================================================

/**
 * @brief Concept for engine subsystems
 */
template<typename T>
concept Subsystem = requires(T subsystem) {
    { subsystem.initialize() } -> std::same_as<bool>;
    { subsystem.shutdown() } -> std::same_as<void>;
    { subsystem.update(std::declval<float>()) } -> std::same_as<void>;
};

/**
 * @brief Concept for renderers
 */
template<typename T>
concept Renderer = Subsystem<T> && requires(T renderer) {
    { renderer.begin_frame() } -> std::same_as<void>;
    { renderer.end_frame() } -> std::same_as<void>;
    { renderer.clear() } -> std::same_as<void>;
    { renderer.present() } -> std::same_as<void>;
};

/**
 * @brief Concept for input managers
 */
template<typename T>
concept InputManager = Subsystem<T> && requires(T manager) {
    { manager.is_key_pressed(std::declval<int>()) } -> std::convertible_to<bool>;
    { manager.get_mouse_position() } -> std::same_as<std::pair<float, float>>;
};

/**
 * @brief Concept for audio managers
 */
template<typename T>
concept AudioManager = Subsystem<T> && requires(T manager) {
    { manager.play_sound(std::declval<std::string>()) } -> std::same_as<void>;
    { manager.stop_sound(std::declval<std::string>()) } -> std::same_as<void>;
    { manager.set_volume(std::declval<float>()) } -> std::same_as<void>;
};

/**
 * @brief Concept for physics engines
 */
template<typename T>
concept PhysicsEngine = Subsystem<T> && requires(T engine) {
    { engine.set_gravity(std::declval<float>(), std::declval<float>(), std::declval<float>()) } -> std::same_as<void>;
    { engine.raycast(std::declval<float>(), std::declval<float>(), std::declval<float>(),
                     std::declval<float>(), std::declval<float>(), std::declval<float>()) } -> std::convertible_to<bool>;
};

// ============================================================================
// Logging Concepts
// ============================================================================

/**
 * @brief Concept for loggers
 */
template<typename T>
concept Logger = requires(T logger) {
    { logger.log(std::declval<int>(), std::declval<const char*>()) } -> std::same_as<void>;
    { logger.set_log_level(std::declval<int>()) } -> std::same_as<void>;
    { logger.flush() } -> std::same_as<void>;
};

/**
 * @brief Concept for async loggers
 */
template<typename T>
concept AsyncLogger = Logger<T> && requires(T logger) {
    { logger.log_async(std::declval<int>(), std::declval<const char*>()) } -> std::same_as<void>;
};

// ============================================================================
// Event Concepts
// ============================================================================

/**
 * @brief Concept for event types
 */
template<typename T>
concept Event = std::is_trivially_copyable_v<T> &&
                std::is_default_constructible_v<T>;

/**
 * @brief Concept for event handlers
 */
template<typename T, typename E>
concept EventHandler = requires(T handler, E event) {
    { handler.handle(event) } -> std::same_as<void>;
};

/**
 * @brief Concept for event managers
 */
template<typename T>
concept EventManager = Subsystem<T> && requires(T manager) {
    { manager.publish(std::declval<int>(), std::declval<void*>()) } -> std::same_as<void>;
};

// ============================================================================
// Scene Concepts
// ============================================================================

/**
 * @brief Concept for scene nodes
 */
template<typename T>
concept SceneNode = requires(T node) {
    { node.get_parent() } -> std::convertible_to<T*>;
    { node.add_child(std::declval<std::unique_ptr<T>>()) } -> std::same_as<void>;
    { node.get_position() } -> std::same_as<std::tuple<float, float, float>>;
    { node.set_position(std::declval<float>(), std::declval<float>(), std::declval<float>()) } -> std::same_as<void>;
};

/**
 * @brief Concept for scenes
 */
template<typename T>
concept Scene = requires(T scene) {
    { scene.initialize() } -> std::same_as<bool>;
    { scene.update(std::declval<float>()) } -> std::same_as<void>;
    { scene.render() } -> std::same_as<void>;
    { scene.shutdown() } -> std::same_as<void>;
};

/**
 * @brief Concept for scene managers
 */
template<typename T>
concept SceneManager = Subsystem<T> && requires(T manager) {
    { manager.load_scene(std::declval<std::string>()) } -> std::same_as<bool>;
    { manager.unload_scene() } -> std::same_as<void>;
    { manager.get_current_scene() } -> std::convertible_to<typename T::SceneType*>;
};

// ============================================================================
// Network Concepts
// ============================================================================

/**
 * @brief Concept for network managers
 */
template<typename T>
concept NetworkManager = Subsystem<T> && requires(T manager) {
    { manager.connect(std::declval<std::string>(), std::declval<uint16_t>()) } -> std::same_as<bool>;
    { manager.disconnect() } -> std::same_as<void>;
    { manager.send(std::declval<const void*>(), std::declval<size_t>()) } -> std::same_as<bool>;
    { manager.is_connected() } -> std::convertible_to<bool>;
};

// ============================================================================
// Memory Concepts
// ============================================================================

/**
 * @brief Concept for allocators
 */
template<typename T>
concept Allocator = requires(T allocator) {
    { allocator.allocate(std::declval<size_t>()) } -> std::same_as<void*>;
    { allocator.deallocate(std::declval<void*>(), std::declval<size_t>()) } -> std::same_as<void>;
};

/**
 * @brief Concept for memory managers
 */
template<typename T>
concept MemoryManager = Subsystem<T> && requires(T manager) {
    { manager.get_stats() } -> std::same_as<typename T::Stats>;
    { manager.has_leaks() } -> std::convertible_to<bool>;
};

// ============================================================================
// Platform Concepts
// ============================================================================

/**
 * @brief Concept for platform abstractions
 */
template<typename T>
concept Platform = requires(T platform) {
    { platform.get_name() } -> std::convertible_to<std::string>;
    { platform.is_mobile() } -> std::convertible_to<bool>;
    { platform.is_desktop() } -> std::convertible_to<bool>;
};

// ============================================================================
// Engine Concepts
// ============================================================================

/**
 * @brief Concept for the main engine class
 */
template<typename T>
concept Engine = requires(T engine) {
    { engine.initialize(std::declval<typename T::Config>()) } -> std::same_as<bool>;
    { engine.shutdown() } -> std::same_as<void>;
    { engine.update(std::declval<float>()) } -> std::same_as<void>;
    { engine.render() } -> std::same_as<void>;
    { engine.is_running() } -> std::convertible_to<bool>;
    { engine.get_renderer() } -> std::convertible_to<typename T::RendererType*>;
    { engine.get_input_manager() } -> std::convertible_to<typename T::InputManagerType*>;
};

// ============================================================================
// Utility Concepts
// ============================================================================

/**
 * @brief Concept for callable types (functions, lambdas, etc.)
 */
template<typename T, typename... Args>
concept Callable = requires(T f, Args... args) {
    { f(args...) };
};

/**
 * @brief Concept for predicate functions
 */
template<typename T, typename Arg>
concept Predicate = requires(T pred, Arg arg) {
    { pred(arg) } -> std::convertible_to<bool>;
};

/**
 * @brief Concept for factory functions
 */
template<typename T, typename Product>
concept Factory = requires(T factory) {
    { factory.create() } -> std::same_as<std::unique_ptr<Product>>;
};

/**
 * @brief Concept for builder pattern
 */
template<typename T>
concept Builder = requires(T builder) {
    { builder.build() };
    { builder.reset() } -> std::same_as<T&>;
};

} // namespace core
} // namespace omnicpp
