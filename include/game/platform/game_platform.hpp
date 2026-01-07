/**
 * @file game_platform.hpp
 * @brief Game platform interface
 */

#pragma once

#include <string>

namespace OmniCpp::Game::Platform {

  class GamePlatform {
  public:
    GamePlatform ();
    ~GamePlatform ();

    void initialize ();
    void shutdown ();
  };

} // namespace OmniCpp::Game::Platform
