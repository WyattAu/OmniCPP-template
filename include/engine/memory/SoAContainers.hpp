/**
 * @file SoAContainers.hpp
 * @brief Data-Oriented Design containers - Struct of Arrays (SoA)
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 5 - Memory, Data & Math Rules
 * - Arrays of large Structs (AoS) are prohibited when iterating over thousands of entities
 * - Must utilize SoA (Struct of Arrays) layouts for contiguous memory
 * - Maximizes L1/L2 cache prefetching and enables SIMD vectorization
 */

#pragma once

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <type_traits>
#include <utility>
#include <new>
#include <algorithm>
#include <span>
#include <optional>
#include <functional>
#include <fmt/format.h>

namespace omnicpp {
namespace memory {

// ============================================================================
// SoA Vector - Contiguous Struct of Arrays
// ============================================================================

/**
 * @brief SoA (Struct of Arrays) container for cache-efficient iteration
 * 
 * Instead of:
 *   struct Particle { float x, y, z; float vx, vy, vz; };
 *   std::vector<Particle> particles;  // AoS - poor cache locality
 * 
 * Use:
 *   SoAVector<float, float, float, float, float, float> particles;  // x, y, z, vx, vy, vz
 *   particles.get<0>()[i] = 1.0f;  // x[i]
 *   particles.get<3>()[i] = 0.5f;  // vx[i]
 * 
 * Benefits:
 * - Contiguous memory per component
 * - Better cache utilization (L1/L2 prefetching)
 * - SIMD-friendly memory layout
 * - 2-4x faster iteration on modern CPUs
 */
template<typename... Components>
class SoAVector {
    static_assert(sizeof...(Components) > 0, "SoAVector requires at least one component type");
    
public:
    static constexpr std::size_t kComponentCount = sizeof...(Components);
    static constexpr std::size_t kAlignment = 64;  // Cache line alignment
    
    using SizeType = std::size_t;
    using ComponentTypes = std::tuple<Components...>;
    
    // Helper to get component type at index
    template<std::size_t I>
    using ComponentType = std::tuple_element_t<I, ComponentTypes>;
    
    // Helper to get component size at index
    template<std::size_t I>
    static constexpr std::size_t kComponentSize = sizeof(ComponentType<I>);
    
    // Helper array of component sizes
    static constexpr std::size_t kComponentSizes[] = { sizeof(Components)... };
    
    // Helper array of component alignments
    static constexpr std::size_t kComponentAligns[] = { alignof(Components)... };
    
private:
    // Aligned storage for each component array
    std::tuple<std::unique_ptr<ComponentType<Components>[]...> > arrays_;
    
    SizeType size_{0};
    SizeType capacity_{0};
    
    // Calculate aligned capacity for a component
    template<std::size_t I>
    [[nodiscard]] static constexpr SizeType aligned_capacity(SizeType count) noexcept {
        constexpr std::size_t alignment = std::max(kComponentAligns[I], kAlignment);
        return ((count * kComponentSize<I>) + alignment - 1) / alignment;
    }
    
    // Allocate aligned memory for a component
    template<std::size_t I>
    void allocate_component(SizeType new_capacity) {
        using T = ComponentType<I>;
        constexpr std::size_t alignment = std::max(kComponentAligns[I], kAlignment);
        
        void* ptr = nullptr;
        #if defined(_MSC_VER)
            ptr = _aligned_malloc(new_capacity * sizeof(T), alignment);
            if (!ptr) throw std::bad_alloc();
            std::get<I>(arrays_).reset(static_cast<T*>(ptr));
        #else
            if (posix_memalign(&ptr, alignment, new_capacity * sizeof(T)) != 0) {
                throw std::bad_alloc();
            }
            std::get<I>(arrays_).reset(static_cast<T*>(ptr));
        #endif
    }
    
    // Deallocate component memory
    template<std::size_t I>
    void deallocate_component() {
        std::get<I>(arrays_).reset();
    }
    
    // Helper to allocate all components
    template<std::size_t... Is>
    void allocate_all(SizeType new_capacity, std::index_sequence<Is...>) {
        (allocate_component<Is>(new_capacity), ...);
    }
    
    // Helper to deallocate all components
    template<std::size_t... Is>
    void deallocate_all(std::index_sequence<Is...>) {
        (deallocate_component<Is>(), ...);
    }
    
