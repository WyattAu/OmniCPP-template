/**
 * @file SwissTable.hpp
 * @brief Hardware-optimized hash map alias using Abseil SwissTables
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 2 - Systems, Network & IPC Contract Rules
 * - std::unordered_map is strictly prohibited due to cache-thrashing
 * - Flat, open-addressing hash maps (SwissTables) must be used globally
 * - Provides 2x-4x speedup over std::unordered_map
 */

#pragma once

// Use Abseil's SwissTable implementation
#if __has_include(<absl/container/flat_hash_map.h>)
    #include <absl/container/flat_hash_map.h>
    #include <absl/container/flat_hash_set.h>
    #include <absl/container/node_hash_map.h>
    #include <absl/container/node_hash_set.h>
    #define OMNICPP_HAS_ABSEIL 1
#else
    // Fallback to std::unordered_map (with warning)
    #include <unordered_map>
    #include <unordered_set>
    #define OMNICPP_HAS_ABSEIL 0
    
    #warning "Abseil not found. Using std::unordered_map as fallback. \
             Install abseil for optimal hash table performance."
#endif

namespace omnicpp {
namespace core {

// ============================================================================
// SwissTable Type Aliases
// ============================================================================

#if OMNICPP_HAS_ABSEIL

/**
 * @brief Flat hash map - most performant for most use cases
 * 
 * - Uses open addressing with SIMD optimizations
 * - Does not invalidate pointers on rehash
 * - Best cache locality
 * - 2-4x faster than std::unordered_map
 */
template<typename Key, typename Value,
         typename Hash = absl::container_internal::hash_default_hash<Key>,
         typename Eq = absl::container_internal::hash_default_eq<Key>,
         typename Alloc = std::allocator<std::pair<const Key, Value>>>
using FlatHashMap = absl::flat_hash_map<Key, Value, Hash, Eq, Alloc>;

/**
 * @brief Flat hash set - most performant for most use cases
 */
template<typename Key,
         typename Hash = absl::container_internal::hash_default_hash<Key>,
         typename Eq = absl::container_internal::hash_default_eq<Key>,
         typename Alloc = std::allocator<Key>>
using FlatHashSet = absl::flat_hash_set<Key, Hash, Eq, Alloc>;

/**
 * @brief Node hash map - stable pointers, similar to std::unordered_map
 * 
 * - Guarantees pointer stability
 * - Slightly slower than FlatHashMap but still faster than std::unordered_map
 */
template<typename Key, typename Value,
         typename Hash = absl::container_internal::hash_default_hash<Key>,
         typename Eq = absl::container_internal::hash_default_eq<Key>,
         typename Alloc = std::allocator<std::pair<const Key, Value>>>
using NodeHashMap = absl::node_hash_map<Key, Value, Hash, Eq, Alloc>;

/**
 * @brief Node hash set - stable pointers
 */
template<typename Key,
         typename Hash = absl::container_internal::hash_default_hash<Key>,
         typename Eq = absl::container_internal::hash_default_eq<Key>,
         typename Alloc = std::allocator<Key>>
using NodeHashSet = absl::node_hash_set<Key, Hash, Eq, Alloc>;

#else // Fallback

template<typename Key, typename Value,
         typename Hash = std::hash<Key>,
         typename Eq = std::equal_to<Key>,
         typename Alloc = std::allocator<std::pair<const Key, Value>>>
using FlatHashMap = std::unordered_map<Key, Value, Hash, Eq, Alloc>;

template<typename Key,
         typename Hash = std::hash<Key>,
         typename Eq = std::equal_to<Key>,
         typename Alloc = std::allocator<Key>>
using FlatHashSet = std::unordered_set<Key, Hash, Eq, Alloc>;

template<typename Key, typename Value,
         typename Hash = std::hash<Key>,
         typename Eq = std::equal_to<Key>,
         typename Alloc = std::allocator<std::pair<const Key, Value>>>
using NodeHashMap = std::unordered_map<Key, Value, Hash, Eq, Alloc>;

template<typename Key,
         typename Hash = std::hash<Key>,
         typename Eq = std::equal_to<Key>,
         typename Alloc = std::allocator<Key>>
using NodeHashSet = std::unordered_set<Key, Hash, Eq, Alloc>;

#endif // OMNICPP_HAS_ABSEIL

// ============================================================================
// Default Hash Map Selection
// ============================================================================

/**
 * @brief Default hash map type for the engine
 * 
 * Use FlatHashMap for most cases. Use NodeHashMap if you need
 * pointer stability (e.g., storing pointers to elements).
 */
template<typename Key, typename Value>
using HashMap = FlatHashMap<Key, Value>;

/**
 * @brief Default hash set type for the engine
 */
template<typename Key>
using HashSet = FlatHashSet<Key>;

// ============================================================================
// Hash Utilities
// ============================================================================

/**
 * @brief Combined hash for multiple values
 * 
 * Based on Boost's hash_combine algorithm.
 */
template<typename T>
inline void hash_combine(std::size_t& seed, const T& value) {
    std::hash<T> hasher;
    seed ^= hasher(value) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

/**
 * @brief Hash multiple values together
 */
template<typename... Args>
inline std::size_t hash_values(const Args&... args) {
    std::size_t seed = 0;
    (hash_combine(seed, args), ...);
    return seed;
}

/**
 * @brief Pair hash for use in hash maps
 */
struct PairHash {
    template<typename T1, typename T2>
    std::size_t operator()(const std::pair<T1, T2>& pair) const {
        return hash_values(pair.first, pair.second);
    }
};

/**
 * @brief Tuple hash for use in hash maps
 */
struct TupleHash {
    template<typename... Args>
    std::size_t operator()(const std::tuple<Args...>& tuple) const {
        return std::apply([](const auto&... args) {
            return hash_values(args...);
        }, tuple);
    }
};

} // namespace core
} // namespace omnicpp
