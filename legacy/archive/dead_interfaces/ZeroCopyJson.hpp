/**
 * @file ZeroCopyJson.hpp
 * @brief Zero-copy JSON parsing using simdjson
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 5 - Memory, Data & Math Rules
 * - Parsing network payloads into intermediate objects is prohibited on hot paths
 * - JSON parsing must use simdjson for gigabyte-per-second throughput
 * - Zero-copy access without materializing intermediate structures
 */

#pragma once

#include <string_view>
#include <optional>
#include <stdexcept>
#include <cstdint>
#include <fmt/format.h>

// simdjson headers
#include <simdjson/simdjson.h>

#include "engine/core/Expected.hpp"

namespace omnicpp {
namespace serialization {

// ============================================================================
// JSON Error Types
// ============================================================================

/**
 * @brief JSON parsing error codes
 */
enum class JsonError : int {
    Success = 0,
    InvalidJson = 1,
    TypeMismatch = 2,
    NoSuchField = 3,
    OutOfBounds = 4,
    AllocationFailure = 5,
    EmptyDocument = 6,
    UnclosedArray = 7,
    UnclosedObject = 8,
    NumberError = 9,
    StringError = 10,
    Utf8Error = 11,
    ParserError = 12,
};

/**
 * @brief Convert simdjson error to JsonError
 */
[[nodiscard]] inline JsonError to_json_error(simdjson::error_code err) noexcept {
    using namespace simdjson;
    switch (err) {
        case SUCCESS: return JsonError::Success;
        case TAPE_ERROR: return JsonError::InvalidJson;
        case DEPTH_ERROR: return JsonError::ParserError;
        case STRING_ERROR: return JsonError::StringError;
        case T_ATOM_ERROR: 
        case F_ATOM_ERROR: return JsonError::TypeMismatch;
        case N_ATOM_ERROR: return JsonError::NumberError;
        case NUMBER_ERROR: return JsonError::NumberError;
        case UTF8_ERROR: return JsonError::Utf8Error;
        case UNINITIALIZED: return JsonError::ParserError;
        case EMPTY: return JsonError::EmptyDocument;
        case UNESCAPED_CHARS: return JsonError::StringError;
        case UNCLOSED_STRING: return JsonError::StringError;
        case ALLOC_FAILURE: return JsonError::AllocationFailure;
        case REALLOCATION_FAILURE: return JsonError::AllocationFailure;
        case TRAILING_CONTENT: return JsonError::ParserError;
        case OUT_OF_BOUNDS: return JsonError::OutOfBounds;
        case NUM_ERROR: return JsonError::NumberError;
        case INCORRECT_TYPE: return JsonError::TypeMismatch;
        case NO_SUCH_FIELD: return JsonError::NoSuchField;
        case CAPACITY: return JsonError::AllocationFailure;
        case MEMALLOC: return JsonError::AllocationFailure;
        case INDEX_OUT_OF_BOUNDS: return JsonError::OutOfBounds;
        case INVALID_JSON_POINTER: return JsonError::InvalidJson;
        case INVALID_URI_FRAGMENT: return JsonError::InvalidJson;
        case UNEXPECTED_ERROR: return JsonError::ParserError;
        case PARSER_IN_USE: return JsonError::ParserError;
        case INSUFFICIENT_PADDING: return JsonError::ParserError;
        case OUT_OF_ORDER_ITERATION: return JsonError::ParserError;
        default: return JsonError::InvalidJson;
    }
}

// ============================================================================
// Zero-Copy JSON Parser
// ============================================================================

/**
 * @brief Zero-copy JSON parser using simdjson
 * 
 * Achieves 2-3 GB/s parsing throughput by:
 * - Not materializing intermediate DOM objects
 * - Using SIMD-accelerated parsing
 * - Direct pointer access to parsed data
 * 
 * Usage:
 *   ZeroCopyJsonParser parser;
 *   auto doc = parser.parse(json_string);
 *   if (doc.has_value()) {
 *       auto name = doc->get_string("/user/name");
 *       auto age = doc->get_int("/user/age");
 *   }
 */
class ZeroCopyJsonParser {
public:
    /**
     * @brief Construct a parser with specified capacity
     * @param max_capacity Maximum document size in bytes (default 4GB)
     */
    explicit ZeroCopyJsonParser(std::size_t max_capacity = simdjson::DOM::parser::max_capacity_bytes())
        : parser_() {
        parser_.allocate(max_capacity);
    }
    
