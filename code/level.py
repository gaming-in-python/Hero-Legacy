import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # Placing player in top left of map 
        self.player = Player((500, 500), [self.visible_sprites], self.obstacle_sprites)

        layouts = {
            'boundary': import_csv_layout('../map/zelda_ground2_Border.csv'),
            'grass' : import_csv_layout('../map/zelda_ground2_Grass.csv'),
            'object': import_csv_layout('../map/zelda_ground2_Trees.csv')
        }

        graphics = {
            'grass' : import_folder('../graphics/Grass'),
            'objects' : import_folder('../graphics/Grass')
        }

        #first iteration is style = boundary and layout = returned list from import_csv_layout
        for style, layout in layouts.items() :
            for row_index,row in enumerate(layout): 
                for col_index,col in enumerate(row) :
                    if col != '-1' :
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary' :
                            #boundary tiles should be invisible obstacles of default surface type
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass' :
                            #create grass tile with a random grass image surafce and make it an obstacle
                            #random_grass_img = choice(graphics['grass'])
                            Tile((x,y), [self.obstacle_sprites], 'grass')
                        if style == 'object' :
                            #surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.obstacle_sprites], 'object')

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor: loading png for background then place at (0,0)
		self.floor_surf = pygame.image.load('../graphics/tilemap/zelda_ground2.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):
		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor (this is background image so it must be done before sprites)
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)