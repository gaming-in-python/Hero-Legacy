import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #create bg rect for each bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, BAR_HEIGHT + 20, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        #create list of weapon graphics
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            weapon = pygame.image.load(weapon['graphic']).convert_alpha()
            self.weapon_graphics.append(weapon)

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

    #put image of current weapon in bottom left of screen
    def weapon_overlay(self, weapon_index, is_switching):
        bg_rect = self.selection_box(10, self.display_surface.get_size()[1] - ITEM_BOX_SIZE - 20, is_switching)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_idx, not player.can_switch_weapon)
        #self.selection_box(10 + ITEM_BOX_SIZE - UI_BORDER_WEIGHT, self.display_surface.get_size()[1] - ITEM_BOX_SIZE - 15)
