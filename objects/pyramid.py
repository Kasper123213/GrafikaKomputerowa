from OpenGL.GL import *
from math import sqrt

from OpenGL.raw.GLU import gluCylinder, gluDisk


class Pyramid:
    edges = (
        (0, 1),
        (1, 2),
        (2, 0),

        (3, 0),
        (3, 1),
        (3, 2)
    )

    surfaces = (
        (0, 1, 2),

        (2, 0, 3),
        (1, 2, 3),
        (0, 1, 3),
    )

    colors = (
        (1, 0, 0),
        (1, 1, 0),
        (1, 0, 1),
        (0, 0, 1),
    )

    def __init__(self, top, size):
        self.height = size*sqrt(6)/3
        self.radius = size*sqrt(3)/3
        self.center = (top[0], top[1] - self.height, top[2])


    def draw(self, quadric):
        glTranslatef(self.center[0], self.center[1], self.center[2])
        glRotatef(-90, 1, 0, 0)

        gluCylinder(quadric, self.radius, 0, self.height, 3, 1)
        gluDisk(quadric, 0, self.radius, 3, 1)

        glRotatef(90, 1, 0, 0)
        glTranslatef(-self.center[0], -self.center[1], -self.center[2])

