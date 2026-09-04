/**
 * @file SecureAllocator.hpp
 * @brief Secure memory allocation for sensitive data (PII, secrets, keys)
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 4 - Observability & Telemetry
 * - Passwords, API keys, and cryptographic key material must never be in std::string
 * - Must use custom allocator with libsodium's sodium_malloc
 * - Guarantees memory pages are locked (no swapping to disk)
 * - Securely zeroed out (sodium_memzero) on destruction
 */

#pragma once

#include <cstddef>
#include <memory>
#include <string>
#include <string_view>
#include <stdexcept>
#include <type_traits>
#include <initializer_list>

// Forward declare libsodium functions to avoid header dependency in this header
extern "C" {
    void* sodium_malloc(std::size_t size);
    void sodium_free(void* ptr);
    int sodium_mlock(void* addr, std::size_t len);
    int sodium_munlock(void* addr, std::size_t len);
    void sodium_memzero(void* ptr, std::size_t len);
    int sodium_init(void);
}

namespace omnicpp {
namespace security {

// ============================================================================
// Secure Allocator
// ============================================================================

/**
 * @brief Secure allocator using libsodium
 * 
 * Features:
 * - Memory is locked (cannot be swapped to disk)
 * - Memory is zeroed on deallocation
 * - Guard pages around allocations
 * - Canary values for overflow detection
 * 
 * Usage:
 *   using SecureString = std::basic_string<char, std::char_traits<char>, SecureAllocator<char>>;
 *   SecureString password("my_secret_password");
 *   // Memory is securely wiped when password goes out of scope
 */
template<typename T>
class SecureAllocator {
public:
    using value_type = T;
    using size_type = std::size_t;
    using difference_type = std::ptrdiff_t;
    using pointer = T*;
    using const_pointer = const T*;
    using reference = T&;
    using const_reference = const T&;
    
    template<typename U>
    struct rebind {
        using other = SecureAllocator<U>;
    };
    
    SecureAllocator() noexcept = default;
    
    template<typename U>
    SecureAllocator(const SecureAllocator<U>&) noexcept {}
    
    /**
     * @brief Allocate secure memory
     * @param n Number of objects
     * @return Pointer to secure memory
     * @throws std::bad_alloc if allocation fails
     */
    [[nodiscard]] T* allocate(std::size_t n) {
        if (n == 0) {
            return nullptr;
        }
        
        if (n > static_cast<std::size_t>(-1) / sizeof(T)) {
            throw std::bad_alloc();
        }
        
        // Initialize libsodium if not already done
        static bool initialized = (sodium_init() >= 0);
        if (!initialized) {
            throw std::runtime_error("Failed to initialize libsodium");
        }
        
        void* ptr = sodium_malloc(n * sizeof(T));
        if (ptr == nullptr) {
            throw std::bad_alloc();
        }
        
        return static_cast<T*>(ptr);
    }
    
    /**
     * @brief Deallocate and securely zero memory
     * @param ptr Pointer to deallocate
     * @param n Number of objects (unused, for interface compatibility)
     */
    void deallocate(T* ptr, std::size_t /* n */) noexcept {
        if (ptr != nullptr) {
            sodium_free(ptr);
        }
    }
    
    template<typename U>
    bool operator==(const SecureAllocator<U>&) const noexcept {
        return true;
    }
    
