# DES-025: Audio Manager Interface

## Overview
Defines the audio manager interface for the OmniCpp game engine.

## Interface Definition

### C++ Header

```cpp
#ifndef OMNICPP_AUDIO_MANAGER_INTERFACE_H
#define OMNICPP_AUDIO_MANAGER_INTERFACE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace omnicpp {
namespace engine {

// Forward declarations
class IAudioSource;
class IAudioListener;
class IAudioBuffer;

// Audio configuration
struct AudioConfig {
    int sample_rate;
    int channels;
    int buffer_size;
    bool enable_3d_audio;
    float doppler_factor;
    float speed_of_sound;
    int max_sources;

    AudioConfig()
        : sample_rate(44100)
        , channels(2)
        , buffer_size(4096)
        , enable_3d_audio(true)
        , doppler_factor(1.0f)
        , speed_of_sound(343.3f)
        , max_sources(32)
    {}
};

// Audio format
enum class AudioFormat {
    MONO8,
    MONO16,
    STEREO8,
    STEREO16
};

// Audio state
enum class AudioState {
    STOPPED,
    PLAYING,
    PAUSED
};

// Audio loop mode
enum class AudioLoopMode {
    NONE,
    LOOP,
    BIDIRECTIONAL
};

// Audio statistics
struct AudioStats {
    uint32_t active_sources;
    uint32_t total_sources;
    uint32_t buffers_loaded;
    double cpu_usage;
    double memory_usage;

    AudioStats()
        : active_sources(0)
        , total_sources(0)
        , buffers_loaded(0)
        , cpu_usage(0.0)
        , memory_usage(0.0)
    {}
};

// Audio manager interface
class IAudioManager {
public:
    virtual ~IAudioManager() = default;

    // Initialization
    virtual bool initialize(const AudioConfig& config) = 0;
    virtual void shutdown() = 0;

    // Update
    virtual void update(double delta_time) = 0;

    // Audio sources
    virtual uint32_t create_audio_source() = 0;
    virtual void destroy_audio_source(uint32_t source_id) = 0;
    virtual IAudioSource* get_audio_source(uint32_t source_id) = 0;
    virtual const IAudioSource* get_audio_source(uint32_t source_id) const = 0;

    // Audio buffers
    virtual uint32_t create_audio_buffer(const void* data, size_t size, AudioFormat format, int sample_rate) = 0;
    virtual void destroy_audio_buffer(uint32_t buffer_id) = 0;
    virtual IAudioBuffer* get_audio_buffer(uint32_t buffer_id) = 0;
    virtual const IAudioBuffer* get_audio_buffer(uint32_t buffer_id) const = 0;

    // Audio listeners
    virtual uint32_t create_audio_listener() = 0;
    virtual void destroy_audio_listener(uint32_t listener_id) = 0;
    virtual IAudioListener* get_audio_listener(uint32_t listener_id) = 0;
    virtual const IAudioListener* get_audio_listener(uint32_t listener_id) const = 0;
    virtual void set_active_listener(uint32_t listener_id) = 0;
    virtual uint32_t get_active_listener() const = 0;

    // Load audio from file
    virtual uint32_t load_audio_file(const std::string& file_path) = 0;
    virtual void unload_audio_file(uint32_t buffer_id) = 0;

    // Play/stop/pause
    virtual void play_audio(uint32_t source_id) = 0;
    virtual void stop_audio(uint32_t source_id) = 0;
    virtual void pause_audio(uint32_t source_id) = 0;
    virtual void resume_audio(uint32_t source_id) = 0;

    // Global volume
    virtual void set_master_volume(float volume) = 0;
    virtual float get_master_volume() const = 0;

    // 3D audio settings
    virtual void set_doppler_factor(float factor) = 0;
    virtual float get_doppler_factor() const = 0;
    virtual void set_speed_of_sound(float speed) = 0;
    virtual float get_speed_of_sound() const = 0;

    // Statistics
    virtual const AudioStats& get_stats() const = 0;
    virtual void reset_stats() = 0;

    // Configuration
    virtual const AudioConfig& get_config() const = 0;
    virtual void set_config(const AudioConfig& config) = 0;
};

// Audio source interface
class IAudioSource {
public:
    virtual ~IAudioSource() = default;

    virtual uint32_t get_id() const = 0;

    // Buffer
    virtual void set_buffer(uint32_t buffer_id) = 0;
    virtual uint32_t get_buffer() const = 0;

    // Playback
    virtual void play() = 0;
    virtual void stop() = 0;
    virtual void pause() = 0;
    virtual void resume() = 0;
    virtual AudioState get_state() const = 0;

    // Volume
    virtual void set_volume(float volume) = 0;
    virtual float get_volume() const = 0;

    // Pitch
    virtual void set_pitch(float pitch) = 0;
    virtual float get_pitch() const = 0;

    // Loop
    virtual void set_loop_mode(AudioLoopMode mode) = 0;
    virtual AudioLoopMode get_loop_mode() const = 0;

    // Position (3D)
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;

    // Velocity (3D)
    virtual void set_velocity(float x, float y, float z) = 0;
    virtual void get_velocity(float& x, float& y, float& z) const = 0;

    // Direction (3D)
    virtual void set_direction(float x, float y, float z) = 0;
    virtual void get_direction(float& x, float& y, float& z) const = 0;

    // Cone (3D)
    virtual void set_cone(float inner_angle, float outer_angle, float outer_gain) = 0;
    virtual void get_cone(float& inner_angle, float& outer_angle, float& outer_gain) const = 0;

    // Distance attenuation
    virtual void set_min_distance(float distance) = 0;
    virtual float get_min_distance() const = 0;
    virtual void set_max_distance(float distance) = 0;
    virtual float get_max_distance() const = 0;
    virtual void set_rolloff_factor(float factor) = 0;
    virtual float get_rolloff_factor() const = 0;

    // Priority
    virtual void set_priority(int priority) = 0;
    virtual int get_priority() const = 0;
};

// Audio listener interface
class IAudioListener {
public:
    virtual ~IAudioListener() = default;

    virtual uint32_t get_id() const = 0;

    // Position
    virtual void set_position(float x, float y, float z) = 0;
    virtual void get_position(float& x, float& y, float& z) const = 0;

    // Velocity
    virtual void set_velocity(float x, float y, float z) = 0;
    virtual void get_velocity(float& x, float& y, float& z) const = 0;

    // Orientation
    virtual void set_orientation(float forward_x, float forward_y, float forward_z,
                                 float up_x, float up_y, float up_z) = 0;
    virtual void get_orientation(float& forward_x, float& forward_y, float& forward_z,
                                float& up_x, float& up_y, float& up_z) const = 0;

    // Gain
    virtual void set_gain(float gain) = 0;
    virtual float get_gain() const = 0;
};

// Audio buffer interface
class IAudioBuffer {
public:
    virtual ~IAudioBuffer() = default;

    virtual uint32_t get_id() const = 0;

    // Format
    virtual AudioFormat get_format() const = 0;
    virtual int get_sample_rate() const = 0;
    virtual int get_channels() const = 0;
    virtual int get_bits_per_sample() const = 0;

    // Size
    virtual size_t get_size() const = 0;
    virtual size_t get_duration() const = 0;

    // Data
    virtual const void* get_data() const = 0;
    virtual void set_data(const void* data, size_t size) = 0;

    // Reference count
    virtual int get_reference_count() const = 0;
    virtual void add_reference() = 0;
    virtual void remove_reference() = 0;
};

// Audio manager factory
class IAudioManagerFactory {
public:
    virtual ~IAudioManagerFactory() = default;

    virtual std::unique_ptr<IAudioManager> create_audio_manager() = 0;
    virtual void destroy_audio_manager(std::unique_ptr<IAudioManager> audio_manager) = 0;
};

} // namespace engine
} // namespace omnicpp

#endif // OMNICPP_AUDIO_MANAGER_INTERFACE_H
```

