from .window import window
from .clock import clock

class Player:

    speed = 6
    last_movement = 0

    def __init__(self, player_input, position=(-6, 0), size=(0.5, 2)):
        self.position = position
        self.size = size
        self.player_input = player_input

    def update(self):
        movement = self.get_desired_movement()
        y_max = (window.get_game_display_rect_no_rotation()[3] - self.size[1]) / 2

        self.position = (
            self.position[0],
            min(max(-y_max, self.position[1] + movement * self.speed * clock.dt_seconds), y_max)
        )

    def draw(self):
        window.draw_rect((
            self.position[0] - self.size[0] / 2,
            self.position[1] + self.size[1] / 2, 
            self.size[0], 
            self.size[1]), 
            (255, 255, 255))
        
    def get_vertical_position_normalized(self):
        """ Normalized between -1 and 1 """
        y_max = (window.get_game_display_rect_no_rotation()[3] - self.size[1]) / 2
        return self.position[1] / y_max


    def get_desired_movement(self):
        return self.player_input.get_movement()