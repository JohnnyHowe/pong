
import pygame


class _Speaker:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {
            "ball_hit_paddle": pygame.mixer.Sound("assets/ball_hit_paddle.wav"),
            "ball_hit_wall": pygame.mixer.Sound("assets/ball_hit_wall.wav"),
            "game_over": pygame.mixer.Sound("assets/game_over.wav"),
            "paddle_hit_wall": pygame.mixer.Sound("assets/paddle_hit_wall.wav"),
        }

    def play(self, sound):
        return
        pygame.mixer.Sound.play(self.sounds[sound])


speaker = _Speaker()