/**
 * @file input_manager.hpp
 * @brief Input management interface
 */

#pragma once

#include <cstdint>
#include <memory>

namespace OmniCpp::Engine::Input {

  /**
   * @brief Key code enumeration
   */
  enum class KeyCode : uint32_t {
    Unknown = 0,
    Space,
    Apostrophe,
    Comma,
    Minus,
    Period,
    Slash,
    Key0,
    Key1,
    Key2,
    Key3,
    Key4,
    Key5,
    Key6,
    Key7,
    Key8,
    Key9,
    Semicolon,
    Equal,
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    X,
    Y,
    Z,
    LeftBracket,
    Backslash,
    RightBracket,
    GraveAccent,
    Escape,
    Enter,
    Tab,
    Backspace,
    Insert,
    Delete,
    Right,
    Left,
    Down,
    Up,
    PageUp,
    PageDown,
    F1,
    F2,
    F3,
    F4,
    F5,
    F6,
    F7,
    F8,
    F9,
    F10,
    F11,
    F12,
    LeftShift,
    LeftControl,
    LeftAlt,
    LeftSuper,
    RightShift,
    RightControl,
    RightAlt,
    RightSuper,
    Menu,
    KP0,
    KP1,
    KP2,
    KP3,
    KP4,
    KP5,
    KP6,
    KP7,
    KP8,
    KP9,
    KPDecimal,
    KPDivide,
    KPMultiply,
    KPSubtract,
    KPAdd,
    KPEnter,
    KPEqual,
    LeftBracket,
    RightBracket
  };

  /**
   * @brief Mouse button enumeration
   */
  enum class MouseButton : uint32_t {
    Left = 0,
    Right,
    Middle,
    Button4,
    Button5,
    Button6,
    Button7,
    Button8
  };

  /**
   * @brief Input manager class
   */
  class InputManager {
  public:
    InputManager ();
    ~InputManager ();

    InputManager (const InputManager&) = delete;
    InputManager& operator= (const InputManager&) = delete;

    InputManager (InputManager&&) noexcept;
    InputManager& operator= (InputManager&&) noexcept;

    bool initialize ();
    void shutdown ();
    void update ();

    bool is_key_pressed (KeyCode key) const;
    bool is_mouse_button_pressed (MouseButton button) const;

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Input
