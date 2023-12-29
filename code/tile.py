import pygame
from settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        # print("Current Working Directory:", os.getcwd())
        self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # inflate changes the size of the hitbox to add the player's depth
        # we want to just shorten the height of the hitbo
        self.hitbox = self.rect.inflate(0, -10)
