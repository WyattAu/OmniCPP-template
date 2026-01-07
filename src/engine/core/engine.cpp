/**
 * @file engine.cpp
 * @brief Core engine implementation
 */

#include "engine/core/engine.hpp"
#include "engine/audio/audio_manager.hpp"
#include "engine/events/event_manager.hpp"
#include "engine/graphics/renderer.hpp"
#include "engine/input/input_manager.hpp"
#include "engine/logging/logger.hpp"
#include "engine/memory/memory_manager.hpp"
#include "engine/network/network_manager.hpp"
#include "engine/physics/physics_engine.hpp"
#include "engine/platform/platform.hpp"
#include "engine/resources/resource_manager.hpp"
#include "engine/scene/scene_manager.hpp"
#include "engine/scripting/script_manager.hpp"
#include "engine/window/window_manager.hpp"
#include <chrono>
#include <thread>

namespace OmniCpp::Engine::Core {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct Engine::Impl {
    EngineConfig config;
    bool running{ false };
    std::unique_ptr<Logging::Logger> logger;
    std::unique_ptr<Memory::MemoryManager> memory_manager;
    std::unique_ptr<Events::EventManager> event_manager;
    std::unique_ptr<Input::InputManager> input_manager;
    std::unique_ptr<Window::WindowManager> window_manager;
    std::unique_ptr<Graphics::Renderer> renderer;
    std::unique_ptr<Audio::AudioManager> audio_manager;
    std::unique_ptr<Resources::ResourceManager> resource_manager;
    std::unique_ptr<Physics::PhysicsEngine> physics_engine;
    std::unique_ptr<Scene::SceneManager> scene_manager;
    std::unique_ptr<Scripting::ScriptManager> script_manager;
    std::unique_ptr<Network::NetworkManager> network_manager;
    std::unique_ptr<Platform::Platform> platform;

    std::chrono::steady_clock::time_point last_frame_time;
    float accumulated_time{ 0.0f };
    uint64_t frame_count{ 0 };
  };

  Engine::Engine () : m_impl (std::make_unique<Impl> ()) {
    // Constructor implementation
  }

  Engine::~Engine () {
    shutdown ();
  }

  Engine::Engine (Engine&& other) noexcept : m_impl (std::move (other.m_impl)) {
    // Move constructor
  }

