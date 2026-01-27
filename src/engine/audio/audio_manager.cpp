/**
 * @file audio_manager.cpp
 * @brief Audio management implementation
 */

#include "engine/audio/audio_manager.hpp"
#include <mutex>
#include <unordered_map>
#include <spdlog/spdlog.h>

namespace OmniCpp::Engine::Audio {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct AudioManager::Impl {
    AudioConfig config;
    std::unordered_map<std::string, std::string> sounds;
    std::mutex mutex;
    bool initialized{ false };
  };

  AudioManager::AudioManager () : m_impl (std::make_unique<Impl> ()) {
  }

  AudioManager::~AudioManager () {
    shutdown ();
  }

  AudioManager::AudioManager (AudioManager&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  AudioManager& AudioManager::operator= (AudioManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool AudioManager::initialize (const AudioConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      spdlog::warn("AudioManager: Already initialized");
      return true;
    }

    m_impl->config = config;
    m_impl->sounds.clear ();
    m_impl->initialized = true;

    spdlog::info("AudioManager: Initialized");
    return true;
  }

  void AudioManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->sounds.clear ();
    m_impl->initialized = false;

    spdlog::info("AudioManager: Shutdown");
  }

  void AudioManager::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update audio state here
  }

  bool AudioManager::load_sound (const std::string& name, const std::string& path) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("AudioManager: Not initialized, cannot load sound: {}", name);
      return false;
    }

    m_impl->sounds[name] = path;
    spdlog::debug("AudioManager: Loaded sound '{}' from '{}'", name, path);
    return true;
  }

  bool AudioManager::play_sound (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("AudioManager: Not initialized, cannot play sound: {}", name);
      return false;
    }

    auto it = m_impl->sounds.find (name);
    if (it != m_impl->sounds.end ()) {
      spdlog::debug("AudioManager: Playing sound '{}'", name);
      return true;
    }
    spdlog::warn("AudioManager: Sound '{}' not found", name);
    return false;
  }

  bool AudioManager::stop_sound (const std::string& name) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      spdlog::error("AudioManager: Not initialized, cannot stop sound: {}", name);
      return false;
    }

    auto it = m_impl->sounds.find (name);
    if (it != m_impl->sounds.end ()) {
      spdlog::debug("AudioManager: Stopping sound '{}'", name);
      return true;
    }
    spdlog::warn("AudioManager: Sound '{}' not found", name);
    return false;
  }

} // namespace OmniCpp::Engine::Audio
