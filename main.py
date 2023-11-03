import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from objects.sierpinskiPyramid import SierpinskiPyramid



lvl = int(input("Podaj wartość do wygenerowania piramidy. wartość powinna być liczbą całkowitą większą od 0 : \n"))


size = 20
topPos = (0,0,0)

figure = SierpinskiPyramid(topPos, size, lvl)




def light():...
    # glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 0)) # źródło światła left, top, front
    #
    # # Ustawienie koloru światła otoczenia
    # glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 0.0, 0.0, 1.0))
    #
    # # Ustawienie koloru światła rozproszonego
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    #
    # # Ustawienie koloru światła wypukłego
    # glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0))
    # glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE )

def main():
    pygame.init()
    display = (1000,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)

    glTranslatef(0.0, 10.0, -30)


    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
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
                    rotation[2]=1
                if event.key == pygame.K_RIGHT:
                    # rotation = [1, 0, -1, 0]
                    rotation[0]=1
                    rotation[2]=-1
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    rotation[0] = 0
                    rotation[1] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    rotation[0] = 0
                    rotation[2] = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    rotation[0] = 0
                    rotation[3] = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    translation = 0

        glRotatef(rotation[0], rotation[1], rotation[2], rotation[3])
        glTranslatef(0.0, 0.0, translation)



        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        figure.draw()
        light()
        pygame.display.flip()
        pygame.time.wait(10)

main()