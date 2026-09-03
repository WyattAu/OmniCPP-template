/**
 * @file IInputManager.hpp
 * @brief Input manager subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for input handling.
 */

#ifndef OMNICPP_IINPUT_MANAGER_HPP
#define OMNICPP_IINPUT_MANAGER_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Input event types
 */
enum class InputEventType {
    KEY_DOWN = 0,
    KEY_UP = 1,
    KEY_LEFT = 2,
    KEY_RIGHT = 3,
    KEY_W = 4,
    KEY_S = 5,
    KEY_A = 6,
    KEY_D = 7,
    KEY_ESCAPE = 8,
    KEY_F1 = 9,
    KEY_F2 = 10,
    KEY_F3 = 11,
    KEY_F4 = 12,
    KEY_F5 = 13,
    KEY_F6 = 14,
    KEY_F7 = 15,
    KEY_F8 = 16,
    KEY_F9 = 17,
    KEY_F10 = 18,
    KEY_F11 = 19,
    KEY_F12 = 20,
    MOUSE_BUTTON_LEFT = 21,
    MOUSE_BUTTON_MIDDLE = 22,
    MOUSE_BUTTON_RIGHT = 23,
    MOUSE_SCROLL_UP = 24,
    MOUSE_SCROLL_DOWN = 25,
    MOUSE_X = 26,
    MOUSE_Y = 27,
    UNKNOWN = 28
};

/**
 * @brief Input event structure
 */
struct InputEvent {
    InputEventType type;
    uint32_t key_code;
    float x;
    float y;
    float scroll_x;
    float scroll_y;
    bool pressed;
};

/**
 * @brief Input state structure
 */
struct InputState {
    bool keys[256];
    bool mouse_buttons[8];
    float mouse_x;
    float mouse_y;
    float mouse_scroll_x;
    float mouse_scroll_y;
};

/**
 * @brief Input manager interface
 */
class IInputManager {
public:
    virtual ~IInputManager() = default;
    
    /**
     * @brief Initialize input manager
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown input manager
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Process input events
     * 
     * @param delta_time Time since last frame in seconds
     */
    virtual void process_events(float delta_time) = 0;
    
    /**
     * @brief Get current input state
     * 
     * @return Current input state
     */
    virtual const InputState& get_state() const = 0;
    
    /**
     * @brief Check if a key is pressed
     * 
     * @param key_code Key code to check
     * @return True if pressed, false otherwise
     */
    virtual bool is_key_pressed(uint32_t key_code) const = 0;
    
    /**
     * @brief Check if a mouse button is pressed
     * 
     * @param button Button code to check
     * @return True if pressed, false otherwise
     */
    virtual bool is_mouse_button_pressed(uint32_t button) const = 0;
    
    /**
     * @brief Get mouse position
     * 
     * @return X coordinate
     */
    virtual float get_mouse_x() const = 0;
    
    /**
     * @brief Get mouse position
     * 
     * @return Y coordinate
     */
    virtual float get_mouse_y() const = 0;
    
    /**
     * @brief Get mouse scroll position
     * 
     * @return X scroll coordinate
     */
    virtual float get_mouse_scroll_x() const = 0;
    
    /**
     * @brief Get mouse scroll position
     * 
     * @return Y scroll coordinate
     */
    virtual float get_mouse_scroll_y() const = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IINPUT_MANAGER_HPP
