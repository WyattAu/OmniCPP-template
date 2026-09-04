#include <iostream>

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
};

class Ball {
public:
    Vec3 position;
    Vec3 velocity;
    float radius;
    
    Ball(float x, float y, float z, float r)
        : position{x, y, z}, velocity{0.0f, 0.0f, 0.0f}, radius(r) {}
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
    
    std::cout << "Test completed successfully!" << std::endl;
    return 0;
}
