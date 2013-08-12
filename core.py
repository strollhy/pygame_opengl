SCREEN_SIZE = (320, 240)

import pygame
from pygame.locals import *
from graphic import Graphic
from world import World

class Core:
    ###
    def __init__(self):
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
        pygame.display.set_caption("Hello, World!")

        # clock for framerate
        self.clock = pygame.time.Clock()

        # Initialize graphic settings
        self.graphic = Graphic(SCREEN_SIZE)

        # Intialize world
        self.world = World()

        # Start
        self.__start()

    def __start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYUP and event.key == K_ESCAPE:
                    return

                if event.type == KEYUP and event.key == K_1:
                    self.graphic.textId = 0
                    
                if event.type == KEYUP and event.key == K_2:
                    self.graphic.textId = 1
                    
                if event.type == KEYUP and event.key == K_3:
                    self.graphic.textId = 2

            # Set frame rate
            self.clock.tick(50)

            # Render background
            self.graphic.render()

            # Draw
            self.draw()

            # Show the screen
            pygame.display.flip()


    def draw(self):
        # Generate coordinates
        pos = World.genCube(0, 0, 0)
        tex = World.genTexcoord(self.graphic.textId)

        # Render cube
        self.graphic.rendRects(pos, tex) 

if __name__ == "__main__":
    core = Core()
