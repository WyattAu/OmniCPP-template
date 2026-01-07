/**
 * @file audio_manager.hpp
 * @brief Audio management interface
 */

#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Audio {

  /**
   * @brief Audio configuration structure
   */
  struct AudioConfig {
    uint32_t sample_rate{ 44100 };
    uint32_t buffer_size{ 512 };
    uint32_t channels{ 2 };
  };

  /**
   * @brief Audio manager class
   */
  class AudioManager {
  public:
    AudioManager ();
    ~AudioManager ();

    AudioManager (const AudioManager&) = delete;
    AudioManager& operator= (const AudioManager&) = delete;

    AudioManager (AudioManager&&) noexcept;
    AudioManager& operator= (AudioManager&&) noexcept;

    bool initialize (const AudioConfig& config);
    void shutdown ();
    void update ();

    bool load_sound (const std::string& name, const std::string& path);
    bool play_sound (const std::string& name);
    bool stop_sound (const std::string& name);

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl;
  };

} // namespace OmniCpp::Engine::Audio
