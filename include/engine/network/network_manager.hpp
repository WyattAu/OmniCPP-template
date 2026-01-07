/**
 * @file network_manager.hpp
 * @brief Network management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Network {

  /**
   * @brief Network configuration structure
   */
  struct NetworkConfig {
    uint16_t port{ 8080 };
    bool is_server{ false };
    uint32_t max_connections{ 32 };
  };

  /**
   * @brief Network manager class
   */
  class NetworkManager {
  public:
    NetworkManager ();
    ~NetworkManager ();

    NetworkManager (const NetworkManager&) = delete;
    NetworkManager& operator= (const NetworkManager&) = delete;

    NetworkManager (NetworkManager&&) noexcept;
    NetworkManager& operator= (NetworkManager&&) noexcept;

    bool initialize (const NetworkConfig& config);
    void shutdown ();
    void update ();

    bool start_server ();
    bool connect_to_server (const std::string& address);
    void disconnect ();

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Network
