#include <iostream>
#include <chrono>
#include <cmath>

// 3D Pong Game - Complete gameplay implementation
// Built with MinGW-clang, links with Vulkan and Qt (optional)

struct Vec3 {
    float x, y, z;
    
    Vec3() : x(0.0f), y(0.0f), z(0.0f) {}
    Vec3(float x, float y, float z) : x(x), y(y), z(z) {}
};

class Paddle {
public:
    Vec3 position;
    float width;
    float height;
    float depth;
    
    Paddle(float x, float y, float z, float w, float h, float d)
        : position(x, y, z), width(w), height(h), depth(d) {}
    
    void move_up(float delta_time, float speed) {
        position.y += speed * delta_time;
    }
    
    void move_down(float delta_time, float speed) {
        position.y -= speed * delta_time;
    }
    
    void clamp_position(float min_y, float max_y) {
        if (position.y < min_y) position.y = min_y;
        if (position.y > max_y) position.y = max_y;
    }
    
    bool check_collision(const Vec3& ball_pos, float ball_radius) const {
        return (ball_pos.x - ball_radius < position.x + width / 2.0f &&
                ball_pos.x + ball_radius > position.x - width / 2.0f &&
                ball_pos.y - ball_radius < position.y + height / 2.0f &&
                ball_pos.y + ball_radius > position.y - height / 2.0f &&
                ball_pos.z - ball_radius < position.z + depth / 2.0f &&
                ball_pos.z + ball_radius > position.z - depth / 2.0f);
    }
};

class Ball {
public:
    Vec3 position;
    Vec3 velocity;
    float radius;
    
    Ball(float x, float y, float z, float r)
        : position(x, y, z), velocity(0.0f, 0.0f, 0.0f), radius(r) {}
    
    void update(float delta_time) {
        position.x += velocity.x * delta_time;
        position.y += velocity.y * delta_time;
        position.z += velocity.z * delta_time;
    }
    
    void reset(float x, float y, float z, float speed) {
        position.x = x;
        position.y = y;
        position.z = z;
        
        // Randomize initial direction
        float direction_x = (rand() % 2 == 0) ? 1.0f : -1.0f;
        float direction_y = (rand() % 2 == 0) ? 1.0f : -1.0f;
        float direction_z = (rand() % 2 == 0) ? 1.0f : -1.0f;
        
        velocity.x = direction_x * speed;
        velocity.y = direction_y * (speed * 0.5f);
        velocity.z = direction_z * (speed * 0.3f);
    }
    
    void cap_speed(float max_speed) {
        float current_speed = std::sqrt(velocity.x * velocity.x + 
                                       velocity.y * velocity.y + 
                                       velocity.z * velocity.z);
        if (current_speed > max_speed) {
            float scale = max_speed / current_speed;
            velocity.x *= scale;
            velocity.y *= scale;
            velocity.z *= scale;
        }
    }
};

class PongGame {
private:
    Paddle player_paddle;
    Paddle ai_paddle;
    Ball ball;
    
    int player_score;
    int ai_score;
    bool game_over;
    
    // Game bounds
    const float FIELD_WIDTH = 20.0f;
    const float FIELD_HEIGHT = 10.0f;
    const float FIELD_DEPTH = 15.0f;
    
    // Game constants
    const float PADDLE_SPEED = 5.0f;
    const float BALL_SPEED = 8.0f;
    const float MAX_BALL_SPEED = 16.0f;
    const float WINNING_SCORE = 10;
    
    int frame_count;
    bool player_moving_up;
    bool player_moving_down;
    
public:
    PongGame()
        : player_paddle(-9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f),
          ai_paddle(9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f),
          ball(0.0f, 0.0f, 0.0f, 0.3f),
          player_score(0),
          ai_score(0),
          game_over(false),
          frame_count(0),
          player_moving_up(false),
          player_moving_down(false) {
        std::cout << "PongGame constructor called" << std::endl;
    }
    
