import pygame, sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))



pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Space Shooter')

clock = pygame.time.Clock()

background_surf = pygame.image.load('./assets/graphics/background.png').convert_alpha()

spaceship_group = pygame.sprite.Group()
ship = Ship(spaceship_group)

#game loop
while True:

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #delta
    dt = clock.tick() / 1000

    #graphics
    display_surface.blit(background_surf, (0, 0))
    spaceship_group.draw(display_surface)

    #draw frame
    pygame.display.update()

