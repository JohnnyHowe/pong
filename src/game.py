import math
import pygame

from .keyboard_player_input import KeyboardPlayerInput
from .clock import clock
from .window import window
from .player import Player

class Game:

    player1 = None
    player2 = None

    def __init__(self):
        self.player1 = Player(KeyboardPlayerInput(pygame.K_w, pygame.K_s), position=(-6, 0))
        self.player2 = Player(KeyboardPlayerInput(pygame.K_UP, pygame.K_DOWN), position=(6, 0))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    window.set_size((event.w, event.h))
            
            clock.tick()

            window.camera_rotation_rads = 0
            window.camera_rotation_rads += self.player1.player_input.get_movement() * math.radians(5)
            window.camera_rotation_rads -= self.player2.player_input.get_movement() * math.radians(5)

            window._draw_buffer.fill((0, 0, 0))
            window.draw_screen_gizmos()
            window.fill_undefined_area((100, 100, 100))

            self.player1.update()
            self.player2.update()

            self.player1.draw()
            self.player2.draw()

            window.update()

        pygame.quit()

