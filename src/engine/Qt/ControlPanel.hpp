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
 * @brief Control panel for engine editor
 * 
 * This class provides a control panel with various controls
 * for the engine editor.
 */
class ControlPanel : public QWidget {
    Q_OBJECT

public:
    explicit ControlPanel(QWidget* parent = nullptr);
    ~ControlPanel() override;

    /**
     * @brief Initialize control panel
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

private:
    void setupUI();
    void setupSceneControls();
    void setupRenderControls();
    void setupPhysicsControls();
    void setupAudioControls();

    // Scene controls
    QGroupBox* m_sceneGroup;
    QPushButton* m_newSceneButton;
    QPushButton* m_loadSceneButton;
    QPushButton* m_saveSceneButton;

    // Render controls
    QGroupBox* m_renderGroup;
    QSlider* m_ambientLightSlider;
    QLabel* m_ambientLightLabel;
    QSlider* m_fovSlider;
    QLabel* m_fovLabel;

    // Physics controls
    QGroupBox* m_physicsGroup;
    QPushButton* m_enablePhysicsButton;
    QPushButton* m_disablePhysicsButton;
    QLabel* m_physicsStatusLabel;

    // Audio controls
    QGroupBox* m_audioGroup;
    QSlider* m_masterVolumeSlider;
    QLabel* m_masterVolumeLabel;
    QPushButton* m_muteButton;

    QVBoxLayout* m_mainLayout;
};

} // namespace OmniCpp