## Dependencies

### Internal Dependencies
- `DES-021` - Engine Core Interfaces

### External Dependencies
- `cstdint` - Fixed-width integers
- `string` - String handling
- `vector` - Dynamic arrays
- `memory` - Smart pointers
- `functional` - Function objects

## Related Requirements
- REQ-037: Audio System Architecture
- REQ-038: 3D Audio Support

## Related ADRs
- ADR-002: C++ Engine Architecture

## Implementation Notes

### Audio Manager Design
1. Abstract audio API
2. Support multiple backends (OpenAL, FMOD, SDL_mixer)
3. Efficient resource management
4. 3D audio support

### Audio Sources
1. Create and destroy sources
2. Control playback state
3. Set volume and pitch
4. Support 3D positioning

### Audio Buffers
1. Load audio data
2. Support multiple formats
3. Reference counting
4. Memory management

### Audio Listeners
1. Position and orientation
2. Velocity tracking
3. Gain control
4. Multiple listeners

### 3D Audio
1. Positional audio
2. Velocity-based Doppler
3. Distance attenuation
4. Cone effects

## Usage Example

```cpp
#include "audio_manager_interface.hpp"

using namespace omnicpp::engine;

int main() {
    // Create audio configuration
    AudioConfig config;
    config.sample_rate = 44100;
    config.channels = 2;
    config.buffer_size = 4096;
    config.enable_3d_audio = true;
    config.doppler_factor = 1.0f;
    config.speed_of_sound = 343.3f;
    config.max_sources = 32;

    // Create audio manager
    auto audio_manager = std::make_unique<AudioManager>();

    // Initialize audio manager
    if (!audio_manager->initialize(config)) {
        std::cerr << "Failed to initialize audio manager" << std::endl;
        return 1;
    }

    // Load audio file
    uint32_t buffer_id = audio_manager->load_audio_file("sounds/explosion.wav");

    // Create audio source
    uint32_t source_id = audio_manager->create_audio_source();
    IAudioSource* source = audio_manager->get_audio_source(source_id);

    // Set buffer
    source->set_buffer(buffer_id);

    // Set 3D position
    source->set_position(10.0f, 0.0f, 0.0f);

    // Set volume
    source->set_volume(0.8f);

    // Play audio
    source->play();

    // Create audio listener
    uint32_t listener_id = audio_manager->create_audio_listener();
    IAudioListener* listener = audio_manager->get_audio_listener(listener_id);

    // Set listener position
    listener->set_position(0.0f, 0.0f, 0.0f);

    // Set active listener
    audio_manager->set_active_listener(listener_id);

    // Update audio
    double delta_time = 0.016; // 60 FPS
    audio_manager->update(delta_time);

    // Cleanup
    audio_manager->destroy_audio_source(source_id);
    audio_manager->unload_audio_file(buffer_id);
    audio_manager->destroy_audio_listener(listener_id);
    audio_manager->shutdown();

    return 0;
}
```
