import pygame 
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # player hitbox
        self.hitbox = self.rect.inflate(0, -26)
        # direction - 2d vector
        # get keyboard input and then multiply by speed to determine motion
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacles = obstacles

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
            print("attack")

        #magic
        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("magic")
    
    def move(self, speed):
        if self.direction.magnitude() != 0: #vector of 0 cant be normalized!
            # making sure magnitude of vector = 1 so player has same speed when moving diagonally
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

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
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    #connecting inputs to animations
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # print(self.frame_index)
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    #updating all player variables
    def update(self):
        self.input()
        self.move(self.speed)

         # self.get_status() 
        self.animate()
    
