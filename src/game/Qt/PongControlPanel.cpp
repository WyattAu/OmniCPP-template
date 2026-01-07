#include "Qt/PongControlPanel.hpp"
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logPongControlPanel, "omnicpp.pongcontrolpanel")

namespace OmniCpp {

PongControlPanel::PongControlPanel(QWidget* parent)
    : QWidget(parent)
    , m_mainLayout(nullptr)
{
    qCDebug(logPongControlPanel) << "Creating PongControlPanel...";
}

PongControlPanel::~PongControlPanel()
{
    qCDebug(logPongControlPanel) << "Destroying PongControlPanel...";
}

bool PongControlPanel::initialize()
{
    qCDebug(logPongControlPanel) << "Initializing PongControlPanel...";

    setupUI();

    qCDebug(logPongControlPanel) << "PongControlPanel initialized successfully";
    return true;
}

void PongControlPanel::setupUI()
{
    qCDebug(logPongControlPanel) << "Setting up UI...";

    // Create main layout
    m_mainLayout = new QVBoxLayout(this);
    m_mainLayout->setContentsMargins(10, 10, 10, 10);
    m_mainLayout->setSpacing(10);

    // Setup control groups
    setupGameControls();
    setupRenderControls();
    setupAudioControls();

    // Add stretch to push controls to top
    m_mainLayout->addStretch();

    qCDebug(logPongControlPanel) << "UI setup complete";
}

void PongControlPanel::setupGameControls()
{
    qCDebug(logPongControlPanel) << "Setting up game controls...";

    // Create game group
    m_gameGroup = new QGroupBox("Game", this);
    QVBoxLayout* gameLayout = new QVBoxLayout(m_gameGroup);

    // Create buttons
    m_newGameButton = new QPushButton("New Game", this);
    m_pauseButton = new QPushButton("Pause", this);
    m_resetButton = new QPushButton("Reset", this);
    m_scoreLabel = new QLabel("Score: 0 - 0", this);

    // Connect signals
    connect(m_newGameButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logPongControlPanel) << "New game";
    });
    connect(m_pauseButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logPongControlPanel) << "Pause game";
    });
    connect(m_resetButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logPongControlPanel) << "Reset game";
    });

    // Add to layout
    gameLayout->addWidget(m_scoreLabel);
    gameLayout->addWidget(m_newGameButton);
    gameLayout->addWidget(m_pauseButton);
    gameLayout->addWidget(m_resetButton);

    // Add to main layout
    m_mainLayout->addWidget(m_gameGroup);

    qCDebug(logPongControlPanel) << "Game controls setup complete";
}

void PongControlPanel::setupRenderControls()
{
    qCDebug(logPongControlPanel) << "Setting up render controls...";

    // Create render group
    m_renderGroup = new QGroupBox("Render", this);
    QFormLayout* renderLayout = new QFormLayout(m_renderGroup);

    // Ball speed slider
    m_ballSpeedSlider = new QSlider(Qt::Horizontal, this);
    m_ballSpeedSlider->setRange(1, 20);
    m_ballSpeedSlider->setValue(8);
    m_ballSpeedLabel = new QLabel("8", this);

    connect(m_ballSpeedSlider, &QSlider::valueChanged, this, [this](int value) {
        m_ballSpeedLabel->setText(QString("%1").arg(value));
        qCDebug(logPongControlPanel) << "Ball speed:" << value;
    });

    renderLayout->addRow("Ball Speed:", m_ballSpeedLabel);
    renderLayout->addRow(m_ballSpeedSlider);

    // Paddle speed slider
    m_paddleSpeedSlider = new QSlider(Qt::Horizontal, this);
    m_paddleSpeedSlider->setRange(1, 10);
    m_paddleSpeedSlider->setValue(5);
    m_paddleSpeedLabel = new QLabel("5", this);

    connect(m_paddleSpeedSlider, &QSlider::valueChanged, this, [this](int value) {
        m_paddleSpeedLabel->setText(QString("%1").arg(value));
        qCDebug(logPongControlPanel) << "Paddle speed:" << value;
    });

    renderLayout->addRow("Paddle Speed:", m_paddleSpeedLabel);
    renderLayout->addRow(m_paddleSpeedSlider);

    // Add to main layout
    m_mainLayout->addWidget(m_renderGroup);

    qCDebug(logPongControlPanel) << "Render controls setup complete";
}

void PongControlPanel::setupAudioControls()
{
    qCDebug(logPongControlPanel) << "Setting up audio controls...";

    // Create audio group
    m_audioGroup = new QGroupBox("Audio", this);
    QVBoxLayout* audioLayout = new QVBoxLayout(m_audioGroup);

    // Master volume slider
    m_masterVolumeSlider = new QSlider(Qt::Horizontal, this);
    m_masterVolumeSlider->setRange(0, 100);
    m_masterVolumeSlider->setValue(80);
    m_masterVolumeLabel = new QLabel("80%", this);

    connect(m_masterVolumeSlider, &QSlider::valueChanged, this, [this](int value) {
        m_masterVolumeLabel->setText(QString("%1%").arg(value));
        qCDebug(logPongControlPanel) << "Master volume:" << value;
    });

    // Mute button
    m_muteButton = new QPushButton("Mute", this);

    connect(m_muteButton, &QPushButton::clicked, this, [this]() {
        static bool muted = false;
        muted = !muted;
        m_muteButton->setText(muted ? "Unmute" : "Mute");
        qCDebug(logPongControlPanel) << "Mute:" << muted;
    });

    // Add to layout
    audioLayout->addWidget(m_masterVolumeLabel);
    audioLayout->addWidget(m_masterVolumeSlider);
    audioLayout->addWidget(m_muteButton);

    // Add to main layout
    m_mainLayout->addWidget(m_audioGroup);

    qCDebug(logPongControlPanel) << "Audio controls setup complete";
}

} // namespace OmniCpp
