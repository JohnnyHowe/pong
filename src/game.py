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
        target_camera_rotation_rads = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    window.set_size((event.w, event.h))
            
            clock.tick()

            target_camera_rotation_rads = 0
            target_camera_rotation_rads += self.player1.player_input.get_movement() * math.radians(3)
            target_camera_rotation_rads -= self.player2.player_input.get_movement() * math.radians(3)
            window.camera_rotation_rads = self.lerp(window.camera_rotation_rads, target_camera_rotation_rads, clock.dt_seconds * 8)

            movement = self.player1.player_input.get_movement() + self.player2.player_input.get_movement()
            target_camera_vertical_position = 0
            if abs(movement) == 2: target_camera_vertical_position = (movement / 2) * 0.5
            window.camera_position = (0, self.lerp(window.camera_position[1], target_camera_vertical_position, clock.dt_seconds * 4))

            window._draw_buffer.fill((0, 0, 0))
            window.fill_undefined_area((100, 100, 100))
            window.draw_screen_gizmos()

            self.player1.update()
            self.player2.update()

            self.player1.draw()
            self.player2.draw()

            window.update()

        pygame.quit()

    def lerp(self, a, b, t):
        return a + (b - a) * t

