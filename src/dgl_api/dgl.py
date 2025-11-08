# dgl.py
# wait we have
import glfw
from OpenGL.GL import (
    glClearColor, glClear, glBegin, glEnd, glVertex2f,
    glColor3f, glMatrixMode, glLoadIdentity, glOrtho,
    GL_COLOR_BUFFER_BIT, GL_PROJECTION, GL_MODELVIEW,
    GL_QUADS, GL_TRIANGLE_FAN
)
from math import cos, sin, pi


class dGL:
    def __init__(self, w=800, h=600, title="dGL:GPU_edition"):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.width = w
        self.height = h
        self.window = glfw.create_window(w, h, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def dglClear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def dglDrawRect(self, x, y, w, h, color):
        r, g, b = [c / 255 for c in color]
        glColor3f(r, g, b)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    def dglDrawCircle(self, cx, cy, radius, color, segments=64):
        r, g, b = [c / 255 for c in color]
        glColor3f(r, g, b)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)
        for i in range(segments + 1):
            angle = 2 * pi * i / segments
            glVertex2f(cx + radius * cos(angle), cy + radius * sin(angle))
        glEnd()

    def dglRun(self, func):
        # main render loop
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            func(self)
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()
