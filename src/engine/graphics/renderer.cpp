/**
 * @file renderer.cpp
 * @brief Graphics renderer implementation
 */

#include "engine/graphics/renderer.hpp"
#include <mutex>

namespace OmniCpp::Engine::Graphics {

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct Renderer::Impl {
    RendererConfig config;
    std::mutex mutex;
    bool initialized{ false };
  };

  Renderer::Renderer () : m_impl (std::make_unique<Impl> ()) {
  }

  Renderer::~Renderer () {
    shutdown ();
  }

  Renderer::Renderer (Renderer&& other) noexcept : m_impl (std::move (other.m_impl)) {
  }

  Renderer& Renderer::operator= (Renderer&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool Renderer::initialize (const RendererConfig& config) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->config = config;
    m_impl->initialized = true;

    return true;
  }

  void Renderer::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    m_impl->initialized = false;
  }

  void Renderer::update () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Update renderer state here
  }

  void Renderer::render () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Render scene here
  }

  void Renderer::clear () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Clear buffers here
  }

  void Renderer::present () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    // Present frame here
  }

} // namespace OmniCpp::Engine::Graphics