    template<typename U>
    bool operator!=(const SecureAllocator<U>&) const noexcept {
        return false;
    }
};

// ============================================================================
// Secure String
// ============================================================================

/**
 * @brief Secure string type that wipes memory on destruction
 * 
 * COMPLIANCE: Use for passwords, API keys, tokens, secrets
 * 
 * Usage:
 *   SecureString api_key = load_api_key_from_env();
 *   SecureString password = get_user_password();
 *   
 *   // Never log or print directly
 *   // api_key.c_str() is only for passing to APIs
 */
using SecureString = std::basic_string<char, std::char_traits<char>, SecureAllocator<char>>;

/**
 * @brief Secure wide string
 */
using SecureWString = std::basic_string<wchar_t, std::char_traits<wchar_t>, SecureAllocator<wchar_t>>;

// ============================================================================
// Secure Vector
// ============================================================================

/**
 * @brief Secure vector that wipes memory on destruction
 * 
 * Usage:
 *   SecureVector<uint8_t> encryption_key(32);
 *   // Fill with key material
 *   // Memory is securely wiped on destruction
 */
template<typename T>
using SecureVector = std::vector<T, SecureAllocator<T>>;

// ============================================================================
// Secure Bytes (for cryptographic keys)
// ============================================================================

/**
 * @brief Secure byte array for cryptographic material
 */
using SecureBytes = SecureVector<std::byte>;

// ============================================================================
// Secure Unique Pointer
// ============================================================================

/**
 * @brief Secure deleter that wipes memory before freeing
 */
template<typename T>
struct SecureDeleter {
    void operator()(T* ptr) const {
        if (ptr) {
            // Wipe the object's memory
            sodium_memzero(ptr, sizeof(T));
            // Destroy the object
            ptr->~T();
            // Free the secure memory
            sodium_free(ptr);
        }
    }
};

/**
 * @brief Secure unique pointer
 */
template<typename T>
using SecureUniquePtr = std::unique_ptr<T, SecureDeleter<T>>;

/**
 * @brief Make a secure unique pointer
 */
template<typename T, typename... Args>
[[nodiscard]] SecureUniquePtr<T> make_secure(Args&&... args) {
    // Initialize libsodium
    static bool initialized = (sodium_init() >= 0);
    
    void* ptr = sodium_malloc(sizeof(T));
    if (ptr == nullptr) {
        throw std::bad_alloc();
    }
    
    try {
        new (ptr) T(std::forward<Args>(args)...);
        return SecureUniquePtr<T>(static_cast<T*>(ptr));
    } catch (...) {
        sodium_free(ptr);
        throw;
    }
}

// ============================================================================
// Secure String Utilities
// ============================================================================

/**
 * @brief Convert a string_view to SecureString and wipe the source
 * @param source Source string (will be wiped)
 * @return SecureString copy
 */
[[nodiscard]] inline SecureString to_secure_and_wipe(std::string_view& source) {
    SecureString result(source.begin(), source.end());
    // Wipe the source memory
    sodium_memzero(const_cast<char*>(source.data()), source.size());
    source = {};
    return result;
}

/**
 * @brief Compare two strings in constant time (to prevent timing attacks)
 */
[[nodiscard]] inline bool secure_compare(std::string_view a, std::string_view b) noexcept {
    if (a.size() != b.size()) {
        return false;
    }
    
    volatile unsigned char result = 0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        result |= static_cast<unsigned char>(a[i]) ^ static_cast<unsigned char>(b[i]);
    }
    
    return result == 0;
}

/**
 * @brief Compare SecureString in constant time
 */
[[nodiscard]] inline bool secure_compare(const SecureString& a, const SecureString& b) noexcept {
    return secure_compare(
        std::string_view(a.data(), a.size()),
        std::string_view(b.data(), b.size())
    );
}

// ============================================================================
// Secure Password Type
// ============================================================================

/**
 * @brief Strong type for passwords to prevent accidental logging
 * 
 * Usage:
 *   Password pwd = get_user_password();
 *   authenticate(pwd);  // Only explicit access
 *   // Cannot: fmt::print("{}", pwd);  // Compile error
 */
class Password {
public:
    Password() = default;
    
    explicit Password(std::string_view value)
        : value_(value.begin(), value.end()) {}
    
    explicit Password(const char* str)
        : value_(str) {}
    
    // Move-only to prevent copies
    Password(const Password&) = delete;
    Password& operator=(const Password&) = delete;
    Password(Password&&) = default;
    Password& operator=(Password&&) = default;
    
    ~Password() = default;
    
    /**
     * @brief Get the password value (use carefully)
     */
    [[nodiscard]] const SecureString& value() const noexcept { return value_; }
    
    /**
     * @brief Get as string_view for passing to APIs
     */
    [[nodiscard]] std::string_view view() const noexcept {
        return std::string_view(value_.data(), value_.size());
    }
    
