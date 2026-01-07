/**
 * @file game_network.hpp
 * @brief Game network interface
 */

#pragma once

#include <string>

namespace OmniCpp::Game::Network {

  class GameNetwork {
  public:
    GameNetwork ();
    ~GameNetwork ();

    void initialize ();
    void connect (const std::string& address, int port);
    void disconnect ();
    void update ();
  };

} // namespace OmniCpp::Game::Network
