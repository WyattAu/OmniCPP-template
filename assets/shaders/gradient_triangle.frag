#version 450

// Graphics consumer of the compute-filled gradient buffer: maps the fragment
// y position (via the built-in gl_FragCoord and a push-constant target height)
// to a buffer index and emits that color. Verifies the compute->graphics
// data handoff: the drawn content must equal the computed gradient.

layout(location = 0) in vec3 color;
layout(location = 0) out vec4 out_color;

layout(binding = 0) restrict readonly buffer Gradient {
    vec4 values[];
} gradient;

layout(push_constant) uniform Push {
    uint value_count;   // must match the compute pass's count
    float pad0;
    float pad1;
    float pad2;
} push;

void main() {
    // The triangle spans the viewport vertically; map y to a buffer index.
    float y01 = clamp(gl_FragCoord.y / float(push.value_count), 0.0, 1.0);
    uint index = uint(y01 * float(push.value_count - 1u));
    out_color = gradient.values[index];
}
