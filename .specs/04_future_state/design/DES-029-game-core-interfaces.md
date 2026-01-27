# DES-029: Game Core Interfaces

## Overview
Defines the core game interfaces for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_GAME_CORE_INTERFACES_H
#define OMNICPP_GAME_CORE_INTERFACES_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace omnicpp {
namespace game {

// Forward declarations
class IGame;
class IGameState;
class IGameMode;
class IGameSession;

// Game configuration
struct GameConfig {
    std::string game_title;
    std::string game_version;
    int max_players;
    bool enable_multiplayer;
    bool enable_networking;
    bool enable_save_load;
    std::string save_directory;

    GameConfig()
        : game_title("OmniCpp Game")
        , game_version("1.0.0")
        , max_players(1)
        , enable_multiplayer(false)
        , enable_networking(false)
        , enable_save_load(true)
        , save_directory("saves/")
    {}
};

// Game state
enum class GameState {
    UNINITIALIZED,
    INITIALIZING,
    LOADING,
    RUNNING,
    PAUSED,
    GAME_OVER,
    SHUTTING_DOWN,
    SHUTDOWN
};

// Game mode type
enum class GameModeType {
    SINGLE_PLAYER,
    MULTIPLAYER_COOP,
    MULTIPLAYER_VERSUS,
    MULTIPLAYER_TEAM
};

// Game statistics
struct GameStats {
    uint32_t total_play_time;
    uint32_t current_play_time;
    uint32_t score;
    uint32_t high_score;
    uint32_t deaths;
    uint32_t kills;
    uint32_t level;
    uint32_t experience;

    GameStats()
        : total_play_time(0)
        , current_play_time(0)
        , score(0)
        , high_score(0)
        , deaths(0)
        , kills(0)
        , level(1)
        , experience(0)
    {}
};

// Game interface
class IGame {
public:
    virtual ~IGame() = default;

    // Initialization
    virtual bool initialize(const GameConfig& config) = 0;
    virtual void shutdown() = 0;

    // Main loop
    virtual void run() = 0;
    virtual void stop() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // State management
    virtual GameState get_state() const = 0;
    virtual void set_state(GameState state) = 0;

    // Game modes
    virtual void set_game_mode(IGameMode* game_mode) = 0;
    virtual IGameMode* get_game_mode() const = 0;

    // Game sessions
    virtual void create_session() = 0;
    virtual void destroy_session() = 0;
    virtual IGameSession* get_session() const = 0;

    // Statistics
    virtual const GameStats& get_stats() const = 0;
    virtual void update_stats(double delta_time) = 0;
    virtual void reset_stats() = 0;

    // Save/Load
    virtual bool save_game(const std::string& slot_name) = 0;
    virtual bool load_game(const std::string& slot_name) = 0;
    virtual bool delete_save(const std::string& slot_name) = 0;
    virtual std::vector<std::string> list_saves() const = 0;

    // Frame callbacks
    virtual void on_frame_start() = 0;
    virtual void on_frame_end() = 0;
    virtual void on_update(double delta_time) = 0;
    virtual void on_render() = 0;

    // Event handling
    virtual void handle_events() = 0;
};

// Game state interface
class IGameState {
public:
    virtual ~IGameState() = default;

    // State lifecycle
    virtual void on_enter() = 0;
    virtual void on_exit() = 0;
    virtual void on_pause() = 0;
    virtual void on_resume() = 0;

    // State update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;

    // State name
    virtual const std::string& get_name() const = 0;
    virtual void set_name(const std::string& name) = 0;

    // State active
    virtual bool is_active() const = 0;
    virtual void set_active(bool active) = 0;
};

// Game mode interface
class IGameMode {
public:
    virtual ~IGameMode() = default;

    // Mode lifecycle
    virtual void on_enter() = 0;
    virtual void on_exit() = 0;

    // Mode update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;

    // Mode type
    virtual GameModeType get_type() const = 0;
    virtual void set_type(GameModeType type) = 0;

    // Player management
    virtual void add_player(uint32_t player_id) = 0;
    virtual void remove_player(uint32_t player_id) = 0;
    virtual std::vector<uint32_t> get_players() const = 0;

    // Mode configuration
    virtual void set_max_players(int max_players) = 0;
    virtual int get_max_players() const = 0;
    virtual void set_team_count(int team_count) = 0;
    virtual int get_team_count() const = 0;

    // Win condition
    virtual bool check_win_condition() const = 0;
    virtual bool check_lose_condition() const = 0;
    virtual void on_win() = 0;
    virtual void on_lose() = 0;
};

// Game session interface
class IGameSession {
public:
    virtual ~IGameSession() = default;

    // Session lifecycle
    virtual void start() = 0;
    virtual void stop() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;

    // Session state
    virtual bool is_running() const = 0;
    virtual bool is_paused() const = 0;

