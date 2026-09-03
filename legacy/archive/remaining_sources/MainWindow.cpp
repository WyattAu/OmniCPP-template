#include "Qt/MainWindow.hpp"
#include "Qt/RenderWidget.hpp"
#include "Qt/ControlPanel.hpp"
#include <QMenuBar>
#include <QStatusBar>
#include <QApplication>
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logMainWindow, "omnicpp.mainwindow")

namespace OmniCpp {

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
    , m_centralWidget(nullptr)
    , m_mainLayout(nullptr)
{
    qCDebug(logMainWindow) << "Creating MainWindow...";
}

MainWindow::~MainWindow()
{
    qCDebug(logMainWindow) << "Destroying MainWindow...";
}

bool MainWindow::initialize()
{
    qCDebug(logMainWindow) << "Initializing MainWindow...";

    setupUI();
    setupMenuBar();
    setupStatusBar();

    // Initialize render widget
    if (!m_renderWidget->initialize()) {
        qCCritical(logMainWindow) << "Failed to initialize render widget";
        return false;
    }

    // Initialize control panel
    if (!m_controlPanel->initialize()) {
        qCCritical(logMainWindow) << "Failed to initialize control panel";
        return false;
    }

    qCDebug(logMainWindow) << "MainWindow initialized successfully";
    return true;
}

void MainWindow::setupUI()
{
    qCDebug(logMainWindow) << "Setting up UI...";

    // Create central widget
    m_centralWidget = new QWidget(this);
    setCentralWidget(m_centralWidget);

    // Create main layout
    m_mainLayout = new QHBoxLayout(m_centralWidget);
    m_mainLayout->setContentsMargins(0, 0, 0, 0);
    m_mainLayout->setSpacing(0);

    // Create render widget
    m_renderWidget = std::make_unique<RenderWidget>(this);
    m_mainLayout->addWidget(m_renderWidget.get(), 3); // 3/4 of the width

    // Create control panel
    m_controlPanel = std::make_unique<ControlPanel>(this);
    m_mainLayout->addWidget(m_controlPanel.get(), 1); // 1/4 of the width

    // Set window properties
    setWindowTitle("OmniCpp Engine Editor");
    resize(1280, 720);

    qCDebug(logMainWindow) << "UI setup complete";
}

void MainWindow::setupMenuBar()
{
    qCDebug(logMainWindow) << "Setting up menu bar...";

    // Create menu bar
    QMenuBar* menuBar = new QMenuBar(this);
    setMenuBar(menuBar);

    // File menu
    QMenu* fileMenu = menuBar->addMenu("&File");

    QAction* newAction = fileMenu->addAction("&New");
    newAction->setShortcut(QKeySequence::New);
    connect(newAction, &QAction::triggered, this, [this]() {
        qCDebug(logMainWindow) << "New project";
    });

    QAction* openAction = fileMenu->addAction("&Open");
    openAction->setShortcut(QKeySequence::Open);
    connect(openAction, &QAction::triggered, this, [this]() {
        qCDebug(logMainWindow) << "Open project";
    });

    QAction* saveAction = fileMenu->addAction("&Save");
    saveAction->setShortcut(QKeySequence::Save);
    connect(saveAction, &QAction::triggered, this, [this]() {
        qCDebug(logMainWindow) << "Save project";
    });

    fileMenu->addSeparator();

    QAction* exitAction = fileMenu->addAction("E&xit");
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &QMainWindow::close);

    // Edit menu
    QMenu* editMenu = menuBar->addMenu("&Edit");

    QAction* undoAction = editMenu->addAction("&Undo");
    undoAction->setShortcut(QKeySequence::Undo);
    connect(undoAction, &QAction::triggered, this, [this]() {
        qCDebug(logMainWindow) << "Undo";
    });

    QAction* redoAction = editMenu->addAction("&Redo");
    redoAction->setShortcut(QKeySequence::Redo);
    connect(redoAction, &QAction::triggered, this, [this]() {
        qCDebug(logMainWindow) << "Redo";
    });

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
        qCDebug(logMainWindow) << "About";
    });

    qCDebug(logMainWindow) << "Menu bar setup complete";
}

void MainWindow::setupStatusBar()
{
    qCDebug(logMainWindow) << "Setting up status bar...";

    QStatusBar* statusBar = new QStatusBar(this);
    setStatusBar(statusBar);
    statusBar->showMessage("Ready");

    qCDebug(logMainWindow) << "Status bar setup complete";
}

} // namespace OmniCpp
