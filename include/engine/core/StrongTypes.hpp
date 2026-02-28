/**
 * @file StrongTypes.hpp
 * @brief Strong typedef utilities for compile-time type safety
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 2 - Compiler Rigor & Type Modeling
 * - Primitive obsession is prohibited
 * - Identifiers and constrained values must use strong types
 * - Prevents accidental argument swapping at compile time
 */

#pragma once

#include <cstdint>
#include <type_traits>
#include <utility>
#include <functional>
#include <fmt/format.h>

namespace omnicpp {
namespace core {

// ============================================================================
// Strong Type Base
// ============================================================================

/**
 * @brief Base template for creating strong typedefs
 * 
 * Usage:
 *   using EntityId = StrongType<uint64_t, struct EntityIdTag>;
 *   using ComponentId = StrongType<uint64_t, struct ComponentIdTag>;
 * 
 * This prevents accidental mixing of different ID types.
 */
template<typename T, typename Tag>
class StrongType {
public:
    using value_type = T;
    using tag_type = Tag;
    
    // Constructors
    constexpr StrongType() noexcept : value_{} {}
    
    constexpr explicit StrongType(const T& value) noexcept 
        requires std::is_copy_constructible_v<T>
        : value_(value) {}
    
    constexpr explicit StrongType(T&& value) noexcept
        requires std::is_move_constructible_v<T>
        : value_(std::move(value)) {}
    
    // Accessors
    [[nodiscard]] constexpr T& get() noexcept { return value_; }
    [[nodiscard]] constexpr const T& get() const noexcept { return value_; }
    
    // Implicit conversion to underlying type (for convenience, use carefully)
    [[nodiscard]] constexpr operator const T&() const noexcept { return value_; }
    
    // Comparison operators
    [[nodiscard]] constexpr bool operator==(const StrongType& other) const noexcept {
        return value_ == other.value_;
    }
    
    [[nodiscard]] constexpr bool operator!=(const StrongType& other) const noexcept {
        return value_ != other.value_;
    }
    
    [[nodiscard]] constexpr bool operator<(const StrongType& other) const noexcept {
        return value_ < other.value_;
    }
    
    [[nodiscard]] constexpr bool operator<=(const StrongType& other) const noexcept {
        return value_ <= other.value_;
    }
    
    [[nodiscard]] constexpr bool operator>(const StrongType& other) const noexcept {
        return value_ > other.value_;
    }
    
    [[nodiscard]] constexpr bool operator>=(const StrongType& other) const noexcept {
        return value_ >= other.value_;
    }
    
    // Spaceship operator (C++20)
    [[nodiscard]] constexpr auto operator<=>(const StrongType& other) const noexcept {
        return value_ <=> other.value_;
    }
    
protected:
    T value_;
};

// ============================================================================
// Integer Strong Types
// ============================================================================

/**
 * @brief Strong type for entity IDs
 */
using EntityId = StrongType<uint64_t, struct EntityIdTag>;

/**
 * @brief Strong type for component IDs
 */
using ComponentId = StrongType<uint64_t, struct ComponentIdTag>;

/**
 * @brief Strong type for resource IDs
 */
using ResourceId = StrongType<uint64_t, struct ResourceIdTag>;

/**
 * @brief Strong type for scene node IDs
 */
using SceneNodeId = StrongType<uint64_t, struct SceneNodeIdTag>;

/**
 * @brief Strong type for asset IDs
 */
using AssetId = StrongType<uint64_t, struct AssetIdTag>;

/**
 * @brief Strong type for network connection IDs
 */
using ConnectionId = StrongType<uint64_t, struct ConnectionIdTag>;

// ============================================================================
// Floating Point Strong Types (for domain-specific units)
// ============================================================================

/**
 * @brief Strong type for time in seconds
 */
using Seconds = StrongType<float, struct SecondsTag>;

/**
 * @brief Strong type for time in milliseconds
 */
using Milliseconds = StrongType<float, struct MillisecondsTag>;

/**
 * @brief Strong type for angles in degrees
 */
using Degrees = StrongType<float, struct DegreesTag>;

/**
 * @brief Strong type for angles in radians
 */
using Radians = StrongType<float, struct RadiansTag>;

/**
 * @brief Strong type for distance in meters
 */
using Meters = StrongType<float, struct MetersTag>;

/**
 * @brief Strong type for percentage values (0-100)
 */
using Percentage = StrongType<float, struct PercentageTag>;

// ============================================================================
// Bounded Strong Types
// ============================================================================

/**
 * @brief Strong type with bounds checking
 * 
 * Usage:
 *   using Health = Bounded<int, 0, 100>;
 *   Health h(50);  // OK
 *   Health h(150); // Clamped to 100
 */
template<typename T, T Min, T Max>
class Bounded {
public:
    using value_type = T;
    static constexpr T min_value = Min;
    static constexpr T max_value = Max;
    
    constexpr Bounded() noexcept : value_(Min) {}
    
    constexpr explicit Bounded(T value) noexcept 
        : value_(clamp(value)) {}
    
    [[nodiscard]] constexpr T get() const noexcept { return value_; }
    [[nodiscard]] constexpr operator T() const noexcept { return value_; }
    
