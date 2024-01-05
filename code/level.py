import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer

class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        #getting the sprites for obstacles+player
        self.visibles = YSortCameraGroup()
        self.obstacles = pygame.sprite.Group()
        #attack sprites
        self.current_attack = None
        self.attacking = pygame.sprite.Group()
        self.attackable = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        #user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()


    def create_map(self):
        layouts = {
            # 'boundary': import_csv_layout('../map/zelda_ground2_Border.csv'),
            # 'grass' : import_csv_layout('../map/zelda_ground2_Grass.csv'),
            # 'object': import_csv_layout('../map/zelda_ground2_Trees.csv'),
            # 'entities': import_csv_layout('../map/zelda_ground2_Entities.csv')
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
        }

        graphics = {
            'grass' : import_folder('../graphics/Grass'),
            'objects' : import_folder('../graphics/objects')
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
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visibles, self.obstacles, self.attackable],
                                'grass',
                                random_grass_image)
                        if style == 'object' :
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visibles,self.obstacles],'object',surf)
                        if style == 'entities' :
                            if col == '394' :
                                  self.player = Player(
                                       (x,y),
                                       [self.visibles],
                                       self.obstacles,
                                       self.create_attack,
                                       self.destroy_attack,
                                       self.create_magic)
                            else :
                                 if col == '390' : monster_name = 'bamboo'
                                 elif col == '391' : monster_name = 'spirit'
                                 elif col == '392' : monster_name = 'raccoon'
                                 else : monster_name = 'squid'
                                 Enemy(
                                    monster_name, 
                                    (x,y), 
                                    [self.visibles,self.attackable], 
                                    self.obstacles,
                                    self.damage_player,
                                    self.trigger_death_particles)
                             
    
    def create_attack(self):
         self.current_attack = Weapon(self.player, [self.visibles, self.attacking]) 

    def create_magic(self, style, strength, cost):
         print(style)
         print(strength)
         print(cost)

    def destroy_attack(self):
        if self.current_attack:
              self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):
        if self.attacking:
            for attack_sprite in self.attacking:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable, False)
                if collision_sprites:
                    for target in collision_sprites:
                        if target.sprite_type == 'grass':
                            pos = target.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset,[self.visibles])
                            target.kill()

                        else:
                            target.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, damage, attack_type):
        if self.player.vulnerable:
            self.player.health -= damage
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visibles])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type, pos,self.visibles)   
    
    def run(self):
        # update and draw the game
        self.visibles.custom_draw(self.player)
        self.visibles.update()
        self.visibles.enemy_update(self.player)
        self.player_attack_logic()
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
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        
    # blit stands for block transfer (copying pixels from one surface to another)
    # blit syntax: destination_surface.blit(source_surface, (x, y))

    def custom_draw(self, player):
        # getting offset from the player's pos (how much player moved from the center of the screen)
        self.offset_cam.x = player.rect.centerx - self.half_width
        self.offset_cam.y = player.rect.centery - self.half_height

        # drawing the floor (this is background image so it must be done before sprites)
        floor_offset_pos = self.floor_rect.topleft - self.offset_cam
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for every sprite, offset its position
        # subtract player movement from its pos so obstacles look like they're moving away
        # sorted accounts for what sprite should be drawn first
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset_cam
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
             sprite.enemy_update(player)

             