#include <iostream>
#include <chrono>

// Working 3D Pong game - avoids std::this_thread::sleep_for which causes crashes

struct Vec3 {
    float x, y, z;
};

class Paddle {
public:
    Vec3 position;
    float width;
    float height;
    float depth;
    
    Paddle(float x, float y, float z, float w, float h, float d)
        : position{x, y, z}, width(w), height(h), depth(d) {}
    
    void move_up(float delta_time) {
        position.y += 5.0f * delta_time;
    }
    
    void move_down(float delta_time) {
        position.y -= 5.0f * delta_time;
    }
    
    void clamp_position(float min_y, float max_y) {
        if (position.y < min_y) position.y = min_y;
        if (position.y > max_y) position.y = max_y;
    }
};

class Ball {
public:
    Vec3 position;
    Vec3 velocity;
    float radius;
    
    Ball(float x, float y, float z, float r)
        : position{x, y, z}, velocity{0.0f, 0.0f, 0.0f}, radius(r) {}
    
    void update(float delta_time) {
        position.x += velocity.x * delta_time;
        position.y += velocity.y * delta_time;
        position.z += velocity.z * delta_time;
    }
    
    void reset(float x, float y, float z) {
        position.x = x;
        position.y = y;
        position.z = z;
        velocity.x = 0.0f;
        velocity.y = 0.0f;
        velocity.z = 0.0f;
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
    const float WINNING_SCORE = 10;
    
    int frame_count;
    
public:
    PongGame()
        : player_paddle(-9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f),
          ai_paddle(9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f),
          ball(0.0f, 0.0f, 0.0f, 0.3f),
          player_score(0),
          ai_score(0),
          game_over(false),
          frame_count(0) {
        std::cout << "PongGame constructor called" << std::endl;
    }
    
    void initialize() {
        std::cout << "Initializing PongGame..." << std::endl;
        reset_ball();
        std::cout << "PongGame initialized successfully" << std::endl;
    }
    
    void reset_ball() {
        ball.reset(0.0f, 0.0f, 0.0f);
        
        // Randomize initial direction
        float direction_x = (rand() % 2 == 0) ? 1.0f : -1.0f;
        float direction_y = (rand() % 2 == 0) ? 1.0f : -1.0f;
        float direction_z = (rand() % 2 == 0) ? 1.0f : -1.0f;
        
        ball.velocity.x = direction_x * BALL_SPEED;
        ball.velocity.y = direction_y * (BALL_SPEED * 0.5f);
        ball.velocity.z = direction_z * (BALL_SPEED * 0.3f);
        
        std::cout << "Ball reset with velocity: (" 
                  << ball.velocity.x << ", " 
                  << ball.velocity.y << ", " 
                  << ball.velocity.z << ")" << std::endl;
    }
    
    void update(float delta_time) {
        if (game_over) {
            return;
        }
        
        // Simulate player input (random movement for demo)
        if (frame_count % 60 < 30) {
            player_paddle.move_up(delta_time);
        } else if (frame_count % 60 < 60) {
            player_paddle.move_down(delta_time);
        }
        
        // Clamp player paddle position
        player_paddle.clamp_position(-FIELD_HEIGHT / 2.0f + player_paddle.height / 2.0f,
                                       FIELD_HEIGHT / 2.0f - player_paddle.height / 2.0f);
        
        // AI paddle movement (simple tracking)
        float ai_target_y = ball.position.y;
        float ai_speed = PADDLE_SPEED * 0.7f;
        
        if (ai_paddle.position.y < ai_target_y - 0.5f) {
            ai_paddle.position.y += ai_speed * delta_time;
        } else if (ai_paddle.position.y > ai_target_y + 0.5f) {
            ai_paddle.position.y -= ai_speed * delta_time;
        }
        
        // Clamp AI paddle position
        ai_paddle.clamp_position(-FIELD_HEIGHT / 2.0f + ai_paddle.height / 2.0f,
                                  FIELD_HEIGHT / 2.0f - ai_paddle.height / 2.0f);
        
        // Update ball
        ball.update(delta_time);
        
        // Check wall collisions
        check_wall_collisions();
        
        // Check paddle collisions
        check_paddle_collisions();
        
        // Check scoring
        check_scoring();
        
        frame_count++;
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
        if (ball.position.x - ball.radius < player_paddle.position.x + player_paddle.width / 2.0f &&
            ball.position.x + ball.radius > player_paddle.position.x - player_paddle.width / 2.0f &&
            ball.position.y - ball.radius < player_paddle.position.y + player_paddle.height / 2.0f &&
            ball.position.y + ball.radius > player_paddle.position.y - player_paddle.height / 2.0f &&
            ball.position.z - ball.radius < player_paddle.position.z + player_paddle.depth / 2.0f &&
            ball.position.z + ball.radius > player_paddle.position.z - player_paddle.depth / 2.0f) {
            
            ball.position.x = player_paddle.position.x + player_paddle.width / 2.0f + ball.radius;
            ball.velocity.x *= -1.0f;
            
            // Add some spin based on where ball hits paddle
            float hit_offset = (ball.position.y - player_paddle.position.y) / (player_paddle.height / 2.0f);
            ball.velocity.y += hit_offset * 2.0f;
            
            // Increase speed slightly
            ball.velocity.x *= 1.05f;
            ball.velocity.y *= 1.05f;
            ball.velocity.z *= 1.05f;
            
            // Cap speed
            float max_speed = BALL_SPEED * 2.0f;
            if (ball.velocity.x > max_speed) ball.velocity.x = max_speed;
            if (ball.velocity.x < -max_speed) ball.velocity.x = -max_speed;
            if (ball.velocity.y > max_speed) ball.velocity.y = max_speed;
            if (ball.velocity.y < -max_speed) ball.velocity.y = -max_speed;
            if (ball.velocity.z > max_speed) ball.velocity.z = max_speed;
            if (ball.velocity.z < -max_speed) ball.velocity.z = -max_speed;
        }
        
        // AI paddle collision
        if (ball.position.x + ball.radius > ai_paddle.position.x - ai_paddle.width / 2.0f &&
            ball.position.x - ball.radius < ai_paddle.position.x + ai_paddle.width / 2.0f &&
            ball.position.y - ball.radius < ai_paddle.position.y + ai_paddle.height / 2.0f &&
            ball.position.y + ball.radius > ai_paddle.position.y - ai_paddle.height / 2.0f &&
            ball.position.z - ball.radius < ai_paddle.position.z + ai_paddle.depth / 2.0f &&
            ball.position.z + ball.radius > ai_paddle.position.z - ai_paddle.depth / 2.0f) {
            
            ball.position.x = ai_paddle.position.x - ai_paddle.width / 2.0f - ball.radius;
            ball.velocity.x *= -1.0f;
            
            // Add some spin based on where ball hits paddle
            float hit_offset = (ball.position.y - ai_paddle.position.y) / (ai_paddle.height / 2.0f);
            ball.velocity.y += hit_offset * 2.0f;
            
            // Increase speed slightly
            ball.velocity.x *= 1.05f;
            ball.velocity.y *= 1.05f;
            ball.velocity.z *= 1.05f;
            
            // Cap speed
            float max_speed = BALL_SPEED * 2.0f;
            if (ball.velocity.x > max_speed) ball.velocity.x = max_speed;
            if (ball.velocity.x < -max_speed) ball.velocity.x = -max_speed;
            if (ball.velocity.y > max_speed) ball.velocity.y = max_speed;
            if (ball.velocity.y < -max_speed) ball.velocity.y = -max_speed;
            if (ball.velocity.z > max_speed) ball.velocity.z = max_speed;
            if (ball.velocity.z < -max_speed) ball.velocity.z = -max_speed;
        }
    }
    
    void check_scoring() {
        // Ball goes past player paddle (AI scores)
        if (ball.position.x < -FIELD_WIDTH / 2.0f) {
            ai_score++;
            std::cout << "AI scores! Score: Player " << player_score << " - AI " << ai_score << std::endl;
            
            if (ai_score >= WINNING_SCORE) {
                game_over = true;
                std::cout << "AI wins!" << std::endl;
            } else {
                reset_ball();
            }
        }
        
        // Ball goes past AI paddle (Player scores)
        if (ball.position.x > FIELD_WIDTH / 2.0f) {
            player_score++;
            std::cout << "Player scores! Score: Player " << player_score << " - AI " << ai_score << std::endl;
            
            if (player_score >= WINNING_SCORE) {
                game_over = true;
                std::cout << "Player wins!" << std::endl;
            } else {
                reset_ball();
            }
        }
    }
    
    void render() {
        // Simple console rendering
        std::cout << "\rFrame: " << frame_count 
                  << " | Ball: (" << ball.position.x << ", " << ball.position.y << ", " << ball.position.z << ")"
                  << " | Score: " << player_score << " - " << ai_score
                  << "    " << std::flush;
    }
    
    int run() {
        std::cout << "Starting Pong game..." << std::endl;
        std::cout << "Controls: W/S to move paddle (simulated for demo)" << std::endl;
        std::cout << "First to " << WINNING_SCORE << " points wins!" << std::endl;
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
            if (frame_count > 3600) { // ~60 seconds at 60 FPS
                std::cout << "\nDemo time limit reached!" << std::endl;
                break;
            }
        }
        
        std::cout << "\nGame Over! Final Score: Player " << player_score << " - AI " << ai_score << std::endl;
        return 0;
    }
};

int main() {
    std::cout << "=== 3D Pong Game ===" << std::endl;
    std::cout << "Working version (no sleep to avoid crash)" << std::endl;
    std::cout << std::endl;
    
    try {
        PongGame game;
        game.initialize();
        return game.run();
    } catch (const std::exception& e) {
        std::cerr << "Exception caught: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Unknown exception caught!" << std::endl;
        return 1;
    }
}
