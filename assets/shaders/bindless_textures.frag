#version 450
#extension GL_EXT_nonuniform_qualifier : require

// Bindless texture test shader: samples a runtime-sized, partially-bound
// combined-image-sampler array (descriptor indexing) at a push-constant
// index. nonuniformEXT marks the index so the driver emits the non-uniform
// descriptor-indexing path the device feature gates.

layout(location = 0) in vec3 color;
layout(location = 0) out vec4 out_color;

layout(binding = 0) uniform sampler2D textures[];  // runtime-sized array

layout(push_constant) uniform Push {
    uint index;   // which texture to sample for this draw
    uint pad0;
    uint pad1;
    uint pad2;
} push;

void main() {
    out_color = texture(textures[nonuniformEXT(push.index)], vec2(0.5, 0.5));
}