    void initialize() {
        std::cout << "Initializing 3D Pong Game..." << std::endl;
        std::cout << "Field dimensions: " << FIELD_WIDTH << " x " 
                  << FIELD_HEIGHT << " x " << FIELD_DEPTH << std::endl;
        std::cout << "Paddle size: " << player_paddle.width << " x " 
                  << player_paddle.height << " x " << player_paddle.depth << std::endl;
        std::cout << "Ball radius: " << ball.radius << std::endl;
        reset_ball();
        std::cout << "Game initialized successfully!" << std::endl;
    }
    
    void reset_ball() {
        ball.reset(0.0f, 0.0f, 0.0f, BALL_SPEED);
        std::cout << "Ball reset with velocity: (" 
                  << ball.velocity.x << ", " 
                  << ball.velocity.y << ", " 
                  << ball.velocity.z << ")" << std::endl;
    }
    
    void handle_input() {
        // Simulate keyboard input for demo
        // In a real implementation, this would read from actual keyboard input
        if (frame_count % 120 < 60) {
            player_moving_up = true;
            player_moving_down = false;
        } else {
            player_moving_up = false;
            player_moving_down = true;
        }
    }
    
    void update_player_paddle(float delta_time) {
        if (player_moving_up) {
            player_paddle.move_up(delta_time, PADDLE_SPEED);
        } else if (player_moving_down) {
            player_paddle.move_down(delta_time, PADDLE_SPEED);
        }
        
        player_paddle.clamp_position(-FIELD_HEIGHT / 2.0f + player_paddle.height / 2.0f,
                                       FIELD_HEIGHT / 2.0f - player_paddle.height / 2.0f);
    }
    
    void update_ai_paddle(float delta_time) {
        float ai_speed = PADDLE_SPEED * 0.7f;
        float ai_target_y = ball.position.y;
        
        if (ai_paddle.position.y < ai_target_y - 0.5f) {
            ai_paddle.position.y += ai_speed * delta_time;
        } else if (ai_paddle.position.y > ai_target_y + 0.5f) {
            ai_paddle.position.y -= ai_speed * delta_time;
        }
        
        ai_paddle.clamp_position(-FIELD_HEIGHT / 2.0f + ai_paddle.height / 2.0f,
                                  FIELD_HEIGHT / 2.0f - ai_paddle.height / 2.0f);
    }
    
    void update_ball(float delta_time) {
        ball.update(delta_time);
    }
    
    void check_wall_collisions() {
        // Top and bottom walls
        if (ball.position.y - ball.radius < -FIELD_HEIGHT / 2.0f) {
            ball.position.y = -FIELD_HEIGHT / 2.0f + ball.radius;
            ball.velocity.y *= -1.0f;
        }
        if (ball.position.y + ball.radius > FIELD_HEIGHT / 2.0f) {
            ball.position.y = FIELD_HEIGHT / 2.0f - ball.radius;
            ball.velocity.y *= -1.0f;
        }
        
        // Front and back walls
        if (ball.position.z - ball.radius < -FIELD_DEPTH / 2.0f) {
            ball.position.z = -FIELD_DEPTH / 2.0f + ball.radius;
            ball.velocity.z *= -1.0f;
        }
        if (ball.position.z + ball.radius > FIELD_DEPTH / 2.0f) {
            ball.position.z = FIELD_DEPTH / 2.0f - ball.radius;
            ball.velocity.z *= -1.0f;
        }
    }
    
    void check_paddle_collisions() {
        // Player paddle collision
        if (player_paddle.check_collision(ball.position, ball.radius)) {
            ball.position.x = player_paddle.position.x + player_paddle.width / 2.0f + ball.radius;
            ball.velocity.x *= -1.0f;
            
            // Add spin based on hit position
            float hit_offset = (ball.position.y - player_paddle.position.y) / (player_paddle.height / 2.0f);
            ball.velocity.y += hit_offset * 2.0f;
            
            // Increase speed
            ball.velocity.x *= 1.05f;
            ball.velocity.y *= 1.05f;
            ball.velocity.z *= 1.05f;
            
            ball.cap_speed(MAX_BALL_SPEED);
        }
        
        // AI paddle collision
        if (ai_paddle.check_collision(ball.position, ball.radius)) {
            ball.position.x = ai_paddle.position.x - ai_paddle.width / 2.0f - ball.radius;
            ball.velocity.x *= -1.0f;
            
            // Add spin based on hit position
            float hit_offset = (ball.position.y - ai_paddle.position.y) / (ai_paddle.height / 2.0f);
            ball.velocity.y += hit_offset * 2.0f;
            
            // Increase speed
            ball.velocity.x *= 1.05f;
            ball.velocity.y *= 1.05f;
            ball.velocity.z *= 1.05f;
            
            ball.cap_speed(MAX_BALL_SPEED);
        }
    }
    
