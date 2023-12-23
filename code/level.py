import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
class Level:
    def __init__(self):

        #getting display surface
        self.display_surface = pygame.display.get_surface()

        #getting the sprites for obstacles+player
        self.visibles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.create_map()
    
    #places a rock wherever an x is labeled, places the player at whatever coordinates p is labeled
    def create_map(self):     
        #iterating through map
        for row in range(0, HEIGHT, TILESIZE):
            for col in range(0, WIDTH, TILESIZE):
                tile_value = WORLD_MAP[row // TILESIZE][col // TILESIZE]
                x = col
                y = row
                #adding a rock
                if tile_value == 'x':
                    Tile((x,y),[self.visibles, self.obstacles])
                #adding the player
                if tile_value == 'p':
                    self.player = Player((x,y),[self.visibles], self.obstacles)



    def run(self):
        self.visibles.draw(self.display_surface)
        self.visibles.update()
        debug(self.player.direction)

    