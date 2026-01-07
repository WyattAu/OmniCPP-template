#pragma once

#include <concepts>
#include <type_traits>

namespace math {

    // Concept for arithmetic types
    template<typename T>
    concept Arithmetic = std::is_arithmetic_v<T>;

    // Function to add two numbers
    template<Arithmetic T>
    T add(T a, T b) {
        return a + b;
    }

    // Function to multiply two numbers
    template<Arithmetic T>
    T multiply(T a, T b) {
        return a * b;
    }

    // Constant for PI
    constexpr double PI = 3.141592653589793;

    // Function to calculate factorial
    int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

} // namespace math