from .window import window
from .clock import clock
from .game_configuration import *
from .easings import *

class Player:

    def __init__(self, player_input, position=(-6, 0), size=(0.5, 2)):
        self.position = list(position)
        self.size = size
        self.player_input = player_input
        self.velocity = [0, 0]
        self.last_movement = 0
        self.speed = 5
        self.target_knock_back = 0;
        self.smoothed_knock_back = 0;

    def update(self):
        self.target_knock_back = lerp(self.target_knock_back, 0, clock.dt_seconds * JUICE_PADDLE_KNOCKBACK_RETURN_LERP_SPEED)
        self.smoothed_knock_back = lerp(self.smoothed_knock_back, self.target_knock_back, clock.dt_seconds * JUICE_PADDLE_KNOCKBACK_RETURN_LERP_SPEED)

        movement = self.get_desired_movement()
        self.velocity[1] = movement * self.speed 

        self.position[0] += self.velocity[0] * clock.dt_seconds
        self.position[1] += self.velocity[1] * clock.dt_seconds

        self.clamp_position()

    def clamp_position(self):
        y_max = (window.get_game_display_rect_no_rotation()[3] - self.size[1]) / 2

        if abs(self.position[1]) > y_max:
            self.velocity[1] = 0

        self.position = [
            self.position[0],
            min(max(-y_max, self.position[1]), y_max)
        ]

    def get_velocity(self):
        return self.velocity

    def draw(self):
        window.draw_rect(self.get_rect(), (255, 255, 255))
        
    def get_vertical_position_normalized(self):
        """ Normalized between -1 and 1 """
        y_max = (window.get_game_display_rect_no_rotation()[3] - self.size[1]) / 2
        return self.position[1] / y_max

    def get_desired_movement(self):
        return self.player_input.get_movement()

    def get_rect(self):
        return (self.position[0] - self.size[0] / 2 + self.smoothed_knock_back, self.position[1] + self.size[1] / 2, self.size[0], self.size[1])
    
    def knock_back(self, knock_back):
        self.target_knock_back = knock_back
        print("knock back", knock_back)