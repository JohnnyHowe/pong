import pygame
from .window import window
from .clock import clock
from .user_config import user_config

class Ball:
    size = 0.4

    def __init__(self):
        self.position = [0, 0]
        self.velocity = [4, 4]

    def update(self, paddle_rects):
        self.position[0] += self.velocity[0] * clock.dt_seconds
        self.position[1] += self.velocity[1] * clock.dt_seconds
        self.process_collisions(paddle_rects)
        self.process_game_border_collisions()

    def process_collisions(self, paddles):
        for paddle in paddles:
            self.process_collision(paddle)

    def process_collision(self, paddle):
        """ Process the potential collision with paddle_rect 
        Is a basic 2d, axis aligned collision detection and resolution """
        paddle_rect = paddle.get_rect()
        if not self.is_colliding(paddle_rect): return

        # collision resolution
        overlap_rect = self.get_overlap_rect(paddle_rect)
        if (overlap_rect[2] < overlap_rect[3]):
            # horizontal overlap resolution
            is_left_of_paddle = self.position[0] < paddle_rect[0] + paddle_rect[2] / 2
            self.position[0] -= overlap_rect[2] * (1 if is_left_of_paddle else -1)
            self.velocity[0] = abs(self.velocity[0]) * (-1 if is_left_of_paddle else 1)
            # vertical velocity adjustment from paddle velocity
            self.velocity[1] += paddle.velocity[1] * user_config.get("game_paddle_speed_effect_on_ball")
            print("collide!", self.velocity, paddle.velocity)
        else:
            # vertical overlap resolution
            is_above_paddle = self.position[1] > paddle_rect[1] - paddle_rect[3] / 2
            self.position[1] += overlap_rect[3] * (1 if is_above_paddle else -1)
            self.velocity[1] = abs(self.velocity[1]) * (1 if is_above_paddle else -1)

    def process_game_border_collisions(self):
        if (self.position[1] + self.size / 2 > window.game_size[1] / 2):
            # horizontal overlap resolution
            self.position[1] = window.game_size[1] / 2 - self.size / 2
            self.velocity[1] *= -1
        elif (self.position[1] - self.size / 2 < -window.game_size[1] / 2):
            # vertical overlap resolution
            self.position[1] = -window.game_size[1] / 2 + self.size / 2
            self.velocity[1] *= -1

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

    def show(self):
        window.draw_rect(self.get_rect(), (255, 255, 255))
    
    def get_rect(self):
        return (self.position[0] - self.size / 2, self.position[1] + self.size / 2, self.size, self.size)

    def is_off_screen_horizontal(self):
        max_x = window.game_size[0] / 2
        return abs(self.position[0]) > max_x 
