import pygame as pg
import sys
from .world import World
from .setting import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height)


    # Game Loop
    def run(self):
        self.playing = True
        
        while self.playing:
            self.clock.tick(60)
            self.draw()
            self.event_handler()
            self.update()
        

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        isometric_world = self.world.isometric_world
        self.screen.blit(self.world.default_surface, (0,0))
        for row in range(self.world.nums_grid_y):
            for col in range(self.world.nums_grid_x):

                # Render graphic
                
                # For graphical object rendering (graphical object is water, prefecture, housing,etc) 

                # Render grid
                cell_render = isometric_world[row][col]['isometric_cell']
                cell_render = [(x + self.width/2, y + self.height/4) for x, y in cell_render]
                pg.draw.polygon(self.screen, (255, 0, 0), cell_render, 1)
                
        pg.display.flip()


    def update(self):
        pass