    // Helper to copy data between arrays
    template<std::size_t I>
    void copy_data(const SoAVector& other, SizeType count) {
        if (count > 0 && std::get<I>(other.arrays_)) {
            std::memcpy(std::get<I>(arrays_).get(), 
                       std::get<I>(other.arrays_).get(), 
                       count * kComponentSize<I>);
        }
    }
    
    template<std::size_t... Is>
    void copy_all(const SoAVector& other, SizeType count, std::index_sequence<Is...>) {
        (copy_data<Is>(other, count), ...);
    }
    
public:
    SoAVector() = default;
    
    explicit SoAVector(SizeType initial_capacity) {
        reserve(initial_capacity);
    }
    
    ~SoAVector() = default;
    
    // Copy constructor
    SoAVector(const SoAVector& other) 
        : size_(other.size_), capacity_(other.capacity_) {
        if (capacity_ > 0) {
            allocate_all(capacity_, std::make_index_sequence<kComponentCount>{});
            copy_all(other, size_, std::make_index_sequence<kComponentCount>{});
        }
    }
    
    // Move constructor
    SoAVector(SoAVector&& other) noexcept
        : arrays_(std::move(other.arrays_)),
          size_(other.size_),
          capacity_(other.capacity_) {
        other.size_ = 0;
        other.capacity_ = 0;
    }
    
    // Copy assignment
    SoAVector& operator=(const SoAVector& other) {
        if (this != &other) {
            deallocate_all(std::make_index_sequence<kComponentCount>{});
            size_ = other.size_;
            capacity_ = other.capacity_;
            if (capacity_ > 0) {
                allocate_all(capacity_, std::make_index_sequence<kComponentCount>{});
                copy_all(other, size_, std::make_index_sequence<kComponentCount>{});
            }
        }
        return *this;
    }
    
    // Move assignment
    SoAVector& operator=(SoAVector&& other) noexcept {
        if (this != &other) {
            deallocate_all(std::make_index_sequence<kComponentCount>{});
            arrays_ = std::move(other.arrays_);
            size_ = other.size_;
            capacity_ = other.capacity_;
            other.size_ = 0;
            other.capacity_ = 0;
        }
        return *this;
    }
    
    /**
     * @brief Reserve capacity for at least n elements
     */
    void reserve(SizeType new_capacity) {
        if (new_capacity <= capacity_) return;
        
        // Create new container with larger capacity
        SoAVector new_container(new_capacity);
        new_container.size_ = size_;
        
        // Copy existing data
        if (size_ > 0) {
            for (SizeType i = 0; i < size_; ++i) {
                copy_element_from_to<0, kComponentCount - 1>(i, *this, new_container);
            }
        }
        
        *this = std::move(new_container);
    }
    
    /**
     * @brief Resize the container
     */
    void resize(SizeType new_size) {
        if (new_size > capacity_) {
            reserve(new_size * 2);  // Grow by 2x
        }
        size_ = new_size;
    }
    
    /**
     * @brief Clear all elements (doesn't free memory)
     */
    void clear() noexcept {
        size_ = 0;
    }
    
    /**
     * @brief Shrink capacity to fit size
     */
    void shrink_to_fit() {
        if (size_ == capacity_) return;
        
        if (size_ == 0) {
            deallocate_all(std::make_index_sequence<kComponentCount>{});
            capacity_ = 0;
            return;
        }
        
        SoAVector new_container(size_);
        new_container.size_ = size_;
        
        for (SizeType i = 0; i < size_; ++i) {
            copy_element_from_to<0, kComponentCount - 1>(i, *this, new_container);
        }
        
        *this = std::move(new_container);
    }
    
    /**
     * @brief Get pointer to component array at index I
     */
    template<std::size_t I>
    [[nodiscard]] ComponentType<I>* get() noexcept {
        return std::get<I>(arrays_).get();
    }
    
    template<std::size_t I>
    [[nodiscard]] const ComponentType<I>* get() const noexcept {
        return std::get<I>(arrays_).get();
    }
    
    /**
     * @brief Get span for component array at index I
     */
    template<std::size_t I>
    [[nodiscard]] std::span<ComponentType<I>> span() noexcept {
        return {get<I>(), size_};
    }
    
    template<std::size_t I>
    [[nodiscard]] std::span<const ComponentType<I>> span() const noexcept {
        return {get<I>(), size_};
    }
    
