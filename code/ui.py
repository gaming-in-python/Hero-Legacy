import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #create bg rect for each bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, BAR_HEIGHT + 20, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = self.load_graphics(weapon_data)
        self.magic_graphics = self.load_graphics(magic_data)

    #creates list of graphics for given dictionary
    def load_graphics(self, data):
        graphics = []
        for item in data.values():
            graphic = pygame.image.load(item['graphic']).convert_alpha()
            graphics.append(graphic)
        return graphics

    #draw a stat bar in top left of screen
    def show_bar(self, current_amount, max_amount, bg_rect, color):
        #draw background rectangle
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        #draw the current health/energy levels on top of bg_rect
        current_width = (current_amount / max_amount) * bg_rect.width
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        #draw border around bar
        #last argument (3) is a border weight and indicates to display only the border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, UI_BORDER_WEIGHT)

    #place text displaying exp in bottom right of screen
    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), UI_BORDER_WEIGHT)
        self.display_surface.blit(text_surf, text_rect)

    #draw a box for displaying an image
    def selection_box(self, left, top, is_switching):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if is_switching:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, UI_BORDER_WEIGHT)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, UI_BORDER_WEIGHT)
        return bg_rect
    
    #displays current items being used in bottom left
    def overlay(self, item_index, graphics, is_switching, box_idx):
        bg_rect = self.selection_box(10 + box_idx * (ITEM_BOX_SIZE - UI_BORDER_WEIGHT), 
                                     self.display_surface.get_size()[1] - ITEM_BOX_SIZE - (20 - (box_idx * 5)),
                                       is_switching)
        surf = graphics[item_index]
        rect = surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(surf, rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.overlay(player.weapon_idx, self.weapon_graphics, not player.can_switch_weapon, 0)
        self.overlay(player.magic_idx, self.magic_graphics, not player.can_switch_magic, 1)
