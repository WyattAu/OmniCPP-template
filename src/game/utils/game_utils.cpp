/**
 * @file game_utils.cpp
 * @brief Game utility functions implementation
 */

#include "game/utils/game_utils.hpp"
#include <spdlog/spdlog.h>

namespace OmniCpp::Game::Utils {

  bool GameUtils::s_initialized = false;

  void GameUtils::initialize () {
    if (s_initialized) {
      spdlog::warn ("GameUtils already initialized, skipping");
      return;
    }

    spdlog::info ("Initializing game utilities...");

    // TODO: Initialize utility subsystems
    // TODO: Setup file paths
    // TODO: Initialize resource caches

    s_initialized = true;
    spdlog::info ("GameUtils initialized successfully");
  }

  void GameUtils::cleanup () {
    if (!s_initialized) {
      spdlog::warn ("GameUtils not initialized, nothing to cleanup");
      return;
    }

    spdlog::info ("Cleaning up game utilities...");

    // TODO: Cleanup utility subsystems
    // TODO: Clear resource caches
    // TODO: Close file handles

    s_initialized = false;
    spdlog::info ("GameUtils cleanup complete");
  }

} // namespace OmniCpp::Game::Utils
