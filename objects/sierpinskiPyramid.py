from math import sqrt
from objects.pyramid import Pyramid
class SierpinskiPyramid:
    pyramids = []
    def __init__(self, top, size, lvl):
        self.makePyramid(top, size, lvl)


    def makePyramid(self, top, size, lvl):
        if lvl <= 1:
            self.pyramids.append(Pyramid(top, size))
            return

        size /= 2
        self.makePyramid(top, size, lvl - 1)

        vertexA = (top[0], top[1]-size*sqrt(6)/3, top[2]-size*sqrt(3)/3)
        self.makePyramid(vertexA, size, lvl-1)

        vertexB = (top[0]-size/2, top[1]-size*sqrt(6)/3,top[2]+size*sqrt(3)/6)
        self.makePyramid(vertexB, size, lvl-1)

        vertexC = (top[0]+size/2, top[1]-size*sqrt(6)/3,top[2]+size*sqrt(3)/6)
        self.makePyramid(vertexC, size, lvl-1)



    def draw(self):
        for f in self.pyramids:
            f.draw()