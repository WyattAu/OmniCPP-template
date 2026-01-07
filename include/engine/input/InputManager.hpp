/**
 * @file InputManager.hpp
 * @brief Input manager for handling user input
 * @version 1.0.0
 */

#pragma once

#include <cstdint>
#include <functional>
#include <unordered_map>
#include <vector>

namespace omnicpp {
namespace input {

/**
 * @brief Key code enumeration
 */
enum class KeyCode {
    UNKNOWN = 0,
    SPACE = 32,
    APOSTROPHE = 39,
    COMMA = 44,
    MINUS = 45,
    PERIOD = 46,
    SLASH = 47,
    KEY_0 = 48,
    KEY_1 = 49,
    KEY_2 = 50,
    KEY_3 = 51,
    KEY_4 = 52,
    KEY_5 = 53,
    KEY_6 = 54,
    KEY_7 = 55,
    KEY_8 = 56,
    KEY_9 = 57,
    SEMICOLON = 59,
    EQUAL = 61,
    A = 65,
    B = 66,
    C = 67,
    D = 68,
    E = 69,
    F = 70,
    G = 71,
    H = 72,
    I = 73,
    J = 74,
    K = 75,
    L = 76,
    M = 77,
    N = 78,
    O = 79,
    P = 80,
    Q = 81,
    R = 82,
    S = 83,
    T = 84,
    U = 85,
    V = 86,
    W = 87,
    X = 88,
    Y = 89,
    Z = 90,
    LEFT_BRACKET = 91,
    BACKSLASH = 92,
    RIGHT_BRACKET = 93,
    GRAVE_ACCENT = 96,
    WORLD_1 = 161,
    WORLD_2 = 162,
    ESCAPE = 256,
    ENTER = 257,
    TAB = 258,
    BACKSPACE = 259,
    INSERT = 260,
    DELETE = 261,
    RIGHT = 262,
    LEFT = 263,
    DOWN = 264,
    UP = 265,
    PAGE_UP = 266,
    PAGE_DOWN = 267,
    HOME = 268,
    END = 269,
    CAPS_LOCK = 280,
    SCROLL_LOCK = 281,
    NUM_LOCK = 282,
    PRINT_SCREEN = 283,
    PAUSE = 284,
    F1 = 290,
    F2 = 291,
    F3 = 292,
    F4 = 293,
    F5 = 294,
    F6 = 295,
    F7 = 296,
    F8 = 297,
    F9 = 298,
    F10 = 299,
    F11 = 300,
    F12 = 301,
    F13 = 302,
    F14 = 303,
    F15 = 304,
    F16 = 305,
    F17 = 306,
    F18 = 307,
    F19 = 308,
    F20 = 309,
    F21 = 310,
    F22 = 311,
    F23 = 312,
    F24 = 313,
    F25 = 314,
    KP_0 = 320,
    KP_1 = 321,
    KP_2 = 322,
    KP_3 = 323,
    KP_4 = 324,
    KP_5 = 325,
    KP_6 = 326,
    KP_7 = 327,
    KP_8 = 328,
    KP_9 = 329,
    KP_DECIMAL = 330,
    KP_DIVIDE = 331,
    KP_MULTIPLY = 332,
    KP_SUBTRACT = 333,
    KP_ADD = 334,
    KP_ENTER = 335,
    KP_EQUAL = 336,
    LEFT_SHIFT = 340,
    LEFT_CONTROL = 341,
    LEFT_ALT = 342,
    LEFT_SUPER = 343,
    RIGHT_SHIFT = 344,
    RIGHT_CONTROL = 345,
    RIGHT_ALT = 346,
    RIGHT_SUPER = 347,
    MENU = 348
};

/**
 * @brief Mouse button enumeration
 */
enum class MouseButton {
    LEFT = 0,
    RIGHT = 1,
    MIDDLE = 2
};

/**
 * @brief Action enumeration
 */
enum class Action {
    RELEASE = 0,
    PRESS = 1,
    REPEAT = 2
};

/**
 * @brief Input event types
 */
enum class EventType {
    KEY_PRESS,
    KEY_RELEASE,
    MOUSE_MOVE,
    MOUSE_BUTTON_PRESS,
    MOUSE_BUTTON_RELEASE,
    MOUSE_SCROLL
};

/**
 * @brief Input event structure
 */
struct InputEvent {
    EventType type;
    KeyCode key_code;
    MouseButton mouse_button;
    Action action;
    float mouse_x;
    float mouse_y;
    float scroll_x;
    float scroll_y;
};

/**
 * @brief Input callback function type
 */
using InputCallback = std::function<void(const InputEvent&)>;

/**
 * @brief Input manager for handling user input
 * 
 * Captures keyboard and mouse input and dispatches events.
 */
class InputManager {
public:
    /**
     * @brief Construct a new Input Manager object
     */
    InputManager() = default;

    /**
     * @brief Destroy the Input Manager object
     */
    ~InputManager() = default;

    // Disable copying
    InputManager(const InputManager&) = delete;
    InputManager& operator=(const InputManager&) = delete;

    // Enable moving
    InputManager(InputManager&&) noexcept = default;
    InputManager& operator=(InputManager&&) noexcept = default;

    /**
     * @brief Initialize input manager
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

    /**
     * @brief Shutdown input manager
     */
    void shutdown();

    /**
     * @brief Process input events
     */
    void process_events();

    /**
     * @brief Register input callback
     * @param callback The callback function
     */
    void register_callback(InputCallback callback);

    /**
     * @brief Check if a key is pressed
     * @param key The key code
     * @return true if pressed, false otherwise
     */
    bool is_key_pressed(KeyCode key) const;

    /**
     * @brief Check if a mouse button is pressed
     * @param button The mouse button
     * @return true if pressed, false otherwise
     */
    bool is_mouse_button_pressed(MouseButton button) const;

    /**
     * @brief Get mouse position
     * @param x Output X position
     * @param y Output Y position
     */
    void get_mouse_position(float& x, float& y) const;

    /**
     * @brief Get mouse delta (movement since last frame)
     * @param x Output X delta
     * @param y Output Y delta
     */
    void get_mouse_delta(float& x, float& y) const;

    /**
     * @brief Get scroll delta
     * @param x Output X scroll
     * @param y Output Y scroll
     */
    void get_scroll_delta(float& x, float& y) const;

private:
    /**
     * @brief Dispatch event to all callbacks
     * @param event The input event
     */
    void dispatch_event(const InputEvent& event);

private:
    std::vector<InputCallback> m_callbacks;
    std::unordered_map<int, bool> m_key_states;
    std::unordered_map<int, bool> m_mouse_button_states;
    float m_mouse_x = 0.0f;
    float m_mouse_y = 0.0f;
    float m_mouse_delta_x = 0.0f;
    float m_mouse_delta_y = 0.0f;
    float m_scroll_x = 0.0f;
    float m_scroll_y = 0.0f;
};

} // namespace input
} // namespace omnicpp
