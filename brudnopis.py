
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from objects.sierpinskiPyramid import SierpinskiPyramid


#ilość poziomów piramidy
# lvl = int(input("Podaj wartość do wygenerowania piramidy. wartość powinna być liczbą całkowitą większą od 0 : \n"))
lvl = 3 #todo

size = 20           #rozmiar piramidy
topPos = (0,0,0)    #pozycja górnego wierzchołka od którego rysowane są kolejne

figure = SierpinskiPyramid(topPos, size, lvl)   # tworzenie piramidy



light_ambient = [0, 0, 0, 1]    #kolor cienia
light_diffuse = [.8, .8, .1, 1] #kolor światła
light_specular = [0, 0, 0, 1]   #kolor światła (blask)

light_position = [-1, 10, -30, 1]   #połorzenie światła





def startup():
    # inicjowanie okna
    pygame.init()
    display = (1000,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #ustawianie perspektywy
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0, 10.0, -30)

    # #ustawianie swiatła punktowego
    # glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    # # glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    # glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    #
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)

    #blokowanie przenikania
    glEnable(GL_DEPTH_TEST)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)#red
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def main():
    startup()

    # rotation = [0.2, 0, 1, 0]
    rotation = [0, 0, 0, 0]
    translation = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_UP:
                    # rotation = [1, -1, 0, 0]
                    rotation[0]=1
                    rotation[1]=-1
                if event.key == pygame.K_DOWN:
                    # rotation = [1, 1, 0, 0]
                    rotation[0]=1
                    rotation[1]=1
                if event.key == pygame.K_LEFT:
                    # rotation = [1, 0, 1, 0]
                    rotation[0]=1
                    rotation[2]=-1
                if event.key == pygame.K_RIGHT:
                    # rotation = [1, 0, -1, 0]
                    rotation[0]=1
                    rotation[2]=1
                if event.key == pygame.K_a:
                    # rotation = [1, 0, 0, 1]
                    rotation[0]=1
                    rotation[3]=1
                if event.key == pygame.K_d:
                    # rotation = [1, 0, 0, -1]
                    rotation[0]=1
                    rotation[3]=-1
                if event.key == pygame.K_w:
                    translation = 0.1
                if event.key == pygame.K_s:
                    translation = -0.1
                if event.key == pygame.K_p:
                    gluLookAt(1, 2, 1,
                              3, 3, 3,
                              0, 0, 0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    rotation[1] = 0
                    rotation[0] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    rotation[2] = 0
                    rotation[0] = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    rotation[3] = 0
                    rotation[0] = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    translation = 0


        glRotatef(rotation[0], rotation[1], rotation[2], rotation[3])
        if translation != 0:
            glTranslatef(0.0, 0.0, translation)



        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        figure.draw()
        axes()
        pygame.display.flip()
        pygame.time.wait(10)

main()
