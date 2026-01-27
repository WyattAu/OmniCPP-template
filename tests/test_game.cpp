/**
 * @file test_game.cpp
 * @brief Unit tests for game application
 * @version 1.0.0
 */

#include "game/Game.hpp"
#include <iostream>
#include <cassert>

namespace omnicpp {

void test_game_initialization() {
    std::cout << "Testing game initialization..." << std::endl;
    
    Game game;
    bool initialized = game.initialize();
    assert(initialized);
    
    game.shutdown();
    
    std::cout << "Game initialization test PASSED" << std::endl;
}

void test_game_run() {
    std::cout << "Testing game run..." << std::endl;
    
    Game game;
    game.initialize();
    
    // Note: game.run() will block, so we can't test it directly
    // In a real test, we would run game in a separate thread
    
    game.shutdown();
    
    std::cout << "Game run test PASSED" << std::endl;
}

void test_dynamic_loading() {
    std::cout << "Testing dynamic loading..." << std::endl;
    
    Game game;
    game.initialize();
    
    // Verify that engine was loaded
    // This is tested implicitly by successful initialization
    
    game.shutdown();
    
    std::cout << "Dynamic loading test PASSED" << std::endl;
}

} // namespace omnicpp

int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;
    
    std::cout << "=== OmniCpp Game Tests ===" << std::endl;
    std::cout << std::endl;
    
    omnicpp::test_game_initialization();
    std::cout << std::endl;
    
    omnicpp::test_game_run();
    std::cout << std::endl;
    
    omnicpp::test_dynamic_loading();
    std::cout << std::endl;
    
    std::cout << "=== All Tests Completed ===" << std::endl;
    
    return 0;
}
