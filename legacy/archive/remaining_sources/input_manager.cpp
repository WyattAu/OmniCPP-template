#include "engine/input/InputManager.hpp"

#include <algorithm>
#include <utility>

namespace omnicpp::input {

bool InputManager::initialize() {
    return true;
}

void InputManager::shutdown() {
    m_key_states.clear();
    m_mouse_button_states.clear();
    m_callbacks.clear();
    m_mouse_delta_x = 0.0f;
    m_mouse_delta_y = 0.0f;
    m_scroll_x = 0.0f;
    m_scroll_y = 0.0f;
}

void InputManager::process_events() {
    m_mouse_delta_x = 0.0f;
    m_mouse_delta_y = 0.0f;
    m_scroll_x = 0.0f;
    m_scroll_y = 0.0f;
}

void InputManager::register_callback(InputCallback callback) {
    if (callback) {
        m_callbacks.push_back(std::move(callback));
    }
}

bool InputManager::is_key_pressed(KeyCode key) const {
    const auto it = m_key_states.find(static_cast<int>(key));
    return it != m_key_states.end() && it->second;
}

bool InputManager::is_mouse_button_pressed(MouseButton button) const {
    const auto it = m_mouse_button_states.find(static_cast<int>(button));
    return it != m_mouse_button_states.end() && it->second;
}

void InputManager::get_mouse_position(float& x, float& y) const {
    x = m_mouse_x;
    y = m_mouse_y;
}

void InputManager::get_mouse_delta(float& x, float& y) const {
    x = m_mouse_delta_x;
    y = m_mouse_delta_y;
}

void InputManager::get_scroll_delta(float& x, float& y) const {
    x = m_scroll_x;
    y = m_scroll_y;
}

void InputManager::dispatch_event(const InputEvent& event) {
    for (const auto& callback : m_callbacks) {
        callback(event);
    }
}

} // namespace omnicpp::input
