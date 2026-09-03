/**
 * @file IPlatform.hpp
 * @brief Platform subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for platform-specific operations.
 */

#ifndef OMNICPP_IPLATFORM_HPP
#define OMNICPP_IPLATFORM_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Platform types
 */
enum class PlatformType : uint32_t {
    WINDOWS = 0,
    LINUX = 1,
    MACOS = 2,
    UNKNOWN = 0xFFFFFFFF
};

/**
 * @brief Window configuration
 */
struct WindowConfig {
    int width;
    int height;
    const char* title;
    bool fullscreen;
    bool resizable;
    bool vsync;
};

/**
 * @brief Platform interface
 */
class IPlatform {
public:
    virtual ~IPlatform() = default;
    
    /**
     * @brief Initialize platform
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown platform
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Create a window
     * 
     * @param config Window configuration
     * @return Window handle (platform-specific), or nullptr on failure
     */
    virtual void* create_window(const WindowConfig& config) = 0;
    
    /**
     * @brief Destroy a window
     * 
     * @param window Window handle
     */
    virtual void destroy_window(void* window) = 0;
    
    /**
     * @brief Update window
     * 
     * @param window Window handle
     */
    virtual void update_window(void* window) = 0;
    
    /**
     * @brief Get platform type
     * 
     * @return Current platform type
     */
    virtual PlatformType get_platform_type() const = 0;
    
    /**
     * @brief Get time in seconds
     * 
     * @return Time since initialization in seconds
     */
    virtual double get_time() const = 0;
    
    /**
     * @brief Sleep for specified duration
     * 
     * @param seconds Duration in seconds
     */
    virtual void sleep(double seconds) = 0;
    
    /**
     * @brief Get executable path
     * 
     * @return Path to executable
     */
    virtual const char* get_executable_path() const = 0;
    
    /**
     * @brief Get working directory
     * 
     * @return Current working directory
     */
    virtual const char* get_working_directory() const = 0;
    
    /**
     * @brief Set working directory
     * 
     * @param path New working directory
     * @return True if successful, false otherwise
     */
    virtual bool set_working_directory(const char* path) = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IPLATFORM_HPP
