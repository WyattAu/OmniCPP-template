/**
 * @file game_physics.hpp
 * @brief Game physics interface
 */

#pragma once

namespace OmniCpp::Game::Physics {

  class GamePhysics {
  public:
    GamePhysics ();
    ~GamePhysics ();

    void initialize ();
    void update (float delta_time);
  };

} // namespace OmniCpp::Game::Physics
