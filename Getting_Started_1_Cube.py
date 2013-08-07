SCREEN_SIZE = (320, 240)

import pygame
from pygame.locals import *

# OpenGL stuff
from OpenGL.GL import *
from OpenGL.GLU import *

''' 
coordinates of vertices 
'''
cube = (
    1, 1, 1, #0
    -1, 1, 1, #1
    -1, -1, 1, #2
    1, -1, 1, #3
    1, 1, -1, #4
    -1, 1, -1, #5
    -1, -1, -1, #6
    1, -1, -1 #7
)

''' 
colors of vertices 
'''
color = (
    1, 1, 0,
    1, 1, 0,
    1, 0, 0,
    1, 0, 0,
    0, 1, 0,
    0, 1, 0,
    0, 0, 1,
    0, 0, 1
)

''' 
Define the vertex indices for the cube 
'''
indice = (
    0, 1, 2, 3, # front face
    0, 4, 5, 1, # top face
    4, 0, 3, 7, # right face
    1, 5, 6, 2, # left face
    3, 2, 6, 7, # bottom face
    4, 5, 6, 7, # back face
)


class myOpenGL:

    def __init__(self):
        # Resize
        self.resize(*SCREEN_SIZE)

        # OpenGL Setup
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.69, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Default parameters
        self.angle = 0

    def resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., float(width)/height, 1., 10000.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self):
        # Reset screen 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()

        # Set current matrix
        glMatrixMode(GL_MODELVIEW)

        # Reset Modelview
        glLoadIdentity()

        # Change Modelview into screen 5 units
        glTranslatef(.0, .0, -5.0)

        # Rotate on x, y, z axis
        self.angle += 1
        self.angle %= 360
        glRotatef(self.angle, 1, 1, 1)

        
        # Set "brush" color
        glColor3f(0.5, 1, 0.5)

        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(-1, -1, 0)
        glEnd()

        # Set "brush" color
        glColor3f(1, .5, .5)

        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, -2)
        glVertex3f(-1, 1, -2)
        glEnd()



###
def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption("Hello, World!")

    # clock for framerate
    clock = pygame.time.Clock()


    # Initialize opengl
    opengl = myOpenGL()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        clock.tick(50)

        opengl.draw()

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
	main()