  Engine& Engine::operator= (Engine&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool Engine::initialize (const EngineConfig& config) {
    m_impl->config = config;

    // Initialize logger first
    m_impl->logger = std::make_unique<Logging::Logger> ("Engine");
    m_impl->logger->info ("Initializing OmniCpp Engine...");

    // Initialize platform
    m_impl->platform = std::make_unique<Platform::Platform> ();
    m_impl->platform->initialize ();
    m_impl->logger->info ("Platform: " + m_impl->platform->get_name ());

    // Initialize memory manager
    m_impl->memory_manager = std::make_unique<Memory::MemoryManager> ();
    m_impl->logger->info ("Memory manager initialized");

    // Initialize event manager
    m_impl->event_manager = std::make_unique<Events::EventManager> ();
    m_impl->logger->info ("Event manager initialized");

    // Initialize input manager
    m_impl->input_manager = std::make_unique<Input::InputManager> ();
    if (!m_impl->input_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize input manager");
      return false;
    }
    m_impl->logger->info ("Input manager initialized");

    // Initialize window manager
    m_impl->window_manager = std::make_unique<Window::WindowManager> ();
    if (!m_impl->window_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize window manager");
      return false;
    }
    m_impl->logger->info ("Window manager initialized");

    // Initialize renderer
    m_impl->renderer = std::make_unique<Graphics::Renderer> ();
    if (!m_impl->renderer->initialize ({})) {
      m_impl->logger->error ("Failed to initialize renderer");
      return false;
    }
    m_impl->logger->info ("Renderer initialized");

    // Initialize audio manager
    m_impl->audio_manager = std::make_unique<Audio::AudioManager> ();
    if (!m_impl->audio_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize audio manager");
      return false;
    }
    m_impl->logger->info ("Audio manager initialized");

    // Initialize resource manager
    m_impl->resource_manager = std::make_unique<Resources::ResourceManager> ();
    if (!m_impl->resource_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize resource manager");
      return false;
    }
    m_impl->logger->info ("Resource manager initialized");

    // Initialize physics engine
    m_impl->physics_engine = std::make_unique<Physics::PhysicsEngine> ();
    if (!m_impl->physics_engine->initialize ()) {
      m_impl->logger->error ("Failed to initialize physics engine");
      return false;
    }
    m_impl->logger->info ("Physics engine initialized");

    // Initialize scene manager
    m_impl->scene_manager = std::make_unique<Scene::SceneManager> ();
    if (!m_impl->scene_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize scene manager");
      return false;
    }
    m_impl->logger->info ("Scene manager initialized");

    // Initialize script manager
    m_impl->script_manager = std::make_unique<Scripting::ScriptManager> ();
    if (!m_impl->script_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize script manager");
      return false;
    }
    m_impl->logger->info ("Script manager initialized");

    // Initialize network manager
    m_impl->network_manager = std::make_unique<Network::NetworkManager> ();
    if (!m_impl->network_manager->initialize ()) {
      m_impl->logger->error ("Failed to initialize network manager");
      return false;
    }
    m_impl->logger->info ("Network manager initialized");

    m_impl->running = true;
    m_impl->last_frame_time = std::chrono::steady_clock::now ();
    m_impl->logger->info ("Engine initialized successfully");

    return true;
  }

  void Engine::run () {
    if (!m_impl->running) {
      m_impl->logger->error ("Engine not initialized, cannot run");
      return;
    }

    m_impl->logger->info ("Starting engine main loop...");

    while (m_impl->running) {
      auto current_time = std::chrono::steady_clock::now ();
      std::chrono::duration<float> elapsed = current_time - m_impl->last_frame_time;
      float deltaTime = elapsed.count ();

      // Fixed timestep update
      m_impl->accumulated_time += deltaTime;
      while (m_impl->accumulated_time >= m_impl->config.fixed_timestep) {
        update (m_impl->config.fixed_timestep);
        m_impl->accumulated_time -= m_impl->config.fixed_timestep;
      }

      // Render every frame
      render ();

      // Update input
      if (m_impl->input_manager) {
        m_impl->input_manager->update ();
      }

      // Update window
      if (m_impl->window_manager) {
        m_impl->window_manager->update ();
      }

      // Update audio
      if (m_impl->audio_manager) {
        m_impl->audio_manager->update ();
      }

      // Update network
      if (m_impl->network_manager) {
        m_impl->network_manager->update ();
      }

      m_impl->last_frame_time = current_time;
      m_impl->frame_count++;

      // Cap FPS
      if (m_impl->config.max_fps > 0) {
        float frame_time = 1.0f / static_cast<float> (m_impl->config.max_fps);
        if (deltaTime < frame_time) {
          std::this_thread::sleep_for (std::chrono::duration<float> (frame_time - deltaTime));
        }
      }
    }

    m_impl->logger->info ("Engine main loop stopped");
  }

  void Engine::shutdown () {
    if (!m_impl->running) {
      return;
    }

    m_impl->logger->info ("Shutting down engine...");

    // Shutdown in reverse order of initialization
    if (m_impl->network_manager) {
      m_impl->network_manager->shutdown ();
      m_impl->logger->info ("Network manager shut down");
    }

    if (m_impl->script_manager) {
      m_impl->script_manager->shutdown ();
      m_impl->logger->info ("Script manager shut down");
    }

    if (m_impl->scene_manager) {
      m_impl->scene_manager->shutdown ();
      m_impl->logger->info ("Scene manager shut down");
    }

    if (m_impl->physics_engine) {
      m_impl->physics_engine->shutdown ();
      m_impl->logger->info ("Physics engine shut down");
    }

    if (m_impl->resource_manager) {
      m_impl->resource_manager->shutdown ();
      m_impl->logger->info ("Resource manager shut down");
    }

    if (m_impl->audio_manager) {
      m_impl->audio_manager->shutdown ();
      m_impl->logger->info ("Audio manager shut down");
    }

    if (m_impl->renderer) {
      m_impl->renderer->shutdown ();
      m_impl->logger->info ("Renderer shut down");
    }

    if (m_impl->window_manager) {
      m_impl->window_manager->shutdown ();
      m_impl->logger->info ("Window manager shut down");
    }

    if (m_impl->input_manager) {
      m_impl->input_manager->shutdown ();
      m_impl->logger->info ("Input manager shut down");
    }

    if (m_impl->event_manager) {
      m_impl->event_manager->shutdown ();
      m_impl->logger->info ("Event manager shut down");
    }

    if (m_impl->memory_manager) {
      m_impl->memory_manager->shutdown ();
      m_impl->logger->info ("Memory manager shut down");
    }

    if (m_impl->platform) {
      m_impl->platform->shutdown ();
      m_impl->logger->info ("Platform shut down");
    }

    m_impl->running = false;
    m_impl->logger->info ("Engine shut down successfully");
  }

  void Engine::update (float deltaTime) {
    // Update physics
    if (m_impl->physics_engine) {
      m_impl->physics_engine->update (deltaTime);
    }

    // Update scene
    if (m_impl->scene_manager) {
      m_impl->scene_manager->update (deltaTime);
    }

    // Update scripts
    if (m_impl->script_manager) {
      m_impl->script_manager->update (deltaTime);
    }
  }

  void Engine::render () {
    if (m_impl->renderer) {
      m_impl->renderer->begin_frame ();
      m_impl->renderer->clear ();

      // Render scene
      if (m_impl->scene_manager) {
        m_impl->scene_manager->render ();
      }

      m_impl->renderer->end_frame ();
    }
  }

  bool Engine::is_running () const noexcept {
    return m_impl->running;
  }

  const EngineConfig& Engine::get_config () const noexcept {
    return m_impl->config;
  }

} // namespace OmniCpp::Engine::Core
