import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
class Level:
    def __init__(self):

        #getting display surface
        self.display_surface = pygame.display.get_surface()

        self.visibles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.create_map()

    def create_map(self):     
        for row in range(0, HEIGHT, TILESIZE):
            for col in range(0, WIDTH, TILESIZE):
                tile_value = WORLD_MAP[row // TILESIZE][col // TILESIZE]
                x = col
                y = row
                if tile_value == 'x':
                    Tile((x,y),[self.visibles, self.obstacles])
                if tile_value == 'p':
                    self.player = Player((x,y),[self.visibles], self.obstacles)



    def run(self):
        self.visibles.draw(self.display_surface)
        self.visibles.update()
        debug(self.player.direction)

    