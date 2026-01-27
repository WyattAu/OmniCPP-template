/**
 * @file Renderer.cpp
 * @brief Stub implementation of renderer subsystem
 * @version 1.0.0
 */

#include "engine/IRenderer.hpp"
#include <spdlog/spdlog.h>

namespace omnicpp {

class RendererStub : public IRenderer {
public:
    RendererStub() = default;
    ~RendererStub() override = default;

    bool initialize() override {
        spdlog::info("Renderer initialized");
        return true;
    }

    void shutdown() override {
        spdlog::info("Renderer shutdown");
    }

    bool begin_frame() override {
        return true;
    }

    void end_frame() override {
        m_frame_number++;
    }

    uint32_t get_frame_number() const noexcept override {
        return m_frame_number;
    }

private:
    uint32_t m_frame_number = 0;
};

} // namespace omnicpp
