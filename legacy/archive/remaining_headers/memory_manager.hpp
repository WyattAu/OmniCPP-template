/**
 * @file memory_manager.hpp
 * @brief Memory management interface
 */

#pragma once

#include <cstddef>
#include <memory>
#include <string>

namespace OmniCpp::Engine::Memory {

  /**
   * @brief Memory allocation statistics
   */
  struct MemoryStats {
    size_t total_allocated{ 0 };
    size_t total_freed{ 0 };
    size_t current_usage{ 0 };
    size_t allocation_count{ 0 };
  };

  /**
   * @brief Memory manager class
   * 
   * Provides custom memory allocation with tracking and leak detection.
   * Follows C++23 best practices with RAII and move semantics.
   */
  class MemoryManager {
  public:
    MemoryManager ();
    ~MemoryManager ();

    // Delete copy operations (C++23 best practice)
    MemoryManager (const MemoryManager&) = delete;
    MemoryManager& operator= (const MemoryManager&) = delete;

    // Enable move operations (C++23 best practice)
    MemoryManager (MemoryManager&&) noexcept;
    MemoryManager& operator= (MemoryManager&&) noexcept;

    /**
     * @brief Allocate memory with alignment
     * @param size Size to allocate in bytes
     * @param alignment Alignment requirement in bytes
     * @return Pointer to allocated memory, or nullptr on failure
     */
    [[nodiscard]] void* allocate (size_t size, size_t alignment = alignof (std::max_align_t));

    /**
     * @brief Deallocate memory
     * @param ptr Pointer to deallocate
     */
    void deallocate (void* ptr);

    /**
     * @brief Get memory statistics
     * @return Current memory statistics
     */
    [[nodiscard]] const MemoryStats& get_stats () const noexcept;

    /**
     * @brief Check for memory leaks
     * @return true if leaks detected, false otherwise
     */
    [[nodiscard]] bool has_leaks () const noexcept;

    /**
     * @brief Initialize memory manager
     * @return true if successful, false otherwise
     */
    bool initialize ();

    /**
     * @brief Shutdown memory manager
     */
    void shutdown ();

  private:
    struct Impl;
    std::unique_ptr<Impl> m_impl; // Pimpl idiom for ABI stability
  };

} // namespace OmniCpp::Engine::Memory