    /**
     * @brief Push back a new element
     */
    template<typename... Args>
    void push_back(Args&&... args) {
        static_assert(sizeof...(Args) == kComponentCount,
                     "push_back requires exactly one argument per component");
        
        if (size_ >= capacity_) {
            reserve(capacity_ == 0 ? 16 : capacity_ * 2);
        }
        
        set_components<0>(size_, std::forward<Args>(args)...);
        ++size_;
    }
    
    /**
     * @brief Emplace back with perfect forwarding
     */
    template<typename... Args>
    void emplace_back(Args&&... args) {
        push_back(std::forward<Args>(args)...);
    }
    
    /**
     * @brief Pop back element
     */
    void pop_back() noexcept {
        if (size_ > 0) {
            --size_;
        }
    }
    
    /**
     * @brief Swap elements at indices i and j
     */
    void swap_elements(SizeType i, SizeType j) noexcept {
        if (i == j || i >= size_ || j >= size_) return;
        swap_components<0, kComponentCount - 1>(i, j);
    }
    
    /**
     * @brief Erase element at index (swap with last, then pop)
     */
    void erase_swap(SizeType index) noexcept {
        if (index >= size_) return;
        if (index != size_ - 1) {
            swap_elements(index, size_ - 1);
        }
        pop_back();
    }
    
    /**
     * @brief Get current size
     */
    [[nodiscard]] SizeType size() const noexcept { return size_; }
    
    /**
     * @brief Get current capacity
     */
    [[nodiscard]] SizeType capacity() const noexcept { return capacity_; }
    
    /**
     * @brief Check if empty
     */
    [[nodiscard]] bool empty() const noexcept { return size_ == 0; }
    
    /**
     * @brief Iterator for iterating over all components together
     */
    class Iterator {
    public:
        using iterator_category = std::random_access_iterator_tag;
        using difference_type = std::ptrdiff_t;
        using value_type = std::tuple<Components&...>;
        using pointer = value_type*;
        using reference = value_type;
        
        Iterator(SoAVector* container, SizeType index)
            : container_(container), index_(index) {}
        
        value_type operator*() const {
            return get_tuple<0>(index_);
        }
        
        Iterator& operator++() { ++index_; return *this; }
        Iterator operator++(int) { Iterator tmp = *this; ++index_; return tmp; }
        Iterator& operator--() { --index_; return *this; }
        Iterator operator--(int) { Iterator tmp = *this; --index_; return tmp; }
        
        Iterator& operator+=(difference_type n) { index_ += n; return *this; }
        Iterator& operator-=(difference_type n) { index_ -= n; return *this; }
        
        friend bool operator==(const Iterator& a, const Iterator& b) {
            return a.index_ == b.index_;
        }
        friend bool operator!=(const Iterator& a, const Iterator& b) {
            return a.index_ != b.index_;
        }
        friend difference_type operator-(const Iterator& a, const Iterator& b) {
            return a.index_ - b.index_;
        }
        
    private:
        SoAVector* container_;
        SizeType index_;
        
        template<std::size_t I>
        value_type get_tuple(SizeType idx) const {
            if constexpr (I < kComponentCount - 1) {
                return std::tuple_cat(
                    std::tie(container_->get<I>()[idx]),
                    get_tuple<I + 1>(idx)
                );
            } else {
                return std::tie(container_->get<I>()[idx]);
            }
        }
    };
    
    Iterator begin() { return Iterator(this, 0); }
    Iterator end() { return Iterator(this, size_); }
    
private:
    // Helper to set all components of an element
    template<std::size_t I, typename First, typename... Rest>
    void set_components(SizeType index, First&& first, Rest&&... rest) {
        std::get<I>(arrays_)[index] = std::forward<First>(first);
        if constexpr (sizeof...(Rest) > 0) {
            set_components<I + 1>(index, std::forward<Rest>(rest)...);
        }
    }
    
    // Helper to copy element between containers
    template<std::size_t I, std::size_t Last>
    void copy_element_from_to(SizeType index, const SoAVector& from, SoAVector& to) {
        to.template get<I>()[index] = from.template get<I>()[index];
        if constexpr (I < Last) {
            copy_element_from_to<I + 1, Last>(index, from, to);
        }
    }
    
