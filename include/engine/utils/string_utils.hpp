/**
 * @file string_utils.hpp
 * @brief String utility functions
 */

#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace OmniCpp::Engine::Utils {

  /**
   * @brief String utility class
   */
  class StringUtils {
  public:
    StringUtils () = delete;
    ~StringUtils () = delete;

    StringUtils (const StringUtils&) = delete;
    StringUtils& operator= (const StringUtils&) = delete;

    static std::string to_lower (const std::string& str);
    static std::string to_upper (const std::string& str);
    static std::string trim (const std::string& str);
    static std::string trim_left (const std::string& str);
    static std::string trim_right (const std::string& str);

    static std::vector<std::string> split (const std::string& str, char delimiter);
    static std::string join (const std::vector<std::string>& parts, const std::string& delimiter);

    static bool starts_with (const std::string& str, const std::string& prefix);
    static bool ends_with (const std::string& str, const std::string& suffix);
    static bool contains (const std::string& str, const std::string& substr);

    static std::string replace (const std::string& str, const std::string& from,
        const std::string& to);
    static std::string replace_all (const std::string& str, const std::string& from,
        const std::string& to);

    static bool equals_ignore_case (const std::string& a, const std::string& b);
  };

} // namespace OmniCpp::Engine::Utils
