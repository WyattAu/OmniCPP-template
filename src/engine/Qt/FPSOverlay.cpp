#include "Qt/FPSOverlay.hpp"
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logFPSOverlay, "omnicpp.fpsoverlay")

namespace OmniCpp {

FPSOverlay::FPSOverlay(QWidget* parent)
    : QWidget(parent)
    , m_fpsLabel(nullptr)
    , m_updateTimer(nullptr)
{
    qCDebug(logFPSOverlay) << "Creating FPSOverlay...";
}

FPSOverlay::~FPSOverlay()
{
    qCDebug(logFPSOverlay) << "Destroying FPSOverlay...";
}

void FPSOverlay::updateFPS(float fps)
{
    m_currentFPS = fps;
    m_fpsLabel->setText(QString("FPS: %1").arg(static_cast<int>(fps)));
}

void FPSOverlay::setupUI()
{
    qCDebug(logFPSOverlay) << "Setting up UI...";

    // Create FPS label
    m_fpsLabel = new QLabel("FPS: 0", this);
    m_fpsLabel->setStyleSheet(
        "QLabel {"
        "  background-color: rgba(0, 0, 0, 150);"
        "  color: white;"
        "  padding: 5px;"
        "  border-radius: 3px;"
        "  font-weight: bold;"
        "}"
    );

    // Create update timer
    m_updateTimer = new QTimer(this);
    connect(m_updateTimer, &QTimer::timeout, this, [this]() {
        m_fpsLabel->setText(QString("FPS: %1").arg(static_cast<int>(m_currentFPS)));
    });
    m_updateTimer->start(500); // Update every 500ms

    qCDebug(logFPSOverlay) << "UI setup complete";
}

} // namespace OmniCpp
