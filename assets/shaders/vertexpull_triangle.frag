#version 450

// vertexpull_triangle.frag — pairs with vertexpull_triangle.vert: outputs the
// interpolated per-vertex hue pulled from the compute-filled storage buffer.
// The triangle's color therefore comes entirely from GPU-computed data.

layout(location = 0) in vec4 v_hue;
layout(location = 0) out vec4 out_color;

void main() {
  out_color = v_hue;
}
