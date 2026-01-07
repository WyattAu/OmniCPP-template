#include <catch2/catch_test_macros.hpp>
import math;

TEST_CASE("Math module tests", "[math]") {
    SECTION("add function") {
        REQUIRE(math::add(2, 3) == 5);
        REQUIRE(math::add(0, 0) == 0);
        REQUIRE(math::add(-1, 1) == 0);
        REQUIRE(math::add(1.5, 2.5) == 4.0);
    }

    SECTION("multiply function") {
        REQUIRE(math::multiply(2, 3) == 6);
        REQUIRE(math::multiply(0, 5) == 0);
        REQUIRE(math::multiply(-2, 3) == -6);
        REQUIRE(math::multiply(1.5, 2.0) == 3.0);
    }

    SECTION("PI constant") {
        REQUIRE(math::PI == Catch::Approx(3.141592653589793));
    }

    SECTION("factorial function") {
        REQUIRE(math::factorial(0) == 1);
        REQUIRE(math::factorial(1) == 1);
        REQUIRE(math::factorial(5) == 120);
        REQUIRE(math::factorial(10) == 3628800);
    }
}