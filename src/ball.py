import math
import random

from .window import window
from .clock import clock
from .game_configuration import * 

class Ball:

    def __init__(self):
        self.position = [0, 0]
        self.velocity = [4, 4]
        self.size = 0.4
        self.base_speed = 4
        self.time_alive = 0
        self.on_collision_delegate = None   # (self, other, resolution_direction)

    def update(self, paddle_rects):
        self.time_alive += clock.dt_seconds

        self.position[0] += self.velocity[0] * clock.dt_seconds
        self.position[1] += self.velocity[1] * clock.dt_seconds

        self.process_paddle_collisions(paddle_rects)
        self.process_game_border_collisions()

        self.clamp_velocity_proportion()
        self.set_speed()

    def clamp_velocity_proportion(self):
        """ Stop the vertical speed/ horizontal speed proportion getting out of hand. """
        if (self.velocity[0] == 0): return
        current_proportion_signed = self.velocity[1] / abs(self.velocity[0])
        max_proportion_unsigned = GAME_MAX_BALL_VERTICAL_SPEED_PROPORTION
        if abs(current_proportion_signed) <= max_proportion_unsigned: return
        self.velocity[1] = abs(self.velocity[0]) * max_proportion_unsigned * (-1 if current_proportion_signed < 0 else 1)

    def set_speed(self):
        if (self.velocity[0] == 0): return
        too_fast_multiplier = self.get_target_speed() / self.get_speed()
        self.velocity[0] *= too_fast_multiplier
        self.velocity[1] *= too_fast_multiplier

    def get_target_speed(self):
        return self.base_speed + GAME_BALL_SPEED_INCREASE_RATE * self.time_alive 

    def get_speed(self):
        return math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

    def process_paddle_collisions(self, paddles):
        for paddle in paddles:
            self.process_paddle_collision(paddle)

    def process_paddle_collision(self, paddle):
        """ Process the potential collision with paddle_rect 
        Is a basic 2d, axis aligned collision detection and resolution """
        paddle_rect = paddle.get_rect()
        if not self.is_colliding(paddle_rect): return

        # collision resolution
        overlap_rect = self.get_overlap_rect(paddle_rect)
        resolution_direction = (0, 0)
        if (overlap_rect[2] < overlap_rect[3]):
            # horizontal overlap resolution
            is_left_of_paddle = self.position[0] < paddle_rect[0] + paddle_rect[2] / 2
            resolution_direction = (-1 if is_left_of_paddle else 1, 0)
            self.position[0] += overlap_rect[2] * resolution_direction[0] 
            self.velocity[0] = abs(self.velocity[0]) * resolution_direction[0]
            self.velocity[1] += paddle.velocity[1] * GAME_PADDLE_SPEED_EFFECT_ON_BALL_VELOCITY 
        else:
            # vertical overlap resolution
            is_above_paddle = self.position[1] > paddle_rect[1] - paddle_rect[3] / 2
            resolution_direction = (0, -1 if is_above_paddle else 1)
            self.position[1] -= overlap_rect[3] * resolution_direction[1] 
            self.velocity[1] = -abs(self.velocity[1]) * resolution_direction[1] 

        self.add_random_velocity();
        self.invoke_collision_delegate(paddle, resolution_direction)

    def process_game_border_collisions(self):
        if (self.position[1] + self.size / 2 > window.game_size[1] / 2):
            # top overlap resolution
            self.position[1] = window.game_size[1] / 2 - self.size / 2
            self.velocity[1] *= -1
            self.invoke_collision_delegate(None, (0, -1))
            self.add_random_velocity();
        elif (self.position[1] - self.size / 2 < -window.game_size[1] / 2):
            # bottom overlap resolution
            self.position[1] = -window.game_size[1] / 2 + self.size / 2
            self.velocity[1] *= -1
            self.invoke_collision_delegate(None, (0, 1))
            self.add_random_velocity();

    def add_random_velocity(self):
        self.velocity[0] += (self.signed_random() * GAME_BALL_BOUNCE_VELOCITY_RANDOMNESS_PROPORTION) * self.velocity[0] + GAME_BALL_VELOCITY_RANDOMNESS_MINIMUM * self.signed_random() 
        self.velocity[1] += (self.signed_random() * GAME_BALL_BOUNCE_VELOCITY_RANDOMNESS_PROPORTION) * self.velocity[1] + GAME_BALL_VELOCITY_RANDOMNESS_MINIMUM * self.signed_random()

    def signed_random(self):
        return random.random() * 2 - 1
        
    def invoke_collision_delegate(self, other, resolution_direction):
        if self.on_collision_delegate is not None: 
            self.on_collision_delegate(other, resolution_direction)

    def get_overlap_rect(self, paddle_rect):
        self_rect = self.get_rect()
        return (
            max(self_rect[0], paddle_rect[0]),
            min(self_rect[1], paddle_rect[1]),
            abs(min(self_rect[0] + self_rect[2], paddle_rect[0] + paddle_rect[2]) - max(self_rect[0], paddle_rect[0])),
            abs(max(self_rect[1] - self_rect[3], paddle_rect[1] - paddle_rect[3]) - min(self_rect[1], paddle_rect[1]))
        )

    def is_colliding(self, paddle_rect):
        """ Is the ball colliding with paddle_rect? """
        self_rect = self.get_rect()
        return (self_rect[0] < paddle_rect[0] + paddle_rect[2] and 
                self_rect[0] + self_rect[2] > paddle_rect[0] and 
                self_rect[1] > paddle_rect[1] - paddle_rect[3] and 
                self_rect[1] - self_rect[3] < paddle_rect[1])

    def draw(self):
        window.draw_rect(self.get_rect(), (255, 255, 255))
    
    def get_rect(self):
        return (self.position[0] - self.size / 2, self.position[1] + self.size / 2, self.size, self.size)

    def is_off_screen_horizontal(self):
        max_x = window.game_size[0] / 2 - self.size / 2
        return abs(self.position[0]) > max_x 
