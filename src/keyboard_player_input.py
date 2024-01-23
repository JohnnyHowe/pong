import pygame
from src.i_player_input import IPlayerInput

class KeyboardPlayerInput(IPlayerInput) :

    def __init__(self, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key

    def get_movement(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            return 1
        elif keys[self.down_key]:
            return -1
        else:
            return 0