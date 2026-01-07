/**
 * @file input_manager.cpp
 * @brief Input management implementation
 */

#include "engine/input/input_manager.hpp"
#include <array>
#include <mutex>

namespace OmniCpp::Engine::Input {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct InputManager::Impl {
    std::array<bool, 512> key_states{};
    std::array<bool, 8> mouse_button_states{};
    std::mutex mutex;
    bool initialized{ false };
  };

  InputManager::InputManager () : m_impl (std::make_unique<Impl> ()) {
    m_impl->key_states.fill (false);
    m_impl->mouse_button_states.fill (false);
  }

  InputManager::~InputManager () {
    shutdown ();
  }

  InputManager::InputManager (InputManager&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  InputManager& InputManager::operator= (InputManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool InputManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->key_states.fill (false);
    m_impl->mouse_button_states.fill (false);
    m_impl->initialized = true;

    return true;
  }

  void InputManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->key_states.fill (false);
    m_impl->mouse_button_states.fill (false);
    m_impl->initialized = false;
  }

  void InputManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update input state here
  }

  bool InputManager::is_key_pressed (KeyCode key) const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    size_t index = static_cast<size_t> (key);
    if (index >= m_impl->key_states.size ()) {
      return false;
    }
    return m_impl->key_states[index];
  }

  bool InputManager::is_mouse_button_pressed (MouseButton button) const {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    size_t index = static_cast<size_t> (button);
    if (index >= m_impl->mouse_button_states.size ()) {
      return false;
    }
    return m_impl->mouse_button_states[index];
  }

} // namespace OmniCpp::Engine::Input
