/**
 * @file Platform.cpp
 * @brief Stub implementation of platform subsystem
 * @version 1.0.0
 */

#include "engine/IPlatform.hpp"
#include <chrono>
#include <thread>

namespace omnicpp {

class PlatformStub : public IPlatform {
public:
    PlatformStub() = default;
    ~PlatformStub() override = default;

    bool initialize() override {
        return true;
    }

    void shutdown() override {
    }

    void* create_window(const WindowConfig& config) override {
        (void)config;
        return nullptr;
    }

    void destroy_window(void* window) override {
        (void)window;
    }

    void update_window(void* window) override {
        (void)window;
    }

    PlatformType get_platform_type() const override {
#ifdef _WIN32
        return PlatformType::WINDOWS;
#elif __linux__
        return PlatformType::LINUX;
#else
        return PlatformType::UNKNOWN;
#endif
    }

    double get_time() const override {
        auto now = std::chrono::high_resolution_clock::now();
        auto duration = now.time_since_epoch();
        return std::chrono::duration<double>(duration).count();
    }

    void sleep(double seconds) override {
        auto duration = std::chrono::duration<double>(seconds);
        std::this_thread::sleep_for(std::chrono::duration_cast<std::chrono::milliseconds>(duration));
    }

    const char* get_executable_path() const override {
        return "./";
    }

    const char* get_working_directory() const override {
        return "./";
    }

    bool set_working_directory(const char* path) override {
        (void)path;
        return true;
    }
};

} // namespace omnicpp
