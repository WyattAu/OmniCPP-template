/**
 * @file event_manager.cpp
 * @brief Event management implementation
 */

#include "engine/events/event_manager.hpp"
#include <algorithm>
#include <mutex>
#include <unordered_map>
#include "engine/logging/Log.hpp"

namespace OmniCpp::Engine::Events {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct EventManager::Impl {
    std::unordered_map<EventType, std::vector<EventCallback> > subscribers;
    std::mutex mutex;
    bool initialized{ false };
  };

  EventManager::EventManager () : m_impl (std::make_unique<Impl> ()) {
    // Constructor implementation
  }

  EventManager::~EventManager () {
    shutdown ();
  }

  EventManager::EventManager (EventManager&& other) noexcept : m_impl (std::move (other.m_impl)) {
    // Move constructor
  }

  EventManager& EventManager::operator= (EventManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool EventManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      omnicpp::log::warn("EventManager: Already initialized");
      return true;
    }

    m_impl->subscribers.clear ();
    m_impl->initialized = true;

    omnicpp::log::info("EventManager: Initialized");
    return true;
  }

  void EventManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->subscribers.clear ();
    m_impl->initialized = false;

    omnicpp::log::info("EventManager: Shutdown");
  }

  void EventManager::publish (Event& event) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      omnicpp::log::error("EventManager: Not initialized, cannot publish event");
      return;
    }

    auto it = m_impl->subscribers.find (event.get_type ());
    if (it != m_impl->subscribers.end ()) {
      omnicpp::log::debug("EventManager: Publishing event type {} to {} subscribers", static_cast<int>(event.get_type()), it->second.size());
      for (const auto& callback : it->second) {
        callback (event);
      }
    }
  }

  void EventManager::subscribe (EventType type, EventCallback callback) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      omnicpp::log::error("EventManager: Not initialized, cannot subscribe to event type {}", static_cast<int>(type));
      return;
    }

    m_impl->subscribers[type].push_back (callback);
    omnicpp::log::debug("EventManager: Subscribed to event type {}", static_cast<int>(type));
  }

  void EventManager::unsubscribe (EventType type, EventCallback callback) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      omnicpp::log::error("EventManager: Not initialized, cannot unsubscribe from event type {}", static_cast<int>(type));
      return;
    }

    auto it = m_impl->subscribers.find (type);
    if (it != m_impl->subscribers.end ()) {
      auto& callbacks = it->second;
      auto new_end = std::remove (callbacks.begin (), callbacks.end (), callback);
      callbacks.erase (new_end, callbacks.end ());
      omnicpp::log::debug("EventManager: Unsubscribed from event type {}", static_cast<int>(type));
    }
  }

} // namespace OmniCpp::Engine::Events
