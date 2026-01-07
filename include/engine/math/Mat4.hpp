/**
 * @file Mat4.hpp
 * @brief 4x4 matrix class for 3D transformations
 * @version 1.0.0
 */

#pragma once

#include "Vec3.hpp"
#include <cmath>
#include <iostream>

namespace omnicpp {
namespace math {

/**
 * @brief 4x4 matrix class for 3D transformations
 */
class Mat4 {
public:
    /**
     * @brief Matrix data stored in column-major order
     */
    float m[4][4];

    /**
     * @brief Default constructor - initializes to identity matrix
     */
    Mat4() {
        identity();
    }

    /**
     * @brief Constructor with initial values
     * @param values Array of 16 values in column-major order
     */
    explicit Mat4(const float* values) {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                m[i][j] = values[i * 4 + j];
            }
        }
    }

    /**
     * @brief Copy constructor
     * @param other Matrix to copy from
     */
    Mat4(const Mat4& other) {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                m[i][j] = other.m[i][j];
            }
        }
    }

    /**
     * @brief Assignment operator
     * @param other Matrix to assign from
     * @return Reference to this matrix
     */
    Mat4& operator=(const Mat4& other) {
        if (this != &other) {
            for (int i = 0; i < 4; ++i) {
                for (int j = 0; j < 4; ++j) {
                    m[i][j] = other.m[i][j];
                }
            }
        }
        return *this;
    }

    /**
     * @brief Set this matrix to identity
     * @return Reference to this matrix
     */
    Mat4& identity() {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                m[i][j] = (i == j) ? 1.0f : 0.0f;
            }
        }
        return *this;
    }

    /**
     * @brief Static identity matrix
     * @return Identity matrix
     */
    static Mat4 identity() {
        return Mat4();
    }

    /**
     * @brief Matrix multiplication
     * @param other Matrix to multiply with
     * @return Resulting matrix
     */
    Mat4 operator*(const Mat4& other) const {
        Mat4 result;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                result.m[i][j] = 0.0f;
                for (int k = 0; k < 4; ++k) {
                    result.m[i][j] += m[k][i] * other.m[j][k];
                }
            }
        }
        return result;
    }

    /**
     * @brief Vector multiplication (transform point)
     * @param vec Vector to transform
     * @return Transformed vector
     */
    Vec3 operator*(const Vec3& vec) const {
        float x = m[0][0] * vec.x + m[1][0] * vec.y + m[2][0] * vec.z + m[3][0];
        float y = m[0][1] * vec.x + m[1][1] * vec.y + m[2][1] * vec.z + m[3][1];
        float z = m[0][2] * vec.x + m[1][2] * vec.y + m[2][2] * vec.z + m[3][2];
        return Vec3(x, y, z);
    }

    /**
     * @brief Scalar multiplication
     * @param scalar Scalar value
     * @return Resulting matrix
     */
    Mat4 operator*(float scalar) const {
        Mat4 result;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                result.m[i][j] = m[i][j] * scalar;
            }
        }
        return result;
    }

    /**
     * @brief Matrix addition
     * @param other Matrix to add
     * @return Resulting matrix
     */
    Mat4 operator+(const Mat4& other) const {
        Mat4 result;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                result.m[i][j] = m[i][j] + other.m[i][j];
            }
        }
        return result;
    }

    /**
     * @brief Matrix subtraction
     * @param other Matrix to subtract
     * @return Resulting matrix
     */
    Mat4 operator-(const Mat4& other) const {
        Mat4 result;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                result.m[i][j] = m[i][j] - other.m[i][j];
            }
        }
        return result;
    }

    /**
     * @brief Matrix multiplication assignment
     * @param other Matrix to multiply with
     * @return Reference to this matrix
     */
    Mat4& operator*=(const Mat4& other) {
        *this = *this * other;
        return *this;
    }

    /**
     * @brief Scalar multiplication assignment
     * @param scalar Scalar value
     * @return Reference to this matrix
     */
    Mat4& operator*=(float scalar) {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                m[i][j] *= scalar;
            }
        }
        return *this;
    }

    /**
     * @brief Create translation matrix
     * @param translation Translation vector
     * @return Translation matrix
     */
    static Mat4 translation(const Vec3& translation) {
        Mat4 result;
        result.m[3][0] = translation.x;
        result.m[3][1] = translation.y;
        result.m[3][2] = translation.z;
        return result;
    }

    /**
     * @brief Create rotation matrix around X axis
     * @param angle Rotation angle in radians
     * @return Rotation matrix
     */
    static Mat4 rotation_x(float angle) {
        Mat4 result;
        float c = std::cos(angle);
        float s = std::sin(angle);
        result.m[1][1] = c;
        result.m[1][2] = s;
        result.m[2][1] = -s;
        result.m[2][2] = c;
        return result;
    }

    /**
     * @brief Create rotation matrix around Y axis
     * @param angle Rotation angle in radians
     * @return Rotation matrix
     */
    static Mat4 rotation_y(float angle) {
        Mat4 result;
        float c = std::cos(angle);
        float s = std::sin(angle);
        result.m[0][0] = c;
        result.m[0][2] = -s;
        result.m[2][0] = s;
        result.m[2][2] = c;
        return result;
    }

    /**
     * @brief Create rotation matrix around Z axis
     * @param angle Rotation angle in radians
     * @return Rotation matrix
     */
    static Mat4 rotation_z(float angle) {
        Mat4 result;
        float c = std::cos(angle);
        float s = std::sin(angle);
        result.m[0][0] = c;
        result.m[0][1] = s;
        result.m[1][0] = -s;
        result.m[1][1] = c;
        return result;
    }

    /**
     * @brief Create rotation matrix from Euler angles
     * @param euler Rotation vector (pitch, yaw, roll) in radians
     * @return Rotation matrix
     */
    static Mat4 rotation(const Vec3& euler) {
        return rotation_x(euler.x) * rotation_y(euler.y) * rotation_z(euler.z);
    }

    /**
     * @brief Create scale matrix
     * @param scale Scale vector
     * @return Scale matrix
     */
    static Mat4 scale(const Vec3& scale) {
        Mat4 result;
        result.m[0][0] = scale.x;
        result.m[1][1] = scale.y;
        result.m[2][2] = scale.z;
        return result;
    }

    /**
     * @brief Create transformation matrix from position, rotation, and scale
     * @param position Position vector
     * @param rotation Rotation vector (Euler angles in radians)
     * @param scale Scale vector
     * @return Transformation matrix
     */
    static Mat4 transform(const Vec3& position, const Vec3& rotation, const Vec3& scale) {
        return translation(position) * rotation(rotation) * scale(scale);
    }

    /**
     * @brief Create perspective projection matrix
     * @param fov Field of view in radians
     * @param aspect Aspect ratio (width/height)
     * @param near Near clipping plane
     * @param far Far clipping plane
     * @return Perspective projection matrix
     */
    static Mat4 perspective(float fov, float aspect, float near, float far) {
        Mat4 result;
        float tan_half_fov = std::tan(fov / 2.0f);
        result.m[0][0] = 1.0f / (aspect * tan_half_fov);
        result.m[1][1] = 1.0f / tan_half_fov;
        result.m[2][2] = -(far + near) / (far - near);
        result.m[2][3] = -1.0f;
        result.m[3][2] = -(2.0f * far * near) / (far - near);
        result.m[3][3] = 0.0f;
        return result;
    }

    /**
     * @brief Create orthographic projection matrix
     * @param left Left clipping plane
     * @param right Right clipping plane
     * @param bottom Bottom clipping plane
     * @param top Top clipping plane
     * @param near Near clipping plane
     * @param far Far clipping plane
     * @return Orthographic projection matrix
     */
    static Mat4 orthographic(float left, float right, float bottom, float top, float near, float far) {
        Mat4 result;
        result.m[0][0] = 2.0f / (right - left);
        result.m[1][1] = 2.0f / (top - bottom);
        result.m[2][2] = -2.0f / (far - near);
        result.m[3][0] = -(right + left) / (right - left);
        result.m[3][1] = -(top + bottom) / (top - bottom);
        result.m[3][2] = -(far + near) / (far - near);
        return result;
    }

    /**
     * @brief Create look-at view matrix
     * @param eye Eye position
     * @param target Target position
     * @param up Up vector
     * @return Look-at view matrix
     */
    static Mat4 look_at(const Vec3& eye, const Vec3& target, const Vec3& up) {
        Vec3 f = (target - eye).normalized();
        Vec3 s = f.cross(up).normalized();
        Vec3 u = s.cross(f);

        Mat4 result;
        result.m[0][0] = s.x;
        result.m[1][0] = s.y;
        result.m[2][0] = s.z;
        result.m[0][1] = u.x;
        result.m[1][1] = u.y;
        result.m[2][1] = u.z;
        result.m[0][2] = -f.x;
        result.m[1][2] = -f.y;
        result.m[2][2] = -f.z;
        result.m[3][0] = -s.dot(eye);
        result.m[3][1] = -u.dot(eye);
        result.m[3][2] = f.dot(eye);
        return result;
    }

    /**
     * @brief Transpose matrix
     * @return Transposed matrix
     */
    Mat4 transposed() const {
        Mat4 result;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                result.m[i][j] = m[j][i];
            }
        }
        return result;
    }

    /**
     * @brief Calculate determinant of matrix
     * @return Determinant
     */
    float determinant() const {
        // Calculate determinant using cofactor expansion
        float det = 0.0f;
        for (int i = 0; i < 4; ++i) {
            float sub_det = 0.0f;
            for (int j = 0; j < 4; ++j) {
                if (j != i) {
                    for (int k = 0; k < 4; ++k) {
                        if (k != i) {
                            int indices[2];
                            int idx = 0;
                            for (int l = 0; l < 4; ++l) {
                                if (l != i && l != j) {
                                    indices[idx++] = l;
                                }
                            }
                            float minor = m[indices[0]][k] * m[indices[1]][3] - m[indices[0]][3] * m[indices[1]][k];
                            sub_det += minor * ((j + k) % 2 == 0 ? 1.0f : -1.0f);
                        }
                    }
                }
            }
            det += m[i][0] * sub_det * ((i % 2 == 0) ? 1.0f : -1.0f);
        }
        return det;
    }

    /**
     * @brief Calculate inverse of matrix
     * @return Inverted matrix
     */
    Mat4 inverse() const {
        // Simplified inverse calculation for transformation matrices
        // For a full implementation, use Gaussian elimination or adjugate method
        Mat4 result;
        float det = determinant();
        if (std::abs(det) < 1e-6f) {
            return result; // Return identity if singular
        }
        
        // For now, return identity (full implementation is complex)
        // TODO: Implement proper matrix inversion
        return result;
    }

    /**
     * @brief Output stream operator
     * @param os Output stream
     * @param mat Matrix to output
     * @return Output stream
     */
    friend std::ostream& operator<<(std::ostream& os, const Mat4& mat) {
        os << "Mat4(\n";
        for (int i = 0; i < 4; ++i) {
            os << "  [";
            for (int j = 0; j < 4; ++j) {
                os << mat.m[i][j];
                if (j < 3) os << ", ";
            }
            os << "]";
            if (i < 3) os << ",\n";
        }
        os << "\n)";
        return os;
    }
};

} // namespace math
} // namespace omnicpp
