SCREEN_SIZE = (320, 240)

import math

import pygame
from pygame.locals import *

# OpenGL stuff
from OpenGL.GL import *
from OpenGL.GLU import *

# Movement speed
SPEED = 1.0

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
        self.angle = (0, 0)
        self.sight = (0, 0, -10)
        self.position = (0, 0, 5)

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

        # Set camera
        param = self.position + self.sight + (0,1,0)
        gluLookAt(*param)

        # Set "brush" color
        glColor3f(0.5, 1, 0.5)

        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(-1, -1, 0)
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

    tx = ty = dz = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

            ''' For view point '''
            # look up
            if event.type == KEYDOWN and event.key == K_UP:
                ty = SPEED
            
            if event.type == KEYUP and event.key == K_UP:
                ty = 0
            
            # look down
            if event.type == KEYDOWN and event.key == K_DOWN:
                ty = -SPEED

            if event.type == KEYUP and event.key == K_DOWN:
                ty = 0

            # look left
            if event.type == KEYDOWN and event.key == K_LEFT:
                tx = -SPEED
            
            if event.type == KEYUP and event.key == K_LEFT:
                tx = 0

            # look right
            if event.type == KEYDOWN and event.key == K_RIGHT:
                tx = SPEED
            
            if event.type == KEYUP and event.key == K_RIGHT:
                tx = 0

        x, y, z = opengl.sight
        a, b = opengl.angle
        a, b = a + tx, b + ty
        b = max(-90, min(90, b))
        opengl.angle = (a, b)

        x = 20*math.sin(math.radians(a/2))*math.cos(math.radians(a/2))
        y = 20*math.sin(math.radians(b/2))*math.cos(math.radians(b/2))
        z = 20*math.sin(math.radians(a/2))*math.sin(math.radians(a/2)) + 20*math.sin(math.radians(a/2))*math.sin(math.radians(b/2))

        print x, y, z
        opengl.sight = (x, y, z)

        # Set frame rate
        clock.tick(50)

        # Start drawing
        opengl.draw()

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
  main()
