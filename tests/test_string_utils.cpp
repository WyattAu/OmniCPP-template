#include <catch2/catch_test_macros.hpp>
#include <vector>
#include <string>
import string_utils;

TEST_CASE("String utils module tests", "[string_utils]") {
    SECTION("split function") {
        auto result = string_utils::split("hello,world,test", ',');
        REQUIRE(result.size() == 3);
        REQUIRE(result[0] == "hello");
        REQUIRE(result[1] == "world");
        REQUIRE(result[2] == "test");

        auto empty_split = string_utils::split("", ',');
        REQUIRE(empty_split.size() == 1);
        REQUIRE(empty_split[0] == "");

        auto no_delimiter = string_utils::split("hello", ',');
        REQUIRE(no_delimiter.size() == 1);
        REQUIRE(no_delimiter[0] == "hello");
    }

    SECTION("join function") {
        std::vector<std::string> strings = {"hello", "world", "test"};
        auto result = string_utils::join(strings, ", ");
        REQUIRE(result == "hello, world, test");

        std::vector<std::string> empty_vec;
        auto empty_join = string_utils::join(empty_vec, ", ");
        REQUIRE(empty_join == "");

        std::vector<std::string> single = {"single"};
        auto single_join = string_utils::join(single, ", ");
        REQUIRE(single_join == "single");
    }

    SECTION("to_upper function") {
        REQUIRE(string_utils::to_upper("hello") == "HELLO");
        REQUIRE(string_utils::to_upper("Hello World") == "HELLO WORLD");
        REQUIRE(string_utils::to_upper("123abc") == "123ABC");
        REQUIRE(string_utils::to_upper("") == "");
    }

    SECTION("to_lower function") {
        REQUIRE(string_utils::to_lower("HELLO") == "hello");
        REQUIRE(string_utils::to_lower("Hello World") == "hello world");
        REQUIRE(string_utils::to_lower("123ABC") == "123abc");
        REQUIRE(string_utils::to_lower("") == "");
    }

    SECTION("trim function") {
        REQUIRE(string_utils::trim("  hello  ") == "hello");
        REQUIRE(string_utils::trim("\t\n hello \t\n") == "hello");
        REQUIRE(string_utils::trim("hello") == "hello");
        REQUIRE(string_utils::trim("") == "");
        REQUIRE(string_utils::trim("   ") == "");
    }
}