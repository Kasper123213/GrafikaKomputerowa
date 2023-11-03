from OpenGL.GL import *
from math import sqrt
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
        self.vertices = (
            (top[0], top[1]-size*sqrt(6)/3, top[2]-size*sqrt(3)/3),
            (top[0]-size/2, top[1]-size*sqrt(6)/3,top[2]+size*sqrt(3)/6),
            (top[0]+size/2, top[1]-size*sqrt(6)/3,top[2]+size*sqrt(3)/6),

            top
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
                # glColor3fv((1.0, 1.0, 1.0))
                glVertex3fv(self.vertices[vertex])
        glEnd()