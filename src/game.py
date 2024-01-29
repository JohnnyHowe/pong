import math
import pygame

from .game_configuration import *
from .keyboard_player_input import KeyboardPlayerInput
from .clock import clock
from .window import window
from .player import Player
from .ball import Ball
from .easings import *

class Game:

    player1 = None
    player2 = None
    ball = None

    def __init__(self):
        self.player1 = Player(KeyboardPlayerInput(pygame.K_w, pygame.K_s), position=(-6, 0))
        self.player2 = Player(KeyboardPlayerInput(pygame.K_UP, pygame.K_DOWN), position=(6, 0))
        self.reset_ball()
        self.board_ball_knock = [0, 0]

    def reset_ball(self):
        self.ball = Ball()
        self.ball.on_collision_delegate = self.ball_collision_delegate

    def run(self):
        while True:
            clock.tick()
            self.step()

    def step(self):
        self.run_event_loop()

        self.player1.update()
        self.player2.update()
        self.ball.update([self.player1, self.player2])

        if (self.ball.is_off_screen_horizontal()):
            self.reset_ball()

        # visuals
        window._draw_buffer.fill((0, 0, 0))
        window.fill_undefined_area((150, 150, 150))

        self.player1.draw()
        self.player2.draw()
        self.ball.show()

        self.step_juice()
        window.update()

    def step_juice(self):
        rotation_effect = math.radians(JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_ROTATION_DEGREES / 2)
        p1_effect = self.get_player_rotation_effect(self.player1)
        p2_effect = self.get_player_rotation_effect(self.player2)
        target_camera_rotation_rads = (p1_effect - p2_effect) * rotation_effect
        window.camera_rotation_rads = lerp(window.camera_rotation_rads, target_camera_rotation_rads, clock.dt_seconds * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_LERP_SPEED)

        screen_movement_effect = p1_effect + p2_effect 
        target_camera_vertical_position = 0
        if abs(screen_movement_effect) == 2: target_camera_vertical_position = (screen_movement_effect / 2) * JUICE_SCREEN_MOVEMENT_FROM_PADDLE_MAX_VERTICAL

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

    def run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.VIDEORESIZE:
                window.set_size((event.w, event.h))

    def ball_collision_delegate(self, other, resolution_direction):
        print("ball collision with", other, resolution_direction)

        # collided with horizontal wall
        if other is None:
            self.board_ball_knock[1] = JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK * resolution_direction[1]

        # collided with paddle
        elif isinstance(other, Player):
            other.knock_back(-resolution_direction[0] * JUICE_PADDLE_KNOCKBACK)
            self.board_ball_knock[0] = -JUICE_SCREEN_MOVEMENT_FROM_BALL_KNOCK * resolution_direction[0]