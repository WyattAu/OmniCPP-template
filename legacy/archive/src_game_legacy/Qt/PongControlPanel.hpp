#pragma once

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSlider>
#include <QGroupBox>
#include <QFormLayout>

namespace OmniCpp {

/**
 * @brief Control panel for 3D Pong game
 * 
 * This class provides a control panel with various controls
 * for the 3D Pong game.
 */
class PongControlPanel : public QWidget {
    Q_OBJECT

public:
    explicit PongControlPanel(QWidget* parent = nullptr);
    ~PongControlPanel() override;

    /**
     * @brief Initialize control panel
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

private:
    void setupUI();
    void setupGameControls();
    void setupRenderControls();
    void setupAudioControls();

    // Game controls
    QGroupBox* m_gameGroup;
    QPushButton* m_newGameButton;
    QPushButton* m_pauseButton;
    QPushButton* m_resetButton;
    QLabel* m_scoreLabel;

    // Render controls
    QGroupBox* m_renderGroup;
    QSlider* m_ballSpeedSlider;
    QLabel* m_ballSpeedLabel;
    QSlider* m_paddleSpeedSlider;
    QLabel* m_paddleSpeedLabel;

    // Audio controls
    QGroupBox* m_audioGroup;
    QSlider* m_masterVolumeSlider;
    QLabel* m_masterVolumeLabel;
    QPushButton* m_muteButton;

    QVBoxLayout* m_mainLayout;
};

} // namespace OmniCpp