    // Helper to swap components
    template<std::size_t I, std::size_t Last>
    void swap_components(SizeType i, SizeType j) {
        std::swap(std::get<I>(arrays_)[i], std::get<I>(arrays_)[j]);
        if constexpr (I < Last) {
            swap_components<I + 1, Last>(i, j);
        }
    }
};

// ============================================================================
// Chunk - Fixed-size SoA block for ECS
// ============================================================================

/**
 * @brief Fixed-size chunk for ECS archetype storage
 * 
 * Designed for use in Entity Component Systems where archetypes
 * store entities with the same component composition.
 */
template<std::size_t ChunkSize, typename... Components>
class Chunk {
public:
    static constexpr std::size_t kCapacity = ChunkSize;
    
    using SoAStorage = SoAVector<Components...>;
    
private:
    SoAStorage storage_;
    std::size_t size_{0};
    std::uint64_t version_{0};  // Incremented on modification
    
public:
    Chunk() {
        storage_.reserve(kCapacity);
    }
    
    /**
     * @brief Add entity to chunk
     * @return Index in chunk, or nullopt if full
     */
    template<typename... Args>
    [[nodiscard]] std::optional<std::size_t> add(Args&&... args) {
        if (size_ >= kCapacity) {
            return std::nullopt;
        }
        
        storage_.push_back(std::forward<Args>(args)...);
        ++version_;
        return size_++;
    }
    
    /**
     * @brief Remove entity at index (swap-with-last)
     */
    void remove(std::size_t index) {
        if (index >= size_) return;
        
        if (index < size_ - 1) {
            storage_.swap_elements(index, size_ - 1);
        }
        storage_.pop_back();
        --size_;
        ++version_;
    }
    
    /**
     * @brief Get component array
     */
    template<std::size_t I>
    auto* get() noexcept { return storage_.template get<I>(); }
    
    template<std::size_t I>
    const auto* get() const noexcept { return storage_.template get<I>(); }
    
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] bool full() const noexcept { return size_ >= kCapacity; }
    [[nodiscard]] bool empty() const noexcept { return size_ == 0; }
    [[nodiscard]] std::uint64_t version() const noexcept { return version_; }
};

// ============================================================================
// Archetype - Collection of chunks with same component types
// ============================================================================

/**
 * @brief Archetype storage for ECS
 * 
 * All entities in an archetype have the exact same component composition.
 * Uses chunk-based allocation for cache-friendly iteration.
 */
template<std::size_t ChunkSize = 1024, typename... Components>
class Archetype {
public:
    using ChunkType = Chunk<ChunkSize, Components...>;
    using EntityIndex = std::pair<std::size_t, std::size_t>;  // chunk_index, element_index
    
private:
    std::vector<std::unique_ptr<ChunkType>> chunks_;
    std::size_t size_{0};
    
public:
    /**
     * @brief Add entity to archetype
     * @return Entity index (chunk, element)
     */
    template<typename... Args>
    EntityIndex add(Args&&... args) {
        // Find non-full chunk or create new one
        for (std::size_t i = 0; i < chunks_.size(); ++i) {
            if (!chunks_[i]->full()) {
                auto index = chunks_[i]->add(std::forward<Args>(args)...);
                if (index) {
                    ++size_;
                    return {i, *index};
                }
            }
        }
        
        // Create new chunk
        chunks_.push_back(std::make_unique<ChunkType>());
        auto index = chunks_.back()->add(std::forward<Args>(args)...);
        ++size_;
        return {chunks_.size() - 1, *index};
    }
    
    /**
     * @brief Remove entity
     */
    void remove(EntityIndex index) {
        if (index.first >= chunks_.size()) return;
        chunks_[index.first]->remove(index.second);
        --size_;
    }
    
    /**
     * @brief Get component from entity
     */
    template<std::size_t ComponentIndex>
    auto& get(EntityIndex index) {
        return chunks_[index.first]->template get<ComponentIndex>()[index.second];
    }
    
    template<std::size_t ComponentIndex>
    const auto& get(EntityIndex index) const {
        return chunks_[index.first]->template get<ComponentIndex>()[index.second];
    }
    
    /**
     * @brief Iterate over all chunks
     */
    template<typename Func>
    void for_each_chunk(Func&& func) {
        for (auto& chunk : chunks_) {
            func(*chunk);
        }
    }
    
    /**
     * @brief Get total entity count
     */
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    
    /**
     * @brief Get chunk count
     */
    [[nodiscard]] std::size_t chunk_count() const noexcept { return chunks_.size(); }
};

} // namespace memory
} // namespace omnicpp
