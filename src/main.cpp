#include <iostream>
#include <string>
#include <vector>

// Include our custom modules as headers (fallback for MSVC)
#include "math.hpp"
#include "string_utils.hpp"

int main() {
    std::cout << "C++ Modules Demo" << std::endl;

    // Test math module
    std::cout << "\nMath Module:" << std::endl;
    std::cout << "add(5, 3) = " << math::add(5, 3) << std::endl;
    std::cout << "multiply(4.5, 2.0) = " << math::multiply(4.5, 2.0) << std::endl;
    std::cout << "factorial(5) = " << math::factorial(5) << std::endl;
    std::cout << "PI = " << math::PI << std::endl;

    // Test string_utils module
    std::cout << "\nString Utils Module:" << std::endl;
    std::string test_str = "  Hello, World!  ";
    std::cout << "Original: '" << test_str << "'" << std::endl;
    std::cout << "Trimmed: '" << string_utils::trim(test_str) << "'" << std::endl;

    std::string sentence = "This is a test sentence";
    auto words = string_utils::split(sentence, ' ');
    std::cout << "Split: ";
    for (const auto& word : words) {
        std::cout << "'" << word << "' ";
    }
    std::cout << std::endl;

    std::cout << "Joined: '" << string_utils::join(words, "-") << "'" << std::endl;
    std::cout << "Upper: '" << string_utils::to_upper("hello") << "'" << std::endl;
    std::cout << "Lower: '" << string_utils::to_lower("WORLD") << "'" << std::endl;

    return 0;
}