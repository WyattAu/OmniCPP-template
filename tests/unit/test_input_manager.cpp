/**
 * @file test_input_manager.cpp
 * @brief Unit tests for InputManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/input/InputManager.hpp"

namespace omnicpp {
namespace test {

class InputManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        input_manager_ = std::make_unique<InputManager>();
    }

    void TearDown() override {
        if (input_manager_) {
            input_manager_->shutdown();
        }
    }

    std::unique_ptr<InputManager> input_manager_;
};

TEST_F(InputManagerTest, DefaultInitialization) {
    ASSERT_TRUE(input_manager_->initialize());
}

TEST_F(InputManagerTest, MultipleInitialization) {
    ASSERT_TRUE(input_manager_->initialize());
    input_manager_->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(input_manager_->initialize());
    input_manager_->shutdown();
}

TEST_F(InputManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    input_manager_->shutdown();
}

TEST_F(InputManagerTest, UpdateWithoutInitialize) {
    // Should not crash
    input_manager_->update();
}

TEST_F(InputManagerTest, IsKeyPressed) {
    ASSERT_TRUE(input_manager_->initialize());

    // Test key press check (should return false for unpressed keys)
    bool pressed = input_manager_->is_key_pressed(KeyCode::KEY_A);
    // We don't assert the value as it depends on the actual input state
}

TEST_F(InputManagerTest, IsMouseButtonPressed) {
    ASSERT_TRUE(input_manager_->initialize());

    // Test mouse button press check
    bool pressed = input_manager_->is_mouse_button_pressed(MouseButton::LEFT);
    // We don't assert the value as it depends on the actual input state
}

TEST_F(InputManagerTest, GetMousePosition) {
    ASSERT_TRUE(input_manager_->initialize());

    auto position = input_manager_->get_mouse_position();
    // We don't assert the value as it depends on the actual input state
}

TEST_F(InputManagerTest, GetMouseDelta) {
    ASSERT_TRUE(input_manager_->initialize());

    auto delta = input_manager_->get_mouse_delta();
    // We don't assert the value as it depends on the actual input state
}

TEST_F(InputManagerTest, GetMouseWheel) {
    ASSERT_TRUE(input_manager_->initialize());

    auto wheel = input_manager_->get_mouse_wheel();
    // We don't assert the value as it depends on the actual input state
}

TEST_F(InputManagerTest, SetMousePosition) {
    ASSERT_TRUE(input_manager_->initialize());

    // Should not crash
    input_manager_->set_mouse_position(100, 100);
}

TEST_F(InputManagerTest, SetMouseCursorVisible) {
    ASSERT_TRUE(input_manager_->initialize());

    // Should not crash
    input_manager_->set_mouse_cursor_visible(true);
    input_manager_->set_mouse_cursor_visible(false);
    input_manager_->set_mouse_cursor_visible(true);
}

TEST_F(InputManagerTest, SetMouseCursorLocked) {
    ASSERT_TRUE(input_manager_->initialize());

    // Should not crash
    input_manager_->set_mouse_cursor_locked(true);
    input_manager_->set_mouse_cursor_locked(false);
}

TEST_F(InputManagerTest, GetGamepadCount) {
    ASSERT_TRUE(input_manager_->initialize());

    auto count = input_manager_->get_gamepad_count();
    ASSERT_GE(count, 0);
}

TEST_F(InputManagerTest, IsGamepadConnected) {
    ASSERT_TRUE(input_manager_->initialize());

    // Test gamepad connection check
    bool connected = input_manager_->is_gamepad_connected(0);
    // We don't assert the value as it depends on the actual hardware
}

TEST_F(InputManagerTest, IsGamepadButtonPressed) {
    ASSERT_TRUE(input_manager_->initialize());

    // Test gamepad button press check
    bool pressed = input_manager_->is_gamepad_button_pressed(0, GamepadButton::A);
    // We don't assert the value as it depends on the actual hardware
}

TEST_F(InputManagerTest, GetGamepadAxis) {
    ASSERT_TRUE(input_manager_->initialize());

    // Test gamepad axis value
    float value = input_manager_->get_gamepad_axis(0, GamepadAxis::LEFT_STICK_X);
    // We don't assert the value as it depends on the actual hardware
}

TEST_F(InputManagerTest, SetGamepadVibration) {
    ASSERT_TRUE(input_manager_->initialize());

    // Should not crash
    input_manager_->set_gamepad_vibration(0, 0.5f, 0.5f);
}

} // namespace test
} // namespace omnicpp
