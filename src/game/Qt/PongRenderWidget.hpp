#pragma once

#include <QVulkanWindow>
#include <QVulkanWindowRenderer>
#include <memory>
#include <chrono>

namespace OmniCpp {

/**
 * @brief Vulkan render widget for 3D Pong game
 * 
 * This class provides a Qt widget that renders 3D Pong game using Vulkan.
 */
class PongRenderWidget : public QVulkanWindow {
    Q_OBJECT

public:
    explicit PongRenderWidget(QWindow* parent = nullptr);
    ~PongRenderWidget() override;

    /**
     * @brief Initialize render widget
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

protected:
    QVulkanWindowRenderer* createRenderer() override;

private:
    std::chrono::time_point<std::chrono::high_resolution_clock> m_lastFrameTime;
    float m_deltaTime = 0.0f;
    int m_frameCount = 0;
    float m_fps = 0.0f;
};

/**
 * @brief Vulkan window renderer for 3D Pong game
 * 
 * This class handles actual Vulkan rendering for the 3D Pong game.
 */
class PongVulkanRenderer : public QVulkanWindowRenderer {
public:
    explicit PongVulkanRenderer(QVulkanWindow* window);
    ~PongVulkanRenderer() override;

    void preInitResources() override;
    void initResources() override;
    void releaseResources() override;
    void startNextFrame() override;

private:
    QVulkanWindow* m_window = nullptr;
    QVulkanDeviceFunctions* m_deviceFunctions = nullptr;
};

} // namespace OmniCpp
