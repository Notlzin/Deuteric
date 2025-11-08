#version 330 core
layout(location = 0) in vec2 aPos;

void main() {
    // gl coords: -1.0 to 1.0, z=0, w=1
    gl_Position = vec4(aPos, 0.0, 1.0);
}
