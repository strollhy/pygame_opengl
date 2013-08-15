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


        ''' Render Cube'''
        ## Front face
        # Set "brush" color
        glColor3f(.3, 1, .3)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(-1, -1, 0)
        glEnd()

        ## Back face
        # Set "brush" color
        glColor3f(1, 1, 1)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, -2)
        glVertex3f(1, 1, -2)
        glVertex3f(1, -1, -2)
        glVertex3f(-1, -1, -2)
        glEnd()

        ## Top face
        # Set "brush" color
        glColor3f(1, .3, .3)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, -2)
        glVertex3f(-1, 1, -2)
        glEnd()

        ## Bottom face
        # Set "brush" color
        glColor3f(1, 1, .3)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(1, -1, 0)
        glVertex3f(1, -1, -2)
        glVertex3f(-1, -1, -2)
        glVertex3f(-1, -1, 0)
        glEnd()

        ## Right face
        # Set "brush" color
        glColor3f(.3, .3, 1)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(1, 1, -2)
        glVertex3f(1, 1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(1, -1, -2)
        glEnd()

        ## Left face
        # Set "brush" color
        glColor3f(.3, 1, 1)
        # Begin rendering
        glBegin(GL_QUADS)
        glVertex3f(-1, 1, 0)
        glVertex3f(-1, 1, -2)
        glVertex3f(-1, -1, -2)
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
    tx = ty = tz = 0

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

            ''' For sight direction '''
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

        if tx != 0 or ty != 0:
            # Get and update sight angle
            a, b = opengl.angle
            a, b = a + tx, b + ty
            b = max(-90, min(90, b))
            opengl.angle = (a, b)

            # Update pointing vector for camera
            # Spin radius: 10
            radius = 1
            x, y, z = opengl.sight
            x += 2*math.sin(math.radians(a/2))*math.cos(math.radians(a/2)) * radius
            y += 2*math.sin(math.radians(b/2))*math.cos(math.radians(b/2)) * radius
            z += (2*math.sin(math.radians(a/2))*math.sin(math.radians(a/2)) + 2*math.sin(math.radians(a/2))*math.sin(math.radians(b/2))) * radius
            opengl.sight = (x, y, z)
        
        x, y, z = opengl.sight
        opengl.sight = (x+dx, y+dy, z+dz)

        # Update camera position
        print x,y,z
        x, y, z = opengl.position
        opengl.position = (x+dx, y+dy, z+dz)

        # Set frame rate
        clock.tick(50)

        # Start drawing
        opengl.draw()

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
  main()