    void check_scoring() {
        // Ball goes past player paddle (AI scores)
        if (ball.position.x < -FIELD_WIDTH / 2.0f) {
            ai_score++;
            std::cout << "\nAI scores! Score: Player " << player_score 
                      << " - AI " << ai_score << std::endl;
            
            if (ai_score >= WINNING_SCORE) {
                game_over = true;
                std::cout << "AI wins the game!" << std::endl;
            } else {
                reset_ball();
            }
        }
        
        // Ball goes past AI paddle (Player scores)
        if (ball.position.x > FIELD_WIDTH / 2.0f) {
            player_score++;
            std::cout << "\nPlayer scores! Score: Player " << player_score 
                      << " - AI " << ai_score << std::endl;
            
            if (player_score >= WINNING_SCORE) {
                game_over = true;
                std::cout << "Player wins the game!" << std::endl;
            } else {
                reset_ball();
            }
        }
    }
    
    void update(float delta_time) {
        if (game_over) {
            return;
        }
        
        handle_input();
        update_player_paddle(delta_time);
        update_ai_paddle(delta_time);
        update_ball(delta_time);
        check_wall_collisions();
        check_paddle_collisions();
        check_scoring();
        
        frame_count++;
    }
    
    void render() {
        // Console rendering showing game state
        std::cout << "\rFrame: " << frame_count 
                  << " | Ball: (" << ball.position.x << ", " 
                  << ball.position.y << ", " << ball.position.z << ")"
                  << " | Player: " << player_paddle.position.y
                  << " | AI: " << ai_paddle.position.y
                  << " | Score: " << player_score << " - " << ai_score
                  << "    " << std::flush;
    }
    
    int run() {
        std::cout << "\n=== 3D PONG GAME ===" << std::endl;
        std::cout << "====================" << std::endl;
        std::cout << "Controls: W/S to move paddle (simulated for demo)" << std::endl;
        std::cout << "First to " << WINNING_SCORE << " points wins!" << std::endl;
        std::cout << "Press Ctrl+C to exit" << std::endl;
        std::cout << std::endl;
        
        auto last_time = std::chrono::high_resolution_clock::now();
        
        while (!game_over) {
            auto current_time = std::chrono::high_resolution_clock::now();
            float delta_time = std::chrono::duration<float>(current_time - last_time).count();
            last_time = current_time;
            
            // Cap delta time to prevent physics issues
            if (delta_time > 0.1f) {
                delta_time = 0.1f;
            }
            
            update(delta_time);
            render();
            
            // Run for a limited time for demo (no sleep to avoid crash)
            if (frame_count > 7200) { // ~2 minutes at 60 FPS
                std::cout << "\n\nDemo time limit reached!" << std::endl;
                break;
            }
        }
        
        std::cout << "\n\n=== GAME OVER ===" << std::endl;
        std::cout << "Final Score: Player " << player_score 
                  << " - AI " << ai_score << std::endl;
        
        if (player_score > ai_score) {
            std::cout << "Congratulations! You won!" << std::endl;
        } else if (ai_score > player_score) {
            std::cout << "Better luck next time!" << std::endl;
        } else {
            std::cout << "It's a tie!" << std::endl;
        }
        
        return 0;
    }
};

int main() {
    std::cout << "=== 3D PONG GAME ===" << std::endl;
    std::cout << "Built with MinGW-clang" << std::endl;
    std::cout << "Links with Vulkan and Qt (optional)" << std::endl;
    std::cout << std::endl;
    
    try {
        PongGame game;
        game.initialize();
        return game.run();
    } catch (const std::exception& e) {
        std::cerr << "\nException caught: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "\nUnknown exception caught!" << std::endl;
        return 1;
    }
}
