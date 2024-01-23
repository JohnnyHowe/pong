import pygame
from src.i_player_input import IPlayerInput

class KeyboardPlayerInput(IPlayerInput) :

    def __init__(self, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key

    def get_movement(self):
        keys = pygame.key.get_pressed()
        movement = 0
        if keys[self.up_key]: movement += 1
        if keys[self.down_key]: movement -= 1
        return movement