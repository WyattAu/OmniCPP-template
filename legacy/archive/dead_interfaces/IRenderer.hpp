/**
 * @file IRenderer.hpp
 * @brief Renderer subsystem interface for OmniCpp engine
 * @version 1.0.0
 * 
 * This interface defines the contract for the rendering subsystem.
 */

#ifndef OMNICPP_IRENDERER_HPP
#define OMNICPP_IRENDERER_HPP

#include <cstdint>

namespace omnicpp {

/**
 * @brief Renderer subsystem interface
 */
class IRenderer {
public:
    virtual ~IRenderer() = default;
    
    /**
     * @brief Initialize the renderer
     * 
     * @return True if successful, false otherwise
     */
    virtual bool initialize() = 0;
    
    /**
     * @brief Shutdown the renderer
     */
    virtual void shutdown() = 0;
    
    /**
     * @brief Begin a new frame
     * 
     * @return True if successful, false otherwise
     */
    virtual bool begin_frame() = 0;
    
    /**
     * @brief End the current frame
     */
    virtual void end_frame() = 0;
    
    /**
     * @brief Get the current frame number
     * 
     * @return Frame number
     */
    virtual uint32_t get_frame_number() const = 0;
};

} // namespace omnicpp

#endif // OMNICPP_IRENDERER_HPP
