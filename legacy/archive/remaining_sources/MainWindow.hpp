#pragma once

#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <memory>

namespace OmniCpp {

class RenderWidget;
class ControlPanel;

/**
 * @brief Main window for the engine editor
 * 
 * This class provides the main window for the OmniCpp engine editor,
 * containing the render widget and control panel.
 */
class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = nullptr);
    ~MainWindow() override;

    /**
     * @brief Initialize the main window
     * @return true if initialization succeeded, false otherwise
     */
    bool initialize();

private:
    void setupUI();
    void setupMenuBar();
    void setupStatusBar();

    std::unique_ptr<RenderWidget> m_renderWidget;
    std::unique_ptr<ControlPanel> m_controlPanel;
    QWidget* m_centralWidget;
    QHBoxLayout* m_mainLayout;
};

} // namespace OmniCpp