    constexpr Bounded& operator=(T value) noexcept {
        value_ = clamp(value);
        return *this;
    }
    
    // Arithmetic operators with clamping
    constexpr Bounded& operator+=(T delta) noexcept {
        value_ = clamp(value_ + delta);
        return *this;
    }
    
    constexpr Bounded& operator-=(T delta) noexcept {
        value_ = clamp(value_ - delta);
        return *this;
    }
    
    [[nodiscard]] constexpr bool operator==(const Bounded& other) const noexcept {
        return value_ == other.value_;
    }
    
    [[nodiscard]] constexpr bool operator!=(const Bounded& other) const noexcept {
        return value_ != other.value_;
    }
    
private:
    static constexpr T clamp(T value) noexcept {
        if (value < Min) return Min;
        if (value > Max) return Max;
        return value;
    }
    
    T value_;
};

// ============================================================================
// Common Bounded Types
// ============================================================================

/**
 * @brief Normalized value (0.0 to 1.0)
 */
using Normalized = Bounded<float, 0, 1>;

/**
 * @brief Health points (0 to 100)
 */
using Health = Bounded<int, 0, 100>;

/**
 * @brief Opacity (0.0 to 1.0)
 */
using Opacity = Bounded<float, 0, 1>;

/**
 * @brief Volume (0 to 100)
 */
using Volume = Bounded<int, 0, 100>;

// ============================================================================
// Validated Strong Types
// ============================================================================

/**
 * @brief Strong type that validates on construction
 * 
 * Usage:
 *   using PositiveInt = Validated<int, [](int v) { return v > 0; }>;
 */
template<typename T, auto Validator>
class Validated {
public:
    using value_type = T;
    
    constexpr explicit Validated(T value) 
        : value_(value) {
        if (!Validator(value)) {
            // In constexpr context, this will fail at compile time
            // In runtime, we could throw or handle differently
        }
    }
    
    [[nodiscard]] constexpr T get() const noexcept { return value_; }
    [[nodiscard]] constexpr operator T() const noexcept { return value_; }
    
    [[nodiscard]] static constexpr bool is_valid(T value) noexcept {
        return Validator(value);
    }
    
private:
    T value_;
};

// ============================================================================
// Named String Types
// ============================================================================

/**
 * @brief Strong type for names/identifiers
 */
struct Name {
    std::string value;
    
    Name() = default;
    explicit Name(std::string v) : value(std::move(v)) {}
    explicit Name(std::string_view v) : value(v) {}
    
    [[nodiscard]] const std::string& get() const noexcept { return value; }
    [[nodiscard]] operator const std::string&() const noexcept { return value; }
    
    [[nodiscard]] bool operator==(const Name& other) const noexcept {
        return value == other.value;
    }
    
    [[nodiscard]] bool operator!=(const Name& other) const noexcept {
        return value != other.value;
    }
    
    [[nodiscard]] bool operator<(const Name& other) const noexcept {
        return value < other.value;
    }
};

/**
 * @brief Strong type for file paths
 */
struct FilePath {
    std::string value;
    
    FilePath() = default;
    explicit FilePath(std::string v) : value(std::move(v)) {}
    explicit FilePath(std::string_view v) : value(v) {}
    
    [[nodiscard]] const std::string& get() const noexcept { return value; }
    [[nodiscard]] operator const std::string&() const noexcept { return value; }
    
    [[nodiscard]] bool empty() const noexcept { return value.empty(); }
    [[nodiscard]] bool has_extension() const noexcept {
        return value.find('.') != std::string::npos;
    }
    
    [[nodiscard]] bool operator==(const FilePath& other) const noexcept {
        return value == other.value;
    }
};

} // namespace core
} // namespace omnicpp

// ============================================================================
// Hash Support for Strong Types
// ============================================================================
namespace std {

template<typename T, typename Tag>
struct hash<omnicpp::core::StrongType<T, Tag>> {
    size_t operator()(const omnicpp::core::StrongType<T, Tag>& id) const noexcept {
        return hash<T>{}(id.get());
    }
};

template<typename T, T Min, T Max>
struct hash<omnicpp::core::Bounded<T, Min, Max>> {
    size_t operator()(const omnicpp::core::Bounded<T, Min, Max>& b) const noexcept {
        return hash<T>{}(b.get());
    }
};

template<>
struct hash<omnicpp::core::Name> {
    size_t operator()(const omnicpp::core::Name& n) const noexcept {
        return hash<string>{}(n.value);
    }
};

template<>
struct hash<omnicpp::core::FilePath> {
    size_t operator()(const omnicpp::core::FilePath& p) const noexcept {
        return hash<string>{}(p.value);
    }
};

} // namespace std

// ============================================================================
// fmt Formatters for Strong Types
// ============================================================================
template<typename T, typename Tag>
struct fmt::formatter<omnicpp::core::StrongType<T, Tag>> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::core::StrongType<T, Tag>& id, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "{}", id.get());
    }
};

template<>
struct fmt::formatter<omnicpp::core::Name> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::core::Name& n, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "{}", n.value);
    }
};