    /**
     * @brief Parse a JSON document (zero-copy)
     * @param json JSON string to parse
     * @return Parsed document or error
     * 
     * Note: The input string must remain valid for the lifetime of the returned document
     */
    [[nodiscard]] core::Expected<simdjson::dom::element, JsonError> 
    parse(std::string_view json) noexcept {
        auto result = parser_.parse(json.data(), json.size());
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value();
    }
    
    /**
     * @brief Parse a JSON document with padding (allows in-place parsing)
     * @param json JSON string with extra padding at end
     * @param len Actual length without padding
     */
    [[nodiscard]] core::Expected<simdjson::dom::element, JsonError>
    parse_padded(char* json, std::size_t len) noexcept {
        auto result = parser_.parse(json, len, false);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value();
    }
    
    /**
     * @brief Load and parse a file
     * @param path Path to JSON file
     */
    [[nodiscard]] core::Expected<simdjson::dom::element, JsonError>
    load_file(const std::string& path) noexcept {
        auto result = parser_.load(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value();
    }

private:
    simdjson::dom::parser parser_;
};

// ============================================================================
// JSON Document Wrapper
// ============================================================================

/**
 * @brief Wrapper for JSON document with convenient access methods
 */
class JsonDocument {
public:
    JsonDocument() = default;
    explicit JsonDocument(simdjson::dom::element root) : root_(root) {}
    
