/**
 * @file game_utils.cpp
 * @brief Game utility functions implementation
 */

#include "game/utils/game_utils.hpp"
#include "engine/logging/Log.hpp"

namespace OmniCpp::Game::Utils {

  bool GameUtils::s_initialized = false;

  void GameUtils::initialize () {
    if (s_initialized) {
      omnicpp::log::warn ("GameUtils already initialized, skipping");
      return;
    }

    omnicpp::log::info ("Initializing game utilities...");

    // TODO: Initialize utility subsystems
    // TODO: Setup file paths
    // TODO: Initialize resource caches

    s_initialized = true;
    omnicpp::log::info ("GameUtils initialized successfully");
  }

  void GameUtils::cleanup () {
    if (!s_initialized) {
      omnicpp::log::warn ("GameUtils not initialized, nothing to cleanup");
      return;
    }

    omnicpp::log::info ("Cleaning up game utilities...");

    // TODO: Cleanup utility subsystems
    // TODO: Clear resource caches
    // TODO: Close file handles

    s_initialized = false;
    omnicpp::log::info ("GameUtils cleanup complete");
  }

} // namespace OmniCpp::Game::Utils
