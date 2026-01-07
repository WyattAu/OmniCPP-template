/**
 * @file game_input.hpp
 * @brief Game input interface
 */

#pragma once

#include <string>

namespace OmniCpp::Game::Input {

  class GameInput {
  public:
    GameInput ();
    ~GameInput ();

    void initialize ();
    void update ();
    bool is_action_pressed (const std::string& action) const;
  };

} // namespace OmniCpp::Game::Input
