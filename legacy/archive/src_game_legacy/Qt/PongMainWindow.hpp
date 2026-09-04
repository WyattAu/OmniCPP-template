#pragma once

#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <memory>

namespace OmniCpp {

class PongRenderWidget;
class PongControlPanel;

/**
 * @brief Main window for 3D Pong game
 * 
 * This class provides main window for 3D Pong game,
 * containing render widget and control panel.
 */
class PongMainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit PongMainWindow(QWidget* parent = nullptr);
    ~PongMainWindow() override;

    /**
     * @brief Initialize main window
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

private:
    void setupUI();
    void setupMenuBar();
    void setupStatusBar();

    std::unique_ptr<PongRenderWidget> m_renderWidget;
    std::unique_ptr<PongControlPanel> m_controlPanel;
    QWidget* m_centralWidget;
    QHBoxLayout* m_mainLayout;
};

} // namespace OmniCpp
