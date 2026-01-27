/**
 * @file game_renderer.hpp
 * @brief Game graphics interface
 */

#pragma once

namespace OmniCpp::Game::Graphics {

  class GameRenderer {
  public:
    GameRenderer ();
    ~GameRenderer ();

    void initialize ();
    void render ();

  private:
    bool m_initialized;
  };

} // namespace OmniCpp::Game::Graphics
