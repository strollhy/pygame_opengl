SCREEN_SIZE = (320, 240)

import pygame
from pygame.locals import *

# OpenGL stuff
from OpenGL.GL import *
from OpenGL.GLU import *

RATIO = 0.25    
TEXTURE_COOD = (   (1, 1),
                    (2, 1),
                    (3, 1),
                    (1, 2),
                    (2, 2),
                    (3, 2)
                )

def genTexcoord(coordId):
    ''' Coordinate is generate clockwisely'''
    x, y = TEXTURE_COOD[coordId]
    x, y = [x*RATIO, y*RATIO]
    return (
        (x-RATIO, y-RATIO), (x, y-RATIO), (x, y), (x-RATIO, y)
    )


def genCube(x, y, z, n=.5):
    return (
        ((x-n,y+n,z-n), (x-n,y+n,z+n), (x+n,y+n,z+n), (x+n,y+n,z-n)),  # top
        ((x-n,y-n,z-n), (x+n,y-n,z-n), (x+n,y-n,z+n), (x-n,y-n,z+n)),  # bottom
        ((x-n,y-n,z-n), (x-n,y-n,z+n), (x-n,y+n,z+n), (x-n,y+n,z-n)),  # left
        ((x+n,y-n,z+n), (x+n,y-n,z-n), (x+n,y+n,z-n), (x+n,y+n,z+n)),  # right
        ((x-n,y-n,z+n), (x+n,y-n,z+n), (x+n,y+n,z+n), (x-n,y+n,z+n)),  # front
        ((x+n,y-n,z-n), (x-n,y-n,z-n), (x-n,y+n,z-n), (x+n,y+n,z-n)),  # back
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
        self.textId = 0
        self.texIDs = self.loadTexture()

    def resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., float(width)/height, 1., 10000.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def loadTexture(self, imgName = "texture.png"):
        im = pygame.image.load(imgName)
        '''
        In pygame the coordinates is rotated 90 degree clockwise
        '''
        im = pygame.transform.rotate(im, 180)
        im = pygame.transform.flip(im, True, False)

        try:
            ix, iy, image = im.get_width(), im.get_height(),  pygame.image.tostring(im, "RGBA")
        except SystemError:
            ix, iy, image = im.get_width(), im.get_height(),  pygame.image.tostring(im, "RGBX")

        IDs = []
        # a Nearest-filtered texture...
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        # linear-filtered
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        # linear + mip-mapping
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)

        return IDs

    def render(self):
        # Reset screen 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()

        # Set current matrix
        glMatrixMode(GL_MODELVIEW)

        # Reset Modelview
        glLoadIdentity()

        # Change Modelview into screen 2 units
        glTranslatef(.0, .0, -2.0)

        # Rotate on x, y, z axis
        self.angle += 2
        self.angle %= 360
        glRotatef(self.angle, 0, 1, 0)

        # Generate coordinates
        pos = genCube(0, 0, 0)
        tex = genTexcoord(self.textId)

        # Render cube
        self.__renderCube(pos, tex)

    def __renderCube(self, position, texCoord):
        for pos in position:
            self.__renderRect(pos, texCoord)
        
    def __renderRect(self, position, texCoord):
        ''' 
        Assign texture and geometric coordinates
        '''
        if len(position) != len(texCoord):
            return -1

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texIDs[0])

        # Begin rendering
        glBegin(GL_QUADS)

        ''''''
        texCoord = iter(texCoord)
        for pos in position:
            tex = texCoord.next()
            glTexCoord2f(*tex)
            glVertex3f(*pos)

        ''' '''
        glEnd()
        glDisable(GL_TEXTURE_2D)

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

            if event.type == KEYUP and event.key == K_1:
                opengl.textId = 0
                
            if event.type == KEYUP and event.key == K_2:
                opengl.textId = 1
                
            if event.type == KEYUP and event.key == K_3:
                opengl.textId = 2
                

        # Set frame rate
        clock.tick(50)

        # Start rendering
        opengl.render()

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
  main()
