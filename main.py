import pygame, sys

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Space Shooter')

clock = pygame.time.Clock()

#game loop
while True:

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick() / 1000

    pygame.display.update()

