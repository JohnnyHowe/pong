import math

from .i_player_input import IPlayerInput
from .clock import clock


class AI_Input(IPlayerInput):
    def __init__(self, ball, window_size):
        self.ball = ball
        self.window_size = window_size

    def get_movement(self):
        return math.sin(clock.time_running_seconds * 10)