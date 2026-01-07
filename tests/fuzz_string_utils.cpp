#include <cstdint>
#include <cstddef>
import string_utils;

// Fuzz test for string_utils functions
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    // Convert fuzz data to string
    std::string input(reinterpret_cast<const char*>(data), size);

    // Test various string operations
    try {
        // Test split
        auto split_result = string_utils::split(input, ',');

        // Test to_upper
        auto upper_result = string_utils::to_upper(input);

        // Test to_lower
        auto lower_result = string_utils::to_lower(input);

        // Test trim
        auto trim_result = string_utils::trim(input);

        // Test join (using the split result)
        auto join_result = string_utils::join(split_result, ",");

        // Basic sanity checks
        if (!input.empty()) {
            // Upper and lower should be different if input contains letters
            if (upper_result == lower_result) {
                // Check if input has no letters
                bool has_letters = false;
                for (char c : input) {
                    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                        has_letters = true;
                        break;
                    }
                }
                if (has_letters) {
                    // This should not happen
                    __builtin_trap();
                }
            }
        }

    } catch (...) {
        // We expect some inputs to cause exceptions, just don't crash
    }

    return 0;
}