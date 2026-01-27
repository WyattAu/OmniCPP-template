/**
 * @file network_manager.cpp
 * @brief Network management implementation
 */

#include "engine/network/network_manager.hpp"
#include <mutex>
#include <spdlog/spdlog.h>

namespace OmniCpp::Engine::Network {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct NetworkManager::Impl {
    NetworkConfig config;
    std::mutex mutex;
    bool initialized{ false };
  };

  NetworkManager::NetworkManager () : m_impl (std::make_unique<Impl> ()) {
  }

  NetworkManager::~NetworkManager () {
    shutdown ();
  }

  NetworkManager::NetworkManager (NetworkManager&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
  }

  NetworkManager& NetworkManager::operator= (NetworkManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool NetworkManager::initialize (const NetworkConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      spdlog::warn("NetworkManager: Already initialized");
      return true;
    }

    m_impl->config = config;
    m_impl->initialized = true;

    spdlog::info("NetworkManager: Initialized");
    return true;
  }

  void NetworkManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->initialized = false;

    spdlog::info("NetworkManager: Shutdown");
  }

  void NetworkManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update network state here
  }

  bool NetworkManager::start_server () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("NetworkManager: Not initialized, cannot start server");
      return false;
    }

    spdlog::info("NetworkManager: Starting server");
    return true;
  }

  bool NetworkManager::connect_to_server (const std::string& address) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("NetworkManager: Not initialized, cannot connect to {}", address);
      return false;
    }

    spdlog::info("NetworkManager: Connecting to server at {}", address);
    return true;
  }

  void NetworkManager::disconnect () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    spdlog::info("NetworkManager: Disconnecting");
    // Disconnect here
  }

} // namespace OmniCpp::Engine::Network
