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




    #ustawianie swiatła
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)
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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


    gluLookAt(viewer[0], viewer[1], viewer[2], .0, .0, .0, .0, 1.0, .0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glScale(viewerMoveVector[2], viewerMoveVector[2], viewerMoveVector[2])

    quadric = gluNewQuadric()

    glDisable(GL_LIGHTING)  #Światło nie wpływa na ten obiekt
    axes()  #osie

    #rysowanie zrodla swiatla
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(-light_position[0], -light_position[1], -light_position[2])

    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.1, 30, 30)


    glTranslatef(*light_position[:-1])

    glEnable(GL_LIGHTING)


    glRotatef(time * 180 / pi /4, 0, -1, 0)



    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    figure.draw(quadric)
    glFlush()


    if viewerMoveVector[0] != 0:
        viewerAngles[0] += viewerMoveVector[0] * viewerSpeed
        calcViewerPose()
    if viewerMoveVector[1] != 0:
        viewerAngles[1] += viewerMoveVector[1] * viewerSpeed
        calcViewerPose()





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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 20.5, -10.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 20.5, -10.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def calcViewerPose():
    viewer[0] = viewerAngles[2] * cos(viewerAngles[1]) * cos(viewerAngles[0])
    viewer[1] = viewerAngles[2] * sin(viewerAngles[1])
    viewer[2] = viewerAngles[2] * sin(viewerAngles[0]) * cos(viewerAngles[1])


def keyboard_key_callback(window, key, scancode, action, mods):

    if (key == GLFW_KEY_ESCAPE or key == GLFW_KEY_Q) and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        viewerMoveVector[0] = 1
    if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
        viewerMoveVector[0] = -1
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        viewerMoveVector[1] = -1
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        viewerMoveVector[1] = 1
    #light
    if key == GLFW_KEY_P and action == GLFW_PRESS:
        light_position[3] = 1
    if key == GLFW_KEY_K and action == GLFW_PRESS:
        light_position[3] = 0

        #zoom
    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        viewerMoveVector[2] *= deltaZoom
    if key == GLFW_KEY_X and action == GLFW_PRESS:
        viewerMoveVector[2] /= deltaZoom


    if (key == GLFW_KEY_RIGHT or key == GLFW_KEY_LEFT) and action == GLFW_RELEASE:
        viewerMoveVector[0] = 0
    if (key == GLFW_KEY_UP or key == GLFW_KEY_DOWN) and action == GLFW_RELEASE:
        viewerMoveVector[1] = 0












print("z - przybliż")
print("x - oddal")
print("UP, DOWN, LEFT, RIGHT strzałka - stwrowanie kamerą")
print("k - światło kierunkowe")
print("p - światło punktowe")
print("q - wyłączanie")
#ilość poziomów piramidy
# lvl = int(input("Podaj wartość do wygenerowania piramidy. wartość powinna być liczbą całkowitą większą od 0 : \n"))
lvl = 1 #todo

size = 7                        #rozmiar piramidy
topPos = (0,size*sqrt(6)/6,0)   #pozycja górnego wierzchołka od którego rysowane są kolejne

figure = SierpinskiPyramid(topPos, size, lvl)   # tworzenie piramidy



#parametry swiatla
mat_ambient = [0.0, 0.0, 0.0, 1.0]  #kolor odbity
mat_diffuse = [1.0, 0.0, 0.0, 1.0]  #kolor rozproszony
mat_specular = [0.0, 0.0, 0.0, 1.0] #kolor odbijanego swiatla
mat_shininess = 30.0

light_ambient = [0.0, 0.0, 0.0, 1.0]    #kolor otoczenia
light_diffuse = [.9, .0, .0, 1.0]    #kolor swiatła rozproszonego
light_specular = [.9, .9, .9, 1.0]   #kolor odbitego swiatla
light_position = [0.0, 0.0, 10.0, 1.0]  #punktowe #pozycja źrodla swiatła
# light_position = [10.0, 5.0, 1.0, 0.0]#kierunkowe

#tłumienie swiatla
att_constant = 1.0
att_linear = 0.001
att_quadratic = 0.0001

# mat_ambient = [1.0, 1.0, 1.0, 1.0]
# mat_diffuse = [1.0, 1.0, 1.0, 1.0]
# mat_specular = [1.0, 1.0, 1.0, 1.0]
# mat_shininess = 20.0
#
# light_ambient = [0.1, 0.1, 0.0, 1.0]
# light_diffuse = [0.8, 0.8, 0.0, 1.0]
# light_specular = [1.0, 1.0, 1.0, 1.0]
# light_position = [0.0, 0.0, 10.0, 1.0]
#
# att_constant = 1.0
# att_linear = 0.05
# att_quadratic = 0.001



display = (1000, 800)


#parametru kamery
viewerAngles = [pi/180 * 90, 0, 3]
viewer = [0.0, 0.0, 3.0]
viewerMoveVector = [0, 0, 1]#x, y, zoom
viewerSpeed = pi/180 * 0.5

deltaZoom = 1.1



if not glfwInit():
    sys.exit(-1)

window = glfwCreateWindow(display[0], display[1], __file__, None, None)
if not window:
    glfwTerminate()
    sys.exit(-1)

glfwMakeContextCurrent(window)
glfwSetFramebufferSizeCallback(window, update_viewport)
glfwSetKeyCallback(window, keyboard_key_callback)
glfwSwapInterval(1)

startup()
while not glfwWindowShouldClose(window):
    render(glfwGetTime())
    glfwSwapBuffers(window)
    glfwPollEvents()
shutdown()

glfwTerminate()
