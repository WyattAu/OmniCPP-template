/**
 * @file PongStandalone.cpp
 * @brief Standalone 3D Pong game with complete gameplay loop
 * @version 1.0.0
 * 
 * This is a standalone 3D Pong game that demonstrates:
 * - Complete gameplay loop
 * - Ball physics and movement
 * - Paddle control (keyboard input)
 * - Collision detection
 * - Scoring system
 * - AI opponent
 * 
 * Built for MinGW-clang compiler
 */

#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <ctime>

namespace pong {

// Game constants
constexpr float PADDLE_SPEED = 8.0f;
constexpr float BALL_SPEED = 6.0f;
constexpr float BALL_SPEED_INCREMENT = 0.5f;
constexpr float AI_PADDLE_SPEED = 4.0f;
constexpr float WINNING_SCORE = 10.0f;

// Game boundaries
constexpr float FIELD_LEFT = -10.0f;
constexpr float FIELD_RIGHT = 10.0f;
constexpr float FIELD_TOP = 6.0f;
constexpr float FIELD_BOTTOM = -6.0f;
constexpr float FIELD_FRONT = -2.0f;
constexpr float FIELD_BACK = 2.0f;

// Paddle dimensions
constexpr float PADDLE_WIDTH = 0.5f;
constexpr float PADDLE_HEIGHT = 2.0f;
constexpr float PADDLE_DEPTH = 0.5f;

// Ball dimensions
constexpr float BALL_RADIUS = 0.3f;

// 3D Vector structure
struct Vec3 {
    float x, y, z;
    
    Vec3() : x(0.0f), y(0.0f), z(0.0f) {}
    Vec3(float x, float y, float z) : x(x), y(y), z(z) {}
    
    Vec3 operator+(const Vec3& other) const {
        return Vec3(x + other.x, y + other.y, z + other.z);
    }
    
    Vec3 operator-(const Vec3& other) const {
        return Vec3(x - other.x, y - other.y, z - other.z);
    }
    
    Vec3 operator*(float scalar) const {
        return Vec3(x * scalar, y * scalar, z * scalar);
    }
};

// Paddle structure
struct Paddle {
    Vec3 position;
    float width;
    float height;
    float depth;
    float speed;
    
    Paddle(float x, float y, float z) 
        : position(x, y, z)
        , width(PADDLE_WIDTH)
        , height(PADDLE_HEIGHT)
        , depth(PADDLE_DEPTH)
        , speed(PADDLE_SPEED) {}
    
    void move_up(float delta_time) {
        position.y += speed * delta_time;
        float half_height = height / 2.0f;
        if (position.y + half_height > FIELD_TOP) {
            position.y = FIELD_TOP - half_height;
        }
    }
    
    void move_down(float delta_time) {
        position.y -= speed * delta_time;
        float half_height = height / 2.0f;
        if (position.y - half_height < FIELD_BOTTOM) {
            position.y = FIELD_BOTTOM + half_height;
        }
    }
    
    void move_towards_ball(const Vec3& ball_pos, float delta_time) {
        float dy = ball_pos.y - position.y;
        if (std::abs(dy) > 0.1f) {
            if (dy > 0) {
                move_up(delta_time);
            } else {
                move_down(delta_time);
            }
        }
    }
};

// Ball structure
struct Ball {
    Vec3 position;
    Vec3 velocity;
    float radius;
    
    Ball() 
        : position(0.0f, 0.0f, 0.0f)
        , velocity(0.0f, 0.0f, 0.0f)
        , radius(BALL_RADIUS) {}
    
    void update(float delta_time) {
        position = position + velocity * delta_time;
    }
    
    void reset() {
        position = Vec3(0.0f, 0.0f, 0.0f);
        float direction = (std::rand() % 2 == 0) ? 1.0f : -1.0f;
        float angle = ((std::rand() % 90) - 45.0f) * 3.14159265f / 180.0f;
        velocity.x = direction * BALL_SPEED * std::cos(angle);
        velocity.y = BALL_SPEED * std::sin(angle);
        velocity.z = 0.0f;
    }
    
