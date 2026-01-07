#pragma once

#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

namespace string_utils {

    // Trim whitespace from both ends of a string
    std::string trim(const std::string& str) {
        const auto first = str.find_first_not_of(' \t\n\r');
        if (std::string::npos == first) return "";
        const auto last = str.find_last_not_of(' \t\n\r');
        return str.substr(first, (last - first + 1));
    }

    // Split a string by delimiter
    std::vector<std::string> split(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(str);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    // Join strings with delimiter
    std::string join(const std::vector<std::string>& strings, const std::string& delimiter) {
        if (strings.empty()) return "";
        std::ostringstream oss;
        oss << strings[0];
        for (size_t i = 1; i < strings.size(); ++i) {
            oss << delimiter << strings[i];
        }
        return oss.str();
    }

    // Convert string to uppercase
    std::string to_upper(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return std::toupper(c); });
        return result;
    }

    // Convert string to lowercase
    std::string to_lower(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return result;
    }

} // namespace string_utils