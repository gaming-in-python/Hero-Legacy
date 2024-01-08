import pygame 
from settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        #commented out below bc tutorial requires an offset but somehow our game does not
        # #check if object bc object sprites are larger than 64x64 pixels (64x128 or 128x128)
        # if sprite_type == 'object' :
        #     self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        # else :
        self.rect = self.image.get_rect(topleft = pos)
        # inflate changes the size of the hitbox to add the player's depth
        # we want to just shorten the height of the hitbo
        self.hitbox = self.rect.inflate(0, y_offset)
