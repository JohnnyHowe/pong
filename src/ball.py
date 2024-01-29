import pygame
from .window import window
from .clock import clock

class Ball:
    size = 0.4

    def __init__(self):
        self.position = [0, 0]
        self.velocity = [1, 0]

    def update(self, paddle_rects):
        if (pygame.key.get_pressed()[pygame.K_r]):
            self.position = [0, 0]

        m = pygame.mouse.get_rel()
        self.position = [self.position[0] + m[0] / 10, self.position[1] - m[1] / 10]

        # self.position[0] += self.velocity[0] * clock.dt_seconds
        # self.position[1] += self.velocity[1] * clock.dt_seconds
        self.process_collisions(paddle_rects)

    def process_collisions(self, paddle_rects):
        for paddle_rect in paddle_rects:
            self.process_collision(paddle_rect)

    def process_collision(self, paddle_rect):
        """ Process the potential collision with paddle_rect 
        Is a basic 2d, axis aligned collision detection and resolution """
        if not self.is_colliding(paddle_rect): return

        overlap_rect = self.get_overlap_rect(paddle_rect)
        window.draw_rect(overlap_rect, (255, 0, 0))
        

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
