#version 450

layout(location = 0) in vec3 color;
layout(location = 0) out vec4 out_color;

layout(binding = 0) uniform Ubo {
    float tint;   // 0.0 = original colors, 1.0 = fully tinted
} ubo;

void main() {
    const vec3 tint_color = vec3(0.2, 0.15, 0.9);
    const vec3 mixed = mix(color, tint_color, vec3(clamp(ubo.tint, 0.0, 1.0)));
    out_color = vec4(mixed, 1.0);
}
