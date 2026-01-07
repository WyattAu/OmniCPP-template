/**
 * @file InputManager.cpp
 * @brief Stub implementation of input manager subsystem
 * @version 1.0.0
 */

#include "engine/IInputManager.hpp"

namespace omnicpp {

class InputManagerStub : public IInputManager {
public:
    InputManagerStub() = default;
    ~InputManagerStub() override = default;

    bool initialize() override {
        return true;
    }

    void shutdown() override {
    }

    void process_events(float delta_time) override {
    }

    const InputState& get_state() const override {
        return m_state;
    }

    bool is_key_pressed(uint32_t key_code) const override {
        return false;
    }

    bool is_mouse_button_pressed(uint32_t button) const override {
        return false;
    }

    float get_mouse_x() const override {
        return 0.0f;
    }

    float get_mouse_y() const override {
        return 0.0f;
    }

    float get_mouse_scroll_x() const override {
        return 0.0f;
    }

    float get_mouse_scroll_y() const override {
        return 0.0f;
    }

private:
    InputState m_state{};
};

} // namespace omnicpp
