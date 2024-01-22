import math
import pygame

if __name__ == "__main__":
    
    pygame.init()
    pygame.display.set_caption("Hello World!")
    screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()
    time_running_ms = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        time_running_ms += clock.tick()

        screen.fill((255, 255, 255))

        width = 200 + 25 * math.sin(time_running_ms / 150)
        height = 100 + 25 * math.sin(time_running_ms / 300)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(-width/2 + 400, -height/2 + 300, width, height))

        pygame.display.update()

    pygame.quit()