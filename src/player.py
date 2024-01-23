from .window import window
from .clock import clock

class Player:

    speed = 2

    def __init__(self, player_input, position=(-6, 0), size=(0.5, 2)):
        self.position = position
        self.size = size
        self.player_input = player_input

    def update(self):
        movement = self.player_input.get_movement()
        self.position = (
            self.position[0],
            self.position[1] + movement * self.speed * clock.dt_seconds
        )

    def draw(self):
        window.draw_rect((
            self.position[0] - self.size[0] / 2,
            self.position[1] + self.size[1] / 2, 
            self.size[0], 
            self.size[1]), 
            (255, 255, 255))