    // Session time
    virtual double get_elapsed_time() const = 0;
    virtual void reset_elapsed_time() = 0;

    // Session data
    virtual void set_data(const std::string& key, const std::string& value) = 0;
    virtual std::string get_data(const std::string& key) const = 0;
    virtual bool has_data(const std::string& key) const = 0;
    virtual void clear_data() = 0;

    // Session players
    virtual void add_player(uint32_t player_id) = 0;
    virtual void remove_player(uint32_t player_id) = 0;
    virtual std::vector<uint32_t> get_players() const = 0;
    virtual uint32_t get_player_count() const = 0;
};

// Game factory
class IGameFactory {
public:
    virtual ~IGameFactory() = default;

    virtual std::unique_ptr<IGame> create_game() = 0;
    virtual void destroy_game(std::unique_ptr<IGame> game) = 0;
};

// Game state manager
class IGameStateManager {
public:
    virtual ~IGameStateManager() = default;

    // State management
    virtual void push_state(IGameState* state) = 0;
    virtual void pop_state() = 0;
    virtual void change_state(IGameState* state) = 0;
    virtual void clear_states() = 0;

    // State queries
    virtual IGameState* get_current_state() const = 0;
    virtual IGameState* get_previous_state() const = 0;
    virtual std::vector<IGameState*> get_all_states() const = 0;
    virtual int get_state_count() const = 0;

    // State update
    virtual void update(double delta_time) = 0;
    virtual void render() = 0;
};

// Game event
struct GameEvent {
    enum class Type {
        GAME_STARTED,
        GAME_STOPPED,
        GAME_PAUSED,
        GAME_RESUMED,
        GAME_OVER,
        LEVEL_STARTED,
        LEVEL_COMPLETED,
        PLAYER_DIED,
        PLAYER_SPAWNED,
        SCORE_CHANGED,
        HIGH_SCORE_ACHIEVED
    };

    Type type;
    std::string message;
    std::unordered_map<std::string, std::string> data;

    GameEvent(Type t, const std::string& msg = "")
        : type(t)
        , message(msg)
    {}
};

// Game event listener
using GameEventListener = std::function<void(const GameEvent&)>;

// Game event manager
class IGameEventManager {
public:
    virtual ~IGameEventManager() = default;

    virtual void add_listener(GameEventListener listener) = 0;
    virtual void remove_listener(GameEventListener listener) = 0;
    virtual void emit_event(const GameEvent& event) = 0;
    virtual void clear_listeners() = 0;
};

// Game profiler
class IGameProfiler {
public:
    virtual ~IGameProfiler() = default;

    virtual void begin_frame() = 0;
    virtual void end_frame() = 0;
    virtual void begin_sample(const std::string& name) = 0;
    virtual void end_sample(const std::string& name) = 0;

    virtual double get_sample_time(const std::string& name) const = 0;
    virtual std::vector<std::string> get_sample_names() const = 0;
    virtual void clear_samples() = 0;
};

} // namespace game
} // namespace omnicpp

#endif // OMNICPP_GAME_CORE_INTERFACES_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces
- `DES-028` - Scene Manager Interface

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects
- `unordered_map` - Hash map

## Related Requirements
- REQ-045: Game Core Architecture
- REQ-046: Game State Management

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Game Design
1. Abstract game interface
2. Support multiple game modes
3. Game state management
4. Session management

### Game States
1. State stack for navigation
2. State transitions
3. Pause/resume functionality
4. State lifecycle

### Game Modes
1. Single player mode
2. Multiplayer modes
3. Team-based modes
4. Win/lose conditions

### Game Sessions
1. Session lifecycle
2. Player management
3. Session data
4. Time tracking

## Usage Example

```cpp
#include "game_core_interfaces.hpp"

using namespace omnicpp::game;

int main() {
    // Create game configuration
    GameConfig config;
    config.game_title = "My Game";
    config.game_version = "1.0.0";
    config.max_players = 4;
    config.enable_multiplayer = true;
    config.enable_save_load = true;
    config.save_directory = "saves/";

    // Create game
    auto game = std::make_unique<Game>();

    // Initialize game
    if (!game->initialize(config)) {
        std::cerr << "Failed to initialize game" << std::endl;
        return 1;
    }

    // Create game session
    game->create_session();

    // Set game mode
    auto game_mode = std::make_unique<MultiplayerVersusMode>();
    game_mode->set_type(GameModeType::MULTIPLAYER_VERSUS);
    game_mode->set_max_players(4);
    game->set_game_mode(game_mode.get());

    // Run game
    game->run();

    // Save game
    game->save_game("save1");

    // List saves
    std::vector<std::string> saves = game->list_saves();
    for (const auto& save : saves) {
        std::cout << "Save: " << save << std::endl;
    }

    // Shutdown game
    game->shutdown();

    return 0;
}
```
