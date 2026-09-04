#version 450

// Bindless test shader: the fragment color is selected by indexing a
// runtime-sized, partially-bound SSBO array (descriptor indexing) with a
// push-constant band index supplied per draw.

layout(location = 0) in vec3 color;
layout(location = 0) out vec4 out_color;

layout(binding = 0) restrict readonly buffer Palette {
    vec4 values[];   // runtime-sized array: requires runtimeDescriptorArray
} palettes[];

layout(push_constant) uniform Push {
    uint index;      // which palette entry to use for this draw
} push;

void main() {
    out_color = palettes[0].values[push.index];
}
