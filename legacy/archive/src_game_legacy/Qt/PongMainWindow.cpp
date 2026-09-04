#include "Qt/PongMainWindow.hpp"
#include "Qt/PongRenderWidget.hpp"
#include "Qt/PongControlPanel.hpp"
#include <QMenuBar>
#include <QStatusBar>
#include <QApplication>
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logPongMainWindow, "omnicpp.pongmainwindow")

namespace OmniCpp {

PongMainWindow::PongMainWindow(QWidget* parent)
    : QMainWindow(parent)
    , m_centralWidget(nullptr)
    , m_mainLayout(nullptr)
{
    qCDebug(logPongMainWindow) << "Creating PongMainWindow...";
}

PongMainWindow::~PongMainWindow()
{
    qCDebug(logPongMainWindow) << "Destroying PongMainWindow...";
}

bool PongMainWindow::initialize()
{
    qCDebug(logPongMainWindow) << "Initializing PongMainWindow...";

    setupUI();
    setupMenuBar();
    setupStatusBar();

    // Initialize render widget
    if (!m_renderWidget->initialize()) {
        qCCritical(logPongMainWindow) << "Failed to initialize render widget";
        return false;
    }

    // Initialize control panel
    if (!m_controlPanel->initialize()) {
        qCCritical(logPongMainWindow) << "Failed to initialize control panel";
        return false;
    }

    qCDebug(logPongMainWindow) << "PongMainWindow initialized successfully";
    return true;
}

void PongMainWindow::setupUI()
{
    qCDebug(logPongMainWindow) << "Setting up UI...";

    // Create central widget
    m_centralWidget = new QWidget(this);
    setCentralWidget(m_centralWidget);

    // Create main layout
    m_mainLayout = new QHBoxLayout(m_centralWidget);
    m_mainLayout->setContentsMargins(0, 0, 0, 0);
    m_mainLayout->setSpacing(0);

    // Create render widget
    m_renderWidget = std::make_unique<PongRenderWidget>(this);
    m_mainLayout->addWidget(m_renderWidget.get(), 3); // 3/4 of width

    // Create control panel
    m_controlPanel = std::make_unique<PongControlPanel>(this);
    m_mainLayout->addWidget(m_controlPanel.get(), 1); // 1/4 of width

    // Set window properties
    setWindowTitle("OmniCpp 3D Pong");
    resize(1280, 720);

    qCDebug(logPongMainWindow) << "UI setup complete";
}

void PongMainWindow::setupMenuBar()
{
    qCDebug(logPongMainWindow) << "Setting up menu bar...";

    // Create menu bar
    QMenuBar* menuBar = new QMenuBar(this);
    setMenuBar(menuBar);

    // Game menu
    QMenu* gameMenu = menuBar->addMenu("&Game");

    QAction* newGameAction = gameMenu->addAction("&New Game");
    newGameAction->setShortcut(QKeySequence::New);
    connect(newGameAction, &QAction::triggered, this, [this]() {
        qCDebug(logPongMainWindow) << "New game";
    });

    QAction* pauseAction = gameMenu->addAction("&Pause");
    pauseAction->setShortcut(QKeySequence("Space"));
    connect(pauseAction, &QAction::triggered, this, [this]() {
        qCDebug(logPongMainWindow) << "Pause game";
    });

    gameMenu->addSeparator();

    QAction* exitAction = gameMenu->addAction("E&xit");
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &QMainWindow::close);

    // View menu
    QMenu* viewMenu = menuBar->addMenu("&View");

    QAction* fullscreenAction = viewMenu->addAction("&Fullscreen");
    fullscreenAction->setShortcut(QKeySequence::FullScreen);
    connect(fullscreenAction, &QAction::triggered, this, [this]() {
        if (isFullScreen()) {
            showNormal();
        } else {
            showFullScreen();
        }
    });

    // Help menu
    QMenu* helpMenu = menuBar->addMenu("&Help");

    QAction* aboutAction = helpMenu->addAction("&About");
    connect(aboutAction, &QAction::triggered, this, [this]() {
        qCDebug(logPongMainWindow) << "About";
    });

    qCDebug(logPongMainWindow) << "Menu bar setup complete";
}

void PongMainWindow::setupStatusBar()
{
    qCDebug(logPongMainWindow) << "Setting up status bar...";

    QStatusBar* statusBar = new QStatusBar(this);
    setStatusBar(statusBar);
    statusBar->showMessage("Ready");

    qCDebug(logPongMainWindow) << "Status bar setup complete";
}

} // namespace OmniCpp
