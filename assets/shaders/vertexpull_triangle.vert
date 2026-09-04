#version 450

// vertexpull_triangle.vert — vertex pulling: no vertex attributes bound;
// positions and hues come from a storage buffer filled by compute. The
// fragment shader receives an interpolated hue vector.

layout(location = 0) out vec4 v_hue;

layout(set = 0, binding = 0, std430) readonly buffer VertexBuffer {
  vec4 data[];  // data[0..2]: clip positions, data[3..5]: hue vectors
};

void main() {
  const uint i = uint(gl_VertexIndex);
  gl_Position = data[i];
  v_hue = data[3 + i];
}
