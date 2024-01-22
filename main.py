import pygame

if __name__ == "__main__":
    
    pygame.init()
    pygame.display.set_caption("Hello World!")
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()