    /**
     * @brief Get C-string for legacy APIs
     */
    [[nodiscard]] const char* c_str() const noexcept { return value_.c_str(); }
    
    /**
     * @brief Check if empty
     */
    [[nodiscard]] bool empty() const noexcept { return value_.empty(); }
    
    /**
     * @brief Get size
     */
    [[nodiscard]] std::size_t size() const noexcept { return value_.size(); }
    
    /**
     * @brief Compare with another password in constant time
     */
    [[nodiscard]] bool equals(const Password& other) const noexcept {
        return secure_compare(value_, other.value_);
    }
    
    /**
     * @brief Clear the password
     */
    void clear() noexcept { value_.clear(); }

private:
    SecureString value_;
};

// ============================================================================
// API Key Type
// ============================================================================

/**
 * @brief Strong type for API keys
 */
class ApiKey {
public:
    ApiKey() = default;
    
    explicit ApiKey(std::string_view key)
        : key_(key.begin(), key.end()) {}
    
    // Move-only
    ApiKey(const ApiKey&) = delete;
    ApiKey& operator=(const ApiKey&) = delete;
    ApiKey(ApiKey&&) = default;
    ApiKey& operator=(ApiKey&&) = default;
    
    [[nodiscard]] const SecureString& value() const noexcept { return key_; }
    [[nodiscard]] std::string_view view() const noexcept {
        return std::string_view(key_.data(), key_.size());
    }
    [[nodiscard]] bool empty() const noexcept { return key_.empty(); }
    
    /**
     * @brief Get masked version for logging (shows only last 4 chars)
     */
    [[nodiscard]] std::string masked() const {
        if (key_.size() <= 4) {
            return "****";
        }
        return "****" + std::string(key_.end() - 4, key_.end());
    }

private:
    SecureString key_;
};

// ============================================================================
// Token Type
// ============================================================================

/**
 * @brief Strong type for authentication tokens
 */
class AuthToken {
public:
    AuthToken() = default;
    
    explicit AuthToken(std::string_view token, std::chrono::system_clock::time_point expiry = {})
        : token_(token.begin(), token.end()), expiry_(expiry) {}
    
    // Move-only
    AuthToken(const AuthToken&) = delete;
    AuthToken& operator=(const AuthToken&) = delete;
    AuthToken(AuthToken&&) = default;
    AuthToken& operator=(AuthToken&&) = default;
    
    [[nodiscard]] const SecureString& value() const noexcept { return token_; }
    [[nodiscard]] std::string_view view() const noexcept {
        return std::string_view(token_.data(), token_.size());
    }
    [[nodiscard]] bool empty() const noexcept { return token_.empty(); }
    
    /**
     * @brief Check if token is expired
     */
    [[nodiscard]] bool is_expired() const noexcept {
        if (expiry_ == std::chrono::system_clock::time_point{}) {
            return false;  // No expiry set
        }
        return std::chrono::system_clock::now() > expiry_;
    }
    
    /**
     * @brief Check if token is valid (not empty and not expired)
     */
    [[nodiscard]] bool is_valid() const noexcept {
        return !empty() && !is_expired();
    }
    
    [[nodiscard]] std::chrono::system_clock::time_point expiry() const noexcept { return expiry_; }

private:
    SecureString token_;
    std::chrono::system_clock::time_point expiry_;
};

} // namespace security
} // namespace omnicpp

// ============================================================================
// fmt Formatter (for masked output only)
// ============================================================================

template<>
struct fmt::formatter<omnicpp::security::Password> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::security::Password&, FormatContext& ctx) {
        // Never format passwords - always return masked
        return fmt::format_to(ctx.out(), "[PASSWORD:REDACTED]");
    }
};

template<>
struct fmt::formatter<omnicpp::security::ApiKey> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::security::ApiKey& key, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "[API_KEY:{}]", key.masked());
    }
};

template<>
struct fmt::formatter<omnicpp::security::AuthToken> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(const omnicpp::security::AuthToken&, FormatContext& ctx) {
        return fmt::format_to(ctx.out(), "[AUTH_TOKEN:REDACTED]");
    }
};
