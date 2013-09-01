import math
import pygame
from pygame.locals import *
from graphic import Graphic
from world import World

#
SCREEN_SIZE = (640, 480)

# Movement speed
SPEED = 1.0

''' Core '''
class Core:
    ###
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Initialize mouse, must before initialize screen, otherwise will triger mouse movement
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        # Initialize screen
        screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
        pygame.display.set_caption("Hello, World!")

        # clock for framerate
        self.clock = pygame.time.Clock()

        # Initialize graphic settings
        self.graphic = Graphic(SCREEN_SIZE)

        # Intialize world
        self.world = World()

        # Intialize movement vector
        self.dx = self.dy = self.dz = 0
        self.tx = self.ty = self.tz = 0

        # Start
        self.__game_loop()

    def __game_loop(self):
        while True:
            # Response to event
            self.__on_event()
            
            # Set frame rate
            self.clock.tick(50)

            # Update sight vector                
            x, y = self.graphic.sight
            self.graphic.sight = (x+self.tx, y+self.ty)
            
            # Update camera position
            x, y, z = self.graphic.position
            self.graphic.position = (x+self.dx, y+self.dy, z+self.dz)

            # Render background
            self.graphic.render()

            # Draw objects
            self.__on_draw()

            # Show the screen
            pygame.display.flip()

    def __on_event(self):

        self.__get_movement()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYUP and event.key == K_ESCAPE:
                exit()

            if event.type == KEYUP and event.key == K_1:
                self.graphic.textId = 0
                    
            if event.type == KEYUP and event.key == K_2:
                self.graphic.textId = 1
                    
            if event.type == KEYUP and event.key == K_3:
                self.graphic.textId = 2

            if event.type == KEYUP and event.key == K_4:
                self.graphic.textId = 3

            if event.type == KEYUP and event.key == K_5:
                self.graphic.textId = 4

            if event.type == KEYUP and event.key == K_6:
                self.graphic.textId = 5


            ''' For sight direction '''
            # look up
            if event.type == KEYDOWN and event.key == K_UP:
                self.ty = SPEED
                
            if event.type == KEYUP and event.key == K_UP:
                self.ty = 0
                
            # look down
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.ty = -SPEED

            if event.type == KEYUP and event.key == K_DOWN:
                self.ty = 0

            # look left
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.tx = -SPEED
                
            if event.type == KEYUP and event.key == K_LEFT:
                self.tx = 0

            # look right
            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.tx = SPEED
                
            if event.type == KEYUP and event.key == K_RIGHT:
                self.tx = 0

            # Change sight via mouse movement
            if event.type == MOUSEMOTION:
                self.tx, self.ty = pygame.mouse.get_rel()
                m = .15
                self.tx *= m
                self.ty *= -m
                x, y = self.graphic.sight
                self.graphic.sight = (x+self.tx, y+self.ty)
                self.tx = self.ty = 0
    
    def __get_movement(self):

        ''' Get movement '''
        x, y = self.graphic.sight

        keys = pygame.key.get_pressed()

        v_z = [0] * 4
        v_x = [0] * 4
        # move forward
        if keys[K_w]:
            v_z[0] = -SPEED * math.cos(math.radians(x))
            v_x[0] = SPEED * math.sin(math.radians(x))
        else:
            v_z[0] = v_x[0] = 0

        
        # move backward
        if keys[K_s]:
            v_z[1] = SPEED * math.cos(math.radians(x))
            v_x[1] = -SPEED * math.sin(math.radians(x))
        else:
            v_z[1] = v_x[1] = 0
            
        # move left
        if keys[K_a]:
            v_z[2] = -SPEED * math.cos(math.radians(x - 90))
            v_x[2] = SPEED * math.sin(math.radians(x - 90))
        else:
            v_z[2] = v_x[2] = 0
        
        # move right
        if keys[K_d]:
            v_z[3] = -SPEED * math.cos(math.radians(x + 90))
            v_x[3] = SPEED * math.sin(math.radians(x + 90))
        else:
            v_z[3] = v_x[3] = 0
        
        # sum the montion vector
        self.dz = sum(v_z)
        self.dx = sum(v_x)

    def __on_draw(self):
        # Draw the entire world
        tex = Graphic.genTexcoord(self.graphic.textId)
        for k,m in self.world.map.items():
            self.graphic.drawRects(m, tex)

if __name__ == "__main__":
    core = Core()
