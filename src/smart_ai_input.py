import math

from .i_player_input import IPlayerInput
from .clock import clock
from.window import window


class Smart_AI_Input(IPlayerInput):
    def __init__(self, ball, game_size):
        self.ball = ball
        self.game_size = game_size
        self.paddle = None

    def get_movement(self):
        threshold = 0.1
        d_y = self.get_target_position() - self.paddle.position[1]
        if d_y < -threshold:
            return -1
        elif d_y > threshold:
            return 1
        return 0

    def get_target_position(self):
        side_ball_is_on = -1 if self.ball.position[0] < self.paddle.position[0] else 1
        ball_heading_to_self = self.ball.velocity[0] * side_ball_is_on < 0
        if not ball_heading_to_self: return 0
        return self.get_projected_ball_intersection_with_self_x()

    def get_projected_ball_intersection_with_self_x(self):
        side_ball_is_on = -1 if self.ball.position[0] < self.paddle.position[0] else 1
        target_x = self.paddle.position[0] + (self.ball.size + self.paddle.size[0]) / 2 * side_ball_is_on
        raw_intersection = get_intersection(self.ball.position, self.ball.velocity, (target_x, 0), [0, 1])

        max_y = (self.game_size[1] - self.ball.size) / 2
        normalized_raw_intersection_y = raw_intersection[1] / max_y
        normalized_intersection_y = normalized_raw_intersection_y

        while normalized_intersection_y > 1: normalized_intersection_y -= 2
        while normalized_intersection_y < -1: normalized_intersection_y += 2

        n_bounces = abs(round_to_even(normalized_raw_intersection_y) / 2)
        if n_bounces % 2 == 1: normalized_intersection_y = -normalized_intersection_y
        intersection_y = normalized_intersection_y * max_y

        return intersection_y


def get_intersection(line1_point, line1_direction, line2_point, line2_direction):
    """ Modified from https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines """
    line1_point2 = [line1_point[0] + line1_direction[0], line1_point[1] + line1_direction[1]]
    line2_point2 = [line2_point[0] + line2_direction[0], line2_point[1] + line2_direction[1]]
    line1 = [line1_point, line1_point2]
    line2 = [line2_point, line2_point2]

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0: return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def round_to_even(n):
    return round(n / 2) * 2