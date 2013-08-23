import math
import pygame

# OpenGL stuff
from OpenGL.GL import *
from OpenGL.GLU import *

RATIO = 0.0625    
TEXTURE_COOD = ( (3, 15),
                 (2, 16),
                 (3, 16),
                 (4, 16),
                 (5, 16),
                 (6, 16)
                )

class Graphic:

    def __init__(self, SCREEN_SIZE):
        # Resize
        self.resize(*SCREEN_SIZE)

        # OpenGL Setup
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.69, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Default parameters
        self.angle = 0
        self.sight = (0, 0)
        self.position = (0, 0, 5)
        self.textId = 0
        self.texIDs = self.loadTexture("texture3.png")

    def resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., float(width)/height, 1., 10000.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def genTexcoord(coordId):
        ''' Coordinate is generate clockwisely'''
        x, y = TEXTURE_COOD[coordId]
        x, y = [x*RATIO, y*RATIO]
        return (
            (x-RATIO, y-RATIO), (x, y-RATIO), (x, y), (x-RATIO, y)
        )

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

    ### Render the environment
    def render(self):
        # Reset screen 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()

        # Set current matrix
        glMatrixMode(GL_MODELVIEW)

        # Reset Modelview
        glLoadIdentity()

        # Move the object
        x, y = self.sight
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    ### Draw rectangles
    def drawRects(self, position, texCoord):
        for pos in position:
            self.drawRect(pos, texCoord)

    ### Draw rectangle
    def drawRect(self, position, texCoord):
        ''' 
        Assign texture and geometric coordinates
        '''
        if len(position) != len(texCoord):
            return -1

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texIDs[0])

        # Begin drawing
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
