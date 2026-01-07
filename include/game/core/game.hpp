/**
 * @file game.hpp
 * @brief Core game interface
 */

#pragma once

namespace OmniCpp::Game::Core {

  class Game {
  public:
    Game ();
    ~Game ();

    void initialize ();
    void run ();
    void shutdown ();

  private:
    bool m_initialized;
    bool m_running;
  };

} // namespace OmniCpp::Game::Core
