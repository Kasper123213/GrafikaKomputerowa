#!/usr/bin/env python3
import sys
import os

from PIL import Image
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import *

from objects.sierpinskiPyramid import SierpinskiPyramid


def countFiles(folder_path):
    try:
        # Uzyskaj listę plików w danym folderze
        files = os.listdir(folder_path)

        # Zlicz pliki (nie uwzględniając podfolderów)
        file_count = len([file for file in files if os.path.isfile(os.path.join(folder_path, file))])

        return file_count
    except Exception as e:
        print(f"Błąd: {e}")
        return None


def getFile(folder_path, n):
    try:
        # Uzyskaj listę plików w danym folderze
        files = os.listdir(folder_path)
        return files[n]

    except Exception as e:
        print(f"Błąd: {e}")
        return None


def loadTexture(filename):
    image = Image.open(filename)
    texture_data = image.tobytes("raw", "RGBX", 0, -1)

    glfwMakeContextCurrent(window)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture


def startup():
    update_viewport(None, display[0], display[1])
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # ustawianie swiatła i materiału
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

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def floor():
    y = -size * sqrt(6) / 6
    glBegin(GL_QUADS)
    glVertex3f(-10, y, -10)
    glVertex3f(10, y, -10)
    glVertex3f(10, y, 10)
    glVertex3f(-10, y, 10)
    glEnd()


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
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glScale(viewerMoveVector[2], viewerMoveVector[2], viewerMoveVector[2])

    quadric = gluNewQuadric()

    glDisable(GL_LIGHTING)  # Światło nie wpływa na ten obiekt
    axes()  # osie

    # rysowanie zrodla swiatla
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(-light_position[0], -light_position[1], -light_position[2])

    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.1, 30, 30)

    glTranslatef(*light_position[:-1])
    glEnable(GL_LIGHTING)
    if floorActive:
        floor()  # pogłoga

    glRotatef(time * 180 / pi / 4, 0, -1, 0)

    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricOrientation(quadric, GLU_INSIDE)

    figure.draw(quadric, texturesActive)
    glFlush()

    if viewerMoveVector[0] != 0:
        viewerAngles[0] += viewerMoveVector[0] * viewerSpeed
        calcPose(viewer, viewerAngles)
    if viewerMoveVector[1] != 0:
        viewerAngles[1] += viewerMoveVector[1] * viewerSpeed
        calcPose(viewer, viewerAngles)
    
    if light_move_vector[0] != 0:
        lightAngles[0] += light_move_vector[0] * light_speed
        calcPose(light_position, lightAngles)
    if light_move_vector[1] != 0:
        lightAngles[1] += light_move_vector[1] * light_speed
        calcPose(light_position, lightAngles)
    if light_move_vector[2] != 0:
        lightAngles[2] += light_move_vector[2] * light_speed
        calcPose(light_position, lightAngles)


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


def calcPose(object, angles):
    print(light_diffuse)
    object[0] = angles[2] * cos(angles[1]) * cos(angles[0])
    object[1] = angles[2] * sin(angles[1])
    object[2] = angles[2] * sin(angles[0]) * cos(angles[1])


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
    # light
    if key == GLFW_KEY_P and action == GLFW_PRESS:
        if glIsEnabled(GL_LIGHT0):
            glDisable(GL_LIGHT0)
        else:
            glEnable(GL_LIGHT0)
    if key == GLFW_KEY_K and action == GLFW_PRESS:
        if glIsEnabled(GL_LIGHT1):
            glDisable(GL_LIGHT1)
        else:
            glEnable(GL_LIGHT1)

        # zoom
    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        viewerMoveVector[2] *= deltaZoom
    if key == GLFW_KEY_X and action == GLFW_PRESS:
        viewerMoveVector[2] /= deltaZoom

    # tekstury
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        global texturesActive
        texturesActive = not texturesActive

        if texturesActive:
            mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        else:
            mat_diffuse = [1.0, .0, .0, 1.0]

        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)

    if key == GLFW_KEY_N and action == GLFW_PRESS:
        global textureCurrent
        textureCurrent += 1

        if textureCurrent >= texturesNumber:
            textureCurrent = 0

        texture = loadTexture("tekstury/" + getFile("tekstury", int(textureCurrent)))
        #podloga
    if key == GLFW_KEY_F and action == GLFW_PRESS:
        global floorActive
        floorActive = not floorActive

    #swiatlo
    if key == GLFW_KEY_W and action == GLFW_PRESS:
        light_move_vector[1] = -1
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        light_move_vector[1] = 1
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        light_move_vector[0] = -1
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        light_move_vector[0] = 1
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        light_move_vector[2] = 1
    if key == GLFW_KEY_V and action == GLFW_PRESS:
        light_move_vector[2] = -1
    #kolory
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        if light_diffuse[0] < 1:
            light_diffuse[0] += 0.1
        else:light_diffuse[0] = 1

    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        if light_diffuse[1] < 1:
            light_diffuse[1] += 0.1
        else:light_diffuse[1] = 1
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        if light_diffuse[2] < 1:
            light_diffuse[2] += 0.1
        else:light_diffuse[2] = 1
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        if light_diffuse[0] > 0:
            light_diffuse[0] -= 0.1
        else:light_diffuse[0] = 0
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        if light_diffuse[1] > 0:
            light_diffuse[1] -= 0.1
        else:light_diffuse[1] = 0
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        if light_diffuse[2] > 0:
            light_diffuse[2] -= 0.1
        else:light_diffuse[2] = 0



    if (key == GLFW_KEY_RIGHT or key == GLFW_KEY_LEFT) and action == GLFW_RELEASE:
        viewerMoveVector[0] = 0
    if (key == GLFW_KEY_UP or key == GLFW_KEY_DOWN) and action == GLFW_RELEASE:
        viewerMoveVector[1] = 0

    if (key == GLFW_KEY_A or key == GLFW_KEY_D) and action == GLFW_RELEASE:
        light_move_vector[0] = 0
    if (key == GLFW_KEY_W or key == GLFW_KEY_S) and action == GLFW_RELEASE:
        light_move_vector[1] = 0
    if (key == GLFW_KEY_C or key == GLFW_KEY_V) and action == GLFW_RELEASE:
        light_move_vector[2] = 0


