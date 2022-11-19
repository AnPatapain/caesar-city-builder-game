import pygame as pg
import os
from perlin_noise import PerlinNoise
import random as rd

from map_element.tile import Tile
from game.setting import *
import game.utils as utils
from class_types.tile_types import TileTypes
from game.textures import Textures


class World:

    def __init__(self, nums_grid_x, nums_grid_y, width, height, panel):
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.width = width
        self.height = height

        self.noise_scale = nums_grid_x/2
        self.graphics = self.load_images()
        self.default_surface = pg.Surface((DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT))
        self.grid: [[Tile]] = self.grid()

        #For building feature
        self.panel = panel
        self.temp_tile = None
        self.start_point = None
        self.temp_end_point = None
        self.end_point = None

        self.in_build_action = False

    def mouse_pos_to_grid(self, mouse_pos, map_pos):
        '''
        DESCRIPTION: Convert position of mouse to row and col on grid. ex: convert (192.15, 30.14) to (row: 40, col: 10)
        To do that we reverse this process: (col, row) -> convert_to_iso -> offset (1/2 default_surface.width, 0) -> offset (map_pos[0], map_pos[1])

        Params: mouse_position: tuple, map_position: tuple

        Return: (col, row) of mouse_position in the grid
        '''

        iso_x = mouse_pos[0] - map_pos[0] - self.default_surface.get_width()/2
        iso_y = mouse_pos[1] - map_pos[1]

        # transform to cart (inverse of cart_to_iso)
        cart_x = (iso_x + 2*iso_y)/2
        cart_y = (2*iso_y - iso_x)/2

        # transform to grid coordinates
        grid_col = int(cart_x // TILE_SIZE)
        grid_row = int(cart_y // TILE_SIZE)
        return (grid_col, grid_row)


    def event_handler(self, event, map_pos):

        '''
        DESCRIPTION: Handling the events that be gotten from event queue in module event_manager.py
        
        Params: event retrieved from pg.event.get() in event_manager.py, map_position in mapcontroller.py

        Return: None
        '''

        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)

        if self.in_map(mouse_grid_pos):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.start_point = mouse_grid_pos
                    self.in_build_action = True
                    print('mouse button down:',  self.start_point)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.in_build_action = False
                    self.end_point = mouse_grid_pos
                    print('mouse button up', self.end_point)

            elif event.type == pg.MOUSEMOTION:
                self.temp_end_point = mouse_grid_pos
                print('mouse motion', self.temp_end_point)


    def update(self, map_pos):
        '''
        DESCRIPTION: updating the state of the world. For now it updates temp_tile, texture of the world 

        Params: map_position from mapcontroller module 

        Return: None
        '''
        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)
        mouse_action = pg.mouse.get_pressed()


        selected_tile = self.panel.get_selected_tile()
        self.temp_tile = None

        if selected_tile != None:
            if self.in_map(mouse_grid_pos):
                tile = self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]
                print(selected_tile)
                self.temp_tile = {
                    'name': selected_tile,
                    'isometric_coor': tile.get_isometric_coord(),
                    'render_img_coor': tile.get_render_coord(),
                    'isBuildable': tile.is_buildable()
                }

            if self.in_build_action == False and self.start_point != None and self.end_point != None:

                if self.in_map(self.start_point) and self.in_map(self.end_point):
                    for row in utils.MyRange(self.start_point[1], self.end_point[1]):
                        for col in utils.MyRange(self.start_point[0], self.end_point[0]):
                            tile: Tile = self.grid[row][col]

                            if tile.is_buildable():
                                tile.set_type(selected_tile)
                                self.grid[row][col].set_type(selected_tile)

                if mouse_action[2]:
                    self.panel.set_selected_tile(None)


    def draw(self, screen, map_pos):
        screen.blit(self.default_surface, map_pos)

        for row in range(self.nums_grid_y):
            for col in range(self.nums_grid_x):
                tile: Tile = self.grid[row][col]
                (x, y) = tile.get_render_coord()
                # cell is placed at 1/2 default_surface.get_width() and be offseted by the position of the default_surface
                (x_offset, y_offset) = (x + self.default_surface.get_width()/2 + map_pos[0],
                                         y + map_pos[1])

                texture_image = tile.get_texture()

                if tile.get_type() != TileTypes.GRASS:
                    screen.blit(texture_image, (x_offset, y_offset - texture_image.get_height() + TILE_SIZE))

        if self.temp_tile is not None and self.in_build_action is False:
            isometric_coor = self.temp_tile['isometric_coor']
            isometric_coor_offset = [(x+map_pos[0]+self.default_surface.get_width()/2, y + map_pos[1]) for x, y in isometric_coor]

            (x, y) = self.temp_tile['render_img_coor']
            (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_pos[0],
                                     y + map_pos[1] )

            #screen.blit(self.graphics['upscale_2x'][self.temp_tile['name']],
            #           (x_offset, y_offset -  self.graphics['upscale_2x'][self.temp_tile['name']].get_height() + TILE_SIZE))

            texture = Textures.get_texture(self.temp_tile['name'])
            screen.blit(texture, (x_offset, y_offset - texture.get_height() + TILE_SIZE))

            if self.temp_tile['isBuildable']:
                pg.draw.polygon(screen, (0, 255, 0), isometric_coor_offset, 4)
            else:
                pg.draw.polygon(screen, (255, 0, 0), isometric_coor_offset, 4)


        if self.in_build_action:

            if self.in_map(self.start_point) and self.in_map(self.temp_end_point):
                for row in utils.MyRange(self.start_point[1], self.temp_end_point[1]):
                    for col in utils.MyRange(self.start_point[0], self.temp_end_point[0]):

                        if self.grid[row][col].is_buildable():

                            (x, y) = self.grid[row][col].get_render_coord()

                            (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_pos[0], y + map_pos[1] )
                            temp_house_image = self.graphics['upscale_2x']['temp_house']
                            screen.blit(temp_house_image, (x_offset, y_offset -  temp_house_image.get_height() + TILE_SIZE))


    def grid(self) -> [[Tile]]:
        grid = []
        for row in range(self.nums_grid_y):

            grid.append([])

            for col in range(self.nums_grid_x):

                iso_tile = self.tile(col, row)
                grid[row].append(iso_tile)

                (x, y) = iso_tile.get_render_coord()
                offset_render = (x + self.default_surface.get_width()/2, y)

                self.default_surface.blit(self.graphics['upscale_2x']['block'], offset_render)

        return grid


    def tile(self, col: int, row: int) -> Tile:
        def graphic_generator():
            normal_random = rd.randint(1, 100)
            noise = PerlinNoise(octaves=1, seed=777)
            perlin_random = 100 * noise([col/self.noise_scale, row/self.noise_scale])

            # perlin_distribution(perlin_random)
            graphic_ = TileTypes.GRASS
            if (perlin_random >= 20) or perlin_random <= -30 :
                graphic_ = TileTypes.TREE
            else:
                if normal_random < 4:
                    graphic_ = TileTypes.ROCK
                if normal_random < 2:
                    graphic_ = TileTypes.TREE
            return graphic_

        tile = Tile(col, row)
        tile.set_type(graphic_generator())

        return tile


    def convert_cart_to_iso(self, x, y):
        '''
        DESCRIPTION: I don't know how to explain this method 
        You can think this method helps us rotate square and then stretch it out : )

        Params: coordination of one point of the square

        Return: new coordination of the rhombus
        ''' 
        return ( x - y, (x + y)/2 )


    def load_images(self):

        path = 'assets/C3_sprites/C3'

        return {
            'origin': {
                'block': pg.image.load(os.path.join(path, 'Land1a_00069.png')).convert_alpha(),
                'tree': pg.image.load(os.path.join(path, 'Land1a_00041.png')).convert_alpha(),
                'rock': pg.image.load(os.path.join(path, 'Land1a_00290.png')).convert_alpha()
            },

            'upscale_2x': {
                'block': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00069.png') ) ).convert_alpha() ,
                'tree': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00041.png') ) ).convert_alpha(),
                'rock': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00290.png') ) ).convert_alpha(),
                'temp_house': self.scale_image_2x(pg.image.load( os.path.join(path, 'Housng1a_00045.png') )).convert_alpha()
            }
        }


    def scale_image_2x(self, image):
        return pg.transform.scale2x(image)


    def in_map(self, grid_pos):
        '''
        DESCRIPTION: Check whether the mouse_grid_pos is in map or not. Ex: our map is 30x30 and mouse_grid_pos is (row: 31, col: 32)
        so the mouse is not in the map

        Params: the grid pos of mouse

        Return: boolean
        '''
        mouse_on_panel = False
        in_map_limit = (0 <= grid_pos[0] < self.nums_grid_x) and (0 <= grid_pos[1] < self.nums_grid_y)
        for rect in self.panel.get_panel_rects():
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        return True if (in_map_limit and not mouse_on_panel) else False


