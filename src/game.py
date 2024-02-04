import math
import random
import pygame

from .smart_ai_input import Smart_AI_Input
from .game_configuration import *
from .keyboard_player_input import KeyboardPlayerInput
from .clock import clock
from .window import window
from .player import Player
from .ball import Ball
from .easings import *
from .speaker import speaker

class Game:
    # Lots of ugly code in this class
    # Please forgive me

    def __init__(self, n_players=1):
        self.ball = Ball()
        self.ball.on_collision_delegate = self.ball_collision_delegate

        self.player1 = self.create_player((-6, 0), (0.25, 1.5), pygame.K_w, pygame.K_s, ai=(n_players == 0))
        self.player2 = self.create_player((6, 0), (0.25, 1.5), pygame.K_UP, pygame.K_DOWN, ai=(n_players == 1))

        self.scores = [0, 0]
        self.last_ball_start_side = 1 
        self.reset_game()
        self.board_ball_knock = [0, 0]
        self.time_since_last_click_seconds = 1
        self.time_running = 0

    def create_player(self, position, size, up_key, down_key, ai=False):
        player = Player(KeyboardPlayerInput(up_key, down_key), position, size)
        if ai:
            player.player_input = Smart_AI_Input(self.ball, window.game_size)
            player.player_input.paddle = player 
        return player

    def reset_game(self):
        self.ball_size_index = random.randint(0, len(GAME_BALL_SIZES) - 1)
        self.paddle_size_index = random.randint(0, len(GAME_PADDLE_SIZES) - 1)

        self.ball.reset()
        self.ball.size = GAME_BALL_SIZES[self.ball_size_index][0]

        self.last_ball_start_side = -self.last_ball_start_side
        self.ball_held_by = self.player1 if self.last_ball_start_side == -1 else self.player2
        self.ball_held_time_left = GAME_BALL_HOLD_TIME

        paddle_size = GAME_PADDLE_SIZES[self.paddle_size_index] 
        self.player1.size = paddle_size
        self.player2.size = paddle_size
        self.rally_time = 0

    def run(self):
        while True:
            clock.tick()
            self.step()

    def step(self):
        self.time_running += clock.dt_seconds
        self.rally_time += clock.dt_seconds

        self.player1.update()
        self.player2.update()
        self.ball.update([self.player1, self.player2])

        if self.ball.is_off_screen_horizontal():
            self.scores[1 if self.ball.position[0] < 0 else 0] += 1
            speaker.play("game_over")
            self.reset_game()

        # pregame thing, when ball is held by player
        if self.ball_held_by is not None:
            self.ball.position = [self.ball_held_by.position[0] + (self.ball_held_by.size[0] / 2 + self.ball.size) * -self.last_ball_start_side, self.ball_held_by.position[1]]
            self.ball_held_time_left -= clock.dt_seconds
            if (self.ball_held_time_left <= 0):
                self.ball_held_by = None
                self.ball.velocity = [GAME_BALL_START_SPEED * self.last_ball_start_side, 0]

        # visuals
        window._screen.fill((50, 50, 50))
        window.fill_game_area((0, 0, 0))

        window.draw_text(self.scores[0], (-3, -.2), (50, 50, 50), 1)
        window.draw_text(self.scores[1], (3, -.2), (50, 50, 50), 1)

        back_to_menu_text_grey = lerp(0, 255, east_in_then_out(self.time_running / 2, ease_out_cubic, ease_out_cubic, hold=0.5))
        window.draw_text("Press ESC to go back to menu", (0, -4), (back_to_menu_text_grey,) * 3, 0.2)

        text_color_t = east_in_then_out(self.rally_time / 2, ease_out_cubic, ease_out_cubic, hold=0.5)
        info_text_brightness = lerp(0, 255, text_color_t)
        info_text_color = (info_text_brightness, ) * 3
        window.draw_text(GAME_PADDLE_SIZES[self.paddle_size_index][2] + " Paddles", (0, 3.5), info_text_color, .5)
        window.draw_text(GAME_BALL_SIZES[self.ball_size_index][1] + " Ball", (0, 2.5), info_text_color, .5)

        self.player1.draw()
        self.player2.draw()
        self.ball.draw()
        
        self.step_juice()

        window.update()

    def step_juice(self):
        for player in [self.player1, self.player2]:
            if (abs(player.position[1]) + player.size[1] / 2 >= window.game_size[1] / 2 and
                not abs(player.last_position[1]) + player.size[1] / 2 >= window.game_size[1] / 2):
                speaker.play("paddle_hit_wall")

        # we know they're the same size
        paddle_mass = self.player1.size[0] * self.player1.size[1]

        rotation_effect = math.radians(JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_ROTATION_DEGREES / 2)
        p1_effect = self.get_player_rotation_effect(self.player1)
        p2_effect = self.get_player_rotation_effect(self.player2)
        target_camera_rotation_rads = (p1_effect - p2_effect) * rotation_effect * paddle_mass
        window.camera_rotation_rads = lerp(window.camera_rotation_rads, target_camera_rotation_rads, clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED)

        screen_movement_effect = p1_effect + p2_effect 
        target_camera_vertical_position = 0
        if abs(screen_movement_effect) == 2: target_camera_vertical_position = (screen_movement_effect / 2) * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_VERTICAL * paddle_mass

        self.board_ball_knock[0] = lerp(self.board_ball_knock[0], 0, clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_RETURN_LERP_SPEED)
        self.board_ball_knock[1] = lerp(self.board_ball_knock[1], 0, clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_RETURN_LERP_SPEED)

        target_camera_vertical_position += self.board_ball_knock[1]
        target_camera_position = (self.board_ball_knock[0], target_camera_vertical_position)
        window.camera_position = (lerp(window.camera_position[0], target_camera_position[0], clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED),
                                  lerp(window.camera_position[1], target_camera_position[1], clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED))

    def get_player_rotation_effect(self, player):
        effect = player.player_input.get_movement()
        if (player.get_desired_movement() > 0 and player.get_vertical_position_normalized() == 1 or 
            player.get_desired_movement() < 0 and player.get_vertical_position_normalized() == -1):
            effect = -effect
        return effect

    def ball_collision_delegate(self, other, resolution_direction):
        # Ugly code. I'm sorry LSP
        ball_mass = self.ball.size ** 2

        # collided with horizontal wall
        if other is None:
            speaker.play("ball_hit_wall")
            self.board_ball_knock[1] = self.get_screen_knock_power()[1] * resolution_direction[1] * ball_mass 

        # collided with paddle
        elif isinstance(other, Player):
            speaker.play("ball_hit_paddle")
            other.knock_back(-resolution_direction[0] * JUICE_PADDLE_KNOCKBACK)
            self.board_ball_knock[0] = self.get_screen_knock_power()[0] * resolution_direction[0] * ball_mass
        
    def get_screen_knock_power(self):
        return (lerp(JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_MIN_X, JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_MAX_X, abs(self.ball.velocity[0]) / JUICE_SCREEN_MOVEMENT_FROM_BALL_SPEED_FOR_KNOCK_MAX_X),
                lerp(JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_MIN_Y, JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK_MAX_Y, abs(self.ball.velocity[1]) / JUICE_SCREEN_MOVEMENT_FROM_BALL_SPEED_FOR_KNOCK_MAX_Y)) 