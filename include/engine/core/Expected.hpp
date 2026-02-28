/**
 * @file Expected.hpp
 * @brief Value-oriented error handling using std::expected (C++23)
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 2 - Compiler Rigor & Type Modeling
 * - Exceptions prohibited for business logic control flow
 * - All fallible operations must return std::expected<T, E>
 * - Exceptions restricted to irrecoverable hardware/system failures
 */

#pragma once

// C++23 std::expected is available in GCC 12+, Clang 15+, MSVC 19.34+
// For older compilers, we provide a fallback using std::variant
#if __has_include(<expected>)
    #include <expected>
    #define OMNICPP_HAS_STD_EXPECTED 1
#else
    // Fallback implementation using std::variant
    #include <variant>
    #include <utility>
    #include <type_traits>
    #define OMNICPP_HAS_STD_EXPECTED 0
#endif

#include <string>
#include <string_view>
#include <fmt/format.h>

namespace omnicpp {
namespace core {

// ============================================================================
// Error Types
// ============================================================================

/**
 * @brief Base error type for all operations
 * 
 * All error types should inherit from this or be convertible to it.
 */
struct Error {
    int code{0};
    std::string message;
    
    Error() = default;
    Error(int c, std::string_view msg) : code(c), message(msg) {}
    
    explicit operator bool() const noexcept { return code != 0; }
    
    std::string format() const {
        return fmt::format("[Error {}]: {}", code, message);
    }
};

/**
 * @brief Common error codes
 */
enum class ErrorCode : int {
    Success = 0,
    Unknown = 1,
    InvalidArgument = 2,
    OutOfRange = 3,
    NotFound = 4,
    AlreadyExists = 5,
    PermissionDenied = 6,
    ResourceExhausted = 7,
    NotInitialized = 8,
    AlreadyInitialized = 9,
    OperationFailed = 10,
    Timeout = 11,
    ConnectionFailed = 12,
    IOError = 13,
    ParseError = 14,
    ValidationError = 15,
};

/**
 * @brief Create an error from an error code
 */
inline Error make_error(ErrorCode code, std::string_view message = "") {
    return Error{static_cast<int>(code), std::string(message)};
}

/**
 * @brief Create an error from a code and message
 */
inline Error make_error(int code, std::string_view message) {
    return Error{code, std::string(message)};
}

// ============================================================================
// std::expected Wrapper (C++23 or fallback)
// ============================================================================

#if OMNICPP_HAS_STD_EXPECTED

/**
 * @brief Alias for std::expected when C++23 is available
 */
template<typename T, typename E = Error>
using Expected = std::expected<T, E>;

/**
 * @brief Alias for std::unexpected
 */
template<typename E>
using Unexpected = std::unexpected<E>;

/**
 * @brief Create an unexpected value
 */
template<typename E>
constexpr auto make_unexpected(E&& e) {
    return std::unexpected(std::forward<E>(e));
}

#else // Fallback implementation

/**
 * @brief Fallback Expected implementation using std::variant
 * 
 * Provides a subset of std::expected interface for pre-C++23 compilers.
 */
template<typename T, typename E = Error>
class Expected {
public:
    using value_type = T;
    using error_type = E;
    using variant_type = std::variant<T, E>;
    
private:
    variant_type data_;
    
public:
    // Constructors
    Expected() requires std::is_default_constructible_v<T>
        : data_(std::in_place_index<0>, T{}) {}
    
    template<typename U = T>
        requires (!std::is_same_v<std::remove_cvref_t<U>, Expected> &&
                  !std::is_same_v<std::remove_cvref_t<U>, std::unexpected<E>> &&
                  std::is_constructible_v<T, U>)
    Expected(U&& value) : data_(std::in_place_index<0>, std::forward<U>(value)) {}
    
    template<typename... Args>
        requires std::is_constructible_v<T, Args...>
    Expected(std::in_place_t, Args&&... args)
        : data_(std::in_place_index<0>, std::forward<Args>(args)...) {}
    
    Expected(const Expected&) = default;
    Expected(Expected&&) = default;
    Expected& operator=(const Expected&) = default;
    Expected& operator=(Expected&&) = default;
    
    // Construct from unexpected
    template<typename G = E>
        requires std::is_constructible_v<E, G>
    Expected(const std::unexpected<G>& e)
        : data_(std::in_place_index<1>, e.error()) {}
    
    template<typename G = E>
        requires std::is_constructible_v<E, G>
    Expected(std::unexpected<G>&& e)
        : data_(std::in_place_index<1>, std::move(e).error()) {}
    
    // Observers
    [[nodiscard]] bool has_value() const noexcept {
        return data_.index() == 0;
    }
    
    [[nodiscard]] explicit operator bool() const noexcept {
        return has_value();
    }
    
