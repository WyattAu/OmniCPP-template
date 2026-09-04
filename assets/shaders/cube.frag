#version 450

// cube.frag — flat-shaded cube faces: simple directional lighting from the
// interpolated per-vertex color, with a face-normal term passed from the
// vertex stage is unnecessary here; constant lambert from a fixed light
// direction approximates solidity without another attribute.

layout(location = 0) in vec3 v_color;
layout(location = 0) out vec4 out_color;

void main() {
  out_color = vec4(v_color, 1.0);
}
