import math
import pygame
from .window import Window

class Game:

    def __init__(self):
        clock = pygame.time.Clock()
        time_running_ms = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    Window.set_size((event.w, event.h))
            time_running_ms += clock.tick()

            Window._screen.fill((255, 255, 255))
            Window.draw_screen_gizmos()
            Window.fill_undefined_area((100, 100, 100))

            width = 200 + 25 * math.sin(time_running_ms / 150)
            height = 100 + 25 * math.sin(time_running_ms / 300)
            pygame.draw.rect(Window._screen, (255, 0, 0), pygame.Rect(-width/2 + 400, -height/2 + 300, width, height))

            width = 2.0 + .5 * math.sin(time_running_ms / 150)
            height = 1.0 + .25 * math.sin(time_running_ms / 300)
            Window.draw_rect((
                -3 - width / 2,
                -2 + height / 2, 
                width, 
                height), 
                (0, 0, 255))

            pygame.display.update()

        pygame.quit()

    def run(self):
        pass