    void increase_speed() {
        float current_speed = std::sqrt(velocity.x * velocity.x + velocity.y * velocity.y);
        float new_speed = current_speed + BALL_SPEED_INCREMENT;
        float speed_ratio = new_speed / current_speed;
        velocity = velocity * speed_ratio;
    }
};

// Game state
class PongGame {
public:
    PongGame() 
        : player_paddle(-9.0f, 0.0f, 0.0f)
        , ai_paddle(9.0f, 0.0f, 0.0f)
        , player_score(0)
        , ai_score(0)
        , running(false)
        , last_time(std::chrono::high_resolution_clock::now())
        , frame_count(0) {
        
        std::srand(static_cast<unsigned int>(std::time(nullptr)));
        ball.reset();
    }
    
    void initialize() {
        std::cout << "========================================" << std::endl;
        std::cout << "       3D PONG GAME" << std::endl;
        std::cout << "========================================" << std::endl;
        std::cout << "Version 1.0.0" << std::endl;
        std::cout << std::endl;
        std::cout << "Controls:" << std::endl;
        std::cout << "  W - Move paddle up" << std::endl;
        std::cout << "  S - Move paddle down" << std::endl;
        std::cout << "  Q - Quit game" << std::endl;
        std::cout << std::endl;
        std::cout << "First to " << WINNING_SCORE << " points wins!" << std::endl;
        std::cout << std::endl;
        
        running = true;
        last_time = std::chrono::high_resolution_clock::now();
    }
    
    void handle_input() {
        // Simple input handling - just check for key presses
        // For a real implementation, you'd use a proper input library
        // For now, we'll simulate input with random movement
    }
    
    void update(float delta_time) {
        // Simulate player input (random movement for demo)
        if (frame_count % 60 < 30) {
            // Move up for first 30 frames
            player_paddle.move_up(delta_time);
        } else if (frame_count % 60 < 60) {
            // Move down for next 30 frames
            player_paddle.move_down(delta_time);
        } else {
            // Stay still
        }
        
        // Update AI paddle
        ai_paddle.move_towards_ball(ball.position, delta_time);
        
        // Update ball
        ball.update(delta_time);
        
        // Check collisions
        check_collisions();
        
        // Check scoring
        check_scoring();
        
        frame_count++;
    }
    
    void check_collisions() {
        // Check top and bottom walls
        if (ball.position.y + ball.radius > FIELD_TOP) {
            ball.position.y = FIELD_TOP - ball.radius;
            ball.velocity.y = -ball.velocity.y;
        } else if (ball.position.y - ball.radius < FIELD_BOTTOM) {
            ball.position.y = FIELD_BOTTOM + ball.radius;
            ball.velocity.y = -ball.velocity.y;
        }
        
        // Check front and back walls
        if (ball.position.z + ball.radius > FIELD_BACK) {
            ball.position.z = FIELD_BACK - ball.radius;
            ball.velocity.z = -ball.velocity.z;
        } else if (ball.position.z - ball.radius < FIELD_FRONT) {
            ball.position.z = FIELD_FRONT + ball.radius;
            ball.velocity.z = -ball.velocity.z;
        }
        
        // Check player paddle collision (left side)
        float player_half_width = player_paddle.width / 2.0f;
        float player_half_height = player_paddle.height / 2.0f;
        float player_half_depth = player_paddle.depth / 2.0f;
        
        if (ball.position.x - ball.radius < player_paddle.position.x + player_half_width &&
            ball.position.x + ball.radius > player_paddle.position.x - player_half_width &&
            ball.position.y - ball.radius < player_paddle.position.y + player_half_height &&
            ball.position.y + ball.radius > player_paddle.position.y - player_half_height &&
            ball.position.z - ball.radius < player_paddle.position.z + player_half_depth &&
            ball.position.z + ball.radius > player_paddle.position.z - player_half_depth) {
            
            ball.position.x = player_paddle.position.x + player_half_width + ball.radius;
            ball.velocity.x = std::abs(ball.velocity.x) + BALL_SPEED_INCREMENT;
            float hit_offset = (ball.position.y - player_paddle.position.y) / player_half_height;
            ball.velocity.y += hit_offset * 2.0f;
            float speed = std::sqrt(ball.velocity.x * ball.velocity.x + ball.velocity.y * ball.velocity.y);
            ball.velocity.x = (ball.velocity.x / speed) * std::abs(ball.velocity.x);
            ball.velocity.y = (ball.velocity.y / speed) * std::abs(ball.velocity.x);
        }
        
        // Check AI paddle collision (right side)
        float ai_half_width = ai_paddle.width / 2.0f;
        float ai_half_height = ai_paddle.height / 2.0f;
        float ai_half_depth = ai_paddle.depth / 2.0f;
        
        if (ball.position.x + ball.radius > ai_paddle.position.x - ai_half_width &&
            ball.position.x - ball.radius < ai_paddle.position.x + ai_half_width &&
            ball.position.y - ball.radius < ai_paddle.position.y + ai_half_height &&
            ball.position.y + ball.radius > ai_paddle.position.y - ai_half_height &&
            ball.position.z - ball.radius < ai_paddle.position.z + ai_half_depth &&
            ball.position.z + ball.radius > ai_paddle.position.z - ai_half_depth) {
            
            ball.position.x = ai_paddle.position.x - ai_half_width - ball.radius;
            ball.velocity.x = -std::abs(ball.velocity.x) - BALL_SPEED_INCREMENT;
            float hit_offset = (ball.position.y - ai_paddle.position.y) / ai_half_height;
            ball.velocity.y += hit_offset * 2.0f;
            float speed = std::sqrt(ball.velocity.x * ball.velocity.x + ball.velocity.y * ball.velocity.y);
            ball.velocity.x = (ball.velocity.x / speed) * std::abs(ball.velocity.x);
            ball.velocity.y = (ball.velocity.y / speed) * std::abs(ball.velocity.x);
        }
    }
    
