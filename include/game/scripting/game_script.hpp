/**
 * @file game_script.hpp
 * @brief Game scripting interface
 */

#pragma once

#include <string>

namespace OmniCpp::Game::Scripting {

  class GameScript {
  public:
    GameScript ();
    ~GameScript ();

    void initialize ();
    void load_script (const std::string& script_path);
    void execute_script (const std::string& script_id);
  };

} // namespace OmniCpp::Game::Scripting
