/**
 * @file event_manager.hpp
 * @brief Event management interface
 */

#pragma once

#include <cstdint>
#include <functional>
#include <memory>
#include <string>
#include <vector>

namespace OmniCpp::Engine::Events {

  /**
   * @brief Event type enumeration
   */
  enum class EventType : uint32_t {
    WindowClose = 0,
    WindowResize,
    KeyPressed,
    KeyReleased,
    MouseMoved,
    MouseButtonPressed,
    MouseButtonReleased,
    MouseScrolled,
    GamepadConnected,
    GamepadDisconnected EngineInitialized,
    EngineShutdown
  };

  /**
   * @brief Base event class
   */
  class Event {
  public:
    explicit Event (EventType type);
    virtual ~Event () = default;

    [[nodiscard]] EventType get_type () const noexcept;
    [[nodiscard]] bool is_handled () const noexcept;
    void set_handled (bool handled) noexcept;

  private:
    EventType m_type;
    bool m_handled{ false };
  };

  /**
   * @brief Event callback type
   */
  using EventCallback = std::function<void (Event&)>;

  /**
   * @brief Event manager class
   */
  class EventManager {
  public:
    EventManager ();
    ~EventManager ();

    EventManager (const EventManager&) = delete;
    EventManager& operator= (const EventManager&) = delete;

    EventManager (EventManager&&) noexcept;
    EventManager& operator= (EventManager&&) noexcept;

    bool initialize ();
    void shutdown ();

    void publish (Event& event);
    void subscribe (EventType type, EventCallback callback);
    void unsubscribe (EventType type, EventCallback callback);

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Events
