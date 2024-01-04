import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacles):
        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles = obstacles

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

    def import_graphics(self, name):
        self.animations = {'idle' :[], 'move' :[], 'attack' :[]}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def update(self):
        pass
        #self.move(self.speed)

    def get_player_distance_direction(self,player) :
        pass
        # enemy_vec = #IN PROGESS
        # return (distance, direction)

    def get_status(self,player):
        pass
        # distance = ???

        # if distance <= self.attack_radius:
        #     self.status = 'attack'
        # elif distance <= self.notice_radius:
        #     self.status = 'move'
        # else :
        #     self.status = 'idle'