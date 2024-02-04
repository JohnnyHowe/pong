import math
import pygame


from .easings import *
from .keyboard_player_input import KeyboardPlayerInput
from .player import Player
from .clock import clock
from .window import window

class Menu:
    def __init__(self):
        self.player1 = Player(KeyboardPlayerInput(pygame.K_w, pygame.K_s), position=(-6, 0), size=(0.3, 1.5))
        self.player2 = Player(KeyboardPlayerInput(pygame.K_UP, pygame.K_DOWN), position=(6, 0), size=(0.3, 1.5))
        self.player1.speed = 12
        self.player2.speed = 12
        self.players_selected = 0
        self.time_player_selected = 0
        self.select_time_to_start_game = 1

    def step(self):
        self.player1.update()
        self.player1.position[1] -= clock.dt_seconds * self.player1.position[1] * 4.5
        self.player2.update()
        self.player2.position[1] -= clock.dt_seconds * self.player2.position[1] * 4.5

        window.camera_rotation_rads = lerp(window.camera_rotation_rads, 0, clock.dt_seconds * 4)
        window.camera_position = lerp_position(window.camera_position, (0, 0), clock.dt_seconds * 4)

        position_threshold = 2
        if (self.player1.position[1] > position_threshold and self.players_selected != 1): 
            self.players_selected = 1
        elif (self.player1.position[1] < -position_threshold and self.players_selected != 2): 
            self.players_selected = 2

        self.time_player_selected += clock.dt_seconds
        if abs(self.player1.position[1]) < position_threshold: 
            self.players_selected = 0
            self.time_player_selected = 0

        self.draw()

    def draw(self):
        window.fill_undefined_area((50, 50, 50))

        self.player1.draw()
        self.player2.draw()

        p1_rect_t = clamp01(self.time_player_selected / self.select_time_to_start_game) if self.players_selected == 1 else 0
        window.draw_rect((-5.65, 3.1, lerp(0, 4.5, p1_rect_t), 1), color=(150, 150, 150))
        p2_rect_t = clamp01(self.time_player_selected / self.select_time_to_start_game) if self.players_selected == 2 else 0
        window.draw_rect((-5.65, -2.2, lerp(0, 4, p2_rect_t), 1), color=(150, 150, 150))

        window.draw_text("Single Player", (-5.5, 3), size=0.5, color=(255, 255, 255) if self.players_selected == 1 else (150, 150, 150), center_aligned=False)
        window.draw_text("Two Player", (-5.5, -2.3), size=0.5, color=(255, 255, 255) if self.players_selected == 2 else (150, 150, 150), center_aligned=False)

        key_off_color = (150, 150, 150)
        p1_moving_up = self.player1.player_input.get_movement() > 0.5
        p1_moving_down = self.player1.player_input.get_movement() < -0.5
        window.draw_text("w", (-5.5, .5),    size=0.2, color=(255, 255, 255) if p1_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^", (-5.5, .7),   size=0.2, color=(255, 255, 255) if p1_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^", (-5.5, -.4),    size=0.2, color=(255, 255, 255) if p1_moving_down else key_off_color, center_aligned=False, rotation_rads=math.pi)
        window.draw_text("s", (-5.45, -.2), size=0.2, color=(255, 255, 255) if p1_moving_down else key_off_color, center_aligned=False)

        p2_moving_up = self.player2.player_input.get_movement() > 0.5
        p2_moving_down = self.player2.player_input.get_movement() < -0.5
        window.draw_text("up",  (5.15, .5),  size=0.25, color=(255, 255, 255) if p2_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^",   (5.25, .7),    size=0.25, color=(255, 255, 255) if p2_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^",   (5.25, -.4),  size=0.25, color=(255, 255, 255) if p2_moving_down else key_off_color, center_aligned=False, rotation_rads=math.pi)
        window.draw_text("down",(4.7, -.2), size=0.25, color=(255, 255, 255) if p2_moving_down else key_off_color, center_aligned=False)
        
        window.update()

    def should_start_game(self):
        return self.time_player_selected > self.select_time_to_start_game

    def get_number_of_players(self):
        return self.players_selected