print("z - przybliż")
print("x - oddal")
print("UP, DOWN, LEFT, RIGHT strzałka - stwrowanie kamerą")
print("k - światło kierunkowe")
print("p - światło punktowe")
print("n - kolejna tekstura")
print("t - włączanie tekstur")
print("f - usuwanie podłogi")
print("w, s, a, d, c, v- poruszanie swiatłem")
print("q - wyłączanie")


# ilość poziomów piramidy
# lvl = int(input("Podaj wartość do wygenerowania piramidy. wartość powinna być liczbą całkowitą większą od 0 : \n"))
lvl = 3  # todo
size = 7  # rozmiar piramidy
topPos = (0, size * sqrt(6) / 6, 0)  # pozycja górnego wierzchołka od którego rysowane są kolejne

figure = SierpinskiPyramid(topPos, size, lvl)  # tworzenie piramidy


floorActive = True

#parametry materiału

mat_ambient = [0.0, 0.0, 0.0, 1.0]  # kolor odbity
mat_diffuse = [.9, 0, 0, 1.0]  # kolor rozproszony
mat_specular = [0.0, 0.0, 0.0, 1.0]  # kolor odbijanego swiatla
mat_shininess = 70.0


# parametry swiatla
light_ambient = [0.0, 0.0, 0.0, 1.0]  # kolor otoczenia
light_diffuse = [.0, .0, .8, 1.0]  # kolor swiatła rozproszonego
light_specular = [.9, .9, .9, 1.0]  # kolor odbitego swiatla
light_position = [0.0, 0.0, 10.0, 1.0]  # punktowe #pozycja źrodla swiatła

lightAngles = [0, 0, 10]
light_move_vector = [0, 0, 0]
light_speed = pi / 180 * 0.5

colorChanges = [0, 0, 0]

# tłumienie swiatla
att_constant = 1.0
att_linear = 0.001
att_quadratic = 0.0001



# parametry swiatla1
light_ambient1 = [0.0, 0.0, 0.0, 1.0]  # kolor otoczenia
light_diffuse1 = [.9, .9, .9, 1.0]  # kolor swiatła rozproszonego
light_specular1 = [.9, .9, .9, 1.0]  # kolor odbitego swiatla
light_position1 = [0.0, 0.0, 10.0, 0.0]  # kierunkowe #pozycja źrodla swiatła

# tłumienie swiatla1
att_constant1 = 1.0
att_linear1 = 0.001
att_quadratic1 = 0.0001



display = (1000, 800)

# parametru kamery
viewerAngles = [pi / 180 * 90, 0, 3]
viewer = [0.0, 0.0, 3.0]
viewerMoveVector = [0, 0, 1]  # x, y, zoom
viewerSpeed = pi / 180 * 0.5

deltaZoom = 1.1

if not glfwInit():
    sys.exit(-1)

window = glfwCreateWindow(display[0], display[1], __file__, None, None)
if not window:
    glfwTerminate()
    sys.exit(-1)

texturesNumber = countFiles("tekstury")
textureCurrent = 0
texture = loadTexture("tekstury/" + getFile("tekstury", int(textureCurrent)))

glfwMakeContextCurrent(window)
glfwSetFramebufferSizeCallback(window, update_viewport)
glfwSetKeyCallback(window, keyboard_key_callback)
glfwSwapInterval(1)

texturesActive = False

startup()
while not glfwWindowShouldClose(window):
    render(glfwGetTime())
    glfwSwapBuffers(window)
    glfwPollEvents()
shutdown()

glfwTerminate()
