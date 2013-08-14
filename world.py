SCREEN_SIZE = (320, 240)

import pygame
from pygame.locals import *

# OpenGL stuff
from OpenGL.GL import *
from OpenGL.GLU import *

# Movement speed
SPEED = .5

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
        self.sight = (0, 0, -1)
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

    dx = dy = dz = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

            ''' For movement '''
            # move forward
            if event.type == KEYDOWN and event.key == K_w:
                dz = -SPEED
            
            if event.type == KEYUP and event.key == K_w:
                dz = 0
            
            # move backward
            if event.type == KEYDOWN and event.key == K_s:
                dz = SPEED

            if event.type == KEYUP and event.key == K_s:
                dz = 0

            # move left
            if event.type == KEYDOWN and event.key == K_a:
                dx = -SPEED
            
            if event.type == KEYUP and event.key == K_a:
                dx = 0

            # move right
            if event.type == KEYDOWN and event.key == K_d:
                dx = SPEED
            
            if event.type == KEYUP and event.key == K_d:
                dx = 0

        x, y, z = opengl.position
        opengl.position = (x+dx, y+dy, z+dz)

        x, y, z = opengl.sight
        opengl.sight = (x+dx, y+dy, z+dz)

        # Set frame rate
        clock.tick(50)

        # Start drawing
        opengl.draw()

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
  main()
