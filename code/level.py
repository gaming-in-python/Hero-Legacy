import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI
class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        #getting the sprites for obstacles+player
        self.visibles = YSortCameraGroup()
        self.obstacles = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        #attack sprites
        self.current_attack = None

        #user interface
        self.ui = UI()

    def create_map(self):
        # Placing player in top left of map 
        self.player = Player((650, 500), [self.visibles], self.obstacles, self.create_attack, self.destroy_attack)

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
                            Tile((x,y), [self.obstacles], 'invisible')
                        if style == 'grass' :
                            #create grass tile with a random grass image surafce and make it an obstacle
                            #random_grass_img = choice(graphics['grass'])
                            Tile((x,y), [self.obstacles], 'grass')
                        if style == 'object' :
                            #surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.obstacles], 'object')
        
    
    def create_attack(self):
         self.current_attack = Weapon(self.player, [self.visibles]) 

    def destroy_attack(self):
         if self.current_attack:
              self.current_attack.kill()
              self.current_attack = None
         
    def run(self):
        # update and draw the game
        self.visibles.custom_draw(self.player)
        self.visibles.update()
        debug(self.player.status)
        self.ui.display(self.player)

# camera group - player is in middle of window by adding an offset to the player's pos
# Y sort: sorting sprites by the y-coord
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
        # get pos for center of window, floored
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
        # init offset 
		self.offset_cam = pygame.math.Vector2()

		# creating the floor: loading png for background then place at (0,0)
		self.floor_surf = pygame.image.load('../graphics/tilemap/zelda_ground2.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
    # blit stands for block transfer (copying pixels from one surface to another)
    # blit syntax: destination_surface.blit(source_surface, (x, y))

	def custom_draw(self,player):
		#getting offset from the player's pos (how much player moved from the center of the screen)
		self.offset_cam.x = player.rect.centerx - self.half_width
		self.offset_cam.y = player.rect.centery - self.half_height

		# drawing the floor (this is background image so it must be done before sprites)
		floor_offset_pos = self.floor_rect.topleft - self.offset_cam
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for every sprite, offset it's position
        # subtract player movement from it's pos so obstacles look like they're moving away
        # sorted accounts for what sprite should be drawn first
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset_cam
			self.display_surface.blit(sprite.image,offset_pos)
