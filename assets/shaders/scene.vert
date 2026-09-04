#version 450

// scene.vert — instanced scene geometry with per-instance model data pulled
// from a storage buffer (no vertex attributes). Instance words (8 per
// instance): pos.xyz, scale, color.rgb, shape (0 = cube, 1 = ground slab).
// Outputs world position + normal for lambert + specular lighting in the
// fragment stage. Winding is authored CW in view space so the projection's
// y-flip lands it CCW in framebuffer space (matches the pipeline's
// COUNTER_CLOCKWISE front face).

layout(location = 0) out vec3 v_world_pos;
layout(location = 1) out vec3 v_normal;
layout(location = 2) out vec3 v_color;

layout(set = 0, binding = 0, std430) readonly buffer InstanceBuffer {
  uint words[];  // 8 per instance, instance i at words[8*i]
} inst;

layout(push_constant) uniform Push {
  mat4 view_proj;  // column-major
  uint instance_count;
  uint pad0;
  uint pad1;
} push;

// Unit cube centered at origin, edge 2. Faces authored CW when viewed from
// outside in a y-up right-handed space (see file comment).
const vec3 CUBE[36] = vec3[36](
  vec3(-1,-1, 1), vec3( 1, 1, 1), vec3( 1,-1, 1),
  vec3(-1,-1, 1), vec3(-1, 1, 1), vec3( 1, 1, 1),
  vec3( 1,-1,-1), vec3(-1, 1,-1), vec3(-1,-1,-1),
  vec3( 1,-1,-1), vec3( 1, 1,-1), vec3(-1, 1,-1),
  vec3( 1,-1, 1), vec3( 1, 1, 1), vec3( 1, 1,-1),
  vec3( 1,-1, 1), vec3( 1, 1,-1), vec3( 1,-1,-1),
  vec3(-1,-1,-1), vec3(-1, 1,-1), vec3(-1, 1, 1),
  vec3(-1,-1,-1), vec3(-1, 1, 1), vec3(-1,-1, 1),
  vec3(-1, 1, 1), vec3(-1, 1,-1), vec3( 1, 1,-1),
  vec3(-1, 1, 1), vec3( 1, 1,-1), vec3( 1, 1, 1),
  vec3(-1,-1,-1), vec3( 1,-1,-1), vec3( 1,-1, 1),
  vec3(-1,-1,-1), vec3( 1,-1, 1), vec3(-1,-1, 1)
);
const vec3 CUBE_N[6] = vec3[6](
  vec3(0,0, 1), vec3(0,0,-1), vec3(1,0,0),
  vec3(-1,0,0), vec3(0,1,0), vec3(0,-1,0)
);

void main() {
  const uint idx = uint(gl_InstanceIndex);
  const uint base = idx * 8u;
  const vec3 pos = vec3(uintBitsToFloat(inst.words[base + 0u]),
                        uintBitsToFloat(inst.words[base + 1u]),
                        uintBitsToFloat(inst.words[base + 2u]));
  const float scale = uintBitsToFloat(inst.words[base + 3u]);
  v_color = vec3(uintBitsToFloat(inst.words[base + 4u]),
                 uintBitsToFloat(inst.words[base + 5u]),
                 uintBitsToFloat(inst.words[base + 6u]));
  const uint shape = inst.words[base + 7u];

  vec3 local;
  vec3 normal;
  if (shape == 0u) {
    local = CUBE[gl_VertexIndex];
    normal = CUBE_N[gl_VertexIndex / 6u];
  } else {
    // Ground slab: 2 x 0.1 x 2 plate.
    local = CUBE[gl_VertexIndex] * vec3(1.0, 0.05, 1.0);
    normal = CUBE_N[gl_VertexIndex / 6u];
  }

  const vec3 world = local * scale + pos;
  v_world_pos = world;
  v_normal = normal;
  gl_Position = push.view_proj * vec4(world, 1.0);
}
