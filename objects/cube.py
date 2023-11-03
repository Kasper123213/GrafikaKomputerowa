import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),

        (2, 1),
        (2, 3),
        (2, 6),

        (4, 5),
        (4, 7),

        (6, 5),
        (6, 7),

        (3, 7),
        (1, 5)
    )

    surfaces = (
        (0, 1, 2, 3),
        (0, 1, 5, 4),
        (0, 4, 7, 3),
        (4, 5, 6, 7),
        (3, 2, 6, 7),
        (1, 5, 6, 2)
    )

    colors = (
        (0, 0, 1),
        (0, 0, 1),
        (1, 0, 0),
        (0, 0, 1),
        (1, 0, 0),
        (1, 0, 0)
    )

    def __init__(self, center):
        self.vertices = (
            (1+center[0], -1+center[1], -1+center[2]),
            (1+center[0], -1+center[1], 1+center[2]),
            (-1+center[0], -1+center[1], 1+center[2]),
            (-1+center[0], -1+center[1], -1+center[2]),

            (1+center[0], 1+center[1], -1+center[2]),
            (1+center[0], 1+center[1], 1+center[2]),
            (-1+center[0], 1+center[1], 1+center[2]),
            (-1+center[0], 1+center[1], -1+center[2]),
        )
    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for i, vertex in enumerate(surface):
                glColor3fv(self.colors[i])
                # glColor3fv((1.0, 0.5, 0.5))
                glVertex3fv(self.vertices[vertex])
        glEnd()
