/**
 * @file game_scene.hpp
 * @brief Game scene interface
 */

#pragma once

namespace OmniCpp::Game::Scene {

  class GameScene {
  public:
    GameScene ();
    ~GameScene ();

    void initialize ();
    void update (float delta_time);
    void render ();
  };

} // namespace OmniCpp::Game::Scene