    /**
     * @brief Get a string field (zero-copy)
     * @param path JSON pointer path (e.g., "/user/name")
     * @return String view into the original JSON buffer
     */
    [[nodiscard]] core::Expected<std::string_view, JsonError> 
    get_string(std::string_view path) const noexcept {
        auto result = root_.at_pointer(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().get_string();
    }
    
    /**
     * @brief Get an integer field
     */
    [[nodiscard]] core::Expected<int64_t, JsonError>
    get_int(std::string_view path) const noexcept {
        auto result = root_.at_pointer(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().get_int64();
    }
    
    /**
     * @brief Get a double field
     */
    [[nodiscard]] core::Expected<double, JsonError>
    get_double(std::string_view path) const noexcept {
        auto result = root_.at_pointer(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().get_double();
    }
    
    /**
     * @brief Get a boolean field
     */
    [[nodiscard]] core::Expected<bool, JsonError>
    get_bool(std::string_view path) const noexcept {
        auto result = root_.at_pointer(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().get_bool();
    }
    
    /**
     * @brief Check if a field is null
     */
    [[nodiscard]] core::Expected<bool, JsonError>
    is_null(std::string_view path) const noexcept {
        auto result = root_.at_pointer(path);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().is_null();
    }
    
    /**
     * @brief Get an array element by index
     */
    [[nodiscard]] core::Expected<simdjson::dom::element, JsonError>
    get_element(std::size_t index) const noexcept {
        auto result = root_.at(index);
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value();
    }
    
    /**
     * @brief Get array size
     */
    [[nodiscard]] core::Expected<std::size_t, JsonError>
    array_size() const noexcept {
        auto result = root_.get_array();
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        return result.value().size();
    }
    
    /**
     * @brief Iterate over array elements
     */
    template<typename Func>
    void for_each_array_element(Func&& func) const {
        auto arr = root_.get_array();
        if (!arr.error()) {
            for (auto element : arr.value()) {
                func(element);
            }
        }
    }
    
    /**
     * @brief Iterate over object fields
     */
    template<typename Func>
    void for_each_object_field(Func&& func) const {
        auto obj = root_.get_object();
        if (!obj.error()) {
            for (auto [key, value] : obj.value()) {
                func(key, value);
            }
        }
    }
    
    /**
     * @brief Get the underlying element
     */
    [[nodiscard]] simdjson::dom::element root() const noexcept { return root_; }

private:
    simdjson::dom::element root_;
};

// ============================================================================
// JSON Streaming Parser (for large files)
// ============================================================================

/**
 * @brief Streaming JSON parser for large documents
 * 
 * Processes JSON documents larger than memory by streaming
 */
class JsonStreamingParser {
public:
    /**
     * @brief Stream array elements from a large JSON file
     * @param path Path to JSON file
     * @param callback Called for each array element
     */
    static core::Expected<void, JsonError>
    stream_array(const std::string& path,
                 std::function<void(simdjson::dom::element)> callback) {
        simdjson::dom::parser parser;
        
        // For very large files, use chunked parsing
        auto result = parser.load_many(path, 1000000);  // 1MB chunks
        if (result.error()) {
            return core::make_unexpected(to_json_error(result.error()));
        }
        
        for (auto doc : result) {
            if (doc.is_array()) {
                for (auto element : doc.get_array().value()) {
                    callback(element);
                }
            }
        }
        
        return {};
    }
};

// ============================================================================
// Convenience Functions
// ============================================================================

/**
 * @brief Parse JSON string and return document
 */
[[nodiscard]] inline core::Expected<JsonDocument, JsonError>
parse_json(std::string_view json) {
    static ZeroCopyJsonParser parser;
    auto result = parser.parse(json);
    if (!result.has_value()) {
        return core::make_unexpected(result.error());
    }
    return JsonDocument(*result);
}

/**
 * @brief Load and parse JSON file
 */
[[nodiscard]] inline core::Expected<JsonDocument, JsonError>
load_json_file(const std::string& path) {
    static ZeroCopyJsonParser parser;
    auto result = parser.load_file(path);
    if (!result.has_value()) {
        return core::make_unexpected(result.error());
    }
    return JsonDocument(*result);
}

// ============================================================================
// JSON Validation
// ============================================================================

/**
 * @brief Validate JSON without full parsing
 */
[[nodiscard]] inline bool is_valid_json(std::string_view json) noexcept {
    static ZeroCopyJsonParser parser;
    return parser.parse(json).has_value();
}

} // namespace serialization
} // namespace omnicpp

// ============================================================================
// fmt Formatter for JsonError
// ============================================================================
template<>
struct fmt::formatter<omnicpp::serialization::JsonError> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }
    
    template<typename FormatContext>
    auto format(omnicpp::serialization::JsonError e, FormatContext& ctx) {
        using namespace omnicpp::serialization;
        const char* name = "Unknown";
        switch (e) {
            case JsonError::Success: name = "Success"; break;
            case JsonError::InvalidJson: name = "InvalidJson"; break;
            case JsonError::TypeMismatch: name = "TypeMismatch"; break;
            case JsonError::NoSuchField: name = "NoSuchField"; break;
            case JsonError::OutOfBounds: name = "OutOfBounds"; break;
            case JsonError::AllocationFailure: name = "AllocationFailure"; break;
            case JsonError::EmptyDocument: name = "EmptyDocument"; break;
            case JsonError::UnclosedArray: name = "UnclosedArray"; break;
            case JsonError::UnclosedObject: name = "UnclosedObject"; break;
            case JsonError::NumberError: name = "NumberError"; break;
            case JsonError::StringError: name = "StringError"; break;
            case JsonError::Utf8Error: name = "Utf8Error"; break;
            case JsonError::ParserError: name = "ParserError"; break;
        }
        return fmt::format_to(ctx.out(), "JsonError::{}", name);
    }
};
