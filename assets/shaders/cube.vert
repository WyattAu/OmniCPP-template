#version 450

// cube.vert — vertex pulling for solid cube meshes. The SSBO holds the
// 36-vertex cube (position + color, 8 floats per vertex). The model matrix
// comes in via push constants so multiple cubes can be drawn from the same
// buffer with different transforms.

layout(set = 0, binding = 0, std430) readonly buffer MeshBuffer {
  float data[];  // 8 floats per vertex: pos.xyz(3) pad(1) color.rgb(3) pad(1)
} mesh;

layout(push_constant) uniform Push {
  mat4 view_proj;
  mat4 model;
} pc;

layout(location = 0) out vec3 v_color;

void main() {
  const uint base = uint(gl_VertexIndex) * 8u;
  const vec3 pos = vec3(mesh.data[base + 0u], mesh.data[base + 1u],
                        mesh.data[base + 2u]);
  v_color = vec3(mesh.data[base + 4u], mesh.data[base + 5u],
                 mesh.data[base + 6u]);
  gl_Position = pc.view_proj * (pc.model * vec4(pos, 1.0));
}
