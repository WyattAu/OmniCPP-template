/**
 * @file InputManager.cpp
 * @brief Stub implementation of input manager subsystem
 * @version 1.0.0
 */

#include "engine/IInputManager.hpp"
#include <spdlog/spdlog.h>

namespace omnicpp {

class InputManagerStub : public IInputManager {
public:
    InputManagerStub() = default;
    ~InputManagerStub() override = default;

    bool initialize() override {
        spdlog::info("Input manager initialized");
        return true;
    }

    void shutdown() override {
        spdlog::info("Input manager shutdown");
    }

    void process_events([[maybe_unused]] float delta_time) noexcept override {
    }

    const InputState& get_state() const noexcept override {
        return m_state;
    }

    bool is_key_pressed(uint32_t key_code) const noexcept override {
        return false;
    }

    bool is_mouse_button_pressed(uint32_t button) const noexcept override {
        return false;
    }

    float get_mouse_x() const noexcept override {
        return 0.0f;
    }

    float get_mouse_y() const noexcept override {
        return 0.0f;
    }

    float get_mouse_scroll_x() const noexcept override {
        return 0.0f;
    }

    float get_mouse_scroll_y() const noexcept override {
        return 0.0f;
    }

private:
    InputState m_state{};
};

} // namespace omnicpp
