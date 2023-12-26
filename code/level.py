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
        self.visibles = YSortCameraGroup()
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
        self.visibles.custom_draw(self.player)
        self.visibles.update()
        # debug(self.player.direction)

# camera group - player is in middle of window by adding an offset to the player's pos
# Y sort: sorting sprites by the y-coord
class YSortCameraGroup(pygame.sprite.Group): 
    def __init__(self):
        #general setup
        super().__init__()
        # get pos for center of window, floored 
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        # init offset 
        self.offset_cam = pygame.math.Vector2()
    
    # blit stands for block transfer (copying pixels from one surface to another)
    # blit syntax: destination_surface.blit(source_surface, (x, y))

    #custom draw method
    def custom_draw(self, player):
        #getting offset from the player's pos (how much player moved from the center of the screen)
        self.offset_cam.x = player.rect.centerx - self.half_width
        self.offset_cam.y = player.rect.centery - self.half_height

        # for every sprite, offset it's position
        # subtract player movement from it's pos so obstacles look like they're moving away
        for sprite in self.sprites():
            offset_position = sprite.rect.topleft - self.offset_cam
            self.display_surface.blit(sprite.image, offset_position)