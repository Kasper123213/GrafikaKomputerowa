#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import *

from objects.sierpinskiPyramid import SierpinskiPyramid


def startup():
    update_viewport(None, display[0], display[1])
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # #ustawianie swiatła punktowego
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass






def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()





def render(time):
    # glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    axes()
    glRotatef(time * 180 / pi /2, 0, -1, 0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    figure.draw(quadric)
    #################################
    # glRotatef(-90, 1, 0, 0)
    # quadric = gluNewQuadric()
    #
    # gluQuadricDrawStyle(quadric, GLU_FILL);
    # gluCylinder(quadric, 4.0, 0, 4.0, 3, 1)
    # #(quadratic, podstawa1, podstawa2, promien(wysokosc),  liczbaBokow, 1)
    # gluQuadricOrientation(quadric, GLU_INSIDE)
    # gluDisk(quadric, 0, 4, 3, 1)
    # #(quadratic, 0, promien, boki, 1)
    #
    # gluDeleteQuadric(quadric)
    #################################
    glFlush()






def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(display[0], display[1], __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)


    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()



#ilość poziomów piramidy
# lvl = int(input("Podaj wartość do wygenerowania piramidy. wartość powinna być liczbą całkowitą większą od 0 : \n"))
lvl = 1 #todo

size = 7         #rozmiar piramidy
topPos = (0,size*sqrt(6)/6,0)    #pozycja górnego wierzchołka od którego rysowane są kolejne

figure = SierpinskiPyramid(topPos, size, lvl)   # tworzenie piramidy

light_ambient = [0, 0, 0, 1]    #kolor cienia
light_diffuse = [.8, .8, .1, 1] #kolor światła
light_specular = [0, 0, 0, 1]   #kolor światła (blask)

light_position = [5, -5, 1, 1]   #połorzenie światła



display = (1000, 800)

viewer = [0.0, 0.0, 3.0]

if __name__ == '__main__':
    main()