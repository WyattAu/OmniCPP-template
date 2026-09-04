/**
 * @file EngineStateMachine.hpp
 * @brief Typestate pattern for Engine using std::variant
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 3 - Control Flow & Fault Tolerance
 * - Objects with mutually exclusive states must use std::variant
 * - State transitions handled via std::visit with exhaustive pattern matching
 * - Compiler enforces all states are handled
 */

#pragma once

#include <variant>
#include <string>
#include <functional>
#include <chrono>
#include "engine/logging/spdlog_shim.hpp"
#include "engine/core/Expected.hpp"

namespace omnicpp {
namespace core {

// ============================================================================
// Engine States (Typestate Pattern)
// ============================================================================

/**
 * @brief Uninitialized state - engine has not been initialized
 */
struct StateUninitialized {
    std::string config_path;
    
    StateUninitialized() = default;
    explicit StateUninitialized(std::string path) : config_path(std::move(path)) {}
};

/**
 * @brief Initializing state - engine is currently initializing
 */
struct StateInitializing {
    std::string current_step;
    float progress{0.0f};
    std::chrono::steady_clock::time_point start_time;
    
    StateInitializing() : start_time(std::chrono::steady_clock::now()) {}
    explicit StateInitializing(std::string step) 
        : current_step(std::move(step)), start_time(std::chrono::steady_clock::now()) {}
};

/**
 * @brief Running state - engine is active and processing
 */
struct StateRunning {
    std::chrono::steady_clock::time_point start_time;
    uint64_t frame_count{0};
    float accumulated_time{0.0f};
    float average_fps{0.0f};
    
    StateRunning() : start_time(std::chrono::steady_clock::now()) {}
};

/**
 * @brief Paused state - engine is paused but can resume
 */
struct StatePaused {
    std::chrono::steady_clock::time_point pause_time;
    uint64_t frame_count_at_pause{0};
    std::string pause_reason;
    
    StatePaused() = default;
    explicit StatePaused(std::string reason) 
        : pause_time(std::chrono::steady_clock::now()), pause_reason(std::move(reason)) {}
};

/**
 * @brief Error state - engine encountered an error
 */
struct StateError {
    Error error;
    std::chrono::steady_clock::time_point error_time;
    bool recoverable{false};
    
    StateError() : error_time(std::chrono::steady_clock::now()) {}
    StateError(Error e, bool can_recover = false) 
        : error(std::move(e)), error_time(std::chrono::steady_clock::now()), recoverable(can_recover) {}
};

/**
 * @brief Shutting down state - engine is in shutdown process
 */
struct StateShuttingDown {
    std::string current_step;
    float progress{0.0f};
    bool force{false};
    
    StateShuttingDown() = default;
    explicit StateShuttingDown(bool force_shutdown) : force(force_shutdown) {}
};

/**
 * @brief Terminated state - engine has fully shut down
 */
struct StateTerminated {
    std::chrono::steady_clock::time_point termination_time;
    uint64_t total_frames{0};
    float total_runtime{0.0f};
    std::string termination_reason;
    
    StateTerminated() : termination_time(std::chrono::steady_clock::now()) {}
    explicit StateTerminated(std::string reason) 
        : termination_time(std::chrono::steady_clock::now()), termination_reason(std::move(reason)) {}
};

// ============================================================================
// Engine State Variant
// ============================================================================

/**
 * @brief All possible engine states as a variant
 * 
 * Using std::variant ensures:
 * 1. Only one state can be active at a time (mutually exclusive)
 * 2. All states must be handled in std::visit (exhaustive matching)
 * 3. State transitions are explicit and type-safe
 */
using EngineState = std::variant<
    StateUninitialized,
    StateInitializing,
    StateRunning,
    StatePaused,
    StateError,
    StateShuttingDown,
    StateTerminated
>;

// ============================================================================
// State Visitor Utilities
// ============================================================================

/**
 * @brief Helper to create overloaded lambda visitors
 * 
 * Usage:
 *   std::visit(overloaded{
 *       [](const StateRunning& s) { ... },
 *       [](const StatePaused& s) { ... },
 *       [](const auto& s) { ... }  // default
 *   }, state);
 */
template<class... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};

template<class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

// ============================================================================
// State Queries
// ============================================================================

/**
 * @brief Get the name of the current state
 */
[[nodiscard]] inline std::string state_name(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateUninitialized&) { return "Uninitialized"; },
        [](const StateInitializing&) { return "Initializing"; },
        [](const StateRunning&) { return "Running"; },
        [](const StatePaused&) { return "Paused"; },
        [](const StateError&) { return "Error"; },
        [](const StateShuttingDown&) { return "ShuttingDown"; },
        [](const StateTerminated&) { return "Terminated"; }
    }, state);
}

