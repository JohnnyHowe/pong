import math

from .i_player_input import IPlayerInput
from .clock import clock


class AI_Input(IPlayerInput):
    def __init__(self, ball, window_size):
        self.ball = ball
        self.window_size = window_size
        self.paddle = None

    def get_movement(self):
        threshold = 0.1
        d_y = self.ball.position[1] - self.paddle.position[1]

        if d_y < -threshold:
            return -1
        elif d_y > threshold:
            return 1
        return 0