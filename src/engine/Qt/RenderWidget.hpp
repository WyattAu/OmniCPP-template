#pragma once

#include <QVulkanWindow>
#include <QVulkanWindowRenderer>
#include <memory>
#include <chrono>

namespace OmniCpp {

class QtVulkanIntegration;

/**
 * @brief Vulkan render widget
 * 
 * This class provides a Qt widget that renders Vulkan content.
 */
class RenderWidget : public QVulkanWindow {
    Q_OBJECT

public:
    explicit RenderWidget(QWindow* parent = nullptr);
    ~RenderWidget() override;

    /**
     * @brief Initialize render widget
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

protected:
    QVulkanWindowRenderer* createRenderer() override;

private:
    std::unique_ptr<QtVulkanIntegration> m_vulkanIntegration;
    std::chrono::time_point<std::chrono::high_resolution_clock> m_lastFrameTime;
    float m_deltaTime = 0.0f;
    int m_frameCount = 0;
    float m_fps = 0.0f;
};

/**
 * @brief Vulkan window renderer
 * 
 * This class handles the actual Vulkan rendering.
 */
class VulkanRenderer : public QVulkanWindowRenderer {
public:
    explicit VulkanRenderer(QVulkanWindow* window);
    ~VulkanRenderer() override;

    void preInitResources() override;
    void initResources() override;
    void releaseResources() override;
    void startNextFrame() override;

private:
    QVulkanWindow* m_window = nullptr;
    QVulkanDeviceFunctions* m_deviceFunctions = nullptr;
};

} // namespace OmniCpp
