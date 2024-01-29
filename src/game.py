import math
import pygame

from .user_config import user_config

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
        while True:
            clock.tick()
            self.step()

    def step(self):
        self.run_event_loop()

        rotation_effect = math.radians(user_config.get("juice_screen_movement_from_paddle_max_rotation_degrees") / 2)
        p1_effect = self.get_player_rotation_effect(self.player1)
        p2_effect = self.get_player_rotation_effect(self.player2)
        target_camera_rotation_rads = (p1_effect - p2_effect) * rotation_effect
        window.camera_rotation_rads = self.lerp(window.camera_rotation_rads, target_camera_rotation_rads, clock.dt_seconds * user_config.get("juice_screen_movement_from_paddle_lerp_speed"))

        movement = p1_effect + p2_effect 
        target_camera_vertical_position = 0
        if abs(movement) == 2: target_camera_vertical_position = (movement / 2) * user_config.get("juice_screen_movement_from_paddle_max_vertical")
        window.camera_position = (0, self.lerp(window.camera_position[1], target_camera_vertical_position, clock.dt_seconds * user_config.get("juice_screen_movement_from_paddle_lerp_speed")))

        window._draw_buffer.fill((0, 0, 0))
        window.fill_undefined_area((150, 150, 150))

        self.player1.update()
        self.player2.update()

        self.player1.draw()
        self.player2.draw()

        window.update()

    def get_player_rotation_effect(self, player):
        effect = player.player_input.get_movement()
        if (player.get_desired_movement() > 0 and player.get_vertical_position_normalized() == 1 or 
            player.get_desired_movement() < 0 and player.get_vertical_position_normalized() == -1):
            effect = -effect
        return effect

    def run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.VIDEORESIZE:
                window.set_size((event.w, event.h))


    def lerp(self, a, b, t):
        return a + (b - a) * t

