/**
 * @file game_audio.hpp
 * @brief Game audio interface
 */

#pragma once

#include <string>

namespace OmniCpp::Game::Audio {

  class GameAudio {
  public:
    GameAudio ();
    ~GameAudio ();

    void initialize ();
    void play_sound (const std::string& sound_id);
    void update ();
  };

} // namespace OmniCpp::Game::Audio
