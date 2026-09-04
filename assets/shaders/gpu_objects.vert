#version 450

// gpu_objects.vert — GPU-driven cube rendering: the cull compute pass
// compacts accepted instance indices; this shader resolves the instance via
// that list and pulls the cube geometry from a compile-time table (no
// vertex buffers bound).

layout(location = 0) out vec3 v_color;

// Binding 0, flat uint words (std430):
//   [0 .. N-1]          compacted accepted instance indices (cull output)
//   [N .. N+8M-1]       per-instance data: 8 words each
//                       (x, y, z, scale, r, g, b, unused)
layout(set = 0, binding = 0, std430) readonly buffer InstanceBuffer {
  uint words[];
} instances;

layout(push_constant) uniform Push {
  mat4 view_proj;   // column-major 4x4
  uint data_offset; // word index where instance data begins (== N)
  uint pad0;
  uint pad1;
  uint pad2;
} push;

// Unit cube, 36 vertices (12 triangles).
const vec3 CUBE[36] = vec3[36](
  vec3(-1,-1, 1), vec3( 1,-1, 1), vec3( 1, 1, 1),
  vec3(-1,-1, 1), vec3( 1, 1, 1), vec3(-1, 1, 1),
  vec3(-1,-1,-1), vec3(-1, 1,-1), vec3( 1, 1,-1),
  vec3(-1,-1,-1), vec3( 1, 1,-1), vec3( 1,-1,-1),
  vec3(-1, 1, 1), vec3( 1, 1, 1), vec3( 1, 1,-1),
  vec3(-1, 1, 1), vec3( 1, 1,-1), vec3(-1, 1,-1),
  vec3(-1,-1,-1), vec3( 1,-1,-1), vec3( 1,-1, 1),
  vec3(-1,-1,-1), vec3( 1,-1, 1), vec3(-1,-1, 1),
  vec3( 1,-1, 1), vec3( 1,-1,-1), vec3( 1, 1,-1),
  vec3( 1,-1, 1), vec3( 1, 1,-1), vec3( 1, 1, 1),
  vec3(-1,-1,-1), vec3(-1,-1, 1), vec3(-1, 1, 1),
  vec3(-1,-1,-1), vec3(-1, 1, 1), vec3(-1, 1,-1)
);

void main() {
  // gl_InstanceIndex enumerates the ACCEPTED set; the cull pass recorded
  // each accepted instance's original index in the compacted list.
  const uint instance = instances.words[gl_InstanceIndex];
  const uint base = push.data_offset + instance * 8u;
  const vec4 xform = vec4(uintBitsToFloat(instances.words[base + 0u]),
                          uintBitsToFloat(instances.words[base + 1u]),
                          uintBitsToFloat(instances.words[base + 2u]),
                          uintBitsToFloat(instances.words[base + 3u]));
  const vec4 tint = vec4(uintBitsToFloat(instances.words[base + 4u]),
                         uintBitsToFloat(instances.words[base + 5u]),
                         uintBitsToFloat(instances.words[base + 6u]),
                         uintBitsToFloat(instances.words[base + 7u]));

  const vec3 local = CUBE[gl_VertexIndex] * xform.w + xform.xyz;
  gl_Position = push.view_proj * vec4(local, 1.0);
  v_color = tint.rgb;
}
