/**
 * @file test_input_manager.cpp
 * @brief Unit tests for InputManager
 * @version 1.0.0
 */

#include <gtest/gtest.h>
#include "engine/input/InputManager.hpp"

namespace omnicpp {
namespace test {

using input::InputManager;
using input::KeyCode;
using input::MouseButton;
using input::InputEvent;
using input::InputCallback;

class InputManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        input_manager = std::make_unique<InputManager>();
    }

    void TearDown() override {
        if (input_manager) {
            input_manager->shutdown();
        }
    }

    std::unique_ptr<InputManager> input_manager;
};

TEST_F(InputManagerTest, DefaultInitialization) {
    ASSERT_TRUE(input_manager->initialize());
}

TEST_F(InputManagerTest, MultipleInitialization) {
    ASSERT_TRUE(input_manager->initialize());
    input_manager->shutdown();

    // Re-initialize should work
    ASSERT_TRUE(input_manager->initialize());
    input_manager->shutdown();
}

TEST_F(InputManagerTest, ShutdownWithoutInitialize) {
    // Should not crash
    input_manager->shutdown();
}

TEST_F(InputManagerTest, ProcessEventsWithoutInitialize) {
    // Should not crash
    input_manager->process_events();
}

TEST_F(InputManagerTest, ProcessEventsAfterInitialize) {
    ASSERT_TRUE(input_manager->initialize());
    
    // Should not crash
    input_manager->process_events();
}

TEST_F(InputManagerTest, IsKeyPressed) {
    ASSERT_TRUE(input_manager->initialize());

    // Test key press check (should return false for unpressed keys)
    bool pressed = input_manager->is_key_pressed(KeyCode::A);
    // We don't assert the value as it depends on the actual input state
    (void)pressed;
}

TEST_F(InputManagerTest, IsMouseButtonPressed) {
    ASSERT_TRUE(input_manager->initialize());

    // Test mouse button press check
    bool pressed = input_manager->is_mouse_button_pressed(MouseButton::LEFT);
    // We don't assert the value as it depends on the actual input state
    (void)pressed;
}

TEST_F(InputManagerTest, GetMousePosition) {
    ASSERT_TRUE(input_manager->initialize());

    float x, y;
    input_manager->get_mouse_position(x, y);
    // We don't assert the value as it depends on the actual input state
    (void)x;
    (void)y;
}

TEST_F(InputManagerTest, GetMouseDelta) {
    ASSERT_TRUE(input_manager->initialize());

    float x, y;
    input_manager->get_mouse_delta(x, y);
    // We don't assert the value as it depends on the actual input state
    (void)x;
    (void)y;
}

TEST_F(InputManagerTest, GetScrollDelta) {
    ASSERT_TRUE(input_manager->initialize());

    float x, y;
    input_manager->get_scroll_delta(x, y);
    // We don't assert the value as it depends on the actual input state
    (void)x;
    (void)y;
}

TEST_F(InputManagerTest, RegisterCallback) {
    ASSERT_TRUE(input_manager->initialize());

    // Should not crash
    InputCallback callback = [](const InputEvent& event) {
        (void)event;
    };
    input_manager->register_callback(callback);
}

TEST_F(InputManagerTest, MultipleCallbacks) {
    ASSERT_TRUE(input_manager->initialize());

    InputCallback callback1 = [](const InputEvent& event) {
        (void)event;
    };
    InputCallback callback2 = [](const InputEvent& event) {
        (void)event;
    };
    
    input_manager->register_callback(callback1);
    input_manager->register_callback(callback2);
}

} // namespace test
} // namespace omnicpp