/**
 * @brief Check if engine is in an active (running) state
 */
[[nodiscard]] inline bool is_active(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateRunning&) { return true; },
        [](const StatePaused&) { return true; },  // Can resume
        [](const auto&) { return false; }
    }, state);
}

/**
 * @brief Check if engine is in a terminal state
 */
[[nodiscard]] inline bool is_terminal(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateTerminated&) { return true; },
        [](const StateError& e) { return !e.recoverable; },
        [](const auto&) { return false; }
    }, state);
}

/**
 * @brief Check if engine can be transitioned to running
 */
[[nodiscard]] inline bool can_run(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateUninitialized&) { return false; },  // Must initialize first
        [](const StateInitializing&) { return false; },   // Wait for completion
        [](const StatePaused&) { return true; },          // Can resume
        [](const StateError& e) { return e.recoverable; },// Can recover
        [](const auto&) { return false; }
    }, state);
}

/**
 * @brief Check if engine can be paused
 */
[[nodiscard]] inline bool can_pause(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateRunning&) { return true; },
        [](const auto&) { return false; }
    }, state);
}

/**
 * @brief Check if engine can be shut down
 */
[[nodiscard]] inline bool can_shutdown(const EngineState& state) noexcept {
    return std::visit(overloaded{
        [](const StateTerminated&) { return false; },     // Already terminated
        [](const auto&) { return true; }
    }, state);
}

// ============================================================================
// State Transitions
// ============================================================================

/**
 * @brief Result of a state transition attempt
 */
enum class TransitionResult {
    Success,
    InvalidTransition,
    AlreadyInState,
    PreconditionFailed,
    ErrorOccurred
};

/**
 * @brief Attempt to transition to initializing state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_initializing(EngineState&& current, std::string first_step = "") {
    return std::visit(overloaded{
        [&](const StateUninitialized&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Transitioning to Initializing");
            return {StateInitializing(std::move(first_step)), TransitionResult::Success};
        },
        [](const StateInitializing&) 
            -> std::pair<EngineState, TransitionResult> {
            return {StateInitializing{}, TransitionResult::AlreadyInState};
        },
        [](const StateTerminated&) 
            -> std::pair<EngineState, TransitionResult> {
            return {std::move(current), TransitionResult::InvalidTransition};
        },
        [&](const auto&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::warn("Engine: Cannot transition to Initializing from {}", state_name(current));
            return {std::move(current), TransitionResult::InvalidTransition};
        }
    }, current);
}

/**
 * @brief Attempt to transition to running state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_running(EngineState&& current) {
    return std::visit(overloaded{
        [&](StateInitializing&& s) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Transitioning to Running (initialization took {:.2f}s)",
                std::chrono::duration<float>(std::chrono::steady_clock::now() - s.start_time).count());
            return {StateRunning{}, TransitionResult::Success};
        },
        [&](StatePaused&& s) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Resuming from pause");
            StateRunning running;
            // Note: frame count resets on resume in this implementation
            return {running, TransitionResult::Success};
        },
        [&](StateError&& s) 
            -> std::pair<EngineState, TransitionResult> {
            if (s.recoverable) {
                spdlog::info("Engine: Recovering from error: {}", s.error.message);
                return {StateRunning{}, TransitionResult::Success};
            }
            spdlog::error("Engine: Cannot recover from error: {}", s.error.message);
            return {std::move(current), TransitionResult::PreconditionFailed};
        },
        [](const StateRunning&) 
            -> std::pair<EngineState, TransitionResult> {
            return {StateRunning{}, TransitionResult::AlreadyInState};
        },
        [&](const auto&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::warn("Engine: Cannot transition to Running from {}", state_name(current));
            return {std::move(current), TransitionResult::InvalidTransition};
        }
    }, std::move(current));
}

/**
 * @brief Attempt to transition to paused state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_paused(EngineState&& current, std::string reason = "") {
    return std::visit(overloaded{
        [&](StateRunning&& s) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Pausing - {}", reason.empty() ? "User requested" : reason);
            StatePaused paused(std::move(reason));
            paused.frame_count_at_pause = s.frame_count;
            return {paused, TransitionResult::Success};
        },
        [](const StatePaused&) 
            -> std::pair<EngineState, TransitionResult> {
            return {StatePaused{}, TransitionResult::AlreadyInState};
        },
        [&](const auto&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::warn("Engine: Cannot pause from {}", state_name(current));
            return {std::move(current), TransitionResult::InvalidTransition};
        }
    }, std::move(current));
}

/**
 * @brief Attempt to transition to error state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_error(EngineState&& current, Error error, bool recoverable = false) {
    spdlog::error("Engine: Entering error state - [{}]: {}", error.code, error.message);
    return {StateError(std::move(error), recoverable), TransitionResult::Success};
}

/**
 * @brief Attempt to transition to shutting down state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_shutting_down(EngineState&& current, bool force = false) {
    return std::visit(overloaded{
        [&](const StateTerminated&) 
            -> std::pair<EngineState, TransitionResult> {
            return {StateTerminated{}, TransitionResult::AlreadyInState};
        },
        [&](auto&&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Initiating shutdown (force={})", force);
            return {StateShuttingDown(force), TransitionResult::Success};
        }
    }, std::move(current));
}

/**
 * @brief Attempt to transition to terminated state
 */
