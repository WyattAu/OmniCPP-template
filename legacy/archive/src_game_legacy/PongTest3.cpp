#include <iostream>
#include <chrono>

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
};

int main() {
    std::cout << "Creating Pong game objects..." << std::endl;
    
    Paddle player_paddle(-9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f);
    Paddle ai_paddle(9.0f, 0.0f, 0.0f, 0.5f, 2.0f, 0.5f);
    Ball ball(0.0f, 0.0f, 0.0f, 0.3f);
    
    std::cout << "Player paddle position: (" << player_paddle.position.x << ", " 
              << player_paddle.position.y << ", " << player_paddle.position.z << ")" << std::endl;
    std::cout << "AI paddle position: (" << ai_paddle.position.x << ", " 
              << ai_paddle.position.y << ", " << ai_paddle.position.z << ")" << std::endl;
    std::cout << "Ball position: (" << ball.position.x << ", " 
              << ball.position.y << ", " << ball.position.z << ")" << std::endl;
    
    std::cout << "Testing movement..." << std::endl;
    
    // Test paddle movement
    player_paddle.move_up(0.1f);
    std::cout << "After moving up, player paddle y: " << player_paddle.position.y << std::endl;
    
    player_paddle.move_down(0.1f);
    std::cout << "After moving down, player paddle y: " << player_paddle.position.y << std::endl;
    
    // Test ball movement
    ball.velocity.x = 1.0f;
    ball.velocity.y = 0.5f;
    ball.velocity.z = 0.3f;
    
    ball.update(0.1f);
    std::cout << "After update, ball position: (" << ball.position.x << ", " 
              << ball.position.y << ", " << ball.position.z << ")" << std::endl;
    
    std::cout << "Testing time measurement..." << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    // Simulate some work instead of sleeping
    volatile int sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += i;
    }
    auto end = std::chrono::high_resolution_clock::now();
    
    float elapsed = std::chrono::duration<float>(end - start).count();
    std::cout << "Elapsed time: " << elapsed << " seconds" << std::endl;
    std::cout << "Sum: " << sum << std::endl;
    
    std::cout << "Test completed successfully!" << std::endl;
    return 0;
}