    // Value access
    [[nodiscard]] T& value() & {
        if (!has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<0>(data_);
    }
    
    [[nodiscard]] const T& value() const& {
        if (!has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<0>(data_);
    }
    
    [[nodiscard]] T&& value() && {
        if (!has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<0>(std::move(data_));
    }
    
    [[nodiscard]] T* operator->() noexcept {
        return has_value() ? &std::get<0>(data_) : nullptr;
    }
    
    [[nodiscard]] const T* operator->() const noexcept {
        return has_value() ? &std::get<0>(data_) : nullptr;
    }
    
    [[nodiscard]] T& operator*() & noexcept {
        return std::get<0>(data_);
    }
    
    [[nodiscard]] const T& operator*() const& noexcept {
        return std::get<0>(data_);
    }
    
    [[nodiscard]] T&& operator*() && noexcept {
        return std::get<0>(std::move(data_));
    }
    
    // Error access
    [[nodiscard]] E& error() & {
        if (has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<1>(data_);
    }
    
    [[nodiscard]] const E& error() const& {
        if (has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<1>(data_);
    }
    
    [[nodiscard]] E&& error() && {
        if (has_value()) {
            throw std::bad_variant_access();
        }
        return std::get<1>(std::move(data_));
    }
    
    // Value or
    template<typename U = T>
    [[nodiscard]] T value_or(U&& default_value) const& {
        return has_value() ? **this : static_cast<T>(std::forward<U>(default_value));
    }
    
    template<typename U = T>
    [[nodiscard]] T value_or(U&& default_value) && {
        return has_value() ? std::move(**this) : static_cast<T>(std::forward<U>(default_value));
    }
};

/**
 * @brief Partial specialization for void value type
 */
template<typename E>
class Expected<void, E> {
public:
    using value_type = void;
    using error_type = E;
    
private:
    std::variant<std::monostate, E> data_;
    
public:
    Expected() : data_(std::monostate{}) {}
    
    template<typename G = E>
        requires std::is_constructible_v<E, G>
    Expected(const std::unexpected<G>& e)
        : data_(std::in_place_index<1>, e.error()) {}
    
    Expected(const Expected&) = default;
    Expected(Expected&&) = default;
    Expected& operator=(const Expected&) = default;
    Expected& operator=(Expected&&) = default;
    
    [[nodiscard]] bool has_value() const noexcept {
        return data_.index() == 0;
    }
    
    [[nodiscard]] explicit operator bool() const noexcept {
        return has_value();
    }
    
    [[nodiscard]] E& error() & {
        return std::get<1>(data_);
    }
    
    [[nodiscard]] const E& error() const& {
        return std::get<1>(data_);
    }
};

/**
 * @brief unexpected wrapper for the fallback
 */
template<typename E>
class unexpected {
public:
    unexpected() = delete;
    
    template<typename G = E>
        requires std::is_constructible_v<E, G>
    explicit unexpected(G&& e) : error_(std::forward<G>(e)) {}
    
    unexpected(const unexpected&) = default;
    unexpected(unexpected&&) = default;
    unexpected& operator=(const unexpected&) = default;
    unexpected& operator=(unexpected&&) = default;
    
    [[nodiscard]] E& error() & noexcept { return error_; }
    [[nodiscard]] const E& error() const& noexcept { return error_; }
    [[nodiscard]] E&& error() && noexcept { return std::move(error_); }
    
private:
    E error_;
};

/**
 * @brief Create an unexpected value (fallback)
 */
template<typename E>
constexpr auto make_unexpected(E&& e) {
    return unexpected<std::remove_cvref_t<E>>(std::forward<E>(e));
}

#endif // OMNICPP_HAS_STD_EXPECTED

// ============================================================================
// Convenience Types
// ============================================================================

/**
 * @brief Expected<void> - for operations that can fail but return no value
 */
using ExpectedVoid = Expected<void, Error>;

/**
 * @brief Make a successful void result
 */
inline ExpectedVoid make_expected() {
    return ExpectedVoid{};
}

/**
 * @brief Make a successful result with a value
 */
template<typename T>
Expected<T, Error> make_expected(T&& value) {
    return Expected<T, Error>(std::forward<T>(value));
}

/**
 * @brief Macros for expected-based error handling
 */

// TRY: Unwrap an Expected or propagate the error
#define OMNICPP_TRY(expr) \
    ({ \
        auto __result = (expr); \
        if (!__result.has_value()) { \
            return omnicpp::core::make_unexpected(std::move(__result.error())); \
        } \
        std::move(*__result); \
    })

// TRY_VOID: Execute an Expected<void> or propagate the error
#define OMNICPP_TRY_VOID(expr) \
    do { \
        auto __result = (expr); \
        if (!__result.has_value()) { \
            return omnicpp::core::make_unexpected(std::move(__result.error())); \
        } \
    } while(0)

// ENSURE: Assert a condition or return an error
#define OMNICPP_ENSURE(cond, error_code, message) \
    do { \
        if (!(cond)) { \
            return omnicpp::core::make_unexpected( \
                omnicpp::core::make_error(error_code, message)); \
        } \
    } while(0)

} // namespace core
} // namespace omnicpp

// ============================================================================
// fmt formatter for Error
// ============================================================================
template<>
struct fmt::formatter<omnicpp::core::Error> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::core::Error& e, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "[Error {}]: {}", e.code, e.message);
    }
};