inline std::pair<EngineState, TransitionResult> 
transition_to_terminated(EngineState&& current, std::string reason = "Normal shutdown") {
    return std::visit(overloaded{
        [&](StateShuttingDown&& s) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Terminated - {}", reason);
            StateTerminated terminated(std::move(reason));
            return {terminated, TransitionResult::Success};
        },
        [&](StateError&& s) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::info("Engine: Terminated due to unrecoverable error");
            StateTerminated terminated(s.error.message);
            return {terminated, TransitionResult::Success};
        },
        [&](const StateTerminated&) 
            -> std::pair<EngineState, TransitionResult> {
            return {StateTerminated{}, TransitionResult::AlreadyInState};
        },
        [&](const auto&) 
            -> std::pair<EngineState, TransitionResult> {
            spdlog::warn("Engine: Must go through ShuttingDown before Terminated");
            return {std::move(current), TransitionResult::InvalidTransition};
        }
    }, std::move(current));
}

// ============================================================================
// State Update Functions
// ============================================================================

/**
 * @brief Update the running state with frame information
 */
inline EngineState update_running_frame(EngineState&& state, float delta_time) {
    return std::visit(overloaded{
        [&](StateRunning&& s) -> EngineState {
            s.frame_count++;
            s.accumulated_time += delta_time;
            
            // Calculate rolling average FPS
            if (s.accumulated_time > 0.0f) {
                s.average_fps = static_cast<float>(s.frame_count) / s.accumulated_time;
            }
            return s;
        },
        [](auto&& s) -> EngineState { return std::move(s); }
    }, std::move(state));
}

/**
 * @brief Update the initializing state with progress
 */
inline EngineState update_initializing_progress(EngineState&& state, std::string step, float progress) {
    return std::visit(overloaded{
        [&](StateInitializing&& s) -> EngineState {
            s.current_step = std::move(step);
            s.progress = progress;
            return s;
        },
        [](auto&& s) -> EngineState { return std::move(s); }
    }, std::move(state));
}

/**
 * @brief Update the shutting down state with progress
 */
inline EngineState update_shutdown_progress(EngineState&& state, std::string step, float progress) {
    return std::visit(overloaded{
        [&](StateShuttingDown&& s) -> EngineState {
            s.current_step = std::move(step);
            s.progress = progress;
            return s;
        },
        [](auto&& s) -> EngineState { return std::move(s); }
    }, std::move(state));
}

} // namespace core
} // namespace omnicpp

// ============================================================================
// fmt Formatters for States
// ============================================================================
template<>
struct fmt::formatter<omnicpp::core::EngineState> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::core::EngineState& state, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "{}", omnicpp::core::state_name(state));
    }
};
