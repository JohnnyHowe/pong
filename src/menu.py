import math
import pygame


from .easings import *
from .keyboard_player_input import KeyboardPlayerInput
from .player import Player
from .clock import clock
from .window import window
from .speaker import speaker
from .game_configuration import *

class Menu:
    def __init__(self):
        self.player1 = Player(KeyboardPlayerInput(pygame.K_w, pygame.K_s), position=(-6, 0), size=(0.3, 1.5))
        self.player2 = Player(KeyboardPlayerInput(pygame.K_UP, pygame.K_DOWN), position=(6, 0), size=(0.3, 1.5))
        self.player1.speed = 12
        self.player2.speed = 12
        # vars used for selection
        self.p1_selection = 0
        self.p2_selection = 0
        self.time_player_1_selected = 0
        self.time_player_2_selected = 0
        self.select_time_to_start_game = 1

        self.has_previously_selected = False
        self.hint_brightness_lerp_speed = 4
        self.hint_brightness_last = 0

        self.board_ball_knock = [0, 0]

    def step(self):
        self.player1.update()
        self.player2.update()

        # pull players back to center
        self.player1.position[1] -= clock.dt_seconds * self.player1.position[1] * 4.5
        self.player2.position[1] -= clock.dt_seconds * self.player2.position[1] * 4.5

        self.update_selection_properties()

        # lerp camera back to center: TODO enable juice instead
        # window.camera_rotation_rads = lerp(window.camera_rotation_rads, 0, clock.dt_seconds * 4)
        # window.camera_position = lerp_position(window.camera_position, (0, 0), clock.dt_seconds * 4)
        self.step_juice()

        self.draw()

    def step_juice(self):
        # copied and pasted from game.py - should refactor somewhere else

        for player in [self.player1, self.player2]:
            if (abs(player.position[1]) + player.size[1] / 2 >= window.game_size[1] / 2 and
                not abs(player.last_position[1]) + player.size[1] / 2 >= window.game_size[1] / 2):
                speaker.play("paddle_hit_wall")

        # we know they're the same size
        paddle_mass = self.player1.size[0] * self.player1.size[1]

        rotation_effect = math.radians(JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_ROTATION_DEGREES)
        p1_effect = self.get_player_rotation_effect(self.player1)
        p2_effect = self.get_player_rotation_effect(self.player2)
        target_camera_rotation_rads = (p1_effect - p2_effect) * rotation_effect * paddle_mass
        window.camera_rotation_rads = lerp(window.camera_rotation_rads, target_camera_rotation_rads, clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED)

        screen_movement_effect = p1_effect + p2_effect 
        target_camera_vertical_position = 0
        if abs(screen_movement_effect) == 2: target_camera_vertical_position = (screen_movement_effect / 2) * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_VERTICAL * paddle_mass * 2

        target_camera_vertical_position += self.board_ball_knock[1]
        target_camera_position = (self.board_ball_knock[0], target_camera_vertical_position)
        window.camera_position = (lerp(window.camera_position[0], target_camera_position[0], clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED),
                                  lerp(window.camera_position[1], target_camera_position[1], clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED))

    def get_player_rotation_effect(self, player):
        # copied and pasted from game.py - should refactor somewhere else
        effect = player.player_input.get_movement()
        if (player.get_desired_movement() > 0 and player.get_vertical_position_normalized() == 1 or 
            player.get_desired_movement() < 0 and player.get_vertical_position_normalized() == -1):
            effect = -effect
        return effect

    def update_selection_properties(self):
        position_threshold = 2
        if (self.player1.position[1] > position_threshold): self.p1_selection = 1
        elif (self.player1.position[1] < -position_threshold): self.p1_selection = -1
        if (self.player2.position[1] > position_threshold): self.p2_selection = 1
        elif (self.player2.position[1] < -position_threshold): self.p2_selection = -1

        self.time_player_1_selected += clock.dt_seconds
        if abs(self.player1.position[1]) < position_threshold:
            self.p1_selection = 0
            self.time_player_1_selected = 0

        self.time_player_2_selected += clock.dt_seconds
        if abs(self.player2.position[1]) < position_threshold:
            self.p2_selection = 0
            self.time_player_2_selected = 0

        # stop timer increasing when other side is selectedss
        if (self.time_player_1_selected > self.time_player_2_selected): self.time_player_2_selected = 0
        if (self.time_player_2_selected > self.time_player_1_selected): self.time_player_1_selected = 0

        if self.get_number_of_players() != None: self.has_previously_selected = True

    def draw(self):
        window.fill_undefined_area((50, 50, 50))

        self.player1.draw()
        self.player2.draw()

        # selection rectangles behind text
        p1_rect_t = clamp01(self.time_player_1_selected / self.select_time_to_start_game) if self.get_number_of_players() == 1 else 0
        window.draw_rect((-5.65, 3.1, lerp(0, 4.5, p1_rect_t), 1), color=(150, 150, 150))
        p2_rect_t = clamp01(self.time_player_1_selected / self.select_time_to_start_game) if self.get_number_of_players() == 2 else 0
        window.draw_rect((-5.65, -2.2, lerp(0, 4, p2_rect_t), 1), color=(150, 150, 150))
        p3_rect_t = clamp01(self.time_player_2_selected / self.select_time_to_start_game) if self.get_number_of_players() == 0 else 0
        window.draw_rect((.8, 3.1, lerp(0, 4.9, p3_rect_t), 1), color=(150, 150, 150))
        p4_rect_t = clamp01(self.time_player_2_selected / self.select_time_to_start_game) if self.get_number_of_players() == -1 else 0
        window.draw_rect((4, -2.1, lerp(0, 1.6, p4_rect_t), 1), color=(150, 150, 150))

        # selection options
        window.draw_text("Single Player", (-5.5, 3), size=0.5, color=(255, 255, 255) if self.get_number_of_players() == 1 else (150, 150, 150), center_aligned=False)
        window.draw_text("Two Players", (-5.5, -2.3), size=0.5, color=(255, 255, 255) if self.get_number_of_players() == 2 else (150, 150, 150), center_aligned=False)
        window.draw_text("Exit", (4.2, -2.3), size=0.5, color=(255, 255, 255) if self.get_number_of_players() == -1 else (150, 150, 150), center_aligned=False)
        if (self.get_number_of_players() == 0): window.draw_text("Zero Players?", (1, 3), size=0.5, color=(255, 255, 255), center_aligned=False)

        # p1 controls 
        key_off_color = (150, 150, 150)
        p1_moving_up = self.player1.player_input.get_movement() > 0.5
        p1_moving_down = self.player1.player_input.get_movement() < -0.5
        window.draw_text("w", (-5.5, .5),    size=0.2, color=(255, 255, 255) if p1_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^", (-5.5, .7),   size=0.2, color=(255, 255, 255) if p1_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^", (-5.5, -.4),    size=0.2, color=(255, 255, 255) if p1_moving_down else key_off_color, center_aligned=False, rotation_rads=math.pi)
        window.draw_text("s", (-5.45, -.2), size=0.2, color=(255, 255, 255) if p1_moving_down else key_off_color, center_aligned=False)

        # p2 controls
        p2_moving_up = self.player2.player_input.get_movement() > 0.5
        p2_moving_down = self.player2.player_input.get_movement() < -0.5
        window.draw_text("up",  (5.15, .5),  size=0.25, color=(255, 255, 255) if p2_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^",   (5.25, .7),    size=0.25, color=(255, 255, 255) if p2_moving_up else key_off_color, center_aligned=False)
        window.draw_text("^",   (5.25, -.4),  size=0.25, color=(255, 255, 255) if p2_moving_down else key_off_color, center_aligned=False, rotation_rads=math.pi)
        window.draw_text("down",(4.7, -.2), size=0.25, color=(255, 255, 255) if p2_moving_down else key_off_color, center_aligned=False)

        # hint brightness
        hint_brightness_target = lerp(0.2, 1, 0.5 - math.cos(clock.time_running_seconds * 4) / 2) if not self.has_previously_selected else 0.2
        hint_brightness = lerp(self.hint_brightness_last, hint_brightness_target, clock.dt_seconds * self.hint_brightness_lerp_speed)
        window.draw_text("Hint: move the paddles to select options", (0, -4), (hint_brightness * 255,) * 3, 0.2)
        self.hint_brightness_last = hint_brightness

        window.update()

    def should_start_game(self):
        return self.time_player_1_selected > self.select_time_to_start_game or self.time_player_2_selected > self.select_time_to_start_game

    def get_number_of_players(self):
        if self.time_player_1_selected > self.time_player_2_selected and self.time_player_1_selected > 0:
            return 1 if self.p1_selection == 1 else 2
        elif self.time_player_2_selected > 0:
            return 0 if self.p2_selection == 1 else -1
        
