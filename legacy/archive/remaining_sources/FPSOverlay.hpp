#pragma once

#include <QWidget>
#include <QLabel>
#include <QTimer>
#include <memory>

namespace OmniCpp {

/**
 * @brief FPS overlay widget
 * 
 * This class provides an overlay that displays the current FPS.
 */
class FPSOverlay : public QWidget {
    Q_OBJECT

public:
    explicit FPSOverlay(QWidget* parent = nullptr);
    ~FPSOverlay() override;

    /**
     * @brief Update FPS display
     * @param fps Current FPS value
     */
    void updateFPS(float fps);

private:
    void setupUI();

    QLabel* m_fpsLabel;
    QTimer* m_updateTimer;
    float m_currentFPS = 0.0f;
};

} // namespace OmniCpp
