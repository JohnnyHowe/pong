import pygame

from .game import Game
from .clock import clock
from .window import window
from .menu import Menu

class App:

    def __init__(self):
        self.time_since_last_click_seconds = 1
        self.menu = Menu()
        self.game_running = False

    def run(self):
        while True:
            self.step()

    def step(self):
        clock.tick()
        self.run_event_loop()

        if self.game_running:
            self.game.step()
        else:
            self.menu.step()
            if self.menu.should_start_game():
                self.start_game()

    def start_game(self):
        self.game_running = True
        n_players = self.menu.get_number_of_players()
        if n_players == -1: quit()
        self.game = Game(n_players)
        self.menu = Menu()

    def run_event_loop(self):
        self.time_since_last_click_seconds += clock.dt_seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.VIDEORESIZE:
                window.set_size((event.w, event.h))
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_running = False
                if event.key == pygame.K_F11:
                    window.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (self.time_since_last_click_seconds < 0.2):
                        window.toggle_fullscreen()
                    else:
                        self.time_since_last_click_seconds = 0

