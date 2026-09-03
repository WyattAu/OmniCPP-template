#include "Qt/PongRenderWidget.hpp"
#include <QVulkanInstance>
#include <QVulkanDeviceFunctions>
#include <QLoggingCategory>
#include <cmath>

Q_LOGGING_CATEGORY(logPongRenderWidget, "omnicpp.pongrenderwidget")

namespace OmniCpp {

// ============================================================================
// PongRenderWidget Implementation
// ============================================================================

PongRenderWidget::PongRenderWidget(QWindow* parent)
    : QVulkanWindow(parent)
{
    qCDebug(logPongRenderWidget) << "Creating PongRenderWidget...";
}

PongRenderWidget::~PongRenderWidget()
{
    qCDebug(logPongRenderWidget) << "Destroying PongRenderWidget...";
}

bool PongRenderWidget::initialize()
{
    qCDebug(logPongRenderWidget) << "Initializing PongRenderWidget...";

    // Initialize timer for FPS calculation
    m_lastFrameTime = std::chrono::high_resolution_clock::now();

    qCDebug(logPongRenderWidget) << "PongRenderWidget initialized successfully";
    return true;
}

QVulkanWindowRenderer* PongRenderWidget::createRenderer()
{
    qCDebug(logPongRenderWidget) << "Creating PongVulkanRenderer...";
    return new PongVulkanRenderer(this);
}

// ============================================================================
// PongVulkanRenderer Implementation
// ============================================================================

PongVulkanRenderer::PongVulkanRenderer(QVulkanWindow* window)
    : m_window(window)
{
    qCDebug(logPongRenderWidget) << "Creating PongVulkanRenderer...";
}

PongVulkanRenderer::~PongVulkanRenderer()
{
    qCDebug(logPongRenderWidget) << "Destroying PongVulkanRenderer...";
}

void PongVulkanRenderer::preInitResources()
{
    qCDebug(logPongRenderWidget) << "Pre-initializing Vulkan resources...";

    // Get device functions
    m_deviceFunctions = m_window->vulkanInstance()->deviceFunctions(m_window->device());
    if (!m_deviceFunctions) {
        qCCritical(logPongRenderWidget) << "Failed to get device functions";
        return;
    }

    qCDebug(logPongRenderWidget) << "Vulkan resources pre-initialized";
}

void PongVulkanRenderer::initResources()
{
    qCDebug(logPongRenderWidget) << "Initializing Vulkan resources...";

    // Initialize render pass, pipeline, etc.
    // This is a minimal implementation for demonstration

    qCDebug(logPongRenderWidget) << "Vulkan resources initialized";
}

void PongVulkanRenderer::releaseResources()
{
    qCDebug(logPongRenderWidget) << "Releasing Vulkan resources...";

    // Clean up Vulkan resources
    // This is a minimal implementation for demonstration

    qCDebug(logPongRenderWidget) << "Vulkan resources released";
}

void PongVulkanRenderer::startNextFrame()
{
    // Get current time
    auto currentTime = std::chrono::high_resolution_clock::now();
    float deltaTime = std::chrono::duration<float>(currentTime - m_window->renderer()->m_lastFrameTime).count();
    m_window->renderer()->m_lastFrameTime = currentTime;

    // Update FPS
    m_window->renderer()->m_frameCount++;
    if (m_window->renderer()->m_frameCount % 60 == 0) {
        m_window->renderer()->m_fps = 1.0f / deltaTime;
        qCDebug(logPongRenderWidget) << "FPS:" << m_window->renderer()->m_fps;
    }

    // Render frame
    // This is a minimal implementation for demonstration
    // In a full implementation, you would:
    // 1. Begin command buffer
    // 2. Begin render pass
    // 3. Bind pipeline
    // 4. Draw geometry (paddles and ball)
    // 5. End render pass
    // 6. End command buffer
    // 7. Submit command buffer
    // 8. Present swapchain image

    // For now, just clear the screen with a dark blue background
    VkClearValue clearColor = {{{0.0f, 0.0f, 0.2f, 1.0f}}};
    m_window->frameReady();
    m_window->requestUpdate();
}

} // namespace OmniCpp
