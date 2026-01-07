/**
 * @file string_utils.cpp
 * @brief String utility functions implementation
 */

#include "engine/utils/string_utils.hpp"
#include <algorithm>
#include <cctype>
#include <sstream>

namespace OmniCpp::Engine::Utils {

  std::string StringUtils::to_lower (const std::string& str) {
    std::string result = str;
    std::transform (result.begin (), result.end (), result.begin (),
        [] (unsigned char c) { return std::tolower (c); });
    return result;
  }

  std::string StringUtils::to_upper (const std::string& str) {
    std::string result = str;
    std::transform (result.begin (), result.end (), result.begin (),
        [] (unsigned char c) { return std::toupper (c); });
    return result;
  }

  std::string StringUtils::trim (const std::string& str) {
    return trim_right (trim_left (str));
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

    return ss.str ();
  }

  bool StringUtils::starts_with (const std::string& str, const std::string& prefix) {
    if (prefix.size () > str.size ()) {
      return false;
    }
    return std::equal (prefix.begin (), prefix.end (), str.begin ());
  }

  bool StringUtils::ends_with (const std::string& str, const std::string& suffix) {
    if (suffix.size () > str.size ()) {
      return false;
    }
    return std::equal (suffix.rbegin (), suffix.rend (), str.rbegin ());
  }

  bool StringUtils::contains (const std::string& str, const std::string& substr) {
    return str.find (substr) != std::string::npos;
  }

  std::string StringUtils::replace (const std::string& str, const std::string& from,
      const std::string& to) {
    size_t pos = str.find (from);
    if (pos == std::string::npos) {
      return str;
    }
    std::string result = str;
    result.replace (pos, from.size (), to);
    return result;
  }

  std::string StringUtils::replace_all (const std::string& str, const std::string& from,
      const std::string& to) {
    if (from.empty ()) {
      return str;
    }

    std::string result = str;
    size_t pos = 0;

    while ((pos = result.find (from, pos)) != std::string::npos) {
      result.replace (pos, from.size (), to);
      pos += to.size ();
    }

    return result;
  }

  bool StringUtils::equals_ignore_case (const std::string& a, const std::string& b) {
    if (a.size () != b.size ()) {
      return false;
    }
    return std::equal (a.begin (), a.end (), b.begin (),
        [] (unsigned char ca, unsigned char cb) { return std::tolower (ca) == std::tolower (cb); });
  }

} // namespace OmniCpp::Engine::Utils
