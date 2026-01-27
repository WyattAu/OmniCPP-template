#include "Qt/ControlPanel.hpp"
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logControlPanel, "omnicpp.controlpanel")

namespace OmniCpp {

ControlPanel::ControlPanel(QWidget* parent)
    : QWidget(parent)
    , m_mainLayout(nullptr)
{
    qCDebug(logControlPanel) << "Creating ControlPanel...";
}

ControlPanel::~ControlPanel()
{
    qCDebug(logControlPanel) << "Destroying ControlPanel...";
}

bool ControlPanel::initialize()
{
    qCDebug(logControlPanel) << "Initializing ControlPanel...";

    setupUI();

    qCDebug(logControlPanel) << "ControlPanel initialized successfully";
    return true;
}

void ControlPanel::setupUI()
{
    qCDebug(logControlPanel) << "Setting up UI...";

    // Create main layout
    m_mainLayout = new QVBoxLayout(this);
    m_mainLayout->setContentsMargins(10, 10, 10, 10);
    m_mainLayout->setSpacing(10);

    // Setup control groups
    setupSceneControls();
    setupRenderControls();
    setupPhysicsControls();
    setupAudioControls();

    // Add stretch to push controls to top
    m_mainLayout->addStretch();

    qCDebug(logControlPanel) << "UI setup complete";
}

void ControlPanel::setupSceneControls()
{
    qCDebug(logControlPanel) << "Setting up scene controls...";

    // Create scene group
    m_sceneGroup = new QGroupBox("Scene", this);
    QVBoxLayout* sceneLayout = new QVBoxLayout(m_sceneGroup);

    // Create buttons
    m_newSceneButton = new QPushButton("New Scene", this);
    m_loadSceneButton = new QPushButton("Load Scene", this);
    m_saveSceneButton = new QPushButton("Save Scene", this);

    // Connect signals
    connect(m_newSceneButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logControlPanel) << "New scene";
    });
    connect(m_loadSceneButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logControlPanel) << "Load scene";
    });
    connect(m_saveSceneButton, &QPushButton::clicked, this, [this]() {
        qCDebug(logControlPanel) << "Save scene";
    });

    // Add to layout
    sceneLayout->addWidget(m_newSceneButton);
    sceneLayout->addWidget(m_loadSceneButton);
    sceneLayout->addWidget(m_saveSceneButton);

    // Add to main layout
    m_mainLayout->addWidget(m_sceneGroup);

    qCDebug(logControlPanel) << "Scene controls setup complete";
}

void ControlPanel::setupRenderControls()
{
    qCDebug(logControlPanel) << "Setting up render controls...";

    // Create render group
    m_renderGroup = new QGroupBox("Render", this);
    QFormLayout* renderLayout = new QFormLayout(m_renderGroup);

    // Ambient light slider
    m_ambientLightSlider = new QSlider(Qt::Horizontal, this);
    m_ambientLightSlider->setRange(0, 100);
    m_ambientLightSlider->setValue(50);
    m_ambientLightLabel = new QLabel("50%", this);

    connect(m_ambientLightSlider, &QSlider::valueChanged, this, [this](int value) {
        m_ambientLightLabel->setText(QString("%1%").arg(value));
        qCDebug(logControlPanel) << "Ambient light:" << value;
    });

    renderLayout->addRow("Ambient Light:", m_ambientLightLabel);
    renderLayout->addRow(m_ambientLightSlider);

    // FOV slider
    m_fovSlider = new QSlider(Qt::Horizontal, this);
    m_fovSlider->setRange(30, 120);
    m_fovSlider->setValue(90);
    m_fovLabel = new QLabel("90°", this);

    connect(m_fovSlider, &QSlider::valueChanged, this, [this](int value) {
        m_fovLabel->setText(QString("%1°").arg(value));
        qCDebug(logControlPanel) << "FOV:" << value;
    });

    renderLayout->addRow("Field of View:", m_fovLabel);
    renderLayout->addRow(m_fovSlider);

    // Add to main layout
    m_mainLayout->addWidget(m_renderGroup);

    qCDebug(logControlPanel) << "Render controls setup complete";
}

void ControlPanel::setupPhysicsControls()
{
    qCDebug(logControlPanel) << "Setting up physics controls...";

    // Create physics group
    m_physicsGroup = new QGroupBox("Physics", this);
    QVBoxLayout* physicsLayout = new QVBoxLayout(m_physicsGroup);

    // Create buttons
    m_enablePhysicsButton = new QPushButton("Enable Physics", this);
    m_disablePhysicsButton = new QPushButton("Disable Physics", this);
    m_physicsStatusLabel = new QLabel("Physics: Disabled", this);

    // Connect signals
    connect(m_enablePhysicsButton, &QPushButton::clicked, this, [this]() {
        m_physicsStatusLabel->setText("Physics: Enabled");
        qCDebug(logControlPanel) << "Physics enabled";
    });
    connect(m_disablePhysicsButton, &QPushButton::clicked, this, [this]() {
        m_physicsStatusLabel->setText("Physics: Disabled");
        qCDebug(logControlPanel) << "Physics disabled";
    });

    // Add to layout
    physicsLayout->addWidget(m_physicsStatusLabel);
    physicsLayout->addWidget(m_enablePhysicsButton);
    physicsLayout->addWidget(m_disablePhysicsButton);

    // Add to main layout
    m_mainLayout->addWidget(m_physicsGroup);

    qCDebug(logControlPanel) << "Physics controls setup complete";
}

void ControlPanel::setupAudioControls()
{
    qCDebug(logControlPanel) << "Setting up audio controls...";

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
        qCDebug(logControlPanel) << "Master volume:" << value;
    });

    // Mute button
    m_muteButton = new QPushButton("Mute", this);

    connect(m_muteButton, &QPushButton::clicked, this, [this]() {
        static bool muted = false;
        muted = !muted;
        m_muteButton->setText(muted ? "Unmute" : "Mute");
        qCDebug(logControlPanel) << "Mute:" << muted;
    });

    // Add to layout
    audioLayout->addWidget(m_masterVolumeLabel);
    audioLayout->addWidget(m_masterVolumeSlider);
    audioLayout->addWidget(m_muteButton);

    // Add to main layout
    m_mainLayout->addWidget(m_audioGroup);

    qCDebug(logControlPanel) << "Audio controls setup complete";
}

} // namespace OmniCpp
