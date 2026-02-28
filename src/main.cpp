/**
 * @file main.cpp
 * @brief OmniCPP Template entry point
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 2 - Compiler Rigor & Type Modeling
 * - Uses fmt::print for compile-time verified formatting
 * - No printf/sprintf/std::cout for security
 */

#include <string>
#include <vector>
#include <fmt/core.h>

// Include our custom modules as headers (fallback for MSVC)
#include "math.hpp"
#include "string_utils.hpp"

int main() {
    fmt::print("C++ Modules Demo\n");

    // Test math module
    fmt::print("\nMath Module:\n");
    fmt::print("add(5, 3) = {}\n", math::add(5, 3));
    fmt::print("multiply(4.5, 2.0) = {}\n", math::multiply(4.5, 2.0));
    fmt::print("factorial(5) = {}\n", math::factorial(5));
    fmt::print("PI = {}\n", math::PI);

    // Test string_utils module
    fmt::print("\nString Utils Module:\n");
    std::string test_str = "  Hello, World!  ";
    fmt::print("Original: '{}'\n", test_str);
    fmt::print("Trimmed: '{}'\n", string_utils::trim(test_str));

    std::string sentence = "This is a test sentence";
    auto words = string_utils::split(sentence, ' ');
    fmt::print("Split: ");
    for (const auto& word : words) {
        fmt::print("'{}' ", word);
    }
    fmt::print("\n");

    fmt::print("Joined: '{}'\n", string_utils::join(words, "-"));
    fmt::print("Upper: '{}'\n", string_utils::to_upper("hello"));
    fmt::print("Lower: '{}'\n", string_utils::to_lower("WORLD"));

    return 0;
}