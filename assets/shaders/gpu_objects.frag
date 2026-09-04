#version 450

// gpu_objects.frag — flat per-instance color from the vertex stage.

layout(location = 0) in vec3 v_color;
layout(location = 0) out vec4 out_color;

void main() {
  out_color = vec4(v_color, 1.0);
}
