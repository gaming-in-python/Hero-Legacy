import pygame 
from settings import *
from support import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacles, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # player hitbox
        self.hitbox = self.rect.inflate(0, -26)
        self.obstacles = obstacles

        #graphics setup
        self.import_player_assets()
        self.status = 'down' #default looking "downwards"
        
        #inherits frame index, direction and animation speed from Entity
        
        #movement variables to help control parsing the input
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_idx = 0
        self.weapon = list(weapon_data.keys())[self.weapon_idx]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_idx = 0
        self.magic = list(magic_data.keys())[self.magic_idx]
        self.can_switch_magic = True
        self.magic_switch_time = None
        
        #stats
        #map each stat to a max value
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        #initialize values that will change to their max
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.speed = self.stats['speed']
        self.exp = 500

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500


    # method to get keyboard input
    def input(self):
        keys = pygame.key.get_pressed() # get all the keys that are potentially being pressed
        # set direction based on key pressed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        else:
            # if no x-dir key pressed, no movement
            # resets x-dir to 0 when you stop pressing key (otherwise player would keep moving in previous direction)
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

         #attack (Because who uses spacebar for anything but jump??)
        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            #print("attack")
            self.create_attack()

        #magic
        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_idx]
            strength = list(magic_data.values())[self.magic_idx].get("strength") + self.stats['magic']
            cost = list(magic_data.values())[self.magic_idx].get("cost")
            self.create_magic(style, strength, cost)

        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if self.weapon_idx < len(list(weapon_data.keys())) - 1:
                self.weapon_idx +=1
            else:
                self.weapon_idx =0
            self.weapon = list(weapon_data.keys())[self.weapon_idx]

        if keys[pygame.K_e] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            if self.magic_idx < len(list(magic_data.keys())) - 1:
                self.magic_idx +=1
            else:
                self.magic_idx =0
            self.magic = list(magic_data.keys())[self.magic_idx]
    
    #removed move and collision and put them in entity for Player class to inherit from
            
    #getting all animation assets
    def import_player_assets(self):
        general_path = '../graphics/player/'
        
        #animations in dictionary include moving, being idle and attacking in all 4 directions
        self.animations = {'up' : [], 
                           'down' : [],
                           'left' : [],
                           'right' : [],
                           'right_idle' : [],
                           'left_idle' : [],
                           'up_idle' : [],
                           'down_idle' : [],
                           'right_attack' : [],
                           'left_attack' : [],
                           'up_attack' : [],
                           'down_attack' : []}
        
        #loop to complete the file path for each state in the dicitionary above
        #uses basic string concatenation
        for animation in self.animations.keys():
            complete_path = general_path + animation
            self.animations[animation] = import_folder(complete_path)

    #getting current status of player
    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    #overwrite '_idle'
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    #processing time cooldowns between actions of the player
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack() 

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    
    #connecting inputs to animations
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # print(self.frame_index)
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #player flickers when attacked
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            #recovery rate increases with magic level
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    #updating all player variables
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
    
