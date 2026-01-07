/**
 * @file memory_manager.cpp
 * @brief Memory management implementation
 */

#include "engine/memory/memory_manager.hpp"
#include <cstdlib>
#include <cstring>
#include <mutex>
#include <unordered_map>

namespace OmniCpp::Engine::Memory {

  /**
   * @brief Allocation record for tracking
   */
  struct AllocationRecord {
    size_t size;
    const char* file;
    int line;
  };

  /**
   * @brief Private implementation structure (Pimpl idiom)
   */
  struct MemoryManager::Impl {
    MemoryStats stats;
    std::unordered_map<void*, AllocationRecord> allocations;
    std::mutex mutex;
    bool initialized{ false };
  };

  MemoryManager::MemoryManager () : m_impl (std::make_unique<Impl> ()) {
    // Constructor implementation
  }

  MemoryManager::~MemoryManager () {
    shutdown ();
  }

  MemoryManager::MemoryManager (MemoryManager&& other) noexcept
      : m_impl (std::move (other.m_impl)) {
    // Move constructor
  }

  MemoryManager& MemoryManager::operator= (MemoryManager&& other) noexcept {
    if (this != &other) {
      m_impl = std::move (other.m_impl);
    }
    return *this;
  }

  bool MemoryManager::initialize () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (m_impl->initialized) {
      return true;
    }

    m_impl->stats = MemoryStats{};
    m_impl->allocations.clear ();
    m_impl->initialized = true;

    return true;
  }

  void MemoryManager::shutdown () {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return;
    }

    // Check for leaks
    if (!m_impl->allocations.empty ()) {
      // Report leaks
      for (const auto& [ptr, record] : m_impl->allocations) {
        // Leak detected - in production, log this
        (void)ptr; // Suppress unused warning
        (void)record;
      }
    }

    m_impl->initialized = false;
  }

  void* MemoryManager::allocate (size_t size, size_t alignment) {
    std::lock_guard<std::mutex> lock (m_impl->mutex);

    if (!m_impl->initialized) {
      return nullptr;
    }

    // Allocate aligned memory
    void* ptr = nullptr;
#ifdef _WIN32
    ptr = _aligned_malloc (size, alignment);
#else
    if (posix_memalign (alignment, size, &ptr) != 0) {
      ptr = nullptr;
    }
#endif

    if (ptr == nullptr) {
      return nullptr;
    }

    // Track allocation
    AllocationRecord record{ size, nullptr, 0 };
    m_impl->allocations[ptr] = record;

    // Update statistics
    m_impl->stats.total_allocated += size;
    m_impl->stats.current_usage += size;
    m_impl->stats.allocation_count++;

    return ptr;
  }

  void MemoryManager::deallocate (void* ptr) {
    if (ptr == nullptr) {
      return;
    }

    std::lock_guard<std::mutex> lock (m_impl->mutex);

    auto it = m_impl->allocations.find (ptr);
    if (it == m_impl->allocations.end ()) {
      // Unknown pointer - ignore or handle error
      return;
    }

    // Update statistics
    m_impl->stats.total_freed += it->second.size;
    m_impl->stats.current_usage -= it->second.size;

    // Remove from tracking
    m_impl->allocations.erase (it);

// Free memory
#ifdef _WIN32
    _aligned_free (ptr);
#else
    free (ptr);
#endif
  }

  const MemoryStats& MemoryManager::get_stats () const noexcept {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return m_impl->stats;
  }

  bool MemoryManager::has_leaks () const noexcept {
    std::lock_guard<std::mutex> lock (m_impl->mutex);
    return !m_impl->allocations.empty ();
  }

} // namespace OmniCpp::Engine::Memory
