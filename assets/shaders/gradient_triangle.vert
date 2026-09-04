#version 450

// Full-viewport triangle: covers the whole target so the fragment shader can
// map gl_FragCoord across the entire vertical range.

layout(location = 0) out vec3 color;

void main() {
  vec2 pos = vec2(
      (gl_VertexIndex == 2) ? 3.0 : (gl_VertexIndex == 1) ? -1.0 : -1.0,
      (gl_VertexIndex == 2) ? -3.0 : (gl_VertexIndex == 1) ? 3.0 : -1.0);
  gl_Position = vec4(pos, 0.0, 1.0);
  color = vec3(pos * 0.5 + 0.5, 0.5);
}
