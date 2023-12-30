import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    #initialize variables
    def __init__(self,pos,groups): 
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        #graphics setup
        self.import_player_assets()
        self.status = 'down' #default looking "downwards"
        self.frame_index = 0
        self.animation_speed = 0.15

        #movement variables to help control parsing the input
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

    #getting all animation assets
    def import_player_assets(self):
        general_path = '.../graphics/player/'
        
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
        
    # #adding input interactions!
    def input(self) :
        if not self.attacking:
            #key that is pressed
            press = pygame.key.get_pressed()

            #movement
            if press[pygame.K_UP or pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif press[pygame.K_DOWN or pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            elif press[pygame.K_LEFT or pygame.K_a]:
                self.direction.x = -1
                self.status = 'right'
            elif press[pygame.K_RIGHT or pygame.K_d]:
                self.direction.x = 1
                self.status = 'left'
            else :
                self.direction.x = 0
                self.direction.y = 0

            #attack (Because who uses spacebar for anything but jump??)
            if press[pygame.K_j] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("attack")

            #magic
            if press[pygame.K_k] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("magic")

    #get the current status of the player and update it
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

    #enforce cooldowns so that the player cannot spam attack
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    #animate the movements!
    def animate(self):
        animation = self.animation[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    #update the various components (variables/states/animation frames) of the player animations
    def update(self):
        self.input()
        self.cooldown()
        # self.get_status()
        self.animate()
        self.move(self.speed)