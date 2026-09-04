#version 450

// scene.frag — directional lambert + specular lighting on the rasterized
// geometry, plus one analytically ray-traced sphere per pixel: a procedural
// object that requires no geometry at all. The sphere intersects the primary
// ray in front of the cubes, so correct depth ordering shows the sphere
// overlapping the cubes and the lit ground plane under everything.

layout(location = 0) in vec3 v_world_pos;
layout(location = 1) in vec3 v_normal;
layout(location = 2) in vec3 v_color;
layout(location = 0) out vec4 out_color;

layout(push_constant) uniform Push {
  mat4 view_proj;   // matches scene.vert layout
  uint instance_count;
  uint pad0;
  uint pad1;
  // --- extended block (fragment-only reads, beyond the vertex block) ---
  vec3 camera_pos;
  float pad2;
  vec3 sphere_center;
  float sphere_radius;
  vec3 light_dir;   // normalized, pointing TOWARD the light
  float pad3;
} push;

//! Lambert + Blinn-Phong for one light; ambient floors the shadow side.
vec3 shade(vec3 albedo, vec3 n, vec3 view_dir, vec3 light_dir) {
  const float ndl = max(dot(n, light_dir), 0.0);
  const vec3 h = normalize(light_dir + view_dir);
  const float spec = pow(max(dot(n, h), 0.0), 32.0) * 0.5;
  return albedo * (0.15 + 0.85 * ndl) + vec3(spec);
}

void main() {
  const vec3 view_dir = normalize(push.camera_pos - v_world_pos);
  vec3 color;

  // Primary ray for the analytic sphere.
  const vec3 rd = normalize(v_world_pos - push.camera_pos);
  const vec3 oc = push.camera_pos - push.sphere_center;
  const float b = dot(oc, rd);
  const float c = dot(oc, oc) - push.sphere_radius * push.sphere_radius;
  const float disc = b * b - c;

  if (disc > 0.0) {
    const float t = -b - sqrt(disc);
    if (t > 0.0) {
      // Ray hit the sphere in front of this fragment: shade the sphere.
      const vec3 hit = push.camera_pos + rd * t;
      const vec3 n = normalize(hit - push.sphere_center);
      color = shade(vec3(0.9, 0.35, 0.15), n, view_dir, push.light_dir);
      out_color = vec4(color, 1.0);
      return;
    }
  }

  // Rasterized surface shading.
  color = shade(v_color, normalize(v_normal), view_dir, push.light_dir);
  out_color = vec4(color, 1.0);
}
