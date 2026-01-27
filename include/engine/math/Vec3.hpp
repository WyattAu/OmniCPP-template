/**
 * @file Vec3.hpp
 * @brief 3D vector class for mathematical operations
 * @version 1.0.0
 */

#pragma once

#include <cmath>
#include <iostream>

namespace omnicpp {
namespace math {

/**
 * @brief 3D vector class for position, rotation, and scale operations
 */
class Vec3 {
public:
    float x;
    float y;
    float z;

    /**
     * @brief Default constructor - initializes to zero vector
     */
    Vec3() : x(0.0f), y(0.0f), z(0.0f) {}

    /**
     * @brief Constructor with initial values
     * @param x X component
     * @param y Y component
     * @param z Z component
     */
    Vec3(float x, float y, float z) : x(x), y(y), z(z) {}

    /**
     * @brief Copy constructor
     * @param other Vector to copy from
     */
    Vec3(const Vec3& other) : x(other.x), y(other.y), z(other.z) {}

    /**
     * @brief Assignment operator
     * @param other Vector to assign from
     * @return Reference to this vector
     */
    Vec3& operator=(const Vec3& other) {
        if (this != &other) {
            x = other.x;
            y = other.y;
            z = other.z;
        }
        return *this;
    }

    /**
     * @brief Addition operator
     * @param other Vector to add
     * @return Resulting vector
     */
    Vec3 operator+(const Vec3& other) const {
        return Vec3(x + other.x, y + other.y, z + other.z);
    }

    /**
     * @brief Subtraction operator
     * @param other Vector to subtract
     * @return Resulting vector
     */
    Vec3 operator-(const Vec3& other) const {
        return Vec3(x - other.x, y - other.y, z - other.z);
    }

    /**
     * @brief Scalar multiplication operator
     * @param scalar Scalar value
     * @return Resulting vector
     */
    Vec3 operator*(float scalar) const {
        return Vec3(x * scalar, y * scalar, z * scalar);
    }

    /**
     * @brief Scalar division operator
     * @param scalar Scalar value
     * @return Resulting vector
     */
    Vec3 operator/(float scalar) const {
        return Vec3(x / scalar, y / scalar, z / scalar);
    }

    /**
     * @brief Addition assignment operator
     * @param other Vector to add
     * @return Reference to this vector
     */
    Vec3& operator+=(const Vec3& other) {
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
    }

    /**
     * @brief Subtraction assignment operator
     * @param other Vector to subtract
     * @return Reference to this vector
     */
    Vec3& operator-=(const Vec3& other) {
        x -= other.x;
        y -= other.y;
        z -= other.z;
        return *this;
    }

    /**
     * @brief Scalar multiplication assignment operator
     * @param scalar Scalar value
     * @return Reference to this vector
     */
    Vec3& operator*=(float scalar) {
        x *= scalar;
        y *= scalar;
        z *= scalar;
        return *this;
    }

    /**
     * @brief Scalar division assignment operator
     * @param scalar Scalar value
     * @return Reference to this vector
     */
    Vec3& operator/=(float scalar) {
        x /= scalar;
        y /= scalar;
        z /= scalar;
        return *this;
    }

    /**
     * @brief Equality operator
     * @param other Vector to compare
     * @return True if vectors are equal
     */
    bool operator==(const Vec3& other) const {
        return x == other.x && y == other.y && z == other.z;
    }

    /**
     * @brief Inequality operator
     * @param other Vector to compare
     * @return True if vectors are not equal
     */
    bool operator!=(const Vec3& other) const {
        return !(*this == other);
    }

    /**
     * @brief Negation operator
     * @return Negated vector
     */
    Vec3 operator-() const {
        return Vec3(-x, -y, -z);
    }

    /**
     * @brief Calculate dot product with another vector
     * @param other Vector to calculate dot product with
     * @return Dot product
     */
    float dot(const Vec3& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    /**
     * @brief Calculate cross product with another vector
     * @param other Vector to calculate cross product with
     * @return Cross product
     */
    Vec3 cross(const Vec3& other) const {
        return Vec3(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }

    /**
     * @brief Calculate length (magnitude) of the vector
     * @return Length of the vector
     */
    float length() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    /**
     * @brief Calculate squared length of the vector
     * @return Squared length of the vector
     */
    float length_squared() const {
        return x * x + y * y + z * z;
    }

    /**
     * @brief Normalize the vector to unit length
     * @return Normalized vector
     */
    Vec3 normalized() const {
        float len = length();
        if (len > 0.0f) {
            return *this / len;
        }
        return Vec3();
    }

    /**
     * @brief Normalize this vector in place
     */
    void normalize() {
        float len = length();
        if (len > 0.0f) {
            x /= len;
            y /= len;
            z /= len;
        }
    }

    /**
     * @brief Calculate distance to another vector
     * @param other Vector to calculate distance to
     * @return Distance between vectors
     */
    float distance_to(const Vec3& other) const {
        return (*this - other).length();
    }

    /**
     * @brief Calculate squared distance to another vector
     * @param other Vector to calculate distance to
     * @return Squared distance between vectors
     */
    float distance_squared_to(const Vec3& other) const {
        return (*this - other).length_squared();
    }

    /**
     * @brief Linear interpolation between this vector and another
     * @param other Other vector
     * @param t Interpolation factor (0.0 to 1.0)
     * @return Interpolated vector
     */
    Vec3 lerp(const Vec3& other, float t) const {
        return *this + (other - *this) * t;
    }

    /**
     * @brief Output stream operator
     * @param os Output stream
     * @param vec Vector to output
     * @return Output stream
     */
    friend std::ostream& operator<<(std::ostream& os, const Vec3& vec) {
        os << "Vec3(" << vec.x << ", " << vec.y << ", " << vec.z << ")";
        return os;
    }

    /**
     * @brief Static zero vector
     * @return Zero vector (0, 0, 0)
     */
    static Vec3 zero() {
        return Vec3(0.0f, 0.0f, 0.0f);
    }

    /**
     * @brief Static one vector
     * @return One vector (1, 1, 1)
     */
    static Vec3 one() {
        return Vec3(1.0f, 1.0f, 1.0f);
    }

    /**
     * @brief Static up vector
     * @return Up vector (0, 1, 0)
     */
    static Vec3 up() {
        return Vec3(0.0f, 1.0f, 0.0f);
    }

    /**
     * @brief Static down vector
     * @return Down vector (0, -1, 0)
     */
    static Vec3 down() {
        return Vec3(0.0f, -1.0f, 0.0f);
    }

    /**
     * @brief Static left vector
     * @return Left vector (-1, 0, 0)
     */
    static Vec3 left() {
        return Vec3(-1.0f, 0.0f, 0.0f);
    }

    /**
     * @brief Static right vector
     * @return Right vector (1, 0, 0)
     */
    static Vec3 right() {
        return Vec3(1.0f, 0.0f, 0.0f);
    }

    /**
     * @brief Static forward vector
     * @return Forward vector (0, 0, 1)
     */
    static Vec3 forward() {
        return Vec3(0.0f, 0.0f, 1.0f);
    }

    /**
     * @brief Static back vector
     * @return Back vector (0, 0, -1)
     */
    static Vec3 back() {
        return Vec3(0.0f, 0.0f, -1.0f);
    }
};

} // namespace math
} // namespace omnicpp