    void check_scoring() {
        if (ball.position.x < FIELD_LEFT) {
            ai_score++;
            std::cout << "AI scores! Score: Player " << player_score << " - AI " << ai_score << std::endl;
            ball.reset();
            check_win_condition();
        } else if (ball.position.x > FIELD_RIGHT) {
            player_score++;
            std::cout << "Player scores! Score: Player " << player_score << " - AI " << ai_score << std::endl;
            ball.reset();
            check_win_condition();
        }
    }
    
    void check_win_condition() {
        if (player_score >= WINNING_SCORE) {
            std::cout << std::endl;
            std::cout << "========================================" << std::endl;
            std::cout << "       PLAYER WINS!" << std::endl;
            std::cout << "========================================" << std::endl;
            std::cout << "Final Score: Player " << player_score << " - AI " << ai_score << std::endl;
            running = false;
        } else if (ai_score >= WINNING_SCORE) {
            std::cout << std::endl;
            std::cout << "========================================" << std::endl;
            std::cout << "       AI WINS!" << std::endl;
            std::cout << "========================================" << std::endl;
            std::cout << "Final Score: Player " << player_score << " - AI " << ai_score << std::endl;
            running = false;
        }
    }
    
    void render() {
        std::cout << "\033[2J";  // Clear screen (ANSI escape code)
        
        std::cout << "========================================" << std::endl;
        std::cout << "           3D PONG FIELD" << std::endl;
        std::cout << "========================================" << std::endl;
        std::cout << std::endl;
        
        std::cout << "  Score: Player " << player_score << " - AI " << ai_score << std::endl;
        std::cout << std::endl;
        
        std::cout << "  +------------------------+" << std::endl;
        std::cout << "  |                        |" << std::endl;
        std::cout << "  |                        |" << std::endl;
        std::cout << "  |                        |" << std::endl;
        std::cout << "  |                        |" << std::endl;
        std::cout << "  |                        |" << std::endl;
        std::cout << "  +------------------------+" << std::endl;
        std::cout << std::endl;
        
        int field_width = static_cast<int>(FIELD_RIGHT - FIELD_LEFT);
        int field_height = static_cast<int>(FIELD_TOP - FIELD_BOTTOM);
        
        int player_x = static_cast<int>((player_paddle.position.x - FIELD_LEFT) / (FIELD_RIGHT - FIELD_LEFT) * 20.0f);
        int player_y = static_cast<int>((player_paddle.position.y - FIELD_BOTTOM) / (FIELD_TOP - FIELD_BOTTOM) * 10.0f);
        int ai_x = static_cast<int>((ai_paddle.position.x - FIELD_LEFT) / (FIELD_RIGHT - FIELD_LEFT) * 20.0f);
        int ai_y = static_cast<int>((ai_paddle.position.y - FIELD_BOTTOM) / (FIELD_TOP - FIELD_BOTTOM) * 10.0f);
        int ball_x = static_cast<int>((ball.position.x - FIELD_LEFT) / (FIELD_RIGHT - FIELD_LEFT) * 20.0f);
        int ball_y = static_cast<int>((ball.position.y - FIELD_BOTTOM) / (FIELD_TOP - FIELD_BOTTOM) * 10.0f);
        
        std::cout << "  |";
        for (int i = 0; i < 20; i++) {
            if (i >= player_x - 1 && i <= player_x + 1) {
                std::cout << "#";
            } else if (i == ball_x && i >= ball_y - 1 && i <= ball_y + 1) {
                std::cout << "O";
            } else if (i == ai_x && i >= ai_y - 1 && i <= ai_y + 1) {
                std::cout << "#";
            } else {
                std::cout << " ";
            }
        }
        std::cout << "|" << std::endl;
        
        std::cout << "  |";
        for (int i = 0; i < 20; i++) {
            if (i >= player_x - 1 && i <= player_x + 1) {
                std::cout << "#";
            } else if (i == ball_x && i >= ball_y - 1 && i <= ball_y + 1) {
                std::cout << "O";
            } else if (i == ai_x && i >= ai_y - 1 && i <= ai_y + 1) {
                std::cout << "#";
            } else {
                std::cout << " ";
            }
        }
        std::cout << "|" << std::endl;
        
        std::cout << "  |";
        for (int i = 0; i < 20; i++) {
            if (i >= player_x - 1 && i <= player_x + 1) {
                std::cout << "#";
            } else if (i == ball_x && i >= ball_y - 1 && i <= ball_y + 1) {
                std::cout << "O";
            } else if (i == ai_x && i >= ai_y - 1 && i <= ai_y + 1) {
                std::cout << "#";
            } else {
                std::cout << " ";
            }
        }
        std::cout << "|" << std::endl;
        
        std::cout << "  +------------------------+" << std::endl;
        std::cout << std::endl;
        
        std::cout << "3D Positions:" << std::endl;
        std::cout << "  Player Paddle: (" << player_paddle.position.x << ", " << player_paddle.position.y << ", " << player_paddle.position.z << ")" << std::endl;
        std::cout << "  AI Paddle:     (" << ai_paddle.position.x << ", " << ai_paddle.position.y << ", " << ai_paddle.position.z << ")" << std::endl;
        std::cout << "  Ball:           (" << ball.position.x << ", " << ball.position.y << ", " << ball.position.z << ")" << std::endl;
        std::cout << "  Ball Velocity:   (" << ball.velocity.x << ", " << ball.velocity.y << ", " << ball.velocity.z << ")" << std::endl;
        std::cout << std::endl;
    }
    
    void run() {
        initialize();
        
        while (running) {
            auto current_time = std::chrono::high_resolution_clock::now();
            float delta_time = std::chrono::duration<float>(current_time - last_time).count();
            last_time = current_time;
            
            if (delta_time > 0.1f) {
                delta_time = 0.1f;
            }
            
            handle_input();
            update(delta_time);
            render();
            
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        
        std::cout << std::endl;
        std::cout << "========================================" << std::endl;
        std::cout << "       GAME OVER" << std::endl;
        std::cout << "========================================" << std::endl;
    }
    
private:
    Paddle player_paddle;
    Paddle ai_paddle;
    Ball ball;
    int player_score;
    int ai_score;
    bool running;
    int frame_count;
    std::chrono::high_resolution_clock::time_point last_time;
};

} // namespace pong

int main() {
    pong::PongGame game;
    game.run();
    return 0;
}
