/**
 * @file string_utils.cpp
 * @brief String utility functions implementation
 */

#include "engine/utils/string_utils.hpp"
#include <algorithm>
#include <cctype>
#include <sstream>
#include "engine/logging/Log.hpp"

namespace OmniCpp::Engine::Utils {

  std::string StringUtils::to_lower (const std::string& str) {
    std::string result = str;
    std::transform (result.begin (), result.end (), result.begin (),
        [] (unsigned char c) { return std::tolower (c); });
    omnicpp::log::trace("StringUtils: Converted '{}' to lowercase", str);
    return result;
  }

  std::string StringUtils::to_upper (const std::string& str) {
    std::string result = str;
    std::transform (result.begin (), result.end (), result.begin (),
        [] (unsigned char c) { return std::toupper (c); });
    omnicpp::log::trace("StringUtils: Converted '{}' to uppercase", str);
    return result;
  }

  std::string StringUtils::trim (const std::string& str) {
    std::string result = trim_right (trim_left (str));
    omnicpp::log::trace("StringUtils: Trimmed whitespace from '{}'", str);
    return result;
  }

  std::string StringUtils::trim_left (const std::string& str) {
    auto it = std::find_if (str.begin (), str.end (),
        [] (unsigned char ch) { return !std::isspace (ch); });
    return std::string (it, str.end ());
  }

  std::string StringUtils::trim_right (const std::string& str) {
    auto it = std::find_if (str.rbegin (), str.rend (),
        [] (unsigned char ch) { return !std::isspace (ch); });
    return std::string (str.begin (), it.base ());
  }

  std::vector<std::string> StringUtils::split (const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss (str);
    std::string item;

    while (std::getline (ss, item, delimiter)) {
      result.push_back (item);
    }

    omnicpp::log::trace("StringUtils: Split '{}' into {} parts", str, result.size());
    return result;
  }

  std::string StringUtils::join (const std::vector<std::string>& parts,
      const std::string& delimiter) {
    if (parts.empty ()) {
      return "";
    }

    std::stringstream ss;
    for (size_t i = 0; i < parts.size (); ++i) {
      if (i > 0) {
        ss << delimiter;
      }
      ss << parts[i];
    }

    std::string result = ss.str ();
    omnicpp::log::trace("StringUtils: Joined {} parts with delimiter '{}'", parts.size(), delimiter);
    return result;
  }

  bool StringUtils::starts_with (const std::string& str, const std::string& prefix) {
    if (prefix.size () > str.size ()) {
      return false;
    }
    bool result = std::equal (prefix.begin (), prefix.end (), str.begin ());
    omnicpp::log::trace("StringUtils: Checking if '{}' starts with '{}': {}", str, prefix, result);
    return result;
  }

  bool StringUtils::ends_with (const std::string& str, const std::string& suffix) {
    if (suffix.size () > str.size ()) {
      return false;
    }
    bool result = std::equal (suffix.rbegin (), suffix.rend (), str.rbegin ());
    omnicpp::log::trace("StringUtils: Checking if '{}' ends with '{}': {}", str, suffix, result);
    return result;
  }

  bool StringUtils::contains (const std::string& str, const std::string& substr) {
    bool result = str.find (substr) != std::string::npos;
    omnicpp::log::trace("StringUtils: Checking if '{}' contains '{}': {}", str, substr, result);
    return result;
  }

  std::string StringUtils::replace (const std::string& str, const std::string& from,
      const std::string& to) {
    size_t pos = str.find (from);
    if (pos == std::string::npos) {
      return str;
    }
    std::string result = str;
    result.replace (pos, from.size (), to);
    omnicpp::log::trace("StringUtils: Replaced first occurrence of '{}' with '{}' in '{}'", from, to, str);
    return result;
  }

  std::string StringUtils::replace_all (const std::string& str, const std::string& from,
      const std::string& to) {
    if (from.empty ()) {
      return str;
    }

    std::string result = str;
    size_t pos = 0;
    int count = 0;

    while ((pos = result.find (from, pos)) != std::string::npos) {
      result.replace (pos, from.size (), to);
      pos += to.size ();
      count++;
    }

    omnicpp::log::trace("StringUtils: Replaced {} occurrences of '{}' with '{}' in '{}'", count, from, to, str);
    return result;
  }

  bool StringUtils::equals_ignore_case (const std::string& a, const std::string& b) {
    if (a.size () != b.size ()) {
      return false;
    }
    bool result = std::equal (a.begin (), a.end (), b.begin (),
        [] (unsigned char ca, unsigned char cb) { return std::tolower (ca) == std::tolower (cb); });
    omnicpp::log::trace("StringUtils: Comparing '{}' and '{}' ignoring case: {}", a, b, result);
    return result;
  }

} // namespace OmniCpp::Engine::Utils
